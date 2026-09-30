import json, sys
from pathlib import Path, PurePosixPath
sys.path.insert(0, str(Path(__file__).parent))
from ablate import *   # reruns the first table too
print("--- variant: rule (a) only for __init__.py")
for name, run, repo, orc in CASES:
    m = json.loads((ROOT / "evaluation/quote-evidence/runs" / run / "graph.json").read_text(encoding="utf-8"))["meta"]
    first = (m.get("review") or {}).get("first_grouping") or m["grouping"]
    idx = pyindex.index(ROOT / "sample-repos" / repo, inventory.scan(ROOT / "sample-repos" / repo))
    oracle = json.loads((ROOT / "experiments/quote-evidence/oracle" / orc).read_text(encoding="utf-8"))
    files = graph.content_files(idx)
    covered = set()
    for c in first["components"]:
        for mm in c.get("members", []):
            mm = mm.strip().lstrip("./")
            covered |= {p for p in files if p == mm or p.startswith(mm.rstrip("/") + "/")}
    extra = {}
    for p in files:
        if p not in covered and PurePosixPath(p).name != "__init__.py":
            extra.setdefault(graph._parent(p), []).append(p)
    ans = {"components": list(first["components"]) + [{"key": "dir:" + d, "members": ps, "shared": False} for d, ps in sorted(extra.items())]}
    comps = graph.assemble(idx, ans)[0]
    print(name, score(idx, comps, oracle), "| flagged:", list(graph.grouping_problems(idx, comps).values())[:0] or len(graph.grouping_problems(idx, comps)))
