"""Repository -> component diagram with quote-checked evidence.

    python run.py <repo> --out <new dir> [--oracle oracle/x.json] [--dry-run]

--dry-run builds every request from a directory-based grouping and prints token estimates; no AI call.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))   # portable Python runs in isolated mode

import ai          # noqa: E402
import evaluate    # noqa: E402
import graph       # noqa: E402
import inventory   # noqa: E402
import llm         # noqa: E402
import pyindex     # noqa: E402
import render      # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def dry_run(idx: dict) -> dict:
    listing = graph.listing(idx)
    comps, _ = graph.assemble(idx, graph.directory_grouping(idx))
    conns = graph.connections(idx, comps)
    sizes = [sum(llm.estimate(t) for _, t in b) for b in ai.batches(idx, comps, conns, 2200)]
    return {"group_prompt_tokens": llm.estimate(ai.GROUP_SYSTEM + listing),
            "describe_batches": len(sizes), "describe_prompt_tokens": sizes,
            "rough_total_with_answers": llm.estimate(ai.GROUP_SYSTEM + listing) + 3000
            + sum(s + llm.estimate(ai.DESCRIBE_SYSTEM) + 2500 for s in sizes)}


def run(repo: Path, out: Path, client, oracle: dict | None) -> dict:
    if out.exists():
        raise FileExistsError(out)
    started = time.perf_counter()
    snapshot = inventory.scan(repo)
    idx = pyindex.index(repo, snapshot)
    local = time.perf_counter() - started
    ai_started = time.perf_counter()
    grouping = ai.group(client, idx)
    ai_time = time.perf_counter() - ai_started
    mark = time.perf_counter()
    comps, issues = graph.assemble(idx, grouping)
    problems, first, notes = graph.grouping_problems(idx, comps), grouping, []
    if problems:
        local += time.perf_counter() - mark
        ai_started = time.perf_counter()
        grouping, notes, more = ai.review(client, idx, grouping, comps, problems)
        ai_time += time.perf_counter() - ai_started
        mark = time.perf_counter()
        comps, issues = graph.assemble(idx, grouping)
        issues += more
    edges = graph.candidates(idx, comps)
    conns = graph.connections(idx, comps)
    local += time.perf_counter() - mark
    ai_started = time.perf_counter()
    answers, more = ai.describe(client, idx, comps, conns)
    ai_time += time.perf_counter() - ai_started
    issues += more
    mark = time.perf_counter()
    result = ai.apply(idx, comps, edges, conns, answers)
    result["file_lines"] = {p: len(idx[p]["lines"]) for p in graph.content_files(idx)}
    if not inventory.unchanged(snapshot):
        raise RuntimeError("source changed during the run; nothing written")
    errors = [p for p, e in idx.items() if e["error"]]
    issues += [f"{len(errors)} files could not be parsed: {', '.join(errors[:5])}"] if errors else []
    new = [c for c in client.calls if not c.get("cached")]
    model_time = sum(c.get("seconds", 0) for c in new)
    local += time.perf_counter() - mark
    timing = {"total_s": round(time.perf_counter() - started, 1), "local_s": round(local, 2),
              "ai_s": round(ai_time, 1), "model_s": round(model_time, 1),
              "waiting_s": round(max(0.0, ai_time - model_time), 1)}
    meta = {"repo": repo.name, "status": "partial" if issues or result["rejected"] else "complete",
            "files": len(graph.content_files(idx)), "issues": issues, "model": llm.MODEL, "timing": timing,
            "tokens": sum(map(llm.cost, new)), "requests": len(new),
            "cached": len(client.calls) - len(new), "calls": client.calls,
            "candidate_edges": len(edges), "grouping": grouping,
            "review": {"problems": problems, "notes": notes, "first_grouping": first} if problems else None}
    render.write(out, result, meta, snapshot)
    summary = {k: meta[k] for k in ("status", "files", "tokens", "requests", "cached", "timing")}
    summary.update(flagged=len(problems), components=len(result["components"]), edges=len(result["edges"]),
                   hidden=len(result["hidden_edges"]), externals=len(result["externals"]), quotes=result["quotes"])
    if oracle:
        scores = evaluate.score(result, oracle)
        scores["comparisons"] = evaluate.comparisons(idx, comps, edges, result, oracle)
        (out / "score.json").write_text(json.dumps(scores, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary["score"] = {part: {k: scores[part][k] for k in ("precision", "precision_strict", "recall")}
                            for part in ("internal", "external")}
        summary["score"].update(quote_validity=scores["quote_validity"],
                                grouping_agreement=scores["grouping_agreement"],
                                comparisons=scores["comparisons"])
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--oracle", type=Path)
    parser.add_argument("--budget", type=int, default=100_000, help="total Groq tokens across all runs")
    parser.add_argument("--env", type=Path, default=ROOT / ".env")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        snapshot = inventory.scan(args.repo)
        print(json.dumps(dry_run(pyindex.index(args.repo, snapshot)), indent=2))
        return
    if not args.out or args.out.exists():
        sys.exit("--out must be a new directory")
    oracle = json.loads(args.oracle.read_text(encoding="utf-8")) if args.oracle else None
    client = llm.Groq(llm.load_key(args.env), args.budget)
    print(json.dumps(run(args.repo, args.out, client, oracle), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
