# prefix_chain — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:c76102dcd74977697e638089e01037e517bb8e4d9a039f63ffbf8bf79eaca9b7`
- Trạng thái phân tích: completed
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/UNG-DUNG-PHU/api/API-PREFIX-CHAIN-UNG-DUNG-PHU-v1.md](tech-specs/UNG-DUNG-PHU/api/API-PREFIX-CHAIN-UNG-DUNG-PHU-v1.md) — component Ứng dụng phụ
- API: [tech-specs/KHOI-DONG/api/API-PREFIX-CHAIN-KHOI-DONG-v1.md](tech-specs/KHOI-DONG/api/API-PREFIX-CHAIN-KHOI-DONG-v1.md) — component Khởi động
- API: [tech-specs/HE-THONG/api/API-PREFIX-CHAIN-HE-THONG-v1.md](tech-specs/HE-THONG/api/API-PREFIX-CHAIN-HE-THONG-v1.md) — component Hệ thống
- API: [tech-specs/MAT-HANG/api/API-PREFIX-CHAIN-MAT-HANG-v1.md](tech-specs/MAT-HANG/api/API-PREFIX-CHAIN-MAT-HANG-v1.md) — component Mặt hàng
- API: [tech-specs/TAI-KHOAN/api/API-PREFIX-CHAIN-TAI-KHOAN-v1.md](tech-specs/TAI-KHOAN/api/API-PREFIX-CHAIN-TAI-KHOAN-v1.md) — component Tài khoản

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Khởi động

- Package `app/`
  - `app/config.py` — Cấu hình (exact) — `app/config.py:4`: `class Settings(BaseSettings):`
  - `app/main.py` — Điểm vào (exact) — `app/main.py:12`: `app = FastAPI(title=settings.PROJECT_NAME)`
- Package `app/api/`
  - `app/api/api.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/api/api.py:5`: `api_router = APIRouter()`

### Mặt hàng

- Package `app/api/`
  - `app/api/items.py` — Route (exact) — `app/api/items.py:6`: `@router.get("/")`
  - `app/api/legacy.py` — Route (exact) — `app/api/legacy.py:6`: `@router.get("/items/{item_id}")`

### Tài khoản

- Package `app/api/`
  - `app/api/users.py` — Route (exact) — `app/api/users.py:6`: `@router.get("/me")`

### Hệ thống

- Package `app/api/`
  - `app/api/admin.py` — Route (exact) — `app/api/admin.py:6`: `@router.get("/stats")`
  - `app/api/health.py` — Route (exact) — `app/api/health.py:6`: `@router.get("/ping")`

### Ứng dụng phụ

- Package `app/`
  - `app/sub.py` — Điểm vào (exact) — `app/sub.py:3`: `sub_app = FastAPI(title="Sub app")`

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `DIAGRAM_NOT_PROVIDED`: Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- `ARCHITECTURE_NOT_EVALUATED`: Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- `CLAIMS_REJECTED`: 2 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
