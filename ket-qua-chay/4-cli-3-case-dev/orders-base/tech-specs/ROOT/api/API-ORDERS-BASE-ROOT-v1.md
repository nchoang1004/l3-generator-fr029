---
generated: true
non_normative: true
snapshot_id: "snap:b4f357c449cb8f2890027f8e3037b30852aa06c14d4f6372ca58ed154c606616"
owner_component_id: "cmp_9bc109dffd090e5b2cd9c9173775fbcdc50dd15cb7fff3be472c7b9a0ae6644a"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:4e8707c75a42409cd9f2eb1abda314649c40656fbb47046c737261d755526f81"]
evidence_ids: ["ev:0b8acf93ef0399f4d3b89c6b1f0bdd8b79255dd04ab11f86bddeb614f28dfacc", "ev:1b4a3a3ce90e36b3ad3b8abc4d90a7cd045c86a81df6d8254d1f34037f69a768", "ev:2e8fca8b190b4f83e2fe22a5f5dd1b518f0462200d8836ac7520f738b0396999", "ev:8455ec4863e0cd7cde39874d5b9341e295857bb4d82c40bc40db6e3ff1dac612", "ev:868243d1a8cfe0445c53495bb0ae7a95eb1d59eb8b0302f07014c0b68963124d", "ev:afdf519b77b9e3b2cbbb8e2aa59e32f3c6b359ce987f6bc09e2472d1ad2971e6", "ev:d3cf1b2515c07ff154af5ba2d589ad2666ecf906257f07e0a81b35eecb593143", "ev:fcc6131fbf0ba47a351e76867616eba15e457a3e634a24ad1604273f599cbac0"]
---
# API — (root)

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:main.py::app | POST | /api/v1/orders | routes.create_order_endpoint | fact:e02ec3db38c72f5c196acea5f5d4332ccecd208d267830a44b9ddf61dcaa2b21 | (rỗng) | unknown — Decorator không khai báo status_code literal; không suy mặc định của framework | unknown — Có Depends(...) nhưng không kết luận cơ chế xác thực | `fact:4e8707c75a42409cd9f2eb1abda314649c40656fbb47046c737261d755526f81` | `ev:afdf519b77b9e3b2cbbb8e2aa59e32f3c6b359ce987f6bc09e2472d1ad2971e6` (main.py:4), `ev:2e8fca8b190b4f83e2fe22a5f5dd1b518f0462200d8836ac7520f738b0396999` (main.py:5), `ev:8455ec4863e0cd7cde39874d5b9341e295857bb4d82c40bc40db6e3ff1dac612` (main.py:5), `ev:868243d1a8cfe0445c53495bb0ae7a95eb1d59eb8b0302f07014c0b68963124d` (routes.py:7), `ev:1b4a3a3ce90e36b3ad3b8abc4d90a7cd045c86a81df6d8254d1f34037f69a768` (routes.py:9), `ev:d3cf1b2515c07ff154af5ba2d589ad2666ecf906257f07e0a81b35eecb593143` (routes.py:9-10), `ev:fcc6131fbf0ba47a351e76867616eba15e457a3e634a24ad1604273f599cbac0` (routes.py:9), `ev:0b8acf93ef0399f4d3b89c6b1f0bdd8b79255dd04ab11f86bddeb614f28dfacc` (routes.py:10) | inferred | partial |

Chưa có khối OpenAPI: Không route nào đủ method, path đầy đủ và status code.

Bỏ khỏi khối OpenAPI:

- Bỏ khỏi OpenAPI: `fact:4e8707c75a42409cd9f2eb1abda314649c40656fbb47046c737261d755526f81` — Status code chưa biết
