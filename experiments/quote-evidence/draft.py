"""A first draft of the blocks, made by code from facts only (flow.analyze). No AI.

    draft(idx, facts, an) -> {"blocks": {key: {"layer", "files", "paths", "evidence": [file, line]}},
                              "shared": {"files", "paths"}}

Pass 1 shows the draft to the model, which corrects it; when the model gives nothing usable, the draft is the
grouping. The rules are the grouping rules the model is given, where facts decide them:
- a file's layer: its sure sign, else its hint (flow.analyze "tier"); files without a layer are placed last;
- entry: one block per way in (the web app with its middleware; a CLI; a background loop or scheduler);
- api: one block for the routers of every feature; socket handlers and admin pages apart (other ways in);
- data: one block; infra: one block per kind of external system (database, redis, http...);
- a file without a sign of its own that one block only checks with, uses as a helper, or gets a session from
  joins that block (a route dependency joins the routes);
- service: files grouped by the kinds of I/O their calls reach, so features that go down the same way merge;
- an interface joins the block of the classes based on it; other files without I/O join the block of their
  users when all sit in one block, else the block most files of their directory are in, else shared.
Evidence of a block: a line of its own files showing its layer (sure sign, I/O line, query, a call downwards).
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import PurePosixPath

import graph

LAYERS = ("entry", "api", "service", "data", "infra")
SERVICE_CAP = 5
IO_ORDER = ("database", "redis", "broker", "smtp", "http", "oauth", "memcached")


def _way_in(tier: str, what: str) -> str:
    """The block name of an entry or api file, from the sign that gave it its layer."""
    what = str(what)
    if tier == "entry":
        if what in ("add_job(", "vòng nền"):
            return "background"
        if what == "__main__":             # run as a program: another way in than the web app
            return "script"
        return "cli" if what.startswith("@") else "app"
    if what in ("AsyncServer", "Server", "@event", "@on"):
        return "socket_api"
    return "admin" if what in ("Admin", "ModelView") else "api"


def file_layer(an: dict, p: str) -> tuple[str | None, int, str]:
    """(layer, line, what) of a file: its sure sign, else its hint; layer None when it has neither."""
    if p in an["sure"]:
        t, line, what = an["sure"][p]
        return t, line, what
    t, line, what = an["tier"].get(p, ["unknown", 0, ""])
    if t in LAYERS and not (t == "service" and str(what).startswith("được ")):
        return t, line, what
    return (("service", line, what) if t == "service" else (None, 0, ""))


def evidence(idx: dict, facts: dict, an: dict, files: list[str], layer: str, owner: dict | None = None,
             rank: dict | None = None) -> list | None:
    """A line of `files` that shows `layer`: a sure sign of that layer, an I/O line (infra), a query (data), a
    call into a block of a lower layer (service), else the first declaration."""
    files = sorted(files)
    for p in files:
        if an["sure"].get(p, [None])[0] == layer:
            return [p, an["sure"][p][1]]
    if layer == "infra":
        for p in files:
            if an["io"].get(p):
                return [p, min(an["io"][p].values())]
    for p in files:
        t, line, what = an["tier"].get(p, [None, 0, ""])
        if t == layer and line and not str(what).startswith("được "):
            return [p, line]
    if owner is not None and rank is not None:
        mine = set(files)
        for (a, b), (kind, line) in sorted(an["pairs"].items()):
            if a in mine and kind == "flow" and b not in mine and rank.get(owner.get(b), -1) > rank.get(owner.get(a), 99):
                return [a, line]
    for p in files:
        if idx[p]["symbols"]:
            return [p, idx[p]["symbols"][0]["line"]]
    for p in files:
        n = next((n for n, line in enumerate(idx[p]["lines"], start=1) if len(line.strip()) >= 8), 0)
        if n:
            return [p, n]
    return None


def compress(owner: dict, files: list[str]) -> dict:
    """{key: paths}: a directory stands for all files under it when they share one key, else its files and
    sub-directories are listed; "" is the repository root."""
    out = defaultdict(list)

    def walk(d: str) -> None:
        under = [f for f in files if f.startswith(d)]
        keys = {owner[f] for f in under}
        if len(keys) == 1:
            out[keys.pop()].append(d)
            return
        subs = sorted({f[len(d):].split("/")[0] + "/" for f in under if "/" in f[len(d):]})
        for f in sorted(f for f in under if "/" not in f[len(d):]):
            out[owner[f]].append(f)
        for s in subs:
            walk(d + s)

    walk("")
    return dict(out)


def draft(idx: dict, facts: dict, an: dict) -> dict:
    files = graph.content_files(idx)
    owner, layer = {}, {}
    callers = defaultdict(dict)                       # file -> {caller file: set of kinds}
    flow_out = defaultdict(set)
    for (a, b), (kind, _) in an["pairs"].items():
        callers[b].setdefault(a, set()).add(kind)
        if kind == "flow":
            flow_out[a].add(b)

    def put(p: str, key: str, t: str) -> None:
        owner[p] = key
        layer.setdefault(key, t)

    # entry, api, data, infra: from each file's own sign
    for p in files:
        t, _, what = file_layer(an, p)
        if t in ("entry", "api"):
            put(p, _way_in(t, what), t)
        elif t == "data":
            put(p, "data", "data")
        elif t == "infra":
            kind = next((k for k in IO_ORDER if k in an["io"].get(p, {})), None) or next(iter(an["io"].get(p, {})), "infra")
            put(p, kind, "infra")

    # a file without a sign of its own that one block only checks with, uses as a helper or gets a session from
    def helper_of(p: str) -> str | None:
        if p in an["sure"] or an["io"].get(p) or p in owner:
            return None
        rows = {a: k for a, k in callers.get(p, {}).items() if k - {"wiring"}}
        blocks = {owner.get(a) for a in rows}
        kinds = set().union(*rows.values()) - {"wiring"} if rows else set()
        if len(blocks) == 1 and None not in blocks and kinds <= {"check", "pass", "helper"}:
            return blocks.pop()
        return None

    for p in files:
        key = helper_of(p)
        if key:
            put(p, key, layer[key])

    # service: grouped by the kinds of I/O their calls reach
    def reach(p: str) -> frozenset:
        seen, todo, out = {p}, [p], set()
        while todo:
            q = todo.pop()
            for b in (flow_out.get(q, set()) | an["implements"].get(q, set())) - seen:
                seen.add(b)
                t = layer.get(owner.get(b)) if b in owner else None
                if t == "data" or (t == "infra" and owner[b] == "database"):
                    out.add("db")          # through the data layer or straight to the engine: the same way down
                elif t == "infra":
                    out.add(owner[b])
                else:
                    todo.append(b)
        return frozenset(out)

    service = [p for p in files if p not in owner and p not in an["pure"]]
    groups = defaultdict(list)
    for p in service:
        groups[reach(p)].append(p)
    ordered = sorted(groups, key=lambda s: (-len(groups[s]), sorted(s)))
    if len(ordered) > SERVICE_CAP:          # the smallest groups share one block
        ordered, rest = ordered[:SERVICE_CAP - 1], ordered[SERVICE_CAP - 1:]
        groups[frozenset({"other"})] = [p for s in rest for p in groups[s]]
        ordered.append(frozenset({"other"}))
    for sig in ordered:
        key = "service" if len(ordered) == 1 else "service_" + ("_".join(sorted(sig)) or "logic")
        for p in groups[sig]:
            put(p, key, "service")

    # files without I/O: an interface and the class based on it share a block; users in one block -> that block;
    # else the block most files of the directory are in; else shared
    importers = defaultdict(set)          # a file that imports p and uses the name uses p (settings, constants)
    for q in files:
        for row in idx[q]["imports"]:
            if row["target"] and row["target"] != q and idx[q]["uses"].get(row["local"]):
                importers[row["target"]].add(q)
    implemented = defaultdict(set)
    for target, subs in an["implements"].items():
        for s in subs:
            implemented[s].add(target)
    left = [p for p in files if p not in owner]
    changed = True
    while changed and left:
        changed = False
        for p in list(left):
            based = {owner.get(q) for q in an["implements"].get(p, set())} - {None, "shared"}
            bases = {owner.get(q) for q in implemented[p]} - {None, "shared"}
            users = {owner.get(a) for a in set(callers.get(p, {})) | importers[p]}
            # the start-up uses everything it wires: it counts only when no other block uses the file
            users = {k for k in users if layer.get(k) != "entry"} or users
            if len(based) == 1:
                key = based.pop()
            elif len(bases) == 1:
                key = bases.pop()
            elif users and None not in users:
                key = users.pop() if len(users) == 1 else "shared"
            else:
                continue
            owner[p] = key
            left.remove(p)
            changed = True
    for p in left:
        near = Counter(owner[q] for q in files if q in owner and owner[q] != "shared"
                       and PurePosixPath(q).parent == PurePosixPath(p).parent)
        owner[p] = min(near, key=lambda k: (-near[k], k)) if near else "shared"

    paths = compress(owner, files)
    rank = {k: LAYERS.index(t) for k, t in layer.items()}
    blocks = {}
    for key, t in layer.items():
        mine = [p for p in files if owner[p] == key]
        if mine:
            blocks[key] = {"layer": t, "files": mine, "paths": paths.get(key, []),
                           "evidence": evidence(idx, facts, an, mine, t, owner, rank)}
    shared = [p for p in files if owner[p] == "shared"]
    return {"blocks": blocks, "shared": {"files": shared, "paths": paths.get("shared", [])}}
