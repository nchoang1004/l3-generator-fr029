"""FR-029 acceptance measurement on the held-out repos of OBS-001 (one run per configuration, totals only).

    python slice/tools/fr029_accept.py --out DIR --model gpt-6-luna --key-env OPENAI_API_KEY --price 0.1 0.01 0.5
        --max-cost-usd 1.2 [--repos tdd-docker agentgpt igorbenav kibo]

Held-out protocol: the person tuning the tool sees only totals. This script prints and writes to DIR/summary.json
only counts and rates per repo and per kind; per-item scores go to DIR/private/ and must not be opened while the
prompt is still being tuned. Each repository is run exactly once; a failure is recorded, never retried for a score.
Thresholds (NFR-ACC-002): P and R >= 0.80 per kind, `exact` wrong <= 5%, on every small and medium held-out repo.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import fr029_golden4  # noqa: E402
import fr029_score  # noqa: E402
from l3slice import snapshot  # noqa: E402
from l3slice.docagent import Budget, ResponsesProvider  # noqa: E402
from l3slice.docpipeline import run_documents  # noqa: E402

REPOS = "D:/VSF/l3-acceptance-repos"
GOLD = "D:/VSF/l3-acceptance-gold"
CASES = {  # name -> (repo folder, gold file, gold format, size class in OBS-001)
    "tdd-docker": (f"{REPOS}/testdrivenio_fastapi-tdd-docker-16433b6", f"{GOLD}/tdd-docker/gold.json", "fr029", "nhỏ"),
    "agentgpt": (f"{REPOS}/reworkd_AgentGPT-18b073a", f"{GOLD}/agentgpt/gold.r2.json", "fr029", "nhỏ"),
    "igorbenav": ("D:/VSF/l3-generator-golden-v2/sample-repos/fastapi-boilerplate",
                  "D:/VSF/l3-generator-golden-v2/.aide/evidence/tests/golden-v1/igorbenav-FastAPI-boilerplate/final-r3.json",
                  "golden-v1", "vừa"),
    "kibo": (f"{REPOS}/KIBO-Agenda_kibo-backend-89eb3bb", f"{GOLD}/kibo/gold.r2.json", "fr029", "vừa"),
    # repositories no tool was ever tuned on; gold by two independent writers (08/10/2026); not run by the agent yet
    "orderflow": ("D:/VSF/l3-heldout-repos2/AlexGoster_orderflow-services",
                  "D:/VSF/l3-heldout-gold2/AlexGoster_orderflow-services/gold.json", "fr029", "nhỏ"),
    "token-proxy": ("D:/VSF/l3-heldout-repos2/zolderio_token-proxy",
                    "D:/VSF/l3-heldout-gold2/zolderio_token-proxy/gold.json", "fr029", "nhỏ"),
    "tgju-api": ("D:/VSF/l3-heldout-repos2/BlackIQ_tgju-api", "D:/VSF/l3-heldout-gold2/BlackIQ_tgju-api/gold.json",
                 "fr029", "nhỏ"),
    "fx-service": ("D:/VSF/l3-heldout-repos2/gabryelvs_fx-service",
                   "D:/VSF/l3-heldout-gold2/gabryelvs_fx-service/gold.json", "fr029", "nhỏ"),
}

# Models of a golden-v1 repository, built later in the fr029 format by two independent agents that agreed on every
# field (07-08/10/2026); golden v1 itself has route model names only.
MODEL_GOLD = {"igorbenav": str(HERE.parents[1] / ".aide/evidence/tests/fr029-igorbenav-models-20261008/gold-models-A.json")}


def score_golden_v1(name: str, folder: str, result: dict, gold: dict) -> tuple[dict, dict]:
    """(per-item report, row fields) for a golden-v1 repository: routes, model names on routes and HTTP from golden
    v1 (with ERRATA), models from MODEL_GOLD when there is one; `exact` over everything that has a gold."""
    rep = fr029_golden4.compare(result, fr029_golden4.apply_errata(folder, gold))
    r, h, m = rep["routes"], rep["http_api"], rep["models_on_matched_routes"]
    row = {"kinds": {"routes": rates(r["tp"], len(r["fp"]), len(r["fn"])),
                     "http_calls": rates(h["tp"], len(h["fp"]), len(h["fn"]))},
           "http_out_of_scope": h["out_of_scope"],
           "attribute_accuracy": {"routes": {"model_names": f"{m['correct']}/{r['tp']}"}}}
    scope = "route và HTTP; model chưa có gold"
    if name in MODEL_GOLD and Path(MODEL_GOLD[name]).exists():
        mg = json.loads(Path(MODEL_GOLD[name]).read_text(encoding="utf-8"))
        models = fr029_score.score(result, {"models": [
            {"file": x["file"], "name": x["name"], "fields": [
                {k: f.get(k) for k in ("name", "alias", "type", "required", "nullable")} | {"alt_types": f.get("alt_types", [])}
                for f in x["fields"]]} for x in mg["models"]]})["models"]
        rep["models"] = models
        rep["facts"] = {**rep["facts"], **models["facts"]}
        row["kinds"]["models"] = rates(models["tp"], models["fp"], models["fn"])
        row["attribute_accuracy"]["models"] = {"fields": accuracy(models["attributes"]["fields"], models["tp"])}
        scope = "route, HTTP (golden v1) và model (gold mới)"
    row["exact"] = {**exact_wrong(result, rep), "scope": scope}
    return rep, row


def rates(tp: int, fp: int, fn: int) -> dict:
    return {"tp": tp, "fp": fp, "fn": fn,
            "precision": round(tp / (tp + fp), 3) if tp + fp else None,
            "recall": round(tp / (tp + fn), 3) if tp + fn else None}


def exact_wrong(result: dict, report: dict) -> dict:
    """Share of published `exact` route/model/HTTP facts that are wrong: extra items, or matched items with a wrong
    attribute. Uses the scorer's verdict per fact id, so it shares one matching with the attribute scores. Facts of
    a kind the gold does not list are counted as not evaluated, outside the rate."""
    verdicts = dict(report.get("facts", {}))  # golden-v1 adapter: one table for the report
    for r in report.values():
        if isinstance(r, dict):
            verdicts.update(r.get("facts", {}))
    total = wrong = unscored = 0
    for f in result["facts"]:
        if f["kind"] not in ("route", "model", "http_call") or f["confidence"] != "exact":
            continue
        v = verdicts.get(f["id"])
        if v is None:
            unscored += 1
            continue
        total += 1
        wrong += v == "wrong"
    return {"exact_facts": total, "exact_wrong": wrong, "rate": round(wrong / total, 3) if total else None,
            "not_evaluated": unscored}


def verdict(row: dict) -> dict:
    """NFR-ACC-002 per kind on raw counts: P and R >= 0.80, `exact` wrong <= 5%. A zero denominator is
    not_evaluated; a kind the gold format cannot measure is "chưa đo" and blocks a pass."""
    out = {}
    for kind in ("routes", "models", "http_calls"):
        r = row.get("kinds", {}).get(kind)
        if r is None:
            out[kind] = "chưa đo"
            continue
        tp, fp, fn = r["tp"], r["fp"], r["fn"]
        checks = [5 * tp >= 4 * (tp + n) for n in (fp, fn) if tp + n]
        out[kind] = "not_evaluated" if not checks else ("đạt" if all(checks) else "không đạt")
    e = row.get("exact")
    out["exact"] = "chưa đo" if e is None else "not_evaluated" if not e["exact_facts"] else (
        "đạt" if 20 * e["exact_wrong"] <= e["exact_facts"] else "không đạt")
    values = list(out.values())
    out["overall"] = "không đạt" if "không đạt" in values else "chưa đủ đo" if "chưa đo" in values else "đạt"
    return out


def accuracy(av: dict, tp: int) -> str:
    """"correct/matched", plus the accepted unknowns kept apart: an accepted unknown is a limit, not a solved value."""
    u = av.get("acceptable_unknown", 0)
    return f"{av['correct']}/{tp}" + (f" (+{u} unknown)" if u else "")


def membership_for(src: Path, gold: dict | None) -> dict:
    snap, _ = snapshot.take(src)
    files = [f["path"] for f in snap["files"]]
    if gold and gold.get("_membership"):
        return gold["_membership"]
    return {"partition_version": "fixture-membership-v1", "components": [
        {"name": "Toàn bộ", "kind": "normal", "files": [f["path"] for f in snap["files"] if f["path"].endswith(".py") and f["byte_size"]]},
        {"name": "Khác", "kind": "other", "files": [p for p in files if p not in
                                                    {f["path"] for f in snap["files"] if f["path"].endswith(".py") and f["byte_size"]}]}]}


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--repos", nargs="+", default=list(CASES))
    p.add_argument("--model", required=True)
    p.add_argument("--key-env", required=True)
    p.add_argument("--base-url", default="https://api.openai.com/v1")
    p.add_argument("--reasoning-effort", default="medium")
    p.add_argument("--price", type=float, nargs=3, required=True)
    p.add_argument("--max-cost-usd", type=float, required=True)
    a = p.parse_args(argv)
    if a.out.exists() and any(a.out.iterdir()):
        print("Thư mục --out phải mới hoặc rỗng", file=sys.stderr)
        return 2
    (a.out / "private").mkdir(parents=True, exist_ok=True)
    provider = ResponsesProvider(a.base_url, a.model, a.key_env, max_output_tokens=16000,
                                 reasoning_effort=a.reasoning_effort, prices=tuple(a.price))
    rows = []
    for name in a.repos:
        repo, gold_path, fmt, size = CASES[name]
        row = {"repo": name, "size": size, "model": a.model}
        try:
            gold = json.loads(Path(gold_path).read_text(encoding="utf-8"))
        except FileNotFoundError:
            row.update(status="not_run", reason="Chưa có gold")
            rows.append(row)
            continue
        src = Path(repo) / gold.get("root", ".") if fmt == "fr029" else Path(repo)
        member_file = Path(gold_path).parent / "membership.json"
        membership = json.loads(member_file.read_text(encoding="utf-8")) if fmt == "fr029" and member_file.exists() \
            else membership_for(src, None)
        mpath = a.out / f"{name}.membership.json"
        mpath.write_text(json.dumps(membership, ensure_ascii=False), encoding="utf-8")
        before = provider.cost_usd
        try:
            bundle = run_documents(src, a.out / name, mpath, name, provider, budget=Budget(
                max_turns=400, max_tokens=60_000_000, max_seconds=4 * 3600, max_context_chars=150_000,
                max_cost_usd=a.max_cost_usd), run_id=f"accept_{name}")
        except Exception as exc:  # recorded, never hidden
            row.update(status="failed", reason=f"{type(exc).__name__}: {exc}"[:300])
            rows.append(row)
            continue
        result = {k: v for k, v in bundle.items() if k != "artifacts"}
        row.update(status=bundle["agent"]["status"], reason=bundle["agent"]["reason"],
                   coverage_complete=bundle["coverage"]["complete"], cost_usd=round(provider.cost_usd - before, 4),
                   prompt=bundle["provenance"]["prompt_version"])
        if fmt == "fr029":
            rep = fr029_score.score(result, gold)
            (a.out / "private" / f"{name}.score.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2, default=str),
                                                                    encoding="utf-8")
            row["kinds"] = {k: rates(r["tp"], r["fp"], r["fn"]) for k, r in rep.items()
                            if isinstance(r, dict) and "tp" in r}
            row["attribute_accuracy"] = {k: {an: accuracy(av, r["tp"]) for an, av in r["attributes"].items()}
                                         for k, r in rep.items() if isinstance(r, dict) and "attributes" in r}
            row["exact"] = exact_wrong(result, rep)
        else:
            rep, part = score_golden_v1(name, Path(gold_path).parent.name, result, gold)
            (a.out / "private" / f"{name}.score.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2, default=str),
                                                                    encoding="utf-8")
            row.update(part)
        row["verdict"] = verdict(row)
        rows.append(row)
        print(f"{name}: {row['status']} cost {row.get('cost_usd')}", file=sys.stderr, flush=True)
        (a.out / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    (a.out / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rows, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
