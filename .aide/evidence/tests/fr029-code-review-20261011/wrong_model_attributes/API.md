---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:25dca7ae41f4d0fd45b528deac6fc907621562d5a991660af2f9f72566891c2b"
owner_component_id: "cmp_d7c4136dc2d44875bc560d4f83db9c566ebd1689c7b5766897fb74543a97367d"
owner_component: "Mục hàng"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v14"
fact_ids: ["fact:4bff5064c259ffa29772c561c8dd63e1a55a22e1515ceb878fe584a15e9b7bdc", "fact:d022884b4838b8625840bc176a9cae930866aad400b3c85ef4d288b66c6bfb5a", "fact:04148e19f7b62f5fbfcdead819ebc5c36e952b797c8fe81bf409b7004cd69097", "fact:31d45a9293cc95a570746f0e3511cea4c5f66ac08a03c58b652ee857e28e5df2", "fact:55d7fff832214b23e0cb240fe826d7c8d7a926e58f78a22cb8f63e093f90fc9c"]
evidence_ids: ["ev:05e65b02101feb87b3d212ef27fdfc2f277f7247b5bfec1e068235e60d882c5d", "ev:0a7e37052ceb591d1b4d83fedd0bc76eaed57d17d6178e0a88edc41ce3d1c8be", "ev:130addd378a27cd7dad0a92e64499284f6a4ec95bc64fc6329e08119918010d8", "ev:237dceb91a0cf56208e09e7373f44c3c64eb29ae2dcc201db50817a0336d5619", "ev:326870611193f1c9dd4ffdf85b292914dd4643b863cb549bf6b64a3f2ec95062", "ev:42cc58820a2526c59bd55facf8a440903c9b43ee532a7aac8c408c39a43bc2cc", "ev:7f91f43b5306074b8bb09370387bc65d9c855d6642fa65fbf25379ea1cb36d32", "ev:91c2746ac4ec1f87ee73694f8cd211829bcf4270af8ce3099f971f5190c54a7d", "ev:94558d859445cd1078eaffbedb42cd5347d1f2344803d096f0c2f238f5a56aa7", "ev:a2b26be30bb91223d60156a8ec7ad45e15e2200b1ab5557fccb2b886e61bc81f", "ev:aa01cc03bb2e0c1478592a2c4331af6c7c7274d6b399cef7a0d60a74f4ae854f", "ev:d206264f03fe48e7680d7ef8a6161ca615fd3c8d7435b425bf28380efa47af36", "ev:d642c8bb52f59d6de179b39ec46b23c832a8041da1f34aac549ec570360ef3eb", "ev:d68c0d166284a11f3d804be4bf50bc675ceb10070868fd738fa3ed8d1b84ab0c", "ev:dcf5d39056044ee47c2e63ef2543555ad457c9f5e673b9aef4d1f202396cd9b6", "ev:ea7c38e0e1a074d8731e34ada586e74eff1c26e8f7429368e013b3cc8c4fc8e3", "ev:efd382fede8edeaf255cc6d114db7266dad1e20aec65ddedacae04e0be4adc0c", "ev:f53a37be10b4079ae91c7f969d6319e17e8ab6ac3aa36b2b48d4d43dbc88ba02", "ev:f7dcf72ff8813243f08a4632df4ad81ce492e57f1867879d72236162238b26f2"]
---
# API — Mục hàng

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /api/v1/items/ | item (body, ItemIn, bắt buộc) | ItemIn | ItemOut | 201 | dependency: (không có); auth: unknown — Không thấy dependency; không kết luận route công khai | inferred (fastapi.json_body_media, fastapi.return_annotation_response_model) / partial | `f:d022884b` |
| GET | /api/v1/items/{item_id} | item_id (path, integer, bắt buộc); verbose (query, boolean, tùy chọn) | (không có) | ItemOut | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy dependency; không kết luận route công khai | inferred (fastapi.default_status_200, fastapi.return_annotation_response_model, fastapi.scalar_param_query) / partial | `f:4bff5064` |


## Model

### ItemIn (request)

