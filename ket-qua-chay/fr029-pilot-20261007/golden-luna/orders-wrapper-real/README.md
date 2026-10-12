# orders-wrapper-real — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:1b33d7f5ef0b0f5a9434a34b0e55cc952ef2f4d2f3f7069fa13515f916707e9f`
- Trạng thái phân tích: completed
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/TOAN-BO/api/API-ORDERS-WRAPPER-REAL-TOAN-BO-v1.md](tech-specs/TOAN-BO/api/API-ORDERS-WRAPPER-REAL-TOAN-BO-v1.md) — component Toàn bộ

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Toàn bộ

- Package `./`
  - `db.py` — Khác (Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `db.py:3`
  - `main.py` — Điểm vào (exact) — `main.py:5`
  - `models.py` — Model bảng (exact) — `models.py:8`
  - `registration.py` — Khác (Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `registration.py:2`
  - `repository.py` — Truy cập dữ liệu (exact) — `repository.py:5`
  - `requirements.txt` — vai trò unknown: agent chưa xác định
  - `routes.py` — Route (exact) — `routes.py:9`
  - `schemas.py` — Schema API (exact) — `schemas.py:3`
  - `service.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `routes.py:11`, `service.py:4`, `repository.py:5`

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `CLAIMS_REJECTED`: 2 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
