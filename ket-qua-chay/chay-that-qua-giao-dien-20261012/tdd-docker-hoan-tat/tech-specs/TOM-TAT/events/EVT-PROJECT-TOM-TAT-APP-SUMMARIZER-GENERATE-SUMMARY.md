---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:8053c30b1c2e0701055f23718e5cba06736e299abd4a84a3ff4f205501454276"
owner_component_id: "cmp_85e5e3b3cfed5d952d022b245b713c4fae7484c0c89106444b395f7de26b8491"
owner_component: "Tóm tắt"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
origin: "đọc tĩnh"
fact_ids: ["fact:dacf5a9ba906a0c66074af3623474e8781830d497b94b3fdb9d1f0c8f8cde278", "fact:21dcc67c5bc2bdb150dde893903f363406f61e8b8cda33f023c78e5a787408a8"]
evidence_ids: ["ev:7eeffcc2f6fbff7a4d59c1bc24a54e1dee8fb5c6133186cd09a279069f733540", "ev:988dda337f18e3f44a8d89d038469a20026e3efd8f2d22ff5123da4898707f30"]
---
# EVT — Tóm tắt — app.summarizer.generate_summary

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt. File mô tả vai trò của chính component này; không có nghĩa component sở hữu độc quyền topic.

| Vai trò | Topic | Broker | Namespace | Serialization | Bên liên quan | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|
| gửi | app.summarizer.generate_summary | fastapi.BackgroundTasks | cùng tiến trình với app | không tuần tự hóa (gọi trong tiến trình) | Tóm tắt | `fact:dacf5a9ba906a0c66074af3623474e8781830d497b94b3fdb9d1f0c8f8cde278` | `ev:988dda337f18e3f44a8d89d038469a20026e3efd8f2d22ff5123da4898707f30` (app/api/summaries.py:38) | exact | partial |
| nhận | app.summarizer.generate_summary | fastapi.BackgroundTasks | cùng tiến trình với app | không tuần tự hóa (gọi trong tiến trình) | Tóm tắt | `fact:21dcc67c5bc2bdb150dde893903f363406f61e8b8cda33f023c78e5a787408a8` | `ev:7eeffcc2f6fbff7a4d59c1bc24a54e1dee8fb5c6133186cd09a279069f733540` (app/summarizer.py:7-21) | exact | partial |

Payload của `fact:dacf5a9ba906a0c66074af3623474e8781830d497b94b3fdb9d1f0c8f8cde278` — schema `{}` không phải schema đầy đủ:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "x-analysis": {
    "completeness": "partial",
    "evidence_ids": [
      "ev:988dda337f18e3f44a8d89d038469a20026e3efd8f2d22ff5123da4898707f30"
    ],
    "fact_ids": [
      "fact:dacf5a9ba906a0c66074af3623474e8781830d497b94b3fdb9d1f0c8f8cde278"
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

Payload của `fact:21dcc67c5bc2bdb150dde893903f363406f61e8b8cda33f023c78e5a787408a8` — schema `{}` không phải schema đầy đủ:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "x-analysis": {
    "completeness": "partial",
    "evidence_ids": [
      "ev:7eeffcc2f6fbff7a4d59c1bc24a54e1dee8fb5c6133186cd09a279069f733540"
    ],
    "fact_ids": [
      "fact:21dcc67c5bc2bdb150dde893903f363406f61e8b8cda33f023c78e5a787408a8"
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
