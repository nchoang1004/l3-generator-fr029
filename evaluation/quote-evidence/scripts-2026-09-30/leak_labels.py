"""Which kinds of edges the code draws that the oracle keeps out of the diagram. No AI call; counts only.

With the oracle's own blocks (grouping perfect), every drawn edge the oracle marks acceptable is counted under
its label (wiring, check, pass, up...), with the kind code gave the file pairs behind it.
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
Q = ROOT / "experiments/quote-evidence"
sys.path.insert(0, str(Q))
import calls, evaluate, flow, graph, inventory, pyindex  # noqa: E402

REPOS = [("rhoboro", "rhoboro-async-fastapi-sqlalchemy"), ("fullstack", "full-stack-fastapi-template"),
         ("realworld", "fastapi-realworld"), ("teamhide", "teamhide-fastapi-boilerplate"),
         ("boilerplate", "fastapi-boilerplate"), ("kibo", "kibo-backend"), ("lnbits", "lnbits"),
         ("fba", "fastapi-best-architecture")]
total = Counter()
for name, orc in REPOS:
    oracle = json.loads((Q / "oracle" / f"{orc}.json").read_text(encoding="utf-8"))
    repo = ROOT / oracle["local_dir"]
    idx = pyindex.index(repo, inventory.scan(repo))
    an = flow.analyze(idx, calls.facts(idx))
    blocks = {}
    for p in graph.content_files(idx):
        b = evaluate.oracle_owner(oracle, p)
        if b:
            blocks.setdefault(b, []).append(p)
    rank = {k: flow.RANK.index(v[0]) for k, v in oracle["layers"].items()}
    run = flow.as_run(an, blocks, set(oracle["shared"]), rank)
    s = evaluate.score(run, oracle)["internal"]
    label = {(r[0], r[1]): (r[2] if len(r) > 2 and r[2] in ("wiring", "check", "pass", "up") else "other")
             for r in oracle["acceptable"]}
    counts = Counter(label[tuple(e)] for e in s["not_counted"])
    total += counts
    print(f"{name}: drawn {s['drawn']}, acceptable drawn {len(s['not_counted'])} {dict(counts)}, wrong {len(s['wrong'])}")
print("total", dict(total))
