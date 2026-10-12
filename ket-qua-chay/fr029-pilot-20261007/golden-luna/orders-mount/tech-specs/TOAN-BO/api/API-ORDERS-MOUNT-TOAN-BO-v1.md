---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:283b9ffd9b1c73ba155569f9d164e98a53e00fc8b953af432ca2ed2069025301"
owner_component_id: "cmp_d0d0ce1261e0fc5dce592920875ae3a144383ad29e8803214385c12b865756cf"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v5"
fact_ids: ["fact:0fbcbbcac9123664d452d5a2c8a1458221b2628f76640ffe70172a39ea12fa54", "fact:0a7f01e7a50aee9710a63722beac79fdab886b0502b6ea3823fcecb35a08b75f"]
evidence_ids: ["ev:26baa6b2ae90d5a99636f864793a4e45070ca10f08b815f9f69714826c2597f9", "ev:438c655c97610396207cbd1a104f78b15cf3449e6e3ee31234ee402196e08ecf", "ev:59fee056dc5a6ec1bf7a74b02f0b11bca968d7d6244b8ebe652c8f1a1d0804d9", "ev:8640e59c6792324e19145ef5561c26379f98f6c3714c7fdae6d12ab7cb5919c1", "ev:9784a6d2eb4571a20aaeba847ed861dbf4a9b46f28b925b8571cb2f66267980c", "ev:b2cdc5b41e3bb7e0285c0f4dd110f0a02d7a1f378381b0948df5e8f19528b8e2", "ev:edd2411c00d16af419f2d8177599109f8132745effdbc6c44421c99655c786f3", "ev:f682b1103437e47fbbed21db3d6180c2d75b2e7fc5ed95bc59b27324ae8d4eaf"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /api/v1/orders | order (body, OrderInput, bắt buộc) | OrderInput | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:0fbcbbca` |


## Model

### OrderInput (request)

Fact `f:0a7f01e7` · exact / full · khai ở schemas.py:3

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| product | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:main.py:4 | POST | /api/v1/orders | routes.py::create_order_endpoint | fact:0a7f01e7a50aee9710a63722beac79fdab886b0502b6ea3823fcecb35a08b75f | (rỗng) | 200 | unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:0fbcbbcac9123664d452d5a2c8a1458221b2628f76640ffe70172a39ea12fa54` | `ev:b2cdc5b41e3bb7e0285c0f4dd110f0a02d7a1f378381b0948df5e8f19528b8e2` (main.py:4), `ev:8640e59c6792324e19145ef5561c26379f98f6c3714c7fdae6d12ab7cb5919c1` (main.py:6), `ev:f682b1103437e47fbbed21db3d6180c2d75b2e7fc5ed95bc59b27324ae8d4eaf` (main.py:7), `ev:26baa6b2ae90d5a99636f864793a4e45070ca10f08b815f9f69714826c2597f9` (routes.py:9), `ev:59fee056dc5a6ec1bf7a74b02f0b11bca968d7d6244b8ebe652c8f1a1d0804d9` (routes.py:9-10), `ev:438c655c97610396207cbd1a104f78b15cf3449e6e3ee31234ee402196e08ecf` (routes.py:10) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "OrderInput_0a7f01e7": {
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
            "fact:0a7f01e7a50aee9710a63722beac79fdab886b0502b6ea3823fcecb35a08b75f"
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
        "operationId": "op_0fbcbbcac9123664",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/OrderInput_0a7f01e7"
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
            "ev:26baa6b2ae90d5a99636f864793a4e45070ca10f08b815f9f69714826c2597f9",
            "ev:438c655c97610396207cbd1a104f78b15cf3449e6e3ee31234ee402196e08ecf",
            "ev:59fee056dc5a6ec1bf7a74b02f0b11bca968d7d6244b8ebe652c8f1a1d0804d9",
            "ev:8640e59c6792324e19145ef5561c26379f98f6c3714c7fdae6d12ab7cb5919c1",
            "ev:b2cdc5b41e3bb7e0285c0f4dd110f0a02d7a1f378381b0948df5e8f19528b8e2",
            "ev:f682b1103437e47fbbed21db3d6180c2d75b2e7fc5ed95bc59b27324ae8d4eaf"
          ],
          "fact_ids": [
            "fact:0fbcbbcac9123664d452d5a2c8a1458221b2628f76640ffe70172a39ea12fa54"
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
