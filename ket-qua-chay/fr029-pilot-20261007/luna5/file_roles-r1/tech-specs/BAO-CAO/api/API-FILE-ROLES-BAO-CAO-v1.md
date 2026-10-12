---
generated: true
non_normative: true
review_status: "Bản sinh tự động, chưa được chủ repository duyệt"
snapshot_id: "snap:3df7e7d2177f25da0603482e3cce1c1d8b380eb610c1188f4d497c9948271449"
owner_component_id: "cmp_7f12cbdf8b1d8e45d52d77dcd69c7deaca26672d072b26b172e859e7922144c8"
owner_component: "Báo cáo"
schema_version: "0.1.0"
pipeline_version: "fr029-doc-v1"
prompt_version: "fr029-agent-prompt-v8"
fact_ids: ["fact:211dfe4d2d2851426e2b2e754cdaf0b05e32785c89e3215c09cc9a62a6d1e24a"]
evidence_ids: ["ev:4cd7cf84eb309089f51742d1b02ae1f7779587a4a0cf1abdc7febdc37965a1d0", "ev:513084c353010faddf8b21f92601376293bb34336388ea4d5512fa3791dd0cf1", "ev:5a37e4446132d650ce0c8ff2414b5c9bddb902e70657958d41fcc30e9b565ecd", "ev:e7fcb221762aa4351a32b3db3848783fbb3c55d033ba019d2abf318a6eb2c83f", "ev:eeecf693957dbaf176b625f461b3c943cb57ea18cd8fb471677fcd231910b818", "ev:f3e78b6a23c8c8f3a3eede8405f2b5bcbc7924387dac98061dfa09e272f2b225"]
---
# API — Báo cáo

Bản sinh tự động từ agent đọc source, đã qua bộ kiểm bằng chứng, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| GET | /reports/daily | (không có) | (không có) | (không có) | 200 (suy theo fastapi.default_status_200) | dependency: get_db; auth: unknown — Mã nguồn không thể hiện cơ chế xác thực cho route này. | inferred (fastapi.default_status_200) / partial | `f:211dfe4d` |


## Model

Không route nào có request/response model đã xác định.

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py:5 | GET | /reports/daily | app/api/reports.py::daily_report | (rỗng) | (rỗng) | 200 | dependency: get_db; auth: unknown — Mã nguồn không thể hiện cơ chế xác thực cho route này. | `fact:211dfe4d2d2851426e2b2e754cdaf0b05e32785c89e3215c09cc9a62a6d1e24a` | `ev:eeecf693957dbaf176b625f461b3c943cb57ea18cd8fb471677fcd231910b818` (app/api/reports.py:7), `ev:4cd7cf84eb309089f51742d1b02ae1f7779587a4a0cf1abdc7febdc37965a1d0` (app/api/reports.py:10-11), `ev:513084c353010faddf8b21f92601376293bb34336388ea4d5512fa3791dd0cf1` (app/api/reports.py:10), `ev:e7fcb221762aa4351a32b3db3848783fbb3c55d033ba019d2abf318a6eb2c83f` (app/api/reports.py:11), `ev:f3e78b6a23c8c8f3a3eede8405f2b5bcbc7924387dac98061dfa09e272f2b225` (app/main.py:5), `ev:5a37e4446132d650ce0c8ff2414b5c9bddb902e70657958d41fcc30e9b565ecd` (app/main.py:7) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "info": {
    "title": "Báo cáo",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/reports/daily": {
      "get": {
        "operationId": "op_211dfe4d2d285142",
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi.default_status_200; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/main.py:5",
          "evidence_ids": [
            "ev:4cd7cf84eb309089f51742d1b02ae1f7779587a4a0cf1abdc7febdc37965a1d0",
            "ev:513084c353010faddf8b21f92601376293bb34336388ea4d5512fa3791dd0cf1",
            "ev:5a37e4446132d650ce0c8ff2414b5c9bddb902e70657958d41fcc30e9b565ecd",
            "ev:e7fcb221762aa4351a32b3db3848783fbb3c55d033ba019d2abf318a6eb2c83f",
            "ev:eeecf693957dbaf176b625f461b3c943cb57ea18cd8fb471677fcd231910b818",
            "ev:f3e78b6a23c8c8f3a3eede8405f2b5bcbc7924387dac98061dfa09e272f2b225"
          ],
          "fact_ids": [
            "fact:211dfe4d2d2851426e2b2e754cdaf0b05e32785c89e3215c09cc9a62a6d1e24a"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Mã nguồn không thể hiện cơ chế xác thực cho route này."
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
