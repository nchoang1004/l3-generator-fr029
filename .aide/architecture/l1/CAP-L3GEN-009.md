---
uid: "01M369VEYTSNHJZCBSTBSSER65"
key: "CAP-L3GEN-009"
type: "capability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"covers":["FR-L3GEN-021"]}
verified_at: 2026-09-23
verified_against: [{"key":"FR-L3GEN-021","revision":2},{"key":"GLOSS-L3GEN-001","revision":5}]
classification: "internal"
ai_assisted: true
---

# CAP-L3GEN-009 — Trích dữ kiện code

## Năng lực này là gì

Đọc source bằng phân tích tĩnh để trích dữ kiện kèm vị trí: route cùng request/response model, entity và bảng, lời gọi HTTP, tham chiếu xuyên file, cấu hình, sự kiện và thư viện. Nối tham chiếu tới đích khi xác định được.

## Ranh giới

- Không dùng mô hình ngôn ngữ; dữ kiện hoàn toàn do phân tích tĩnh sinh.
- Không thực thi source.
- Tham chiếu không xác định được đích giữ nhãn `unresolved`, không nâng thành quan hệ kiến trúc.
- Giá trị bí mật trong cấu hình bị che trước khi vào bất kỳ đầu ra nào.

## FR được phủ

| FR key | Tên |
|---|---|
| [FR-L3GEN-021](../../requirements/fr/FR-L3GEN-021.md) | Trích dữ kiện code |

## Ràng buộc chính

[NFR-L3GEN-ACC-002](../../requirements/nfr/NFR-L3GEN-ACC-002.md), [NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md).

## Ghi chú

Đây là năng lực, không phải component triển khai. Cách chia component nằm ở L2, lập sau L1. Thuật ngữ theo [glossary](../../domain/glossary-core.md).
