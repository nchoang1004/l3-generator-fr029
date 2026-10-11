"""Score the FR-029 agent flow on the approved golden v1 answers for 4 real repos (APPROVAL-golden-v1-2026-10-04).

    python slice/tools/fr029_golden4.py --golden-repo D:/VSF/l3-generator-golden-v2 --repos teamhide-fastapi-boilerplate ...
        --out DIR --model M --key-env ENV [--api responses] [--price IN CACHED OUT] [--max-cost-usd X]

Golden v1 records routes (method, full path, handler, request/response model names) and external calls; it has no
parameters, model fields or file roles, so only those parts are scored here. Routes match on (method, path, handler);
a gold path holding the `{prefix}` placeholder (prefix read from configuration outside the old scope) matches an
unknown path or the path with the prefix resolved. Audited corrections (ERRATA) are applied to a copy of the gold
before scoring and listed in the result. Model names are compared on matched routes. HTTP calls: only system_kind http_api made with the three
libraries FR-029 covers; a tool call matches one gold call when its line lies in the gold span (one-to-one). Other
http_api entries (OAuth client constructors, SDKs) are counted as out_of_scope, never as misses.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from l3slice import snapshot  # noqa: E402
from l3slice.docagent import Budget, OpenAICompatProvider, ResponsesProvider  # noqa: E402
from l3slice.docpipeline import run_documents  # noqa: E402

REPOS = {  # golden folder -> (approved answer, source folder under sample-repos, role in the approval)
    "teamhide-fastapi-boilerplate": ("final-r3.json", "teamhide_fastapi-boilerplate-df4e6d4", "đo"),
    "fastapi_best_architecture": ("final-r2.json", "fastapi-practices_fastapi_best_architecture-123a44a", "đo"),
    "full-stack-fastapi-template": ("final-r2.json", "full-stack-fastapi-template-cb740b6", "chỉnh prompt"),
    "igorbenav-FastAPI-boilerplate": ("final-r3.json", "fastapi-boilerplate", "chỉnh prompt"),
}


HTTP_LIBRARIES = {"httpx", "requests", "aiohttp"}  # FR-029 AC-08
PLACEHOLDERS = ("{prefix}",)  # golden v1 marks a prefix it could not resolve statically
PY_NAMES = {"boolean": "bool", "integer": "int", "string": "str", "number": "float", "any": "Any", "object": "dict"}


# Values of the approved golden v1 that the 07/10/2026 audit found wrong against the source (two reviewers: the
# golden-v1-large Claude agent and the main session, each reading the cited lines). The approved files stay unchanged;
# scoring applies these corrections and records it. `before` must match, so a correction never lands on another value.
ERRATA = {
    "igorbenav-FastAPI-boilerplate": [
        {"route": ("DELETE", "backend/src/modules/api_keys/routes.py::delete_api_key"), "field": "response_model",
         "before": "None", "after": None, "why": "routes.py:198 `-> None`: no response model; the string 'None' is not a class"},
        {"route": ("GET", "backend/src/infrastructure/app_factory.py::get_swagger_documentation"), "field": "response_model",
         "before": "fastapi.responses.HTMLResponse", "after": None,
         "why": "app_factory.py:314 `-> HTMLResponse`: a Response subclass is not a response model in FastAPI"},
        {"route": ("GET", "backend/src/infrastructure/app_factory.py::get_redoc_documentation"), "field": "response_model",
         "before": "fastapi.responses.HTMLResponse", "after": None, "why": "app_factory.py:318, same as /docs"},
    ],
    "fastapi_best_architecture": [
        {"route": ("GET", "backend/app/admin/api/v1/sys/plugin.py::download_plugin"), "field": "response_model",
         "before": "StreamingResponse", "after": None,
         "why": "sys/plugin.py:68 `-> StreamingResponse`: a Response subclass is not a response model"},
        {"route": ("WEBSOCKET", "backend/common/socketio/server.py::connect"), "drop": True,
         "why": "server.py:32 `@sio.event`: a python-socketio handler, not a FastAPI/APIRouter route (FR-029)"},
    ],
}


def apply_errata(name: str, gold: dict, check: bool = True) -> dict:
    """A copy of the gold with the audited corrections of ERRATA[name]; with check, every correction must apply."""
    fixed = json.loads(json.dumps(gold))
    done = []
    for e in ERRATA.get(name, []):
        hits = [r for r in fixed["routes"] if (r["method"], r["handler"]) == e["route"]]
        if e.get("drop"):
            fixed["routes"] = [r for r in fixed["routes"] if (r["method"], r["handler"]) != e["route"]]
        for r in hits if not e.get("drop") else []:
            if r.get(e["field"]) == e["before"]:
                r[e["field"]] = e["after"]
            else:
                hits = []
        if hits:
            done.append(e)
        elif check:
            raise ValueError(f"{name}: errata {e['route']} không khớp gold")
    fixed["errata_applied"] = [{"route": list(e["route"]), "why": e["why"]} for e in done]
    return fixed


def _short(name):
    """Compare model names the way golden v1 writes them: class name only, list[...] kept; dict[...] is dict."""
    if not name:
        return None
    if name.startswith("list[") and name.endswith("]"):
        return f"list[{_short(name[5:-1])}]"
    if name.lower().startswith("dict"):
        return "dict"
    return name.rsplit("::", 1)[-1].rsplit(".", 1)[-1]


def _placeholder_rx(path: str):
    """`{prefix}` stands for a prefix golden v1 did not resolve: any run of literal segments, or none."""
    if not any(p in path for p in PLACEHOLDERS):
        return None
    rx = re.escape(path)
    for p in PLACEHOLDERS:
        rx = rx.replace(re.escape(p), r"(?:/[^/{}]+)*")
    return re.compile(rx)


def _arg_name(schema, models: dict) -> str:
    """Name of one argument of a generic response model, as golden v1 writes it (Page[Item], Page[list[Item]])."""
    if "x-model-fact" in schema:
        return models.get(schema["x-model-fact"], "?")
    if "x-external-model" in schema:  # library generic: PaginatedListResponse[APIKeyRead]
        args = ", ".join(_arg_name(t, models) for t in schema.get("x-type-args", []))
        return schema["x-external-model"].rsplit(".", 1)[-1] + (f"[{args}]" if args else "")
    if schema.get("type") == "array":
        return f"list[{_arg_name(schema.get('items', {}), models)}]"
    return _type_name(schema)


def _type_name(schema) -> str:
    if schema.get("type") == "array":
        return f"list[{_type_name(schema.get('items', {}))}]"
    return PY_NAMES.get(schema.get("type") or "any", schema.get("type") or "Any")


def compare(result: dict, gold: dict) -> dict:
    models = {f["id"]: f["attributes"]["name"]["value"] for f in result["facts"] if f["kind"] == "model"}
    ours, ids = {}, {}  # ids: route key -> fact ids (a second fact with the same key is an extra, wrong one)
    for f in result["facts"]:
        if f["kind"] != "route":
            continue
        a = f["attributes"]
        key = (a["method"]["value"], a["path"]["value"] if a["path"]["state"] == "known" else None, a["handler"]["value"])
        req = [models.get(i) for i in a["request_model_ids"]["value"]] if a["request_model_ids"]["state"] == "known" else "unknown"
        resp = [models.get(i) for i in a["response_model_ids"]["value"]] if a["response_model_ids"]["state"] == "known" else "unknown"
        bodies = (a.get("bodies") or {}).get("value", [])
        arrays = {b["model_id"] for b in bodies if b.get("array")}
        generic = {b["model_id"]: ", ".join(_arg_name(t, models) for t in b["type_args"]) for b in bodies if b.get("type_args")}
        if resp != "unknown":
            resp = [(lambda n: f"list[{n}]" if i in arrays else n)(f"{models.get(i)}[{generic[i]}]" if i in generic else models.get(i))
                    for i in a["response_model_ids"]["value"]]
            if not resp and a.get("response_type", {}).get("state") == "known":
                resp = [_arg_name(a["response_type"]["value"]["schema"], models)]
        ours[key] = (req, resp)
        ids.setdefault(key, []).append(f["id"])
    want = {(r["method"], None if _placeholder_rx(r["path"] or "") else r["path"], r["handler"]):
            (r.get("request_model"), r.get("response_model")) for r in gold["routes"]}
    open_prefix = [(r["method"], r["handler"], _placeholder_rx(r["path"])) for r in gold["routes"]
                   if _placeholder_rx(r["path"] or "")]
    for key in [k for k in ours if k not in want and k[1]]:  # a resolved prefix matches the placeholder too
        hit = next(((m, None, h) for m, h, rx in open_prefix
                    if (m, h) == (key[0], key[2]) and rx.fullmatch(key[1]) and (m, None, h) not in ours), None)
        if hit:
            ours[hit] = ours.pop(key)
            ids[hit] = ids.pop(key)
    tp = sorted(set(ours) & set(want), key=str)
    model_wrong = []
    for k in tp:
        (req, resp), (wreq, wresp) = ours[k], want[k]
        got_req = None if req == [] else (req if req == "unknown" else req[0])
        got_resp = None if resp == [] else (resp if resp == "unknown" else resp[0])
        if (_short(got_req) if got_req != "unknown" else got_req) != _short(wreq) or \
                (_short(got_resp) if got_resp != "unknown" else got_resp) != _short(wresp):
            model_wrong.append({"route": str(k), "got": [got_req, got_resp], "want": [wreq, wresp]})
    calls = [x for x in gold["external_calls"] if x["system_kind"] == "http_api"]
    left = [x for x in calls if x.get("library") in HTTP_LIBRARIES]
    http_tp, http_fp = 0, []
    wrong_routes = {w["route"] for w in model_wrong}
    facts = {}  # verdict per fact id, so the `exact` error rate uses this same matching
    for key, fids in ids.items():
        facts[fids[0]] = "ok" if key in want and str(key) not in wrong_routes else "wrong"
        facts.update({i: "wrong" for i in fids[1:]})
    for fid, path, line in sorted((f["id"], f["evidence"][0]["path"], f["evidence"][0]["start_line"])
                                  for f in result["facts"] if f["kind"] == "http_call"):
        hit = next((x for x in left if x["file"] == path and x["line_from"] <= line <= x.get("line_to", x["line_from"])), None)
        if hit:
            left.remove(hit)
            http_tp += 1
        else:
            http_fp.append(f"{path}:{line}")
        facts[fid] = "ok" if hit else "wrong"
    return {"routes": {"tp": len(tp), "fp": sorted(map(str, set(ours) - set(want))), "fn": sorted(map(str, set(want) - set(ours)))},
            "models_on_matched_routes": {"correct": len(tp) - len(model_wrong), "wrong": model_wrong},
            "http_api": {"tp": http_tp, "fp": http_fp, "fn": sorted(f"{x['file']}:{x['line_from']}" for x in left),
                         "out_of_scope": len(calls) - len([x for x in calls if x.get("library") in HTTP_LIBRARIES])},
            "facts": facts}


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--golden-repo", type=Path, required=True)
    p.add_argument("--repos", nargs="+", default=list(REPOS))
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--base-url", default="https://api.openai.com/v1")
    p.add_argument("--api", choices=["chat", "responses"], default="responses")
    p.add_argument("--model", required=True)
    p.add_argument("--key-env", required=True)
    p.add_argument("--reasoning-effort", default="medium")
    p.add_argument("--price", type=float, nargs=3)
    p.add_argument("--max-cost-usd", type=float)
    p.add_argument("--max-turns", type=int, default=400)
    p.add_argument("--max-context-chars", type=int, default=150_000,
                   help="Rút gọn kết quả cũ khi lịch sử vượt mức này; dữ kiện đã nộp vẫn còn trong sổ")
    a = p.parse_args(argv)
    if a.out.exists() and any(a.out.iterdir()):
        print("Thư mục --out phải mới hoặc rỗng", file=sys.stderr)
        return 2
    a.out.mkdir(parents=True, exist_ok=True)
    cls = ResponsesProvider if a.api == "responses" else OpenAICompatProvider
    provider = cls(a.base_url, a.model, a.key_env, max_output_tokens=16000, reasoning_effort=a.reasoning_effort,
                   prices=tuple(a.price) if a.price else None)
    rows = []
    for name in a.repos:
        answer, src_dir, role = REPOS[name]
        gold = apply_errata(name, json.loads((a.golden_repo / ".aide/evidence/tests/golden-v1" / name / answer)
                                             .read_text(encoding="utf-8")))
        src = a.golden_repo / "sample-repos" / src_dir
        snap, _ = snapshot.take(src)
        membership = a.out / f"{name}.membership.json"
        membership.write_text(json.dumps({"partition_version": "fixture-membership-v1", "components": [
            {"name": "Toàn bộ", "kind": "normal", "files": [f["path"] for f in snap["files"]
                                                          if f["path"].endswith(".py") and f["byte_size"]]},
            {"name": "Khác", "kind": "other", "files": [f["path"] for f in snap["files"]
                                                        if not (f["path"].endswith(".py") and f["byte_size"])]}]}),
            encoding="utf-8")
        cost_before = provider.cost_usd
        row = {"repo": name, "role": role, "gold_routes": len(gold["routes"])}
        try:
            bundle = run_documents(src, a.out / name, membership, name, provider, budget=Budget(
                max_turns=a.max_turns, max_tokens=60_000_000, max_seconds=4 * 3600, max_context_chars=a.max_context_chars,
                max_cost_usd=a.max_cost_usd), run_id=f"golden4_{name}")
        except Exception as exc:  # recorded, never hidden
            row.update(status="failed", error=f"{type(exc).__name__}: {exc}"[:300])
        else:
            result = {k: v for k, v in bundle.items() if k != "artifacts"}
            row.update(status=bundle["agent"]["status"], reason=bundle["agent"]["reason"], turns=bundle["agent"]["turns"],
                       coverage_complete=bundle["coverage"]["complete"], cost_usd=round(provider.cost_usd - cost_before, 4),
                       score=compare(result, gold))
        rows.append(row)
        s = row.get("score", {}).get("routes", {})
        print(f"{name}: {row['status']} routes TP {s.get('tp')} FP {len(s.get('fp', []))} FN {len(s.get('fn', []))} "
              f"cost {row.get('cost_usd')}", file=sys.stderr, flush=True)
        (a.out / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
