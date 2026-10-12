---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:e834022c8ce97e51ed00b4473d50845bf3d6339716cd565a545bc0ea2d0c2d8b"
owner_component_id: "cmp_b376b0d6812f5b20c563cc7e5a0ada664cb792747d57e5a28e7d4f0a69ff2e4d"
owner_component: "Đơn hàng"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v8"
fact_ids: ["fact:941aa7f872cb44c888a2ba2c44b679073e5088f770494f9a6a70b60a795d6947", "fact:ac4c59477e710cb5b12cf769628898d4bf32b32b793e820a6845e1a387434cc0", "fact:d3740d81ce2947a20ffba36a7b9f979713e0780d189685c219fb1b5faea4be78"]
evidence_ids: ["ev:2f65220c081887c27b29860daa976461b7306ddfc9682907ae7254465fe6a46b", "ev:3484ecb0d9c6093f4d21f771b1ba91fc8f60a2a83ca7722defed18c7ff26bdc3", "ev:4d7527507db36b1f37f6e79aa9783f020a0058980c40340f9ef4dd0ee278922f", "ev:53e034381cb18787911cba7c5a55bde3b6ca512db1c59d056fedb1e0b70e92d7", "ev:9aa2773d217e71863454a3628ab991c79e3199e4d8c440cfb9da811d4761aa94", "ev:ade4e2d3b8a02420b977ee888e12127d40f6243dc2383efd5cd30d948c89b3e1", "ev:c16bc6a92ad278d863cd86cb2e8400afdbfa720558ed3d067d0113a0c1a7a695", "ev:c468e75d15ccc087a9911e9c392a35cffeef8f4c67fb6478630bcda0c90e4c2f", "ev:dcfeeab0c499e3a153765c3055d112b3f152d80978218bfd823a2d321cad9810", "ev:e0815ed5f19a47854bbf175b626806b0b0a96894895b8488fa55681087918874", "ev:fa789a428eb37f575ae3585b38bdec66d23054bbb39c97774ff020acaccb075d"]
---
# API — Đơn hàng

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /orders/{order_id} | order_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200) / partial | `f:ac4c5947` |
| POST | /orders/{order_id}/reserve | order_id (path, integer, bắt buộc); sku (query, string, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200, fastapi.scalar_param_query) / partial | `f:941aa7f8` |
| POST | /rates/refresh | (không có) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200) / partial | `f:d3740d81` |


## Model

Không route nào có request/response model đã xác định.

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:5 | GET | /orders/{order_id} | app/routes.py::get_order | (rỗng) | (rỗng) | 200 | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:ac4c59477e710cb5b12cf769628898d4bf32b32b793e820a6845e1a387434cc0` | `ev:c16bc6a92ad278d863cd86cb2e8400afdbfa720558ed3d067d0113a0c1a7a695` (app/main.py:5), `ev:dcfeeab0c499e3a153765c3055d112b3f152d80978218bfd823a2d321cad9810` (app/main.py:6), `ev:fa789a428eb37f575ae3585b38bdec66d23054bbb39c97774ff020acaccb075d` (app/routes.py:7), `ev:4d7527507db36b1f37f6e79aa9783f020a0058980c40340f9ef4dd0ee278922f` (app/routes.py:10-11), `ev:c468e75d15ccc087a9911e9c392a35cffeef8f4c67fb6478630bcda0c90e4c2f` (app/routes.py:10), `ev:ade4e2d3b8a02420b977ee888e12127d40f6243dc2383efd5cd30d948c89b3e1` (app/routes.py:11) | inferred | partial |
| app:app/main.py:5 | POST | /orders/{order_id}/reserve | app/routes.py::reserve | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:941aa7f872cb44c888a2ba2c44b679073e5088f770494f9a6a70b60a795d6947` | `ev:c16bc6a92ad278d863cd86cb2e8400afdbfa720558ed3d067d0113a0c1a7a695` (app/main.py:5), `ev:dcfeeab0c499e3a153765c3055d112b3f152d80978218bfd823a2d321cad9810` (app/main.py:6), `ev:fa789a428eb37f575ae3585b38bdec66d23054bbb39c97774ff020acaccb075d` (app/routes.py:7), `ev:2f65220c081887c27b29860daa976461b7306ddfc9682907ae7254465fe6a46b` (app/routes.py:21-22), `ev:e0815ed5f19a47854bbf175b626806b0b0a96894895b8488fa55681087918874` (app/routes.py:21), `ev:9aa2773d217e71863454a3628ab991c79e3199e4d8c440cfb9da811d4761aa94` (app/routes.py:22) | inferred | partial |
| app:app/main.py:5 | POST | /rates/refresh | app/routes.py::refresh_rates | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:d3740d81ce2947a20ffba36a7b9f979713e0780d189685c219fb1b5faea4be78` | `ev:c16bc6a92ad278d863cd86cb2e8400afdbfa720558ed3d067d0113a0c1a7a695` (app/main.py:5), `ev:dcfeeab0c499e3a153765c3055d112b3f152d80978218bfd823a2d321cad9810` (app/main.py:6), `ev:fa789a428eb37f575ae3585b38bdec66d23054bbb39c97774ff020acaccb075d` (app/routes.py:7), `ev:3484ecb0d9c6093f4d21f771b1ba91fc8f60a2a83ca7722defed18c7ff26bdc3` (app/routes.py:16), `ev:53e034381cb18787911cba7c5a55bde3b6ca512db1c59d056fedb1e0b70e92d7` (app/routes.py:16-17) | inferred | partial |

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
        "operationId": "op_ac4c59477e710cb5",
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
            "ev:c468e75d15ccc087a9911e9c392a35cffeef8f4c67fb6478630bcda0c90e4c2f",
            "ev:dcfeeab0c499e3a153765c3055d112b3f152d80978218bfd823a2d321cad9810",
            "ev:fa789a428eb37f575ae3585b38bdec66d23054bbb39c97774ff020acaccb075d"
          ],
          "fact_ids": [
            "fact:ac4c59477e710cb5b12cf769628898d4bf32b32b793e820a6845e1a387434cc0"
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
    "/orders/{order_id}/reserve": {
      "post": {
        "operationId": "op_941aa7f872cb44c8",
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
            "ev:dcfeeab0c499e3a153765c3055d112b3f152d80978218bfd823a2d321cad9810",
            "ev:e0815ed5f19a47854bbf175b626806b0b0a96894895b8488fa55681087918874",
            "ev:fa789a428eb37f575ae3585b38bdec66d23054bbb39c97774ff020acaccb075d"
          ],
          "fact_ids": [
            "fact:941aa7f872cb44c888a2ba2c44b679073e5088f770494f9a6a70b60a795d6947"
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
    "/rates/refresh": {
      "post": {
        "operationId": "op_d3740d81ce2947a2",
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
            "ev:c16bc6a92ad278d863cd86cb2e8400afdbfa720558ed3d067d0113a0c1a7a695",
            "ev:dcfeeab0c499e3a153765c3055d112b3f152d80978218bfd823a2d321cad9810",
            "ev:fa789a428eb37f575ae3585b38bdec66d23054bbb39c97774ff020acaccb075d"
          ],
          "fact_ids": [
            "fact:d3740d81ce2947a20ffba36a7b9f979713e0780d189685c219fb1b5faea4be78"
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
