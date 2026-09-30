"""Score a run against a hand-written oracle, and compare it with two ways that skip AI steps.

Rules (fixed before any AI run):
- Each pipeline component stands for the oracle component with which it shares the most files
  (tie: more lines of code).
- A drawn edge maps to (oracle source, oracle target); edges inside one oracle component are ignored.
- An external system maps to the first oracle external whose alias occurs in its name.
- Mapped edge in `required` = hit; in `acceptable` = not counted; anything else = wrong.
- precision = hits / (hits + wrong); precision_strict = hits / all drawn (acceptable counts as wrong);
  recall = hits / len(required).

flow_score (added 30/09, beside the rules above): flow recall, flow precision and ARI, for a diagram that is
right but drawn another way than the oracle (see its docstring).

Comparisons (internal edges only, externals need AI to be named):
- rule_edges: the same AI components, but every import edge drawn except those touching shared support.
- no_ai: one component per directory, every import edge drawn.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import graph


def oracle_owner(oracle: dict, path: str) -> str | None:
    best = None
    for key, prefixes in oracle["components"].items():
        for p in prefixes:
            if path == p or (p.endswith("/") and path.startswith(p)):
                if best is None or len(p) > best[0]:
                    best = (len(p), key)
    return best[1] if best else None


def _ratio(a: int, b: int) -> float | None:
    return round(a / b, 3) if b else None


def score(run: dict, oracle: dict) -> dict:
    owner = {p: oracle_owner(oracle, p) for c in run["components"] for p in c["files"]}
    sizes = run.get("file_lines", {})
    mapping = {}
    for c in run["components"]:
        counts = {}
        for p in c["files"]:
            if owner[p]:
                files, lines = counts.get(owner[p], (0, 0))
                counts[owner[p]] = (files + 1, lines + sizes.get(p, 0))
        mapping[c["id"]] = max(sorted(counts), key=counts.get) if counts else None
    agree = sum(1 for c in run["components"] for p in c["files"] if owner[p] and owner[p] == mapping[c["id"]])
    total = sum(1 for p in owner if owner[p])

    def ext_id(name: str) -> str:
        low = name.lower()
        for key, aliases in oracle["externals"].items():
            if any(a in low for a in aliases):
                return "ext:" + key
        return "ext?:" + name

    drawn = set()
    for e in run["edges"]:
        a, b = mapping[e["source"]], mapping[e["target"]]
        if a and b and a != b:
            drawn.add((a, b))
    for x in run["externals"]:
        for e in x["edges"]:
            if mapping[e["source"]]:
                drawn.add((mapping[e["source"]], ext_id(x["name"])))
    required = {(r[0], r[1]) for r in oracle["required"]}
    acceptable = {(r[0], r[1]) for r in oracle["acceptable"]}

    def part(pairs: set, req: set) -> dict:
        hits, wrong = pairs & req, pairs - required - acceptable
        return {"precision": _ratio(len(hits), len(hits | wrong)), "precision_strict": _ratio(len(hits), len(pairs)),
                "recall": _ratio(len(hits), len(req)), "drawn": len(pairs), "hits": sorted(hits),
                "wrong": sorted(wrong), "not_counted": sorted(pairs & acceptable), "missed": sorted(req - pairs)}

    is_ext = lambda pair: pair[1].startswith("ext")
    q = run.get("quotes", {})
    return {"all": part(drawn, required),
            "internal": part({p for p in drawn if not is_ext(p)}, {r for r in required if not is_ext(r)}),
            "external": part({p for p in drawn if is_ext(p)}, {r for r in required if is_ext(r)}),
            "quote_validity": _ratio(q.get("valid", 0), q.get("returned", 0)),
            "grouping_agreement": _ratio(agree, total), "components": len(run["components"]),
            "mapping": {c["id"]: [c.get("name") or c.get("key"), mapping[c["id"]]] for c in run["components"]},
            "files_outside_oracle": sorted(p for p, o in owner.items() if o is None)}


def flow_score(run: dict, oracle: dict, share: float = 0.25, hops: int = 3) -> dict:
    """Scores for a diagram drawn another way than the oracle (added 30/09): does it still show the flows?
    - A pipeline block stands for every oracle block holding at least `share` of its files (not only the one with
      most files), so a merged block stands for all the blocks it merged.
    - flow recall: a required internal edge X -> Y is shown when a block standing for X reaches a block standing
      for Y by at most `hops` drawn edges; "merged" when one block stands for both (the flow is hidden inside).
    - flow precision: a drawn edge is right when its ends stand for X, Y with X -> Y required or reached by two
      required edges; neutral when its ends stand for one oracle block only (a split block) or the pair is
      acceptable; else wrong.
    - ARI: adjusted Rand index of the two ways to group the files the oracle names (1 = the same grouping,
      0 = no better than chance), the grouping measure of architecture recovery papers."""
    owner = {p: oracle_owner(oracle, p) for c in run["components"] for p in c["files"]}
    shared_o = set(oracle["shared"])
    stands = {}
    for c in run["components"]:
        if c.get("shared"):
            continue
        count = Counter(owner[p] for p in c["files"] if owner[p] and owner[p] not in shared_o)
        total = sum(count.values())
        stands[c["id"]] = {k for k, n in count.items() if total and n / total >= share}
    out_edges = defaultdict(set)
    for e in run["edges"]:
        if e["source"] in stands and e["target"] in stands:
            out_edges[e["source"]].add(e["target"])

    def reaches(a: str, b: str) -> bool:
        seen, front = {a}, {a}
        for _ in range(hops):
            front = {t for s in front for t in out_edges[s]} - seen
            if b in front:
                return True
            seen |= front
        return False

    required = {(r[0], r[1]) for r in oracle["required"] if not r[1].startswith("ext")}
    acceptable = {(r[0], r[1]) for r in oracle["acceptable"]}
    two_hops = required | {(x, z) for x, y in required for y2, z in required if y == y2 and x != z}
    shown, merged, missed = [], [], []
    for x, y in sorted(required):
        xs = [c for c, ks in stands.items() if x in ks]
        ys = [c for c, ks in stands.items() if y in ks]
        if any(reaches(a, b) for a in xs for b in ys if a != b):
            shown.append([x, y])
        elif set(xs) & set(ys):
            merged.append([x, y])
        else:
            missed.append([x, y])
    right, wrong, neutral = [], [], []
    for a in sorted(out_edges):
        for b in sorted(out_edges[a]):
            pairs = {(x, y) for x in stands[a] for y in stands[b] if x != y}
            (right if pairs & two_hops else neutral if not pairs or pairs & acceptable else wrong).append([a, b])
    labels = [(owner[p], c["id"]) for c in run["components"] for p in c["files"] if owner[p]]
    return {"flow_recall": _ratio(len(shown), len(required)), "flow_precision": _ratio(len(right), len(right) + len(wrong)),
            "shown": len(shown), "merged": len(merged), "missed": missed, "required": len(required),
            "right": len(right), "wrong": wrong, "neutral": len(neutral), "ari": _ari(labels)}


def _ari(labels: list[tuple[str, str]]) -> float | None:
    """Adjusted Rand index between the first and the second label of each item."""
    n = len(labels)
    if n < 2:
        return None
    pairs = lambda k: k * (k - 1) / 2
    both = sum(pairs(v) for v in Counter(labels).values())
    first = sum(pairs(v) for v in Counter(a for a, _ in labels).values())
    second = sum(pairs(v) for v in Counter(b for _, b in labels).values())
    expected = first * second / pairs(n)
    top = (first + second) / 2 - expected
    return round((both - expected) / top, 3) if top else 1.0


def comparisons(idx: dict, comps: dict, edges: dict, run: dict, oracle: dict) -> dict:
    """Internal-edge scores of the two ways that skip AI steps, on the same repository and oracle."""
    rule = [{"source": e["source"], "target": e["target"]} for e in edges.values()
            if not comps[e["source"]]["shared"] and not comps[e["target"]]["shared"]]
    dir_comps, _ = graph.assemble(idx, graph.directory_grouping(idx))
    dir_edges = [{"source": e["source"], "target": e["target"]} for e in graph.candidates(idx, dir_comps).values()]
    no_ai = {"components": list(dir_comps.values()), "edges": dir_edges, "externals": [],
             "file_lines": run.get("file_lines", {})}
    out = {}
    for name, data in (("rule_edges", {**run, "edges": rule, "externals": []}), ("no_ai", no_ai)):
        s = score(data, oracle)
        out[name] = {k: s["internal"][k] for k in ("precision", "precision_strict", "recall", "drawn")}
        out[name]["components"] = s["components"]
        out[name]["grouping_agreement"] = s["grouping_agreement"]
    return out


if __name__ == "__main__":
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    oracle = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    print(json.dumps(score(data, oracle), ensure_ascii=False, indent=2))
