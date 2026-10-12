---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:1326eda69bd4f7d71bdf7ea9a40c2598bb3e59fa328fc2de8fecf8547874c438"
owner_component_id: "cmp_6d46c07ffda45960997d2c200c058af2acd32c1247cf8f8721f051fd6e253cb0"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v5"
fact_ids: ["fact:e8daabaa4d6970f35a242bf0bd108b2bf22c73ecbbb24150d72472d65d43d119", "fact:3327e5dac7114ede05f9208609ab438ff9c3ab2b5745d94643a9e5b030dddf35"]
evidence_ids: ["ev:1e99daf6b9db01718476929a73b92761ece424e9326fd82e3ef456bf8be96bd1", "ev:35b7ef2c8665efdb71ddcc28c183705802039b96070c6793c84226880cea38a0", "ev:88eed7570027e61cf8873b0bd0b60d3d9198572e82de71ddba1c260812314068", "ev:af5c48639c18750bd6d8b77f4f6a6f94b77bb1fee91a9b910d0a9a2fdda6628e", "ev:c7a91ff1ac99225575c2fd3b2da936f73f8c6040a0bd511106d2de4dbc7028e1", "ev:dc81d7eb71184c62d2973ff3d54812af4a5333964338d214341f77796e755fbb", "ev:f7215a17a6187c9e0f3212b856ca0685bb0cabca4621e9b2aa1387b8186ec3ab"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /api/v2/orders | order (body, OrderInput, bắt buộc) | OrderInput | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Không thấy khai báo cơ chế xác thực cho route này | inferred (fastapi.default_status_200, fastapi.json_body_media) / partial | `f:e8daabaa` |


## Model

### OrderInput (request)

Fact `f:3327e5da` · inferred / full · khai ở schemas.py:3

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| product | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:main.py:4 | POST | /api/v2/orders | routes.py::create_order_endpoint | fact:3327e5dac7114ede05f9208609ab438ff9c3ab2b5745d94643a9e5b030dddf35 | (rỗng) | 200 | unknown — Không thấy khai báo cơ chế xác thực cho route này | `fact:e8daabaa4d6970f35a242bf0bd108b2bf22c73ecbbb24150d72472d65d43d119` | `ev:af5c48639c18750bd6d8b77f4f6a6f94b77bb1fee91a9b910d0a9a2fdda6628e` (main.py:4), `ev:1e99daf6b9db01718476929a73b92761ece424e9326fd82e3ef456bf8be96bd1` (main.py:5), `ev:dc81d7eb71184c62d2973ff3d54812af4a5333964338d214341f77796e755fbb` (routes.py:9), `ev:f7215a17a6187c9e0f3212b856ca0685bb0cabca4621e9b2aa1387b8186ec3ab` (routes.py:9-10), `ev:88eed7570027e61cf8873b0bd0b60d3d9198572e82de71ddba1c260812314068` (routes.py:10) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "OrderInput_3327e5da": {
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
            "fact:3327e5dac7114ede05f9208609ab438ff9c3ab2b5745d94643a9e5b030dddf35"
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
    "/api/v2/orders": {
      "post": {
        "operationId": "op_e8daabaa4d6970f3",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/OrderInput_3327e5da"
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
            "ev:1e99daf6b9db01718476929a73b92761ece424e9326fd82e3ef456bf8be96bd1",
            "ev:88eed7570027e61cf8873b0bd0b60d3d9198572e82de71ddba1c260812314068",
            "ev:af5c48639c18750bd6d8b77f4f6a6f94b77bb1fee91a9b910d0a9a2fdda6628e",
            "ev:dc81d7eb71184c62d2973ff3d54812af4a5333964338d214341f77796e755fbb",
            "ev:f7215a17a6187c9e0f3212b856ca0685bb0cabca4621e9b2aa1387b8186ec3ab"
          ],
          "fact_ids": [
            "fact:e8daabaa4d6970f35a242bf0bd108b2bf22c73ecbbb24150d72472d65d43d119"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy khai báo cơ chế xác thực cho route này"
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
