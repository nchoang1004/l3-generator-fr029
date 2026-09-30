"""Compare runs on the 8 repos: strict P / Pk / R, flow P / R, ARI, files in the right block, cost. Totals only.

    python compare_v8.py <run prefix> [<run prefix> ...]      e.g. v7c- v8-nodraft- v8-draft-

A prefix names runs <prefix><repo> in runs/; repos without such a run are skipped. Also scores the code alone:
"luật" (every file by the fallback rules, no model) and "nháp" (the code draft, draft.py).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
Q = ROOT / "experiments/quote-evidence"
RUNS = ROOT / "evaluation/quote-evidence/runs"
sys.path.insert(0, str(Q))
import ai7, calls, draft, evaluate, flow, graph, inventory, pyindex  # noqa: E402

REPOS = [("rhoboro", "rhoboro-async-fastapi-sqlalchemy"), ("fullstack", "full-stack-fastapi-template"),
         ("realworld", "fastapi-realworld"), ("teamhide", "teamhide-fastapi-boilerplate"),
         ("boilerplate", "fastapi-boilerplate"), ("kibo", "kibo-backend"), ("lnbits", "lnbits"),
         ("fba", "fastapi-best-architecture")]
f2 = lambda x: "-" if x is None else f"{x:.2f}".replace(".", ",")


class Nothing:
    calls = []

    def json(self, *a, **k):
        return {}


def code_only(idx, facts, an, use_draft):
    g = ai7.group(Nothing(), idx, facts, an, use_draft)
    out = ai7.describe(Nothing(), idx, facts, an, g, {})
    out["file_lines"] = {p: len(idx[p]["lines"]) for p in graph.content_files(idx)}
    return out


def row(name, label, run, oracle, meta=None):
    s, f = evaluate.score(run, oracle), evaluate.flow_score(run, oracle)
    i = s["internal"]
    blocks = len([c for c in run["components"] if not c.get("shared")])
    cost = ""
    if meta:
        cost = (f"{meta.get('tokens', 0):,} tok, {meta.get('usd', 0)} USD, {meta['timing']['total_s']:.0f} s, "
                f"lượt 1: {meta.get('top', {}).get('source', '?')}, bằng chứng do code {len(meta.get('top', {}).get('evidence_by_code', []))}, "
                f"file theo luật {len(meta.get('by_rule', []))}").replace(",", ".", 1)
    return (f"| {name} | {label} | {blocks} | {f2(i['precision'])} / {f2(i['precision_strict'])} / {f2(i['recall'])} | "
            f"{f2(f['flow_precision'])} / {f2(f['flow_recall'])} (gộp {f['merged']}) | {f2(f['ari'])} | "
            f"{f2(s['grouping_agreement'])} | {cost} |")


print("| Repo | Cách | Khối | P / Pk / R | P luồng / R luồng | ARI | File đúng khối | Chi phí, ghi chú |")
print("|---|---|---:|---|---|---:|---:|---|")
for name, orc in REPOS:
    oracle = json.loads((Q / "oracle" / f"{orc}.json").read_text(encoding="utf-8"))
    repo = ROOT / oracle["local_dir"]
    idx = pyindex.index(repo, inventory.scan(repo))
    facts = calls.facts(idx)
    an = flow.analyze(idx, facts)
    print(row(name, "luật (không AI)", code_only(idx, facts, an, False), oracle))
    print(row(name, "nháp (không AI)", code_only(idx, facts, an, True), oracle))
    for prefix in sys.argv[1:]:
        path = RUNS / f"{prefix}{name}" / "graph.json"
        if path.exists():
            d = json.loads(path.read_text(encoding="utf-8"))
            print(row(name, prefix.rstrip("-"), d, oracle, d["meta"]))
