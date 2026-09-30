---
uid: "01M369VEYVTNDWABXMQGG5H4W1"
key: "CAP-L3GEN-012"
type: "capability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"covers":["FR-L3GEN-025","FR-L3GEN-026","FR-L3GEN-027"]}
verified_at: 2026-09-23
verified_against: [{"key":"FR-L3GEN-025","revision":2},{"key":"FR-L3GEN-026","revision":1},{"key":"FR-L3GEN-027","revision":3},{"key":"GLOSS-L3GEN-001","revision":5}]
classification: "internal"
ai_assisted: true
---

# CAP-L3GEN-012 — Trình bày và xuất kết quả

## Năng lực này là gì

Từ cùng một mô hình kiến trúc đã kiểm, sinh sơ đồ component (mức L2) kèm mã nguồn sơ đồ, tài liệu L3 contract (API, TBL, EVT đặt trong `tech-specs/` theo đúng mẫu của mentor, quy tắc tên ở FR-L3GEN-027) và JSON có schema version. Trên web, cho theo dõi lần chạy, xem tổng quan, đi sâu theo component và mở bằng chứng.

## Phần sinh tài liệu L3

Ba đầu ra thuộc năng lực này, theo [FR-L3GEN-027](../../requirements/fr/FR-L3GEN-027.md):

| Đầu ra | Nội dung | AC |
|---|---|---|
| API | Endpoint, request/response, status, dependency/auth nếu biết; bảng đọc được và OpenAPI cùng nội dung | AC-L3GEN-027-01 |
| TBL | Bảng, cột, kiểu, khóa, nullable; bảng đọc được và DDL cùng nội dung | AC-L3GEN-027-02 |
| EVT | Topic, bên phát/nhận, payload nếu biết; phần chưa biết có lý do | AC-L3GEN-027-03 |

Đường dữ liệu: [CAP-009](CAP-L3GEN-009.md) trích dữ kiện → [CAP-010](CAP-L3GEN-010.md) dựng mô hình component → [CAP-011](CAP-L3GEN-011.md) kiểm bằng chứng → CAP-012 sinh tài liệu. Mỗi dòng contract giữ được nguồn chứng minh. Giới hạn số node của sơ đồ không được dùng để bỏ dữ kiện khỏi tài liệu L3.

Lát triển khai ưu tiên là FR-027 cùng phần phụ thuộc cần để đi từ source đến tài liệu. Các năng lực dùng chung được triển khai đến mức phục vụ lát này; việc nghiệm thu đầy đủ từng FR vẫn theo AC của FR đó.

## Ranh giới

- Không phân tích lại source; mọi nội dung lấy từ mô hình đã kiểm.
- Không artifact nào chứa component hoặc quan hệ mà artifact khác không có.
- Sơ đồ mặc định giữ mức application/component theo NFR-L3GEN-ABST-002.
- Khám phá tương tác chỉ có trên web; dòng lệnh chỉ ghi file.

## FR được phủ

| FR key | Tên |
|---|---|
| [FR-L3GEN-025](../../requirements/fr/FR-L3GEN-025.md) | Xuất kết quả |
| [FR-L3GEN-026](../../requirements/fr/FR-L3GEN-026.md) | Khám phá kết quả trên web |
| [FR-L3GEN-027](../../requirements/fr/FR-L3GEN-027.md) | Sinh tài liệu L3 contract |

## Ràng buộc chính

[NFR-L3GEN-ABST-002](../../requirements/nfr/NFR-L3GEN-ABST-002.md), [NFR-L3GEN-OPS-001](../../requirements/nfr/NFR-L3GEN-OPS-001.md), [NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md).

## Ghi chú

Đây là năng lực, không phải component triển khai. Cách chia component nằm ở L2, lập sau L1. Thuật ngữ theo [glossary](../../domain/glossary-core.md).
