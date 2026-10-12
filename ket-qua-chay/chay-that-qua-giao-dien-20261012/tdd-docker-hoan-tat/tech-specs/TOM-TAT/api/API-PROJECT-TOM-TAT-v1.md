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
fact_ids: ["fact:321500b56a096ad85bdccc317648480f177d1589a71b65032352cbb7bd9b7f65", "fact:528d1ffdf910cb2228b66bb0a82b2b33b66683bf0512d8e99c750e078ce0d69a", "fact:5fe067026bfce0fed23898d2a8d53c8557770b6561dbdde548933b9e969a6362", "fact:9949c83f239b7a1063036de0b3421ea85325a38f120f8d6276d5f625d95c5601", "fact:e0ea3c8f4c2ecfacee809ac502fdf71b0fd6d370e66e5092e311bbeb616650de", "fact:05d7c81519deaef5aa62c9ab491941fe87e71c45eb46016e4d2abe1f2957cc70", "fact:167feb5e47f5be075e423e3f8a2eef41e54a144d671b330afd0b9742b51f1cda", "fact:43f1c2376faaeee7f585a94ae06c8bbd43b6fecaeef9e060532bd2beac767353", "fact:4bb453f7317e4ea3e7627b37eb8f400a6ae09871da25f4b37e3ba0ee493efbad"]
evidence_ids: ["ev:016117a02e51da1c4121983620a5d9cc77afc96a5a6c5ffc3b3d01659bdec586", "ev:0dc70978b1bd16cf5202caa1b64ce8c5b31a6deddd3a84270e0f0c9440d58da5", "ev:1904148ef6e4fd18cfaf05dd71e760a77a76aaf5af855f52150c6d9973b3729b", "ev:1e26640e144cd5f41199af7f3acc4576c3a107c835c7c2902cf33f7612b4cae5", "ev:20f0df2053f5798368db91b552d5c021c0428696b431400ce7f7ea71f966ef7c", "ev:28d77f8bfa7706db41278cf274144d6a97083d5f01c459a1945ef53fa977db74", "ev:348b57d60a023374d7c074008931232cb7a6785b7c89f9a83b4f1f92fbe98de5", "ev:406e121790c7605c95ae609af74b056eaf49b7ec146be9f7990ef68c7844afc3", "ev:43e1188202433f9c6edbd035e7d74b954b77e2267fb5ed0603026e461788a6e5", "ev:59c19f1809111b1f34e0a84cf2b17b7adc3624fdd202ff3447f5806bd7286970", "ev:6760bb4ef3b0e3e4c34839a7cf279f0573d516f7304e81e8b80bbd5ec2ba738f", "ev:6a65161d107244c45e8360473ce06c0133b51d768958a02c2a7d6bdd53aa5d42", "ev:71c3fb6811bd07366379c5ebcce0297d62ef90d2b4ec99febe4e2c3f3478dbea", "ev:77d57a224bad898fa97daeffab8cd0ed8b4c0cce0454ffd2c3e724082af59c74", "ev:7c2711ce8cd3252b4571781e6073a689fa6b60d172da05c8945de62c4ffbaaad", "ev:7c28ede5320e4a030b415f410962e61651356b697f18ba69b471e43d1db83f01", "ev:7ff81516b88d2fe70e370a6645489ff542ac4db5e425732aec97f8c91a4654b4", "ev:906f80b4d81c7d89b0196225241ea4af68381a02ec474f1752814d50523539db", "ev:9df3b74005a8464d761295c99c88d945b91b4e291bb307da5f4f3f2e008080d2", "ev:bef1584eee1014bda8f10937676ea56f0b92fea40b518aec06eae8a00845a53e", "ev:bf6d07b334c674ade6fa7d61306130a78cdec07238ddac46eaba53cd3978b87a", "ev:daf275969c51cbaeebdc0038c3d3c00bdc3feb560ffae83f64ff907ea225500b", "ev:dcb23e8eb0e9bf043bf1fd468723a3c7710f1d11a5dd62d995fab54e10a6ccfe", "ev:e4095ecce252c3e4d25fb52006d94d3916d3246bfcff0cc237e076f491215592", "ev:ec335a0e1fc46a84860fa7b545926df54ad495b7793110f5607290ee630e573f", "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"]
---
# API — Tóm tắt

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /summaries/ | (không có) | (không có) | list[SummarySchema] | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn | inferred (fastapi.default_status_200) / partial | `f:321500b5` |
| POST | /summaries/ | payload (body, SummaryPayloadSchema, bắt buộc) | SummaryPayloadSchema | SummaryResponseSchema | 201 | dependency: (không có); auth: unknown — Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn | inferred (fastapi.model_param_body) / partial | `f:e0ea3c8f` |
| DELETE | /summaries/{id}/ | id (path, integer, bắt buộc) | (không có) | SummaryResponseSchema | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn | inferred (fastapi.default_status_200) / partial | `f:528d1ffd` |
| GET | /summaries/{id}/ | id (path, integer, bắt buộc) | (không có) | SummarySchema | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn | inferred (fastapi.default_status_200) / partial | `f:9949c83f` |
| PUT | /summaries/{id}/ | id (path, integer, bắt buộc); payload (body, SummaryUpdatePayloadSchema, bắt buộc) | SummaryUpdatePayloadSchema | SummarySchema | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:5fe06702` |


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
| id | integer | True | False |

### SummarySchema (response)

Fact `f:05d7c815` · exact / partial · khai ở app/models/tortoise.py:14

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| unknown — Model sinh lúc chạy: Model được tạo động bằng pydantic_model_creator(TextSummary) nên các trường chỉ xác định lúc chạy | | | |

### SummaryUpdatePayloadSchema (request)

Fact `f:4bb453f7` · inferred (pydantic.v2_required_no_default) / full · khai ở app/models/pydantic.py:12

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| summary | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:12 | GET | /summaries/ | app/api/summaries.py::read_all_summaries | (rỗng) | fact:05d7c81519deaef5aa62c9ab491941fe87e71c45eb46016e4d2abe1f2957cc70 | 200 | dependency: (không có); auth: unknown — Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn | `fact:321500b56a096ad85bdccc317648480f177d1589a71b65032352cbb7bd9b7f65` | `ev:59c19f1809111b1f34e0a84cf2b17b7adc3624fdd202ff3447f5806bd7286970` (app/api/summaries.py:27-28), `ev:7c28ede5320e4a030b415f410962e61651356b697f18ba69b471e43d1db83f01` (app/api/summaries.py:27), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:bef1584eee1014bda8f10937676ea56f0b92fea40b518aec06eae8a00845a53e` (app/main.py:14-16) | inferred | partial |
| app:app/main.py:12 | POST | /summaries/ | app/api/summaries.py::create_summary | fact:43f1c2376faaeee7f585a94ae06c8bbd43b6fecaeef9e060532bd2beac767353 | fact:167feb5e47f5be075e423e3f8a2eef41e54a144d671b330afd0b9742b51f1cda | 201 | dependency: (không có); auth: unknown — Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn | `fact:e0ea3c8f4c2ecfacee809ac502fdf71b0fd6d370e66e5092e311bbeb616650de` | `ev:1904148ef6e4fd18cfaf05dd71e760a77a76aaf5af855f52150c6d9973b3729b` (app/api/summaries.py:32-35), `ev:daf275969c51cbaeebdc0038c3d3c00bdc3feb560ffae83f64ff907ea225500b` (app/api/summaries.py:32), `ev:71c3fb6811bd07366379c5ebcce0297d62ef90d2b4ec99febe4e2c3f3478dbea` (app/api/summaries.py:34), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:bef1584eee1014bda8f10937676ea56f0b92fea40b518aec06eae8a00845a53e` (app/main.py:14-16) | inferred | partial |
| app:app/main.py:12 | DELETE | /summaries/{id}/ | app/api/summaries.py::delete_summary | (rỗng) | fact:167feb5e47f5be075e423e3f8a2eef41e54a144d671b330afd0b9742b51f1cda | 200 | dependency: (không có); auth: unknown — Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn | `fact:528d1ffdf910cb2228b66bb0a82b2b33b66683bf0512d8e99c750e078ce0d69a` | `ev:1e26640e144cd5f41199af7f3acc4576c3a107c835c7c2902cf33f7612b4cae5` (app/api/summaries.py:55-56), `ev:7ff81516b88d2fe70e370a6645489ff542ac4db5e425732aec97f8c91a4654b4` (app/api/summaries.py:55), `ev:77d57a224bad898fa97daeffab8cd0ed8b4c0cce0454ffd2c3e724082af59c74` (app/api/summaries.py:56), `ev:906f80b4d81c7d89b0196225241ea4af68381a02ec474f1752814d50523539db` (app/api/summaries.py:59), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:bef1584eee1014bda8f10937676ea56f0b92fea40b518aec06eae8a00845a53e` (app/main.py:14-16) | inferred | partial |
| app:app/main.py:12 | GET | /summaries/{id}/ | app/api/summaries.py::read_summary | (rỗng) | fact:05d7c81519deaef5aa62c9ab491941fe87e71c45eb46016e4d2abe1f2957cc70 | 200 | dependency: (không có); auth: unknown — Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn | `fact:9949c83f239b7a1063036de0b3421ea85325a38f120f8d6276d5f625d95c5601` | `ev:43e1188202433f9c6edbd035e7d74b954b77e2267fb5ed0603026e461788a6e5` (app/api/summaries.py:18), `ev:9df3b74005a8464d761295c99c88d945b91b4e291bb307da5f4f3f2e008080d2` (app/api/summaries.py:18-19), `ev:28d77f8bfa7706db41278cf274144d6a97083d5f01c459a1945ef53fa977db74` (app/api/summaries.py:19), `ev:6760bb4ef3b0e3e4c34839a7cf279f0573d516f7304e81e8b80bbd5ec2ba738f` (app/api/summaries.py:22), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:bef1584eee1014bda8f10937676ea56f0b92fea40b518aec06eae8a00845a53e` (app/main.py:14-16) | inferred | partial |
| app:app/main.py:12 | PUT | /summaries/{id}/ | app/api/summaries.py::update_summary | fact:4bb453f7317e4ea3e7627b37eb8f400a6ae09871da25f4b37e3ba0ee493efbad | fact:05d7c81519deaef5aa62c9ab491941fe87e71c45eb46016e4d2abe1f2957cc70 | 200 | dependency: (không có); auth: unknown — Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn | `fact:5fe067026bfce0fed23898d2a8d53c8557770b6561dbdde548933b9e969a6362` | `ev:0dc70978b1bd16cf5202caa1b64ce8c5b31a6deddd3a84270e0f0c9440d58da5` (app/api/summaries.py:44), `ev:7c2711ce8cd3252b4571781e6073a689fa6b60d172da05c8945de62c4ffbaaad` (app/api/summaries.py:44-47), `ev:016117a02e51da1c4121983620a5d9cc77afc96a5a6c5ffc3b3d01659bdec586` (app/api/summaries.py:46), `ev:20f0df2053f5798368db91b552d5c021c0428696b431400ce7f7ea71f966ef7c` (app/api/summaries.py:50), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:bef1584eee1014bda8f10937676ea56f0b92fea40b518aec06eae8a00845a53e` (app/main.py:14-16) | inferred | partial |

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
          }
        },
        "required": [
          "id"
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
          }
        },
        "required": [
          "summary"
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
        "operationId": "op_321500b56a096ad8",
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
        "summary": "Liệt kê tất cả các bản tóm tắt.",
        "tags": [
          "summaries"
        ],
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:59c19f1809111b1f34e0a84cf2b17b7adc3624fdd202ff3447f5806bd7286970",
            "ev:7c28ede5320e4a030b415f410962e61651356b697f18ba69b471e43d1db83f01",
            "ev:bef1584eee1014bda8f10937676ea56f0b92fea40b518aec06eae8a00845a53e",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"
          ],
          "fact_ids": [
            "fact:321500b56a096ad85bdccc317648480f177d1589a71b65032352cbb7bd9b7f65"
          ],
          "summary_origin": "AI viết, không phải dữ kiện đã kiểm",
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn"
            }
          ]
        }
      },
      "post": {
        "operationId": "op_e0ea3c8f4c2ecfac",
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
        "summary": "Tạo mới một URL cần tóm tắt và trả về id.",
        "tags": [
          "summaries"
        ],
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:1904148ef6e4fd18cfaf05dd71e760a77a76aaf5af855f52150c6d9973b3729b",
            "ev:71c3fb6811bd07366379c5ebcce0297d62ef90d2b4ec99febe4e2c3f3478dbea",
            "ev:bef1584eee1014bda8f10937676ea56f0b92fea40b518aec06eae8a00845a53e",
            "ev:daf275969c51cbaeebdc0038c3d3c00bdc3feb560ffae83f64ff907ea225500b",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"
          ],
          "fact_ids": [
            "fact:e0ea3c8f4c2ecfacee809ac502fdf71b0fd6d370e66e5092e311bbeb616650de"
          ],
          "summary_origin": "AI viết, không phải dữ kiện đã kiểm",
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn"
            }
          ]
        }
      }
    },
    "/summaries/{id}/": {
      "delete": {
        "operationId": "op_528d1ffdf910cb22",
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
        "summary": "Xóa bản tóm tắt theo id.",
        "tags": [
          "summaries"
        ],
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:1e26640e144cd5f41199af7f3acc4576c3a107c835c7c2902cf33f7612b4cae5",
            "ev:77d57a224bad898fa97daeffab8cd0ed8b4c0cce0454ffd2c3e724082af59c74",
            "ev:7ff81516b88d2fe70e370a6645489ff542ac4db5e425732aec97f8c91a4654b4",
            "ev:906f80b4d81c7d89b0196225241ea4af68381a02ec474f1752814d50523539db",
            "ev:bef1584eee1014bda8f10937676ea56f0b92fea40b518aec06eae8a00845a53e",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"
          ],
          "fact_ids": [
            "fact:528d1ffdf910cb2228b66bb0a82b2b33b66683bf0512d8e99c750e078ce0d69a"
          ],
          "summary_origin": "AI viết, không phải dữ kiện đã kiểm",
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn"
            }
          ]
        }
      },
      "get": {
        "operationId": "op_9949c83f239b7a10",
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
            "ev:6760bb4ef3b0e3e4c34839a7cf279f0573d516f7304e81e8b80bbd5ec2ba738f",
            "ev:9df3b74005a8464d761295c99c88d945b91b4e291bb307da5f4f3f2e008080d2",
            "ev:bef1584eee1014bda8f10937676ea56f0b92fea40b518aec06eae8a00845a53e",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"
          ],
          "fact_ids": [
            "fact:9949c83f239b7a1063036de0b3421ea85325a38f120f8d6276d5f625d95c5601"
          ],
          "summary_origin": "AI viết, không phải dữ kiện đã kiểm",
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn"
            }
          ]
        }
      },
      "put": {
        "operationId": "op_5fe067026bfce0fe",
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
        "summary": "Cập nhật URL và nội dung tóm tắt theo id.",
        "tags": [
          "summaries"
        ],
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:016117a02e51da1c4121983620a5d9cc77afc96a5a6c5ffc3b3d01659bdec586",
            "ev:0dc70978b1bd16cf5202caa1b64ce8c5b31a6deddd3a84270e0f0c9440d58da5",
            "ev:20f0df2053f5798368db91b552d5c021c0428696b431400ce7f7ea71f966ef7c",
            "ev:7c2711ce8cd3252b4571781e6073a689fa6b60d172da05c8945de62c4ffbaaad",
            "ev:bef1584eee1014bda8f10937676ea56f0b92fea40b518aec06eae8a00845a53e",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"
          ],
          "fact_ids": [
            "fact:5fe067026bfce0fed23898d2a8d53c8557770b6561dbdde548933b9e969a6362"
          ],
          "summary_origin": "AI viết, không phải dữ kiện đã kiểm",
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy dùng Security/Depends với scheme bảo mật nào trong mã nguồn"
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
