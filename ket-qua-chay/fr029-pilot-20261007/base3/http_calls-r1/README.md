# http_calls — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:e834022c8ce97e51ed00b4473d50845bf3d6339716cd565a545bc0ea2d0c2d8b`
- Trạng thái phân tích: partial — MODEL_ERROR: HTTP 429 rate_limit_exceeded
- Độ phủ đọc source: chưa đủ, xem Giới hạn

## Mục lục contract

- (không có)

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Khởi động

- Package `app/`
  - `app/main.py` — vai trò unknown: agent chưa xác định

### Đơn hàng

- Package `app/`
  - `app/clients.py` — vai trò unknown: agent chưa xác định
  - `app/config.py` — vai trò unknown: agent chưa xác định
  - `app/db.py` — vai trò unknown: agent chưa xác định
  - `app/inventory_client.py` — vai trò unknown: agent chưa xác định
  - `app/routes.py` — vai trò unknown: agent chưa xác định

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `ANALYSIS_PARTIAL`: MODEL_ERROR: HTTP 429 rate_limit_exceeded
- `SOURCE_NOT_FULLY_READ`: app/clients.py thiếu [[1, 65]]; app/config.py thiếu [[1, 10]]; app/db.py thiếu [[1, 25]]; app/inventory_client.py thiếu [[1, 6]]; app/main.py thiếu [[1, 6]]; app/routes.py thiếu [[1, 24]]; requirements.txt thiếu [[1, 7]]
