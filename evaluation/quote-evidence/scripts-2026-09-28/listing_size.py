"""Token size of the directory listing at each detail level, per repo. No AI call."""
import sys
from pathlib import Path
ROOT = Path(r"D:/GitLab-Project/VSF-L3 Generator")
sys.path.insert(0, str(ROOT / "experiments/quote-evidence"))
import ai, graph, inventory, llm, pyindex

REPOS = {"rhoboro": "rhoboro_async-fastapi-sqlalchemy-6c08827", "teamhide": "teamhide_fastapi-boilerplate-df4e6d4",
         "boilerplate": "fastapi-boilerplate", "lnbits": "lnbits_lnbits-958e4da",
         "realworld": "fastapi-realworld-diagram", "fullstack": "full-stack-fastapi-template-cb740b6",
         "kibo": "kibo-backend-89eb3bb", "fba": "fastapi-practices_fastapi_best_architecture-123a44a"}
print("repo | files | dirs | level1 (names+symbols) | level2 (names) | used today | top-level branches")
for name, repo in REPOS.items():
    idx = pyindex.index(ROOT / "sample-repos" / repo, inventory.scan(ROOT / "sample-repos" / repo))
    sizes = [llm.estimate(graph.listing(idx, budget=10**9 if lvl == 1 else 0)) for lvl in (1,)]
    lvl1 = llm.estimate(graph.listing(idx, budget=10**9))
    files = graph.content_files(idx)
    dirs = {str(Path(p).parent) for p in files}
    # level 2 size: rebuild by forcing a budget between level1 and level2
    lvl2 = None
    for b in range(0, lvl1 + 1, 50):
        t = graph.listing(idx, budget=b)
        if "[" not in t and "files:" not in t:
            lvl2 = llm.estimate(t); break
    used = llm.estimate(graph.listing(idx))
    branches = {}
    for p in files:
        parts = Path(p).parts
        key = "/".join(parts[:2]) if len(parts) > 2 else parts[0] if len(parts) > 1 else "."
        branches[key] = branches.get(key, 0) + 1
    print(f"{name} | {len(files)} | {len(dirs)} | {lvl1} | {lvl2} | {used} | {len(branches)}")
print("group request = system", llm.estimate(ai.GROUP_SYSTEM), "+ listing + 4400 answer; cap 7000")
