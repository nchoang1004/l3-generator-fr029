"""FR-029 agent pipeline, offline: reader/coverage, evidence checks, and the first end-to-end case.

A scripted provider stands in for the model. These tests prove the plumbing (reading, checking, rendering);
they say nothing about how well a real model reads code.
"""
from __future__ import annotations

import copy
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from openapi_spec_validator import validate as validate_openapi  # noqa: E402

from l3slice import docpipeline, snapshot  # noqa: E402
from l3slice.docagent import Budget, ProviderError, ScriptedProvider, run_agent  # noqa: E402
from l3slice.docfacts import Claims, build_facts  # noqa: E402
from l3slice.source_tools import SourceTools  # noqa: E402

FIX = HERE / "fixtures" / "fr029_e2e"
MEMBERSHIP = HERE / "fixtures" / "fr029_e2e.membership.json"
READABLE = ["app/api/__init__.py", "app/api/items.py", "app/main.py", "app/schemas.py", "requirements.txt"]

MODELS = [
    {"id": "app/schemas.py::Tag", "at": "app/schemas.py:4",
     "fields": [{"name": "label", "alias": None, "type": "string", "required": True, "nullable": False, "at": "app/schemas.py:5"}]},
    {"id": "app/schemas.py::ItemIn", "at": "app/schemas.py:8",
     "fields": [{"name": "name", "alias": None, "type": "string", "required": True, "nullable": False, "at": "app/schemas.py:9"},
                {"name": "price", "alias": None, "type": "number", "required": False, "nullable": True, "at": "app/schemas.py:10"}]},
    {"id": "app/schemas.py::ItemOut", "at": "app/schemas.py:13",
     "fields": [{"name": "id", "alias": None, "type": "integer", "required": True, "nullable": False, "at": "app/schemas.py:14"},
                {"name": "name", "alias": None, "type": "string", "required": True, "nullable": False, "at": "app/schemas.py:15"},
                {"name": "tags", "alias": None, "type": "array[app/schemas.py::Tag]", "required": True, "nullable": False,
                 "at": "app/schemas.py:16"}]},
]
CHAIN = [{"kind": "include_prefix", "value": "/api", "at": "app/main.py:6"},
         {"kind": "router_prefix", "value": "/v1", "at": "app/api/__init__.py:5"},
         {"kind": "include_prefix", "value": "/items", "at": "app/api/__init__.py:6"}]
CREATE = {"method": "POST", "handler": "app/api/items.py::create_item", "decorator": "app/api/items.py:9-10",
          "application": "app/main.py:5",
          "path_parts": CHAIN + [{"kind": "decorator", "value": "/", "at": "app/api/items.py:9"}],
          "params": [],
          "request_body": {"models": ["app/schemas.py::ItemIn"], "param": "item", "media_type": "application/json", "required": True,
                           "embedded": False, "at": "app/api/items.py:10", "rule": "fastapi.json_body_media"},
          "response": {"model": "app/schemas.py::ItemOut", "array": False, "at": "app/api/items.py:10",
                       "rule": "fastapi.return_annotation_response_model"},
          "status": {"codes": [201], "at": "app/api/items.py:9", "rule": None},
          "dependencies": [], "auth": {"unknown": "Không thấy dependency; không kết luận route công khai"}}
READ = {"method": "GET", "handler": "app/api/items.py::read_item", "decorator": "app/api/items.py:15-16",
        "application": "app/main.py:5",
        "path_parts": CHAIN + [{"kind": "decorator", "value": "/{item_id}", "at": "app/api/items.py:15"}],
        "params": [{"name": "item_id", "in": "path", "type": "integer", "required": True, "at": "app/api/items.py:16"},
                   {"name": "verbose", "in": "query", "type": "boolean", "required": False, "at": "app/api/items.py:16",
                    "rule": "fastapi.scalar_param_query"}],
        "request_body": None,
        "response": {"model": "app/schemas.py::ItemOut", "array": False, "at": "app/api/items.py:16",
                     "rule": "fastapi.return_annotation_response_model"},
        "status": {"codes": [200], "rule": "fastapi.default_status_200"},
        "dependencies": [], "auth": {"unknown": "Không thấy dependency; không kết luận route công khai"}}
FINDINGS = {
    "models": MODELS, "routes": [CREATE, READ],
    "http_calls": [{"at": "app/api/items.py:11", "library": "httpx", "method": "POST",
                    "target": {"kind": "literal", "value": "https://audit.example.com/log"}}],
    "file_roles": [{"file": "app/main.py", "role": "Điểm vào", "at": "app/main.py:5"},
                   {"file": "app/api/__init__.py", "role": "Khác", "at": "app/api/__init__.py:5"},
                   {"file": "app/api/items.py", "role": "Route", "at": "app/api/items.py:9"},
                   {"file": "app/schemas.py", "role": "Schema API", "at": "app/schemas.py:8"}],
    "limitations": [{"kind": "add_api_route", "at": "app/main.py:13", "detail": "Route /ping đăng ký không qua decorator"}],
}
BAD = {"routes": [dict(CREATE, path_parts=[{"kind": "include_prefix", "value": "/v2", "at": "app/main.py:6"},
                                           {"kind": "decorator", "value": "/", "at": "app/api/items.py:9"}])]}


def script(findings=FINDINGS, bad=True):
    reads = [("read_file", {"path": p}) for p in READABLE]
    steps = [[("list_files", {})], reads]
    if bad:
        steps.append([("submit_findings", BAD)])
    steps += [[("submit_findings", findings)], [("finish", {})]]
    return steps


def run(provider, archdia=None, diagram=None):
    t = tempfile.TemporaryDirectory()
    out = Path(t.name) / "out"
    paths = {}
    for name, value in (("archdia", archdia), ("diagram", diagram)):
        if value is not None:
            p = Path(t.name) / name
            p.write_text(value if isinstance(value, str) else json.dumps(value), encoding="utf-8")
            paths[name] = p
    bundle = docpipeline.run_documents(FIX, out, MEMBERSHIP, "fr029-e2e", provider,
                                       archdia_path=paths.get("archdia"), diagram_path=paths.get("diagram"))
    return t, out, bundle


def tools_for(files: dict[str, str]):
    t = tempfile.TemporaryDirectory()
    root = Path(t.name)
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    snap, sources = snapshot.take(root)
    t.cleanup()
    return SourceTools(snap, sources)


class SourceToolsTest(unittest.TestCase):
    def test_scope_follows_fr028(self):
        tools = tools_for({"app/main.py": "x = 1\n", "tests/test_a.py": "", "conftest.py": "", "alembic/env.py": "",
                           "scripts/seed.py": "from app.main import x\n", "examples/demo.py": "print(1)\n"})
        self.assertEqual(tools.readable, ["app/main.py", "scripts/seed.py"])
        scopes = {x["path"]: x["scope"] for x in tools.not_readable()}
        self.assertEqual(scopes, {"alembic/env.py": "migration", "conftest.py": "test", "examples/demo.py": "conditional_out",
                                  "tests/test_a.py": "test"})
        self.assertIn("error", tools.read_file("tests/test_a.py"))

    def test_delivered_is_not_processed_until_the_model_answers(self):
        tools = tools_for({"a.py": "\n".join(f"x{i} = {i}" for i in range(250)) + "\n"})
        res = tools.read_file("a.py")
        self.assertEqual((res["start_line"], res["end_line"]), (1, 200))
        self.assertEqual(tools.unread(), [{"path": "a.py", "missing": [[1, 250]]}])
        tools.model_answered()
        self.assertEqual(tools.unread(), [{"path": "a.py", "missing": [[201, 250]]}])
        self.assertFalse(tools.coverage()["complete"])

    def test_masking_keeps_line_numbers(self):
        src = ('A = 1\nKEY = """-----BEGIN RSA PRIVATE KEY-----\nabc\n-----END RSA PRIVATE KEY-----"""\n'
               'password = "hunter2hunter2"\nB = 2\n')
        tools = tools_for({"a.py": src})
        text = tools.read_file("a.py")["text"]
        self.assertNotIn("abc", text)
        self.assertNotIn("hunter2", text)
        self.assertRegex(text, r"(?m)^\s+6\| B = 2$")

    def test_long_lines_are_cut_and_not_counted_as_fully_read(self):
        tools = tools_for({"a.py": "x = '" + "y" * 600 + "'\n"})
        self.assertEqual(tools.read_file("a.py")["cut_lines"], [1])
        tools.model_answered()
        self.assertFalse(tools.coverage()["complete"])


class ClaimsTest(unittest.TestCase):
    def setUp(self):
        self.tools = tools_for({"m.py": "from fastapi import FastAPI\napp = FastAPI()\n\n\n@app.get('/a', status_code=204)\n"
                                        "def a():\n    pass\n"})
        self.claims = Claims(self.tools)
        self.route = {"method": "GET", "handler": "m.py::a", "decorator": "m.py:5-6", "application": "m.py:2",
                      "path_parts": [{"kind": "decorator", "value": "/a", "at": "m.py:5"}], "params": [],
                      "request_body": None, "response": None, "status": {"codes": [204], "rule": None},
                      "dependencies": [], "auth": {"unknown": "chưa rõ"}}

    def submit(self, **change):
        return self.claims.submit({"routes": [dict(self.route, **change)]})

    def test_unread_lines_cannot_be_cited(self):
        errs = self.submit()["errors"]
        self.assertTrue(any("chưa được đọc" in e for x in errs for e in x["errors"]))

    def test_checks_literals_rules_and_status(self):
        self.tools.read_file("m.py")
        self.assertEqual(self.submit()["accepted"], 1)
        cases = {"path": dict(path_parts=[{"kind": "decorator", "value": "/b", "at": "m.py:5"}]),
                 "method": dict(method="POST"),
                 "rule": dict(status={"codes": [200], "rule": "fastapi.my_guess"}),
                 "default": dict(status={"codes": [200], "rule": "fastapi.default_status_200"}),
                 "status": dict(status={"codes": [201], "rule": None})}
        for name, change in cases.items():
            with self.subTest(name):
                self.assertEqual(self.submit(**change)["accepted"], 0)

    def test_service_needs_a_call_path(self):
        self.tools.read_file("m.py")
        res = self.claims.submit({"file_roles": [{"file": "m.py", "role": "Service", "at": "m.py:6"}]})
        self.assertEqual(res["accepted"], 0)

    def test_role_needs_its_signal(self):
        self.tools.read_file("m.py")
        res = self.claims.submit({"file_roles": [{"file": "m.py", "role": "Cấu hình", "at": "m.py:2"}]})
        self.assertEqual(res["accepted"], 0)


