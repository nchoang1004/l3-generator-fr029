"""CMP-001 HTTP facade `/api/v1` (API-001 §5–7) on the standard library. Loopback only; no UI.

    python -m l3slice.web --workdir DIR [--port 8000]

Checks in order: Host/Origin, local UI header on POST, ID syntax, run expiry, ownership, readiness (API-001 §5).
The GitHub route validates its input, then answers 503: fetching is off until the Security review of API-002 §1.
"""
from __future__ import annotations

import argparse
import email.parser
import email.policy
import json
import re
import threading
import zipfile
import io
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .engine import NOTICE_VERSION, Engine, EngineError

UI_DIR = Path(__file__).resolve().parent / "ui"
UI_FILES = {"index.html": "text/html; charset=utf-8", "app.js": "text/javascript; charset=utf-8",
            "app.css": "text/css; charset=utf-8"}
CSP = ("default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; "
       "base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
MAX_ZIP = 100_000_000
MULTIPART_OVERHEAD = 64 * 1024
OPAQUE = re.compile(r"^[A-Za-z0-9_:-]{1,128}$")
GITHUB = re.compile(r"^https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(\.git)?/?$")
ROUTES = [(re.compile(p), name) for p, name in [
    (r"^/api/v1/runs/github$", "github"), (r"^/api/v1/runs/zip$", "zip"),
    (r"^/api/v1/runs/([^/]+)$", "run"), (r"^/api/v1/runs/([^/]+)/result$", "result"),
    (r"^/api/v1/runs/([^/]+)/evidence/([^/]+)$", "evidence"), (r"^/api/v1/runs/([^/]+)/artifacts/([^/]+)$", "artifact"),
    (r"^/api/v1/runs/([^/]+)/artifacts/([^/]+)/retry$", "retry")]]
METHODS = {"github": "POST", "zip": "POST", "run": "GET", "result": "GET", "evidence": "GET", "artifact": "GET",
           "retry": "POST"}


def err(status, code, message, action, run_id=None, field=None):
    return EngineError(status, code, message, action, run_id, field)


def normalize_github(url) -> str:
    """API-001 §2.1 rule 3. Returns `https://github.com/<owner>/<repo>`."""
    if not isinstance(url, str) or len(url) > 2048:
        raise err(422, "invalid_github_url", "URL không hợp lệ", "Dùng https://github.com/<owner>/<repo>", field="github_url")
    parts = urlsplit(url)
    m = GITHUB.match(url)
    if not m or parts.username or parts.password or parts.port or parts.query or parts.fragment \
            or {m.group(1), m.group(2)} & {".", ".."} or not m.group(2):
        raise err(422, "invalid_github_url", "Chỉ nhận https://github.com/<owner>/<repo>, không query/port/tree/blob",
                  "Sửa URL repository public", field="github_url")
    return f"https://github.com/{m.group(1)}/{m.group(2)}"


def zip_label(filename) -> str | None:
    """Display name from the upload filename: last path part, no `.zip`, only [A-Za-z0-9._-], at most 64 chars.
    Used as the repository name in titles and file names (slugged again by CMP-008), never as a path (API-001 §2.2)."""
    if not isinstance(filename, str):
        return None
    base = re.split(r"[\\/]", filename)[-1]
    base = re.sub(r"\.zip$", "", base, flags=re.IGNORECASE)
    label = re.sub(r"[^A-Za-z0-9._-]+", "-", base).strip(".-")[:64]
    return label or None


def _no_dup_keys(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise err(400, "invalid_json", "JSON có khóa trùng", "Gửi lại JSON hợp lệ")
    return dict(pairs)


class Handler(BaseHTTPRequestHandler):
    engine: Engine
    origin: str
    server_version = "l3slice"
    sys_version = ""

    def log_message(self, fmt, *args):  # no request lines with IDs or paths in logs
        pass

    def _send(self, status, body: bytes, ctype, extra=None):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status, value, extra=None):
        self._send(status, json.dumps(value, ensure_ascii=False).encode("utf-8"), "application/json", extra)

    def _check_origin(self, post: bool):
        allowed = {self.origin.split("://", 1)[1], self.origin.split("://", 1)[1].replace("127.0.0.1", "localhost")}
        if self.headers.get("Host") not in allowed:
            raise err(403, "origin_rejected", "Host không phải origin loopback của UI", "Mở UI đúng origin loopback")
        origin = self.headers.get("Origin")
        if origin is not None and origin not in {f"http://{h}" for h in allowed}:
            raise err(403, "origin_rejected", "Origin khác origin của UI", "Mở UI đúng origin loopback")
        if post and self.headers.get("X-L3GEN-Client") != "web-v1":
            raise err(403, "origin_rejected", "Thiếu header X-L3GEN-Client: web-v1", "Gửi từ UI cục bộ")
        if post and self.headers.get("Idempotency-Key") is not None:
            raise err(400, "idempotency_key_unsupported", "Không hỗ trợ Idempotency-Key", "Bỏ header; không tự gửi lại POST")

    def _body(self, limit) -> bytes:
        length = self.headers.get("Content-Length")
        if length is None or not length.isdigit():
            raise err(400, "invalid_multipart", "Cần Content-Length; không nhận chunked", "Gửi lại request")
        if int(length) > limit:
            raise err(413, "compressed_size_exceeded", "ZIP vượt 100.000.000 byte", "Giảm kích thước ZIP")
        data = self.rfile.read(int(length))
        if len(data) != int(length):
            raise err(400, "invalid_multipart", "Upload bị ngắt", "Gửi lại request")
        return data

    def _dispatch(self, method):
        path = urlsplit(self.path).path
        if method == "GET" and (path == "/" or path.startswith("/ui/")):
            self._check_origin(False)
            return self._ui(path)
        for rx, name in ROUTES:
            m = rx.match(path)
            if m:
                break
        else:
            raise err(404, "run_not_found", "Không có route này", "Kiểm URL")
        if METHODS[name] != method:
            raise err(404, "run_not_found", "Không có route này với method đó", "Kiểm method")
        self._check_origin(method == "POST")
        ids = [unquote(i) for i in m.groups()]  # the UI sends encodeURIComponent(id): "ev:…" arrives as "ev%3A…"
        if any(not OPAQUE.match(i) for i in ids):
            raise err(404, "run_not_found", "ID không hợp lệ", "Kiểm ID")
        getattr(self, f"_{name}")(*ids)

    def do_GET(self):
        self._safe("GET")

    def do_POST(self):
        self._safe("POST")

    def _safe(self, method):
        try:
            self._dispatch(method)
        except EngineError as exc:
            self._json(exc.status, exc.body)
        except Exception:  # no stack trace or path in the response
            self._json(500, {"code": "internal_error", "message": "Lỗi nội bộ", "action": "Thử run mới",
                             "retryable": False, "run_id": None, "field": None})

    # ---------- local UI (static files of l3slice/ui, no third-party script)

    def _ui(self, path):
        name = "index.html" if path == "/" else path[len("/ui/"):]
        if name not in UI_FILES:
            raise err(404, "run_not_found", "Không có trang này", "Mở /")
        data = (UI_DIR / name).read_bytes()
        self._send(200, data, UI_FILES[name], {"Content-Security-Policy": CSP, "X-Content-Type-Options": "nosniff",
                                                "Referrer-Policy": "no-referrer", "X-Frame-Options": "DENY"})

    # ---------- routes

    def _accepted(self, view):
        self._json(202, view, {"Location": view["links"]["self"], "Retry-After": "2"})

    def _github(self):
        if self.headers.get_content_type() != "application/json":
            raise err(415, "unsupported_media_type", "Cần application/json", "Gửi JSON")
        try:
            body = json.loads(self._body(64 * 1024), object_pairs_hook=_no_dup_keys)
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise err(400, "invalid_json", "JSON không hợp lệ", "Gửi lại JSON hợp lệ") from None
        if not isinstance(body, dict):
            raise err(422, "unknown_field", "Body phải là object", "Gửi object JSON")
        for key in body:
            if key not in ("github_url", "egress_notice_version"):
                raise err(422, "unknown_field", f"Request chứa trường {key[:80]} không được hỗ trợ",
                          "Bỏ trường này; không gửi credential", field=key[:80])
        if body.get("egress_notice_version") != NOTICE_VERSION:
            raise err(422, "notice_version_mismatch", "Thiếu hoặc sai phiên bản thông báo", "Tải lại UI",
                      field="egress_notice_version")
        self._accepted(self.engine.submit_github(normalize_github(body.get("github_url"))))

    def _zip(self):
        if self.headers.get_content_type() != "multipart/form-data":
            raise err(415, "unsupported_media_type", "Cần multipart/form-data", "Gửi một ZIP multipart")
        raw = self._body(MAX_ZIP + MULTIPART_OVERHEAD)
        msg = email.parser.BytesParser(policy=email.policy.HTTP).parsebytes(
            b"Content-Type: " + self.headers["Content-Type"].encode("latin-1") + b"\r\n\r\n" + raw)
        if not msg.is_multipart():
            raise err(400, "invalid_multipart", "Multipart hỏng", "Gửi lại request")
        parts = {}
        for part in msg.iter_parts():
            name = part.get_param("name", header="content-disposition")
            if name in parts:
                raise err(400, "invalid_multipart", f"Part {name} bị trùng", "Gửi đúng một part mỗi loại")
            parts[name] = part
        if set(parts) != {"archive", "egress_notice_version"}:
            raise err(422, "unknown_field", "Cần đúng hai part archive và egress_notice_version", "Sửa form",
                      field=",".join(sorted(str(k) for k in parts)))
        if parts["egress_notice_version"].get_content().strip() != NOTICE_VERSION:
            raise err(422, "notice_version_mismatch", "Sai phiên bản thông báo", "Tải lại UI", field="egress_notice_version")
        data = parts["archive"].get_payload(decode=True) or b""
        if len(data) > MAX_ZIP:
            raise err(413, "compressed_size_exceeded", "ZIP vượt 100.000.000 byte", "Giảm kích thước ZIP")
        if not data.startswith(b"PK") or not zipfile.is_zipfile(io.BytesIO(data)):
            raise err(422, "invalid_zip", "File không phải ZIP đọc được", "Tạo lại ZIP", field="archive")
        self._accepted(self.engine.submit_zip(data, zip_label(parts["archive"].get_filename())))

    def _run(self, run_id):
        self._json(200, self.engine.view(run_id))

    def _result(self, run_id):
        self._json(200, self.engine.result(run_id))

    def _evidence(self, run_id, evidence_id):
        self._json(200, self.engine.evidence(run_id, evidence_id))

    def _artifact(self, run_id, artifact_id):
        art, data = self.engine.artifact(run_id, artifact_id)
        name = re.sub(r"[^A-Za-z0-9._-]", "_", art["path"].rsplit("/", 1)[-1])
        self._send(200, data, "application/octet-stream",
                   {"Content-Disposition": f'attachment; filename="{name}"', "X-Content-Type-Options": "nosniff"})

    def _retry(self, run_id, artifact_id):
        if self.headers.get("Content-Length") not in (None, "0"):
            raise err(400, "unexpected_body", "Retry không nhận body", "Gửi POST không body", run_id)
        status, _ = self.engine.retry(run_id, artifact_id)
        view = self.engine.view(run_id)
        if status == 202:
            self._accepted(view)
        else:
            self._json(200, view)


def make_server(engine: Engine, port: int = 0) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    handler = type("BoundHandler", (Handler,), {"engine": engine, "origin": f"http://127.0.0.1:{server.server_port}"})
    server.RequestHandlerClass = handler
    return server


def demo_partition(snap) -> dict:
    """Stand-in membership for trying the web UI: one component per first directory (candidate A `directory-v1`
    of the D-03 experiment). Not a D-03 choice; every run that uses it says so in its reasons."""
    groups = {}
    for f in snap["files"]:
        head = f["path"].split("/", 1)[0] if "/" in f["path"] else "(root)"
        groups.setdefault(head, []).append(f["path"])
    return {"partition_version": "fixture-membership-v1",
            "components": [{"name": n, "files": fs} for n, fs in sorted(groups.items())]}


DEMO_NOTE = {"code": "demo_partition", "message": "Component chia tạm theo thư mục đầu tiên để chạy thử giao diện; "
             "chưa phải thuật toán D-03 đã chọn", "action": "Không dùng sơ đồ này làm kết luận kiến trúc"}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="l3slice.web")
    p.add_argument("--workdir", type=Path, required=True)
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--demo-partition", action="store_true",
                   help="Chia component tạm theo thư mục (chỉ để chạy thử; D-03 chưa chọn)")
    p.add_argument("--enable-github", action="store_true",
                   help="Bật tải source GitHub (API-002 §1: cần Security review danh sách host trước khi dùng)")
    p.add_argument("--llm", action="store_true", help="Hỏi khóa model lúc khởi động (không hiện chữ)")
    a = p.parse_args(argv)
    from .__main__ import model_context_builder
    engine = Engine(a.workdir, partition=demo_partition if a.demo_partition else None,
                    partition_note=DEMO_NOTE if a.demo_partition else None,
                    github={} if a.enable_github else None,
                    model_context=model_context_builder() if a.llm else None)
    stop = threading.Event()
    threading.Thread(target=engine.serve_forever, args=(stop,), daemon=True).start()
    server = make_server(engine, a.port)
    print(f"http://127.0.0.1:{server.server_port}/ (chỉ loopback)")
    try:
        server.serve_forever()
    finally:
        stop.set()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
