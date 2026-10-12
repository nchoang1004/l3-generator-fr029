---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:e4e27e11d7144a76c6769f4ef5b22a5a87677c49654fd84ff8cdd5e9f9e9216f"
owner_component_id: "cmp_3b9d0256e5a665eab542497ef80c1bb4ce7b13a4fc83671740f49a8ac68e5c8d"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v7"
fact_ids: ["fact:f1fa988e47e2a3b671afa9ec746dcd3f1a10fa672c63b2b3f128042503181ad8", "fact:dcc8c0eb0adcb056e555a2b37d825caa4f678921c46230b0e3c16522c7942d52"]
evidence_ids: ["ev:2becbca1585fd97e1e01a34a3c4722805a6fc875c8a390e80adc870d69fc1b55", "ev:3528a71b7b21d26a1f2c8fbab068e20206ba934411a0345d90e59926e26447bb", "ev:59e78ed9dd3d61ece95ba8d4a912b300d2363bfb166b2f3c58d57e34b7610062", "ev:8535219ae7e0ea64fbdea30ed366dbda3169944d7fd55b4628eadc755458a650", "ev:c72684b3b361929edcd571846b8c4707da451d4d3fec35810123b29d89659715", "ev:c9053d39c94b385cc002f43ef4c1c5f5c939a5294e8feabe4a62e25757f865cc", "ev:f6d93b246d334b1d237041bdd8fd48bf5a8fcba0ca9ad0d3dad1a97d45973a88"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /api/v1/orders | order (body, OrderInput, bắt buộc) | OrderInput | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:f1fa988e` |


## Model

### OrderInput (request)

Fact `f:dcc8c0eb` · inferred (pydantic.v2_required_no_default) / full · khai ở schemas.py:3

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| product | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:main.py:4 | POST | /api/v1/orders | routes.py::create_order_endpoint | fact:dcc8c0eb0adcb056e555a2b37d825caa4f678921c46230b0e3c16522c7942d52 | (rỗng) | 200 | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:f1fa988e47e2a3b671afa9ec746dcd3f1a10fa672c63b2b3f128042503181ad8` | `ev:2becbca1585fd97e1e01a34a3c4722805a6fc875c8a390e80adc870d69fc1b55` (main.py:4), `ev:59e78ed9dd3d61ece95ba8d4a912b300d2363bfb166b2f3c58d57e34b7610062` (main.py:5), `ev:3528a71b7b21d26a1f2c8fbab068e20206ba934411a0345d90e59926e26447bb` (routes.py:9), `ev:c72684b3b361929edcd571846b8c4707da451d4d3fec35810123b29d89659715` (routes.py:9-10), `ev:c9053d39c94b385cc002f43ef4c1c5f5c939a5294e8feabe4a62e25757f865cc` (routes.py:10) | inferred | partial |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| OrderInput | fact:dcc8c0eb0adcb056e555a2b37d825caa4f678921c46230b0e3c16522c7942d52 | schemas.py:3 |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "OrderInput_dcc8c0eb": {
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
            "fact:dcc8c0eb0adcb056e555a2b37d825caa4f678921c46230b0e3c16522c7942d52"
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
        "operationId": "op_f1fa988e47e2a3b6",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/OrderInput_dcc8c0eb"
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
            "ev:2becbca1585fd97e1e01a34a3c4722805a6fc875c8a390e80adc870d69fc1b55",
            "ev:3528a71b7b21d26a1f2c8fbab068e20206ba934411a0345d90e59926e26447bb",
            "ev:59e78ed9dd3d61ece95ba8d4a912b300d2363bfb166b2f3c58d57e34b7610062",
            "ev:c72684b3b361929edcd571846b8c4707da451d4d3fec35810123b29d89659715",
            "ev:c9053d39c94b385cc002f43ef4c1c5f5c939a5294e8feabe4a62e25757f865cc"
          ],
          "fact_ids": [
            "fact:f1fa988e47e2a3b671afa9ec746dcd3f1a10fa672c63b2b3f128042503181ad8"
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
