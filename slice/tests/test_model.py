"""Đợt 2–3: static edges (CMP-005) and their verification (CMP-007)."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import contracts  # noqa: E402
from l3slice import extract, model, render, snapshot, verify  # noqa: E402

FIX = HERE / "fixtures"


def pipeline(name):
    snap, sources = snapshot.take(FIX / name)
    inv = snapshot.inventory(snap)
    unit = inv["units"][0]["id"]
    facts = extract.extract(snap, sources, unit)
    membership = json.loads((FIX / f"{name}.membership.json").read_text(encoding="utf-8"))
    arch = model.build(snap, unit, facts, membership)
    return snap, sources, inv, facts, arch


class StaticEdges(unittest.TestCase):
    def test_call_across_components_becomes_verified_edge(self):
        snap, sources, inv, facts, arch = pipeline("shop_full")
        names = {c["id"]: c["name"] for c in arch["components"]}
        edges = [(names[e["source_component_id"]], names[e["target_component_id"]], e["relation_type"], e["rule_id"])
                 for e in arch["edges"]]
        self.assertEqual(edges, [("Cửa hàng API", "Lưu trữ", "calls", "resolved-target")])
        contracts.validate(arch, 5, "ArchitectureModel")
        verified = verify.verify(snap, sources, inv, facts, arch)
        self.assertEqual(len(verified["model"]["edges"]), 1)
        decision = next(d for d in verified["decisions"] if d["subject_id"] == arch["edges"][0]["id"])
        self.assertEqual(decision["verdict"], "accepted")
        with tempfile.TemporaryDirectory() as t:
            bundle = render.render(verified, "run_e", "shop_full", Path(t) / "out")
            mmd = (Path(t) / "out/architecture.mmd").read_text(encoding="utf-8")
        self.assertIn("-->|calls|", mmd)
        contracts.check_bundle_invariants(bundle)

    def test_edge_whose_call_site_is_outside_source_component_is_rejected(self):
        snap, sources, inv, facts, arch = pipeline("shop_full")
        bad = copy.deepcopy(arch)
        e = bad["edges"][0]
        e["source_component_id"], e["target_component_id"] = e["target_component_id"], e["source_component_id"]
        verified = verify.verify(snap, sources, inv, facts, bad)
        self.assertEqual(verified["model"]["edges"], [])
        decision = next(d for d in verified["decisions"] if d["subject_id"] == e["id"])
        self.assertTrue(decision["reason"].startswith("ENDPOINT_MISMATCH"))

    def test_no_edge_inside_one_component(self):
        snap, sources = snapshot.take(FIX / "shop_full")
        unit = snapshot.inventory(snap)["units"][0]["id"]
        facts = extract.extract(snap, sources, unit)
        arch = model.build(snap, unit, facts, {"partition_version": "fixture-membership-v1",
                                               "components": [{"name": "All", "files": ["app/main.py", "db/models.py"]}]})
        self.assertEqual(arch["edges"], [])

    def test_open_evidence_detects_changed_file(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "a.py").write_text("x = 1\n", encoding="utf-8")
            snap, sources = snapshot.take(root)
            ev = extract._Builder(snap, "u", sources).evidence("a.py", 1, 1)
            self.assertEqual(verify.open_evidence(root, ev), "x = 1")
            (root / "a.py").write_text("x = 2\n", encoding="utf-8")
            with self.assertRaises(verify.VerificationError):
                verify.open_evidence(root, ev)


if __name__ == "__main__":
    unittest.main()
