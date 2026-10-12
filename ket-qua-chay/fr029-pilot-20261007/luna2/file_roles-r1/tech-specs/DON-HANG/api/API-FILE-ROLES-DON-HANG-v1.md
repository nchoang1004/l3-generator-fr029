---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:3df7e7d2177f25da0603482e3cce1c1d8b380eb610c1188f4d497c9948271449"
owner_component_id: "cmp_3f8f65e632aee3971ebfc74990b673a272fabc9ec213073a8510024c7de29df3"
owner_component: "Đơn hàng"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v4"
fact_ids: ["fact:136d6c6d7c7372f1cb3c6b591b3a8a445fce903c94a883fc69cd0f136c6bd3e6", "fact:1e2f286bcf0839a6e93c498b2d076d6a3c9a1f6b2803b4cc1106d77418bd97ba", "fact:152a1767a07f4dbbfa1670d1b79a165f8ac28ca4e71afb726791cf09386d82ea", "fact:2d4ddfdd789f76c885298919f8d80ebadc05ed90cac228278b74abe32e60e365"]
evidence_ids: ["ev:14f5897b3b96d6c642bdfb2f06621d5ea6bedd16d73bca6cd088120eff4f5209", "ev:29c4c4873d49850a41709f36c6040dcef81bbcd0e71649346a89160af23b39fc", "ev:3b8b5c81435c0e097d6d36cd0e152f8a151824fc9a24271b12c72d9c751129cb", "ev:5b7a65b9ceb60a96142bd33eec1f7e2b9680e3c80c698b4fea83dab3351d249a", "ev:62c60e4567f0a15bdb5796aee290935e7874e3f828e5eb900580c9f1fc90ab1e", "ev:62ccaea1cb4afa2c348de5073271a963e6a75265f22c79ba2f59ddc6f559374b", "ev:71ffa5bebeb9c3134ce3a08257b4fa8dc1b747454d054bb0696cb5e7d0fed410", "ev:b191dfa07a54da2bcf3c3c0b5131b28a0cc072e6b45580633f765c865f7533bf", "ev:b61a9c8d175b322a83d5920dcb6512c0ea7c46cbadf680c044a3cfbbcf7a89f5", "ev:c8da9e993b52278bd328851e57739cbdecb98acc0e3c517ee928f2833ad7edc3", "ev:e1671146a4654a631beb8c63c8914ca10531e336346eb063b19449bd9ba42e03", "ev:e9f96c344fec709a4afc2788ce84784d4904c0af0c8394cc370f10881e8d5b83", "ev:ee6da2ee7c45bdb91471ee01780f6834bf2c59c3077a1f487857dc07a0a8b2c1", "ev:f3e78b6a23c8c8f3a3eede8405f2b5bcbc7924387dac98061dfa09e272f2b225", "ev:ff7f181885df45f371189a366b61d4b0f29739dddd64b9483da70bf02e7c258a"]
---
# API — Đơn hàng

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /orders | payload (body, OrderIn, bắt buộc) | OrderIn | OrderOut | 201 | unknown — Không thấy cơ chế xác thực trong mã nguồn đã đọc. | inferred (fastapi.model_param_body) / partial | `f:136d6c6d` |
| GET | /orders/{order_id} | order_id (path, integer, bắt buộc) | (không có) | OrderOut | 200 (suy theo fastapi.default_status_200) | unknown — Không thấy cơ chế xác thực trong mã nguồn đã đọc. | inferred (fastapi.default_status_200) / partial | `f:1e2f286b` |


## Model

### OrderIn (request)

Fact `f:2d4ddfdd` · inferred / full · khai ở app/schemas.py:4

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| product | string | True | False |
| quantity | integer | True | False |

### OrderOut (response)

Fact `f:152a1767` · inferred / full · khai ở app/schemas.py:9

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| id | integer | True | False |
| product | string | True | False |
| quantity | integer | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:5 | POST | /orders | app/api/orders.py::create_order | fact:2d4ddfdd789f76c885298919f8d80ebadc05ed90cac228278b74abe32e60e365 | fact:152a1767a07f4dbbfa1670d1b79a165f8ac28ca4e71afb726791cf09386d82ea | 201 | unknown — Không thấy cơ chế xác thực trong mã nguồn đã đọc. | `fact:136d6c6d7c7372f1cb3c6b591b3a8a445fce903c94a883fc69cd0f136c6bd3e6` | `ev:b61a9c8d175b322a83d5920dcb6512c0ea7c46cbadf680c044a3cfbbcf7a89f5` (app/api/orders.py:7), `ev:5b7a65b9ceb60a96142bd33eec1f7e2b9680e3c80c698b4fea83dab3351d249a` (app/api/orders.py:10), `ev:e9f96c344fec709a4afc2788ce84784d4904c0af0c8394cc370f10881e8d5b83` (app/api/orders.py:10-11), `ev:14f5897b3b96d6c642bdfb2f06621d5ea6bedd16d73bca6cd088120eff4f5209` (app/api/orders.py:11), `ev:f3e78b6a23c8c8f3a3eede8405f2b5bcbc7924387dac98061dfa09e272f2b225` (app/main.py:5) | inferred | partial |
| app:app/main.py:5 | GET | /orders/{order_id} | app/api/orders.py::read_order | (rỗng) | fact:152a1767a07f4dbbfa1670d1b79a165f8ac28ca4e71afb726791cf09386d82ea | 200 | unknown — Không thấy cơ chế xác thực trong mã nguồn đã đọc. | `fact:1e2f286bcf0839a6e93c498b2d076d6a3c9a1f6b2803b4cc1106d77418bd97ba` | `ev:b61a9c8d175b322a83d5920dcb6512c0ea7c46cbadf680c044a3cfbbcf7a89f5` (app/api/orders.py:7), `ev:29c4c4873d49850a41709f36c6040dcef81bbcd0e71649346a89160af23b39fc` (app/api/orders.py:15-16), `ev:62c60e4567f0a15bdb5796aee290935e7874e3f828e5eb900580c9f1fc90ab1e` (app/api/orders.py:15), `ev:3b8b5c81435c0e097d6d36cd0e152f8a151824fc9a24271b12c72d9c751129cb` (app/api/orders.py:16), `ev:f3e78b6a23c8c8f3a3eede8405f2b5bcbc7924387dac98061dfa09e272f2b225` (app/main.py:5) | inferred | partial |

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
        "operationId": "op_136d6c6d7c7372f1",
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
            "ev:e9f96c344fec709a4afc2788ce84784d4904c0af0c8394cc370f10881e8d5b83",
            "ev:f3e78b6a23c8c8f3a3eede8405f2b5bcbc7924387dac98061dfa09e272f2b225"
          ],
          "fact_ids": [
            "fact:136d6c6d7c7372f1cb3c6b591b3a8a445fce903c94a883fc69cd0f136c6bd3e6"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực trong mã nguồn đã đọc."
            }
          ]
        }
      }
    },
    "/orders/{order_id}": {
      "get": {
        "operationId": "op_1e2f286bcf0839a6",
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
            "ev:f3e78b6a23c8c8f3a3eede8405f2b5bcbc7924387dac98061dfa09e272f2b225"
          ],
          "fact_ids": [
            "fact:1e2f286bcf0839a6e93c498b2d076d6a3c9a1f6b2803b4cc1106d77418bd97ba"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực trong mã nguồn đã đọc."
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
