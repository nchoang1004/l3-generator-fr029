---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:c76102dcd74977697e638089e01037e517bb8e4d9a039f63ffbf8bf79eaca9b7"
owner_component_id: "cmp_d98876360788a56b755a5e6aff01808e8ae50c526988530d22bc81f1e7679c88"
owner_component: "Mặt hàng"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v8"
fact_ids: ["fact:4af986b523d190dd12492a7e6dc8f67081079ef07972d97a3f7217e74706b162", "fact:53dbfa1304a5b9bb6fb31b16df401bf93b822f8770e3ea7c4dd320dc14551398", "fact:631f57cf7960b52f10bd9008eb0949ae80c5ab639367b89f117dfbf4264f4e68", "fact:da35f30233c7c0a537de443860f8d4b8ac10343898c637d8bed3b33dca8ff0d4", "fact:fe073f6a2071a2e7f38eb01d78a1acc1f580375c3aa5a3fc36ab9d6245d1b94d"]
evidence_ids: ["ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08", "ev:24d151db74b631eda4dd7001edd5d150edbf6dca26c749f54baa104f6da3330b", "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8", "ev:3b22b758593bf064eaee418912af609b4781e0f7d5a3f047eccb38ef23f5217b", "ev:46ad7464f5a634bbf89a004ef1bc88aea06c53a6b55e290c8ee4852d45f3b47b", "ev:47511c47971a4955079c4940aab1acea0aa8b11300b9f1a4cc73c03e97369659", "ev:4cf53e990e7cf13f02a8b0c2fcc4af86cc7d67461fbe1f94a6ab7694e5f1944f", "ev:4dd2bac78fe43c63f4bca027c70f8301a6c37c1f6d595f3a0eadbf16616cadd4", "ev:703b930c1028fbed1c8afe330f9eaa663a67af836e4d1be5062339455b771777", "ev:7276eb7ef247279e4449322090b044c449b5196da6659d9d5f2d4ecd9a5d4d5f", "ev:7ba4ab3015c67faf8bc96b71b02d63d3e05ec2c825f02e69c5b4ef93a199cc05", "ev:7cb8593ccc0bc2a9f6fd2dbbdbae894fb22cdfbdf7ddf2480043df7be77fba49", "ev:81382dd3d8f5d5798b9ce5a19076a38bf32f8d364eb1b8e13f1a422d1b37c8ed", "ev:9f9afff67aa5c984d8bf9fd449e0dbc38222603692e14e67084eafbf40351c78", "ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d", "ev:f70dcc170f659b24ea45c999b771d01e88def0db531bf10c91ea90b09ab117e0", "ev:f741f556ff3bcb22bf65b6a7c7b5b809ca8d9ce984e28a83d0967674c4f326dd", "ev:fc46390ad8f5e9fceb97dff255e4b4e9564e48be2aada1fd59db41e2323c8b6c"]
---
# API — Mặt hàng

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /api/v1/items/ | (không có) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200, settings.default_prefix) / partial | `f:53dbfa13` |
| GET | /api/v1/items/{item_id} | item_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200, settings.default_prefix) / partial | `f:4af986b5` |
| GET | /api/v1/items/{item_id}/sync | item_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200, settings.default_prefix) / partial | `f:da35f302` |
| POST | /api/v1/items/{item_id}/sync | item_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200, settings.default_prefix) / partial | `f:631f57cf` |
| GET | /v1/api/items/{item_id} | item_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200) / partial | `f:fe073f6a` |


## Model

