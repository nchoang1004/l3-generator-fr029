"""Kiểm tra ba bộ trích xuất: route, bảng dữ liệu, gọi ra ngoài."""

from pathlib import Path

from l3gen.languages.python.frameworks.fastapi.external import extract_external_calls
from l3gen.languages.python.frameworks.fastapi.routes import extract_routes
from l3gen.languages.python.parser import DEFAULT_EXCLUDES, parse_all, scan
from l3gen.languages.python.resolution import build_resolver
from l3gen.orm.sqlalchemy import extract_entities

FIXTURES = Path(__file__).parents[1] / "fixtures" / "python" / "fastapi"


def analyze(fixture_name: str):
    root = FIXTURES / fixture_name
    parsed, failed = parse_all(scan(root, DEFAULT_EXCLUDES), root)
    resolver, module_of = build_resolver(parsed)
    return parsed, failed, resolver, module_of


def routes_of(fixture_name: str):
    parsed, _, resolver, module_of = analyze(fixture_name)
    return extract_routes(parsed, resolver, module_of, "test")


def entities_of(fixture_name: str):
    parsed, _, resolver, module_of = analyze(fixture_name)
    return extract_entities(parsed, resolver, module_of, "test")


# --- fixture 1: route khai báo thẳng trên FastAPI() ----------------------

def test_fixture_1_route_don_gian():
    routes, dropped = routes_of("fixture_1_simple_route")

    assert [(r.method, r.path) for r in routes] == [
        ("GET", "/orders"),
        ("POST", "/orders"),
    ]
    assert all(r.confidence == "exact" and r.completeness == "full" for r in routes)
    assert dropped == []


# --- fixture 2: router lồng ba tầng, một tầng prefix là biến -------------

def test_fixture_2_ghep_prefix_ba_tang():
    """app(/v1) -> api_router(settings.API_PREFIX) -> items_router(/items) -> /{item_id}"""
    routes, _ = routes_of("fixture_2_nested_router")

    assert len(routes) == 1
    assert routes[0].path == "/v1/{settings.API_PREFIX}/items/{item_id}"


def test_fixture_2_prefix_la_bien_thi_route_van_exact_nhung_partial():
    """Route có thật (exact) nhưng đường dẫn chưa đủ (partial) — SPEC mục 5.1."""
    routes, _ = routes_of("fixture_2_nested_router")

    assert routes[0].confidence == "exact"
    assert routes[0].completeness == "partial"
    assert "settings.API_PREFIX" in routes[0].reason


# --- fixture 3: bảng SQLAlchemy ------------------------------------------

def test_fixture_3_doc_khoa_chinh_va_khoa_ngoai():
    parsed, _, resolver, module_of = analyze("fixture_3_sqlalchemy_entity")
    entities = {e.class_name: e for e in extract_entities(parsed, resolver, module_of, "test")}

    order = entities["Order"]
    assert order.table_name == "orders"
    assert order.confidence == "exact"
    columns = {c.name: c for c in order.columns}
    assert columns["id"].is_primary_key is True
    assert columns["customer_id"].foreign_key_ref == "customers.id"


def test_fixture_3_ten_bang_ghep_tu_bien_thi_partial():
    parsed, _, resolver, module_of = analyze("fixture_3_sqlalchemy_entity")
    entities = {e.class_name: e for e in extract_entities(parsed, resolver, module_of, "test")}

    invoice = entities["Invoice"]
    assert invoice.completeness == "partial"
    assert invoice.table_name == "{TABLE_PREFIX}invoices"
    assert "TABLE_PREFIX" in invoice.reason


# --- fixture 7: bảng kế thừa qua class trung gian ở file khác ------------

def test_fixture_7_nhan_ra_bang_qua_class_trung_gian_o_file_khac():
    """Order kế thừa TimestampedBase (file khác), chính nó mới kế thừa Base."""
    parsed, _, resolver, module_of = analyze("fixture_7_cross_file_inherit")
    entities = extract_entities(parsed, resolver, module_of, "test")

    assert [e.class_name for e in entities] == ["Order"]
    assert entities[0].base_class.resolved is True
    assert entities[0].base_class.resolved_module == "base.py"


def test_class_trung_gian_danh_dau_abstract_khong_bi_coi_la_bang():
    parsed, _, resolver, module_of = analyze("fixture_7_cross_file_inherit")
    entities = extract_entities(parsed, resolver, module_of, "test")

    assert "TimestampedBase" not in [e.class_name for e in entities]


# --- fixture 4: gọi HTTP ra ngoài ----------------------------------------

def test_fixture_4_nhan_ra_httpx_va_requests():
    parsed, _, resolver, module_of = analyze("fixture_4_external_call")
    calls = extract_external_calls(parsed, resolver, module_of, "test")

    found = {(c.http_method, c.url_or_host) for c in calls}
    assert ("GET", "https://api.payment.com/charge") in found
    assert ("PUT", "https://hooks.internal/notify") in found


def test_fixture_4_url_ghep_tu_bien_giu_nguyen_ten_bien():
    """KHÔNG được đoán giá trị thật của settings.PAYMENT_URL."""
    parsed, _, resolver, module_of = analyze("fixture_4_external_call")
    calls = {c.url_or_host: c for c in extract_external_calls(parsed, resolver, module_of, "t")}

    call = calls["{settings.PAYMENT_URL}/charge"]
    assert call.completeness == "partial"
    assert call.http_method == "POST"


