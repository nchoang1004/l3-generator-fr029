"""Pass-1 checks (ai7._violations) run on the oracle itself, as if it were the model's answer. No AI call.

    python top_check_oracle.py

Any problem found here is a false alarm of the checks. Exposed repos: each problem; closed repos: counts only.
Also prints the size of the first pass-1 request (overview + TOP_SYSTEM) and the answer room left.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
Q = ROOT / "experiments/quote-evidence"
sys.path.insert(0, str(Q))
import ai7, calls, flow, inventory, llm, pyindex  # noqa: E402

REPOS = [("rhoboro", "rhoboro-async-fastapi-sqlalchemy", True), ("fullstack", "full-stack-fastapi-template", True),
         ("realworld", "fastapi-realworld", True), ("teamhide", "teamhide-fastapi-boilerplate", True),
         ("boilerplate", "fastapi-boilerplate", False), ("kibo", "kibo-backend", False),
         ("lnbits", "lnbits", False), ("fba", "fastapi-best-architecture", False)]

limit = ai7.TOP_PROMPT - llm.estimate(ai7.TOP_SYSTEM)
print(f"TOP_SYSTEM {llm.estimate(ai7.TOP_SYSTEM)} tokens; overview limit {limit}")
for name, orc_name, exposed in REPOS:
    oracle = json.loads((Q / "oracle" / f"{orc_name}.json").read_text(encoding="utf-8"))
    repo = ROOT / oracle["local_dir"]
    idx = pyindex.index(repo, inventory.scan(repo))
    facts = calls.facts(idx)
    an = flow.analyze(idx, facts)
    blocks = {k: {"layer": oracle["layers"][k][0], "paths": v} for k, v in oracle["components"].items()
              if k not in oracle["shared"]}
    shared = [p for k in oracle["shared"] for p in oracle["components"][k]]
    found = ai7._violations(idx, facts, an, blocks, shared)
    text, _, _ = ai7.overview(idx, facts, an, limit)
    prompt = llm.estimate(ai7.TOP_SYSTEM + text)
    kinds = {}
    for p in found:
        kind = ("cap" if "above the limit" in p else "api" if p.startswith("api blocks") else
                "one caller" if "called only by" in p else "data" if p.startswith("data block") else "shared")
        kinds[kind] = kinds.get(kind, 0) + 1
    print(f"{name}: prompt {prompt}, answer room {ai7.LIMIT - prompt}; false alarms {len(found)} {kinds}")
    if exposed:
        for p in found:
            print("   ", p)
