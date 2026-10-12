---
generated: true
non_normative: true
snapshot_id: "snap:635b641f86bb84e0f7ffb93ce783c06e41c8c910708a20838997b48c8d11d2f4"
owner_component_id: "cmp_82f84192155a15f7481f767abbcc66d389beb9a8da98a72ecdb0ea4be815ceeb"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:8cf689a8cf7d4875d3e9bbdc6e72eb2c637dd8d527da62515db5c050f9177ea3"]
evidence_ids: ["ev:1dcbc3923d75aa40c5c14df1653a0b46eb66ac2a645a6f8593bafffa17e5dddc", "ev:2cb9d9a752cbd38e378a5af309166228a09aa41c42544b9ccdaf107f9c484de5", "ev:444d4e0975b61762336b48c6045082f21125341bf579cb3ef22d5553e59c35a0", "ev:6b90b180c8b548c9a32aa2c1613e5e71c113a920d6643e078fdb2c75c60247a6", "ev:72b2701d9d9f3fcf7968d0fb9f6c6bde89aa21a9443fe008ff571ca64f26a9ff", "ev:b2d183e5d82205a82645b705765e9c88a763249a15665fce603ae7364ea037d2", "ev:c8c477a6036366a37d29478fe6c7d77a0bd08f1adb79b3fab7f3dfbcf2a0ffc8", "ev:c9f38c05bb253b4eda41ad78623a0a65468a682783fe58f3ed09677a205f4cda"]
---
# API — Orders API

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/main.py::app | GET | unknown — Prefix phụ thuộc lúc chạy: {os.environ['API_PREFIX']} (hậu tố đã biết: /v1/orders) | app.routes.list_orders | (rỗng) | (rỗng) | unknown — Decorator không khai báo status_code literal; không suy mặc định của framework | unknown — Không thấy dependency; không kết luận route công khai | `fact:8cf689a8cf7d4875d3e9bbdc6e72eb2c637dd8d527da62515db5c050f9177ea3` | `ev:b2d183e5d82205a82645b705765e9c88a763249a15665fce603ae7364ea037d2` (app/main.py:7), `ev:6b90b180c8b548c9a32aa2c1613e5e71c113a920d6643e078fdb2c75c60247a6` (app/main.py:8), `ev:c8c477a6036366a37d29478fe6c7d77a0bd08f1adb79b3fab7f3dfbcf2a0ffc8` (app/main.py:8), `ev:2cb9d9a752cbd38e378a5af309166228a09aa41c42544b9ccdaf107f9c484de5` (app/routes.py:3), `ev:72b2701d9d9f3fcf7968d0fb9f6c6bde89aa21a9443fe008ff571ca64f26a9ff` (app/routes.py:3), `ev:1dcbc3923d75aa40c5c14df1653a0b46eb66ac2a645a6f8593bafffa17e5dddc` (app/routes.py:6), `ev:444d4e0975b61762336b48c6045082f21125341bf579cb3ef22d5553e59c35a0` (app/routes.py:6-7), `ev:c9f38c05bb253b4eda41ad78623a0a65468a682783fe58f3ed09677a205f4cda` (app/routes.py:6) | inferred | partial |

Chưa có khối OpenAPI: Không route nào đủ method, path đầy đủ và status code.

Bỏ khỏi khối OpenAPI:

- Bỏ khỏi OpenAPI: `fact:8cf689a8cf7d4875d3e9bbdc6e72eb2c637dd8d527da62515db5c050f9177ea3` — Path đầy đủ chưa biết
