"""Khoá ranh giới giữa giao diện web và lõi (SPEC mục 13.1, 13.6).

Giao diện là lớp phủ. Ba điều dưới đây là chỗ dễ vi phạm nhất khi thêm tính năng:
lõi lỡ import từ `ui/`, giao diện lỡ dùng thư viện trên mạng, hoặc giao diện tự
đọc source thay vì đọc file JSON đã sinh.
"""

import ast
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).parents[2]
SRC = REPO / "src" / "l3gen"
UI = SRC / "ui"
ASSETS = UI / "assets"
SAMPLE_APP = REPO / "tests" / "fixtures" / "python" / "fastapi" / "sample_app"

CORE_OUTPUT = ("L3.md", "diagram.mmd", "graph.json", "IAM.json", "findings.json")


def _core_modules():
    """Mọi file .py của gói, trừ chính thư mục giao diện."""
    return [p for p in SRC.rglob("*.py") if UI not in p.parents and p.parent != UI]


def test_loi_khong_import_gi_tu_ui():
    """Lõi không được phụ thuộc lên giao diện — nếu có thì xoá ui/ sẽ làm sập lõi.

    Ngoại lệ duy nhất là `cli.py`, và ở đó phải là import muộn nằm trong hàm,
    không phải import ở đầu file.
    """
    offenders = []
    for path in _core_modules():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            module = None
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
            elif isinstance(node, ast.Import):
                module = " ".join(a.name for a in node.names)
            if module and "l3gen.ui" in module:
                top_level = any(node is stmt for stmt in tree.body)
                if path.name != "cli.py" or top_level:
                    offenders.append(f"{path.relative_to(REPO)}:{node.lineno}")
    assert offenders == [], f"lõi đang import từ l3gen.ui: {offenders}"


def test_xoa_thu_muc_ui_thi_lenh_phan_tich_van_chay(tmp_path):
    """SPEC mục 13.6 tiêu chí 1: xoá cả giao diện thì output không đổi một byte."""
    before = tmp_path / "before"
    after = tmp_path / "after"
    run = [sys.executable, "-m", "l3gen.cli", str(SAMPLE_APP), "--no-ai", "-o"]

    assert subprocess.run([*run, str(before)], cwd=REPO, capture_output=True).returncode == 0

    moved = tmp_path / "ui_backup"
    shutil.move(str(UI), str(moved))
    try:
        done = subprocess.run([*run, str(after)], cwd=REPO, capture_output=True)
    finally:
        shutil.move(str(moved), str(UI))

    assert done.returncode == 0, done.stderr.decode("utf-8", "replace")
    for name in CORE_OUTPUT:
        assert (before / name).read_bytes() == (after / name).read_bytes(), name


def test_giao_dien_khong_goi_ra_mang():
    """SPEC mục 13.5: mở được khi ngắt mạng, nên không được có CDN hay font ngoài."""
    # w3.org/2000/svg là chuỗi định danh namespace của SVG, trình duyệt không tải
    # gì từ đó. Mọi địa chỉ khác đều là vi phạm.
    allowed = {"http://www.w3.org/2000/svg"}
    pattern = re.compile(r"https?://[^\s'\"()]+")
    found = set()
    for path in ASSETS.iterdir():
        for url in pattern.findall(path.read_text(encoding="utf-8")):
            if url not in allowed and not url.startswith("http://127.0.0.1"):
                found.add(f"{path.name}: {url}")
    assert found == set(), f"giao diện đang trỏ ra ngoài: {sorted(found)}"

    for path in ASSETS.iterdir():
        text = path.read_text(encoding="utf-8")
        assert "@import url(" not in text, f"{path.name} nạp CSS từ nơi khác"


def test_giao_dien_chi_doc_file_json_da_sinh():
    """SPEC mục 13.1: giao diện không bao giờ tự phân tích source."""
    js = (ASSETS / "app.js").read_text(encoding="utf-8")
    fetched = set(re.findall(r"fetch\(\s*'([^']*)'|loadJSON\('([^']+)'", js))
    names = {a or b for a, b in fetched}
    names.discard("../")
    allowed = {"IAM.json", "graph.json", "findings.json", "descriptions.json", "run.json"}
    assert names <= allowed, f"giao diện đang đọc file lạ: {sorted(names - allowed)}"


@pytest.mark.parametrize("name", ["index.html", "style.css", "app.js"])
def test_du_file_giao_dien(name):
    assert (ASSETS / name).is_file()


def test_man_gioi_han_luon_hien_ke_ca_khi_rong():
    """SPEC mục 13.4 cấm ẩn mục Giới hạn đã biết khi không có giới hạn nào."""
    js = (ASSETS / "app.js").read_text(encoding="utf-8")
    assert "Không có giới hạn nào được ghi nhận trong lần chạy này." in js
