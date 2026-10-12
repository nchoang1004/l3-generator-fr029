---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:96f8c4c9bb1fbd6f13ba0f2b1a22b3c98fb3e718c6744a39e04ab68535bb4a3f"
owner_component_id: "cmp_77d00468473b3d9cbf4115656fefa81533a7e1ded485391ddf934929803f1718"
owner_component: "app"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v14"
fact_ids: ["fact:58267a2dc97be8e1cf98db45864284014d54b1d3b866ce12ce6cdd69724ea468", "fact:88865f96799816cb25d1f9820774627c1568181d0700347031677de424af1ca9", "fact:d31b8c0bcef1f0b726ad90ae881ddf6119466ec6c79e8dc7f2a8486a4c9fe3a6", "fact:4bf1bb9fdd716a56a2f96a7885d1526ffd6e5df62022c696160988132b5717fb", "fact:96b5ecfb218cc917d4679fd6970ab1d252ce8255cf1493cb31d79e92549751eb", "fact:af1ae74b2961783d48f87906e8ca0c6ee5bdf647844848341d34d133b3d536f3", "fact:bb7ada39b88829d0e47d239ee5c7c8574dc8e3f6580ac71e62ef413d774f7832"]
evidence_ids: ["ev:06676ce2ec12644967d3dcd45ae9fec820ae4d3a5aff7131a33d25551291be94", "ev:2a49ce633ff92b646be4aed043f881dff3c3d59ded8d74aab4909110417b207d", "ev:31f9f3f18b56fd3bc5d5476f30f12ea5dc682e4c9e45e4415c2d789d98906d5f", "ev:42890896d296aede559557207a53d74fbbfa78271fbf12f2032c93d6e6ddc4eb", "ev:471ff81f5b918161d9c92353a15b80fd78d7dc0834ae463470dfeda2e2c998dc", "ev:47fe30beca58e156fc1de8cc87b9540a2413acf494d016c0d87ef9f6470476a8", "ev:514a89571100dc0c54e802353dcc10b25a47d8766f7fed05e2ab8f31549ff224", "ev:550f204a3b1830d6d448c325460d2387eb3a8670efd60f7e38753e4e5afaff7a", "ev:5ab8476e889847d3c43160c87152958dad8fc4c0fb790afd26bba78cde85e26f", "ev:65747df9bdc5657e6683698ca867e04f1e2d5a71c0dcb73170f3b3a626b89958", "ev:691eb42a696f133ac73407bd1c74c8137c7599729261a2422c5f1c5f08b109c4", "ev:69644e82240d6c1437eb1bc09455d568b2a229436cb762dbec57854c8467084e", "ev:6d1d9da583f3ae572e52066766a789740e6bdf7823565b15264d4fbec14d3e35", "ev:6e36025adb6e7afdf78eae80f251ae761c043b1e6184657733cf17112ff2a84c", "ev:8a480d9c60693e24e2196ba68b5bfd2261dfa43526774ad15221ed4d5677c84a", "ev:99a6b9f259794ac3c3cfea812eb59749ca3c3902561b7d2f76fd6c3dc8e7a866", "ev:a07fbdc6a26995824d2ca34bfa3e68471cace5095952a72c3dcb5b59c29d2a78", "ev:abf9aff71d53838541bcb99f82f0389eda7e5a0eb98493b69d770c23ac528831", "ev:ad9d8dbb632d2fe198b397ceb9b23413b790c4b8a3d4716486e299a2e0eb6b12", "ev:b8e78a6be419783187a0e2ce1d601068cc061837c837e3fec4bf1aa037aa9f73", "ev:c74a142deaa5ef2db657a00eb30ab165e7f1368c563a864613c5e2cd522cf121", "ev:d026a62f1fbcf03948291bae2c35d68b126bf015f22bf09fbcae62b467501367", "ev:d407f990ac428364cd62e2a18a81a02f294009518eca7c67cfeef53ed0c1443c", "ev:d9d342b43668ddb2e10a5bf46f4d869ec0ed50ad1d1dc2cdc986393b59730d55", "ev:db6feb5005fb09cf3bd9f921637b666b7c6e34be6f26dfa4a4480b2b61447be9", "ev:ddf8b13b1bd073ca78db021b4ad616a1d85b0f79835f0451661ff8a452fe711d", "ev:dea5a604df7602532395b3c348f6fa865ad6786993efc8d54356325789c4bbfd", "ev:e28f2d976f2bb9f4a4f5425ba7a44c0cd04b334b4d3df2d899a9af52a56f4d1d", "ev:e370521275ec5d5f7842f7ef01e1cc4f823523aa602967b73f0e1f158f14328d", "ev:edc6a1a7c98763f04a73bd8fecde0815bd61cf3b16cb7ebab3a2e5aec6b70820"]
---
# API — app

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | / | limit (query, integer, tùy chọn); prev (query, integer, tùy chọn) | (không có) | list[GetUserListResponseDTO] | 200 (suy theo fastapi.default_status_200) | dependency: PermissionDependency; auth: unknown — Không thấy mã xác thực cụ thể trong mã nguồn; chỉ thấy dependency kiểm tra quyền cho route này | inferred (fastapi.default_status_200, fastapi.scalar_param_query) / partial | `f:d31b8c0b` |
| POST | / | request (body, CreateUserRequest, bắt buộc) | CreateUserRequest | unknown — Model chưa được agent nộp: app/user/application/dto/__init__.py::CreateUserResponseDTO | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy mã xác thực cụ thể trong mã nguồn | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:58267a2d` |
| POST | /login | request (body, LoginRequest, bắt buộc) | LoginRequest | LoginResponse | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy mã xác thực cụ thể trong mã nguồn | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:88865f96` |