class AgentLoopTest(unittest.TestCase):
    def components(self):
        return json.loads(MEMBERSHIP.read_text(encoding="utf-8"))["components"]

    def setUp(self):
        snap, sources = snapshot.take(FIX)
        self.tools = SourceTools(snap, sources)
        self.claims = Claims(self.tools)

    def test_finish_is_refused_while_source_is_unread(self):
        provider = ScriptedProvider([[("finish", {})], [("finish", {})], [("finish", {})], [("finish", {})]])
        run = run_agent(self.tools, self.claims, self.components(), provider)
        self.assertEqual(run.status, "partial")
        self.assertIn("FINISH_WITH_GAPS", run.reason)
        refusal = json.loads(provider.seen[1]["content"])
        self.assertFalse(refusal["ok"])
        self.assertTrue(refusal["unread"])

    def test_turn_budget_and_model_errors_end_as_partial(self):
        run = run_agent(self.tools, self.claims, self.components(), ScriptedProvider([[("list_files", {})]] * 5),
                        Budget(max_turns=2))
        self.assertEqual((run.status, run.reason), ("partial", "BUDGET_TURNS: hết số lượt"))
        run = run_agent(self.tools, Claims(self.tools), self.components(),
                        ScriptedProvider([ProviderError("HTTP 401", False)]))
        self.assertEqual(run.status, "failed")


class EndToEnd(unittest.TestCase):
    def test_first_case(self):
        boom = mock.Mock(side_effect=AssertionError("luồng FR-029 không được gọi bước này"))
        # extract.extract is called since 11/10/2026, only for tables, events, libraries and config (docstatic);
        # that no route comes from it is guarded by test_static_parts.test_api_facts_come_only_from_the_agent
        with mock.patch("l3slice.model.build", boom), \
                mock.patch("l3slice.annotate.annotate", boom), mock.patch("l3slice.render.mermaid", boom), \
                mock.patch("l3slice.render.svg", boom):
            t, out, bundle = run(ScriptedProvider(script()))
        self.addCleanup(t.cleanup)
        self.assertEqual(bundle["agent"]["status"], "completed")
        self.assertTrue(bundle["coverage"]["complete"])
        self.assertEqual(len(bundle["rejected_claims"]), 1)  # the wrong prefix was refused, then fixed
        self.assertTrue(all(a["status"] == "ready" for a in bundle["artifacts"]))
        api = (out / "tech-specs/MUC-HANG/api/API-FR029-E2E-MUC-HANG-v1.md").read_text(encoding="utf-8")
        doc = json.loads(re.findall(r"^```json\n(.*?)^```", api, re.M | re.S)[0])
        validate_openapi(doc)
        self.assertEqual(sorted(doc["paths"]), ["/api/v1/items/", "/api/v1/items/{item_id}"])
        post = doc["paths"]["/api/v1/items/"]["post"]
        self.assertEqual(list(post["responses"]), ["201"])
        out_schema = doc["components"]["schemas"][post["responses"]["201"]["content"]["application/json"]["schema"]["$ref"]
                                                  .rsplit("/", 1)[1]]
        self.assertEqual(out_schema["properties"]["tags"]["type"], "array")
        get = doc["paths"]["/api/v1/items/{item_id}"]["get"]
        self.assertEqual([(p["name"], p["in"], p["required"]) for p in get["parameters"]],
                         [("item_id", "path", True), ("verbose", "query", False)])
        self.assertNotIn("only-in-test", api)
        self.assertIn("item (body, ItemIn, bắt buộc)", api)  # body parameter listed with name and place
        self.assertIn("inferred (fastapi.json_body_media, fastapi.return_annotation_response_model) / partial", api)
        readme = (out / "README.md").read_text(encoding="utf-8")
        self.assertIn("app/main.py:13", readme)
        self.assertIn("ROUTE_NOT_DECORATOR", readme)
        self.assertIn("https://audit.example.com/log", readme)
        self.assertIn("Chưa được cấp sơ đồ", readme)
        self.assertIn("`app/api/items.py` — Route (exact)", readme)
        self.assertIn("`app/api/__init__.py` — Khác", readme)
        self.assertIn("not_evaluated", readme)
        self.assertNotIn("Kiểm thử", readme.split("## Cấu trúc component")[1].split("## Lời gọi")[0])

    def test_architecture_parity(self):
        comps = json.loads(MEMBERSHIP.read_text(encoding="utf-8"))["components"]
        arch = {"schema": "archdia-fixture-v1", "snapshot_id": snapshot.take(FIX)[0]["snapshot_id"],
                "components": [{"id": f"c{i}", "name": c["name"], "files": sorted(c["files"])} for i, c in enumerate(comps)],
                "routes": [{"method": "POST", "path": "/api/v1/items/", "file": "app/api/items.py", "line": 9, "component_id": "c0"},
                           {"method": "GET", "path": "/api/v1/items/{item_id}", "file": "app/api/items.py", "line": 15,
                            "component_id": "c0"}]}
        t, _, bundle = run(ScriptedProvider(script(bad=False)), archdia=arch, diagram="flowchart LR\n  A --> B\n")
        self.addCleanup(t.cleanup)
        self.assertEqual(bundle["architecture_parity"]["status"], "passed")
        arch["routes"][1]["path"] = "/v1/api/items/{item_id}"  # same segments, wrong order
        arch["routes"][0]["component_id"] = "c1"
        t2, out, bundle = run(ScriptedProvider(script(bad=False)), archdia=arch)
        self.addCleanup(t2.cleanup)
        parity = bundle["architecture_parity"]
        self.assertEqual(parity["status"], "failed")
        self.assertEqual(parity["routes_only_in_architecture"], ["GET /v1/api/items/{item_id} @ app/api/items.py:15"])
        self.assertEqual(parity["owner_mismatch"], ["POST /api/v1/items/ @ app/api/items.py:9"])


