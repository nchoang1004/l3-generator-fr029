# params_models — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:f4c379df5bbe6f7ce12b9a2921b44ec8e7f9d4e100c82e340d37e1075b5c8b60`
- Trạng thái phân tích: failed — MODEL_ERROR: HTTP 429 rate_limit_exceeded
- Độ phủ đọc source: chưa đủ, xem Giới hạn

## Mục lục contract

- (không có)

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Khởi động

- Package `app/`
  - `app/main.py` — vai trò unknown: agent chưa xác định

### Mặt hàng

- Package `app/`
  - `app/deps.py` — vai trò unknown: agent chưa xác định
  - `app/routes.py` — vai trò unknown: agent chưa xác định
- Package `app/schemas/`
  - `app/schemas/items.py` — vai trò unknown: agent chưa xác định
  - `app/schemas/legacy.py` — vai trò unknown: agent chưa xác định

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `ANALYSIS_PARTIAL`: MODEL_ERROR: HTTP 429 rate_limit_exceeded
- `SOURCE_NOT_FULLY_READ`: app/deps.py thiếu [[1, 18]]; app/main.py thiếu [[1, 6]]; app/routes.py thiếu [[1, 69]]; app/schemas/items.py thiếu [[1, 30]]; app/schemas/legacy.py thiếu [[1, 6]]; requirements.txt thiếu [[1, 3]]
