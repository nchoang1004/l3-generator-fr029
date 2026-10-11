"""Score saved acceptance runs again with the current scorer and gold, without calling any model.

    python slice/tools/fr029_rescore.py --run ket-qua-chay/fr029-accept-v13 --out DIR [--gold-file agentgpt=PATH ...]

Reads RUN/<repo>/<repo>/result.json written by fr029_accept.py. Writes DIR/private/<repo>.score.json (per item) and
DIR/summary.json (totals, verdict, and the sha256 of the scorer files and gold used), and prints totals only.
The old summary of the run is never changed, so the old and new scoring stay side by side.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import fr029_accept  # noqa: E402
import fr029_score  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--run", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--gold-file", nargs="*", default=[], help="repo=PATH: dùng gold khác bản trong fr029_accept.CASES")
    a = p.parse_args(argv)
    if a.out.exists() and any(a.out.iterdir()):
        print("Thư mục --out phải mới hoặc rỗng", file=sys.stderr)
        return 2
    (a.out / "private").mkdir(parents=True, exist_ok=True)
    override = dict(x.split("=", 1) for x in a.gold_file)
    scorer = {f: sha(HERE / f) for f in ("fr029_score.py", "fr029_accept.py", "fr029_golden4.py")}
    rows = []
    for name, (_, gold_path, fmt, size) in fr029_accept.CASES.items():
        saved = a.run / name / name / "result.json"
        row = {"repo": name, "size": size}
        if not saved.exists():
            row.update(status="not_run", reason="Không có result.json đã lưu")
            rows.append(row)
            continue
        gpath = Path(override.get(name, gold_path))
        result = json.loads(saved.read_text(encoding="utf-8"))
        gold = json.loads(gpath.read_text(encoding="utf-8"))
        row.update(status=result["agent"]["status"], gold=str(gpath), gold_sha256=sha(gpath),
                   result_sha256=sha(saved))
        if fmt == "fr029":
            rep = fr029_score.score(result, gold)
            row["kinds"] = {k: fr029_accept.rates(r["tp"], r["fp"], r["fn"]) for k, r in rep.items()
                            if isinstance(r, dict) and "tp" in r}
            row["not_evaluated"] = sorted(k for k, r in rep.items() if isinstance(r, dict) and r.get("status") == "not_evaluated")
            row["attribute_accuracy"] = {k: {an: fr029_accept.accuracy(av, r["tp"]) for an, av in r["attributes"].items()}
                                         for k, r in rep.items() if isinstance(r, dict) and "attributes" in r}
            row["exact"] = fr029_accept.exact_wrong(result, rep)
        else:
            rep, part = fr029_accept.score_golden_v1(name, gpath.parent.name, result, gold)
            row.update(part)
        row["verdict"] = fr029_accept.verdict(row)
        (a.out / "private" / f"{name}.score.json").write_text(
            json.dumps(rep, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        rows.append(row)
    summary = {"run": str(a.run), "scorer_sha256": scorer, "rows": rows}
    (a.out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
