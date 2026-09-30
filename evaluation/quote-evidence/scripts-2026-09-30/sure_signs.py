"""Dấu hiệu chắc (flow.analyze "sure") so với tầng khối đáp án. Không gọi AI.

    python sure_signs.py [--detail]

Đếm file có dấu hiệu chắc nằm trong khối không dùng chung của đáp án: đúng tầng / tổng.
Cột phụ: file có dấu hiệu chắc nằm trong khối dùng chung, và nằm ngoài đáp án.
--detail in file sai, chỉ cho repo lộ (repo kín chỉ số tổng).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
Q = ROOT / "experiments/quote-evidence"
sys.path.insert(0, str(Q))
import calls, evaluate, flow, graph, inventory, pyindex  # noqa: E402

REPOS = [("rhoboro", "rhoboro-async-fastapi-sqlalchemy", True), ("fullstack", "full-stack-fastapi-template", True),
         ("realworld", "fastapi-realworld", True), ("teamhide", "teamhide-fastapi-boilerplate", True),
         ("boilerplate", "fastapi-boilerplate", False), ("kibo", "kibo-backend", False),
         ("lnbits", "lnbits", False), ("fba", "fastapi-best-architecture", False)]

print("| Repo | File | Có dấu hiệu chắc | Đúng tầng | Trong dùng chung | Ngoài đáp án |")
print("|---|---:|---:|---:|---:|---:|")
total = [0, 0]
for name, orc, exposed in REPOS:
    oracle = json.loads((Q / "oracle" / f"{orc}.json").read_text(encoding="utf-8"))
    repo = ROOT / oracle["local_dir"]
    idx = pyindex.index(repo, inventory.scan(repo))
    an = flow.analyze(idx, calls.facts(idx))
    layer = {k: v[0] for k, v in oracle["layers"].items()}
    judged, wrong, in_shared, outside = 0, [], 0, 0
    for p, (t, line, what) in sorted(an["sure"].items()):
        b = evaluate.oracle_owner(oracle, p)
        if b is None:
            outside += 1
        elif b in oracle["shared"]:
            in_shared += 1
        else:
            judged += 1
            if layer[b] != t:
                wrong.append((p, t, what, b, layer[b]))
    total[0] += judged - len(wrong)
    total[1] += judged
    print(f"| {name} | {len(graph.content_files(idx))} | {len(an['sure'])} | {judged - len(wrong)}/{judged} | "
          f"{in_shared} | {outside} |")
    if "--detail" in sys.argv and exposed and wrong:
        for row in wrong:
            print("    sai:", row)
print(f"\nTổng: {total[0]}/{total[1]}")
