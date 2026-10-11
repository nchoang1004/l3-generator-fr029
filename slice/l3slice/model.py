"""CMP-005 subset: membership from a fixture file and contract owners (API-005 §3, §3.2).

No grouping algorithm is chosen here (D-03 stays open). Static edges are built by code (API-005 §4):
`resolved-target` from resolved references, `event-binding` from matching publish/consume points.
"""
from __future__ import annotations

from .common import SCHEMA_VERSION, compact, is_known, sha

PARTITION_VERSION = "fixture-membership-v1"
CONTRACT_KINDS = {"route": "api", "table": "table", "event": "event"}
MAX_NODES = 50


class BuildError(ValueError):
    """API-005 BuildError; `code` follows the schema enum."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def _components(snapshot: dict, unit_id: str, membership: dict, evidence: list[dict]) -> list[dict]:
    by_path = {f["path"]: f["file_id"] for f in snapshot["files"]}
    seen = [p for group in membership["components"] for p in group["files"]]
    if sorted(seen) != sorted(by_path) or len(seen) != len(set(seen)):
        missing = sorted(set(by_path) - set(seen))
        extra = sorted(set(seen) - set(by_path))
        raise BuildError("INVALID_INPUT", f"Membership phải phủ mỗi file đúng một lần; thiếu {missing}, thừa {extra}")
    components = []
    for group in membership["components"]:
        files = sorted(by_path[p] for p in group["files"])
        ev_ids = sorted({e["id"] for e in evidence if e["file_id"] in files})
        comp = {"id": "cmp_" + sha(compact([snapshot["snapshot_id"], unit_id, files]).encode()),
                "unit_id": unit_id, "name": group["name"], "member_file_ids": files, "grouping_source": "code",
                "confidence": "inferred",
                "inference_reason": "Membership soạn sẵn trong fixture, không phải kết quả thuật toán chia nhóm",
                "completeness": "full" if ev_ids else "partial", "evidence_ids": ev_ids,
                "label_status": "path_fallback"}
        if not ev_ids:
            comp["completeness_reason"] = "Component chưa có dữ kiện nào được trích"
        components.append(comp)
    if len(components) > MAX_NODES:
        raise BuildError("INTERNAL_INVARIANT", f"Model có {len(components)} node, vượt trần {MAX_NODES}")
    return sorted(components, key=lambda c: c["id"])


def contract_owners(facts: list[dict], components: list[dict]) -> list[dict]:
    """Rule `declaration-file` / `1-draft`."""
    owners = []
    for fact in facts:
        if fact["kind"] not in CONTRACT_KINDS:
            continue
        entry = {"fact_id": fact["id"], "contract_kind": CONTRACT_KINDS[fact["kind"]], "component_id": None,
                 "rule_id": "declaration-file", "rule_version": "1-draft", "evidence_ids": []}
        decl = fact["attributes"].get("declaration_evidence_id")
        ev = next((e for e in fact["evidence"] if is_known(decl) and e["id"] == decl["value"]), None)
        if ev is None:
            entry["reason"] = "Không có declaration_evidence_id known trỏ evidence của fact"
        else:
            match = [c for c in components if c["unit_id"] == fact["unit_id"] and ev["file_id"] in c["member_file_ids"]]
            if len(match) == 1:
                entry.update(component_id=match[0]["id"], evidence_ids=[ev["id"]])
            else:
                entry["reason"] = f"File khai báo thuộc {len(match)} component; cần đúng một"
        owners.append(entry)
    return owners


RELATION = {"calls": "calls", "depends": "depends_on", "reads": "depends_on"}
CHANNEL = ("broker", "namespace", "serialization_context", "topic")


def _component_of(file_id: str, components: list[dict]) -> str | None:
    return next((c["id"] for c in components if file_id in c["member_file_ids"]), None)


def _same(a, b) -> bool:
    if a is None or b is None:
        return False
    if a.get("state") == b.get("state") == "not_applicable":
        return True
    return is_known(a) and is_known(b) and a["value"] == b["value"]


def static_edges(snapshot_id: str, facts: list[dict], components: list[dict]) -> list[dict]:
    """Edges A→B between different components. One edge per (A, B, relation); every cited fact kept."""
    by_id = {f["id"]: f for f in facts}
    groups = {}
    for f in facts:
        if f["kind"] != "reference" or f["resolution"] != "resolved" or not f["target_fact_ids"]:
            continue
        target = by_id.get(f["target_fact_ids"][0])
        if target is None:
            continue
        a = _component_of(f["evidence"][0]["file_id"], components)
        b = _component_of(target["evidence"][0]["file_id"], components)
        rel = RELATION.get(f["attributes"]["reference_kind"]["value"])
        if a and b and a != b and rel:
            groups.setdefault((a, b, rel, "resolved-target"), []).append(f)
    events = [f for f in facts if f["kind"] == "event" and is_known(f["attributes"].get("action"))]
    for p in [e for e in events if e["attributes"]["action"]["value"] == "publish"]:
        for c in [e for e in events if e["attributes"]["action"]["value"] == "consume"]:
            if all(_same(p["attributes"].get(k), c["attributes"].get(k)) for k in CHANNEL):
                a = _component_of(p["evidence"][0]["file_id"], components)
                b = _component_of(c["evidence"][0]["file_id"], components)
                if a and b and a != b:
                    groups.setdefault((a, b, "publishes", "event-binding"), []).extend([p, c])
    edges = []
    for (a, b, rel, rule), cited in sorted(groups.items()):
        cited = list({f["id"]: f for f in cited}.values())
        inferred = [f for f in cited if f["confidence"] == "inferred"]
        edge = {"id": "edge_" + sha(compact([snapshot_id, a, b, rel]).encode()), "source_component_id": a,
                "target_component_id": b, "relation_type": rel, "fact_ids": sorted(f["id"] for f in cited),
                "evidence_ids": sorted({e["id"] for f in cited for e in f["evidence"]}), "origin": "static",
                "confidence": "inferred" if inferred else "exact", "completeness": "full",
                "rule_id": rule, "rule_version": "1-draft"}
        if inferred:
            edge["inference_reason"] = "Có reference được trích dẫn mang nhãn inferred (đích theo luồng giá trị)"
        edges.append(edge)
    return edges


def build(snapshot: dict, unit_id: str, fact_set: dict, membership: dict) -> dict:
    if membership.get("partition_version") != PARTITION_VERSION:
        raise BuildError("PARTITION_POLICY_UNAVAILABLE", "Lát cắt chỉ nhận fixture-membership-v1")
    evidence = [e for f in fact_set["facts"] for e in f["evidence"]]
    components = _components(snapshot, unit_id, membership, evidence)
    return {"schema_version": SCHEMA_VERSION, "snapshot_id": snapshot["snapshot_id"],
            "partition_version": PARTITION_VERSION, "components": components, "external_systems": [],
            "edges": static_edges(snapshot["snapshot_id"], fact_set["facts"], components),
            "contract_owners": contract_owners(fact_set["facts"], components),
            "limitations": [
                {"code": "MODEL_NOT_RUN", "message": "Không gọi provider; tên component lấy từ membership",
                 "stage": "model", "affected_ids": [c["id"] for c in components]}],
            "rejected_proposals": []}
