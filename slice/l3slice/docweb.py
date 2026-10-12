"""Local UI for the FR-029 agent pipeline. Run with python -m l3slice.docweb."""
from __future__ import annotations

import argparse
import copy
import json
import secrets
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .docagent import Budget, OpenAICompatProvider, ProviderError, ScriptedProvider
from .docpipeline import InputError, run_documents
from .snapshot import IntakeError
from .web import CSP, Handler, UI_FILES, err

UI_DIR = Path(__file__).resolve().parent / "docui"
NOTICE = "fr029-source-v1"


class DocumentService:
    """One active run; provider credentials and output locations stay server-side."""

    def __init__(self, workdir, provider_factory, *, model, offline=False, endpoint=None, defaults=None, budget=None):
        self.workdir = Path(workdir).resolve()
        self.workdir.mkdir(parents=True, exist_ok=True)  # the oneshot checkpoint is written here before the output exists
        self.factory = provider_factory
        # A recorded script answers agent-mode tool calls only, so offline runs cannot use oneshot.
        self.config = {"model": model, "offline": offline, "endpoint": endpoint, "defaults": defaults or {},
                       "notice_version": NOTICE, "modes": ["agent"] if offline else ["agent", "oneshot"]}
        self.budget = budget or Budget()
        self.lock = threading.Lock()
        self.runs = {}

    def submit(self, body):
        fields = {"source", "membership", "archdia", "diagram", "name", "notice_version", "mode"}
        if not isinstance(body, dict) or set(body) - fields:
            raise err(422, "invalid_input", "Đầu vào chứa trường không được hỗ trợ.", "Kiểm tra biểu mẫu")
        if body.get("notice_version") != NOTICE:
            raise err(422, "notice_required", "Cần xác nhận thông báo gửi source.", "Đọc thông báo và xác nhận")
        paths = {}
        for key in ("source", "membership", "archdia", "diagram"):
            value = body.get(key, "")
            if not value and key in ("archdia", "diagram"):
                paths[key] = None
                continue
            if not isinstance(value, str) or not value.strip() or len(value) > 4096:
                raise err(422, "invalid_input", f"Thiếu hoặc sai trường {key}.", "Nhập đường dẫn tuyệt đối", field=key)
            path = Path(value.strip())
            if not path.is_absolute() or not (path.is_dir() if key == "source" else path.is_file()):
                raise err(422, "invalid_path", f"Không tìm thấy {key} tại đường dẫn tuyệt đối này.",
                          "Chọn đường dẫn trên máy chạy server", field=key)
            paths[key] = path.resolve()
        source = paths["source"]
        if source == self.workdir or source in self.workdir.parents or self.workdir in source.parents:
            raise err(422, "source_output_overlap", "Thư mục kết quả và source không được bao nhau.",
                      "Khởi động server với --workdir nằm ngoài cây source", field="source")
        mode = body.get("mode", "agent")
        if mode not in self.config["modes"]:
            raise err(422, "invalid_mode", "Chế độ đọc không được hỗ trợ ở server này.", "Chọn chế độ khác", field="mode")
        name = body.get("name") or source.name
        if not isinstance(name, str) or len(name) > 128 or not name.strip():
            raise err(422, "invalid_name", "Tên dự án cần từ 1 đến 128 ký tự.", "Sửa tên dự án", field="name")
        with self.lock:
            if any(r["status"] == "running" for r in self.runs.values()):
                raise err(409, "run_busy", "Đang có một lần sinh tài liệu.", "Chờ lần hiện tại kết thúc")
            run_id = "run_" + secrets.token_hex(8)
            self.runs[run_id] = {"run_id": run_id, "name": name, "mode": mode, "status": "running", "turns": 0,
                                 "message": "Đang chuẩn bị snapshot và kiểm tra membership."}
            view = copy.deepcopy(self.runs[run_id])
            threading.Thread(target=self._run, args=(run_id, paths, name, mode), daemon=True).start()
        return view

    def view(self, run_id=None):
        with self.lock:
            if run_id is None:
                return [{k: copy.deepcopy(v) for k, v in r.items() if k != "result"} for r in self.runs.values()]
            if run_id not in self.runs:
                raise err(404, "run_not_found", "Không tìm thấy lần chạy trong phiên server này.", "Chọn lần chạy khác")
            return copy.deepcopy(self.runs[run_id])

    def _update(self, run_id, **values):
        with self.lock:
            self.runs[run_id].update(values)

    def _run(self, run_id, paths, name, mode="agent"):
        try:
            provider = self.factory()
            service = self

            class ObservedProvider:
                def __getattr__(self, attr):
                    return getattr(provider, attr)

                def chat(self, messages, tools, **options):
                    turn = service.view(run_id)["turns"] + 1
                    service._update(run_id, turns=turn, message="Agent đang đọc và đối chiếu source.")
                    return provider.chat(messages, tools, **options)

            # The output directory must start empty, so the checkpoint lives beside it.
            bundle = run_documents(paths["source"], self.workdir / run_id, paths["membership"], name,
                                   ObservedProvider(), paths["archdia"], paths["diagram"], self.budget, run_id,
                                   mode=mode, checkpoint=self.workdir / f"{run_id}.checkpoint.json" if mode == "oneshot" else None)
            # Finished describes the job, not FR-029 acceptance. Preserve all pipeline verdicts.
            self._update(run_id, status="finished", message="Đã xuất kết quả. Cần xem các giới hạn trước khi sử dụng.",
                         result=bundle, output_directory=str(self.workdir / run_id))
        except (InputError, IntakeError, ProviderError) as exc:
            self._update(run_id, status="failed", message=str(exc)[:1000])
        except (OSError, ValueError, KeyError, TypeError):
            self._update(run_id, status="failed", message="Không đọc hoặc ghi được dữ liệu. Kiểm tra file đầu vào và quyền thư mục kết quả.")
        except Exception:
            self._update(run_id, status="failed", message="Luồng sinh tài liệu gặp lỗi nội bộ. Kiểm tra bằng CLI document.")

    def artifact(self, run_id, artifact_id):
        run = self.view(run_id)
        art = next((a for a in run.get("result", {}).get("artifacts", []) if a["artifact_id"] == artifact_id), None)
        if art is None or art["status"] != "ready":
            raise err(404, "artifact_not_ready", "Tài liệu chưa sẵn sàng.", "Xem trạng thái lần chạy")
        root = (self.workdir / run_id).resolve()
        path = (root / art["path"]).resolve()
        if root not in path.parents:
            raise err(404, "invalid_artifact", "Đường dẫn tài liệu không hợp lệ.", "Xem result.json")
        return path.name, path.read_bytes()


