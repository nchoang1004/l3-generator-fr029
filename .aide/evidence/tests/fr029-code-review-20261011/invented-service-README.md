# synthetic — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:fb294b52e0adc571a19557ca6087a26c8afa2053eda757efcb3f6d9935bbb747`
- Trạng thái phân tích: completed
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/DEMO/api/API-SYNTHETIC-DEMO-v1.md](tech-specs/DEMO/api/API-SYNTHETIC-DEMO-v1.md) — component Demo

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Demo

- Package `./`
  - `db.py` — Truy cập dữ liệu (exact) — `db.py:1`: `def save(db): db.commit()`
  - `helper.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `route.py:4`, `helper.py:1`, `db.py:1`
  - `route.py` — Điểm vào (exact) — `route.py:2`: `app=FastAPI()`

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
