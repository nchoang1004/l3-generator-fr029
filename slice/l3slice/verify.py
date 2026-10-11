"""CMP-007: evidence ranges, MEMBER-SOURCE, CONTRACT-FIELD, CONTRACT-OWNER, resolved-target, event-binding,
LABEL-DIRECT (API-007 §1–2), and the snapshot check when evidence is opened later (AC-023-03)."""
from __future__ import annotations

import ast
import copy
import re
from pathlib import Path

from .common import SCHEMA_VERSION, is_known, sha, unknown


class VerificationError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def _text(sources: dict[str, bytes], ev: dict) -> str:
    """Text of an evidence range (API-002: lines 1-based; columns 0-based code points, end exclusive)."""
    lines = sources[ev["path"]].decode("utf-8").splitlines()[ev["start_line"] - 1:ev["end_line"]]
    if ev["start_column"] is None:
        return "\n".join(lines)
    if len(lines) == 1:
        return lines[0][ev["start_column"]:ev["end_column"]]
    return "\n".join([lines[0][ev["start_column"]:], *lines[1:-1], lines[-1][:ev["end_column"]]])


def _check_evidence(snapshot: dict, sources: dict[str, bytes], ev: dict):
    files = {f["file_id"]: f for f in snapshot["files"]}
    f = files.get(ev["file_id"])
    if ev["snapshot_id"] != snapshot["snapshot_id"] or f is None or f["path"] != ev["path"]:
        raise VerificationError("SNAPSHOT_MISMATCH", f"Evidence {ev['id']} không thuộc snapshot")
    raw = sources[ev["path"]]
    if sha(raw) != ev["sha256"] or not 1 <= ev["start_line"] <= ev["end_line"] <= len(raw.decode("utf-8").splitlines()):
        raise VerificationError("SNAPSHOT_MISMATCH", f"Evidence {ev['id']} sai hash hoặc ngoài file")


def _string_piece(text: str) -> str | None:
    try:
        value = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        return None
    return value if isinstance(value, str) else None


def _field_check(field: dict, literal, evidence: dict, sources, ignore_case=False, pieces=False) -> dict:
    """Return the field, or an unknown replacement when its evidence does not prove it.
    `pieces`: the value is joined from several string literals (prefix + path); each literal must occur in it."""
    if not is_known(field):
        return field
    evs = [evidence.get(i) for i in field["evidence_ids"]]
    if any(e is None for e in evs):
        return unknown("EVIDENCE_MISSING: evidence của trường không thuộc fact")
    if pieces and literal is not None and len(evs) > 1:
        parts = [_string_piece(_text(sources, e)) for e in evs]
        def segs(text):
            return sorted(s for s in text.split("/") if s)
        if any(p is None for p in parts) or segs(literal) != sorted(s for p in parts for s in segs(p)):
            return unknown("VALUE_NOT_IN_EVIDENCE: path không ghép được từ các literal trong evidence")
        return field
    if literal is not None:
        texts = [_text(sources, e) for e in evs]
        wanted = [str(x) for x in literal] if isinstance(literal, list) else [literal]
        if ignore_case:
            wanted, texts = [w.lower() for w in wanted], [t.lower() for t in texts]
        if not all(any(_occurs(w, t) for t in texts) for w in wanted):
            return unknown("VALUE_NOT_IN_EVIDENCE: giá trị không có nguyên văn trong evidence")
    return field


def _occurs(wanted: str, text: str) -> bool:
    """The value is the whole literal of the range, or a whole token in it. `20` does not occur in `200`."""
    try:
        value = ast.literal_eval(text.strip())
    except (ValueError, SyntaxError, MemoryError, RecursionError):
        value = None
    if isinstance(value, (str, int)) and not isinstance(value, bool) and str(value) == wanted:
        return True
    return re.search(rf"(?<![\w]){re.escape(wanted)}(?![\w])", text) is not None


