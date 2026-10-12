---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:229c9a746a0b5cc8bd99c7c06529a1a4ebcfd8a4b8fec654a03811edd747a904"
owner_component_id: "cmp_5015c50ac5fbcf39c3bde82652ebe44ddae93b295df2897d68a55abd755a4b27"
owner_component: "Khởi động"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v14"
fact_ids: ["fact:cba3ee38cdaf100f4524123457111aa486afab986ed1206495a909e900fbb093"]
evidence_ids: ["ev:88d0c51fd73b926af10bf7b6da15b176a4a7afdbe5b2f2caf653a63ddb1b74e1", "ev:b9b475c53a8abc80b8656805dc2232a0731e1581774b2364211f9cc86ca9076b", "ev:cc5ed5699db9f277ebaa5af48894251d707aefc48db6413f7fcbc2e411ce0d46", "ev:f3346b9c5a9829fded598935cae7d89d663486057f2aa98449b1a47fee9f81aa"]
---
# API — Khởi động

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /health | (không có) | (không có) | object | 200 (suy theo fastapi.default_status_200) | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo cho route này trong mã nguồn đã đọc. | inferred (fastapi.default_status_200, fastapi.return_annotation_response_model) / partial | `f:cba3ee38` |


## Model

Không route nào có request/response model đã xác định.

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:50 | GET | /health | app/main.py::health_check | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Không thấy cơ chế xác thực được khai báo cho route này trong mã nguồn đã đọc. | `fact:cba3ee38cdaf100f4524123457111aa486afab986ed1206495a909e900fbb093` | `ev:cc5ed5699db9f277ebaa5af48894251d707aefc48db6413f7fcbc2e411ce0d46` (app/main.py:50), `ev:88d0c51fd73b926af10bf7b6da15b176a4a7afdbe5b2f2caf653a63ddb1b74e1` (app/main.py:73-74), `ev:f3346b9c5a9829fded598935cae7d89d663486057f2aa98449b1a47fee9f81aa` (app/main.py:73), `ev:b9b475c53a8abc80b8656805dc2232a0731e1581774b2364211f9cc86ca9076b` (app/main.py:74) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Khởi động",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/health": {
      "get": {
        "operationId": "op_cba3ee38cdaf100f",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object"
                }
              }
            },
            "description": "Status code suy theo fastapi.default_status_200"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:50",
          "evidence_ids": [
            "ev:88d0c51fd73b926af10bf7b6da15b176a4a7afdbe5b2f2caf653a63ddb1b74e1",
            "ev:b9b475c53a8abc80b8656805dc2232a0731e1581774b2364211f9cc86ca9076b",
            "ev:cc5ed5699db9f277ebaa5af48894251d707aefc48db6413f7fcbc2e411ce0d46",
            "ev:f3346b9c5a9829fded598935cae7d89d663486057f2aa98449b1a47fee9f81aa"
          ],
          "fact_ids": [
            "fact:cba3ee38cdaf100f4524123457111aa486afab986ed1206495a909e900fbb093"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo cho route này trong mã nguồn đã đọc."
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
