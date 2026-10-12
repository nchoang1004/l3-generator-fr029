# orders-base — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:b4f357c449cb8f2890027f8e3037b30852aa06c14d4f6372ca58ed154c606616`
- Trạng thái phân tích: completed
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/TOAN-BO/api/API-ORDERS-BASE-TOAN-BO-v1.md](tech-specs/TOAN-BO/api/API-ORDERS-BASE-TOAN-BO-v1.md) — component Toàn bộ

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Toàn bộ

- Package `./`
  - `db.py` — Khác (Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `db.py:1`
  - `main.py` — Điểm vào (exact) — `main.py:4`
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

- (không có)
