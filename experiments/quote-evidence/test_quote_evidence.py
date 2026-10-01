import json
import re
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ai          # noqa: E402
import evaluate    # noqa: E402
import graph       # noqa: E402
import inventory   # noqa: E402
import llm         # noqa: E402
import pyindex     # noqa: E402
import run         # noqa: E402
import verify      # noqa: E402

FILES = {
    "pkg/__init__.py": "",
    "pkg/main.py": "from pkg.api import routes\nfrom pkg.core.config import settings\n\napp = make_app()\n"
                   "app.include(routes.router)\n",
    "pkg/api/__init__.py": "",
    "pkg/api/routes.py": "from ..services import place_order\nfrom pkg.models import Order\n\nrouter = Router()\n\n\n"
                         "@router.post('/orders')\ndef create(o: Order):\n    return place_order(o)\n",
    "pkg/services/__init__.py": "from .orders import place_order\n",
    "pkg/services/orders.py": "import httpx\nfrom pkg.models import Order\nfrom pkg.core import config\n\n\n"
                              "def place_order(o: Order):\n    client = httpx.Client(base_url=config.settings.PAY_URL)\n"
                              "    return client.post('/pay')\n",
    "pkg/models.py": "class Order:\n    pass\n",
    "pkg/core/__init__.py": "",
    "pkg/core/config.py": "class Settings:\n    PAY_URL: str = 'https://pay.example'\n    TOKEN: str = "
                          "'sk-abcdefghijklmnopqrstuvwx'\n\n\nsettings = Settings()\n",
    "pkg/core/logging.py": "def setup():\n    return 1\n",
    "pkg/core/audit.py": "import logging\n\n\ndef audit():\n    logging.info('x')\n",
    "tests/test_orders.py": "from pkg.models import Order\n",
}


class FakeLLM:
    """Answers like a model would, from the request text; the first role quote is deliberately wrong."""

    def __init__(self, grouping, drop_last_first_pass=False):
        self.grouping, self.calls, self.drop = grouping, [], drop_last_first_pass

    def json(self, system, user, schema, *, step, max_tokens):
        self.calls.append({"step": step, "total_tokens": 0, "user": user})
        if step == "group":
            return self.grouping
        if step == "review":
            return self.review
        rows, cur = [], None
        for line in user.splitlines():
            head = re.match(r"## (C\d+) ", line)
            edge = re.match(r"(E\d+) -> ", line)
            quote = re.match(r"(.+?):(\d+)\| (.*)", line)
            if head:
                cur = {"id": head[1], "name": "Khối " + head[1], "role": "Làm việc", "role_quote": None,
                       "edges": [], "externals": [], "_edge": None, "_conn": False}
                rows.append(cur)
            elif edge:
                uses = line.split("| uses ", 1)[-1]
                typed = "call" not in uses and ("annotation" in uses or "base" in uses)
                cur["_edge"], cur["_kind"] = edge[1], "type" if typed else "call"
            elif line == "connection lines:":
                cur["_conn"], cur["_edge"] = True, None
            elif quote and cur:
                q = {"file": quote[1], "line": int(quote[2]), "text": quote[3].strip()}
                if cur["role_quote"] is None:
                    cur["role_quote"] = q
                elif cur["_edge"] and not any(e["id"] == cur["_edge"] for e in cur["edges"]):
                    cur["edges"].append({"id": cur["_edge"], "kind": cur["_kind"], "label": "gọi", "quote": q})
                elif cur["_conn"] and not cur["externals"]:
                    cur["externals"].append({"system": "Pay API", "kind": "http_api", "label": "gửi thanh toán",
                                             "quote": q})
        if self.drop and step.startswith("describe"):
            rows = rows[:-1]
        if rows[0]["id"] == "C1":
            rows[0]["role_quote"] = {**rows[0]["role_quote"], "text": "invented line of code"}
        return {"components": [{k: v for k, v in r.items() if not k.startswith("_")} for r in rows]}


