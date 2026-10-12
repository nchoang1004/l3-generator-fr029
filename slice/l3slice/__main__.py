"""CLI (API-001 §8):

    python -m l3slice [analyze] --source DIR --output DIR --membership FILE [--name NAME] [--llm] [--json]
    python -m l3slice retry --output DIR --artifact ARTIFACT_ID [--json]
    python -m l3slice document --source DIR --output DIR --membership FILE [--archdia FILE] [--diagram FILE]
        (--base-url URL --model NAME --key-env ENV | --script FILE) [--max-turns N] [--max-tokens N] [--json]

Exit code: 0 completed / artifact ready; 2 input, intake or output-place error; 3 partial / artifact still failed;
4 engine could not publish a consistent result or internal error; 130 interrupted (Ctrl-C).
Exit 75 (engine busy) is never returned: the CLI runs the engine in-process, one run per call.
`--json` prints one `CliResult` object on stdout; notices and progress go to stderr.
"""
from __future__ import annotations

import argparse
import getpass
import json
import secrets
import sys
from pathlib import Path

from . import gateway, run
from .engine import METRIC_KEYS, peak_memory
from .model import BuildError
from .render import ExportError, retry_artifact
from .snapshot import IntakeError
from .verify import VerificationError

NOTICE = ("Thông báo l3gen-egress-v1: dữ kiện đã trích, tên symbol, đường dẫn tương đối, vị trí, literal như route path, "
          "chữ ký hàm và đoạn code có giới hạn có thể được gửi tới Groq và Google. Không gửi cả repository hoặc "
          "nguyên file; giá trị giống bí mật được che trước. Bộ lọc bí mật có giới hạn.")
USER_ERRORS = {"OUTPUT_UNSAFE"}  # ExportError codes caused by the chosen output place, not by the engine


def model_context_builder():
    """Keys come from a local prompt without echo (API-001 §5); one ledger for every run of this process, so the
    per-minute windows of a credential are shared (API-006 §4). Capability and free-only records stay empty until
    they are checked against the real provider, so every model task stops before the network for now."""
    print(NOTICE, file=sys.stderr)
    keys = {}
    for provider in ("groq", "google"):
        value = getpass.getpass(f"Khóa {provider} (Enter để bỏ qua): ", stream=sys.stderr)
        if value:
            keys[provider] = gateway.KeyHandle(value)
    ledger = gateway.Ledger()

    def build(run_id, snap, sources):
        return gateway.RunContext(
            run_id=run_id, snapshot_id=snap["snapshot_id"], sources=sources,
            files={f["file_id"]: f for f in snap["files"]},
            disclosure={"snapshot_id": snap["snapshot_id"], "notice_version": "l3gen-egress-v1",
                        "providers": ["groq", "google"]},
            keys=keys, providers={"groq": gateway.GroqHTTP(keys["groq"]) if "groq" in keys else None,
                                  "google": gateway.GeminiHTTP(keys["google"]) if "google" in keys else None},
            capabilities={}, free_only={}, ledger=ledger)
    return build


def _reason(code, message, action):
    return {"code": code, "message": message[:1000], "action": action}


def _result(command, code, run_id=None, bundle=None, output=None, reasons=(), metrics=None):
    """API-001 CliResult."""
    state = outcome = None
    files, out_dir = [], None
    if bundle is not None:
        failed = any(a["status"] != "ready" for a in bundle["artifacts"])
        outcome = "partial" if bundle["result"]["limitations"] else "completed"
        state = "partial" if outcome == "partial" or failed else "completed"
        out_dir = str(output)
        files = [{"artifact_id": a["artifact_id"], "path": a["path"]} for a in bundle["artifacts"] if a["status"] == "ready"]
    elif run_id is not None:
        state, outcome = "failed", "failed"
    return {"schema_version": "0.1.0", "command": command, "exit_code": code, "run_id": run_id, "state": state,
            "analysis_outcome": outcome, "output_directory": out_dir, "files": files, "reasons": list(reasons),
            "metrics": {k: (metrics or {}).get(k) for k in METRIC_KEYS}}


def _emit(as_json, result) -> int:
    if as_json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        for f in result["files"]:
            print(f["path"])
        for r in result["reasons"]:
            print(f"{r['code']}: {r['message']}", file=sys.stderr)
    return result["exit_code"]


def _bundle_reasons(bundle):
    reasons = [_reason(code.lower(), f"Giới hạn {code}", "Xem mục Giới hạn trong README.md")
               for code in sorted({lim["code"] for lim in bundle["result"]["limitations"]})]
    reasons += [_reason("artifact_export_failed", f"{a['path']} chưa sinh được",
                        f"Chạy retry --artifact {a['artifact_id']}" if (a["error"] or {}).get("retryable")
                        else "Artifact này không thử lại được")
                for a in bundle["artifacts"] if a["status"] != "ready"]
    return reasons


