"""Upper bound of placing files by path (step 2 of the top-down grouping). No AI call.

    python upper_bound.py [--limit N, default: TOP_PROMPT - TOP_SYSTEM] [--detail]

The model can only write paths it sees in the overview (ai7.overview): each directory line, the file names
and sub-directories listed on it. Suppose it writes them perfectly: every visible path goes to the oracle block
holding most of the files whose deepest visible path it is; each file then goes to its deepest visible path.
Reported per repo, over files that belong to an oracle block:
- right: files placed in their oracle block, and %
- wrong: files no visible path can place right (the second pass must ask the model)
- sure_up: files with a sure layer above the layer of their oracle block, or in the shared block (flagged
  ambiguous by the second pass even when placed right)
- paths: visible paths the model must write at least (a path whose block differs from its nearest ancestor's)
Each at the overview limit and with no limit (all directories shown).
--detail  wrong files and sure_up files of the exposed repos (rule: closed repos, totals only).
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[3]
Q = ROOT / "experiments/quote-evidence"
sys.path.insert(0, str(Q))
import ai7, calls, evaluate, flow, inventory, llm, pyindex  # noqa: E402

REPOS = [("rhoboro", "rhoboro-async-fastapi-sqlalchemy", True), ("fullstack", "full-stack-fastapi-template", True),
         ("realworld", "fastapi-realworld", True), ("teamhide", "teamhide-fastapi-boilerplate", True),
         ("boilerplate", "fastapi-boilerplate", False), ("kibo", "kibo-backend", False),
         ("lnbits", "lnbits", False), ("fba", "fastapi-best-architecture", False)]


def visible(units: dict) -> set:
    """Paths written on the overview: directory lines, listed file names and listed sub-directories."""
    out = set()
    for u, ps in units.items():
        base = "" if u == "./" else u
        out.add(base)
        rel = sorted(p[len(base):] for p in ps)
        out |= {base + r for r in [r for r in rel if "/" not in r][:ai7.SHOW_FILES]}
        out |= {base + s for s in sorted({r.split("/")[0] + "/" for r in rel if "/" in r})[:ai7.SHOW_DIRS]}
    return out


def deepest(p: str, paths: set) -> str:
    return max((q for q in paths if p == q or (q.endswith("/") and p.startswith(q)) or q == ""), key=len)


def bound(owner: dict, paths: set) -> tuple:
    mine = defaultdict(list)
    for p in owner:
        mine[deepest(p, paths)].append(p)
    block = {q: Counter(owner[p] for p in ps).most_common(1)[0][0] for q, ps in mine.items()}
    right = [p for p in owner if block[deepest(p, paths)] == owner[p]]
    # paths to write: each visible directory takes the block of most files below it; a path is written when its
    # block differs from the one of its nearest visible ancestor (the top one is always written)
    under = lambda q: [p for p in owner if q == "" or p == q or (q.endswith("/") and p.startswith(q))]
    label = {q: block[q] if q in block and not q.endswith("/") and q else
             Counter(owner[p] for p in under(q)).most_common(1)[0][0] for q in paths if under(q)}

    def written(q: str) -> bool:
        up = [a for a in label if a != q and (a == "" or (a.endswith("/") and q.startswith(a)))]
        return not up or label[max(up, key=len)] != label[q]
    return right, sum(written(q) for q in label)


parser = argparse.ArgumentParser()
parser.add_argument("--limit", type=int, default=ai7.TOP_PROMPT - llm.estimate(ai7.TOP_SYSTEM))
parser.add_argument("--detail", action="store_true")
args = parser.parse_args()
rank = {t: n for n, t in enumerate(ai7.LAYERS)}
print("| Repo | File trong đáp án | Trần: đúng / sai / path | Không trần: đúng / sai / path | sure_up |")
print("|---|---:|---|---|---:|")
details = []
for name, orc_name, exposed in REPOS:
    oracle = json.loads((Q / "oracle" / f"{orc_name}.json").read_text(encoding="utf-8"))
    repo = ROOT / oracle["local_dir"]
    idx = pyindex.index(repo, inventory.scan(repo))
    facts = calls.facts(idx)
    an = flow.analyze(idx, facts)
    owner = {p: b for p in ai7.graph.content_files(idx) if (b := evaluate.oracle_owner(oracle, p))}
    layer = {k: v[0] for k, v in oracle["layers"].items()}
    up = [p for p in owner if p in an["sure"] and (owner[p] in oracle["shared"]
                                                   or rank[an["sure"][p][0]] < rank[layer[owner[p]]])]
    cells = []
    for limit in (args.limit, 10**9):
        _, units, _ = ai7.overview(idx, facts, an, limit)
        right, paths = bound(owner, visible(units))
        n = len(owner)
        cells.append(f"{len(right)} ({len(right) / n:.0%}) / {n - len(right)} / {paths}")
        if exposed and args.detail and limit == args.limit:
            details.append(f"{name} wrong: " + ", ".join(f"{p} ({owner[p]})" for p in owner if p not in right))
    print(f"| {name} | {len(owner)} | {cells[0]} | {cells[1]} | {len(up)} |")
    if exposed and args.detail:
        details.append(f"{name} sure_up: " + ", ".join(f"{p} ({an['sure'][p][0]} in {owner[p]})" for p in up))
print("\n".join(details))
