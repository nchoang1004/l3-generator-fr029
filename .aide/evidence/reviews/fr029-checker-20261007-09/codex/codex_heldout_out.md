```json
{
  "repos": [
    {
      "repo": "dispatch",
      "dependencies": {
        "params_dung": 0,
        "params_sai": [],
        "params_thieu": []
      },
      "deps_bo_sot": {
        "routes_kiem": 30,
        "items": [
          {"route":"GET /{organization}/ai","dependency":"common_parameters qua CommonParameters","cap":"handler","source":"src/dispatch/ai/prompt/views.py:30; src/dispatch/database/service.py:615"},
          {"route":"GET /{organization}/incidents","dependency":"common_parameters qua CommonParameters","cap":"handler","source":"src/dispatch/incident/views.py:78; src/dispatch/database/service.py:615"},
          {"route":"GET /{organization}/data/sources","dependency":"common_parameters qua CommonParameters","cap":"handler","source":"src/dispatch/data/source/views.py:19; src/dispatch/database/service.py:615"},
          {"route":"GET /{organization}/documents","dependency":"common_parameters qua CommonParameters","cap":"handler","source":"src/dispatch/document/views.py:14; src/dispatch/database/service.py:615"},
          {"route":"GET /{organization}/entity","dependency":"common_parameters qua CommonParameters","cap":"handler","source":"src/dispatch/entity/views.py:20; src/dispatch/database/service.py:615"},
          {"route":"GET /{organization}/projects","dependency":"common_parameters qua CommonParameters","cap":"handler","source":"src/dispatch/project/views.py:29; src/dispatch/database/service.py:615"},
          {"route":"GET /{organization}/tags","dependency":"common_parameters qua CommonParameters","cap":"handler","source":"src/dispatch/tag/views.py:21; src/dispatch/database/service.py:615"},
          {"route":"GET /{organization}/tasks","dependency":"common_parameters qua CommonParameters","cap":"handler","source":"src/dispatch/task/views.py:28; src/dispatch/database/service.py:615"},
          {"route":"GET /{organization}/workflows","dependency":"common_parameters qua CommonParameters","cap":"handler","source":"src/dispatch/workflow/views.py:25; src/dispatch/database/service.py:615"},
          {"route":"GET /{organization}/ai","dependency":"get_organization_path","cap":"router","source":"src/dispatch/ai/prompt/views.py:29; src/dispatch/api.py:99; src/dispatch/api.py:253"},
          {"route":"GET /{organization}/ai/genai-types","dependency":"get_organization_path","cap":"router","source":"src/dispatch/ai/prompt/views.py:35; src/dispatch/api.py:99; src/dispatch/api.py:253"},
          {"route":"GET /{organization}/ai/defaults","dependency":"get_organization_path","cap":"router","source":"src/dispatch/ai/prompt/views.py:41; src/dispatch/api.py:99; src/dispatch/api.py:253"},
          {"route":"GET /{organization}/cases/{case_id}","dependency":"get_organization_path","cap":"router","source":"src/dispatch/case/views.py:78; src/dispatch/api.py:99; src/dispatch/api.py:191"},
          {"route":"GET /{organization}/cases/{case_id}/participants/minimal","dependency":"get_organization_path","cap":"router","source":"src/dispatch/case/views.py:93; src/dispatch/api.py:99; src/dispatch/api.py:191"},
          {"route":"GET /{organization}/cases/{case_id}/participants","dependency":"get_organization_path","cap":"router","source":"src/dispatch/case/views.py:107; src/dispatch/api.py:99; src/dispatch/api.py:191"},
          {"route":"GET /{organization}/incidents","dependency":"get_organization_path","cap":"router","source":"src/dispatch/incident/views.py:76; src/dispatch/api.py:99; src/dispatch/api.py:176"},
          {"route":"GET /{organization}/incidents/{incident_id}","dependency":"get_organization_path","cap":"router","source":"src/dispatch/incident/views.py:102; src/dispatch/api.py:99; src/dispatch/api.py:176"},
          {"route":"POST /{organization}/incidents","dependency":"get_organization_path","cap":"router","source":"src/dispatch/incident/views.py:117; src/dispatch/api.py:99; src/dispatch/api.py:176"},
          {"route":"GET /{organization}/data/sources","dependency":"get_organization_path","cap":"router","source":"src/dispatch/data/source/views.py:18; src/dispatch/api.py:99; src/dispatch/api.py:126"},
          {"route":"GET /{organization}/data/sources/{source_id}","dependency":"get_organization_path","cap":"router","source":"src/dispatch/data/source/views.py:24; src/dispatch/api.py:99; src/dispatch/api.py:126"},
          {"route":"POST /{organization}/data/sources","dependency":"get_organization_path","cap":"router","source":"src/dispatch/data/source/views.py:36; src/dispatch/api.py:99; src/dispatch/api.py:126"},
          {"route":"GET /{organization}/documents","dependency":"get_organization_path","cap":"router","source":"src/dispatch/document/views.py:13; src/dispatch/api.py:99; src/dispatch/api.py:142"},
          {"route":"GET /{organization}/documents/{document_id}","dependency":"get_organization_path","cap":"router","source":"src/dispatch/document/views.py:19; src/dispatch/api.py:99; src/dispatch/api.py:142"},
          {"route":"POST /{organization}/documents","dependency":"get_organization_path","cap":"router","source":"src/dispatch/document/views.py:31; src/dispatch/api.py:99; src/dispatch/api.py:142"},
          {"route":"GET /{organization}/entity","dependency":"get_organization_path","cap":"router","source":"src/dispatch/entity/views.py:19; src/dispatch/api.py:99; src/dispatch/api.py:145"},
          {"route":"GET /{organization}/entity/{entity_id}","dependency":"get_organization_path","cap":"router","source":"src/dispatch/entity/views.py:25; src/dispatch/api.py:99; src/dispatch/api.py:145"},
          {"route":"POST /{organization}/entity","dependency":"get_organization_path","cap":"router","source":"src/dispatch/entity/views.py:37; src/dispatch/api.py:99; src/dispatch/api.py:145"},
          {"route":"GET /{organization}/projects","dependency":"get_organization_path","cap":"router","source":"src/dispatch/project/views.py:28; src/dispatch/api.py:99; src/dispatch/api.py:103"},
          {"route":"POST /{organization}/projects","dependency":"get_organization_path","cap":"router","source":"src/dispatch/project/views.py:34; src/dispatch/api.py:99; src/dispatch/api.py:103"},
          {"route":"GET /{organization}/projects/{project_id}","dependency":"get_organization_path","cap":"router","source":"src/dispatch/project/views.py:74; src/dispatch/api.py:99; src/dispatch/api.py:103"},
          {"route":"GET /{organization}/tags","dependency":"get_organization_path","cap":"router","source":"src/dispatch/tag/views.py:20; src/dispatch/api.py:99; src/dispatch/api.py:150"},
          {"route":"GET /{organization}/tags/{tag_id}","dependency":"get_organization_path","cap":"router","source":"src/dispatch/tag/views.py:26; src/dispatch/api.py:99; src/dispatch/api.py:150"},
          {"route":"POST /{organization}/tags","dependency":"get_organization_path","cap":"router","source":"src/dispatch/tag/views.py:38; src/dispatch/api.py:99; src/dispatch/api.py:150"},
          {"route":"GET /{organization}/tasks","dependency":"get_organization_path","cap":"router","source":"src/dispatch/task/views.py:27; src/dispatch/api.py:99; src/dispatch/api.py:168"},
          {"route":"POST /{organization}/tasks","dependency":"get_organization_path","cap":"router","source":"src/dispatch/task/views.py:47; src/dispatch/api.py:99; src/dispatch/api.py:168"},
          {"route":"POST /{organization}/tasks/ticket/{task_id}","dependency":"get_organization_path","cap":"router","source":"src/dispatch/task/views.py:73; src/dispatch/api.py:99; src/dispatch/api.py:168"},
          {"route":"GET /{organization}/workflows","dependency":"get_organization_path","cap":"router","source":"src/dispatch/workflow/views.py:24; src/dispatch/api.py:99; src/dispatch/api.py:221"},
          {"route":"GET /{organization}/workflows/{workflow_id}","dependency":"get_organization_path","cap":"router","source":"src/dispatch/workflow/views.py:30; src/dispatch/api.py:99; src/dispatch/api.py:221"},
          {"route":"GET /{organization}/workflows/instances/{workflow_instance_id}","dependency":"get_organization_path","cap":"router","source":"src/dispatch/workflow/views.py:45; src/dispatch/api.py:99; src/dispatch/api.py:221"}
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
        {"at":"src/dispatch/plugins/dispatch_zoom/plugin.py:31","code":"return client.delete(\"/meetings/{}\".format(event_id))"},
        {"at":"src/dispatch/plugins/dispatch_zoom/plugin.py:51","code":"return client.post(\"/users/{}/meetings\".format(user_id), data=body)"}
      ]
    },
    {
      "repo": "nsidnev_fastapi-realworld-example-app",
      "dependencies": {
        "params_dung": 12,
        "params_sai": [
          {
            "dep":"get_current_user_authorizer",
            "in":"query",
            "name":"required",
            "ly_do":"Đối số cấu hình factory; Depends nhận hàm được factory trả về, không nhận chữ ký factory.",
            "source":"app/api/dependencies/authentication.py:35; app/api/dependencies/authentication.py:36; app/api/routes/articles/articles_common.py:30"
          },
          {
            "dep":"get_article_by_slug_from_path",
            "in":"query",
            "name":"required",
            "ly_do":"required=False được truyền lúc gọi factory; không trở thành query parameter của dependency lồng.",
            "source":"app/api/dependencies/articles.py:39; app/api/dependencies/authentication.py:35; app/api/dependencies/authentication.py:36"
          },
          {
            "dep":"check_article_modification_permissions",
            "in":"query",
            "name":"required",
            "ly_do":"Hai nhánh xác thực đều dùng hàm do factory trả về; required chỉ cấu hình factory.",
            "source":"app/api/dependencies/articles.py:52; app/api/dependencies/articles.py:53; app/api/dependencies/authentication.py:36"
          },
          {
            "dep":"get_comment_by_id_from_path",
            "in":"query",
            "name":"required",
            "ly_do":"required=False là đối số factory xác thực, kể cả nhánh lồng qua article.",
            "source":"app/api/dependencies/comments.py:18; app/api/dependencies/comments.py:20; app/api/dependencies/authentication.py:36"
          },
          {
            "dep":"check_comment_modification_permissions",
            "in":"query",
            "name":"required",
            "ly_do":"Factory chọn hàm xác thực; không có query parameter required trong các hàm thực sự được inject.",
            "source":"app/api/dependencies/comments.py:40; app/api/dependencies/comments.py:41; app/api/dependencies/authentication.py:36"
          },
          {
            "dep":"get_profile_by_username_from_path",
            "in":"query",
            "name":"required",
            "ly_do":"required=False là đối số cấu hình factory, không phải dữ liệu request.",
            "source":"app/api/dependencies/profiles.py:17; app/api/dependencies/authentication.py:35; app/api/dependencies/authentication.py:36"
          }
        ],
        "params_thieu": [
          {"dep":"get_current_user_authorizer","in":"header","name":"Authorization","source":"app/api/dependencies/authentication.py:18; app/api/dependencies/authentication.py:47; app/api/dependencies/authentication.py:68; app/api/dependencies/authentication.py:80; app/api/dependencies/authentication.py:105"},
          {"dep":"get_article_by_slug_from_path","in":"header","name":"Authorization","source":"app/api/dependencies/articles.py:39; app/api/dependencies/authentication.py:18; app/api/dependencies/authentication.py:68; app/api/dependencies/authentication.py:105"},
          {"dep":"check_article_modification_permissions","in":"header","name":"Authorization","source":"app/api/dependencies/articles.py:52; app/api/dependencies/articles.py:53; app/api/dependencies/authentication.py:18; app/api/dependencies/authentication.py:47"},
          {"dep":"get_comment_by_id_from_path","in":"header","name":"Authorization","source":"app/api/dependencies/comments.py:18; app/api/dependencies/comments.py:20; app/api/dependencies/authentication.py:18; app/api/dependencies/authentication.py:68"},
          {"dep":"check_comment_modification_permissions","in":"header","name":"Authorization","source":"app/api/dependencies/comments.py:40; app/api/dependencies/comments.py:41; app/api/dependencies/authentication.py:18; app/api/dependencies/authentication.py:47"},
          {"dep":"get_profile_by_username_from_path","in":"header","name":"Authorization","source":"app/api/dependencies/profiles.py:17; app/api/dependencies/authentication.py:18; app/api/dependencies/authentication.py:68"}
        ]
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
      "http_bo_sot": [
        {"at":"tests/test_api/test_errors/test_422_error.py:15","code":"response = await client.get(\"/wrong_path/asd\")"},
        {"at":"tests/test_api/test_errors/test_error.py:11","code":"response = await client.get(\"/wrong_path/asd\")"},
        {"at":"tests/test_api/test_routes/test_articles.py:26","code":"response = await authorized_client.post("},
        {"at":"tests/test_api/test_routes/test_articles.py:40","code":"response = await authorized_client.post("},
        {"at":"tests/test_api/test_routes/test_articles.py:57","code":"response = await authorized_client.post("},
        {"at":"tests/test_api/test_routes/test_articles.py:75","code":"response = await authorized_client.request("},
        {"at":"tests/test_api/test_routes/test_articles.py:84","code":"response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_articles.py:107","code":"response = await authorized_client.put("},
        {"at":"tests/test_api/test_routes/test_articles.py:153","code":"response = await authorized_client.request("},
        {"at":"tests/test_api/test_routes/test_articles.py:167","code":"await authorized_client.delete("},
        {"at":"tests/test_api/test_routes/test_articles.py:201","code":"await authorized_client.request("},
        {"at":"tests/test_api/test_routes/test_articles.py:205","code":"response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_articles.py:239","code":"response = await authorized_client.request("},
        {"at":"tests/test_api/test_routes/test_articles.py:271","code":"response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_articles.py:311","code":"response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_articles.py:356","code":"full_response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_articles.py:361","code":"response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_articles.py:397","code":"response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_articles.py:446","code":"response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_articles.py:494","code":"response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_articles.py:543","code":"response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_articles.py:565","code":"full_response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_articles.py:570","code":"response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_authentication.py:15","code":"response = await client.get("},
        {"at":"tests/test_api/test_routes/test_authentication.py:28","code":"response = await client.get("},
        {"at":"tests/test_api/test_routes/test_comments.py:18","code":"created_comment_response = await authorized_client.post("},
        {"at":"tests/test_api/test_routes/test_comments.py:25","code":"comments_for_article_response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_comments.py:37","code":"created_comment_response = await authorized_client.post("},
        {"at":"tests/test_api/test_routes/test_comments.py:44","code":"await authorized_client.delete("},
        {"at":"tests/test_api/test_routes/test_comments.py:52","code":"comments_for_article_response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_comments.py:74","code":"forbidden_response = await authorized_client.delete("},
        {"at":"tests/test_api/test_routes/test_comments.py:88","code":"not_found_response = await authorized_client.delete("},
        {"at":"tests/test_api/test_routes/test_login.py:16","code":"response = await client.post(app.url_path_for(\"auth:login\"), json=login_json)"},
        {"at":"tests/test_api/test_routes/test_login.py:33","code":"response = await client.post(app.url_path_for(\"auth:login\"), json=login_json)"},
        {"at":"tests/test_api/test_routes/test_profiles.py:18","code":"response = await client.get("},
        {"at":"tests/test_api/test_routes/test_profiles.py:37","code":"response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_profiles.py:61","code":"response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_profiles.py:80","code":"response = await authorized_client.request("},
        {"at":"tests/test_api/test_routes/test_profiles.py:116","code":"change_following_response = await authorized_client.request("},
        {"at":"tests/test_api/test_routes/test_profiles.py:121","code":"response = await authorized_client.get("},
        {"at":"tests/test_api/test_routes/test_profiles.py:159","code":"response = await authorized_client.request("},
        {"at":"tests/test_api/test_routes/test_profiles.py:177","code":"response = await authorized_client.request("},
        {"at":"tests/test_api/test_routes/test_registration.py:20","code":"response = await client.post("},
        {"at":"tests/test_api/test_routes/test_registration.py:53","code":"response = await client.post("},
        {"at":"tests/test_api/test_routes/test_tags.py:12","code":"response = await client.get(app.url_path_for(\"tags:get-all\"))"},
        {"at":"tests/test_api/test_routes/test_tags.py:25","code":"response = await client.get(app.url_path_for(\"tags:get-all\"))"},
        {"at":"tests/test_api/test_routes/test_users.py:30","code":"response = await client.request(api_method, app.url_path_for(route_name))"},
        {"at":"tests/test_api/test_routes/test_users.py:46","code":"response = await client.request("},
        {"at":"tests/test_api/test_routes/test_users.py:57","code":"response = await authorized_client.get(app.url_path_for(\"users:get-current-user\"))"},
        {"at":"tests/test_api/test_routes/test_users.py:81","code":"response = await authorized_client.put("},
        {"at":"tests/test_api/test_routes/test_users.py:98","code":"response = await authorized_client.put("},
        {"at":"tests/test_api/test_routes/test_users.py:136","code":"response = await authorized_client.put("}
      ]
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
      "http_bo_sot": [
        {"at":"app/tests/test_main.py:7","code":"response = await ac.get("},
        {"at":"app/tests/api/notebooks/test_views.py:32","code":"response = await ac.get("},
        {"at":"app/tests/api/notebooks/test_views.py:88","code":"response = await ac.get("},
        {"at":"app/tests/api/notebooks/test_views.py:121","code":"response = await ac.post(\"/api/notebooks\", json={\"title\": \"Test Notebook\", \"notes\": []})"},
        {"at":"app/tests/api/notebooks/test_views.py:142","code":"response = await ac.put("},
        {"at":"app/tests/api/notebooks/test_views.py:181","code":"response = await ac.delete("},
        {"at":"app/tests/api/notes/test_views.py:32","code":"response = await ac.get("},
        {"at":"app/tests/api/notes/test_views.py:77","code":"response = await ac.get("},
        {"at":"app/tests/api/notes/test_views.py:104","code":"response = await ac.post("},
        {"at":"app/tests/api/notes/test_views.py:137","code":"response = await ac.put("},
        {"at":"app/tests/api/notes/test_views.py:174","code":"response = await ac.delete("}
      ]
    },
    {
      "repo": "rafsaf_minimal-fastapi-postgres-template",
      "dependencies": {
        "params_dung": 0,
        "params_sai": [],
        "params_thieu": [
          {
            "dep":"dependencies.get_current_user",
            "in":"header",
            "name":"Authorization",
            "source":"app/auth/dependencies.py:4; app/auth/dependencies.py:13; app/auth/dependencies.py:17"
          }
        ]
      },
      "deps_bo_sot": {
        "routes_kiem": 8,
        "items": [
          {
            "route":"POST /auth/access-token",
            "dependency":"OAuth2PasswordRequestForm qua Depends() không đối số",
            "cap":"handler",
            "source":"app/auth/views.py:5; app/auth/views.py:66; app/auth/views.py:74; app/main.py:24"
          }
        ]
      },
      "suspects": {
        "http_that": 0,
        "http_khac": 0,
        "registration": 0,
        "can_giai_thich": 0,
        "nhieu": []
      },
      "http_bo_sot": [
        {"at":"app/probe/tests/test_views.py:7","code":"response = await client.get(app.url_path_for(\"live_probe\"))"},
        {"at":"app/probe/tests/test_views.py:14","code":"response = await client.get(app.url_path_for(\"health_probe\"))"},
        {"at":"app/auth/tests/test_view_delete_current_user.py:14","code":"response = await client.delete("},
        {"at":"app/auth/tests/test_view_delete_current_user.py:28","code":"await client.delete("},
        {"at":"app/auth/tests/test_view_read_current_user.py:18","code":"response = await client.get("},
        {"at":"app/auth/tests/test_view_read_current_user.py:31","code":"response = await client.get("},
        {"at":"app/auth/tests/test_view_read_current_user.py:45","code":"response = await client.get("},
        {"at":"app/auth/tests/test_view_read_current_user.py:61","code":"response = await client.get("},
        {"at":"app/auth/tests/test_view_read_current_user.py:79","code":"response = await client.get("},
        {"at":"app/auth/tests/test_view_refresh_token.py:19","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_refresh_token.py:43","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_refresh_token.py:68","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_refresh_token.py:93","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_refresh_token.py:117","code":"await client.post("},
        {"at":"app/auth/tests/test_view_refresh_token.py:145","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_refresh_token.py:171","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_refresh_token.py:201","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_refresh_token.py:232","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_refresh_token.py:261","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_register_new_user.py:15","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_register_new_user.py:30","code":"await client.post("},
        {"at":"app/auth/tests/test_view_register_new_user.py:50","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_login_access_token.py:21","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_login_access_token.py:36","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_login_access_token.py:54","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_login_access_token.py:76","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_login_access_token.py:99","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_login_access_token.py:122","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_login_access_token.py:145","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_login_access_token.py:169","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_login_access_token.py:186","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_reset_current_user_password.py:15","code":"response = await client.post("},
        {"at":"app/auth/tests/test_view_reset_current_user_password.py:30","code":"await client.post("}
      ]
    }
  ],
  "ghi_chu": [
    "Chỉ đọc packet và source; không sửa file, không import/chạy code repo, không đọc slice/, HANDOFF, docs/ hoặc .aide/. Đường dẫn source tương đối với repo tương ứng. params_dung đếm cặp dependency–tham số có trong packet, không đếm dependency có danh sách rỗng.",
    "Quy ước deps_bo_sot: kiểm dependency gắn trực tiếp tại handler/decorator/router/app, có giải alias và factory. Dependency lồng được lần theo để xác định tham số; không coi việc thiếu khóa riêng cho mọi nút lồng là một lỗi độc lập. Ví dụ: nsidnev app/api/dependencies/database.py:25–30; rhoboro app/db.py:24–31; dispatch src/dispatch/database/service.py:593–615.",
    "Authorization trong params_thieu là đầu vào HTTP của security dependency. Trong OpenAPI, các security dependency này được biểu diễn bằng securitySchemes/security, không phải parameters thông thường. Nếu tiêu chí chỉ đếm OpenAPI parameters thì loại sáu mục Authorization của nsidnev và một mục của rafsaf khỏi params_thieu. Nguồn: nsidnev app/api/dependencies/authentication.py:5,18,21,47,68; rafsaf app/auth/dependencies.py:4,13,17.",
    "Dispatch: cả sáu danh sách tham số rỗng trong packet đều đúng theo chữ ký dependency. get_db chỉ nhận Request (src/dispatch/database/core.py:152); get_current_user chỉ nhận Request (src/dispatch/auth/service.py:256); instance PermissionsDependency có __call__(request: Request), không dùng đối số constructor làm query (src/dispatch/auth/permissions.py:129,132); get_current_case/get_current_incident nhận DbSession và Request (src/dispatch/case/views.py:64; src/dispatch/incident/views.py:62), với DbSession là Depends(get_db) tại src/dispatch/database/core.py:162; get_body chỉ nhận Request (src/dispatch/plugins/dispatch_slack/endpoints.py:25). Đọc request.path_params hoặc request.body trong thân hàm không tự thêm parameter khai báo.",
    "Dispatch: common_parameters bị thiếu toàn bộ dependency nên không đưa vào params_thieu của sáu mục hiện có. Các query đúng của nó là page (src/dispatch/database/service.py:587), itemsPerPage (:588), q (:589), filter (:590), sortBy[] (:591), descending[] (:592), security_event_only (:594). Nhánh get_current_role tại :593 đi tới Request và Depends(get_current_user), không thêm query (src/dispatch/auth/service.py:283–287). get_organization_path thêm path organization (src/dispatch/api.py:86,99).",
    "Dispatch: mẫu gồm đúng ba route đầu của mỗi module ai/prompt, case, incident, data/source, document, entity, project, tag, task, workflow; 30 vị trí decorator được ghi trong các items cấp router. Dependency router get_current_user đã có trong packet, được gắn tại src/dispatch/api.py:263,268. Không có dependency cấp app trong các constructor đã đọc tại src/dispatch/main.py:56,62,76–83. Route ghi theo đường dẫn router; cấu hình root_path là /api/v1 tại src/dispatch/main.py:79.",
    "Dispatch: phân loại từng suspect là http_that tại src/dispatch/cli.py:1071 (requests.Session được tạo tại :1055); src/dispatch/plugins/dispatch_atlassian_confluence/plugin.py:135; src/dispatch/plugins/dispatch_core/plugin.py:129,188; src/dispatch/plugins/dispatch_github/plugin.py:94; src/dispatch/plugins/dispatch_jira/plugin.py:88,98; src/dispatch/plugins/dispatch_microsoft_teams/conference/client.py:66; src/dispatch/plugins/dispatch_opsgenie/service.py:13,43; src/dispatch/plugins/dispatch_zoom/client.py:28,36,44; src/dispatch/plugins/generic_workflow/plugin.py:95,111. Tổng cộng 15, không có suspect thuộc nhóm khác.",
    "Dispatch: hai mục http_bo_sot là lời gọi phương thức của wrapper ZoomClient cục bộ. Client được tạo và truyền vào helper tại src/dispatch/plugins/dispatch_zoom/plugin.py:72–77,90–93; post/delete chuyển thẳng sang requests tại src/dispatch/plugins/dispatch_zoom/client.py:35–44. Hai vị trí wrapper chưa có trong suspects, còn các vị trí gọi requests bên trong đã có. Nếu chỉ tính điểm gọi trực tiếp API của requests/httpx/aiohttp thì Dispatch không thiếu điểm gọi trực tiếp nào đã tìm thấy.",
    "Nsidnev: 12 tham số trong packet được đánh dấu đúng gồm get_articles_filters.query.tag, author, favorited, limit, offset (app/api/dependencies/articles.py:22–26); get_article_by_slug_from_path.path.slug (:38); check_article_modification_permissions.path.slug (:52 dẫn tới :38); get_comment_by_id_from_path.path.comment_id và path.slug (app/api/dependencies/comments.py:17,18); check_comment_modification_permissions.path.comment_id và path.slug (:40 dẫn tới :17,18); get_profile_by_username_from_path.path.username (app/api/dependencies/profiles.py:16).",
    "Nsidnev: bộ tham số đúng đầy đủ của các mục có lỗi là get_current_user_authorizer={header Authorization}; get_article_by_slug_from_path và check_article_modification_permissions={path slug, header Authorization}; get_comment_by_id_from_path và check_comment_modification_permissions={path comment_id, path slug, header Authorization}; get_profile_by_username_from_path={path username, header Authorization}. Chuỗi nguồn tương ứng nằm trong params_sai/params_thieu. get_repository không thêm tham số request: factory trả _get_repo(conn=Depends(...)) rồi đi tới Request, tại app/api/dependencies/database.py:11,15–17,22–30. get_app_settings không có đối số tại app/core/config.py:18.",
    "Nsidnev: đã kiểm 19 route ứng dụng, không thấy dependency trực tiếp bị bỏ sót: app/api/routes/users.py:18,38; tags.py:10; profiles.py:16,27,57; comments.py:26,40,60; authentication.py:22,56; articles/articles_resource.py:30,53,82,89,109; articles/articles_common.py:22,47,77. Dependency decorator có tại comments.py:64 và articles/articles_resource.py:93,113, đều đã có trong packet. Router/app không gắn thêm dependency tại app/api/routes/api.py:6–16; app/api/routes/articles/api.py:5–8; app/main.py:18,40; app/core/settings/app.py:40–49.",
    "Nsidnev: 52 vị trí HTTP thiếu đều nằm trong test và gọi httpx.AsyncClient. Nguồn tạo client: tests/conftest.py:7,39–45; authorized_client trả cùng client sau khi thêm header tại tests/conftest.py:86–93. Các mục code nhiều dòng trích nguyên dòng bắt đầu lời gọi.",
    "Rhoboro: cả mười dependency class có bộ tham số request rỗng. Constructor chỉ nhận AsyncSession: app/api/notebooks/use_cases.py:10,23,33,45,63 và app/api/notes/use_cases.py:10,23,33,45,68. Đây là alias Annotated[..., Depends(get_session)] tại app/db.py:31; get_session không nhận đối số tại app/db.py:24. Các đối số execute như notebook_id/title không thuộc chữ ký constructor mà FastAPI inject.",
    "Rhoboro: đã kiểm toàn bộ 11 route khai báo, không đủ 15 route riêng biệt để lấy mẫu: app/main.py:11; app/api/notebooks/views.py:18,27,34,46,59; app/api/notes/views.py:18,27,35,44,57. Không thấy dependency trực tiếp bị bỏ sót hoặc dependency router/app bổ sung: app/main.py:6,8; app/api/main.py:6–8; app/api/notebooks/views.py:15; app/api/notes/views.py:15. Mười một lời gọi HTTP thiếu dùng fixture httpx.AsyncClient với ASGITransport tại app/tests/conftest.py:4,22–27.",
    "Rafsaf: get_current_user nhận Authorization qua OAuth2PasswordBearer lồng trong Annotated Depends, còn session là dependency CSDL (app/auth/dependencies.py:13,16–18). new_async_session có bộ tham số request rỗng tại app/core/database_session.py:38. OAuth2PasswordRequestForm bị bỏ sót là dependency form/body, không phải query/header, tại app/auth/views.py:5,74.",
    "Rafsaf: đã kiểm toàn bộ tám route khai báo, không đủ 15 route riêng biệt để lấy mẫu: app/auth/views.py:31,38,51,66,111,164; app/probe/views.py:14,19. Không có dependency cấp router/app tại app/auth/views.py:28; app/probe/views.py:11; app/main.py:15–25. Ba mươi ba lời gọi HTTP thiếu sử dụng fixture httpx.AsyncClient với ASGITransport tại app/conftest.py:10,122–127.",
    "Cả bốn packet có decorators_refused=[] tại D:/VSF/l3-generator-l3/ket-qua-chay/fr029-heldout-20261008/dispatch.packet.json:5, nsidnev_fastapi-realworld-example-app.packet.json:5, rhoboro_async-fastapi-sqlalchemy.packet.json:5 và rafsaf_minimal-fastapi-postgres-template.packet.json:5. Đây là trạng thái packet, không phải khẳng định đã kiểm độc lập toàn bộ decorator của Dispatch.",
    "Phần HTTP bao gồm test theo yêu cầu toàn repo, nhưng không tính dòng đã comment thành lời gọi thực thi; ví dụ dispatch tests/api/test_schema.py:27. Các request test của ba repo nhỏ dùng transport ASGI nội bộ, không đồng nghĩa gửi HTTP ra mạng ngoài: nsidnev tests/conftest.py:40–42; rhoboro app/tests/conftest.py:23–25; rafsaf app/conftest.py:124–125."
  ]
}
```