def _retry(argv) -> int:
    p = argparse.ArgumentParser(prog="l3slice retry")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--artifact", required=True)
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    output = a.output.resolve()
    try:
        bundle = retry_artifact(output, a.artifact)
    except ExportError as exc:
        code = 4 if exc.code == "PUBLISH_FAILED" else 2
        return _emit(a.json, _result("retry", code, reasons=[_reason(exc.code.lower(), str(exc), "Sửa nguyên nhân rồi thử lại")]))
    except (OSError, ValueError) as exc:
        return _emit(a.json, _result("retry", 2, reasons=[_reason("invalid_output", f"{type(exc).__name__}: {exc}",
                                                                  "Kiểm thư mục output và manifest.json")]))
    except KeyboardInterrupt:
        return _emit(a.json, _result("retry", 130, reasons=[_reason("interrupted", "Người dùng dừng retry",
                                                                    "Chạy lại lệnh retry")]))
    art = next(x for x in bundle["artifacts"] if x["artifact_id"] == a.artifact)
    code = 0 if art["status"] == "ready" else 3
    return _emit(a.json, _result("retry", code, bundle["run_id"], bundle, output, _bundle_reasons(bundle)))


DOC_NOTICE = ("Thông báo fr029-egress-v1: luồng tài liệu FR-029 gửi tới {provider} (model {model}) nội dung các file "
              "trong phạm vi phân tích, theo từng đoạn tối đa 200 dòng, kèm đường dẫn tương đối. Giá trị giống bí mật "
              "được che trước khi gửi; bộ lọc bí mật có giới hạn.")


