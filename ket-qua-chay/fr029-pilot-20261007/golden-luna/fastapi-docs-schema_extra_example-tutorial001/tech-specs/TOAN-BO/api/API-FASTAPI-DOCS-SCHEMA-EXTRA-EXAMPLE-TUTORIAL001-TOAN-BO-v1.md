---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:eac671b99c35827af2d53586503a7a0f618464e7e905584b56fb15b149ae3f16"
owner_component_id: "cmp_c2be7868938d8e59010bab6a1541d4ca844a882c75005b1dfdf1d92e5e322bbc"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v5"
fact_ids: ["fact:e7d72d4e81b502f49da48f9fe89a702ad2832df940f707496216dc6819f2ab57", "fact:564452dc20528513355aa1d3c6fe1bed75370bf0a37ac666984075c6f1f827ad"]
evidence_ids: ["ev:1a3aefd273feff2f3b80ee2a5c568e95d78030a5d5fbd81e018016d016e77a1c", "ev:35d4202024ea8becd2777ed49d9ec1378b067f373641b20a6363a93fc52bfd5d", "ev:581f4de55c6b8e027ad0ca32d5fb61e9438a11cb2b0b7c070d22e02bbdaf21b1", "ev:7f9f8b55a9ff2aefa56f05f9881ba9ca8405abe97d2f02a5bb3bf799d38ea289", "ev:81a9a477f3b7a31a4fc1f80cd30ae80ac45489e381891833c1845bd685f6a7d3", "ev:b4f4ac90ff6aebf821090f22aae1370eed6eb0587940c58148284dde839a33de", "ev:db86bb1f8488d7c7f693414b3a78f910f8704d6cdbc48b773a0aba08c09223e1", "ev:de901556e68df7e7e88068c08c181fa257924d793eba09c3f467297d5125a6dc", "ev:eb68f20ec294e96f3b3446b280f773a9f5738c207c2f840775ae529316e471ff"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| PUT | /items/{item_id} | item_id (path, integer, bắt buộc); item (body, Item, bắt buộc) | Item | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Không thấy cơ chế xác thực trong mã nguồn đã đọc. | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:e7d72d4e` |


## Model

### Item (request)

Fact `f:564452dc` · exact / full · khai ở schema_extra_example/tutorial001_py310.py:7

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| name | string | True | False |
| description | string | False | True |
| price | number | True | False |
| tax | number | False | True |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:schema_extra_example/tutorial001_py310.py:4 | PUT | /items/{item_id} | schema_extra_example/tutorial001_py310.py::update_item | fact:564452dc20528513355aa1d3c6fe1bed75370bf0a37ac666984075c6f1f827ad | (rỗng) | 200 | unknown — Không thấy cơ chế xác thực trong mã nguồn đã đọc. | `fact:e7d72d4e81b502f49da48f9fe89a702ad2832df940f707496216dc6819f2ab57` | `ev:db86bb1f8488d7c7f693414b3a78f910f8704d6cdbc48b773a0aba08c09223e1` (schema_extra_example/tutorial001_py310.py:4), `ev:581f4de55c6b8e027ad0ca32d5fb61e9438a11cb2b0b7c070d22e02bbdaf21b1` (schema_extra_example/tutorial001_py310.py:27-28), `ev:eb68f20ec294e96f3b3446b280f773a9f5738c207c2f840775ae529316e471ff` (schema_extra_example/tutorial001_py310.py:27), `ev:7f9f8b55a9ff2aefa56f05f9881ba9ca8405abe97d2f02a5bb3bf799d38ea289` (schema_extra_example/tutorial001_py310.py:28) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "Item_564452dc": {
        "properties": {
          "description": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ]
          },
          "name": {
            "type": "string"
          },
          "price": {
            "type": "number"
          },
          "tax": {
            "anyOf": [
              {
                "type": "number"
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "required": [
          "name",
          "price"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:564452dc20528513355aa1d3c6fe1bed75370bf0a37ac666984075c6f1f827ad"
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
    "/items/{item_id}": {
      "put": {
        "operationId": "op_e7d72d4e81b502f4",
        "parameters": [
          {
            "in": "path",
            "name": "item_id",
            "required": true,
            "schema": {
              "type": "integer"
            }
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/Item_564452dc"
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
          "application_id": "app:schema_extra_example/tutorial001_py310.py:4",
          "evidence_ids": [
            "ev:581f4de55c6b8e027ad0ca32d5fb61e9438a11cb2b0b7c070d22e02bbdaf21b1",
            "ev:7f9f8b55a9ff2aefa56f05f9881ba9ca8405abe97d2f02a5bb3bf799d38ea289",
            "ev:db86bb1f8488d7c7f693414b3a78f910f8704d6cdbc48b773a0aba08c09223e1",
            "ev:eb68f20ec294e96f3b3446b280f773a9f5738c207c2f840775ae529316e471ff"
          ],
          "fact_ids": [
            "fact:e7d72d4e81b502f49da48f9fe89a702ad2832df940f707496216dc6819f2ab57"
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
