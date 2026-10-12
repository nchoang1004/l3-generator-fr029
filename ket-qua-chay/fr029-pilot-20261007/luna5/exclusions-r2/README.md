# exclusions — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:580534b662619976e5bee16365f43113b4a3ee22c99b2801ee45f291e2b399b6`
- Trạng thái phân tích: completed
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/DON-HANG/api/API-EXCLUSIONS-DON-HANG-v1.md](tech-specs/DON-HANG/api/API-EXCLUSIONS-DON-HANG-v1.md) — component Đơn hàng

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Khởi động

- Package `app/`
  - `app/main.py` — Điểm vào (exact) — `app/main.py:6`: `app = FastAPI(title="Exclusions")`

### Đơn hàng

- Package `app/`
  - `app/hooks.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/hooks.py:1`: `class Registry:`
- Package `app/routers/`
  - `app/routers/internal.py` — Route (exact) — `app/routers/internal.py:6`: `@router.get("/debug/state")`
  - `app/routers/orders.py` — Route (exact) — `app/routers/orders.py:8`: `@router.get("")`

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
- `ROUTE_NOT_DECORATOR`: add_api_route tại app/main.py:23 — Đăng ký tuyến bằng app.add_api_route, không phải decorator; không tạo mục route theo định dạng.
- `ROUTE_NOT_DECORATOR`: add_route tại app/main.py:24 — Đăng ký tuyến bằng app.add_route, không phải decorator; không tạo mục route theo định dạng.
- `ROUTE_NOT_DECORATOR`: add_websocket_route tại app/main.py:25 — Đăng ký WebSocket, không phải decorator HTTP; không tạo mục route HTTP.
- `OUT_OF_SCOPE_FILES`: conditional_out: 1 file, test: 3 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- `CLAIMS_REJECTED`: 1 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
