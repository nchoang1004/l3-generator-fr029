---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:250a5bacad9a853b77d19e383811ac3bb8d7b4ba85789c92dd722f0d7b6dcc95"
owner_component_id: "cmp_dfe74efc2c7423af29ea8e9399da9ed53514bfec76376c6552f602101ff412d5"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v5"
fact_ids: ["fact:6c9fa2c9f3efb7c836dfbd2f26459805d04bbe8466f9e9b9526e11bbfed9185d", "fact:c6973ea7334b8d79d5778ebc4da138248a810d1d18fae3bb8a1e1d13348f9552"]
evidence_ids: ["ev:1dc0c5824b4c7327ab04f9c5e89a61a3b7c5fd2443e0d5dc9d4825ce20de201c", "ev:5861af712d06c346c0146349100970274c43986e126230b827c363a3b0ca2e06", "ev:ab952219e2e3d70d34575d00be52a7c48aab02131846bbf2c6d5df8b238fe092", "ev:d435b8bdc888d1c12b1afbfdcc5de013784d3352da52c00083f0eb69606e966d", "ev:db1ddd38a299808a025d18cc23d182592b883357621caacd297a28a91c80d904", "ev:e34a4ff5c672f44c1b0412445e65e3a707da7de7263a5d5a88df3206c35c9d67", "ev:f653f998ef2586e58951736013f8345950615707dd61b26a9dc5979a5d7ec686"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /api/v1/orders | order (body, OrderInput, bắt buộc) | OrderInput | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:6c9fa2c9` |


## Model

### OrderInput (request)

Fact `f:c6973ea7` · inferred / full · khai ở schemas.py:3

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| product | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:main.py:4 | POST | /api/v1/orders | routes.py::create_order_endpoint | fact:c6973ea7334b8d79d5778ebc4da138248a810d1d18fae3bb8a1e1d13348f9552 | (rỗng) | 200 | unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn | `fact:6c9fa2c9f3efb7c836dfbd2f26459805d04bbe8466f9e9b9526e11bbfed9185d` | `ev:e34a4ff5c672f44c1b0412445e65e3a707da7de7263a5d5a88df3206c35c9d67` (main.py:4), `ev:d435b8bdc888d1c12b1afbfdcc5de013784d3352da52c00083f0eb69606e966d` (main.py:5), `ev:ab952219e2e3d70d34575d00be52a7c48aab02131846bbf2c6d5df8b238fe092` (routes.py:9), `ev:db1ddd38a299808a025d18cc23d182592b883357621caacd297a28a91c80d904` (routes.py:9-10), `ev:5861af712d06c346c0146349100970274c43986e126230b827c363a3b0ca2e06` (routes.py:10) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "OrderInput_c6973ea7": {
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
            "fact:c6973ea7334b8d79d5778ebc4da138248a810d1d18fae3bb8a1e1d13348f9552"
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
        "operationId": "op_6c9fa2c9f3efb7c8",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/OrderInput_c6973ea7"
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
            "ev:5861af712d06c346c0146349100970274c43986e126230b827c363a3b0ca2e06",
            "ev:ab952219e2e3d70d34575d00be52a7c48aab02131846bbf2c6d5df8b238fe092",
            "ev:d435b8bdc888d1c12b1afbfdcc5de013784d3352da52c00083f0eb69606e966d",
            "ev:db1ddd38a299808a025d18cc23d182592b883357621caacd297a28a91c80d904",
            "ev:e34a4ff5c672f44c1b0412445e65e3a707da7de7263a5d5a88df3206c35c9d67"
          ],
          "fact_ids": [
            "fact:6c9fa2c9f3efb7c836dfbd2f26459805d04bbe8466f9e9b9526e11bbfed9185d"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn"
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
