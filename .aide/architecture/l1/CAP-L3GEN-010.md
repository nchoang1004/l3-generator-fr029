---
uid: "01M369VEYTPZT8AK24PR5BEZGJ"
key: "CAP-L3GEN-010"
type: "capability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"covers":["FR-L3GEN-022"]}
verified_at: 2026-09-23
verified_against: [{"key":"FR-L3GEN-022","revision":2},{"key":"GLOSS-L3GEN-001","revision":5}]
classification: "internal"
ai_assisted: true
---

# CAP-L3GEN-010 — Dựng mô hình kiến trúc mức component

## Năng lực này là gì

Từ tập dữ kiện, dựng component, vai trò và cạnh dependency ở mức application/component. Code chia file vào component và dựng cạnh từ lời gọi đã xác định đích. Mô hình ngôn ngữ đặt tên, mô tả, gắn nhãn cạnh, đề xuất cạnh phân tích tĩnh không thấy, và chia nhóm khi repository phẳng. Phân việc giữa hai model theo NFR-L3GEN-AI-002.

## Ranh giới

- Không trích dữ kiện mới từ source — chỉ dùng dữ kiện của CAP-L3GEN-009 và đoạn code đọc qua công cụ có giới hạn.
- Kiểm đề xuất của model trước khi đưa vào mô hình thuộc năng lực này (AC-L3GEN-022-02, AC-L3GEN-022-05): đề xuất không có dữ kiện chứng minh bị loại kèm lý do. Kiểm lần cuối mọi kết luận trước khi công bố là CAP-L3GEN-011.
- Model không thêm, bớt, gộp hay tách component do code chia.
- Model lỗi hoặc hết quota thì dừng bước dùng model, giữ phần do code dựng, trạng thái `partial`.

## FR được phủ

| FR key | Tên |
|---|---|
| [FR-L3GEN-022](../../requirements/fr/FR-L3GEN-022.md) | Dựng component và quan hệ kiến trúc |

## Ràng buộc chính

[NFR-L3GEN-AI-002](../../requirements/nfr/NFR-L3GEN-AI-002.md), [NFR-L3GEN-ABST-002](../../requirements/nfr/NFR-L3GEN-ABST-002.md), [NFR-L3GEN-ACC-002](../../requirements/nfr/NFR-L3GEN-ACC-002.md).

## Ghi chú

Đây là năng lực, không phải component triển khai. Cách chia component nằm ở L2, lập sau L1. Thuật ngữ theo [glossary](../../domain/glossary-core.md).
