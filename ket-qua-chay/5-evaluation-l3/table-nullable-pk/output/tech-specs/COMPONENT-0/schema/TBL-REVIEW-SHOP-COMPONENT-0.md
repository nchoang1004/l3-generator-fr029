---
generated: true
non_normative: true
snapshot_id: "snapshot-render-eval-v1"
owner_component_id: "cmp-000"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:0d4fc4a78d3706edccafb665a8b2fdd9309e82c78625bb0f2b8e7bb9e1c4d21c"]
evidence_ids: ["ev-render-eval"]
---
# TBL — Component 0

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.

## Bảng orders

Dialect: sqlite. Fact `fact:0d4fc4a78d3706edccafb665a8b2fdd9309e82c78625bb0f2b8e7bb9e1c4d21c`. Confidence exact, completeness full.

Evidence: `ev-render-eval` (app/api.py:1).

| Cột | Kiểu | PK | FK | Nullable |
|---|---|---|---|---|
| id | INTEGER | True | không áp dụng — Explicitly absent in this synthetic case | True |
| note | TEXT | False | không áp dụng — Explicitly absent in this synthetic case | True |

DDL dẫn xuất tĩnh, không phải migration; không được thực thi. Bảng thiếu dữ kiện bị bỏ khỏi DDL.

```sql
-- omitted: fact:0d4fc4a78d3706edccafb665a8b2fdd9309e82c78625bb0f2b8e7bb9e1c4d21c: Khóa chính không được nullable
```
