---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:c76102dcd74977697e638089e01037e517bb8e4d9a039f63ffbf8bf79eaca9b7"
owner_component_id: "cmp_1f1639ef081a6145fe0a8571d0b65183700c16a938a5b059818eef8ce2811374"
owner_component: "Khởi động"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v13"
fact_ids: ["fact:59424527ee1aeb762f1fb7ee77a332c12806914bdb70de7d86dafdf22f87f6ba"]
evidence_ids: ["ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8", "ev:5fcd1690c58c5fab289c3b8f02b276d9580e876207fb8667db8629815f5795b7", "ev:c8523e8868fd875c225d0875a04fa3af9a61a4f6a3e39fc5db193c6eb48bcda1"]
---
# API — Khởi động

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | / | (không có) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn đã đọc. | inferred (fastapi.default_status_200) / partial | `f:59424527` |


## Model

Không route nào có request/response model đã xác định.

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:12 | GET | / | app/main.py::root | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn đã đọc. | `fact:59424527ee1aeb762f1fb7ee77a332c12806914bdb70de7d86dafdf22f87f6ba` | `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12), `ev:5fcd1690c58c5fab289c3b8f02b276d9580e876207fb8667db8629815f5795b7` (app/main.py:14-15), `ev:c8523e8868fd875c225d0875a04fa3af9a61a4f6a3e39fc5db193c6eb48bcda1` (app/main.py:14) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Khởi động",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/": {
      "get": {
        "operationId": "op_59424527ee1aeb76",
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8",
            "ev:5fcd1690c58c5fab289c3b8f02b276d9580e876207fb8667db8629815f5795b7",
            "ev:c8523e8868fd875c225d0875a04fa3af9a61a4f6a3e39fc5db193c6eb48bcda1"
          ],
          "fact_ids": [
            "fact:59424527ee1aeb762f1fb7ee77a332c12806914bdb70de7d86dafdf22f87f6ba"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn đã đọc."
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
