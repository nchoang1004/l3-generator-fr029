"""D-03 experiment: compare file-partition candidates on golden v1 development cases that have architecture labels.

    python slice/tools/d03_experiment.py --golden-root "D:/VSF/VSF-L3 Generator" --out <new dir>

This is a measuring tool, not a product policy. It does not choose D-03 (API-005 §3.1); the owner chooses.
Candidates:
- A `directory-v1`: first directory of the path; files at the root form one group.
- B `signals-v0`: layer word in the path (table LAYERS, written by hand after reading the dev cases), then files with
  no layer word join the group they share most resolved references with; otherwise their first directory.
- C pipeline v8 grouping: not run (code of v8 is not in this repository and it needs a model call).
Gold is `candidate`; only TP/FP/FN are reported (golden D12). Held-out has no architecture labels and is refused.
`container` is copied from gold (one container per case): the product has no container concept.
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0]))
sys.path.insert(0, str(HERE))

from golden_adapter import to_prediction  # noqa: E402
from l3slice import extract, snapshot  # noqa: E402
from l3slice.model import MAX_NODES  # noqa: E402

LAYERS = {"api": {"api", "routes", "route", "router", "routers", "views", "endpoints", "handlers"},
          "business": {"service", "services", "crud", "business", "logic", "domain", "usecases"},
          "persistence": {"repository", "repositories", "repo", "models", "model", "db", "database", "orm", "tables",
                          "storage", "store", "dao"}}


def directory_v1(paths, refs):
    return {p: (PurePosixPath(p).parts[0] if len(PurePosixPath(p).parts) > 1 else "(root)") for p in paths}


def signals_v0(paths, refs):
    group = {}
    for p in paths:
        words = {w.lower() for w in PurePosixPath(p).with_suffix("").parts}
        hits = sorted(layer for layer, vocab in LAYERS.items() if words & vocab)
        if len(hits) == 1:
            group[p] = hits[0]
    for p in sorted(set(paths) - set(group)):
        votes = collections.Counter(group[q] for a, b in refs for q in (a, b) if p in (a, b) and q != p and q in group)
        best = votes.most_common(2)
        group[p] = best[0][0] if best and (len(best) == 1 or best[0][1] > best[1][1]) else directory_v1([p], refs)[p]
    return group


CANDIDATES = {"A directory-v1": directory_v1, "B signals-v0": signals_v0}


def lift(pred: dict, group_of: dict, container: str) -> dict:
    """File partition -> golden architecture variant. Members must be covered by a cited fact (golden core check)."""
    ents = {e["id"]: e for e in pred["entities"]}
    touching = collections.defaultdict(set)
    for f in pred["facts"]:
        for eid in (f["source_id"], f["target_id"]):
            if eid in ents:
                touching[eid].add(f["id"])
    comps = collections.defaultdict(lambda: {"members": set(), "facts": set()})
    for eid, fids in touching.items():
        g = group_of.get(ents[eid]["path"])
        if g is not None:
            comps[g]["members"].add(eid)
            comps[g]["facts"] |= fids
    components = [{"id": g, "container": container, "name": g, "role": "nhóm theo ứng viên", "members": sorted(c["members"]),
                   "fact_refs": sorted(c["facts"]), "confidence": "inferred", "completeness": "full",
                   "reason": "Ứng viên D-03 trong thí nghiệm, chưa được chọn"} for g, c in sorted(comps.items())]
    comp_of = {m: c["id"] for c in components for m in c["members"]}
    edges = collections.defaultdict(list)
    for f in pred["facts"]:
        if f["kind"] == "reference" and f["target_id"]:
            a, b = comp_of.get(f["source_id"]), comp_of.get(f["target_id"])
            if a and b and a != b:
                edges[(a, b, f["attributes"]["relation"])].append(f["id"])
    return {"id": "candidate", "components": components,
            "edges": [{"id": f"{a}->{b}:{k}", "source": a, "target": b, "kind": k, "condition": None,
                       "fact_refs": sorted(fs), "confidence": "inferred", "completeness": "full",
                       "reason": "Gộp từ reference đã nối đích"} for (a, b, k), fs in sorted(edges.items())]}


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--golden-root", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    root = a.golden_root.resolve()
    sys.path.insert(0, str(root))
    from evaluation.score import evaluate  # noqa: E402  (project scorer, unchanged)
    manifest = json.loads((root / "evaluation/golden/v1/manifest.json").read_text(encoding="utf-8"))
    if a.out.exists():
        print(f"{a.out} đã tồn tại; chọn thư mục mới", file=sys.stderr)
        return 2
    a.out.mkdir(parents=True)
    rows, totals = [], collections.defaultdict(collections.Counter)
    for case in manifest["cases"]:
        if case["split"] != "development":
            continue
        case_dir, src = root / case["case"], root / case["source"]
        gold = json.loads((case_dir / "gold.json").read_text(encoding="utf-8"))
        primary = next(v for v in gold["architectures"] if v["id"] == gold["primary_architecture"]) \
            if gold["primary_architecture"] != "none" else None
        if not primary or not primary["components"]:
            continue
        containers = sorted({c["container"] for c in primary["components"]})
        cm = json.loads((case_dir / "source-manifest.json").read_text(encoding="utf-8"))
        snap, sources = snapshot.take(src)
        inv = snapshot.inventory(snap)
        facts = extract.extract(snap, sources, inv["units"][0]["id"])
        base = to_prediction(facts, snap, sources, case["case_id"], cm["source_digest"], extract.EXTRACTOR_VERSION)
        refs = [(e1["path"], e2["path"]) for f in base["facts"] if f["kind"] == "reference" and f["target_id"]
                for e1 in [next(e for e in base["entities"] if e["id"] == f["source_id"])]
                for e2 in [next(e for e in base["entities"] if e["id"] == f["target_id"])]]
        paths = [f["path"] for f in snap["files"]]
        for name, fn in CANDIDATES.items():
            group_of = fn(paths, refs)
            n_groups = len(set(group_of.values()))
            pred = dict(base, status="partial", architectures=[lift(base, group_of, containers[0])])
            path = a.out / f"{case['case_id']}.{name.split()[0]}.prediction.json"
            path.write_text(json.dumps(pred, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            report = evaluate(case_dir, src, path)
            row = {"case_id": case["case_id"], "candidate": name, "groups": n_groups, "over_cap": n_groups > MAX_NODES,
                   "status": report["status"], "errors": report["errors"][:3]}
            if report["status"] == "scored":
                for g in ("membership", "edges"):
                    v = report["primary_architecture"][g]
                    row[g] = {k: v.get(k) for k in ("tp", "fp", "fn")}
                    for k in ("tp", "fp", "fn"):
                        totals[(name, g)][k] += v.get(k) or 0
            rows.append(row)
    cases = sorted({r["case_id"] for r in rows})
    summary = {"split": "development", "gold_status": manifest.get("status"), "cases": cases,
               "extractor_version": extract.EXTRACTOR_VERSION, "rows": rows,
               "totals": {f"{n}/{g}": dict(v) for (n, g), v in sorted(totals.items())},
               "not_run": {"C v8": "Mã pipeline v8 không có trong repo này và cần gọi model"}}
    (a.out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# D-03 — so sánh ứng viên chia nhóm (tập development)", "",
             f"Gold `{summary['gold_status']}`; chỉ báo TP/FP/FN. Case có nhãn kiến trúc: {len(cases)}.", "",
             "| Ứng viên | Membership TP | FP | FN | Cạnh TP | FP | FN |", "|---|---:|---:|---:|---:|---:|---:|"]
    for name in CANDIDATES:
        m, e = totals[(name, "membership")], totals[(name, "edges")]
        lines.append(f"| {name} | {m['tp']} | {m['fp']} | {m['fn']} | {e['tp']} | {e['fp']} | {e['fn']} |")
    lines += ["| C v8 | not_run | | | | | |", "", "| Case | Ứng viên | Số nhóm | Membership TP/FP/FN | Cạnh TP/FP/FN |",
              "|---|---|---:|---|---|"]
    for r in rows:
        fmt = (lambda g: "/".join(str(r[g][k]) for k in ("tp", "fp", "fn")) if g in r else r["status"])
        lines.append(f"| {r['case_id']} | {r['candidate']} | {r['groups']} | {fmt('membership')} | {fmt('edges')} |")
    (a.out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
