# file_roles — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:3df7e7d2177f25da0603482e3cce1c1d8b380eb610c1188f4d497c9948271449`
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
  - `app/config.py` — vai trò unknown: agent chưa xác định
  - `app/repository.py` — vai trò unknown: agent chưa xác định
  - `app/schemas.py` — vai trò unknown: agent chưa xác định
  - `app/service_utils.py` — vai trò unknown: agent chưa xác định
  - `app/services.py` — vai trò unknown: agent chưa xác định
- Package `app/api/`
  - `app/api/orders.py` — vai trò unknown: agent chưa xác định

### Báo cáo

- Package `app/api/`
  - `app/api/reports.py` — vai trò unknown: agent chưa xác định

### Hạ tầng CSDL

- Package `app/`
  - `app/db.py` — vai trò unknown: agent chưa xác định

### Dữ liệu dùng chung

- Package `app/`
  - `app/models.py` — vai trò unknown: agent chưa xác định

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `ANALYSIS_PARTIAL`: MODEL_ERROR: HTTP 429 rate_limit_exceeded
- `SOURCE_NOT_FULLY_READ`: app/api/orders.py thiếu [[1, 20]]; app/api/reports.py thiếu [[1, 13]]; app/config.py thiếu [[1, 8]]; app/db.py thiếu [[1, 17]]; app/main.py thiếu [[1, 7]]; app/models.py thiếu [[1, 14]]; app/repository.py thiếu [[1, 15]]; app/schemas.py thiếu [[1, 12]]; app/service_utils.py thiếu [[1, 7]]; app/services.py thiếu [[1, 11]]; requirements.txt thiếu [[1, 4]]
