"""CMP-005 model tasks through CMP-006 (API-005 §3–5, API-006 §3).

The model only annotates: names, descriptions, roles and edge labels for IDs that code made, and edge proposals that
must be proven by the same rules as static edges. It never changes membership, IDs or facts. `group_flat` is written
and tested, but not wired into the pipeline: no partition policy is chosen yet (D-03 open).
"""
from __future__ import annotations

import copy

from . import gateway
from .common import compact, sha
from .model import MAX_NODES, static_edges

NOT_RUN = "MODEL_NOT_RUN"


def _base(run_id, snapshot_id, kind, scope_id, file_ids, fact_set, components, edges, max_out, request_id):
    return {"schema_version": "0.1.0", "run_id": run_id, "request_id": request_id, "snapshot_id": snapshot_id,
            "kind": kind, "scope_id": scope_id, "file_ids": sorted(file_ids), "fact_set": fact_set,
            "components": components, "edges": edges, "prompt_version": gateway.PROMPT_VERSION,
            "tool_version": gateway.TOOL_VERSION, "max_output_tokens": max_out}


def _file_of(fact):
    return fact["evidence"][0]["file_id"] if fact["evidence"] else None


def label_request(run_id: str, fact_set: dict, arch: dict, comp: dict, max_out: int = 1000) -> dict:
    """Facts of member files plus target facts of the component's edges; fixed before the task (API-006 §3)."""
    edges = [e for e in arch["edges"] if comp["id"] in (e["source_component_id"], e["target_component_id"])]
    by_id = {f["id"]: f for f in fact_set["facts"]}
    wanted = {f["id"] for f in fact_set["facts"] if _file_of(f) in comp["member_file_ids"]}
    for e in edges:
        for fid in e["fact_ids"]:
            wanted |= {fid, *by_id[fid]["target_fact_ids"]} if fid in by_id else set()
    facts = dict(fact_set, facts=[f for f in fact_set["facts"] if f["id"] in wanted])
    return _base(run_id, arch["snapshot_id"], "label_components", f"component:{comp['id']}", comp["member_file_ids"],
                 facts, [comp], edges, max_out, f"label:{comp['id']}")


def edge_request(run_id: str, fact_set: dict, arch: dict, file_ids, max_out: int = 4000) -> dict:
    return _base(run_id, arch["snapshot_id"], "propose_edges", f"repository:{arch['snapshot_id']}", file_ids, fact_set,
                 arch["components"], arch["edges"], max_out, f"edges:{arch['snapshot_id']}")


def group_request(run_id: str, snapshot_id: str, fact_set: dict, flat_units: list, max_out: int = 4000) -> dict:
    req = _base(run_id, snapshot_id, "group_flat", f"repository:{snapshot_id}",
                {f for u in flat_units for f in u["file_ids"]}, fact_set, [], [], max_out, f"group:{snapshot_id}")
    req["flat_units"] = flat_units
    return req


def _reject(arch, proposal_id, kind, code, message, ids):
    arch["rejected_proposals"].append({"proposal_id": proposal_id, "kind": kind, "reason_code": code,
                                       "message": message[:1000], "referenced_ids": sorted(set(ids))})


def _failed(arch, resp, affected):
    arch["limitations"].append({"code": resp["error"]["code"], "message": resp["error"]["message"],
                                "stage": "model", "affected_ids": sorted(affected)})


def apply_labels(arch: dict, fact_set: dict, comp_id: str, resp: dict) -> None:
    """Annotation only. A label citing a fact outside the component's files is rejected (OUTSIDE_SCOPE)."""
    if resp["status"] != "ok":
        _failed(arch, resp, [comp_id])
        return
    comp = next(c for c in arch["components"] if c["id"] == comp_id)
    own = {f["id"] for f in fact_set["facts"] if _file_of(f) in comp["member_file_ids"]}
    for label in resp["result"]["component_labels"]:
        pid = f"{resp['request_id']}:{label['component_id']}"
        if label["component_id"] != comp_id:
            _reject(arch, pid, "label_components", "OUTSIDE_SCOPE", "Nhãn cho component ngoài scope", [label["component_id"]])
        elif not set(label["fact_ids"]) <= own:
            _reject(arch, pid, "label_components", "OUTSIDE_SCOPE", "Nhãn dẫn fact không thuộc file của component",
                    label["fact_ids"])
        else:
            comp.update(name=label["name"], description=label["description"], role=label["role"],
                        label_status="model_labeled", provenance=resp["provenance"])
    edges = {e["id"]: e for e in arch["edges"] if comp_id in (e["source_component_id"], e["target_component_id"])}
    for label in resp["result"]["edge_labels"]:
        edge = edges.get(label["edge_id"])
        if edge is None or not set(label["fact_ids"]) <= set(edge["fact_ids"]):
            _reject(arch, f"{resp['request_id']}:{label['edge_id']}", "label_components", "OUTSIDE_SCOPE",
                    "Nhãn cạnh ngoài scope hoặc dẫn fact không thuộc cạnh", [label["edge_id"], *label["fact_ids"]])
        else:
            edge["label"] = label["label"]


