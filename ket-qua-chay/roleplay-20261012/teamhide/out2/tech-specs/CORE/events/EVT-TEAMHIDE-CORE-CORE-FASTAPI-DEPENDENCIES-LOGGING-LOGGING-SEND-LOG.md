---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:96f8c4c9bb1fbd6f13ba0f2b1a22b3c98fb3e718c6744a39e04ab68535bb4a3f"
owner_component_id: "cmp_ff7af69bf31531c2d55fe3d833814fd6fc8af1290e87663d3ec8976f77fc41de"
owner_component: "core"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
origin: "đọc tĩnh"
fact_ids: ["fact:63b6d44dd3fc30e2701dcdf54398eb6475cb8a88ddc14da51c7d78605dc41727", "fact:ff1683456cbdd6d08c2bd7729919dbd1601146694a8e131c6e34d5c0f7c8f596"]
evidence_ids: ["ev:0c42c0d099c1c538cbdfaf60046eb45c1aa63af9b818824f891d395ae2a58b36", "ev:31f691ec52fda7a393658ea26163330b9d63525b44e740a36cc02d6f6f9f8fbd"]
---
# EVT — core — core.fastapi.dependencies.logging.Logging._send_log

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt. File mô tả vai trò của chính component này; không có nghĩa component sở hữu độc quyền topic.

| Vai trò | Topic | Broker | Namespace | Serialization | Bên liên quan | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|
| gửi | core.fastapi.dependencies.logging.Logging._send_log | fastapi.BackgroundTasks | cùng tiến trình với app | không tuần tự hóa (gọi trong tiến trình) | core | `fact:63b6d44dd3fc30e2701dcdf54398eb6475cb8a88ddc14da51c7d78605dc41727` | `ev:0c42c0d099c1c538cbdfaf60046eb45c1aa63af9b818824f891d395ae2a58b36` (core/fastapi/dependencies/logging.py:6) | exact | partial |
| nhận | core.fastapi.dependencies.logging.Logging._send_log | fastapi.BackgroundTasks | cùng tiến trình với app | không tuần tự hóa (gọi trong tiến trình) | core | `fact:ff1683456cbdd6d08c2bd7729919dbd1601146694a8e131c6e34d5c0f7c8f596` | `ev:31f691ec52fda7a393658ea26163330b9d63525b44e740a36cc02d6f6f9f8fbd` (core/fastapi/dependencies/logging.py:8-9) | exact | partial |

Payload của `fact:63b6d44dd3fc30e2701dcdf54398eb6475cb8a88ddc14da51c7d78605dc41727` — schema `{}` không phải schema đầy đủ:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "x-analysis": {
    "completeness": "partial",
    "evidence_ids": [
      "ev:0c42c0d099c1c538cbdfaf60046eb45c1aa63af9b818824f891d395ae2a58b36"
    ],
    "fact_ids": [
      "fact:63b6d44dd3fc30e2701dcdf54398eb6475cb8a88ddc14da51c7d78605dc41727"
    ],
    "unknowns": [
      {
        "field": "payload",
        "reason": "Đối số tác vụ không có schema đọc được"
      }
    ]
  }
}
```

Payload của `fact:ff1683456cbdd6d08c2bd7729919dbd1601146694a8e131c6e34d5c0f7c8f596` — schema `{}` không phải schema đầy đủ:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "x-analysis": {
    "completeness": "partial",
    "evidence_ids": [
      "ev:31f691ec52fda7a393658ea26163330b9d63525b44e740a36cc02d6f6f9f8fbd"
    ],
    "fact_ids": [
      "fact:ff1683456cbdd6d08c2bd7729919dbd1601146694a8e131c6e34d5c0f7c8f596"
    ],
    "unknowns": [
      {
        "field": "payload",
        "reason": "Đối số tác vụ không có schema đọc được"
      }
    ]
  }
}
```
