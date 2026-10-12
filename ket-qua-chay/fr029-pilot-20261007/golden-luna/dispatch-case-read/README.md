# dispatch-case-read — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:cfd2c61676ad1172404183ea995d9d3fa42d51454c0181ff585e4262764c6a48`
- Trạng thái phân tích: partial — BUDGET_TOKENS: hết token
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/TOAN-BO/api/API-DISPATCH-CASE-READ-TOAN-BO-v1.md](tech-specs/TOAN-BO/api/API-DISPATCH-CASE-READ-TOAN-BO-v1.md) — component Toàn bộ

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Toàn bộ

- Package `./`
  - `pyproject.toml` — vai trò unknown: agent chưa xác định
- Package `src/dispatch/`
  - `src/dispatch/api.py` — Route (exact) — `src/dispatch/api.py:256`
  - `src/dispatch/main.py` — Điểm vào (exact) — `src/dispatch/main.py:56`
  - `src/dispatch/models.py` — Schema API (exact) — `src/dispatch/models.py:113`
- Package `src/dispatch/case/`
  - `src/dispatch/case/enums.py` — Khác (Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `src/dispatch/case/enums.py:4`
  - `src/dispatch/case/models.py` — Model bảng (exact) — `src/dispatch/case/models.py:63`
  - `src/dispatch/case/service.py` — Truy cập dữ liệu (exact) — `src/dispatch/case/service.py:38`
  - `src/dispatch/case/views.py` — Route (exact) — `src/dispatch/case/views.py:78`
- Package `src/dispatch/database/`
  - `src/dispatch/database/core.py` — Model bảng (exact) — `src/dispatch/database/core.py:101`
- Package `src/dispatch/project/`
  - `src/dispatch/project/models.py` — Khác (Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `src/dispatch/project/models.py:89`

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `ANALYSIS_PARTIAL`: BUDGET_TOKENS: hết token
- `CLAIMS_REJECTED`: 40 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
