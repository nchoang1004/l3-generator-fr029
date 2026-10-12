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
  - `app/main.py` — Điểm vào (exact) — `app/main.py:6`

### Đơn hàng

- Package `app/`
  - `app/hooks.py` — Khác (Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/hooks.py:1`
- Package `app/routers/`
  - `app/routers/internal.py` — Route (exact) — `app/routers/internal.py:6`
  - `app/routers/orders.py` — Route (exact) — `app/routers/orders.py:8`

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `ROUTE_NOT_DECORATOR`: add_api_route tại app/main.py:23 — Đăng ký route không dùng decorator; không đưa vào danh sách routes.
- `ROUTE_NOT_DECORATOR`: add_route tại app/main.py:24 — Đăng ký route không dùng decorator; không đưa vào danh sách routes.
- `ROUTE_NOT_DECORATOR`: add_websocket_route tại app/main.py:25 — Đăng ký WebSocket route không dùng decorator; không đưa vào danh sách routes.
- `OUT_OF_SCOPE_FILES`: conditional_out: 1 file, test: 3 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
