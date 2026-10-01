"""Score the code draft of blocks (draft.py) against oracle rev 4, without any AI. Totals only (closed repos).

    python draft_score.py [--show rhoboro]

--show prints the draft of one exposed repo.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
Q = ROOT / "experiments/quote-evidence"
sys.path.insert(0, str(Q))
import calls, draft, evaluate, flow, graph, inventory, pyindex  # noqa: E402

REPOS = [("rhoboro", "rhoboro-async-fastapi-sqlalchemy", True), ("fullstack", "full-stack-fastapi-template", True),
         ("realworld", "fastapi-realworld", True), ("teamhide", "teamhide-fastapi-boilerplate", True),
         ("boilerplate", "fastapi-boilerplate", False), ("kibo", "kibo-backend", False),
         ("lnbits", "lnbits", False), ("fba", "fastapi-best-architecture", False),
         ("tdd-docker", "fastapi-tdd-docker", False), ("agentgpt", "agentgpt", False)]
f2 = lambda x: "-" if x is None else f"{x:.2f}".replace(".", ",")

parser = argparse.ArgumentParser()
parser.add_argument("--show")
args = parser.parse_args()
print("| Repo | Khối nháp (đáp án) | Nội bộ: P / Pk / R | Ngoài: P / R | File đúng khối |")
print("|---|---|---|---|---|")
for name, orc, exposed in REPOS:
    oracle = json.loads((Q / "oracle" / f"{orc}.json").read_text(encoding="utf-8"))
    repo = ROOT / oracle["local_dir"]
    idx = pyindex.index(repo, inventory.scan(repo))
    facts = calls.facts(idx)
    an = flow.analyze(idx, facts)
    d = draft.draft(idx, facts, an)
    blocks = {k: b["files"] for k, b in d["blocks"].items()}
    if d["shared"]["files"]:
        blocks["shared"] = d["shared"]["files"]
    rank = {k: flow.RANK.index(b["layer"]) for k, b in d["blocks"].items()}
    run = flow.as_run(an, blocks, {"shared"} & set(blocks), rank)
    run["file_lines"] = {p: len(idx[p]["lines"]) for p in graph.content_files(idx)}
    s = evaluate.score(run, oracle)
    i, e = s["internal"], s["external"]
    print(f"| {name} | {len(d['blocks'])} ({len(oracle['components']) - len(oracle['shared'])}) | "
          f"{f2(i['precision'])} / {f2(i['precision_strict'])} / {f2(i['recall'])} | {f2(e['precision'])} / "
          f"{f2(e['recall'])} | {f2(s['grouping_agreement'])} |")
    if args.show == name:
        if not exposed:
            sys.exit("closed repo: totals only")
        for k, b in d["blocks"].items():
            print(f"   {k} ({b['layer']}): {', '.join(b['paths'])} | evidence {b['evidence']}")
        print(f"   shared: {', '.join(d['shared']['paths'])}")
        print(f"   hits {i['hits']}\n   wrong {i['wrong']}\n   missed {i['missed']}")
