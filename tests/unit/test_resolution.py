"""Kiểm tra việc nối tham chiếu — phần khó nhất của dự án (SPEC mục 15).

Mỗi test tương ứng một fixture, khoá lại đúng một cách sai dễ mắc.
"""

from pathlib import Path

import pytest

from l3gen.core.resolution.inheritance import MAX_DEPTH
from l3gen.languages.python.common.callgraph import calls_inside
from l3gen.languages.python.parser import DEFAULT_EXCLUDES, parse_all, scan
from l3gen.languages.python.resolution import FUNCTION_NODES, build_resolver, is_external

FIXTURES = Path(__file__).parents[1] / "fixtures" / "python"


def load(fixture_dir: Path):
    parsed, _ = parse_all(scan(fixture_dir, DEFAULT_EXCLUDES), fixture_dir)
    resolver, _ = build_resolver(parsed)
    return {p.rel_path: p for p in parsed}, resolver


def refs_in(files, resolver, rel_path: str, func_name: str):
    tree = files[rel_path].tree
    func = next(
        n for n in tree.body if isinstance(n, FUNCTION_NODES) and n.name == func_name
    )
    scope = resolver.tables.for_file(rel_path)
    return {r.name: r for r in calls_inside(func, scope, resolver)}


# --- fixture 6: gọi hàm xuyên file ---------------------------------------

def test_fixture_6_goi_ham_o_file_khac():
    files, resolver = load(FIXTURES / "fastapi" / "fixture_6_cross_file_call")
    refs = refs_in(files, resolver, "handler.py", "handle")

    assert refs["svc.create"].resolved is True
    assert refs["svc.create"].resolved_module == "service.py"
    assert refs["svc.create"].confidence == "exact"


def test_fixture_6_import_thu_vien_ngoai_khong_bi_coi_la_loi():
    files, resolver = load(FIXTURES / "fastapi" / "fixture_6_cross_file_call")
    ref = refs_in(files, resolver, "handler.py", "handle")["os.getenv"]

    assert ref.resolved is False
    assert ref.resolved_module is None
    assert ref.confidence is None
    assert ref.completeness == "partial"
    assert is_external(ref)


# --- fixture 7: kế thừa xuyên file ---------------------------------------

def test_fixture_7_ke_thua_xuyen_file():
    _, resolver = load(FIXTURES / "fastapi" / "fixture_7_cross_file_inherit")
    result = resolver.find_method("entity.Order", "touch")

    assert result.owner is not None
    assert result.owner.qualified_name == "base.TimestampedBase"
    assert result.owner.rel_path == "base.py"


# --- fixture 8: cùng tên, khác module (lỗi nguy hiểm nhất) ---------------

@pytest.mark.parametrize(
    ("caller", "expected_file"),
    [("caller_modern.py", "modern.py"), ("caller_legacy.py", "legacy.py")],
)
def test_fixture_8_cung_ten_class_nhung_khac_module(caller, expected_file):
    """Hai file cùng dùng tên OrderService nhưng lấy từ hai module khác nhau.

    Nếu dùng một bảng tên gọi chung cho cả repo thì cả hai sẽ trỏ về cùng một
    file — graph vẫn đẹp, test khác vẫn qua, và không cách nào phát hiện.
    """
    files, resolver = load(FIXTURES / "resolution" / "fixture_8_same_name_diff_module")
    ref = refs_in(files, resolver, caller, "run")["svc.create"]

    assert ref.resolved is True
    assert ref.resolved_module == expected_file


# --- fixture 9: kế thừa sâu 3 tầng qua 3 file ----------------------------

def test_fixture_9_leo_ba_tang_ke_thua():
    _, resolver = load(FIXTURES / "resolution" / "fixture_9_deep_inheritance")
    result = resolver.find_method("c.Level1", "deep")

    assert result.owner is not None
    assert result.owner.rel_path == "a.py"
    assert result.ambiguous is False


# --- fixture 10: class cha thuộc thư viện ngoài --------------------------

def test_fixture_10_class_cha_ngoai_repo_la_ket_qua_dung_khong_phai_loi():
    _, resolver = load(FIXTURES / "resolution" / "fixture_10_external_base")
    result = resolver.find_method("model.User", "model_dump")

    assert result.owner is None
    assert "ngoài repo" in result.reason


# --- fixture 11: kế thừa vòng --------------------------------------------

def test_fixture_11_ke_thua_vong_khong_lam_treo_tool():
    _, resolver = load(FIXTURES / "resolution" / "fixture_11_circular_inherit")
    result = resolver.find_method("a.A", "khong_ton_tai")

    assert result.owner is None
    assert result.reason is not None


# --- fixture 12: đa kế thừa ----------------------------------------------

def test_fixture_12_da_ke_thua_lay_cha_khai_bao_truoc():
    _, resolver = load(FIXTURES / "resolution" / "fixture_12_multiple_inherit")
    result = resolver.find_method("model.Record", "save")

    assert result.owner is not None
    assert result.owner.qualified_name == "mixins.Loggable"
    assert result.ambiguous is True
    assert "nhiều class cha" in result.reason


# --- ví dụ 4 file trong plan ---------------------------------------------

def test_vi_du_trong_plan_noi_duoc_svc_confirm():
    """Ca chính của plan: svc.confirm() -> app/services/order.py.

    Đi qua đủ bốn bước: chú thích kiểu -> bảng tên gọi -> danh bạ -> tìm method.
    """
    files, resolver = load(FIXTURES / "fastapi" / "sample_app")
    ref = refs_in(files, resolver, "app/api/orders.py", "confirm_order")["svc.confirm"]

    assert ref.resolved is True
    assert ref.resolved_module == "app/services/order.py"
    assert ref.confidence == "exact"


def test_decorator_khong_bi_tinh_la_loi_goi_trong_than_ham():
    """@router.post(...) là khai báo route, không phải lời gọi khi hàm chạy."""
    files, resolver = load(FIXTURES / "fastapi" / "sample_app")
    names = refs_in(files, resolver, "app/api/orders.py", "confirm_order").keys()

    assert "router.post" not in names
    assert "Depends" not in names


def test_gioi_han_do_sau_ke_thua_la_muoi_tang():
    assert MAX_DEPTH == 10


# --- fixture 13: bí danh kiểu (phát sinh thêm ngoài 12 fixture ban đầu) ---

def test_fixture_13_di_theo_bi_danh_kieu_toi_class_trong_repo():
    """`RepoDep = Annotated[OrderRepository, Depends(get_repo)]` — idiom FastAPI
    hiện đại. Không đi theo bí danh thì mọi lời gọi trên biến đó đều mất."""
    files, resolver = load(FIXTURES / "resolution" / "fixture_13_type_alias")
    ref = refs_in(files, resolver, "routes.py", "create_order")["repo.save"]

    assert ref.resolved is True
    assert ref.resolved_module == "repo.py"


def test_fixture_13_bi_danh_toi_class_ngoai_repo_bao_dung_la_thu_vien_ngoai():
    """`SessionDep = Annotated[Session, ...]` với Session của sqlmodel.

    Phải nói "gọi ra thư viện ngoài", KHÔNG được nói "không biết session là gì" —
    ta biết chính xác nó là gì, chỉ là không đọc được bên trong.
    """
    files, resolver = load(FIXTURES / "resolution" / "fixture_13_type_alias")
    ref = refs_in(files, resolver, "routes.py", "create_order")["session.commit"]

    assert ref.resolved is False
    assert is_external(ref)