def _contract_fields(fact: dict, sources) -> list[str]:
    """Rule CONTRACT-FIELD / 1-draft. Mutates fact; returns field paths turned unknown."""
    evidence = {e["id"]: e for e in fact["evidence"]}
    attrs, changed = fact["attributes"], []

    def apply(container, key, literal, path, ignore_case=False, pieces=False):
        new = _field_check(container[key], literal, evidence, sources, ignore_case, pieces)
        if new is not container[key]:
            container[key] = new
            changed.append(path)

    rule = attrs.get("name_rule")
    codes = attrs.get("status_codes") if fact["kind"] == "route" else None
    if is_known(codes) and not (isinstance(codes["value"], list) and all(
            isinstance(c, int) and not isinstance(c, bool) and 100 <= c <= 599 for c in codes["value"])):
        attrs["status_codes"] = unknown("VALUE_OUT_OF_RANGE: status code HTTP phải là số nguyên 100–599")
        changed.append("/attributes/status_codes")
    status_rule = attrs.get("status_rule") if fact["kind"] == "route" else None
    if is_known(status_rule) and is_known(attrs.get("status_codes")):
        ev = evidence.get(attrs["status_codes"]["evidence_ids"][0])
        text = _text(sources, ev) if ev else ""
        codes = attrs["status_codes"]["value"]
        ok = (status_rule["value"] == "fastapi-status-default-v1" and codes == [200] and "status_code" not in text) or \
             (status_rule["value"] == "starlette-status-constant-v1" and len(codes) == 1
              and re.search(rf"\bHTTP_{codes[0]}_\w+", text) is not None)
        if not ok:
            attrs["status_codes"] = unknown("VALUE_NOT_IN_EVIDENCE: status không khớp quy tắc đã ghi")
            changed.append("/attributes/status_codes")
    for key, value in list(attrs.items()):
        literal = None
        if is_known(value):
            if fact["kind"] == "route" and key == "status_codes" and is_known(status_rule):
                pass  # checked above against its rule; the number is not written in the source
            elif fact["kind"] == "route" and key in ("path", "method", "status_codes"):
                literal = value["value"]
            elif fact["kind"] == "table" and key == "name" and not is_known(rule):
                literal = value["value"]
            elif fact["kind"] == "event" and key == "topic":
                literal = value["value"]
        apply(attrs, key, literal, "/attributes/" + key, ignore_case=fact["kind"] == "route" and key == "method",
              pieces=fact["kind"] == "route" and key == "path")
    if fact["kind"] == "table" and is_known(rule) and is_known(attrs.get("name")):
        # sqlmodel-default-tablename-v1: the name must be the class name in lower case
        ev = evidence.get(attrs["name"]["evidence_ids"][0])
        m = re.search(r"class\s+(\w+)", _text(sources, ev)) if ev else None
        if not m or m.group(1).lower() != attrs["name"]["value"] or rule["value"] != "sqlmodel-default-tablename-v1":
            attrs["name"] = unknown("VALUE_NOT_IN_EVIDENCE: tên bảng không khớp quy tắc đã ghi")
            changed.append("/attributes/name")
    for key in ("columns", "parameters", "fields", "bodies"):
        if fact["kind"] in ("table", "route", "request_model", "response_model") and is_known(attrs.get(key)):
            for i, item in enumerate(attrs[key]["value"]):
                if not isinstance(item, dict):
                    continue
                for sub in list(item):
                    if not isinstance(item[sub], dict) or "state" not in item[sub]:
                        continue
                    literal = item[sub]["value"] if key == "columns" and sub == "name" and is_known(item[sub]) else None
                    apply(item, sub, literal, f"/attributes/{key}/value/{i}/{sub}")
    if changed:
        fact["completeness"] = "partial"
        fact["completeness_reason"] = (fact.get("completeness_reason", "") + "; kiểm trường: " + ", ".join(changed)).lstrip("; ")
    return changed


BINDING_KEYS = ("broker", "namespace", "serialization_context", "topic")


def _declaration_file(fact: dict) -> str | None:
    decl = fact["attributes"].get("declaration_evidence_id")
    ev = next((e for e in fact["evidence"] if is_known(decl) and e["id"] == decl["value"]), None)
    return ev["file_id"] if ev else None


