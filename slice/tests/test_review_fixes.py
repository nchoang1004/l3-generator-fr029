"""Regression tests for the 7 findings of ket-qua-chay/review-codex-20261001-164427/REVIEW.md.

Each test failed before its fix (the review probes reproduced it) and passes after. Inputs are synthetic.
"""
from __future__ import annotations

import copy
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import contracts  # noqa: E402
from l3slice import engine as engine_mod, extract, gateway, model, render, snapshot, verify  # noqa: E402

MARKER = "FAKE_REVIEW_PASSWORD_123"


def build(files: dict[str, str]):
    t = tempfile.TemporaryDirectory()
    root = Path(t.name) / "src"
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    snap, sources = snapshot.take(root)
    inv = snapshot.inventory(snap)
    unit = inv["units"][0]["id"]
    facts = extract.extract(snap, sources, unit)
    membership = {"partition_version": "fixture-membership-v1", "components": [{"name": "App", "files": sorted(sources)}]}
    return t, snap, sources, inv, facts, model.build(snap, unit, facts, membership)


def route_of(facts):
    return next(f for f in facts["facts"] if f["kind"] == "route")


class Finding1Credentials(unittest.TestCase):
    def test_url_password_is_redacted_in_facts_output_and_egress(self):
        src = ("from pydantic_settings import BaseSettings\n"
               "class Settings(BaseSettings):\n"
               f"    DATABASE_URL: str = 'postgresql://demo:{MARKER}@localhost/db'\n"
               f"    CALLBACK: str = 'https://h/cb?token={MARKER}&x=1'\n"
               "import httpx\n"
               f"def f():\n    return httpx.get('https://u:{MARKER}@api.example/v1')\n")
        t, snap, sources, inv, facts, arch = build({"settings.py": src})
        with t:
            self.assertNotIn(MARKER, json.dumps(facts))
            contracts.validate(facts, 4, "FactSet")
            self.assertIn("VALUE_REDACTED", [lim["code"] for lim in facts["limitations"]])
            out = Path(t.name) / "out"
            render.render(verify.verify(snap, sources, inv, facts, arch), "run_s", "s", out)
            self.assertFalse(any(MARKER.encode() in p.read_bytes() for p in out.rglob("*") if p.is_file()))
        self.assertNotIn(MARKER, gateway.mask(f"postgresql://demo:{MARKER}@h/db and ?password={MARKER}"))
        self.assertNotIn(MARKER, json.dumps(gateway.mask_obj({"a": [f"redis://:{MARKER}@cache:6379/0"]})))


class Finding2Verifier(unittest.TestCase):
    API = "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/items', status_code=200)\ndef items():\n    return []\n"

    def check(self, value):
        t, snap, sources, inv, facts, arch = build({"main.py": self.API})
        with t:
            bad = copy.deepcopy(facts)
            route_of(bad)["attributes"]["status_codes"]["value"] = value
            return route_of(verify.verify(snap, sources, inv, bad, arch)["facts"])["attributes"]["status_codes"]

    def test_status_must_be_the_whole_literal(self):
        self.assertEqual(self.check([200])["state"], "known")
        self.assertEqual(self.check([20])["state"], "unknown")
        self.assertEqual(self.check([2])["state"], "unknown")

    def test_status_out_of_http_range_is_unknown(self):
        got = self.check([999])
        self.assertTrue(got["reason"].startswith("VALUE_OUT_OF_RANGE"))
        self.assertTrue(self.check(["200"])["reason"].startswith("VALUE_OUT_OF_RANGE"))

    def test_path_piece_must_be_whole_segment(self):
        src = ("from fastapi import FastAPI, APIRouter\napp = FastAPI()\nr = APIRouter(prefix='/v1')\n"
               "@r.get('/items', status_code=200)\ndef items():\n    return []\napp.include_router(r)\n")
        t, snap, sources, inv, facts, arch = build({"main.py": src})
        with t:
            self.assertEqual(route_of(facts)["attributes"]["path"]["value"], "/v1/items")
            for wrong in ["/v1/item", "/v1/items/extra"]:
                bad = copy.deepcopy(facts)
                route_of(bad)["attributes"]["path"]["value"] = wrong
                got = route_of(verify.verify(snap, sources, inv, bad, arch)["facts"])["attributes"]["path"]
                self.assertEqual(got["state"], "unknown", wrong)

    def test_status_from_a_rule_must_match_the_rule(self):
        src = ("from fastapi import FastAPI, status\napp = FastAPI()\n@app.get('/a')\ndef a():\n    return 1\n"
               "@app.post('/b', status_code=status.HTTP_201_CREATED)\ndef b():\n    return 1\n")
        t, snap, sources, inv, facts, arch = build({"main.py": src})
        with t:
            ok = {f["attributes"]["path"]["value"]: f["attributes"]["status_codes"]["state"]
                  for f in verify.verify(snap, sources, inv, facts, arch)["facts"]["facts"] if f["kind"] == "route"}
            bad = copy.deepcopy(facts)
            for f in bad["facts"]:
                if f["kind"] == "route":
                    f["attributes"]["status_codes"]["value"] = [204]
            got = {f["attributes"]["path"]["value"]: f["attributes"]["status_codes"]["state"]
                   for f in verify.verify(snap, sources, inv, bad, arch)["facts"]["facts"] if f["kind"] == "route"}
        self.assertEqual(ok, {"/a": "known", "/b": "known"})
        self.assertEqual(got, {"/a": "unknown", "/b": "unknown"})

    def test_table_name_must_be_whole_token(self):
        src = ("from sqlalchemy import Column, Integer\nfrom sqlalchemy.orm import declarative_base\nBase = declarative_base()\n"
               "class T(Base):\n    __tablename__ = 'items_old'\n    id = Column(Integer, primary_key=True)\n")
        t, snap, sources, inv, facts, arch = build({"m.py": src})
        with t:
            bad = copy.deepcopy(facts)
            next(f for f in bad["facts"] if f["kind"] == "table")["attributes"]["name"]["value"] = "items"
            got = next(f for f in verify.verify(snap, sources, inv, bad, arch)["facts"]["facts"] if f["kind"] == "table")
        self.assertEqual(got["attributes"]["name"]["state"], "unknown")


