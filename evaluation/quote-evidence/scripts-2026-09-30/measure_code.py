"""Measure the code-only steps of the v7 pipeline (calls.py, flow.py) against oracle rev 4. No AI call.

    python measure_code.py [--detail]

--detail   print wrong and missed edges and wrong tiers, for the exposed repos only
           (rule: closed repos, totals only).

A.  tier the code gives each block (highest sign among its files) vs the oracle layer; and, for files
    with a sign (entry, api, data, infra), the file tier vs the layer of its block
B.  flow edges grouped by the oracle blocks, edges going up judged by oracle layers: P / Pk / R
B'. the same, edges going up judged by the tiers the code gives each block
C.  required internal edges that have no import: found / total
D.  files the code marks "no I/O" vs files of the shared block: P / R
E.  blocks no flow reaches from an entry point: expected idle found / expected, other idle blocks
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
IDLE = {"teamhide": {"cache", "celery"}, "boilerplate": {"cache", "taskiq"}, "realworld": {"services"}}
f2 = lambda x: "-" if x is None else f"{x:.2f}".replace(".", ",")
ratio = lambda a, b: f"{a}/{b}"


def measure(name: str, orc_name: str, exposed: bool) -> list[str]:
    oracle = json.loads((Q / "oracle" / f"{orc_name}.json").read_text(encoding="utf-8"))
    repo = ROOT / oracle["local_dir"]
    idx = pyindex.index(repo, inventory.scan(repo))
    an = flow.analyze(idx, calls.facts(idx))
    shared = set(oracle["shared"])
    blocks = {}
    for p in graph.content_files(idx):
        b = evaluate.oracle_owner(oracle, p)
        if b:
            blocks.setdefault(b, []).append(p)
    layer = {k: v[0] for k, v in oracle["layers"].items()}
    tier_of = lambda p: an["tier"].get(p, ["unknown"])[0]

    # A
    own = [(p, b) for b, ps in blocks.items() if b not in shared for p in ps if tier_of(p) in ("entry", "api", "data", "infra")]
    wrong_tier = [(p, b, tier_of(p)) for p, b in own if tier_of(p) != layer.get(b)]
    block_wrong = [(b, flow.block_tier(an, ps), layer[b]) for b, ps in blocks.items()
                   if b not in shared and flow.block_tier(an, ps) != layer[b]]
    # B, B'
    rank = {b: flow.RANK.index(layer[b]) for b in layer}
    code_rank = {b: flow.RANK.index(flow.block_tier(an, ps)) for b, ps in blocks.items()}
    s = evaluate.score(flow.as_run(an, blocks, shared, rank), oracle)
    s2 = evaluate.score(flow.as_run(an, blocks, shared, code_rank), oracle)
    # C
    comps = {b: {"id": b, "key": b, "shared": b in shared, "files": ps} for b, ps in blocks.items()}
    imported = {(e["source"], e["target"]) for e in graph.candidates(idx, comps).values()}
    no_import = [(r[0], r[1]) for r in oracle["required"] if not r[1].startswith("ext:") and (r[0], r[1]) not in imported]
    found = [x for x in no_import if tuple(x) in {tuple(h) for h in s["internal"]["hits"]}]
    # D
    shared_files = {p for b in shared for p in blocks.get(b, [])}
    owned = {p for ps in blocks.values() for p in ps}
    pure = an["pure"] & owned
    # E
    idle = {b for b, ps in blocks.items() if b not in shared and layer.get(b) != "entry"
            and not set(ps) & an["reached"]}
    expected = IDLE.get(name, set())

    i, x, i2 = s["internal"], s["external"], s2["internal"]
    n_blocks = len(blocks) - len(shared & set(blocks))
    row = [name, f"{ratio(n_blocks - len(block_wrong), n_blocks)}; file {ratio(len(own) - len(wrong_tier), len(own))}",
           f"{f2(i['precision'])} / {f2(i['precision_strict'])} / {f2(i['recall'])}",
           f"{f2(i2['precision'])} / {f2(i2['precision_strict'])} / {f2(i2['recall'])}",
           f"{f2(x['precision'])} / {f2(x['recall'])}",
           ratio(len(found), len(no_import)),
           f"{f2(len(pure & shared_files) / len(pure) if pure else None)} / "
           f"{f2(len(pure & shared_files) / len(shared_files) if shared_files else None)}",
           f"{ratio(len(idle & expected), len(expected))} (+{len(idle - expected)})"]
    if "--detail" in sys.argv and exposed:
        print(f"\n== {name}")
        print("  khối sai tầng (khối, code, đáp án):", block_wrong)
        print("  file sai tầng:", [(p, b, t) for p, b, t in wrong_tier])
        for part in ("internal", "external"):
            print(f"  {part}: sai {s[part]['wrong']}\n    thiếu {s[part]['missed']}\n    không tính {s[part]['not_counted']}")
        print("  không qua import:", no_import, "tìm được:", found)
        print("  không IO nhưng không dùng chung:", sorted(pure - shared_files))
        print("  dùng chung mà code không thấy:", sorted(shared_files - pure))
        print("  khối không ai tới:", sorted(idle), "mong đợi:", sorted(expected))
    return row


rows = [measure(*r) for r in REPOS]
print("| Repo | A tầng đúng: khối; file có dấu hiệu | B: P / Pk / R | B': P / Pk / R | Ngoài: P / R | C không qua import | D dùng chung: P / R | E khối không ai gọi |")
print("|---|---|---|---|---|---|---|---|")
for r in rows:
    print("| " + " | ".join(r) + " |")
