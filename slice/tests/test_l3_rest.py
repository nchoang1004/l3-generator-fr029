"""Remaining L3 parts: GitHub intake (offline, fake transport), run budgets, CLI --json, local UI files."""
from __future__ import annotations

import http.client
import io
import json
import socket
import sys
import tempfile
import threading
import unittest
import zipfile
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import contracts  # noqa: E402
from l3slice import __main__ as cli, engine as engine_mod, github, web  # noqa: E402

FIX = HERE / "fixtures"
SHA = "a" * 40
PUBLIC = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("140.82.112.3", 443))]
PRIVATE = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.0.0.5", 443))]


def zipball(files, wrapper="acme-shop-aaaaaaa"):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr(wrapper + "/", b"")
        for rel, data in files.items():
            zf.writestr(f"{wrapper}/{rel}", data)
    return buf.getvalue()


def fake_github(responses):
    """responses: url -> (status, headers, body); records each URL asked."""
    asked = []

    def get(url, timeout):
        asked.append(url)
        return responses.get(url, (404, {}, b""))
    return get, asked


def standard(files, **override):
    base = {
        "https://api.github.com/repos/acme/shop": (200, {}, json.dumps({"default_branch": "main", "private": False}).encode()),
        "https://api.github.com/repos/acme/shop/commits/main": (200, {}, json.dumps({"sha": SHA}).encode()),
        f"https://api.github.com/repos/acme/shop/zipball/{SHA}": (302, {"Location": f"https://codeload.github.com/acme/shop/legacy.zip/{SHA}"}, b""),
        f"https://codeload.github.com/acme/shop/legacy.zip/{SHA}": (200, {}, zipball(files)),
    }
    base.update(override)
    return base


