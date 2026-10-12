---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:1b33d7f5ef0b0f5a9434a34b0e55cc952ef2f4d2f3f7069fa13515f916707e9f"
owner_component_id: "cmp_9c9b40acef388f58698d886f33995e94312e9b897089507a591b21c6ed1844cb"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v7"
fact_ids: ["fact:be4823b534db010428f922c6fd3e9bbba0a3edb6472147fbf668f5d94ddc02cc", "fact:7a2c001468b28516f8261b537991115b2631b233a01574f82923911c64a6577a"]
evidence_ids: ["ev:3261f066951c9afd9b91351d517f30ebac6d43546c713f812f5ffb647ed92bfe", "ev:4d674c105cf52e8acc3738126b41351ebb6e3e22fc48f303835d0b5fb5d71e97", "ev:5d6f7bbf4593dfa825c4949ce67188dc511471c421ebdf3dfff3de6c798078d0", "ev:812229c493b4d99402ff13138f2a84392d8223630ff087a13d1cfd044b957d66", "ev:a8a9b7766e87e24f66b488e8819c08fab5c26a2d8ef8e8651bb63b63c3b61818", "ev:a92242ebe1e3a03c90f89acdeeae0d2019403d039b5d1b59f81813f5d23e09d6", "ev:e3e9f8eca0288eaf6cb206afc116f0d509de6ad1989781b78dcf755edc3faf5f", "ev:e50ceaed8de08af9ec8c674d623347bdc48bb52fd0d24410c3a9f783ca3a62f4"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /api/v1/orders | order (body, OrderInput, bắt buộc) | OrderInput | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200, fastapi.json_body_media) / partial | `f:be4823b5` |


## Model

### OrderInput (request)

Fact `f:7a2c0014` · inferred (pydantic.v2_required_no_default) / full · khai ở schemas.py:3

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| product | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:main.py:5 | POST | /api/v1/orders | routes.py::create_order_endpoint | fact:7a2c001468b28516f8261b537991115b2631b233a01574f82923911c64a6577a | (rỗng) | 200 | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:be4823b534db010428f922c6fd3e9bbba0a3edb6472147fbf668f5d94ddc02cc` | `ev:a92242ebe1e3a03c90f89acdeeae0d2019403d039b5d1b59f81813f5d23e09d6` (main.py:5), `ev:812229c493b4d99402ff13138f2a84392d8223630ff087a13d1cfd044b957d66` (main.py:6), `ev:3261f066951c9afd9b91351d517f30ebac6d43546c713f812f5ffb647ed92bfe` (registration.py:2), `ev:5d6f7bbf4593dfa825c4949ce67188dc511471c421ebdf3dfff3de6c798078d0` (routes.py:9-10), `ev:e50ceaed8de08af9ec8c674d623347bdc48bb52fd0d24410c3a9f783ca3a62f4` (routes.py:9), `ev:e3e9f8eca0288eaf6cb206afc116f0d509de6ad1989781b78dcf755edc3faf5f` (routes.py:10) | inferred | partial |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| OrderInput | fact:7a2c001468b28516f8261b537991115b2631b233a01574f82923911c64a6577a | schemas.py:3 |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "OrderInput_7a2c0014": {
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
            "fact:7a2c001468b28516f8261b537991115b2631b233a01574f82923911c64a6577a"
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
        "operationId": "op_be4823b534db0104",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/OrderInput_7a2c0014"
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
          "application_id": "app:main.py:5",
          "evidence_ids": [
            "ev:3261f066951c9afd9b91351d517f30ebac6d43546c713f812f5ffb647ed92bfe",
            "ev:5d6f7bbf4593dfa825c4949ce67188dc511471c421ebdf3dfff3de6c798078d0",
            "ev:812229c493b4d99402ff13138f2a84392d8223630ff087a13d1cfd044b957d66",
            "ev:a92242ebe1e3a03c90f89acdeeae0d2019403d039b5d1b59f81813f5d23e09d6",
            "ev:e3e9f8eca0288eaf6cb206afc116f0d509de6ad1989781b78dcf755edc3faf5f",
            "ev:e50ceaed8de08af9ec8c674d623347bdc48bb52fd0d24410c3a9f783ca3a62f4"
          ],
          "fact_ids": [
            "fact:be4823b534db010428f922c6fd3e9bbba0a3edb6472147fbf668f5d94ddc02cc"
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
