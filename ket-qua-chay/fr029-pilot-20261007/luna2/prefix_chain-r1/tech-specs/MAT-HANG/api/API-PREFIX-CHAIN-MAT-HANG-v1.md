---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:c76102dcd74977697e638089e01037e517bb8e4d9a039f63ffbf8bf79eaca9b7"
owner_component_id: "cmp_d98876360788a56b755a5e6aff01808e8ae50c526988530d22bc81f1e7679c88"
owner_component: "Mặt hàng"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v4"
fact_ids: ["fact:00ca5809c7e87a39f20fb4365dea8df1e8444c9ae2ee2c65187e29e93e05a9fa", "fact:1bb54c8667ddd8e97780c30b28f274108fbb0de761859339089487ee00293394", "fact:4ee7aa9feab4a99922ad3997bbe3ee7de1ed3cfae74496c4593ad22a69f81a55", "fact:801799501b964772628d9480c47c9337a9170e56d36bb1793011d7aa3d08447a", "fact:97bedc7f9dc212ac1ca1088b85edd015377ce69e3f21d4f4a1c42cb86635d403", "fact:a92cf47e58c999e445cd225913e60f9e92d21e39f9e96092a36022b2906771f7", "fact:b4570306ed8ac2a2e2569acb0810d70df315dc584b6137427bd8c5523f4b974f", "fact:daf9270b42d46da6e47153ab3a927933a0867a389c7f468da6c2fed2258f0860", "fact:de41457a430353f311eb15a91d2cf90428a4aff8844c6abcaa9e08f091441b82", "fact:fe073f6a2071a2e7f38eb01d78a1acc1f580375c3aa5a3fc36ab9d6245d1b94d"]
evidence_ids: ["ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08", "ev:24d151db74b631eda4dd7001edd5d150edbf6dca26c749f54baa104f6da3330b", "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8", "ev:3b22b758593bf064eaee418912af609b4781e0f7d5a3f047eccb38ef23f5217b", "ev:4cf53e990e7cf13f02a8b0c2fcc4af86cc7d67461fbe1f94a6ab7694e5f1944f", "ev:4dd2bac78fe43c63f4bca027c70f8301a6c37c1f6d595f3a0eadbf16616cadd4", "ev:703b930c1028fbed1c8afe330f9eaa663a67af836e4d1be5062339455b771777", "ev:7276eb7ef247279e4449322090b044c449b5196da6659d9d5f2d4ecd9a5d4d5f", "ev:7ba4ab3015c67faf8bc96b71b02d63d3e05ec2c825f02e69c5b4ef93a199cc05", "ev:7cb8593ccc0bc2a9f6fd2dbbdbae894fb22cdfbdf7ddf2480043df7be77fba49", "ev:81382dd3d8f5d5798b9ce5a19076a38bf32f8d364eb1b8e13f1a422d1b37c8ed", "ev:9f9afff67aa5c984d8bf9fd449e0dbc38222603692e14e67084eafbf40351c78", "ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d", "ev:f70dcc170f659b24ea45c999b771d01e88def0db531bf10c91ea90b09ab117e0", "ev:f741f556ff3bcb22bf65b6a7c7b5b809ca8d9ce984e28a83d0967674c4f326dd", "ev:fc46390ad8f5e9fceb97dff255e4b4e9564e48be2aada1fd59db41e2323c8b6c"]
---
# API — Mặt hàng

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | unknown — Chưa đọc tệp khởi động/gắn router (hậu tố đã biết: /api/items/{item_id}) | item_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Mã nguồn đã đọc không chứng minh cơ chế xác thực | inferred (fastapi.default_status_200) / partial | `f:4ee7aa9f` |
| GET | /api/v1/items/ | (không có) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Mã nguồn không chứng minh cơ chế xác thực | inferred (fastapi.default_status_200, settings.default_prefix) / partial | `f:80179950` |
| GET | /api/v1/items/{item_id} | item_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Mã nguồn không chứng minh cơ chế xác thực | inferred (fastapi.default_status_200, settings.default_prefix) / partial | `f:a92cf47e` |
| GET | /api/v1/items/{item_id}/sync | item_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Mã nguồn không chứng minh cơ chế xác thực | inferred (fastapi.default_status_200, settings.default_prefix) / partial | `f:daf9270b` |
| POST | /api/v1/items/{item_id}/sync | item_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Mã nguồn không chứng minh cơ chế xác thực | inferred (fastapi.default_status_200, settings.default_prefix) / partial | `f:97bedc7f` |
| GET | unknown — Chưa đọc tệp khởi động/gắn router (hậu tố đã biết: /items/) | (không có) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Mã nguồn đã đọc không chứng minh cơ chế xác thực | inferred (fastapi.default_status_200) / partial | `f:b4570306` |
| GET | unknown — Chưa đọc tệp khởi động/gắn router (hậu tố đã biết: /items/{item_id}) | item_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Mã nguồn đã đọc không chứng minh cơ chế xác thực | inferred (fastapi.default_status_200) / partial | `f:de41457a` |
| GET | unknown — Chưa đọc tệp khởi động/gắn router (hậu tố đã biết: /items/{item_id}/sync) | item_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Chưa đọc tệp nguồn chứng minh cơ chế xác thực | inferred (fastapi.default_status_200) / partial | `f:1bb54c86` |
| POST | unknown — Chưa đọc tệp khởi động/gắn router (hậu tố đã biết: /items/{item_id}/sync) | item_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Chưa đọc tệp nguồn chứng minh cơ chế xác thực | inferred (fastapi.default_status_200) / partial | `f:00ca5809` |
| GET | /v1/api/items/{item_id} | item_id (path, integer, bắt buộc) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | unknown — Mã nguồn không chứng minh cơ chế xác thực | inferred (fastapi.default_status_200) / partial | `f:fe073f6a` |


