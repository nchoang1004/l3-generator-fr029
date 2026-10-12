---
generated: true
non_normative: true
snapshot_id: "snap:f4964f64b825d8af3f7a92e49254c5e6c506822efac23974978c5d32c175a886"
owner_component_id: "cmp_26389ab80ab07e415ca6fce29c0193d3fd1659902ce3fe0ddf2d916fb890a516"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:143cf8539f899564c875407bc3595895cd565c42af719c8bc90d3c867028eae6"]
evidence_ids: ["ev:6b3be780417a42c84e5cafb76c3045603a0c1c05297e5a77ace9a5a8bc442487", "ev:6d5479b207165bb6b796f1ce63418176d61786d6a4b387f58e8a85abd947ee35", "ev:913efefc1a5711c0cb0223e268556f83519326ce174a07b21b5fd8d84e399d0c", "ev:c4253ca4abb1b57de8d445785cddce796440608b395741fa1e6f76ac227d14a4", "ev:c7fe15730653208456a05625d96ce0ab571e143ab20000a6a9d406e3c508767b"]
---
# API — Cửa hàng API

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py::app | GET | /items | app.main.list_items | (rỗng) | (rỗng) | 200 | unknown — Không thấy dependency; không kết luận route công khai | `fact:143cf8539f899564c875407bc3595895cd565c42af719c8bc90d3c867028eae6` | `ev:c4253ca4abb1b57de8d445785cddce796440608b395741fa1e6f76ac227d14a4` (app/main.py:5), `ev:6b3be780417a42c84e5cafb76c3045603a0c1c05297e5a77ace9a5a8bc442487` (app/main.py:8), `ev:6d5479b207165bb6b796f1ce63418176d61786d6a4b387f58e8a85abd947ee35` (app/main.py:8), `ev:913efefc1a5711c0cb0223e268556f83519326ce174a07b21b5fd8d84e399d0c` (app/main.py:8), `ev:c7fe15730653208456a05625d96ce0ab571e143ab20000a6a9d406e3c508767b` (app/main.py:8-9) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Cửa hàng API",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/items": {
      "get": {
        "operationId": "op_143cf8539f899564",
        "responses": {
          "200": {
            "description": "Status code lấy từ source; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py::app",
          "evidence_ids": [
            "ev:6b3be780417a42c84e5cafb76c3045603a0c1c05297e5a77ace9a5a8bc442487",
            "ev:6d5479b207165bb6b796f1ce63418176d61786d6a4b387f58e8a85abd947ee35",
            "ev:913efefc1a5711c0cb0223e268556f83519326ce174a07b21b5fd8d84e399d0c",
            "ev:c4253ca4abb1b57de8d445785cddce796440608b395741fa1e6f76ac227d14a4",
            "ev:c7fe15730653208456a05625d96ce0ab571e143ab20000a6a9d406e3c508767b"
          ],
          "fact_ids": [
            "fact:143cf8539f899564c875407bc3595895cd565c42af719c8bc90d3c867028eae6"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy dependency; không kết luận route công khai"
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
