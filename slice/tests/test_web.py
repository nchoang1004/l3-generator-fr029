"""Đợt 9: run lifecycle and HTTP facade (API-001 §2–7). Loopback server on a free port; no network beyond it."""
from __future__ import annotations

import hashlib
import http.client
import io
import json
import sys
import tempfile
import threading
import unittest
import uuid
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import contracts  # noqa: E402
from l3slice import engine as engine_mod, render, web  # noqa: E402

FIX = HERE / "fixtures"
MEMBERSHIP = json.loads((FIX / "shop_full.membership.json").read_text(encoding="utf-8"))


def shop_zip(extra=None) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for p in sorted((FIX / "shop_full").rglob("*.py")):
            zf.writestr(p.relative_to(FIX / "shop_full").as_posix(), p.read_bytes())
        for name, data in (extra or {}).items():
            info = zipfile.ZipInfo("x")
            info.filename = name
            zf.writestr(info, data)
    return buf.getvalue()


def multipart(parts):
    boundary = uuid.uuid4().hex
    body = b""
    for name, data, ctype in parts:
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\nContent-Type: {ctype}\r\n\r\n"
                 ).encode() + data + b"\r\n"
    return body + f"--{boundary}--\r\n".encode(), f"multipart/form-data; boundary={boundary}"


