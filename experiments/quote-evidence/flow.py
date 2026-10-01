"""Tiers, edge kinds, edges without an import, reach from entry points. No AI. Input: calls.facts().

    analyze(idx, facts) -> {"tier": {path: [tier, line, what]}, "pure": set of paths,
                            "pairs": {(a, b): [kind, line]}, "reached": set, "io": {path: {kind: line}},
                            "db_files": set, "implements": {path: files with a class based on one of its classes},
                            "sure": {path: [tier, line, what]} for files with a sign that is almost never wrong}

A file's tier comes from its own signs; a session call (get, commit, refresh) is not a data sign, a library
object that others query with a session (FastCRUD(User), aiosql) is. A file with no I/O is "shared".
The walk from entry points follows flow edges and goes from an interface to the classes that implement it
(DI); it reaches a shared file but does not go on from it.

Kinds of a file pair, strongest first: flow > check > helper > pass > wiring. Only flow is drawn.
- check: a call that checks and returns (check_*, verify_*, get_current_*, Depends in dependencies=[...]).
- helper: a call to a function with no I/O that calls only such functions (hash, slug, sign a token).
- pass: opening or receiving a database session only to hand it on (get_db, SessionLocal(), .begin()).
- wiring: start-up, shut-down, app factory, DI container (a repository name handed to a library).
Edges without an import: a file that queries through a session reaches the file that creates the
database engine; a library object built in a file (FastCRUD(User), aiosql) queries for that file;
session=/engine= handed to a library; import_module by name; "pkg.mod:attr" strings; app.state.<attr>.
"""
from __future__ import annotations

import re

RANK = ("entry", "api", "service", "data", "infra")
KINDS = ("flow", "check", "helper", "pass", "wiring")
CHECK = re.compile(r"^(check|verify|validate|require|ensure|has|is|can)_|^get_current_|"
                   r"(^|_)(authentication|authorize|authorization|permission|permissions)($|_)", re.I)
OPENS_SESSION = re.compile(r"session|connect|engine|begin|get_db|transaction", re.I)
EXT_NAME = {"database": "Database", "redis": "Redis", "smtp": "SMTP", "broker": "Message broker",
            "memcached": "Memcached", "http": "HTTP API", "oauth": "OAuth"}


def _dotted(path: str) -> list[str]:
    parts = path[:-3].split("/")
    return parts[:-1] if parts[-1] == "__init__" else parts


def _modules(paths, name: str) -> list[str]:
    """Files whose dotted module name ends with `name` (a module may be imported from any source root)."""
    want = name.strip(".").split(".")
    return [p for p in paths if _dotted(p)[-len(want):] == want]


def _under(paths, parts: list[str], names: list[str], idx: dict) -> list[str]:
    """Files under the constant prefix of a module name built at run time, that define one of `names`."""
    prefix = parts[0].strip(".").split(".")
    out = []
    for p in paths:
        d = _dotted(p)
        if any(d[i:i + len(prefix)] == prefix for i in range(len(d) - len(prefix) + 1)):
            defined = {s["name"] for s in idx[p]["symbols"]}
            if not names or defined & set(names):
                out.append(p)
    return out


