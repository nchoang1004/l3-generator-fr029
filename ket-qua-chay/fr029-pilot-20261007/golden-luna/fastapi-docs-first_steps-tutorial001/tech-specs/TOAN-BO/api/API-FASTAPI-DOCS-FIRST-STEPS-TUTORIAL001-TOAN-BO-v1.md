---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:39d57520f2ce67ae46351df4d0a16628f7b70c21ff0dd7a8e3ceaf3592a8530d"
owner_component_id: "cmp_eba15a45af07e03907f351976a154e76703a8570c26ad6a0fd19e7917f225f34"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v5"
fact_ids: ["fact:85ed7e35f34b08540bc5ecbefa79a07c7c94383673a23559287c65db9c65162b"]
evidence_ids: ["ev:8022221a089dfc94c1f0715ddbf4b04e3c1c7d220154af60be48171c02a4c92d", "ev:901cca1b8c753dede9db4116d3da940037040a44d4fbdc163abbcef7f0c1c819", "ev:e59c0c4cc7e737f269a2532cffcdb7a84d1a18cff207bcf50333c4716edfe3d3"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | / | (không có) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn của route. | inferred (fastapi.default_status_200) / partial | `f:85ed7e35` |


## Model

Không route nào có request/response model đã xác định.

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:first_steps/tutorial001_py310.py:3 | GET | / | first_steps/tutorial001_py310.py::root | (rỗng) | (rỗng) | 200 | unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn của route. | `fact:85ed7e35f34b08540bc5ecbefa79a07c7c94383673a23559287c65db9c65162b` | `ev:8022221a089dfc94c1f0715ddbf4b04e3c1c7d220154af60be48171c02a4c92d` (first_steps/tutorial001_py310.py:3), `ev:901cca1b8c753dede9db4116d3da940037040a44d4fbdc163abbcef7f0c1c819` (first_steps/tutorial001_py310.py:6), `ev:e59c0c4cc7e737f269a2532cffcdb7a84d1a18cff207bcf50333c4716edfe3d3` (first_steps/tutorial001_py310.py:6-7) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Toàn bộ",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/": {
      "get": {
        "operationId": "op_85ed7e35f34b0854",
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:first_steps/tutorial001_py310.py:3",
          "evidence_ids": [
            "ev:8022221a089dfc94c1f0715ddbf4b04e3c1c7d220154af60be48171c02a4c92d",
            "ev:901cca1b8c753dede9db4116d3da940037040a44d4fbdc163abbcef7f0c1c819",
            "ev:e59c0c4cc7e737f269a2532cffcdb7a84d1a18cff207bcf50333c4716edfe3d3"
          ],
          "fact_ids": [
            "fact:85ed7e35f34b08540bc5ecbefa79a07c7c94383673a23559287c65db9c65162b"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn của route."
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
