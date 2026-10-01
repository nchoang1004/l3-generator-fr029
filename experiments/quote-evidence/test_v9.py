"""Offline tests for v9.py with a fake model: every answer of the model is checked by code."""
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import calls     # noqa: E402
import cluster   # noqa: E402
import flow      # noqa: E402
import graph     # noqa: E402
import inventory  # noqa: E402
import pyindex   # noqa: E402
import v9        # noqa: E402
from test_ai7 import FILES  # noqa: E402


class Fake:
    """Answers per step from `answers` (a function of the user text), records each request."""

    def __init__(self, answers):
        self.answers, self.calls, self.reasoning, self.model = answers, [], {}, "fake"

    def json(self, system, user, schema, *, step, max_tokens, effort="medium"):
        self.calls.append({"step": step, "user": user, "schema": schema, "total_tokens": 0, "cached": True})
        make = self.answers.get(step.split("-")[0])
        return make(user) if make else {}


class V9Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        for rel, text in FILES.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text, encoding="utf-8")
        self.root = root
        self.idx = pyindex.index(root, inventory.scan(root))

    def tearDown(self):
        self.tmp.cleanup()

    def test_library_roles_keep_only_names_the_repository_calls(self):
        fake = Fake({"libs": lambda u: {"libraries": [
            {"library": "sqlalchemy", "role": "database", "opens": ["create_async_engine", "invented_name"]},
            {"library": "httpx", "role": "http", "opens": []},
            {"library": "fastapi", "role": "none", "opens": []}]}})
        roles = v9.library_roles(fake, self.idx, [])
        self.assertEqual(roles["io"]["sqlalchemy"], ("database", {"create_async_engine"}))
        self.assertEqual(roles["io"]["httpx"], ("http", None))          # empty opens: any call talks to it
        self.assertNotIn("fastapi", roles["io"])
        facts = calls.facts(self.idx, roles)
        self.assertEqual(facts["app/db.py"]["sure"]["infra"], [3, "sqlalchemy.create_async_engine"])
        self.assertEqual(facts["app/clients/pay.py"]["io"][0][2], "http")

    def test_no_library_answer_means_no_io(self):
        roles = v9.library_roles(Fake({}), self.idx, [])
        facts = calls.facts(self.idx, roles)
        self.assertFalse(any(f["io"] for f in facts.values()))

    def test_summary_line_is_checked_and_a_sure_sign_wins(self):
        facts = calls.facts(self.idx)
        an = flow.analyze(self.idx, facts)
        files = graph.content_files(self.idx)
        module = cluster.modules(self.idx, an, files)

        def answer(user):
            names = re.findall(r"^### (\S+)", user, re.M)
            return {"files": [{"file": p, "summary": "does things", "layer": "service",
                               "line": 999 if p == "app/crud.py" else 1} for p in names]}
        issues = []
        summ = v9.summaries(Fake({"sum": answer}), self.idx, an, files, module, issues)
        self.assertIsNone(summ["app/crud.py"]["quote"])                 # line 999 does not exist
        self.assertEqual(summ["app/models.py"]["quote"]["line"], 1)
        self.assertEqual(v9.file_layer(an, summ, "app/models.py"), "data")     # __tablename__ is sure
        self.assertEqual(v9.file_layer(an, summ, "app/service/user.py"), "service")

    def test_assemble_places_every_unit_once(self):
        an = flow.analyze(self.idx, calls.facts(self.idx))
        units = {"U1": ["app/main.py"], "U2": ["app/api/users.py"], "U3": ["app/constants.py"], "U4": ["app/crud.py"]}
        ulayer = {"U1": "entry", "U2": "api", "U3": "shared", "U4": "data"}
        fake = Fake({"assemble": lambda u: {"blocks": [{"name": "Web App", "layer": "entry", "units": ["U1"]},
                                                       {"name": "routes", "layer": "api", "units": ["U2", "U1"]}],
                                            "shared": ["U3"]}})
        blocks, layer, shared = v9.assemble(fake, an, {}, units, ulayer, issues := [])
        self.assertEqual(blocks["web_app"], ["app/main.py"])
        self.assertEqual(blocks["routes"], ["app/api/users.py"])        # U1 already placed: not twice
        self.assertEqual(shared, ["app/constants.py"])
        self.assertIn(["app/crud.py"], blocks.values())                 # left out: a block of its own
        self.assertTrue(any("left out" in i for i in issues))

    def test_refine_applies_only_answers_with_a_shown_line(self):
        facts = calls.facts(self.idx)
        an = flow.analyze(self.idx, facts)
        files = graph.content_files(self.idx)
        link = cluster.links(self.idx, an, files)
        blocks = {"app": ["app/main.py"], "mixed": ["app/api/users.py", "app/models.py", "app/crud.py"]}
        layer = {"app": "entry", "mixed": "api"}

        def answer(user):
            ids = re.findall(r"\[(L\d+)\]", user)
            q = re.search(r"^(Q\d+) split block mixed", user, re.M).group(1)
            return {"answers": [{"id": q, "action": "apply", "target": "", "reason": ids[-1]}]}
        log = v9.refine(Fake({"refine": answer}), self.idx, an, {}, link, blocks, layer, [], [])
        self.assertEqual(blocks["mixed"], ["app/api/users.py", "app/crud.py"])
        self.assertEqual(blocks["mixed_data"], ["app/models.py"])
        self.assertTrue(log and log[0]["reason"])

        blocks = {"app": ["app/main.py"], "mixed": ["app/api/users.py", "app/models.py"]}
        layer = {"app": "entry", "mixed": "api"}
        bad = Fake({"refine": lambda u: {"answers": [{"id": "Q1", "action": "apply", "target": "", "reason": "L999"}]}})
        v9.refine(bad, self.idx, an, {}, link, blocks, layer, [], [])
        self.assertEqual(blocks["mixed"], ["app/api/users.py", "app/models.py"])

    def test_dry_run_sends_every_step(self):
        est = v9.Estimate()
        v9.pipeline(est, self.root)
        steps = {c["step"].split("-")[0] for c in est.calls}
        self.assertTrue({"libs", "sum", "assemble"} <= steps)


if __name__ == "__main__":
    unittest.main()