class Finding3DocumentValues(unittest.TestCase):
    """Change one value in the published text while keeping every ID: the checker must refuse it."""

    def setUp(self):
        api = ("from fastapi import FastAPI\nfrom pydantic import BaseModel\nclass Item(BaseModel):\n    name: str\n"
               "app = FastAPI()\n@app.post('/items', status_code=201)\ndef create(item: Item):\n    return item\n")
        tbl = ("from sqlalchemy import Column, Integer, ForeignKey, create_engine\nfrom sqlalchemy.orm import declarative_base\n"
               "Base = declarative_base()\nclass C(Base):\n    __tablename__ = 'cats'\n    id = Column(Integer, primary_key=True)\n"
               "class P(Base):\n    __tablename__ = 'pets'\n    id = Column(Integer, primary_key=True)\n"
               "    cat_id = Column(Integer, ForeignKey('cats.id'), nullable=True)\n"
               "engine = create_engine('sqlite:///x.db')\nBase.metadata.create_all(engine)\n")
        self.t, snap, sources, inv, facts, arch = build({"api.py": api, "db.py": tbl})
        self.facts = {f["id"]: f for f in facts["facts"]}
        comp = arch["components"][0]
        routes = [f for f in facts["facts"] if f["kind"] == "route"]
        tables = [f for f in facts["facts"] if f["kind"] == "table"]
        self.api, _, _, self.api_cov = render.render_api(comp, routes, "a.md", "A", self.facts)
        self.tbl, _, self.tbl_cov = render.render_tbl(comp, tables, "t.md", "T")

    def tearDown(self):
        self.t.cleanup()

    def test_untouched_files_pass(self):
        self.assertIsNone(render.check_doc("api", self.api, self.api_cov))
        self.assertIsNone(render.check_doc("table", self.tbl, self.tbl_cov))

    def test_changed_api_values_are_caught(self):
        for old, new in [("| 201 |", "| 404 |"), ("| POST |", "| GET |"), ("| /items |", "| /item |"),
                         ('"201": {', '"404": {'), ('"post": {', '"put": {'), ('"required": true', '"required": false')]:
            with self.subTest(change=new):
                self.assertIn(old, self.api)
                self.assertIsNotNone(render.check_doc("api", self.api.replace(old, new, 1), self.api_cov))

    def test_changed_table_values_are_caught(self):
        # TBL cells since 12/10/2026: có/không for flags, table.column for a foreign key
        for old, new in [("| cat_id | INTEGER | không |", "| cat_id | TEXT | không |"),
                         ("| cats.id |", "| dogs.id |"), ('"cat_id" INTEGER,', '"cat_id" INTEGER NOT NULL,'),
                         ('REFERENCES "cats"', 'REFERENCES "dogs"')]:
            with self.subTest(change=new):
                self.assertIn(old, self.tbl)
                self.assertIsNotNone(render.check_doc("table", self.tbl.replace(old, new, 1), self.tbl_cov))

    def test_nullable_cell_change_is_caught(self):
        rows = [ln for ln in self.tbl.splitlines() if ln.startswith("| cat_id")]
        self.assertIn("| cats.id | có |", rows[0])  # nullable, before the label and evidence cells
        broken = self.tbl.replace(rows[0], rows[0].replace("| cats.id | có |", "| cats.id | không |"))
        self.assertIsNotNone(render.check_doc("table", broken, self.tbl_cov))


