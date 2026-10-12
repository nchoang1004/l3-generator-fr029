---
generated: true
non_normative: true
snapshot_id: "snap:193008397fc6e5a13fa5f1b7e8adbca4357fea55797a181e0b72f3e7c058bf09"
owner_component_id: "cmp_053e352ca24100eb6bff9b5feaf362811e73d59dec0647ec9bd45c2869035cd3"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:83e0f5ee0813baedbf0e41e675a278fd553613c6e4a2bc70c82bcf9ff637b540"]
evidence_ids: ["ev:bf4c9eb056dba0d13af84f4f5866794558ed9fb40953a341483cf18500e9703e", "ev:e66a0935c849399a7b182cbd3d54c0f9ac1028f62caae7941f4438235e79220d"]
---
# EVT — Stock — order-created

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt. File mô tả vai trò của chính component này; không có nghĩa component sở hữu độc quyền topic.

| Vai trò | Topic | Broker | Namespace | Serialization | Bên liên quan | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|
| nhận | order-created | kafka:kafka:9092 | không áp dụng — Kafka không có namespace riêng; channel xác định bằng broker + topic | json | Orders | `fact:83e0f5ee0813baedbf0e41e675a278fd553613c6e4a2bc70c82bcf9ff637b540` | `ev:bf4c9eb056dba0d13af84f4f5866794558ed9fb40953a341483cf18500e9703e` (stock.py:5), `ev:e66a0935c849399a7b182cbd3d54c0f9ac1028f62caae7941f4438235e79220d` (stock.py:5) | inferred | partial |

Payload của `fact:83e0f5ee0813baedbf0e41e675a278fd553613c6e4a2bc70c82bcf9ff637b540` — schema `{}` không phải schema đầy đủ:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "x-analysis": {
    "completeness": "partial",
    "evidence_ids": [
      "ev:bf4c9eb056dba0d13af84f4f5866794558ed9fb40953a341483cf18500e9703e",
      "ev:e66a0935c849399a7b182cbd3d54c0f9ac1028f62caae7941f4438235e79220d"
    ],
    "fact_ids": [
      "fact:83e0f5ee0813baedbf0e41e675a278fd553613c6e4a2bc70c82bcf9ff637b540"
    ],
    "unknowns": [
      {
        "field": "payload",
        "reason": "Payload không có schema đọc được"
      }
    ]
  }
}
```
