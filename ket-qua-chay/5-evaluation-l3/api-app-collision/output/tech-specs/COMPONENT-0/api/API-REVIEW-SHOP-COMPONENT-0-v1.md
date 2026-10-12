---
generated: true
non_normative: true
snapshot_id: "snapshot-render-eval-v1"
owner_component_id: "cmp-000"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:3fc4ccfe745870e2c0d99f71f30ff0656c8dedd41cc1d7d3d376b0dbe685e2f3", "fact:7692c3ad3540bb803c020b3aee66cd8887123234ea0c6e7143c0add73ff431ed"]
evidence_ids: ["ev-render-eval"]
---
# API — Component 0

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app-other | GET | /v1/orders | app.api.orders | (rỗng) | (rỗng) | 200 | unknown — Synthetic case: upstream could not establish this field | `fact:3fc4ccfe745870e2c0d99f71f30ff0656c8dedd41cc1d7d3d376b0dbe685e2f3` | `ev-render-eval` (app/api.py:1) | exact | full |
| app-main | GET | /v1/orders | app.api.orders | (rỗng) | (rỗng) | 200 | unknown — Synthetic case: upstream could not establish this field | `fact:7692c3ad3540bb803c020b3aee66cd8887123234ea0c6e7143c0add73ff431ed` | `ev-render-eval` (app/api.py:1) | exact | full |

Chưa có khối OpenAPI: Không route nào đủ method, path đầy đủ và status code.

Bỏ khỏi khối OpenAPI:

- Bỏ khỏi OpenAPI: `fact:3fc4ccfe745870e2c0d99f71f30ff0656c8dedd41cc1d7d3d376b0dbe685e2f3` — Trùng method/path trong cùng file; không chọn handler
- Bỏ khỏi OpenAPI: `fact:7692c3ad3540bb803c020b3aee66cd8887123234ea0c6e7143c0add73ff431ed` — Trùng method/path trong cùng file; không chọn handler
