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
        "routes_kiem": 30,
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
        "http_that": 31,
        "http_khac": 2,
        "registration": 4,
        "can_giai_thich": 0,
        "nhieu": []
      },
      "http_bo_sot": [
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
        },
        {
          "at": "scripts/repro_contradictions_with_entity_links.py:71",
          "code": "ent_resp = client.post("
        },
        {
          "at": "scripts/repro_contradictions_with_entity_links.py:97",
          "code": "a_resp = client.post("
        },
        {
          "at": "scripts/repro_contradictions_with_entity_links.py:109",
          "code": "b_resp = client.post("
        },
        {
          "at": "scripts/repro_contradictions_with_entity_links.py:123",
          "code": "a_now = client.get(f\"/api/v1/memories/{a['id']}\", params=qp).json()"
        },
        {
          "at": "scripts/repro_contradictions_with_entity_links.py:124",
          "code": "b_now = client.get(f\"/api/v1/memories/{b['id']}\", params=qp).json()"
        }
      ],
      "decorators_refused_judgement": []
    }
  ],
  "ghi_chu": [
    "Giả định phạm vi cần lưu ý: hiểu 'import code của repo' bao gồm helper scripts/_env_compat.py, có định nghĩa tại scripts/_env_compat.py:26. Sáu script import helper tại scripts/repro_contradictions_collision.py:52; scripts/repro_contradictions_diagnostic.py:39; scripts/repro_contradictions_not_detected.py:48; scripts/repro_contradictions_proper_noun.py:57; scripts/repro_contradictions_race.py:68; scripts/repro_contradictions_with_entity_links.py:34. Vì vậy 37 lời gọi trong http_bo_sot được tính trong phạm vi. Nếu FR-028 chỉ tính import package ứng dụng, loại cả 37 mục này; khi đó không phát hiện HTTP trực tiếp bị bỏ sót trong phần còn lại đã quét.",
    "Nguồn receiver của 37 lời gọi trên là httpx.Client: scripts/repro_contradictions_collision.py:117; scripts/repro_contradictions_diagnostic.py:70; scripts/repro_contradictions_not_detected.py:84; scripts/repro_contradictions_proper_noun.py:220; scripts/repro_contradictions_race.py:246; scripts/repro_contradictions_with_entity_links.py:52.",
    "get_auth_context, called=false: danh sách tham số request đúng là []; gói đúng. Chữ ký chỉ có request: Request và key=Security(api_key_header), tại core-api/src/core_api/auth.py:640, core-api/src/core_api/auth.py:641, core-api/src/core_api/auth.py:642. APIKeyHeader được tạo tại core-api/src/core_api/auth.py:19, thuộc auth/securitySchemes. Các header đọc thủ công tại core-api/src/core_api/auth.py:647, core-api/src/core_api/auth.py:666, core-api/src/core_api/auth.py:671 không phải tham số FastAPI tự thêm từ Header.",
    "get_session, called=false: danh sách tham số request đúng là []; gói đúng. Route import từ database.init tại core-storage-api/src/core_storage_api/routers/debug.py:33; định nghĩa không đối số tại core-storage-api/src/core_storage_api/database/init.py:164 và yield AsyncSession tại core-storage-api/src/core_storage_api/database/init.py:168. Không nhầm với hàm cùng tên trong services/postgres_service.py. params_dung=0 là số tham số, không phải số dependency đúng.",
    "Dependency router bị bỏ sót _require_debug_endpoints không sinh tham số request: chữ ký rỗng tại core-storage-api/src/core_storage_api/routers/debug.py:36. Đây là thiếu mục dependency, không phải thiếu header/query/cookie/path.",
    "Mẫu core-api gồm 15 route, mỗi route một module: GET /agents tại core-api/src/core_api/routes/agents.py:14; GET /audit-log tại core-api/src/core_api/routes/audit.py:31; GET /conflicts tại core-api/src/core_api/routes/conflicts.py:52; POST /crystallize tại core-api/src/core_api/routes/crystallizer.py:54; POST /documents tại core-api/src/core_api/routes/documents.py:404; GET /entities tại core-api/src/core_api/routes/entities.py:63; POST /evolve/report tại core-api/src/core_api/routes/evolve.py:96; POST /fleet tại core-api/src/core_api/routes/fleet.py:397; GET /version tại core-api/src/core_api/routes/health.py:36 và core-api/src/core_api/constants.py:263; POST /insights/generate tại core-api/src/core_api/routes/insights.py:66; POST /interview/submit tại core-api/src/core_api/routes/interview.py:151; GET /keystones tại core-api/src/core_api/routes/keystones.py:93 và core-api/src/core_api/routes/keystones.py:344; POST /admin/lifecycle/fanout/{action} tại core-api/src/core_api/routes/lifecycle.py:272; GET /tenants tại core-api/src/core_api/routes/memories.py:323; GET /settings tại core-api/src/core_api/routes/settings.py:35. Các route này được gắn prefix /api/v1 tại core-api/src/core_api/app.py:1208, core-api/src/core_api/app.py:1223, core-api/src/core_api/app.py:1234, core-api/src/core_api/app.py:1241.",
    "Trong 15 route core-api đã đọc, /version không có dependency; 14 route còn lại dùng get_auth_context ở handler, đều có trong gói: core-api/src/core_api/routes/health.py:37; core-api/src/core_api/routes/agents.py:18; core-api/src/core_api/routes/audit.py:61; core-api/src/core_api/routes/conflicts.py:61; core-api/src/core_api/routes/crystallizer.py:57; core-api/src/core_api/routes/documents.py:412; core-api/src/core_api/routes/entities.py:71; core-api/src/core_api/routes/evolve.py:99; core-api/src/core_api/routes/fleet.py:404; core-api/src/core_api/routes/insights.py:69; core-api/src/core_api/routes/interview.py:154; core-api/src/core_api/routes/keystones.py:361; core-api/src/core_api/routes/lifecycle.py:275; core-api/src/core_api/routes/memories.py:325; core-api/src/core_api/routes/settings.py:38.",
    "Mẫu core-storage-api gồm 15 route, mỗi route một module: POST /agents tại core-storage-api/src/core_storage_api/routers/agents.py:14; POST /audit-logs tại core-storage-api/src/core_storage_api/routers/audit.py:67; POST /capability-usage tại core-storage-api/src/core_storage_api/routers/capability_usage.py:27; GET /_debug/pg_locks tại core-storage-api/src/core_storage_api/routers/debug.py:117; POST /documents tại core-storage-api/src/core_storage_api/routers/documents.py:16; POST /entities tại core-storage-api/src/core_storage_api/routers/entities.py:55; POST /evolve/filter-by-scope tại core-storage-api/src/core_storage_api/routers/evolve.py:42; GET /fleet tại core-storage-api/src/core_storage_api/routers/fleet.py:23; GET /healthz tại core-storage-api/src/core_storage_api/routers/health.py:32; GET /idempotency tại core-storage-api/src/core_storage_api/routers/idempotency.py:33; POST /insights/contradictions tại core-storage-api/src/core_storage_api/routers/insights.py:87; GET /keystones tại core-storage-api/src/core_storage_api/routers/keystones.py:229; POST /lifecycle-audit tại core-storage-api/src/core_storage_api/routers/lifecycle_audit.py:21; POST /memories tại core-storage-api/src/core_storage_api/routers/memories.py:91; GET /organization-settings/{org_id} tại core-storage-api/src/core_storage_api/routers/organization_settings.py:32. Prefix storage được đặt tại core-storage-api/src/core_storage_api/app.py:314; health còn được gắn ở root tại core-storage-api/src/core_storage_api/app.py:312. Chỉ route debug trong mẫu có Depends ở handler và router.",
    "Cấp app: không có dependencies truyền vào hai FastAPI constructor của mẫu, tại core-api/src/core_api/app.py:782 và core-storage-api/src/core_storage_api/app.py:177. Các include_router đã đọc không thêm dependency; ví dụ core-api/src/core_api/app.py:1214 và core-storage-api/src/core_storage_api/app.py:364. Không phát hiện dependency thiếu ở cấp handler/decorator/app trong 30 route đã kiểm.",
    "Phân loại http_that: clients/python/src/caura_client/client.py:248 gọi self._http.request, receiver tạo bằng httpx.Client tại clients/python/src/caura_client/client.py:99; common/ranking/providers/remote.py:175 gọi self._client.post, receiver tạo bằng httpx.AsyncClient tại common/ranking/providers/remote.py:96.",
    "Phân loại http_that cho hai super().request: core-api/src/core_api/clients/identity_token.py:101 và core-worker/src/core_worker/clients/identity_token.py:102. Lớp cha là requests.Session tại core-api/src/core_api/clients/identity_token.py:98 và core-worker/src/core_worker/clients/identity_token.py:99.",
    "Phân loại http_that cho tám lời gọi storage của core-api: core-api/src/core_api/clients/storage_client.py:594; core-api/src/core_api/clients/storage_client.py:621; core-api/src/core_api/clients/storage_client.py:636; core-api/src/core_api/clients/storage_client.py:683; core-api/src/core_api/clients/storage_client.py:698; core-api/src/core_api/clients/storage_client.py:723; core-api/src/core_api/clients/storage_client.py:2911; core-api/src/core_api/clients/storage_client.py:3197. Receiver được gán tại core-api/src/core_api/clients/storage_client.py:345, core-api/src/core_api/clients/storage_client.py:356, core-api/src/core_api/clients/storage_client.py:364; factory tạo httpx.AsyncClient tại core-api/src/core_api/clients/storage_client.py:396.",
    "Phân loại http_that: core-api/src/core_api/heartbeat/sender.py:383, receiver httpx.AsyncClient tại core-api/src/core_api/heartbeat/sender.py:382; core-api/src/core_api/services/ingest_service.py:615 gọi client.send(stream=True), annotation tại core-api/src/core_api/services/ingest_service.py:607 và client tạo tại core-api/src/core_api/services/ingest_service.py:841.",
    "Phân loại http_that cho bảy lời gọi core-operations: core-operations/src/core_operations/lease.py:61; core-operations/src/core_operations/tasks.py:51; core-operations/src/core_operations/tasks.py:130; core-operations/src/core_operations/tasks.py:205; core-operations/src/core_operations/tasks.py:394; core-operations/src/core_operations/tasks.py:512; core-operations/src/core_operations/tasks.py:567. Mỗi receiver nằm trong context httpx.AsyncClient, lần lượt tại core-operations/src/core_operations/lease.py:60; core-operations/src/core_operations/tasks.py:48; core-operations/src/core_operations/tasks.py:128; core-operations/src/core_operations/tasks.py:203; core-operations/src/core_operations/tasks.py:392; core-operations/src/core_operations/tasks.py:510; core-operations/src/core_operations/tasks.py:565.",
    "Phân loại http_that cho cả mười _signed_call trong gói: core-worker/src/core_worker/clients/storage_client.py:163; core-worker/src/core_worker/clients/storage_client.py:235; core-worker/src/core_worker/clients/storage_client.py:305; core-worker/src/core_worker/clients/storage_client.py:350; core-worker/src/core_worker/clients/storage_client.py:373; core-worker/src/core_worker/clients/storage_client.py:402; core-worker/src/core_worker/clients/storage_client.py:428; core-worker/src/core_worker/clients/storage_client.py:460; core-worker/src/core_worker/clients/storage_client.py:498; core-worker/src/core_worker/clients/storage_client.py:551. Mỗi dòng ngay sau truyền client.get/post/patch; receiver là httpx.AsyncClient, được tạo tại core-worker/src/core_worker/clients/storage_client.py:61. Chênh một dòng được coi là đã có trong suspects.",
    "Phân loại http_khac: benchmark/a37_n_way_chain.py:26 và benchmark/a66_subject_stability.py:27 đều gọi urllib.request.urlopen. Phân loại registration: core-api/src/core_api/routes/plugin.py:1041; core-api/src/core_api/routes/plugin.py:1049; core-api/src/core_api/routes/plugin.py:1050; core-api/src/core_api/routes/plugin.py:1056. Receiver được tạo bằng APIRouter tại core-api/src/core_api/routes/plugin.py:1040. Như vậy đã phân loại đủ từng mục trong 37 suspects, không có nhiễu.",
    "Các lời gọi qua hàm bọc được tách khỏi HTTP trực tiếp: clients/python/src/caura_client/client.py:242 gọi self._request; core-worker/src/core_worker/backfill.py:104 gọi get_memory và core-worker/src/core_worker/backfill.py:131 gọi iter_memories_with_null_embedding; core-worker/src/core_worker/lifecycle.py:24 gọi archive_expired; core-worker/src/core_worker/lifecycle.py:27 gọi archive_stale; core-api/src/core_api/services/ingest_service.py:859 gọi _stream_request. client.build_request tại core-api/src/core_api/services/ingest_service.py:853 chỉ tạo request. Các callback fn trong _signed_call tại core-worker/src/core_worker/clients/storage_client.py:128 và core-worker/src/core_worker/clients/storage_client.py:138 không được đếm thêm một lần nữa.",
    "Các script không import code nội bộ được loại theo FR-028: scripts/benchmark_nano_vs_flash.py:13, scripts/benchmark_nano_vs_flash.py:19; scripts/entity_retrieval_probe.py:84, scripts/entity_retrieval_probe.py:95; scripts/wet_test_triple_emission.py:45, scripts/wet_test_triple_emission.py:53. Không đưa HTTP của chúng vào http_bo_sot. Test cũng được loại khỏi phép quét. Chỉ đọc văn bản bằng rg/Get-Content; không sửa file, không chạy code repo, không đọc bộ kiểm hoặc các thư mục bị cấm."
  ]
}
```