"""Grouping-only trial: A = current AI grouping + (a') + (b), C = directory proposal with AI operations + (b).
Internal edges are drawn by rule, so they are scored without the describe step.
Usage: python trial_c.py <budget> <repo names...>   (key from GROQ_API_KEY in the environment)"""
import json, sys, time
from pathlib import Path
ROOT = Path(r"D:/GitLab-Project/VSF-L3 Generator")
sys.path.insert(0, str(ROOT / "experiments/quote-evidence"))
import ai, evaluate, graph, inventory, llm, pyindex

REPOS = {"rhoboro": ("rhoboro_async-fastapi-sqlalchemy-6c08827", "rhoboro-async-fastapi-sqlalchemy.json"),
         "teamhide": ("teamhide_fastapi-boilerplate-df4e6d4", "teamhide-fastapi-boilerplate.json"),
         "boilerplate": ("fastapi-boilerplate", "fastapi-boilerplate.json"),
         "lnbits": ("lnbits_lnbits-958e4da", "lnbits.json"),
         "realworld": ("fastapi-realworld-diagram", "fastapi-realworld.json"),
         "fullstack": ("full-stack-fastapi-template-cb740b6", "full-stack-fastapi-template.json"),
         "kibo": ("kibo-backend-89eb3bb", "kibo-backend.json"),
         "fba": ("fastapi-practices_fastapi_best_architecture-123a44a", "fastapi-best-architecture.json")}
OUT = ROOT / "evaluation/quote-evidence/runs/c-trial"
OUT.mkdir(parents=True, exist_ok=True)
client = llm.Groq(llm.load_key(ROOT / ".env"), int(sys.argv[1]))


def score(idx, comps, oracle):
    res = ai.apply(idx, comps, graph.candidates(idx, comps), graph.connections(idx, comps), {})
    res["file_lines"] = {}
    s = evaluate.score(res, oracle)
    return {k: s["internal"][k] for k in ("precision", "precision_strict", "recall", "drawn")} | {
        "components": len(comps), "grouping_agreement": s["grouping_agreement"]}


def variant(idx, oracle, first_step):
    start, n0 = time.perf_counter(), len(client.calls)
    try:
        grouping, notes = first_step()
    except Exception as exc:
        return {"error": str(exc)[:300]}
    comps, issues = graph.assemble(idx, grouping)
    problems, review = graph.grouping_problems(idx, comps), []
    if problems:
        grouping, review, more = ai.review(client, idx, grouping, comps, problems)
        comps, issues = graph.assemble(idx, grouping)
        issues += more
    calls = client.calls[n0:]
    return {"score": score(idx, comps, oracle), "flagged": problems, "review": review, "notes": notes,
            "issues": issues, "tokens": sum(llm.cost(c) for c in calls if not c.get("cached")),
            "requests": sum(not c.get("cached") for c in calls), "seconds": round(time.perf_counter() - start, 1),
            "grouping": grouping}


for name in sys.argv[2:]:
    repo, orc = REPOS[name]
    idx = pyindex.index(ROOT / "sample-repos" / repo, inventory.scan(ROOT / "sample-repos" / repo))
    oracle = json.loads((ROOT / "experiments/quote-evidence/oracle" / orc).read_text(encoding="utf-8"))
    row = {"A": variant(idx, oracle, lambda: (ai.group(client, idx), [])),
           "C": variant(idx, oracle, lambda: ai.group_dirs(client, idx)),
           "no_ai": {"score": score(idx, graph.assemble(idx, graph.directory_grouping(idx))[0], oracle)}}
    (OUT / f"{name}.json").write_text(json.dumps(row, ensure_ascii=False, indent=1), encoding="utf-8")
    brief = {k: (v.get("score"), v.get("tokens"), v.get("seconds"), len(v.get("flagged") or {}), v.get("error"))
             for k, v in row.items()}
    print(name, json.dumps(brief, ensure_ascii=False), flush=True)
