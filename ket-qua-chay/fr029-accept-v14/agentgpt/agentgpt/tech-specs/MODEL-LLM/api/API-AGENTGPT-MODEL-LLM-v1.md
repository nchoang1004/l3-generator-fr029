---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:e4165f3a98b552337d7cda0a275136581555ea99b60a6a5cfeedd44532cd86af"
owner_component_id: "cmp_3b1cd87773de2fabd56a7f727808def726dbcf9c6a021314d789a987446d12a3"
owner_component: "Model LLM"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v14"
fact_ids: ["fact:349a80f54d9c7ec89913b615a55246a4fb5e2a13e8f7fe742f842a91ed0f4fa0", "fact:ed800b8ae54638fab113f28c7811d7b905aaaf940c81a532d1a860d157e0a82c"]
evidence_ids: ["ev:08acf4cbfdde83f76b057f0b27367bb109da9133790ebb0feeff45c9dc9f4a09", "ev:14fb6560de8a266ace96eec95d3389375f108d5213ac3cec055db5c1b1b0e9e8", "ev:1a738a121f7ce57c6996d50f50a8cba87f651bbed28a3ca317146e74ed192da0", "ev:1e533e15475ad9128c5aefe0020d91c2beb536ea1ef363b15edb8fcc35e278ed", "ev:6767ab52a2b7a7801939a0c47295ce486437f9af4877becf5e2d80f78503dc79", "ev:6b1eb96c671f0200238561e906e087d0ee32e7f3f1c9a446ddbfc8da64a3007b", "ev:85f4b2f855303380d846e6636fd65fb606b6ee8dc01a4e1c8360e0b45dc62600", "ev:8be248aa50693df04e1d18b6f498dab95a10087e4c681c123691aadcb3e09c01", "ev:90fec2a9e744ee4e294537f72a9a541785c6cacacf3a7538f5512f258a52c055", "ev:971de71bbc40bf85f9320bab881245c7a27d0eb37f85ecf9c46061cfe8a8f93c", "ev:97bba44c6c83a8cd03600aad4f7b946977778ba5ff66956a8d9dfbce917a1316", "ev:b222489cf09040f7fa6813e6e9940f7549ace77256b688752d8a4c95a241f1ac", "ev:b632ce7e64ed0a1f79b4b6a984894795eef2941c73e00224e38d3646d5abaa7c", "ev:c4faf1a04ea560d6f5514a166e3c828df7bd2a93c9e8580c4a84f90254e6868e", "ev:e35e8f519c29b0040648bdb8187bd01217fcc9545d59dadb358f052f7cbf1c4c", "ev:e95964044f2a1646cea2bc58fca1c51b596c34814894ddcd49580799382a7660", "ev:f1632bba4244c46b202ec6c7c567f213de6569af5d39ef264af3a2611b4fcd63"]
---
# API — Model LLM

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /api/models | x-organization-id (header, string, tùy chọn) | (không có) | list[ModelWithAccess] | 200 (suy theo fastapi.response_class_default_status) | dependency: get_current_user, HTTPBearer, user_crud, get_db_session; auth: Xác thực bearer thông qua HTTPBearer, kiểm tra session token bằng get_current_user. | inferred (fastapi.header_underscore_to_hyphen, fastapi.response_class_default_status, fastapi.return_annotation_response_model) / full | `f:349a80f5` |


## Model

### ModelWithAccess (response)

