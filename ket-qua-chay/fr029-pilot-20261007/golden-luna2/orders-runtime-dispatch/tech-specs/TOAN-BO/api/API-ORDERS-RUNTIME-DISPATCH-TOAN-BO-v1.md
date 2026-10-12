---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:8d44108b45c8269ab91b5bf02d96cb3b5a27c46c6e627b50dd398fa7133b9cea"
owner_component_id: "cmp_772a2d777994c952bf24f46554f2da53c4983f5029f01b012459396d1929d2e1"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v7"
fact_ids: ["fact:3e41b6d4c47884ffe7350816bc32f1beed1ba0783aaf1a87edf39654a0ae1f64", "fact:9a3f7bed02916aa76cf42cdee7262c2f95de85db6e195f60c5f382d77c770dc5", "fact:e10353d0279d0b117fa8ca7ee6aa12a14e720faed9e2b9feff167eb848b1fce6", "fact:f1e3052089aa5818b3ed7c95438bdabb056aaa82d92d7dc82e9e7cf8394dfa4c", "fact:a3ba698de978c2e396943a28a42a2699aec33690f1dc6b8a21b8b07f1165e319"]
evidence_ids: ["ev:0957d73b64440ff86fa0e14e3ddabab864b9c008212353c50fc0fce095481aae", "ev:1dfd8922a12fdb7aa07d936e2cbf675893ce4ba0a31f64607dba74121874c7f1", "ev:22b1d9ce16071275eae9f645064de8858627383c9669c49bf21274fe9c0ea9e6", "ev:275b4af442c669f2cb67c328467601230fcc292bcb11d764701e79cef5e54e5f", "ev:3ce99285880fb16f0d167f62c5a96762c0bc5bddc5e4fab8fdab9f5552738b25", "ev:7169fc4d09e91d95ffc5dc2f8793ebc3381143dd2fc43581c219c4403a3fa1cb", "ev:7ba2a8566e46455b980f4987f7a943c7a4266b6c7f9467b0b8914c42f6ed4a6a", "ev:7f85d5f23851930b7204f2acef10f6318d472e7725685ccb8ac853933a7a40b7", "ev:96da31b3714444a48d42319087d24f6ec1541cb3d70f3866d6411f7f0fa071a3", "ev:ab314dabb00b8537acad916d8d4fabeaf0927ad25390b85302b5974c6af97b9b", "ev:b3c828e0bf0a7d255fa5b19cfdb0f41c1ac2fbf116406d4750aa76949c16a320", "ev:c08ebad5d0fe63e41c4c08478b75f6743257c4bf4dc3a10f1fef4daff2eb8f42", "ev:e032a0b1b2fd240718af33e914f5c084d5f19b014b7bf51ee77a53c62fd1eb73", "ev:e0b021c5c26297bc812153cfebbad0a0c96ecdbcb2ddb0ee399cbf768fe915eb", "ev:e91dc9384d382fa7c55d67603ee9da9b8f352fd35681c99f519113d9179df717", "ev:f11ee0464e470f52ef263496f503c8553293d792b6ec5285822ee473d56ecc89"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /api/v1/orders | order (body, OrderInput, bắt buộc) | OrderInput | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:e10353d0` |
| POST | /api/v1/orders/batch/{actions} | actions (path, string, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200) / partial | `f:f1e30520` |
| POST | /api/v1/orders/{order_id}/actions/{action} | order_id (path, integer, bắt buộc); action (path, string, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200) / partial | `f:9a3f7bed` |
| POST | /api/v1/orders/{order_id}/operations/{name} | order_id (path, integer, bắt buộc); name (path, string, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200) / partial | `f:3e41b6d4` |


## Model

### OrderInput (request)

Fact `f:a3ba698d` · inferred (pydantic.v2_required_no_default) / full · khai ở schemas.py:3

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| product | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:main.py:4 | POST | /api/v1/orders | routes.py::create_order_endpoint | fact:a3ba698de978c2e396943a28a42a2699aec33690f1dc6b8a21b8b07f1165e319 | (rỗng) | 200 | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:e10353d0279d0b117fa8ca7ee6aa12a14e720faed9e2b9feff167eb848b1fce6` | `ev:22b1d9ce16071275eae9f645064de8858627383c9669c49bf21274fe9c0ea9e6` (main.py:4), `ev:0957d73b64440ff86fa0e14e3ddabab864b9c008212353c50fc0fce095481aae` (main.py:5), `ev:7ba2a8566e46455b980f4987f7a943c7a4266b6c7f9467b0b8914c42f6ed4a6a` (routes.py:10-11), `ev:c08ebad5d0fe63e41c4c08478b75f6743257c4bf4dc3a10f1fef4daff2eb8f42` (routes.py:10), `ev:f11ee0464e470f52ef263496f503c8553293d792b6ec5285822ee473d56ecc89` (routes.py:11) | inferred | partial |
| app:main.py:4 | POST | /api/v1/orders/batch/{actions} | routes.py::run_batch | (rỗng) | (rỗng) | 200 | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:f1e3052089aa5818b3ed7c95438bdabb056aaa82d92d7dc82e9e7cf8394dfa4c` | `ev:22b1d9ce16071275eae9f645064de8858627383c9669c49bf21274fe9c0ea9e6` (main.py:4), `ev:0957d73b64440ff86fa0e14e3ddabab864b9c008212353c50fc0fce095481aae` (main.py:5), `ev:275b4af442c669f2cb67c328467601230fcc292bcb11d764701e79cef5e54e5f` (routes.py:23), `ev:3ce99285880fb16f0d167f62c5a96762c0bc5bddc5e4fab8fdab9f5552738b25` (routes.py:23-24), `ev:7169fc4d09e91d95ffc5dc2f8793ebc3381143dd2fc43581c219c4403a3fa1cb` (routes.py:24) | inferred | partial |
| app:main.py:4 | POST | /api/v1/orders/{order_id}/actions/{action} | routes.py::run_order_action | (rỗng) | (rỗng) | 200 | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:9a3f7bed02916aa76cf42cdee7262c2f95de85db6e195f60c5f382d77c770dc5` | `ev:22b1d9ce16071275eae9f645064de8858627383c9669c49bf21274fe9c0ea9e6` (main.py:4), `ev:0957d73b64440ff86fa0e14e3ddabab864b9c008212353c50fc0fce095481aae` (main.py:5), `ev:1dfd8922a12fdb7aa07d936e2cbf675893ce4ba0a31f64607dba74121874c7f1` (routes.py:14-15), `ev:e0b021c5c26297bc812153cfebbad0a0c96ecdbcb2ddb0ee399cbf768fe915eb` (routes.py:14), `ev:e91dc9384d382fa7c55d67603ee9da9b8f352fd35681c99f519113d9179df717` (routes.py:15) | inferred | partial |
| app:main.py:4 | POST | /api/v1/orders/{order_id}/operations/{name} | routes.py::run_order_operation | (rỗng) | (rỗng) | 200 | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:3e41b6d4c47884ffe7350816bc32f1beed1ba0783aaf1a87edf39654a0ae1f64` | `ev:22b1d9ce16071275eae9f645064de8858627383c9669c49bf21274fe9c0ea9e6` (main.py:4), `ev:0957d73b64440ff86fa0e14e3ddabab864b9c008212353c50fc0fce095481aae` (main.py:5), `ev:96da31b3714444a48d42319087d24f6ec1541cb3d70f3866d6411f7f0fa071a3` (routes.py:19), `ev:e032a0b1b2fd240718af33e914f5c084d5f19b014b7bf51ee77a53c62fd1eb73` (routes.py:19-20), `ev:7f85d5f23851930b7204f2acef10f6318d472e7725685ccb8ac853933a7a40b7` (routes.py:20) | inferred | partial |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| OrderInput | fact:a3ba698de978c2e396943a28a42a2699aec33690f1dc6b8a21b8b07f1165e319 | schemas.py:3 |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "OrderInput_a3ba698d": {
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
            "fact:a3ba698de978c2e396943a28a42a2699aec33690f1dc6b8a21b8b07f1165e319"
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
        "operationId": "op_e10353d0279d0b11",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/OrderInput_a3ba698d"
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
            "ev:0957d73b64440ff86fa0e14e3ddabab864b9c008212353c50fc0fce095481aae",
            "ev:22b1d9ce16071275eae9f645064de8858627383c9669c49bf21274fe9c0ea9e6",
            "ev:7ba2a8566e46455b980f4987f7a943c7a4266b6c7f9467b0b8914c42f6ed4a6a",
            "ev:c08ebad5d0fe63e41c4c08478b75f6743257c4bf4dc3a10f1fef4daff2eb8f42",
            "ev:f11ee0464e470f52ef263496f503c8553293d792b6ec5285822ee473d56ecc89"
          ],
          "fact_ids": [
            "fact:e10353d0279d0b117fa8ca7ee6aa12a14e720faed9e2b9feff167eb848b1fce6"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn."
            }
          ]
        }
      }
    },
    "/api/v1/orders/batch/{actions}": {
      "post": {
        "operationId": "op_f1e3052089aa5818",
        "parameters": [
          {
            "in": "path",
            "name": "actions",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:main.py:4",
          "evidence_ids": [
            "ev:0957d73b64440ff86fa0e14e3ddabab864b9c008212353c50fc0fce095481aae",
            "ev:22b1d9ce16071275eae9f645064de8858627383c9669c49bf21274fe9c0ea9e6",
            "ev:275b4af442c669f2cb67c328467601230fcc292bcb11d764701e79cef5e54e5f",
            "ev:3ce99285880fb16f0d167f62c5a96762c0bc5bddc5e4fab8fdab9f5552738b25",
            "ev:7169fc4d09e91d95ffc5dc2f8793ebc3381143dd2fc43581c219c4403a3fa1cb"
          ],
          "fact_ids": [
            "fact:f1e3052089aa5818b3ed7c95438bdabb056aaa82d92d7dc82e9e7cf8394dfa4c"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn."
            }
          ]
        }
      }
    },
    "/api/v1/orders/{order_id}/actions/{action}": {
      "post": {
        "operationId": "op_9a3f7bed02916aa7",
        "parameters": [
          {
            "in": "path",
            "name": "order_id",
            "required": true,
            "schema": {
              "type": "integer"
            }
          },
          {
            "in": "path",
            "name": "action",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:main.py:4",
          "evidence_ids": [
            "ev:0957d73b64440ff86fa0e14e3ddabab864b9c008212353c50fc0fce095481aae",
            "ev:1dfd8922a12fdb7aa07d936e2cbf675893ce4ba0a31f64607dba74121874c7f1",
            "ev:22b1d9ce16071275eae9f645064de8858627383c9669c49bf21274fe9c0ea9e6",
            "ev:e0b021c5c26297bc812153cfebbad0a0c96ecdbcb2ddb0ee399cbf768fe915eb",
            "ev:e91dc9384d382fa7c55d67603ee9da9b8f352fd35681c99f519113d9179df717"
          ],
          "fact_ids": [
            "fact:9a3f7bed02916aa76cf42cdee7262c2f95de85db6e195f60c5f382d77c770dc5"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn."
            }
          ]
        }
      }
    },
    "/api/v1/orders/{order_id}/operations/{name}": {
      "post": {
        "operationId": "op_3e41b6d4c47884ff",
        "parameters": [
          {
            "in": "path",
            "name": "order_id",
            "required": true,
            "schema": {
              "type": "integer"
            }
          },
          {
            "in": "path",
            "name": "name",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:main.py:4",
          "evidence_ids": [
            "ev:0957d73b64440ff86fa0e14e3ddabab864b9c008212353c50fc0fce095481aae",
            "ev:22b1d9ce16071275eae9f645064de8858627383c9669c49bf21274fe9c0ea9e6",
            "ev:7f85d5f23851930b7204f2acef10f6318d472e7725685ccb8ac853933a7a40b7",
            "ev:96da31b3714444a48d42319087d24f6ec1541cb3d70f3866d6411f7f0fa071a3",
            "ev:e032a0b1b2fd240718af33e914f5c084d5f19b014b7bf51ee77a53c62fd1eb73"
          ],
          "fact_ids": [
            "fact:3e41b6d4c47884ffe7350816bc32f1beed1ba0783aaf1a87edf39654a0ae1f64"
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
