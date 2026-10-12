---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:3df7e7d2177f25da0603482e3cce1c1d8b380eb610c1188f4d497c9948271449"
owner_component_id: "cmp_3f8f65e632aee3971ebfc74990b673a272fabc9ec213073a8510024c7de29df3"
owner_component: "Đơn hàng"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v13"
fact_ids: ["fact:141269e11aadbeb24dd4142857c405d132089868b11f182f2a79bae0db9cad67", "fact:c3f927f5f1ee096b1e2c26e808d8cb4ea0c318ffc9ec513df702edd23becb14f", "fact:152a1767a07f4dbbfa1670d1b79a165f8ac28ca4e71afb726791cf09386d82ea", "fact:2d4ddfdd789f76c885298919f8d80ebadc05ed90cac228278b74abe32e60e365"]
evidence_ids: ["ev:14f5897b3b96d6c642bdfb2f06621d5ea6bedd16d73bca6cd088120eff4f5209", "ev:29c4c4873d49850a41709f36c6040dcef81bbcd0e71649346a89160af23b39fc", "ev:3b8b5c81435c0e097d6d36cd0e152f8a151824fc9a24271b12c72d9c751129cb", "ev:5b7a65b9ceb60a96142bd33eec1f7e2b9680e3c80c698b4fea83dab3351d249a", "ev:62c60e4567f0a15bdb5796aee290935e7874e3f828e5eb900580c9f1fc90ab1e", "ev:62ccaea1cb4afa2c348de5073271a963e6a75265f22c79ba2f59ddc6f559374b", "ev:71ffa5bebeb9c3134ce3a08257b4fa8dc1b747454d054bb0696cb5e7d0fed410", "ev:b191dfa07a54da2bcf3c3c0b5131b28a0cc072e6b45580633f765c865f7533bf", "ev:b61a9c8d175b322a83d5920dcb6512c0ea7c46cbadf680c044a3cfbbcf7a89f5", "ev:c8da9e993b52278bd328851e57739cbdecb98acc0e3c517ee928f2833ad7edc3", "ev:cf5c8ead28fe152622affde3dcb96ebb42334c962136d25a0f41bd34c99c52a1", "ev:e1671146a4654a631beb8c63c8914ca10531e336346eb063b19449bd9ba42e03", "ev:e9f96c344fec709a4afc2788ce84784d4904c0af0c8394cc370f10881e8d5b83", "ev:ee6da2ee7c45bdb91471ee01780f6834bf2c59c3077a1f487857dc07a0a8b2c1", "ev:f3e78b6a23c8c8f3a3eede8405f2b5bcbc7924387dac98061dfa09e272f2b225", "ev:ff7f181885df45f371189a366b61d4b0f29739dddd64b9483da70bf02e7c258a"]
---
# API — Đơn hàng

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /orders | payload (body, OrderIn, bắt buộc) | OrderIn | OrderOut | 201 | dependency: get_db; auth: unknown — Mã nguồn đã đọc chưa chứng minh cơ chế xác thực. | inferred (fastapi.json_body_media) / partial | `f:c3f927f5` |
| GET | /orders/{order_id} | order_id (path, integer, bắt buộc) | (không có) | OrderOut | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Mã nguồn đã đọc chưa chứng minh cơ chế xác thực. | inferred (fastapi.default_status_200) / partial | `f:141269e1` |


## Model

### OrderIn (request)

Fact `f:2d4ddfdd` · inferred (pydantic.v2_required_no_default) / full · khai ở app/schemas.py:4

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| product | string | True | False |
| quantity | integer | True | False |

### OrderOut (response)

