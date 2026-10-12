---
generated: true
non_normative: true
snapshot_id: "snap:193008397fc6e5a13fa5f1b7e8adbca4357fea55797a181e0b72f3e7c058bf09"
owner_component_id: "cmp_b99af8888eed0555ea9cd3ceb3162fe572f70056691b80c883abef994dbde1fa"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:f4b9d6de1bd3516522a009e570c0caa078b452a5a476f9de34d3f4de8ca5914e"]
evidence_ids: ["ev:130c14fb8eb723f517c8179ec3c59392241ce8b619376186b3c94114f2c14faf", "ev:fbe9b27adb596eb48b7b00ee924875793149d79fa588ef38e7f788efcec342c4"]
---
# EVT — Orders — order-created

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt. File mô tả vai trò của chính component này; không có nghĩa component sở hữu độc quyền topic.

| Vai trò | Topic | Broker | Namespace | Serialization | Bên liên quan | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|
| gửi | order-created | kafka:kafka:9092 | không áp dụng — Kafka không có namespace riêng; channel xác định bằng broker + topic | json | Stock | `fact:f4b9d6de1bd3516522a009e570c0caa078b452a5a476f9de34d3f4de8ca5914e` | `ev:130c14fb8eb723f517c8179ec3c59392241ce8b619376186b3c94114f2c14faf` (orders.py:8), `ev:fbe9b27adb596eb48b7b00ee924875793149d79fa588ef38e7f788efcec342c4` (orders.py:8) | inferred | partial |

Payload của `fact:f4b9d6de1bd3516522a009e570c0caa078b452a5a476f9de34d3f4de8ca5914e` — schema `{}` không phải schema đầy đủ:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "x-analysis": {
    "completeness": "partial",
    "evidence_ids": [
      "ev:130c14fb8eb723f517c8179ec3c59392241ce8b619376186b3c94114f2c14faf",
      "ev:fbe9b27adb596eb48b7b00ee924875793149d79fa588ef38e7f788efcec342c4"
    ],
    "fact_ids": [
      "fact:f4b9d6de1bd3516522a009e570c0caa078b452a5a476f9de34d3f4de8ca5914e"
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
