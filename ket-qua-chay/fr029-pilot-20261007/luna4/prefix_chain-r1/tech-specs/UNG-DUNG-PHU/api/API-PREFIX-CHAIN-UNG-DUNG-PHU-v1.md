---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:c76102dcd74977697e638089e01037e517bb8e4d9a039f63ffbf8bf79eaca9b7"
owner_component_id: "cmp_09a5fa6ed4ea29f637e680183f8995ade80d110b56593354b4ef14836d68988b"
owner_component: "Ứng dụng phụ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v6"
fact_ids: ["fact:a68868b8adf561f4863f7b66b0ee910b8025e0a8553552ff268ebbbbbe2a79f2"]
evidence_ids: ["ev:2464987157fe9367a3011e85630f4b2dcfc37f45ec179265513813e9d4993739", "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8", "ev:3de86a11cda63cb05a2e59c7b9688e8a2f8c0d3bbffa32486e244758a407bab4", "ev:a73ea18e2591070cf1d4cb9f66ef21734d476baf4741516fdc769bd937d3d9d5"]
---
# API — Ứng dụng phụ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /sub/hello | (không có) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Chưa thấy cơ chế xác thực trong mã nguồn đã đọc. | inferred (fastapi.default_status_200) / partial | `f:a68868b8` |


## Model

Không route nào có request/response model đã xác định.

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:12 | GET | /sub/hello | app/sub.py::sub_hello | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Chưa thấy cơ chế xác thực trong mã nguồn đã đọc. | `fact:a68868b8adf561f4863f7b66b0ee910b8025e0a8553552ff268ebbbbbe2a79f2` | `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12), `ev:a73ea18e2591070cf1d4cb9f66ef21734d476baf4741516fdc769bd937d3d9d5` (app/main.py:23), `ev:2464987157fe9367a3011e85630f4b2dcfc37f45ec179265513813e9d4993739` (app/sub.py:6), `ev:3de86a11cda63cb05a2e59c7b9688e8a2f8c0d3bbffa32486e244758a407bab4` (app/sub.py:6-7) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Ứng dụng phụ",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/sub/hello": {
      "get": {
        "operationId": "op_a68868b8adf561f4",
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:2464987157fe9367a3011e85630f4b2dcfc37f45ec179265513813e9d4993739",
            "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8",
            "ev:3de86a11cda63cb05a2e59c7b9688e8a2f8c0d3bbffa32486e244758a407bab4",
            "ev:a73ea18e2591070cf1d4cb9f66ef21734d476baf4741516fdc769bd937d3d9d5"
          ],
          "fact_ids": [
            "fact:a68868b8adf561f4863f7b66b0ee910b8025e0a8553552ff268ebbbbbe2a79f2"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Chưa thấy cơ chế xác thực trong mã nguồn đã đọc."
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
