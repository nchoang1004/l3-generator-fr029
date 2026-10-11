"""FactSet (API-004) -> prediction document of golden v1 (`evaluation/golden/v1/prediction-schema.json`).

This is a measuring tool, not product code. It only renames; it does not add or repair facts.
Label mapping, so the scorer compares like with like:
- route: confidence exact (method/handler/registration are read directly); completeness partial when the full path is unknown.
- entity: confidence inferred only when the table name comes from a named framework rule; partial when the name is unknown.
- reference: exact / inferred / unresolved from the fact; context = call site `path:line:col`, or the call text if unresolved (D32).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from l3slice.common import is_known  # noqa: E402

LIMITS = {"PARSE_FAILED": "syntax_error_file", "RUNTIME_DEPENDENT_PREFIX": "runtime_dependent_prefix"}


def to_prediction(fact_set: dict, snapshot: dict, sources: dict[str, bytes], case_id: str, source_digest: str,
                  tool_revision: str) -> dict:
    files = {f["file_id"]: f for f in snapshot["files"]}
    lines_of = {p: len(raw.decode("utf-8", errors="replace").splitlines()) for p, raw in sources.items()}
    facts = fact_set["facts"]
    by_id = {f["id"]: f for f in facts}
    entities, evidence, out = {}, {}, []

    def entity_for_symbol(sym):
        a = sym["attributes"]
        ev = sym["evidence"][0]
        eid = f"{ev['path']}::{a['local_name']['value']}"
        kind = a["symbol_kind"]["value"]
        entities[eid] = {"id": eid, "path": ev["path"], "line_start": ev["start_line"], "line_end": ev["end_line"],
                         "symbol": a["local_name"]["value"], "kind": kind if kind in ("function", "class", "module", "variable") else "function"}
        return eid

    def module_entity(path):
        eid = f"{path}::__module__"
        n = max(lines_of.get(path, 1), 1)
        entities.setdefault(eid, {"id": eid, "path": path, "line_start": 1, "line_end": n, "symbol": "__module__", "kind": "module"})
        return eid

    def ev_ref(ev):
        rid = "e" + ev["id"].split(":", 1)[1][:16]
        evidence[rid] = {"id": rid, "path": ev["path"], "line_start": ev["start_line"], "line_end": ev["end_line"],
                         "sha256": ev["sha256"]}
        return rid

    symbols_by_q = {f["attributes"]["name"]["value"]: f for f in facts if f["kind"] == "symbol"}
    for f in facts:
        a = f["attributes"]
        refs = sorted({ev_ref(e) for e in f["evidence"]})
        base = {"id": f["id"], "evidence_refs": refs, "target_id": None}
        if f["kind"] == "route":
            handler = by_id.get(a["handler_fact_id"]["value"]) if is_known(a.get("handler_fact_id")) else None
            if handler is None:
                continue
            path_known = is_known(a.get("path"))
            attrs = {"method": a["method"]["value"], "path": a["path"]["value"] if path_known else None,
                     "condition": a["condition"]["value"] if is_known(a.get("condition")) else None}
            if not path_known and is_known(a.get("path_suffix")):
                attrs["path_suffix"] = a["path_suffix"]["value"]
            out.append({**base, "kind": "route", "source_id": entity_for_symbol(handler),
                        "context": a["registration_context"]["value"], "attributes": attrs, "confidence": "exact",
                        "completeness": "full" if path_known else "partial",
                        "reason": None if path_known else a["path"]["reason"]})
        elif f["kind"] == "table":
            decl = next(e for e in f["evidence"] if e["id"] == a["declaration_evidence_id"]["value"])
            sym = next((s for s in symbols_by_q.values() if s["evidence"][0]["id"] == decl["id"]), None)
            if sym is None:
                continue
            cols = a["columns"]["value"] if is_known(a.get("columns")) else []
            name_known = is_known(a.get("name"))
            rule = is_known(a.get("name_rule"))
            out.append({**base, "kind": "entity", "source_id": entity_for_symbol(sym), "context": "default",
                        "attributes": {"table": a["name"]["value"] if name_known else None,
                                       "columns": sorted(c["name"]["value"] for c in cols if is_known(c.get("name"))),
                                       "foreign_keys": sorted(f"{c['name']['value']}->{c['foreign_key']['value']['table']}."
                                                              f"{c['foreign_key']['value']['column']}"
                                                              for c in cols if is_known(c.get("foreign_key")))},
                        "confidence": "inferred" if rule else "exact",
                        "completeness": "full" if name_known else "partial",
                        "reason": (f.get("confidence_reason") if rule else None) or (None if name_known else a["name"]["reason"])})
        elif f["kind"] == "reference":
            src = symbols_by_q.get(a["source_symbol"]["value"])
            if src is None:
                continue
            target = by_id.get(f["target_fact_ids"][0]) if f["target_fact_ids"] else None
            site = f["evidence"][0]
            resolved = target is not None
            out.append({**base, "kind": "reference", "source_id": entity_for_symbol(src),
                        "target_id": entity_for_symbol(target) if resolved else None,
                        "context": f"{site['path']}:{site['start_line']}:{site['start_column']}" if resolved
                        else a["call_text"]["value"],
                        "attributes": {"relation": a["reference_kind"]["value"], "condition": None},
                        "confidence": ("inferred" if f["confidence"] == "inferred" else "exact") if resolved else "unresolved",
                        "completeness": "full" if resolved else "partial",
                        "reason": f.get("confidence_reason") if resolved and f["confidence"] == "inferred"
                        else (None if resolved else f.get("resolution_reason"))})
    for lim in fact_set["limitations"]:
        code = LIMITS.get(lim["code"])
        if code is None:
            continue
        for affected in lim["affected_ids"]:
            if lim["code"] == "PARSE_FAILED":
                file = files[affected]
                path = file["path"]
                source, ctx = module_entity(path), "file"
                rid = "e" + file["sha256"][:16]
                evidence[rid] = {"id": rid, "path": path, "line_start": 1, "line_end": max(lines_of.get(path, 1), 1),
                                 "sha256": file["sha256"]}
            else:
                route = by_id.get(affected)
                handler = by_id.get(route["attributes"]["handler_fact_id"]["value"]) if route else None
                if handler is None:
                    continue
                source, ctx = entity_for_symbol(handler), "prefix"
                decl = next(e for e in route["evidence"] if e["id"] == route["attributes"]["declaration_evidence_id"]["value"])
                rid = ev_ref(decl)
            out.append({"id": f"lim:{lim['code']}:{affected}", "kind": "limitation", "source_id": source, "target_id": None,
                        "context": ctx, "attributes": {"code": code, "details": lim["message"]},
                        "evidence_refs": [rid], "confidence": "exact", "completeness": "full", "reason": None})
    return {"schema_version": "0.1", "kind": "prediction", "case_id": case_id, "source_digest": source_digest,
            "status": "facts_only", "entities": sorted(entities.values(), key=lambda e: e["id"]),
            "evidence": sorted(evidence.values(), key=lambda e: e["id"]),
            "facts": out, "architectures": [{"id": "facts-only", "components": [], "edges": []}],
            "provenance": {"origin": "product", "author": "l3slice", "tool_revision": tool_revision, "unsupported": []}}
