"""L3 Generator code slice: one directory -> snapshot -> facts -> fixture membership -> verify -> API/TBL/EVT.

Follows the draft contracts in `.aide/tech-specs/` (revision 4). The model step runs only with `--llm`.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from . import annotate, extract, model, render, snapshot, verify


def run(source: Path, output: Path, membership_path: Path, repository_name: str, run_id: str = "run_slice",
        model_context=None, metrics: dict | None = None) -> dict:
    """`model_context(snapshot, sources)` returns a gateway.RunContext; None keeps the static model (MODEL_NOT_RUN).
    `metrics` (optional) receives stage durations in ms, API-001 Metrics names."""
    m = metrics if metrics is not None else {}
    t = time.monotonic()
    snap, sources = snapshot.take(source)
    m["intake_ms"] = int((time.monotonic() - t) * 1000)
    inv = snapshot.inventory(snap)
    if not inv["units"]:
        raise model.BuildError("INVALID_INPUT", "Thư mục không có file .py")
    unit_id = inv["units"][0]["id"]
    t = time.monotonic()
    facts = extract.extract(snap, sources, unit_id)
    membership = json.loads(membership_path.read_text(encoding="utf-8"))
    arch = model.build(snap, unit_id, facts, membership)
    m["static_analysis_ms"] = int((time.monotonic() - t) * 1000)
    if model_context is not None:
        t = time.monotonic()
        arch = annotate.annotate(arch, facts, snap, model_context(snap, sources))
        m["model_ms"] = int((time.monotonic() - t) * 1000)
    verified = verify.verify(snap, sources, inv, facts, arch)
    t = time.monotonic()
    bundle = render.render(verified, run_id, repository_name, output)
    m["export_ms"] = int((time.monotonic() - t) * 1000)
    m["output_bytes"] = sum(a["bytes"] or 0 for a in bundle["artifacts"] if a["status"] == "ready")
    return bundle
