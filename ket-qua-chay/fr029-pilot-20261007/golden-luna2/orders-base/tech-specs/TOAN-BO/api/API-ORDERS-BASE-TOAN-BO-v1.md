---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:b4f357c449cb8f2890027f8e3037b30852aa06c14d4f6372ca58ed154c606616"
owner_component_id: "cmp_0fae6ac2d5cebe0e6677fa00dfb1a4d32d1515fa41caa26bfceca3188f930ec3"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v7"
fact_ids: ["fact:d557aedb6977e66ac2a914b8c01949dedf05c23810cbb1246e49daa25ce1ba45", "fact:b0e1cf649223a0203523a9c77843c0d805cc0aec9195227cdc6cf52bd171aef2"]
evidence_ids: ["ev:05d242d6d25b8129183d2dda7ee11f6e62dfb6b94e5b3cc3719dff06275e26d5", "ev:067df3cd374d0765dceaeee3b41697986dc08524c763e43628e22a3de6de9b32", "ev:0b0f35b7d580f9129f6adf7cad40995f2f16206842587f30a0de4d9ef3cedd0a", "ev:8455ec4863e0cd7cde39874d5b9341e295857bb4d82c40bc40db6e3ff1dac612", "ev:868243d1a8cfe0445c53495bb0ae7a95eb1d59eb8b0302f07014c0b68963124d", "ev:afdf519b77b9e3b2cbbb8e2aa59e32f3c6b359ce987f6bc09e2472d1ad2971e6", "ev:d3373336ae66b36bfead6f584d3c6d121b1b65f347191918a1163db3cb945832", "ev:d3cf1b2515c07ff154af5ba2d589ad2666ecf906257f07e0a81b35eecb593143"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /api/v1/orders | order (body, OrderInput, bắt buộc) | OrderInput | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:d557aedb` |


## Model

### OrderInput (request)

Fact `f:b0e1cf64` · exact / full · khai ở schemas.py:3

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| product | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:main.py:4 | POST | /api/v1/orders | routes.py::create_order_endpoint | fact:b0e1cf649223a0203523a9c77843c0d805cc0aec9195227cdc6cf52bd171aef2 | (rỗng) | 200 | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:d557aedb6977e66ac2a914b8c01949dedf05c23810cbb1246e49daa25ce1ba45` | `ev:afdf519b77b9e3b2cbbb8e2aa59e32f3c6b359ce987f6bc09e2472d1ad2971e6` (main.py:4), `ev:8455ec4863e0cd7cde39874d5b9341e295857bb4d82c40bc40db6e3ff1dac612` (main.py:5), `ev:868243d1a8cfe0445c53495bb0ae7a95eb1d59eb8b0302f07014c0b68963124d` (routes.py:7), `ev:d3373336ae66b36bfead6f584d3c6d121b1b65f347191918a1163db3cb945832` (routes.py:9), `ev:d3cf1b2515c07ff154af5ba2d589ad2666ecf906257f07e0a81b35eecb593143` (routes.py:9-10), `ev:05d242d6d25b8129183d2dda7ee11f6e62dfb6b94e5b3cc3719dff06275e26d5` (routes.py:10) | inferred | partial |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| OrderInput | fact:b0e1cf649223a0203523a9c77843c0d805cc0aec9195227cdc6cf52bd171aef2 | schemas.py:3 |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "OrderInput_b0e1cf64": {
        "properties": {
          "product": {
            "type": "string"
          }
        },
        "required": [
          "product"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:b0e1cf649223a0203523a9c77843c0d805cc0aec9195227cdc6cf52bd171aef2"
          ]
        }
      }
    }
  },
  "info": {
    "title": "Toàn bộ",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/api/v1/orders": {
      "post": {
        "operationId": "op_d557aedb6977e66a",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/OrderInput_b0e1cf64"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:main.py:4",
          "evidence_ids": [
            "ev:05d242d6d25b8129183d2dda7ee11f6e62dfb6b94e5b3cc3719dff06275e26d5",
            "ev:8455ec4863e0cd7cde39874d5b9341e295857bb4d82c40bc40db6e3ff1dac612",
            "ev:868243d1a8cfe0445c53495bb0ae7a95eb1d59eb8b0302f07014c0b68963124d",
            "ev:afdf519b77b9e3b2cbbb8e2aa59e32f3c6b359ce987f6bc09e2472d1ad2971e6",
            "ev:d3373336ae66b36bfead6f584d3c6d121b1b65f347191918a1163db3cb945832",
            "ev:d3cf1b2515c07ff154af5ba2d589ad2666ecf906257f07e0a81b35eecb593143"
          ],
          "fact_ids": [
            "fact:d557aedb6977e66ac2a914b8c01949dedf05c23810cbb1246e49daa25ce1ba45"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn."
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
