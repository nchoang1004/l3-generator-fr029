"""CMP-008: result.json, manifest, README, Mermaid, SVG, API/TBL/EVT files, checks, publish and retry (API-008).

SVG is drawn here from the same plan as the Mermaid source (no Node.js, no browser, no script in the output).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from .common import SCHEMA_VERSION, is_known, sha

RENDERER_VERSION = "slice-render-v3"
TEMPLATE_VERSION = "slice-template-v1"
MAX_PATH_WINDOWS = 260
RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
DDL_TYPES = {"sqlite": {"INTEGER", "REAL", "TEXT", "BLOB"},
             "postgresql": {"SMALLINT", "INTEGER", "BIGINT", "REAL", "DOUBLE PRECISION", "BOOLEAN", "TEXT", "BYTEA",
                            "DATE", "TIMESTAMP WITHOUT TIME ZONE", "TIMESTAMP WITH TIME ZONE"}}
OPENAPI_METHODS = {"GET", "PUT", "POST", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"}


class ExportError(ValueError):
    def __init__(self, code: str, reason: str):
        super().__init__(f"{code}: {reason}")
        self.code = code


# ---------- names (API-008 §4) ----------

def slug(name: str, empty: str) -> str:
    text = unicodedata.normalize("NFKD", name.replace("Đ", "D").replace("đ", "d"))
    text = "".join(ch for ch in text if not unicodedata.combining(ch)).upper()
    out = "".join(ch if "A" <= ch <= "Z" or "0" <= ch <= "9" else "-" for ch in text)
    out = "-".join(part for part in out.split("-") if part) or empty
    if out in RESERVED:
        out = "X-" + out
    if len(out) > 64:
        out = out[:47] + "-" + sha(name.encode())[:16]
    return out


def unique_slugs(items: list[tuple[str, str]], empty: str) -> dict[str, str]:
    """items = (stable key, display name) in tie-break order; suffix -2, -3 ... on case-folded clashes."""
    used, result = set(), {}
    for key, name in items:
        base = slug(name, empty)
        candidate, n = base, 1
        while candidate.casefold() in used:
            n += 1
            suffix = f"-{n}"
            candidate = base[:64 - len(suffix)].rstrip("-") + suffix  # API-008 §4: cut the base, keep 64
        used.add(candidate.casefold())
        result[key] = candidate
    return result


# ---------- text helpers ----------

def md(text) -> str:
    s = str(text).replace("\r", " ").replace("\n", " ")
    return s.replace("|", "\\|").replace("`", "\\`").replace("<", "&lt;").replace(">", "&gt;")


def code(text) -> str:
    """A Markdown code span that shows the text as written: no HTML escaping inside; only the table pipe is escaped."""
    s = str(text).replace("\r", " ").replace("\n", " ").replace("|", "\\|")
    return f"`` {s} ``" if "`" in s else f"`{s}`"


def cell(field) -> str:
    if field is None:
        return "unknown — trường không có trong dữ kiện"
    state = field["state"]
    if state == "known":
        value = field["value"]
        if isinstance(value, list):
            return md(", ".join(map(str, value))) if value else "(rỗng)"
        if isinstance(value, dict):
            return md(json.dumps(value, ensure_ascii=False, sort_keys=True))
        return md(value)
    label = {"unknown": "unknown", "redacted": "đã che", "not_applicable": "không áp dụng"}[state]
    return f"{label} — {md(field['reason'])}"


def frontmatter(values: dict) -> str:
    lines = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in values.items()] + ["---", ""]
    return "\n".join(lines)


def dump(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def notice(code, reason, fact_ids, field_paths, artifact_path):
    return {"code": code, "reason": reason, "fact_ids": sorted(fact_ids), "field_paths": sorted(field_paths),
            "artifact_path": artifact_path}


# ---------- API (API-008 §5) ----------

def _row_label(fact, owner_comp):
    conf = "inferred" if fact["confidence"] == "inferred" or owner_comp["confidence"] == "inferred" else "exact"
    comp = "partial" if fact["completeness"] == "partial" or owner_comp["completeness"] == "partial" else "full"
    return conf, comp


def _unknowns(fact):
    return [{"field": k, "reason": v["reason"]} for k, v in sorted(fact["attributes"].items())
            if v["state"] in ("unknown", "redacted")]


def ev_cell(evidence: list[dict], link: dict | None) -> str:
    """Evidence IDs with `path:line` (API-008 §4). A web link only when repository URL + commit are known."""
    out = []
    for e in sorted(evidence, key=lambda e: (e["path"], e["start_line"], e["id"])):
        where = f"{e['path']}:{e['start_line']}" + (f"-{e['end_line']}" if e["end_line"] != e["start_line"] else "")
        if link:
            url = f"{link['base_url']}/blob/{link['commit']}/{e['path']}#L{e['start_line']}" + \
                (f"-L{e['end_line']}" if e["end_line"] != e["start_line"] else "")
            out.append(f"`{e['id']}` ([{md(where)}]({url}))")
        else:
            out.append(f"`{e['id']}` ({md(where)})")
    return ", ".join(out)


def _schema_name(model_fact) -> str:
    return model_fact["attributes"]["name"]["value"].rsplit(".", 1)[-1] + "_" + model_fact["id"].split(":", 1)[1][:8]


def _field_schema(fv, facts: dict, components: dict):
    """OpenAPI 3.1 schema for one ModelField; unknown stays `{}` with an annotation, never a guessed type."""
    t = fv.get("type")
    if not is_known(t):
        return {"x-analysis": {"unknown": t["reason"] if t else "Kiểu chưa xác định"}}
    schema = _resolve_refs(t["value"], facts, components)
    if is_known(fv.get("nullable")) and fv["nullable"]["value"]:
        schema = {"anyOf": [schema, {"type": "null"}]}
    return schema


def _resolve_refs(schema, facts: dict, components: dict):
    if isinstance(schema, dict):
        if "x-model-fact" in schema:
            target = facts.get(schema["x-model-fact"])
            return _model_ref(target, facts, components) if target else {"x-analysis": {"unknown": "Model lồng không còn"}}
        return {k: _resolve_refs(v, facts, components) for k, v in schema.items()}
    if isinstance(schema, list):
        return [_resolve_refs(v, facts, components) for v in schema]
    return schema


def _model_ref(model_fact, facts: dict, components: dict) -> dict:
    """Add the model to `components.schemas` once; return a local `$ref`."""
    name = _schema_name(model_fact)
    if name not in components:
        components[name] = {}  # placeholder stops recursion on self-referencing models
        a = model_fact["attributes"]
        fields = a["fields"]["value"] if is_known(a.get("fields")) else []
        def wire(f):  # FastAPI writes the alias into the schema when a field has one
            return f["alias"]["value"] if is_known(f.get("alias")) else f["name"]["value"]
        props = {wire(f): _field_schema(f, facts, components) for f in fields if is_known(f.get("name"))}
        required = sorted(wire(f) for f in fields if is_known(f.get("name")) and is_known(f.get("required"))
                          and f["required"]["value"])
        schema = {"type": "object", "properties": props, "x-analysis": {"fact_ids": [model_fact["id"]]}}
        if required:
            schema["required"] = required
        if model_fact["completeness"] == "partial":
            schema["x-analysis"]["completeness"] = "partial"
        components[name] = schema
    return {"$ref": f"#/components/schemas/{name}"}


def _parameters_oas(a) -> tuple[list | None, str | None, list]:
    """OpenAPI parameters (path/query/header/cookie), or (None, reason, []) when they cannot be shown safely.
    A parameter whose place is unknown is left out and named in the third value, never given a guessed place."""
    if not is_known(a.get("parameters")):
        return None, "Tham số chưa xác định", []
    out, unplaced = [], []
    for p in a["parameters"]["value"]:
        if is_known(p.get("name")) and not is_known(p.get("in")):
            unplaced.append({"name": p["name"]["value"], "reason": p["in"].get("reason", "Vị trí chưa biết")})
            continue
        if not all(is_known(p.get(k)) for k in ("name", "in", "required")):
            return None, "Một tham số thiếu tên, vị trí hoặc required", []
        item = {"name": p["name"]["value"], "in": p["in"]["value"], "required": p["required"]["value"]}
        item["schema"] = p["schema"]["value"] if is_known(p.get("schema")) else {}
        if is_known(p.get("nullable")) and p["nullable"]["value"] and item["schema"]:
            item["schema"] = {"anyOf": [item["schema"], {"type": "null"}]}  # Optional[X] parameter, as FastAPI writes it
        if not is_known(p.get("schema")):
            item["x-analysis"] = {"unknown": (p.get("schema") or {}).get("reason", "Tham số không có trường schema")}
        out.append(item)
    return out, None, unplaced


def _path_cell(a: dict) -> str:
    text = cell(a.get("path"))
    if not is_known(a.get("path")) and is_known(a.get("path_suffix")):
        text += f" (hậu tố đã biết: {md(a['path_suffix']['value'])})"
    return text


def _short(fid: str) -> str:
    return "f:" + fid.split(":", 1)[1][:8]


def _model_name(model_fact) -> str:
    return model_fact["attributes"]["name"]["value"].rsplit(".", 1)[-1] if is_known(model_fact["attributes"].get("name")) \
        else model_fact["id"]


def _model_label(model_fact, facts: dict) -> str:
    """Class name, plus the declaring file when another model in the document has the same name."""
    name = _model_name(model_fact)
    same = [x for x in facts.values() if x.get("kind") in ("model", "request_model", "response_model")
            and x["id"] != model_fact["id"] and _model_name(x) == name]
    return f"{name} ({model_fact['evidence'][0]['path']})" if same and model_fact.get("evidence") else name


def _type_text(schema, facts: dict) -> str:
    """A JSON Schema in a few words for the reader table: `string(uuid)`, `list[ItemPublic]`, `integer | null`."""
    if not isinstance(schema, dict) or not schema:
        return "?"
    if "x-model-fact" in schema:
        target = facts.get(schema["x-model-fact"])
        return _model_name(target) if target else "model?"
    if "x-external-model" in schema:  # a library generic: PaginatedListResponse[ItemRead]
        args = ", ".join(_type_text(t, facts) for t in schema.get("x-type-args", []))
        return schema["x-external-model"].rsplit(".", 1)[-1] + (f"[{args}]" if args else "")
    if "anyOf" in schema:
        return " | ".join(_type_text(s, facts) for s in schema["anyOf"])
    if schema.get("type") == "array":
        return f"list[{_type_text(schema.get('items', {}), facts)}]"
    if "type" in schema:
        return f"{schema['type']}({schema['format']})" if schema.get("format") else str(schema["type"])
    return "?"


def _nested_ids(schema) -> list[str]:
    if isinstance(schema, dict):
        return ([schema["x-model-fact"]] if "x-model-fact" in schema else []) + \
            [i for v in schema.values() for i in _nested_ids(v)]
    if isinstance(schema, list):
        return [i for v in schema for i in _nested_ids(v)]
    return []


def _response_schema(b: dict, facts: dict, components: dict) -> dict:
    """A response body's schema; a generic model keeps its arguments beside the $ref (x-type-args)."""
    ref = _model_ref(facts[b["model_id"]], facts, components)
    if b.get("type_args"):
        ref = {**ref, "x-type-args": [_resolve_refs(t, facts, components) for t in b["type_args"]]}
    return {"type": "array", "items": ref} if b.get("array") else ref


