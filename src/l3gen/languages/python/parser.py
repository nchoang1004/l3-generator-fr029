"""Bước 1 và 2: liệt kê file .py và đọc cây cú pháp.

Chỉ đọc file như văn bản. Không bao giờ import hay chạy code của repo đang phân
tích (SPEC mục 3.2) — vì nạp một file lạ vào bộ nhớ có thể vô tình kích hoạt kết
nối database thật hoặc gọi API thật.
"""

import ast
from dataclasses import dataclass
from pathlib import Path

DEFAULT_EXCLUDES = (
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "node_modules",
    "build",
    "dist",
    "tests",
)


@dataclass
class ParsedFile:
    """Một file đã đọc được cây cú pháp."""

    rel_path: str
    tree: ast.Module
    line_count: int


@dataclass
class FailedFile:
    """Một file không đọc được cây cú pháp. Bỏ qua file này, không dừng cả lần chạy."""

    rel_path: str
    error_message: str


def scan(root: Path, excludes: tuple[str, ...] = DEFAULT_EXCLUDES) -> list[Path]:
    """Liệt kê mọi file .py dưới root, bỏ những file nằm trong thư mục bị loại.

    Kết quả sắp xếp theo tên để hai lần chạy cho cùng thứ tự.
    """
    excluded = set(excludes)
    found = []
    for path in root.rglob("*.py"):
        if excluded.isdisjoint(path.relative_to(root).parts[:-1]):
            found.append(path)
    return sorted(found)


def parse_all(paths: list[Path], root: Path) -> tuple[list[ParsedFile], list[FailedFile]]:
    """Đọc cây cú pháp từng file. File lỗi cú pháp được ghi lại chứ không làm dừng."""
    parsed: list[ParsedFile] = []
    failed: list[FailedFile] = []

    for path in paths:
        rel_path = path.relative_to(root).as_posix()
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            failed.append(FailedFile(rel_path, f"không đọc được file: {exc}"))
            continue

        try:
            tree = ast.parse(source, filename=rel_path)
        except SyntaxError as exc:
            failed.append(FailedFile(rel_path, f"lỗi cú pháp dòng {exc.lineno}: {exc.msg}"))
            continue
        except (RecursionError, ValueError) as exc:
            failed.append(FailedFile(rel_path, f"parser không đọc được cấu trúc: {exc}"))
            continue

        parsed.append(ParsedFile(rel_path, tree, source.count("\n") + 1))

    return parsed, failed
