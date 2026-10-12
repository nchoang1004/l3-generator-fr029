"""Exercise the local UI HTTP boundary and real FR-029 pipeline without network model calls."""
import http.client
import json
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from l3slice.docagent import ScriptedProvider
from l3slice.docweb import DocumentService, NOTICE, make_server
from test_docagent import FIX, MEMBERSHIP, script


class DocumentWebTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.service = DocumentService(self.tmp.name, lambda: ScriptedProvider(script(bad=False)), model="scripted", offline=True)
        self.server = make_server(self.service, 0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.body = {"source": str(FIX), "membership": str(MEMBERSHIP), "notice_version": NOTICE}

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.tmp.cleanup()

    def request(self, path, method="GET", body=None, headers=None):
        h = {"Content-Type": "application/json", "X-L3GEN-Client": "web-v1"}
        h.update(headers or {})
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=5)
        conn.request(method, path, json.dumps(body).encode() if body is not None else None, h)
        response = conn.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        conn.close()
        return result

    def finished(self, run_id):
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            status, _, raw = self.request("/api/runs/" + run_id)
            self.assertEqual(status, 200)
            run = json.loads(raw)
            if run["status"] != "running":
                return run
            time.sleep(.01)
        self.fail("Run did not finish")

    def start(self):
        status, _, raw = self.request("/api/runs", "POST", self.body)
        self.assertEqual(status, 202, raw)
        return json.loads(raw)["run_id"]

    def test_real_pipeline_download_and_reload(self):
        run_id = self.start()
        run = self.finished(run_id)
        self.assertEqual(run["status"], "finished", run)
        self.assertEqual(run["result"]["agent"]["status"], "completed")
        self.assertTrue(run["result"]["coverage"]["complete"])
        self.assertEqual(run["result"]["architecture_parity"]["status"], "not_evaluated")
        self.assertIn("DIAGRAM_NOT_PROVIDED", {x["code"] for x in run["result"]["limitations"]})
        self.assertGreater(run["turns"], 0)
        for art in run["result"]["artifacts"]:
            status, headers, data = self.request(f"/api/runs/{run_id}/artifacts/{quote(art['artifact_id'], safe='')}")
            self.assertEqual(status, 200)
            self.assertIn("attachment", headers["Content-Disposition"])
            self.assertEqual(data, (Path(run["output_directory"]) / art["path"]).read_bytes())
        _, _, raw = self.request("/api/runs")
        self.assertEqual(json.loads(raw)[0]["run_id"], run_id)
        self.assertNotIn("result", json.loads(raw)[0])

    def test_static_assets_and_script_config(self):
        for path in ("/", "/ui/app.js", "/ui/app.css"):
            status, headers, data = self.request(path)
            self.assertEqual(status, 200)
            self.assertIn("default-src 'none'", headers["Content-Security-Policy"])
            self.assertTrue(data)
        status, _, data = self.request("/api/config")
        self.assertEqual(status, 200)
        self.assertTrue(json.loads(data)["offline"])
        self.assertNotIn("key", json.loads(data))

    def test_csrf_and_dns_rebinding_rejected(self):
        for headers in ({"Origin": "https://outside.example"}, {"Host": "outside.example"}, {"X-L3GEN-Client": "wrong"}):
            self.assertEqual(self.request("/api/runs", "POST", self.body, headers)[0], 403)
        self.assertEqual(self.request("/api/config", headers={"Origin": "https://outside.example"})[0], 403)
        self.assertEqual(self.service.view(), [])

    def test_invalid_paths_notice_and_fields(self):
        for update in ({"source": "relative"}, {"membership": "missing"}, {"notice_version": ""}, {"key": "never accepted"}, {"name": [1]}):
            with self.subTest(update=update):
                self.assertEqual(self.request("/api/runs", "POST", dict(self.body, **update))[0], 422)
        self.assertEqual(self.service.view(), [])

    def test_source_output_overlap(self):
        for workdir in (FIX, FIX / "out", FIX.parent):
            self.service.workdir = workdir
            self.assertEqual(self.request("/api/runs", "POST", self.body)[0], 422)

    def test_failed_input_and_recovery(self):
        membership = Path(self.tmp.name) / "bad.json"
        membership.write_text('{"components": []}', encoding="utf-8")
        self.body["membership"] = str(membership)
        run = self.finished(self.start())
        self.assertEqual(run["status"], "failed")
        self.assertNotIn("result", run)
        self.body["membership"] = str(MEMBERSHIP)
        self.assertEqual(self.finished(self.start())["status"], "finished")

    def test_partial_agent_is_not_presented_as_complete(self):
        self.service.factory = lambda: ScriptedProvider([])
        run = self.finished(self.start())
        self.assertEqual(run["status"], "finished")
        self.assertNotEqual(run["result"]["agent"]["status"], "completed")
        self.assertFalse(run["result"]["coverage"]["complete"])

    def test_one_active_run(self):
        entered, release = threading.Event(), threading.Event()
        def factory():
            entered.set()
            release.wait(5)
            return ScriptedProvider(script(bad=False))
        self.service.factory = factory
        run_id = self.start()
        try:
            self.assertTrue(entered.wait(2))
            self.assertEqual(self.request("/api/runs", "POST", self.body)[0], 409)
        finally:
            release.set()
        self.assertEqual(self.finished(run_id)["status"], "finished")

    def test_offline_script_offers_only_agent_mode(self):
        self.assertEqual(json.loads(self.request("/api/config")[2])["modes"], ["agent"])
        for mode in ("oneshot", "fast", 1):
            with self.subTest(mode=mode):
                self.assertEqual(self.request("/api/runs", "POST", dict(self.body, mode=mode))[0], 422)
        self.assertEqual(self.service.view(), [])

    def test_oneshot_mode_reaches_the_pipeline_with_a_checkpoint(self):
        seen = {}

        def fake_run(source, output, membership, name, provider, archdia, diagram, budget, run_id, mode="agent", checkpoint=None):
            seen.update(mode=mode, checkpoint=checkpoint, output=output)
            provider.chat([], [], tool_choice="submit_findings")  # oneshot forces one tool
            return {"agent": {"mode": mode}}

        class Provider:
            def chat(self, messages, tools, tool_choice=None):
                seen["tool_choice"] = tool_choice

        self.service.config["offline"] = False
        self.service.config["modes"] = ["agent", "oneshot"]
        self.service.factory = Provider
        with mock.patch("l3slice.docweb.run_documents", fake_run):
            run = self.finished(self.start_with(mode="oneshot"))
        self.assertEqual(run["status"], "finished", run)
        self.assertEqual(run["mode"], "oneshot")
        self.assertEqual(seen["mode"], "oneshot")
        self.assertEqual(seen["tool_choice"], "submit_findings")
        self.assertNotEqual(seen["checkpoint"].parent, seen["output"])  # outside the fresh output directory
        self.assertEqual(seen["checkpoint"].parent, Path(self.tmp.name).resolve())

    def test_cost_cap_needs_prices_and_reaches_the_budget(self):
        from l3slice import docweb
        with self.assertRaises(SystemExit):
            docweb.main(["--workdir", self.tmp.name, "--script", str(FIX / "x"), "--max-cost-usd", "0.3"])
        with mock.patch.object(docweb, "make_server", side_effect=RuntimeError("stop")) as made,                 mock.patch.dict("os.environ", {"K": "x"}):
            with self.assertRaises(RuntimeError):
                docweb.main(["--workdir", self.tmp.name, "--base-url", "https://api.example/v1", "--model", "m",
                             "--key-env", "K", "--prices", "1.25,0.125,10", "--max-cost-usd", "0.35", "--timeout", "600"])
            service = made.call_args.args[0]
            self.assertEqual(service.budget.max_cost_usd, 0.35)
            self.assertEqual(service.factory().prices, (1.25, 0.125, 10.0))
            self.assertEqual(service.factory().timeout, 600)

    def test_missing_workdir_is_created_and_oneshot_checkpoint_is_writable(self):
        workdir = Path(self.tmp.name) / "not" / "yet" / "there"
        service = DocumentService(workdir, lambda: ScriptedProvider(script(bad=False)), model="m", offline=False)
        self.assertTrue(workdir.is_dir())
        seen = {}

        def fake_run(*args, mode="agent", checkpoint=None, **kw):
            checkpoint.write_text("{}", encoding="utf-8")  # what run_oneshot does first
            seen["ok"] = True
            return {"agent": {"mode": mode}}

        with mock.patch("l3slice.docweb.run_documents", fake_run):
            view = service.submit(dict(self.body, mode="oneshot"))
            deadline = time.monotonic() + 5
            while service.view(view["run_id"])["status"] == "running" and time.monotonic() < deadline:
                time.sleep(.01)
        self.assertEqual(service.view(view["run_id"])["status"], "finished")
        self.assertTrue(seen["ok"])

    def start_with(self, **fields):
        status, _, raw = self.request("/api/runs", "POST", dict(self.body, **fields))
        self.assertEqual(status, 202, raw)
        return json.loads(raw)["run_id"]

    def test_unknown_artifact_and_traversal(self):
        run_id = self.start()
        self.finished(run_id)
        for path in ("/ui/../docweb.py", "/ui/%2e%2e/docweb.py", "/api/runs/unknown",
                     f"/api/runs/{run_id}/artifacts/%2e%2e%2fresult.json"):
            self.assertEqual(self.request(path)[0], 404)


if __name__ == "__main__":
    unittest.main()
