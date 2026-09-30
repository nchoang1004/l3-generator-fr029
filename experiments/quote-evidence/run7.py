"""Repository -> component diagram, pipeline v7 (calls.py, flow.py, ai7.py).

    python run7.py <repo> --out <new dir> [--oracle oracle/x.json] [--budget N]
    python run7.py <repo> [<repo> ...] --dry-run

--dry-run builds every request without a model and prints its estimated tokens and answer room; no AI call.
Pass 1 gets no answer there, so the code draft is the grouping (see dry_run).
--no-draft: pass 1 without the code draft of the blocks (to measure what the draft brings).
Output: graph.json in the shape of v6 (evaluate.score reads it), diagram.mmd, score.json with --oracle.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))   # portable Python runs in isolated mode

import ai7         # noqa: E402
import calls       # noqa: E402
import evaluate    # noqa: E402
import flow        # noqa: E402
import graph       # noqa: E402
import inventory   # noqa: E402
import llm         # noqa: E402
import pyindex     # noqa: E402
import render      # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


class Estimate:
    """Stands in for the model in --dry-run: records the size of each request and answers nothing (pass 1 then
    falls back to the code draft, as in a real run with no usable answer)."""

    def __init__(self):
        self.calls = []

    def json(self, system, user, schema, *, step, max_tokens, effort="medium"):
        self.calls.append({"step": step, "prompt": llm.estimate(system + user), "max_tokens": max_tokens})
        return {}


def dry_run(repo: Path, use_draft: bool = True) -> dict:
    """Every request, built without a model. Pass 1 gets no answer, so the code draft is the grouping (with
    use_draft) and the edge check and naming are sized for it; pass 2 is sized apart for the worst case, every
    file ambiguous."""
    idx = pyindex.index(repo, inventory.scan(repo))
    facts = calls.facts(idx)
    an = flow.analyze(idx, facts)
    est = Estimate()
    grouping = ai7.group(est, idx, facts, an, use_draft)
    checked = ai7.check_edges(est, idx, facts, an, grouping)
    named = ai7.describe(est, idx, facts, an, grouping, checked["edges"])
    rows = [r for r in est.calls if not r["step"].startswith("name-retry")]   # a retry only follows a failure
    worst = ai7._Grouping(idx, facts, an, {"blocks": {}, "shared": []})
    batches = worst.batches(worst.files)
    head = llm.estimate(ai7.PLACE_SYSTEM + "Blocks:\n")
    return {"files": len(graph.content_files(idx)), "requests": len(rows),
            "prompt_tokens": {r["step"]: r["prompt"] for r in rows},
            "answer_room": {r["step"]: r["max_tokens"] for r in rows},
            "prompt_total": sum(r["prompt"] for r in rows),
            "min_answer_room": min((r["max_tokens"] for r in rows), default=0),
            "largest_request": max((r["prompt"] + r["max_tokens"] for r in rows), default=0),
            "not_sent": [i for i in grouping["issues"] + checked["issues"] + named["issues"] if "not sent" in i],
            "overview": [i for i in grouping["issues"] if i.startswith("overview")],
            "pass2_worst": {"requests": len(batches),
                            "prompt_total": sum(head + sum(llm.estimate(worst.entry(p)) for p in b) for b in batches)}}


def run(repo: Path, out: Path, client, oracle: dict | None, use_draft: bool = True) -> dict:
    if out.exists():
        raise FileExistsError(out)
    started = time.perf_counter()
    snapshot = inventory.scan(repo)
    idx = pyindex.index(repo, snapshot)
    facts = calls.facts(idx)
    an = flow.analyze(idx, facts)
    grouping = ai7.group(client, idx, facts, an, use_draft)
    checked = ai7.check_edges(client, idx, facts, an, grouping)
    result = ai7.describe(client, idx, facts, an, grouping, checked["edges"])
    result["file_lines"] = {p: len(idx[p]["lines"]) for p in graph.content_files(idx)}
    if not inventory.unchanged(snapshot):
        raise RuntimeError("source changed during the run; nothing written")
    issues = grouping["issues"] + checked["issues"] + result["issues"]
    errors = [p for p, e in idx.items() if e["error"]]
    issues += [f"{len(errors)} files could not be parsed: {', '.join(errors[:5])}"] if errors else []
    new = [c for c in client.calls if not c.get("cached")]
    model_time = sum(c.get("seconds", 0) for c in new)
    total = time.perf_counter() - started
    meta = {"repo": repo.name, "pipeline": "v7", "prompt_sha": ai7.PROMPT_SHA, "draft": use_draft,
            "status": "partial" if issues or result["rejected"] else "complete",
            "files": len(graph.content_files(idx)), "issues": issues, "model": getattr(client, "model", llm.MODEL),
            "timing": {"total_s": round(total, 1), "model_s": round(model_time, 1)},
            "tokens": sum(map(llm.cost, new)), "usd": round(sum(c.get("usd") or 0 for c in new), 4),
            "requests": len(new), "cached": len(client.calls) - len(new),
            "calls": client.calls, "grouping": {k: {"layer": grouping["layer"][k], "files": files}
                                                for k, files in grouping["blocks"].items()},
            "reasons": grouping["reasons"], "block_reasons": grouping["block_reasons"],
            "ambiguous": grouping["ambiguous"], "by_rule": grouping["by_rule"], "top": grouping["top"],
            "layer_differs": grouping["layer_differs"],
            "edge_check": checked["decisions"]}
    out.mkdir(parents=True)
    (out / "diagram.mmd").write_text(render.mermaid(result), encoding="utf-8")
    data = {"meta": meta, **result, "snapshot": {p: snapshot["files"][p]["sha256"] for p in snapshot["scope"]},
            "excluded": snapshot["excluded"]}
    (out / "graph.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    reasoning = getattr(client, "reasoning", {})
    if reasoning:              # why the model answered so, per step, for review
        (out / "reasoning.json").write_text(json.dumps(reasoning, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {k: meta[k] for k in ("status", "files", "tokens", "usd", "requests", "cached", "timing")}
    summary.update(components=len(result["components"]), edges=len(result["edges"]),
                   externals=len(result["externals"]), quotes=result["quotes"], issues=len(issues),
                   pass1=grouping["top"]["source"], evidence_by_code=len(grouping["top"]["evidence_by_code"]),
                   by_rule=len(grouping["by_rule"]))
    if oracle:
        scores = evaluate.score(result, oracle)
        scores["flow"] = evaluate.flow_score(result, oracle)
        (out / "score.json").write_text(json.dumps(scores, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary["score"] = {part: {k: scores[part][k] for k in ("precision", "precision_strict", "recall")}
                            for part in ("internal", "external")}
        summary["score"].update(quote_validity=scores["quote_validity"],
                                grouping_agreement=scores["grouping_agreement"],
                                flow={k: scores["flow"][k] for k in ("flow_precision", "flow_recall", "merged", "ari")})
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo", type=Path, nargs="+")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--oracle", type=Path)
    parser.add_argument("--budget", type=int, default=100_000, help="total tokens across all runs of the provider")
    parser.add_argument("--env", type=Path, default=ROOT / ".env")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--provider", choices=["groq", "openrouter"], default="groq")
    parser.add_argument("--model", default=llm.MODEL, help="with --provider openrouter, e.g. anthropic/claude-haiku-4.5")
    parser.add_argument("--no-draft", action="store_true", help="pass 1 without the code draft of the blocks")
    args = parser.parse_args()
    if args.provider == "openrouter":      # no 6k cap per request there: whole overview, room to answer
        ai7.LIMIT, ai7.TOP_PROMPT = 32_000, 16_000
    if args.dry_run:
        print(json.dumps({r.name: dry_run(r, not args.no_draft) for r in args.repo}, indent=2))
        return
    if len(args.repo) != 1 or not args.out or args.out.exists():
        sys.exit("one repository, and --out must be a new directory")
    oracle = json.loads(args.oracle.read_text(encoding="utf-8")) if args.oracle else None
    if args.provider == "openrouter":
        client = llm.Groq(llm.load_key(args.env, "OPENROUTER_API_KEY"), args.budget, model=args.model,
                          url=llm.OPENROUTER_URL)
    else:
        client = llm.Groq(llm.load_key(args.env), args.budget)
    print(json.dumps(run(args.repo[0], args.out, client, oracle, not args.no_draft), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
