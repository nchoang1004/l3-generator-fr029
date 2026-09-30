"""Table of the grouping trial: A vs C vs no_ai, internal edges P / P strict / R, blocks, flagged, tokens."""
import json, sys
from pathlib import Path
DIR = Path(r"D:/GitLab-Project/VSF-L3 Generator/evaluation/quote-evidence/runs/c-trial")
f = lambda x: f"{x:.2f}".replace(".", ",")
print("| Repo | A P / Pk / R (khối) | C P / Pk / R (khối) | no_ai P / Pk / R (khối) | A báo / token | C báo / token |")
print("|---|---|---|---|---|---|")
for name in sys.argv[1:]:
    r = json.loads((DIR / f"{name}.json").read_text(encoding="utf-8"))
    cell = lambda v: ("lỗi: " + v["error"][:40]) if "error" in v else \
        f"{f(v['score']['precision'])} / {f(v['score']['precision_strict'])} / {f(v['score']['recall'])} ({v['score']['components']})"
    cost = lambda v: "—" if "error" in v else f"{len(v['flagged'])} / {v['tokens']:,}" + \
        (" ⚠" if any("failed" in i for i in v["issues"]) else "")
    print(f"| {name} | {cell(r['A'])} | {cell(r['C'])} | {cell(r['no_ai'])} | {cost(r['A'])} | {cost(r['C'])} |")
