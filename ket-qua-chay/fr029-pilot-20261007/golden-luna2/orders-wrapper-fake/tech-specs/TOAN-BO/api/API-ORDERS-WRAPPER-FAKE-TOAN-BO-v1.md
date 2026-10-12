---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:c1dcbd5bec6cf97c949bc44e3968909d4404aa760065ac50806aebb183e2ff74"
owner_component_id: "cmp_5c5581b0f025fa0f7adb99b498952ad86820ac6b47e1ef4e3a9a469b82b34050"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v7"
fact_ids: ["fact:e6581f290c0bbfecddb97fd2012b5a5bea2e9b0a36bab05e5684c0165e3373c3", "fact:378282ccb24cf866178f208760f4054dacb672fce4d63549172dc0565eba9bfb"]
evidence_ids: ["ev:00385fdf5f6a80a04475352e21724c399134e6017ca4c5630a4e14bf5dbecb23", "ev:0e5b6b97cf2005628db23ab93c310a0d55fa7f582f0c3387de5a61ba1d6765de", "ev:99b108c3749b591361422c254763550dca1df530d03fd5b9e7e8b9cc1d77cecc", "ev:bec8bd1b82f313fdf51e85ded7f22b8efd89100722738919def8b22b1005cf3e", "ev:ef31e0fdd0a92a2c3c31bb9861b02116b099bfb722e9436c9830d81a34f9b65c"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | unknown — Router chỉ được tạo; lời gọi attach trả lại router mà không đăng ký vào app nên không xác định app phục vụ route. (hậu tố đã biết: /orders) | order (body, OrderInput, bắt buộc) | OrderInput | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Mã nguồn không chứng minh cơ chế xác thực. | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:e6581f29` |


## Model

### OrderInput (request)

Fact `f:378282cc` · exact / full · khai ở schemas.py:3

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| product | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| unknown — Router chỉ được tạo; lời gọi attach trả lại router mà không đăng ký vào app nên không xác định app phục vụ route. | POST | unknown — Router chỉ được tạo; lời gọi attach trả lại router mà không đăng ký vào app nên không xác định app phục vụ route. (hậu tố đã biết: /orders) | routes.py::create_order_endpoint | fact:378282ccb24cf866178f208760f4054dacb672fce4d63549172dc0565eba9bfb | (rỗng) | 200 | dependency: get_db; auth: unknown — Mã nguồn không chứng minh cơ chế xác thực. | `fact:e6581f290c0bbfecddb97fd2012b5a5bea2e9b0a36bab05e5684c0165e3373c3` | `ev:00385fdf5f6a80a04475352e21724c399134e6017ca4c5630a4e14bf5dbecb23` (routes.py:9), `ev:99b108c3749b591361422c254763550dca1df530d03fd5b9e7e8b9cc1d77cecc` (routes.py:9-10), `ev:bec8bd1b82f313fdf51e85ded7f22b8efd89100722738919def8b22b1005cf3e` (routes.py:10) | inferred | partial |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| OrderInput | fact:378282ccb24cf866178f208760f4054dacb672fce4d63549172dc0565eba9bfb | schemas.py:3 |

Chưa có khối OpenAPI: Không route nào đủ method, path đầy đủ và status code.

Bỏ khỏi khối OpenAPI:

- Bỏ khỏi OpenAPI: `fact:e6581f290c0bbfecddb97fd2012b5a5bea2e9b0a36bab05e5684c0165e3373c3` (POST /orders) — Path đầy đủ chưa biết
