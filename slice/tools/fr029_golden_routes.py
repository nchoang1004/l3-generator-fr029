"""Route check of the FR-029 agent flow on golden v1 development cases (gold status: candidate, review pending).

    python slice/tools/fr029_golden_routes.py --golden-root "D:/VSF/VSF-L3 Generator" --out DIR --model M --key-env ENV
        [--base-url URL] [--api responses] [--price IN CACHED OUT] [--max-cost-usd X] [--families ...]

Only routes are compared, by (method, path, handler `file::function`), and only inside the files the case's
source-manifest declares exhaustive for routes; routes found elsewhere are counted as outside_scope, not as FP.
Held-out cases are refused. Every case gets one component holding all files: membership does not change which
routes exist. A case run once; failures are recorded.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from l3slice import snapshot  # noqa: E402
from l3slice.docagent import Budget, OpenAICompatProvider, ResponsesProvider  # noqa: E402
from l3slice.docpipeline import run_documents  # noqa: E402


def gold_routes(gold: dict) -> Counter:
    """A multiset: one router served by two applications is two routes with the same key (case orders-two-apps)."""
    return Counter((f["attributes"]["method"], f["attributes"].get("path"), f["source_id"])
                   for f in gold["facts"] if f["kind"] == "route")


def our_routes(result: dict) -> Counter:
    return Counter((f["attributes"]["method"]["value"],
                    f["attributes"]["path"]["value"] if f["attributes"]["path"]["state"] == "known" else None,
                    f["attributes"]["handler"]["value"]) for f in result["facts"] if f["kind"] == "route")


def count(got: Counter, want: Counter) -> tuple:
    """(TP, FP, FN) of two multisets."""
    tp = sum((got & want).values())
    return tp, sum(got.values()) - tp, sum(want.values()) - tp


def in_scope(got: set, want: set, manifest: dict) -> tuple:
    """Keep the routes whose handler file the manifest labels exhaustively; return (got, want, got outside)."""
    files = ((manifest.get("scored_scope") or {}).get("exhaustive") or {}).get("route")
    if not files:
        return got, want, 0
    inside = lambda r: bool(r[2]) and r[2].split("::")[0] in files  # noqa: E731
    keep = lambda c: Counter({k: v for k, v in c.items() if inside(k)}) if isinstance(c, Counter)         else {k for k in c if inside(k)}  # noqa: E731
    kept = keep(got)
    size = lambda c: sum(c.values()) if isinstance(c, Counter) else len(c)  # noqa: E731
    return kept, keep(want), size(got) - size(kept)


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--golden-root", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--base-url", default="https://api.openai.com/v1")
    p.add_argument("--api", choices=["chat", "responses"], default="responses")
    p.add_argument("--model", required=True)
    p.add_argument("--key-env", required=True)
    p.add_argument("--reasoning-effort", default="medium")
    p.add_argument("--price", type=float, nargs=3)
    p.add_argument("--max-cost-usd", type=float)
    p.add_argument("--families", nargs="*", default=["fastapi-docs", "orders-fixture", "netflix-dispatch"])
    a = p.parse_args(argv)
    if a.out.exists() and any(a.out.iterdir()):
        print("Thư mục --out phải mới hoặc rỗng", file=sys.stderr)
        return 2
    a.out.mkdir(parents=True, exist_ok=True)
    root = a.golden_root.resolve()
    manifest = json.loads((root / "evaluation/golden/v1/manifest.json").read_text(encoding="utf-8"))
    cls = ResponsesProvider if a.api == "responses" else OpenAICompatProvider
    provider = cls(a.base_url, a.model, a.key_env, max_output_tokens=16000, reasoning_effort=a.reasoning_effort,
                   prices=tuple(a.price) if a.price else None)
    rows = []
    for case in manifest["cases"]:
        if case["split"] != "development" or case["family"] not in a.families:
            continue
        cid, src = case["case_id"], root / case["source"]
        gold = json.loads((root / case["case"] / "gold.json").read_text(encoding="utf-8"))
        want = gold_routes(gold)
        snap, _ = snapshot.take(src)
        membership = a.out / f"{cid}.membership.json"
        membership.write_text(json.dumps({"partition_version": "fixture-membership-v1", "components": [
            {"name": "Toàn bộ", "kind": "normal", "files": [f["path"] for f in snap["files"]
                                                          if f["path"].endswith(".py") and f["byte_size"]]},
            {"name": "Khác", "kind": "other", "files": [f["path"] for f in snap["files"]
                                                        if not (f["path"].endswith(".py") and f["byte_size"])]}]}),
            encoding="utf-8")
        cost_before = provider.cost_usd
        row = {"case": cid, "family": case["family"]}
        try:
            bundle = run_documents(src, a.out / cid, membership, cid, provider,
                                   budget=Budget(max_turns=120, max_tokens=4_000_000, max_context_chars=1_000_000,
                                                 max_cost_usd=a.max_cost_usd),
                                   run_id=f"golden_{cid}")
        except Exception as exc:  # recorded, never hidden
            row.update(status="failed", error=f"{type(exc).__name__}: {exc}"[:300], tp=0, fp=[],
                       fn=sorted(map(str, want.elements())))  # a failed case misses every gold route
            rows.append(row)
            print(f"{cid}: failed", file=sys.stderr, flush=True)
            continue
        manifest_file = root / case["case"] / "source-manifest.json"
        manifest_json = json.loads(manifest_file.read_text(encoding="utf-8")) if manifest_file.exists() else {}
        got, want, outside = in_scope(our_routes({k: v for k, v in bundle.items() if k != "artifacts"}), want, manifest_json)
        row.update(status=bundle["agent"]["status"], reason=bundle["agent"]["reason"],
                   cost_usd=round(provider.cost_usd - cost_before, 4), tp=count(got, want)[0],
                   fp=sorted(map(str, (got - want).elements())), fn=sorted(map(str, (want - got).elements())),
                   outside_scope=outside)
        rows.append(row)
        print(f"{cid}: {row['status']} TP {row['tp']} FP {len(row['fp'])} FN {len(row['fn'])}", file=sys.stderr, flush=True)
    tp = sum(r.get("tp", 0) for r in rows)
    fp = sum(len(r.get("fp", [])) for r in rows)
    fn = sum(len(r.get("fn", [])) for r in rows)
    summary = {"model": a.model, "cases": len(rows), "failed": sum(r["status"] == "failed" for r in rows),
               "tp": tp, "fp": fp, "fn": fn, "cost_usd": round(provider.cost_usd, 4), "rows": rows}
    (a.out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "rows"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