def _resolved_target(edge: dict, by_fact: dict, src: dict, tgt: dict) -> str | None:
    """Rule resolved-target / 1-draft: every cited reference is resolved, its call site is in A, its target in B."""
    refs = [by_fact.get(i) for i in edge["fact_ids"]]
    refs = [f for f in refs if f is not None and f["kind"] == "reference"]
    if not refs:
        return "REFERENCE_UNRESOLVED: cạnh không trích dẫn reference nào"
    for f in refs:
        if f["resolution"] != "resolved" or not f["target_fact_ids"] or f["target_fact_ids"][0] not in by_fact:
            return "REFERENCE_UNRESOLVED: reference chưa nối được đích"
        if f["evidence"][0]["file_id"] not in src["member_file_ids"]:
            return "ENDPOINT_MISMATCH: chỗ gọi không thuộc component nguồn"
        if by_fact[f["target_fact_ids"][0]]["evidence"][0]["file_id"] not in tgt["member_file_ids"]:
            return "ENDPOINT_MISMATCH: đích không thuộc component đích"
    return None


def _edge_problem(edge: dict, by_fact: dict, components: dict) -> str | None:
    """Rules resolved-target and event-binding (API-007 §2). http-binding and config-binding are not implemented yet."""
    src, tgt = components.get(edge["source_component_id"]), components.get(edge["target_component_id"])
    if edge["rule_id"] == "resolved-target" and edge["relation_type"] in ("calls", "depends_on"):
        if src is None or tgt is None:
            return "ENDPOINT_MISMATCH: endpoint không phải component đã accepted"
        return _resolved_target(edge, by_fact, src, tgt)
    if edge["rule_id"] != "event-binding" or edge["relation_type"] not in ("publishes", "consumes"):
        return f"RULE_UNSUPPORTED: chưa hiện thực rule {edge['rule_id']}"
    if src is None or tgt is None:
        return "ENDPOINT_MISMATCH: endpoint không phải component đã accepted"
    facts = [by_fact.get(i) for i in edge["fact_ids"]]
    if len(facts) != 2 or any(f is None or f["kind"] != "event" for f in facts):
        return "REFERENCE_UNRESOLVED: cạnh event cần đúng hai fact event"
    actions = {f["attributes"]["action"]["value"]: f for f in facts if is_known(f["attributes"].get("action"))}
    if set(actions) != {"publish", "consume"}:
        return "ENDPOINT_MISMATCH: cần một điểm publish và một điểm consume"
    prod, cons = actions["publish"], actions["consume"]
    for key in BINDING_KEYS:
        a, b = prod["attributes"].get(key), cons["attributes"].get(key)
        if a and b and a.get("state") == b.get("state") == "not_applicable":
            continue  # e.g. Kafka has no namespace on either side
        if not (is_known(a) and is_known(b)):
            return f"BROKER_UNKNOWN: {key} chưa biết ở một đầu; không nối chỉ vì cùng tên topic"
        if a["value"] != b["value"]:
            return f"TOPIC_MISMATCH: {key} khác nhau"
    sender, receiver = (src, tgt) if edge["relation_type"] == "publishes" else (tgt, src)
    if _declaration_file(prod) not in sender["member_file_ids"] or _declaration_file(cons) not in receiver["member_file_ids"]:
        return "ENDPOINT_MISMATCH: chiều cạnh không khớp nơi gửi/nhận"
    return None


