```json
{
  "repos": [
    {
      "repo": "xiao-villamor_PrintStash",
      "dependencies": {
        "params_dung": 2,
        "params_sai": [],
        "params_thieu": []
      },
      "deps_bo_sot": {
        "routes_kiem": 33,
        "items": [
          {
            "route": "GET /api/v1/models/{model_id}/similar-text",
            "dependency": "_reject_retired_group_queries",
            "cap": "router",
            "source": "backend/app/api/v1/models.py:181; backend/app/api/v1/models.py:192; định nghĩa tại backend/app/api/v1/models.py:169 chỉ nhận Request, không khai báo tham số query"
          },
          {
            "route": "WEBSOCKET /api/v1/printers/{printer_id}/ws",
            "dependency": "get_hub_from_ws",
            "cap": "handler",
            "source": "backend/app/api/v1/printers.py:1377; backend/app/api/v1/printers.py:1381; định nghĩa tại backend/app/bootstrap/dependencies.py:13 chỉ nhận WebSocket, không thêm tham số request"
          }
        ]
      },
      "suspects": {
        "http_that": 21,
        "http_khac": 0,
        "registration": 3,
        "can_giai_thich": 11,
        "nhieu": [
          {
            "at": "backend/app/core/http_client.py:37",
            "ly_do": "_clients.get(loop) là tra cứu WeakKeyDictionary; kiểu và khởi tạo tại backend/app/core/http_client.py:16."
          },
          {
            "at": "backend/app/modules/ingestion/capture_provider_transport.py:109",
            "ly_do": "_pooled_clients.get(key) là tra cứu dictionary chứa client; khai báo tại backend/app/modules/ingestion/capture_provider_transport.py:40."
          }
        ]
      },
      "http_bo_sot": [],
      "decorators_refused_judgement": []
    }
  ],
  "ghi_chu": [
    "Chỉ đọc gói và source PrintStash; không sửa file, không chạy code repo. Đường dẫn source dưới đây tính từ D:/VSF/l3-heldout-repos3/xiao-villamor_PrintStash.",
    "Đã chấm đủ 22 mục dependency và 37 suspects. decorators_refused rỗng, không có mục để phán xét: D:/VSF/l3-generator-l3/ket-qua-chay/fr029-heldout-20261008-r23/xiao-villamor_PrintStash.packet.json:5.",
    "edit_precondition: header if-match ĐÚNG, từ if_match và Header không đặt alias tại backend/app/api/edit_preconditions.py:11 và backend/app/api/edit_preconditions.py:13; header X-PrintStash-Edit-Contract ĐÚNG, alias khai rõ tại backend/app/api/edit_preconditions.py:18. Không có tham số khác.",
    "get_session: params=[] đúng, hàm không nhận đối số tại backend/app/db/session.py:284. get_hub: params=[] đúng, chỉ nhận Request tại backend/app/bootstrap/dependencies.py:8. require_feature: params=[] đúng, chỉ Depends(get_session) tại backend/app/api/v1/external_libraries.py:57.",
    "get_current_user, require_auth, require_user, require_superuser: params=[] đều đúng. Chữ ký và chuỗi Depends lần lượt tại backend/app/core/security.py:46, backend/app/core/security.py:70, backend/app/core/security.py:89, backend/app/core/security.py:105; dependency lồng get_token_payload tại backend/app/core/security.py:31 nhận Request và Depends(oauth2_scheme). Session và các giá trị trả về qua Depends không phải query/body tự động.",
    "oauth2_scheme: params=[] đúng. Đây là instance BearerToken kế thừa HTTPBearer tại backend/app/core/security.py:18 và backend/app/core/security.py:28; FastAPI đọc __call__(request: Request) tại backend/app/core/security.py:21. Authorization thuộc securitySchemes, không tính thiếu header parameter.",
    "require_command_user, require_command_writer, require_capture_actor: params=[] đều đúng; chữ ký tại backend/app/api/command_actor.py:73, backend/app/api/command_actor.py:86, backend/app/api/command_actor.py:96 chỉ chứa Depends hoặc Request. require_search_user: params=[] đúng, hai Depends tại backend/app/api/v1/search.py:34.",
    "_create_limit, _plan_limit, _chunk_limit, _finalize_limit, _native_part_limit: params=[] đều đúng; từng alias factory tại backend/app/api/v1/artifact_uploads.py:73, backend/app/api/v1/artifact_uploads.py:74, backend/app/api/v1/artifact_uploads.py:75, backend/app/api/v1/artifact_uploads.py:76, backend/app/api/v1/artifact_uploads.py:77. _login_rate_limit và _refresh_rate_limit: params=[] đúng, alias tại backend/app/api/v1/auth.py:57 và backend/app/api/v1/auth.py:58. _claim_limit: params=[] đúng, alias tại backend/app/api/v1/provider_connections.py:29. Tất cả trả về _dependency(request: Request) tại backend/app/core/ratelimit.py:64.",
    "rate_limit với called=true: params=[] đúng. Depends(rate_limit(30, 60)) tại backend/app/api/v1/setup.py:124 dùng hàm lồng được trả về tại backend/app/core/ratelimit.py:70; limit và window_s của factory tại backend/app/core/ratelimit.py:60 không phải query parameters.",
    "Mẫu 33 route gồm 32 HTTP và 1 WebSocket, trải trên 30 module. Nhóm đầu: backend/app/api/v1/admin.py:70; backend/app/api/v1/artifact_cache.py:24; backend/app/api/v1/artifact_uploads.py:191; backend/app/api/v1/auth.py:97; backend/app/api/v1/backup.py:50; backend/app/api/v1/captions.py:17; backend/app/api/v1/config.py:145; backend/app/api/v1/documents.py:176; backend/app/api/v1/external_libraries.py:231; backend/app/api/v1/filaments.py:43; backend/app/api/v1/files.py:120; backend/app/api/v1/fleet.py:63; backend/app/api/v1/health.py:404; backend/app/api/v1/inbox.py:56; backend/app/api/v1/inference.py:40; backend/app/api/v1/inference.py:41.",
    "Mẫu route còn lại: backend/app/api/v1/inference_models.py:37; backend/app/api/v1/ingest.py:194; backend/app/api/v1/jobs.py:45; backend/app/api/v1/maintenance.py:21; backend/app/api/v1/models.py:192; backend/app/api/v1/multipart_builds.py:26; backend/app/api/v1/multipart_models.py:137; backend/app/api/v1/notifications.py:83; backend/app/api/v1/outliner.py:50; backend/app/api/v1/printer_profiles.py:43; backend/app/api/v1/printers.py:350; backend/app/api/v1/provider_connections.py:44; backend/app/api/v1/saved_views.py:13; backend/app/api/v1/search.py:47; backend/app/api/v1/setup.py:63; backend/app/api/v1/setup.py:121; backend/app/api/v1/printers.py:1377.",
    "Cấp router đã kiểm riêng: require_superuser ở backend/app/api/v1/admin.py:48, backend/app/api/v1/artifact_cache.py:20, backend/app/api/v1/inference.py:33, backend/app/api/v1/inference.py:36, backend/app/api/v1/inference_models.py:33; require_auth ở backend/app/api/v1/outliner.py:20. Các tên này đều có trong gói. _reject_retired_group_queries ở backend/app/api/v1/models.py:181 chưa có; việc tự đọc request.query_params tại backend/app/api/v1/models.py:172 không làm FastAPI khai thêm query parameters.",
    "Cấp app: FastAPI tại backend/app/main.py:56 và include_router tại backend/app/main.py:243 không truyền dependencies. Router gốc tại backend/app/api/v1/__init__.py:46 và các include_router bắt đầu tại backend/app/api/v1/__init__.py:47 cũng không thêm dependency. Hai dependency ghi trong deps_bo_sot không làm thiếu tham số header/query/cookie/path; get_hub_from_ws chỉ áp dụng cho WebSocket.",
    "http_that, nhóm 1: backend/app/api/v1/health.py:380; backend/app/modules/administration/release_check.py:70; backend/app/modules/identity/oidc.py:69; backend/app/modules/identity/oidc.py:83; backend/app/modules/inference/http_runtime.py:104; backend/app/modules/inference/model_acquisition.py:103; backend/app/modules/ingestion/capture_provider_transport.py:70; backend/app/modules/ingestion/importer.py:167. Đây là lời gọi trực tiếp httpx hoặc phương thức client httpx; client dùng chung được tạo tại backend/app/core/http_client.py:24.",
    "http_that, nhóm 2: backend/app/modules/notifications/notifications.py:384; backend/app/modules/notifications/notifications.py:902; backend/app/modules/printing/moonraker.py:30; backend/app/modules/printing/moonraker.py:33; backend/app/modules/printing/spoolman.py:80; backend/app/modules/printing/spoolman.py:181; backend/app/modules/printing/spoolman.py:212; backend/app/modules/storage/remote_io_adapters.py:113; backend/app/modules/storage/webdav_listing.py:75. Factory của notifications trả httpx.AsyncClient tại backend/app/modules/notifications/notifications.py:95.",
    "http_that, nhóm 3: backend/packages/printstash-core/src/printstash_core/printers/moonraker.py:108; backend/packages/printstash-core/src/printstash_core/printers/moonraker.py:215; backend/packages/printstash-core/src/printstash_core/printers/octoprint.py:89; backend/packages/printstash-core/src/printstash_core/printers/prusalink.py:117. Factory mặc định là httpx.AsyncClient tại backend/packages/printstash-core/src/printstash_core/printers/moonraker.py:93, backend/packages/printstash-core/src/printstash_core/printers/octoprint.py:75, backend/packages/printstash-core/src/printstash_core/printers/prusalink.py:96.",
    "can_giai_thich: 10 thao tác session CSDL tại backend/app/modules/notifications/notifications.py:128; backend/app/modules/notifications/notifications.py:141; backend/app/modules/notifications/notifications.py:266; backend/app/modules/notifications/notifications.py:267; backend/app/modules/notifications/notifications.py:524; backend/app/modules/notifications/notifications.py:584; backend/app/modules/notifications/notifications.py:704; backend/app/modules/notifications/notifications.py:804; backend/app/modules/notifications/notifications.py:867; backend/app/modules/notifications/notifications.py:923. Session được import từ sqlmodel tại backend/app/modules/notifications/notifications.py:33.",
    "can_giai_thich còn lại: backend/app/modules/inference/transport.py:197 gọi hàm bọc của dự án http_runtime.request, định nghĩa tại backend/app/modules/inference/http_runtime.py:123. Lời gọi httpx trực tiếp nằm ở backend/app/modules/inference/http_runtime.py:104 và đã có trong suspects.",
    "Ba mục registration là đăng ký WebSocket bằng decorator tại backend/app/api/v1/jobs.py:166, backend/app/api/v1/printers.py:1377, backend/packages/printstash-core/src/printstash_core_testkit/mock_printer.py:273. Receiver thật là APIRouter/FastAPI tại backend/app/api/v1/jobs.py:35, backend/app/api/v1/printers.py:82, backend/packages/printstash-core/src/printstash_core_testkit/mock_printer.py:177. Lưu ý: gói thực tế chứa ba decorator với looks_like=route, khác mô tả ban đầu rằng suspects không chứa decorator; số registration ở đây bao gồm ba đăng ký WebSocket này.",
    "Đã quét văn bản toàn bộ source Python trong phạm vi bằng rg cho httpx/requests/aiohttp, kiểm tra nguồn client, factory và lời gọi nhiều dòng. Không tìm thấy lời gọi trực tiếp bị bỏ sót; 21 lời gọi trong phạm vi đều thuộc ba nhóm http_that nêu trên.",
    "Không tính HTTP trong script độc lập: scripts/backup_compatibility.py:48 và các lời gọi cùng file, backend/scripts/bench_api.py:109 và các lời gọi cùng file. Các import tại scripts/backup_compatibility.py:8 đến scripts/backup_compatibility.py:20 và backend/scripts/bench_api.py:30 đến backend/scripts/bench_api.py:39 không import code repo, nên thuộc diện loại FR-028.",
    "Các lời gọi qua hàm bọc chưa có trong suspects tại backend/app/modules/ingestion/capture_provider_connections.py:201, backend/app/modules/ingestion/capture_provider_connections.py:224, backend/app/modules/ingestion/capture_provider_connections.py:248 không đưa vào http_bo_sot. ProviderTransport được truyền vào tại backend/app/modules/ingestion/provider_connections.py:71 và backend/app/modules/ingestion/provider_connections.py:462; tầng gửi httpx trực tiếp tại backend/app/modules/ingestion/capture_provider_transport.py:70 đã có trong gói."
  ]
}
```