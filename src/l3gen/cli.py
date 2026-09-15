"""Điểm vào dòng lệnh (SPEC mục 4.2, 4.3).

Nguyên tắc xử lý lỗi: không bao giờ in traceback cho lỗi đã lường trước được.
Mọi thông báo phải nói rõ chuyện gì xảy ra và làm gì tiếp theo.

Mã thoát: 0 thành công, 1 lỗi đầu vào, 2 lỗi không lường trước.
"""

import argparse
import os
import sys
from pathlib import Path

from l3gen import __version__
from l3gen.languages.python.parser import DEFAULT_EXCLUDES
from l3gen.pipeline import EmptyInputError, Result, analyze, write_outputs

API_KEY_VARS = ("L3GEN_API_KEY", "ANTHROPIC_API_KEY")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="l3gen",
        description="Sinh tài liệu kiến trúc L3 từ source code Python/FastAPI.",
    )
    parser.add_argument("source", type=Path, help="thư mục chứa source code cần phân tích")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("./l3-output"),
        help="nơi ghi kết quả (mặc định: ./l3-output)",
    )
    parser.add_argument(
        "--no-ai", action="store_true", help="chạy thuần phân tích tĩnh, không gọi AI"
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=None,
        metavar="TÊN",
        help=f"thư mục bỏ qua, lặp lại được (mặc định: {', '.join(DEFAULT_EXCLUDES)})",
    )
    parser.add_argument(
        "--fail-on-empty",
        action="store_true",
        help="thoát với mã lỗi nếu không tìm thấy route hay bảng dữ liệu nào",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="in chi tiết hơn")
    parser.add_argument("--version", action="version", version=f"l3gen {__version__}")
    return parser


def resolve_ai_enabled(no_ai: bool) -> bool:
    """Quyết định có dùng AI không, và nói rõ lý do nếu không.

    Thiếu API key thì tự chạy chế độ tĩnh chứ không dừng (SPEC mục 4.3).
    """
    if no_ai:
        return False
    if not any(os.environ.get(var) for var in API_KEY_VARS):
        print(
            "Cảnh báo: chưa cấu hình API key — đang chạy chế độ phân tích tĩnh.\n"
            f"         Tài liệu sẽ không có mô tả do AI viết. Đặt {API_KEY_VARS[0]} để bật.",
            file=sys.stderr,
        )
        return False
    return True


def report(result: Result, written: list[Path], verbose: bool) -> None:
    iam = result.iam
    metrics = iam.metrics
    stack = iam.detected_stack

    for service in stack.services:
        name = service.name or "(thư mục gốc)"
        if service.analyzed:
            frameworks = ", ".join(service.frameworks) or "chưa rõ framework"
            print(
                f"  [phân tích] {name} — {service.language}, {frameworks}, "
                f"{service.file_count} file"
            )
        else:
            print(f"  [bỏ qua]    {name} — {service.skip_reason}")

    print(
        f"\nĐã đọc {metrics.files_analyzed}/{metrics.files_found} file Python "
        f"({metrics.lines_of_code:,} dòng) trong {metrics.duration_seconds:.2f} giây."
    )
    print(
        f"Phát hiện: {len(iam.routes)} route, {len(iam.entities)} bảng dữ liệu, "
        f"{len(iam.external_calls)} lời gọi ra ngoài, {len(iam.functions)} hàm."
    )
    print(f"Graph: {len(result.graph.nodes)} node, {len(result.graph.edges)} cạnh.")

    if iam.parse_errors:
        print(f"\n{len(iam.parse_errors)} file bỏ qua vì lỗi cú pháp:")
        shown = iam.parse_errors if verbose else iam.parse_errors[:5]
        for error in shown:
            print(f"  - {error.file}: {error.error_message}")
        if len(shown) < len(iam.parse_errors):
            print(f"  ... còn {len(iam.parse_errors) - len(shown)} file nữa, dùng -v để xem hết")

    print("\nĐã ghi:")
    for path in written:
        print(f"  {path}")


def run_ui(argv: list[str]) -> int:
    """`l3gen ui <thư-mục-output>` — SPEC mục 13.2.

    Import muộn có chủ ý: xoá cả thư mục `l3gen/ui/` thì lệnh phân tích vẫn chạy
    bình thường, chỉ lệnh này báo thiếu (SPEC mục 13.1 ràng buộc 2).
    """
    parser = argparse.ArgumentParser(
        prog="l3gen ui", description="Mở giao diện web xem kết quả đã sinh."
    )
    parser.add_argument("output", type=Path, help="thư mục kết quả do l3gen sinh ra")
    parser.add_argument(
        "-p", "--port", type=int, default=8000, help="cổng khởi đầu (mặc định: 8000)"
    )
    parser.add_argument(
        "--no-browser", action="store_true", help="không tự mở trình duyệt"
    )
    args = parser.parse_args(argv)

    try:
        from l3gen.ui.server import serve
    except ImportError:
        print(
            "Lỗi: không tìm thấy phần giao diện web (l3gen/ui/).\n"
            "     Lệnh phân tích `l3gen <đường-dẫn>` không bị ảnh hưởng.",
            file=sys.stderr,
        )
        return 1
    return serve(args.output, args.port, not args.no_browser)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "ui":
        return run_ui(argv[1:])

    args = build_parser().parse_args(argv)

    root = args.source
    if not root.is_dir():
        print(f"Lỗi: không tìm thấy thư mục '{root}'.", file=sys.stderr)
        return 1

    excludes = tuple(args.exclude) if args.exclude else DEFAULT_EXCLUDES
    ai_enabled = resolve_ai_enabled(args.no_ai)

    try:
        result = analyze(root.resolve(), excludes, ai_enabled)
        written = write_outputs(result, args.output)
    except EmptyInputError as exc:
        print(
            f"Lỗi: {exc.message}\n"
            f"     Đã bỏ qua các thư mục: {', '.join(excludes)}.\n"
            f"     Dùng --exclude để đổi danh sách này.",
            file=sys.stderr,
        )
        return 1
    except Exception as exc:  # noqa: BLE001 - không để traceback lọt ra màn hình
        print(f"Lỗi không lường trước: {exc}", file=sys.stderr)
        return 2

    report(result, written, args.verbose)

    if args.fail_on_empty and not result.iam.routes and not result.iam.entities:
        print(
            "\nKhông phát hiện route hay bảng dữ liệu nào (--fail-on-empty).",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
