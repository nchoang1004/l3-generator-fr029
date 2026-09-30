"""Bảng đếm tầng file neo: code xếp (dòng) so với tầng khối đáp án (cột). Chỉ in số, không in tên file.

    python tier_confusion.py lnbits [fba ...]

File neo = file có dấu hiệu riêng (entry, api, data, infra). Chỉ đếm file thuộc khối không dùng chung của đáp án.
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
Q = ROOT / "experiments/quote-evidence"
sys.path.insert(0, str(Q))
import calls, evaluate, flow, graph, inventory, pyindex  # noqa: E402

ORACLES = {"rhoboro": "rhoboro-async-fastapi-sqlalchemy", "fullstack": "full-stack-fastapi-template",
           "realworld": "fastapi-realworld", "teamhide": "teamhide-fastapi-boilerplate",
           "boilerplate": "fastapi-boilerplate", "kibo": "kibo-backend", "lnbits": "lnbits",
           "fba": "fastapi-best-architecture"}
ANCHOR = ("entry", "api", "data", "infra")

for name in sys.argv[1:]:
    oracle = json.loads((Q / "oracle" / f"{ORACLES[name]}.json").read_text(encoding="utf-8"))
    repo = ROOT / oracle["local_dir"]
    idx = pyindex.index(repo, inventory.scan(repo))
    an = flow.analyze(idx, calls.facts(idx))
    layer = {k: v[0] for k, v in oracle["layers"].items()}
    count = Counter()
    for p in graph.content_files(idx):
        t = an["tier"].get(p, ["unknown"])[0]
        b = evaluate.oracle_owner(oracle, p)
        if t in ANCHOR and b and b not in oracle["shared"]:
            count[(t, layer[b])] += 1
    cols = list(flow.RANK)
    print(f"\n{name}: {sum(count.values())} file neo, {sum(n for (t, l), n in count.items() if t != l)} sai tầng")
    print("| Code xếp \\ Bản vẽ | " + " | ".join(cols) + " | Tổng |")
    print("|---|" + "---:|" * (len(cols) + 1))
    for t in ANCHOR:
        row = [count[(t, c)] for c in cols]
        print(f"| {t} | " + " | ".join(str(n) for n in row) + f" | {sum(row)} |")
