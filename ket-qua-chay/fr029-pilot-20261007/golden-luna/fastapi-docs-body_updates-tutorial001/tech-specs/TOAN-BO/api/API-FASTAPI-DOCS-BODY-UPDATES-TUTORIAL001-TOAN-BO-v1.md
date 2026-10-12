---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:5221f8bbd9bc5868ad08768d2555ff71f5e929d4ba20726a1f041fc799d7bb9a"
owner_component_id: "cmp_617cbac4f3d176f4e3dfe8cb20face2ddf3904332e308c59e5779a45c574c026"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v5"
fact_ids: ["fact:778d74dfff440aa856a0f7b517028a60e428f12634e67783a67340ae1afeda94", "fact:f51b64031a6661c3b510aed95273b407023f4e65527c28f1122437ba65bf0032", "fact:4956f971e1e08f7ee4a9ec8fd8f8120b4124ce78833f3aab6257f1332251e10c"]
evidence_ids: ["ev:0b88b8b7381ec9c9df6e2c45f714861b65f24b5b2ebb2ffdc63869eb8f5047b3", "ev:207166c1be1cabc3296124c8ac9d2ff5d8bbe74a6aceffa6d308f74deacb439b", "ev:34bdc6342828f0378f06ac9cf09330b8dcf5304f8f4f56faf86ea0914a0c5209", "ev:3b5846b21fb78436a8a5b84970c16962cb14c991fa95c1c463af5d59612a056c", "ev:3d74e3573800f42896b5aa06c1f2baf98698acfd17675e45da75b881ddc2259e", "ev:4e5ff6d19e4d732430235cbceb9d47d250c48f0781fa9b5e3ffd03548ec1956d", "ev:549ed6262bdccbba2dfcf2c90c4097942d5e89cbd06d5f6760e90e288fd665ef", "ev:62713cbb424ed623b26261f21e7dfeed62fffa4f9143aca9261972d37be2f9b6", "ev:867c9ce086af734888245aee0a521dfd78a92a84acf2672e15ecc3fe80661c62", "ev:a74b97e0628b6921784183c8546ae3c864a5ed759cd9c508cdf188ec14ba38c0", "ev:ee80a0462671fa5803eb06f087b081189a8881045c16da318c0f5935a9595083", "ev:fa4d79acec67a557d8110bd7f107d2d1a0186ef796d6a753f6d8b17be4b5e7c8", "ev:ff2268d333f43c6866a3696cacb812df141c63f417f533a0c002bc6fee259ead"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /items/{item_id} | item_id (path, string, bắt buộc) | (không có) | Item | 200 (suy theo fastapi.default_status_200) | unknown — Không thấy khai báo cơ chế xác thực cho route này. | inferred (fastapi.default_status_200) / partial | `f:f51b6403` |
| PUT | /items/{item_id} | item_id (path, string, bắt buộc); item (body, Item, bắt buộc) | Item | Item | 200 (suy theo fastapi.default_status_200) | unknown — Không thấy khai báo cơ chế xác thực cho route này. | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:778d74df` |


## Model

### Item (response)

Fact `f:4956f971` · exact / full · khai ở body_updates/tutorial001_py310.py:8

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| name | string | False | True |
| description | string | False | True |
| price | number | False | True |
| tax | number | False | False |
| tags | list[string] | False | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:body_updates/tutorial001_py310.py:5 | GET | /items/{item_id} | body_updates/tutorial001_py310.py::read_item | (rỗng) | fact:4956f971e1e08f7ee4a9ec8fd8f8120b4124ce78833f3aab6257f1332251e10c | 200 | unknown — Không thấy khai báo cơ chế xác thực cho route này. | `fact:f51b64031a6661c3b510aed95273b407023f4e65527c28f1122437ba65bf0032` | `ev:3d74e3573800f42896b5aa06c1f2baf98698acfd17675e45da75b881ddc2259e` (body_updates/tutorial001_py310.py:5), `ev:62713cbb424ed623b26261f21e7dfeed62fffa4f9143aca9261972d37be2f9b6` (body_updates/tutorial001_py310.py:23-24), `ev:867c9ce086af734888245aee0a521dfd78a92a84acf2672e15ecc3fe80661c62` (body_updates/tutorial001_py310.py:23), `ev:3b5846b21fb78436a8a5b84970c16962cb14c991fa95c1c463af5d59612a056c` (body_updates/tutorial001_py310.py:24) | inferred | partial |
| app:body_updates/tutorial001_py310.py:5 | PUT | /items/{item_id} | body_updates/tutorial001_py310.py::update_item | fact:4956f971e1e08f7ee4a9ec8fd8f8120b4124ce78833f3aab6257f1332251e10c | fact:4956f971e1e08f7ee4a9ec8fd8f8120b4124ce78833f3aab6257f1332251e10c | 200 | unknown — Không thấy khai báo cơ chế xác thực cho route này. | `fact:778d74dfff440aa856a0f7b517028a60e428f12634e67783a67340ae1afeda94` | `ev:3d74e3573800f42896b5aa06c1f2baf98698acfd17675e45da75b881ddc2259e` (body_updates/tutorial001_py310.py:5), `ev:0b88b8b7381ec9c9df6e2c45f714861b65f24b5b2ebb2ffdc63869eb8f5047b3` (body_updates/tutorial001_py310.py:28-29), `ev:ee80a0462671fa5803eb06f087b081189a8881045c16da318c0f5935a9595083` (body_updates/tutorial001_py310.py:28), `ev:207166c1be1cabc3296124c8ac9d2ff5d8bbe74a6aceffa6d308f74deacb439b` (body_updates/tutorial001_py310.py:29) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "Item_4956f971": {
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
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ]
          },
          "price": {
            "anyOf": [
              {
                "type": "number"
              },
              {
                "type": "null"
              }
            ]
          },
          "tags": {
            "items": {
              "type": "string"
            },
            "type": "array"
          },
          "tax": {
            "type": "number"
          }
        },
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:4956f971e1e08f7ee4a9ec8fd8f8120b4124ce78833f3aab6257f1332251e10c"
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
      "get": {
        "operationId": "op_f51b64031a6661c3",
        "parameters": [
          {
            "in": "path",
            "name": "item_id",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Item_4956f971"
                }
              }
            },
            "description": "Status code suy theo fastapi.default_status_200"
          }
        },
        "x-analysis": {
          "application_id": "app:body_updates/tutorial001_py310.py:5",
          "evidence_ids": [
            "ev:3b5846b21fb78436a8a5b84970c16962cb14c991fa95c1c463af5d59612a056c",
            "ev:3d74e3573800f42896b5aa06c1f2baf98698acfd17675e45da75b881ddc2259e",
            "ev:62713cbb424ed623b26261f21e7dfeed62fffa4f9143aca9261972d37be2f9b6",
            "ev:867c9ce086af734888245aee0a521dfd78a92a84acf2672e15ecc3fe80661c62"
          ],
          "fact_ids": [
            "fact:f51b64031a6661c3b510aed95273b407023f4e65527c28f1122437ba65bf0032"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy khai báo cơ chế xác thực cho route này."
            }
          ]
        }
      },
      "put": {
        "operationId": "op_778d74dfff440aa8",
        "parameters": [
          {
            "in": "path",
            "name": "item_id",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/Item_4956f971"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Item_4956f971"
                }
              }
            },
            "description": "Status code suy theo fastapi.default_status_200"
          }
        },
        "x-analysis": {
          "application_id": "app:body_updates/tutorial001_py310.py:5",
          "evidence_ids": [
            "ev:0b88b8b7381ec9c9df6e2c45f714861b65f24b5b2ebb2ffdc63869eb8f5047b3",
            "ev:207166c1be1cabc3296124c8ac9d2ff5d8bbe74a6aceffa6d308f74deacb439b",
            "ev:3d74e3573800f42896b5aa06c1f2baf98698acfd17675e45da75b881ddc2259e",
            "ev:ee80a0462671fa5803eb06f087b081189a8881045c16da318c0f5935a9595083"
          ],
          "fact_ids": [
            "fact:778d74dfff440aa856a0f7b517028a60e428f12634e67783a67340ae1afeda94"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy khai báo cơ chế xác thực cho route này."
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