class Finding4BadManifest(unittest.TestCase):
    def test_wrong_typed_dependencies_become_limitation(self):
        t, snap, sources, inv, facts, arch = build({"main.py": "x = 1\n", "pyproject.toml": "[project]\ndependencies = 1\n"})
        with t:
            self.assertIn("MANIFEST_INVALID", [lim["code"] for lim in facts["limitations"]])

    def test_unexpected_error_fails_run_and_worker_continues(self):
        with tempfile.TemporaryDirectory() as t:
            eng = engine_mod.Engine(Path(t), partition=lambda s: {"partition_version": "fixture-membership-v1",
                                                                  "components": [{"name": "A", "files": ["main.py"]}]})
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as zf:
                zf.writestr("main.py", "x = 1\n")
            first = eng.submit_zip(buf.getvalue())["run_id"]
            second = eng.submit_zip(buf.getvalue())["run_id"]
            real = extract.extract
            calls = []

            def boom(*a, **k):
                calls.append(1)
                if len(calls) == 1:
                    raise TypeError("simulated")
                return real(*a, **k)
            engine_mod.extract.extract = boom
            try:
                eng.step()
                eng.step()
            finally:
                engine_mod.extract.extract = real
            v1, v2 = eng.view(first), eng.view(second)
        contracts.validate_http(v1, "RunView")
        self.assertEqual((v1["state"], v1["reasons"][0]["code"]), ("failed", "internal_error"))
        self.assertIn(v2["state"], ("partial", "completed"))


class Finding5LocalZipParity(unittest.TestCase):
    def test_same_tree_gives_same_snapshot_and_excluded(self):
        files = {"main.py": b"x = 1\n", ".venv/dependency.py": b"y = 2\n", "node_modules/a/b.py": b"",
                 ".git/config": b"[core]\n", "pkg/__pycache__/m.pyc": b"\0", "pkg/m.py": b"z = 3\n", "README.md": b"#\n"}
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "src"
            for rel, data in files.items():
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_bytes(data)
            archive = Path(t) / "in.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                for rel, data in files.items():
                    zf.writestr(rel, data)
            local, _ = snapshot.take(root)
            zipped, _ = snapshot.take_zip(archive)
        self.assertEqual([f["path"] for f in local["files"]], ["main.py", "pkg/m.py"])
        self.assertEqual(local["snapshot_id"], zipped["snapshot_id"])
        self.assertEqual(local["excluded"], zipped["excluded"])


class Findings6And7OpenApiTypes(unittest.TestCase):
    def doc(self, src):
        t, snap, sources, inv, facts, arch = build({"api.py": src})
        with t:
            out = Path(t.name) / "out"
            render.render(verify.verify(snap, sources, inv, facts, arch), "run_o", "o", out)
            [api] = out.glob("tech-specs/*/api/*.md")
            text = api.read_text(encoding="utf-8")
        return json.loads(text.split("```json\n", 1)[1].split("```", 1)[0])

    def test_optional_body_is_not_required(self):
        base = ("from fastapi import FastAPI\nfrom pydantic import BaseModel\nclass Item(BaseModel):\n    name: str\n"
                "app = FastAPI()\n")
        doc = self.doc(base + "@app.post('/a', status_code=200)\ndef a(item: Item = None):\n    return 1\n"
                              "@app.post('/b', status_code=200)\ndef b(item: Item):\n    return 1\n")
        self.assertIs(doc["paths"]["/a"]["post"]["requestBody"]["required"], False)
        self.assertIs(doc["paths"]["/b"]["post"]["requestBody"]["required"], True)

    def test_nullable_items_and_tuples(self):
        doc = self.doc("from fastapi import FastAPI\nfrom pydantic import BaseModel\n"
                       "class M(BaseModel):\n    values: list[int | None]\n    pair: tuple[int, str]\n    many: tuple[int, ...]\n"
                       "app = FastAPI()\n@app.post('/m', status_code=200)\ndef m(x: M):\n    return 1\n")
        props = doc["components"]["schemas"][next(iter(doc["components"]["schemas"]))]["properties"]
        self.assertEqual(props["values"], {"type": "array", "items": {"anyOf": [{"type": "integer"}, {"type": "null"}]}})
        self.assertEqual(props["many"], {"type": "array", "items": {"type": "integer"}})
        self.assertIn("x-analysis", props["pair"])  # multi-type tuple is unknown, not its first element


