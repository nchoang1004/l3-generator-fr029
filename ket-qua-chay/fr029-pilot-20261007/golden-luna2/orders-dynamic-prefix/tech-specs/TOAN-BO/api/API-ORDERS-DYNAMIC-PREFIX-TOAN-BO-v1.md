---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:bc37a5effa79c1c85312e4a32c1b54d8decd67b7e8119387a74e840fbf3eaaac"
owner_component_id: "cmp_0a77ec3fd6d170dfcabff39c83c13b7f42b451dfc02a64fe1040282430241675"
owner_component: "Toàn bộ"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v7"
fact_ids: ["fact:6aab9dcf4a38bcbc7ff00da197212336cde2ed9c25f45d370f4414eaec47e819", "fact:e5a34f066c2ce3bf564e50e18c3c8a4a39a2fd39855a1dd6936b360f3455d5ec"]
evidence_ids: ["ev:0288d93de510919042db838d572a8c2347a7ba2ec082072ab617364cd77308ff", "ev:1ed15ac07c299741ac22cea40361d61abe3a445ed7b197247a75912f5a4aa594", "ev:6c82156f3366a8e016afe93d93f91aa7a803faa1f164ac9f70ec4792f3361e4e", "ev:7e55a1b2410147063246808a84bd2be69baf6d796e88908381dc0f4324cfaf1f", "ev:92dd6e4ae0add603996b39fa4b605feafd3c8cd5f2c61349d2b3d2cdaa71d977", "ev:960193784bc5e59322277332a178ab0cad49037c05f86c7446c33f0f473578fa", "ev:f954bda191e11619a7457d0f217f098adf00c2f7822f576263a209335f4f9087"]
---
# API — Toàn bộ

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | unknown — Giá trị prefix lấy từ biến môi trường API_PREFIX, không có giá trị mặc định đọc được. (hậu tố đã biết: /orders) | order (body, OrderInput, bắt buộc) | OrderInput | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | inferred (fastapi.default_status_200, fastapi.model_param_body) / partial | `f:6aab9dcf` |


## Model

### OrderInput (request)

Fact `f:e5a34f06` · inferred (pydantic.v2_required_no_default) / full · khai ở schemas.py:3

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| product | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:main.py:5 | POST | unknown — Giá trị prefix lấy từ biến môi trường API_PREFIX, không có giá trị mặc định đọc được. (hậu tố đã biết: /orders) | routes.py::create_order_endpoint | fact:e5a34f066c2ce3bf564e50e18c3c8a4a39a2fd39855a1dd6936b360f3455d5ec | (rỗng) | 200 | dependency: get_db; auth: unknown — Không thấy cơ chế xác thực được khai báo trong mã nguồn. | `fact:6aab9dcf4a38bcbc7ff00da197212336cde2ed9c25f45d370f4414eaec47e819` | `ev:f954bda191e11619a7457d0f217f098adf00c2f7822f576263a209335f4f9087` (main.py:5), `ev:960193784bc5e59322277332a178ab0cad49037c05f86c7446c33f0f473578fa` (main.py:7), `ev:7e55a1b2410147063246808a84bd2be69baf6d796e88908381dc0f4324cfaf1f` (routes.py:9-10), `ev:92dd6e4ae0add603996b39fa4b605feafd3c8cd5f2c61349d2b3d2cdaa71d977` (routes.py:9), `ev:6c82156f3366a8e016afe93d93f91aa7a803faa1f164ac9f70ec4792f3361e4e` (routes.py:10) | inferred | partial |

Model (mã dữ kiện đầy đủ và vị trí khai báo):

| Model | Fact | Evidence |
|---|---|---|
| OrderInput | fact:e5a34f066c2ce3bf564e50e18c3c8a4a39a2fd39855a1dd6936b360f3455d5ec | schemas.py:3 |

Chưa có khối OpenAPI: Không route nào đủ method, path đầy đủ và status code.

Bỏ khỏi khối OpenAPI:

- Bỏ khỏi OpenAPI: `fact:6aab9dcf4a38bcbc7ff00da197212336cde2ed9c25f45d370f4414eaec47e819` (POST /orders) — Path đầy đủ chưa biết
