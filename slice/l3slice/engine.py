"""CMP-001 subset: run lifecycle, FIFO queue, 24-hour retention, cleanup on start (API-001 §2.2–4).

One run at a time; later runs wait in arrival order with no capacity limit and no waiting deadline. A run record is a
JSON file under `<workdir>/runs/<run_id>/`; the published output sits next to it. Source bytes of a run are kept in
memory only, so evidence of a run can be opened until the process stops.

Budgets of NFR-OPS-001 (30 minutes from `started_at`, 2 GiB) are checked between stages, not inside one: a run
over budget skips the optional model step and still verifies and publishes what is done (`partial`); over budget
before a snapshot exists it fails. Peak memory is the peak of the whole process (server included).
GitHub intake runs only when the engine is built with `github=...` (API-002 §1 asks for a Security review first).
No partition policy is chosen (D-03): without `partition` every run fails with `partition_policy_unavailable`.
"""
from __future__ import annotations

import collections
import json
import os
import secrets
import shutil
import sys
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import annotate, extract, gateway, github, model, render, snapshot, verify
from .verify import VerificationError

RETENTION = timedelta(hours=24)
NOTICE_VERSION = "l3gen-egress-v1"
METRIC_KEYS = ("intake_ms", "static_analysis_ms", "model_ms", "export_ms", "peak_memory_bytes", "output_bytes")
TIME_BUDGET_S = 30 * 60
MEMORY_BUDGET = 2 * 2 ** 30
INTAKE_CODES = {"PATH_ESCAPE": "unsafe_archive_path", "PATH_COLLISION": "unsafe_archive_path",
                "LINK_NOT_ALLOWED": "unsafe_archive_path", "GITHUB_NOT_FOUND_OR_PRIVATE": "github_not_found_or_private",
                "GITHUB_ACCESS_DENIED": "github_access_denied", "FETCH_TIMEOUT": "github_timeout",
                "GITHUB_FETCH_FAILED": "github_fetch_failed"}


def peak_memory() -> int | None:
    """Peak resident memory of this process in bytes, or None when the platform does not tell."""
    try:
        if sys.platform == "win32":
            import ctypes
            from ctypes import wintypes

            class Counters(ctypes.Structure):
                _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
                    (n, ctypes.c_size_t) for n in ("PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
                                                   "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage",
                                                   "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage")]
            c = Counters()
            c.cb = ctypes.sizeof(c)
            psapi = ctypes.WinDLL("psapi")
            psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
            kernel = ctypes.WinDLL("kernel32")
            kernel.GetCurrentProcess.restype = wintypes.HANDLE
            ok = psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(c), c.cb)
            return int(c.PeakWorkingSetSize) if ok else None
        import resource
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return int(peak if sys.platform == "darwin" else peak * 1024)
    except Exception:
        return None


class EngineError(Exception):
    """Maps to an HTTP status and an API-001 Error code."""

    def __init__(self, status: int, code: str, message: str, action: str, run_id=None, field=None):
        super().__init__(f"{code}: {message}")
        self.status = status
        self.body = {"code": code, "message": message, "action": action, "retryable": False, "run_id": run_id,
                     "field": field}


def _iso(t: datetime | None):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ") if t else None


def _parse(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) if s else None


def _reason(code, message, action="Xem giới hạn trong ResultBundle"):
    return {"code": code, "message": message[:1000], "action": action}


