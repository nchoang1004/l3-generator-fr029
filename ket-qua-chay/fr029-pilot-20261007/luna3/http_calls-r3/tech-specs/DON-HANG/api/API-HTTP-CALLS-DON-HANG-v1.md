---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:e834022c8ce97e51ed00b4473d50845bf3d6339716cd565a545bc0ea2d0c2d8b"
owner_component_id: "cmp_b376b0d6812f5b20c563cc7e5a0ada664cb792747d57e5a28e7d4f0a69ff2e4d"
owner_component: "Đơn hàng"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v5"
fact_ids: ["fact:263cdf1408cf1e262263861ef100291b518b15b12a617aae761a4f6617ffc3ee", "fact:60fe6aaa7c9255f19c327f84c122194013051e4cb215fb17ed03ab69b3c3eec2", "fact:eb729d3ddf8880c03da005b61dfd0e99b867c151109cd2f00ee54e303ea8ed35"]
evidence_ids: ["ev:2f65220c081887c27b29860daa976461b7306ddfc9682907ae7254465fe6a46b", "ev:3484ecb0d9c6093f4d21f771b1ba91fc8f60a2a83ca7722defed18c7ff26bdc3", "ev:4d7527507db36b1f37f6e79aa9783f020a0058980c40340f9ef4dd0ee278922f", "ev:53e034381cb18787911cba7c5a55bde3b6ca512db1c59d056fedb1e0b70e92d7", "ev:9aa2773d217e71863454a3628ab991c79e3199e4d8c440cfb9da811d4761aa94", "ev:ade4e2d3b8a02420b977ee888e12127d40f6243dc2383efd5cd30d948c89b3e1", "ev:c16bc6a92ad278d863cd86cb2e8400afdbfa720558ed3d067d0113a0c1a7a695", "ev:c468e75d15ccc087a9911e9c392a35cffeef8f4c67fb6478630bcda0c90e4c2f", "ev:e0815ed5f19a47854bbf175b626806b0b0a96894895b8488fa55681087918874"]
---
# API — Đơn hàng

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /orders/{order_id} | order_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Không thấy khai báo hoặc cơ chế xác thực trong mã nguồn của route. | inferred (fastapi.default_status_200) / partial | `f:263cdf14` |
| POST | /orders/{order_id}/reserve | order_id (path, integer, bắt buộc); sku (query, string, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Không thấy khai báo hoặc cơ chế xác thực trong mã nguồn của route. | inferred (fastapi.default_status_200, fastapi.scalar_param_query) / partial | `f:60fe6aaa` |
| POST | /rates/refresh | (không có) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Không thấy khai báo hoặc cơ chế xác thực trong mã nguồn của route. | inferred (fastapi.default_status_200) / partial | `f:eb729d3d` |


## Model

Không route nào có request/response model đã xác định.

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:5 | GET | /orders/{order_id} | app/routes.py::get_order | (rỗng) | (rỗng) | 200 | unknown — Không thấy khai báo hoặc cơ chế xác thực trong mã nguồn của route. | `fact:263cdf1408cf1e262263861ef100291b518b15b12a617aae761a4f6617ffc3ee` | `ev:c16bc6a92ad278d863cd86cb2e8400afdbfa720558ed3d067d0113a0c1a7a695` (app/main.py:5), `ev:4d7527507db36b1f37f6e79aa9783f020a0058980c40340f9ef4dd0ee278922f` (app/routes.py:10-11), `ev:c468e75d15ccc087a9911e9c392a35cffeef8f4c67fb6478630bcda0c90e4c2f` (app/routes.py:10), `ev:ade4e2d3b8a02420b977ee888e12127d40f6243dc2383efd5cd30d948c89b3e1` (app/routes.py:11) | inferred | partial |
| app:app/main.py:5 | POST | /orders/{order_id}/reserve | app/routes.py::reserve | (rỗng) | (rỗng) | 200 | unknown — Không thấy khai báo hoặc cơ chế xác thực trong mã nguồn của route. | `fact:60fe6aaa7c9255f19c327f84c122194013051e4cb215fb17ed03ab69b3c3eec2` | `ev:c16bc6a92ad278d863cd86cb2e8400afdbfa720558ed3d067d0113a0c1a7a695` (app/main.py:5), `ev:2f65220c081887c27b29860daa976461b7306ddfc9682907ae7254465fe6a46b` (app/routes.py:21-22), `ev:e0815ed5f19a47854bbf175b626806b0b0a96894895b8488fa55681087918874` (app/routes.py:21), `ev:9aa2773d217e71863454a3628ab991c79e3199e4d8c440cfb9da811d4761aa94` (app/routes.py:22) | inferred | partial |
| app:app/main.py:5 | POST | /rates/refresh | app/routes.py::refresh_rates | (rỗng) | (rỗng) | 200 | unknown — Không thấy khai báo hoặc cơ chế xác thực trong mã nguồn của route. | `fact:eb729d3ddf8880c03da005b61dfd0e99b867c151109cd2f00ee54e303ea8ed35` | `ev:c16bc6a92ad278d863cd86cb2e8400afdbfa720558ed3d067d0113a0c1a7a695` (app/main.py:5), `ev:3484ecb0d9c6093f4d21f771b1ba91fc8f60a2a83ca7722defed18c7ff26bdc3` (app/routes.py:16), `ev:53e034381cb18787911cba7c5a55bde3b6ca512db1c59d056fedb1e0b70e92d7` (app/routes.py:16-17) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Đơn hàng",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/orders/{order_id}": {
      "get": {
        "operationId": "op_263cdf1408cf1e26",
        "parameters": [
          {
            "in": "path",
            "name": "order_id",
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
          "application_id": "app:app/main.py:5",
          "evidence_ids": [
            "ev:4d7527507db36b1f37f6e79aa9783f020a0058980c40340f9ef4dd0ee278922f",
            "ev:ade4e2d3b8a02420b977ee888e12127d40f6243dc2383efd5cd30d948c89b3e1",
            "ev:c16bc6a92ad278d863cd86cb2e8400afdbfa720558ed3d067d0113a0c1a7a695",
            "ev:c468e75d15ccc087a9911e9c392a35cffeef8f4c67fb6478630bcda0c90e4c2f"
          ],
          "fact_ids": [
            "fact:263cdf1408cf1e262263861ef100291b518b15b12a617aae761a4f6617ffc3ee"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy khai báo hoặc cơ chế xác thực trong mã nguồn của route."
            }
          ]
        }
      }
    },
    "/orders/{order_id}/reserve": {
      "post": {
        "operationId": "op_60fe6aaa7c9255f1",
        "parameters": [
          {
            "in": "path",
            "name": "order_id",
            "required": true,
            "schema": {
              "type": "integer"
            }
          },
          {
            "in": "query",
            "name": "sku",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:5",
          "evidence_ids": [
            "ev:2f65220c081887c27b29860daa976461b7306ddfc9682907ae7254465fe6a46b",
            "ev:9aa2773d217e71863454a3628ab991c79e3199e4d8c440cfb9da811d4761aa94",
            "ev:c16bc6a92ad278d863cd86cb2e8400afdbfa720558ed3d067d0113a0c1a7a695",
            "ev:e0815ed5f19a47854bbf175b626806b0b0a96894895b8488fa55681087918874"
          ],
          "fact_ids": [
            "fact:60fe6aaa7c9255f19c327f84c122194013051e4cb215fb17ed03ab69b3c3eec2"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy khai báo hoặc cơ chế xác thực trong mã nguồn của route."
            }
          ]
        }
      }
    },
    "/rates/refresh": {
      "post": {
        "operationId": "op_eb729d3ddf8880c0",
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:5",
          "evidence_ids": [
            "ev:3484ecb0d9c6093f4d21f771b1ba91fc8f60a2a83ca7722defed18c7ff26bdc3",
            "ev:53e034381cb18787911cba7c5a55bde3b6ca512db1c59d056fedb1e0b70e92d7",
            "ev:c16bc6a92ad278d863cd86cb2e8400afdbfa720558ed3d067d0113a0c1a7a695"
          ],
          "fact_ids": [
            "fact:eb729d3ddf8880c03da005b61dfd0e99b867c151109cd2f00ee54e303ea8ed35"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy khai báo hoặc cơ chế xác thực trong mã nguồn của route."
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
