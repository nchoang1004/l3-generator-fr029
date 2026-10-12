# prefix_chain — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:c76102dcd74977697e638089e01037e517bb8e4d9a039f63ffbf8bf79eaca9b7`
- Trạng thái phân tích: partial — MODEL_ERROR: HTTP 429 rate_limit_exceeded
- Độ phủ đọc source: chưa đủ, xem Giới hạn

## Mục lục contract

- (không có)

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Khởi động

- Package `app/`
  - `app/config.py` — vai trò unknown: agent chưa xác định
  - `app/main.py` — vai trò unknown: agent chưa xác định
- Package `app/api/`
  - `app/api/api.py` — vai trò unknown: agent chưa xác định

### Mặt hàng

- Package `app/api/`
  - `app/api/items.py` — vai trò unknown: agent chưa xác định
  - `app/api/legacy.py` — vai trò unknown: agent chưa xác định

### Tài khoản

- Package `app/api/`
  - `app/api/users.py` — vai trò unknown: agent chưa xác định

### Hệ thống

- Package `app/api/`
  - `app/api/admin.py` — vai trò unknown: agent chưa xác định
  - `app/api/health.py` — vai trò unknown: agent chưa xác định

### Ứng dụng phụ

- Package `app/`
  - `app/sub.py` — vai trò unknown: agent chưa xác định

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `ANALYSIS_PARTIAL`: MODEL_ERROR: HTTP 429 rate_limit_exceeded
- `SOURCE_NOT_FULLY_READ`: app/api/admin.py thiếu [[1, 8]]; app/api/health.py thiếu [[1, 8]]; app/api/items.py thiếu [[1, 18]]; app/api/legacy.py thiếu [[1, 8]]; app/api/users.py thiếu [[1, 8]]; app/main.py thiếu [[1, 24]]; app/sub.py thiếu [[1, 8]]; requirements.txt thiếu [[1, 3]]
