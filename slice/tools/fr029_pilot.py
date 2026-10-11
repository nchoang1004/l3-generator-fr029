"""FR-029 pilot: run the agent flow on gold fixtures with a real provider, then score every run against its gold.

    python slice/tools/fr029_pilot.py --out DIR --model openai/gpt-oss-120b --key-env GROQ_API_KEY [--key-env GROQ_API_KEY_3]
        [--fixtures prefix_chain params_models ...] [--runs 1] [--base-url https://api.groq.com/openai/v1]

Each `--key-env` gets its own worker, because provider limits are per key. A run is never retried for a bad score;
a run that fails on infrastructure is recorded as failed with its reason. Writes DIR/summary.json and DIR/summary.md.
"""
from __future__ import annotations

import argparse
import json
import queue
import sys
import threading
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import fr029_score  # noqa: E402
from l3slice.docagent import Budget, OpenAICompatProvider, ResponsesProvider  # noqa: E402
from l3slice.docpipeline import run_documents  # noqa: E402

FIXTURES = HERE.parent / "tests" / "fixtures" / "fr029"
KINDS = ("routes", "models", "http_calls", "file_roles", "limitations")


def one(job, args, key_env, provider) -> dict:
    name, k = job
    out = args.out / f"{name}-r{k}"
    waited_before, cost_before = provider.waited_s, provider.cost_usd
    start = time.monotonic()
    row = {"fixture": name, "run": k, "key_env": key_env, "model": args.model}
    try:
        bundle = run_documents(FIXTURES / name, out, FIXTURES / f"{name}.membership.json", name, provider,
                               budget=Budget(max_turns=args.max_turns, max_tokens=args.max_tokens,
                                             max_context_chars=args.max_context_chars,
                                             max_request_tokens=args.max_request_tokens or None,
                                             max_turn_read_chars=args.max_turn_read_chars or None,
                                             max_cost_usd=args.max_cost_usd),
                               run_id=f"pilot_{name}_r{k}")
    except Exception as exc:  # recorded, never hidden: the summary shows the failure
        row.update(status="failed", error=f"{type(exc).__name__}: {exc}"[:500], trace=traceback.format_exc()[-1500:])
        return row
    result = {key: v for key, v in bundle.items() if key != "artifacts"}
    gold = json.loads((FIXTURES / f"{name}.gold.json").read_text(encoding="utf-8"))
    score = fr029_score.score(result, gold)
    (out.parent / f"{name}-r{k}.score.json").write_text(json.dumps(score, ensure_ascii=False, indent=2, default=str),
                                                        encoding="utf-8")
    row.update(status=bundle["agent"]["status"], reason=bundle["agent"]["reason"], turns=bundle["agent"]["turns"],
               tokens_in=bundle["agent"]["tokens_in"], tokens_out=bundle["agent"]["tokens_out"],
               waited_s=round(provider.waited_s - waited_before), seconds=round(time.monotonic() - start),
               cost_usd=round(provider.cost_usd - cost_before, 4) if args.price else None,
               coverage_complete=bundle["coverage"]["complete"], rejected=len(bundle["rejected_claims"]),
               artifacts_ready=all(a["status"] == "ready" for a in bundle["artifacts"]), score=score)
    return row


def worker(jobs: queue.Queue, results: list, args, key_env, lock):
    # one provider per key, so its per-minute window carries over from one fixture to the next
    cls = ResponsesProvider if args.api == "responses" else OpenAICompatProvider
    provider = cls(args.base_url, args.model, key_env, max_output_tokens=args.max_output_tokens,
                                    reasoning_effort=args.reasoning_effort, tokens_per_minute=args.tokens_per_minute or None,
                                    prices=tuple(args.price) if args.price else None)
    while True:
        try:
            job = jobs.get_nowait()
        except queue.Empty:
            return
        row = one(job, args, key_env, provider)
        with lock:
            results.append(row)
            print(f"[{key_env}] {row['fixture']} r{row['run']}: {row['status']}", file=sys.stderr, flush=True)


def summarize(rows: list) -> str:
    lines = ["| Fixture | Lần | Trạng thái | Lượt | Token vào/ra | " + " | ".join(KINDS) + " | Thuộc tính sai |",
             "|---|---|---|---|---|" + "---|" * len(KINDS) + "---|"]
    for r in sorted(rows, key=lambda r: (r["fixture"], r["run"])):
        if r["status"] == "failed":
            lines.append(f"| {r['fixture']} | {r['run']} | failed: {(r.get('error') or r.get('reason') or '')[:80]} |"
                         + " |" * (len(KINDS) + 3))
            continue
        cells, wrong = [], 0
        for kind in KINDS:
            s = r["score"].get(kind, {})
            if s.get("status") == "not_evaluated":
                cells.append("—")
                continue
            cells.append(f"TP {s['tp']} FP {s['fp']} FN {s['fn']}")
            wrong += sum(len(a["wrong"]) for a in s["attributes"].values())
        lines.append(f"| {r['fixture']} | {r['run']} | {r['status']} | {r['turns']} | {r['tokens_in']}/{r['tokens_out']}"
                     + (f" ({r['cost_usd']} USD)" if r.get("cost_usd") is not None else "") + " | "
                     + " | ".join(cells) + f" | {wrong} |")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--base-url", default="https://api.groq.com/openai/v1")
    p.add_argument("--model", default="openai/gpt-oss-120b")
    p.add_argument("--api", choices=["chat", "responses"], default="chat",
                   help="responses: OpenAI Responses API (công cụ + suy luận cùng lúc)")
    p.add_argument("--key-env", action="append", required=True)
    p.add_argument("--fixtures", nargs="*", default=["prefix_chain", "params_models", "pydantic_v1", "exclusions",
                                                     "http_calls", "file_roles"])
    p.add_argument("--runs", type=int, default=1)
    p.add_argument("--max-turns", type=int, default=80)
    p.add_argument("--max-tokens", type=int, default=400_000)
    p.add_argument("--max-context-chars", type=int, default=16_000)
    p.add_argument("--max-output-tokens", type=int, default=2500)
    p.add_argument("--max-request-tokens", type=int, default=7800, help="Groq miễn phí: 8.000 token/phút mỗi model")
    p.add_argument("--max-turn-read-chars", type=int, default=6000)
    p.add_argument("--tokens-per-minute", type=int, default=8000, help="0 = không giãn nhịp")
    p.add_argument("--price", type=float, nargs=3, metavar=("IN", "CACHED", "OUT"), help="USD / 1M token")
    p.add_argument("--max-cost-usd", type=float, help="Trần chi phí chung của cả lần chạy; cần --price")
    p.add_argument("--reasoning-effort", default="medium")
    args = p.parse_args(argv)
    if args.out.exists() and any(args.out.iterdir()):
        print("Thư mục --out phải mới hoặc rỗng", file=sys.stderr)
        return 2
    args.out.mkdir(parents=True, exist_ok=True)
    jobs = queue.Queue()
    for k in range(1, args.runs + 1):
        for name in args.fixtures:
            jobs.put((name, k))
    rows, lock = [], threading.Lock()
    threads = [threading.Thread(target=worker, args=(jobs, rows, args, env, lock)) for env in args.key_env]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    (args.out / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    (args.out / "summary.md").write_text(summarize(rows), encoding="utf-8")
    print(summarize(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
