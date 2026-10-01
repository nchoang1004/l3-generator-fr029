"""Modules of a repository: groups of files that work together, found from the code. No AI.

    modules(idx, an, files) -> {path: module id}

Louvain (Blondel et al. 2008): the partition of the file graph with high modularity, i.e. more links inside a
group than chance would give. Links: a file imports and uses a name of another file, or calls it (flow.analyze
pairs); start-up wiring is left out, since the app factory touches every module. A file with no link is a module
with the other unlinked files of its directory. Deterministic: files are visited in path order.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import PurePosixPath


def links(idx: dict, an: dict, files: list[str]) -> dict:
    """{(a, b): weight}, a < b: 1 per direction in which one file uses the other."""
    mine = set(files)
    used = set()
    for a in files:
        for row in idx[a]["imports"]:
            b = row["target"]
            if b in mine and b != a and idx[a]["uses"].get(row["local"]):
                used.add((a, b))
    for (a, b), (kind, _) in an["pairs"].items():
        if a in mine and b in mine and a != b and kind != "wiring":
            used.add((a, b))
    wiring = {(a, b) for (a, b), (kind, _) in an["pairs"].items() if kind == "wiring"}
    out = defaultdict(float)
    for a, b in used - wiring:
        out[tuple(sorted((a, b)))] += 1.0
    return dict(out)


def louvain(nodes: list, weight: dict) -> dict:
    """{node: community} with high modularity. `weight`: {(a, b): w}, undirected."""
    adj = defaultdict(lambda: defaultdict(float))
    for (a, b), w in weight.items():
        adj[a][b] += w
        adj[b][a] += w
    member = {n: n for n in nodes}                 # original node -> current super node
    level_nodes = list(nodes)
    while True:
        m2 = sum(sum(nb.values()) for nb in adj.values())          # 2m, self loops counted twice
        if not m2:
            break
        deg = {n: sum(adj[n].values()) for n in level_nodes}
        comm = {n: n for n in level_nodes}
        tot = dict(deg)
        moved_any, moved = False, True
        while moved:
            moved = False
            for n in level_nodes:
                old = comm[n]
                tot[old] -= deg[n]
                towards = defaultdict(float)
                for nb, w in adj[n].items():
                    if nb != n:
                        towards[comm[nb]] += w
                best, gain = old, towards.get(old, 0.0) - tot[old] * deg[n] / m2
                for c in sorted(towards, key=str):
                    g = towards[c] - tot[c] * deg[n] / m2
                    if g > gain + 1e-12:
                        best, gain = c, g
                comm[n] = best
                tot[best] += deg[n]
                if best != old:
                    moved = moved_any = True
        if not moved_any:
            break
        new_adj = defaultdict(lambda: defaultdict(float))
        for a in level_nodes:
            for b, w in adj[a].items():
                new_adj[comm[a]][comm[b]] += w
        member = {n: comm[s] for n, s in member.items()}
        level_nodes = sorted(set(comm.values()), key=str)
        adj = new_adj
    return member


def modules(idx: dict, an: dict, files: list[str]) -> dict:
    files = sorted(files)
    weight = links(idx, an, files)
    linked = sorted({p for pair in weight for p in pair})
    member = louvain(linked, weight)
    out = {p: "m:" + member[p] for p in linked}
    for p in files:
        if p not in out:
            out[p] = "d:" + str(PurePosixPath(p).parent)
    return out
