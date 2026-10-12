# tdd-docker — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:8053c30b1c2e0701055f23718e5cba06736e299abd4a84a3ff4f205501454276`
- Trạng thái phân tích: completed
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/TOM-TAT/api/API-TDD-DOCKER-TOM-TAT-v1.md](tech-specs/TOM-TAT/api/API-TDD-DOCKER-TOM-TAT-v1.md) — component Tóm tắt
- API: [tech-specs/PING/api/API-TDD-DOCKER-PING-v1.md](tech-specs/PING/api/API-TDD-DOCKER-PING-v1.md) — component Ping

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Khởi động

- Package `app/`
  - `app/db.py` — Điểm vào (exact) — `app/db.py:44`: `if __name__ == "__main__":`
  - `app/main.py` — Điểm vào (exact) — `app/main.py:12`: `application = FastAPI()`

### Ping

- Package `app/`
  - `app/config.py` — Cấu hình (exact) — `app/config.py:10`: `class Settings(BaseSettings):`
- Package `app/api/`
  - `app/api/ping.py` — Route (exact) — `app/api/ping.py:8`: `@router.get("/ping")`

### Tóm tắt

- Package `app/`
  - `app/summarizer.py` — Truy cập dữ liệu (exact) — `app/summarizer.py:21`: `await TextSummary.filter(id=summary_id).update(summary=summary)`
- Package `app/api/`
  - `app/api/crud.py` — Truy cập dữ liệu (exact) — `app/api/crud.py:12`: `summary = await TextSummary.filter(id=id).first().values()`
  - `app/api/summaries.py` — Route (exact) — `app/api/summaries.py:18`: `@router.get("/{id}/", response_model=SummarySchema)`
- Package `app/models/`
  - `app/models/pydantic.py` — Schema API (exact) — `app/models/pydantic.py:4`: `class SummaryPayloadSchema(BaseModel):`
  - `app/models/tortoise.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/models/tortoise.py:1`: `from tortoise import fields, models`

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
- `HTTP_LIBRARY_UNSUPPORTED`: unsupported_http_library tại app/summarizer.py:9 — article.download() dùng thư viện newspaper, không thuộc nhóm httpx/requests/aiohttp được liệt kê để lập HTTP call.
- `OUT_OF_SCOPE_FILES`: migration: 1 file, test: 5 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- `CLAIMS_REJECTED`: 12 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