class ReviewFindings(unittest.TestCase):
    """Regressions for the Codex cross-check of 07/10/2026 (numbers are the review's)."""

    def fixture(self):
        snap, sources = snapshot.take(FIX)
        tools = SourceTools(snap, sources)
        for p in READABLE:
            tools.read_file(p)
        return tools, Claims(tools)

    def test_01_unknown_values_do_not_crash(self):
        tools, claims = self.fixture()
        route = dict(READ, params=[dict(READ["params"][0], **{"in": {"unknown": "chưa rõ"}})])
        self.assertEqual(claims.submit({"routes": [route]})["accepted"], 1)
        http = dict(FINDINGS["http_calls"][0], method={"unknown": "chưa rõ"})
        self.assertEqual(claims.submit({"http_calls": [http]})["accepted"], 1)

    def test_02_partial_run_without_models_still_renders(self):
        steps = [[("list_files", {})], [("read_file", {"path": p}) for p in READABLE],
                 [("submit_findings", {"routes": [CREATE]})]]
        t, out, bundle = run(ScriptedProvider(steps))
        self.addCleanup(t.cleanup)
        self.assertEqual(bundle["agent"]["status"], "partial")
        route = next(f for f in bundle["facts"] if f["kind"] == "route")
        self.assertEqual(route["attributes"]["request_model_ids"]["state"], "unknown")
        self.assertTrue(all(a["status"] == "ready" for a in bundle["artifacts"]))

    def test_04_prefix_part_must_sit_on_its_kind_of_line(self):
        _, claims = self.fixture()
        parts = [dict(CHAIN[0], kind="router_prefix")] + CHAIN[1:] + [CREATE["path_parts"][-1]]
        self.assertEqual(claims.submit({"routes": [dict(CREATE, path_parts=parts)]})["accepted"], 0)

    def test_05_decorator_range_is_one_function(self):
        _, claims = self.fixture()
        bad = dict(READ, method="POST", decorator="app/api/items.py:9-16",
                   status={"codes": [201], "at": "app/api/items.py:9", "rule": None})
        self.assertEqual(claims.submit({"routes": [bad]})["accepted"], 0)

    def test_08_status_cannot_borrow_another_decorator(self):
        _, claims = self.fixture()
        bad = dict(READ, status={"codes": [201], "at": "app/api/items.py:9", "rule": None})
        self.assertEqual(claims.submit({"routes": [bad]})["accepted"], 0)

    def test_09_url_must_be_the_url_argument(self):
        tools = tools_for({"c.py": 'import httpx\nhttpx.get("https://right.example", headers={"Referer": "https://wrong.example"})\n'})
        tools.read_file("c.py")
        claims = Claims(tools)
        item = {"at": "c.py:2", "library": "httpx", "method": "GET", "target": {"kind": "literal", "value": "https://wrong.example"}}
        self.assertEqual(claims.submit({"http_calls": [item]})["accepted"], 0)
        item["target"]["value"] = "https://right.example"
        self.assertEqual(claims.submit({"http_calls": [item]})["accepted"], 1)
        self.assertEqual(claims.submit({"http_calls": [dict(item, method="POST")]})["accepted"], 0)

    def test_10_role_order_and_khac(self):
        _, claims = self.fixture()
        self.assertEqual(claims.submit({"file_roles": [{"file": "app/main.py", "role": "Khác", "at": "app/main.py:9"}]})["accepted"], 0)
        res = claims.submit({"file_roles": [{"file": "app/main.py", "role": "Khác", "at": "app/main.py:9",
                                             "not_signal": "giả định để kiểm đường thoát"}]})
        self.assertEqual(res["accepted"], 1)
        self.assertEqual(claims.submit({"file_roles": [{"file": "app/api/__init__.py", "role": "Hạ tầng",
                                                        "at": "app/api/__init__.py:1"}]})["accepted"], 0)

    def test_11_context_is_shrunk_only_after_sending(self):
        snap, sources = snapshot.take(FIX)
        tools = SourceTools(snap, sources)
        provider = ScriptedProvider([[("read_file", {"path": "app/main.py"})], [("finish", {})]])
        run_agent(tools, Claims(tools), [], provider, Budget(max_context_chars=1, max_finish_attempts=1))
        self.assertIn("receipt", provider.seen[1]["content"])

    def test_13_archdia_without_snapshot_is_not_evaluated(self):
        t, _, bundle = run(ScriptedProvider(script(bad=False)), archdia={"components": [], "routes": []})
        self.addCleanup(t.cleanup)
        self.assertEqual(bundle["architecture_parity"]["status"], "not_evaluated")

    def test_15_suspect_lines_must_be_accounted_for(self):
        _, claims = self.fixture()
        found = {s["at"] for s in claims.suspects()}
        self.assertEqual(found, {"app/api/items.py:9", "app/api/items.py:11", "app/api/items.py:15", "app/main.py:13"})
        claims.submit({k: v for k, v in FINDINGS.items() if k != "limitations"})
        self.assertEqual([s["at"] for s in claims.suspects()], ["app/main.py:13"])
        # app is built from FastAPI() in that file, so its add_api_route cannot be dismissed (Codex audit F08)
        res = claims.submit({"dismissed": [{"at": "app/main.py:13", "reason": "không phải đăng ký route"}]})
        self.assertEqual(res["accepted"], 0)
        self.assertEqual([s["at"] for s in claims.suspects()], ["app/main.py:13"])

    def test_17_masked_literal_matches_what_the_model_saw(self):
        tools = tools_for({"c.py": 'import httpx\nhttpx.get("https://u:demo-only-password@host/")\n'})
        self.assertIn("***", tools.read_file("c.py")["text"])
        item = {"at": "c.py:2", "library": "httpx", "method": "GET", "target": {"kind": "literal", "value": "https://u:***@host/"}}
        self.assertEqual(Claims(tools).submit({"http_calls": [item]})["accepted"], 1)

    def test_19_nested_unknown_makes_the_model_partial(self):
        models = [dict(MODELS[0], fields=[dict(MODELS[0]["fields"][0], required={"unknown": "chưa rõ"})])] + MODELS[1:]
        t, _, bundle = run(ScriptedProvider(script(dict(FINDINGS, models=models), bad=False)))
        self.addCleanup(t.cleanup)
        tag = next(f for f in bundle["facts"] if f["kind"] == "model" and f["attributes"]["name"]["value"] == "Tag")
        self.assertEqual(tag["completeness"], "partial")

    def test_scope_virtualenv_marker_and_src_layout(self):
        tools = tools_for({"src/shop/api.py": "x = 1\n", "examples/a.py": "from shop import api\n",
                           "toolenv/pyvenv.cfg": "home = x\n", "toolenv/lib/mod.py": "y = 2\n"})
        self.assertEqual(tools.readable, ["examples/a.py", "src/shop/api.py"])
        self.assertEqual({x["path"]: x["scope"] for x in tools.not_readable()}, {"toolenv/lib/mod.py": "environment"})


class ReviewRound2(unittest.TestCase):
    """Regressions for the second Codex review (07/10/2026)."""

    def test_signal_across_lines_does_not_crash(self):
        tools = tools_for({"m.py": 'x = 1\nif (__name__ ==\n    "__main__"):\n    pass\n'})
        tools.read_file("m.py")
        res = Claims(tools).submit({"file_roles": [{"file": "m.py", "role": "Khác", "at": "m.py:1"}]})
        self.assertEqual(res["accepted"], 0)
        self.assertIn("dòng 2", res["errors"][0]["errors"][0])

    def test_form_body_survives_the_final_check(self):
        t, out, bundle = run(ScriptedProvider(script(dict(FINDINGS, routes=[CREATE, dict(
            READ, request_body={"models": [], "media_type": "application/x-www-form-urlencoded", "required": True,
                                "embedded": False, "at": "app/api/items.py:16",
                                "fields": [{"name": "verbose", "type": "boolean", "required": False,
                                            "at": "app/api/items.py:16"}]})]), bad=False)))
        self.addCleanup(t.cleanup)
        self.assertTrue(all(a["status"] == "ready" for a in bundle["artifacts"]), bundle["artifacts"])

    def test_http_keywords(self):
        tools = tools_for({"c.py": 'import httpx\nhttpx.request(url="https://right.example", method="GET")\n'})
        tools.read_file("c.py")
        item = {"at": "c.py:2", "library": "httpx", "method": "GET", "target": {"kind": "literal", "value": "https://right.example"}}
        self.assertEqual(Claims(tools).submit({"http_calls": [item]})["errors"], [])

    def test_raw_secret_is_refused_as_target(self):
        tools = tools_for({"c.py": 'import httpx\nhttpx.get("https://u:demo-only-password@host/")\n'})
        tools.read_file("c.py")
        item = {"at": "c.py:2", "library": "httpx", "method": "GET",
                "target": {"kind": "literal", "value": "https://u:demo-only-password@host/"}}
        self.assertEqual(Claims(tools).submit({"http_calls": [item]})["accepted"], 0)

    def test_unknown_required_of_inline_body_is_kept(self):
        tools = tools_for({"m.py": "from fastapi import FastAPI, Form\napp = FastAPI()\n\n\n@app.post('/l')\n"
                                   "def login(user: str = Form()):\n    pass\n"})
        tools.read_file("m.py")
        claims = Claims(tools)
        res = claims.submit({"routes": [{"method": "POST", "handler": "m.py::login", "decorator": "m.py:5-6",
                                         "application": "m.py:2", "params": [], "response": None,
                                         "path_parts": [{"kind": "decorator", "value": "/l", "at": "m.py:5"}],
                                         "status": {"codes": [200], "rule": "fastapi.default_status_200"},
                                         "dependencies": [], "auth": {"unknown": "chưa rõ"},
                                         "request_body": {"models": [], "media_type": "application/x-www-form-urlencoded",
                                                          "required": {"unknown": "chưa rõ"}, "embedded": False, "at": "m.py:6",
                                                          "fields": [{"name": "user", "type": "string",
                                                                      "required": {"unknown": "chưa rõ"}, "at": "m.py:6"}]}}]})
        self.assertEqual(res["errors"], [])
        from l3slice.docfacts import build_facts
        route = next(f for f in build_facts(claims, {"snapshot_id": tools.snapshot_id, "files": list(tools.files.values())},
                                            "unit:x") if f["kind"] == "route")
        self.assertEqual(route["completeness"], "partial")

    def test_second_decorator_on_same_handler_stays_suspect(self):
        tools = tools_for({"m.py": "from fastapi import FastAPI\napp = FastAPI()\n\n\n@app.get('/a')\n@app.post('/b')\n"
                                   "def h():\n    pass\n"})
        tools.read_file("m.py")
        claims = Claims(tools)
        claims.submit({"routes": [{"method": "GET", "handler": "m.py::h", "decorator": "m.py:5-7", "application": "m.py:2",
                                   "path_parts": [{"kind": "decorator", "value": "/a", "at": "m.py:5"}], "params": [],
                                   "request_body": None, "response": None,
                                   "status": {"codes": [200], "rule": "fastapi.default_status_200"},
                                   "dependencies": [], "auth": {"unknown": "chưa rõ"}}]})
        self.assertEqual([s["at"] for s in claims.suspects()], ["m.py:6"])

    def test_decorator_of_a_non_fastapi_object_is_refused(self):
        tools = tools_for({"m.py": "from fastapi import FastAPI\napp = FastAPI()\ndb = Registry()\n\n\n@db.get('/fake')\n"
                                   "def h():\n    pass\n"})
        tools.read_file("m.py")
        res = Claims(tools).submit({"routes": [{"method": "GET", "handler": "m.py::h", "decorator": "m.py:6-7",
                                                "application": "m.py:2", "params": [], "request_body": None, "response": None,
                                                "path_parts": [{"kind": "decorator", "value": "/fake", "at": "m.py:6"}],
                                                "status": {"codes": [200], "rule": "fastapi.default_status_200"},
                                                "dependencies": [], "auth": {"unknown": "chưa rõ"}}]})
        self.assertEqual(res["accepted"], 0)

    def test_http_suspects_follow_clients_not_every_get(self):
        src = ("import httpx\nimport requests\n\n\nasync def fetch(url):\n    async with httpx.AsyncClient() as c:\n"
               "        return (await c.get(url)).json()\n\n\nasync def use():\n    data = await fetch('x')\n"
               "    return data.get('k')\n\n\ndef ping():\n    return requests.Session().get('https://a.example/p')\n")
        tools = tools_for({"h.py": src})
        tools.read_file("h.py")
        self.assertEqual([s["at"] for s in Claims(tools).suspects()], ["h.py:7", "h.py:16"])

    def test_dismissals_are_kept(self):
        # an untyped `session` may be an HTTP session: it stays a suspect; a dict `.get` does not (line 6)
        tools = tools_for({"c.py": "import httpx\n\n\ndef load(session, key, row):\n    return session.get(key)\n"
                                   "    return row.get(key)\n"})
        tools.read_file("c.py")
        claims = Claims(tools)
        self.assertEqual([s["at"] for s in claims.suspects()], ["c.py:5"])
        res = claims.submit({"dismissed": [{"at": "c.py:5", "reason": "session.get là truy vấn CSDL, không phải HTTP"}]})
        self.assertEqual(res["accepted"], 1)
        self.assertEqual(claims.suspects(), [])
        self.assertEqual(list(claims.dismissed.values())[0]["reason"], "session.get là truy vấn CSDL, không phải HTTP")