def analyze(idx: dict, facts: dict) -> dict:
    files = set(facts)
    db_files = {p for p in files if any(k == "database" for _, _, k in facts[p]["io"])}
    db_use = {p: set(f["db_use"]) for p, f in facts.items()}
    query_objects = {p: set() for p in facts}
    for p, f in facts.items():
        for c in f["calls"]:
            t = c["target"]
            if c["session_arg"] and t in facts and c["symbol"] in facts[t]["objects"]:
                db_use[t].add(facts[t]["objects"][c["symbol"]][0])      # FastCRUD(User), aiosql queries
                query_objects[t].add(facts[t]["objects"][c["symbol"]][0])
        for line, t in f["config_refs"]:
            if t in db_files:
                db_use[p].add(line)

    # wiring context: lifespan, app factory, and same-file helpers only they call
    wiring, routing = {}, {}
    for p, f in facts.items():
        w = {n for n, r in f["funcs"].items() if r["wiring"]}
        w |= {c["func"].split(".")[-1] for c in f["calls"] if c["last"] == "FastAPI" and c["lib"] == "fastapi"}
        callers = {}
        for c in f["calls"]:
            if c["target"] == p and c["symbol"]:
                callers.setdefault(c["symbol"], set()).add(c["func"].split(".")[-1])
        changed = True
        while changed:
            changed = False
            for name, by in callers.items():
                if name not in w and by and by <= w:
                    w.add(name)
                    changed = True
        wiring[p] = w
        for n, r in f["funcs"].items():
            routing[(p, n)] = r["routing"]
    changed = True
    while changed:
        changed = False
        for p, f in facts.items():
            for c in f["calls"]:
                key = (p, c["func"].split(".")[-1])
                if routing.get((c["target"], c["last"])) and not routing.get(key) and key[1] in facts[p]["funcs"]:
                    routing[key] = changed = True

    impure = _impure_functions(facts, db_use)
    pairs: dict = {}

    def add(a: str, b: str, kind: str, line: int) -> None:
        if a == b or b not in files:
            return
        old = pairs.get((a, b))
        if old is None or KINDS.index(kind) < KINDS.index(old[0]) or (kind == old[0] and line < old[1]):
            pairs[(a, b)] = [kind, line]

    for p, f in facts.items():
        for c in f["calls"]:
            t = c["target"]
            if not t or t == p:
                continue
            func = c["func"].split(".")[-1]
            if c["how"] == "routing":
                kind = "flow"
            elif c["how"] == "route_dep" or CHECK.search(c["last"]):
                kind = "check"
            elif c["how"] == "arg_ref":
                kind = "wiring"
            elif func in wiring[p] and not routing.get((t, c["last"])):
                kind = "wiring"
            elif t in db_files and OPENS_SESSION.search(c["last"]):
                kind = "pass"
            elif c["how"] == "call" and t in facts and c["last"] in facts[t]["funcs"] and (t, c["last"]) not in impure:
                kind = "helper"
            else:
                kind = "flow"
            add(p, t, kind, c["line"])
        if db_use[p]:
            for d in db_files:
                add(p, d, "flow", min(db_use[p]))
        for line, parts, names in f["dynamic"]:
            for q in _under(files, parts, names, idx):
                add(p, q, "flow", line)
        for line, name in f["strings"]:
            for q in _modules(files, name):
                add(p, q, "flow", line)
        for attr, line in f["state_get"].items():
            for q, g in facts.items():
                if attr in g["state_set"]:
                    add(p, q, "pass" if q in db_files and not db_use[p] else "flow", line)

    # tiers
    tier = {}
    for p, f in facts.items():
        sig = dict(f["signals"])
        if query_objects[p] and "data" not in sig and "infra" not in sig:
            sig["data"] = [min(query_objects[p]), "đối tượng truy vấn"]
        best = min(sig, key=RANK.index) if sig else None
        if p in db_files:                 # the file that creates the database engine is the connection point
            best = "infra"
        if best:
            tier[p] = [best, *sig[best]]
    flow_out = {}
    for (a, b), (kind, _) in pairs.items():
        if kind == "flow":
            flow_out.setdefault(a, set()).add(b)
    pure = {p for p in files if p not in tier and not facts[p]["io"]}
    changed = True
    while changed:
        changed = False
        for p in list(pure):
            if flow_out.get(p, set()) - pure:
                pure.discard(p)
                changed = True
    for p in pure:
        tier[p] = ["shared", 0, "không IO"]
    implements = {}
    for p in files:
        for row in idx[p]["imports"]:
            if row["target"] in files and any(k == "base" for _, k in idx[p]["uses"].get(row["local"], [])):
                implements.setdefault(row["target"], set()).add(p)
    changed = True
    while changed:
        changed = False
        for (a, b), (kind, line) in pairs.items():
            if kind != "flow" or tier.get(a, [None])[0] not in ("entry", "api", "service"):
                continue
            for q in {b} | implements.get(b, set()):
                if q not in tier:
                    tier[q] = ["service", line, f"được {a} gọi"]
                    changed = True
    for p in files - set(tier):
        tier[p] = ["unknown", 0, ""]

    seen = {p for p in files if tier[p][0] == "entry"}
    todo = list(seen)
    while todo:
        p = todo.pop()
        nxt = implements.get(p, set()) | (set() if p in pure else flow_out.get(p, set()))
        for q in nxt - seen:
            seen.add(q)
            todo.append(q)
    reached = seen
    io = {}
    for p, f in facts.items():
        for line, _, kind in f["io"]:
            if kind != "monitoring":
                io.setdefault(p, {}).setdefault(kind, line)
    sure = {p: [t, *f["sure"][t]] for p, f in facts.items() if f["sure"] for t in [min(f["sure"], key=RANK.index)]}
    return {"tier": tier, "pure": pure, "pairs": pairs, "reached": reached, "io": io, "db_files": db_files,
            "implements": implements, "sure": sure}