# --- fixture 5: file lỗi cú pháp không kéo sập phần còn lại --------------

def test_fixture_5_file_loi_cu_phap_khong_lam_mat_route_o_file_khac():
    parsed, failed, resolver, module_of = analyze("fixture_5_broken_syntax")
    routes, _ = extract_routes(parsed, resolver, module_of, "test")

    assert [f.rel_path for f in failed] == ["broken.py"]
    assert [(r.method, r.path) for r in routes] == [("GET", "/health")]


# --- ví dụ 4 file trong plan: nối được từ route xuống tận bảng -----------

def test_vi_du_trong_plan_du_ba_loai_thuc_the():
    parsed, _, resolver, module_of = analyze("sample_app")
    routes, _ = extract_routes(parsed, resolver, module_of, "test")
    entities = extract_entities(parsed, resolver, module_of, "test")
    calls = extract_external_calls(parsed, resolver, module_of, "test")

    assert [(r.method, r.path) for r in routes] == [
        ("POST", "/api/v1/orders/{order_id}/confirm")
    ]
    assert [e.table_name for e in entities] == ["orders"]
    assert [(c.http_method, c.url_or_host) for c in calls] == [
        ("POST", "https://payment.internal/charge")
    ]


# --- fixture 14: app.mount() cua Starlette -------------------------------

def test_fixture_14_doc_duoc_tien_to_cua_app_mount():
    """app.mount("/api/v1", app=api) phải được tính vào đường dẫn.

    Lỗi số 1 tìm ra ở Mốc 7: công cụ chỉ đọc include_router nên 61/61 route của
    Netflix/dispatch mất tiền tố /api/v1 mà vẫn bị ghi nhãn "full".
    """
    routes, dropped = routes_of("fixture_14_starlette_mount")

    assert [(r.method, r.path) for r in routes] == [("GET", "/api/v1/orders/{order_id}")]
    assert dropped == []


def test_fixture_14_mount_thu_muc_tinh_khong_tao_chang_prefix():
    """frontend.mount("/", StaticFiles(...)) không phải router, phải bỏ qua."""
    routes, _ = routes_of("fixture_14_starlette_mount")

    assert len(routes) == 1, "StaticFiles không có route, không được sinh thêm đường dẫn"


def test_fixture_14_duong_dan_du_thi_van_la_full():
    """Mọi chặng đều là chuỗi hằng nên đường dẫn đã đầy đủ — SPEC mục 5.1."""
    routes, _ = routes_of("fixture_14_starlette_mount")

    assert routes[0].confidence == "exact"
    assert routes[0].completeness == "full"
    assert routes[0].reason is None


# --- fixture 15: lop co so tu sinh __tablename__ luc chay -----------------

def test_fixture_15_khong_doan_ten_bang_khi_lop_co_so_tu_sinh():
    """Thiếu __tablename__ thì ghi None, không đoán — nguyên tắc bất biến số 3.

    Lỗi số 2 tìm ra ở Mốc 7: quy ước "tên class viết thường" sai 7/9 ca trên
    Netflix/dispatch, vì lớp cơ sở repo đó tách tên theo chữ hoa.
    """
    entities = entities_of("fixture_15_tablename_tu_sinh")
    by_class = {e.class_name: e for e in entities}

    case_notes = by_class["CaseNotes"]
    assert case_notes.table_name is None
    assert case_notes.table_name != "casenotes", "không được đoán theo tên class"
    assert "lớp cơ sở sinh lúc chạy" in case_notes.reason


def test_fixture_15_thuc_the_van_duoc_phat_hien_du_khong_biet_ten_bang():
    """Không đọc được tên bảng KHÔNG có nghĩa là bỏ sót cả bảng."""
    entities = entities_of("fixture_15_tablename_tu_sinh")

    assert sorted(e.class_name for e in entities) == ["CaseNotes", "Order"]


def test_fixture_15_co_khai_tablename_thi_van_doc_duoc_binh_thuong():
    entities = entities_of("fixture_15_tablename_tu_sinh")
    order = next(e for e in entities if e.class_name == "Order")

    assert order.table_name == "orders"
    assert order.confidence == "exact"
    assert order.completeness == "full"


# --- fixture 16: route dang ky trong khoi if ----------------------------

def test_fixture_16_route_trong_khoi_if_phai_neu_dieu_kien():
    """Lỗi số 3 tìm ra ở Mốc 7: route chỉ có ở môi trường dev bị liệt kê như
    route bình thường, người đọc không có cách nào biết."""
    routes, _ = routes_of("fixture_16_route_co_dieu_kien")
    private = next(r for r in routes if "/private" in r.path)

    assert private.completeness == "partial"
    assert "chỉ được đăng ký khi" in private.reason
    assert "settings.ENV == 'development'" in private.reason


def test_fixture_16_route_vo_dieu_kien_van_la_full():
    """Chỉ route nằm trong `if` mới bị hạ nhãn, không lan sang route khác."""
    routes, _ = routes_of("fixture_16_route_co_dieu_kien")
    public = next(r for r in routes if "/public" in r.path)

    assert public.completeness == "full"
    assert public.reason is None
