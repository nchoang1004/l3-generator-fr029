"""Parts of the FR-029 run read statically: tables (FR-030), events and background tasks (FR-031), libraries and
configuration keys (FR-028), middleware and global exception handlers.

API facts (routes, models, HTTP calls, file roles) never come from here: the agent proposes them and the checker
verifies them (ADR-2026-006). This module only reuses the static reader for the other kinds, on in-scope files.
"""
from __future__ import annotations

import ast
import re

from . import astscan, extract
from .common import is_known

STATIC_KINDS = ("table", "event", "config", "library")
# limitations of the static reader that concern these kinds; route/reference ones belong to the agent's part
STATIC_LIMITS = {"MANIFEST_INVALID", "PARSE_FAILED", "QUEUE_LIBRARY_UNSUPPORTED", "TABLES_IN_MIGRATIONS_NOT_READ",
                 "VALUE_REDACTED"}


def static_facts(snap: dict, sources: dict, tools, unit_id: str) -> tuple[list[dict], list[dict], list[dict]]:
    """(facts, limitations, references) for STATIC_KINDS, read from the files the agent may read (FR-028 Phạm vi
    đọc). `references`: resolved calls/Depends/table reads as {"kind", "from": path:line, "to": path:line}."""
    try:
        result = extract.extract(snap, {p: sources[p] for p in tools.readable}, unit_id)
    except Exception as exc:  # noqa: BLE001 - the agent's part must still be published; say what was lost
        return [], [{"code": "STATIC_READ_FAILED", "stage": "static",
                     "message": f"Phần đọc tĩnh lỗi ({type(exc).__name__}); tài liệu thiếu bảng, sự kiện, thư viện, "
                                "cấu hình và quan hệ component"}], []
    facts = [f for f in result["facts"] if f["kind"] in STATIC_KINDS]
    symbols = {f["id"]: f for f in result["facts"] if f["kind"] in ("symbol", "table")}
    refs = []
    for f in result["facts"]:
        if f["kind"] != "reference" or f["resolution"] != "resolved" or not f["target_fact_ids"]:
            continue
        target = symbols.get(f["target_fact_ids"][0])
        if target and target["evidence"] and f["evidence"]:
            src, dst = f["evidence"][0], declared(target)
            refs.append({"kind": f["attributes"]["reference_kind"]["value"] if is_known(f["attributes"].get("reference_kind"))
                         else "?", "from": f"{src['path']}:{src['start_line']}", "to": f"{dst['path']}:{dst['start_line']}"})
    kept = {f["id"] for f in facts}
    limits = []
    for x in result["limitations"]:
        affected = x.get("affected_ids") or []
        if x["code"] not in STATIC_LIMITS or (x["code"] == "VALUE_REDACTED" and not set(affected) & kept):
            continue
        limits.append({"code": x["code"], "message": x["message"], "stage": "static"})
    missed = tables_not_read(tools, {v["value"] for f in facts if f["kind"] == "table"
                                     for v in [f["attributes"].get("name") or {}] if is_known(v)})
    if missed:  # AC-030-04: never let the reader conclude the repository has no tables
        limits.append({"code": "TABLES_NOT_READ", "stage": "static",
                       "message": "Có bảng khai theo cách công cụ chưa đọc (FR-030 Phạm vi đọc), không có trong tài liệu: "
                                  + "; ".join(missed)})
    return facts, limits, refs


OTHER_ORMS = {"tortoise": "Tortoise", "peewee": "Peewee", "beanie": "Beanie", "odmantic": "ODMantic",
              "mongoengine": "MongoEngine", "pony": "Pony ORM", "piccolo": "Piccolo", "ormar": "ormar", "django": "Django ORM"}