class DocumentHandler(Handler):
    service: DocumentService

    def _dispatch(self, method):
        self._check_origin(method == "POST")
        path = urlsplit(self.path).path
        if method == "GET" and (path == "/" or path.startswith("/ui/")):
            name = "index.html" if path == "/" else path[4:]
            if name not in UI_FILES:
                raise err(404, "not_found", "Không có trang này.", "Mở /")
            return self._send(200, (UI_DIR / name).read_bytes(), UI_FILES[name],
                              {"Content-Security-Policy": CSP, "X-Content-Type-Options": "nosniff"})
        if method == "GET" and path == "/api/config":
            return self._json(200, self.service.config)
        if path == "/api/runs":
            if method == "GET":
                return self._json(200, self.service.view())
            if self.headers.get_content_type() != "application/json":
                raise err(415, "invalid_type", "Cần application/json.", "Gửi lại biểu mẫu")
            length = self.headers.get("Content-Length", "")
            if not length.isdigit() or int(length) > 32768:
                raise err(413, "invalid_length", "Đầu vào vượt giới hạn 32 KB hoặc thiếu Content-Length.", "Rút gọn đầu vào")
            try:
                body = json.loads(self._body(32768))
            except (ValueError, UnicodeDecodeError):
                raise err(400, "invalid_json", "JSON không hợp lệ.", "Gửi lại biểu mẫu") from None
            return self._json(202, self.service.submit(body))
        parts = path.strip("/").split("/")
        if method == "GET" and len(parts) >= 3 and parts[:2] == ["api", "runs"]:
            if len(parts) == 3:
                return self._json(200, self.service.view(parts[2]))
            if len(parts) == 5 and parts[3] == "artifacts":
                name, data = self.service.artifact(parts[2], unquote(parts[4]))
                from urllib.parse import quote
                return self._send(200, data, "application/octet-stream", {
                    "Content-Disposition": "attachment; filename*=UTF-8''" + quote(name),
                    "X-Content-Type-Options": "nosniff"})
        raise err(404, "not_found", "Không có đường dẫn này.", "Mở /")