def _models_cell(fv, facts: dict, bodies=None) -> str:
    """Request/response models by class name for the reader table."""
    if not is_known(fv):
        return cell(fv)
    arrays = {b['model_id'] for b in bodies['value'] if b.get('array')} if is_known(bodies) else set()
    generic = {b['model_id']: b['type_args'] for b in bodies['value'] if b.get('type_args')} if is_known(bodies) else {}
    names = [_model_label(facts[i], facts) if i in facts else i for i in fv["value"]]
    names = [f"{n}[{', '.join(_type_text(t, facts) for t in generic[i])}]" if i in generic else n
             for i, n in zip(fv['value'], names)]
    names = [f'list[{n}]' if i in arrays else n for i, n in zip(fv['value'], names)]
    return md(", ".join(names)) if names else "(không có)"


def _need(fv) -> str:
    """Required as text; an unknown value stays unknown instead of reading as optional."""
    if isinstance(fv, bool):
        return "bắt buộc" if fv else "tùy chọn"
    if is_known(fv):
        return "bắt buộc" if fv["value"] else "tùy chọn"
    return "bắt buộc: unknown"


def _params_cell(a: dict, facts: dict | None = None) -> str:
    """Path/query/header/cookie parameters, then the body parameters (FR-029: tên, vị trí, kiểu, bắt buộc)."""
    facts = facts or {}
    fv = a.get("parameters")
    if not is_known(fv):
        return cell(fv)
    out = []
    for p in fv["value"]:
        where = p["in"]["value"] if is_known(p.get("in")) else "vị trí chưa biết"
        kind = _type_text(p["schema"]["value"], facts) if is_known(p.get("schema")) else "kiểu ?"
        out.append(f"{p['name']['value']} ({where}, {kind}, {_need(p.get('required'))})")
    bodies = [b for b in (a["bodies"]["value"] if is_known(a.get("bodies")) else []) if b["direction"] == "request"]
    if is_known(a.get("request_inline")):
        inline = a["request_inline"]["value"]
        where = "body" if inline["media_type"] == "application/json" else "form"
        for x in inline["fields"]:
            kind = _type_text(x["schema"]["value"], facts) if is_known(x["schema"]) else "kiểu ?"
            out.append(f"{x['name']} ({where}, {kind}, {_need(x['required'])})")
    elif is_known(a.get("request_body_param")) and bodies:
        names = "|".join(_model_name(facts[b["model_id"]]) if b["model_id"] in facts else "model?" for b in bodies)
        req = bodies[0].get("required")
        out.append(f"{a['request_body_param']['value']} (body, {names}, {_need(req) if req is not None else 'bắt buộc: unknown'})")
    return md("; ".join(out)) if out else "(không có)"


def _auth_cell(a: dict) -> str:
    """FR-029 column "dependency hoặc auth": the dependencies the source shows, then what is known about auth."""
    deps = a.get("dependencies")
    if not is_known(deps):
        return cell(a.get("auth")) if deps is None else f"dependency: {cell(deps)}; auth: {cell(a.get('auth'))}"
    names = ", ".join(deps["value"]) if deps["value"] else "(không có)"
    return f"dependency: {md(names)}; auth: {cell(a.get('auth'))}"


def _label(f, completeness: str, conf: str) -> str:
    """Label cell; an inferred label names its rules (AC-029-03)."""
    rules = re.findall(r"(?:^|; )([\w.-]+):", f.get("confidence_reason", "")) if conf == "inferred" else []
    return f"{conf} ({', '.join(sorted(set(rules)))}) / {completeness}" if rules else f"{conf} / {completeness}"


EXACT_STATUS_RULES = {"fastapi.status_constant"}  # a named constant is declared in code; only defaults are inferred


def _status_cell(a: dict) -> str:
    text = cell(a.get("status_codes"))
    rule = a.get("status_rule")
    if not is_known(rule):
        return text
    if rule["value"] in EXACT_STATUS_RULES:
        return text + " (hằng status khai trong code)"
    return text + f" (suy theo {md(rule['value'])})"


def _route_sort_key(f):
    a = f["attributes"]
    where = a["path"]["value"] if is_known(a.get("path")) else (a["path_suffix"]["value"] if is_known(a.get("path_suffix")) else "")
    return (where, a["method"]["value"] if is_known(a.get("method")) else "", f["id"])


def _summary_row(f, comp, facts) -> str:
    a = f["attributes"]
    conf, completeness = _row_label(f, comp)
    path = md(a["path"]["value"]) if is_known(a.get("path")) else _path_cell(a)
    request = _models_cell(a.get("request_model_ids"), facts)
    response = _models_cell(a.get("response_model_ids"), facts, a.get('bodies'))
    if is_known(a.get("response_type")):
        response = md(_type_text(a["response_type"]["value"]["schema"], facts))
    if is_known(a.get("request_inline")):
        inline = a["request_inline"]["value"]
        request = md(f"{inline['media_type']}: " + ", ".join(f["name"] for f in inline["fields"]))
    return "| " + " | ".join([cell(a.get("method")), path, _params_cell(a, facts), request,
                              response, _status_cell(a), _auth_cell(a),
                              _label(f, completeness, conf), f"`{_short(f['id'])}`"]) + " |"


def _model_section(model_fact, direction, facts: dict) -> list[str]:
    a = model_fact["attributes"]
    lines = [f"### {md(_model_label(model_fact, facts))} ({direction})", "",
             f"Fact `{_short(model_fact['id'])}` · {_label(model_fact, model_fact['completeness'], model_fact['confidence'])} · "
             f"khai ở {md(model_fact['evidence'][0]['path'])}:{model_fact['evidence'][0]['start_line']}", "",
             "| Field | Kiểu | Bắt buộc | Nullable |", "|---|---|---|---|"]
    fields = a["fields"]["value"] if is_known(a.get("fields")) else []
    for fv in fields:
        kind = _type_text(fv["type"]["value"], facts) if is_known(fv.get("type")) else cell(fv.get("type"))
        name = cell(fv.get("name")) + (f" (alias {cell(fv['alias'])})" if is_known(fv.get("alias")) else "")
        lines.append("| " + " | ".join([name, kind, cell(fv.get("required")), cell(fv.get("nullable"))]) + " |")
    if not fields:
        lines.append(f"| {cell(a.get('fields'))} | | | |")
    return lines + [""]


