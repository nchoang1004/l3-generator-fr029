"""Tests for the first slice. Run from repo root:
    scripts/.venv/Scripts/python.exe -m unittest discover -s slice/tests
"""
from __future__ import annotations

import copy
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from openapi_spec_validator import validate as validate_openapi  # noqa: E402

import contracts  # noqa: E402
from l3slice import __main__ as cli, extract, model, render, run, snapshot, verify  # noqa: E402

FIX = HERE / "fixtures"


def build(name: str, tmp: Path, membership: Path | None = None):
    out = tmp / "out"
    bundle = run(FIX / name, out, membership or FIX / f"{name}.membership.json", name)
    return bundle, out


def block(text: str, lang: str) -> str:
    found = re.findall(rf"^```{lang}\n(.*?)^```", text, re.M | re.S)
    return found[0] if found else None


def contract_file(out: Path, kind: str) -> list[Path]:
    return sorted(out.glob(f"tech-specs/*/{'api' if kind == 'api' else 'schema'}/*.md"))


class FullFixture(unittest.TestCase):
    """shop_full: FastAPI app route with status code; SQLite tables with explicit keywords."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.bundle, cls.out = build("shop_full", Path(cls.tmp.name))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_bundle_matches_contract_schema_and_invariants(self):
        contracts.validate(self.bundle, 8, "ResultBundle")
        result = json.loads((self.out / "result.json").read_text(encoding="utf-8"))
        contracts.validate(result, 8, "ResultData")
        manifest = json.loads((self.out / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest, self.bundle)
        self.assertEqual({k: v for k, v in manifest.items() if k != "artifacts"}, result)
        contracts.check_bundle_invariants(self.bundle)

    def test_artifact_hashes_match_files(self):
        for art in self.bundle["artifacts"]:
            if art["status"] == "ready":
                raw = (self.out / art["path"]).read_bytes()
                self.assertEqual(art["sha256"], render.sha(raw), art["path"])
                self.assertEqual(art["bytes"], len(raw))
        svg = next(a for a in self.bundle["artifacts"] if a["kind"] == "diagram_image")
        self.assertEqual(svg["status"], "ready")
        render.check_svg(self.bundle["result"]["model"], (self.out / "architecture.svg").read_text(encoding="utf-8"))

    def test_owners_follow_declaration_file(self):
        owners = self.bundle["result"]["model"]["contract_owners"]
        comps = {c["id"]: c["name"] for c in self.bundle["result"]["model"]["components"]}
        facts = {f["id"]: f for f in self.bundle["result"]["facts"]["facts"]}
        got = sorted((facts[o["fact_id"]]["kind"], comps[o["component_id"]]) for o in owners)
        self.assertEqual(got, [("route", "Cửa hàng API"), ("table", "Lưu trữ"), ("table", "Lưu trữ")])

    def test_api_file_has_one_valid_openapi_block_matching_table(self):
        [api] = contract_file(self.out, "api")
        self.assertEqual(api.relative_to(self.out).as_posix(),
                         "tech-specs/CUA-HANG-API/api/API-SHOP-FULL-CUA-HANG-API-v1.md")
        text = api.read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"^```json", text, re.M)), 1)
        doc = json.loads(block(text, "json"))
        validate_openapi(doc)
        op = doc["paths"]["/items"]["get"]
        self.assertEqual(list(op["responses"]), ["200"])
        self.assertIn(f"`{op['x-analysis']['fact_ids'][0]}`", text)
        self.assertIn("unknown — Không thấy dependency; không kết luận route công khai", text)
        self.assertNotIn('"field": "condition"', text)

    def test_tbl_ddl_for_sqlite(self):
        [tbl] = contract_file(self.out, "table")
        sql = block(tbl.read_text(encoding="utf-8"), "sql")
        self.assertIn('CREATE TABLE "items" (\n  "id" INTEGER NOT NULL,\n  "name" TEXT NOT NULL,\n  "category_id" INTEGER,\n'
                      '  PRIMARY KEY ("id"),\n  FOREIGN KEY ("category_id") REFERENCES "categories" ("id")\n);', sql)
        self.assertIn('CREATE TABLE "categories"', sql)
        self.assertNotIn("DEFAULT", sql)
        self.assertEqual([n for n in self.bundle["render_notices"] if n["code"].startswith("DDL")], [])

    def test_readme_and_diagram_share_nodes(self):
        mmd = (self.out / "architecture.mmd").read_text(encoding="utf-8")
        readme = (self.out / "README.md").read_text(encoding="utf-8")
        self.assertIn(mmd.rstrip("\n"), readme)
        self.assertEqual(mmd.count('["'), len(self.bundle["result"]["model"]["components"]))
        for art in self.bundle["artifacts"]:
            if art["kind"] in ("api", "table"):
                self.assertIn(f"]({art['path']})", readme)

    def test_deterministic(self):
        with tempfile.TemporaryDirectory() as t:
            again, out = build("shop_full", Path(t))
        self.assertEqual(again, self.bundle)


class PartialFixture(unittest.TestCase):
    """shop_partial: router prefix (mount unknown), no status code, no engine (dialect unknown)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.bundle, cls.out = build("shop_partial", Path(cls.tmp.name))
        cls.codes = sorted(n["code"] for n in cls.bundle["render_notices"])

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_still_valid(self):
        contracts.validate(self.bundle, 8, "ResultBundle")
        contracts.check_bundle_invariants(self.bundle)

    def test_openapi_block_omitted_with_notices(self):
        [api] = contract_file(self.out, "api")
        text = api.read_text(encoding="utf-8")
        self.assertIsNone(block(text, "json"))
        self.assertIn("Chưa có khối OpenAPI:", text)
        self.assertIn("(hậu tố đã biết: /v1/orders)", text)
        self.assertIn("OPENAPI_BLOCK_OMITTED", self.codes)
        self.assertIn("OPENAPI_OPERATION_OMITTED", self.codes)

    def test_ddl_omitted_dialect_unknown(self):
        [tbl] = contract_file(self.out, "table")
        text = tbl.read_text(encoding="utf-8")
        sql = block(text, "sql")
        self.assertNotIn("CREATE TABLE", sql)
        self.assertRegex(sql, r"-- omitted: fact:[0-9a-f]{64}: dialect chưa biết")
        self.assertIn("unknown — Chưa xác định SQL dialect từ source", text)
        self.assertIn("DDL_TABLE_OMITTED", self.codes)
        self.assertIn("DDL_BLOCK_OMITTED", self.codes)

    def test_facts_partial_with_reason(self):
        for fact in self.bundle["result"]["facts"]["facts"]:
            if fact["kind"] in ("route", "table"):
                self.assertEqual(fact["completeness"], "partial")
                self.assertTrue(fact["completeness_reason"])


