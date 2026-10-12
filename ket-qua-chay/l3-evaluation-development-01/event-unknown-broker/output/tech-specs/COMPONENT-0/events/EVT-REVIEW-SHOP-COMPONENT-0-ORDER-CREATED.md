---
generated: true
non_normative: true
snapshot_id: "snapshot-render-eval-v1"
owner_component_id: "cmp-000"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:8b5cc4df7eec7d32a7814eca4af047ae33b2d52342667715682e19c25b0b9faa"]
evidence_ids: ["ev-render-eval"]
---
# EVT — Component 0 — order-created

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt. File mô tả vai trò của chính component này; không có nghĩa component sở hữu độc quyền topic.

| Vai trò | Topic | Broker | Namespace | Serialization | Bên liên quan | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|
| nhận | order-created | unknown — Synthetic case: upstream could not establish this field | sales | json-v1 | unknown — chưa có cạnh event đã kiểm nối bên gửi | `fact:8b5cc4df7eec7d32a7814eca4af047ae33b2d52342667715682e19c25b0b9faa` | `ev-render-eval` (app/api.py:1) | exact | partial |

Payload của `fact:8b5cc4df7eec7d32a7814eca4af047ae33b2d52342667715682e19c25b0b9faa`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "properties": {
    "order_id": {
      "type": "integer"
    }
  },
  "required": [
    "order_id"
  ],
  "type": "object",
  "x-analysis": {
    "completeness": "full",
    "evidence_ids": [
      "ev-render-eval"
    ],
    "fact_ids": [
      "fact:8b5cc4df7eec7d32a7814eca4af047ae33b2d52342667715682e19c25b0b9faa"
    ]
  }
}
```