def render_api(comp, routes, path, title, facts=None, link=None, origin="phân tích tĩnh"):
    facts = facts or {}
    routes = sorted(routes, key=_route_sort_key)
    notices, rows, ops, omitted, components = [], [], {}, [], {}
    keys = {}
    for f in routes:
        a = f["attributes"]
        if is_known(a.get("method")) and is_known(a.get("path")):
            keys.setdefault((a["method"]["value"], a["path"]["value"]), []).append(f["id"])
    for f in routes:
        a = f["attributes"]
        conf, completeness = _row_label(f, comp)
        path_cell = _path_cell(a)
        ev_ids = sorted(e["id"] for e in f["evidence"])
        rows.append("| " + " | ".join([cell(a.get("application_id")), cell(a.get("method")), path_cell, cell(a.get("handler")),
                    cell(a.get("request_model_ids")), cell(a.get("response_model_ids")), cell(a.get("status_codes")),
                    _auth_cell(a), f"`{f['id']}`", ev_cell(f["evidence"], link), conf, completeness]) + " |")
        params, param_reason, unplaced = _parameters_oas(a)
        reason, fields = None, []
        path_params = set(re.findall(r"{(\w+)", a["path"]["value"])) if is_known(a.get("path")) else set()
        if not is_known(a.get("method")) or a["method"]["value"] not in OPENAPI_METHODS:
            reason, fields = "Method chưa biết hoặc không biểu diễn được", ["/attributes/method"]
        elif not is_known(a.get("path")):
            reason, fields = "Path đầy đủ chưa biết", ["/attributes/path"]
        elif path_params and (params is None or not path_params <= {p["name"] for p in params if p["in"] == "path"}):
            reason, fields = "Path có tham số nhưng tham số chưa được trích đủ", ["/attributes/parameters"]
        elif len(keys[(a["method"]["value"], a["path"]["value"])]) > 1:
            reason, fields = "Trùng method/path trong cùng file; không chọn handler", ["/attributes/path"]
        elif not is_known(a.get("status_codes")) or not a["status_codes"]["value"]:
            reason, fields = "Status code chưa biết", ["/attributes/status_codes"]
        elif not (is_known(a.get("application_id")) and is_known(a.get("registration_context"))):
            # API-008 §5: without app/mount identity the operation could be merged with another app's
            reason, fields = "Application hoặc registration context chưa biết", ["/attributes/application_id",
                                                                                "/attributes/registration_context"]
        if reason:
            omitted.append({"fact_id": f["id"], "reason": reason})
            notices.append(notice("OPENAPI_OPERATION_OMITTED", reason, [f["id"]], fields, path))
            continue
        bodies = a["bodies"]["value"] if is_known(a.get("bodies")) else []
        responses = {}
        rule = a["status_rule"]["value"] if is_known(a.get("status_rule")) else None
        for code in a["status_codes"]["value"]:
            resp = {"description": f"Status code suy theo {rule}" if rule else "Status code lấy từ source"}
            content = {b["media_type"]: {"schema": _response_schema(b, facts, components)}
                       for b in bodies if b["direction"] == "response" and b["status"] == code
                       and b.get("media_type") and b["model_id"] in facts}
            if not content and is_known(a.get("response_type")):
                rtype = a["response_type"]["value"]
                content = {rtype["media_type"]: {"schema": _resolve_refs(rtype["schema"], facts, components)}}
            if content:
                resp["content"] = content
            else:
                resp["description"] += "; nội dung response chưa xác định"
            responses[str(code)] = resp
        op = {"operationId": "op_" + f["id"].split(":", 1)[1][:16], "responses": responses,
              "x-analysis": {"fact_ids": [f["id"]], "evidence_ids": ev_ids,
                             "application_id": a["application_id"]["value"] if is_known(a.get("application_id")) else None,
                             "unknowns": _unknowns(f)}}
        if params is not None and params:
            op["parameters"] = params
        elif params is None:
            op["x-analysis"]["parameters_unknown"] = param_reason
        if unplaced:
            op["x-analysis"]["parameters_unknown"] = unplaced
        requests = [b for b in bodies if b["direction"] == "request" and b.get("media_type") and b["model_id"] in facts]
        if is_known(a.get("request_inline")):  # Form/File fields, or a body FastAPI wraps by parameter name
            inline = a["request_inline"]["value"]
            props = {f["name"]: _resolve_refs(f["schema"]["value"], facts, components) if is_known(f["schema"])
                     else {"x-analysis": {"unknown": f["schema"]["reason"]}} for f in inline["fields"]}
            schema = {"type": "object", "properties": props}
            if any(is_known(f["required"]) and f["required"]["value"] for f in inline["fields"]):
                schema["required"] = sorted(f["name"] for f in inline["fields"]
                                            if is_known(f["required"]) and f["required"]["value"])
            unsure = sorted(f["name"] for f in inline["fields"] if not is_known(f["required"]))
            if unsure:
                schema["x-analysis"] = {"required_unknown": unsure}
            op["requestBody"] = {"content": {inline["media_type"]: {"schema": schema}}}
            if is_known(inline["required"]):
                op["requestBody"]["required"] = inline["required"]["value"]
            else:
                op["x-analysis"]["request_body_required"] = "unknown"
        elif len(requests) == 1:
            op["requestBody"] = {"content": {requests[0]["media_type"]: {
                "schema": _model_ref(facts[requests[0]["model_id"]], facts, components)}}}
            if isinstance(requests[0].get("required"), bool):
                op["requestBody"]["required"] = requests[0]["required"]
            else:  # OpenAPI reads a missing `required` as false; say that it is not known
                op["x-analysis"]["request_body_required"] = "unknown"
        elif len(requests) > 1:
            op["x-analysis"]["request_bodies_unrepresented"] = "Nhiều body model; FastAPI gộp chúng, chưa biểu diễn"
        ops.setdefault(a["path"]["value"], {})[a["method"]["value"].lower()] = op
    head = "| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |"
    uses = {}  # model fact -> every way a route uses it: request, response, and nested in either
    for f in routes:
        for direction, key in (("request", "request_model_ids"), ("response", "response_model_ids")):
            fv = f["attributes"].get(key)
            for mid in (fv["value"] if is_known(fv) else []):
                if mid in facts:
                    uses.setdefault(mid, set()).add(direction)
        bodies = f["attributes"]["bodies"]["value"] if is_known(f["attributes"].get("bodies")) else []
        rtype = f["attributes"].get("response_type")
        args = [t for b in bodies for t in b.get("type_args", [])] + \
            ([rtype["value"]["schema"]] if is_known(rtype) else [])  # library generic arguments too
        for mid in _nested_ids(args):  # Page[Item]: Item is used
            if mid in facts:
                uses.setdefault(mid, set()).add("response")
    todo = list(uses)
    while todo:  # models used inside a field (`notes: list[NoteSchema]`) are listed too
        mf = facts[todo.pop()]
        fields = mf["attributes"]["fields"]["value"] if is_known(mf["attributes"].get("fields")) else []
        for nested in _nested_ids([x["type"]["value"] for x in fields if is_known(x.get("type"))]):
            if nested not in facts:
                continue
            new = {d if d.endswith(", lồng") else d + ", lồng" for d in uses[mf["id"]]} - uses.get(nested, set())
            if new:
                uses.setdefault(nested, set()).update(new)
                todo.append(nested)
    used = {mid: "; ".join(sorted(ds)) for mid, ds in uses.items()}
    model_lines = [line for mid in sorted(used, key=lambda i: (_model_name(facts[i]), i))
                   for line in _model_section(facts[mid], used[mid], facts)]
    body = [f"# API — {md(title)}", "", f"Bản sinh tự động từ {origin}, chưa được chủ repository duyệt.", "",
            "## Endpoint", "",
            "Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.", "",
            "| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |", "|" + "---|" * 9,
            *[_summary_row(f, comp, facts) for f in routes], "",
            *[f"- Tham số {md(n)} có vị trí chưa biết: {md(r)}" for n, r in sorted({
                (p["name"]["value"], p["in"]["reason"]) for f in routes if is_known(f["attributes"].get("parameters"))
                for p in f["attributes"]["parameters"]["value"] if is_known(p.get("name")) and not is_known(p.get("in"))})],
            "",
            "## Model", "", *(model_lines or ["Không route nào có request/response model đã xác định.", ""]),
            "## Truy vết", "", head, "|" + "---|" * 12, *rows, "",
            *(["Model (mã dữ kiện đầy đủ và vị trí khai báo):", "", "| Model | Fact | Evidence |", "|---|---|---|"]
              + [f"| {md(_model_name(facts[mid]))} | {facts[mid]['id']} | "  # plain ID: only route rows carry `fact:` in backticks
                 + ", ".join(md(f"{e['path']}:{e['start_line']}") for e in facts[mid]["evidence"][:1]) + " |"
                 for mid in sorted(used, key=lambda i: (_model_name(facts[i]), i))] + [""] if used else [])]
    if ops:
        doc = {"openapi": "3.1.0", "info": {"title": title, "version": "generated-v1"}, "paths": ops,
               "x-analysis": {"omitted_operations": omitted}}
        if components:
            doc["components"] = {"schemas": components}
        body += ["Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.", "",
                 "```json", json.dumps(doc, ensure_ascii=False, sort_keys=True, indent=2), "```", ""]
    else:
        doc = None
        reason = "Không route nào đủ method, path đầy đủ và status code"
        body += [f"Chưa có khối OpenAPI: {reason}.", ""]
        notices.append(notice("OPENAPI_BLOCK_OMITTED", reason, [f["id"] for f in routes], [], path))
    if omitted:
        where = {f["id"]: f"{cell(f['attributes'].get('method'))} {_route_sort_key(f)[0] or '?'}" for f in routes}
        body += ["Bỏ khỏi khối OpenAPI:", ""] + [f"- Bỏ khỏi OpenAPI: `{o['fact_id']}` ({md(where[o['fact_id']])}) — "
                                                 f"{md(o['reason'])}" for o in omitted] + [""]
    machine = sorted(i for ops_ in ops.values() for op in ops_.values() for i in op["x-analysis"]["fact_ids"])
    cov = {"rows": [f["id"] for f in routes], "machine": machine, "omitted": sorted(o["fact_id"] for o in omitted),
           "facts": {f["id"]: f for f in routes}}
    return "\n".join(body), doc, notices, cov


