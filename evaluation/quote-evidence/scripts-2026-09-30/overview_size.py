"""Size of the repository overview (ai7.overview) on the 8 repos. No AI call.

    python overview_size.py [--limit N] [--show rhoboro]

--show prints the overview of one exposed repo (rule: closed repos, sizes only).
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
Q = ROOT / "experiments/quote-evidence"
sys.path.insert(0, str(Q))
import ai7, calls, flow, graph, inventory, llm, pyindex  # noqa: E402

REPOS = [("rhoboro", "rhoboro-async-fastapi-sqlalchemy", True), ("fullstack", "full-stack-fastapi-template", True),
         ("realworld", "fastapi-realworld", True), ("teamhide", "teamhide-fastapi-boilerplate", True),
         ("boilerplate", "fastapi-boilerplate", False), ("kibo", "kibo-backend", False),
         ("lnbits", "lnbits", False), ("fba", "fastapi-best-architecture", False)]

parser = argparse.ArgumentParser()
parser.add_argument("--limit", type=int, default=ai7.TOP_PROMPT - llm.estimate(ai7.TOP_SYSTEM))
parser.add_argument("--show")
args = parser.parse_args()
print("| Repo | File | Thư mục | Đơn vị | Dòng cây router | Token | Ghi chú |")
print("|---|---:|---:|---:|---:|---:|---|")
for name, orc_name, exposed in REPOS:
    oracle = json.loads((Q / "oracle" / f"{orc_name}.json").read_text(encoding="utf-8"))
    repo = ROOT / oracle["local_dir"]
    idx = pyindex.index(repo, inventory.scan(repo))
    facts = calls.facts(idx)
    an = flow.analyze(idx, facts)
    text, units, issues = ai7.overview(idx, facts, an, args.limit)
    files = graph.content_files(idx)
    dirs = {str(Path(p).parent) for p in files}
    tree = text.split("\n\nDirectories")[0].count("\n")
    print(f"| {name} | {len(files)} | {len(dirs)} | {len(units)} | {tree} | {llm.estimate(text)} | {'; '.join(issues)} |")
    if args.show == name:
        if not exposed:
            sys.exit("closed repo: sizes only")
        print(text)
