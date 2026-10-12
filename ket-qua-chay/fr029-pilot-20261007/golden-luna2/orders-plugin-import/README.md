# orders-plugin-import — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:f2ff94965085f7055cca0d20f4a131c55bd99a47f3917a8d96f4dde2592ff747`
- Trạng thái phân tích: completed
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/TOAN-BO/api/API-ORDERS-PLUGIN-IMPORT-TOAN-BO-v1.md](tech-specs/TOAN-BO/api/API-ORDERS-PLUGIN-IMPORT-TOAN-BO-v1.md) — component Toàn bộ

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Toàn bộ

- Package `./`
  - `db.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `db.py:1`: `def get_db():`
  - `main.py` — Điểm vào (exact) — `main.py:4`: `app = FastAPI()`
  - `models.py` — Model bảng (exact) — `models.py:8`: `__tablename__ = "orders"`
  - `repository.py` — Truy cập dữ liệu (exact) — `repository.py:5`: `db.add(order)`
  - `requirements.txt` — vai trò unknown: agent chưa xác định
  - `routes.py` — Route (exact) — `routes.py:12`: `@router.post("/orders")`
  - `schemas.py` — Schema API (exact) — `schemas.py:3`: `class OrderInput(BaseModel):`
  - `service.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `routes.py:14`, `service.py:3`, `repository.py:5`
- Package `plugins/`
  - `plugins/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file)
  - `plugins/email.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `plugins/email.py:1`: `def notify(order_id):`
  - `plugins/sms.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `plugins/sms.py:1`: `def notify(order_id):`

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `DIAGRAM_NOT_PROVIDED`: Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- `ARCHITECTURE_NOT_EVALUATED`: Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- `CLAIMS_REJECTED`: 1 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
