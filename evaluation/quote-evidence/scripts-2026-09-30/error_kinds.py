"""Why a run misses or draws a wrong edge, as counts per cause (closed repos stay closed). No AI call.

    python error_kinds.py <run prefix> [...]      e.g. v8-nodraft- v8-draft-   ("luật" = no AI, always shown)

A pipeline block "holds" an oracle block when at least 25% of its files belong to it (evaluate.flow_score).
Missed required edge X -> Y:
  merged    one block holds both X and Y (the flow is inside a block)
  lost      X or Y is held by some block but no block is mapped to it (it is a minority in every block holding it:
            the strict score maps each block to the oracle block with most files)
  absent    X and Y have mapped blocks, no edge drawn between them (grouping elsewhere, or code)
  nowhere   X or Y is held by no block (its files sit in shared or in blocks where they are few)
Wrong drawn edge A -> B (mapped pair neither required nor acceptable):
  mapping   the blocks also hold a pair that is required (right under the flow score)
  real      otherwise
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
Q = ROOT / "experiments/quote-evidence"
RUNS = ROOT / "evaluation/quote-evidence/runs"
sys.path.insert(0, str(Q))
import ai7, calls, evaluate, flow, graph, inventory, pyindex  # noqa: E402

REPOS = [("rhoboro", "rhoboro-async-fastapi-sqlalchemy"), ("fullstack", "full-stack-fastapi-template"),
         ("realworld", "fastapi-realworld"), ("teamhide", "teamhide-fastapi-boilerplate"),
         ("boilerplate", "fastapi-boilerplate"), ("kibo", "kibo-backend"), ("lnbits", "lnbits"),
         ("fba", "fastapi-best-architecture")]


class Nothing:
    calls = []

    def json(self, *a, **k):
        return {}


def kinds(run: dict, oracle: dict) -> tuple[Counter, Counter, int, int]:
    s = evaluate.score(run, oracle)
    i = s["internal"]
    owner = {p: evaluate.oracle_owner(oracle, p) for c in run["components"] for p in c["files"]}
    shared_o = set(oracle["shared"])
    holds = {}
    for c in run["components"]:
        if c.get("shared"):
            continue
        n = Counter(owner[p] for p in c["files"] if owner[p] and owner[p] not in shared_o)
        total = sum(n.values())
        holds[c["id"]] = {k for k, v in n.items() if total and v / total >= 0.25}
    mapped = defaultdict(set)
    for cid, (_, o) in s["mapping"].items():
        if cid in holds and o:
            mapped[o].add(cid)
    miss = Counter()
    for x, y in (tuple(e) for e in i["missed"]):
        hx = {c for c, ks in holds.items() if x in ks}
        hy = {c for c, ks in holds.items() if y in ks}
        if hx & hy:
            miss["merged"] += 1
        elif not hx or not hy:
            miss["nowhere"] += 1
        elif not mapped[x] or not mapped[y]:
            miss["lost"] += 1
        else:
            miss["absent"] += 1
    required = {(r[0], r[1]) for r in oracle["required"]}
    wrong = Counter()
    edges = {(e["source"], e["target"]) for e in run["edges"]}
    for a, b in (tuple(e) for e in i["wrong"]):
        pairs = {(x, y) for (s1, s2) in edges if s["mapping"].get(s1, [0, None])[1] == a
                 and s["mapping"].get(s2, [0, None])[1] == b for x in holds.get(s1, ()) for y in holds.get(s2, ())}
        wrong["mapping" if pairs & required else "real"] += 1
    return miss, wrong, len(i["not_counted"]), len(i["missed"]) + len(i["hits"])


def code_only(idx, facts, an):
    g = ai7.group(Nothing(), idx, facts, an, False)
    out = ai7.describe(Nothing(), idx, facts, an, g, {})
    out["file_lines"] = {p: len(idx[p]["lines"]) for p in graph.content_files(idx)}
    return out


print("| Repo | Cách | Cạnh thiếu: gộp / mất khối / không vẽ / không khối nào giữ | Cạnh sai: do ánh xạ / sai thật | "
      "Cạnh chấp nhận được bị vẽ | Cạnh bắt buộc |")
print("|---|---|---|---|---:|---:|")
total = defaultdict(Counter)
for name, orc in REPOS:
    oracle = json.loads((Q / "oracle" / f"{orc}.json").read_text(encoding="utf-8"))
    repo = ROOT / oracle["local_dir"]
    idx = pyindex.index(repo, inventory.scan(repo))
    facts = calls.facts(idx)
    an = flow.analyze(idx, facts)
    runs = [("luật", code_only(idx, facts, an))]
    for prefix in sys.argv[1:]:
        path = RUNS / f"{prefix}{name}" / "graph.json"
        if path.exists():
            runs.append((prefix.rstrip("-"), json.loads(path.read_text(encoding="utf-8"))))
    for label, run in runs:
        miss, wrong, acc, req = kinds(run, oracle)
        total[label] += miss + Counter({"w_" + k: v for k, v in wrong.items()}) + Counter(acc=acc, req=req)
        print(f"| {name} | {label} | {miss['merged']} / {miss['lost']} / {miss['absent']} / {miss['nowhere']} | "
              f"{wrong['mapping']} / {wrong['real']} | {acc} | {req} |")
print("\nTổng 8 repo:")
for label, c in total.items():
    print(f"  {label}: thiếu gộp {c['merged']}, mất khối {c['lost']}, không vẽ {c['absent']}, không khối nào giữ "
          f"{c['nowhere']}; sai do ánh xạ {c['w_mapping']}, sai thật {c['w_real']}; chấp nhận được bị vẽ {c['acc']}; "
          f"bắt buộc {c['req']}")