class Clock:
    def __init__(self):
        self.t = datetime(2026, 10, 1, 8, 0, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.t


class Web(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.clock = Clock()
        self.engine = engine_mod.Engine(Path(self.tmp.name), partition=lambda snap: MEMBERSHIP, now=self.clock)
        self.server = web.make_server(self.engine)
        self.port = self.server.server_port
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()

    def call(self, method, path, body=None, ctype=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        h = {"Host": f"127.0.0.1:{self.port}"}
        if method == "POST":
            h["X-L3GEN-Client"] = "web-v1"
        if ctype:
            h["Content-Type"] = ctype
        h.update(headers or {})
        conn.request(method, path, body=body, headers={k: v for k, v in h.items() if v is not None})
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        self.assertEqual(resp.getheader("Cache-Control"), "no-store")
        return resp, data

    def json_call(self, *a, **k):
        resp, data = self.call(*a, **k)
        value = json.loads(data)
        contracts.validate_http(value, "RunView" if resp.status in (200, 202) and "state" in value else
                                "Error" if resp.status >= 400 else "EvidenceView" if "content" in value else "RunView")
        return resp.status, value

    def post_zip(self, data=None, notice=b"l3gen-egress-v1"):
        body, ctype = multipart([("archive", data if data is not None else shop_zip(), "application/zip"),
                                 ("egress_notice_version", notice, "text/plain")])
        return self.json_call("POST", "/api/v1/runs/zip", body, ctype)

    def test_zip_run_end_to_end(self):
        status, view = self.post_zip()
        self.assertEqual((status, view["state"], view["stage"]), (202, "queued", "queue"))
        run_id = view["run_id"]
        self.assertTrue(self.engine.step())
        status, view = self.json_call("GET", f"/api/v1/runs/{run_id}")
        self.assertEqual((view["state"], view["analysis_outcome"], view["result_available"]), ("partial", "partial", True))
        self.assertEqual(view["expires_at"], "2026-10-02T08:00:00Z")
        resp, data = self.call("GET", f"/api/v1/runs/{run_id}/result")
        bundle = json.loads(data)
        contracts.validate(bundle, 8, "ResultBundle")
        ev = bundle["result"]["evidence_index"][0]["id"]
        status, evidence = self.json_call("GET", f"/api/v1/runs/{run_id}/evidence/{ev}")
        contracts.validate_http(evidence, "EvidenceView")
        self.assertEqual((status, evidence["evidence"]["id"]), (200, ev))
        # the UI sends encodeURIComponent(id): ":" arrives as "%3A"
        status, evidence = self.json_call("GET", f"/api/v1/runs/{run_id}/evidence/{ev.replace(':', '%3A')}")
        self.assertEqual((status, evidence["evidence"]["id"]), (200, ev))
        art = next(a for a in bundle["artifacts"] if a["kind"] == "readme")
        resp, data = self.call("GET", f"/api/v1/runs/{run_id}/artifacts/{art['artifact_id']}")
        self.assertEqual(hashlib.sha256(data).hexdigest(), art["sha256"])
        self.assertEqual(resp.getheader("X-Content-Type-Options"), "nosniff")
        self.assertEqual(resp.getheader("Content-Disposition"), 'attachment; filename="README.md"')

    def test_zip_filename_names_the_repository(self):
        """PRD r28 FR-027: file names carry a system code from the repository name, not "REPOSITORY"."""
        boundary = uuid.uuid4().hex
        body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"archive\"; filename=\"C:\\\\x\\\\teamhide.zip\"\r\n"
                f"Content-Type: application/zip\r\n\r\n").encode() + shop_zip() + (
                f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"egress_notice_version\"\r\n\r\n"
                f"l3gen-egress-v1\r\n--{boundary}--\r\n").encode()
        run_id = self.json_call("POST", "/api/v1/runs/zip", body, f"multipart/form-data; boundary={boundary}")[1]["run_id"]
        self.engine.step()
        bundle = json.loads(self.call("GET", f"/api/v1/runs/{run_id}/result")[1])
        self.assertEqual(bundle["export_context"]["repository_name"], "teamhide")
        self.assertTrue(any("API-TEAMHIDE-" in a["path"] for a in bundle["artifacts"]))
        self.assertEqual([web.zip_label(n) for n in ["../../etc/x.ZIP", "a b<c>.zip", ".zip", None]],
                         ["x", "a-b-c", None, None])

    def test_fifo_order_and_one_at_a_time(self):
        first = self.post_zip()[1]["run_id"]
        second = self.post_zip()[1]["run_id"]
        self.engine.step()
        self.assertEqual(self.json_call("GET", f"/api/v1/runs/{first}")[1]["state"], "partial")
        self.assertEqual(self.json_call("GET", f"/api/v1/runs/{second}")[1]["state"], "queued")
        self.engine.busy = "someone"
        self.assertFalse(self.engine.step())

    def test_host_origin_and_client_header(self):
        cases = [({"Host": "evil.example"}, "GET"), ({"Origin": "http://evil.example"}, "GET"),
                 ({"X-L3GEN-Client": None}, "POST")]
        for headers, method in cases:
            path = "/api/v1/runs/run_x" if method == "GET" else "/api/v1/runs/zip"
            status, body = self.json_call(method, path, b"", "multipart/form-data; boundary=x", headers)
            self.assertEqual((status, body["code"]), (403, "origin_rejected"), headers)
        status, body = self.json_call("POST", "/api/v1/runs/zip", b"", "multipart/form-data; boundary=x",
                                      {"Idempotency-Key": "k"})
        self.assertEqual((status, body["code"]), (400, "idempotency_key_unsupported"))

    def test_github_input_checks(self):
        def post(value, raw=None):
            body = raw if raw is not None else json.dumps(value).encode()
            return self.json_call("POST", "/api/v1/runs/github", body, "application/json")
        status, body = post({"github_url": "https://github.com/a/b", "egress_notice_version": "l3gen-egress-v1",
                             "repository_token": "not-a-real-token"})
        self.assertEqual((status, body["code"], body["field"]), (422, "unknown_field", "repository_token"))
        for bad in ["http://github.com/a/b", "https://github.com/a/b/tree/main", "https://github.com/a/b?x=1",
                    "https://github.com:8443/a/b", "https://u@github.com/a/b", "https://github.com/../b",
                    "https://gitlab.com/a/b"]:
            status, body = post({"github_url": bad, "egress_notice_version": "l3gen-egress-v1"})
            self.assertEqual((status, body["code"]), (422, "invalid_github_url"), bad)
        status, body = post(None, b'{"github_url":"x","github_url":"y"}')
        self.assertEqual((status, body["code"]), (400, "invalid_json"))
        status, body = post({"github_url": "https://github.com/a/b.git", "egress_notice_version": "l3gen-egress-v1"})
        self.assertEqual((status, body["code"]), (503, "engine_unavailable"))
        self.assertEqual(web.normalize_github("https://github.com/a/b.git/"), "https://github.com/a/b")

    def test_zip_admission_errors(self):
        self.assertEqual(self.post_zip(b"not a zip")[1]["code"], "invalid_zip")
        self.assertEqual(self.post_zip(notice=b"old")[1]["code"], "notice_version_mismatch")
        body, ctype = multipart([("archive", shop_zip(), "application/zip"), ("archive", shop_zip(), "application/zip"),
                                 ("egress_notice_version", b"l3gen-egress-v1", "text/plain")])
        self.assertEqual(self.json_call("POST", "/api/v1/runs/zip", body, ctype)[1]["code"], "invalid_multipart")
        with mock.patch.object(web, "MAX_ZIP", 10), mock.patch.object(web, "MULTIPART_OVERHEAD", 0):
            status, body = self.post_zip()
        self.assertEqual((status, body["code"]), (413, "compressed_size_exceeded"))
        self.assertEqual(list((Path(self.tmp.name) / "runs").iterdir()), [])  # no run admitted

    def test_unsafe_zip_fails_after_admission(self):
        status, view = self.post_zip(shop_zip({"../evil.py": b"x"}))
        self.assertEqual(status, 202)
        self.engine.step()
        status, view = self.json_call("GET", f"/api/v1/runs/{view['run_id']}")
        self.assertEqual((view["state"], view["reasons"][0]["code"]), ("failed", "unsafe_archive_path"))
        status, body = self.json_call("GET", f"/api/v1/runs/{view['run_id']}/result")
        self.assertEqual((status, body["code"]), (409, "result_unavailable"))

    def test_ids_and_ownership(self):
        self.assertEqual(self.json_call("GET", "/api/v1/runs/run_missing")[0], 404)
        self.assertEqual(self.json_call("GET", "/api/v1/runs/a.b")[0], 404)
        run_id = self.post_zip()[1]["run_id"]
        self.engine.step()
        status, body = self.json_call("GET", f"/api/v1/runs/{run_id}/evidence/ev:other")
        self.assertEqual((status, body["code"]), (404, "evidence_not_found"))
        status, body = self.json_call("GET", f"/api/v1/runs/{run_id}/artifacts/art_other")
        self.assertEqual((status, body["code"]), (404, "artifact_not_found"))

    def test_expiry_then_restart(self):
        run_id = self.post_zip()[1]["run_id"]
        self.engine.step()
        self.clock.t += timedelta(hours=24)
        status, body = self.json_call("GET", f"/api/v1/runs/{run_id}/result")
        self.assertEqual((status, body["code"]), (410, "run_expired"))
        engine_mod.Engine(Path(self.tmp.name), now=self.clock)  # restart purges expired runs
        self.assertEqual(self.json_call("GET", f"/api/v1/runs/{run_id}")[0], 404)

    def test_restart_fails_interrupted_runs(self):
        run_id = self.post_zip()[1]["run_id"]
        engine_mod.Engine(Path(self.tmp.name), now=self.clock)
        status, view = self.json_call("GET", f"/api/v1/runs/{run_id}")
        self.assertEqual((view["state"], view["reasons"][0]["code"]), ("failed", "process_interrupted"))
        self.assertEqual([p.name for p in (Path(self.tmp.name) / "runs" / run_id).iterdir()], ["run.json"])

    def test_no_partition_policy_fails_run(self):
        self.engine.partition = None
        run_id = self.post_zip()[1]["run_id"]
        self.engine.step()
        view = self.json_call("GET", f"/api/v1/runs/{run_id}")[1]
        self.assertEqual((view["state"], view["reasons"][0]["code"]), ("failed", "partition_policy_unavailable"))

    def test_retry_failed_svg(self):
        run_id = self.post_zip()[1]["run_id"]
        with mock.patch.object(render, "svg", side_effect=OSError("disk full")):
            self.engine.step()
        view = self.json_call("GET", f"/api/v1/runs/{run_id}")[1]
        svg = next(a for a in view["artifacts"] if a["kind"] == "diagram_image")
        readme = next(a for a in view["artifacts"] if a["kind"] == "readme")
        self.assertEqual(svg["status"], "failed")
        self.assertIn("artifact_export_failed", [r["code"] for r in view["reasons"]])
        retry = f"/api/v1/runs/{run_id}/artifacts/{svg['artifact_id']}/retry"
        self.assertEqual(self.json_call("POST", retry, b"{}", "application/json")[1]["code"], "unexpected_body")
        self.engine.busy = "other"
        self.assertEqual(self.json_call("POST", retry)[1]["code"], "engine_busy")
        self.engine.busy = None
        status, after = self.json_call("POST", retry)
        self.assertEqual(status, 200)
        new = next(a for a in after["artifacts"] if a["kind"] == "diagram_image")
        self.assertEqual(new["status"], "ready")
        self.assertEqual(next(a for a in after["artifacts"] if a["kind"] == "readme")["sha256"], readme["sha256"])
        self.assertEqual((after["state"], after["finished_at"]), (view["state"], view["finished_at"]))
        self.assertEqual(self.json_call("POST", retry)[0], 200)  # already ready: no-op


if __name__ == "__main__":
    unittest.main()
