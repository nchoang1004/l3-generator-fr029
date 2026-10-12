# Rà soát gold route FR-029: 19 case development

Người rà: Claude (độc lập). Ngày: 07/10/2026. Chỉ đọc, không chạy code của case.

## Kết luận

Không tìm thấy lỗi gold loại A, B hoặc C trong 19 case.
Mọi route trong gold khớp source về method, path đầy đủ, handler và vị trí.
Không có route nào trong phạm vi chấm mà gold bỏ sót.
Có 2 vấn đề của scorer (loại E) và 1 điểm cần quyết định cách hiểu spec (loại D).
Cả 19 gold vẫn ở trạng thái `candidate`, chưa có người duyệt độc lập. Phần lớn gold không viết mù (xem `provenance`).

## Cách kiểm

- Danh sách case lấy từ `manifest.json`: split `development`, family `fastapi-docs`, `orders-fixture`, `netflix-dispatch`. Kết quả 19 case, giống logic của `slice/tools/fr029_golden_routes.py`.
- Đọc tay mọi file `.py` có route hoặc có lời gọi `include_router`/`mount`.
- Duyệt cây cú pháp (`ast.parse`, không chạy code) các file trong `scored_scope.exhaustive.route` để đếm decorator route và lời gọi `add_api_route`/`add_route`/`add_websocket_route`/`api_route`. So từng decorator với gold: method, đuôi path, tên handler, dòng bắt đầu và kết thúc của bằng chứng.
- Tính lại sha256 từng file nguồn, so với `source-manifest.json` và với `evidence[].sha256` của gold. Kiểm tra không có file thừa hoặc thiếu so với manifest.

## Độ phủ từng case

| Case | Route gold | Decorator trong phạm vi | Prefix đã dò tay | sha256 khớp | Kết quả |
|---|---|---|---|---|---|
| orders-base | 1 | 1 | `include_router(prefix="/api/v1")` | có | đúng |
| orders-prefix | 1 | 1 | `/api/v2` | có | đúng |
| orders-two-apps | 2 (cùng khóa chấm) | 1 | hai app, cùng `/api/v1` | có | gold đúng; xem E-1 |
| orders-wrapper-real | 1 | 1 | qua `registration.attach` → `include_router` | có | đúng |
| orders-wrapper-fake | 0 | 1 | `attach` chỉ `return router` | có | gold đúng theo cách hiểu "route phải được gắn vào app"; xem D-1 |
| orders-dynamic-prefix | 1, path `null` + limitation | 1 | `os.environ["API_PREFIX"]`, không có mặc định | có | đúng theo FR-029 "không có mặc định thì unknown" |
| orders-conditional-route | 1, có `condition` | 1 | `include_router` trong `if` | có | gold đúng; xem E-2 |
| orders-derived-tablename | 1 | 1 | `/api/v1` | có | đúng |
| orders-mount | 1 | 1 | `mount("/api")` + `prefix="/v1"` | có | đúng (`/api/v1/orders`) |
| orders-plugin-import | 2 | 2 | `/api/v1` | có | đúng |
| orders-runtime-dispatch | 4 | 4 | `/api/v1` | có | đúng |
| orders-syntax-error | 1 (+ limitation file lỗi cú pháp) | 1 (`legacy.py` không parse được, không có route) | `/api/v1` | có | đúng |
| dispatch-case-read | 18 | 18 | `mount("/api/v1")` → `api_router` → `APIRouter(prefix="/{organization}")` → `prefix="/cases"` | có | đúng |
| fastapi-docs-body_updates-tutorial001 | 2 | 2 | không có | có | đúng |
| fastapi-docs-first_steps-tutorial001 | 1 | 1 | không có | có | đúng |
| fastapi-docs-handling_errors-tutorial001 | 1 | 1 | không có | có | đúng |
| fastapi-docs-path_params-tutorial001 | 1 | 1 | không có | có | đúng |
| fastapi-docs-query_params_str_validations-tutorial001 | 1 | 1 (giữ `/items/` có `/` cuối) | không có | có | đúng |
| fastapi-docs-schema_extra_example-tutorial001 | 1 | 1 | không có | có | đúng |

Tổng: 42 route gold, 41 decorator trong phạm vi. Chênh 1 do orders-two-apps (1 decorator, 2 app) trừ orders-wrapper-fake (1 decorator, 0 route).

Chuỗi prefix của dispatch-case-read đã dò tay:

- `src/dispatch/main.py:268` `app.mount("/api/v1", app=api)`
- `src/dispatch/main.py:262` `api.include_router(api_router)`
- `src/dispatch/api.py:262-264` `api_router.include_router(authenticated_organization_api_router, ...)`
- `src/dispatch/api.py:98-100` `APIRouter(prefix="/{organization}", ...)`
- `src/dispatch/api.py:191` `include_router(case_router, prefix="/cases", ...)`
- `root_path="/api/v1"` ở `main.py:79` không đổi path định tuyến. Gold không cộng nó hai lần, đúng.

## Phát hiện

| Mã | Loại | Gold file + JSON path | Source | Gold ghi | Nên là | Lý do |
|---|---|---|---|---|---|---|
| E-1 | E | `cases/orders-two-apps/gold.json` `facts[0]` (`route-app_a`), `facts[1]` (`route-app_b`) | `main.py:6-7` `app_a.include_router(router, prefix="/api/v1")` / `app_b.include_router(router, prefix="/api/v1")` | 2 route, cùng `(POST, /api/v1/orders, routes.py::create_order_endpoint)`, khác `context` | Gold giữ nguyên. Scorer cần thêm app (`context`) vào khóa, hoặc đếm theo danh sách thay cho tập | `gold_routes()` trả về `set` theo 3 trường, nên 2 fact gộp thành 1. Sản phẩm gộp hai app vẫn được TP 1/1, FN 0. Ý định của case ("Do not merge registrations from distinct apps") không được chấm |
| E-2 | E | `cases/orders-conditional-route/gold.json` `facts[0].attributes.condition`; `cases/orders-dynamic-prefix/gold.json` `facts[0].attributes.path_suffix` | `main.py:7` `if os.environ.get("ENABLE_ORDERS") == "1":`; `main.py:6` `prefix = os.environ["API_PREFIX"]` | `condition: "os.environ.get('ENABLE_ORDERS') == '1'"`; `path_suffix: "/orders"` | Gold giữ nguyên. Scorer cần chấm thêm `condition`, hoặc ghi rõ là không chấm | Scorer chỉ so method, path, handler. Sản phẩm bỏ mất điều kiện vẫn được TP. Negative expectation của case ("the condition must be kept") không được chấm |
| D-1 | D | `cases/orders-wrapper-fake/gold.json` `facts` (không có route) | `routes.py:9` `@router.post("/orders")`; `registration.py:2` `return router  # same function name, no registration` | 0 route | Cần chốt cách hiểu. Gold hiện đúng theo nghĩa "route thật sự được phục vụ" | FR-029 AC-01 nói route khai bằng decorator của `APIRouter`, không nói router phải được gắn vào app. FR-029 không có quy tắc cho router không gắn. Với gold hiện tại, sản phẩm ghi route này với path `/orders` hoặc `unknown` đều bị tính FP. Nên ghi rõ quy tắc trong FR hoặc manifest |

Không có phát hiện loại A, B, C.

## Đếm theo loại

| Loại | Số |
|---|---|
| A | 0 |
| B | 0 |
| C | 0 |
| D | 1 |
| E | 2 |

## Giới hạn

- Chỉ kiểm thuộc tính route mà scorer dùng (method, path, handler) và vị trí bằng chứng. Không kiểm fact `entity`, `reference`, kiến trúc, tham số, model, status code.
- Gold không có trường "alternate" nào ở các fact route, nên không có gì để kiểm cho loại B.
- Không đọc file reviewer, judge, adjudication trong thư mục case. Không đọc kết quả chạy sản phẩm.
- Không chạy code case. Không chạy FastAPI để đối chiếu path. Path được dò tay theo chuỗi `include_router`/`mount`.
- Route ngoài `exhaustive.route` không được kiểm. Ví dụ dispatch-case-read: route `healthcheck` ở `api.py:256`, route plugin thêm lúc chạy qua `install_plugin_events(api_router)` ở `main.py:259`. Scorer tính các route đó là `outside_scope`, không phải FP.
- Không có file test hoặc lời gọi `add_api_route`/`add_route`/`add_websocket_route` trong phạm vi của 19 case. Vì vậy quy tắc loại trừ của AC-L3GEN-029-05 chưa được bộ case này thử.
- Gold không mù: `provenance` ghi người sửa đã thấy output l3gen (case orders cũ, dispatch) hoặc đọc OpenAPI snapshot (fastapi-docs). Tôi không đánh giá ảnh hưởng của việc này.