class SmallContext(unittest.TestCase):
    """Provider windows like Groq's 8K tokens per request (first real pilot, 07/10/2026)."""

    def setUp(self):
        snap, sources = snapshot.take(FIX)
        self.tools = SourceTools(snap, sources)

    def test_413_shortens_and_resends_and_new_results_are_never_shortened_unseen(self):
        reads = [[("read_file", {"path": p})] for p in READABLE]
        provider = ScriptedProvider([[("list_files", {})], *reads[:2], ProviderError("HTTP 413 rate_limit_exceeded", False),
                                     *reads[2:], [("finish", {})]])
        run = run_agent(self.tools, Claims(self.tools), [], provider,
                        Budget(max_request_tokens=4000, max_turn_read_chars=100_000, max_finish_attempts=1))
        self.assertNotIn("MODEL_ERROR", run.reason)
        for i, msg in enumerate(provider.seen[1:], 1):  # the result of each read reached the model whole
            if msg.get("role") == "tool" and i < len(provider.seen) - 1:
                self.assertNotIn("shortened", msg["content"])

    def test_turn_read_cap_delivers_nothing_beyond_it(self):
        provider = ScriptedProvider([[("read_file", {"path": p}) for p in READABLE], [("finish", {})]])
        run_agent(self.tools, Claims(self.tools), [], provider, Budget(max_turn_read_chars=10, max_finish_attempts=1))
        delivered = [p for p in READABLE if self.tools.state.get(p)]
        self.assertEqual(delivered, READABLE[:1])


class Pacing(unittest.TestCase):
    def test_waits_until_the_minute_window_has_room(self):
        import os
        from l3slice.docagent import OpenAICompatProvider
        now, slept = [0.0], []
        os.environ["FR029_TEST_KEY"] = "x"
        self.addCleanup(os.environ.pop, "FR029_TEST_KEY")
        p = OpenAICompatProvider("http://unused", "m", "FR029_TEST_KEY", tokens_per_minute=8000, clock=lambda: now[0],
                                 sleep=lambda s: (slept.append(s), now.__setitem__(0, now[0] + s)))
        p.window = [(0.0, 7000)]
        now[0] = 10.0
        p._pace(3000)
        self.assertEqual(slept, [51.0])
        p._pace(3000)
        self.assertEqual(slept, [51.0])


class ResponsesApi(unittest.TestCase):
    def test_transcript_carries_reasoning_and_tool_outputs(self):
        import os
        from l3slice.docagent import TOOL_SPECS, ResponsesProvider
        os.environ["FR029_TEST_KEY"] = "x"
        self.addCleanup(os.environ.pop, "FR029_TEST_KEY")
        p = ResponsesProvider("https://api.openai.com/v1", "m", "FR029_TEST_KEY", prices=(1.0, 0.1, 2.0))
        sent = []
        replies = [{"output": [{"type": "reasoning", "encrypted_content": "e1"},
                               {"type": "function_call", "call_id": "c1", "name": "list_files", "arguments": "{}"}],
                    "usage": {"input_tokens": 100, "input_tokens_details": {"cached_tokens": 40}, "output_tokens": 10}},
                   {"output": [{"type": "message", "content": [{"type": "output_text", "text": "xong"}]}], "usage": {}}]
        p._post = lambda payload: (sent.append(json.loads(json.dumps(payload))), replies.pop(0))[1]
        msgs = [{"role": "system", "content": "S"}, {"role": "user", "content": "U"}]
        r = p.chat(msgs, TOOL_SPECS)
        self.assertEqual(r["tool_calls"], [{"id": "c1", "name": "list_files", "arguments": {}}])
        self.assertAlmostEqual(p.cost_usd, (60 * 1.0 + 40 * 0.1 + 10 * 2.0) / 1e6)
        msgs += [{"role": "assistant", "content": "", "tool_calls": []},
                 {"role": "tool", "tool_call_id": "c1", "content": "{\"files\": []}"}]
        r = p.chat(msgs, TOOL_SPECS)
        second = sent[1]
        self.assertFalse(second["store"])
        self.assertEqual(second["instructions"], "S")
        self.assertEqual([x.get("type") or x.get("role") for x in second["input"]],
                         ["user", "reasoning", "function_call", "function_call_output"])
        self.assertEqual(r["content"], "xong")


class SupersededRoute(unittest.TestCase):
    def test_attached_version_replaces_unattached_one(self):
        snap, sources = snapshot.take(FIX)
        tools = SourceTools(snap, sources)
        for p in READABLE:
            tools.read_file(p)
        claims = Claims(tools)
        early = dict(CREATE, application={"unknown": "chưa đọc main.py"}, path_parts=[CREATE["path_parts"][-1]])
        self.assertEqual(claims.submit({"routes": [early]})["accepted"], 1)
        self.assertEqual(claims.submit({"routes": [CREATE]})["accepted"], 1)
        self.assertEqual(len(claims.routes), 1)
        claims.submit({"routes": [early]})  # a late unattached copy is ignored too
        self.assertEqual([k[2] for k in claims.routes], [("app/main.py", 5, 5)])


class PrefixThroughHelper(unittest.TestCase):
    def test_literal_at_call_site_with_registration_in_helper(self):
        tools = tools_for({"main.py": "from fastapi import FastAPI\nfrom reg import attach\nfrom routes import router\n"
                                      "app = FastAPI()\nattach(app, router, prefix=\"/api/v1\")\n",
                           "reg.py": "def attach(app, router, prefix):\n    app.include_router(router, prefix=prefix)\n",
                           "routes.py": "from fastapi import APIRouter\nrouter = APIRouter()\n\n\n@router.post(\"/orders\")\n"
                                        "def create():\n    pass\n"})
        for p in ("main.py", "reg.py", "routes.py"):
            tools.read_file(p)
        route = {"method": "POST", "handler": "routes.py::create", "decorator": "routes.py:5-6", "application": "main.py:4",
                 "path_parts": [{"kind": "include_prefix", "value": "/api/v1", "at": "main.py:5", "used_at": "reg.py:2"},
                                {"kind": "decorator", "value": "/orders", "at": "routes.py:5"}],
                 "params": [], "request_body": None, "response": None, "dependencies": [],
                 "status": {"codes": [200], "rule": "fastapi.default_status_200"}, "auth": {"unknown": "chưa rõ"}}
        claims = Claims(tools)
        self.assertEqual(claims.submit({"routes": [route]})["errors"], [])
        # the same route resubmitted with an equivalent chain (one more empty registration) replaces the first one
        same = dict(route, path_parts=[route["path_parts"][0], {"kind": "include_prefix", "value": "", "at": "reg.py:2"},
                                       route["path_parts"][1]])
        claims.submit({"routes": [same]})
        self.assertEqual(len(claims.routes), 1)
        bad = dict(route, path_parts=[dict(route["path_parts"][0], used_at=None)] + route["path_parts"][1:])
        bad["path_parts"][0].pop("used_at")
        self.assertEqual(Claims(tools).submit({"routes": [bad]})["accepted"], 0)