## Model

### CreateUserRequest (request)

Fact `f:bb7ada39` · exact / full · khai ở app/user/adapter/input/api/v1/request/__init__.py:9

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| email | string | True | False |
| password1 | string | True | False |
| password2 | string | True | False |
| nickname | string | True | False |
| lat | number | True | False |
| lng | number | True | False |

### GetUserListResponseDTO (response)

Fact `f:96b5ecfb` · exact / full · khai ở app/user/application/dto/__init__.py:4

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| id | integer | True | False |
| email | string | True | False |

### LoginRequest (request)

Fact `f:af1ae74b` · exact / full · khai ở app/user/adapter/input/api/v1/request/__init__.py:4

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| email | string | True | False |
| password | string | True | False |

### LoginResponse (response)

Fact `f:4bf1bb9f` · exact / full · khai ở app/user/adapter/input/api/v1/response/__init__.py:4

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| token | string | True | False |
| refresh_token | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/server.py:77 | GET | / | app/user/adapter/input/api/v1/user.py::get_user_list | (rỗng) | fact:96b5ecfb218cc917d4679fd6970ab1d252ce8255cf1493cb31d79e92549751eb | 200 | dependency: PermissionDependency; auth: unknown — Không thấy mã xác thực cụ thể trong mã nguồn; chỉ thấy dependency kiểm tra quyền cho route này | `fact:d31b8c0bcef1f0b726ad90ae881ddf6119466ec6c79e8dc7f2a8486a4c9fe3a6` | `ev:31f9f3f18b56fd3bc5d5476f30f12ea5dc682e4c9e45e4415c2d789d98906d5f` (app/server.py:77), `ev:db6feb5005fb09cf3bd9f921637b666b7c6e34be6f26dfa4a4480b2b61447be9` (app/user/adapter/input/api/v1/user.py:15-26), `ev:69644e82240d6c1437eb1bc09455d568b2a229436cb762dbec57854c8467084e` (app/user/adapter/input/api/v1/user.py:16), `ev:5ab8476e889847d3c43160c87152958dad8fc4c0fb790afd26bba78cde85e26f` (app/user/adapter/input/api/v1/user.py:17), `ev:6d1d9da583f3ae572e52066766a789740e6bdf7823565b15264d4fbec14d3e35` (app/user/adapter/input/api/v1/user.py:18), `ev:42890896d296aede559557207a53d74fbbfa78271fbf12f2032c93d6e6ddc4eb` (app/user/adapter/input/api/v1/user.py:22), `ev:ad9d8dbb632d2fe198b397ceb9b23413b790c4b8a3d4716486e299a2e0eb6b12` (app/user/adapter/input/api/v1/user.py:23) | inferred | partial |
| app:app/server.py:77 | POST | / | app/user/adapter/input/api/v1/user.py::create_user | fact:bb7ada39b88829d0e47d239ee5c7c8574dc8e3f6580ac71e62ef413d774f7832 | unknown — Model chưa được agent nộp: app/user/application/dto/__init__.py::CreateUserResponseDTO | 200 | dependency: (không có); auth: unknown — Không thấy mã xác thực cụ thể trong mã nguồn | `fact:58267a2dc97be8e1cf98db45864284014d54b1d3b866ce12ce6cdd69724ea468` | `ev:31f9f3f18b56fd3bc5d5476f30f12ea5dc682e4c9e45e4415c2d789d98906d5f` (app/server.py:77), `ev:471ff81f5b918161d9c92353a15b80fd78d7dc0834ae463470dfeda2e2c998dc` (app/user/adapter/input/api/v1/user.py:29-40), `ev:d026a62f1fbcf03948291bae2c35d68b126bf015f22bf09fbcae62b467501367` (app/user/adapter/input/api/v1/user.py:30), `ev:dea5a604df7602532395b3c348f6fa865ad6786993efc8d54356325789c4bbfd` (app/user/adapter/input/api/v1/user.py:35) | inferred | partial |
| app:app/server.py:77 | POST | /login | app/user/adapter/input/api/v1/user.py::login | fact:af1ae74b2961783d48f87906e8ca0c6ee5bdf647844848341d34d133b3d536f3 | fact:4bf1bb9fdd716a56a2f96a7885d1526ffd6e5df62022c696160988132b5717fb | 200 | dependency: (không có); auth: unknown — Không thấy mã xác thực cụ thể trong mã nguồn | `fact:88865f96799816cb25d1f9820774627c1568181d0700347031677de424af1ca9` | `ev:31f9f3f18b56fd3bc5d5476f30f12ea5dc682e4c9e45e4415c2d789d98906d5f` (app/server.py:77), `ev:e370521275ec5d5f7842f7ef01e1cc4f823523aa602967b73f0e1f158f14328d` (app/user/adapter/input/api/v1/user.py:43-53), `ev:c74a142deaa5ef2db657a00eb30ab165e7f1368c563a864613c5e2cd522cf121` (app/user/adapter/input/api/v1/user.py:44), `ev:e28f2d976f2bb9f4a4f5425ba7a44c0cd04b334b4d3df2d899a9af52a56f4d1d` (app/user/adapter/input/api/v1/user.py:45), `ev:b8e78a6be419783187a0e2ce1d601068cc061837c837e3fec4bf1aa037aa9f73` (app/user/adapter/input/api/v1/user.py:49) | inferred | partial |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| CreateUserRequest | fact:bb7ada39b88829d0e47d239ee5c7c8574dc8e3f6580ac71e62ef413d774f7832 | app/user/adapter/input/api/v1/request/__init__.py:9 |
| GetUserListResponseDTO | fact:96b5ecfb218cc917d4679fd6970ab1d252ce8255cf1493cb31d79e92549751eb | app/user/application/dto/__init__.py:4 |
| LoginRequest | fact:af1ae74b2961783d48f87906e8ca0c6ee5bdf647844848341d34d133b3d536f3 | app/user/adapter/input/api/v1/request/__init__.py:4 |
| LoginResponse | fact:4bf1bb9fdd716a56a2f96a7885d1526ffd6e5df62022c696160988132b5717fb | app/user/adapter/input/api/v1/response/__init__.py:4 |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "CreateUserRequest_bb7ada39": {
        "properties": {
          "email": {
            "type": "string"
          },
          "lat": {
            "type": "number"
          },
          "lng": {
            "type": "number"
          },
          "nickname": {
            "type": "string"
          },
          "password1": {
            "type": "string"
          },
          "password2": {
            "type": "string"
          }
        },
        "required": [
          "email",
          "lat",
          "lng",
          "nickname",
          "password1",
          "password2"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:bb7ada39b88829d0e47d239ee5c7c8574dc8e3f6580ac71e62ef413d774f7832"
          ]
        }
      },
      "GetUserListResponseDTO_96b5ecfb": {
        "properties": {
          "email": {
            "type": "string"
          },
          "id": {
            "type": "integer"
          }
        },
        "required": [
          "email",
          "id"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:96b5ecfb218cc917d4679fd6970ab1d252ce8255cf1493cb31d79e92549751eb"
          ]
        }
      },
      "LoginRequest_af1ae74b": {
        "properties": {
          "email": {
            "type": "string"
          },
          "password": {
            "type": "string"
          }
        },
        "required": [
          "email",
          "password"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:af1ae74b2961783d48f87906e8ca0c6ee5bdf647844848341d34d133b3d536f3"
          ]
        }
      },
      "LoginResponse_4bf1bb9f": {
        "properties": {
          "refresh_token": {
            "type": "string"
          },
          "token": {
            "type": "string"
          }
        },
        "required": [
          "refresh_token",
          "token"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:4bf1bb9fdd716a56a2f96a7885d1526ffd6e5df62022c696160988132b5717fb"
          ]
        }
      }
    }
  },
  "info": {
    "title": "app",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/": {
      "get": {
        "operationId": "op_d31b8c0bcef1f0b7",
        "parameters": [
          {
            "in": "query",
            "name": "limit",
            "required": false,
            "schema": {
              "type": "integer"
            }
          },
          {
            "in": "query",
            "name": "prev",
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
                  "items": {
                    "$ref": "#/components/schemas/GetUserListResponseDTO_96b5ecfb"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Status code suy theo fastapi.default_status_200"
          }
        },
        "x-analysis": {
          "application_id": "app:app/server.py:77",
          "evidence_ids": [
            "ev:31f9f3f18b56fd3bc5d5476f30f12ea5dc682e4c9e45e4415c2d789d98906d5f",
            "ev:42890896d296aede559557207a53d74fbbfa78271fbf12f2032c93d6e6ddc4eb",
            "ev:5ab8476e889847d3c43160c87152958dad8fc4c0fb790afd26bba78cde85e26f",
            "ev:69644e82240d6c1437eb1bc09455d568b2a229436cb762dbec57854c8467084e",
            "ev:6d1d9da583f3ae572e52066766a789740e6bdf7823565b15264d4fbec14d3e35",
            "ev:ad9d8dbb632d2fe198b397ceb9b23413b790c4b8a3d4716486e299a2e0eb6b12",
            "ev:db6feb5005fb09cf3bd9f921637b666b7c6e34be6f26dfa4a4480b2b61447be9"
          ],
          "fact_ids": [
            "fact:d31b8c0bcef1f0b726ad90ae881ddf6119466ec6c79e8dc7f2a8486a4c9fe3a6"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy mã xác thực cụ thể trong mã nguồn; chỉ thấy dependency kiểm tra quyền cho route này"
            }
          ]
        }
      },
      "post": {
        "operationId": "op_58267a2dc97be8e1",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/CreateUserRequest_bb7ada39"
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
          "application_id": "app:app/server.py:77",
          "evidence_ids": [
            "ev:31f9f3f18b56fd3bc5d5476f30f12ea5dc682e4c9e45e4415c2d789d98906d5f",
            "ev:471ff81f5b918161d9c92353a15b80fd78d7dc0834ae463470dfeda2e2c998dc",
            "ev:d026a62f1fbcf03948291bae2c35d68b126bf015f22bf09fbcae62b467501367",
            "ev:dea5a604df7602532395b3c348f6fa865ad6786993efc8d54356325789c4bbfd"
          ],
          "fact_ids": [
            "fact:58267a2dc97be8e1cf98db45864284014d54b1d3b866ce12ce6cdd69724ea468"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy mã xác thực cụ thể trong mã nguồn"
            },
            {
              "field": "response_model_ids",
              "reason": "Model chưa được agent nộp: app/user/application/dto/__init__.py::CreateUserResponseDTO"
            }
          ]
        }
      }
    },
    "/login": {
      "post": {
        "operationId": "op_88865f96799816cb",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/LoginRequest_af1ae74b"
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
                  "$ref": "#/components/schemas/LoginResponse_4bf1bb9f"
                }
              }
            },
            "description": "Status code suy theo fastapi.default_status_200"
          }
        },
        "x-analysis": {
          "application_id": "app:app/server.py:77",
          "evidence_ids": [
            "ev:31f9f3f18b56fd3bc5d5476f30f12ea5dc682e4c9e45e4415c2d789d98906d5f",
            "ev:b8e78a6be419783187a0e2ce1d601068cc061837c837e3fec4bf1aa037aa9f73",
            "ev:c74a142deaa5ef2db657a00eb30ab165e7f1368c563a864613c5e2cd522cf121",
            "ev:e28f2d976f2bb9f4a4f5425ba7a44c0cd04b334b4d3df2d899a9af52a56f4d1d",
            "ev:e370521275ec5d5f7842f7ef01e1cc4f823523aa602967b73f0e1f158f14328d"
          ],
          "fact_ids": [
            "fact:88865f96799816cb25d1f9820774627c1568181d0700347031677de424af1ca9"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy mã xác thực cụ thể trong mã nguồn"
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
