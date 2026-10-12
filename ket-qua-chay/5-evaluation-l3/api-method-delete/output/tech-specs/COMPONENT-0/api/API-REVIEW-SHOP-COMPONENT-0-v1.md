---
generated: true
non_normative: true
snapshot_id: "snapshot-render-eval-v1"
owner_component_id: "cmp-000"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:8a84e406c08ac9594f47222406598f7598e15c55f8044b04813e28c9dee70976"]
evidence_ids: ["ev-render-eval"]
---
# API — Component 0

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app-main | DELETE | /v1/orders | app.api.orders | (rỗng) | (rỗng) | 201 | unknown — Synthetic case: upstream could not establish this field | `fact:8a84e406c08ac9594f47222406598f7598e15c55f8044b04813e28c9dee70976` | `ev-render-eval` (app/api.py:1) | exact | full |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Component 0",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/v1/orders": {
      "delete": {
        "operationId": "op_8a84e406c08ac959",
        "responses": {
          "201": {
            "description": "Status code lấy từ source; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app-main",
          "evidence_ids": [
            "ev-render-eval"
          ],
          "fact_ids": [
            "fact:8a84e406c08ac9594f47222406598f7598e15c55f8044b04813e28c9dee70976"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Synthetic case: upstream could not establish this field"
            }
          ]
        }
      }
    }
  },
  "x-analysis": {
    "omitted_operations": []
  }
}
```
