"""Đợt 0: one reproduction per known bug of the first slice. Each test failed before its fix."""
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
from l3slice import extract, model, render, run, snapshot, verify  # noqa: E402

FIX = HERE / "fixtures"


def pieces(src: Path, membership: dict):
    snap, sources = snapshot.take(src)
    inv = snapshot.inventory(snap)
    unit = inv["units"][0]["id"]
    facts = extract.extract(snap, sources, unit)
    return snap, sources, inv, unit, facts, membership


def write(root: Path, files: dict[str, str]) -> Path:
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return root


class StagingIsNotDeleted(unittest.TestCase):
    def test_existing_dot_staging_folder_of_user_survives(self):
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / "out"
            mine = Path(t) / "out.staging"
            mine.mkdir()
            (mine / "keep.txt").write_text("user data", encoding="utf-8")
            run(FIX / "shop_full", out, FIX / "shop_full.membership.json", "shop_full")
            self.assertEqual((mine / "keep.txt").read_text(encoding="utf-8"), "user data")
            self.assertEqual(sorted(p.name for p in Path(t).iterdir()), ["out", "out.staging"])


class DialectNeedsBinding(unittest.TestCase):
    def table(self, files):
        with tempfile.TemporaryDirectory() as t:
            src = write(Path(t) / "src", files)
            snap, sources, inv, unit, facts, _ = pieces(src, {})
        return next(f for f in facts["facts"] if f["kind"] == "table")

    MODEL = ('from sqlalchemy import Column, Integer, create_engine\n'
             'from sqlalchemy.orm import declarative_base\n'
             'Base = declarative_base()\n'
             'class A(Base):\n    __tablename__ = "a"\n'
             '    id = Column(Integer, primary_key=True, nullable=False)\n')

    def test_single_engine_without_binding_is_unknown(self):
        t = self.table({"m.py": self.MODEL + 'engine = create_engine("sqlite:///x.db")\n'})
        self.assertEqual(t["attributes"]["dialect"]["state"], "unknown")

    def test_create_all_binds_base_to_engine(self):
        t = self.table({"m.py": self.MODEL + 'engine = create_engine("sqlite:///x.db")\nBase.metadata.create_all(engine)\n'})
        self.assertEqual(t["attributes"]["dialect"]["state"], "known")
        self.assertEqual(t["attributes"]["dialect"]["value"], "sqlite")

    def test_binding_across_files_through_import(self):
        t = self.table({"db/models.py": self.MODEL,
                        "db/engine.py": 'from sqlalchemy import create_engine\nengine = create_engine("postgresql+psycopg://h/db")\n',
                        "main.py": 'from db.engine import engine\nfrom db.models import Base\nBase.metadata.create_all(bind=engine)\n'})
        self.assertEqual(t["attributes"]["dialect"]["value"], "postgresql")

    def test_engine_bound_to_other_base_does_not_count(self):
        t = self.table({"m.py": self.MODEL + 'Other = declarative_base()\nengine = create_engine("sqlite:///x.db")\n'
                                            'Other.metadata.create_all(engine)\n'})
        self.assertEqual(t["attributes"]["dialect"]["state"], "unknown")


class ParityById(unittest.TestCase):
    def test_reversed_edge_with_same_count_fails(self):
        import test_slice
        test_slice.EventsFixture.setUpClass()
        try:
            verified = test_slice.EventsFixture.verified
            m = verified["model"]
            [edge] = m["edges"]
            flipped = copy.deepcopy(m)
            flipped["edges"][0].update(source_component_id=edge["target_component_id"],
                                       target_component_id=edge["source_component_id"])
            text, plan = render.mermaid(flipped)
            with self.assertRaises(render.ExportError):
                render.check_diagram(m, plan, text)
        finally:
            test_slice.EventsFixture.tearDownClass()


class DocumentChecksReadTheText(unittest.TestCase):
    """check_doc reads fact IDs back from the rendered file instead of trusting the renderer's own plan."""

    def api_doc(self):
        snap, sources, inv, unit, facts, _ = pieces(FIX / "shop_full", {})
        membership = json.loads((FIX / "shop_full.membership.json").read_text(encoding="utf-8"))
        verified = verify.verify(snap, sources, inv, facts, model.build(snap, unit, facts, membership))
        comp = next(c for c in verified["model"]["components"] if c["name"] == "Cửa hàng API")
        routes = [f for f in verified["facts"]["facts"] if f["kind"] == "route"]
        text, _, _, cov = render.render_api(comp, routes, "x.md", comp["name"])
        return text, cov, routes[0]["id"]

    def test_consistent_file_passes(self):
        text, cov, _ = self.api_doc()
        self.assertIsNone(render.check_doc("api", text, cov))

    def test_operation_without_table_row_is_format_invalid(self):
        text, cov, fid = self.api_doc()
        broken = "\n".join(l for l in text.splitlines() if not (l.startswith("| ") and f"`{fid}`" in l))
        self.assertIsNotNone(render.check_doc("api", broken, cov))

    def test_contract_in_wrong_component_blocks_publish(self):
        docs = {"a.md": {"kind": "api", "cid": "cmp_other", "text": "", "cov": {"rows": ["f1"], "machine": [], "omitted": []}}}
        owners = [{"fact_id": "f1", "contract_kind": "api", "component_id": "cmp_owner"}]
        with self.assertRaises(render.ExportError):
            render.check_placement(docs, owners)


class StatusCodeEvidence(unittest.TestCase):
    SRC = ('from fastapi import FastAPI\napp = FastAPI()\n\n\n'
           '@app.get("/items", status_code=200)  # trước đây là 201\ndef items():\n    return []\n')

    def verified_route(self, tamper):
        with tempfile.TemporaryDirectory() as t:
            src = write(Path(t) / "src", {"app.py": self.SRC})
            snap, sources, inv, unit, facts, _ = pieces(src, {})
            route = next(f for f in facts["facts"] if f["kind"] == "route")
            tamper(route)
            arch = model.build(snap, unit, facts, {"partition_version": "fixture-membership-v1",
                                                   "components": [{"name": "API", "files": ["app.py"]}]})
            out = verify.verify(snap, sources, inv, facts, arch)
        return next(f for f in out["facts"]["facts"] if f["id"] == route["id"])

    def test_true_status_kept(self):
        r = self.verified_route(lambda f: None)
        self.assertEqual(r["attributes"]["status_codes"]["value"], [200])

    def test_value_only_in_comment_is_not_evidence(self):
        def tamper(f):
            f["attributes"]["status_codes"]["value"] = [201]
        r = self.verified_route(tamper)
        self.assertEqual(r["attributes"]["status_codes"]["state"], "unknown")
        self.assertTrue(r["attributes"]["status_codes"]["reason"].startswith("VALUE_NOT_IN_EVIDENCE"))

    def test_status_evidence_is_the_keyword_value_only(self):
        r = self.verified_route(lambda f: None)
        ev = {e["id"]: e for e in r["evidence"]}[r["attributes"]["status_codes"]["evidence_ids"][0]]
        self.assertEqual((ev["start_line"], ev["end_line"]), (5, 5))
        self.assertEqual(self.SRC.splitlines()[4][ev["start_column"]:ev["end_column"]], "200")


if __name__ == "__main__":
    unittest.main()
