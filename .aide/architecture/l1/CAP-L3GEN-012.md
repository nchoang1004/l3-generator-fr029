---
uid: "01M369VEYVTNDWABXMQGG5H4W1"
key: "CAP-L3GEN-012"
type: "capability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"covers":["FR-L3GEN-025","FR-L3GEN-026","FR-L3GEN-027"]}
verified_at: 2026-09-23
verified_against: [{"key":"FR-L3GEN-025","revision":2},{"key":"FR-L3GEN-026","revision":1},{"key":"FR-L3GEN-027","revision":1},{"key":"GLOSS-L3GEN-001","revision":5}]
classification: "internal"
ai_assisted: true
---

# CAP-L3GEN-012 — Trình bày và xuất kết quả

## Năng lực này là gì

Từ cùng một mô hình kiến trúc đã kiểm, sinh sơ đồ component (mức L2) kèm mã nguồn sơ đồ, tài liệu L3 contract (API, TBL, EVT theo cấu trúc `tech-specs/` của mentor) và JSON có schema version. Trên web, cho theo dõi lần chạy, xem tổng quan, đi sâu theo component và mở bằng chứng.

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
