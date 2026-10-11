"""Đợt 4: bộ sinh tài liệu (CMP-008) — OpenAPI body/parameters, DDL catalogue, escaping, evidence links."""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import sqlglot  # noqa: E402
from openapi_spec_validator import validate as validate_openapi  # noqa: E402

import contracts  # noqa: E402
from l3slice import extract, model, render, snapshot, verify  # noqa: E402


def run_on(files: dict[str, str], groups: list[tuple[str, list[str]]], name="demo", link=None):
    t = tempfile.TemporaryDirectory()
    root = Path(t.name) / "src"
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    snap, sources = snapshot.take(root)
    inv = snapshot.inventory(snap)
    unit = inv["units"][0]["id"]
    facts = extract.extract(snap, sources, unit)
    membership = {"partition_version": "fixture-membership-v1", "components": [{"name": n, "files": fs} for n, fs in groups]}
    verified = verify.verify(snap, sources, inv, facts, model.build(snap, unit, facts, membership))
    out = Path(t.name) / "out"
    bundle = render.render(verified, "run_r", name, out, link)
    contracts.validate(bundle, 8, "ResultBundle")
    contracts.check_bundle_invariants(bundle)
    return t, out, bundle


def block(text, lang):
    found = re.findall(rf"^```{lang}\n(.*?)^```", text, re.M | re.S)
    return found[0] if found else None


API = ("from fastapi import FastAPI\nfrom pydantic import BaseModel\n"
       "class Item(BaseModel):\n    name: str\n    tags: list[str] = []\n    note: str | None = None\n"
       "class Saved(Item):\n    id: int\n"
       "app = FastAPI()\n"
       "@app.post('/items', response_model=Saved, status_code=201)\ndef create(item: Item):\n    return item\n"
       "@app.get('/items/{item_id}', status_code=200)\ndef read(item_id: int, verbose: bool = False) -> Saved:\n    return None\n")


class OpenApiBodies(unittest.TestCase):
    def setUp(self):
        self.t, self.out, self.bundle = run_on({"api.py": API}, [("Items API", ["api.py"])])

    def tearDown(self):
        self.t.cleanup()

    def test_request_response_and_parameters_are_valid_openapi(self):
        [api] = self.out.glob("tech-specs/*/api/*.md")
        doc = json.loads(block(api.read_text(encoding="utf-8"), "json"))
        validate_openapi(doc)
        post = doc["paths"]["/items"]["post"]
        ref = post["requestBody"]["content"]["application/json"]["schema"]["$ref"]
        schema = doc["components"]["schemas"][ref.rsplit("/", 1)[1]]
        self.assertEqual(schema["required"], ["name"])
        self.assertEqual(schema["properties"]["note"], {"anyOf": [{"type": "string"}, {"type": "null"}]})
        self.assertIn("content", post["responses"]["201"])
        get = doc["paths"]["/items/{item_id}"]["get"]
        self.assertEqual({p["name"]: (p["in"], p["required"]) for p in get["parameters"]},
                         {"item_id": ("path", True), "verbose": ("query", False)})
        self.assertIn("content", get["responses"]["200"])  # return annotation, rule fastapi-defaults-v1

    def test_reader_table_and_model_section(self):
        """A newcomer reads parameters, model names and model fields without opening the source (GOAL-006)."""
        [api] = self.out.glob("tech-specs/*/api/*.md")
        text = api.read_text(encoding="utf-8")
        get = next(ln for ln in text.splitlines() if ln.startswith("| GET | /items/{item_id} |"))
        self.assertIn("item_id (path, integer, bắt buộc); verbose (query, boolean, tùy chọn)", get)
        self.assertIn("| Saved |", get)
        post = next(ln for ln in text.splitlines() if ln.startswith("| POST | /items |"))
        self.assertIn("| Item | Saved | 201 |", post)
        model = text.split("### Item (request)", 1)[1].split("###", 1)[0]
        self.assertIn("| name | string | True | False |", model)
        self.assertIn("| tags | list[string] | False | False |", model)
        self.assertIn("| note | string | False | True |", model)
        self.assertLess(text.index("## Endpoint"), text.index("## Model"))
        self.assertLess(text.index("## Model"), text.index("## Truy vết"))

    def test_no_auth_or_default_status_invented(self):
        [api] = self.out.glob("tech-specs/*/api/*.md")
        doc = json.loads(block(api.read_text(encoding="utf-8"), "json"))
        self.assertNotIn("security", json.dumps(doc))
        self.assertEqual(sorted(doc["paths"]["/items"]["post"]["responses"]), ["201"])