def _impure_functions(facts: dict, db_use: dict) -> set:
    """(file, function) pairs that do I/O, hand a session on, call such a function, or are abstract."""
    impure = set()
    for p, f in facts.items():
        lines = db_use[p] | {line for line, _, kind in f["io"]}
        for name, r in f["funcs"].items():
            if r["abstract"] or any(a <= line <= b for a, b in r["lines"] for line in lines):
                impure.add((p, name))
    changed = True
    while changed:
        changed = False
        for p, f in facts.items():
            for c in f["calls"]:
                key = (p, c["func"].split(".")[-1])
                if key in impure or key[1] not in f["funcs"] or c["how"] not in ("call", "decorator"):
                    continue
                t = c["target"]
                if t is None:                    # a library call; I/O libraries are already in f["io"]
                    continue
                if c["session_arg"] or (t, c["last"]) in impure or (t in facts and c["last"] not in facts[t]["funcs"]
                                                                     and facts[t]["signals"]):
                    impure.add(key)
                    changed = True
    return impure


def block_tier(an: dict, files: list[str]) -> str:
    """The highest tier any file shows a sign of; a block with no sign is service."""
    tiers = [an["tier"][p][0] for p in files if an["tier"].get(p, ["unknown"])[0] in RANK]
    signed = [x for x in tiers if x != "service"]
    return min(signed, key=RANK.index) if signed else "service"


def block_edges(an: dict, owner: dict, shared: set, rank: dict) -> dict:
    """Flow edges between blocks: not inside one block, not touching a shared block, not going up."""
    out = {}
    for (a, b), (kind, line) in sorted(an["pairs"].items()):
        A, B = owner.get(a), owner.get(b)
        if kind != "flow" or not A or not B or A == B or A in shared or B in shared:
            continue
        if rank.get(B, 0) < rank.get(A, 0):
            continue
        out.setdefault((A, B), [a, line])
    return out


def as_run(an: dict, blocks: dict, shared: set, rank: dict) -> dict:
    """A run in the shape evaluate.score reads: the given blocks, drawn flow edges, externals by kind."""
    owner = {p: b for b, files in blocks.items() for p in files}
    edges = [{"source": A, "target": B, "evidence": ev} for (A, B), ev in block_edges(an, owner, shared, rank).items()]
    ext = {}
    for p, kinds in an["io"].items():
        if owner.get(p) and owner[p] not in shared:
            for kind in kinds:
                ext.setdefault(EXT_NAME.get(kind, kind), set()).add(owner[p])
    return {"components": [{"id": b, "files": files} for b, files in blocks.items()], "edges": edges,
            "externals": [{"name": n, "edges": [{"source": b} for b in sorted(bs)]} for n, bs in ext.items()],
            "file_lines": {}}