class EventsFixture(unittest.TestCase):
    """events: hand-written event facts (the slice extractor does not detect events), one proven binding."""

    @classmethod
    def setUpClass(cls):
        from jsonschema import Draft202012Validator
        cls.Draft = Draft202012Validator
        snap, sources = snapshot.take(FIX / "events")
        inv = snapshot.inventory(snap)
        unit = inv["units"][0]["id"]
        fact_set = extract.extract(snap, sources, unit)
        b = extract._Builder(snap, unit)
        payload = {"type": "object", "properties": {"order_id": {"type": "integer"}}, "required": ["order_id"]}

        def event(path, line, action, bound, schema=None):
            ev = b.evidence(path, line, line)
            k = lambda v: {"state": "known", "value": v, "evidence_ids": [ev["id"]]}
            u = {"state": "unknown", "reason": "Client nhận từ tham số; broker/cấu hình chưa xác định"}
            attrs = {"action": k(action), "topic": k("order-created"), "declaration_evidence_id": k(ev["id"]),
                     "broker": k("kafka:main") if bound else u, "namespace": k("default") if bound else u,
                     "serialization_context": k("json") if bound else u,
                     "payload": k(schema) if schema else {"state": "unknown", "reason": "Payload là biến, không có schema"}}
            f = b.fact("event", ev, f"{path}:{line}:{action}", attrs)
            if not (bound and schema):
                f.update(completeness="partial", completeness_reason="Broker hoặc payload chưa xác định")
            return f

        cls.f1 = event("orders/producer.py", 2, "publish", True, payload)
        cls.f4 = event("orders/producer.py", 6, "publish", False)
        cls.f2 = event("stock/consumer.py", 2, "consume", True)
        cls.f3 = event("billing/consumer.py", 2, "consume", False)
        fact_set["facts"] = sorted(b.facts, key=lambda f: f["id"])
        membership = json.loads((FIX / "events.membership.json").read_text(encoding="utf-8"))
        arch = model.build(snap, unit, fact_set, membership)
        cid = {c["name"]: c["id"] for c in arch["components"]}
        cls.cid = cid

        def edge(src, tgt, pair):
            return {"id": "edge_" + render.sha(json.dumps([snap["snapshot_id"], cid[src], cid[tgt], "publishes"]).encode()),
                    "source_component_id": cid[src], "target_component_id": cid[tgt], "relation_type": "publishes",
                    "fact_ids": sorted(f["id"] for f in pair), "evidence_ids": sorted(e["id"] for f in pair for e in f["evidence"]),
                    "origin": "static", "confidence": "exact", "completeness": "full", "rule_id": "event-binding",
                    "rule_version": "1-draft"}

        cls.good = edge("Orders", "Stock", [cls.f1, cls.f2])
        cls.bad = edge("Orders", "Billing", [cls.f1, cls.f3])
        arch["edges"] = sorted([cls.good, cls.bad], key=lambda e: e["id"])
        cls.verified = verify.verify(snap, sources, inv, fact_set, arch)
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "out"
        cls.bundle = render.render(cls.verified, "run_evt", "events", cls.out)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def evt(self, name):
        return (self.out / f"tech-specs/{name}/events").glob("*.md")

    def test_valid_bundle(self):
        contracts.validate(self.bundle, 8, "ResultBundle")
        contracts.check_bundle_invariants(self.bundle)

    def test_edge_without_proven_broker_rejected(self):
        self.assertEqual([e["id"] for e in self.verified["model"]["edges"]], [self.good["id"]])
        bad = next(d for d in self.verified["decisions"] if d["subject_id"] == self.bad["id"])
        self.assertEqual(bad["verdict"], "rejected")
        self.assertTrue(bad["reason"].startswith("BROKER_UNKNOWN"))

    def test_file_per_sending_and_receiving_component(self):
        self.assertEqual(sorted(p.name for p in self.evt("ORDERS")),
                         ["EVT-EVENTS-ORDERS-ORDER-CREATED-2.md", "EVT-EVENTS-ORDERS-ORDER-CREATED.md"])
        first = (self.out / "tech-specs/ORDERS/events/EVT-EVENTS-ORDERS-ORDER-CREATED.md").read_text(encoding="utf-8")
        second = (self.out / "tech-specs/ORDERS/events/EVT-EVENTS-ORDERS-ORDER-CREATED-2.md").read_text(encoding="utf-8")
        self.assertIn(f"`{self.f1['id']}`", first)  # line 2 comes first in source order
        self.assertIn(f"`{self.f4['id']}`", second)
        self.assertIn("| gửi | order-created | kafka:main |", first)
        self.assertIn("| Stock |", first)
        [stock] = self.evt("STOCK")
        self.assertIn("| nhận | order-created |", stock.read_text(encoding="utf-8"))
        self.assertIn("| Orders |", stock.read_text(encoding="utf-8"))

    def test_receiver_only_still_exported_with_unknown_sender(self):
        [billing] = self.evt("BILLING")
        text = billing.read_text(encoding="utf-8")
        self.assertIn("unknown — chưa có cạnh event đã kiểm nối bên gửi", text)
        self.assertIn("| partial |", text)

    def test_payload_blocks_are_json_schema(self):
        for comp in ("ORDERS", "STOCK", "BILLING"):
            for p in self.evt(comp):
                for raw in re.findall(r"^```json\n(.*?)^```", p.read_text(encoding="utf-8"), re.M | re.S):
                    schema = json.loads(raw)
                    self.Draft.check_schema(schema)
                    if schema["x-analysis"]["completeness"] == "partial":
                        self.assertNotIn("additionalProperties", schema)

    def test_notices(self):
        got = sorted((n["code"], tuple(n["fact_ids"])) for n in self.bundle["render_notices"])
        expected = sorted([("EVENT_PAYLOAD_UNKNOWN", (f["id"],)) for f in (self.f2, self.f3, self.f4)] +
                          [("EVENT_BINDING_UNRESOLVED", (f["id"],)) for f in (self.f3, self.f4)])
        self.assertEqual(got, expected)

    def test_readme_topic_index(self):
        readme = (self.out / "README.md").read_text(encoding="utf-8")
        line = next(l for l in readme.splitlines() if l.startswith("- order-created:"))
        self.assertEqual(line.count("](tech-specs/"), 4)
        self.assertEqual((self.out / "architecture.mmd").read_text(encoding="utf-8").count("-->"), 1)