def tables_not_read(tools, read_names: set) -> list[str]:
    """Places that declare tables outside FR-030's reading scope: models of other ORMs, tables created only in
    migration files, hand-written CREATE TABLE. One entry per kind, with path:line."""
    orm, migration, sql = [], [], []
    for path in sorted(tools.raw):
        if not path.endswith(".py"):
            continue
        scope = tools.scope.get(path, ("", ""))[0]
        if scope == "migration":
            for i, line in enumerate(tools.lines[path], 1):  # alembic op.create_table('t') or raw CREATE TABLE "t"
                m = re.search(r"create_table\(\s*['\"](\w+)['\"]", line) or \
                    re.search(r"create\s+table\s+(?:if\s+not\s+exists\s+)?[\"`\[]?(\w+)", line, re.I)
                if m and m.group(1) not in read_names:
                    migration.append(f"{m.group(1)} ({path}:{i})")
            continue
        if path not in tools.readable:
            continue
        tree = astscan.parse(tools.raw[path])
        if tree is None:
            continue
        libs = {OTHER_ORMS[m.split(".")[0]] for m, _ in astscan.imports(tree).values() if m.split(".")[0] in OTHER_ORMS}
        if libs:
            orm += [f"{'/'.join(sorted(libs))}: {path}:{n.lineno} ({n.name})" for n in ast.walk(tree)
                    if isinstance(n, ast.ClassDef) and any((astscan.name_of(b) or "").endswith(("Model", "Document"))
                                                           for b in n.bases)]
        sql += [f"{path}:{n.lineno}" for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)
                and re.search(r"\bcreate\s+table\b", n.value, re.I)]
    out = []
    if orm:
        out.append("ORM khác — " + ", ".join(orm))
    if migration:
        out.append("bảng chỉ có trong migration — " + ", ".join(migration))
    if sql:
        out.append("SQL viết tay (CREATE TABLE) — " + ", ".join(sql))
    return out


def component_relations(refs: list[dict], components: list[dict]) -> list[dict]:
    """Component -> component uses read from resolved references between their files, with one example each."""
    owner = {p: c for c in components for p in c["files"]}
    out = {}
    for r in refs:
        a, b = owner.get(r["from"].rsplit(":", 1)[0]), owner.get(r["to"].rsplit(":", 1)[0])
        if a and b and a["id"] != b["id"] and a["kind"] == "normal" and b["kind"] == "normal":
            x = out.setdefault((a["name"], b["name"]), {"from": a["name"], "to": b["name"], "kinds": set(), "count": 0,
                                                       "example": r["from"]})
            x["kinds"].add(r["kind"])
            x["count"] += 1
    return [dict(x, kinds=sorted(x["kinds"])) for _, x in sorted(out.items())]


def declared(fact: dict) -> dict:
    """The evidence of the line that declares a fact."""
    decl = fact["attributes"].get("declaration_evidence_id")
    return next((e for e in fact["evidence"] if is_known(decl) and e["id"] == decl["value"]), fact["evidence"][0])


def event_edges(events: list[dict], owner_of) -> list[dict]:
    """Sender -> receiver pairs proven by the same broker, namespace and topic (FR-031: never by the name alone)."""
    def channel(f):
        a = f["attributes"]
        vals = tuple(a[k]["value"] if is_known(a.get(k)) else None for k in ("broker", "namespace", "topic"))
        return None if None in vals else vals
    out = []
    for p in (f for f in events if is_known(f["attributes"].get("action")) and f["attributes"]["action"]["value"] == "publish"):
        for c in (f for f in events if is_known(f["attributes"].get("action")) and f["attributes"]["action"]["value"] == "consume"):
            src, dst = owner_of(p), owner_of(c)
            if channel(p) and channel(p) == channel(c) and src and dst:
                out.append({"relation_type": "publishes", "fact_ids": [p["id"], c["id"]],
                            "source_component_id": src["id"], "target_component_id": dst["id"]})
    return out


def app_globals(tools) -> list[dict]:
    """Middleware and exception handlers registered on an app: add_middleware(X), Middleware(X), @app.middleware,
    exception_handler(X) / add_exception_handler(X, ...). Read from the syntax tree of in-scope files."""
    out = []
    for path in tools.readable:
        if not path.endswith(".py"):
            continue
        tree = astscan.parse(tools.raw[path])
        if tree is None:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = astscan.name_of(node.func)
                arg = node.args[0] if node.args else None
                if name in ("add_middleware", "Middleware") and arg is not None:
                    out.append({"kind": "middleware", "name": ast.unparse(arg), "at": f"{path}:{node.lineno}"})
                elif name in ("exception_handler", "add_exception_handler") and arg is not None \
                        and isinstance(node.func, ast.Attribute):
                    out.append({"kind": "exception_handler", "name": ast.unparse(arg), "at": f"{path}:{node.lineno}"})
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for dec in node.decorator_list:
                    if isinstance(dec, ast.Call) and astscan.name_of(dec.func) == "middleware":
                        out.append({"kind": "middleware", "name": f"hàm {node.name}", "at": f"{path}:{dec.lineno}"})
    seen, unique = set(), []
    for x in out:  # @app.exception_handler(X) is both a call and a decorator: keep one
        if (x["kind"], x["at"]) not in seen:
            seen.add((x["kind"], x["at"]))
            unique.append(x)
    return sorted(unique, key=lambda x: (x["kind"], x["at"]))
