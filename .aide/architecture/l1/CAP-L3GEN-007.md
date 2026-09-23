---
uid: "01M369VEYT247G7S70TKVN02AE"
key: "CAP-L3GEN-007"
type: "capability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"covers":["FR-L3GEN-019"]}
verified_at: 2026-09-23
verified_against: [{"key":"FR-L3GEN-019","revision":1},{"key":"GLOSS-L3GEN-001","revision":5}]
classification: "internal"
ai_assisted: true
---

# CAP-L3GEN-007 — Tiếp nhận source và điều phối lần chạy

## Năng lực này là gì

Biến đầu vào của người dùng thành một `source snapshot` bất biến có content digest, rồi chạy đúng một `analysis run` trên snapshot đó. Giữ định danh, trạng thái `completed` / `partial` / `failed` và ngân sách của lần chạy: thời gian, bộ nhớ, trần tiếp nhận, trần token và số request tới từng model.

## Ranh giới

- Không quyết định phần nào của repository được phân tích — đó là CAP-L3GEN-008.
- Không đọc nội dung source để sinh dữ kiện — đó là CAP-L3GEN-009.
- Source đầu vào là read-only: không import, chạy, cài dependency hay ghi ngược vào source.
- Hết ngân sách thì dừng và đánh dấu `partial`; phần phạm vi đã mất do CAP-L3GEN-011 công bố.

## FR được phủ

| FR key | Tên |
|---|---|
| [FR-L3GEN-019](../../requirements/fr/FR-L3GEN-019.md) | Nhận source và chạy phân tích |

## Ràng buộc chính

[NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md), [NFR-L3GEN-OPS-001](../../requirements/nfr/NFR-L3GEN-OPS-001.md), [NFR-L3GEN-AI-002](../../requirements/nfr/NFR-L3GEN-AI-002.md).

## Ghi chú

Đây là năng lực, không phải component triển khai. Cách chia component nằm ở L2, lập sau L1. Thuật ngữ theo [glossary](../../domain/glossary-core.md).