class Rules(unittest.TestCase):
    def pieces(self, name="shop_full"):
        snap, sources = snapshot.take(FIX / name)
        inv = snapshot.inventory(snap)
        unit = inv["units"][0]["id"]
        facts = extract.extract(snap, sources, unit)
        membership = json.loads((FIX / f"{name}.membership.json").read_text(encoding="utf-8"))
        return snap, sources, inv, unit, facts, membership

    def test_value_not_in_evidence_becomes_unknown(self):
        snap, sources, inv, unit, facts, membership = self.pieces()
        table = next(f for f in facts["facts"] if f["kind"] == "table" and f["attributes"]["name"]["value"] == "items")
        table["attributes"]["name"]["value"] = "orders"
        arch = model.build(snap, unit, facts, membership)
        verified = verify.verify(snap, sources, inv, facts, arch)
        checked = next(f for f in verified["facts"]["facts"] if f["id"] == table["id"])
        self.assertEqual(checked["attributes"]["name"]["state"], "unknown")
        self.assertTrue(checked["attributes"]["name"]["reason"].startswith("VALUE_NOT_IN_EVIDENCE"))

    def test_owner_null_without_declaration(self):
        snap, sources, inv, unit, facts, membership = self.pieces()
        route = next(f for f in facts["facts"] if f["kind"] == "route")
        route["attributes"]["declaration_evidence_id"] = {"state": "unknown", "reason": "test"}
        arch = model.build(snap, unit, facts, membership)
        owner = next(o for o in arch["contract_owners"] if o["fact_id"] == route["id"])
        self.assertIsNone(owner["component_id"])
        contracts.validate(arch, 5, "ArchitectureModel")
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / "out"
            bundle = render.render(verify.verify(snap, sources, inv, facts, arch), "run_t", "shop_full", out)
            self.assertEqual(contract_file(out, "api"), [])
            self.assertIn(route["id"], (out / "README.md").read_text(encoding="utf-8"))
        self.assertIn("CONTRACT_OWNER_UNRESOLVED", [n["code"] for n in bundle["render_notices"]])
        contracts.check_bundle_invariants(bundle)

    def test_wrong_owner_is_cleared_by_verifier(self):
        snap, sources, inv, unit, facts, membership = self.pieces()
        arch = model.build(snap, unit, facts, membership)
        route_owner = next(o for o in arch["contract_owners"] if o["contract_kind"] == "api")
        other = next(c["id"] for c in arch["components"] if c["id"] != route_owner["component_id"])
        route_owner["component_id"] = other
        verified = verify.verify(snap, sources, inv, facts, arch)
        owner = next(o for o in verified["model"]["contract_owners"] if o["fact_id"] == route_owner["fact_id"])
        self.assertIsNone(owner["component_id"])
        self.assertTrue(owner["reason"].startswith("OWNER_UNPROVEN"))

    def test_membership_must_cover_each_file_once(self):
        snap, sources, inv, unit, facts, membership = self.pieces()
        membership["components"][0]["files"] = []
        with self.assertRaises(model.BuildError):
            model.build(snap, unit, facts, membership)

    def test_more_than_50_nodes_rejected(self):
        snap, sources, inv, unit, facts, membership = self.pieces()
        arch = model.build(snap, unit, facts, membership)
        verified = verify.verify(snap, sources, inv, facts, arch)
        big = copy.deepcopy(verified)
        big["model"]["components"] += [dict(big["model"]["components"][0], id=f"cmp_x{i}") for i in range(49)]
        with tempfile.TemporaryDirectory() as t, self.assertRaises(render.ExportError):
            render.render(big, "run_t", "shop_full", Path(t) / "out")

    def test_output_not_overwritten(self):
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / "out"
            out.mkdir()
            (out / "keep.txt").write_text("x", encoding="utf-8")
            with self.assertRaises(render.ExportError):
                run(FIX / "shop_full", out, FIX / "shop_full.membership.json", "shop_full")
            self.assertEqual([p.name for p in out.iterdir()], ["keep.txt"])

    def test_parameterised_type_stays_unknown(self):
        with tempfile.TemporaryDirectory() as t:
            src = Path(t) / "src"
            src.mkdir()
            (src / "m.py").write_text('from sqlalchemy import Column, String, create_engine\n'
                                      'from sqlalchemy.orm import declarative_base\n'
                                      'Base = declarative_base()\n'
                                      'engine = create_engine("sqlite:///x.db")\n'
                                      'class A(Base):\n    __tablename__ = "a"\n'
                                      '    name = Column(String(80), primary_key=True, nullable=False)\n'
                                      'Base.metadata.create_all(engine)\n', encoding="utf-8")
            snap, sources = snapshot.take(src)
            unit = snapshot.inventory(snap)["units"][0]["id"]
            [table] = [f for f in extract.extract(snap, sources, unit)["facts"] if f["kind"] == "table"]
        col = table["attributes"]["columns"]["value"][0]
        self.assertEqual(col["type"]["state"], "unknown")
        self.assertIn("String(...)", col["type"]["reason"])

    def test_slug(self):
        self.assertEqual(render.slug("Cửa hàng Đơn", "C"), "CUA-HANG-DON")
        self.assertEqual(render.slug("con", "C"), "X-CON")
        self.assertEqual(render.slug("***", "COMPONENT"), "COMPONENT")
        self.assertEqual(render.unique_slugs([("a", "API"), ("b", "api"), ("c", "Api")], "C"),
                         {"a": "API", "b": "API-2", "c": "API-3"})

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as t:
            code = cli.main(["--source", str(FIX / "shop_full"), "--output", str(Path(t) / "o"),
                             "--membership", str(FIX / "shop_full.membership.json")])
            self.assertEqual(code, 3)  # MODEL_NOT_RUN limitation: partial
            self.assertEqual(cli.main(["--source", str(FIX / "shop_full"), "--output", str(FIX / "shop_full" / "x"),
                                       "--membership", str(FIX / "shop_full.membership.json")]), 2)


if __name__ == "__main__":
    unittest.main()
