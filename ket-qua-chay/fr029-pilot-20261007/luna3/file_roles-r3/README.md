# file_roles — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:3df7e7d2177f25da0603482e3cce1c1d8b380eb610c1188f4d497c9948271449`
- Trạng thái phân tích: completed
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/DON-HANG/api/API-FILE-ROLES-DON-HANG-v1.md](tech-specs/DON-HANG/api/API-FILE-ROLES-DON-HANG-v1.md) — component Đơn hàng
- API: [tech-specs/BAO-CAO/api/API-FILE-ROLES-BAO-CAO-v1.md](tech-specs/BAO-CAO/api/API-FILE-ROLES-BAO-CAO-v1.md) — component Báo cáo

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Khởi động

- Package `app/`
  - `app/main.py` — Điểm vào (exact) — `app/main.py:5`

### Đơn hàng

- Package `app/`
  - `app/config.py` — Cấu hình (exact) — `app/config.py:4`
  - `app/repository.py` — Truy cập dữ liệu (exact) — `app/repository.py:9`
  - `app/schemas.py` — Schema API (exact) — `app/schemas.py:4`
  - `app/service_utils.py` — Khác (Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/service_utils.py:1`
  - `app/services.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `app/api/orders.py:12`, `app/services.py:5`, `app/repository.py:7`
- Package `app/api/`
  - `app/api/orders.py` — Route (exact) — `app/api/orders.py:10`

### Báo cáo

- Package `app/api/`
  - `app/api/reports.py` — Route (exact) — `app/api/reports.py:10`

### Hạ tầng CSDL

- Package `app/`
  - `app/db.py` — Hạ tầng (exact) — `app/db.py:8`

### Dữ liệu dùng chung

- Package `app/`
  - `app/models.py` — Model bảng (exact) — `app/models.py:10`

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- (không có)
