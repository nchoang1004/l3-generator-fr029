"""Internal-edge score of one AI grouping under: old fallback (v4), rule (a), and (a)+(b) when a review exists. No AI call."""
import json, sys, unittest.mock
from pathlib import Path, PurePosixPath
ROOT = Path(r"D:/GitLab-Project/VSF-L3 Generator")
sys.path.insert(0, str(ROOT / "experiments/quote-evidence"))
import graph, inventory, pyindex, ai, evaluate

CASES = [("lnbits", "v5-lnbits", "lnbits_lnbits-958e4da", "lnbits.json"),
         ("teamhide", "v3-teamhide", "teamhide_fastapi-boilerplate-df4e6d4", "teamhide-fastapi-boilerplate.json"),
         ("boilerplate", "v3-boilerplate", "fastapi-boilerplate", "fastapi-boilerplate.json"),
         ("rhoboro", "v4-rhoboro", "rhoboro_async-fastapi-sqlalchemy-6c08827", "rhoboro-async-fastapi-sqlalchemy.json"),
         ("realworld", "realworld-r1", "fastapi-realworld-diagram", "fastapi-realworld.json"),
         ("fullstack", "fullstack-r4", "full-stack-fastapi-template-cb740b6", "full-stack-fastapi-template.json"),
         ("kibo", "kibo-r3", "kibo-backend-89eb3bb", "kibo-backend.json")]

def old_assemble(idx, answer):
    """v4 behaviour: every missed file goes to a component of its own directory."""
    real_parent = graph._parent
    with unittest.mock.patch.object(graph, "_parent", side_effect=lambda p: real_parent(p)) as _:
        pass
    files = graph.content_files(idx)
    comps, issues = graph.assemble(idx, answer)
    # undo rule (a): rebuild with a grouping that lists only the files the AI covered
    covered = []
    for c in answer["components"]:
        covered.append(c)
    ai_files = set()
    for c in answer["components"]:
        for m in c.get("members", []):
            m = m.strip().lstrip("./")
            ai_files |= {p for p in files if p == m or p.startswith(m.rstrip("/") + "/")}
    extra = {}
    for p in files:
        if p not in ai_files:
            extra.setdefault(real_parent(p), []).append(p)
    ans = {"components": list(answer["components"]) + [{"key": "dir:" + d, "members": ps, "shared": False}
                                                       for d, ps in sorted(extra.items())]}
    return graph.assemble(idx, ans)[0]

def score(idx, comps, oracle):
    res = ai.apply(idx, comps, graph.candidates(idx, comps), graph.connections(idx, comps), {})
    res["file_lines"] = {}
    s = evaluate.score(res, oracle)["internal"]
    return f"{s['precision']:.2f}/{s['precision_strict']:.2f}/{s['recall']:.2f} ({len(comps)} khối)"

for name, run, repo, orc in CASES:
    m = json.loads((ROOT / "evaluation/quote-evidence/runs" / run / "graph.json").read_text(encoding="utf-8"))["meta"]
    first = (m.get("review") or {}).get("first_grouping") or m["grouping"]
    idx = pyindex.index(ROOT / "sample-repos" / repo, inventory.scan(ROOT / "sample-repos" / repo))
    oracle = json.loads((ROOT / "experiments/quote-evidence/oracle" / orc).read_text(encoding="utf-8"))
    row = [name, score(idx, old_assemble(idx, first), oracle), score(idx, graph.assemble(idx, first)[0], oracle)]
    if m.get("review"):
        row.append(score(idx, graph.assemble(idx, m["grouping"])[0], oracle))
    print(" | ".join(row))
