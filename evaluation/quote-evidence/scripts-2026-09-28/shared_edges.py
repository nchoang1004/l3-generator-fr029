"""Offline: shared flag by code (fan-in) and edge filters, on the cached AI grouping + (a'). No request is sent."""
import json, sys
from pathlib import Path
ROOT = Path(r"D:/GitLab-Project/VSF-L3 Generator")
sys.path.insert(0, str(ROOT / "experiments/quote-evidence"))
import ai, evaluate, graph, inventory, llm, pyindex

REPOS = {"rhoboro": ("rhoboro_async-fastapi-sqlalchemy-6c08827", "rhoboro-async-fastapi-sqlalchemy.json", "kiểm"),
         "teamhide": ("teamhide_fastapi-boilerplate-df4e6d4", "teamhide-fastapi-boilerplate.json", "kiểm"),
         "boilerplate": ("fastapi-boilerplate", "fastapi-boilerplate.json", "kiểm"),
         "lnbits": ("lnbits_lnbits-958e4da", "lnbits.json", "kiểm"),
         "fba": ("fastapi-practices_fastapi_best_architecture-123a44a", "fastapi-best-architecture.json", "kiểm"),
         "realworld": ("fastapi-realworld-diagram", "fastapi-realworld.json", "chỉnh"),
         "fullstack": ("full-stack-fastapi-template-cb740b6", "full-stack-fastapi-template.json", "chỉnh"),
         "kibo": ("kibo-backend-89eb3bb", "kibo-backend.json", "chỉnh")}
client = llm.Groq("offline", budget=0)
WEAK = {"annotation", "raise", "except"}


def fan_in(comps, edges):
    src = {}
    for e in edges.values():
        src.setdefault(e["target"], set()).add(e["source"])
    return {cid: len(src.get(cid, ())) for cid in comps}


def score(idx, comps, oracle, keep=lambda e: True):
    edges = {k: e for k, e in graph.candidates(idx, comps).items() if keep(e)}
    res = ai.apply(idx, comps, edges, graph.connections(idx, comps), {})
    res["file_lines"] = {}
    s = evaluate.score(res, oracle)["internal"]
    return f"{s['precision']:.2f}/{s['precision_strict']:.2f}/{s['recall']:.2f} ({s['drawn']})"


rows = []
for name, (repo, orc, group) in REPOS.items():
    idx = pyindex.index(ROOT / "sample-repos" / repo, inventory.scan(ROOT / "sample-repos" / repo))
    oracle = json.loads((ROOT / "experiments/quote-evidence/oracle" / orc).read_text(encoding="utf-8"))
    g = ai.group(client, idx)
    g = {"components": [{**c, "members": [m[:-3] if m.endswith("/...") else m for m in c["members"]]}
                        for c in g["components"]]}
    comps, _ = graph.assemble(idx, g)
    n = len(comps)
    fi = fan_in(comps, graph.candidates(idx, comps))
    out = [name, group, str(n), score(idx, comps, oracle)]
    for share in (0.2, 0.3, 0.4):
        t = max(3, round(n * share))
        code = {cid: {**c, "shared": fi[cid] >= t} for cid, c in comps.items()}
        out.append(score(idx, code, oracle))
    t = max(3, round(n * 0.3))
    code = {cid: {**c, "shared": fi[cid] >= t} for cid, c in comps.items()}
    strong = lambda e: any(k not in WEAK for uses in e["symbols"].values() for k in uses)
    out.append(score(idx, comps, oracle, strong))
    out.append(score(idx, code, oracle, strong))
    rows.append(out)
print("| Repo | Nhóm | Khối | AI đặt cờ | Code: fan-in ≥20% | ≥30% | ≥40% | AI cờ + bỏ cạnh chỉ-kiểu | Code 30% + bỏ cạnh chỉ-kiểu |")
print("|---|---|---:|---|---|---|---|---|---|")
for r in rows:
    print("| " + " | ".join(r) + " |")
