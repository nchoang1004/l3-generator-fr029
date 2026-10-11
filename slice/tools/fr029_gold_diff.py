"""Compare two independently written FR-029 golds of one repository, field by field.

    python slice/tools/fr029_gold_diff.py GOLD_A.json GOLD_B.json

Prints what only one gold lists and every field where both list the item but disagree. Agreement of two
independent writers is the evidence a gold gets before a reviewer settles each disagreement against the source.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def routes(g):
    return {(r["method"], r.get("path"), r.get("handler")): r for r in g.get("routes", [])}


def models(g):
    return {(m["file"], m["name"]): m for m in g.get("models", [])}


def calls(g):
    return {h["where"]: h for h in g.get("http_calls", [])}


def lims(g):
    return {(x["kind"], x["where"]): x for x in g.get("limitations", [])}


def norm_params(r):
    return sorted((p["name"].lower() if p["in"] == "header" else p["name"], p["in"], p["type"], p["required"])
                  for p in r.get("params", []))


def compare(a: dict, b: dict) -> list[str]:
    out = []
    for label, index, fields in (
            ("route", routes, {"declared_at": lambda r: r.get("declared_at"), "params": norm_params,
                               "request_body": lambda r: r.get("request_body"), "response": lambda r: r.get("response"),
                               "status": lambda r: r.get("status")}),
            ("model", models, {"fields": lambda m: [(f["name"], f.get("alias"), f["type"], f["required"], f["nullable"])
                                                    for f in m["fields"]]}),
            ("http", calls, {"library": lambda h: h["library"], "method": lambda h: h["method"],
                             "target": lambda h: h["target"].get("kind") + ":" + str(h["target"].get("value"))}),
            ("limitation", lims, {})):
        ia, ib = index(a), index(b)
        for k in sorted(set(ia) - set(ib), key=str):
            out.append(f"{label} chỉ có ở A: {k}")
        for k in sorted(set(ib) - set(ia), key=str):
            out.append(f"{label} chỉ có ở B: {k}")
        for k in sorted(set(ia) & set(ib), key=str):
            for name, get in fields.items():
                va, vb = get(ia[k]), get(ib[k])
                if va != vb:
                    out.append(f"{label} {k} · {name}: A={va} | B={vb}")
    return out


def main(argv=None) -> int:
    args = argv or sys.argv[1:]
    a, b = (json.loads(Path(p).read_text(encoding="utf-8")) for p in args[:2])
    diffs = compare(a, b)
    for line in diffs:
        print(line)
    print(f"{len(diffs)} khác biệt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
