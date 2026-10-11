"""Merge blind grading results from several reviewer models and show where they agree.

    python slice/tools/fr029_grade_merge.py FILE [FILE ...] [--json OUT]

Each FILE holds one reviewer's JSON (a bare object, or the first ```json block of a Markdown answer):
{"reviewer": ..., "errors": [{"fixture", "kind", "item", "field", "doc_value", "correct_value", "evidence", "confidence"}]}.
Errors are grouped by (fixture, kind, full field path, evidence file:line); a group reported by two or more reviewers
is "agreed".
Grouping by evidence line is coarse on purpose: reviewers word the same finding differently, but cite the same line.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def load(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.S)
    return json.loads(m.group(1) if m else text)


def key(e: dict) -> tuple:
    ev = re.match(r"\s*([^\s:,]+):(\d+)", e.get("evidence") or "")
    # the full field path is part of the key: two reviewers citing one line for different faults do not agree
    return (e.get("fixture"), e.get("kind"), (e.get("field") or "").strip().lower(),
            f"{ev.group(1)}:{ev.group(2)}" if ev else (e.get("item") or "").strip())


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("files", nargs="+", type=Path)
    p.add_argument("--json", type=Path)
    a = p.parse_args(argv)
    groups, reviewers = {}, []
    for f in a.files:
        r = load(f)
        name = r.get("reviewer") or f.stem
        reviewers.append(name)
        for e in r.get("errors", []):
            groups.setdefault(key(e), []).append(dict(e, reviewer=name))
    rows = sorted(groups.items(), key=lambda kv: (-len({x["reviewer"] for x in kv[1]}), str(kv[0])))
    print(f"Người chấm: {', '.join(reviewers)}; {len(rows)} nhóm lỗi")
    for k, items in rows:
        who = sorted({x["reviewer"] for x in items})
        tag = "ĐỒNG THUẬN" if len(who) >= 2 else "một người"
        print(f"\n[{tag} {len(who)}/{len(reviewers)}] {k[0]} · {k[1]} · {k[2]}")
        for x in items:
            print(f"  - {x['reviewer']} ({x.get('confidence')}): {x.get('item')} [{x.get('field')}] "
                  f"ghi {x.get('doc_value')!r} → đúng {x.get('correct_value')!r}")
    if a.json:
        a.json.write_text(json.dumps([{"key": list(k), "reviewers": sorted({x['reviewer'] for x in v}), "items": v}
                                      for k, v in rows], ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
