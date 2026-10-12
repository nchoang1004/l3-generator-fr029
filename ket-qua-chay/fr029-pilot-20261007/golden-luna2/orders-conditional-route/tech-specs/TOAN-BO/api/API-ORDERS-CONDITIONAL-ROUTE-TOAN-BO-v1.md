---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:7b6f298a2c35f3846bc4c1802d935aed204242e0699034f879464decf1588c59"
owner_component_id: "cmp_c1deda8b0277a99ac73996586fe6abe3aacad705fc5970e87158d554efe8af6c"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v7"
fact_ids: ["fact:3c1d708cc3936024b1ac63c7156cb70d6faa2f07ffe5b353f6284d65d1415b72", "fact:8b890fd0e166431784ba13fc238e20dcab1ec02a50d0e774b76ba9ffe0245ff1"]
evidence_ids: ["ev:199d82105f420634d240bf26b84f7bd1faf87c58ea6e2a8759f4a0323e342fe0", "ev:3373b44e736c6c22a691daa9e7d49f8a573690e4566bfd7332819cb7367520ed", "ev:44850975d8fe913bc9fd4bf960dcea4ca24ee5451c6339b52b3a45dfdf296ae7", "ev:6aa86d2f747c3cf0325ca656b9aaec49dc6ae755a9e5ab089196bc44ccda2e89", "ev:bdba230aff4132dfa3f30800ef42bb891fc70095854b6e1d788693fad8644396", "ev:c3a7dabd4c61eb1ed7d601e1e89d919adaf5e239b61be64b5625f8055d78ab9c", "ev:ed5154f3d546c5110425ee9818cb5b91ea3ea17ffdd06d8bee85f88bf361789f", "ev:f705273fcdb5bf545a69e8e82ba6d10f01ca5904cc763451df4886371ceab3b6"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /api/v1/orders | order (body, OrderInput, bắt buộc) | OrderInput | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Mã nguồn không thể hiện cơ chế xác thực cho route này. | inferred (fastapi.default_status_200, fastapi.json_body_media) / partial | `f:3c1d708c` |


## Model

### OrderInput (request)

Fact `f:8b890fd0` · exact / full · khai ở schemas.py:3

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| product | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:main.py:6 | POST | /api/v1/orders | routes.py::create_order_endpoint | fact:8b890fd0e166431784ba13fc238e20dcab1ec02a50d0e774b76ba9ffe0245ff1 | (rỗng) | 200 | dependency: get_db; auth: unknown — Mã nguồn không thể hiện cơ chế xác thực cho route này. | `fact:3c1d708cc3936024b1ac63c7156cb70d6faa2f07ffe5b353f6284d65d1415b72` | `ev:f705273fcdb5bf545a69e8e82ba6d10f01ca5904cc763451df4886371ceab3b6` (main.py:6), `ev:44850975d8fe913bc9fd4bf960dcea4ca24ee5451c6339b52b3a45dfdf296ae7` (main.py:8), `ev:c3a7dabd4c61eb1ed7d601e1e89d919adaf5e239b61be64b5625f8055d78ab9c` (routes.py:7), `ev:3373b44e736c6c22a691daa9e7d49f8a573690e4566bfd7332819cb7367520ed` (routes.py:9), `ev:bdba230aff4132dfa3f30800ef42bb891fc70095854b6e1d788693fad8644396` (routes.py:9-10), `ev:ed5154f3d546c5110425ee9818cb5b91ea3ea17ffdd06d8bee85f88bf361789f` (routes.py:10) | inferred | partial |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| OrderInput | fact:8b890fd0e166431784ba13fc238e20dcab1ec02a50d0e774b76ba9ffe0245ff1 | schemas.py:3 |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "OrderInput_8b890fd0": {
        "properties": {
          "product": {
            "type": "string"
          }
        },
        "required": [
          "product"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:8b890fd0e166431784ba13fc238e20dcab1ec02a50d0e774b76ba9ffe0245ff1"
          ]
        }
      }
    }
  },
  "info": {
    "title": "Toàn bộ",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/api/v1/orders": {
      "post": {
        "operationId": "op_3c1d708cc3936024",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/OrderInput_8b890fd0"
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
          "application_id": "app:main.py:6",
          "evidence_ids": [
            "ev:3373b44e736c6c22a691daa9e7d49f8a573690e4566bfd7332819cb7367520ed",
            "ev:44850975d8fe913bc9fd4bf960dcea4ca24ee5451c6339b52b3a45dfdf296ae7",
            "ev:bdba230aff4132dfa3f30800ef42bb891fc70095854b6e1d788693fad8644396",
            "ev:c3a7dabd4c61eb1ed7d601e1e89d919adaf5e239b61be64b5625f8055d78ab9c",
            "ev:ed5154f3d546c5110425ee9818cb5b91ea3ea17ffdd06d8bee85f88bf361789f",
            "ev:f705273fcdb5bf545a69e8e82ba6d10f01ca5904cc763451df4886371ceab3b6"
          ],
          "fact_ids": [
            "fact:3c1d708cc3936024b1ac63c7156cb70d6faa2f07ffe5b353f6284d65d1415b72"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Mã nguồn không thể hiện cơ chế xác thực cho route này."
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
