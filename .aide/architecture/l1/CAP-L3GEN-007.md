---
uid: "01M369VEYT247G7S70TKVN02AE"
key: "CAP-L3GEN-007"
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

# CAP-L3GEN-007 — Tiếp nhận source và điều phối lần chạy

## Năng lực này là gì

Biến đầu vào của người dùng thành một `source snapshot` bất biến có content digest, rồi chạy đúng một `analysis run` trên snapshot đó. Giữ định danh, trạng thái `completed` / `partial` / `failed` và ngân sách của lần chạy: thời gian, bộ nhớ, trần tiếp nhận, trần token, chi phí và số request tới model (NFR-L3GEN-AI-002).

## Ranh giới

- Không quyết định phần nào của repository được phân tích — đó là CAP-L3GEN-008.
- Không đọc nội dung source để sinh dữ kiện — đó là CAP-L3GEN-009.
- Source đầu vào là read-only: không import, chạy, cài dependency hay ghi ngược vào source.
- Hết ngân sách thì dừng và đánh dấu `partial`; phần phạm vi đã mất do CAP-L3GEN-011 công bố.

## FR được phủ

| FR key | Tên | Phần dựa vào năng lực này |
|---|---|---|
| [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md) | Sơ đồ kiến trúc có bằng chứng | Nhận thư mục, dừng sớm khi đầu vào hoặc thư mục output không hợp lệ (AC-02), trạng thái lần chạy |
| [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md) | Tài liệu L3 API và cấu trúc component | Cùng lần chạy với sơ đồ |
| [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md) | Tài liệu L3 bảng dữ liệu | Cùng lần chạy với sơ đồ |
| [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md) | Tài liệu L3 sự kiện và tác vụ nền | Cùng lần chạy với sơ đồ |

## Ràng buộc chính

[NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md), [NFR-L3GEN-OPS-001](../../requirements/nfr/NFR-L3GEN-OPS-001.md), [NFR-L3GEN-AI-002](../../requirements/nfr/NFR-L3GEN-AI-002.md).

## Ghi chú

Đây là năng lực, không phải component triển khai. Cách chia component nằm ở L2, lập sau L1. Thuật ngữ theo [glossary](../../domain/glossary-core.md).
