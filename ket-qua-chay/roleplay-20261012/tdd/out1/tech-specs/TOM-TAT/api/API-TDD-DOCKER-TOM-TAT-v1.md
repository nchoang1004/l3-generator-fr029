---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:8053c30b1c2e0701055f23718e5cba06736e299abd4a84a3ff4f205501454276"
owner_component_id: "cmp_85e5e3b3cfed5d952d022b245b713c4fae7484c0c89106444b395f7de26b8491"
owner_component: "Tóm tắt"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-oneshot-prompt-v6"
fact_ids: ["fact:0822326e3bf6bb85a802a7eeedb001ed2f3c0e07acf9a0f424215f7486d05bae", "fact:177c9640333a140c68331990c1078aaf9b36fe7038ae3a9784b4ef4e0854e714", "fact:8b8c5875eab12049b12451832488f4090afae35bac2f0b350ee4390e635ccfe9", "fact:c22f01ae83b5021b3719e73c5335ef22ae07853f4d1bf5ce3529eb6e2956f8d1", "fact:dbff9c6797826abfcdd3069f4b6c4ce935b61f469bf0286e93ed44aafe07ebfc", "fact:05d7c81519deaef5aa62c9ab491941fe87e71c45eb46016e4d2abe1f2957cc70", "fact:167feb5e47f5be075e423e3f8a2eef41e54a144d671b330afd0b9742b51f1cda", "fact:43f1c2376faaeee7f585a94ae06c8bbd43b6fecaeef9e060532bd2beac767353", "fact:4bb453f7317e4ea3e7627b37eb8f400a6ae09871da25f4b37e3ba0ee493efbad"]
evidence_ids: ["ev:016117a02e51da1c4121983620a5d9cc77afc96a5a6c5ffc3b3d01659bdec586", "ev:0dc70978b1bd16cf5202caa1b64ce8c5b31a6deddd3a84270e0f0c9440d58da5", "ev:1e26640e144cd5f41199af7f3acc4576c3a107c835c7c2902cf33f7612b4cae5", "ev:1f2326b1dacc7549f58bd600b9f8db6f5ec906e23bd21772cd530694a0a34962", "ev:20f0df2053f5798368db91b552d5c021c0428696b431400ce7f7ea71f966ef7c", "ev:28d77f8bfa7706db41278cf274144d6a97083d5f01c459a1945ef53fa977db74", "ev:348b57d60a023374d7c074008931232cb7a6785b7c89f9a83b4f1f92fbe98de5", "ev:406e121790c7605c95ae609af74b056eaf49b7ec146be9f7990ef68c7844afc3", "ev:43e1188202433f9c6edbd035e7d74b954b77e2267fb5ed0603026e461788a6e5", "ev:534a97bfa92553507488957abe57655df836f0a2f772ee7074c11b39691c5253", "ev:59c19f1809111b1f34e0a84cf2b17b7adc3624fdd202ff3447f5806bd7286970", "ev:6760bb4ef3b0e3e4c34839a7cf279f0573d516f7304e81e8b80bbd5ec2ba738f", "ev:6a65161d107244c45e8360473ce06c0133b51d768958a02c2a7d6bdd53aa5d42", "ev:71c3fb6811bd07366379c5ebcce0297d62ef90d2b4ec99febe4e2c3f3478dbea", "ev:77d57a224bad898fa97daeffab8cd0ed8b4c0cce0454ffd2c3e724082af59c74", "ev:7c28ede5320e4a030b415f410962e61651356b697f18ba69b471e43d1db83f01", "ev:7ff81516b88d2fe70e370a6645489ff542ac4db5e425732aec97f8c91a4654b4", "ev:906f80b4d81c7d89b0196225241ea4af68381a02ec474f1752814d50523539db", "ev:9df3b74005a8464d761295c99c88d945b91b4e291bb307da5f4f3f2e008080d2", "ev:bac6e629b483c09d0bdfbd1d1cb2419d1ae55a8096bb413f9f7db37a8f71f479", "ev:bf6d07b334c674ade6fa7d61306130a78cdec07238ddac46eaba53cd3978b87a", "ev:daf275969c51cbaeebdc0038c3d3c00bdc3feb560ffae83f64ff907ea225500b", "ev:dcb23e8eb0e9bf043bf1fd468723a3c7710f1d11a5dd62d995fab54e10a6ccfe", "ev:e0605a834811343eee2ccb02a9de68909f261c70ee83f795d0eb143142e23222", "ev:e12fbe273883da69805b1191a13781d6d5c37481c5a85af37097681d76b8fe35", "ev:e4095ecce252c3e4d25fb52006d94d3916d3246bfcff0cc237e076f491215592", "ev:ec335a0e1fc46a84860fa7b545926df54ad495b7793110f5607290ee630e573f", "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3", "ev:f199f3e344c41e6831db09172f5d1224bbd7464d34da882327a44ed97a18c4ee"]
---
# API — Tóm tắt

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /summaries/ | (không có) | (không có) | list[SummarySchema] | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security) | inferred (fastapi.default_status_200) / partial | `f:dbff9c67` |
| POST | /summaries/ | payload (body, SummaryPayloadSchema, bắt buộc) | SummaryPayloadSchema | SummaryResponseSchema | 201 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security) | inferred (fastapi.model_param_body) / partial | `f:0822326e` |
| DELETE | /summaries/{id}/ | id (path, integer, bắt buộc) | (không có) | SummaryResponseSchema | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security) | inferred (fastapi.default_status_200) / partial | `f:177c9640` |
| GET | /summaries/{id}/ | id (path, integer, bắt buộc) | (không có) | SummarySchema | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security) | inferred (fastapi.default_status_200) / partial | `f:8b8c5875` |
| PUT | /summaries/{id}/ | id (path, integer, bắt buộc); payload (body, SummaryUpdatePayloadSchema, bắt buộc) | SummaryUpdatePayloadSchema | SummarySchema | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security) | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:c22f01ae` |


## Model

### SummaryPayloadSchema (request)

Fact `f:43f1c237` · inferred (pydantic.v2_required_no_default) / full · khai ở app/models/pydantic.py:4

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| url | string | True | False |

### SummaryResponseSchema (response)

Fact `f:167feb5e` · inferred (pydantic.v2_required_no_default) / full · khai ở app/models/pydantic.py:8

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| url | string | True | False |
| id | integer | True | False |

### SummarySchema (response)

Fact `f:05d7c815` · exact / partial · khai ở app/models/tortoise.py:14

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| unknown — Model sinh lúc chạy: SummarySchema được tạo lúc chạy bằng pydantic_model_creator(TextSummary); các trường sinh ra từ model Tortoise nên chỉ biết khi chạy | | | |

### SummaryUpdatePayloadSchema (request)

Fact `f:4bb453f7` · inferred (pydantic.v2_required_no_default) / full · khai ở app/models/pydantic.py:12

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| url | string | True | False |
| summary | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:12 | GET | /summaries/ | app/api/summaries.py::read_all_summaries | (rỗng) | fact:05d7c81519deaef5aa62c9ab491941fe87e71c45eb46016e4d2abe1f2957cc70 | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security) | `fact:dbff9c6797826abfcdd3069f4b6c4ce935b61f469bf0286e93ed44aafe07ebfc` | `ev:59c19f1809111b1f34e0a84cf2b17b7adc3624fdd202ff3447f5806bd7286970` (app/api/summaries.py:27-28), `ev:7c28ede5320e4a030b415f410962e61651356b697f18ba69b471e43d1db83f01` (app/api/summaries.py:27), `ev:bac6e629b483c09d0bdfbd1d1cb2419d1ae55a8096bb413f9f7db37a8f71f479` (app/api/summaries.py:28), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:534a97bfa92553507488957abe57655df836f0a2f772ee7074c11b39691c5253` (app/main.py:15) | inferred | partial |
| app:app/main.py:12 | POST | /summaries/ | app/api/summaries.py::create_summary | fact:43f1c2376faaeee7f585a94ae06c8bbd43b6fecaeef9e060532bd2beac767353 | fact:167feb5e47f5be075e423e3f8a2eef41e54a144d671b330afd0b9742b51f1cda | 201 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security) | `fact:0822326e3bf6bb85a802a7eeedb001ed2f3c0e07acf9a0f424215f7486d05bae` | `ev:daf275969c51cbaeebdc0038c3d3c00bdc3feb560ffae83f64ff907ea225500b` (app/api/summaries.py:32), `ev:e0605a834811343eee2ccb02a9de68909f261c70ee83f795d0eb143142e23222` (app/api/summaries.py:32-33), `ev:1f2326b1dacc7549f58bd600b9f8db6f5ec906e23bd21772cd530694a0a34962` (app/api/summaries.py:33), `ev:71c3fb6811bd07366379c5ebcce0297d62ef90d2b4ec99febe4e2c3f3478dbea` (app/api/summaries.py:34), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:534a97bfa92553507488957abe57655df836f0a2f772ee7074c11b39691c5253` (app/main.py:15) | inferred | partial |
| app:app/main.py:12 | DELETE | /summaries/{id}/ | app/api/summaries.py::delete_summary | (rỗng) | fact:167feb5e47f5be075e423e3f8a2eef41e54a144d671b330afd0b9742b51f1cda | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security) | `fact:177c9640333a140c68331990c1078aaf9b36fe7038ae3a9784b4ef4e0854e714` | `ev:1e26640e144cd5f41199af7f3acc4576c3a107c835c7c2902cf33f7612b4cae5` (app/api/summaries.py:55-56), `ev:7ff81516b88d2fe70e370a6645489ff542ac4db5e425732aec97f8c91a4654b4` (app/api/summaries.py:55), `ev:77d57a224bad898fa97daeffab8cd0ed8b4c0cce0454ffd2c3e724082af59c74` (app/api/summaries.py:56), `ev:906f80b4d81c7d89b0196225241ea4af68381a02ec474f1752814d50523539db` (app/api/summaries.py:59), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:534a97bfa92553507488957abe57655df836f0a2f772ee7074c11b39691c5253` (app/main.py:15) | inferred | partial |
| app:app/main.py:12 | GET | /summaries/{id}/ | app/api/summaries.py::read_summary | (rỗng) | fact:05d7c81519deaef5aa62c9ab491941fe87e71c45eb46016e4d2abe1f2957cc70 | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security) | `fact:8b8c5875eab12049b12451832488f4090afae35bac2f0b350ee4390e635ccfe9` | `ev:43e1188202433f9c6edbd035e7d74b954b77e2267fb5ed0603026e461788a6e5` (app/api/summaries.py:18), `ev:9df3b74005a8464d761295c99c88d945b91b4e291bb307da5f4f3f2e008080d2` (app/api/summaries.py:18-19), `ev:28d77f8bfa7706db41278cf274144d6a97083d5f01c459a1945ef53fa977db74` (app/api/summaries.py:19), `ev:6760bb4ef3b0e3e4c34839a7cf279f0573d516f7304e81e8b80bbd5ec2ba738f` (app/api/summaries.py:22), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:534a97bfa92553507488957abe57655df836f0a2f772ee7074c11b39691c5253` (app/main.py:15) | inferred | partial |
| app:app/main.py:12 | PUT | /summaries/{id}/ | app/api/summaries.py::update_summary | fact:4bb453f7317e4ea3e7627b37eb8f400a6ae09871da25f4b37e3ba0ee493efbad | fact:05d7c81519deaef5aa62c9ab491941fe87e71c45eb46016e4d2abe1f2957cc70 | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security) | `fact:c22f01ae83b5021b3719e73c5335ef22ae07853f4d1bf5ce3529eb6e2956f8d1` | `ev:0dc70978b1bd16cf5202caa1b64ce8c5b31a6deddd3a84270e0f0c9440d58da5` (app/api/summaries.py:44), `ev:f199f3e344c41e6831db09172f5d1224bbd7464d34da882327a44ed97a18c4ee` (app/api/summaries.py:44-45), `ev:e12fbe273883da69805b1191a13781d6d5c37481c5a85af37097681d76b8fe35` (app/api/summaries.py:45), `ev:016117a02e51da1c4121983620a5d9cc77afc96a5a6c5ffc3b3d01659bdec586` (app/api/summaries.py:46), `ev:20f0df2053f5798368db91b552d5c021c0428696b431400ce7f7ea71f966ef7c` (app/api/summaries.py:50), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:534a97bfa92553507488957abe57655df836f0a2f772ee7074c11b39691c5253` (app/main.py:15) | inferred | partial |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| SummaryPayloadSchema | fact:43f1c2376faaeee7f585a94ae06c8bbd43b6fecaeef9e060532bd2beac767353 | app/models/pydantic.py:4 |
| SummaryResponseSchema | fact:167feb5e47f5be075e423e3f8a2eef41e54a144d671b330afd0b9742b51f1cda | app/models/pydantic.py:8 |
| SummarySchema | fact:05d7c81519deaef5aa62c9ab491941fe87e71c45eb46016e4d2abe1f2957cc70 | app/models/tortoise.py:14 |
| SummaryUpdatePayloadSchema | fact:4bb453f7317e4ea3e7627b37eb8f400a6ae09871da25f4b37e3ba0ee493efbad | app/models/pydantic.py:12 |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "SummaryPayloadSchema_43f1c237": {
        "properties": {
          "url": {
            "type": "string"
          }
        },
        "required": [
          "url"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:43f1c2376faaeee7f585a94ae06c8bbd43b6fecaeef9e060532bd2beac767353"
          ]
        }
      },
      "SummaryResponseSchema_167feb5e": {
        "properties": {
          "id": {
            "type": "integer"
          },
          "url": {
            "type": "string"
          }
        },
        "required": [
          "id",
          "url"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:167feb5e47f5be075e423e3f8a2eef41e54a144d671b330afd0b9742b51f1cda"
          ]
        }
      },
      "SummarySchema_05d7c815": {
        "properties": {},
        "type": "object",
        "x-analysis": {
          "completeness": "partial",
          "fact_ids": [
            "fact:05d7c81519deaef5aa62c9ab491941fe87e71c45eb46016e4d2abe1f2957cc70"
          ]
        }
      },
      "SummaryUpdatePayloadSchema_4bb453f7": {
        "properties": {
          "summary": {
            "type": "string"
          },
          "url": {
            "type": "string"
          }
        },
        "required": [
          "summary",
          "url"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:4bb453f7317e4ea3e7627b37eb8f400a6ae09871da25f4b37e3ba0ee493efbad"
          ]
        }
      }
    }
  },
  "info": {
    "title": "Tóm tắt",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/summaries/": {
      "get": {
        "operationId": "op_dbff9c6797826abf",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/SummarySchema_05d7c815"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Status code suy theo fastapi.default_status_200"
          }
        },
        "summary": "Lấy danh sách tất cả bản tóm tắt.",
        "tags": [
          "summaries"
        ],
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:534a97bfa92553507488957abe57655df836f0a2f772ee7074c11b39691c5253",
            "ev:59c19f1809111b1f34e0a84cf2b17b7adc3624fdd202ff3447f5806bd7286970",
            "ev:7c28ede5320e4a030b415f410962e61651356b697f18ba69b471e43d1db83f01",
            "ev:bac6e629b483c09d0bdfbd1d1cb2419d1ae55a8096bb413f9f7db37a8f71f479",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"
          ],
          "fact_ids": [
            "fact:dbff9c6797826abfcdd3069f4b6c4ce935b61f469bf0286e93ed44aafe07ebfc"
          ],
          "summary_origin": "AI viết, không phải dữ kiện đã kiểm",
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security)"
            }
          ]
        }
      },
      "post": {
        "operationId": "op_0822326e3bf6bb85",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/SummaryPayloadSchema_43f1c237"
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
                  "$ref": "#/components/schemas/SummaryResponseSchema_167feb5e"
                }
              }
            },
            "description": "Status code lấy từ source"
          }
        },
        "summary": "Tạo bản ghi tóm tắt cho một URL và chạy nền việc sinh nội dung tóm tắt.",
        "tags": [
          "summaries"
        ],
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:1f2326b1dacc7549f58bd600b9f8db6f5ec906e23bd21772cd530694a0a34962",
            "ev:534a97bfa92553507488957abe57655df836f0a2f772ee7074c11b39691c5253",
            "ev:71c3fb6811bd07366379c5ebcce0297d62ef90d2b4ec99febe4e2c3f3478dbea",
            "ev:daf275969c51cbaeebdc0038c3d3c00bdc3feb560ffae83f64ff907ea225500b",
            "ev:e0605a834811343eee2ccb02a9de68909f261c70ee83f795d0eb143142e23222",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"
          ],
          "fact_ids": [
            "fact:0822326e3bf6bb85a802a7eeedb001ed2f3c0e07acf9a0f424215f7486d05bae"
          ],
          "summary_origin": "AI viết, không phải dữ kiện đã kiểm",
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security)"
            }
          ]
        }
      }
    },
    "/summaries/{id}/": {
      "delete": {
        "operationId": "op_177c9640333a140c",
        "parameters": [
          {
            "in": "path",
            "name": "id",
            "required": true,
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
                  "$ref": "#/components/schemas/SummaryResponseSchema_167feb5e"
                }
              }
            },
            "description": "Status code suy theo fastapi.default_status_200"
          },
          "404": {
            "description": "Lỗi HTTPException, suy từ chỗ ném lỗi app/api/summaries.py:59",
            "x-analysis": {
              "inferred": "raise + exception_handler"
            }
          }
        },
        "summary": "Xóa một bản tóm tắt theo id và trả về bản ghi đã xóa.",
        "tags": [
          "summaries"
        ],
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:1e26640e144cd5f41199af7f3acc4576c3a107c835c7c2902cf33f7612b4cae5",
            "ev:534a97bfa92553507488957abe57655df836f0a2f772ee7074c11b39691c5253",
            "ev:77d57a224bad898fa97daeffab8cd0ed8b4c0cce0454ffd2c3e724082af59c74",
            "ev:7ff81516b88d2fe70e370a6645489ff542ac4db5e425732aec97f8c91a4654b4",
            "ev:906f80b4d81c7d89b0196225241ea4af68381a02ec474f1752814d50523539db",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"
          ],
          "fact_ids": [
            "fact:177c9640333a140c68331990c1078aaf9b36fe7038ae3a9784b4ef4e0854e714"
          ],
          "summary_origin": "AI viết, không phải dữ kiện đã kiểm",
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security)"
            }
          ]
        }
      },
      "get": {
        "operationId": "op_8b8c5875eab12049",
        "parameters": [
          {
            "in": "path",
            "name": "id",
            "required": true,
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
                  "$ref": "#/components/schemas/SummarySchema_05d7c815"
                }
              }
            },
            "description": "Status code suy theo fastapi.default_status_200"
          },
          "404": {
            "description": "Lỗi HTTPException, suy từ chỗ ném lỗi app/api/summaries.py:22",
            "x-analysis": {
              "inferred": "raise + exception_handler"
            }
          }
        },
        "summary": "Lấy một bản tóm tắt theo id.",
        "tags": [
          "summaries"
        ],
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:28d77f8bfa7706db41278cf274144d6a97083d5f01c459a1945ef53fa977db74",
            "ev:43e1188202433f9c6edbd035e7d74b954b77e2267fb5ed0603026e461788a6e5",
            "ev:534a97bfa92553507488957abe57655df836f0a2f772ee7074c11b39691c5253",
            "ev:6760bb4ef3b0e3e4c34839a7cf279f0573d516f7304e81e8b80bbd5ec2ba738f",
            "ev:9df3b74005a8464d761295c99c88d945b91b4e291bb307da5f4f3f2e008080d2",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"
          ],
          "fact_ids": [
            "fact:8b8c5875eab12049b12451832488f4090afae35bac2f0b350ee4390e635ccfe9"
          ],
          "summary_origin": "AI viết, không phải dữ kiện đã kiểm",
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security)"
            }
          ]
        }
      },
      "put": {
        "operationId": "op_c22f01ae83b5021b",
        "parameters": [
          {
            "in": "path",
            "name": "id",
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
                "$ref": "#/components/schemas/SummaryUpdatePayloadSchema_4bb453f7"
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
                  "$ref": "#/components/schemas/SummarySchema_05d7c815"
                }
              }
            },
            "description": "Status code suy theo fastapi.default_status_200"
          },
          "404": {
            "description": "Lỗi HTTPException, suy từ chỗ ném lỗi app/api/summaries.py:50",
            "x-analysis": {
              "inferred": "raise + exception_handler"
            }
          }
        },
        "summary": "Cập nhật URL và nội dung của một bản tóm tắt theo id.",
        "tags": [
          "summaries"
        ],
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:016117a02e51da1c4121983620a5d9cc77afc96a5a6c5ffc3b3d01659bdec586",
            "ev:0dc70978b1bd16cf5202caa1b64ce8c5b31a6deddd3a84270e0f0c9440d58da5",
            "ev:20f0df2053f5798368db91b552d5c021c0428696b431400ce7f7ea71f966ef7c",
            "ev:534a97bfa92553507488957abe57655df836f0a2f772ee7074c11b39691c5253",
            "ev:e12fbe273883da69805b1191a13781d6d5c37481c5a85af37097681d76b8fe35",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3",
            "ev:f199f3e344c41e6831db09172f5d1224bbd7464d34da882327a44ed97a18c4ee"
          ],
          "fact_ids": [
            "fact:c22f01ae83b5021b3719e73c5335ef22ae07853f4d1bf5ce3529eb6e2956f8d1"
          ],
          "summary_origin": "AI viết, không phải dữ kiện đã kiểm",
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security)"
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
