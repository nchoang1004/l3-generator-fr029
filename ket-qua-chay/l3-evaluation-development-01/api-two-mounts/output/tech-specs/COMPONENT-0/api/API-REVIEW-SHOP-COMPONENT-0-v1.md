---
generated: true
non_normative: true
snapshot_id: "snapshot-render-eval-v1"
owner_component_id: "cmp-000"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:b3131636c9c29c53dd1dae2eae2d2111e3a14035d4fe5172d0f9950aad3aeef4", "fact:c8321216723489a3654220897f5d14252511a8fa829ad3a372d688e9e5324f3c"]
evidence_ids: ["ev-render-eval"]
---
# API — Component 0

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app-main | GET | /b/orders | app.api.orders | (rỗng) | (rỗng) | 200 | unknown — Synthetic case: upstream could not establish this field | `fact:b3131636c9c29c53dd1dae2eae2d2111e3a14035d4fe5172d0f9950aad3aeef4` | `ev-render-eval` (app/api.py:1) | exact | full |
| app-main | GET | /a/orders | app.api.orders | (rỗng) | (rỗng) | 200 | unknown — Synthetic case: upstream could not establish this field | `fact:c8321216723489a3654220897f5d14252511a8fa829ad3a372d688e9e5324f3c` | `ev-render-eval` (app/api.py:1) | exact | full |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Component 0",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/a/orders": {
      "get": {
        "operationId": "op_c8321216723489a3",
        "responses": {
          "200": {
            "description": "Status code lấy từ source; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app-main",
          "evidence_ids": [
            "ev-render-eval"
          ],
          "fact_ids": [
            "fact:c8321216723489a3654220897f5d14252511a8fa829ad3a372d688e9e5324f3c"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Synthetic case: upstream could not establish this field"
            }
          ]
        }
      }
    },
    "/b/orders": {
      "get": {
        "operationId": "op_b3131636c9c29c53",
        "responses": {
          "200": {
            "description": "Status code lấy từ source; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app-main",
          "evidence_ids": [
            "ev-render-eval"
          ],
          "fact_ids": [
            "fact:b3131636c9c29c53dd1dae2eae2d2111e3a14035d4fe5172d0f9950aad3aeef4"
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
