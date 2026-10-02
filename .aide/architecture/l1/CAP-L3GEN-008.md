---
uid: "01M369VEYTS970JDEQ317ABPC2"
key: "CAP-L3GEN-008"
type: "capability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"covers":["FR-L3GEN-028","FR-L3GEN-029","FR-L3GEN-030","FR-L3GEN-031"]}
verified_at: 2026-10-02
verified_against: [{"key":"FR-L3GEN-028","revision":3},{"key":"FR-L3GEN-029","revision":3},{"key":"FR-L3GEN-030","revision":2},{"key":"FR-L3GEN-031","revision":2},{"key":"GLOSS-L3GEN-001","revision":9}]
classification: "internal"
ai_assisted: true
---

# CAP-L3GEN-008 — Kiểm kê phạm vi và đơn vị phân tích

## Năng lực này là gì

Từ snapshot, xác định đơn vị phân tích, ngôn ngữ và framework của từng đơn vị, phần nào được xét, phần nào bỏ qua kèm lý do, và mức hỗ trợ áp cho từng đơn vị theo ma trận hỗ trợ.

## Ranh giới

- Không trích dữ kiện code — đó là CAP-L3GEN-009.
- Manifest và thư mục giúp tìm đơn vị phân tích nhưng không chứng minh ranh giới deployment.
- Repository rỗng hoặc toàn bộ ngoài phạm vi hỗ trợ thì báo đúng trạng thái, không trả kết quả thành công rỗng.

## FR được phủ

| FR key | Tên | Phần dựa vào năng lực này |
|---|---|---|
| [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md) | Sơ đồ kiến trúc có bằng chứng | Bảng "Phạm vi đọc": file được xét, file bị loại kèm lý do |
| [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md) | Tài liệu L3 API và cấu trúc component | Route trong file test hoặc ngoài phạm vi không vào tài liệu (AC-05) |
| [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md) | Tài liệu L3 bảng dữ liệu | Bảng khai trong file ngoài phạm vi không vào tài liệu |
| [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md) | Tài liệu L3 sự kiện và tác vụ nền | Như FR-030, cho điểm gửi và nhận |

## Ràng buộc chính

[NFR-L3GEN-OPS-001](../../requirements/nfr/NFR-L3GEN-OPS-001.md), [NFR-L3GEN-ACC-002](../../requirements/nfr/NFR-L3GEN-ACC-002.md).

## Ghi chú

Đây là năng lực, không phải component triển khai. Cách chia component nằm ở L2, lập sau L1. Thuật ngữ theo [glossary](../../domain/glossary-core.md).
