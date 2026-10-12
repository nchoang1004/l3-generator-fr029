```json
{
  "repos": [
    {
      "repo": "primerhq_primer",
      "dependencies": {
        "params_dung": 4,
        "params_sai": [],
        "params_thieu": []
      },
      "deps_bo_sot": {
        "routes_kiem": 31,
        "items": [
          {
            "route": "POST /v1/artifact_storage_providers",
            "dependency": "get_artifact_storage_provider_storage",
            "cap": "handler",
            "source": "primer/api/routers/artifact_storage.py:46; primer/api/routers/_crud.py:545; primer/api/deps.py:140"
          },
          {
            "route": "POST /v1/embedding_providers",
            "dependency": "get_embedding_provider_storage",
            "cap": "handler",
            "source": "primer/api/routers/providers.py:811; primer/api/routers/_crud.py:545; primer/api/deps.py:213"
          },
          {
            "route": "POST /v1/cross_encoder_providers",
            "dependency": "get_cross_encoder_provider_storage",
            "cap": "handler",
            "source": "primer/api/routers/providers.py:988; primer/api/routers/_crud.py:545; primer/api/deps.py:219"
          },
          {
            "route": "POST /v1/documents",
            "dependency": "get_document_storage",
            "cap": "handler",
            "source": "primer/api/routers/knowledge.py:956; primer/api/routers/_crud.py:545; primer/api/deps.py:267"
          },
          {
            "route": "POST /v1/channel_providers",
            "dependency": "_get_channel_provider_storage",
            "cap": "handler",
            "source": "primer/api/routers/channels.py:127; primer/api/routers/_crud.py:545; primer/api/routers/channels.py:29"
          },
          {
            "route": "POST /v1/channels",
            "dependency": "_get_channel_storage",
            "cap": "handler",
            "source": "primer/api/routers/channels.py:190; primer/api/routers/_crud.py:545; primer/api/routers/channels.py:33"
          },
          {
            "route": "POST /v1/stt_providers",
            "dependency": "_stt_storage",
            "cap": "handler",
            "source": "primer/api/routers/speech.py:260; primer/api/routers/_crud.py:545; primer/api/routers/speech.py:43"
          },
          {
            "route": "POST /v1/tts_providers",
            "dependency": "_tts_storage",
            "cap": "handler",
            "source": "primer/api/routers/speech.py:271; primer/api/routers/_crud.py:545; primer/api/routers/speech.py:47"
          },
          {
            "route": "POST /v1/tool_approval_policies",
            "dependency": "_get_tool_approval_policy_storage",
            "cap": "handler",
            "source": "primer/api/routers/tool_approval.py:387; primer/api/routers/tool_approval.py:47; primer/api/routers/_crud.py:545; primer/api/routers/tool_approval.py:51"
          },
          {
            "route": "POST /v1/web_fetch_providers",
            "dependency": "_web_fetch_provider_storage",
            "cap": "handler",
            "source": "primer/api/routers/web_fetch.py:224; primer/api/routers/_crud.py:545; primer/api/routers/web_fetch.py:48"
          },
          {
            "route": "POST /v1/web_search_providers",
            "dependency": "_web_search_provider_storage",
            "cap": "handler",
            "source": "primer/api/routers/web_search.py:227; primer/api/routers/_crud.py:545; primer/api/routers/web_search.py:48"
          }
        ]
      },
      "suspects": {
        "http_that": 26,
        "http_khac": 0,
        "registration": 1,
        "can_giai_thich": 0,
        "nhieu": [
          {
            "at": "primer/channel/slack/adapter.py:228",
            "ly_do": "Tra cứu bộ nhớ bằng self._session_threads.get(session_id). Thuộc tính được tạo bằng BoundedDict tại primer/channel/slack/adapter.py:76; BoundedDict kế thừa OrderedDict tại primer/channel/adapter.py:30. Không phải HTTP hay session CSDL."
          }
        ]
      },
      "http_bo_sot": [],
      "decorators_refused_judgement": []
    }
  ],
  "ghi_chu": [
    "Chỉ đọc gói và source của primerhq_primer; không sửa file, không chạy code repo. Các đường dẫn source bên dưới tương đối với D:/VSF/l3-heldout-repos3/primerhq_primer. Phạm vi quét loại tests/, test_*.py, conftest.py và các thư mục bị cấm.",
    "Chấm từng tham số có trong gói: parse_page.query.limit đúng tại primer/api/pagination.py:19; parse_page.query.offset đúng tại primer/api/pagination.py:20; parse_page.query.cursor đúng tại primer/api/pagination.py:25; parse_order_by.query.order_by đúng tại primer/api/pagination.py:39.",
    "Các mục sau đúng với params=[] vì chỉ nhận Request, không khai báo header/query/cookie/path: get_storage_provider — primer/api/deps.py:76; get_provider_registry — primer/api/deps.py:81; get_semantic_search_registry — primer/api/deps.py:86; get_optional_artifact_storage_registry — primer/api/deps.py:128; get_workspace_registry — primer/api/deps.py:179; get_document_service — primer/api/deps.py:273; get_document_tree_service — primer/api/deps.py:288; get_scheduler — primer/api/deps.py:385; get_event_bus — primer/api/deps.py:400; get_approval_resolver — primer/api/deps.py:436; get_claim_engine — primer/api/deps.py:467; get_principal — primer/api/deps.py:477; require_auth — primer/api/deps.py:488; require_user — primer/api/deps.py:517; require_admin — primer/api/deps.py:544.",
    "Các mục sau đúng với params=[] vì tham số duy nhất là Depends(get_storage_provider), mà dependency lồng này chỉ nhận Request tại primer/api/deps.py:76: get_semantic_search_storage — primer/api/deps.py:107; get_event_subscription_storage — primer/api/deps.py:147; get_oidc_provider_storage — primer/api/deps.py:154; get_user_identity_storage — primer/api/deps.py:166; get_llm_provider_storage — primer/api/deps.py:195; get_user_storage — primer/api/deps.py:201; get_toolset_storage — primer/api/deps.py:225; get_agent_storage — primer/api/deps.py:231; get_model_profile_storage — primer/api/deps.py:237; get_graph_storage — primer/api/deps.py:243; get_service_storage — primer/api/deps.py:249; get_collection_storage — primer/api/deps.py:261; get_workspace_provider_storage — primer/api/deps.py:313; get_workspace_template_storage — primer/api/deps.py:319; get_workspace_storage — primer/api/deps.py:325; get_session_storage — primer/api/deps.py:331; get_external_tool_call_storage — primer/api/deps.py:337; get_internal_collections_config_storage — primer/api/deps.py:346; get_internal_collections_bootstrap_status_storage — primer/api/deps.py:352.",
    "storage_dep không phải hàm độc lập: đây là đối số callable của make_crud_router tại primer/api/routers/_crud.py:166, được đóng vào Depends tại primer/api/routers/_crud.py:370 và primer/api/routers/_crud.py:545. params=[] phù hợp với các binding đã đối chiếu. 11 mục deps_bo_sot là thiếu tên hàm cụ thể trong danh sách gói, không phải thiếu tham số request: chúng chỉ nhận Request hoặc Depends(get_storage_provider), như các định nghĩa được dẫn trong từng item. Không tính các tham số factory model_cls/plural/tag hoặc entity=Body(...) tại primer/api/routers/_crud.py:544 thành query.",
    "31 route mẫu gồm 11 route CRUD POST nêu trong deps_bo_sot và 20 route khai báo trực tiếp. 10 route trực tiếp đầu: GET /v1/admin/users/{user_id}/tokens — primer/api/routers/admin_tokens.py:43; POST /v1/admin/users — primer/api/routers/admin_users.py:296; GET /v1/auth/status — primer/api/routers/auth.py:190; GET /v1/agents/{agent_id}/status — primer/api/routers/compute.py:61; GET /v1/events — primer/api/routers/events.py:60; GET /v1/sessions/{session_id}/external_tools/pending — primer/api/routers/external_tools.py:92; POST /v1/harnesses — primer/api/routers/harness.py:101; PUT /v1/internal_collections/config — primer/api/routers/internal_collections.py:172; GET /v1/collections/{collection_id}/docs — primer/api/routers/knowledge.py:182; GET /v1/mcp_exposure — primer/api/routers/mcp_exposure.py:82.",
    "10 route trực tiếp còn lại: GET /v1/ssp/_types — primer/api/routers/semantic_search.py:141; POST /v1/services/{service_id}/versions — primer/api/routers/services.py:123; POST /v1/workspaces/{workspace_id}/sessions — primer/api/routers/sessions.py:129; GET /v1/auth/sso/providers — primer/api/routers/sso.py:364; GET /v1/tools/catalogue — primer/api/routers/tools.py:55; GET /v1/workers — primer/api/routers/workers.py:29; GET /v1/workspaces — primer/api/routers/workspaces.py:637; GET /v1/sessions/{session_id}/ask_user/pending — primer/api/routers/yields.py:215; POST /v1/auth/tokens — primer/api/routers/api_tokens.py:136; PUT /v1/mcp_exposure — primer/api/routers/mcp_exposure.py:98. Các dependency handler/decorator của 20 route này đều có tên trong gói.",
    "Cấp router được kiểm riêng: require_admin và require_user được đóng thành admin_dep/user_dep tại primer/api/_app_routes.py:98 và primer/api/_app_routes.py:99, rồi gắn bằng include_router, ví dụ primer/api/_app_routes.py:107, primer/api/_app_routes.py:145, primer/api/_app_routes.py:206, primer/api/_app_routes.py:258, primer/api/_app_routes.py:269, primer/api/_app_routes.py:270. Cả hai dependency đã có trong gói và không thêm tham số request. Cấp app không khai báo dependencies trong FastAPI(...) tại primer/api/app.py:119. Cấp decorator của PUT /v1/mcp_exposure có Depends(require_admin) tại primer/api/routers/mcp_exposure.py:98, cũng đã có trong gói.",
    "Phân loại http_that qua httpx, từng suspect: primer/api/routers/providers.py:955; primer/auth/oidc.py:156; primer/auth/oidc.py:252; primer/auth/oidc.py:432; primer/channel/slack/adapter.py:274; primer/llm/anthropic.py:894; primer/llm/gemini.py:129; primer/llm/openrouter.py:363; primer/speech/discovery.py:30. Mỗi lời gọi dùng client được tạo bằng httpx.AsyncClient trong cùng khối.",
    "Phân loại http_that qua httpx, từng suspect tiếp theo: primer/toolset/oauth/discovery.py:91; primer/toolset/oauth/discovery.py:111; primer/toolset/oauth/discovery.py:226; primer/toolset/oauth/registration.py:103; primer/toolset/web/tools.py:344; primer/toolset/web/tools.py:505. Kiểu client được khai báo tại primer/toolset/oauth/discovery.py:87, primer/toolset/oauth/discovery.py:107, primer/toolset/oauth/discovery.py:216, primer/toolset/oauth/registration.py:93, primer/toolset/web/tools.py:321 và primer/toolset/web/tools.py:438.",
    "Phân loại http_that qua httpx, từng suspect tiếp theo: primer/web_fetch/exa.py:33; primer/web_fetch/firecrawl.py:33; primer/web_fetch/jina.py:34; primer/web_fetch/local.py:70; primer/web_search/exa.py:107; primer/web_search/firecrawl.py:95; primer/web_search/tavily.py:89. self._client được nhận hoặc tạo dưới kiểu httpx.AsyncClient tại primer/web_fetch/exa.py:22, primer/web_fetch/firecrawl.py:22, primer/web_fetch/jina.py:22, primer/web_fetch/local.py:57, primer/web_search/exa.py:73, primer/web_search/firecrawl.py:66 và primer/web_search/tavily.py:62.",
    "Bốn suspect http_that còn lại: primer/workspace/files.py:94 dùng aiohttp.ClientSession từ primer/workspace/files.py:50; scripts/e2e/seed_staged_fixtures.py:210, scripts/e2e/seed_staged_fixtures.py:213 và scripts/e2e/seed_staged_fixtures.py:216 dùng self.c, được nhận từ httpx.AsyncClient tại scripts/e2e/seed_staged_fixtures.py:206. File seed này không thuộc các đường dẫn test bị loại theo quy ước.",
    "Suspect primer/api/routers/terminal.py:152 được xếp registration: đó là decorator đăng ký WebSocket trên APIRouter thật, receiver được tạo tại primer/api/routers/terminal.py:49. Đây là ngoại lệ so với mô tả rằng suspects không chứa decorator route; không phải lời gọi HTTP đi ra. decorators_refused của gói rỗng nên không có mục để phán xét.",
    "Sau quét văn bản toàn phạm vi source cho httpx/requests/aiohttp và đối chiếu các client, không tìm thấy lời gọi HTTP trực tiếp bị thiếu ngoài 26 vị trí đã liệt kê. primer/workspace/runtime/runtime_client.py:952 là aiohttp.ws_connect mở WebSocket, được ghi nhận riêng và không tính HTTP bỏ sót; primer/workspace/runtime/ws_sandbox.py:194 gọi RuntimeClient.delete, triển khai bằng giao thức runtime tại primer/workspace/runtime/runtime_client.py:288, không phải HTTP DELETE."
  ]
}
```