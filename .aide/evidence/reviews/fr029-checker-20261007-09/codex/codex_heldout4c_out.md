```json
{
  "repos": [
    {
      "repo": "stevezau_shortlist",
      "dependencies": {
        "params_dung": 0,
        "params_sai": [],
        "params_thieu": []
      },
      "deps_bo_sot": {
        "routes_kiem": 53,
        "items": [
          {
            "route": "GET /api/support/health",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:422; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/title",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:543; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/person/{slug}",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:691; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/libraries",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:813; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/rows",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:864; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/bundle.txt",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:926; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/row-schedule",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:1085; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/jobs",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:1211; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/clocks",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:1253; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/database",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:1294; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/config",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:1338; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/pick",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:1449; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/missing",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:1493; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/funnel",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:1540; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/ai",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:1586; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/timeline",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:1629; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/settings-history",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:1697; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/connection",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:1790; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/read-as",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:1882; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/sharing",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:1987; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/surfaces",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:2101; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/drift",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:2221; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/suggestions",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:2304; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/errors",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:2332; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/runs",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:2386; shortlist/server/api/support.py:137"
          },
          {
            "route": "GET /api/support/report.zip",
            "dependency": "require_support_mode",
            "cap": "router",
            "source": "shortlist/server/api/support.py:2439; shortlist/server/api/support.py:137"
          }
        ]
      },
      "suspects": {
        "http_that": 43,
        "http_khac": 0,
        "registration": 0,
        "can_giai_thich": 7,
        "nhieu": []
      },
      "http_bo_sot": [
        {
          "at": "shortlist/engine/clients/plex_pms.py:397",
          "code": "response = super().send(request, **kwargs)"
        },
        {
          "at": "shortlist/engine/clients/search.py:306",
          "code": "response = http_retry.idempotent_post("
        },
        {
          "at": "shortlist/engine/clients/tautulli.py:31",
          "code": "r = http_retry.get("
        },
        {
          "at": "shortlist/engine/clients/tmdb.py:92",
          "code": "r = http_retry.get("
        },
        {
          "at": "shortlist/engine/clients/http_retry.py:122",
          "code": "return _send("
        },
        {
          "at": "shortlist/engine/clients/http_retry.py:141",
          "code": "return _send("
        },
        {
          "at": "shortlist/engine/clients/http_retry.py:155",
          "code": "return _send(method, url, attempts=attempts, retry_exc=_WRITE_RETRY_EXC, retry_status=_WRITE_RETRY_STATUS, **kwargs)"
        }
      ],
      "decorators_refused_judgement": []
    }
  ],
  "ghi_chu": [
    "Chỉ đọc gói và source của stevezau_shortlist; không sửa file, không chạy code repo, không đọc slice/, HANDOFF, docs/ hoặc .aide/. Quét HTTP bằng rg và loại tests/, test_*.py, conftest.py.",
    "require_owner, called=false: tham số request do FastAPI khai báo là []; params=[] trong gói đúng. Hàm chỉ nhận request: Request, không có Depends lồng nhau: shortlist/server/auth.py:290. Việc tự đọc bearer/session trong thân hàm không tự sinh Header hoặc Cookie trong signature: shortlist/server/auth.py:305; shortlist/server/auth.py:314.",
    "require_browser_owner, called=false: tham số request do FastAPI khai báo là []; params=[] trong gói đúng. Hàm chỉ nhận request: Request: shortlist/server/assistant_auth/routes.py:67. BrowserOwner là kiểu trả về, còn BrowserOwnerDep là Annotated[BrowserOwner, Depends(require_browser_owner)], không phải body hay dependency class: shortlist/server/assistant_auth/routes.py:83; shortlist/server/assistant_auth/routes.py:86. Cách dùng alias đã đối chiếu tại shortlist/server/api/requests.py:711 và shortlist/server/assistant_auth/routes.py:289.",
    "params_dung=0 là số tham số, không phải số dependency đúng: cả hai dependency đều có danh sách tham số rỗng, căn cứ shortlist/server/auth.py:290 và shortlist/server/assistant_auth/routes.py:67.",
    "Dependency bị bỏ sót là một hàm duy nhất, require_support_mode, được dùng trên 26 route đã liệt kê. Hàm chỉ nhận Request nên không làm phát sinh params_thieu: shortlist/server/api/support.py:111. Dependency thuộc router _tool tại shortlist/server/api/support.py:137, được ghép vào router xuất ra tại shortlist/server/api/support.py:2502 rồi gắn prefix /api tại shortlist/server/main.py:464.",
    "53 route được kiểm gồm 26 route _tool trong deps_bo_sot.items, GET /api/support/status tại shortlist/server/api/support.py:157 và 26 route ngoài support được ghi trong các mục tiếp theo. GET /api/support/status chỉ kế thừa require_owner từ _mode: shortlist/server/api/support.py:133.",
    "Mẫu ngoài support, nhóm 1: POST /api/ai/web-prompt-preview — shortlist/server/api/ai.py:44; GET /api/collections — shortlist/server/api/collections.py:1520; GET /api/events — shortlist/server/api/events.py:49; GET /api/notifications — shortlist/server/api/notifications.py:47; GET /api/picks/{rating_key}/poster — shortlist/server/api/picks.py:138; GET /api/privacy/status — shortlist/server/api/privacy.py:123; POST /api/report/sync — shortlist/server/api/report.py:56; GET /api/requests — shortlist/server/api/requests.py:93; GET /api/requests/acquisition-claims — shortlist/server/api/requests.py:708.",
    "Mẫu ngoài support, nhóm 2: GET /api/runs — shortlist/server/api/runs.py:95; GET /api/schedule — shortlist/server/api/schedule.py:72; GET /api/seasons — shortlist/server/api/seasons.py:257; GET /api/settings — shortlist/server/api/settings.py:515; PUT /api/settings — shortlist/server/api/settings.py:521; GET /api/setup/servers — shortlist/server/api/setup.py:93; GET /api/system/version — shortlist/server/api/system.py:89; GET /api/themes/capabilities — shortlist/server/api/themes.py:184.",
    "Mẫu ngoài support, nhóm 3: GET /api/users/{user_id}/rows — shortlist/server/api/user_rows.py:78; GET /api/users — shortlist/server/api/users.py:386; GET /api/watching-account/candidates — shortlist/server/api/watching_account.py:119; POST /api/auth/pin — shortlist/server/auth.py:369; GET /api/catalogs/settings — shortlist/server/assistant/routes.py:22; GET /api/assistant/changes/{change_id} — shortlist/server/assistant/routes.py:51; GET /assistant/grants — shortlist/server/assistant_auth/routes.py:288; GET /assistant/oauth/authorize — shortlist/server/assistant_auth/routes.py:393; GET /{path:path} — shortlist/server/main.py:518.",
    "Cấp router đã kiểm, require_owner đã có trong gói: shortlist/server/api/ai.py:18; shortlist/server/api/collections.py:92; shortlist/server/api/events.py:23; shortlist/server/api/notifications.py:16; shortlist/server/api/picks.py:29; shortlist/server/api/privacy.py:35; shortlist/server/api/report.py:53; shortlist/server/api/requests.py:32; shortlist/server/api/runs.py:26; shortlist/server/api/schedule.py:24; shortlist/server/api/seasons.py:51; shortlist/server/api/settings.py:46; shortlist/server/api/system.py:63; shortlist/server/api/themes.py:39; shortlist/server/api/user_rows.py:30; shortlist/server/api/users.py:39; shortlist/server/api/watching_account.py:29; shortlist/server/api/support.py:133; shortlist/server/api/support.py:137.",
    "Cấp router assistant và catalogs dùng require_browser_owner đã có trong gói: shortlist/server/assistant/routes.py:18; shortlist/server/assistant/routes.py:19. Cấp handler khai lại dependency đã có tại shortlist/server/assistant/routes.py:53 và shortlist/server/api/settings.py:528. App không khai dependencies trong FastAPI hoặc các include_router đã đọc: shortlist/server/main.py:423; shortlist/server/main.py:442; shortlist/server/main.py:464; shortlist/server/main.py:473; shortlist/server/main.py:474; shortlist/server/main.py:475. require_setup_access tại shortlist/server/api/setup.py:101 là lời gọi thủ công trong handler, không phải Depends.",
    "Phân loại từng suspect http_that qua httpx.Client: scripts/fetch_demo_posters.py:43; scripts/fetch_demo_posters.py:52; scripts/fetch_demo_posters.py:78. Nguồn client: scripts/fetch_demo_posters.py:39; scripts/fetch_demo_posters.py:69.",
    "Phân loại từng suspect http_that qua wrapper http_retry: shortlist/engine/clients/arr.py:116; shortlist/engine/clients/arr.py:139; shortlist/engine/clients/mdblist.py:141; shortlist/engine/clients/mdblist.py:192; shortlist/engine/clients/plex_pms.py:1802; shortlist/engine/clients/plex_pms.py:1815; shortlist/engine/clients/plex_pms.py:1870; shortlist/engine/clients/plex_pms.py:1895; shortlist/engine/clients/plex_pms.py:1951; shortlist/engine/clients/plex_pms.py:2044; shortlist/engine/clients/plex_pms.py:2129; shortlist/engine/clients/plex_pms.py:2203; shortlist/engine/clients/plex_pms.py:2619; shortlist/engine/clients/plex_pms.py:2675; shortlist/engine/clients/plex_pms.py:2773. Wrapper chuyển tới httpx.request tại shortlist/engine/clients/http_retry.py:181.",
    "Phân loại từng suspect http_that qua wrapper http_retry, tiếp: shortlist/engine/clients/plextv.py:146; shortlist/engine/clients/plextv.py:206; shortlist/engine/clients/plextv.py:269; shortlist/engine/clients/plextv.py:362; shortlist/engine/clients/plextv.py:379; shortlist/engine/clients/plextv.py:387; shortlist/engine/clients/search.py:471; shortlist/engine/clients/seerr.py:174; shortlist/engine/clients/seerr.py:197; shortlist/engine/clients/trakt.py:45. Đường gọi được xác nhận tại shortlist/engine/clients/http_retry.py:122; shortlist/engine/clients/http_retry.py:155; shortlist/engine/clients/http_retry.py:181.",
    "Phân loại suspect shortlist/engine/clients/plex_pms.py:551 là http_that: original lấy từ session.request tại shortlist/engine/clients/plex_pms.py:547; session là requests.Session tạo tại shortlist/engine/clients/plex_pms.py:433, được truyền qua shortlist/engine/clients/plex_pms.py:629 và shortlist/engine/clients/plex_pms.py:635.",
    "Phân loại từng suspect http_that gọi trực tiếp httpx: shortlist/engine/clients/http_retry.py:181; shortlist/engine/clients/plextv.py:298; shortlist/server/api/support.py:1946; shortlist/server/services/notify.py:215; shortlist/server/services/setup_probe.py:19; shortlist/server/version_check.py:50; shortlist/server/version_check.py:81.",
    "Phân loại từng suspect http_that qua httpx.AsyncClient: shortlist/server/api/setup.py:106; shortlist/server/api/setup.py:125; shortlist/server/auth.py:118; shortlist/server/auth.py:184; shortlist/server/auth.py:373; shortlist/server/auth.py:407; shortlist/server/auth.py:415. Nguồn client tương ứng: shortlist/server/api/setup.py:105; shortlist/server/api/setup.py:124; shortlist/server/auth.py:117; shortlist/server/auth.py:183; shortlist/server/auth.py:372; shortlist/server/auth.py:406.",
    "Phân loại từng suspect can_giai_thich: shortlist/server/api/requests.py:242 là session.delete đối tượng ORM; shortlist/server/api/requests.py:674 là session.get(RequestCandidate, ...); shortlist/server/api/requests.py:763 là session.get(AssistantRequestDispatch, ...); shortlist/server/services/notify.py:258, shortlist/server/services/notify.py:290 và shortlist/server/services/notify.py:371 là session.get(Run, ...); shortlist/server/services/notify.py:334 là session.get(Job, ...). Đây là thao tác CSDL, hợp lý để giải thích receiver session nhưng không phải HTTP; nguồn SQLAlchemy được xác nhận tại shortlist/server/services/notify.py:40 và shortlist/server/db/session.py:43.",
    "http_bo_sot đếm vị trí gọi trong source, không đếm số giao dịch mạng độc lập. Bốn vị trí caller/transport là shortlist/engine/clients/plex_pms.py:397, shortlist/engine/clients/search.py:306, shortlist/engine/clients/tautulli.py:31 và shortlist/engine/clients/tmdb.py:92. super().send thuộc lớp kế thừa requests.adapters.HTTPAdapter: shortlist/engine/clients/plex_pms.py:31; shortlist/engine/clients/plex_pms.py:383.",
    "Ba vị trí bổ sung trong http_bo_sot là lời gọi chuyển tiếp nội bộ _send tại shortlist/engine/clients/http_retry.py:122, shortlist/engine/clients/http_retry.py:141 và shortlist/engine/clients/http_retry.py:155; cả ba đi tới httpx.request ở shortlist/engine/clients/http_retry.py:181. Chúng được liệt kê riêng để phân biệt với bốn điểm caller/transport và tránh hiểu thành bảy hoạt động mạng độc lập.",
    "decorators_refused trong gói rỗng nên không có mục để phán xét. Ngoài danh sách suspects, source có đăng ký Starlette Route bằng append tại shortlist/server/main.py:476; đây là registration chưa có trong gói, không phải HTTP outbound nên không đưa vào http_bo_sot và không cộng vào số registration của suspects."
  ]
}
```