---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:580534b662619976e5bee16365f43113b4a3ee22c99b2801ee45f291e2b399b6"
owner_component_id: "cmp_31b297b7d7bd30deed27cc1affcbe66aefd15d7ac2e7e9e5e83081d9395c2b87"
owner_component: "Đơn hàng"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v5"
fact_ids: ["fact:8cd48a5c6ccabe0def07cad156de29ebe7e45d4d5b63394d1ff6e8d111cbbb78"]
evidence_ids: ["ev:7280cf5de032de19ba96ddac663efe7fd3cd5dfd45ddd23e23673ba3dce6786f", "ev:9c589074f1730754c1adc59f150a61b4cdca8c42fc58a84d9c4c3243e0f5edd3", "ev:a8c9af97ee3c937fcb6d9e422f74821ef267ff2cd1649a4356d1f337fb35072f", "ev:eb64404d6cd2fe56328deebd9af136b2227cbe429332fd905577f16d9901dd87"]
---
# API — Đơn hàng

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /orders | (không có) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Không thấy cơ chế xác thực được khai báo cho route này. | inferred (fastapi.default_status_200) / partial | `f:8cd48a5c` |


## Model

Không route nào có request/response model đã xác định.

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:6 | GET | /orders | app/routers/orders.py::list_orders | (rỗng) | (rỗng) | 200 | unknown — Không thấy cơ chế xác thực được khai báo cho route này. | `fact:8cd48a5c6ccabe0def07cad156de29ebe7e45d4d5b63394d1ff6e8d111cbbb78` | `ev:7280cf5de032de19ba96ddac663efe7fd3cd5dfd45ddd23e23673ba3dce6786f` (app/main.py:6), `ev:a8c9af97ee3c937fcb6d9e422f74821ef267ff2cd1649a4356d1f337fb35072f` (app/routers/orders.py:5), `ev:9c589074f1730754c1adc59f150a61b4cdca8c42fc58a84d9c4c3243e0f5edd3` (app/routers/orders.py:8-9), `ev:eb64404d6cd2fe56328deebd9af136b2227cbe429332fd905577f16d9901dd87` (app/routers/orders.py:8) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Đơn hàng",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/orders": {
      "get": {
        "operationId": "op_8cd48a5c6ccabe0d",
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:6",
          "evidence_ids": [
            "ev:7280cf5de032de19ba96ddac663efe7fd3cd5dfd45ddd23e23673ba3dce6786f",
            "ev:9c589074f1730754c1adc59f150a61b4cdca8c42fc58a84d9c4c3243e0f5edd3",
            "ev:a8c9af97ee3c937fcb6d9e422f74821ef267ff2cd1649a4356d1f337fb35072f",
            "ev:eb64404d6cd2fe56328deebd9af136b2227cbe429332fd905577f16d9901dd87"
          ],
          "fact_ids": [
            "fact:8cd48a5c6ccabe0def07cad156de29ebe7e45d4d5b63394d1ff6e8d111cbbb78"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy cơ chế xác thực được khai báo cho route này."
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