class Engine:
    def __init__(self, workdir: Path, partition=None, now=lambda: datetime.now(timezone.utc), model_context=None,
                 github=None, clock=time.monotonic, memory=peak_memory, partition_note=None):
        self.dir = Path(workdir)
        (self.dir / "runs").mkdir(parents=True, exist_ok=True)
        self.partition = partition          # callable(snapshot) -> membership dict, or None (D-03 open)
        self.model_context = model_context  # callable(run_id, snapshot, sources) -> gateway.RunContext, or None
        self.github = github                # None: GitHub off; dict: transport kwargs for github.take_github
        self.partition_note = partition_note  # Reason shown on every run when the partition is a stand-in
        self.now, self.clock, self.memory = now, clock, memory
        self.lock = threading.Lock()        # guards records and the busy flag
        self.file_lock = threading.Lock()   # run.json: Windows refuses os.replace while another thread reads it
        self.queue = collections.deque()
        self.busy = None                    # run_id being analysed, or ("retry", run_id, artifact_id)
        self.sources = {}                   # run_id -> (snapshot, sources) kept for evidence
        self.wake = threading.Condition(self.lock)
        self._cleanup_on_start()

    # ---------- records

    def _path(self, run_id):
        return self.dir / "runs" / run_id

    def _load(self, run_id) -> dict | None:
        p = self._path(run_id) / "run.json"
        with self.file_lock:
            return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None

    def _save(self, rec):
        p = self._path(rec["run_id"]) / "run.json"
        tmp = p.with_name(".run.json.tmp")
        with self.file_lock:
            tmp.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
            os.replace(tmp, p)

    def _finish(self, rec, state, outcome, reasons):
        rec.update(state=state, stage=None, analysis_outcome=outcome, reasons=reasons, finished_at=_iso(self.now()),
                   expires_at=_iso(self.now() + RETENTION))
        self._save(rec)

    def _cleanup_on_start(self):
        """Purge expired runs; runs left queued/running by a dead process become failed (API-001 §2.2)."""
        for d in sorted((self.dir / "runs").iterdir()):
            rec = self._load(d.name)
            if rec is None:
                shutil.rmtree(d, ignore_errors=True)
                continue
            if rec["expires_at"] and _parse(rec["expires_at"]) <= self.now():
                shutil.rmtree(d, ignore_errors=True)
            elif rec["state"] in ("queued", "running"):
                for child in d.iterdir():
                    if child.name != "run.json":
                        shutil.rmtree(child, ignore_errors=True) if child.is_dir() else child.unlink()
                rec.update(snapshot_id=None, analysis_outcome="failed", result_available=False)
                self._finish(rec, "failed", "failed", [_reason("process_interrupted", "Tiến trình dừng khi run chưa xong",
                                                               "Tạo run mới; không tự chạy lại")])

    # ---------- admission

    def submit_zip(self, data: bytes, name: str | None = None) -> dict:
        """`name` is a display label from the upload filename (web.zip_label); it never becomes a path."""
        source = {"kind": "zip", "name": name} if name else {"kind": "zip"}
        return self._admit(source, lambda d: (d / "upload.zip").write_bytes(data))

    def submit_github(self, normalized_url: str) -> dict:
        """`normalized_url` comes from web.normalize_github. Nothing is fetched while the run waits (API-001 §2.2)."""
        if self.github is None:
            raise EngineError(503, "engine_unavailable", "Tải source từ GitHub chưa bật: chờ Security review danh sách "
                              "host (API-002 §1)", "Dùng ZIP, hoặc khởi động web với --enable-github sau khi review")
        return self._admit({"kind": "github", "url": normalized_url}, lambda d: None)

    def _admit(self, source: dict, stage_input) -> dict:
        run_id = "run_" + secrets.token_hex(8)
        d = self._path(run_id)
        d.mkdir()
        stage_input(d)
        rec = {"run_id": run_id, "snapshot_id": None, "state": "queued", "stage": "queue", "analysis_outcome": None,
               "created_at": _iso(self.now()), "started_at": None, "finished_at": None, "expires_at": None,
               "result_available": False, "reasons": [], "metrics": dict.fromkeys(METRIC_KEYS), "source": source}
        with self.lock:
            self._save(rec)
            self.queue.append(run_id)
            self.wake.notify()
        return self.view(run_id)

    # ---------- worker

    def step(self) -> bool:
        """Run the oldest queued run to the end. Returns False when the queue is empty."""
        with self.lock:
            if self.busy is not None or not self.queue:
                return False
            run_id = self.queue.popleft()
            self.busy = run_id
        try:
            self._analyse(run_id)
        except Exception as exc:  # last boundary of one run: always end in a terminal state, keep the queue going
            self._fail_unexpected(run_id, exc)
        finally:
            with self.lock:
                self.busy = None
        return True

    def _fail_unexpected(self, run_id, exc):
        d = self._path(run_id)
        for child in d.iterdir():
            if child.name != "run.json":
                shutil.rmtree(child, ignore_errors=True) if child.is_dir() else child.unlink(missing_ok=True)
        self.sources.pop(run_id, None)
        rec = self._load(run_id)
        rec.update(result_available=False, analysis_outcome=rec.get("analysis_outcome") or "failed")
        self._finish(rec, "failed", rec["analysis_outcome"] or "failed", [_reason(
            "internal_error", f"Lỗi nội bộ ở giai đoạn {rec.get('stage') or 'không rõ'}: {type(exc).__name__}",
            "Tạo run mới; nếu lặp lại, gửi run_id cho người bảo trì")])

    def serve_forever(self, stop: threading.Event):
        while not stop.is_set():
            try:
                worked = self.step()
            except Exception:  # e.g. disk error while writing the failed record; try the next run
                worked = True
            if not worked:
                with self.lock:
                    self.wake.wait(timeout=0.5)

    def _over_budget(self, rec, t0) -> bool:
        """NFR-OPS-001: 30 minutes from start, 2 GiB. Leaves the reason in metrics['_budget'] (popped by caller)."""
        peak = self.memory()
        rec["metrics"]["peak_memory_bytes"] = peak
        if self.clock() - t0 > TIME_BUDGET_S:
            rec["metrics"]["_budget"] = _reason("time_budget_exceeded", "Run vượt 30 phút; bỏ các bước còn lại có thể bỏ",
                                                "Xem phần đã xử lý; thu hẹp repository rồi tạo run mới")
            return True
        if peak is not None and peak > MEMORY_BUDGET:
            rec["metrics"]["_budget"] = _reason("memory_budget_exceeded", "Bộ nhớ vượt 2 GiB; bỏ các bước còn lại có thể bỏ",
                                                "Xem phần đã xử lý; thu hẹp repository rồi tạo run mới")
            return True
        return False

    def _stage(self, rec, stage):
        rec["stage"] = stage
        self._save(rec)

    def _analyse(self, run_id):
        rec = self._load(run_id)
        rec.update(state="running", started_at=_iso(self.now()))
        self._stage(rec, "intake")
        d = self._path(run_id)
        t0 = self.clock()
        source = rec.get("source", {"kind": "zip"})
        name = source["url"].rsplit("/", 1)[-1] if source["kind"] == "github" else source.get("name") or "repository"
        try:
            if source["kind"] == "github":
                snap, sources, commit = github.take_github(source["url"], run_id, **self.github)
                rec["source"]["commit"] = commit
            else:
                snap, sources = snapshot.take_zip(d / "upload.zip", run_id)
        except snapshot.IntakeError as exc:
            code = INTAKE_CODES.get(exc.code) or {"INTAKE_LIMIT": "expanded_size_exceeded" if "giải nén" in
                                                  exc.payload["message"] else "file_count_exceeded"}.get(exc.code, "invalid_zip")
            rec["result_available"] = False
            self._finish(rec, "failed", "failed", [_reason(code, exc.payload["message"], exc.payload["action"])])
            return
        finally:
            (d / "upload.zip").unlink(missing_ok=True)
        rec["metrics"]["intake_ms"] = int((self.clock() - t0) * 1000)
        if self._over_budget(rec, t0):
            self._finish(rec, "failed", "failed", [rec["metrics"].pop("_budget")])
            return
        rec["snapshot_id"] = snap["snapshot_id"]
        self._stage(rec, "inventory")
        inv = snapshot.inventory(snap)
        if not inv["units"]:
            self._finish(rec, "failed", "failed", [_reason("analysis_unit_failed", "Không có file .py để phân tích",
                                                           "Kiểm nội dung ZIP")])
            return
        t1 = self.clock()
        self._stage(rec, "extraction")
        unit_id = inv["units"][0]["id"]
        facts = extract.extract(snap, sources, unit_id)
        self._stage(rec, "assembly")
        if self.partition is None:
            self._finish(rec, "failed", "failed", [_reason(
                "partition_policy_unavailable", "Chưa chọn thuật toán chia component (D-03 còn mở)",
                "Chờ chốt D-03; bản này không tự chọn thuật toán")])
            return
        budget = []
        try:
            arch = model.build(snap, unit_id, facts, self.partition(snap))
            rec["metrics"]["static_analysis_ms"] = int((self.clock() - t1) * 1000)
            if self._over_budget(rec, t0):
                budget.append(rec["metrics"].pop("_budget"))
            elif self.model_context is not None:
                tm = self.clock()
                arch = annotate.annotate(arch, facts, snap, self.model_context(run_id, snap, sources))
                rec["metrics"]["model_ms"] = int((self.clock() - tm) * 1000)
                if self._over_budget(rec, t0):
                    budget.append(rec["metrics"].pop("_budget"))
            self._stage(rec, "verification")
            verified = verify.verify(snap, sources, inv, facts, arch)
        except (model.BuildError, VerificationError) as exc:
            self._finish(rec, "failed", "failed", [_reason("analysis_failed", str(exc), "Xem lỗi; tạo run mới")])
            return
        outcome = "partial" if verified["limitations"] or budget else "completed"
        self._stage(rec, "export")
        t2 = self.clock()
        try:
            bundle = render.render(verified, run_id, name, d / "out")
        except render.ExportError as exc:
            rec["result_available"] = False
            self._finish(rec, "failed", outcome, [_reason("export_failed", str(exc), "Tạo run mới")])
            return
        rec["metrics"]["export_ms"] = int((self.clock() - t2) * 1000)
        rec["metrics"]["output_bytes"] = sum(a["bytes"] or 0 for a in bundle["artifacts"] if a["status"] == "ready")
        rec["metrics"]["peak_memory_bytes"] = self.memory()
        self.sources[run_id] = (snap, sources)
        reasons = budget + [_reason(code.lower(), f"Giới hạn {code}") for code in
                            sorted({lim["code"] for lim in verified["limitations"]})]
        if self.partition_note:
            reasons.insert(0, dict(self.partition_note))
        failed = [a for a in bundle["artifacts"] if a["status"] != "ready"]
        reasons += [_reason("artifact_export_failed", f"{a['path']} chưa sinh được",
                            f"Thử lại artifact {a['artifact_id']}" if a["error"]["retryable"] else "Không thử lại được")
                    for a in failed]
        rec["result_available"] = True
        self._finish(rec, "partial" if outcome == "partial" or failed else "completed", outcome, reasons)

    # ---------- reads

    def _record(self, run_id) -> dict:
        rec = self._load(run_id)
        if rec is None:
            raise EngineError(404, "run_not_found", "Không có run này", "Kiểm run_id; dữ liệu có thể đã bị dọn")
        if rec["expires_at"] and _parse(rec["expires_at"]) <= self.now():
            out = self._path(run_id) / "out"
            shutil.rmtree(out, ignore_errors=True)
            self.sources.pop(run_id, None)
            raise EngineError(410, "run_expired", "Run đã quá hạn 24 giờ", "Tạo run mới", run_id)
        return rec

    def _bundle(self, run_id) -> dict:
        return json.loads((self._path(run_id) / "out/manifest.json").read_text(encoding="utf-8"))

    def view(self, run_id) -> dict:
        rec = self._record(run_id)
        artifacts = self._bundle(run_id)["artifacts"] if rec["result_available"] else []
        if self.busy and self.busy[0:2] == ("retry", run_id):
            artifacts = [dict(a, status="retrying") if a["artifact_id"] == self.busy[2] else a for a in artifacts]
        return {**{k: rec[k] for k in ("run_id", "snapshot_id", "state", "stage", "analysis_outcome", "created_at",
                                       "started_at", "finished_at", "expires_at", "result_available", "reasons",
                                       "metrics")},
                "artifacts": artifacts,
                "links": {"self": f"/api/v1/runs/{run_id}",
                          "result": f"/api/v1/runs/{run_id}/result" if rec["result_available"] else None}}

    def result(self, run_id) -> dict:
        rec = self._record(run_id)
        if not rec["result_available"]:
            raise EngineError(409, "result_unavailable", "Run chưa có bundle đã publish", "Poll run; nếu failed đọc lý do",
                              run_id)
        return self._bundle(run_id)

    def evidence(self, run_id, evidence_id) -> dict:
        bundle = self.result(run_id)
        ev = next((e for e in bundle["result"]["evidence_index"] if e["id"] == evidence_id), None)
        if ev is None:
            raise EngineError(404, "evidence_not_found", "Evidence không thuộc run này", "Dùng ID từ bundle của run", run_id)
        held = self.sources.get(run_id)
        if held is None:
            raise EngineError(409, "snapshot_mismatch", "Snapshot của run không còn trong tiến trình",
                              "Chạy phân tích mới để tạo snapshot mới", run_id)
        snap, sources = held
        try:
            verify._check_evidence(snap, sources, ev)
            text = verify._text(sources, ev)
        except VerificationError:
            raise EngineError(409, "snapshot_mismatch", "Snapshot không còn khớp; không thể mở bằng chứng này",
                              "Chạy phân tích mới trên source hiện tại", run_id) from None
        masked = gateway.mask(text)
        return {"run_id": run_id, "snapshot_id": bundle["snapshot_id"], "evidence": ev, "content": masked,
                "redacted": masked != text}

    def artifact(self, run_id, artifact_id) -> tuple[dict, bytes]:
        bundle = self.result(run_id)
        art = next((a for a in bundle["artifacts"] if a["artifact_id"] == artifact_id), None)
        if art is None:
            raise EngineError(404, "artifact_not_found", "Artifact không thuộc run này", "Dùng ID từ manifest", run_id)
        if art["status"] != "ready":
            raise EngineError(409, "artifact_not_ready", "Artifact chưa ready", "Thử lại artifact nếu được phép", run_id)
        data = (self._path(run_id) / "out" / art["path"]).read_bytes()
        if render.sha(data) != art["sha256"]:
            raise EngineError(409, "artifact_not_ready", "File khác hash trong manifest", "Tạo run mới", run_id)
        return art, data

    # ---------- retry

    def retry(self, run_id, artifact_id) -> tuple[int, dict]:
        """Synchronous export task in the single engine slot (API-001 §4, proposal under review)."""
        rec = self._record(run_id)
        with self.lock:
            if self.busy == ("retry", run_id, artifact_id):
                return 202, None
            if rec["state"] not in ("partial", "completed") or not rec["result_available"]:
                raise EngineError(409, "artifact_not_retryable", "Run chưa có bundle đã publish", "Đọc lý do của run", run_id)
            art = next((a for a in self._bundle(run_id)["artifacts"] if a["artifact_id"] == artifact_id), None)
            if art is None:
                raise EngineError(404, "artifact_not_found", "Artifact không thuộc run này", "Dùng ID từ manifest", run_id)
            if art["status"] == "ready":
                return 200, None
            if self.busy is not None:
                raise EngineError(409, "engine_busy", "Engine đang chạy tác vụ khác", "Chờ rồi thử lại", run_id)
            self.busy = ("retry", run_id, artifact_id)
        try:
            render.retry_artifact(self._path(run_id) / "out", artifact_id)
        except render.ExportError as exc:
            raise EngineError(409, "artifact_not_retryable", str(exc)[:500], "Tạo run mới", run_id) from None
        finally:
            with self.lock:
                self.busy = None
        return 200, None