def apply_proposals(arch: dict, fact_set: dict, resp: dict) -> None:
    """A proposal is kept only if the static rules prove it from the cited facts (binding-v1-draft, API-005 §4)."""
    if resp["status"] != "ok":
        _failed(arch, resp, [c["id"] for c in arch["components"]])
        return
    by_id = {f["id"]: f for f in fact_set["facts"]}
    comps = {c["id"]: c for c in arch["components"]}
    for p in resp["result"]["proposals"]:
        src, tgt = comps.get(p["source_component_id"]), comps.get(p["target_component_id"])
        ids = [p["source_component_id"], p["target_component_id"], *p["fact_ids"]]
        if src is None or tgt is None or not all(i in by_id for i in p["fact_ids"]):
            _reject(arch, p["proposal_id"], "propose_edges", "UNKNOWN_ID", "Component hoặc fact không có trong model", ids)
            continue
        cited = [by_id[i] for i in p["fact_ids"]]
        files = {_file_of(f) for f in cited}
        if not (files & set(src["member_file_ids"]) and files & set(tgt["member_file_ids"])):
            _reject(arch, p["proposal_id"], "propose_edges", "MISSING_ENDPOINT_EVIDENCE",
                    "Không có fact được trích dẫn ở cả hai đầu", ids)
            continue
        targets = [by_id[t] for f in cited for t in f["target_fact_ids"] if t in by_id]
        proven = [e for e in static_edges(arch["snapshot_id"], cited + targets, [src, tgt])
                  if (e["source_component_id"], e["target_component_id"], e["relation_type"])
                  == (src["id"], tgt["id"], p["relation_type"])]
        if not proven:
            _reject(arch, p["proposal_id"], "propose_edges", "UNPROVEN_BINDING",
                    "Rule tĩnh không chứng minh được loại, chiều hoặc đích từ fact được trích dẫn", ids)
            continue
        existing = next((e for e in arch["edges"] if e["id"] == proven[0]["id"]), None)
        if existing is not None:  # keep the static edge, add the proposal's provenance
            existing["provenance"] = existing.get("provenance", []) + resp["provenance"]
        else:
            arch["edges"].append(dict(proven[0], origin="llm", confidence="inferred", provenance=resp["provenance"],
                                      inference_reason="Đề xuất của model, được rule tĩnh chứng minh từ fact trích dẫn"))
    arch["edges"].sort(key=lambda e: e["id"])


def apply_groups(arch_base: dict, unit_files: dict, resp: dict, partition_version: str) -> list:
    """Flat grouping: accept the whole proposal only if each file of each unit is in exactly one group; otherwise
    one fallback component per unit (API-005 §3). Returns the components."""
    snapshot_id = arch_base["snapshot_id"]

    def comp(unit_id, files, source, reason):
        c = {"id": "cmp_" + sha(compact([snapshot_id, unit_id, sorted(files)]).encode()), "unit_id": unit_id,
             "name": f"{unit_id} (chưa chia nhóm)" if source == "fallback" else f"Nhóm {len(files)} file",
             "member_file_ids": sorted(files), "grouping_source": source, "confidence": "inferred",
             "inference_reason": reason, "completeness": "partial" if source == "fallback" else "full",
             "evidence_ids": [], "label_status": "path_fallback"}
        if source == "fallback":
            c["completeness_reason"] = "Chưa chia nhóm được repo phẳng"
        if source == "llm":
            c["provenance"] = resp["provenance"]
        return c
    fallback = [comp(u, fs, "fallback", "Fallback một component cho mỗi unit") for u, fs in sorted(unit_files.items())]
    if resp["status"] != "ok":
        _failed(arch_base, resp, list(unit_files))
        return fallback
    groups = resp["result"]["groups"]
    for unit_id, files in unit_files.items():
        placed = [f for g in groups if g["unit_id"] == unit_id for f in g["file_ids"]]
        if sorted(placed) != sorted(files):
            _reject(arch_base, resp["request_id"], "group_flat", "MEMBERSHIP_MISMATCH",
                    f"Unit {unit_id}: nhóm thiếu, trùng hoặc thừa file", [unit_id])
            return fallback
    out = [comp(g["unit_id"], g["file_ids"], "llm", f"Chia nhóm bởi model theo {partition_version}") for g in groups]
    if len(out) > MAX_NODES:
        _reject(arch_base, resp["request_id"], "group_flat", "MEMBERSHIP_MISMATCH", "Vượt trần 50 node", [])
        return fallback
    return sorted(out, key=lambda c: c["id"])


def annotate(arch: dict, fact_set: dict, snapshot: dict, ctx: gateway.RunContext) -> dict:
    """Label tasks (Groq) then one edge proposal task (Gemini). Any failure keeps the static model (partial)."""
    arch = copy.deepcopy(arch)
    arch["limitations"] = [lim for lim in arch["limitations"] if lim["code"] != NOT_RUN]
    for comp in list(arch["components"]):
        resp = gateway.invoke_model(label_request(ctx.run_id, fact_set, arch, comp), ctx)
        apply_labels(arch, fact_set, comp["id"], resp)
    resp = gateway.invoke_model(edge_request(ctx.run_id, fact_set, arch, [f["file_id"] for f in snapshot["files"]]), ctx)
    apply_proposals(arch, fact_set, resp)
    return arch
