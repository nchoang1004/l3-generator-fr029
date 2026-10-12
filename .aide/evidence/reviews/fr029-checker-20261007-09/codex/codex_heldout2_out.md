```json
{
  "repos": [
    {
      "repo": "dispatch",
      "dependencies": {
        "params_dung": 7,
        "params_sai": [],
        "params_thieu": []
      },
      "deps_bo_sot": {
        "routes_kiem": 32,
        "items": [
          {
            "route": "GET /{organization}/ai; GET /{organization}/ai/genai-types",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/ai/prompt/views.py:29; src/dispatch/ai/prompt/views.py:35; src/dispatch/api.py:253; src/dispatch/api.py:99; src/dispatch/api.py:86"
          },
          {
            "route": "GET /{organization}/users; POST /{organization}/users",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/auth/views.py:54; src/dispatch/auth/views.py:91; src/dispatch/api.py:140; src/dispatch/api.py:99; src/dispatch/api.py:86"
          },
          {
            "route": "GET /{organization}/cases/{case_id}; GET /{organization}/cases/{case_id}/participants/minimal",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/case/views.py:78; src/dispatch/case/views.py:93; src/dispatch/api.py:191; src/dispatch/api.py:99; src/dispatch/api.py:86"
          },
          {
            "route": "GET /{organization}/incidents; GET /{organization}/incidents/{incident_id}",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/incident/views.py:76; src/dispatch/incident/views.py:102; src/dispatch/api.py:175; src/dispatch/api.py:99; src/dispatch/api.py:86"
          },
          {
            "route": "GET /{organization}/projects; POST /{organization}/projects",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/project/views.py:28; src/dispatch/project/views.py:34; src/dispatch/api.py:102; src/dispatch/api.py:99; src/dispatch/api.py:86"
          },
          {
            "route": "GET /{organization}/data/alerts/{alert_id}; POST /{organization}/data/alerts",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/data/alert/views.py:16; src/dispatch/data/alert/views.py:28; src/dispatch/api.py:132; src/dispatch/api.py:99; src/dispatch/api.py:86"
          },
          {
            "route": "GET /{organization}/data/sources; GET /{organization}/data/sources/{source_id}",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/data/source/views.py:18; src/dispatch/data/source/views.py:24; src/dispatch/api.py:125; src/dispatch/api.py:99; src/dispatch/api.py:86"
          },
          {
            "route": "GET /{organization}/tasks; POST /{organization}/tasks",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/task/views.py:27; src/dispatch/task/views.py:47; src/dispatch/api.py:168; src/dispatch/api.py:99; src/dispatch/api.py:86"
          },
          {
            "route": "GET /{organization}/workflows; GET /{organization}/workflows/{workflow_id}",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/workflow/views.py:24; src/dispatch/workflow/views.py:30; src/dispatch/api.py:220; src/dispatch/api.py:99; src/dispatch/api.py:86"
          },
          {
            "route": "GET /{organization}/plugins; GET /{organization}/plugins/instances",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/plugin/views.py:22; src/dispatch/plugin/views.py:28; src/dispatch/api.py:223; src/dispatch/api.py:99; src/dispatch/api.py:86"
          },
          {
            "route": "GET /{organization}/forms; GET /{organization}/forms/{form_id}",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/forms/views.py:25; src/dispatch/forms/views.py:31; src/dispatch/api.py:246; src/dispatch/api.py:99; src/dispatch/api.py:86"
          },
          {
            "route": "GET /{organization}/tags; GET /{organization}/tags/{tag_id}",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/tag/views.py:20; src/dispatch/tag/views.py:26; src/dispatch/api.py:150; src/dispatch/api.py:99; src/dispatch/api.py:86"
          },
          {
            "route": "GET /{organization}/notifications; GET /{organization}/notifications/{notification_id}",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/notification/views.py:20; src/dispatch/notification/views.py:26; src/dispatch/api.py:232; src/dispatch/api.py:99; src/dispatch/api.py:86"
          },
          {
            "route": "GET /{organization}/teams; POST /{organization}/teams",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/team/views.py:19; src/dispatch/team/views.py:25; src/dispatch/api.py:157; src/dispatch/api.py:99; src/dispatch/api.py:86"
          },
          {
            "route": "GET /{organization}/signals/instances; POST /{organization}/signals/instances",
            "dependency": "get_organization_path: path organization",
            "cap": "router",
            "source": "src/dispatch/signal/views.py:64; src/dispatch/signal/views.py:70; src/dispatch/api.py:136; src/dispatch/api.py:99; src/dispatch/api.py:86"
          }
        ]
      },
      "suspects": {
        "http_that": 15,
        "http_khac": 0,
        "registration": 0,
        "can_giai_thich": 0,
        "nhieu": []
      },
      "http_bo_sot": [
        {
          "at": "src/dispatch/plugins/dispatch_zoom/plugin.py:31",
          "code": "return client.delete(\"/meetings/{}\".format(event_id))"
        },
        {
          "at": "src/dispatch/plugins/dispatch_zoom/plugin.py:51",
          "code": "return client.post(\"/users/{}/meetings\".format(user_id), data=body)"
        }
      ],
      "decorators_refused_judgement": [
        {
          "at": "src/dispatch/plugins/dispatch_slack/incident/interactive.py:253",
          "dung_hay_sai": "đúng",
          "ly_do": "Receiver app là slack_bolt.app.App; options đăng ký xử lý lựa chọn của Slack, không phải route OPTIONS của FastAPI/APIRouter.",
          "source": "src/dispatch/plugins/dispatch_slack/incident/interactive.py:60; src/dispatch/plugins/dispatch_slack/incident/interactive.py:253; src/dispatch/plugins/dispatch_slack/bolt.py:7; src/dispatch/plugins/dispatch_slack/bolt.py:33"
        }
      ]
    },
    {
      "repo": "nsidnev_fastapi-realworld-example-app",
      "dependencies": {
        "params_dung": 12,
        "params_sai": [],
        "params_thieu": []
      },
      "deps_bo_sot": {
        "routes_kiem": 19,
        "items": []
      },
      "suspects": {
        "http_that": 0,
        "http_khac": 0,
        "registration": 0,
        "can_giai_thich": 0,
        "nhieu": []
      },
      "http_bo_sot": [],
      "decorators_refused_judgement": []
    },
    {
      "repo": "rhoboro_async-fastapi-sqlalchemy",
      "dependencies": {
        "params_dung": 0,
        "params_sai": [],
        "params_thieu": []
      },
      "deps_bo_sot": {
        "routes_kiem": 11,
        "items": []
      },
      "suspects": {
        "http_that": 0,
        "http_khac": 0,
        "registration": 0,
        "can_giai_thich": 0,
        "nhieu": []
      },
      "http_bo_sot": [],
      "decorators_refused_judgement": []
    },
    {
      "repo": "rafsaf_minimal-fastapi-postgres-template",
      "dependencies": {
        "params_dung": 0,
        "params_sai": [],
        "params_thieu": []
      },
      "deps_bo_sot": {
        "routes_kiem": 8,
        "items": []
      },
      "suspects": {
        "http_that": 0,
        "http_khac": 0,
        "registration": 0,
        "can_giai_thich": 0,
        "nhieu": []
      },
      "http_bo_sot": [],
      "decorators_refused_judgement": []
    }
  ],
  "ghi_chu": [
    "Chỉ đọc gói và source, không sửa file, không import hoặc chạy code repo. Tìm kiếm HTTP trên source toàn repo, loại tests/, test_*.py, conftest.py và các vùng bị cấm. Đường dẫn source là tương đối với repo tương ứng. params_dung đếm từng cặp dependency–tham số trong gói, không đếm số endpoint bị ảnh hưởng.",
    "dispatch — common_parameters: query page đúng (src/dispatch/database/service.py:587); query itemsPerPage đúng (:588); query q đúng (:589); query filter đúng (:590); query sortBy[] đúng (:591); query descending[] đúng (:592); query security_event_only đúng (:594). Các alias trên là tên HTTP thực tế; CommonParameters nối tới hàm qua Annotated và Depends tại src/dispatch/database/service.py:610, src/dispatch/database/service.py:615.",
    "dispatch — get_db có tập tham số request thuộc bốn loại đang kiểm là rỗng: nhận Request rồi lấy session từ state, không khai báo query Session (src/dispatch/database/core.py:152, src/dispatch/database/core.py:154). get_current_user cũng rỗng: chỉ nhận Request (src/dispatch/auth/service.py:256). Alias DbSession và CurrentUser được nối tại src/dispatch/database/core.py:162 và src/dispatch/auth/service.py:280.",
    "dispatch — PermissionsDependency là factory tạo instance; FastAPI dùng __call__(request: Request), không dùng permissions_classes của constructor làm query/body của endpoint. Tập header/query/cookie/path rỗng là đúng (src/dispatch/auth/permissions.py:129, src/dispatch/auth/permissions.py:132). get_current_case và get_current_incident cũng rỗng: nhận DbSession và Request, đọc ID bằng request.path_params; ID khai báo ở handler không phải tham số do dependency thêm (src/dispatch/case/views.py:64, src/dispatch/case/views.py:66, src/dispatch/case/views.py:85; src/dispatch/incident/views.py:62, src/dispatch/incident/views.py:64, src/dispatch/incident/views.py:109). get_body rỗng: chỉ nhận Request và đọc raw body (src/dispatch/plugins/dispatch_slack/endpoints.py:25).",
    "dispatch — Depends lồng get_current_role không có mục riêng trong gói, nhưng đã kiểm đệ quy: nó chỉ nhận Request và Depends(get_current_user), không thêm header/query/cookie/path. Không ghi thành dependency trực tiếp bị bỏ sót của handler (src/dispatch/database/service.py:593; src/dispatch/auth/service.py:283).",
    "dispatch — mẫu chính thức gồm 32 route: 30 route đã nêu trong deps_bo_sot, cộng GET /organizations và POST /organizations (src/dispatch/organization/views.py:32; src/dispatch/organization/views.py:38; src/dispatch/api.py:94). Các mục deps_bo_sot được nhóm hai route/mục; chúng phản ánh một dependency cấp router bị thiếu tên trong gói, không phải 15 dependency khác nhau.",
    "dispatch — get_organization_path thêm path organization, vì tên này nằm trong prefix /{organization}; OrganizationSlug là Annotated[str, StringConstraints], không phải model body (src/dispatch/api.py:86; src/dispatch/api.py:99; src/dispatch/models.py:19). Dependency hoàn toàn vắng trong gói được ghi ở deps_bo_sot, không ghi trùng vào params_thieu của những mục đã có.",
    "dispatch — cấp router còn có get_current_user khi include cả authenticated_organization_api_router và authenticated_api_router; dependency này đã có trong gói (src/dispatch/api.py:262; src/dispatch/api.py:266). Không thấy Depends cấp app trong các constructor app, frontend, api hoặc khi include api_router (src/dispatch/main.py:56; src/dispatch/main.py:62; src/dispatch/main.py:76; src/dispatch/main.py:262). Các route dispatch trong báo cáo bỏ prefix mount /api/v1 để dễ đọc; mount nằm tại src/dispatch/main.py:268.",
    "dispatch — từng suspect sau là http_that: src/dispatch/cli.py:1071 (session được tạo bằng requests.Session tại src/dispatch/cli.py:1055, truyền vào hàm tại src/dispatch/cli.py:1101); src/dispatch/plugins/dispatch_atlassian_confluence/plugin.py:135 (requests.request); src/dispatch/plugins/dispatch_core/plugin.py:129 và src/dispatch/plugins/dispatch_core/plugin.py:188 (requests.get); src/dispatch/plugins/dispatch_github/plugin.py:94 (requests.get); src/dispatch/plugins/dispatch_jira/plugin.py:88 và src/dispatch/plugins/dispatch_jira/plugin.py:98 (requests.request).",
    "dispatch — các suspect còn lại đều là http_that: src/dispatch/plugins/dispatch_microsoft_teams/conference/client.py:66 (requests.post); src/dispatch/plugins/dispatch_opsgenie/service.py:13 (requests.get) và src/dispatch/plugins/dispatch_opsgenie/service.py:43 (requests.post); src/dispatch/plugins/dispatch_zoom/client.py:28 (requests.get), src/dispatch/plugins/dispatch_zoom/client.py:36 (requests.post), src/dispatch/plugins/dispatch_zoom/client.py:44 (requests.delete); src/dispatch/plugins/generic_workflow/plugin.py:95 (requests.get) và src/dispatch/plugins/generic_workflow/plugin.py:111 (requests.post).",
    "dispatch — hai http_bo_sot là lời gọi qua wrapper nội bộ đã truy nguồn, không phải hai lời gọi requests trực tiếp mới: client tại plugin.py:31 nhận ZoomClient tạo tại src/dispatch/plugins/dispatch_zoom/plugin.py:90 và truyền tại src/dispatch/plugins/dispatch_zoom/plugin.py:93; ZoomClient.delete gọi requests.delete tại src/dispatch/plugins/dispatch_zoom/client.py:44. client tại plugin.py:51 nhận ZoomClient tạo tại src/dispatch/plugins/dispatch_zoom/plugin.py:72 và truyền tại src/dispatch/plugins/dispatch_zoom/plugin.py:76; ZoomClient.post gọi requests.post tại src/dispatch/plugins/dispatch_zoom/client.py:36. Nếu giới hạn chỉ các call site trực tiếp của thư viện hoặc instance requests.Session/httpx/aiohttp, số HTTP bỏ sót của dispatch là 0; với phạm vi bao gồm wrapper HTTP nội bộ như báo cáo này, có 2.",
    "nsidnev — get_article_by_slug_from_path: path slug đúng (app/api/dependencies/articles.py:38). get_articles_filters: query tag đúng (:22), author đúng (:23), favorited đúng (:24), limit đúng (:25), offset đúng (:26). check_article_modification_permissions: path slug đúng qua Depends(get_article_by_slug_from_path) (app/api/dependencies/articles.py:52; app/api/dependencies/articles.py:38).",
    "nsidnev — get_comment_by_id_from_path: path comment_id đúng (app/api/dependencies/comments.py:17), path slug đúng qua dependency article (:18; app/api/dependencies/articles.py:38). check_comment_modification_permissions: path comment_id và path slug đều đúng qua Depends(get_comment_by_id_from_path) (app/api/dependencies/comments.py:40; app/api/dependencies/comments.py:17; app/api/dependencies/articles.py:38). get_profile_by_username_from_path: path username đúng (app/api/dependencies/profiles.py:16).",
    "nsidnev — get_current_user_authorizer trả về _get_current_user hoặc _get_current_user_optional, không đưa tham số cấu hình factory required vào query. Cả hai nhánh chỉ đi qua repository, settings và security; tập tham số đang kiểm rỗng là đúng (app/api/dependencies/authentication.py:35; app/api/dependencies/authentication.py:78; app/api/dependencies/authentication.py:103). Authorization thuộc Security(RWAPIKeyHeader), không phải Header nên không tính thiếu (app/api/dependencies/authentication.py:18; app/api/dependencies/authentication.py:21; app/api/dependencies/authentication.py:47; app/api/dependencies/authentication.py:67).",
    "nsidnev — get_repository trả về _get_repo; repo_type là đối số factory, không phải request param. Chuỗi _get_repo → _get_connection_from_pool → _get_db_pool chỉ lấy pool từ Request, nên tập tham số rỗng đúng (app/api/dependencies/database.py:11; app/api/dependencies/database.py:15; app/api/dependencies/database.py:22; app/api/dependencies/database.py:25). get_app_settings không nhận đối số, tập tham số rỗng đúng (app/core/config.py:18). Các hàm con này được kiểm đệ quy, không tính là dependency trực tiếp mới của route.",
    "nsidnev — đã kiểm toàn bộ 19 route: articles_common tại app/api/routes/articles/articles_common.py:22, :47, :77; articles_resource tại app/api/routes/articles/articles_resource.py:30, :53, :82, :89, :109; authentication tại app/api/routes/authentication.py:22, :56; comments tại app/api/routes/comments.py:26, :40, :60; profiles tại app/api/routes/profiles.py:16, :27, :57; users tại app/api/routes/users.py:18, :38; tags tại app/api/routes/tags.py:10. Dependency decorator kiểm quyền đã có trong gói (app/api/routes/articles/articles_resource.py:93; app/api/routes/articles/articles_resource.py:113; app/api/routes/comments.py:64).",
    "nsidnev — không thấy dependency bổ sung cấp router/app trong cấu hình đã đọc (app/api/routes/api.py:6; app/api/routes/api.py:7; app/api/routes/api.py:11; app/api/routes/articles/api.py:5; app/api/routes/articles/api.py:7; app/main.py:18; app/main.py:40; app/core/settings/app.py:40). Không tìm thấy call site httpx/requests/aiohttp ngoài test; tên requests trong dependency xác thực là starlette.requests, dùng làm kiểu Request, không phải thư viện HTTP client (app/api/dependencies/authentication.py:6; app/api/dependencies/authentication.py:24).",
    "rhoboro — cả 10 dependency trong gói đều có tập header/query/cookie/path rỗng đúng. Constructor CreateNotebook, ReadAllNotebook, ReadNotebook, UpdateNotebook, DeleteNotebook chỉ nhận session: AsyncSession (app/api/notebooks/use_cases.py:10; :23; :33; :45; :63). Constructor CreateNote, ReadAllNote, ReadNote, UpdateNote, DeleteNote cũng vậy (app/api/notes/use_cases.py:10; :23; :33; :45; :68). AsyncSession là Annotated[..., Depends(get_session)], và get_session không nhận đối số (app/db.py:31; app/db.py:24). Các đối số của execute không phải chữ ký dependency mà FastAPI phân tích.",
    "rhoboro — chỉ có 11 route khai báo trong source đã quét, nên không thể lấy 15 route khác nhau. Đã kiểm hết: app/api/notebooks/views.py:18, :27, :34, :46, :59; app/api/notes/views.py:18, :27, :35, :44, :57; app/main.py:11. get_session là dependency lồng đã kiểm, không thiếu request param (app/db.py:24). Không có dependency thêm cấp router/app tại app/api/main.py:6, app/api/main.py:7, app/api/main.py:8, app/main.py:6, app/main.py:8.",
    "rhoboro — không tìm thấy call site httpx/requests/aiohttp ngoài test. Những lời gọi delete dễ nhầm là thao tác model/session SQLAlchemy, không phải HTTP (app/api/notes/use_cases.py:76; app/api/notebooks/use_cases.py:71; app/db.py:6). Model request là body, còn note_id/notebook_id được khai báo trực tiếp ở handler, không phải tham số của dependency (app/api/notes/views.py:21; app/api/notes/views.py:38; app/api/notebooks/views.py:21; app/api/notebooks/views.py:40).",
    "rafsaf — dependencies.get_current_user có tập tham số đang kiểm rỗng đúng: token đi qua OAuth2PasswordBearer, session qua new_async_session; không tính token thành query/header thiếu (app/auth/dependencies.py:13; app/auth/dependencies.py:16; app/auth/dependencies.py:17; app/auth/dependencies.py:18). new_async_session không nhận đối số, tập tham số rỗng đúng (app/core/database_session.py:38).",
    "rafsaf — OAuth2PasswordRequestForm = Depends() không có mục trong gói, nhưng đây là dependency class cung cấp form; theo quy ước không ghi vào deps_bo_sot hoặc params_thieu (app/auth/views.py:5; app/auth/views.py:74). Các model ở handler là body, không phải query của session dependency (app/auth/views.py:57; app/auth/views.py:118; app/auth/views.py:171).",
    "rafsaf — chỉ có 8 route khai báo trong source đã quét, nên không thể lấy 15 route khác nhau. Đã kiểm hết: app/auth/views.py:31, :38, :51, :66, :111, :164; app/probe/views.py:14, :19. Không có dependency thêm cấp router/app tại app/auth/views.py:28, app/probe/views.py:11, app/main.py:15, app/main.py:24, app/main.py:25. Không tìm thấy call site httpx/requests/aiohttp ngoài test; các thao tác session trong handler dùng AsyncSession SQLAlchemy (app/auth/views.py:8; app/auth/views.py:45; app/auth/views.py:47)."
  ]
}
```