class RendererInputAndPublish(unittest.TestCase):
    """Cases from slice/evaluation_l3 (independent CMP-008 evaluation) that failed before these fixes."""

    def setUp(self):
        api = "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/items', status_code=200)\ndef items():\n    return []\n"
        lib = "from main import items\ndef use():\n    return items()\n"
        self.t, snap, sources, inv, facts, _ = build({"main.py": api, "lib.py": lib})
        unit = inv["units"][0]["id"]
        arch = model.build(snap, unit, facts, {"partition_version": "fixture-membership-v1", "components": [
            {"name": "Api", "files": ["main.py"]}, {"name": "Lib", "files": ["lib.py"]}]})
        self.v = verify.verify(snap, sources, inv, facts, arch)
        self.assertEqual(len(self.v["model"]["edges"]), 1)

    def tearDown(self):
        self.t.cleanup()

    def refused(self, mutate, code):
        v = copy.deepcopy(self.v)
        mutate(v)
        out = Path(self.t.name) / ("out-" + code)
        with self.assertRaises(render.ExportError) as e:
            render.render(v, "run_i", "i", out)
        self.assertEqual(e.exception.code, code)
        self.assertFalse(out.exists())

    def test_invalid_inputs_are_typed_and_publish_nothing(self):
        self.refused(lambda v: v.pop("schema_version"), "INVALID_INPUT")
        self.refused(lambda v: v.update(schema_version="99.0.0"), "INVALID_INPUT")
        self.refused(lambda v: v["evidence_index"][0].update(snapshot_id="snap:other"), "SNAPSHOT_MISMATCH")
        self.refused(lambda v: v["model"]["edges"][0].update(target_component_id="not-a-component"), "REFERENCE_INVALID")
        self.refused(lambda v: v["facts"]["facts"].append(copy.deepcopy(v["facts"]["facts"][0])), "INVALID_INPUT")
        self.refused(lambda v: v.update(evidence_index=[]), "REFERENCE_INVALID")
        self.refused(lambda v: next(d for d in v["decisions"] if d["subject_id"] == v["model"]["components"][0]["id"])
                     .update(verdict="rejected"), "INVALID_INPUT")

    def test_write_failure_is_publish_failed_and_leaves_no_output(self):
        from unittest import mock
        out = Path(self.t.name) / "out-w"
        with mock.patch.object(Path, "write_bytes", side_effect=OSError(28, "No space left on device")), \
                self.assertRaises(render.ExportError) as e:
            render.render(self.v, "run_w", "w", out)
        self.assertEqual(e.exception.code, "PUBLISH_FAILED")
        self.assertFalse(out.exists())
        self.assertEqual([p.name for p in Path(self.t.name).glob(".out-w*")], [])

    def test_unknown_application_identity_omits_operation(self):
        v = copy.deepcopy(self.v)
        route_of(v["facts"])["attributes"]["application_id"] = {"state": "unknown", "reason": "test"}
        out = Path(self.t.name) / "out-a"
        render.render(v, "run_a", "a", out)
        [api] = out.glob("tech-specs/*/api/*.md")
        text = api.read_text(encoding="utf-8")
        self.assertNotIn("```json", text)
        self.assertIn("Application hoặc registration context chưa biết", text)

    def test_fk_target_with_control_character_is_not_ddl(self):
        col = {"name": {"state": "known", "value": "c", "evidence_ids": ["e"]},
               "type": {"state": "known", "value": "INTEGER", "evidence_ids": ["e"]},
               "primary_key": {"state": "known", "value": False, "evidence_ids": ["e"]},
               "nullable": {"state": "known", "value": True, "evidence_ids": ["e"]},
               "foreign_key": {"state": "known", "value": {"table": "t\x07", "column": "id"}, "evidence_ids": ["e"]}}
        fact = {"id": "fact:x", "attributes": {"name": {"state": "known", "value": "t", "evidence_ids": ["e"]},
                                               "dialect": {"state": "known", "value": "sqlite", "evidence_ids": ["e"]},
                                               "columns": {"state": "known", "value": [col], "evidence_ids": ["e"]}}}
        ddl, reason, _ = render._ddl(fact)
        self.assertIsNone(ddl)
        self.assertIn("khóa ngoại", reason)

    def test_slug_suffix_keeps_64_chars(self):
        slugs = render.unique_slugs([("a", "X" * 64), ("b", "x" * 64)], "COMPONENT")
        self.assertEqual(len(slugs["b"]), 64)
        self.assertTrue(slugs["b"].endswith("-2"))


if __name__ == "__main__":
    unittest.main()