# ---------- TBL (API-008 §6) ----------

def _quote(name: str) -> str | None:
    if any(ord(ch) < 32 for ch in name):
        return None
    return '"' + name.replace('"', '""') + '"'


def _catalogue_type(dialect: str, token: str) -> bool:
    """ddl-core-v1 (API-008 §6.1): fixed tokens, plus VARCHAR(n>0) and NUMERIC(1<=p<=1000, 0<=s<=p) for PostgreSQL."""
    if token in DDL_TYPES[dialect]:
        return True
    if dialect == "postgresql":
        m = re.fullmatch(r"VARCHAR\((\d+)\)", token)
        if m:
            return int(m.group(1)) > 0
        m = re.fullmatch(r"NUMERIC\((\d+),(\d+)\)", token)
        if m:
            p, s = int(m.group(1)), int(m.group(2))
            return 1 <= p <= 1000 and 0 <= s <= p
    return False


def _ddl(fact) -> tuple[str | None, str | None, list[str]]:
    """Return (ddl, omit_reason, field_paths)."""
    a = fact["attributes"]
    for key in ("name", "dialect", "columns"):
        if not is_known(a.get(key)):
            return None, f"{key} chưa biết", [f"/attributes/{key}"]
    dialect = a["dialect"]["value"]
    if dialect not in DDL_TYPES:
        return None, f"Dialect {dialect!r} ngoài catalogue ddl-core-v1", ["/attributes/dialect"]
    cols, pks, fks, missing = [], [], [], []
    for i, col in enumerate(a["columns"]["value"]):
        for key in ("name", "type", "primary_key", "nullable"):
            if not is_known(col.get(key)):
                missing.append(f"/attributes/columns/value/{i}/{key}")
        fk = col.get("foreign_key")
        if fk is None or fk["state"] not in ("known", "not_applicable"):
            missing.append(f"/attributes/columns/value/{i}/foreign_key")
    if missing:
        return None, "Cột thiếu trường bắt buộc", missing
    for col in a["columns"]["value"]:
        name, ctype = _quote(col["name"]["value"]), col["type"]["value"]
        if name is None or not _catalogue_type(dialect, ctype):
            return None, "Tên cột hoặc kiểu ngoài catalogue", ["/attributes/columns"]
        cols.append(f"  {name} {ctype}" + ("" if col["nullable"]["value"] else " NOT NULL"))
        if col["primary_key"]["value"]:
            if col["nullable"]["value"]:
                return None, "Khóa chính không được nullable", ["/attributes/columns"]
            pks.append(name)
        if col["foreign_key"]["state"] == "known":
            t = col["foreign_key"]["value"]
            if not (isinstance(t, dict) and isinstance(t.get("table"), str) and isinstance(t.get("column"), str)
                    and _quote(t["table"]) and _quote(t["column"])):
                return None, "Đích khóa ngoại không biểu diễn được thành định danh SQL", ["/attributes/columns"]
            fks.append(f"  FOREIGN KEY ({name}) REFERENCES {_quote(t['table'])} ({_quote(t['column'])})")
    if len(pks) > 1:
        return None, "Khóa chính nhiều cột chưa hỗ trợ ở v1", ["/attributes/columns"]
    table = _quote(a["name"]["value"])
    if table is None or not cols:
        return None, "Tên bảng không hợp lệ hoặc không có cột", ["/attributes/name"]
    lines = cols + ([f"  PRIMARY KEY ({pks[0]})"] if pks else []) + fks
    return f"-- fact: {fact['id']}\nCREATE TABLE {table} (\n" + ",\n".join(lines) + "\n);", None, []


def render_tbl(comp, tables, path, title, link=None):
    notices, body = [], [f"# TBL — {md(title)}", "", "Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.", ""]
    ddl_parts, emitted = [], 0
    cov = {"rows": [f["id"] for f in tables], "machine": [], "omitted": [], "facts": {f["id"]: f for f in tables}}
    for f in tables:
        a = f["attributes"]
        conf, completeness = _row_label(f, comp)
        body += [f"## Bảng {cell(a.get('name'))}", "",
                 f"Dialect: {cell(a.get('dialect'))}. Fact `{f['id']}`. Confidence {conf}, completeness {completeness}.", "",
                 f"Evidence: {ev_cell(f['evidence'], link)}.", "",
                 "| Cột | Kiểu | PK | FK | Nullable |", "|---|---|---|---|---|"]
        columns = a["columns"]["value"] if is_known(a.get("columns")) else []
        for col in columns:
            body.append("| " + " | ".join(cell(col.get(k)) for k in ("name", "type", "primary_key", "foreign_key", "nullable")) + " |")
        if not columns:
            body.append(f"| {cell(a.get('columns'))} | | | | |")
        body.append("")
        ddl, reason, fields = _ddl(f)
        if ddl:
            ddl_parts.append(ddl)
            emitted += 1
            cov["machine"].append(f["id"])
        else:
            ddl_parts.append(f"-- omitted: {f['id']}: {reason}".replace("\n", " "))
            cov["omitted"].append(f["id"])
            notices.append(notice("DDL_TABLE_OMITTED", reason, [f["id"]], fields, path))
    if not emitted:
        notices.append(notice("DDL_BLOCK_OMITTED", "Không bảng nào đủ dữ kiện cho DDL", [f["id"] for f in tables], [], path))
    body += ["DDL dẫn xuất tĩnh, không phải migration; không được thực thi. Bảng thiếu dữ kiện bị bỏ khỏi DDL.", "",
             "```sql", "\n".join(ddl_parts), "```", ""]
    return "\n".join(body), notices, cov


# ---------- EVT (API-008 §6.2) ----------

BINDING_KEYS = ("broker", "namespace", "serialization_context", "topic")
JSON_SCHEMA = "https://json-schema.org/draft/2020-12/schema"


def _source_order(fact):
    decl = fact["attributes"].get("declaration_evidence_id")
    ev = next((e for e in fact["evidence"] if is_known(decl) and e["id"] == decl["value"]), fact["evidence"][0])
    return ev["path"], ev["start_line"], fact["id"]


def plan_events(events: list[dict]) -> list[tuple[str, str, list[dict]]]:
    """Group a component's event points into files: (group key, file topic label, facts) in stable source order."""
    groups = {}
    for f in events:
        a = f["attributes"]
        if all(is_known(a.get(k)) for k in BINDING_KEYS):
            key = "chan:" + sha(json.dumps([a[k]["value"] for k in BINDING_KEYS], ensure_ascii=False).encode())
        else:
            key = f["id"]  # binding not proven: keep the point on its own
        groups.setdefault(key, []).append(f)
    ordered = sorted(groups.items(), key=lambda kv: min(_source_order(f) for f in kv[1]))
    names = []
    for key, facts in ordered:
        topic = facts[0]["attributes"].get("topic")
        names.append((key, topic["value"] if is_known(topic) else "UNKNOWN-" + facts[0]["id"].split(":", 1)[1][:12]))
    labels = unique_slugs(names, "TOPIC")
    return [(key, labels[key], sorted(facts, key=_source_order)) for key, facts in ordered]


