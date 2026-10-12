---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:f2ff94965085f7055cca0d20f4a131c55bd99a47f3917a8d96f4dde2592ff747"
owner_component_id: "cmp_fd5f3fda3a38acb293f59c8f6a3f68b193bff8ef856144b4b56eca7f19ba1882"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v7"
fact_ids: ["fact:2d61c34d88ffe3b6049f728c37acdee1625e4a2d2a187d291546ef8a56e92f82", "fact:37c4a0371c31268014ca14391030299161de633927457cebcab0252f62eaf934", "fact:da520f146e842d47b24c4a3759c9fab1a49b1a1fe239b5b02a02f6f798e9b695"]
evidence_ids: ["ev:057d020e66fa386d8b666b5b576b53c7817ec3e2896c2ffa9045ae07e2ca69c7", "ev:4f4b4dbed3cd825493d31b9e49ece722aff0728646ad331b395d9e4b1cc28b51", "ev:781256139f5f7cac0cca4f21bc6be474e7d4cf16e741fb5582e86cfb4ca36ce9", "ev:798069713ff492029dc6dd83775f2a3b7eec7f8a7048beef06f4c8e1c7fb4881", "ev:8816d585a840fe62755d48865697bd115f89d8a8bf0313af66aeb6a22dd0ff1f", "ev:8ddf264c1dec53f14058b4d2d908b01321d93329afc50b9e596a7fbbe8465b41", "ev:8f35bd2ca5846c6d7bec27d14949e9eea3cff8a5379817da31b3d870d8ee5df3", "ev:b9b413d3df2cc4c5e57e3082f3f1a7167a5aa531cdb20017539e784f0eba69aa", "ev:c5c7035bc61e6159f7091f1605dc5cbdd80aab857111ea96bc1f13c3cdb3a408", "ev:d4d110cdb2b559e8105339bf60b96eff98993437645dba4cd292fe460192cc2d"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /api/v1/orders | order (body, OrderInput, bắt buộc) | OrderInput | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo. | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:2d61c34d` |
| POST | /api/v1/orders/{order_id}/notify | order_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo. | inferred (fastapi.default_status_200) / partial | `f:37c4a037` |


## Model

### OrderInput (request)

Fact `f:da520f14` · inferred (pydantic.v2_required_no_default) / full · khai ở schemas.py:3

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| product | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:main.py:4 | POST | /api/v1/orders | routes.py::create_order_endpoint | fact:da520f146e842d47b24c4a3759c9fab1a49b1a1fe239b5b02a02f6f798e9b695 | (rỗng) | 200 | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo. | `fact:2d61c34d88ffe3b6049f728c37acdee1625e4a2d2a187d291546ef8a56e92f82` | `ev:c5c7035bc61e6159f7091f1605dc5cbdd80aab857111ea96bc1f13c3cdb3a408` (main.py:4), `ev:057d020e66fa386d8b666b5b576b53c7817ec3e2896c2ffa9045ae07e2ca69c7` (main.py:5), `ev:781256139f5f7cac0cca4f21bc6be474e7d4cf16e741fb5582e86cfb4ca36ce9` (routes.py:12), `ev:8816d585a840fe62755d48865697bd115f89d8a8bf0313af66aeb6a22dd0ff1f` (routes.py:12-13), `ev:b9b413d3df2cc4c5e57e3082f3f1a7167a5aa531cdb20017539e784f0eba69aa` (routes.py:13) | inferred | partial |
| app:main.py:4 | POST | /api/v1/orders/{order_id}/notify | routes.py::notify_order | (rỗng) | (rỗng) | 200 | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo. | `fact:37c4a0371c31268014ca14391030299161de633927457cebcab0252f62eaf934` | `ev:c5c7035bc61e6159f7091f1605dc5cbdd80aab857111ea96bc1f13c3cdb3a408` (main.py:4), `ev:057d020e66fa386d8b666b5b576b53c7817ec3e2896c2ffa9045ae07e2ca69c7` (main.py:5), `ev:798069713ff492029dc6dd83775f2a3b7eec7f8a7048beef06f4c8e1c7fb4881` (routes.py:16), `ev:8f35bd2ca5846c6d7bec27d14949e9eea3cff8a5379817da31b3d870d8ee5df3` (routes.py:16-17), `ev:4f4b4dbed3cd825493d31b9e49ece722aff0728646ad331b395d9e4b1cc28b51` (routes.py:17) | inferred | partial |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| OrderInput | fact:da520f146e842d47b24c4a3759c9fab1a49b1a1fe239b5b02a02f6f798e9b695 | schemas.py:3 |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "OrderInput_da520f14": {
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
            "fact:da520f146e842d47b24c4a3759c9fab1a49b1a1fe239b5b02a02f6f798e9b695"
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
        "operationId": "op_2d61c34d88ffe3b6",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/OrderInput_da520f14"
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
            "ev:057d020e66fa386d8b666b5b576b53c7817ec3e2896c2ffa9045ae07e2ca69c7",
            "ev:781256139f5f7cac0cca4f21bc6be474e7d4cf16e741fb5582e86cfb4ca36ce9",
            "ev:8816d585a840fe62755d48865697bd115f89d8a8bf0313af66aeb6a22dd0ff1f",
            "ev:b9b413d3df2cc4c5e57e3082f3f1a7167a5aa531cdb20017539e784f0eba69aa",
            "ev:c5c7035bc61e6159f7091f1605dc5cbdd80aab857111ea96bc1f13c3cdb3a408"
          ],
          "fact_ids": [
            "fact:2d61c34d88ffe3b6049f728c37acdee1625e4a2d2a187d291546ef8a56e92f82"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo."
            }
          ]
        }
      }
    },
    "/api/v1/orders/{order_id}/notify": {
      "post": {
        "operationId": "op_37c4a0371c312680",
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
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:main.py:4",
          "evidence_ids": [
            "ev:057d020e66fa386d8b666b5b576b53c7817ec3e2896c2ffa9045ae07e2ca69c7",
            "ev:4f4b4dbed3cd825493d31b9e49ece722aff0728646ad331b395d9e4b1cc28b51",
            "ev:798069713ff492029dc6dd83775f2a3b7eec7f8a7048beef06f4c8e1c7fb4881",
            "ev:8f35bd2ca5846c6d7bec27d14949e9eea3cff8a5379817da31b3d870d8ee5df3",
            "ev:c5c7035bc61e6159f7091f1605dc5cbdd80aab857111ea96bc1f13c3cdb3a408"
          ],
          "fact_ids": [
            "fact:37c4a0371c31268014ca14391030299161de633927457cebcab0252f62eaf934"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo."
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
