"""Kiểm tra toàn bộ đường chạy: chia service, gộp IAM, dựng graph, ghi file."""

from pathlib import Path

import pytest

from l3gen.cli import main
from l3gen.languages.python.parser import DEFAULT_EXCLUDES, parse_all, scan
from l3gen.pipeline import EmptyInputError, analyze, write_outputs

FIXTURES = Path(__file__).parents[1] / "fixtures"
SAMPLE_APP = FIXTURES / "python" / "fastapi" / "sample_app"
MULTI_SERVICE = FIXTURES / "detection" / "multi_service"

DETERMINISTIC_FILES = ("IAM.json", "graph.json", "diagram.mmd")
"""File phải giống hệt từng byte qua hai lần chạy.

L3.md không nằm ở đây vì nó in thời điểm và thời lượng chạy — SPEC mục 0.2 nói rõ
hai thứ đó không tính vào yêu cầu lặp lại được.
"""


def run(root: Path):
    return analyze(root, DEFAULT_EXCLUDES, ai_enabled=False)


# --- quét và đọc cây cú pháp --------------------------------------------

def test_quet_bo_qua_thu_muc_bi_loai(tmp_path):
    (tmp_path / "app").mkdir()
    (tmp_path / "app" / "main.py").write_text("x = 1")
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "lib.py").write_text("y = 2")

    assert [p.name for p in scan(tmp_path, DEFAULT_EXCLUDES)] == ["main.py"]


def test_thu_tu_quet_on_dinh_giua_hai_lan_chay():
    assert scan(SAMPLE_APP, DEFAULT_EXCLUDES) == scan(SAMPLE_APP, DEFAULT_EXCLUDES)


def test_file_loi_cu_phap_bi_bo_qua_khong_lam_dung():
    paths = scan(SAMPLE_APP, DEFAULT_EXCLUDES)
    parsed, failed = parse_all(paths, SAMPLE_APP)

    assert [f.rel_path for f in failed] == ["app/broken.py"]
    assert len(parsed) == len(paths) - 1


# --- bất biến của số liệu ------------------------------------------------

def test_bat_bien_cua_so_lieu():
    metrics = run(SAMPLE_APP).iam.metrics

    assert metrics.files_found == metrics.files_analyzed + metrics.files_skipped
    assert metrics.is_partial is True
    assert metrics.ai_enabled is False


def test_thu_muc_khong_co_source_bao_loi_ro_rang(tmp_path):
    with pytest.raises(EmptyInputError):
        run(tmp_path)


# --- chia service --------------------------------------------------------

def test_repo_nhieu_service_van_phan_tich_phan_lam_duoc():
    """Java + FastAPI trong cùng repo: bỏ qua riêng Java, không bỏ cả repo."""
    stack = run(MULTI_SERVICE).iam.detected_stack
    by_name = {s.name: s for s in stack.services}

    assert by_name["ai-service"].analyzed is True
    assert by_name["ai-service"].frameworks == ["fastapi"]
    assert by_name["mobile-app"].analyzed is False
    assert "java" in by_name["mobile-app"].skip_reason


def test_don_vi_bi_bo_qua_van_xuat_hien_trong_tai_lieu(tmp_path):
    """Im lặng bỏ qua một service là kiểu thất bại tệ nhất."""
    result = run(MULTI_SERVICE)
    write_outputs(result, tmp_path)

    document = (tmp_path / "L3.md").read_text(encoding="utf-8")
    assert "mobile-app" in document
    assert "Bỏ qua" in document


def test_moi_thuc_the_deu_biet_minh_thuoc_service_nao():
    iam = run(MULTI_SERVICE).iam
    assert {r.service for r in iam.routes} == {"ai-service"}


# --- graph ---------------------------------------------------------------

def test_graph_khong_them_thong_tin_ngoai_iam():
    """Mọi node Route trong graph phải ứng đúng một route trong IAM."""
    result = run(SAMPLE_APP)
    route_nodes = [n for n in result.graph.nodes if n.type == "Route"]

    assert len(route_nodes) == len(result.iam.routes)


def test_tham_chieu_chua_noi_duoc_van_co_node_rieng():
    """Không được âm thầm loại khỏi graph (SPEC mục 5.2)."""
    result = run(SAMPLE_APP)
    unresolved = [n for n in result.graph.nodes if n.type == "Unresolved"]

    assert unresolved
    assert all(n.location is not None for n in unresolved)


def test_id_node_duy_nhat():
    result = run(SAMPLE_APP)
    ids = [n.id for n in result.graph.nodes]

    assert len(ids) == len(set(ids))


def test_route_noi_duoc_xuong_bang_du_lieu():
    """POST /orders/{id}/confirm -> OrderService.confirm -> bảng orders."""
    result = run(SAMPLE_APP)
    reads = [e for e in result.graph.edges if e.type == "reads_writes"]

    assert reads
    assert any("Order" in e.target_id for e in reads)


# --- chạy hai lần cho kết quả giống hệt ----------------------------------

def test_chay_hai_lan_ra_file_giong_het(tmp_path):
    for name in ("run1", "run2"):
        write_outputs(run(SAMPLE_APP), tmp_path / name)

    for filename in DETERMINISTIC_FILES:
        first = (tmp_path / "run1" / filename).read_bytes()
        second = (tmp_path / "run2" / filename).read_bytes()
        assert first == second, f"{filename} khác nhau giữa hai lần chạy"


# --- lệnh dòng lệnh ------------------------------------------------------

def test_lenh_chay_xong_tra_ve_0(tmp_path, capsys):
    code = main([str(SAMPLE_APP), "--no-ai", "-o", str(tmp_path)])
    capsys.readouterr()

    assert code == 0
    assert (tmp_path / "L3.md").exists()


def test_thu_muc_khong_ton_tai_tra_ve_1_khong_co_traceback(tmp_path, capsys):
    code = main([str(tmp_path / "khong-co"), "--no-ai"])
    captured = capsys.readouterr()

    assert code == 1
    assert "Traceback" not in captured.err
    assert "không tìm thấy thư mục" in captured.err