class GitHub(unittest.TestCase):
    FILES = {"app/main.py": b"x = 1\n", "README.md": b"#\n"}

    def take(self, responses, resolve=lambda *a, **k: PUBLIC, clock=None):
        get, asked = fake_github(responses)
        kwargs = {"get": get, "resolve": resolve}
        if clock:
            kwargs["clock"] = clock
        return github.take_github("https://github.com/acme/shop", "run_g", **kwargs), asked

    def refused(self, code, responses, **kw):
        with self.assertRaises(github.IntakeError) as e:
            self.take(responses, **kw)
        self.assertEqual(e.exception.code, code)
        contracts.validate(e.exception.payload, 2, "SnapshotError")

    def test_one_revision_and_wrapper_removed(self):
        (snap, sources, sha), asked = self.take(standard(self.FILES))
        self.assertEqual(sha, SHA)
        self.assertEqual(sorted(sources), ["app/main.py"])
        self.assertTrue(all(f"/{SHA}" in u for u in asked[2:]))  # archive of the resolved commit only
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "app").mkdir()
            (Path(t) / "app/main.py").write_bytes(b"x = 1\n")
            (Path(t) / "README.md").write_bytes(b"#\n")
            from l3slice import snapshot
            self.assertEqual(snapshot.take(Path(t))[0]["snapshot_id"], snap["snapshot_id"])

    def test_not_found_denied_and_bad_redirect(self):
        self.refused("GITHUB_NOT_FOUND_OR_PRIVATE", {})
        self.refused("GITHUB_ACCESS_DENIED", {"https://api.github.com/repos/acme/shop": (403, {}, b"")})
        evil = standard(self.FILES, **{f"https://api.github.com/repos/acme/shop/zipball/{SHA}":
                                       (302, {"Location": "https://evil.example/x.zip"}, b"")})
        self.refused("GITHUB_FETCH_FAILED", evil)
        plain = standard(self.FILES, **{f"https://api.github.com/repos/acme/shop/zipball/{SHA}":
                                        (302, {"Location": f"http://codeload.github.com/acme/shop/legacy.zip/{SHA}"}, b"")})
        self.refused("GITHUB_FETCH_FAILED", plain)

    def test_private_address_is_refused(self):
        self.refused("GITHUB_FETCH_FAILED", standard(self.FILES), resolve=lambda *a, **k: PRIVATE)

    def test_whole_operation_has_120_seconds(self):
        ticks = iter([0, 0, 50, 100, 130, 130, 130])
        self.refused("FETCH_TIMEOUT", standard(self.FILES), clock=lambda: next(ticks))

    def test_unsafe_entry_in_zipball_refused(self):
        self.refused("PATH_ESCAPE", standard({"../evil.py": b""}))

    def test_engine_runs_github_when_enabled(self):
        get, _ = fake_github(standard({"main.py": b"from fastapi import FastAPI\napp = FastAPI()\n"}))
        with tempfile.TemporaryDirectory() as t:
            eng = engine_mod.Engine(Path(t), partition=web.demo_partition, partition_note=web.DEMO_NOTE,
                                    github={"get": get, "resolve": lambda *a, **k: PUBLIC})
            run_id = eng.submit_github("https://github.com/acme/shop")["run_id"]
            eng.step()
            view = eng.view(run_id)
            contracts.validate_http(view, "RunView")
            rec = eng._load(run_id)
        self.assertEqual(view["state"], "partial")
        self.assertEqual(view["reasons"][0]["code"], "demo_partition")
        self.assertEqual(rec["source"]["commit"], SHA)

    def test_engine_without_github_answers_503(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(engine_mod.EngineError) as e:
                engine_mod.Engine(Path(t)).submit_github("https://github.com/acme/shop")
        self.assertEqual(e.exception.status, 503)


class Budgets(unittest.TestCase):
    def run_with(self, clock=None, memory=None):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("main.py", "from fastapi import FastAPI\napp = FastAPI()\n")
        with tempfile.TemporaryDirectory() as t:
            kwargs = {"partition": web.demo_partition}
            if clock:
                kwargs["clock"] = clock
            if memory:
                kwargs["memory"] = memory
            eng = engine_mod.Engine(Path(t), **kwargs)
            run_id = eng.submit_zip(buf.getvalue())["run_id"]
            eng.step()
            view = eng.view(run_id)
        contracts.validate_http(view, "RunView")
        return view

    def test_over_time_after_snapshot_still_publishes_partial(self):
        times = iter([0, 1, 2] + [engine_mod.TIME_BUDGET_S + 10] * 50)
        view = self.run_with(clock=lambda: next(times))
        self.assertEqual((view["state"], view["result_available"]), ("partial", True))
        self.assertIn("time_budget_exceeded", [r["code"] for r in view["reasons"]])

    def test_over_time_during_intake_fails(self):
        times = iter([0] + [engine_mod.TIME_BUDGET_S + 10] * 50)
        view = self.run_with(clock=lambda: next(times))
        self.assertEqual((view["state"], view["reasons"][0]["code"]), ("failed", "time_budget_exceeded"))

    def test_memory_over_two_gib(self):
        view = self.run_with(memory=lambda: engine_mod.MEMORY_BUDGET + 1)
        self.assertIn("memory_budget_exceeded", [r["code"] for r in view["reasons"]])
        self.assertEqual(view["metrics"]["peak_memory_bytes"], engine_mod.MEMORY_BUDGET + 1)

    def test_peak_memory_is_measured(self):
        peak = engine_mod.peak_memory()
        self.assertTrue(peak is None or peak > 1_000_000)

    def test_polling_while_the_run_saves(self):
        """The UI reads run.json every second while the worker replaces it (Windows: PermissionError)."""
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("main.py", "from fastapi import FastAPI\napp = FastAPI()\n")
        with tempfile.TemporaryDirectory() as t:
            eng = engine_mod.Engine(Path(t), partition=web.demo_partition)
            run_id = eng.submit_zip(buf.getvalue())["run_id"]
            worker = threading.Thread(target=eng.step)
            worker.start()
            while worker.is_alive():
                eng.view(run_id)
            worker.join()
            view = eng.view(run_id)
        self.assertEqual(view["state"], "partial", view["reasons"])


class CliJson(unittest.TestCase):
    def call(self, argv):
        out = io.StringIO()
        with mock.patch("sys.stdout", out), mock.patch("sys.stderr", io.StringIO()):
            code = cli.main(argv)
        result = json.loads(out.getvalue())
        contracts.validate_http(result, "CliResult")
        self.assertEqual(result["exit_code"], code)
        return result

    def test_analyze_json_and_retry_json(self):
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / "out"
            r = self.call(["analyze", "--source", str(FIX / "shop_full"), "--output", str(out),
                           "--membership", str(FIX / "shop_full.membership.json"), "--json"])
            self.assertEqual((r["exit_code"], r["state"], r["analysis_outcome"]), (3, "partial", "partial"))
            self.assertEqual(len(r["files"]), 6)
            self.assertIsNotNone(r["metrics"]["export_ms"])
            readme = next(f for f in r["files"] if f["path"] == "README.md")
            again = self.call(["retry", "--output", str(out), "--artifact", readme["artifact_id"], "--json"])
            self.assertEqual(again["exit_code"], 0)

    def test_overlap_and_output_unsafe(self):
        r = self.call(["--source", str(FIX), "--output", str(FIX / "x"), "--membership", "m.json", "--json"])
        self.assertEqual((r["exit_code"], r["run_id"], r["reasons"][0]["code"]), (2, None, "source_output_overlap"))
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "out").mkdir()
            (Path(t) / "out/keep.txt").write_text("x")
            r = self.call(["--source", str(FIX / "shop_full"), "--output", str(Path(t) / "out"),
                           "--membership", str(FIX / "shop_full.membership.json"), "--json"])
        self.assertEqual((r["exit_code"], r["reasons"][0]["code"]), (2, "output_unsafe"))

    def test_interrupt_is_130(self):
        with tempfile.TemporaryDirectory() as t, mock.patch.object(cli, "run", side_effect=KeyboardInterrupt):
            r = self.call(["--source", str(FIX / "shop_full"), "--output", str(Path(t) / "o"),
                           "--membership", str(FIX / "shop_full.membership.json"), "--json"])
        self.assertEqual((r["exit_code"], r["state"]), (130, "failed"))

    def test_publish_failure_is_4(self):
        from l3slice import render
        with tempfile.TemporaryDirectory() as t, mock.patch.object(render, "_publish",
                                                                   side_effect=render.ExportError("PUBLISH_FAILED", "x")):
            r = self.call(["--source", str(FIX / "shop_full"), "--output", str(Path(t) / "o"),
                           "--membership", str(FIX / "shop_full.membership.json"), "--json"])
        self.assertEqual((r["exit_code"], r["reasons"][0]["code"]), (4, "publish_failed"))


