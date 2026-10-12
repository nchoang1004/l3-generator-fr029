```json
{
  "repos": [
    {
      "repo": "3441293738_creatorhub",
      "dependencies": {
        "params_dung": 0,
        "params_sai": [],
        "params_thieu": []
      },
      "deps_bo_sot": {
        "routes_kiem": 30,
        "items": []
      },
      "suspects": {
        "http_that": 7,
        "http_khac": 2,
        "registration": 2,
        "can_giai_thich": 39,
        "nhieu": []
      },
      "http_bo_sot": [],
      "decorators_refused_judgement": []
    }
  ],
  "ghi_chu": [
    "Gói có dependencies và decorators_refused rỗng. params_dung=0 nghĩa là không có tham số dependency trong gói để chấm, không phải endpoint không có tham số. Không phát hiện Depends, Security, Annotated dependency hoặc cấu hình dependencies trong source thuộc phạm vi quét. FastAPI được khởi tạo không có dependencies tại app/main.py:556.",
    "Mẫu kiểm gồm 29 route trong app/main.py và 1 route desktop; đã đọc decorator và toàn bộ chữ ký handler. Không thấy dependency cấp handler/decorator tại: app/main.py:1316, app/main.py:1499, app/main.py:1532, app/main.py:1701, app/main.py:2183, app/main.py:2263, app/main.py:2369, app/main.py:2743, app/main.py:3081, app/main.py:3286, app/main.py:3440, app/main.py:3480, app/main.py:3821, app/main.py:3986, app/main.py:4233, app/main.py:4345, app/main.py:4816, app/main.py:5162, app/main.py:5347, app/main.py:5434, app/main.py:6076, app/main.py:6209, app/main.py:6699, app/main.py:6840, app/main.py:7282, app/main.py:7435, app/main.py:8213, app/main.py:9193, app/main.py:10303, desktop/launcher.py:191.",
    "Cấp router/app: không phát hiện APIRouter/include_router hay dependency cấp router; các route mẫu đăng ký trực tiếp trên app tạo tại app/main.py:556. Route desktop dùng cùng app được import tại desktop/launcher.py:184. app/main.py:557 đăng ký middleware, không phải dependency.",
    "Không tính tham số trực tiếp của handler thành dependency: body KeywordCollectionIn là model BaseModel tại app/main.py:6445 và được nhận cùng Request tại app/main.py:6700; upload dùng File tại app/main.py:9194. get_session được gọi trực tiếp trong thân handler, ví dụ app/main.py:1536, và trả về SQLModel Session tại app/db.py:195.",
    "http_that gồm đúng 7 dòng: app/engine/compose.py:112; app/engine/downloader.py:88; app/main.py:4899; app/main.py:4944; app/notifier/__init__.py:30; app/notifier/__init__.py:47; app/notifier/__init__.py:62. Receiver đều là httpx.AsyncClient, được tạo hoặc khai kiểu tại app/engine/compose.py:111, app/engine/downloader.py:78, app/main.py:4898, app/main.py:4941, app/notifier/__init__.py:29, app/notifier/__init__.py:46, app/notifier/__init__.py:61.",
    "http_khac gồm creatorhub.py:209 và desktop/updates.py:160: cả hai gọi urllib.request.urlopen.",
    "registration gồm app/main.py:6840 và app/main.py:8213: cả hai là decorator @app.api_route thật trên FastAPI app tại app/main.py:556, đăng ký GET/HEAD. Xếp theo bản chất đăng ký route; việc đưa chúng vào suspects trái với mô tả gói rằng decorator route không nằm trong danh sách này. Chúng không phải mục decorators_refused.",
    "can_giai_thich gồm 39 dòng thao tác CSDL, không phải HTTP: app/main.py:285, app/main.py:1949, app/main.py:2267, app/main.py:2296, app/main.py:2297, app/main.py:2324, app/main.py:2326, app/main.py:2362, app/main.py:2674, app/main.py:2746, app/main.py:2893, app/main.py:2918, app/main.py:2954, app/main.py:3025, app/main.py:3044, app/main.py:4246, app/main.py:4260, app/main.py:4273, app/main.py:4276, app/main.py:4293, app/main.py:4400, app/main.py:4410, app/main.py:4423, app/main.py:5931, app/main.py:6704, app/main.py:6731, app/main.py:6738, app/main.py:6775, app/main.py:6787, app/main.py:6808, app/main.py:6901, app/main.py:6917, app/main.py:6936, app/main.py:6959, app/main.py:6967, app/main.py:6971, app/main.py:6972, app/main.py:6979, app/main.py:8559. Session được định nghĩa tại app/db.py:193 và khởi tạo tại app/db.py:195; hai helper nhận session từ caller tại app/main.py:6847, app/main.py:6848, app/main.py:8631, app/main.py:8632.",
    "Sau quét văn bản toàn repo trong phạm vi FR-028 và đối chiếu receiver, không phát hiện lời gọi trực tiếp httpx/requests/aiohttp nào thiếu khỏi suspects. Các lời gọi httpx trực tiếp là 7 vị trí đã liệt kê. Không đưa lời gọi trong test vào http_bo_sot.",
    "Các lời gọi qua hàm bọc được ghi riêng, không tính HTTP trực tiếp: app/main.py:5887, app/main.py:6047 và app/engine/downloader.py:63 gọi _download_one; lời gọi trực tiếp bên trong ở app/engine/downloader.py:88 đã có trong gói. app/main.py:5451 và app/engine/monitor.py:3766 gọi compose.generate; lời gọi trực tiếp bên trong ở app/engine/compose.py:112 cũng đã có trong gói.",
    "curl_cffi.requests là thư viện khác, không phải requests thuộc phạm vi http_bo_sot. Nguồn import được đối chiếu tại app/netfp.py:39, app/platforms/douyin/client.py:15, app/platforms/douyin/qrlogin.py:20, app/platforms/douyin/resolve.py:7, app/platforms/douyin/signing/mstoken.py:11, app/platforms/kuaishou/resolve.py:15, app/platforms/xhs/client.py:62, app/platforms/xhs/creator_api.py:20, app/platforms/xhs/resolve.py:11. Ví dụ lời gọi thuộc thư viện này: app/netfp.py:43, app/platforms/douyin/qrlogin.py:84, app/platforms/xhs/client.py:116 và app/platforms/xhs/creator_api.py:144."
  ]
}
```