def make_server(service, port=8001):
    server = ThreadingHTTPServer(("127.0.0.1", port), DocumentHandler)
    server.RequestHandlerClass = type("BoundDocumentHandler", (DocumentHandler,), {
        "service": service, "origin": f"http://127.0.0.1:{server.server_port}"})
    return server


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workdir", type=Path, required=True)
    p.add_argument("--port", type=int, default=8001)
    p.add_argument("--source", type=Path, help="Điền sẵn source trên giao diện")
    p.add_argument("--membership", type=Path, help="Điền sẵn membership trên giao diện")
    p.add_argument("--script", type=Path, help="Kịch bản công cụ offline, cùng định dạng CLI document")
    p.add_argument("--base-url")
    p.add_argument("--model")
    p.add_argument("--key-env")
    p.add_argument("--max-turns", type=int, default=200)
    p.add_argument("--max-tokens", type=int, default=2_000_000)
    p.add_argument("--max-seconds", type=int, default=1800)
    p.add_argument("--max-output-tokens", type=int)
    p.add_argument("--timeout", type=float, default=120, help="Giây chờ một request tới model; model suy luận cần 300 trở lên")
    p.add_argument("--reasoning-effort", help="Mức suy luận của model (ví dụ low); bỏ trống thì theo mặc định của model")
    p.add_argument("--prices", help="USD mỗi 1 triệu token: đầu vào,đầu vào từ bộ đệm,đầu ra (ví dụ 1.25,0.125,10)")
    p.add_argument("--max-cost-usd", type=float, help="Dừng trước request kế tiếp khi chi phí đã đạt mức này; cần --prices")
    a = p.parse_args(argv)
    try:
        prices = tuple(float(x) for x in a.prices.split(",")) if a.prices else None
        if prices is not None and len(prices) != 3:
            raise ValueError
    except ValueError:
        p.error("--prices cần đúng 3 số, cách nhau bằng dấu phẩy")
    if a.max_cost_usd is not None and (a.max_cost_usd <= 0 or not prices):
        p.error("--max-cost-usd cần số dương và --prices")
    if min(a.max_turns, a.max_tokens, a.max_seconds, a.timeout) <= 0:
        p.error("Ngân sách phải lớn hơn 0")
    if a.script and any((a.base_url, a.model, a.key_env)):
        p.error("Chọn --script hoặc cấu hình model, không dùng đồng thời")
    if a.script:
        try:
            steps = json.loads(a.script.read_text(encoding="utf-8"))
            replies = [[(c["name"], c["arguments"]) for c in step] for step in steps]
        except (OSError, ValueError, KeyError, TypeError):
            p.error("Không đọc được kịch bản công cụ")
        factory = lambda: ScriptedProvider(copy.deepcopy(replies))
    else:
        if not all((a.base_url, a.model, a.key_env)):
            p.error("Cần --script hoặc đủ --base-url, --model, --key-env")
        endpoint = urlsplit(a.base_url)
        if endpoint.scheme not in ("http", "https") or not endpoint.hostname or endpoint.username or endpoint.password or endpoint.query or endpoint.fragment:
            p.error("--base-url cần HTTP(S) URL không chứa credential, query hoặc fragment")
        factory = lambda: OpenAICompatProvider(a.base_url, a.model, a.key_env, timeout=a.timeout, max_output_tokens=a.max_output_tokens, prices=prices,
                                            reasoning_effort=a.reasoning_effort)
        try:
            factory()  # Validate credentials before opening the UI; no network call.
        except ProviderError as exc:
            p.error(str(exc))
    service = DocumentService(a.workdir, factory, model=a.model or "Kịch bản offline", offline=bool(a.script), endpoint=a.base_url,
                              defaults={k: str(v.resolve()) for k, v in (("source", a.source), ("membership", a.membership)) if v},
                              budget=Budget(max_turns=a.max_turns, max_tokens=a.max_tokens, max_seconds=a.max_seconds, max_cost_usd=a.max_cost_usd))
    server = make_server(service, a.port)
    print(f"FR-029: http://127.0.0.1:{server.server_port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
