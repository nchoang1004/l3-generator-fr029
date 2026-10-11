"""Run the slice extractor on golden v1 development cases and score it with the project's scorer.

    python slice/tools/run_golden.py --golden-root "D:/VSF/VSF-L3 Generator" --out <new dir>

Held-out cases are refused: they are kept for one final run after gold review (plan, Đợt 10).
Gold is still `candidate`; the summary reports TP/FP/FN only, never a rate (golden D12).
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0]))
sys.path.insert(0, str(HERE))

from golden_adapter import to_prediction  # noqa: E402
from l3slice import extract, snapshot  # noqa: E402


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--golden-root", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--case", action="append", help="Chỉ chạy các case này (mặc định: mọi case development)")
    a = p.parse_args(argv)
    root = a.golden_root.resolve()
    sys.path.insert(0, str(root))
    from evaluation.score import evaluate  # noqa: E402  (project scorer, unchanged)
    manifest = json.loads((root / "evaluation/golden/v1/manifest.json").read_text(encoding="utf-8"))
    if a.out.exists():
        print(f"{a.out} đã tồn tại; chọn thư mục mới", file=sys.stderr)
        return 2
    a.out.mkdir(parents=True)
    rows, totals, by_family = [], collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
    for case in manifest["cases"]:
        if a.case and case["case_id"] not in a.case:
            continue
        if case["split"] != "development":
            if a.case:
                print(f"Từ chối {case['case_id']}: thuộc tập {case['split']}", file=sys.stderr)
                return 2
            continue
        src, case_dir = root / case["source"], root / case["case"]
        cm = json.loads((case_dir / "source-manifest.json").read_text(encoding="utf-8"))
        snap, sources = snapshot.take(src)
        inv = snapshot.inventory(snap)
        facts = extract.extract(snap, sources, inv["units"][0]["id"]) if inv["units"] else \
            {"facts": [], "limitations": [], "extractor_version": extract.EXTRACTOR_VERSION}
        pred = to_prediction(facts, snap, sources, case["case_id"], cm["source_digest"], extract.EXTRACTOR_VERSION)
        pred_path = a.out / f"{case['case_id']}.prediction.json"
        pred_path.write_text(json.dumps(pred, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report = evaluate(case_dir, src, pred_path)
        (a.out / f"{case['case_id']}.report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n",
                                                             encoding="utf-8")
        row = {"case_id": case["case_id"], "family": cm.get("source_family"), "status": report["status"],
               "errors": report["errors"][:5], "groups": {}, "false_exact": None}
        if report["status"] == "scored":
            for g, v in report["fact_groups"].items():
                row["groups"][g] = {k: v.get(k) for k in ("tp", "fp", "fn", "status")}
                if v.get("status") not in ("not_run", "not_labeled"):
                    for k in ("tp", "fp", "fn"):
                        totals[g][k] += v.get(k) or 0
                        by_family[(cm.get("source_family"), g)][k] += v.get(k) or 0
            row["false_exact"] = report["labels"].get("false_exact")
            totals["false_exact"]["count"] += report["labels"].get("false_exact") or 0
        rows.append(row)
    summary = {"split": "development", "gold_status": manifest.get("status"),
               "human_review_complete": manifest.get("human_review_complete"), "extractor_version": extract.EXTRACTOR_VERSION,
               "cases": len(rows), "invalid": [r["case_id"] for r in rows if r["status"] != "scored"],
               "totals": {g: dict(v) for g, v in totals.items()},
               "by_family": {f"{fam}/{g}": dict(v) for (fam, g), v in sorted(by_family.items(), key=str)}, "rows": rows}
    (a.out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Golden v1 — tập development", "",
             f"Gold: `{summary['gold_status']}`, human_review_complete = {summary['human_review_complete']}. "
             "Chỉ báo TP/FP/FN, không báo tỷ lệ (D12).", "",
             f"Extractor: `{summary['extractor_version']}`. Case: {summary['cases']}. Không chấm được: {summary['invalid'] or 'không'}.", "",
             "| Nhóm | TP | FP | FN |", "|---|---:|---:|---:|"]
    lines += [f"| {g} | {v.get('tp', 0)} | {v.get('fp', 0)} | {v.get('fn', 0)} |" for g, v in sorted(summary["totals"].items())
              if g != "false_exact"]
    lines += ["", f"false_exact (tổng): {summary['totals'].get('false_exact', {}).get('count', 0)}", "",
              "| Nguồn / nhóm | TP | FP | FN |", "|---|---:|---:|---:|"]
    lines += [f"| {k} | {v.get('tp', 0)} | {v.get('fp', 0)} | {v.get('fn', 0)} |" for k, v in summary["by_family"].items()]
    (a.out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