Fact `f:ed800b8a` · exact / full · khai ở reworkd_platform/web/api/models/views.py:13

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| name | string | True | False |
| max_tokens | integer | True | False |
| has_access | boolean | False | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:reworkd_platform/web/application.py:28 | GET | /api/models | reworkd_platform/web/api/models/views.py::get_models | (rỗng) | fact:ed800b8ae54638fab113f28c7811d7b905aaaf940c81a532d1a860d157e0a82c | 200 | dependency: get_current_user, HTTPBearer, user_crud, get_db_session; auth: Xác thực bearer thông qua HTTPBearer, kiểm tra session token bằng get_current_user. | `fact:349a80f54d9c7ec89913b615a55246a4fb5e2a13e8f7fe742f842a91ed0f4fa0` | `ev:97bba44c6c83a8cd03600aad4f7b946977778ba5ff66956a8d9dfbce917a1316` (reworkd_platform/web/api/dependencies.py:16), `ev:b632ce7e64ed0a1f79b4b6a984894795eef2941c73e00224e38d3646d5abaa7c` (reworkd_platform/web/api/dependencies.py:21), `ev:08acf4cbfdde83f76b057f0b27367bb109da9133790ebb0feeff45c9dc9f4a09` (reworkd_platform/web/api/dependencies.py:22), `ev:f1632bba4244c46b202ec6c7c567f213de6569af5d39ef264af3a2611b4fcd63` (reworkd_platform/web/api/dependencies.py:23), `ev:1e533e15475ad9128c5aefe0020d91c2beb536ea1ef363b15edb8fcc35e278ed` (reworkd_platform/web/api/dependencies.py:24), `ev:85f4b2f855303380d846e6636fd65fb606b6ee8dc01a4e1c8360e0b45dc62600` (reworkd_platform/web/api/models/views.py:26), `ev:8be248aa50693df04e1d18b6f498dab95a10087e4c681c123691aadcb3e09c01` (reworkd_platform/web/api/models/views.py:26-29), `ev:90fec2a9e744ee4e294537f72a9a541785c6cacacf3a7538f5512f258a52c055` (reworkd_platform/web/api/models/views.py:28), `ev:6767ab52a2b7a7801939a0c47295ce486437f9af4877becf5e2d80f78503dc79` (reworkd_platform/web/api/models/views.py:29), `ev:c4faf1a04ea560d6f5514a166e3c828df7bd2a93c9e8580c4a84f90254e6868e` (reworkd_platform/web/api/router.py:8), `ev:b222489cf09040f7fa6813e6e9940f7549ace77256b688752d8a4c95a241f1ac` (reworkd_platform/web/application.py:28), `ev:6b1eb96c671f0200238561e906e087d0ee32e7f3f1c9a446ddbfc8da64a3007b` (reworkd_platform/web/application.py:34), `ev:971de71bbc40bf85f9320bab881245c7a27d0eb37f85ecf9c46061cfe8a8f93c` (reworkd_platform/web/application.py:51) | inferred | full |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| ModelWithAccess | fact:ed800b8ae54638fab113f28c7811d7b905aaaf940c81a532d1a860d157e0a82c | reworkd_platform/web/api/models/views.py:13 |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "ModelWithAccess_ed800b8a": {
        "properties": {
          "has_access": {
            "type": "boolean"
          },
          "max_tokens": {
            "type": "integer"
          },
          "name": {
            "type": "string"
          }
        },
        "required": [
          "max_tokens",
          "name"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:ed800b8ae54638fab113f28c7811d7b905aaaf940c81a532d1a860d157e0a82c"
          ]
        }
      }
    }
  },
  "info": {
    "title": "Model LLM",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/api/models": {
      "get": {
        "operationId": "op_349a80f54d9c7ec8",
        "parameters": [
          {
            "in": "header",
            "name": "x-organization-id",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ]
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/ModelWithAccess_ed800b8a"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Status code suy theo fastapi.response_class_default_status"
          }
        },
        "x-analysis": {
          "application_id": "app:reworkd_platform/web/application.py:28",
          "evidence_ids": [
            "ev:08acf4cbfdde83f76b057f0b27367bb109da9133790ebb0feeff45c9dc9f4a09",
            "ev:1e533e15475ad9128c5aefe0020d91c2beb536ea1ef363b15edb8fcc35e278ed",
            "ev:6767ab52a2b7a7801939a0c47295ce486437f9af4877becf5e2d80f78503dc79",
            "ev:6b1eb96c671f0200238561e906e087d0ee32e7f3f1c9a446ddbfc8da64a3007b",
            "ev:85f4b2f855303380d846e6636fd65fb606b6ee8dc01a4e1c8360e0b45dc62600",
            "ev:8be248aa50693df04e1d18b6f498dab95a10087e4c681c123691aadcb3e09c01",
            "ev:90fec2a9e744ee4e294537f72a9a541785c6cacacf3a7538f5512f258a52c055",
            "ev:971de71bbc40bf85f9320bab881245c7a27d0eb37f85ecf9c46061cfe8a8f93c",
            "ev:97bba44c6c83a8cd03600aad4f7b946977778ba5ff66956a8d9dfbce917a1316",
            "ev:b222489cf09040f7fa6813e6e9940f7549ace77256b688752d8a4c95a241f1ac",
            "ev:b632ce7e64ed0a1f79b4b6a984894795eef2941c73e00224e38d3646d5abaa7c",
            "ev:c4faf1a04ea560d6f5514a166e3c828df7bd2a93c9e8580c4a84f90254e6868e",
            "ev:f1632bba4244c46b202ec6c7c567f213de6569af5d39ef264af3a2611b4fcd63"
          ],
          "fact_ids": [
            "fact:349a80f54d9c7ec89913b615a55246a4fb5e2a13e8f7fe742f842a91ed0f4fa0"
          ],
          "unknowns": []
        }
      }
    }
  },
  "x-analysis": {
    "omitted_operations": []
  }
}
```