class Ui(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.server = web.make_server(engine_mod.Engine(Path(self.tmp.name)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()

    def get(self, path, host=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=10)
        conn.request("GET", path, headers={"Host": host or f"127.0.0.1:{self.server.server_port}"})
        resp = conn.getresponse()
        body = resp.read()
        conn.close()
        return resp, body

    def test_pages_have_csp_and_no_external_script(self):
        for path, ctype in [("/", "text/html"), ("/ui/app.js", "text/javascript"), ("/ui/app.css", "text/css")]:
            resp, body = self.get(path)
            self.assertEqual(resp.status, 200, path)
            self.assertTrue(resp.getheader("Content-Type").startswith(ctype))
            self.assertIn("script-src 'self'", resp.getheader("Content-Security-Policy"))
            self.assertNotIn(b"http://", body.replace(b"http://127.0.0.1", b""))
            self.assertNotIn(b"https://", body)
        self.assertEqual(self.get("/ui/../engine.py")[0].status, 404)
        self.assertEqual(self.get("/ui/missing.js")[0].status, 404)
        self.assertEqual(self.get("/", host="evil.example")[0].status, 403)

    def test_ui_never_writes_results_to_browser_storage(self):
        js = (web.UI_DIR / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("localStorage", js)
        self.assertNotIn("innerHTML", js)  # every text goes through textContent


if __name__ == "__main__":
    unittest.main()
