# params_models — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:f4c379df5bbe6f7ce12b9a2921b44ec8e7f9d4e100c82e340d37e1075b5c8b60`
- Trạng thái phân tích: completed
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/MAT-HANG/api/API-PARAMS-MODELS-MAT-HANG-v1.md](tech-specs/MAT-HANG/api/API-PARAMS-MODELS-MAT-HANG-v1.md) — component Mặt hàng

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Khởi động

- Package `app/`
  - `app/main.py` — Điểm vào (exact) — `app/main.py:5`

### Mặt hàng

- Package `app/`
  - `app/deps.py` — Khác (Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/deps.py:6`
  - `app/routes.py` — Route (exact) — `app/routes.py:13`
- Package `app/schemas/`
  - `app/schemas/items.py` — Schema API (exact) — `app/schemas/items.py:6`
  - `app/schemas/legacy.py` — Schema API (exact) — `app/schemas/legacy.py:4`

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- (không có)
