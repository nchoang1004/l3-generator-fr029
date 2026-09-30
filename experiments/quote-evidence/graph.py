"""Turn the file index into components and candidate edges. No framework knowledge here.

- Components come from the AI grouping (path prefixes); an __init__.py it misses joins a component of the
  same directory, other missed files fall back to their directory. grouping_problems lists signs of a wrong grouping.
- Edges come from resolved imports between components, with the lines that use them and a code-made label.
- External-connection lines are found by a keyword scan over text, so any language works.
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import PurePosixPath

from pyindex import STDLIB

KIND_ORDER = {"call": 0, "decorator": 1, "ref": 2, "annotation": 3, "base": 4, "raise": 5, "except": 6}
CONNECT = re.compile(r"(?i)(https?://|\burl\b|_url\b|\buri\b|\bdsn\b|_host\b|\bhost\s*=|smtp|broker|"
                     r"api_key|apikey|webhook|endpoint|connect\(|create_engine|create_pool|client\()")
NETWORK_STDLIB = {"smtplib", "socket", "http", "urllib", "ftplib", "imaplib", "poplib", "sqlite3", "ssl", "xmlrpc"}


def content_files(idx: dict) -> list[str]:
    return [p for p, e in idx.items() if not e.get("empty")]


def libraries(entry: dict) -> set[str]:
    return {r["external"] for r in entry["imports"]
            if r["external"] and (r["external"] not in STDLIB or r["external"] in NETWORK_STDLIB)}


def ubiquitous(idx: dict) -> set[str]:
    """Libraries imported by a large share of files (the web framework, the ORM): they say little per file."""
    files = content_files(idx)
    common = defaultdict(int)
    for p in files:
        for lib in libraries(idx[p]):
            common[lib] += 1
    return {lib for lib, n in common.items() if n > max(3, len(files) * 0.3)}


def listing(idx: dict, budget: int = 2100) -> str:
    """One line per directory, as detailed as the token budget allows:
    1) files with a few top-level names, 2) file names only, 3) file count and the first file names."""
    from llm import estimate           # local import: graph stays usable without the HTTP client
    files = content_files(idx)
    common = ubiquitous(idx)
    by_dir = defaultdict(list)
    for p in sorted(files):
        by_dir[str(PurePosixPath(p).parent)].append(p)

    def render(level: int) -> str:
        lines = []
        for folder, paths in sorted(by_dir.items()):
            libs = set().union(*(libraries(idx[p]) - common for p in paths))
            names = [PurePosixPath(p).name for p in paths]
            if level == 1:
                parts = []
                for p, name in zip(paths, names):
                    symbols = [s["name"] for s in idx[p]["symbols"]]
                    more = f",+{len(symbols) - 3}" if len(symbols) > 3 else ""
                    parts.append(f"{name}[{','.join(symbols[:3])}{more}]")
                body = " ".join(parts)
            elif level == 2:
                body = " ".join(names)
            else:
                body = f"{len(names)} files: " + " ".join(names[:4]) + (" ..." if len(names) > 4 else "")
            folder = "" if folder == "." else folder + "/"
            lines.append(f"{folder}: {body}" + (f" | libs: {','.join(sorted(libs))}" if libs else ""))
        return "\n".join(lines)

    for level in (1, 2, 3):
        text = render(level)
        if estimate(text) <= budget:
            return text
    return text                        # still too big: the request cap will refuse it and say so


def directory_grouping(idx: dict) -> dict:
    """The grouping a directory walk gives without AI: one component per directory of content files."""
    dirs = sorted({str(PurePosixPath(p).parent) for p in content_files(idx)})
    return {"components": [{"key": d, "members": [d + "/" if d != "." else d], "shared": False} for d in dirs]}


def assemble(idx: dict, answer: dict) -> tuple[dict, list[str]]:
    """Map every content file to one component by the longest matching member prefix."""
    files, issues = content_files(idx), []
    members = []
    for n, comp in enumerate(answer.get("components", [])):
        for m in comp.get("members", []):
            m = m.strip().lstrip("./")
            if m in idx or any(p.startswith(m.rstrip("/") + "/") for p in files):
                members.append((m.rstrip("/") + ("" if m in idx else "/"), n))
            else:
                issues.append(f"component {comp.get('key')}: unknown member {m}")
    owner: dict[str, int | str] = {}
    for p in files:
        hits = [(len(m), n) for m, n in members if p == m or (m.endswith("/") and p.startswith(m))]
        if hits:
            owner[p] = max(hits)[1]
    by_ai, joined = dict(owner), 0
    for p in files:                   # a package __init__ the AI missed joins a component of its directory;
        if p in by_ai:                # other missed modules may have their own role, so they keep their directory
            continue
        near = {n for q, n in by_ai.items() if _parent(q) == _parent(p)} if p.endswith("__init__.py") else set()
        if near:
            held = lambda n: [q for q, m in by_ai.items() if m == n]
            owner[p] = max(near, key=lambda n: (_links(idx, p, held(n)),
                                                sum(_parent(q) == _parent(p) for q in held(n)), -n))
            joined += 1
        else:
            owner[p] = "dir:" + _parent(p)
    if joined:
        issues.append(f"{joined} files not grouped by AI; joined a component holding files of the same directory")
    comps: dict[str, dict] = {}
    keys = answer.get("components", [])
    for p in files:
        o = owner[p]
        if isinstance(o, int):
            cid, key, shared = f"C{o + 1}", keys[o].get("key", f"c{o + 1}"), bool(keys[o].get("shared"))
        else:
            cid, key, shared = o, o, False
        comps.setdefault(cid, {"id": cid, "key": key, "shared": shared, "files": []})["files"].append(p)
    fallback = sorted(c for c in comps if c.startswith("dir:"))
    if fallback:
        issues.append(f"{sum(len(comps[c]['files']) for c in fallback)} files not grouped by AI; grouped by directory")
    for n, cid in enumerate(fallback, start=len(keys) + 1):
        comps[f"C{n}"] = {**comps.pop(cid), "id": f"C{n}"}
    return dict(sorted(comps.items(), key=lambda kv: int(kv[0][1:]))), issues


def _parent(path: str) -> str:
    return str(PurePosixPath(path).parent)


def _links(idx: dict, path: str, files: list[str]) -> int:
    """Imports between one file and a set of files, both directions."""
    group = set(files)
    return (sum(r["target"] in group for r in idx[path]["imports"])
            + sum(r["target"] == path for q in files for r in idx[q]["imports"]))


def _crossing(idx: dict, files: list[str]) -> tuple[str, str] | None:
    """Two sub-directories of a component (below the files' common directory) where one imports the other."""
    parts = [PurePosixPath(p).parent.parts for p in files]
    depth = 0
    while all(len(x) > depth for x in parts) and len({x[depth] for x in parts}) == 1:
        depth += 1
    sub = {p: "/".join(x[:depth + 1]) for p, x in zip(files, parts) if len(x) > depth}
    pairs = sorted((sub[p], sub[r["target"]]) for p in sub for r in idx[p]["imports"]
                   if r["target"] in sub and sub[r["target"]] != sub[p])
    return pairs[0] if pairs else None


def grouping_problems(idx: dict, comps: dict) -> dict[str, str]:
    """Signs, found by code, that the AI grouping is wrong: {component id: reason}.
    Files in sub-directories that import each other are likely different layers. Checks on shared flags were
    tried on 28/09 and dropped: they raised recall on one repo but cut precision on two."""
    out = {}
    for cid, comp in comps.items():
        crossed = None if comp["key"].startswith("dir:") else _crossing(idx, comp["files"])
        if crossed:
            out[cid] = f"mixes sub-directories that import each other: {crossed[0]}/ imports {crossed[1]}/"
    return out


def _definition_line(idx: dict, target: str, symbol: str | None) -> int:
    """Where the imported name is defined in the target file; a whole-module import points at its first declaration."""
    for s in idx[target]["symbols"]:
        if s["name"] == symbol:
            return s["line"]
    return (idx[target]["signals"] or [1])[0]


def candidates(idx: dict, comps: dict) -> dict:
    """Edges between components that an import proves. Each keeps lines on both ends:
    `lines` in the source (the use, then the import) and `target_lines` where the used names are defined."""
    owner = {p: cid for cid, c in comps.items() for p in c["files"]}
    grouped: dict[tuple[str, str], dict] = {}
    for p, entry in idx.items():
        src = owner.get(p)
        if not src:
            continue
        for row in entry["imports"]:
            dst = owner.get(row["target"] or "")
            if not dst or dst == src:
                continue
            uses = entry["uses"].get(row["local"], [])
            edge = grouped.setdefault((src, dst), {"source": src, "target": dst, "symbols": {}, "lines": [],
                                                   "target_lines": []})
            kinds = edge["symbols"].setdefault(row["local"], defaultdict(int))
            for _, kind in uses:
                kinds[kind] += 1
            best = min(uses, key=lambda u: (KIND_ORDER[u[1]], u[0])) if uses else None
            edge["lines"].append((KIND_ORDER[best[1]] if best else 9, p, best[0] if best else row["line"]))
            edge["lines"].append((10, p, row["line"]))
            if uses:
                edge["target_lines"].append([row["target"], _definition_line(idx, row["target"], row["symbol"])])
    edges = {}
    for n, key in enumerate(sorted(grouped), start=1):
        edge = grouped[key]
        if not any(edge["symbols"].values()):
            continue                          # imported but never used, e.g. a re-export
        seen, lines = set(), []
        for _, p, line in sorted(edge["lines"]):
            if (p, line) not in seen:
                seen.add((p, line))
                lines.append([p, line])
        targets = [list(t) for t in dict.fromkeys(map(tuple, edge["target_lines"]))]
        edges[f"E{n}"] = {"id": f"E{n}", "source": edge["source"], "target": edge["target"],
                          "symbols": {s: dict(k) for s, k in edge["symbols"].items()}, "lines": lines[:6],
                          "target_lines": targets[:4]}
    return edges


VERBS = {"call": "gọi", "decorator": "đăng ký qua", "ref": "dùng", "annotation": "dùng kiểu",
         "base": "kế thừa", "raise": "ném", "except": "bắt"}


def edge_label(edge: dict) -> str:
    """Label from the strongest use in code, e.g. 'gọi crud' or 'dùng kiểu User'. No AI involved."""
    kinds = {k for uses in edge["symbols"].values() for k in uses}
    kind = min(kinds, key=KIND_ORDER.get) if kinds else "ref"
    names = [s for s, uses in edge["symbols"].items() if kind in uses][:2]
    return f"{VERBS[kind]} {', '.join(names)}"


def connections(idx: dict, comps: dict, limit: int = 6, per_file: int = 2) -> dict[str, list[list]]:
    """Per component, the lines allowed as evidence of an external system, strongest first:
    lines with connection words (url, dsn, host, smtp, client(...), create_engine...) and the first
    call into each library that few files use (an SDK such as a payment or storage client)."""
    common = ubiquitous(idx)
    out = {}
    for cid, comp in comps.items():
        scored, first_call = [], set()
        for p in comp["files"]:
            entry, mine = idx[p], []
            calls = {c[0]: c[2] for c in entry["external_calls"]}
            for no, text in enumerate(entry["lines"], start=1):
                code = text.strip()
                if not code or code.startswith("#") or ":" in code and re.match(r"^\w+\s*:\s*[\w\[\]| .]+(=.*)?$", code):
                    continue                   # comments and bare settings declarations like 'SMTP_HOST: str = ...'
                hits = len(CONNECT.findall(code))
                lib = calls.get(no)
                rare = lib and lib not in common and (lib not in STDLIB or lib in NETWORK_STDLIB)
                if rare and lib not in first_call:
                    first_call.add(lib)
                    hits += 1
                if hits:
                    mine.append((-(2 * hits + (no in calls)), p, no))
            scored += sorted(mine)[:per_file]
        out[cid] = [[p, no] for _, p, no in sorted(scored)[:limit]]
    return out


def signal_lines(idx: dict, comp: dict, limit: int = 8) -> list[list]:
    """Round-robin over files so every file of the component shows at least one declaration."""
    queues = [[[p, n] for n in idx[p]["signals"]] for p in comp["files"] if idx[p]["signals"]]
    out = []
    while queues and len(out) < limit:
        for q in list(queues):
            if q and len(out) < limit:
                out.append(q.pop(0))
            if not q:
                queues.remove(q)
    return out
