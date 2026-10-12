---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:5bb8f8dab23ad52fff3529bdd3b387e2fbe241a46b8532b20990b11f1bc0564e"
owner_component_id: "cmp_cc4eb221a43fdb7fea0b2b4d1b55f500939a1cd5f85b0d4c94262f4ab112cb5e"
owner_component: "Ghi chú"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v5"
fact_ids: ["fact:47bc105bbb57254356bb523fb919965547ed8f70066644d61ca6986f9605967a", "fact:5b8375c23e0645e54e91e403819ca8f6e9554f0441ca63f5fe0c7211cfdaf2bd", "fact:1e238cded9ab96593368ffdfc532b267cdfd4d29d90e6fce1beae40436c2513a"]
evidence_ids: ["ev:31c3997f9dea6d324a283550e74ad8c5ac59385aaf5d14c7f2ec76ff4d9d7691", "ev:3af9911e17939707a53d6802e2f1a8e5526d9c71078697e00b6786d835ef7095", "ev:5242e49dd37c6a0129c449f9ca268b711eefb0429d55676450d9c21c9b8587e7", "ev:59a21fb4bece8766eef9e0482cb65e4ed36ee2bf0669f98999389158fb810caf", "ev:6e8147430da1b86601d26d7dc6b30ace73fec55ab9dfd9286b084ee341d6075b", "ev:996a29b7c893cffc52cb35b14928d42ecd72c4a7601a3a22ec0ee9d407d00509", "ev:9e274e7fb95b1b6919e49e12a8c1ae1cceaf07551fb0820fc4dce609820a3025", "ev:aa3569d7e11c61cdee308e160b3c02ff7bdad7343e1d95a5e3055871c230fa2e", "ev:e11560b23f310c2df57ecd69d5556da0aa0810fa91a465e0f55916b093e3ed41", "ev:e8a32bb4dece2d68ec2811c04711d1fff104ee113fbca536d896d99eff34ce4b", "ev:efe4680caac693ea69809cf89b9d8a532e7e01e566a0b3c11de102e6b520019f"]
---
# API — Ghi chú

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /notes | note (body, Note, bắt buộc) | Note | Note | 201 | unknown — Mã nguồn không khai báo cơ chế xác thực cho route này | inferred (fastapi.model_param_body) / partial | `f:47bc105b` |
| GET | /notes/{note_id} | note_id (path, integer, bắt buộc); q (query, integer, tùy chọn) | (không có) | Note | 200 (suy theo fastapi.default_status_200) | unknown — Mã nguồn không khai báo cơ chế xác thực cho route này | inferred (fastapi.default_status_200, fastapi.scalar_param_query) / partial | `f:5b8375c2` |


## Model

### Note (request)

Fact `f:1e238cde` · inferred / full · khai ở app/main.py:9

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| title | string | True | False |
| priority | integer | False | True |
| body | string | False | True |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:6 | POST | /notes | app/main.py::create_note | fact:1e238cded9ab96593368ffdfc532b267cdfd4d29d90e6fce1beae40436c2513a | fact:1e238cded9ab96593368ffdfc532b267cdfd4d29d90e6fce1beae40436c2513a | 201 | unknown — Mã nguồn không khai báo cơ chế xác thực cho route này | `fact:47bc105bbb57254356bb523fb919965547ed8f70066644d61ca6986f9605967a` | `ev:9e274e7fb95b1b6919e49e12a8c1ae1cceaf07551fb0820fc4dce609820a3025` (app/main.py:6), `ev:6e8147430da1b86601d26d7dc6b30ace73fec55ab9dfd9286b084ee341d6075b` (app/main.py:15), `ev:aa3569d7e11c61cdee308e160b3c02ff7bdad7343e1d95a5e3055871c230fa2e` (app/main.py:15-16), `ev:3af9911e17939707a53d6802e2f1a8e5526d9c71078697e00b6786d835ef7095` (app/main.py:16) | inferred | partial |
| app:app/main.py:6 | GET | /notes/{note_id} | app/main.py::get_note | (rỗng) | fact:1e238cded9ab96593368ffdfc532b267cdfd4d29d90e6fce1beae40436c2513a | 200 | unknown — Mã nguồn không khai báo cơ chế xác thực cho route này | `fact:5b8375c23e0645e54e91e403819ca8f6e9554f0441ca63f5fe0c7211cfdaf2bd` | `ev:9e274e7fb95b1b6919e49e12a8c1ae1cceaf07551fb0820fc4dce609820a3025` (app/main.py:6), `ev:996a29b7c893cffc52cb35b14928d42ecd72c4a7601a3a22ec0ee9d407d00509` (app/main.py:20-21), `ev:e11560b23f310c2df57ecd69d5556da0aa0810fa91a465e0f55916b093e3ed41` (app/main.py:20), `ev:59a21fb4bece8766eef9e0482cb65e4ed36ee2bf0669f98999389158fb810caf` (app/main.py:21) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "Note_1e238cde": {
        "properties": {
          "body": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ]
          },
          "priority": {
            "anyOf": [
              {
                "type": "integer"
              },
              {
                "type": "null"
              }
            ]
          },
          "title": {
            "type": "string"
          }
        },
        "required": [
          "title"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:1e238cded9ab96593368ffdfc532b267cdfd4d29d90e6fce1beae40436c2513a"
          ]
        }
      }
    }
  },
  "info": {
    "title": "Ghi chú",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/notes": {
      "post": {
        "operationId": "op_47bc105bbb572543",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/Note_1e238cde"
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
                  "$ref": "#/components/schemas/Note_1e238cde"
                }
              }
            },
            "description": "Status code lấy từ source"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:6",
          "evidence_ids": [
            "ev:3af9911e17939707a53d6802e2f1a8e5526d9c71078697e00b6786d835ef7095",
            "ev:6e8147430da1b86601d26d7dc6b30ace73fec55ab9dfd9286b084ee341d6075b",
            "ev:9e274e7fb95b1b6919e49e12a8c1ae1cceaf07551fb0820fc4dce609820a3025",
            "ev:aa3569d7e11c61cdee308e160b3c02ff7bdad7343e1d95a5e3055871c230fa2e"
          ],
          "fact_ids": [
            "fact:47bc105bbb57254356bb523fb919965547ed8f70066644d61ca6986f9605967a"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Mã nguồn không khai báo cơ chế xác thực cho route này"
            }
          ]
        }
      }
    },
    "/notes/{note_id}": {
      "get": {
        "operationId": "op_5b8375c23e0645e5",
        "parameters": [
          {
            "in": "path",
            "name": "note_id",
            "required": true,
            "schema": {
              "type": "integer"
            }
          },
          {
            "in": "query",
            "name": "q",
            "required": false,
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
                  "$ref": "#/components/schemas/Note_1e238cde"
                }
              }
            },
            "description": "Status code suy theo fastapi.default_status_200"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:6",
          "evidence_ids": [
            "ev:59a21fb4bece8766eef9e0482cb65e4ed36ee2bf0669f98999389158fb810caf",
            "ev:996a29b7c893cffc52cb35b14928d42ecd72c4a7601a3a22ec0ee9d407d00509",
            "ev:9e274e7fb95b1b6919e49e12a8c1ae1cceaf07551fb0820fc4dce609820a3025",
            "ev:e11560b23f310c2df57ecd69d5556da0aa0810fa91a465e0f55916b093e3ed41"
          ],
          "fact_ids": [
            "fact:5b8375c23e0645e54e91e403819ca8f6e9554f0441ca63f5fe0c7211cfdaf2bd"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Mã nguồn không khai báo cơ chế xác thực cho route này"
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
