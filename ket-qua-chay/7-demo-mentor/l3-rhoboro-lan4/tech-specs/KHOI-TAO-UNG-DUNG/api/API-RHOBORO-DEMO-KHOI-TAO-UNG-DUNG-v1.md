---
generated: true
non_normative: true
snapshot_id: "snap:c1495361276c6c8cd263abcb7919dea2d99441c993412393b1b5bc40363054af"
owner_component_id: "cmp_e0eec3530f42bf8364ab7755b22c499e6783365e9f44d06510d7e5a8998bbd68"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:c85e7bbfbc5387fef3868da123d3023bb10305b2b0ab22fd62e6a7b7260b5666"]
evidence_ids: ["ev:233b5f9dc35a8e0e46da0f972f60a15344596cf806b7d02df6e74d43f3f8b8f1", "ev:8f76536231d78580f9246f358d591383dc793f013b291c8eb2c6fdea9ec94ea9", "ev:9c27354fbc27515aebfa59f55efe077972e9dd6620969475d2af7cb5428cb1ba", "ev:d420cf3a86deb4d7129a53dd0e7f89f397cb928b2ca6c033c56c43923c85cf09"]
---
# API — Khởi tạo ứng dụng

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | / | (không có) | (không có) | unknown — Response model không phải Pydantic model trong repo: JSONResponse | 200 (suy theo fastapi-status-default-v1) | unknown — Không thấy dependency; không kết luận route công khai | inferred / partial | `f:c85e7bbf` |

## Model

Không route nào có request/response model đã xác định.

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py::app | GET | / | app.main.health | (rỗng) | unknown — Response model không phải Pydantic model trong repo: JSONResponse | 200 | unknown — Không thấy dependency; không kết luận route công khai | `fact:c85e7bbfbc5387fef3868da123d3023bb10305b2b0ab22fd62e6a7b7260b5666` | `ev:8f76536231d78580f9246f358d591383dc793f013b291c8eb2c6fdea9ec94ea9` (app/main.py:6), `ev:233b5f9dc35a8e0e46da0f972f60a15344596cf806b7d02df6e74d43f3f8b8f1` (app/main.py:11), `ev:9c27354fbc27515aebfa59f55efe077972e9dd6620969475d2af7cb5428cb1ba` (app/main.py:11), `ev:d420cf3a86deb4d7129a53dd0e7f89f397cb928b2ca6c033c56c43923c85cf09` (app/main.py:11-12) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Khởi tạo ứng dụng",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/": {
      "get": {
        "operationId": "op_c85e7bbfbc5387fe",
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi-status-default-v1; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py::app",
          "evidence_ids": [
            "ev:233b5f9dc35a8e0e46da0f972f60a15344596cf806b7d02df6e74d43f3f8b8f1",
            "ev:8f76536231d78580f9246f358d591383dc793f013b291c8eb2c6fdea9ec94ea9",
            "ev:9c27354fbc27515aebfa59f55efe077972e9dd6620969475d2af7cb5428cb1ba",
            "ev:d420cf3a86deb4d7129a53dd0e7f89f397cb928b2ca6c033c56c43923c85cf09"
          ],
          "fact_ids": [
            "fact:c85e7bbfbc5387fef3868da123d3023bb10305b2b0ab22fd62e6a7b7260b5666"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy dependency; không kết luận route công khai"
            },
            {
              "field": "response_model_ids",
              "reason": "Response model không phải Pydantic model trong repo: JSONResponse"
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
