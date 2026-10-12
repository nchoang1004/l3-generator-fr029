---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:e4165f3a98b552337d7cda0a275136581555ea99b60a6a5cfeedd44532cd86af"
owner_component_id: "cmp_971bf4624f5d60de9b0d249dee17ebb4fe781339e232ac36357412cd7ade7e83"
owner_component: "Metadata trang"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v13"
fact_ids: ["fact:392e8bd96a7a525a9979f9a5b84aa90757d3d937888aaa5a1d71ab1275d43ada", "fact:da88b848e838031a1330747430f6760c07df4d6f667feed017713cbf5d77426a"]
evidence_ids: ["ev:1ae1b37d06ee3c67dd1a85691b24f94a5723bb85308bfa86e2abe19e34560d1b", "ev:4068d6e7fc732a13d4bd7c5d8176f67a889b32df7933b6a1354f7bc0356dafb9", "ev:41b76e328869f1fe33c78541b58d05604d3b0aeb2f8b4a1dc5fa467ef21a64e8", "ev:8df3e892f77996038dff5e82bd9c9f9189776ec7ab684674e8594c3d49883b87", "ev:9352a170f42a0ff7cd4c10261140511be690b99c47e5eb173fd11940fe07477a", "ev:971de71bbc40bf85f9320bab881245c7a27d0eb37f85ecf9c46061cfe8a8f93c", "ev:a81afa82051e5170cfc9cbb05c49f089681a6be1d2e43d4ac76275c9ba576d8d", "ev:b222489cf09040f7fa6813e6e9940f7549ace77256b688752d8a4c95a241f1ac", "ev:dc3460221549092b1e4e47909c3602698bfd3a98882e02acfa80ae35dfcc172b", "ev:fbb3fb8d4fdbb1c705a436b129bb283590ed6900296707d5212d37a49db802c8"]
---
# API — Metadata trang

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /api/metadata | url (query, string, bắt buộc) | (không có) | Metadata | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong route | inferred (fastapi.default_status_200, fastapi.return_annotation_response_model, fastapi.scalar_param_query) / partial | `f:392e8bd9` |


## Model

### Metadata (response)

Fact `f:da88b848` · exact / full · khai ở reworkd_platform/web/api/metadata.py:14

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| title | string | False | True |
| hostname | string | False | True |
| favicon | string | False | True |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:reworkd_platform/web/application.py:28 | GET | /api/metadata | reworkd_platform/web/api/metadata.py::extract_metadata | (rỗng) | fact:da88b848e838031a1330747430f6760c07df4d6f667feed017713cbf5d77426a | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong route | `fact:392e8bd96a7a525a9979f9a5b84aa90757d3d937888aaa5a1d71ab1275d43ada` | `ev:1ae1b37d06ee3c67dd1a85691b24f94a5723bb85308bfa86e2abe19e34560d1b` (reworkd_platform/web/api/metadata.py:20-23), `ev:9352a170f42a0ff7cd4c10261140511be690b99c47e5eb173fd11940fe07477a` (reworkd_platform/web/api/metadata.py:21), `ev:8df3e892f77996038dff5e82bd9c9f9189776ec7ab684674e8594c3d49883b87` (reworkd_platform/web/api/metadata.py:23), `ev:4068d6e7fc732a13d4bd7c5d8176f67a889b32df7933b6a1354f7bc0356dafb9` (reworkd_platform/web/api/router.py:10), `ev:b222489cf09040f7fa6813e6e9940f7549ace77256b688752d8a4c95a241f1ac` (reworkd_platform/web/application.py:28), `ev:971de71bbc40bf85f9320bab881245c7a27d0eb37f85ecf9c46061cfe8a8f93c` (reworkd_platform/web/application.py:51) | inferred | partial |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| Metadata | fact:da88b848e838031a1330747430f6760c07df4d6f667feed017713cbf5d77426a | reworkd_platform/web/api/metadata.py:14 |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "Metadata_da88b848": {
        "properties": {
          "favicon": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ]
          },
          "hostname": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ]
          },
          "title": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:da88b848e838031a1330747430f6760c07df4d6f667feed017713cbf5d77426a"
          ]
        }
      }
    }
  },
  "info": {
    "title": "Metadata trang",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/api/metadata": {
      "get": {
        "operationId": "op_392e8bd96a7a525a",
        "parameters": [
          {
            "in": "query",
            "name": "url",
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
                  "$ref": "#/components/schemas/Metadata_da88b848"
                }
              }
            },
            "description": "Status code suy theo fastapi.default_status_200"
          }
        },
        "x-analysis": {
          "application_id": "app:reworkd_platform/web/application.py:28",
          "evidence_ids": [
            "ev:1ae1b37d06ee3c67dd1a85691b24f94a5723bb85308bfa86e2abe19e34560d1b",
            "ev:4068d6e7fc732a13d4bd7c5d8176f67a889b32df7933b6a1354f7bc0356dafb9",
            "ev:8df3e892f77996038dff5e82bd9c9f9189776ec7ab684674e8594c3d49883b87",
            "ev:9352a170f42a0ff7cd4c10261140511be690b99c47e5eb173fd11940fe07477a",
            "ev:971de71bbc40bf85f9320bab881245c7a27d0eb37f85ecf9c46061cfe8a8f93c",
            "ev:b222489cf09040f7fa6813e6e9940f7549ace77256b688752d8a4c95a241f1ac"
          ],
          "fact_ids": [
            "fact:392e8bd96a7a525a9979f9a5b84aa90757d3d937888aaa5a1d71ab1275d43ada"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong route"
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
