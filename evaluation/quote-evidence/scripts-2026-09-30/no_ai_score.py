"""Whole v7 pipeline with no model (every request answers nothing, so every file is placed by the fallback
rules), scored against oracle rev 4. No AI call. Totals only (closed repos: no detail)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
Q = ROOT / "experiments/quote-evidence"
sys.path.insert(0, str(Q))
import ai7, calls, evaluate, flow, graph, inventory, pyindex  # noqa: E402

REPOS = [("rhoboro", "rhoboro-async-fastapi-sqlalchemy"), ("fullstack", "full-stack-fastapi-template"),
         ("realworld", "fastapi-realworld"), ("teamhide", "teamhide-fastapi-boilerplate"),
         ("boilerplate", "fastapi-boilerplate"), ("kibo", "kibo-backend"), ("lnbits", "lnbits"),
         ("fba", "fastapi-best-architecture"),
         ("tdd-docker", "fastapi-tdd-docker"), ("agentgpt", "agentgpt")]


class Nothing:
    calls = []

    def json(self, *a, **k):
        return {}


f2 = lambda x: "-" if x is None else f"{x:.2f}".replace(".", ",")
print("| Repo | Khối (đáp án) | Nội bộ: P / Pk / R | Ngoài: P / R | File đúng khối |")
print("|---|---|---|---|---|")
for name, orc in REPOS:
    oracle = json.loads((Q / "oracle" / f"{orc}.json").read_text(encoding="utf-8"))
    repo = ROOT / oracle["local_dir"]
    idx = pyindex.index(repo, inventory.scan(repo))
    facts = calls.facts(idx)
    an = flow.analyze(idx, facts)
    g = ai7.group(Nothing(), idx, facts, an)
    out = ai7.describe(Nothing(), idx, facts, an, g, {})
    out["file_lines"] = {p: len(idx[p]["lines"]) for p in graph.content_files(idx)}
    s = evaluate.score(out, oracle)
    i, e = s["internal"], s["external"]
    n = len([c for c in out["components"] if not c["shared"]])
    print(f"| {name} | {n} ({len(oracle['components']) - len(oracle['shared'])}) | {f2(i['precision'])} / "
          f"{f2(i['precision_strict'])} / {f2(i['recall'])} | {f2(e['precision'])} / {f2(e['recall'])} | "
          f"{f2(s['grouping_agreement'])} |")