GROUPING = {"components": [
    {"key": "entry", "members": ["pkg/main.py"], "shared": False},
    {"key": "routes", "members": ["pkg/api/"], "shared": False},
    {"key": "services", "members": ["pkg/services/"], "shared": False},
    {"key": "models", "members": ["pkg/models.py"], "shared": False},
    {"key": "config", "members": ["pkg/core/config.py"], "shared": True},
]}


class QuoteEvidenceTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name) / "repo"
        for rel, text in FILES.items():
            (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.root / rel).write_text(text, encoding="utf-8")
        self.out = Path(tmp.name) / "out"
        self.snap = inventory.scan(self.root)
        self.idx = pyindex.index(self.root, self.snap)

    def imp(self, path, local):
        return next(r for r in self.idx[path]["imports"] if r["local"] == local)

    def test_scope_skips_tests(self):
        self.assertNotIn("tests/test_orders.py", self.snap["scope"])
        self.assertIn("pkg/services/orders.py", self.snap["scope"])

    def test_scope_keeps_scripts_that_import_own_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel, text in {"app/__init__.py": "", "app/db.py": "x = 1\n",
                              "scripts/seed.py": "import os\nfrom app.db import x\n",
                              "scripts/tool.py": "import os\nimport logging\n"}.items():
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_text(text, encoding="utf-8")
            snap = inventory.scan(root)
            self.assertIn("scripts/seed.py", snap["scope"])
            self.assertNotIn("scripts/tool.py", snap["scope"])

    def test_imports_resolve_relative_reexport_and_stdlib(self):
        self.assertEqual(self.imp("pkg/api/routes.py", "place_order")["target"], "pkg/services/orders.py")
        self.assertEqual(self.imp("pkg/main.py", "routes")["target"], "pkg/api/routes.py")
        audit = self.imp("pkg/core/audit.py", "logging")
        self.assertIsNone(audit["target"])            # stdlib, not the local pkg/core/logging.py
        self.assertEqual(audit["external"], "logging")
        self.assertEqual(self.imp("pkg/services/orders.py", "httpx")["external"], "httpx")

    def test_use_kinds(self):
        uses = self.idx["pkg/api/routes.py"]["uses"]
        self.assertEqual([k for _, k in uses["Order"]], ["annotation"])
        self.assertEqual([k for _, k in uses["place_order"]], ["call"])
        tree = pyindex.ast.parse("try:\n    f()\nexcept NotFound:\n    raise Gone('x')\nraise Missing\n")
        kinds = pyindex._use_kinds(tree)
        names = {n.id: kinds.get(id(n)) for n in pyindex.ast.walk(tree) if isinstance(n, pyindex.ast.Name)}
        self.assertEqual(names, {"f": "call", "NotFound": "except", "Gone": "raise", "Missing": "raise"})

    def test_quote_check(self):
        files = ["pkg/services/orders.py"]
        ok = {"file": files[0], "line": 7, "text": "httpx.Client(base_url=config.settings.PAY_URL)"}
        self.assertIsNone(verify.check(self.idx, ok, files, ["httpx"]))
        self.assertEqual(verify.check(self.idx, {**ok, "line": 6}, files), "text not on that line")
        self.assertEqual(verify.check(self.idx, {**ok, "text": "requests.get(url)"}, files), "text not on that line")
        self.assertEqual(verify.check(self.idx, {**ok, "line": 99}, files), "line out of range")
        self.assertEqual(verify.check(self.idx, {**ok, "file": "pkg/models.py"}, files), "file outside this component")
        self.assertEqual(verify.check(self.idx, {**ok, "text": "Client"}, files), "quote too short")
        self.assertEqual(verify.check(self.idx, ok, files, ["Order"]), "line does not use the related symbol")

    def test_secret_redacted_before_sending(self):
        shown = verify.show(self.idx, "pkg/core/config.py", 3)
        self.assertNotIn("sk-abcdefghijklmnopqrstuvwx", shown)
        self.assertIn("***", shown)

    def test_end_to_end_with_fake_model(self):
        fake = FakeLLM(GROUPING)
        summary = run.run(self.root, self.out, fake, None)
        data = json.loads((self.out / "graph.json").read_text(encoding="utf-8"))
        comps = {c["key"]: c for c in data["components"]}
        pairs = {(comps_id_key, t) for comps_id_key, t in
                 ((next(c["key"] for c in data["components"] if c["id"] == e["source"]),
                   next(c["key"] for c in data["components"] if c["id"] == e["target"])) for e in data["edges"])}
        self.assertIn(("entry", "routes"), pairs)
        self.assertIn(("routes", "services"), pairs)
        self.assertNotIn(("services", "config"), pairs)          # edges into shared support are never drawn
        self.assertEqual(comps["entry"]["role"], "")               # its invented quote was rejected
        self.assertTrue(any(r["reason"] == "text not on that line" for r in data["rejected"]))
        self.assertEqual([x["name"] for x in data["externals"]], ["Pay API"])
        self.assertTrue(any(c["key"] == "dir:pkg/core" for c in data["components"]))   # modules AI left out
        self.assertEqual(summary["status"], "partial")
        self.assertIn("flowchart LR", (self.out / "diagram.mmd").read_text(encoding="utf-8"))

    def test_component_left_out_is_retried(self):
        fake = FakeLLM(GROUPING, drop_last_first_pass=True)
        run.run(self.root, self.out, fake, None)
        data = json.loads((self.out / "graph.json").read_text(encoding="utf-8"))
        self.assertTrue(all(c["described"] for c in data["components"]))
        self.assertIn("retry-1", [c["step"] for c in fake.calls])

    def test_rejected_generation_salvaged_only_when_complete(self):
        self.assertEqual(llm._first_object('{"components": []}}'), {"components": []})
        self.assertIsNone(llm._first_object('{"components": [{"id": "C1"'))

    def test_broken_json_is_resent_once_with_the_parse_error(self):
        client = llm.Groq("test-key", budget=100_000, state=self.root.parent / "state")
        broken = {"error": {"message": "Failed to validate JSON. Please adjust your prompt.",
                            "failed_generation": '{"components": [1, 2 3]}'}}
        replies = [(400, {}, broken),
                   (200, {}, {"choices": [{"finish_reason": "stop", "message": {"content": '{"components": []}'}}],
                              "usage": {"total_tokens": 10}})]
        sent = []
        client._post = lambda body: (sent.append(body), replies[len(sent) - 1])[1]
        self.assertEqual(client.json("sys", "user", {"type": "object"}, step="s", max_tokens=100),
                         {"components": []})
        self.assertEqual(sent[1]["response_format"], sent[0]["response_format"])        # same strict schema
        self.assertEqual(sent[1]["messages"][0], sent[0]["messages"][0])
        self.assertTrue(sent[1]["messages"][1]["content"].startswith(
            "user\n\nYour previous answer was rejected: Expecting ',' delimiter at character 21: "
            "...{\"components\": [1, 2 3]}..."))
        self.assertEqual([r.get("mode") for r in client.calls], [None, "resent with the parse error"])
        again = client.json("sys", "user", {"type": "object"}, step="s", max_tokens=100)   # served from cache
        self.assertEqual((again, len(sent)), ({"components": []}, 2))
        client._post = lambda body: (sent.append(body), (400, {}, broken))[1]
        with self.assertRaises(llm.ModelError):                                           # resent once only
            client.json("sys", "other", {"type": "object"}, step="s", max_tokens=100)
        self.assertEqual(len(sent), 4)

    def test_network_failure_is_retried_and_costs_nothing(self):
        client = llm.Groq("test-key", budget=100_000, state=self.root.parent / "state3")
        replies = [(0, {}, {"error": {"message": "network: getaddrinfo failed"}}),
                   (200, {}, {"choices": [{"finish_reason": "stop", "message": {"content": '{"a": 1}'}}],
                              "usage": {"total_tokens": 7}})]
        sent = []
        client._post = lambda body: (sent.append(body), replies[len(sent) - 1])[1]
        with unittest.mock.patch("llm.time.sleep"):
            self.assertEqual(client.json("sys", "user", {"type": "object"}, step="s", max_tokens=100), {"a": 1})
        self.assertEqual((len(sent), client.spent()), (2, 7))

    def test_empty_generation_retries_with_low_reasoning(self):
        client = llm.Groq("test-key", budget=100_000, state=self.root.parent / "state4")
        empty = {"error": {"message": "Failed to validate JSON.", "code": "json_validate_failed", "failed_generation": ""}}
        replies = [(400, {}, empty), (200, {}, {"choices": [{"finish_reason": "stop", "message": {"content": '{"a": 1}'}}],
                                                "usage": {"total_tokens": 5}})]
        sent = []
        client._post = lambda body: (sent.append(body), replies[len(sent) - 1])[1]
        self.assertEqual(client.json("sys", "user", {"type": "object"}, step="s", max_tokens=100), {"a": 1})
        self.assertEqual([b["reasoning_effort"] for b in sent], ["medium", "low"])

    def test_openrouter_effort_sent_and_reasoning_kept(self):
        client = llm.Groq("test-key", budget=100_000, state=self.root.parent / "state5", url=llm.OPENROUTER_URL)
        reply = {"choices": [{"finish_reason": "stop", "message": {"content": '{"a": 1}', "reasoning": "why: x"}}],
                 "usage": {"total_tokens": 9, "completion_tokens_details": {"reasoning_tokens": 4}, "cost": 0.001}}
        sent = []
        client._post = lambda body: (sent.append(body), (200, {}, reply))[1]
        self.assertEqual(client.json("sys", "user", {"type": "object"}, step="top-1", max_tokens=100, effort="low"),
                         {"a": 1})
        self.assertEqual((sent[0]["reasoning"], "reasoning_effort" in sent[0]), ({"effort": "low"}, False))
        self.assertEqual((client.reasoning, client.calls[-1]["reasoning_tokens"]), ({"top-1": "why: x"}, 4))
        again = llm.Groq("test-key", budget=100_000, state=self.root.parent / "state5", url=llm.OPENROUTER_URL)
        again.json("sys", "user", {"type": "object"}, step="top-1", max_tokens=100, effort="low")   # from cache
        self.assertEqual((again.reasoning, len(sent)), ({"top-1": "why: x"}, 1))

    def test_gpt6_gets_no_temperature_but_an_effort(self):
        client = llm.Groq("test-key", budget=100_000, state=self.root.parent / "state6", url=llm.OPENROUTER_URL,
                          model="openai/gpt-6-luna")
        reply = {"choices": [{"finish_reason": "stop", "message": {"content": '{"a": 1}'}}], "usage": {"total_tokens": 3}}
        sent = []
        client._post = lambda body: (sent.append(body), (200, {}, reply))[1]
        client.json("sys", "user", {"type": "object"}, step="s", max_tokens=100, effort="low")
        self.assertEqual(("temperature" in sent[0], sent[0]["reasoning"]), (False, {"effort": "low"}))

    def test_body_of_blank_lines_is_a_network_failure_retried(self):
        client = llm.Groq("test-key", budget=100_000, state=self.root.parent / "state7", url=llm.OPENROUTER_URL)
        bodies = [b"\n" * 600, b'{"choices": [{"finish_reason": "stop", "message": {"content": "{\\"a\\": 3}"}}], '
                               b'"usage": {"total_tokens": 5}}']

        class Resp:
            status, headers = 200, {}

            def __init__(self, body):
                self.body = body

            def read(self):
                return self.body

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

        with unittest.mock.patch("llm.urllib.request.urlopen", lambda req, timeout: Resp(bodies.pop(0))), \
                unittest.mock.patch("llm.time.sleep"):
            self.assertEqual(client.json("sys", "user", {"type": "object"}, step="s", max_tokens=100), {"a": 3})
        self.assertEqual([c["status"] for c in client.calls], [0, 200])
        self.assertIn("the answer was not JSON (600 bytes)", client.calls[0]["error"])

    def test_answer_cut_by_length_is_asked_again_with_low_reasoning(self):
        client = llm.Groq("test-key", budget=100_000, state=self.root.parent / "state6", url=llm.OPENROUTER_URL)
        cut = {"choices": [{"finish_reason": "length", "message": {"content": ""}}], "usage": {"total_tokens": 100}}
        done = {"choices": [{"finish_reason": "stop", "message": {"content": '{"a": 2}'}}], "usage": {"total_tokens": 9}}
        replies, sent = [(200, {}, cut), (200, {}, done)], []
        client._post = lambda body: (sent.append(body), replies[len(sent) - 1])[1]
        self.assertEqual(client.json("sys", "user", {"type": "object"}, step="s", max_tokens=100), {"a": 2})
        self.assertEqual([b["reasoning"]["effort"] for b in sent], ["medium", "low"])
        self.assertEqual(client.calls[0]["note"], "cut by length; retry with low reasoning")

    def test_truncated_generation_is_not_salvaged_or_resent(self):
        client = llm.Groq("test-key", budget=100_000, state=self.root.parent / "state2")
        cut = {"error": {"message": "max completion tokens reached before generating a valid document",
                         "failed_generation": '{"components": [{"id": "C1"}]}'}}
        sent = []
        client._post = lambda body: (sent.append(body), (400, {}, cut))[1]
        with self.assertRaises(llm.ModelError):
            client.json("sys", "user", {"type": "object"}, step="s", max_tokens=100)
        self.assertEqual(len(sent), 1)

    def test_malformed_answer_rows_do_not_crash(self):
        comps, _ = graph.assemble(self.idx, GROUPING)
        edges = graph.candidates(self.idx, comps)
        answers = {r["id"]: r for r in map(ai._clean, [{"id": "C1", "edges": [{"id": "E1"}], "externals": "x"}, 5])
                   if r}
        result = ai.apply(self.idx, comps, edges, graph.connections(self.idx, comps), answers)
        self.assertTrue(result["edges"])                                     # rule still draws them
        self.assertTrue(all(e["label"] and e["quote"]["text"] for e in result["edges"]))
        self.assertEqual(result["quotes"]["valid"], 0)
        self.assertTrue(all(h["reason"] for h in result["hidden_edges"]))

    def test_external_must_quote_a_connection_line(self):
        comps, _ = graph.assemble(self.idx, GROUPING)
        edges, conns = graph.candidates(self.idx, comps), graph.connections(self.idx, comps)
        services = next(c for c in comps.values() if c["key"] == "services")
        self.assertIn(["pkg/services/orders.py", 7], conns[services["id"]])
        role = {"file": "pkg/services/orders.py", "line": 6, "text": "def place_order(o: Order):"}
        good = {"system": "Pay API", "kind": "http_api", "label": "gửi",
                "quote": {"file": "pkg/services/orders.py", "line": 7, "text": "httpx.Client(base_url"}}
        bad = {**good, "quote": role}          # real line, but not one that opens a connection
        for ext, count in ((good, 1), (bad, 0)):
            row = ai._clean({"id": services["id"], "name": "Dịch vụ", "role": "x", "role_quote": role,
                             "edges": [], "externals": [ext]})
            result = ai.apply(self.idx, comps, edges, conns, {services["id"]: row})
            self.assertEqual(len(result["externals"]), count)

    def test_drawn_edges_carry_both_ends_and_hidden_edges_a_reason(self):
        run.run(self.root, self.out, FakeLLM(GROUPING), None)
        data = json.loads((self.out / "graph.json").read_text(encoding="utf-8"))
        key = {c["id"]: c["key"] for c in data["components"]}
        drawn = {(key[e["source"]], key[e["target"]]): e for e in data["edges"]}
        self.assertEqual(drawn[("routes", "services")]["target_evidence"], [["pkg/services/orders.py", 6]])
        self.assertEqual(drawn[("routes", "services")]["label"], "gọi place_order")      # label made by code
        self.assertEqual(drawn[("routes", "models")]["label"], "dùng kiểu Order")         # rule draws it too
        self.assertEqual(drawn[("routes", "services")]["quote"]["text"], "return place_order(o)")
        hidden = {(key[h["source"]], key[h["target"]]): h["reason"] for h in data["hidden_edges"]}
        self.assertIn("SPEC", hidden[("services", "config")])
        self.assertEqual(set(hidden.values()), {"shared support is drawn without edges (SPEC)"})
        self.assertIn("total_s", data["meta"]["timing"])

    def test_existing_output_refused_by_cli_contract(self):
        self.out.mkdir()
        with self.assertRaises(FileExistsError):
            run.run(self.root, self.out, FakeLLM(GROUPING), None)

    def test_missed_init_joins_component_of_its_directory(self):
        (self.root / "pkg/services/billing.py").write_text("def bill():\n    return 1\n", encoding="utf-8")
        idx = pyindex.index(self.root, inventory.scan(self.root))
        grouping = {"components": [{"key": "billing", "members": ["pkg/services/billing.py"], "shared": False},
                                   {"key": "orders", "members": ["pkg/services/orders.py"], "shared": False},
                                   {"key": "config", "members": ["pkg/core/config.py"], "shared": True}]}
        comps, issues = graph.assemble(idx, grouping)
        owner = {p: c["key"] for c in comps.values() for p in c["files"]}
        self.assertEqual(owner["pkg/services/__init__.py"], "orders")  # the one it imports, not the first one
        self.assertEqual(owner["pkg/core/audit.py"], "dir:pkg/core")   # a missed module keeps its directory
        self.assertIn("1 files not grouped by AI; joined", issues[0])

    def test_grouping_problems(self):
        grouping = {"components": [{"key": "backend", "members": ["pkg/api/", "pkg/services/"], "shared": False},
                                   {"key": "entry", "members": ["pkg/main.py", "pkg/models.py"], "shared": True},
                                   {"key": "config", "members": ["pkg/core/"], "shared": True}]}
        comps, _ = graph.assemble(self.idx, grouping)
        found = graph.grouping_problems(self.idx, comps)
        self.assertEqual(found, {"C1": "mixes sub-directories that import each other: pkg/api/ imports pkg/services/"})
        # entry (pkg/ files) and config (one directory) span no sub-directories; shared flags are not checked

    def test_review_splits_flagged_component(self):
        grouping = {"components": [{"key": "entry", "members": ["pkg/main.py"], "shared": False},
                                   {"key": "backend", "members": ["pkg/api/", "pkg/services/"], "shared": False},
                                   {"key": "models", "members": ["pkg/models.py"], "shared": False},
                                   {"key": "config", "members": ["pkg/core/"], "shared": True}]}
        fake = FakeLLM(grouping)
        fake.review = {"fixes": [{"id": "C2", "action": "change", "reason": "routes and services",
                                  "components": [{"key": "routes", "members": ["pkg/api/", "pkg/models.py"],
                                                  "shared": False},
                                                 {"key": "services", "members": ["pkg/services/orders.py"],
                                                  "shared": False}]}]}
        run.run(self.root, self.out, fake, None)
        data = json.loads((self.out / "graph.json").read_text(encoding="utf-8"))
        owner = {p: c["key"] for c in data["components"] for p in c["files"]}
        self.assertEqual(owner["pkg/api/routes.py"], "routes")
        self.assertEqual(owner["pkg/models.py"], "models")              # not a file of the flagged component
        self.assertEqual(owner["pkg/services/__init__.py"], "services")  # left out by the fix: joins by directory
        self.assertIn("## C2 backend (not shared)", fake.calls[1]["user"])
        self.assertEqual(data["meta"]["review"]["problems"], {"C2": "mixes sub-directories that import each other: "
                                                                   "pkg/api/ imports pkg/services/"})
        key = {c["id"]: c["key"] for c in data["components"]}
        self.assertIn(("routes", "services"), {(key[e["source"]], key[e["target"]]) for e in data["edges"]})

    def test_review_keep_leaves_grouping(self):
        grouping = {"components": [{"key": "backend", "members": ["pkg/api/", "pkg/services/"], "shared": False}]}
        comps, _ = graph.assemble(self.idx, grouping)
        fake = FakeLLM(grouping)
        fake.review = {"fixes": [{"id": "C1", "action": "keep", "reason": "one feature", "components": []}]}
        revised, notes, issues = ai.review(fake, self.idx, grouping, comps, graph.grouping_problems(self.idx, comps))
        self.assertEqual((revised, issues), (grouping, []))
        self.assertEqual(notes, ["C1 backend kept: one feature"])

    def test_score(self):
        graph_data = {
            "components": [{"id": "C1", "name": "a", "files": ["pkg/main.py"]},
                           {"id": "C2", "name": "b", "files": ["pkg/api/routes.py"]},
                           {"id": "C3", "name": "c", "files": ["pkg/services/orders.py", "pkg/models.py"]}],
            "edges": [{"source": "C1", "target": "C2"}, {"source": "C2", "target": "C3"},
                      {"source": "C1", "target": "C3"}],
            "externals": [{"name": "Stripe API", "edges": [{"source": "C3"}]}],
            "quotes": {"returned": 4, "valid": 3},
            "file_lines": {"pkg/services/orders.py": 8, "pkg/models.py": 2}}
        oracle = {"components": {"entry": ["pkg/main.py"], "routes": ["pkg/api/"], "services": ["pkg/services/"],
                                 "models": ["pkg/models.py"]},
                  "externals": {"pay": ["stripe"]},
                  "required": [["entry", "routes"], ["routes", "services"], ["services", "ext:pay"],
                               ["services", "models"]],
                  "acceptable": [["entry", "services"]]}
        s = evaluate.score(graph_data, oracle)
        self.assertEqual(s["all"]["recall"], 0.75)          # services->models hidden inside one component
        self.assertEqual(s["all"]["precision"], 1.0)        # entry->services is acceptable, not counted
        self.assertEqual(s["all"]["precision_strict"], 0.75)  # ...unless acceptable counts as wrong
        self.assertEqual(s["external"]["recall"], 1.0)
        self.assertEqual(s["quote_validity"], 0.75)
        self.assertEqual(s["grouping_agreement"], 0.75)

    def test_comparisons_without_ai_steps(self):
        comps, _ = graph.assemble(self.idx, GROUPING)
        edges = graph.candidates(self.idx, comps)
        run_data = {"components": [{**c, "name": c["key"]} for c in comps.values()], "edges": [],
                    "externals": [], "quotes": {}, "file_lines": {}}
        oracle = {"components": {"entry": ["pkg/main.py"], "routes": ["pkg/api/"], "services": ["pkg/services/"],
                                 "models": ["pkg/models.py"], "core": ["pkg/core/"]},
                  "externals": {}, "required": [["entry", "routes"], ["routes", "services"]], "acceptable": []}
        c = evaluate.comparisons(self.idx, comps, edges, run_data, oracle)
        self.assertEqual(c["rule_edges"]["recall"], 1.0)
        self.assertEqual(c["no_ai"]["components"], 4)     # pkg/, pkg/api/, pkg/services/, pkg/core/


if __name__ == "__main__":
    unittest.main()
