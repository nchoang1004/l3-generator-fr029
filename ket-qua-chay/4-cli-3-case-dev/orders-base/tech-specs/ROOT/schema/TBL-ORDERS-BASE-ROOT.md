---
generated: true
non_normative: true
snapshot_id: "snap:b4f357c449cb8f2890027f8e3037b30852aa06c14d4f6372ca58ed154c606616"
owner_component_id: "cmp_9bc109dffd090e5b2cd9c9173775fbcdc50dd15cb7fff3be472c7b9a0ae6644a"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:8ca5a859c53265448e0c088facbc6a4dbc57a5dd383f8a6bf7101cc78206208e"]
evidence_ids: ["ev:86eccaa7b3df126eae78a1c0fabf10deea9e485f8f0020788ad04bfc09cd0db0", "ev:8d188fa8cd1eab93fee230c2dda4c1a7da155efb81dbf246330086828184dcf8", "ev:975718e0852f78cbd4313a3f3aaa75af6c307fb51a09c7e3f8eeaae979d32fc4", "ev:c35ffe50b92379e3609586c0bb4230e661c27cdca6e6a33e2d6521c52028f1d2", "ev:ed93a9224246528bd6c9a065c8a7edb9ccd0674313939f90ad8b90c12f942993", "ev:fccaad536828b5f40799b75d9cf2fc443f9a33a48a3feb84e12ec15e68ddc2c7"]
---
# TBL — (root)

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.

## Bảng orders

Dialect: unknown — Không có Base.metadata.create_all(engine) nối base này với một engine có URL literal. Fact `fact:8ca5a859c53265448e0c088facbc6a4dbc57a5dd383f8a6bf7101cc78206208e`. Confidence inferred, completeness partial.

Evidence: `ev:ed93a9224246528bd6c9a065c8a7edb9ccd0674313939f90ad8b90c12f942993` (models.py:7-10), `ev:975718e0852f78cbd4313a3f3aaa75af6c307fb51a09c7e3f8eeaae979d32fc4` (models.py:8), `ev:8d188fa8cd1eab93fee230c2dda4c1a7da155efb81dbf246330086828184dcf8` (models.py:9), `ev:fccaad536828b5f40799b75d9cf2fc443f9a33a48a3feb84e12ec15e68ddc2c7` (models.py:9), `ev:86eccaa7b3df126eae78a1c0fabf10deea9e485f8f0020788ad04bfc09cd0db0` (models.py:10), `ev:c35ffe50b92379e3609586c0bb4230e661c27cdca6e6a33e2d6521c52028f1d2` (models.py:10).

| Cột | Kiểu | PK | FK | Nullable |
|---|---|---|---|---|
| id | unknown — Chưa xác định SQL dialect từ source | True | không áp dụng — Không khai ForeignKey/foreign_key | False |
| product | unknown — Chưa xác định SQL dialect từ source | False | không áp dụng — Không khai ForeignKey/foreign_key | False |

DDL dẫn xuất tĩnh, không phải migration; không được thực thi. Bảng thiếu dữ kiện bị bỏ khỏi DDL.

```sql
-- omitted: fact:8ca5a859c53265448e0c088facbc6a4dbc57a5dd383f8a6bf7101cc78206208e: dialect chưa biết
```
