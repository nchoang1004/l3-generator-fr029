---
uid: "01M369VEYTSNHJZCBSTBSSER65"
key: "CAP-L3GEN-009"
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

# CAP-L3GEN-009 — Trích dữ kiện code

## Năng lực này là gì

Đọc source bằng phân tích tĩnh để trích dữ kiện kèm vị trí: route cùng request/response model, entity và bảng, lời gọi HTTP, tham chiếu xuyên file, cấu hình, sự kiện, tác vụ nền, thư viện và dấu hiệu vai trò file (glossary mục 3a). Nối tham chiếu tới đích khi xác định được.

## Ranh giới

- Không dùng mô hình ngôn ngữ; dữ kiện hoàn toàn do phân tích tĩnh sinh.
- Không thực thi source.
- Tham chiếu không xác định được đích giữ nhãn `unresolved`, không nâng thành quan hệ kiến trúc.
- Giá trị bí mật trong cấu hình bị che trước khi vào bất kỳ đầu ra nào.

## FR được phủ

| FR key | Tên | Phần dựa vào năng lực này |
|---|---|---|
| [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md) | Sơ đồ kiến trúc có bằng chứng | Lời gọi, hệ thống ngoài, điểm vào, khóa cấu hình, thư viện |
| [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md) | Tài liệu L3 API và cấu trúc component | Route, tham số, request/response model, dấu hiệu vai trò file, lời gọi HTTP ra ngoài |
| [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md) | Tài liệu L3 bảng dữ liệu | Model bảng, cột, kiểu, khóa |
| [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md) | Tài liệu L3 sự kiện và tác vụ nền | Điểm gửi và nhận sự kiện, tác vụ nền |

## Ràng buộc chính

[NFR-L3GEN-ACC-002](../../requirements/nfr/NFR-L3GEN-ACC-002.md), [NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md).

## Ghi chú

Đây là năng lực, không phải component triển khai. Cách chia component nằm ở L2, lập sau L1. Thuật ngữ theo [glossary](../../domain/glossary-core.md).
