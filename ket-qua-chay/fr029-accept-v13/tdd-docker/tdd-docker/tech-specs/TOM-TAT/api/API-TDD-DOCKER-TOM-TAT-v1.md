---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:8053c30b1c2e0701055f23718e5cba06736e299abd4a84a3ff4f205501454276"
owner_component_id: "cmp_85e5e3b3cfed5d952d022b245b713c4fae7484c0c89106444b395f7de26b8491"
owner_component: "Tóm tắt"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v13"
fact_ids: ["fact:27d4c03f2cc6ab992589bdc2140f284fbde74d3d4ee4df039651c83f0828a5f3", "fact:9cc26dbf00e1ced95dfba1696c572e0df1e1e81b1c7cb3fbc726e3edde3dd901", "fact:a81cc73da6dc338036d4c3c4cc2290ab9945f940b1a27ade22cbb612e9040d3f", "fact:b2245d2cb5ae50340b50f6118481296eef0a4873567f2ccf3bc988b522ef4f88", "fact:b58a62b51ef611299d947f8f1a89a6c1cac6bd38b226c016214fff8e2ca80ecd", "fact:167feb5e47f5be075e423e3f8a2eef41e54a144d671b330afd0b9742b51f1cda", "fact:43f1c2376faaeee7f585a94ae06c8bbd43b6fecaeef9e060532bd2beac767353", "fact:4bb453f7317e4ea3e7627b37eb8f400a6ae09871da25f4b37e3ba0ee493efbad"]
evidence_ids: ["ev:016117a02e51da1c4121983620a5d9cc77afc96a5a6c5ffc3b3d01659bdec586", "ev:0dc70978b1bd16cf5202caa1b64ce8c5b31a6deddd3a84270e0f0c9440d58da5", "ev:1904148ef6e4fd18cfaf05dd71e760a77a76aaf5af855f52150c6d9973b3729b", "ev:1e26640e144cd5f41199af7f3acc4576c3a107c835c7c2902cf33f7612b4cae5", "ev:28d77f8bfa7706db41278cf274144d6a97083d5f01c459a1945ef53fa977db74", "ev:348b57d60a023374d7c074008931232cb7a6785b7c89f9a83b4f1f92fbe98de5", "ev:43e1188202433f9c6edbd035e7d74b954b77e2267fb5ed0603026e461788a6e5", "ev:59c19f1809111b1f34e0a84cf2b17b7adc3624fdd202ff3447f5806bd7286970", "ev:65714d070ef1ef28621f1c3b5e49c35f8583deea45ec2544532a17735965264c", "ev:6a65161d107244c45e8360473ce06c0133b51d768958a02c2a7d6bdd53aa5d42", "ev:71c3fb6811bd07366379c5ebcce0297d62ef90d2b4ec99febe4e2c3f3478dbea", "ev:77d57a224bad898fa97daeffab8cd0ed8b4c0cce0454ffd2c3e724082af59c74", "ev:7c2711ce8cd3252b4571781e6073a689fa6b60d172da05c8945de62c4ffbaaad", "ev:7c28ede5320e4a030b415f410962e61651356b697f18ba69b471e43d1db83f01", "ev:7ff81516b88d2fe70e370a6645489ff542ac4db5e425732aec97f8c91a4654b4", "ev:9df3b74005a8464d761295c99c88d945b91b4e291bb307da5f4f3f2e008080d2", "ev:bf6d07b334c674ade6fa7d61306130a78cdec07238ddac46eaba53cd3978b87a", "ev:daf275969c51cbaeebdc0038c3d3c00bdc3feb560ffae83f64ff907ea225500b", "ev:dcb23e8eb0e9bf043bf1fd468723a3c7710f1d11a5dd62d995fab54e10a6ccfe", "ev:e4095ecce252c3e4d25fb52006d94d3916d3246bfcff0cc237e076f491215592", "ev:ec335a0e1fc46a84860fa7b545926df54ad495b7793110f5607290ee630e573f", "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"]
---
# API — Tóm tắt

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /summaries/ | (không có) | (không có) | unknown — SummarySchema được tạo động bằng pydantic_model_creator(TextSummary); cấu trúc Pydantic hoàn chỉnh không được khai báo trực tiếp trong snapshot. | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200) / partial | `f:27d4c03f` |
| POST | /summaries/ | payload (body, SummaryPayloadSchema, bắt buộc) | SummaryPayloadSchema | SummaryResponseSchema | 201 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.model_param_body) / partial | `f:a81cc73d` |
| DELETE | /summaries/{id}/ | id (path, integer, bắt buộc) | (không có) | SummaryResponseSchema | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200) / partial | `f:b2245d2c` |
| GET | /summaries/{id}/ | id (path, integer, bắt buộc) | (không có) | unknown — SummarySchema được tạo động bằng pydantic_model_creator(TextSummary); cấu trúc Pydantic hoàn chỉnh không được khai báo trực tiếp trong snapshot. | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200) / partial | `f:9cc26dbf` |
| PUT | /summaries/{id}/ | id (path, integer, bắt buộc); payload (body, SummaryUpdatePayloadSchema, bắt buộc) | SummaryUpdatePayloadSchema | unknown — SummarySchema được tạo động bằng pydantic_model_creator(TextSummary); cấu trúc Pydantic hoàn chỉnh không được khai báo trực tiếp trong snapshot. | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:b58a62b5` |


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

### SummaryUpdatePayloadSchema (request)

Fact `f:4bb453f7` · inferred (pydantic.v2_required_no_default) / full · khai ở app/models/pydantic.py:12

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| url | string | True | False |
| summary | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:12 | GET | /summaries/ | app/api/summaries.py::read_all_summaries | (rỗng) | unknown — SummarySchema được tạo động bằng pydantic_model_creator(TextSummary); cấu trúc Pydantic hoàn chỉnh không được khai báo trực tiếp trong snapshot. | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:27d4c03f2cc6ab992589bdc2140f284fbde74d3d4ee4df039651c83f0828a5f3` | `ev:59c19f1809111b1f34e0a84cf2b17b7adc3624fdd202ff3447f5806bd7286970` (app/api/summaries.py:27-28), `ev:7c28ede5320e4a030b415f410962e61651356b697f18ba69b471e43d1db83f01` (app/api/summaries.py:27), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:65714d070ef1ef28621f1c3b5e49c35f8583deea45ec2544532a17735965264c` (app/main.py:14-15) | inferred | partial |
| app:app/main.py:12 | POST | /summaries/ | app/api/summaries.py::create_summary | fact:43f1c2376faaeee7f585a94ae06c8bbd43b6fecaeef9e060532bd2beac767353 | fact:167feb5e47f5be075e423e3f8a2eef41e54a144d671b330afd0b9742b51f1cda | 201 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:a81cc73da6dc338036d4c3c4cc2290ab9945f940b1a27ade22cbb612e9040d3f` | `ev:1904148ef6e4fd18cfaf05dd71e760a77a76aaf5af855f52150c6d9973b3729b` (app/api/summaries.py:32-35), `ev:daf275969c51cbaeebdc0038c3d3c00bdc3feb560ffae83f64ff907ea225500b` (app/api/summaries.py:32), `ev:71c3fb6811bd07366379c5ebcce0297d62ef90d2b4ec99febe4e2c3f3478dbea` (app/api/summaries.py:34), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:65714d070ef1ef28621f1c3b5e49c35f8583deea45ec2544532a17735965264c` (app/main.py:14-15) | inferred | partial |
| app:app/main.py:12 | DELETE | /summaries/{id}/ | app/api/summaries.py::delete_summary | (rỗng) | fact:167feb5e47f5be075e423e3f8a2eef41e54a144d671b330afd0b9742b51f1cda | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:b2245d2cb5ae50340b50f6118481296eef0a4873567f2ccf3bc988b522ef4f88` | `ev:1e26640e144cd5f41199af7f3acc4576c3a107c835c7c2902cf33f7612b4cae5` (app/api/summaries.py:55-56), `ev:7ff81516b88d2fe70e370a6645489ff542ac4db5e425732aec97f8c91a4654b4` (app/api/summaries.py:55), `ev:77d57a224bad898fa97daeffab8cd0ed8b4c0cce0454ffd2c3e724082af59c74` (app/api/summaries.py:56), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:65714d070ef1ef28621f1c3b5e49c35f8583deea45ec2544532a17735965264c` (app/main.py:14-15) | inferred | partial |
| app:app/main.py:12 | GET | /summaries/{id}/ | app/api/summaries.py::read_summary | (rỗng) | unknown — SummarySchema được tạo động bằng pydantic_model_creator(TextSummary); cấu trúc Pydantic hoàn chỉnh không được khai báo trực tiếp trong snapshot. | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:9cc26dbf00e1ced95dfba1696c572e0df1e1e81b1c7cb3fbc726e3edde3dd901` | `ev:43e1188202433f9c6edbd035e7d74b954b77e2267fb5ed0603026e461788a6e5` (app/api/summaries.py:18), `ev:9df3b74005a8464d761295c99c88d945b91b4e291bb307da5f4f3f2e008080d2` (app/api/summaries.py:18-19), `ev:28d77f8bfa7706db41278cf274144d6a97083d5f01c459a1945ef53fa977db74` (app/api/summaries.py:19), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:65714d070ef1ef28621f1c3b5e49c35f8583deea45ec2544532a17735965264c` (app/main.py:14-15) | inferred | partial |
| app:app/main.py:12 | PUT | /summaries/{id}/ | app/api/summaries.py::update_summary | fact:4bb453f7317e4ea3e7627b37eb8f400a6ae09871da25f4b37e3ba0ee493efbad | unknown — SummarySchema được tạo động bằng pydantic_model_creator(TextSummary); cấu trúc Pydantic hoàn chỉnh không được khai báo trực tiếp trong snapshot. | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:b58a62b51ef611299d947f8f1a89a6c1cac6bd38b226c016214fff8e2ca80ecd` | `ev:0dc70978b1bd16cf5202caa1b64ce8c5b31a6deddd3a84270e0f0c9440d58da5` (app/api/summaries.py:44), `ev:7c2711ce8cd3252b4571781e6073a689fa6b60d172da05c8945de62c4ffbaaad` (app/api/summaries.py:44-47), `ev:016117a02e51da1c4121983620a5d9cc77afc96a5a6c5ffc3b3d01659bdec586` (app/api/summaries.py:46), `ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3` (app/main.py:12), `ev:65714d070ef1ef28621f1c3b5e49c35f8583deea45ec2544532a17735965264c` (app/main.py:14-15) | inferred | partial |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| SummaryPayloadSchema | fact:43f1c2376faaeee7f585a94ae06c8bbd43b6fecaeef9e060532bd2beac767353 | app/models/pydantic.py:4 |
| SummaryResponseSchema | fact:167feb5e47f5be075e423e3f8a2eef41e54a144d671b330afd0b9742b51f1cda | app/models/pydantic.py:8 |
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
        "operationId": "op_27d4c03f2cc6ab99",
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:59c19f1809111b1f34e0a84cf2b17b7adc3624fdd202ff3447f5806bd7286970",
            "ev:65714d070ef1ef28621f1c3b5e49c35f8583deea45ec2544532a17735965264c",
            "ev:7c28ede5320e4a030b415f410962e61651356b697f18ba69b471e43d1db83f01",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"
          ],
          "fact_ids": [
            "fact:27d4c03f2cc6ab992589bdc2140f284fbde74d3d4ee4df039651c83f0828a5f3"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn."
            },
            {
              "field": "response_model_ids",
              "reason": "SummarySchema được tạo động bằng pydantic_model_creator(TextSummary); cấu trúc Pydantic hoàn chỉnh không được khai báo trực tiếp trong snapshot."
            }
          ]
        }
      },
      "post": {
        "operationId": "op_a81cc73da6dc3380",
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
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:1904148ef6e4fd18cfaf05dd71e760a77a76aaf5af855f52150c6d9973b3729b",
            "ev:65714d070ef1ef28621f1c3b5e49c35f8583deea45ec2544532a17735965264c",
            "ev:71c3fb6811bd07366379c5ebcce0297d62ef90d2b4ec99febe4e2c3f3478dbea",
            "ev:daf275969c51cbaeebdc0038c3d3c00bdc3feb560ffae83f64ff907ea225500b",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"
          ],
          "fact_ids": [
            "fact:a81cc73da6dc338036d4c3c4cc2290ab9945f940b1a27ade22cbb612e9040d3f"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn."
            }
          ]
        }
      }
    },
    "/summaries/{id}/": {
      "delete": {
        "operationId": "op_b2245d2cb5ae5034",
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
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:1e26640e144cd5f41199af7f3acc4576c3a107c835c7c2902cf33f7612b4cae5",
            "ev:65714d070ef1ef28621f1c3b5e49c35f8583deea45ec2544532a17735965264c",
            "ev:77d57a224bad898fa97daeffab8cd0ed8b4c0cce0454ffd2c3e724082af59c74",
            "ev:7ff81516b88d2fe70e370a6645489ff542ac4db5e425732aec97f8c91a4654b4",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"
          ],
          "fact_ids": [
            "fact:b2245d2cb5ae50340b50f6118481296eef0a4873567f2ccf3bc988b522ef4f88"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn."
            }
          ]
        }
      },
      "get": {
        "operationId": "op_9cc26dbf00e1ced9",
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
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:28d77f8bfa7706db41278cf274144d6a97083d5f01c459a1945ef53fa977db74",
            "ev:43e1188202433f9c6edbd035e7d74b954b77e2267fb5ed0603026e461788a6e5",
            "ev:65714d070ef1ef28621f1c3b5e49c35f8583deea45ec2544532a17735965264c",
            "ev:9df3b74005a8464d761295c99c88d945b91b4e291bb307da5f4f3f2e008080d2",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"
          ],
          "fact_ids": [
            "fact:9cc26dbf00e1ced95dfba1696c572e0df1e1e81b1c7cb3fbc726e3edde3dd901"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn."
            },
            {
              "field": "response_model_ids",
              "reason": "SummarySchema được tạo động bằng pydantic_model_creator(TextSummary); cấu trúc Pydantic hoàn chỉnh không được khai báo trực tiếp trong snapshot."
            }
          ]
        }
      },
      "put": {
        "operationId": "op_b58a62b51ef61129",
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
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:016117a02e51da1c4121983620a5d9cc77afc96a5a6c5ffc3b3d01659bdec586",
            "ev:0dc70978b1bd16cf5202caa1b64ce8c5b31a6deddd3a84270e0f0c9440d58da5",
            "ev:65714d070ef1ef28621f1c3b5e49c35f8583deea45ec2544532a17735965264c",
            "ev:7c2711ce8cd3252b4571781e6073a689fa6b60d172da05c8945de62c4ffbaaad",
            "ev:ee9e0bb20a698c850733acca9c03a84f6bb9c9afadde4c7d26d0930f31876ff3"
          ],
          "fact_ids": [
            "fact:b58a62b51ef611299d947f8f1a89a6c1cac6bd38b226c016214fff8e2ca80ecd"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn."
            },
            {
              "field": "response_model_ids",
              "reason": "SummarySchema được tạo động bằng pydantic_model_creator(TextSummary); cấu trúc Pydantic hoàn chỉnh không được khai báo trực tiếp trong snapshot."
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