def _counterparts(fact, comp, model, comps):
    names = []
    for e in model["edges"]:
        if e["relation_type"] in ("publishes", "consumes") and fact["id"] in e["fact_ids"] \
                and comp["id"] in (e["source_component_id"], e["target_component_id"]):
            other = e["target_component_id"] if e["source_component_id"] == comp["id"] else e["source_component_id"]
            names.append(comps[other]["name"])
    return sorted(names)


def render_evt(comp, facts, path, model, comps, binding_proven, link=None):
    notices = []
    topic = facts[0]["attributes"].get("topic")
    body = [f"# EVT — {md(comp['name'])} — {cell(topic)}", "",
            "Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt. File mô tả vai trò của chính component này; "
            "không có nghĩa component sở hữu độc quyền topic.", "",
            "| Vai trò | Topic | Broker | Namespace | Serialization | Bên liên quan | Fact | Evidence | Confidence | Completeness |",
            "|" + "---|" * 10]
    blocks = []
    for f in facts:
        a = f["attributes"]
        conf, completeness = _row_label(f, comp)
        others = _counterparts(f, comp, model, comps)
        role = {"publish": "gửi", "consume": "nhận"}.get(a["action"]["value"]) if is_known(a.get("action")) else None
        other_side = "bên nhận" if role == "gửi" else "bên gửi"
        if others:
            party = md(", ".join(others))
        else:
            party = f"unknown — chưa có cạnh event đã kiểm nối {other_side}"
            completeness = "partial"
        ev_ids = sorted(e["id"] for e in f["evidence"])
        body.append("| " + " | ".join([role or cell(a.get("action")), cell(a.get("topic")), cell(a.get("broker")),
                    cell(a.get("namespace")), cell(a.get("serialization_context")), party, f"`{f['id']}`",
                    ev_cell(f["evidence"], link), conf, completeness]) + " |")
        payload = a.get("payload")
        analysis = {"fact_ids": [f["id"]], "evidence_ids": ev_ids}
        if is_known(payload) and isinstance(payload["value"], dict):
            schema = dict(payload["value"], **{"$schema": JSON_SCHEMA, "x-analysis": dict(analysis, completeness="full")})
        else:
            reason = payload["reason"] if payload and "reason" in payload else "Payload chưa xác định"
            schema = {"$schema": JSON_SCHEMA, "x-analysis": dict(analysis, completeness="partial",
                                                                    unknowns=[{"field": "payload", "reason": reason}])}
            notices.append(notice("EVENT_PAYLOAD_UNKNOWN", reason, [f["id"]], ["/attributes/payload"], path))
        blocks += [f"Payload của `{f['id']}`" + ("" if is_known(payload) else " — schema `{}` không phải schema đầy đủ") + ":", "",
                   "```json", json.dumps(schema, ensure_ascii=False, sort_keys=True, indent=2), "```", ""]
    if not binding_proven:
        missing = [f"/attributes/{k}" for k in BINDING_KEYS if not is_known(facts[0]["attributes"].get(k))]
        notices.append(notice("EVENT_BINDING_UNRESOLVED", "Chưa chứng minh broker/namespace/serialization/topic; điểm này giữ riêng",
                              [f["id"] for f in facts], missing, path))
    ids = [f["id"] for f in facts]
    return "\n".join(body + [""] + blocks), notices, {"rows": ids, "machine": list(ids), "omitted": [],
                                                      "facts": {f["id"]: f for f in facts}}


# ---------- diagram, README, parity ----------

def mermaid_label(text: str) -> str:
    """Text from the repository is data: Mermaid entity codes for #, quotes and angle brackets; no line breaks."""
    out = str(text).replace("#", "#35;").replace(chr(34), "#quot;").replace("<", "#lt;").replace(">", "#gt;")
    return " ".join(out.split())


def _mermaid_lines(model, plan):
    names = {n["id"]: n["name"] for n in model["components"] + model["external_systems"]}
    token = {nid: f"n{i}" for i, nid in enumerate(plan["nodes"])}
    lines = ["flowchart LR"] + [f'  {token[nid]}["{mermaid_label(names[nid])}"]' for nid in plan["nodes"]]
    lines += [f"  {token[s]} -->|{rel}| {token[t]}" for s, t, rel in plan["edges"]]
    return lines


def mermaid(model) -> tuple[str, dict]:
    """Mermaid source plus the plan it was drawn from (node IDs, (source, target, relation) edges)."""
    nodes = sorted(n["id"] for n in model["components"] + model["external_systems"])
    edges = [(e["source_component_id"], e["target_component_id"], e["relation_type"])
             for e in sorted(model["edges"], key=lambda e: e["id"])]
    plan = {"nodes": nodes, "edges": edges}
    return "\n".join(_mermaid_lines(model, plan)) + "\n", plan


def check_diagram(model, plan, text):
    """Same node IDs and same (source, target, relation) edges as the model, and the text draws exactly the plan."""
    nodes = {n["id"] for n in model["components"] + model["external_systems"]}
    edges = Counter((e["source_component_id"], e["target_component_id"], e["relation_type"]) for e in model["edges"])
    if set(plan["nodes"]) != nodes or len(plan["nodes"]) != len(nodes) or Counter(plan["edges"]) != edges:
        raise ExportError("PARITY_FAILED", "Sơ đồ khác tập node hoặc cạnh (nguồn, đích, loại) của model")
    if text.splitlines() != _mermaid_lines(model, plan):
        raise ExportError("PARITY_FAILED", "Mã Mermaid không khớp kế hoạch vẽ")


def readme(verified, export_context, contract_files, notices, diagram, evt_index) -> str:
    inv = verified["inventory"]
    unassigned = [o for o in verified["model"]["contract_owners"] if o["component_id"] is None]
    lines = [f"# {md(export_context['repository_name'])} — kết quả phân tích (bản sinh tự động)", "",
             f"- Snapshot: `{verified['snapshot_id']}`",
             f"- Schema {SCHEMA_VERSION}; renderer {RENDERER_VERSION}; template {TEMPLATE_VERSION}",
             f"- Phạm vi: {sum(len(u['file_ids']) for u in inv['units'])} file trong {len(inv['units'])} unit; "
             f"{len(inv['excluded'])} file bị loại khỏi snapshot", "",
             "## Sơ đồ component", "", "```mermaid", diagram.rstrip("\n"), "```", "",
             "## Mục lục contract", ""]
    lines += [f"- {kind}: [{p}]({p}) — component `{cid}`" for p, kind, cid in contract_files] or ["- (không có)"]
    lines += ["", "## Mục lục EVT theo topic", ""]
    by_topic = {}
    for topic, p, roles in evt_index:
        by_topic.setdefault(topic, []).append(f"[{p}]({p}) ({', '.join(roles) or 'vai trò chưa biết'})")
    lines += [f"- {md(t)}: " + "; ".join(v) for t, v in sorted(by_topic.items())] or ["- (không có)"]
    lines += ["", "## Contract chưa gán được component", ""]
    lines += [f"- `{o['fact_id']}` ({o['contract_kind']}): {md(o['reason'])}" for o in unassigned] or ["- (không có)"]
    lines += ['', '## Lời gọi HTTP ra ngoài', '']
    calls = [f for f in verified['facts']['facts'] if f['kind'] == 'http_call']
    if calls:
        lines += ['| Component | Thư viện, method | Đích | Bằng chứng |', '|---|---|---|---|']
        owners = {fid: c['name'] for c in verified['model']['components'] for fid in c['member_file_ids']}
        for f in calls:
            a, ev = f['attributes'], f['evidence'][0]
            target = cell(a.get('url'))
            if not is_known(a.get('url')) and is_known(a.get('url_config_key')):
                target = 'khóa cấu hình ' + cell(a['url_config_key'])
            owner = owners.get(ev['file_id'], 'unknown — chưa gán component')
            location = md(f"{ev['path']}:{ev['start_line']}")
            lines.append('| ' + ' | '.join([md(owner), cell(a.get('library')) + ', ' + cell(a.get('method')),
                                             target, location + ': ' + cell(a.get('call_text'))]) + ' |')
    else:
        lines += ['- (không có)']
    lines += ["", "## Giới hạn", ""]
    lines += [f"- `{l['code']}` ({l['stage']}): {md(l['message'])}" for l in verified["limitations"]] or ["- (không có)"]
    lines += ["", "## Giới hạn biểu diễn", ""]
    lines += [f"- `{n['code']}`: {md(n['reason'])} — {', '.join(f'`{i}`' for i in n['fact_ids'])}" for n in notices] or ["- (không có)"]
    return "\n".join(lines) + "\n"


FACT = r"fact:[0-9a-f]{64}"