def _document(argv) -> int:
    """FR-029 agent flow: components, architecture data and diagram are inputs; nothing is drawn or grouped here."""
    from .docagent import Budget, OpenAICompatProvider, ProviderError, ScriptedProvider
    from .docpipeline import InputError, run_documents
    p = argparse.ArgumentParser(prog="l3slice document")
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--membership", type=Path, required=True, help="Component do bước kiến trúc (FR-028) cấp")
    p.add_argument("--archdia", type=Path, help="archdia.json cùng snapshot, để đối chiếu route (AC-04)")
    p.add_argument("--diagram", type=Path, help="Sơ đồ Mermaid do bước kiến trúc cấp, nhúng vào README")
    p.add_argument("--name", help="Tên repository; mặc định là tên thư mục source")
    p.add_argument("--base-url", help="Endpoint dạng OpenAI chat completions")
    p.add_argument("--model")
    p.add_argument("--key-env", help="Tên biến môi trường chứa khóa API")
    p.add_argument("--script", type=Path, help="Chạy lại kịch bản công cụ đã ghi (offline, không gọi model)")
    p.add_argument("--max-turns", type=int, default=200)
    p.add_argument("--max-tokens", type=int, default=2_000_000)
    p.add_argument("--max-context-chars", type=int, default=400_000, help="Rút gọn tin cũ khi lịch sử vượt mức này")
    p.add_argument("--max-output-tokens", type=int, help="Trần token mỗi câu trả lời của model")
    p.add_argument("--reasoning-effort", choices=["low", "medium", "high"])
    p.add_argument("--mode", choices=["agent", "oneshot"], default="agent",
                   help="agent: model đọc qua công cụ; oneshot: gửi toàn bộ source một lần (repo nhỏ, ít request hơn)")
    p.add_argument("--checkpoint", type=Path, help="oneshot: file lưu tiến độ sau mỗi request; chạy lại thì làm tiếp")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    source, output = a.source.resolve(), a.output.resolve()

    def fail(code, reason, message, action):
        return _emit(a.json, _result("document", code, reasons=[_reason(reason, message, action)]))
    if source == output or source in output.parents or output in source.parents:
        return fail(2, "source_output_overlap", "Source và output bao nhau.", "Chọn output nằm ngoài cây source.")
    if not source.is_dir():
        return fail(2, "source_invalid", "Source không phải thư mục đọc được.", "Chỉ định một thư mục source có thật.")
    try:
        if a.script:
            steps = json.loads(a.script.read_text(encoding="utf-8"))
            provider = ScriptedProvider([[(c["name"], c["arguments"]) for c in step] for step in steps])
        elif a.base_url and a.model and a.key_env:
            provider = OpenAICompatProvider(a.base_url, a.model, a.key_env, max_output_tokens=a.max_output_tokens,
                                            reasoning_effort=a.reasoning_effort)
        else:
            return fail(2, "provider_missing", "Cần --script, hoặc đủ --base-url, --model, --key-env.",
                        "Chọn provider rồi chạy lại")
    except ProviderError as exc:
        return fail(2, "provider_invalid", str(exc), "Đặt biến môi trường chứa khóa rồi chạy lại")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return fail(2, "script_invalid", f"{type(exc).__name__}: {exc}", "Kiểm file kịch bản")
    print(DOC_NOTICE.format(provider=provider.name, model=provider.model), file=sys.stderr)
    run_id = "run_" + secrets.token_hex(8)
    try:
        bundle = run_documents(source, output, a.membership.resolve(), a.name or source.name, provider,
                               a.archdia.resolve() if a.archdia else None, a.diagram.resolve() if a.diagram else None,
                               Budget(max_turns=a.max_turns, max_tokens=a.max_tokens,
                                      max_context_chars=a.max_context_chars), run_id, a.mode,
                               a.checkpoint.resolve() if a.checkpoint else None)
    except KeyboardInterrupt:
        return fail(130, "interrupted", "Người dùng dừng lần chạy; không có kết quả được publish", "Chạy lại khi sẵn sàng")
    except (InputError, IntakeError, OSError, json.JSONDecodeError) as exc:
        return fail(2, getattr(exc, "code", "invalid_input").lower(), str(exc)[:1000], "Sửa đầu vào rồi chạy lại")
    except ExportError as exc:
        return fail(2 if exc.code in USER_ERRORS else 4, exc.code.lower(), str(exc)[:1000], "Chọn output khác hoặc báo người bảo trì")
    ready = all(x["status"] == "ready" for x in bundle["artifacts"])
    done = (bundle["agent"]["status"] == "completed" and bundle["coverage"]["complete"] and ready
            and bundle["architecture_parity"]["status"] != "failed")
    result = {"schema_version": "0.1.0", "command": "document", "exit_code": 0 if done else 3, "run_id": run_id,
              "agent": bundle["agent"], "coverage_complete": bundle["coverage"]["complete"],
              "architecture_parity": bundle["architecture_parity"]["status"], "output_directory": str(output),
              "files": [{"artifact_id": x["artifact_id"], "path": x["path"]} for x in bundle["artifacts"] if x["status"] == "ready"],
              "reasons": [_reason(x["code"].lower(), x["message"], "Xem mục Giới hạn trong README.md")
                          for x in bundle["limitations"]]}
    return _emit(a.json, result)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["retry"]:
        return _retry(argv[1:])
    if argv[:1] == ["document"]:
        return _document(argv[1:])
    if argv[:1] == ["analyze"]:
        argv = argv[1:]
    p = argparse.ArgumentParser(prog="l3slice")
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--membership", type=Path, required=True)
    p.add_argument("--name", help="Tên repository; mặc định là tên thư mục source")
    p.add_argument("--llm", action="store_true", help="Chạy bước model (in thông báo, hỏi khóa không hiện chữ)")
    p.add_argument("--json", action="store_true", help="In đúng một object CliResult ra stdout")
    a = p.parse_args(argv)
    source, output = a.source.resolve(), a.output.resolve()
    if source == output or source in output.parents or output in source.parents:
        return _emit(a.json, _result("analyze", 2, reasons=[_reason("source_output_overlap", "Source và output bao nhau.",
                                                                    "Chọn output nằm ngoài cây source.")]))
    if not source.is_dir():
        return _emit(a.json, _result("analyze", 2, reasons=[_reason("source_invalid", "Source không phải thư mục đọc được.",
                                                                    "Chỉ định một thư mục source có thật.")]))
    run_id = "run_" + secrets.token_hex(8)
    metrics = {}
    try:
        build = model_context_builder() if a.llm else None
        bundle = run(source, output, a.membership, a.name or source.name, run_id=run_id,
                     model_context=(lambda snap, src: build(run_id, snap, src)) if build else None, metrics=metrics)
    except KeyboardInterrupt:
        return _emit(a.json, _result("analyze", 130, run_id, reasons=[_reason(
            "interrupted", "Người dùng dừng lần chạy; không có kết quả được publish", "Chạy lại khi sẵn sàng")]))
    except (BuildError, IntakeError, OSError, json.JSONDecodeError) as exc:
        return _emit(a.json, _result("analyze", 2, reasons=[_reason(
            getattr(exc, "code", "invalid_input").lower(), str(exc)[:1000], "Sửa đầu vào rồi chạy lại")]))
    except ExportError as exc:
        code = 2 if exc.code in USER_ERRORS else 4
        return _emit(a.json, _result("analyze", code, run_id if code == 4 else None, reasons=[_reason(
            exc.code.lower(), str(exc)[:1000], "Chọn output khác" if code == 2 else "Báo người bảo trì kèm run_id")]))
    except VerificationError as exc:
        return _emit(a.json, _result("analyze", 4, run_id, reasons=[_reason(exc.code.lower(), str(exc)[:1000],
                                                                            "Báo người bảo trì kèm run_id")]))
    metrics["peak_memory_bytes"] = peak_memory()
    result = _result("analyze", 0, run_id, bundle, output, _bundle_reasons(bundle), metrics)
    result["exit_code"] = 0 if result["state"] == "completed" else 3
    return _emit(a.json, result)


if __name__ == "__main__":
    sys.exit(main())