Fact `f:31d45a92` · exact / full · khai ở app/schemas.py:8

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| name | string | True | False |
| price | boolean | True | False |

### ItemOut (response)

Fact `f:04148e19` · exact / full · khai ở app/schemas.py:13

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| id | integer | True | False |
| name | string | True | False |
| tags | list[Tag] | True | False |

### Tag (response, lồng)

Fact `f:55d7fff8` · exact / full · khai ở app/schemas.py:4

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| label | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:5 | POST | /api/v1/items/ | app/api/items.py::create_item | fact:31d45a9293cc95a570746f0e3511cea4c5f66ac08a03c58b652ee857e28e5df2 | fact:04148e19f7b62f5fbfcdead819ebc5c36e952b797c8fe81bf409b7004cd69097 | 201 | dependency: (không có); auth: unknown — Không thấy dependency; không kết luận route công khai | `fact:d022884b4838b8625840bc176a9cae930866aad400b3c85ef4d288b66c6bfb5a` | `ev:ea7c38e0e1a074d8731e34ada586e74eff1c26e8f7429368e013b3cc8c4fc8e3` (app/api/__init__.py:5), `ev:f7dcf72ff8813243f08a4632df4ad81ce492e57f1867879d72236162238b26f2` (app/api/__init__.py:6), `ev:a2b26be30bb91223d60156a8ec7ad45e15e2200b1ab5557fccb2b886e61bc81f` (app/api/items.py:9), `ev:d68c0d166284a11f3d804be4bf50bc675ceb10070868fd738fa3ed8d1b84ab0c` (app/api/items.py:9-10), `ev:05e65b02101feb87b3d212ef27fdfc2f277f7247b5bfec1e068235e60d882c5d` (app/api/items.py:10), `ev:dcf5d39056044ee47c2e63ef2543555ad457c9f5e673b9aef4d1f202396cd9b6` (app/main.py:5), `ev:237dceb91a0cf56208e09e7373f44c3c64eb29ae2dcc201db50817a0336d5619` (app/main.py:6) | inferred | partial |
| app:app/main.py:5 | GET | /api/v1/items/{item_id} | app/api/items.py::read_item | (rỗng) | fact:04148e19f7b62f5fbfcdead819ebc5c36e952b797c8fe81bf409b7004cd69097 | 200 | dependency: (không có); auth: unknown — Không thấy dependency; không kết luận route công khai | `fact:4bff5064c259ffa29772c561c8dd63e1a55a22e1515ceb878fe584a15e9b7bdc` | `ev:ea7c38e0e1a074d8731e34ada586e74eff1c26e8f7429368e013b3cc8c4fc8e3` (app/api/__init__.py:5), `ev:f7dcf72ff8813243f08a4632df4ad81ce492e57f1867879d72236162238b26f2` (app/api/__init__.py:6), `ev:130addd378a27cd7dad0a92e64499284f6a4ec95bc64fc6329e08119918010d8` (app/api/items.py:15-16), `ev:f53a37be10b4079ae91c7f969d6319e17e8ab6ac3aa36b2b48d4d43dbc88ba02` (app/api/items.py:15), `ev:94558d859445cd1078eaffbedb42cd5347d1f2344803d096f0c2f238f5a56aa7` (app/api/items.py:16), `ev:dcf5d39056044ee47c2e63ef2543555ad457c9f5e673b9aef4d1f202396cd9b6` (app/main.py:5), `ev:237dceb91a0cf56208e09e7373f44c3c64eb29ae2dcc201db50817a0336d5619` (app/main.py:6) | inferred | partial |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| ItemIn | fact:31d45a9293cc95a570746f0e3511cea4c5f66ac08a03c58b652ee857e28e5df2 | app/schemas.py:8 |
| ItemOut | fact:04148e19f7b62f5fbfcdead819ebc5c36e952b797c8fe81bf409b7004cd69097 | app/schemas.py:13 |
| Tag | fact:55d7fff832214b23e0cb240fe826d7c8d7a926e58f78a22cb8f63e093f90fc9c | app/schemas.py:4 |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "ItemIn_31d45a92": {
        "properties": {
          "name": {
            "type": "string"
          },
          "price": {
            "type": "boolean"
          }
        },
        "required": [
          "name",
          "price"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:31d45a9293cc95a570746f0e3511cea4c5f66ac08a03c58b652ee857e28e5df2"
          ]
        }
      },
      "ItemOut_04148e19": {
        "properties": {
          "id": {
            "type": "integer"
          },
          "name": {
            "type": "string"
          },
          "tags": {
            "items": {
              "$ref": "#/components/schemas/Tag_55d7fff8"
            },
            "type": "array"
          }
        },
        "required": [
          "id",
          "name",
          "tags"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:04148e19f7b62f5fbfcdead819ebc5c36e952b797c8fe81bf409b7004cd69097"
          ]
        }
      },
      "Tag_55d7fff8": {
        "properties": {
          "label": {
            "type": "string"
          }
        },
        "required": [
          "label"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:55d7fff832214b23e0cb240fe826d7c8d7a926e58f78a22cb8f63e093f90fc9c"
          ]
        }
      }
    }
  },
  "info": {
    "title": "Mục hàng",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/api/v1/items/": {
      "post": {
        "operationId": "op_d022884b4838b862",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/ItemIn_31d45a92"
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
                  "$ref": "#/components/schemas/ItemOut_04148e19"
                }
              }
            },
            "description": "Status code lấy từ source"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:5",
          "evidence_ids": [
            "ev:05e65b02101feb87b3d212ef27fdfc2f277f7247b5bfec1e068235e60d882c5d",
            "ev:237dceb91a0cf56208e09e7373f44c3c64eb29ae2dcc201db50817a0336d5619",
            "ev:a2b26be30bb91223d60156a8ec7ad45e15e2200b1ab5557fccb2b886e61bc81f",
            "ev:d68c0d166284a11f3d804be4bf50bc675ceb10070868fd738fa3ed8d1b84ab0c",
            "ev:dcf5d39056044ee47c2e63ef2543555ad457c9f5e673b9aef4d1f202396cd9b6",
            "ev:ea7c38e0e1a074d8731e34ada586e74eff1c26e8f7429368e013b3cc8c4fc8e3",
            "ev:f7dcf72ff8813243f08a4632df4ad81ce492e57f1867879d72236162238b26f2"
          ],
          "fact_ids": [
            "fact:d022884b4838b8625840bc176a9cae930866aad400b3c85ef4d288b66c6bfb5a"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy dependency; không kết luận route công khai"
            }
          ]
        }
      }
    },
    "/api/v1/items/{item_id}": {
      "get": {
        "operationId": "op_4bff5064c259ffa2",
        "parameters": [
          {
            "in": "path",
            "name": "item_id",
            "required": true,
            "schema": {
              "type": "integer"
            }
          },
          {
            "in": "query",
            "name": "verbose",
            "required": false,
            "schema": {
              "type": "boolean"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ItemOut_04148e19"
                }
              }
            },
            "description": "Status code suy theo fastapi.default_status_200"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:5",
          "evidence_ids": [
            "ev:130addd378a27cd7dad0a92e64499284f6a4ec95bc64fc6329e08119918010d8",
            "ev:237dceb91a0cf56208e09e7373f44c3c64eb29ae2dcc201db50817a0336d5619",
            "ev:94558d859445cd1078eaffbedb42cd5347d1f2344803d096f0c2f238f5a56aa7",
            "ev:dcf5d39056044ee47c2e63ef2543555ad457c9f5e673b9aef4d1f202396cd9b6",
            "ev:ea7c38e0e1a074d8731e34ada586e74eff1c26e8f7429368e013b3cc8c4fc8e3",
            "ev:f53a37be10b4079ae91c7f969d6319e17e8ab6ac3aa36b2b48d4d43dbc88ba02",
            "ev:f7dcf72ff8813243f08a4632df4ad81ce492e57f1867879d72236162238b26f2"
          ],
          "fact_ids": [
            "fact:4bff5064c259ffa29772c561c8dd63e1a55a22e1515ceb878fe584a15e9b7bdc"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy dependency; không kết luận route công khai"
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
