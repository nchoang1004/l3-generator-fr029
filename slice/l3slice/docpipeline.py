"""FR-029 pipeline: snapshot + given components -> agent -> checked facts -> API files, README, result.json.

Components, the architecture data (`archdia.json`) and the diagram come from the FR-028 step; this module never
creates, splits or names components and never draws a diagram. Missing upstream input is reported, not replaced.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from . import snapshot as snapshot_mod
from .common import SCHEMA_VERSION, compact, is_known, sha
from .docagent import Budget, run_agent, run_oneshot
from .docfacts import LIMIT_KINDS, Claims, build_facts
from .docstatic import app_globals, component_relations, declared, event_edges, static_facts
from .render import (_artifact, _publish, cell, check_doc, code, dump, frontmatter, md, plan_events, render_api,
                     render_evt, render_tbl, slug, unique_slugs)
from .source_tools import SourceTools
from .tailieu import tai_lieu

PIPELINE_VERSION = "fr029-doc-v1"
KINDS = {"normal", "test", "migration", "other"}


class InputError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def _scope_kind(files, scope: dict) -> str | None:
    """"test" or "migration" when every .py file of a component has that reading scope (FR-028), else None."""
    kinds = {scope[p][0] for p in files if p.endswith(".py") and p in scope}
    return kinds.pop() if len(kinds) == 1 and kinds <= {"test", "migration"} else None


def load_components(membership: dict, snap: dict, unit_id: str, scope: dict | None = None) -> list[dict]:
    """Given components, checked against the snapshot: every file exactly once. Never edited here, except a
    missing kind: with `scope` (SourceTools.scope) a component of only test or migration files gets that kind."""
    paths = {f["path"]: f["file_id"] for f in snap["files"]}
    if isinstance(membership, dict) and membership.get("snapshot_id") not in (None, snap["snapshot_id"]):
        raise InputError("SNAPSHOT_MISMATCH", "Membership ghi snapshot_id khác snapshot của source")
    groups = membership.get("components") if isinstance(membership, dict) else None
    if not isinstance(groups, list):
        raise InputError("INVALID_INPUT", "Membership thiếu danh sách components")
    seen = [p for g in groups for p in g.get("files", [])]
    if sorted(seen) != sorted(paths) or len(seen) != len(set(seen)):
        raise InputError("INVALID_INPUT", f"Membership phải phủ mỗi file đúng một lần; thiếu {sorted(set(paths) - set(seen))}, "
                                          f"thừa {sorted(set(seen) - set(paths))}")
    names = [g.get("name") for g in groups]
    ids = [g.get("id") for g in groups if g.get("id") is not None]
    if len(set(names)) != len(names) or len(set(ids)) != len(ids):
        raise InputError("INVALID_INPUT", "Component trùng tên hoặc trùng id")
    out = []
    for g in groups:
        kind = g.get("kind") or (_scope_kind(g.get("files", []), scope) if scope else None) or "normal"
        if kind not in KINDS or not isinstance(g.get("name"), str) or not g["name"].strip():
            raise InputError("INVALID_INPUT", f"Component cần name và kind trong {sorted(KINDS)}")
        files = sorted(g["files"])
        out.append({"id": g.get("id") or "cmp_" + sha(compact([snap["snapshot_id"], unit_id, files]).encode()),
                    "name": g["name"], "kind": kind, "files": files, "member_file_ids": sorted(paths[p] for p in files),
                    "confidence": "exact", "completeness": "full"})
    return out


def compare_architecture(archdia: dict | None, snap: dict, routes: list[dict], owners: dict, components: list[dict]) -> dict:
    """AC-04. Route keys: (method, path or None, declaring file, decorator line). Never edits either side."""
    if archdia is None:
        return {"status": "not_evaluated", "reason": "Chưa được cấp archdia.json cùng snapshot"}
    if not isinstance(archdia, dict) or archdia.get("schema") != "archdia-fixture-v1":
        return {"status": "not_evaluated", "reason": "Định dạng archdia.json chưa được hỗ trợ (cần schema archdia-fixture-v1)"}
    if not archdia.get("snapshot_id"):
        return {"status": "not_evaluated", "reason": "archdia.json không ghi snapshot_id; không xác nhận được cùng snapshot"}
    if archdia["snapshot_id"] != snap["snapshot_id"]:
        return {"status": "failed", "reason": "archdia.json thuộc snapshot khác", "snapshot_id": archdia["snapshot_id"]}
    try:
        theirs = {(r["method"], r.get("path"), r["file"], r["line"]) for r in archdia["routes"]}
        arch_comps = archdia["components"]
    except (KeyError, TypeError):
        return {"status": "failed", "reason": "archdia.json thiếu routes/components hoặc sai dạng"}
    ours = {}
    for f in routes:
        a, ev = f["attributes"], f["evidence"][0]
        ours[(a["method"]["value"], a["path"]["value"] if is_known(a.get("path")) else None, ev["path"], ev["start_line"])] = f
    by_files = {tuple(sorted(c.get("files", []))): c for c in arch_comps}
    owning = sorted({owners[f["id"]] for f in routes if owners.get(f["id"])})
    comp_by_id = {c["id"]: c for c in components}
    unmatched = [comp_by_id[cid]["name"] for cid in owning if tuple(comp_by_id[cid]["files"]) not in by_files]
    wrong_owner = []
    arch_owner = {(r["method"], r.get("path"), r["file"], r["line"]): r.get("component_id") for r in archdia["routes"]}
    for key, f in ours.items():
        if key in arch_owner and owners.get(f["id"]):
            mine = by_files.get(tuple(comp_by_id[owners[f["id"]]]["files"]))
            if mine is not None and mine.get("id") != arch_owner[key]:
                wrong_owner.append(_key_text(key))
    missing = sorted(_key_text(k) for k in theirs - set(ours))
    extra = sorted(_key_text(k) for k in set(ours) - theirs)
    ok = not (missing or extra or unmatched or wrong_owner)
    return {"status": "passed" if ok else "failed", "routes_only_in_architecture": missing,
            "routes_only_in_documents": extra, "document_dirs_without_component": unmatched, "owner_mismatch": wrong_owner}


def _key_text(k) -> str:
    return f"{k[0]} {k[1] or '(path unknown)'} @ {k[2]}:{k[3]}"


def run_documents(source: Path, output: Path, membership_path: Path, repository_name: str, provider,
                  archdia_path: Path | None = None, diagram_path: Path | None = None, budget: Budget | None = None,
                  run_id: str = "run_fr029", mode: str = "agent", checkpoint: Path | None = None) -> dict:
    """`mode`: "agent" (the model reads through tools) or "oneshot" (the whole source in one request, see run_oneshot)."""
    if output.exists() and (not output.is_dir() or any(output.iterdir())):  # refuse before any model call costs money
        raise InputError("OUTPUT_UNSAFE", f"Output {output} đã tồn tại và không rỗng; không ghi đè")
    snap, sources = snapshot_mod.take(source)
    inv = snapshot_mod.inventory(snap)
    if not inv["units"]:
        raise InputError("INVALID_INPUT", "Thư mục không có file .py")
    unit_id = inv["units"][0]["id"]
    tools = SourceTools(snap, sources)
    membership = json.loads(membership_path.read_text(encoding="utf-8"))
    components = load_components(membership, snap, unit_id, tools.scope)
    archdia = json.loads(archdia_path.read_text(encoding="utf-8")) if archdia_path else None
    diagram = diagram_path.read_text(encoding="utf-8") if diagram_path else None
    claims = Claims(tools)
    agent = (run_oneshot(tools, claims, components, provider, budget, checkpoint) if mode == "oneshot"
             else run_agent(tools, claims, components, provider, budget))
    static, static_limits, refs = static_facts(snap, sources, tools, unit_id)  # tables, events, libraries, config
    facts = build_facts(claims, snap, unit_id) + static
    data, payloads = plan_documents(snap, inv, components, tools, claims, facts, agent, archdia, diagram,
                                    repository_name, run_id, provider,
                                    _kind_notes(membership, components, tools.scope) + static_limits, refs)
    artifacts = [_artifact(run_id, k, p, m, t.encode("utf-8") if t is not None else None, err)
                 for p, (k, m, t, err) in payloads.items()]
    bundle = dict(data, artifacts=sorted(artifacts, key=lambda a: a["path"]))
    _publish(output, {p: t for p, (_, _, t, _) in payloads.items() if t is not None}, dump(bundle))
    return bundle


def _kind_notes(membership: dict, components: list[dict], scope: dict) -> list[dict]:
    """Limitations about component kinds: derived from the scope, or given as normal on test/migration files."""
    out = []
    derived = [c for c, g in zip(components, membership["components"]) if not g.get("kind") and c["kind"] != "normal"]
    if derived:
        out.append({"code": "MEMBERSHIP_KIND_DERIVED", "stage": "input", "message": "Membership không ghi loại component; "
                    "xếp theo phạm vi đọc (FR-028): " + ", ".join(f"{c['name']} → {c['kind']}" for c in derived)})
    suspect = [c["name"] for c in components if c["kind"] == "normal" and _scope_kind(c["files"], scope)]
    if suspect:
        out.append({"code": "MEMBERSHIP_KIND_SUSPECT", "stage": "input", "message": "Component ghi loại normal nhưng "
                    "mọi file .py là file kiểm thử hoặc migration: " + ", ".join(suspect)})
    return out


def plan_documents(snap, inv, components, tools, claims, facts, agent, archdia, diagram, repository_name, run_id,
                   provider, notes=(), refs=()) -> tuple[dict, dict]:
    by_id = {f["id"]: f for f in facts}
    file_owner = {p: c for c in components for p in c["files"]}
    routes = [f for f in facts if f["kind"] == "route"]
    owners = {f["id"]: file_owner[f["evidence"][0]["path"]]["id"] for f in routes if f["evidence"][0]["path"] in file_owner}
    sys_slug = slug(repository_name, "SYSTEM")
    slugs = unique_slugs([(c["id"], c["name"]) for c in sorted(components, key=lambda c: c["id"])], "COMPONENT")
    payloads, contract_files = {}, []
    notices = []
    for comp in sorted(components, key=lambda c: c["id"]):
        mine = sorted((f for f in routes if owners.get(f["id"]) == comp["id"]), key=lambda f: f["id"])
        if not mine:
            continue
        cslug = slugs[comp["id"]]
        path = f"tech-specs/{cslug}/api/API-{sys_slug}-{cslug}-v1.md"
        text, _, more, cov = render_api(comp, mine, path, comp["name"], by_id, origin="agent đọc source, đã qua bộ kiểm bằng chứng")
        notices += more
        used_models = sorted({i for f in mine for i in _model_ids(f, by_id)})
        front = {"generated": True, "non_normative": True, "review_status": "Bản sinh tự động, chưa được chủ repository duyệt",
                 "snapshot_id": snap["snapshot_id"], "owner_component_id": comp["id"], "owner_component": comp["name"],
                 "schema_version": SCHEMA_VERSION, "pipeline_version": PIPELINE_VERSION, "prompt_version": agent.prompt_version,
                 "fact_ids": [f["id"] for f in mine] + used_models,
                 "evidence_ids": sorted({e["id"] for i in [f["id"] for f in mine] + used_models for e in by_id[i]["evidence"]})}
        reason = check_doc("api", text, cov)
        payloads[path] = ("api", "text/markdown", None if reason else frontmatter(front) + text,
                          {"code": "FORMAT_INVALID", "reason": reason, "retryable": False} if reason else None)
        contract_files.append((path, comp, reason))
    other_files = _table_event_files(snap, components, facts, file_owner, slugs, sys_slug, payloads, notices)
    coverage = tools.coverage()
    unpublished = {c["id"] for _, c, err in contract_files if err}
    exported = [f for f in routes if owners.get(f["id"]) not in unpublished]  # AC-04 compares what was written
    parity = compare_architecture(archdia, snap, exported, owners, components)
    limitations = list(notes) + _limitations(claims, tools, agent, coverage, parity, diagram)
    unassigned = [f["id"] for f in routes if f["id"] not in owners]
    readme_text = readme(repository_name, snap, components, contract_files, facts, file_owner, unassigned, parity,
                         limitations, coverage, agent, diagram, other_files)
    globals_ = app_globals(tools)
    relations = component_relations(refs, components)
    evidence = {e["id"]: e for f in facts for e in f["evidence"]}
    data = {"run_id": run_id, "schema_version": SCHEMA_VERSION, "pipeline_version": PIPELINE_VERSION,
            "snapshot_id": snap["snapshot_id"], "repository_name": repository_name,
            "provenance": {"provider": getattr(provider, "name", "?"), "model": getattr(provider, "model", "?"),
                           "prompt_version": agent.prompt_version},
            "agent": {"mode": agent.mode, "status": agent.status, "reason": agent.reason, "turns": agent.turns,
                      "tokens_in": agent.tokens_in, "tokens_out": agent.tokens_out,
                      "usage_missing_turns": agent.usage_missing_turns, "open_problems": agent.open_problems,
                      "requests": agent.requests},
            "coverage": coverage, "components": components, "contract_owners": owners, "unassigned": unassigned,
            "facts": facts, "evidence_index": [evidence[k] for k in sorted(evidence)],
            "limitations": limitations, "architecture_parity": parity, "render_notices": notices,
            "rejected_claims": claims.rejected, "unreferenced_models": claims.unreferenced_models,
            "excluded_from_snapshot": inv["excluded"], "app_globals": globals_,
            "component_relations": relations,
            "dismissed_suspects": [{"at": f"{w[0]}:{w[1]}-{w[2]}", "reason": x["reason"]}
                                   for w, x in ((x["at"], x) for x in claims.dismissed.values())]}
    payloads["README.md"] = ("readme", "text/markdown", readme_text, None)
    payloads["TAI-LIEU.md"] = ("readme", "text/markdown", tai_lieu(repository_name, agent, coverage, components, facts,
                                                                  limitations, contract_files, claims.suspects(),
                                                                  other_files, globals_, data["provenance"],
                                                                  _route_chains(routes, facts, tools), relations), None)
    payloads["result.json"] = ("json", "application/json", dump(data), None)
    return data, payloads


def _route_chains(routes, facts, tools) -> dict:
    """Route fact id -> [{"steps": [path:line...], "tables": [table names]}]: the accepted Service call paths whose first
    step lies in the route's handler (from its declaration to the next route declared in that file), and the tables
    whose model class the last (data access) file names. Shown as inferred."""
    decl = {f["id"]: declared(f) for f in routes}
    starts = {}
    for ev in decl.values():
        starts.setdefault(ev["path"], []).append(ev["start_line"])
    classes = []
    for t in (f for f in facts if f["kind"] == "table" and is_known(f["attributes"].get("name"))):
        ev = declared(t)
        m = re.search(r"class\s+(\w+)", tools.lines.get(ev["path"], [""] * ev["start_line"])[ev["start_line"] - 1])
        if m:
            classes.append((m.group(1), t["attributes"]["name"]["value"]))
    out = {}
    for role in (f for f in facts if f["kind"] == "file_role" and is_known(f["attributes"].get("call_path"))):
        steps = role["attributes"]["call_path"]["value"]
        if not steps:
            continue
        path, line = steps[0].rsplit(":", 1)[0], int(re.split(r"[:-]", steps[0].rsplit(":", 1)[1])[0])
        for fid, ev in decl.items():
            later = [s for s in starts[ev["path"]] if s > ev["start_line"]]
            if ev["path"] == path and ev["start_line"] <= line < (min(later) if later else 10 ** 9):
                data_path = steps[-1].rsplit(":", 1)[0]
                text = tools.raw.get(data_path, "")
                tables = sorted({name for cls, name in classes if re.search(rf"\b{re.escape(cls)}\b", text)})
                if not any(c["steps"] == steps for c in out.get(fid, [])):
                    out.setdefault(fid, []).append({"steps": steps, "tables": tables})
    return out


def _table_event_files(snap, components, facts, file_owner, slugs, sys_slug, payloads, notices) -> list:
    """TBL (FR-030) and EVT (FR-031) files per component, from the statically read facts. Returns
    [(label, path, component, error reason or None)] in component order."""
    def owner_of(f):
        return file_owner.get(declared(f)["path"])
    tables = [f for f in facts if f["kind"] == "table"]
    events = [f for f in facts if f["kind"] == "event"]
    model = {"edges": event_edges(events, owner_of)}
    comps = {c["id"]: c for c in components}
    out = []

    def publish(kind, label, path, comp, group, text, cov):
        reason = check_doc(kind, text, cov)
        front = {"generated": True, "non_normative": True, "review_status": "Bản sinh tự động, chưa được chủ repository duyệt",
                 "snapshot_id": snap["snapshot_id"], "owner_component_id": comp["id"], "owner_component": comp["name"],
                 "schema_version": SCHEMA_VERSION, "pipeline_version": PIPELINE_VERSION, "origin": "đọc tĩnh",
                 "fact_ids": [f["id"] for f in group], "evidence_ids": sorted({e["id"] for f in group for e in f["evidence"]})}
        payloads[path] = (kind, "text/markdown", None if reason else frontmatter(front) + text,
                          {"code": "FORMAT_INVALID", "reason": reason, "retryable": False} if reason else None)
        out.append((label, path, comp, reason))
    for comp in sorted(components, key=lambda c: c["id"]):
        cslug = slugs[comp["id"]]
        mine = sorted((f for f in tables if (owner_of(f) or {}).get("id") == comp["id"]), key=lambda f: f["id"])
        if mine:
            path = f"tech-specs/{cslug}/schema/TBL-{sys_slug}-{cslug}.md"
            text, more, cov = render_tbl(comp, mine, path, comp["name"])
            notices += more
            publish("table", "TBL", path, comp, mine, text, cov)
        mine = [f for f in events if (owner_of(f) or {}).get("id") == comp["id"]]
        for key, label, group in plan_events(mine):
            path = f"tech-specs/{cslug}/events/EVT-{sys_slug}-{cslug}-{label}.md"
            text, more, cov = render_evt(comp, group, path, model, comps, key.startswith("chan:"))
            notices += more
            publish("event", "EVT", path, comp, group, text, cov)
    return out


def _model_ids(route: dict, by_id: dict) -> list[str]:
    """Models a route uses, nested ones included."""
    a = route["attributes"]
    todo = [i for k in ("request_model_ids", "response_model_ids") if is_known(a.get(k)) for i in a[k]["value"]]
    if is_known(a.get("parameters")):
        todo += [i for p in a["parameters"]["value"] if is_known(p.get("schema")) for i in _refs(p["schema"]["value"])]
    if is_known(a.get("bodies")):  # arguments of a generic response model (Page[Item])
        todo += [i for b in a["bodies"]["value"] for i in _refs(b.get("type_args", []))]
    for key in ("response_type", "request_type"):  # a library generic, or a JSON body typed list[Item]
        if is_known(a.get(key)):
            todo += _refs(a[key]["value"]["schema"])
    seen = []
    while todo:
        i = todo.pop()
        if i in seen or i not in by_id:
            continue
        seen.append(i)
        f = by_id[i]["attributes"]["fields"]
        fields = f["value"] if is_known(f) else []  # a model created at runtime has unknown fields
        todo += [r for fv in fields if is_known(fv.get("type")) for r in _refs(fv["type"]["value"])]
    return seen


def _refs(schema) -> list[str]:
    if isinstance(schema, dict):
        return ([schema["x-model-fact"]] if "x-model-fact" in schema else []) + [i for v in schema.values() for i in _refs(v)]
    if isinstance(schema, list):
        return [i for v in schema for i in _refs(v)]
    return []


def _limitations(claims, tools, agent, coverage, parity=None, diagram=None) -> list[dict]:
    out = []
    if diagram is None:
        out.append({"code": "DIAGRAM_NOT_PROVIDED", "stage": "input", "message": "Chưa được cấp sơ đồ component từ "
                    "bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06"})
    if parity is not None and parity["status"] == "not_evaluated":
        out.append({"code": "ARCHITECTURE_NOT_EVALUATED", "stage": "input",
                    "message": "Chưa đối chiếu được với archdia.json (AC-029-04): " + parity.get("reason", "")})
    for (kind, where), x in sorted(claims.limits.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        out.append({"code": LIMIT_KINDS[kind], "message": f"{kind} tại {where[0]}:{where[1]}"
                    + (f" — {x['detail']}" if x["detail"] else ""), "stage": "analysis", "where": f"{where[0]}:{where[1]}"})
    if agent.status != "completed":
        out.append({"code": "ANALYSIS_PARTIAL", "message": agent.reason or agent.status, "stage": "agent"})
    unread = [f for f in coverage["files"] if f["missing"] or f["cut_lines"]]
    if unread:
        out.append({"code": "SOURCE_NOT_FULLY_READ", "stage": "agent",
                    "message": "; ".join(f"{f['path']} thiếu {f['missing']}" + (f" cắt {f['cut_lines']}" if f["cut_lines"] else "")
                                         for f in unread)})
    counts = {}
    for x in coverage["not_readable"]:
        counts[x["scope"]] = counts.get(x["scope"], 0) + 1
    if counts:
        out.append({"code": "OUT_OF_SCOPE_FILES", "stage": "scope",
                    "message": ", ".join(f"{k}: {v} file" for k, v in sorted(counts.items()))
                    + ". Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)"})
    if claims.rejected:
        out.append({"code": "CLAIMS_REJECTED", "stage": "verification",
                    "message": f"{len(claims.rejected)} lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); "
                               "chi tiết ở result.json"})
    return out


def readme(repository_name, snap, components, contract_files, facts, file_owner, unassigned, parity, limitations,
           coverage, agent, diagram, other_files=()) -> str:
    roles = {f["attributes"]["file"]["value"]: f for f in facts if f["kind"] == "file_role"}
    empty = {f["path"] for f in coverage["files"] if f["status"] == "empty"}
    outside = {x["path"]: x["scope"] for x in coverage["not_readable"]}
    lines = [f"# {md(repository_name)} — tài liệu L3 API (bản sinh tự động)", "",
             "Bản sinh tự động, chưa được chủ repository duyệt.", "",
             f"- Snapshot: `{snap['snapshot_id']}`",
             f"- Trạng thái phân tích: {agent.status}" + (f" — {md(agent.reason)}" if agent.reason else ""),
             f"- Độ phủ đọc source: {'đủ' if coverage['complete'] else 'chưa đủ, xem Giới hạn'}", "",
             "## Mục lục contract", ""]
    lines += [f"- API: [{p}]({p}) — component {md(c['name'])}" if not err else
              f"- API: {p} — component {md(c['name'])} — chưa xuất được: {md(err)}" for p, c, err in contract_files] \
        + [f"- {k}: [{p}]({p}) — component {md(c['name'])}" if not err else
           f"- {k}: {p} — component {md(c['name'])} — chưa xuất được: {md(err)}" for k, p, c, err in other_files] \
        or ["- (không có)"]
    lines += ["", "## Sơ đồ component", ""]
    if diagram is None:
        lines += ["Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ."]
    else:
        lines += ["```mermaid", diagram.rstrip("\n"), "```"]
    lines += ["", "## Cấu trúc component", ""]
    for c in components:
        if c["kind"] != "normal":
            continue
        lines += [f"### {md(c['name'])}", ""]
        packages = {}
        for p in c["files"]:
            packages.setdefault(p.rsplit("/", 1)[0] + "/" if "/" in p else "./", []).append(p)
        for pkg in sorted(packages):
            lines.append(f"- Package `{md(pkg)}`")
            for p in sorted(packages[pkg]):
                f = roles.get(p)
                if f is None:
                    lines.append(f"  - `{md(p)}` — " + ("file rỗng, không có vai trò" if p in empty else
                                 f"ngoài phạm vi đọc ({outside[p]})" if p in outside else "vai trò unknown: agent chưa xác định"))
                    continue
                a = f["attributes"]
                ev = f["evidence"][0] if f["evidence"] else None
                where = f" — `{md(ev['path'])}:{ev['start_line']}`" if ev and a["role"]["value"] != "Service" else ""
                label = "inferred: " + md(a["reason"]["value"]) if f["confidence"] == "inferred" else "exact"
                if a["role"]["value"] == "Khác":
                    label = "exact: " + md(a["reason"]["value"])
                if a["role"]["value"] == "Service":
                    where = " — đường gọi " + ", ".join(f"`{md(x)}`" for x in a["call_path"]["value"])
                text = f": {code(a['code']['value'])}" if is_known(a.get("code")) and a["role"]["value"] != "Service" else ""
                lines.append(f"  - `{md(p)}` — {md(a['role']['value'])} ({label}){where}{text}")
        lines.append("")
    lines += ["## Lời gọi HTTP ra ngoài", ""]
    calls = [f for f in facts if f["kind"] == "http_call"]
    if calls:
        lines += ["| Component | Thư viện, method | Đích | Bằng chứng |", "|---|---|---|---|"]
        for f in calls:
            a, ev = f["attributes"], f["evidence"][0]
            target = cell(a.get("url"))
            if not is_known(a.get("url")) and is_known(a.get("url_config_key")):
                target = "khóa cấu hình " + cell(a["url_config_key"]) + " (exact)"
            elif is_known(a.get("url")):
                target += " (exact)"
            owner = file_owner[ev["path"]]["name"] if ev["path"] in file_owner else "unknown — chưa gán component"
            lines.append("| " + " | ".join([md(owner), cell(a.get("library")) + ", " + cell(a.get("method")), target,
                                              md(f"{ev['path']}:{ev['start_line']}") + ": " + code(a["call_text"]["value"])])
                         + " |")
    else:
        lines += ["- (không có)"]
    lines += ["", "## Contract chưa gán được component", ""]
    lines += [f"- `{i}`" for i in unassigned] or ["- (không có)"]
    lines += ["", "## Đối chiếu với dữ liệu kiến trúc", "", f"- Trạng thái: {parity['status']}"]
    for k in ("reason", "routes_only_in_architecture", "routes_only_in_documents", "document_dirs_without_component",
              "owner_mismatch"):
        if parity.get(k):
            lines.append(f"- {k}: {md(parity[k] if isinstance(parity[k], str) else '; '.join(parity[k]))}")
    lines += ["", "## Giới hạn", ""]
    lines += [f"- `{x['code']}`: {md(x['message'])}" for x in limitations] or ["- (không có)"]
    return "\n".join(lines) + "\n"

