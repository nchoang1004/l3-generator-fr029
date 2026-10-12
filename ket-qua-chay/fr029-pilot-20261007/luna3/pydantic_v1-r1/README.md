# pydantic_v1 — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:5bb8f8dab23ad52fff3529bdd3b387e2fbe241a46b8532b20990b11f1bc0564e`
- Trạng thái phân tích: completed
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/GHI-CHU/api/API-PYDANTIC-V1-GHI-CHU-v1.md](tech-specs/GHI-CHU/api/API-PYDANTIC-V1-GHI-CHU-v1.md) — component Ghi chú

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Ghi chú

- Package `app/`
  - `app/main.py` — Điểm vào (exact) — `app/main.py:6`

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `CLAIMS_REJECTED`: 1 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
