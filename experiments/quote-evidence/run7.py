"""Repository -> component diagram, pipeline v7 (calls.py, flow.py, ai7.py).

    python run7.py <repo> --out <new dir> [--oracle oracle/x.json] [--budget N]
    python run7.py <repo> [<repo> ...] --dry-run

--dry-run builds every request without a model and prints its estimated tokens and answer room; no AI call.
Pass 1 is answered with one block per directory (see dry_run), so later requests are an upper estimate.
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
import verify      # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


class Estimate:
    """Stands in for the model in --dry-run: records the size of each request. Pass 1 gets `top` as its answer;
    every other request gets none."""

    def __init__(self, top: dict | None = None):
        self.calls, self.top = [], top

    def json(self, system, user, schema, *, step, max_tokens):
        self.calls.append({"step": step, "prompt": llm.estimate(system + user), "max_tokens": max_tokens})
        return self.top if step == "top-1" and self.top else {}


def stand_in(idx: dict, facts: dict, an: dict) -> dict:
    """A pass-1 answer for --dry-run: one block per directory of the overview; its layer is the highest sure layer
    of its files (else service), its reason that sure line (else the first line of its first file)."""
    _, units, _ = ai7.overview(idx, facts, an, ai7.TOP_PROMPT - llm.estimate(ai7.TOP_SYSTEM))
    blocks = []
    for u, files in sorted(units.items()):
        sure = sorted((ai7.LAYERS.index(an["sure"][p][0]), p) for p in files if p in an["sure"])
        p = sure[0][1] if sure else files[0]
        layer, line = an["sure"][p][:2] if sure else ("service", 1)
        text = verify.redact(idx[p]["lines"][line - 1]).strip() if idx[p]["lines"] else ""
        blocks.append({"name": ai7._clean(u) or "root", "layer": layer, "paths": [u], "reason": f"{p}:{line} {text}"})
    return {"blocks": blocks, "shared": []}


def dry_run(repo: Path) -> dict:
    """Every request, built without a model. Pass 1 is answered with stand_in, so the retry, the edge check and
    naming are sized for one block per directory (more blocks than a real answer); pass 2 gets no ambiguous file
    from it, so it is sized apart for the worst case, every file ambiguous."""
    idx = pyindex.index(repo, inventory.scan(repo))
    facts = calls.facts(idx)
    an = flow.analyze(idx, facts)
    est = Estimate(stand_in(idx, facts, an))
    grouping = ai7.group(est, idx, facts, an)
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
            "pass1_problems": len(grouping["top"]["found"]),
            "pass2_worst": {"requests": len(batches),
                            "prompt_total": sum(head + sum(llm.estimate(worst.entry(p)) for p in b) for b in batches)}}


def run(repo: Path, out: Path, client, oracle: dict | None) -> dict:
    if out.exists():
        raise FileExistsError(out)
    started = time.perf_counter()
    snapshot = inventory.scan(repo)
    idx = pyindex.index(repo, snapshot)
    facts = calls.facts(idx)
    an = flow.analyze(idx, facts)
    grouping = ai7.group(client, idx, facts, an)
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
    meta = {"repo": repo.name, "pipeline": "v7", "prompt_sha": ai7.PROMPT_SHA,
            "status": "partial" if issues or result["rejected"] else "complete",
            "files": len(graph.content_files(idx)), "issues": issues, "model": llm.MODEL,
            "timing": {"total_s": round(total, 1), "model_s": round(model_time, 1)},
            "tokens": sum(map(llm.cost, new)), "requests": len(new), "cached": len(client.calls) - len(new),
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
    summary = {k: meta[k] for k in ("status", "files", "tokens", "requests", "cached", "timing")}
    summary.update(components=len(result["components"]), edges=len(result["edges"]),
                   externals=len(result["externals"]), quotes=result["quotes"], issues=len(issues))
    if oracle:
        scores = evaluate.score(result, oracle)
        (out / "score.json").write_text(json.dumps(scores, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary["score"] = {part: {k: scores[part][k] for k in ("precision", "precision_strict", "recall")}
                            for part in ("internal", "external")}
        summary["score"].update(quote_validity=scores["quote_validity"],
                                grouping_agreement=scores["grouping_agreement"])
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo", type=Path, nargs="+")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--oracle", type=Path)
    parser.add_argument("--budget", type=int, default=100_000, help="total Groq tokens across all runs")
    parser.add_argument("--env", type=Path, default=ROOT / ".env")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print(json.dumps({r.name: dry_run(r) for r in args.repo}, indent=2))
        return
    if len(args.repo) != 1 or not args.out or args.out.exists():
        sys.exit("one repository, and --out must be a new directory")
    oracle = json.loads(args.oracle.read_text(encoding="utf-8")) if args.oracle else None
    client = llm.Groq(llm.load_key(args.env), args.budget)
    print(json.dumps(run(args.repo[0], args.out, client, oracle), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