Fact `f:152a1767` · inferred (pydantic.v2_required_no_default) / full · khai ở app/schemas.py:9

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| id | integer | True | False |
| product | string | True | False |
| quantity | integer | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:5 | POST | /orders | app/api/orders.py::create_order | fact:2d4ddfdd789f76c885298919f8d80ebadc05ed90cac228278b74abe32e60e365 | fact:152a1767a07f4dbbfa1670d1b79a165f8ac28ca4e71afb726791cf09386d82ea | 201 | dependency: get_db; auth: unknown — Mã nguồn đã đọc chưa chứng minh cơ chế xác thực. | `fact:c3f927f5f1ee096b1e2c26e808d8cb4ea0c318ffc9ec513df702edd23becb14f` | `ev:b61a9c8d175b322a83d5920dcb6512c0ea7c46cbadf680c044a3cfbbcf7a89f5` (app/api/orders.py:7), `ev:5b7a65b9ceb60a96142bd33eec1f7e2b9680e3c80c698b4fea83dab3351d249a` (app/api/orders.py:10), `ev:e9f96c344fec709a4afc2788ce84784d4904c0af0c8394cc370f10881e8d5b83` (app/api/orders.py:10-11), `ev:14f5897b3b96d6c642bdfb2f06621d5ea6bedd16d73bca6cd088120eff4f5209` (app/api/orders.py:11), `ev:f3e78b6a23c8c8f3a3eede8405f2b5bcbc7924387dac98061dfa09e272f2b225` (app/main.py:5), `ev:cf5c8ead28fe152622affde3dcb96ebb42334c962136d25a0f41bd34c99c52a1` (app/main.py:6) | inferred | partial |
| app:app/main.py:5 | GET | /orders/{order_id} | app/api/orders.py::read_order | (rỗng) | fact:152a1767a07f4dbbfa1670d1b79a165f8ac28ca4e71afb726791cf09386d82ea | 200 | dependency: get_db; auth: unknown — Mã nguồn đã đọc chưa chứng minh cơ chế xác thực. | `fact:141269e11aadbeb24dd4142857c405d132089868b11f182f2a79bae0db9cad67` | `ev:b61a9c8d175b322a83d5920dcb6512c0ea7c46cbadf680c044a3cfbbcf7a89f5` (app/api/orders.py:7), `ev:29c4c4873d49850a41709f36c6040dcef81bbcd0e71649346a89160af23b39fc` (app/api/orders.py:15-16), `ev:62c60e4567f0a15bdb5796aee290935e7874e3f828e5eb900580c9f1fc90ab1e` (app/api/orders.py:15), `ev:3b8b5c81435c0e097d6d36cd0e152f8a151824fc9a24271b12c72d9c751129cb` (app/api/orders.py:16), `ev:f3e78b6a23c8c8f3a3eede8405f2b5bcbc7924387dac98061dfa09e272f2b225` (app/main.py:5), `ev:cf5c8ead28fe152622affde3dcb96ebb42334c962136d25a0f41bd34c99c52a1` (app/main.py:6) | inferred | partial |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| OrderIn | fact:2d4ddfdd789f76c885298919f8d80ebadc05ed90cac228278b74abe32e60e365 | app/schemas.py:4 |
| OrderOut | fact:152a1767a07f4dbbfa1670d1b79a165f8ac28ca4e71afb726791cf09386d82ea | app/schemas.py:9 |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "OrderIn_2d4ddfdd": {
        "properties": {
          "product": {
            "type": "string"
          },
          "quantity": {
            "type": "integer"
          }
        },
        "required": [
          "product",
          "quantity"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:2d4ddfdd789f76c885298919f8d80ebadc05ed90cac228278b74abe32e60e365"
          ]
        }
      },
      "OrderOut_152a1767": {
        "properties": {
          "id": {
            "type": "integer"
          },
          "product": {
            "type": "string"
          },
          "quantity": {
            "type": "integer"
          }
        },
        "required": [
          "id",
          "product",
          "quantity"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:152a1767a07f4dbbfa1670d1b79a165f8ac28ca4e71afb726791cf09386d82ea"
          ]
        }
      }
    }
  },
  "info": {
    "title": "Đơn hàng",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/orders": {
      "post": {
        "operationId": "op_c3f927f5f1ee096b",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/OrderIn_2d4ddfdd"
              }
            }
          },
          "required": true
        },
        "responses": {
          "201": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/OrderOut_152a1767"
                }
              }
            },
            "description": "Status code lấy từ source"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:5",
          "evidence_ids": [
            "ev:14f5897b3b96d6c642bdfb2f06621d5ea6bedd16d73bca6cd088120eff4f5209",
            "ev:5b7a65b9ceb60a96142bd33eec1f7e2b9680e3c80c698b4fea83dab3351d249a",
            "ev:b61a9c8d175b322a83d5920dcb6512c0ea7c46cbadf680c044a3cfbbcf7a89f5",
            "ev:cf5c8ead28fe152622affde3dcb96ebb42334c962136d25a0f41bd34c99c52a1",
            "ev:e9f96c344fec709a4afc2788ce84784d4904c0af0c8394cc370f10881e8d5b83",
            "ev:f3e78b6a23c8c8f3a3eede8405f2b5bcbc7924387dac98061dfa09e272f2b225"
          ],
          "fact_ids": [
            "fact:c3f927f5f1ee096b1e2c26e808d8cb4ea0c318ffc9ec513df702edd23becb14f"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Mã nguồn đã đọc chưa chứng minh cơ chế xác thực."
            }
          ]
        }
      }
    },
    "/orders/{order_id}": {
      "get": {
        "operationId": "op_141269e11aadbeb2",
        "parameters": [
          {
            "in": "path",
            "name": "order_id",
            "required": true,
            "schema": {
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/OrderOut_152a1767"
                }
              }
            },
            "description": "Status code suy theo fastapi.default_status_200"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:5",
          "evidence_ids": [
            "ev:29c4c4873d49850a41709f36c6040dcef81bbcd0e71649346a89160af23b39fc",
            "ev:3b8b5c81435c0e097d6d36cd0e152f8a151824fc9a24271b12c72d9c751129cb",
            "ev:62c60e4567f0a15bdb5796aee290935e7874e3f828e5eb900580c9f1fc90ab1e",
            "ev:b61a9c8d175b322a83d5920dcb6512c0ea7c46cbadf680c044a3cfbbcf7a89f5",
            "ev:cf5c8ead28fe152622affde3dcb96ebb42334c962136d25a0f41bd34c99c52a1",
            "ev:f3e78b6a23c8c8f3a3eede8405f2b5bcbc7924387dac98061dfa09e272f2b225"
          ],
          "fact_ids": [
            "fact:141269e11aadbeb24dd4142857c405d132089868b11f182f2a79bae0db9cad67"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Mã nguồn đã đọc chưa chứng minh cơ chế xác thực."
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