def _parsed(kind: str, text: str) -> dict:
    """Read back fact IDs from the rendered text: table rows, machine blocks, omitted entries."""
    if kind == "table":
        rows = re.findall(rf"^Dialect: .*Fact `({FACT})`", text, re.M)
        return {"rows": rows, "machine": re.findall(rf"^-- fact: ({FACT})$", text, re.M),
                "omitted": re.findall(rf"^-- omitted: ({FACT}):", text, re.M)}
    rows = re.findall(rf"^\|.*\| `({FACT})` \|", text, re.M)
    machine = []
    for raw in re.findall(r"^```json\n(.*?)^```", text, re.M | re.S):
        doc = json.loads(raw)
        if kind == "api":
            machine += [i for ops in doc.get("paths", {}).values() for op in ops.values() for i in op["x-analysis"]["fact_ids"]]
        else:
            machine += doc["x-analysis"]["fact_ids"]
    omitted = re.findall(rf"^- Bỏ khỏi OpenAPI: `({FACT})`", text, re.M) if kind == "api" else []
    return {"rows": rows, "machine": machine, "omitted": omitted}


def check_doc(kind: str, text: str, cov: dict) -> str | None:
    """API-008 §3.1 'Bảng và khối máy cùng nguồn'. Returns a reason when the artifact is FORMAT_INVALID."""
    got = _parsed(kind, text)
    for part in ("rows", "machine", "omitted"):
        if sorted(got[part]) != sorted(cov[part]):
            return f"{part} trong file khác kế hoạch sinh"
    if set(got["machine"]) & set(got["omitted"]) or set(got["rows"]) != set(got["machine"]) | set(got["omitted"]):
        return "Mỗi dòng phải có trong khối máy hoặc được ghi là bị bỏ, không cả hai"
    return _value_problem(kind, text, cov.get("facts", {}))


def _cells(line: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]


def _fact_rows(text: str) -> dict:
    """Table rows of an API/EVT file keyed by the fact ID they cite."""
    out = {}
    for line in text.splitlines():
        m = re.search(rf"\| `({FACT})` \|", line)
        if line.startswith("|") and m:
            out[m.group(1)] = _cells(line)
    return out


def _value_problem(kind: str, text: str, facts: dict) -> str | None:
    """Read each published value back from the table and the machine block and compare it with the fact, so a
    wrong method/path/status/column/topic is caught even when every ID is right (API-008 §3.1)."""
    if kind == "api":
        rows = _fact_rows(text)
        for fid, f in facts.items():
            a, got = f["attributes"], rows.get(fid)
            want = [cell(a.get("application_id")), cell(a.get("method")), _path_cell(a), cell(a.get("handler")),
                    cell(a.get("request_model_ids")), cell(a.get("response_model_ids")), cell(a.get("status_codes"))]
            if got is None or got[:7] != want:
                return f"Bảng API khác dữ kiện ở {fid}"
        summary = {}
        for line in text.splitlines():
            m = re.search(r"\| `(f:[0-9a-f]{8})` \|$", line)
            if line.startswith("|") and m:
                summary[m.group(1)] = _cells(line)
        for fid, f in facts.items():
            a, got = f["attributes"], summary.get(_short(fid))
            path = md(a["path"]["value"]) if is_known(a.get("path")) else _path_cell(a)
            if got is None or [got[0], got[1], got[5]] != [cell(a.get("method")), path, _status_cell(a)]:
                return f"Bảng tóm tắt API khác dữ kiện ở {fid}"
        for raw in re.findall(r"^```json\n(.*?)^```", text, re.M | re.S):
            for path, ops in json.loads(raw).get("paths", {}).items():
                for method, op in ops.items():
                    f = facts.get(op["x-analysis"]["fact_ids"][0])
                    if f is None:
                        return "Operation dẫn fact không có trong file"
                    a = f["attributes"]
                    if not (is_known(a.get("method")) and a["method"]["value"].lower() == method
                            and is_known(a.get("path")) and a["path"]["value"] == path
                            and is_known(a.get("status_codes"))
                            and sorted(op["responses"]) == sorted(str(c) for c in a["status_codes"]["value"])):
                        return f"OpenAPI khác dữ kiện ở {f['id']}"
                    bodies = a["bodies"]["value"] if is_known(a.get("bodies")) else []
                    req = [b for b in bodies if b["direction"] == "request"]
                    body = op.get("requestBody")
                    inline = a["request_inline"]["value"] if is_known(a.get("request_inline")) else None
                    if inline is not None:
                        want = inline["required"]["value"] if is_known(inline["required"]) else None
                        if body is None or body.get("required") is not want:
                            return f"requestBody inline khác dữ kiện ở {f['id']}"
                    elif len(req) == 1 and isinstance(req[0].get("required"), bool) and (
                            body is None or body.get("required") is not req[0]["required"]):
                        return f"requestBody.required khác dữ kiện ở {f['id']}"
                    elif not req and body is not None:
                        return f"requestBody không có trong dữ kiện ở {f['id']}"
                    for response_body in (b for b in bodies if b['direction'] == 'response' and b.get('array')):
                        schema = op['responses'].get(str(response_body['status']), {}).get('content', {}).get(
                            response_body['media_type'], {}).get('schema', {})
                        if schema.get('type') != 'array' or not isinstance(schema.get('items'), dict):
                            return f"Response array khác dữ kiện ở {f['id']}"
    elif kind == "table":
        sql = "\n".join(re.findall(r"^```sql\n(.*?)^```", text, re.M | re.S))
        for fid, f in facts.items():
            a = f["attributes"]
            part = re.search(rf"^## Bảng ([^\n]*)\n\nDialect: ([^\n]*?)\. Fact `{fid}`[^\n]*\n\n[^\n]*\n\n"
                             rf"\| Cột [^\n]*\n\|---[^\n]*\n((?:\|[^\n]*(?:\n|$))*)", text, re.M)
            cols = a["columns"]["value"] if is_known(a.get("columns")) else []
            want = ["| " + " | ".join(cell(c.get(k)) for k in ("name", "type", "primary_key", "foreign_key", "nullable")) + " |"
                    for c in cols] or [f"| {cell(a.get('columns'))} | | | | |"]
            if part is None or part.group(1) != cell(a.get("name")) or part.group(2) != cell(a.get("dialect")) \
                    or part.group(3).strip("\n").split("\n") != want:
                return f"Bảng cột khác dữ kiện ở {fid}"
            ddl = _ddl(f)[0]
            if ddl is not None and ddl not in sql:
                return f"DDL khác dữ kiện ở {fid}"
    elif kind == "event":
        rows = _fact_rows(text)
        for fid, f in facts.items():
            a, got = f["attributes"], rows.get(fid)
            want = [cell(a.get(k)) for k in ("topic", "broker", "namespace", "serialization_context")]
            if got is None or got[1:5] != want:
                return f"Bảng EVT khác dữ kiện ở {fid}"
        for raw in re.findall(r"^```json\n(.*?)^```", text, re.M | re.S):
            schema = json.loads(raw)
            f = facts.get(schema["x-analysis"]["fact_ids"][0])
            payload = f["attributes"].get("payload") if f else None
            body = {k: v for k, v in schema.items() if k not in ("$schema", "x-analysis")}
            if f is None or (is_known(payload) and isinstance(payload["value"], dict) and body != payload["value"]) \
                    or (not is_known(payload) and body):
                return "Payload khác dữ kiện"
    return None


def check_placement(docs: dict, owners: list):
    """Each contract fact sits in exactly one file of its kind owned by its component; unresolved ones in none."""
    where = {}
    for path, d in docs.items():
        for fid in d["cov"]["rows"]:
            where.setdefault(fid, []).append((d["kind"], d["cid"]))
    kinds = {"api": "api", "table": "table", "event": "event"}
    for o in owners:
        got = where.get(o["fact_id"], [])
        want = [] if o["component_id"] is None else [(kinds[o["contract_kind"]], o["component_id"])]
        if got != want:
            raise ExportError("PARITY_FAILED", f"Contract {o['fact_id']} nằm ở {len(got)} file hoặc sai component")


# ---------- render ----------

def _artifact(run_id, kind, path, media, raw: bytes | None, error=None):
    art = {"artifact_id": "art_" + sha(f"{run_id}\n{path}".encode())[:24], "kind": kind, "path": path,
           "media_type": media, "status": "ready" if raw is not None else "failed",
           "sha256": sha(raw) if raw is not None else None, "bytes": len(raw) if raw is not None else None,
           "error": error}
    return art


# ---------- SVG ----------

BOX_W, BOX_H, GAP_X, GAP_Y, MARGIN = 220, 56, 80, 70, 24


