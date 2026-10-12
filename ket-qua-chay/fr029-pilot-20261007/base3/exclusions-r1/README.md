# exclusions — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:580534b662619976e5bee16365f43113b4a3ee22c99b2801ee45f291e2b399b6`
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
  - `app/hooks.py` — vai trò unknown: agent chưa xác định
- Package `app/routers/`
  - `app/routers/internal.py` — vai trò unknown: agent chưa xác định
  - `app/routers/orders.py` — vai trò unknown: agent chưa xác định

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `ANALYSIS_PARTIAL`: MODEL_ERROR: HTTP 429 rate_limit_exceeded
- `SOURCE_NOT_FULLY_READ`: app/hooks.py thiếu [[1, 13]]; app/main.py thiếu [[1, 25]]; app/routers/internal.py thiếu [[1, 8]]; app/routers/orders.py thiếu [[1, 15]]; requirements.txt thiếu [[1, 2]]
- `OUT_OF_SCOPE_FILES`: conditional_out: 1 file, test: 3 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