Không route nào có request/response model đã xác định.

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:12 | GET | /api/v1/items/ | app/api/items.py::list_items | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:53dbfa1304a5b9bb6fb31b16df401bf93b822f8770e3ea7c4dd320dc14551398` | `ev:46ad7464f5a634bbf89a004ef1bc88aea06c53a6b55e290c8ee4852d45f3b47b` (app/api/api.py:6), `ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d` (app/api/items.py:3), `ev:7276eb7ef247279e4449322090b044c449b5196da6659d9d5f2d4ecd9a5d4d5f` (app/api/items.py:6), `ev:f70dcc170f659b24ea45c999b771d01e88def0db531bf10c91ea90b09ab117e0` (app/api/items.py:6-7), `ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08` (app/config.py:5), `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12), `ev:47511c47971a4955079c4940aab1acea0aa8b11300b9f1a4cc73c03e97369659` (app/main.py:18) | inferred | partial |
| app:app/main.py:12 | GET | /api/v1/items/{item_id} | app/api/items.py::get_item | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:4af986b523d190dd12492a7e6dc8f67081079ef07972d97a3f7217e74706b162` | `ev:46ad7464f5a634bbf89a004ef1bc88aea06c53a6b55e290c8ee4852d45f3b47b` (app/api/api.py:6), `ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d` (app/api/items.py:3), `ev:7ba4ab3015c67faf8bc96b71b02d63d3e05ec2c825f02e69c5b4ef93a199cc05` (app/api/items.py:11-12), `ev:81382dd3d8f5d5798b9ce5a19076a38bf32f8d364eb1b8e13f1a422d1b37c8ed` (app/api/items.py:11), `ev:24d151db74b631eda4dd7001edd5d150edbf6dca26c749f54baa104f6da3330b` (app/api/items.py:12), `ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08` (app/config.py:5), `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12), `ev:47511c47971a4955079c4940aab1acea0aa8b11300b9f1a4cc73c03e97369659` (app/main.py:18) | inferred | partial |
| app:app/main.py:12 | GET | /api/v1/items/{item_id}/sync | app/api/items.py::sync_item | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:da35f30233c7c0a537de443860f8d4b8ac10343898c637d8bed3b33dca8ff0d4` | `ev:46ad7464f5a634bbf89a004ef1bc88aea06c53a6b55e290c8ee4852d45f3b47b` (app/api/api.py:6), `ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d` (app/api/items.py:3), `ev:4cf53e990e7cf13f02a8b0c2fcc4af86cc7d67461fbe1f94a6ab7694e5f1944f` (app/api/items.py:16-17), `ev:4dd2bac78fe43c63f4bca027c70f8301a6c37c1f6d595f3a0eadbf16616cadd4` (app/api/items.py:16), `ev:7cb8593ccc0bc2a9f6fd2dbbdbae894fb22cdfbdf7ddf2480043df7be77fba49` (app/api/items.py:17), `ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08` (app/config.py:5), `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12), `ev:47511c47971a4955079c4940aab1acea0aa8b11300b9f1a4cc73c03e97369659` (app/main.py:18) | inferred | partial |
| app:app/main.py:12 | POST | /api/v1/items/{item_id}/sync | app/api/items.py::sync_item | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:631f57cf7960b52f10bd9008eb0949ae80c5ab639367b89f117dfbf4264f4e68` | `ev:46ad7464f5a634bbf89a004ef1bc88aea06c53a6b55e290c8ee4852d45f3b47b` (app/api/api.py:6), `ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d` (app/api/items.py:3), `ev:4cf53e990e7cf13f02a8b0c2fcc4af86cc7d67461fbe1f94a6ab7694e5f1944f` (app/api/items.py:16-17), `ev:4dd2bac78fe43c63f4bca027c70f8301a6c37c1f6d595f3a0eadbf16616cadd4` (app/api/items.py:16), `ev:7cb8593ccc0bc2a9f6fd2dbbdbae894fb22cdfbdf7ddf2480043df7be77fba49` (app/api/items.py:17), `ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08` (app/config.py:5), `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12), `ev:47511c47971a4955079c4940aab1acea0aa8b11300b9f1a4cc73c03e97369659` (app/main.py:18) | inferred | partial |
| app:app/main.py:12 | GET | /v1/api/items/{item_id} | app/api/legacy.py::legacy_get_item | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:fe073f6a2071a2e7f38eb01d78a1acc1f580375c3aa5a3fc36ab9d6245d1b94d` | `ev:3b22b758593bf064eaee418912af609b4781e0f7d5a3f047eccb38ef23f5217b` (app/api/legacy.py:3), `ev:703b930c1028fbed1c8afe330f9eaa663a67af836e4d1be5062339455b771777` (app/api/legacy.py:6), `ev:f741f556ff3bcb22bf65b6a7c7b5b809ca8d9ce984e28a83d0967674c4f326dd` (app/api/legacy.py:6-7), `ev:9f9afff67aa5c984d8bf9fd449e0dbc38222603692e14e67084eafbf40351c78` (app/api/legacy.py:7), `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12), `ev:fc46390ad8f5e9fceb97dff255e4b4e9564e48be2aada1fd59db41e2323c8b6c` (app/main.py:21) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Mặt hàng",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/api/v1/items/": {
      "get": {
        "operationId": "op_53dbfa1304a5b9bb",
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08",
            "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8",
            "ev:46ad7464f5a634bbf89a004ef1bc88aea06c53a6b55e290c8ee4852d45f3b47b",
            "ev:47511c47971a4955079c4940aab1acea0aa8b11300b9f1a4cc73c03e97369659",
            "ev:7276eb7ef247279e4449322090b044c449b5196da6659d9d5f2d4ecd9a5d4d5f",
            "ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d",
            "ev:f70dcc170f659b24ea45c999b771d01e88def0db531bf10c91ea90b09ab117e0"
          ],
          "fact_ids": [
            "fact:53dbfa1304a5b9bb6fb31b16df401bf93b822f8770e3ea7c4dd320dc14551398"
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
    "/api/v1/items/{item_id}": {
      "get": {
        "operationId": "op_4af986b523d190dd",
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
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08",
            "ev:24d151db74b631eda4dd7001edd5d150edbf6dca26c749f54baa104f6da3330b",
            "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8",
            "ev:46ad7464f5a634bbf89a004ef1bc88aea06c53a6b55e290c8ee4852d45f3b47b",
            "ev:47511c47971a4955079c4940aab1acea0aa8b11300b9f1a4cc73c03e97369659",
            "ev:7ba4ab3015c67faf8bc96b71b02d63d3e05ec2c825f02e69c5b4ef93a199cc05",
            "ev:81382dd3d8f5d5798b9ce5a19076a38bf32f8d364eb1b8e13f1a422d1b37c8ed",
            "ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d"
          ],
          "fact_ids": [
            "fact:4af986b523d190dd12492a7e6dc8f67081079ef07972d97a3f7217e74706b162"
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
    "/api/v1/items/{item_id}/sync": {
      "get": {
        "operationId": "op_da35f30233c7c0a5",
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
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08",
            "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8",
            "ev:46ad7464f5a634bbf89a004ef1bc88aea06c53a6b55e290c8ee4852d45f3b47b",
            "ev:47511c47971a4955079c4940aab1acea0aa8b11300b9f1a4cc73c03e97369659",
            "ev:4cf53e990e7cf13f02a8b0c2fcc4af86cc7d67461fbe1f94a6ab7694e5f1944f",
            "ev:4dd2bac78fe43c63f4bca027c70f8301a6c37c1f6d595f3a0eadbf16616cadd4",
            "ev:7cb8593ccc0bc2a9f6fd2dbbdbae894fb22cdfbdf7ddf2480043df7be77fba49",
            "ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d"
          ],
          "fact_ids": [
            "fact:da35f30233c7c0a537de443860f8d4b8ac10343898c637d8bed3b33dca8ff0d4"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn."
            }
          ]
        }
      },
      "post": {
        "operationId": "op_631f57cf7960b52f",
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
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08",
            "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8",
            "ev:46ad7464f5a634bbf89a004ef1bc88aea06c53a6b55e290c8ee4852d45f3b47b",
            "ev:47511c47971a4955079c4940aab1acea0aa8b11300b9f1a4cc73c03e97369659",
            "ev:4cf53e990e7cf13f02a8b0c2fcc4af86cc7d67461fbe1f94a6ab7694e5f1944f",
            "ev:4dd2bac78fe43c63f4bca027c70f8301a6c37c1f6d595f3a0eadbf16616cadd4",
            "ev:7cb8593ccc0bc2a9f6fd2dbbdbae894fb22cdfbdf7ddf2480043df7be77fba49",
            "ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d"
          ],
          "fact_ids": [
            "fact:631f57cf7960b52f10bd9008eb0949ae80c5ab639367b89f117dfbf4264f4e68"
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
    "/v1/api/items/{item_id}": {
      "get": {
        "operationId": "op_fe073f6a2071a2e7",
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
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8",
            "ev:3b22b758593bf064eaee418912af609b4781e0f7d5a3f047eccb38ef23f5217b",
            "ev:703b930c1028fbed1c8afe330f9eaa663a67af836e4d1be5062339455b771777",
            "ev:9f9afff67aa5c984d8bf9fd449e0dbc38222603692e14e67084eafbf40351c78",
            "ev:f741f556ff3bcb22bf65b6a7c7b5b809ca8d9ce984e28a83d0967674c4f326dd",
            "ev:fc46390ad8f5e9fceb97dff255e4b4e9564e48be2aada1fd59db41e2323c8b6c"
          ],
          "fact_ids": [
            "fact:fe073f6a2071a2e7f38eb01d78a1acc1f580375c3aa5a3fc36ab9d6245d1b94d"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn."
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
