```json
{
  "repos": [
    {
      "repo": "dengyie_xianyu-auto-bot",
      "dependencies": {
        "params_dung": 1,
        "params_sai": [],
        "params_thieu": []
      },
      "deps_bo_sot": {
        "routes_kiem": 35,
        "items": []
      },
      "suspects": {
        "http_that": 66,
        "http_khac": 2,
        "registration": 2,
        "can_giai_thich": 0,
        "nhieu": [
          {
            "at": "utils/qr_login.py:454",
            "ly_do": "Tra cứu dictionary self.sessions, được khai báo tại utils/qr_login.py:107; không gọi HTTP."
          },
          {
            "at": "utils/qr_login.py:1030",
            "ly_do": "Tra cứu dictionary self.sessions, được khai báo tại utils/qr_login.py:107; không gọi HTTP."
          },
          {
            "at": "utils/qr_login.py:1246",
            "ly_do": "Tra cứu dictionary self.sessions, được khai báo tại utils/qr_login.py:107; không gọi HTTP."
          },
          {
            "at": "utils/qr_login.py:1360",
            "ly_do": "Tra cứu dictionary self.sessions, được khai báo tại utils/qr_login.py:107; không gọi HTTP."
          },
          {
            "at": "utils/qr_login.py:1419",
            "ly_do": "Tra cứu dictionary self.sessions, được khai báo tại utils/qr_login.py:107; không gọi HTTP."
          },
          {
            "at": "utils/qr_login.py:1428",
            "ly_do": "Tra cứu dictionary self.sessions, được khai báo tại utils/qr_login.py:107; không gọi HTTP."
          },
          {
            "at": "utils/qr_login.py:1569",
            "ly_do": "Tra cứu dictionary self.sessions, được khai báo tại utils/qr_login.py:107; không gọi HTTP."
          },
          {
            "at": "utils/qr_login.py:1600",
            "ly_do": "Tra cứu dictionary self.sessions, được khai báo tại utils/qr_login.py:107; không gọi HTTP."
          },
          {
            "at": "utils/qr_login.py:1829",
            "ly_do": "Tra cứu dictionary self.sessions, được khai báo tại utils/qr_login.py:107; không gọi HTTP."
          },
          {
            "at": "utils/qr_login.py:1963",
            "ly_do": "Tra cứu dictionary self.sessions, được khai báo tại utils/qr_login.py:107; không gọi HTTP."
          },
          {
            "at": "utils/qr_login.py:2034",
            "ly_do": "Tra cứu dictionary self.sessions, được khai báo tại utils/qr_login.py:107; không gọi HTTP."
          },
          {
            "at": "utils/xianyu_slider_stealth.py:3191",
            "ly_do": "Lệnh CDP Network.enable trên session tạo bằng new_cdp_session tại utils/xianyu_slider_stealth.py:3190; không phải HTTP client."
          },
          {
            "at": "utils/xianyu_slider_stealth.py:3192",
            "ly_do": "Lệnh CDP Network.setUserAgentOverride tại utils/xianyu_slider_stealth.py:3193, dùng session tạo tại utils/xianyu_slider_stealth.py:3190; không phải HTTP client."
          }
        ]
      },
      "http_bo_sot": [
        {
          "at": "item_polish_module.py:80",
          "code": "async with self.runtime.session.post(\n    'https://h5api.m.goofish.com/h5/mtop.taobao.idle.item.polish/1.0/',\n    params=params,\n    data=payload,\n    proxy=getattr(self.runtime, '_http_proxy_url', None),\n) as response:"
        },
        {
          "at": "item_polish_module.py:123",
          "code": "async with self.runtime.session.post(\n    'https://h5api.m.goofish.com/h5/mtop.idle.item.polish/1.0/',\n    params=params,\n    data=payload,\n    proxy=getattr(self.runtime, '_http_proxy_url', None),\n) as response:"
        },
        {
          "at": "utils/notification_dispatcher.py:454",
          "code": "async with request(webhook_url, json=data, headers=headers, timeout=10) as response:"
        },
        {
          "at": "xianyu_cookie_mixin.py:634",
          "code": "async with self.session.get(\n    'https://www.goofish.com/im',\n    proxy=self._get_proxy_url() or get_global_proxy_url(),\n    headers={\n        'cookie': self.cookies_str,\n        'Referer': 'https://www.goofish.com/',\n        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',\n    },\n    allow_redirects=True\n) as response:"
        },
        {
          "at": "xianyu_token_mixins.py:222",
          "code": "async with self.session.post(\n    api_url,\n    params=params,\n    data=data,\n    headers=headers,\n    timeout=_host.aiohttp.ClientTimeout(total=30),\n    **request_kwargs,\n) as response:"
        },
        {
          "at": "xianyu_trading_mixins.py:1862",
          "code": "async with self.session.post(\n    'https://h5api.m.goofish.com/h5/mtop.taobao.idle.pc.detail/1.0/',\n    params=params,\n    data=data,\n    proxy=getattr(self, '_http_proxy_url', None)\n) as response:"
        },
        {
          "at": "xianyu_trading_mixins.py:2130",
          "code": "async with self.session.post(\n    'https://h5api.m.goofish.com/h5/mtop.idle.web.xyh.item.list/1.0/',\n    params=params,\n    data={'data': data_val},\n    proxy=getattr(self, '_http_proxy_url', None)\n) as response:"
        }
      ],
      "decorators_refused_judgement": []
    }
  ],
  "ghi_chu": [
    "Chỉ đọc gói và source của repo được chỉ định, tìm kiếm bằng rg; không sửa file, không chạy code repo, không đọc slice/, HANDOFF, docs/ hoặc .aide/. Phạm vi HTTP áp dụng các ngoại lệ FR-028 đã nêu.",
    "Dependency require_captcha_control_key: params=[] là đúng. Chữ ký chỉ nhận Request tại api_captcha_remote.py:72. Header X-Captcha-Control-Key và Authorization được đọc thủ công tại api_captcha_remote.py:46, api_captcha_remote.py:47 và api_captcha_remote.py:77, không phải tham số FastAPI tự thêm từ khai báo dependency.",
    "Dependency reply_server.verify_token: params=[] là đúng. Chữ ký nhận Request và Depends(security) tại reply_server.py:666, reply_server.py:667, reply_server.py:668. Authorization và auth_token được đọc thủ công tại reply_server.py:649 và reply_server.py:652; security là HTTPBearer tại reply_server.py:146, thuộc auth/securitySchemes.",
    "Dependency reply_server.get_current_user: params=[] là đúng. Chuỗi get_current_user → require_auth → verify_token → security nằm tại reply_server.py:707, reply_server.py:700, reply_server.py:668 và reply_server.py:146; không sinh header/query/cookie/path khai báo.",
    "Dependency reply_server.require_admin: params=[] là đúng; Depends(get_current_user) tại reply_server.py:724, tiếp tục chuỗi tại reply_server.py:707, reply_server.py:700 và reply_server.py:668.",
    "Dependency reply_server.get_current_user_optional: params=[] là đúng; Depends(verify_token) tại reply_server.py:712, chữ ký dependency con tại reply_server.py:666.",
    "Dependency reply_server.verify_admin_token: params=[] là đúng; Depends(verify_token) tại reply_server.py:686, chữ ký dependency con tại reply_server.py:666.",
    "Dependency verify_dependency: params=[] là đúng. Đây là tham số factory tại app/api/routers/auth.py:13, được dùng trong Depends tại app/api/routers/auth.py:22 và được truyền verify_token tại reply_server.py:881.",
    "Dependency security: params=[] là đúng. Instance HTTPBearer(auto_error=False) tại reply_server.py:146 được truyền vào factory tại reply_server.py:882 và dùng tại app/api/routers/auth.py:23, app/api/routers/auth.py:46; thông tin xác thực không tính thành params_thieu.",
    "Dependency reply_server.require_xianyu_reply_api_key: tham số header X-Internal-API-Key được chấm đúng, là tham số request duy nhất trong các dependency của gói. Alias được khai báo rõ tại reply_server.py:1236; route sử dụng tại app/api/routers/orderschat.py:148.",
    "Mẫu route, accountlogin: POST /manual-cookie-import tại app/api/routers/accountlogin.py:25; GET /manual-cookie-import/check/{session_id} tại app/api/routers/accountlogin.py:83; POST /password-login tại app/api/routers/accountlogin.py:143. Cả ba dùng dependency đã có trong gói, lần lượt tại app/api/routers/accountlogin.py:28, app/api/routers/accountlogin.py:86, app/api/routers/accountlogin.py:146.",
    "Mẫu route, adminops: GET /ai-reply-settings/{cookie_id}, PUT /ai-reply-settings/{cookie_id}, GET /ai-reply-settings tại app/api/routers/adminops.py:52, app/api/routers/adminops.py:71, app/api/routers/adminops.py:107. Dependency đã có trong gói tại app/api/routers/adminops.py:53, app/api/routers/adminops.py:72, app/api/routers/adminops.py:108.",
    "Mẫu route, auth: GET /verify và POST /logout tại app/api/routers/auth.py:19, app/api/routers/auth.py:42. Dependency đã có trong gói tại app/api/routers/auth.py:22, app/api/routers/auth.py:23, app/api/routers/auth.py:46.",
    "Mẫu route, cookies: GET /cookies, GET /cookies/details, POST /cookies và GET /cookies/check tại app/api/routers/cookies.py:17, app/api/routers/cookies.py:27, app/api/routers/cookies.py:63, app/api/routers/cookies.py:828. Dependency đã có trong gói tại app/api/routers/cookies.py:18, app/api/routers/cookies.py:28, app/api/routers/cookies.py:64, app/api/routers/cookies.py:830.",
    "Mẫu route, keywords: GET /keywords/{cid}, GET /keywords-with-item-id/{cid}, POST /keywords/{cid} tại app/api/routers/keywords.py:22, app/api/routers/keywords.py:49, app/api/routers/keywords.py:79. Dependency đã có trong gói tại app/api/routers/keywords.py:23, app/api/routers/keywords.py:50, app/api/routers/keywords.py:80.",
    "Mẫu route, login: GET /captcha/generate, GET /captcha/check-required, GET /login.html không khai báo Depends tại app/api/routers/login.py:454, app/api/routers/login.py:455, app/api/routers/login.py:500, app/api/routers/login.py:501, app/api/routers/login.py:513, app/api/routers/login.py:514. GET /admin/security/login-stats dùng dependency đã có trong gói tại app/api/routers/login.py:826, app/api/routers/login.py:827.",
    "Mẫu route, notifications: GET /notification-channels, POST /notification-channels, GET /notification-channels/{channel_id} tại app/api/routers/notifications.py:17, app/api/routers/notifications.py:26, app/api/routers/notifications.py:41. Dependency đã có trong gói tại app/api/routers/notifications.py:18, app/api/routers/notifications.py:27, app/api/routers/notifications.py:42.",
    "Mẫu route, orderschat: POST /send-message không khai báo Depends tại app/api/routers/orderschat.py:29, app/api/routers/orderschat.py:30. POST /xianyu/reply và POST /api/orders/history-sync dùng dependency đã có trong gói tại app/api/routers/orderschat.py:145, app/api/routers/orderschat.py:148, app/api/routers/orderschat.py:190, app/api/routers/orderschat.py:191.",
    "Mẫu route, settings: GET /system-settings, PUT /system-settings/{key}, GET /api/sales dùng dependency đã có trong gói tại app/api/routers/settings.py:19, app/api/routers/settings.py:20, app/api/routers/settings.py:31, app/api/routers/settings.py:32, app/api/routers/settings.py:250, app/api/routers/settings.py:254. GET /registration-status không khai báo Depends tại app/api/routers/settings.py:54, app/api/routers/settings.py:55.",
    "Mẫu route, trading: GET /items/{cid}, POST /upload-image, GET /cards tại app/api/routers/trading.py:23, app/api/routers/trading.py:62, app/api/routers/trading.py:99. Dependency đã có trong gói tại app/api/routers/trading.py:24, app/api/routers/trading.py:65, app/api/routers/trading.py:100.",
    "Mẫu route, captcha: GET /api/captcha/sessions, GET /api/captcha/session/{session_id}, GET /api/captcha/screenshot/{session_id}; prefix tại api_captcha_remote.py:20, decorator và dependency tại api_captcha_remote.py:284, api_captcha_remote.py:285, api_captcha_remote.py:301, api_captcha_remote.py:302, api_captcha_remote.py:318, api_captcha_remote.py:319. Dependency đã có trong gói. Tổng mẫu được liệt kê là 35 route.",
    "Cấp router: không khai báo dependencies chung tại api_captcha_remote.py:20, app/api/routers/accountlogin.py:24, app/api/routers/adminops.py:51, app/api/routers/auth.py:17, app/api/routers/cookies.py:16, app/api/routers/keywords.py:21, app/api/routers/login.py:453, app/api/routers/notifications.py:16, app/api/routers/orderschat.py:28, app/api/routers/settings.py:18, app/api/routers/trading.py:22.",
    "Cấp app/include_router: không thêm dependencies chung trong FastAPI tại reply_server.py:868 hoặc các lần include_router tại reply_server.py:878, reply_server.py:889, reply_server.py:4901, reply_server.py:4909, reply_server.py:4910, reply_server.py:4911, reply_server.py:4912, reply_server.py:4913, reply_server.py:4914, reply_server.py:4915, reply_server.py:4916. Các decorator của 35 route đã liệt kê cũng không thêm dependencies=[...].",
    "Phân loại http_that qua requests: ai_reply_engine.py:174, ai_reply_engine.py:245, ai_reply_engine.py:285, ai_reply_engine.py:323, ai_reply_engine.py:374, ai_reply_engine.py:408; utils/build_cookies.py:64, utils/build_cookies.py:72; utils/qr_login_lite.py:134, utils/qr_login_lite.py:178, utils/qr_login_lite.py:240, utils/qr_login_lite.py:281, utils/qr_login_lite.py:302; utils/refresh_util.py:1926, utils/refresh_util.py:1981, utils/refresh_util.py:2051; utils/slider_orchestrator.py:160; utils/xianyu_slider_stealth.py:223. Nguồn Session tương ứng tại utils/build_cookies.py:58, utils/qr_login_lite.py:124, utils/build_cookies.py:92, utils/refresh_util.py:1852, utils/xianyu_slider_stealth.py:164.",
    "Phân loại http_that qua httpx: utils/qr_login.py:383, utils/qr_login.py:394, utils/qr_login.py:422, utils/qr_login.py:1173, utils/qr_login.py:1200, utils/qr_login.py:1633, utils/qr_login.py:1659, utils/qr_login.py:1690, utils/qr_login.py:1739, utils/qr_login.py:1818. Các AsyncClient được tạo tại utils/qr_login.py:372, utils/qr_login.py:1166, utils/qr_login.py:1631, utils/qr_login.py:1688, utils/qr_login.py:1738, utils/qr_login.py:1817.",
    "Phân loại http_that qua aiohttp, nhóm 1: XianyuAutoAsync.py:2270, XianyuAutoAsync.py:3989; app/api/routers/notifications.py:329, app/api/routers/notifications.py:357, app/api/routers/notifications.py:374, app/api/routers/notifications.py:391, app/api/routers/notifications.py:407; auto_updater.py:326, auto_updater.py:348, auto_updater.py:496; db_manager/users.py:689; secure_confirm_decrypted.py:204; secure_freeshipping_decrypted.py:147. Nguồn client gồm XianyuAutoAsync.py:3933, app/api/routers/notifications.py:328, app/api/routers/notifications.py:356, app/api/routers/notifications.py:373, app/api/routers/notifications.py:390, app/api/routers/notifications.py:406, auto_updater.py:324, auto_updater.py:484, db_manager/users.py:686, secure_confirm_decrypted.py:203; session được truyền vào SecureFreeshipping tại XianyuAutoAsync.py:2974.",
    "Phân loại http_that qua aiohttp, nhóm 2: utils/image_uploader.py:150; utils/item_publisher.py:464, utils/item_publisher.py:777; utils/notification_dispatcher.py:243, utils/notification_dispatcher.py:274, utils/notification_dispatcher.py:301, utils/notification_dispatcher.py:337, utils/notification_dispatcher.py:470, utils/notification_dispatcher.py:488; utils/order_history_sync.py:328; utils/rate_service.py:179, utils/rate_service.py:302. Nguồn client tại utils/image_uploader.py:36, utils/item_publisher.py:69, utils/notification_dispatcher.py:242, utils/notification_dispatcher.py:273, utils/notification_dispatcher.py:300, utils/notification_dispatcher.py:336, utils/notification_dispatcher.py:469, utils/notification_dispatcher.py:487, utils/order_history_sync.py:267, utils/rate_service.py:176, utils/rate_service.py:299.",
    "Phân loại http_that qua aiohttp, nhóm 3: xianyu_delivery_mixin.py:1944, xianyu_delivery_mixin.py:1948, xianyu_delivery_mixin.py:2086, xianyu_delivery_mixin.py:2225; xianyu_messaging_mixins.py:158, xianyu_messaging_mixins.py:218, xianyu_messaging_mixins.py:282, xianyu_messaging_mixins.py:360, xianyu_messaging_mixins.py:560, xianyu_messaging_mixins.py:568, xianyu_messaging_mixins.py:603, xianyu_messaging_mixins.py:637, xianyu_messaging_mixins.py:4012. Session dùng chung thuộc lớp ghép mixin tại XianyuAutoAsync.py:277 và được tạo tại XianyuAutoAsync.py:3933; session cục bộ tại xianyu_messaging_mixins.py:157, xianyu_messaging_mixins.py:217, xianyu_messaging_mixins.py:281, xianyu_messaging_mixins.py:359, xianyu_messaging_mixins.py:558, xianyu_messaging_mixins.py:602, xianyu_messaging_mixins.py:636.",
    "Phân loại http_khac: generate_update_manifest.py:216 dùng urllib.request, import tại generate_update_manifest.py:20; reply_server.py:374 dùng urllib.request, import alias tại reply_server.py:8.",
    "Phân loại registration: api_captcha_remote.py:158 và reply_server.py:1093 là đăng ký WebSocket thật trên APIRouter/FastAPI, receiver được tạo tại api_captcha_remote.py:20 và reply_server.py:868. Gói đưa hai decorator WebSocket vào suspects với looks_like=route; chúng không phải lời gọi HTTP đi ra. decorators_refused rỗng nên không có mục cần phán xét.",
    "Bảy vị trí HTTP bỏ sót đều gọi trực tiếp aiohttp. Token/trading dùng session của lớp ghép mixin tại XianyuAutoAsync.py:277, được tạo tại XianyuAutoAsync.py:3933. ItemPolishModule nhận chính runtime đó tại xianyu_trading_mixins.py:2306 và lưu tại item_polish_module.py:23. Cookie mixin tạo aiohttp.ClientSession tại xianyu_cookie_mixin.py:632.",
    "Tại utils/notification_dispatcher.py:454, request là alias trực tiếp của session.post hoặc session.put, được gán tại utils/notification_dispatcher.py:450 trên aiohttp.ClientSession tạo tại utils/notification_dispatcher.py:449. Đây là một vị trí gọi HTTP trực tiếp bị bỏ sót, không phải hàm bọc của dự án.",
    "Các lời gọi qua hàm bọc được ghi riêng, không cộng vào http_bo_sot: _post_mtop_api tại XianyuAutoAsync.py:4017, XianyuAutoAsync.py:4032, XianyuAutoAsync.py:4051, với HTTP trực tiếp nằm tại XianyuAutoAsync.py:3989; wrapper polish tại xianyu_trading_mixins.py:2309, xianyu_trading_mixins.py:2312, xianyu_trading_mixins.py:2315; build_initial_session tại utils/qr_login_lite.py:124 và utils/build_cookies.py:97, với HTTP trực tiếp tại utils/build_cookies.py:64 và utils/build_cookies.py:72; gọi provider qua hàm dự án tại ai_reply_engine.py:497 và ai_reply_engine.py:557, phân nhánh tại ai_reply_engine.py:678, ai_reply_engine.py:680, ai_reply_engine.py:682, ai_reply_engine.py:684, ai_reply_engine.py:686, ai_reply_engine.py:688, ai_reply_engine.py:690.",
    "Lời gọi context.request.post tại utils/slider_stealth_mixins.py:4164, receiver lấy từ context.request tại utils/slider_stealth_mixins.py:4161, không thuộc ba thư viện httpx/requests/aiohttp nên không đưa vào http_bo_sot."
  ]
}
```