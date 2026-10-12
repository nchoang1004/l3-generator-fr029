```json
{
  "repos": [
    {
      "repo": "caura-ai_caura",
      "dependencies": {
        "params_dung": 0,
        "params_sai": [],
        "params_thieu": []
      },
      "deps_bo_sot": {
        "routes_kiem": 31,
        "items": [
          {
            "route": "GET /api/v1/storage/_debug/pg_locks",
            "dependency": "_require_debug_endpoints",
            "cap": "router",
            "source": "core-storage-api/src/core_storage_api/routers/debug.py:36; core-storage-api/src/core_storage_api/routers/debug.py:42; core-storage-api/src/core_storage_api/routers/debug.py:117; core-storage-api/src/core_storage_api/app.py:364"
          }
        ]
      },
      "suspects": {
        "http_that": 19,
        "http_khac": 2,
        "registration": 4,
        "can_giai_thich": 0,
        "nhieu": []
      },
      "http_bo_sot": [
        {
          "at": "core-api/src/core_api/clients/identity_token.py:101",
          "code": "return super().request(*args, **kwargs)"
        },
        {
          "at": "core-worker/src/core_worker/clients/identity_token.py:102",
          "code": "return super().request(*args, **kwargs)"
        },
        {
          "at": "core-worker/src/core_worker/clients/storage_client.py:128",
          "code": "resp = await retry(lambda: fn(*args, headers=headers, **kwargs), label=label)"
        },
        {
          "at": "core-worker/src/core_worker/clients/storage_client.py:138",
          "code": "resp = await retry(lambda: fn(*args, headers=fresh_headers, **kwargs), label=label)"
        },
        {
          "at": "scripts/benchmark_nano_vs_flash.py:83",
          "code": "r = await client.post("
        },
        {
          "at": "scripts/benchmark_nano_vs_flash.py:111",
          "code": "r = await client.post("
        },
        {
          "at": "scripts/entity_retrieval_probe.py:138",
          "code": "r = client.post(f\"{base}/search\", json=payload, timeout=60.0)"
        },
        {
          "at": "scripts/latency_test.py:87",
          "code": "result = func(*args, **kwargs)"
        },
        {
          "at": "scripts/latency_test.py:107",
          "code": "r = client.get(f\"{api}/health\")"
        },
        {
          "at": "scripts/latency_test.py:213",
          "code": "r = client.delete(f\"{api}/memories\", params={\"tenant_id\": tenant})"
        },
        {
          "at": "scripts/hyperagent_test.py:59",
          "code": "return self.client.post(self.url, json=body, headers=headers)"
        },
        {
          "at": "scripts/hyperagent_test.py:1223",
          "code": "r = client.post(f\"{api}/memories/bulk\", json=body)"
        },
        {
          "at": "scripts/hyperagent_test.py:1239",
          "code": "r = client.post(f\"{api}/memories\", json=body)"
        },
        {
          "at": "scripts/hyperagent_test.py:1318",
          "code": "rest_client.patch("
        },
        {
          "at": "scripts/hyperagent_test.py:1574",
          "code": "r = httpx.post("
        },
        {
          "at": "scripts/hyperagent_test.py:1604",
          "code": "rest_admin.post("
        },
        {
          "at": "scripts/repro_contradictions_collision.py:140",
          "code": "r = client.post(\"/api/v1/memories\", json=body_a)"
        },
        {
          "at": "scripts/repro_contradictions_collision.py:146",
          "code": "r = client.post(\"/api/v1/memories\", json=body_b)"
        },
        {
          "at": "scripts/repro_contradictions_collision.py:155",
          "code": "r = client.get(f\"/api/v1/memories/{mem_a['id']}\", params=qp)"
        },
        {
          "at": "scripts/repro_contradictions_collision.py:158",
          "code": "r = client.get(f\"/api/v1/memories/{mem_b['id']}\", params=qp)"
        },
        {
          "at": "scripts/repro_contradictions_collision.py:161",
          "code": "r = client.get(f\"/api/v1/memories/{mem_a['id']}/contradictions\", params=qp)"
        },
        {
          "at": "scripts/repro_contradictions_collision.py:164",
          "code": "r = client.get(f\"/api/v1/memories/{mem_b['id']}/contradictions\", params=qp)"
        },
        {
          "at": "scripts/repro_contradictions_diagnostic.py:85",
          "code": "r = client.post("
        },
        {
          "at": "scripts/repro_contradictions_diagnostic.py:91",
          "code": "r = client.post("
        },
        {
          "at": "scripts/repro_contradictions_diagnostic.py:105",
          "code": "a_now = client.get(f\"/api/v1/memories/{a['id']}\", params=qp).json()"
        },
        {
          "at": "scripts/repro_contradictions_diagnostic.py:106",
          "code": "b_now = client.get(f\"/api/v1/memories/{b['id']}\", params=qp).json()"
        },
        {
          "at": "scripts/repro_contradictions_diagnostic.py:141",
          "code": "sresp = client.post(\"/api/v1/search\", json=search_body)"
        },
        {
          "at": "scripts/repro_contradictions_diagnostic.py:165",
          "code": "eresp = client.post(\"/api/v1/entities/upsert\", json=ent_body)"
        },
        {
          "at": "scripts/repro_contradictions_diagnostic.py:175",
          "code": "r = client.post("
        },
        {
          "at": "scripts/repro_contradictions_diagnostic.py:192",
          "code": "cfetched = client.get("
        },
        {
          "at": "scripts/repro_contradictions_not_detected.py:98",
          "code": "r = client.post(\"/api/v1/memories\", json=body_a)"
        },
        {
          "at": "scripts/repro_contradictions_not_detected.py:109",
          "code": "r = client.post(\"/api/v1/memories\", json=body_b)"
        },
        {
          "at": "scripts/repro_contradictions_not_detected.py:130",
          "code": "a_now = client.get(f\"/api/v1/memories/{mem_a['id']}\", params=qp).json()"
        },
        {
          "at": "scripts/repro_contradictions_not_detected.py:131",
          "code": "b_now = client.get(f\"/api/v1/memories/{mem_b['id']}\", params=qp).json()"
        },
        {
          "at": "scripts/repro_contradictions_not_detected.py:132",
          "code": "a_contra = client.get("
        },
        {
          "at": "scripts/repro_contradictions_not_detected.py:135",
          "code": "b_contra = client.get("
        },
        {
          "at": "scripts/repro_contradictions_proper_noun.py:126",
          "code": "r = client.post(\"/api/v1/memories\", json=body_a)"
        },
        {
          "at": "scripts/repro_contradictions_proper_noun.py:129",
          "code": "r = client.post(\"/api/v1/memories\", json=body_b)"
        },
        {
          "at": "scripts/repro_contradictions_proper_noun.py:139",
          "code": "r = client.get(f\"/api/v1/memories/{mem_a['id']}\", params=qp)"
        },
        {
          "at": "scripts/repro_contradictions_proper_noun.py:142",
          "code": "r = client.get(f\"/api/v1/memories/{mem_b['id']}\", params=qp)"
        },
        {
          "at": "scripts/repro_contradictions_proper_noun.py:145",
          "code": "r = client.get(f\"/api/v1/memories/{mem_a['id']}/contradictions\", params=qp)"
        },
        {
          "at": "scripts/repro_contradictions_proper_noun.py:148",
          "code": "r = client.get(f\"/api/v1/memories/{mem_b['id']}/contradictions\", params=qp)"
        },
        {
          "at": "scripts/repro_contradictions_race.py:115",
          "code": "r = client.post(\"/api/v1/memories\", json=body_a)"
        },
        {
          "at": "scripts/repro_contradictions_race.py:120",
          "code": "r = client.post(\"/api/v1/memories\", json=body_b)"
        },
        {
          "at": "scripts/repro_contradictions_race.py:138",
          "code": "r = client.get(f\"/api/v1/memories/{mem_a['id']}/contradictions\", params=qp)"
        },
        {
          "at": "scripts/repro_contradictions_race.py:141",
          "code": "r = client.get(f\"/api/v1/memories/{mem_b['id']}/contradictions\", params=qp)"
        },
        {
          "at": "scripts/repro_contradictions_race.py:155",
          "code": "r = client.get(f\"/api/v1/memories/{mem_a['id']}\", params=qp)"
        },
        {
          "at": "scripts/repro_contradictions_race.py:158",
          "code": "r = client.get(f\"/api/v1/memories/{mem_b['id']}\", params=qp)"
        }
      ],
      "decorators_refused_judgement": []
    }
  ],
  "ghi_chu": [
    "Chỉ đọc gói và source caura-ai_caura; không sửa file, không chạy code repo, không đọc slice/, HANDOFF, docs/ hoặc .aide/. Các đường dẫn source là tương đối từ D:/VSF/l3-heldout-repos3/caura-ai_caura.",
    "get_auth_context, called=false: params=[] là đúng. Chữ ký chỉ có request: Request và key=Security(api_key_header), không có tham số header/query/cookie/path do Depends thêm: core-api/src/core_api/auth.py:640, core-api/src/core_api/auth.py:641, core-api/src/core_api/auth.py:642. APIKeyHeader thuộc securitySchemes: core-api/src/core_api/auth.py:19; tên X-API-Key tại core-api/src/core_api/constants.py:977. Các request.headers.get trong thân hàm không tự trở thành tham số OpenAPI, ví dụ core-api/src/core_api/auth.py:647 và core-api/src/core_api/auth.py:666.",
    "get_session, called=false: params=[] là đúng. Import của route trỏ tới database.init, không phải hàm trùng tên trong services.postgres_service: core-storage-api/src/core_storage_api/routers/debug.py:33. Hàm đúng không nhận đối số và yield AsyncSession: core-storage-api/src/core_storage_api/database/init.py:164, core-storage-api/src/core_storage_api/database/init.py:168. params_dung=0 là số tham số, không phải số dependency đúng.",
    "Dependency router bị bỏ sót _require_debug_endpoints không nhận tham số request; đây là thiếu mục dependency, không phải thiếu parameter: core-storage-api/src/core_storage_api/routers/debug.py:36, core-storage-api/src/core_storage_api/routers/debug.py:42.",
    "Mẫu core-api gồm 25 route, tính riêng alias dấu / của skills-inbox. Vị trí decorator: core-api/src/core_api/routes/agents.py:14; core-api/src/core_api/routes/audit.py:31; core-api/src/core_api/routes/conflicts.py:52; core-api/src/core_api/routes/crystallizer.py:54; core-api/src/core_api/routes/documents.py:404; core-api/src/core_api/routes/entities.py:63; core-api/src/core_api/routes/evolve.py:96; core-api/src/core_api/routes/fleet.py:397; core-api/src/core_api/routes/health.py:36; core-api/src/core_api/routes/insights.py:66; core-api/src/core_api/routes/interview.py:151; core-api/src/core_api/routes/keystones.py:344; core-api/src/core_api/routes/lifecycle.py:272; core-api/src/core_api/routes/memories.py:323; core-api/src/core_api/routes/org_deletion.py:90; core-api/src/core_api/routes/plugin.py:146; core-api/src/core_api/routes/reports.py:198; core-api/src/core_api/routes/scheduler_lease.py:88; core-api/src/core_api/routes/settings.py:35; core-api/src/core_api/routes/skills_inbox.py:644; core-api/src/core_api/routes/skills_inbox.py:645; core-api/src/core_api/routes/stats.py:38; core-api/src/core_api/routes/stm.py:241; core-api/src/core_api/routes/telemetry.py:27; core-api/src/core_api/routes/testing.py:81.",
    "Sáu route còn lại trong mẫu: core-storage-api/src/core_storage_api/routers/agents.py:14; core-storage-api/src/core_storage_api/routers/debug.py:117; core-operations/src/core_operations/app.py:315; core-operations/src/core_operations/app.py:319; core-worker/src/core_worker/app.py:141; core-worker/src/core_worker/app.py:145. Tổng mẫu là 31, không lấy số route_decorators trong gói làm số đã kiểm.",
    "Cấp app: không có dependencies ở bốn constructor đã đọc: core-api/src/core_api/app.py:782; core-storage-api/src/core_storage_api/app.py:177; core-operations/src/core_operations/app.py:305; core-worker/src/core_worker/app.py:129. Cấp router: dependency thiếu nằm ở debug.py:42 như items; các include_router liên quan không bổ sung dependency: core-api/src/core_api/app.py:1208, core-api/src/core_api/app.py:1229, core-api/src/core_api/app.py:1253; core-storage-api/src/core_storage_api/app.py:320, core-storage-api/src/core_storage_api/app.py:364.",
    "Phân loại từng suspect http_that, nhóm client: clients/python/src/caura_client/client.py:248; common/ranking/providers/remote.py:175; core-api/src/core_api/clients/storage_client.py:594; core-api/src/core_api/clients/storage_client.py:621; core-api/src/core_api/clients/storage_client.py:636; core-api/src/core_api/clients/storage_client.py:683; core-api/src/core_api/clients/storage_client.py:698; core-api/src/core_api/clients/storage_client.py:723; core-api/src/core_api/clients/storage_client.py:2911; core-api/src/core_api/clients/storage_client.py:3197. Nguồn client httpx được xác nhận tại clients/python/src/caura_client/client.py:99, common/ranking/providers/remote.py:96, core-api/src/core_api/clients/storage_client.py:345, core-api/src/core_api/clients/storage_client.py:356, core-api/src/core_api/clients/storage_client.py:396.",
    "Phân loại từng suspect http_that, nhóm còn lại: core-api/src/core_api/heartbeat/sender.py:383; core-api/src/core_api/services/ingest_service.py:615; core-operations/src/core_operations/lease.py:61; core-operations/src/core_operations/tasks.py:51; core-operations/src/core_operations/tasks.py:130; core-operations/src/core_operations/tasks.py:205; core-operations/src/core_operations/tasks.py:394; core-operations/src/core_operations/tasks.py:512; core-operations/src/core_operations/tasks.py:567. Client của ingest được khai kiểu httpx.AsyncClient tại core-api/src/core_api/services/ingest_service.py:607 và tạo tại core-api/src/core_api/services/ingest_service.py:841.",
    "Phân loại từng suspect http_khac: benchmark/a37_n_way_chain.py:26 và benchmark/a66_subject_stability.py:27 đều gọi urllib.request.urlopen; import tương ứng tại benchmark/a37_n_way_chain.py:12 và benchmark/a66_subject_stability.py:13.",
    "Phân loại từng suspect registration: core-api/src/core_api/routes/plugin.py:1041; core-api/src/core_api/routes/plugin.py:1049; core-api/src/core_api/routes/plugin.py:1050; core-api/src/core_api/routes/plugin.py:1056. Receiver là APIRouter được tạo tại core-api/src/core_api/routes/plugin.py:1040, được mount tại core-api/src/core_api/app.py:1237. Không có suspect nhiễu hoặc chỉ cần giải thích.",
    "Hai lời gọi super().request bị bỏ sót thực sự gọi requests.Session.request: lớp cha tại core-api/src/core_api/clients/identity_token.py:98 và core-worker/src/core_worker/clients/identity_token.py:99. Hai lời gọi fn bị bỏ sót gọi bound method httpx, ví dụ client.get được truyền tại core-worker/src/core_worker/clients/storage_client.py:163 và core-worker/src/core_worker/clients/storage_client.py:164; nguồn AsyncClient tại core-worker/src/core_worker/clients/storage_client.py:61. Đếm tại dòng thực thi fn, không đếm thêm mỗi nơi truyền method.",
    "scripts/latency_test.py:87 thực thi bound method client.post được truyền ở scripts/latency_test.py:140, scripts/latency_test.py:174 và scripts/latency_test.py:197; client được tạo ở scripts/latency_test.py:104. Chỉ đếm dòng thực thi func một lần. Wrapper gọi callback ở common/http_retry.py:137 không được đếm thêm cho các HTTP call site đã xác định.",
    "Phạm vi HTTP đã quét văn bản toàn repo bằng rg cho httpx/requests/aiohttp, loại tests/, test_*.py, conftest.py và các thư mục cấm. Không đưa các script tự xác định là test vào http_bo_sot: scripts/smoke_test.py:2; scripts/gateway_integration_test.py:2; scripts/wet_test_triple_emission.py:2; scripts/repro_contradictions_with_entity_links.py:2.",
    "Các script benchmark và chẩn đoán ngoài mẫu tên loại trừ được giữ trong phạm vi: scripts/benchmark_nano_vs_flash.py:2; scripts/latency_test.py:2; scripts/hyperagent_test.py:2; scripts/entity_retrieval_probe.py:2; scripts/repro_contradictions_collision.py:2; scripts/repro_contradictions_diagnostic.py:2; scripts/repro_contradictions_not_detected.py:2; scripts/repro_contradictions_proper_noun.py:2; scripts/repro_contradictions_race.py:2. Vì vậy http_bo_sot gồm cả công cụ benchmark/chẩn đoán, không chỉ dịch vụ production.",
    "Không tính việc khởi tạo transport hoặc gọi SDK OpenAI là call trực tiếp qua httpx/requests/aiohttp: common/embedding/providers/openai.py:158 và common/embedding/providers/openai.py:167; common/llm/providers/openai.py:187. Hai module này còn import httpx2 dưới tên httpx: common/embedding/providers/openai.py:8; common/llm/providers/openai.py:23."
  ]
}
```