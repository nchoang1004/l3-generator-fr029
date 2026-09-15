"""Lệnh `l3gen ui <thư-mục-output>` — mở giao diện web xem kết quả.

Vì sao cần một máy chủ mà không mở thẳng file HTML: trình duyệt chặn `fetch`
trên giao thức `file://`, nên trang không đọc được `IAM.json`. Máy chủ ở đây chỉ
đưa file tĩnh ra, không có xử lý gì phía sau.

Các file giao diện được chép vào `<output>/ui/` để cả thư mục output mang đi đâu
cũng xem được, không phụ thuộc chỗ cài công cụ.
"""

import shutil
import socket
import sys
import threading
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"
DEFAULT_PORT = 8000
MAX_PORT_TRIES = 20

REQUIRED = "IAM.json"
OPTIONAL = ("graph.json", "findings.json", "descriptions.json")


class _QuietHandler(SimpleHTTPRequestHandler):
    """Giống SimpleHTTPRequestHandler nhưng không in log mỗi lần tải file."""

    def log_message(self, format, *args):  # noqa: A002 - giữ nguyên chữ ký của lớp cha
        pass


def _free_port(start: int) -> int:
    """Tìm cổng trống, bắt đầu từ `start`. Máy nào cũng có thể đã chiếm 8000."""
    for port in range(start, start + MAX_PORT_TRIES):
        with socket.socket() as probe:
            try:
                probe.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise OSError(f"không còn cổng trống trong khoảng {start}-{start + MAX_PORT_TRIES}")


def install_assets(output_dir: Path) -> Path:
    """Chép file giao diện vào <output>/ui/. Ghi đè để luôn khớp phiên bản công cụ."""
    target = output_dir / "ui"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(ASSETS, target)
    return target


def serve(output_dir: Path, port: int = DEFAULT_PORT, open_browser: bool = True) -> int:
    """Chạy máy chủ tĩnh cho thư mục output. Trả về mã thoát."""
    if not output_dir.is_dir():
        print(f"Lỗi: không tìm thấy thư mục '{output_dir}'.", file=sys.stderr)
        return 1

    if not (output_dir / REQUIRED).is_file():
        print(
            f"Lỗi: '{output_dir}' không có {REQUIRED}, đây không phải thư mục kết quả.\n"
            f"     Chạy `l3gen <đường-dẫn-source> -o {output_dir}` trước.",
            file=sys.stderr,
        )
        return 1

    missing = [name for name in OPTIONAL if not (output_dir / name).is_file()]
    if missing:
        print(f"Ghi chú: thư mục này không có {', '.join(missing)}.")
        print("         Giao diện sẽ nói rõ phần nào thiếu thay vì để màn hình trống.")

    install_assets(output_dir)

    try:
        port = _free_port(port)
    except OSError as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 1

    handler = partial(_QuietHandler, directory=str(output_dir))
    url = f"http://127.0.0.1:{port}/ui/index.html"

    with ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        print(f"Đang phục vụ {output_dir.resolve()}")
        print(f"Mở: {url}")
        print("Bấm Ctrl+C để dừng.")
        if open_browser:
            threading.Timer(0.4, webbrowser.open, args=(url,)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã dừng.")
    return 0