def svg(model, plan) -> str:
    """Grid layout in plan order. Every node/edge carries its ID so the check can read the drawing back."""
    names = {n["id"]: n["name"] for n in model["components"] + model["external_systems"]}
    n = len(plan["nodes"])
    cols = max(1, int(n ** 0.5 + 0.999))
    pos = {nid: (MARGIN + (i % cols) * (BOX_W + GAP_X), MARGIN + (i // cols) * (BOX_H + GAP_Y))
           for i, nid in enumerate(plan["nodes"])}
    width = MARGIN * 2 + cols * BOX_W + (cols - 1) * GAP_X if n else 2 * MARGIN + BOX_W
    height = MARGIN * 2 + max(1, -(-n // cols)) * (BOX_H + GAP_Y) - GAP_Y if n else 2 * MARGIN + BOX_H
    q = lambda s: xml_escape(str(s), {'"': "&quot;"})
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="sans-serif" '
           'font-size="13">' % (width, height, width, height),
           '<defs><marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" '
           'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#555"/></marker></defs>']
    if not n:
        out.append(f'<text x="{MARGIN}" y="{MARGIN + 20}">Chưa có kiến trúc đủ bằng chứng</text>')
    for s, t, rel in plan["edges"]:
        (x1, y1), (x2, y2) = pos[s], pos[t]
        a = (x1 + BOX_W / 2, y1 + BOX_H / 2)
        b = (x2 + BOX_W / 2, y2 + BOX_H / 2)
        out.append(f'<g data-edge="{q(s)}|{q(t)}|{q(rel)}"><line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" '
                   f'stroke="#555" marker-end="url(#arrow)"/><text x="{(a[0] + b[0]) / 2:.0f}" y="{(a[1] + b[1]) / 2 - 4:.0f}" '
                   f'text-anchor="middle" fill="#333">{q(rel)}</text></g>')
    for nid in plan["nodes"]:
        x, y = pos[nid]
        label = names[nid] if len(names[nid]) <= 28 else names[nid][:27] + "…"
        out.append(f'<g data-node="{q(nid)}"><rect x="{x}" y="{y}" width="{BOX_W}" height="{BOX_H}" rx="6" fill="#f4f6fb" '
                   f'stroke="#3b5998"/><text x="{x + BOX_W / 2}" y="{y + BOX_H / 2 + 4}" text-anchor="middle">{q(label)}</text>'
                   f'<title>{q(names[nid])}</title></g>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def check_svg(model, text: str):
    """SVG parses as XML, has no script/foreign/link elements, and shows exactly the model's nodes and edges."""
    root = ET.fromstring(text)
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag in ("script", "foreignObject", "a", "image", "use", "iframe") or any(
                k.lower().startswith("on") or "href" in k.lower() for k in el.attrib):
            raise ExportError("OUTPUT_UNSAFE", f"SVG chứa phần tử hoặc thuộc tính không cho phép: {tag}")
    nodes = {el.attrib["data-node"] for el in root.iter() if "data-node" in el.attrib}
    edges = Counter(tuple(el.attrib["data-edge"].split("|")) for el in root.iter() if "data-edge" in el.attrib)
    want_nodes = {n["id"] for n in model["components"] + model["external_systems"]}
    want_edges = Counter((e["source_component_id"], e["target_component_id"], e["relation_type"]) for e in model["edges"])
    if nodes != want_nodes or edges != want_edges:
        raise ExportError("PARITY_FAILED", "SVG khác tập node/cạnh của model")


# ---------- render ----------

def _evidence_refs(value):
    if isinstance(value, dict):
        for k, v in value.items():
            if k == "evidence_ids" and isinstance(v, list):
                yield from v
            else:
                yield from _evidence_refs(v)
    elif isinstance(value, list):
        for v in value:
            yield from _evidence_refs(v)


def _check_input(v: dict):
    """API-008 §1/§3: refuse a VerifiedResult that is not one consistent, accepted, fully referenced set, before any
    file is planned. Raises ExportError; nothing is published."""
    if not isinstance(v, dict) or v.get("schema_version") != SCHEMA_VERSION:
        raise ExportError("INVALID_INPUT", f"schema_version phải là {SCHEMA_VERSION}")
    try:
        snap, facts, model, index = v["snapshot_id"], v["facts"]["facts"], v["model"], v["evidence_index"]
        parts = [v["inventory"]["snapshot_id"], v["facts"]["snapshot_id"], model["snapshot_id"]]
    except (KeyError, TypeError):
        raise ExportError("INVALID_INPUT", "VerifiedResult thiếu trường bắt buộc") from None
    if any(s != snap for s in parts) or any(e.get("snapshot_id") != snap for e in index) \
            or any(e.get("snapshot_id") != snap for f in facts for e in f["evidence"]):
        raise ExportError("SNAPSHOT_MISMATCH", "Inventory, facts, model và evidence phải cùng snapshot")
    for name, items in (("fact", facts), ("evidence", index), ("component", model["components"]),
                        ("edge", model["edges"])):
        ids = [x["id"] for x in items]
        if len(ids) != len(set(ids)):
            raise ExportError("INVALID_INPUT", f"ID {name} bị trùng")
    ev_ids, fact_ids = {e["id"] for e in index}, {f["id"] for f in facts}
    nodes = {c["id"] for c in model["components"]} | {x["id"] for x in model["external_systems"]}
    cited = [*_evidence_refs(facts), *_evidence_refs(model["components"]), *_evidence_refs(model["edges"]),
             *(e["id"] for f in facts for e in f["evidence"])]
    if not set(cited) <= ev_ids:
        raise ExportError("REFERENCE_INVALID", "Có evidence được trích dẫn nhưng không có trong evidence_index")
    for e in model["edges"]:
        if e["source_component_id"] not in nodes or e["target_component_id"] not in nodes \
                or not set(e["fact_ids"]) <= fact_ids:
            raise ExportError("REFERENCE_INVALID", f"Cạnh {e['id']} trỏ node hoặc fact không có")
    verdicts = {}
    for d in v.get("decisions", []):
        verdicts.setdefault(d["subject_id"], set()).add(d["verdict"])
    for obj in [*model["components"], *model["edges"]]:
        if verdicts.get(obj["id"]) != {"accepted"}:
            raise ExportError("INVALID_INPUT", f"{obj['id']} trong model phải có đúng decision accepted (API-007 §2)")


def plan_bundle(verified: dict, run_id: str, repository_name: str, source_link: dict | None = None,
                renderers: dict | None = None) -> tuple[dict, dict]:
    """Everything a publish needs, without touching the disk: (result data, {path: (kind, media, text | None, error)}).
    Deterministic for the same inputs and versions, which is what lets a retry rebuild one artifact."""
    renderers = {"svg": svg, **(renderers or {})}
    _check_input(verified)
    model = verified["model"]
    if len(model["components"]) + len(model["external_systems"]) > 50:
        raise ExportError("INVALID_INPUT", "Model vượt 50 node")
    facts = {f["id"]: f for f in verified["facts"]["facts"]}
    comps = {c["id"]: c for c in model["components"]}
    sys_slug = slug(repository_name, "SYSTEM")
    slugs = unique_slugs([(c["id"], c["name"]) for c in sorted(model["components"], key=lambda c: c["id"])], "COMPONENT")
    export_context = {"repository_name": repository_name, "system_slug": sys_slug, "renderer_version": RENDERER_VERSION,
                      "template_version": TEMPLATE_VERSION, "component_slugs": slugs}
    if source_link:
        export_context["source_link"] = source_link
    owners = model["contract_owners"]
    notices = [notice("CONTRACT_OWNER_UNRESOLVED", o["reason"], [o["fact_id"]], [], None)
               for o in owners if o["component_id"] is None]
    files, docs, contract_files, evt_index = {}, {}, [], []
    for cid in sorted(comps):
        comp, cslug = comps[cid], slugs[cid]
        for kind, contract_kind in (("api", "api"), ("table", "table")):
            mine = sorted((facts[o["fact_id"]] for o in owners if o["component_id"] == cid and o["contract_kind"] == contract_kind),
                          key=lambda f: f["id"])
            if not mine:
                continue
            front = {"generated": True, "non_normative": True, "snapshot_id": verified["snapshot_id"], "owner_component_id": cid,
                     "schema_version": SCHEMA_VERSION, "renderer_version": RENDERER_VERSION, "template_version": TEMPLATE_VERSION,
                     "fact_ids": [f["id"] for f in mine], "evidence_ids": sorted({e["id"] for f in mine for e in f["evidence"]})}
            if kind == "api":
                path = f"tech-specs/{cslug}/api/API-{sys_slug}-{cslug}-v1.md"
                text, _, more, cov = render_api(comp, mine, path, comp["name"], facts, source_link)
            else:
                path = f"tech-specs/{cslug}/schema/TBL-{sys_slug}-{cslug}.md"
                text, more, cov = render_tbl(comp, mine, path, comp["name"], source_link)
            docs[path] = {"kind": kind, "cid": cid, "text": text, "cov": cov}
            notices += more
            files[path] = (kind, frontmatter(front) + text)
            contract_files.append((path, kind, cid))
        events = [facts[o["fact_id"]] for o in owners if o["component_id"] == cid and o["contract_kind"] == "event"]
        for key, label, group in plan_events(events):
            path = f"tech-specs/{cslug}/events/EVT-{sys_slug}-{cslug}-{label}.md"
            text, more, cov = render_evt(comp, group, path, model, comps, key.startswith("chan:"), source_link)
            docs[path] = {"kind": "event", "cid": cid, "text": text, "cov": cov}
            front = {"generated": True, "non_normative": True, "snapshot_id": verified["snapshot_id"], "owner_component_id": cid,
                     "schema_version": SCHEMA_VERSION, "renderer_version": RENDERER_VERSION, "template_version": TEMPLATE_VERSION,
                     "fact_ids": [f["id"] for f in group], "evidence_ids": sorted({e["id"] for f in group for e in f["evidence"]})}
            notices += more
            files[path] = ("event", frontmatter(front) + text)
            contract_files.append((path, "event", cid))
            topic = group[0]["attributes"].get("topic")
            roles = sorted({f["attributes"]["action"]["value"] for f in group if is_known(f["attributes"].get("action"))})
            evt_index.append((topic["value"] if is_known(topic) else "(topic chưa biết)", path, roles))
    notices.sort(key=lambda n: (n["code"], n["fact_ids"][0], n["artifact_path"] or ""))
    diagram, plan = mermaid(model)
    check_diagram(model, plan, diagram)
    check_placement(docs, owners)
    readme_text = readme(verified, export_context, contract_files, notices, diagram, evt_index)
    if "\n".join(["```mermaid", diagram.rstrip("\n"), "```"]) not in readme_text:
        raise ExportError("PARITY_FAILED", "README không chứa đúng sơ đồ")
    data = {"run_id": run_id, "snapshot_id": verified["snapshot_id"], "schema_version": SCHEMA_VERSION,
            "result": verified, "export_context": export_context, "render_notices": notices}
    payloads = {"README.md": ("readme", "text/markdown", readme_text, None),
                "result.json": ("json", "application/json", dump(data), None),
                "architecture.mmd": ("diagram_source", "text/plain", diagram, None)}
    for p, (k, t) in files.items():
        reason = check_doc(docs[p]["kind"], docs[p]["text"], docs[p]["cov"])
        payloads[p] = (k, "text/markdown", None, {"code": "FORMAT_INVALID", "reason": reason, "retryable": False}) if reason \
            else (k, "text/markdown", t, None)
    try:
        image = renderers["svg"](model, plan)
        check_svg(model, image)
        payloads["architecture.svg"] = ("diagram_image", "image/svg+xml", image, None)
    except ExportError as exc:
        payloads["architecture.svg"] = ("diagram_image", "image/svg+xml", None,
                                        {"code": "FORMAT_INVALID", "reason": str(exc), "retryable": False})
    except Exception as exc:  # renderer failure of one artifact must not stop the others (AC-025-03)
        payloads["architecture.svg"] = ("diagram_image", "image/svg+xml", None,
                                        {"code": "RENDER_FAILED", "reason": f"{type(exc).__name__}: {exc}"[:500], "retryable": True})
    return data, payloads


def _bundle(run_id: str, data: dict, payloads: dict) -> dict:
    artifacts = [_artifact(run_id, k, p, m, t.encode("utf-8") if t is not None else None, err)
                 for p, (k, m, t, err) in payloads.items()]
    return dict(data, artifacts=sorted(artifacts, key=lambda a: a["path"]))


def render(verified: dict, run_id: str, repository_name: str, output: Path, source_link: dict | None = None,
           renderers: dict | None = None) -> dict:
    data, payloads = plan_bundle(verified, run_id, repository_name, source_link, renderers)
    bundle = _bundle(run_id, data, payloads)
    _publish(output, {p: t for p, (_, _, t, _) in payloads.items() if t is not None}, dump(bundle))
    return bundle


def retry_artifact(output: Path, artifact_id: str, renderers: dict | None = None, _crash_after_install=False) -> dict:
    """API-008 §7: rebuild one failed, retryable artifact from the committed result.json. Ready files keep their bytes;
    the manifest is replaced last, so a crash before that leaves the artifact `failed` and the stray file unserved."""
    manifest_path = output / "manifest.json"
    bundle = json.loads(manifest_path.read_text(encoding="utf-8"))
    art = next((a for a in bundle["artifacts"] if a["artifact_id"] == artifact_id), None)
    if art is None:
        raise ExportError("INVALID_INPUT", f"Không có artifact {artifact_id}")
    if art["status"] == "ready":
        return bundle
    if not (art["error"] or {}).get("retryable"):
        raise ExportError("ARTIFACT_NOT_RETRYABLE", art["error"]["reason"] if art["error"] else "Artifact không ở trạng thái failed")
    ctx = bundle["export_context"]
    if (ctx["renderer_version"], ctx["template_version"]) != (RENDERER_VERSION, TEMPLATE_VERSION):
        raise ExportError("VERSION_UNAVAILABLE", "Phiên bản renderer/template hiện tại khác phiên bản đã dùng; không tự nâng")
    for other in bundle["artifacts"]:
        if other["status"] == "ready" and sha((output / other["path"]).read_bytes()) != other["sha256"]:
            raise ExportError("INVALID_INPUT", f"File ready {other['path']} đã bị đổi; không retry trên bộ không nhất quán")
    if art["kind"] == "diagram_image" and next(a for a in bundle["artifacts"] if a["kind"] == "diagram_source")["status"] != "ready":
        raise ExportError("ARTIFACT_NOT_RETRYABLE", "DEPENDENCY_UNAVAILABLE: architecture.mmd chưa ready")
    data = {k: v for k, v in bundle.items() if k != "artifacts"}
    if dump(data).encode("utf-8") != (output / "result.json").read_bytes():
        raise ExportError("INVALID_INPUT", "result.json khác manifest; không retry")
    _, payloads = plan_bundle(data["result"], data["run_id"], ctx["repository_name"], ctx.get("source_link"), renderers)
    kind, media, text, err = payloads[art["path"]]
    new = _artifact(data["run_id"], kind, art["path"], media, text.encode("utf-8") if text is not None else None, err)
    if text is not None:
        target = (output / art["path"]).resolve()
        if output.resolve() not in target.parents:
            raise ExportError("OUTPUT_UNSAFE", f"Path {art['path']} thoát vùng output")
        tmp = target.with_name(f".{target.name}.retry-{os.getpid()}")
        tmp.write_bytes(text.encode("utf-8"))
        os.replace(tmp, target)
        if _crash_after_install:
            raise RuntimeError("simulated crash after install, before manifest")
    bundle["artifacts"] = sorted([new if a["artifact_id"] == artifact_id else a for a in bundle["artifacts"]],
                                 key=lambda a: a["path"])
    tmp_manifest = manifest_path.with_name(f".manifest.json.retry-{os.getpid()}")
    try:
        tmp_manifest.write_bytes(dump(bundle).encode("utf-8"))
        os.replace(tmp_manifest, manifest_path)
    except OSError as exc:  # old manifest stays; the new file is not referenced, so it is not served
        tmp_manifest.unlink(missing_ok=True)
        raise ExportError("PUBLISH_FAILED", f"Không thay được manifest: {type(exc).__name__}") from None
    return bundle


def _publish(output: Path, texts: dict[str, str], manifest: str):
    """Write into a fresh staging directory owned by this run, then rename once. Never touch other folders."""
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ExportError("OUTPUT_UNSAFE", f"Output {output} đã tồn tại và không rỗng; không ghi đè")
    longest = max([len(str(output.resolve() / rel)) for rel in texts] + [0]) + len(".l3slice-xxxxxxxx") + 1
    if os.name == "nt" and longest >= MAX_PATH_WINDOWS:
        # API-008 §4: the whole path must be valid on the output platform; no second silent cut
        raise ExportError("OUTPUT_UNSAFE", f"Đường dẫn file dài {longest} ký tự, vượt giới hạn {MAX_PATH_WINDOWS - 1} của "
                                           "Windows; chọn thư mục output ngắn hơn")
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=f".{output.name}.l3slice-", dir=output.parent))
    except OSError as exc:
        raise ExportError("PUBLISH_FAILED", f"Không tạo được thư mục tạm: {type(exc).__name__}") from None
    try:
        root = staging.resolve()
        for rel, text in texts.items():
            target = (staging / rel).resolve()
            if root not in target.parents:
                raise ExportError("OUTPUT_UNSAFE", f"Path {rel} thoát vùng output")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(text.encode("utf-8"))
        (staging / "manifest.json").write_bytes(manifest.encode("utf-8"))
        if output.exists():
            output.rmdir()
        staging.rename(output)
    except OSError as exc:
        shutil.rmtree(staging, ignore_errors=True)  # only the directory this call created
        raise ExportError("PUBLISH_FAILED", f"Ghi output thất bại: {type(exc).__name__}: {exc.strerror or exc}"[:500]) from None
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
