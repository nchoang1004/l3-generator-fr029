---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:9266c293645385b7105ee9fbdd4569adb33048c46932c31cf4042582c7d7e4e5"
owner_component_id: "cmp_dabb40d6ded48a307f9c73f63e655d581f317d0a30557f346b2cffb5237074ed"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v5"
fact_ids: ["fact:92f794496cf89e60b1b1e9db650261540178b3995a257c3508ec70dc911d7301", "fact:97deeb6c03b8571fc3e2b0dddb231a5fea0cbba5aee82894d734289041e71097", "fact:42f3e6f780663d1c99244099485bcc9287376f3b510850e79ca3a58aeb1af07d"]
evidence_ids: ["ev:024b506c9302625f35a5bf79a584a9484fc2f9b7632e1a24f876cb245a65d0c6", "ev:3e64c25273158a198a8c3a76f618049b61e124a56e88ea430c42b2de34bbfdf3", "ev:78952f6bd6d377cfe6c45cf659d471a75bfa100cf262821ff77f43794476984e", "ev:8363e024ab449d7ee87532f3161546ad95a37f22fbcf486c79e23a5b326ddbff", "ev:91490ecbb571d779c779d25638064588598c2dafb0f7eb04af44f210be131edc", "ev:9ea0693934715954e949ff4670d34630873593381388994e99ec480ba88f0b13", "ev:c6a93a83064df2557e1a9f537163a45f6cbe8ccebca5643b4fd326d30210f106", "ev:ea3b674ebe2d993199934075231a1c35d463f2503ca7f845798e660f4ccaa396", "ev:ee906ea56d34d3de2e2cc6c72e2267a77310b6275ce9634c10120e05fe5e2d03"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /api/v1/orders | order (body, OrderInput, bắt buộc) | OrderInput | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:92f79449` |
| POST | /api/v1/orders | order (body, OrderInput, bắt buộc) | OrderInput | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:97deeb6c` |


## Model

### OrderInput (request)

Fact `f:42f3e6f7` · inferred / full · khai ở schemas.py:3

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| product | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:main.py:4 | POST | /api/v1/orders | routes.py::create_order_endpoint | fact:42f3e6f780663d1c99244099485bcc9287376f3b510850e79ca3a58aeb1af07d | (rỗng) | 200 | unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:92f794496cf89e60b1b1e9db650261540178b3995a257c3508ec70dc911d7301` | `ev:9ea0693934715954e949ff4670d34630873593381388994e99ec480ba88f0b13` (main.py:4), `ev:78952f6bd6d377cfe6c45cf659d471a75bfa100cf262821ff77f43794476984e` (main.py:6), `ev:3e64c25273158a198a8c3a76f618049b61e124a56e88ea430c42b2de34bbfdf3` (routes.py:9), `ev:91490ecbb571d779c779d25638064588598c2dafb0f7eb04af44f210be131edc` (routes.py:9-10), `ev:024b506c9302625f35a5bf79a584a9484fc2f9b7632e1a24f876cb245a65d0c6` (routes.py:10) | inferred | partial |
| app:main.py:5 | POST | /api/v1/orders | routes.py::create_order_endpoint | fact:42f3e6f780663d1c99244099485bcc9287376f3b510850e79ca3a58aeb1af07d | (rỗng) | 200 | unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:97deeb6c03b8571fc3e2b0dddb231a5fea0cbba5aee82894d734289041e71097` | `ev:ee906ea56d34d3de2e2cc6c72e2267a77310b6275ce9634c10120e05fe5e2d03` (main.py:5), `ev:ea3b674ebe2d993199934075231a1c35d463f2503ca7f845798e660f4ccaa396` (main.py:7), `ev:3e64c25273158a198a8c3a76f618049b61e124a56e88ea430c42b2de34bbfdf3` (routes.py:9), `ev:91490ecbb571d779c779d25638064588598c2dafb0f7eb04af44f210be131edc` (routes.py:9-10), `ev:024b506c9302625f35a5bf79a584a9484fc2f9b7632e1a24f876cb245a65d0c6` (routes.py:10) | inferred | partial |

Chưa có khối OpenAPI: Không route nào đủ method, path đầy đủ và status code.

Bỏ khỏi khối OpenAPI:

- Bỏ khỏi OpenAPI: `fact:92f794496cf89e60b1b1e9db650261540178b3995a257c3508ec70dc911d7301` (POST /api/v1/orders) — Trùng method/path trong cùng file; không chọn handler
- Bỏ khỏi OpenAPI: `fact:97deeb6c03b8571fc3e2b0dddb231a5fea0cbba5aee82894d734289041e71097` (POST /api/v1/orders) — Trùng method/path trong cùng file; không chọn handler