## Model

Không route nào có request/response model đã xác định.

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| unknown — Chưa đọc tệp khởi động/gắn router | GET | unknown — Chưa đọc tệp khởi động/gắn router (hậu tố đã biết: /api/items/{item_id}) | app/api/legacy.py::legacy_get_item | (rỗng) | (rỗng) | 200 | unknown — Mã nguồn đã đọc không chứng minh cơ chế xác thực | `fact:4ee7aa9feab4a99922ad3997bbe3ee7de1ed3cfae74496c4593ad22a69f81a55` | `ev:3b22b758593bf064eaee418912af609b4781e0f7d5a3f047eccb38ef23f5217b` (app/api/legacy.py:3), `ev:703b930c1028fbed1c8afe330f9eaa663a67af836e4d1be5062339455b771777` (app/api/legacy.py:6), `ev:f741f556ff3bcb22bf65b6a7c7b5b809ca8d9ce984e28a83d0967674c4f326dd` (app/api/legacy.py:6-7), `ev:9f9afff67aa5c984d8bf9fd449e0dbc38222603692e14e67084eafbf40351c78` (app/api/legacy.py:7) | inferred | partial |
| app:app/main.py:12 | GET | /api/v1/items/ | app/api/items.py::list_items | (rỗng) | (rỗng) | 200 | unknown — Mã nguồn không chứng minh cơ chế xác thực | `fact:801799501b964772628d9480c47c9337a9170e56d36bb1793011d7aa3d08447a` | `ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d` (app/api/items.py:3), `ev:7276eb7ef247279e4449322090b044c449b5196da6659d9d5f2d4ecd9a5d4d5f` (app/api/items.py:6), `ev:f70dcc170f659b24ea45c999b771d01e88def0db531bf10c91ea90b09ab117e0` (app/api/items.py:6-7), `ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08` (app/config.py:5), `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12) | inferred | partial |
| app:app/main.py:12 | GET | /api/v1/items/{item_id} | app/api/items.py::get_item | (rỗng) | (rỗng) | 200 | unknown — Mã nguồn không chứng minh cơ chế xác thực | `fact:a92cf47e58c999e445cd225913e60f9e92d21e39f9e96092a36022b2906771f7` | `ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d` (app/api/items.py:3), `ev:7ba4ab3015c67faf8bc96b71b02d63d3e05ec2c825f02e69c5b4ef93a199cc05` (app/api/items.py:11-12), `ev:81382dd3d8f5d5798b9ce5a19076a38bf32f8d364eb1b8e13f1a422d1b37c8ed` (app/api/items.py:11), `ev:24d151db74b631eda4dd7001edd5d150edbf6dca26c749f54baa104f6da3330b` (app/api/items.py:12), `ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08` (app/config.py:5), `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12) | inferred | partial |
| app:app/main.py:12 | GET | /api/v1/items/{item_id}/sync | app/api/items.py::sync_item | (rỗng) | (rỗng) | 200 | unknown — Mã nguồn không chứng minh cơ chế xác thực | `fact:daf9270b42d46da6e47153ab3a927933a0867a389c7f468da6c2fed2258f0860` | `ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d` (app/api/items.py:3), `ev:4cf53e990e7cf13f02a8b0c2fcc4af86cc7d67461fbe1f94a6ab7694e5f1944f` (app/api/items.py:16-17), `ev:4dd2bac78fe43c63f4bca027c70f8301a6c37c1f6d595f3a0eadbf16616cadd4` (app/api/items.py:16), `ev:7cb8593ccc0bc2a9f6fd2dbbdbae894fb22cdfbdf7ddf2480043df7be77fba49` (app/api/items.py:17), `ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08` (app/config.py:5), `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12) | inferred | partial |
| app:app/main.py:12 | POST | /api/v1/items/{item_id}/sync | app/api/items.py::sync_item | (rỗng) | (rỗng) | 200 | unknown — Mã nguồn không chứng minh cơ chế xác thực | `fact:97bedc7f9dc212ac1ca1088b85edd015377ce69e3f21d4f4a1c42cb86635d403` | `ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d` (app/api/items.py:3), `ev:4cf53e990e7cf13f02a8b0c2fcc4af86cc7d67461fbe1f94a6ab7694e5f1944f` (app/api/items.py:16-17), `ev:4dd2bac78fe43c63f4bca027c70f8301a6c37c1f6d595f3a0eadbf16616cadd4` (app/api/items.py:16), `ev:7cb8593ccc0bc2a9f6fd2dbbdbae894fb22cdfbdf7ddf2480043df7be77fba49` (app/api/items.py:17), `ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08` (app/config.py:5), `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12) | inferred | partial |
| unknown — Chưa đọc tệp khởi động/gắn router | GET | unknown — Chưa đọc tệp khởi động/gắn router (hậu tố đã biết: /items/) | app/api/items.py::list_items | (rỗng) | (rỗng) | 200 | unknown — Mã nguồn đã đọc không chứng minh cơ chế xác thực | `fact:b4570306ed8ac2a2e2569acb0810d70df315dc584b6137427bd8c5523f4b974f` | `ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d` (app/api/items.py:3), `ev:7276eb7ef247279e4449322090b044c449b5196da6659d9d5f2d4ecd9a5d4d5f` (app/api/items.py:6), `ev:f70dcc170f659b24ea45c999b771d01e88def0db531bf10c91ea90b09ab117e0` (app/api/items.py:6-7) | inferred | partial |
| unknown — Chưa đọc tệp khởi động/gắn router | GET | unknown — Chưa đọc tệp khởi động/gắn router (hậu tố đã biết: /items/{item_id}) | app/api/items.py::get_item | (rỗng) | (rỗng) | 200 | unknown — Mã nguồn đã đọc không chứng minh cơ chế xác thực | `fact:de41457a430353f311eb15a91d2cf90428a4aff8844c6abcaa9e08f091441b82` | `ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d` (app/api/items.py:3), `ev:7ba4ab3015c67faf8bc96b71b02d63d3e05ec2c825f02e69c5b4ef93a199cc05` (app/api/items.py:11-12), `ev:81382dd3d8f5d5798b9ce5a19076a38bf32f8d364eb1b8e13f1a422d1b37c8ed` (app/api/items.py:11), `ev:24d151db74b631eda4dd7001edd5d150edbf6dca26c749f54baa104f6da3330b` (app/api/items.py:12) | inferred | partial |
| unknown — Chưa đọc tệp khởi động/gắn router | GET | unknown — Chưa đọc tệp khởi động/gắn router (hậu tố đã biết: /items/{item_id}/sync) | app/api/items.py::sync_item | (rỗng) | (rỗng) | 200 | unknown — Chưa đọc tệp nguồn chứng minh cơ chế xác thực | `fact:1bb54c8667ddd8e97780c30b28f274108fbb0de761859339089487ee00293394` | `ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d` (app/api/items.py:3), `ev:4cf53e990e7cf13f02a8b0c2fcc4af86cc7d67461fbe1f94a6ab7694e5f1944f` (app/api/items.py:16-17), `ev:4dd2bac78fe43c63f4bca027c70f8301a6c37c1f6d595f3a0eadbf16616cadd4` (app/api/items.py:16), `ev:7cb8593ccc0bc2a9f6fd2dbbdbae894fb22cdfbdf7ddf2480043df7be77fba49` (app/api/items.py:17) | inferred | partial |
| unknown — Chưa đọc tệp khởi động/gắn router | POST | unknown — Chưa đọc tệp khởi động/gắn router (hậu tố đã biết: /items/{item_id}/sync) | app/api/items.py::sync_item | (rỗng) | (rỗng) | 200 | unknown — Chưa đọc tệp nguồn chứng minh cơ chế xác thực | `fact:00ca5809c7e87a39f20fb4365dea8df1e8444c9ae2ee2c65187e29e93e05a9fa` | `ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d` (app/api/items.py:3), `ev:4cf53e990e7cf13f02a8b0c2fcc4af86cc7d67461fbe1f94a6ab7694e5f1944f` (app/api/items.py:16-17), `ev:4dd2bac78fe43c63f4bca027c70f8301a6c37c1f6d595f3a0eadbf16616cadd4` (app/api/items.py:16), `ev:7cb8593ccc0bc2a9f6fd2dbbdbae894fb22cdfbdf7ddf2480043df7be77fba49` (app/api/items.py:17) | inferred | partial |
| app:app/main.py:12 | GET | /v1/api/items/{item_id} | app/api/legacy.py::legacy_get_item | (rỗng) | (rỗng) | 200 | unknown — Mã nguồn không chứng minh cơ chế xác thực | `fact:fe073f6a2071a2e7f38eb01d78a1acc1f580375c3aa5a3fc36ab9d6245d1b94d` | `ev:3b22b758593bf064eaee418912af609b4781e0f7d5a3f047eccb38ef23f5217b` (app/api/legacy.py:3), `ev:703b930c1028fbed1c8afe330f9eaa663a67af836e4d1be5062339455b771777` (app/api/legacy.py:6), `ev:f741f556ff3bcb22bf65b6a7c7b5b809ca8d9ce984e28a83d0967674c4f326dd` (app/api/legacy.py:6-7), `ev:9f9afff67aa5c984d8bf9fd449e0dbc38222603692e14e67084eafbf40351c78` (app/api/legacy.py:7), `ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8` (app/main.py:12), `ev:fc46390ad8f5e9fceb97dff255e4b4e9564e48be2aada1fd59db41e2323c8b6c` (app/main.py:21) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Mặt hàng",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/api/v1/items/": {
      "get": {
        "operationId": "op_801799501b964772",
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08",
            "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8",
            "ev:7276eb7ef247279e4449322090b044c449b5196da6659d9d5f2d4ecd9a5d4d5f",
            "ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d",
            "ev:f70dcc170f659b24ea45c999b771d01e88def0db531bf10c91ea90b09ab117e0"
          ],
          "fact_ids": [
            "fact:801799501b964772628d9480c47c9337a9170e56d36bb1793011d7aa3d08447a"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Mã nguồn không chứng minh cơ chế xác thực"
            }
          ]
        }
      }
    },
    "/api/v1/items/{item_id}": {
      "get": {
        "operationId": "op_a92cf47e58c999e4",
        "parameters": [
          {
            "in": "path",
            "name": "item_id",
            "required": true,
            "schema": {
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08",
            "ev:24d151db74b631eda4dd7001edd5d150edbf6dca26c749f54baa104f6da3330b",
            "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8",
            "ev:7ba4ab3015c67faf8bc96b71b02d63d3e05ec2c825f02e69c5b4ef93a199cc05",
            "ev:81382dd3d8f5d5798b9ce5a19076a38bf32f8d364eb1b8e13f1a422d1b37c8ed",
            "ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d"
          ],
          "fact_ids": [
            "fact:a92cf47e58c999e445cd225913e60f9e92d21e39f9e96092a36022b2906771f7"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Mã nguồn không chứng minh cơ chế xác thực"
            }
          ]
        }
      }
    },
    "/api/v1/items/{item_id}/sync": {
      "get": {
        "operationId": "op_daf9270b42d46da6",
        "parameters": [
          {
            "in": "path",
            "name": "item_id",
            "required": true,
            "schema": {
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08",
            "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8",
            "ev:4cf53e990e7cf13f02a8b0c2fcc4af86cc7d67461fbe1f94a6ab7694e5f1944f",
            "ev:4dd2bac78fe43c63f4bca027c70f8301a6c37c1f6d595f3a0eadbf16616cadd4",
            "ev:7cb8593ccc0bc2a9f6fd2dbbdbae894fb22cdfbdf7ddf2480043df7be77fba49",
            "ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d"
          ],
          "fact_ids": [
            "fact:daf9270b42d46da6e47153ab3a927933a0867a389c7f468da6c2fed2258f0860"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Mã nguồn không chứng minh cơ chế xác thực"
            }
          ]
        }
      },
      "post": {
        "operationId": "op_97bedc7f9dc212ac",
        "parameters": [
          {
            "in": "path",
            "name": "item_id",
            "required": true,
            "schema": {
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:21875fb3f52374921efe38e2b8f4d85e77c23c1ae7ec2ca9582fa88577162b08",
            "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8",
            "ev:4cf53e990e7cf13f02a8b0c2fcc4af86cc7d67461fbe1f94a6ab7694e5f1944f",
            "ev:4dd2bac78fe43c63f4bca027c70f8301a6c37c1f6d595f3a0eadbf16616cadd4",
            "ev:7cb8593ccc0bc2a9f6fd2dbbdbae894fb22cdfbdf7ddf2480043df7be77fba49",
            "ev:c5ec2fb893697e20adc1d85ad9fb4bd766ff034665def70565f47070fc433d1d"
          ],
          "fact_ids": [
            "fact:97bedc7f9dc212ac1ca1088b85edd015377ce69e3f21d4f4a1c42cb86635d403"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Mã nguồn không chứng minh cơ chế xác thực"
            }
          ]
        }
      }
    },
    "/v1/api/items/{item_id}": {
      "get": {
        "operationId": "op_fe073f6a2071a2e7",
        "parameters": [
          {
            "in": "path",
            "name": "item_id",
            "required": true,
            "schema": {
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:12",
          "evidence_ids": [
            "ev:2878408ecd188e7c176ae1fe2cb97f80e07ac20f19fe57e40d0882747d8f74e8",
            "ev:3b22b758593bf064eaee418912af609b4781e0f7d5a3f047eccb38ef23f5217b",
            "ev:703b930c1028fbed1c8afe330f9eaa663a67af836e4d1be5062339455b771777",
            "ev:9f9afff67aa5c984d8bf9fd449e0dbc38222603692e14e67084eafbf40351c78",
            "ev:f741f556ff3bcb22bf65b6a7c7b5b809ca8d9ce984e28a83d0967674c4f326dd",
            "ev:fc46390ad8f5e9fceb97dff255e4b4e9564e48be2aada1fd59db41e2323c8b6c"
          ],
          "fact_ids": [
            "fact:fe073f6a2071a2e7f38eb01d78a1acc1f580375c3aa5a3fc36ab9d6245d1b94d"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Mã nguồn không chứng minh cơ chế xác thực"
            }
          ]
        }
      }
    }
  },
  "x-analysis": {
    "omitted_operations": [
      {
        "fact_id": "fact:4ee7aa9feab4a99922ad3997bbe3ee7de1ed3cfae74496c4593ad22a69f81a55",
        "reason": "Path đầy đủ chưa biết"
      },
      {
        "fact_id": "fact:b4570306ed8ac2a2e2569acb0810d70df315dc584b6137427bd8c5523f4b974f",
        "reason": "Path đầy đủ chưa biết"
      },
      {
        "fact_id": "fact:de41457a430353f311eb15a91d2cf90428a4aff8844c6abcaa9e08f091441b82",
        "reason": "Path đầy đủ chưa biết"
      },
      {
        "fact_id": "fact:1bb54c8667ddd8e97780c30b28f274108fbb0de761859339089487ee00293394",
        "reason": "Path đầy đủ chưa biết"
      },
      {
        "fact_id": "fact:00ca5809c7e87a39f20fb4365dea8df1e8444c9ae2ee2c65187e29e93e05a9fa",
        "reason": "Path đầy đủ chưa biết"
      }
    ]
  }
}
```

Bỏ khỏi khối OpenAPI:

- Bỏ khỏi OpenAPI: `fact:4ee7aa9feab4a99922ad3997bbe3ee7de1ed3cfae74496c4593ad22a69f81a55` (GET /api/items/{item_id}) — Path đầy đủ chưa biết
- Bỏ khỏi OpenAPI: `fact:b4570306ed8ac2a2e2569acb0810d70df315dc584b6137427bd8c5523f4b974f` (GET /items/) — Path đầy đủ chưa biết
- Bỏ khỏi OpenAPI: `fact:de41457a430353f311eb15a91d2cf90428a4aff8844c6abcaa9e08f091441b82` (GET /items/{item_id}) — Path đầy đủ chưa biết
- Bỏ khỏi OpenAPI: `fact:1bb54c8667ddd8e97780c30b28f274108fbb0de761859339089487ee00293394` (GET /items/{item_id}/sync) — Path đầy đủ chưa biết
- Bỏ khỏi OpenAPI: `fact:00ca5809c7e87a39f20fb4365dea8df1e8444c9ae2ee2c65187e29e93e05a9fa` (POST /items/{item_id}/sync) — Path đầy đủ chưa biết
