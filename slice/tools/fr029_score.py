"""FR-029 V1 scorer: compare one run's result.json with an independent gold file (format fr029-gold-v1).

    python slice/tools/fr029_score.py --result OUT/result.json --gold GOLD.json [--json]

Existence is scored per kind (route, model, http call, file role, limitation) as TP/FP/FN. Attributes are scored only
on matched items, one counter per attribute, so a wrong prefix and a wrong `required` are reported separately.
An `unknown` value never counts as correct: when the gold accepts it, it is counted as `acceptable_unknown`.
Matching is one-to-one: of several facts with one key, the best one matches and the others are extra (FP).
A kind the gold does not list is `not_evaluated`. Each report carries a verdict per fact id, so other measures
(the `exact` error rate) use the same matching. The scorer reads output files only; it never runs the analysis.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def _known(fv):
    return isinstance(fv, dict) and fv.get("state") == "known"


def _val(fv):
    return fv["value"] if _known(fv) else None


def _route_path(path):
    """One endpoint, one key: {p:path} (source form) and {p} (OpenAPI form) are the same path."""
    return re.sub(r"\{(\w+):\w+\}", r"{\1}", path) if isinstance(path, str) else path


def _pname(name, place):
    """HTTP header names are case-insensitive (RFC 9110); other parameter names are compared as written."""
    return name.lower() if place == "header" and isinstance(name, str) else name


FORMAT_NAMES = {"uuid": "uuid", "date": "date", "date-time": "datetime", "email": "email"}


def type_text(schema, names: dict) -> str | None:
    if not isinstance(schema, dict):
        return None
    if "x-model-fact" in schema:
        return names.get(schema["x-model-fact"], "?")
    if schema.get("type") == "string" and schema.get("format"):
        # gold notation 7.3 names uuid/date/datetime/email; other formats (binary, uri, time) are written as string
        return FORMAT_NAMES.get(schema["format"], "string")
    if "anyOf" in schema:  # a nullable parameter: compare the base type; nullability is scored elsewhere
        return type_text(next((s for s in schema["anyOf"] if s.get("type") != "null"), {}), names)
    if schema.get("type") == "array":
        inner = type_text(schema.get("items", {}), names)
        return f"array[{inner}]"
    if "type" in schema:
        return schema["type"]
    return "any" if not schema else None


def _inline_fields(inline, names) -> list:
    if not inline:
        return []
    return sorted((x["name"], type_text(_val(x["schema"]), names), _val(x["required"])) for x in inline["fields"])


def from_result(result: dict) -> dict:
    facts = result["facts"]
    models = {f["id"]: f for f in facts if f["kind"] == "model"}
    names = {i: _val(f["attributes"]["name"]) for i, f in models.items()}
    files = {i: _val(f["attributes"]["declared_in"]) for i, f in models.items()}
    out = {"routes": [], "models": [], "http_calls": [], "file_roles": [], "limitations": []}
    normal_files = {p for c in result.get("components", []) if c.get("kind", "normal") == "normal" for p in c["files"]}
    for f in facts:
        a = f["attributes"]
        if f["kind"] == "route":
            ev = f["evidence"][0]
            params = None
            if _known(a.get("parameters")):
                params = sorted((_pname(_val(p["name"]), _val(p.get("in"))), _val(p.get("in")),
                                 type_text(_val(p.get("schema")), names), _val(p.get("required")))
                                for p in a["parameters"]["value"])
            bodies = _val(a.get("bodies")) or []
            req = [b for b in bodies if b["direction"] == "request"]
            inline = _val(a.get("request_inline"))
            form = inline if inline and not req else None
            resp = [b for b in bodies if b["direction"] == "response"]
            out["routes"].append({
                "fact_id": f["id"],
                "key": (_val(a["method"]), _route_path(_val(a.get("path"))), f"{ev['path']}:{ev['start_line']}"),
                "handler": _val(a.get("handler")),
                "params": params,
                "request_body": ([], form["media_type"], _val(form["required"]), False, _inline_fields(form, names)) if form else
                None if not req and _known(a.get("request_model_ids")) else (
                    (sorted(names[b["model_id"]] for b in req), req[0]["media_type"], req[0]["required"],
                     bool(_val(a.get("request_body_embedded"))), _inline_fields(inline, names)) if req else "unknown"),
                "response": _type_response(type_text(_val(a["response_type"])["schema"], names), False)
                if _known(a.get("response_type")) else
                None if not resp and _known(a.get("response_model_ids")) else (
                    (names[resp[0]["model_id"]], files[resp[0]["model_id"]], bool(resp[0].get("array"))) if resp else "unknown"),
                "status": _val(a.get("status_codes"))})
        elif f["kind"] == "model":
            fields = sorted((_val(x["name"]), _val(x.get("alias")), type_text(_val(x.get("type")), names),
                             _val(x.get("required")), _val(x.get("nullable"))) for x in (_val(a["fields"]) or []))
            out["models"].append({"fact_id": f["id"], "key": (files[f["id"]], names[f["id"]]), "fields": fields})
        elif f["kind"] == "http_call":
            ev = f["evidence"][0]
            target = ("literal", _val(a["url"])) if _known(a.get("url")) else (
                ("config", _val(a["url_config_key"])) if _known(a.get("url_config_key")) else ("unknown", None))
            out["http_calls"].append({"fact_id": f["id"], "key": f"{ev['path']}:{ev['start_line']}",
                                      "span": (ev["path"], ev["start_line"], ev.get("end_line") or ev["start_line"]),
                                      "library": _val(a["library"]),
                                      "method": _val(a.get("method")) or "unknown", "target": target})
        elif f["kind"] == "file_role":
            if _val(f["attributes"]["file"]) not in normal_files:
                continue  # FR-029 lists roles only for components of kind normal; others never reach the README
            ev = f["evidence"][0] if f["evidence"] else None
            out["file_roles"].append({"fact_id": f["id"], "key": _val(a["file"]), "role": _val(a["role"]),
                                      "label": f["confidence"], "line": ev["start_line"] if ev else None})
    for x in result["limitations"]:
        if x["code"] in ("ROUTE_NOT_DECORATOR", "HTTP_LIBRARY_UNSUPPORTED") and x.get("where"):
            kind = x["message"].split(" ", 1)[0]
            out["limitations"].append({"key": (kind, x["where"])})
    return out


def from_gold(gold: dict) -> dict:
    out = {"routes": [], "models": [], "http_calls": [], "file_roles": [], "limitations": []}
    alt_names = {(m["file"], m["name"]): m.get("alt_names", []) for m in gold.get("models", [])}
    for r in gold.get("routes", []):
        rb = r.get("request_body")
        resp = r.get("response")
        out["routes"].append({
            # a response model the gold also accepts under another name (Model.alt_names) is the same answer
            "alt_responses": [(n, resp.get("model_file"), bool(resp.get("array")))
                              for n in alt_names.get((resp.get("model_file"), resp["model"]), [])]
            if resp and "model" in resp else [],
            "key": (r["method"], _route_path(r.get("path")), r["declared_at"]),
            "handler": r.get("handler"),
            "params": sorted((_pname(p["name"], p["in"]), p["in"], p["type"], p["required"]) for p in r.get("params", [])),
            "request_body": None if rb is None else (sorted(rb["models"]), rb["media_type"], rb["required"], bool(rb.get("embedded")),
                                                     sorted((x["name"], x["type"], x["required"]) for x in rb.get("fields", []))),
            "response": None if resp is None else (
                (resp["model"], resp.get("model_file"), bool(resp.get("array"))) if "model" in resp
                else _type_response(resp["type"], bool(resp.get("array")))),
            "status": r.get("status")})
    for m in gold.get("models", []):
        out["models"].append({"key": (m["file"], m["name"]),
                              "alt_keys": [(m["file"], n) for n in m.get("alt_names", [])],
                              "fields": sorted((f["name"], f.get("alias"), f["type"], f["required"], f["nullable"])
                                               for f in m["fields"]),
                              # alternatives the gold accepts: other types per field; any unknown fields for a
                              # model created at runtime
                              "alt_types": {f["name"]: f.get("alt_types", []) for f in m["fields"]},
                              "unknown_ok": bool((m.get("dynamic") or {}).get("unknown_fields_acceptable"))})
    for h in gold.get("http_calls", []):
        t = h["target"]
        alt = h.get("accept_alt_target")
        out["http_calls"].append({"key": h["where"], "library": h["library"], "method": h["method"],
                                  "alt_methods": h.get("alt_methods", []),
                                  "alt_keys": list(h.get("alt_where", [])),
                                  "alt_targets": [(alt["kind"], alt.get("value") if alt["kind"] != "unknown" else None)]
                                  if isinstance(alt, dict) else [],
                                  "target": (t["kind"], t.get("value") if t["kind"] != "unknown" else None)})
    for x in gold.get("file_roles", []):
        out["file_roles"].append({"key": x["file"], "role": x["role"], "alt_roles": x.get("alt_roles", []),
                                  "optional": bool(x.get("optional")),
                                  "label": x.get("label"),
                                  "line": [x.get("line"), *x.get("alt_lines", [])]})
    for x in gold.get("limitations", []):
        out["limitations"].append({"key": (x["kind"], x["where"]),
                                   "alt_keys": [(x["kind"], wh) for wh in x.get("alt_where", [])]})
    return out


def _type_response(t: str | None, array: bool) -> tuple:
    """A response that is a type, not a model: ("type", base type, array depth), the same way for tool and gold."""
    t = t or "any"
    depth = int(array)
    while t.startswith("array[") and t.endswith("]"):
        t, depth = t[6:-1], depth + 1
    return ("type", t, depth)


def _fields_ok(got: list, want: dict) -> str:
    """"correct", "wrong", or "unknown" when the gold accepts unknown fields of a model created at runtime.
    The alternative types the gold lists are accepted. An empty table is never counted as solved."""
    if want.get("unknown_ok") and all(f[2] is None for f in got):
        return "unknown"
    if [f[0] for f in got] != [f[0] for f in want["fields"]]:
        return "wrong"
    for g, w in zip(got, want["fields"]):
        types = [w[2], *want["alt_types"].get(w[0], [])]
        if g[1] != w[1] or g[2] not in types or g[3] != w[3] or g[4] != w[4]:
            return "wrong"
    return "correct"


ATTRS = {"routes": ["handler", "params", "request_body", "response", "status"], "models": ["fields"],
         "http_calls": ["library", "method", "target"], "file_roles": ["role", "label", "line"], "limitations": []}
ALTS = {("http_calls", "target"): "alt_targets", ("http_calls", "method"): "alt_methods",
        ("file_roles", "role"): "alt_roles", ("routes", "response"): "alt_responses"}


def _unknown(attr: str, v) -> bool:
    if attr in ("request_body", "response"):  # None there means "no body" / "no model", which is known
        return v == "unknown"
    return v is None or v == "unknown" or (isinstance(v, tuple) and len(v) > 0 and v[0] == "unknown")


def _verdict(kind: str, attr: str, g: dict, w: dict) -> str:
    """One attribute of one matched item: "correct", "unknown" (accepted by the gold, not solved) or "wrong"."""
    if kind == "file_roles" and attr == "line":
        # gold line null (role Khác): any line of the file is fine, but the tool must cite one
        ok = g["line"] is not None if w["line"][0] is None else g["line"] in w["line"]
        return "correct" if ok else "wrong"
    if kind == "models" and attr == "fields":
        return _fields_ok(g["fields"], w)
    if g[attr] not in [w[attr], *w.get(ALTS.get((kind, attr)), [])]:
        return "wrong"
    return "unknown" if _unknown(attr, g[attr]) else "correct"


def score(result: dict, gold: dict) -> dict:
    got, want = from_result(result), from_gold(gold)
    report = {}
    for kind, attrs in ATTRS.items():
        if kind not in gold:
            report[kind] = {"status": "not_evaluated", "reason": "Gold không có mục này"}
            continue
        w = {x["key"]: x for x in want[kind]}
        alias = {a: x["key"] for x in want[kind] for a in x.get("alt_keys", [])}  # alternatives the gold accepts
        groups = {}
        for x in got[kind]:
            k = alias.get(x["key"], x["key"])
            if k not in w and x.get("span"):  # an evidence range that holds the gold call line (or its alternative)
                path, start, end = x["span"]
                k = next((alias.get(c, c) for c in [*w, *alias] if isinstance(c, str) and c.rpartition(":")[0] == path
                          and c.rpartition(":")[2].isdigit() and start <= int(c.rpartition(":")[2]) <= end), k)
            groups.setdefault(k, []).append(x)
        g, extra = {}, []  # one-to-one: the best fact of a key matches, the others are extra; order does not matter
        for k, xs in groups.items():
            if k in w:
                xs = sorted(xs, key=lambda x: (sum(_verdict(kind, a, x, w[k]) == "wrong" for a in attrs),
                                               str(x.get("fact_id"))))
                g[k] = xs[0]
                extra += xs[1:]
            else:
                extra += xs
        accepted = []
        if kind == "limitations":  # extra items the gold says are not wrong (an SDK listed as unsupported HTTP)
            ok_kinds = {x["kind"] for x in gold.get("accept_extra_limitations", [])}
            accepted = [x for x in extra if x["key"][0] in ok_kinds]
            extra = [x for x in extra if x["key"][0] not in ok_kinds]
        tp = sorted(g, key=str)
        fn = sorted((k for k in set(w) - set(g) if not w[k].get("optional")), key=str)  # optional: not a miss
        facts = {x["fact_id"]: "wrong" for x in extra if x.get("fact_id")}
        attr = {}
        for a in attrs:
            v = {k: _verdict(kind, a, g[k], w[k]) for k in tp}
            bad = [k for k in tp if v[k] == "wrong"]
            for k in bad:
                if g[k].get("fact_id"):
                    facts[g[k]["fact_id"]] = "wrong"
            attr[a] = {"correct": sum(x == "correct" for x in v.values()),
                       "acceptable_unknown": sum(x == "unknown" for x in v.values()),
                       "wrong": [{"key": str(k), "got": g[k][a], "want": w[k][a]} for k in bad]}
        for k in tp:
            if g[k].get("fact_id"):
                facts.setdefault(g[k]["fact_id"], "ok")
        n = len(tp)
        report[kind] = {"tp": n, "fp": len(extra), "fn": len(fn),
                        "precision": n / (n + len(extra)) if n + len(extra) else None,
                        "recall": n / (n + len(fn)) if n + len(fn) else None,
                        "false_positive": sorted((str(x["key"]) + (" (trùng)" if alias.get(x["key"], x["key"]) in g else "")
                                                  for x in extra), key=str),
                        "false_negative": [str(k) for k in fn], "attributes": attr, "facts": facts,
                        "accepted_extra": len(accepted)}
    if "out_of_scope" in gold:
        counts = {}
        for x in result["coverage"]["not_readable"]:
            counts[x["scope"]] = counts.get(x["scope"], 0) + 1
        want_counts = {k: v for k, v in gold["out_of_scope"].items() if v}  # a zero count equals an absent key
        report["out_of_scope"] = {"ok": counts == want_counts, "got": counts, "want": gold["out_of_scope"]}
    return report


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--result", type=Path, required=True)
    p.add_argument("--gold", type=Path, required=True)
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    rep = score(json.loads(a.result.read_text(encoding="utf-8")), json.loads(a.gold.read_text(encoding="utf-8")))
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2, default=str))
        return 0
    for kind, r in rep.items():
        if kind == "out_of_scope":
            print(f"out_of_scope: {'đúng' if r['ok'] else 'sai'} — có {r['got']}, cần {r['want']}")
            continue
        if r.get("status") == "not_evaluated":
            print(f"{kind}: not_evaluated — {r['reason']}")
            continue
        print(f"{kind}: TP {r['tp']} FP {r['fp']} FN {r['fn']}")
        for k in r["false_positive"]:
            print(f"  thừa: {k}")
        for k in r["false_negative"]:
            print(f"  thiếu: {k}")
        for name, x in r["attributes"].items():
            unknown = f", unknown chấp nhận {x['acceptable_unknown']}" if x["acceptable_unknown"] else ""
            print(f"  {name}: đúng {x['correct']}/{r['tp']}{unknown}")
            for w in x["wrong"]:
                print(f"    sai {w['key']}: có {w['got']} — cần {w['want']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