class DynamicModel(unittest.TestCase):
    """A model created at runtime (SummarySchema = pydantic_model_creator(TextSummary)) can be submitted by its
    assignment line; its fields are unknown with the reason, instead of the whole response becoming unknown."""
    SRC = ("from tortoise.contrib.pydantic import pydantic_model_creator\nfrom fastapi import FastAPI\n\n\n"
           "class TextSummary:\n    url: str\n\n\nSummarySchema = pydantic_model_creator(TextSummary)\napp = FastAPI()\n"
           "\n\n@app.get('/s', response_model=SummarySchema)\ndef s():\n    pass\n")
    ROUTE = {"method": "GET", "handler": "m.py::s", "decorator": "m.py:13-14", "application": "m.py:10",
             "path_parts": [{"kind": "decorator", "value": "/s", "at": "m.py:13"}], "params": [], "request_body": None,
             "response": {"model": "m.py::SummarySchema", "array": False, "at": "m.py:13"},
             "status": {"codes": [200], "rule": "fastapi.default_status_200"}, "dependencies": [],
             "auth": {"unknown": "chưa rõ"}}

    def test_dynamic_model_is_accepted_with_unknown_fields(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "m.py").write_text(self.SRC, encoding="utf-8")
            snap, sources = snapshot.take(Path(d))
        tools = SourceTools(snap, sources)
        tools.read_file("m.py")
        claims = Claims(tools)
        item = {"id": "m.py::SummarySchema", "at": "m.py:9", "fields": [],
                "dynamic": {"reason": "tạo bằng pydantic_model_creator lúc chạy"}}
        self.assertEqual(claims.add_model(item), [])
        self.assertEqual(claims.add_route(self.ROUTE), [])
        fact = next(f for f in build_facts(claims, snap, "u") if f["kind"] == "model")
        self.assertEqual(fact["attributes"]["fields"]["state"], "unknown")
        self.assertIn("pydantic_model_creator", fact["attributes"]["fields"]["reason"])

    def test_dynamic_model_goes_through_the_whole_pipeline(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "src"
            src.mkdir()
            (src / "m.py").write_text(self.SRC, encoding="utf-8")
            members = Path(d) / "members.json"
            members.write_text(json.dumps({"partition_version": "fixture-membership-v1", "components": [
                {"name": "Toàn bộ", "kind": "normal", "files": ["m.py"]}]}), encoding="utf-8")
            findings = {"models": [{"id": "m.py::SummarySchema", "at": "m.py:9", "fields": [],
                                    "dynamic": {"reason": "tạo bằng pydantic_model_creator"}}],
                        "routes": [self.ROUTE], "file_roles": [{"file": "m.py", "role": "Điểm vào", "at": "m.py:10"}]}
            provider = ScriptedProvider([[("list_files", {})], [("read_file", {"path": "m.py"})],
                                         [("submit_findings", findings)], [("finish", {})]])
            bundle = docpipeline.run_documents(src, Path(d) / "out", members, "dyn", provider)
            api = next(a for a in bundle["artifacts"] if a["kind"] == "api")
            self.assertEqual(api["status"], "ready", api)

    def test_dynamic_needs_an_assignment_from_a_call_and_no_invented_fields(self):
        tools = tools_for({"m.py": self.SRC})
        tools.read_file("m.py")
        claims = Claims(tools)
        dyn = {"reason": "sinh lúc chạy"}
        self.assertTrue(claims.add_model({"id": "m.py::TextSummary", "at": "m.py:5", "fields": [], "dynamic": dyn}))
        self.assertTrue(claims.add_model({"id": "m.py::SummarySchema", "at": "m.py:9", "dynamic": dyn,
                                          "fields": [{"name": "url", "type": "string", "required": True,
                                                      "nullable": False, "at": "m.py:6"}]}))


class UnreferencedModels(unittest.TestCase):
    def test_models_no_route_uses_are_left_out_and_listed(self):
        findings = copy.deepcopy(FINDINGS)
        extra = copy.deepcopy(findings["models"][0])
        findings["models"].append(extra)  # resubmitting the same model changes nothing
        snap, sources = snapshot.take(FIX)
        tools = SourceTools(snap, sources)
        for p in READABLE:
            tools.read_file(p)
        claims = Claims(tools)
        claims.submit({"models": findings["models"]})
        before = {f["attributes"]["name"]["value"] for f in build_facts(claims, snap, "u") if f["kind"] == "model"}
        self.assertEqual(before, set(), "no route yet: no model is documented")
        self.assertEqual(sorted(claims.unreferenced_models), sorted(claims.models))
        claims.submit({"routes": findings["routes"]})
        after = {f["attributes"]["name"]["value"] for f in build_facts(claims, snap, "u") if f["kind"] == "model"}
        self.assertEqual(len(after), len(claims.models))
        self.assertEqual(claims.unreferenced_models, [])


class GenericResponse(unittest.TestCase):
    """response_model=PaginatedListResponse[APIKeyRead]: the generic class and its arguments are documented."""
    SRC = ("from typing import Generic, TypeVar\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel\n\n"
           "T = TypeVar('T')\n\n\nclass Page(BaseModel, Generic[T]):\n    data: list[T]\n    total: int\n\n\n"
           "class KeyRead(BaseModel):\n    name: str\n\n\napp = FastAPI()\n\n\n"
           "@app.get('/keys', response_model=Page[KeyRead])\ndef keys():\n    pass\n")
    MODELS = [{"id": "m.py::Page", "at": "m.py:8", "fields": [
                   {"name": "data", "type": {"unknown": "kiểu tham số T"}, "required": True, "nullable": False, "at": "m.py:9"},
                   {"name": "total", "type": "integer", "required": True, "nullable": False, "at": "m.py:10"}]},
              {"id": "m.py::KeyRead", "at": "m.py:13", "fields": [
                   {"name": "name", "type": "string", "required": True, "nullable": False, "at": "m.py:14"}]}]
    ROUTE = {"method": "GET", "handler": "m.py::keys", "decorator": "m.py:20-21", "application": "m.py:17",
             "path_parts": [{"kind": "decorator", "value": "/keys", "at": "m.py:20"}], "params": [], "request_body": None,
             "response": {"model": "m.py::Page", "args": ["m.py::KeyRead"], "array": False, "at": "m.py:20"},
             "status": {"codes": [200], "rule": "fastapi.default_status_200"}, "dependencies": [],
             "auth": {"unknown": "chưa rõ"}}

    def run_pipeline(self, route):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "src"
            src.mkdir()
            (src / "m.py").write_text(self.SRC, encoding="utf-8")
            members = Path(d) / "members.json"
            members.write_text(json.dumps({"partition_version": "fixture-membership-v1", "components": [
                {"name": "Toàn bộ", "kind": "normal", "files": ["m.py"]}]}), encoding="utf-8")
            findings = {"models": self.MODELS, "routes": [route],
                        "file_roles": [{"file": "m.py", "role": "Điểm vào", "at": "m.py:17"}]}
            provider = ScriptedProvider([[("list_files", {})], [("read_file", {"path": "m.py"})],
                                         [("submit_findings", findings)], [("finish", {})]])
            bundle = docpipeline.run_documents(src, Path(d) / "out", members, "gen", provider)
            text = next((Path(d) / "out").rglob("API-*.md")).read_text(encoding="utf-8")
        return bundle, text

    def test_generic_response_is_documented_with_its_arguments(self):
        bundle, text = self.run_pipeline(self.ROUTE)
        self.assertEqual(bundle["rejected_claims"], [])
        self.assertEqual(bundle["unreferenced_models"], [])
        self.assertIn("Page[KeyRead]", text)
        api = next(a for a in bundle["artifacts"] if a["kind"] == "api")
        self.assertEqual(api["status"], "ready", api)
        spec = json.loads(re.search(r"```json\s*\n(.*?)```", text, re.S).group(1))
        from openapi_spec_validator import validate
        validate(spec)

    def test_argument_must_appear_at_the_cited_line(self):
        route = copy.deepcopy(self.ROUTE)
        route["response"]["args"] = ["m.py::Missing"]  # no Missing on line 20
        tools = tools_for({"m.py": self.SRC})
        tools.read_file("m.py")
        self.assertTrue(Claims(tools).add_route(route))


class ExternalGenericResponse(GenericResponse):
    """response_model=PaginatedListResponse[KeyRead] with the generic from a library (fastcrud) outside the repo."""
    SRC = ("from fastcrud import PaginatedListResponse\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel\n\n\n"
           "\n\n\n\n\n\n\n"
           "class KeyRead(BaseModel):\n    name: str\n\n\napp = FastAPI()\n\n\n"
           "@app.get('/keys', response_model=PaginatedListResponse[KeyRead])\ndef keys():\n    pass\n")
    MODELS = [GenericResponse.MODELS[1]]
    ROUTE = dict(GenericResponse.ROUTE, response={"external": "fastcrud.PaginatedListResponse", "args": ["m.py::KeyRead"],
                                                  "array": False, "at": "m.py:20"})

    def test_generic_response_is_documented_with_its_arguments(self):
        bundle, text = self.run_pipeline(self.ROUTE)
        self.assertEqual(bundle["rejected_claims"], [])
        self.assertEqual(bundle["unreferenced_models"], [])
        self.assertIn("PaginatedListResponse[KeyRead]", text)
        api = next(a for a in bundle["artifacts"] if a["kind"] == "api")
        self.assertEqual(api["status"], "ready", api)
        spec = json.loads(re.search(r"```json\s*\n(.*?)```", text, re.S).group(1))
        from openapi_spec_validator import validate
        validate(spec)

    def test_argument_must_appear_at_the_cited_line(self):
        route = copy.deepcopy(self.ROUTE)
        route["response"]["args"] = ["m.py::Missing"]
        tools = tools_for({"m.py": self.SRC})
        tools.read_file("m.py")
        self.assertTrue(Claims(tools).add_route(route))
        route["response"] = dict(self.ROUTE["response"], external="fastcrud.OtherPage")
        self.assertTrue(Claims(tools).add_route(route))


class DependencyAlias(unittest.TestCase):
    """db: AsyncSessionDep, with AsyncSessionDep = Annotated[AsyncSession, Depends(async_session)] in another file."""
    FILES = {"deps.py": "from typing import Annotated\nfrom fastapi import Depends\n\n\nasync def async_session():\n"
                        "    yield None\n\n\nAsyncSessionDep = Annotated[object, Depends(async_session)]\n",
             "main.py": "from fastapi import FastAPI\nfrom deps import AsyncSessionDep\napp = FastAPI()\n\n\n"
                        "@app.get(\"/u\")\nasync def users(db: AsyncSessionDep):\n    pass\n"}

    def submit(self, name):
        tools = tools_for(self.FILES)
        for p in self.FILES:
            tools.read_file(p)
        return Claims(tools).add_route({
            "method": "GET", "handler": "main.py::users", "decorator": "main.py:6-7", "application": "main.py:3",
            "path_parts": [{"kind": "decorator", "value": "/u", "at": "main.py:6"}], "params": [], "request_body": None,
            "response": None, "dependencies": [{"name": name, "at": "main.py:7"}],
            "status": {"codes": [200], "rule": "fastapi.default_status_200"}, "auth": {"unknown": "chưa rõ"}})

    def test_dependency_through_an_annotated_alias(self):
        self.assertEqual(self.submit("async_session"), [])

    def test_a_name_the_alias_does_not_wrap_is_refused(self):
        self.assertTrue(self.submit("get_db"))


class AppFromFactory(unittest.TestCase):
    """app = create_application(...) where the factory returns FastAPI(...): @app.get is a FastAPI route."""
    FILES = {"factory.py": "from fastapi import FastAPI\n\n\ndef create_application(**kw):\n"
                           "    application = FastAPI(**kw)\n    return application\n",
             "main.py": "from factory import create_application\n\napp = create_application(title='x')\n\n\n"
                        "@app.get(\"/health\")\nasync def health_check() -> dict[str, str]:\n    return {}\n",
             "fake.py": "def make():\n    return object()\n\n\nthing = make()\n\n\n@thing.get(\"/x\")\ndef x():\n    pass\n"}

    def claims(self):
        tools = tools_for(self.FILES)
        for p in self.FILES:
            tools.read_file(p)
        return Claims(tools)

    def route(self, handler, decorator, path, application):
        return {"method": "GET", "handler": handler, "decorator": decorator, "application": application,
                "path_parts": [{"kind": "decorator", "value": path, "at": decorator.split("-")[0]}], "params": [],
                "request_body": None, "response": None, "dependencies": [],
                "status": {"codes": [200], "rule": "fastapi.default_status_200"}, "auth": {"unknown": "chưa rõ"}}

    def test_receiver_built_by_a_factory_returning_fastapi(self):
        self.assertEqual(self.claims().add_route(self.route("main.py::health_check", "main.py:6-7", "/health",
                                                            "factory.py:5")), [])

    def test_receiver_built_by_another_function_is_refused(self):
        self.assertTrue(self.claims().add_route(self.route("fake.py::x", "fake.py:9-10", "/x", {"unknown": "?"})))


class MultiLineCall(unittest.TestCase):
    """The URL literal of a call split over lines (session.post(\\n "https://..."), is the call's URL argument."""
    SRC = ("import aiohttp\n\n\nasync def token():\n    async with aiohttp.ClientSession() as session:\n"
           "        async with session.post(\n            \"https://auth.sid.ai/oauth/token\",\n"
           "            headers={},\n        ) as r:\n            return await r.json()\n")

    def submit(self, value, at="a.py:6"):
        tools = tools_for({"a.py": self.SRC})
        tools.read_file("a.py")
        return Claims(tools).add_http({"at": at, "library": "aiohttp", "method": "POST",
                                       "target": {"kind": "literal", "value": value}})

    def test_literal_on_the_next_line_is_the_url_argument(self):
        self.assertEqual(self.submit("https://auth.sid.ai/oauth/token"), [])

    def test_long_call_with_a_nested_body(self):
        src = ("import aiohttp\n\n\nasync def revoke():\n    async with aiohttp.ClientSession() as session:\n"
               "        await session.post(\n            \"https://auth.sid.ai/oauth/revoke\",\n            headers={\n"
               + "".join(f"                \"h{i}\": \"v\",\n" for i in range(12)) +
               "            },\n            data=json.dumps({\"a\": 1}),\n        )\n")
        tools = tools_for({"a.py": src})
        tools.read_file("a.py")
        self.assertEqual(Claims(tools).add_http({"at": "a.py:6", "library": "aiohttp", "method": "POST", "target":
                                                 {"kind": "literal", "value": "https://auth.sid.ai/oauth/revoke"}}), [])

    def test_other_literals_or_lines_are_still_refused(self):
        self.assertTrue(self.submit("https://other.example/x"))
        self.assertTrue(self.submit("https://auth.sid.ai/oauth/token", at="a.py:5"))


class BaseUrlConfig(unittest.TestCase):
    """A relative URL on a client made with base_url=settings.X targets the setting X, cited at the base_url line."""
    SRC = ("import httpx\nfrom config import settings\n\n\ndef client():\n"
           "    return httpx.AsyncClient(base_url=settings.EVOLUTION_API_BASE_URL)\n\n\n"
           "async def find(name):\n    async with client() as c:\n        return await c.get(f\"/webhook/{name}\")\n")

    def submit(self, target):
        tools = tools_for({"e.py": self.SRC})
        tools.read_file("e.py")
        return Claims(tools).add_http({"at": "e.py:11", "library": "httpx", "method": "GET", "target": target})

    def test_config_key_cited_at_the_base_url_line(self):
        self.assertEqual(self.submit({"kind": "config", "value": "EVOLUTION_API_BASE_URL", "config_at": "e.py:6"}), [])

    def test_config_key_must_be_at_the_call_or_at_config_at(self):
        self.assertTrue(self.submit({"kind": "config", "value": "EVOLUTION_API_BASE_URL"}))
        self.assertTrue(self.submit({"kind": "config", "value": "OTHER_URL", "config_at": "e.py:6"}))


class DependencyParams(unittest.TestCase):
    """FastAPI flattens Header/Query/Cookie/Path parameters of Depends functions into the endpoint (07/10/2026: the
    model left them out on 62 routes of two repositories). The check names them as open problems; the agent submits."""
    FILES = {"deps.py": "from typing import Annotated\nfrom fastapi import Depends, Header, Query\n\n\n"
                        "def org(x_organization_id: Annotated[str | None, Header()] = None):\n    return x_organization_id\n\n\n"
                        "def user(authorization: Annotated[str | None, Header(alias=\"Authorization\")] = None,\n"
                        "         o=Depends(org), page: int = Query(1)):\n    return authorization\n",
             "main.py": "from fastapi import FastAPI, Depends\nfrom deps import user\napp = FastAPI()\n\n\n"
                        "@app.get(\"/me\")\ndef me(u=Depends(user)):\n    pass\n"}

    def route(self, params):
        return {"method": "GET", "handler": "main.py::me", "decorator": "main.py:6-7", "application": "main.py:3",
                "path_parts": [{"kind": "decorator", "value": "/me", "at": "main.py:6"}], "params": params,
                "request_body": None, "response": None, "dependencies": [{"name": "user", "at": "main.py:7"}],
                "status": {"codes": [200], "rule": "fastapi.default_status_200"}, "auth": {"unknown": "chưa rõ"}}

    def claims(self, params):
        tools = tools_for(self.FILES)
        for p in self.FILES:
            tools.read_file(p)
        claims = Claims(tools)
        self.assertEqual(claims.submit({"routes": [self.route(params)]})["errors"], [])
        return [p for p in claims.open_problems([]) if "dependency" in p]

    def test_missing_dependency_params_are_open_problems(self):
        problems = self.claims([])
        self.assertEqual(len(problems), 3, problems)
        text = " ".join(problems)
        for name in ("'Authorization'", "'x-organization-id'", "'page'"):
            self.assertIn(name, text)

    def test_factory_dependency_and_alias_are_followed(self):
        files = {"deps.py": "from typing import Annotated\nfrom fastapi import Depends, Header\n\n\n"
                            "def token(authorization: Annotated[str | None, Header(alias=\"Authorization\")] = None):\n"
                            "    return authorization\n\n\nTokenDep = Annotated[str, Depends(token)]\n\n\n"
                            "def plan(tier: str):\n    def _dependency(t: TokenDep):\n        return t\n    return _dependency\n",
                 "main.py": "from fastapi import FastAPI, Depends\nfrom deps import plan\napp = FastAPI()\n\n\n"
                            "@app.get(\"/w\")\ndef w(u=Depends(plan(\"PRO\"))):\n    pass\n"}
        tools = tools_for(files)
        for p in files:
            tools.read_file(p)
        claims = Claims(tools)
        route = dict(self.route([]), handler="main.py::w", path_parts=[{"kind": "decorator", "value": "/w", "at": "main.py:6"}],
                     dependencies=[{"name": "plan", "at": "main.py:7"}])
        self.assertEqual(claims.submit({"routes": [route]})["errors"], [])
        problems = [p for p in claims.open_problems([]) if "dependency" in p]
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("'Authorization'", problems[0])  # `tier`, the factory's own argument, is not a request parameter

    def test_class_method_dependency_and_plain_query_params(self):
        files = {"deps.py": "from fastapi import Depends, Header, Request\n\n\n"
                            "def org(x_org: str | None = Header(None)):\n    return x_org\n\n\n"
                            "class Crud:\n    @classmethod\n    def inject(cls, o=Depends(org)):\n        return cls()\n\n\n"
                            "def search(request: Request, q: str | None = None, skip: int = 0, body: dict = None):\n"
                            "    return q\n",
                 "main.py": "from fastapi import FastAPI, Depends\nfrom deps import Crud, search\napp = FastAPI()\n\n\n"
                            "@app.get(\"/w\")\ndef w(c=Depends(Crud.inject), s=Depends(search)):\n    pass\n"}
        tools = tools_for(files)
        for p in files:
            tools.read_file(p)
        claims = Claims(tools)
        route = dict(self.route([]), handler="main.py::w", path_parts=[{"kind": "decorator", "value": "/w", "at": "main.py:6"}],
                     dependencies=[{"name": "Crud.inject", "at": "main.py:7"}, {"name": "search", "at": "main.py:7"}])
        self.assertEqual(claims.submit({"routes": [route]})["errors"], [])
        text = " ".join(p for p in claims.open_problems([]) if "dependency" in p)
        for name in ("'x-org'", "'q'", "'skip'"):
            self.assertIn(name, text)
        for name in ("'request'", "'body'"):  # Request is not a parameter; a dict is a body, not a query
            self.assertNotIn(name, text)

    def test_factory_choosing_module_functions_and_multiline_alias(self):
        files = {"deps.py": "from typing import Annotated\nfrom fastapi import Depends, Header, Query\n\n\n"
                            "def _strict(token: str = Header(...)):\n    return token\n\n\n"
                            "def _loose(token: str | None = Header(None)):\n    return token\n\n\n"
                            "def authorizer(*, required: bool = True):\n    return _strict if required else _loose\n\n\n"
                            "def paging(page: int = Query(1), per_page: int = Query(10, alias=\"itemsPerPage\")):\n"
                            "    return page\n\n\nPaging = Annotated[\n    dict,\n    Depends(paging),\n]\n",
                 "main.py": "from fastapi import FastAPI, Depends\nfrom deps import authorizer, Paging\napp = FastAPI()\n\n\n"
                            "@app.get(\"/w\")\ndef w(u=Depends(authorizer(required=False)), p: Paging = None):\n    pass\n"}
        tools = tools_for(files)
        for p in files:
            tools.read_file(p)
        claims = Claims(tools)
        route = dict(self.route([]), handler="main.py::w", path_parts=[{"kind": "decorator", "value": "/w", "at": "main.py:6"}],
                     dependencies=[{"name": "authorizer", "at": "main.py:7"}, {"name": "paging", "at": "main.py:7"}])
        self.assertEqual(claims.submit({"routes": [route]})["errors"], [])  # paging through the multi-line alias
        text = " ".join(p for p in claims.open_problems([]) if "dependency" in p)
        for name in ("'token'", "'page'", "'itemsPerPage'"):
            self.assertIn(name, text)
        self.assertNotIn("'required'", text)  # the factory's own argument

    def test_submitted_dependency_params_close_the_problem(self):
        params = [{"name": "Authorization", "in": "header", "type": "string", "required": False, "at": "deps.py:9"},
                  {"name": "x-organization-id", "in": "header", "type": "string", "required": False, "at": "deps.py:5"},
                  {"name": "page", "in": "query", "type": "integer", "required": False, "at": "deps.py:10"}]
        self.assertEqual(self.claims(params), [])


class ResponseType(unittest.TestCase):
    def test_non_model_response_type_is_documented(self):
        tools = tools_for({"m.py": "from fastapi import FastAPI\napp = FastAPI()\n\n\n@app.get('/health')\n"
                                   "def health() -> bool:\n    return True\n"})
        tools.read_file("m.py")
        claims = Claims(tools)
        res = claims.submit({"routes": [{"method": "GET", "handler": "m.py::health", "decorator": "m.py:5-6",
                                         "application": "m.py:2", "params": [], "request_body": None, "dependencies": [],
                                         "path_parts": [{"kind": "decorator", "value": "/health", "at": "m.py:5"}],
                                         "response": {"type": "boolean", "at": "m.py:6",
                                                      "rule": "fastapi.return_annotation_response_model"},
                                         "status": {"codes": [200], "rule": "fastapi.default_status_200"},
                                         "auth": {"unknown": "chưa rõ"}}]})
        self.assertEqual(res["errors"], [])
        from l3slice.docfacts import build_facts
        from l3slice.render import render_api
        facts = build_facts(claims, {"snapshot_id": tools.snapshot_id, "files": list(tools.files.values())}, "unit:x")
        text, doc, _, _ = render_api({"confidence": "exact", "completeness": "full"}, facts, "x.md", "X",
                                     {f["id"]: f for f in facts})
        validate_openapi(doc)
        schema = doc["paths"]["/health"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
        self.assertEqual(schema, {"type": "boolean"})
        self.assertIn("| GET | /health | (không có) | (không có) | boolean |", text)


class AuditFixes(unittest.TestCase):
    """Regressions for the Codex gpt-6-astra audit of 07/10/2026 (F-numbers are the audit's)."""

    def fixture(self):
        snap, sources = snapshot.take(FIX)
        tools = SourceTools(snap, sources)
        for p in READABLE:
            tools.read_file(p)
        return tools

    def test_f01_annotated_secret_is_masked(self):
        tools = tools_for({"s.py": 'class S:\n    password: str = "audit_dummy_secret"\n    SECRET_KEY: str = "k-123456"\n'})
        text = tools.read_file("s.py")["text"]
        self.assertNotIn("audit_dummy_secret", text)
        self.assertNotIn("k-123456", text)

    def test_f02_rejected_items_do_not_keep_values(self):
        claims = Claims(self.fixture())
        claims.submit({"http_calls": [{"at": "app/api/items.py:11", "library": "httpx", "method": "POST",
                                       "target": {"kind": "literal", "value": "https://alice:audit_dummy_secret@example.com"}}]})
        self.assertNotIn("audit_dummy_secret", json.dumps(claims.rejected))

    def test_f03_resubmission_replaces_and_empty_prefix_is_refused(self):
        claims = Claims(self.fixture())
        wrong = dict(CREATE, path_parts=[dict(CHAIN[0], value="")] + CHAIN[1:] + [CREATE["path_parts"][-1]])
        self.assertEqual(claims.submit({"routes": [wrong]})["accepted"], 0)
        swapped = dict(CREATE, status={"codes": [201], "at": "app/api/items.py:9", "rule": None})
        claims.submit({"routes": [CREATE]})
        claims.submit({"routes": [swapped]})
        self.assertEqual(len(claims.routes), 1)

    def test_f04_path_parameter_must_be_required(self):
        bad = dict(READ, params=[dict(READ["params"][0], required=False), READ["params"][1]])
        self.assertEqual(Claims(self.fixture()).submit({"routes": [bad]})["accepted"], 0)

    def test_f14_wrong_types_are_errors_not_crashes(self):
        res = Claims(self.fixture()).submit({"limitations": [{"kind": []}], "file_roles": [{"file": "app/main.py", "role": []}]})
        self.assertEqual(res["accepted"], 0)
        self.assertEqual(len(res["errors"]), 2)

    def test_f11_duplicate_components_are_refused(self):
        snap, _ = snapshot.take(FIX)
        groups = json.loads(MEMBERSHIP.read_text(encoding="utf-8"))
        groups["components"][1]["name"] = groups["components"][0]["name"]
        with self.assertRaises(docpipeline.InputError):
            docpipeline.load_components(groups, snap, "unit:x")

    def test_f18_responses_retry_does_not_double_tool_outputs(self):
        import os
        from l3slice.docagent import TOOL_SPECS, ResponsesProvider
        os.environ["FR029_TEST_KEY"] = "x"
        self.addCleanup(os.environ.pop, "FR029_TEST_KEY")
        p = ResponsesProvider("https://api.openai.com/v1", "m", "FR029_TEST_KEY")
        sent, replies = [], [{"output": [{"type": "function_call", "call_id": "c1", "name": "list_files", "arguments": "{}"}]},
                             ProviderError("HTTP 500", True), {"output": []}]

        def post(payload):
            sent.append(json.loads(json.dumps(payload)))
            r = replies.pop(0)
            if isinstance(r, Exception):
                raise r
            return r
        p._post = post
        msgs = [{"role": "system", "content": "S"}, {"role": "user", "content": "U"}]
        p.chat(msgs, TOOL_SPECS)
        msgs += [{"role": "assistant", "content": ""}, {"role": "tool", "tool_call_id": "c1", "content": "{}"}]
        with self.assertRaises(ProviderError):
            p.chat(msgs, TOOL_SPECS)
        p.chat(msgs, TOOL_SPECS)
        outputs = [x for x in sent[-1]["input"] if x.get("type") == "function_call_output"]
        self.assertEqual(len(outputs), 1)

    def test_f19_cost_cap_needs_prices(self):
        import os
        from l3slice.docagent import OpenAICompatProvider
        os.environ["FR029_TEST_KEY"] = "x"
        self.addCleanup(os.environ.pop, "FR029_TEST_KEY")
        tools = self.fixture()
        run = run_agent(tools, Claims(tools), [], OpenAICompatProvider("http://unused", "m", "FR029_TEST_KEY"),
                        Budget(max_cost_usd=0.1))
        self.assertEqual(run.status, "failed")
        self.assertIn("COST_CAP_WITHOUT_PRICES", run.reason)

    def test_f20_non_empty_output_is_refused_before_the_model(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        out = Path(t.name) / "out"
        out.mkdir()
        (out / "x.txt").write_text("x", encoding="utf-8")
        provider = ScriptedProvider([[("list_files", {})]])
        with self.assertRaises(docpipeline.InputError):
            docpipeline.run_documents(FIX, out, MEMBERSHIP, "x", provider)
        self.assertEqual(provider.seen, [])


class Scorer(unittest.TestCase):
    def test_perfect_then_each_kind_of_error_is_counted(self):
        sys.path.insert(0, str(HERE.parent / "tools"))
        import fr029_score
        t, _, bundle = run(ScriptedProvider(script(bad=False)))
        self.addCleanup(t.cleanup)
        result = {k: v for k, v in bundle.items() if k != "artifacts"}  # same content as result.json
        gold = json.loads((HERE / "fixtures" / "fr029_e2e.gold.json").read_text(encoding="utf-8"))
        rep = fr029_score.score(result, gold)
        for kind in ("routes", "models", "http_calls", "file_roles", "limitations"):
            with self.subTest(kind):
                self.assertEqual((rep[kind]["fp"], rep[kind]["fn"]), (0, 0))
                self.assertTrue(all(not a["wrong"] for a in rep[kind]["attributes"].values()), rep[kind]["attributes"])
        self.assertTrue(rep["out_of_scope"]["ok"])
        gold["routes"][1]["path"] = "/v1/api/items/{item_id}"
        gold["routes"][0]["status"] = [200]
        gold["models"][1]["fields"][1]["required"] = True
        gold["http_calls"][0]["method"] = "GET"
        gold["file_roles"][3]["role"] = "Service"
        rep = fr029_score.score(result, gold)
        self.assertEqual((rep["routes"]["fp"], rep["routes"]["fn"]), (1, 1))
        self.assertEqual(len(rep["routes"]["attributes"]["status"]["wrong"]), 1)
        self.assertEqual(len(rep["models"]["attributes"]["fields"]["wrong"]), 1)
        self.assertEqual(len(rep["http_calls"]["attributes"]["method"]["wrong"]), 1)
        self.assertEqual(len(rep["file_roles"]["attributes"]["role"]["wrong"]), 1)


class EmbeddedBody(unittest.TestCase):
    def test_embedded_and_form_bodies_render_inline(self):
        src = ("from fastapi import FastAPI, Body, Form\nfrom pydantic import BaseModel\n\n\nclass Tag(BaseModel):\n"
               "    label: str\n\n\napp = FastAPI()\n\n\n@app.put('/t')\ndef put(tag: Tag = Body(embed=True)):\n    pass\n\n\n"
               "@app.post('/login')\ndef login(user: str = Form(), pw: str = Form()):\n    pass\n")
        tools = tools_for({"m.py": src})
        tools.read_file("m.py")
        claims = Claims(tools)
        base = {"application": "m.py:9", "params": [], "response": None,
                "status": {"codes": [200], "rule": "fastapi.default_status_200"}, "dependencies": [], "auth": {"unknown": "chưa rõ"}}
        res = claims.submit({
            "models": [{"id": "m.py::Tag", "at": "m.py:5", "fields": [
                {"name": "label", "alias": None, "type": "string", "required": True, "nullable": False, "at": "m.py:6"}]}],
            "routes": [dict(base, method="PUT", handler="m.py::put", decorator="m.py:12-13",
                            path_parts=[{"kind": "decorator", "value": "/t", "at": "m.py:12"}],
                            request_body={"models": ["m.py::Tag"], "media_type": "application/json", "required": True,
                                          "embedded": True, "at": "m.py:13",
                                          "fields": [{"name": "tag", "type": "m.py::Tag", "required": True, "at": "m.py:13"}]}),
                       dict(base, method="POST", handler="m.py::login", decorator="m.py:17-18",
                            path_parts=[{"kind": "decorator", "value": "/login", "at": "m.py:17"}],
                            request_body={"models": [], "media_type": "application/x-www-form-urlencoded", "required": True,
                                          "embedded": False, "at": "m.py:18",
                                          "fields": [{"name": "user", "type": "string", "required": True, "at": "m.py:18"},
                                                     {"name": "pw", "type": "string", "required": True, "at": "m.py:18"}]})]})
        self.assertEqual(res["errors"], [])
        from l3slice.docfacts import build_facts
        from l3slice.render import render_api
        facts = build_facts(claims, {"snapshot_id": tools.snapshot_id, "files": list(tools.files.values())}, "unit:x")
        by_id = {f["id"]: f for f in facts}
        routes = [f for f in facts if f["kind"] == "route"]
        text, doc, _, _ = render_api({"confidence": "exact", "completeness": "full"}, routes, "x.md", "X", by_id)
        validate_openapi(doc)
        put = doc["paths"]["/t"]["put"]["requestBody"]["content"]["application/json"]["schema"]
        self.assertEqual(list(put["properties"]), ["tag"])
        self.assertIn("$ref", put["properties"]["tag"])
        form = doc["paths"]["/login"]["post"]["requestBody"]["content"]["application/x-www-form-urlencoded"]["schema"]
        self.assertEqual(form["required"], ["pw", "user"])


class OneShot(unittest.TestCase):
    """Chế độ đọc một lần: toàn bộ source trong request đầu, các request sau chỉ mang lỗi; checkpoint để chạy tiếp."""

    def setUp(self):
        from l3slice.docagent import run_oneshot
        self.run_oneshot = run_oneshot
        self.components = json.loads(MEMBERSHIP.read_text(encoding="utf-8"))["components"]
        snap, sources = snapshot.take(FIX)
        self.tools = SourceTools(snap, sources)
        self.claims = Claims(self.tools)

    def test_whole_source_once_then_only_the_refusals(self):
        provider = ScriptedProvider([[("submit_findings", BAD)], [("submit_findings", FINDINGS)]])
        run = self.run_oneshot(self.tools, self.claims, self.components, provider)
        self.assertEqual((run.status, run.mode, len(run.requests)), ("completed", "oneshot", 2))
        first = provider.seen[0]["content"]
        for p in READABLE:
            self.assertIn(f"=== {p} (", first)
        self.assertIn("    9| @router.post(", first)
        self.assertTrue(self.tools.coverage()["complete"])
        self.assertIn("FILES THAT NEED A ROLE (4):\napp/api/__init__.py\napp/api/items.py\napp/main.py\napp/schemas.py", first)
        repair = json.loads(provider.seen[1]["content"])  # the second request adds only the note after the refusal
        self.assertEqual(repair["refused"], 1)
        self.assertIn("note", repair)
        self.assertEqual([r["refused"] for r in run.requests], [1, 0])

    def test_repair_rounds_are_capped(self):
        seen = []
        provider = ScriptedProvider([[("submit_findings", BAD)],
                                     lambda msgs: (seen.append(json.loads(msgs[-2]["content"])), [("submit_findings", BAD)])[1]])
        run = self.run_oneshot(self.tools, self.claims, self.components, provider, Budget(max_repair_rounds=1))
        self.assertEqual(seen[0]["errors"][0]["what"], "POST app/api/items.py::create_item")
        self.assertIn("app/main.py:6-6", seen[0]["errors"][0]["source"])  # the cited prefix line, as the model saw it
        self.assertEqual(run.status, "partial")
        self.assertIn("REPAIR_ROUNDS", run.reason)
        self.assertEqual(len(provider.seen), 2)
        self.assertTrue(run.open_problems)

    def test_too_large_source_sends_nothing(self):
        provider = ScriptedProvider([[("submit_findings", FINDINGS)]])
        run = self.run_oneshot(self.tools, self.claims, self.components, provider, Budget(max_context_chars=100))
        self.assertEqual(run.status, "failed")
        self.assertIn("SOURCE_TOO_LARGE", run.reason)
        self.assertEqual(provider.seen, [])

    def test_checkpoint_resumes_and_rechecks_saved_items(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        ck = Path(t.name) / "checkpoint.json"
        part = dict(FINDINGS, routes=[CREATE])  # READ is missing: its decorator is an open problem
        run = self.run_oneshot(self.tools, self.claims, self.components,
                               ScriptedProvider([[("submit_findings", part)], ProviderError("HTTP 500", False)]),
                               checkpoint=ck)
        self.assertEqual(run.status, "partial")
        self.assertEqual(json.loads(ck.read_text(encoding="utf-8"))["requests"][0]["accepted"], 10)
        snap, sources = snapshot.take(FIX)
        tools = SourceTools(snap, sources)
        claims = Claims(tools)
        provider = ScriptedProvider([[("submit_findings", {"routes": [READ]})]])
        run = self.run_oneshot(tools, claims, self.components, provider, checkpoint=ck)
        self.assertEqual((run.status, len(run.requests), len(provider.seen)), ("completed", 2, 1))
        self.assertEqual((len(claims.routes), len(claims.models)), (2, 3))  # saved items went through the checker again
        self.assertEqual(claims.rejected, [])

    def test_pipeline_records_mode_and_requests(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        bundle = docpipeline.run_documents(FIX, Path(t.name) / "out", MEMBERSHIP, "fr029-e2e",
                                           ScriptedProvider([[("submit_findings", FINDINGS)]]), mode="oneshot")
        self.assertEqual((bundle["agent"]["mode"], bundle["agent"]["status"]), ("oneshot", "completed"))
        self.assertEqual(bundle["provenance"]["prompt_version"], "fr029-oneshot-prompt-v6")
        self.assertEqual(len(bundle["agent"]["requests"]), 1)

    def test_forced_tool_and_cached_tokens_on_the_wire(self):
        import os
        from l3slice.docagent import SUBMIT_SPEC, OpenAICompatProvider
        os.environ["FR029_TEST_KEY"] = "x"
        self.addCleanup(os.environ.pop, "FR029_TEST_KEY")
        p = OpenAICompatProvider("https://api.openai.com/v1", "m", "FR029_TEST_KEY", prices=(1.0, 0.1, 2.0))
        sent = []

        class Resp:
            def __init__(self, req):
                sent.append(json.loads(req.data))

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return json.dumps({"choices": [{"message": {"tool_calls": [{"id": "c1", "function": {
                    "name": "submit_findings", "arguments": "{}"}}]}, "finish_reason": "tool_calls"}],
                    "usage": {"prompt_tokens": 100, "prompt_tokens_details": {"cached_tokens": 40},
                              "completion_tokens": 10}}).encode()
        with mock.patch("urllib.request.urlopen", lambda req, timeout=None: Resp(req)):
            r = p.chat([{"role": "user", "content": "U"}], [SUBMIT_SPEC], tool_choice="submit_findings")
        self.assertEqual(sent[0]["tool_choice"], {"type": "function", "function": {"name": "submit_findings"}})
        self.assertEqual(r["usage"], {"input": 100, "output": 10, "cached": 40})
        self.assertAlmostEqual(p.cost_usd, (60 * 1.0 + 40 * 0.1 + 10 * 2.0) / 1e6)


if __name__ == "__main__":
    unittest.main()
