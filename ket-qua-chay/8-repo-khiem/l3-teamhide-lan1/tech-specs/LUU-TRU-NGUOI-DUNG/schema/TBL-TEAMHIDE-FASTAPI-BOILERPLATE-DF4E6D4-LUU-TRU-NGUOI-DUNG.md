---
generated: true
non_normative: true
snapshot_id: "snap:96f8c4c9bb1fbd6f13ba0f2b1a22b3c98fb3e718c6744a39e04ab68535bb4a3f"
owner_component_id: "cmp_95405d59cd1bf6793aaabbd1b2d696e9fe7a60b0fff12b43107b53c242f65a4a"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:8cc7f2347c01991ba09383b9e750166a40ac852dd0ad3530d07a8b3998c2460c"]
evidence_ids: ["ev:142864d139fb8c461bb03ecfbdf254c59867c5c1c503e87464b63a2313f566dd", "ev:153be938e47e9cea8eb441a594eac680a0743f892f64ad1d31f237de8fe5cb87", "ev:28e563dbfcaa17e3c251c36133402169b8c45192a876833777776460f21fb90c", "ev:3f9f3cabaa13f852de9e7cf93e44c48b7f115b97e532511b02190629c0d68155", "ev:45d6a300869bbb151298bd7f2a2dd69257142fac603a377aaecfc496b185af11", "ev:69d8fd33f67c0495353ad0782be4d82f9b892f4f36edb1a74f21224072d36722", "ev:86078c4c68173cc29ce80870c9ef2b3ec705e92778c8fdc9d73dd1543a617baa", "ev:b805da7fb2a77260631f5ee6c512340979cbb29d96fc4921e3b56a5ce67bdac5", "ev:c70037d01a56527d6b0713288d9d7e8ad9f49e6386a600e9a0a42da54eb395dd", "ev:de5bc8828bab78bceaa11a949197d0869f13edfe5c1ff747b6e023e64c700efb", "ev:deeac9267e5cfeb37820eb26dccbcbf32f74bec7ed130ac3fcee1c5a92b4a486", "ev:fdc28961653ac1e8f09b2243a073b899a3687c571b7e71d41e08c1956893ed0c"]
---
# TBL — Lưu trữ người dùng

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.

## Bảng user

Dialect: unknown — Không có Base.metadata.create_all(engine) nối base này với một engine có URL literal. Fact `fact:8cc7f2347c01991ba09383b9e750166a40ac852dd0ad3530d07a8b3998c2460c`. Confidence inferred, completeness partial.

Evidence: `ev:28e563dbfcaa17e3c251c36133402169b8c45192a876833777776460f21fb90c` (app/user/domain/entity/user.py:10-30), `ev:3f9f3cabaa13f852de9e7cf93e44c48b7f115b97e532511b02190629c0d68155` (app/user/domain/entity/user.py:11), `ev:b805da7fb2a77260631f5ee6c512340979cbb29d96fc4921e3b56a5ce67bdac5` (app/user/domain/entity/user.py:13), `ev:de5bc8828bab78bceaa11a949197d0869f13edfe5c1ff747b6e023e64c700efb` (app/user/domain/entity/user.py:13), `ev:69d8fd33f67c0495353ad0782be4d82f9b892f4f36edb1a74f21224072d36722` (app/user/domain/entity/user.py:14), `ev:86078c4c68173cc29ce80870c9ef2b3ec705e92778c8fdc9d73dd1543a617baa` (app/user/domain/entity/user.py:14), `ev:142864d139fb8c461bb03ecfbdf254c59867c5c1c503e87464b63a2313f566dd` (app/user/domain/entity/user.py:15), `ev:153be938e47e9cea8eb441a594eac680a0743f892f64ad1d31f237de8fe5cb87` (app/user/domain/entity/user.py:15), `ev:deeac9267e5cfeb37820eb26dccbcbf32f74bec7ed130ac3fcee1c5a92b4a486` (app/user/domain/entity/user.py:16), `ev:fdc28961653ac1e8f09b2243a073b899a3687c571b7e71d41e08c1956893ed0c` (app/user/domain/entity/user.py:16), `ev:45d6a300869bbb151298bd7f2a2dd69257142fac603a377aaecfc496b185af11` (app/user/domain/entity/user.py:17), `ev:c70037d01a56527d6b0713288d9d7e8ad9f49e6386a600e9a0a42da54eb395dd` (app/user/domain/entity/user.py:17).

| Cột | Kiểu | PK | FK | Nullable |
|---|---|---|---|---|
| id | unknown — Chưa xác định SQL dialect từ source | True | không áp dụng — Không khai ForeignKey/foreign_key | False |
| password | unknown — Chưa xác định SQL dialect từ source | False | không áp dụng — Không khai ForeignKey/foreign_key | False |
| email | unknown — Chưa xác định SQL dialect từ source | False | không áp dụng — Không khai ForeignKey/foreign_key | False |
| nickname | unknown — Chưa xác định SQL dialect từ source | False | không áp dụng — Không khai ForeignKey/foreign_key | False |
| is_admin | unknown — Chưa xác định SQL dialect từ source | False | không áp dụng — Không khai ForeignKey/foreign_key | False |

DDL dẫn xuất tĩnh, không phải migration; không được thực thi. Bảng thiếu dữ kiện bị bỏ khỏi DDL.

```sql
-- omitted: fact:8cc7f2347c01991ba09383b9e750166a40ac852dd0ad3530d07a8b3998c2460c: dialect chưa biết
```
