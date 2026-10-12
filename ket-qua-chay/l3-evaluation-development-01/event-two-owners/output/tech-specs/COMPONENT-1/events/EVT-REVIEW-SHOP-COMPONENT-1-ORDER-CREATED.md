---
generated: true
non_normative: true
snapshot_id: "snapshot-render-eval-v1"
owner_component_id: "cmp-001"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:95100519be0342216c9c23348de6ab31630e6bd1c5c0b5b95e03f15c6b52a00b"]
evidence_ids: ["ev-render-eval"]
---
# EVT — Component 1 — order-created

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt. File mô tả vai trò của chính component này; không có nghĩa component sở hữu độc quyền topic.

| Vai trò | Topic | Broker | Namespace | Serialization | Bên liên quan | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|
| nhận | order-created | kafka-cluster-A | sales | json-v1 | unknown — chưa có cạnh event đã kiểm nối bên gửi | `fact:95100519be0342216c9c23348de6ab31630e6bd1c5c0b5b95e03f15c6b52a00b` | `ev-render-eval` (app/api.py:1) | exact | partial |

Payload của `fact:95100519be0342216c9c23348de6ab31630e6bd1c5c0b5b95e03f15c6b52a00b`:

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
      "fact:95100519be0342216c9c23348de6ab31630e6bd1c5c0b5b95e03f15c6b52a00b"
    ]
  }
}
```
