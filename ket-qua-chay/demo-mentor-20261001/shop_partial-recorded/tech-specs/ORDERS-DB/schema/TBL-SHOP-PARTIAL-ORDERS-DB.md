---
generated: true
non_normative: true
snapshot_id: "snap:635b641f86bb84e0f7ffb93ce783c06e41c8c910708a20838997b48c8d11d2f4"
owner_component_id: "cmp_ec5ecd4006c93338b0efaa089a6cfd839fd5080a1ec15a0aad228557672c5c3f"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:b77b978a3e9157f4ef684ea53660f58fbd3c576a1b136528343c2cceb2e081dc"]
evidence_ids: ["ev:6bb8b20bb5919105a966812ff6c9b49ad2a167bbd4bc9a831115c30c16873e22", "ev:71d939180340f3a54bfd3a34f5d83e956b0b29c54cc6fcab0bfdfce2c41d0868", "ev:736e349d49fd4d3d015ab66a7949b664475576671cd5c3378e6a28e6e00aed52", "ev:8c0ee0905a4bf526e0af59ed986920eaa069d749522e422078d715cc959b8797"]
---
# TBL — Orders DB

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.

## Bảng orders

Dialect: unknown — Không có Base.metadata.create_all(engine) nối base này với một engine có URL literal. Fact `fact:b77b978a3e9157f4ef684ea53660f58fbd3c576a1b136528343c2cceb2e081dc`. Confidence inferred, completeness partial.

Evidence: `ev:736e349d49fd4d3d015ab66a7949b664475576671cd5c3378e6a28e6e00aed52` (db/models.py:7-9), `ev:71d939180340f3a54bfd3a34f5d83e956b0b29c54cc6fcab0bfdfce2c41d0868` (db/models.py:8), `ev:6bb8b20bb5919105a966812ff6c9b49ad2a167bbd4bc9a831115c30c16873e22` (db/models.py:9), `ev:8c0ee0905a4bf526e0af59ed986920eaa069d749522e422078d715cc959b8797` (db/models.py:9).

| Cột | Kiểu | PK | FK | Nullable |
|---|---|---|---|---|
| id | unknown — Chưa xác định SQL dialect từ source | True | không áp dụng — Không khai ForeignKey/foreign_key | False |

DDL dẫn xuất tĩnh, không phải migration; không được thực thi. Bảng thiếu dữ kiện bị bỏ khỏi DDL.

```sql
-- omitted: fact:b77b978a3e9157f4ef684ea53660f58fbd3c576a1b136528343c2cceb2e081dc: dialect chưa biết
```