def verify(snapshot: dict, sources: dict[str, bytes], inventory: dict, fact_set: dict, model: dict) -> dict:
    snap = snapshot["snapshot_id"]
    if not (inventory["snapshot_id"] == fact_set["snapshot_id"] == model["snapshot_id"] == snap):
        raise VerificationError("SNAPSHOT_MISMATCH", "Inventory, facts và model khác snapshot")
    facts = copy.deepcopy(fact_set)
    model = copy.deepcopy(model)
    decisions, limitations = [], []
    for fact in facts["facts"]:
        for ev in fact["evidence"]:
            _check_evidence(snapshot, sources, ev)
        changed = _contract_fields(fact, sources)
        if changed:
            limitations.append({"code": "CONTRACT_FIELD_UNPROVEN", "message": ", ".join(changed),
                                "stage": "verification", "affected_ids": [fact["id"]]})
    by_fact = {f["id"]: f for f in facts["facts"]}
    kept = []
    for comp in model["components"]:
        comp_facts = sorted(f["id"] for f in facts["facts"] if f["evidence"][0]["file_id"] in comp["member_file_ids"])
        if comp["evidence_ids"]:
            kept.append(comp)
            decisions.append({"subject_id": comp["id"], "verdict": "accepted", "rule_id": "MEMBER-SOURCE",
                              "rule_version": "1", "fact_ids": comp_facts, "evidence_ids": comp["evidence_ids"],
                              "reason": "File thành viên có trong snapshot; component có evidence nguồn"})
        else:
            decisions.append({"subject_id": comp["id"], "verdict": "rejected", "rule_id": "MEMBER-SOURCE",
                              "rule_version": "1", "fact_ids": [], "evidence_ids": [],
                              "reason": "Component không có dữ kiện nào"})
            limitations.append({"code": "COMPONENT_WITHOUT_EVIDENCE", "message": comp["name"],
                                "stage": "verification", "affected_ids": comp["member_file_ids"]})
    model["components"] = kept
    accepted = {c["id"]: c for c in kept}
    for owner in model["contract_owners"]:  # CONTRACT-OWNER / 1-draft
        if owner["component_id"] is None:
            continue
        fact = by_fact[owner["fact_id"]]
        decl = fact["attributes"].get("declaration_evidence_id")
        ev = next((e for e in fact["evidence"] if is_known(decl) and e["id"] == decl["value"]), None)
        comp = accepted.get(owner["component_id"])
        if ev is None or comp is None or owner["evidence_ids"] != [ev["id"]] or ev["file_id"] not in comp["member_file_ids"]:
            owner.update(component_id=None, evidence_ids=[], reason="OWNER_UNPROVEN: owner không chứa file khai báo")
    kept_edges = []
    for edge in model["edges"]:
        problem = _edge_problem(edge, by_fact, accepted)
        if not problem and edge["confidence"] == "exact" and any(
                by_fact[i]["confidence"] == "inferred" for i in edge["fact_ids"] if i in by_fact):
            # LABEL-DIRECT / 1: exact only when every cited fact is exact
            edge["confidence"], edge["inference_reason"] = "inferred", "Có fact được trích dẫn mang nhãn inferred"
        decisions.append({"subject_id": edge["id"], "verdict": "rejected" if problem else "accepted",
                          "rule_id": edge["rule_id"], "rule_version": edge["rule_version"],
                          "fact_ids": edge["fact_ids"] if not problem else [], "evidence_ids": edge["evidence_ids"] if not problem else [],
                          "reason": problem or ("Reference đã nối đích; chỗ gọi thuộc A, đích thuộc B"
                                                if edge["rule_id"] == "resolved-target" else
                                                "Hai đầu cùng broker/namespace/serialization/topic; chiều gửi → nhận đúng")})
        if problem:
            limitations.append({"code": "EDGE_REJECTED", "message": problem, "stage": "verification",
                                "affected_ids": [edge["id"]]})
        else:
            kept_edges.append(edge)
    model["edges"] = kept_edges
    evidence_index = {e["id"]: e for f in facts["facts"] for e in f["evidence"]}
    return {"schema_version": SCHEMA_VERSION, "snapshot_id": snap, "inventory": inventory, "facts": facts,
            "model": model, "evidence_index": [evidence_index[k] for k in sorted(evidence_index)],
            "decisions": sorted(decisions, key=lambda d: d["subject_id"]),
            "limitations": inventory["limitations"] + facts["limitations"] + model["limitations"] + limitations}


def open_evidence(root: Path, ev: dict) -> str:
    """AC-023-03: read evidence from disk again; a file that changed or vanished since the snapshot is refused."""
    path = (Path(root) / ev["path"]).resolve()
    if Path(root).resolve() not in path.parents or not path.is_file():
        raise VerificationError("SNAPSHOT_MISMATCH", "File bằng chứng không còn trong source")
    raw = path.read_bytes()
    if sha(raw) != ev["sha256"]:
        raise VerificationError("SNAPSHOT_MISMATCH", "Snapshot không còn khớp; không dùng nội dung mới làm bằng chứng")
    return _text({ev["path"]: raw}, ev)
