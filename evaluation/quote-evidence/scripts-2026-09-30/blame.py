"""Where do the errors of a run come from: grouping (the blocks) or code (edges drawn from blocks)?
Counts only, so closed repos stay closed. No AI call.

For each run: the same repo scored with the oracle's own blocks (code only, measure_code's B) gives the edges
code draws when grouping is perfect. A required edge the run misses is blamed on grouping when code finds it
with oracle blocks, on code otherwise; a wrong edge is blamed on code when it is drawn with oracle blocks too.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
Q = ROOT / "experiments/quote-evidence"
sys.path.insert(0, str(Q))
import ai7, calls, evaluate, flow, graph, inventory, pyindex  # noqa: E402

ORACLE = {"rhoboro": "rhoboro-async-fastapi-sqlalchemy", "fullstack": "full-stack-fastapi-template",
          "realworld": "fastapi-realworld", "teamhide": "teamhide-fastapi-boilerplate",
          "boilerplate": "fastapi-boilerplate", "kibo": "kibo-backend", "lnbits": "lnbits",
          "fba": "fastapi-best-architecture"}
RUNS = sys.argv[1:]
cache = {}


def repo_facts(name):
    if name not in cache:
        oracle = json.loads((Q / "oracle" / f"{ORACLE[name]}.json").read_text(encoding="utf-8"))
        repo = ROOT / oracle["local_dir"]
        idx = pyindex.index(repo, inventory.scan(repo))
        an = flow.analyze(idx, calls.facts(idx))
        blocks = {}
        for p in graph.content_files(idx):
            b = evaluate.oracle_owner(oracle, p)
            if b:
                blocks.setdefault(b, []).append(p)
        shared = set(oracle["shared"])
        rank = {k: flow.RANK.index(v[0]) for k, v in oracle["layers"].items()}
        perfect = evaluate.score(flow.as_run(an, blocks, shared, rank), oracle)["internal"]
        cache[name] = (oracle, perfect)
    return cache[name]


f2 = lambda x: "-" if x is None else f"{x:.2f}".replace(".", ",")
rows = []
for run in RUNS:
    d = json.loads((ROOT / "evaluation/quote-evidence/runs" / run / "graph.json").read_text(encoding="utf-8"))
    name = next(k for k in ORACLE if run.endswith(k))
    oracle, perfect = repo_facts(name)
    s = evaluate.score(d, oracle)
    i = s["internal"]
    found = {tuple(e) for e in perfect["hits"]}
    perfect_wrong = {tuple(e) for e in perfect["wrong"]} | {tuple(e) for e in perfect["not_counted"]}
    missed = [tuple(e) for e in i["missed"]]
    wrong = [tuple(e) for e in i["wrong"]] + [tuple(e) for e in i["not_counted"]]
    miss_group = sum(e in found for e in missed)
    wrong_code = sum(e in perfect_wrong for e in wrong)
    oracle_blocks = [k for k in oracle["components"] if k not in oracle["shared"]]
    mapped = Counter(m[1] for cid, m in s["mapping"].items() if m[1])
    lost = sum(1 for k in oracle_blocks if k not in mapped)
    extra = sum(n - 1 for k, n in mapped.items() if k not in oracle["shared"] and n > 1)
    meta = d["meta"]
    issues = " ".join(meta.get("issues", []))
    dropped = re.search(r"blocks dropped for a reason not in the code: ([^\n]*?)(?:$|top:)", issues)
    by_rule = len(meta.get("by_rule", []))
    rows.append([run, f2(i["precision"]), f2(i["precision_strict"]), f2(i["recall"]), f2(s["grouping_agreement"]),
                 f"{len([c for c in d['components'] if not c.get('shared')])}/{len(oracle_blocks)}", str(lost), str(extra),
                 f"{len(missed)} = {miss_group} khối + {len(missed) - miss_group} code",
                 f"{len(wrong)} = {len(wrong) - wrong_code} khối + {wrong_code} code",
                 str(len(dropped[1].split(",")) if dropped else 0), str(by_rule), str(meta.get("tokens", "?"))])
print("| Lần chạy | P | Pk | R | File đúng khối | Khối chạy/đáp án | Khối đáp án bị mất | Khối thừa (tách đôi) | "
      "Cạnh thiếu | Cạnh sai (gồm acceptable) | Khối lượt 1 bị bỏ | File theo luật | Token |")
print("|" + "---|" * 13)
for r in rows:
    print("| " + " | ".join(r) + " |")
print("\nKhối đúng như đáp án (chỉ code): P / Pk / R, cạnh sai, cạnh thiếu")
for name, (oracle, p) in cache.items():
    print(f"  {name}: {f2(p['precision'])} / {f2(p['precision_strict'])} / {f2(p['recall'])}, sai {len(p['wrong'])} + "
          f"acceptable {len(p['not_counted'])}, thiếu {len(p['missed'])} / {len(p['hits']) + len(p['missed'])}")
