---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:c76102dcd74977697e638089e01037e517bb8e4d9a039f63ffbf8bf79eaca9b7"
owner_component_id: "cmp_ada04a52bd6d2d972e19a012b6d08a295db5c7c1f556554b45478d88da58d50d"
owner_component: "Hệ thống"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v13"
fact_ids: ["fact:17a03a98af07952b6ecb1772989e4e5eaa25ae9a902343ca872c91cc253ea3b0", "fact:3f4b188ef3319eb777eb38d2ad611ff56e7da8dce5c2a21e2e5643b8656a7bb1", "fact:c30ae2aa8ca0cbe9ddfd6cff087f8715416f1052336c411799b4ac705b4e5087"]
evidence_ids: ["ev:2066b89061d0fba8bbe891ade78fb9f9577711c1da0e6760254ee081ff9d8c32", "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8", "ev:589b0b62a62d800481c87f8fe7e2aca182eeb71335e4cd496eeb95528c0941cf", "ev:5a3d893d0c5f01a4cbff278e597934b7272b8f2db69e89150e3b9fe3b815bdc5", "ev:877b82fa9f0768547d2f0e233fc84ddfc51601ada7669d0ec14047b689f8413a", "ev:925c7807419f3127759872e0cb964a3cd2e3a94b8ed4c47165d7a5dd423526b9", "ev:ac8fc39bd0e71687a0207fd260c46980e0b3218e86bf43351e2848fe505a9ab6", "ev:bea6d946f68ce345700aa69747286536357b61d7576f1790cc9a8f3b0745dfe1", "ev:e009bd865149d34df2af59bc4de81941c0f0cdef4d8fecc6c705ad0d275d3359"]
---
# API — Hệ thống

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /internal/status/ping | (không có) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn đã đọc. | inferred (fastapi.default_status_200) / partial | `f:3f4b188e` |
| GET | /public/status/ping | (không có) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn đã đọc. | inferred (fastapi.default_status_200) / partial | `f:17a03a98` |
| GET | unknown — Giá trị ADMIN_PREFIX lấy trực tiếp từ biến môi trường và không có giá trị mặc định trong mã nguồn. (hậu tố đã biết: /stats) | (không có) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn đã đọc. | inferred (fastapi.default_status_200) / partial | `f:c30ae2aa` |


## Model

Không route nào có request/response model đã xác định.

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:12 | GET | /internal/status/ping | app/api/health.py::ping | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn đã đọc. | `fact:3f4b188ef3319eb777eb38d2ad611ff56e7da8dce5c2a21e2e5643b8656a7bb1` | `ev:e009bd865149d34df2af59bc4de81941c0f0cdef4d8fecc6c705ad0d275d3359` (app/api/health.py:3), `ev:589b0b62a62d800481c87f8fe7e2aca182eeb71335e4cd496eeb95528c0941cf` (app/api/health.py:6-7), `ev:877b82fa9f0768547d2f0e233fc84ddfc51601ada7669d0ec14047b689f8413a` (app/api/health.py:6), `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12), `ev:ac8fc39bd0e71687a0207fd260c46980e0b3218e86bf43351e2848fe505a9ab6` (app/main.py:20) | inferred | partial |
| app:app/main.py:12 | GET | /public/status/ping | app/api/health.py::ping | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn đã đọc. | `fact:17a03a98af07952b6ecb1772989e4e5eaa25ae9a902343ca872c91cc253ea3b0` | `ev:e009bd865149d34df2af59bc4de81941c0f0cdef4d8fecc6c705ad0d275d3359` (app/api/health.py:3), `ev:589b0b62a62d800481c87f8fe7e2aca182eeb71335e4cd496eeb95528c0941cf` (app/api/health.py:6-7), `ev:877b82fa9f0768547d2f0e233fc84ddfc51601ada7669d0ec14047b689f8413a` (app/api/health.py:6), `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12), `ev:bea6d946f68ce345700aa69747286536357b61d7576f1790cc9a8f3b0745dfe1` (app/main.py:19) | inferred | partial |
| app:app/main.py:12 | GET | unknown — Giá trị ADMIN_PREFIX lấy trực tiếp từ biến môi trường và không có giá trị mặc định trong mã nguồn. (hậu tố đã biết: /stats) | app/api/admin.py::admin_stats | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn đã đọc. | `fact:c30ae2aa8ca0cbe9ddfd6cff087f8715416f1052336c411799b4ac705b4e5087` | `ev:2066b89061d0fba8bbe891ade78fb9f9577711c1da0e6760254ee081ff9d8c32` (app/api/admin.py:6), `ev:5a3d893d0c5f01a4cbff278e597934b7272b8f2db69e89150e3b9fe3b815bdc5` (app/api/admin.py:6-7), `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12), `ev:925c7807419f3127759872e0cb964a3cd2e3a94b8ed4c47165d7a5dd423526b9` (app/main.py:22) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Hệ thống",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/internal/status/ping": {
      "get": {
        "operationId": "op_3f4b188ef3319eb7",
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8",
            "ev:589b0b62a62d800481c87f8fe7e2aca182eeb71335e4cd496eeb95528c0941cf",
            "ev:877b82fa9f0768547d2f0e233fc84ddfc51601ada7669d0ec14047b689f8413a",
            "ev:ac8fc39bd0e71687a0207fd260c46980e0b3218e86bf43351e2848fe505a9ab6",
            "ev:e009bd865149d34df2af59bc4de81941c0f0cdef4d8fecc6c705ad0d275d3359"
          ],
          "fact_ids": [
            "fact:3f4b188ef3319eb777eb38d2ad611ff56e7da8dce5c2a21e2e5643b8656a7bb1"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo trong mã nguồn đã đọc."
            }
          ]
        }
      }
    },
    "/public/status/ping": {
      "get": {
        "operationId": "op_17a03a98af07952b",
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8",
            "ev:589b0b62a62d800481c87f8fe7e2aca182eeb71335e4cd496eeb95528c0941cf",
            "ev:877b82fa9f0768547d2f0e233fc84ddfc51601ada7669d0ec14047b689f8413a",
            "ev:bea6d946f68ce345700aa69747286536357b61d7576f1790cc9a8f3b0745dfe1",
            "ev:e009bd865149d34df2af59bc4de81941c0f0cdef4d8fecc6c705ad0d275d3359"
          ],
          "fact_ids": [
            "fact:17a03a98af07952b6ecb1772989e4e5eaa25ae9a902343ca872c91cc253ea3b0"
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
    "omitted_operations": [
      {
        "fact_id": "fact:c30ae2aa8ca0cbe9ddfd6cff087f8715416f1052336c411799b4ac705b4e5087",
        "reason": "Path đầy đủ chưa biết"
      }
    ]
  }
}
```

Bỏ khỏi khối OpenAPI:

- Bỏ khỏi OpenAPI: `fact:c30ae2aa8ca0cbe9ddfd6cff087f8715416f1052336c411799b4ac705b4e5087` (GET /stats) — Path đầy đủ chưa biết
