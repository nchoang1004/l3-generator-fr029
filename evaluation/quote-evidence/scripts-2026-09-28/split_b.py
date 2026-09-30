"""Offline: apply only some of the review fixes, to see which (b) rule helps. No request is sent (budget 0)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
ROOT = Path(r"D:/GitLab-Project/VSF-L3 Generator")
sys.path.insert(0, str(ROOT / "experiments/quote-evidence"))
import ai, evaluate, graph, inventory, llm, pyindex

REPOS = {"teamhide": ("teamhide_fastapi-boilerplate-df4e6d4", "teamhide-fastapi-boilerplate.json"),
         "boilerplate": ("fastapi-boilerplate", "fastapi-boilerplate.json"),
         "lnbits": ("lnbits_lnbits-958e4da", "lnbits.json")}
client = llm.Groq("offline", budget=0)


def score(idx, comps, oracle):
    res = ai.apply(idx, comps, graph.candidates(idx, comps), graph.connections(idx, comps), {})
    res["file_lines"] = {}
    s = evaluate.score(res, oracle)["internal"]
    return f"{s['precision']:.2f} / {s['precision_strict']:.2f} / {s['recall']:.2f} ({len(comps)})".replace(".", ",")


for name, (repo, orc) in REPOS.items():
    idx = pyindex.index(ROOT / "sample-repos" / repo, inventory.scan(ROOT / "sample-repos" / repo))
    oracle = json.loads((ROOT / "experiments/quote-evidence/oracle" / orc).read_text(encoding="utf-8"))
    trial = json.loads((ROOT / "evaluation/quote-evidence/runs/c-trial" / f"{name}.json").read_text(encoding="utf-8"))["A"]
    first = ai.group(client, idx)
    comps, _ = graph.assemble(idx, first)
    n = len(first["components"])
    new_rows = trial["grouping"]["components"][n:]
    fixes, at = {}, 0                               # cid -> its replacement rows, in note order
    for note in trial["review"]:
        cid, rest = note.split(" ", 1)
        if " kept:" in rest.split(":")[0] + ":":
            continue
        keys = rest.split(" -> ", 1)[1].split(":", 1)[0].split(", ")
        fixes[cid] = new_rows[at:at + len(keys)]
        at += len(keys)
    kinds = {cid: ("layer" if "mixes" in why else "") + ("+shared" if "shared" in why else "")
             for cid, why in trial["flagged"].items()}
    print(f"\n{name}: flagged {kinds}")
    for label, pick in (("none", set()), ("layer only", {c for c, k in kinds.items() if k.startswith("layer")}),
                        ("shared only", {c for c, k in kinds.items() if "shared" in k}), ("all", set(fixes))):
        rows = [({"key": r["key"], "members": [], "shared": False} if f"C{i + 1}" in pick and f"C{i + 1}" in fixes else r)
                for i, r in enumerate(first["components"])]
        rows += [r for c in pick if c in fixes for r in fixes[c]]
        print(f"  {label:12} {score(idx, graph.assemble(idx, {'components': rows})[0], oracle)}")
