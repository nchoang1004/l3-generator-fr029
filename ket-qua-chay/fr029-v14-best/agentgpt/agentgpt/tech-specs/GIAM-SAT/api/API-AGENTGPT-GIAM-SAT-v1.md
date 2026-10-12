---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:e4165f3a98b552337d7cda0a275136581555ea99b60a6a5cfeedd44532cd86af"
owner_component_id: "cmp_ce65d4ba336b329d95fb1548c1e83992fef1417ce6e57f71b9aebba8a93fbd20"
owner_component: "Giám sát"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v14"
fact_ids: ["fact:78b499d8b410d01a78dfe0b1217041f9b81a7c62a5fa5d772f769625ce69496f", "fact:9ad2d7f8232f6c2ccfb5220ab4b811fb3d0ac0039392c5a1337dc9d0bf30396f"]
evidence_ids: ["ev:075cd5d7b1aa96e0799a9058759cff8ae76153889961ae42c25f2eaf7c3ca07e", "ev:34ea7cfafe1f88c273fc902bcd4fb36ca1283672e03a89943acaec741a0aebf6", "ev:3c3a86034c2e6593742e94a25f0e99479416b775cf33d9455289c849509dd4eb", "ev:6b1eb96c671f0200238561e906e087d0ee32e7f3f1c9a446ddbfc8da64a3007b", "ev:9242e380026a6da396bfb19a79305177095fe452e1d67678a8b049d61af5bf56", "ev:971de71bbc40bf85f9320bab881245c7a27d0eb37f85ecf9c46061cfe8a8f93c", "ev:b222489cf09040f7fa6813e6e9940f7549ace77256b688752d8a4c95a241f1ac", "ev:c9c1f3b96909412f9e84ddf49cd820175c07b023a4777a27598b49051d07f2fd"]
---
# API — Giám sát

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /api/monitoring/error | (không có) | (không có) | (không có) | 200 (suy theo fastapi.response_class_default_status) | dependency: (không có); auth: unknown — Không thấy dependency xác thực trên endpoint error. | inferred (fastapi.response_class_default_status) / partial | `f:78b499d8` |
| GET | /api/monitoring/health | (không có) | (không có) | (không có) | 200 (suy theo fastapi.response_class_default_status) | dependency: (không có); auth: unknown — Không thấy dependency xác thực trên endpoint health. | inferred (fastapi.response_class_default_status) / partial | `f:9ad2d7f8` |


## Model

Không route nào có request/response model đã xác định.

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:reworkd_platform/web/application.py:28 | GET | /api/monitoring/error | reworkd_platform/web/api/monitoring/views.py::error_check | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Không thấy dependency xác thực trên endpoint error. | `fact:78b499d8b410d01a78dfe0b1217041f9b81a7c62a5fa5d772f769625ce69496f` | `ev:34ea7cfafe1f88c273fc902bcd4fb36ca1283672e03a89943acaec741a0aebf6` (reworkd_platform/web/api/monitoring/views.py:15-16), `ev:c9c1f3b96909412f9e84ddf49cd820175c07b023a4777a27598b49051d07f2fd` (reworkd_platform/web/api/monitoring/views.py:15), `ev:9242e380026a6da396bfb19a79305177095fe452e1d67678a8b049d61af5bf56` (reworkd_platform/web/api/router.py:6), `ev:b222489cf09040f7fa6813e6e9940f7549ace77256b688752d8a4c95a241f1ac` (reworkd_platform/web/application.py:28), `ev:6b1eb96c671f0200238561e906e087d0ee32e7f3f1c9a446ddbfc8da64a3007b` (reworkd_platform/web/application.py:34), `ev:971de71bbc40bf85f9320bab881245c7a27d0eb37f85ecf9c46061cfe8a8f93c` (reworkd_platform/web/application.py:51) | inferred | partial |
| app:reworkd_platform/web/application.py:28 | GET | /api/monitoring/health | reworkd_platform/web/api/monitoring/views.py::health_check | (rỗng) | (rỗng) | 200 | dependency: (không có); auth: unknown — Không thấy dependency xác thực trên endpoint health. | `fact:9ad2d7f8232f6c2ccfb5220ab4b811fb3d0ac0039392c5a1337dc9d0bf30396f` | `ev:075cd5d7b1aa96e0799a9058759cff8ae76153889961ae42c25f2eaf7c3ca07e` (reworkd_platform/web/api/monitoring/views.py:6), `ev:3c3a86034c2e6593742e94a25f0e99479416b775cf33d9455289c849509dd4eb` (reworkd_platform/web/api/monitoring/views.py:6-7), `ev:9242e380026a6da396bfb19a79305177095fe452e1d67678a8b049d61af5bf56` (reworkd_platform/web/api/router.py:6), `ev:b222489cf09040f7fa6813e6e9940f7549ace77256b688752d8a4c95a241f1ac` (reworkd_platform/web/application.py:28), `ev:6b1eb96c671f0200238561e906e087d0ee32e7f3f1c9a446ddbfc8da64a3007b` (reworkd_platform/web/application.py:34), `ev:971de71bbc40bf85f9320bab881245c7a27d0eb37f85ecf9c46061cfe8a8f93c` (reworkd_platform/web/application.py:51) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Giám sát",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/api/monitoring/error": {
      "get": {
        "operationId": "op_78b499d8b410d01a",
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.response_class_default_status; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:reworkd_platform/web/application.py:28",
          "evidence_ids": [
            "ev:34ea7cfafe1f88c273fc902bcd4fb36ca1283672e03a89943acaec741a0aebf6",
            "ev:6b1eb96c671f0200238561e906e087d0ee32e7f3f1c9a446ddbfc8da64a3007b",
            "ev:9242e380026a6da396bfb19a79305177095fe452e1d67678a8b049d61af5bf56",
            "ev:971de71bbc40bf85f9320bab881245c7a27d0eb37f85ecf9c46061cfe8a8f93c",
            "ev:b222489cf09040f7fa6813e6e9940f7549ace77256b688752d8a4c95a241f1ac",
            "ev:c9c1f3b96909412f9e84ddf49cd820175c07b023a4777a27598b49051d07f2fd"
          ],
          "fact_ids": [
            "fact:78b499d8b410d01a78dfe0b1217041f9b81a7c62a5fa5d772f769625ce69496f"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy dependency xác thực trên endpoint error."
            }
          ]
        }
      }
    },
    "/api/monitoring/health": {
      "get": {
        "operationId": "op_9ad2d7f8232f6c2c",
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.response_class_default_status; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:reworkd_platform/web/application.py:28",
          "evidence_ids": [
            "ev:075cd5d7b1aa96e0799a9058759cff8ae76153889961ae42c25f2eaf7c3ca07e",
            "ev:3c3a86034c2e6593742e94a25f0e99479416b775cf33d9455289c849509dd4eb",
            "ev:6b1eb96c671f0200238561e906e087d0ee32e7f3f1c9a446ddbfc8da64a3007b",
            "ev:9242e380026a6da396bfb19a79305177095fe452e1d67678a8b049d61af5bf56",
            "ev:971de71bbc40bf85f9320bab881245c7a27d0eb37f85ecf9c46061cfe8a8f93c",
            "ev:b222489cf09040f7fa6813e6e9940f7549ace77256b688752d8a4c95a241f1ac"
          ],
          "fact_ids": [
            "fact:9ad2d7f8232f6c2ccfb5220ab4b811fb3d0ac0039392c5a1337dc9d0bf30396f"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Không thấy dependency xác thực trên endpoint health."
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
