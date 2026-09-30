import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import shared_edges as se      # reuses REPOS, score, helpers (its own table prints first)
import json
print("\n| Repo | AI cờ | V1: AI hoặc (fan-in≥30% và import ≤1 khối) | V2: AI trừ khối import ≥2 khối | V3: V1 rồi V2 |")
print("|---|---|---|---|---|")
for name, (repo, orc, group) in se.REPOS.items():
    idx = se.pyindex.index(se.ROOT / "sample-repos" / repo, se.inventory.scan(se.ROOT / "sample-repos" / repo))
    oracle = json.loads((se.ROOT / "experiments/quote-evidence/oracle" / orc).read_text(encoding="utf-8"))
    g = se.ai.group(se.client, idx)
    g = {"components": [{**c, "members": [m[:-3] if m.endswith("/...") else m for m in c["members"]]} for c in g["components"]]}
    comps, _ = se.graph.assemble(idx, g)
    edges = se.graph.candidates(idx, comps)
    fi = se.fan_in(comps, edges)
    fo = {cid: len({e["target"] for e in edges.values() if e["source"] == cid}) for cid in comps}
    t = max(3, round(len(comps) * 0.3))
    passive = {cid for cid in comps if fi[cid] >= t and fo[cid] <= 1}
    busy = {cid for cid in comps if fo[cid] >= 2}
    v1 = {cid: {**c, "shared": c["shared"] or cid in passive} for cid, c in comps.items()}
    v2 = {cid: {**c, "shared": c["shared"] and cid not in busy} for cid, c in comps.items()}
    v3 = {cid: {**c, "shared": (c["shared"] or cid in passive) and cid not in busy} for cid, c in comps.items()}
    print(f"| {name} ({group}) | " + " | ".join(se.score(idx, x, oracle) for x in (comps, v1, v2, v3)) + " |")
    ch = lambda x: sorted(c["key"] for cid, c in x.items() if c["shared"] != comps[cid]["shared"])
    print(f"|  đổi cờ | | {ch(v1)} | {ch(v2)} | |")