class UnknownParameterPlace(unittest.TestCase):
    def test_operation_kept_and_unknown_parameter_named(self):
        # fullstack: `session: SessionDep` comes from a file that does not parse
        files = {"deps.py": "SessionDep = (\n",
                 "api.py": "from fastapi import FastAPI\nfrom deps import SessionDep\napp = FastAPI()\n"
                           "@app.get('/items/{item_id}')\ndef read(session: SessionDep, item_id: int):\n    return 1\n"}
        t, out, bundle = run_on(files, [("Items API", ["api.py", "deps.py"])])
        with t:
            [api] = out.glob("tech-specs/*/api/*.md")
            doc = json.loads(block(api.read_text(encoding="utf-8"), "json"))
        validate_openapi(doc)
        op = doc["paths"]["/items/{item_id}"]["get"]
        self.assertEqual([p["name"] for p in op["parameters"]], ["item_id"])
        self.assertEqual([x["name"] for x in op["x-analysis"]["parameters_unknown"]], ["session"])


class DdlCatalogue(unittest.TestCase):
    def test_postgres_varchar_numeric_and_sqlglot_parses(self):
        t, out, _ = run_on({"m.py": "from sqlalchemy import Column, Integer, Numeric, String, create_engine\n"
                            "from sqlalchemy.orm import declarative_base\nBase = declarative_base()\n"
                            "class P(Base):\n    __tablename__ = 'products'\n    id = Column(Integer, primary_key=True)\n"
                            "    code = Column(String(12), nullable=False)\n    price = Column(Numeric(10, 2))\n"
                            "engine = create_engine('postgresql://h/db')\nBase.metadata.create_all(engine)\n"},
                           [("Catalog", ["m.py"])])
        with t:
            [tbl] = out.glob("tech-specs/*/schema/*.md")
            sql = block(tbl.read_text(encoding="utf-8"), "sql")
        self.assertIn('"code" VARCHAR(12) NOT NULL', sql)
        self.assertIn('"price" NUMERIC(10,2)', sql)
        for stmt in sqlglot.parse(sql, read="postgres"):
            self.assertIsNotNone(stmt)
        self.assertEqual(sqlglot.parse_one(sql.split("\n", 1)[1], read="postgres").args["this"].this.name, "products")

    def test_catalogue_bounds(self):
        self.assertTrue(render._catalogue_type("postgresql", "VARCHAR(1)"))
        self.assertFalse(render._catalogue_type("postgresql", "VARCHAR(0)"))
        self.assertFalse(render._catalogue_type("postgresql", "NUMERIC(5,6)"))
        self.assertFalse(render._catalogue_type("sqlite", "VARCHAR(10)"))


class Escaping(unittest.TestCase):
    def test_hostile_names_do_not_break_markdown_or_mermaid(self):
        evil = 'Kho | "] --> n9 <script>x</script>\n# tiêu đề'
        t, out, bundle = run_on({"a.py": "def f():\n    return 1\n", "b.py": "from a import f\nf()\n"},
                                [(evil, ["a.py"]), ("B", ["b.py"])])
        with t:
            mmd = (out / "architecture.mmd").read_text(encoding="utf-8")
            readme = (out / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("<script>", readme)
        self.assertEqual(mmd.count("\n"), len(mmd.splitlines()))
        node_lines = [l for l in mmd.splitlines() if '["' in l]
        self.assertEqual(len(node_lines), 2)
        self.assertTrue(all(l.count('["') == 1 and l.endswith('"]') and '"' not in l[l.index('["') + 2:-2] for l in node_lines))
        render.check_diagram(bundle["result"]["model"], render.mermaid(bundle["result"]["model"])[1], mmd)

    def test_pipe_in_cell_is_escaped(self):
        self.assertEqual(render.cell({"state": "known", "value": "a|b", "evidence_ids": ["e"]}), "a\\|b")
        self.assertNotIn("\n", render.cell({"state": "unknown", "reason": "x\ny"}))


class EvidenceLinks(unittest.TestCase):
    def test_link_only_with_repository_and_commit(self):
        link = {"base_url": "https://github.com/acme/shop", "commit": "a" * 40}
        t, out, bundle = run_on({"api.py": API}, [("Items API", ["api.py"])], link=link)
        with t:
            [api] = out.glob("tech-specs/*/api/*.md")
            text = api.read_text(encoding="utf-8")
        self.assertIn("https://github.com/acme/shop/blob/" + "a" * 40 + "/api.py#L", text)
        self.assertEqual(bundle["export_context"]["source_link"], link)
        t2, out2, _ = run_on({"api.py": API}, [("Items API", ["api.py"])])
        with t2:
            [api2] = out2.glob("tech-specs/*/api/*.md")
            self.assertNotIn("https://", api2.read_text(encoding="utf-8").split("```json")[0])


if __name__ == "__main__":
    unittest.main()
