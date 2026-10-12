# Rà soát golden v1: igorbenav và fastapi_best_architecture

Ngày 07/10/2026. Người rà: Claude (độc lập, chỉ đọc). Chỉ sửa file này.

## Kết luận

- Đường dẫn, method, handler, request model của cả hai gold khớp source. Không thấy route decorator nào bị sót (lớp C = 0).
- Có 4 chỗ gold sai giá trị (lớp A). Cả 4 đều làm scorer chấm sai một route đúng.
- 25 route plugin của FBA giữ `{prefix}` dù `plugin.toml` có trong repo. Theo FR-029 thì chấp nhận được (D). Nhưng scorer sẽ chấm trượt công cụ nào đọc đúng prefix thật (E).
- Scorer có thêm một lỗi so tên kiểu `dict[...]` (E). Lỗi này chưa chạy để xác nhận, mới suy từ code.

## Phạm vi đã rà

| Hạng mục | igorbenav (final-r3) | FBA (final-r2) |
|---|---|---|
| Commit source | 765efec…, khớp gold | 123a44a…, khớp gold |
| Route trong gold | 34 | 139 (138 decorator + 1 Socket.IO) |
| Decorator route trong source (ngoài tests, bỏ docstring) | 34. Grep ra 37; 3 cái nằm trong docstring (`http_exceptions.py:65`, `cache/decorator.py:58`, `database/session.py:137`) | 138. Grep ra 147; 9 cái nằm trong docstring (`common/pagination.py`, `common/response/response_schema.py`). 5 cái trong `api.jinja` là template |
| method, path đầy đủ, handler, dòng decorator, status_code | Đủ 34/34. Dùng script `ast` đối chiếu, prefix lần tay | Đủ 138/138. Dùng script `ast`, bảng prefix lần tay cho cả 30 file route. Đọc tay khoảng 10 route |
| response model | Đủ 34/34 | Đủ 138/138 |
| request model | Đủ 34/34 (đọc tay tham số) | Đủ 138/138 (liệt kê tham số body, đọc tay) |
| Chuỗi prefix | `app` → `""` → `/api` → `/v1` → `/users`, `/tiers`, `/rate-limits`, `/auth`, `/api-keys` | Đủ mọi nhóm: auth, logs, monitors, sys, task, 3 plugin ứng dụng, 3 plugin mở rộng (đọc `plugin.toml`, `plugin/router.py`, `plugin/core.py`) |
| `add_api_route`, `add_route`, `add_websocket_route` | Không có | Không có |
| Lời gọi HTTP (`httpx`, `requests`, `aiohttp`) | Không có trong source; gold không ghi mục nào, đúng | Chỉ 1 (`utils/request_parse.py:47-49`), gold có, đúng |
| Route đăng ký có điều kiện | Docs route (`show_docs`), OAuth router của thư viện; gold đã ghi uncertain | Plugin; gold đã ghi uncertain |

Không rà: entities, data_access, config, dependencies, auth, evidence quote của từng route (chỉ xem dòng bắt đầu), external_calls loại khác http_api.

## Phát hiện

### A. Gold sai giá trị

| # | Gold JSON path | Source | Gold | Đúng | Lý do |
|---|---|---|---|---|---|
| A1 | igorbenav `routes[13].response_model` (DELETE `/api/v1/api-keys/{key_id}`) | `backend/src/modules/api_keys/routes.py:174,198`: `status_code=204,` … `) -> None:` | chuỗi `"None"` | `null` | `-> None` nghĩa là không có response model. Gold ghi chuỗi `"None"`, trong khi chỗ khác dùng `null`. Scorer so `_short("None")` = `"None"` với `None` của công cụ, nên route đúng luôn bị chấm sai model |
| A2 | igorbenav `routes[6]`, `routes[7]` `.response_model` (`/docs`, `/redoc`) | `backend/src/infrastructure/app_factory.py:314`: `async def get_swagger_documentation() -> fastapi.responses.HTMLResponse:` (tương tự dòng 318) | `fastapi.responses.HTMLResponse` | `null` | FastAPI không lấy kiểu trả về làm response model khi kiểu đó là lớp con của `Response`. `HTMLResponse` không phải model. Gold không nhất quán: `download_code` (FBA) trả Response nhưng ghi `null` |
| A3 | FBA `routes[50].response_model` (GET `/api/v1/sys/plugins/{plugin}`) | `backend/app/admin/api/v1/sys/plugin.py:68`: `async def download_plugin(...) -> StreamingResponse:` | `StreamingResponse` | `null` | Cùng lý do A2 |
| A4 | FBA `routes[87]` (WEBSOCKET `/ws/socket.io`, handler `common/socketio/server.py::connect`) | `backend/common/socketio/server.py:32`: `@sio.event(namespace='*')` | Có trong danh sách route | Không thuộc tập route của FR-029 | FR-029 chỉ tính decorator của `FastAPI`/`APIRouter`. Đây là handler sự kiện của python-socketio; method `WEBSOCKET` do gold tự đặt. Scorer sẽ tính 1 FN cho mọi công cụ làm đúng spec |

Ghi chú A2, A3: nếu nhóm quyết định "response model = mọi kiểu trả về khai báo" thì đổi thành D. Dù chọn cách nào, gold cần một quy tắc chung cho `HTMLResponse`, `StreamingResponse` và `download_code`.

### C. Gold sót mục

Không có. igorbenav: 34/34 decorator có trong gold. FBA: 138/138 decorator có trong gold.

### D. Mơ hồ / cách hiểu spec

| # | Vị trí | Nội dung |
|---|---|---|
| D1 | FBA `routes[106..131]` trừ `[126]` (25 route của plugin config, dict, notice) | Gold ghi `/api/v1/sys{prefix}…` và nói `plugin.toml` nằm ngoài scope. Nhưng file có trong repo: `backend/plugin/config/plugin.toml` (`prefix = "/configs"`), `dict/plugin.toml` (`/dict-datas`, `/dict-types`), `notice/plugin.toml` (`/notices`). `plugin/router.py:34-35,65-70` gắn prefix này vào router `backend.app.admin.api.v1.sys`. Path thật: `/api/v1/sys/configs/all`, `/api/v1/sys/dict-datas/type-codes/{code}`, `/api/v1/sys/notices/{pk}`… FR-029 cho phép `unknown` khi prefix đọc từ cấu hình không có mặc định trong code, nên placeholder hợp lệ. Phần `/api/v1/sys` và `extend = "admin"` của gold là đúng |
| D2 | igorbenav `routes[6..8]` | Ở môi trường mặc định (development), `serve_builtin_docs` đúng (`app_factory.py:262`). FastAPI đăng ký route docs có sẵn trước, nên 3 handler tự viết bị che. Gold vẫn ghi theo decorator và đã nêu trong uncertain. Hợp với FR-029 |
| D3 | FBA `update_user_email` (`sys/user.py`), `send_email_captcha` (`plugin/email/api/v1/email.py`) và các route có `Body(embed=True)` | Gold ghi `request_model: null`. FastAPI tự sinh model ẩn `Body_…`. Không phải tên model khai trong code, nên `null` hợp lý; cần ghi rõ quy tắc |
| D4 | FBA `routes[38]`, `routes[47]` (upload file) | Body multipart `UploadFile` → `null`. Hợp lý, cùng quy tắc D3 |

### E. Lỗi scorer / định dạng

| # | Vị trí | Nội dung |
|---|---|---|
| E1 | `slice/tools/fr029_golden4.py` hàm `compare`, dòng tạo `want` | Gold path có `{prefix}` thành key `None`, chỉ khớp khi công cụ ghi path `unknown`. Công cụ đọc `plugin.toml` và ghi đúng `/api/v1/sys/configs/all` sẽ bị tính 1 FP + 1 FN. Ảnh hưởng 25 route FBA (repo dùng để đo). Đề xuất: placeholder chấp nhận cả `unknown` và path thật (hoặc ghi path thật vào gold như phương án thay thế) |
| E2 | `fr029_golden4.py` `_type_name` | Khi route không có model, scorer lấy tên kiểu từ schema: `object` → `"dict"`. Gold igorbenav ghi `dict[str, Any]` (11 route) và `dict[str, str]` (9 route). `_short` giữ nguyên hai chuỗi này, nên `"dict"` không bao giờ khớp. Chưa chạy; suy từ code. Nếu công cụ biểu diễn kiểu này bằng schema thì 20 route bị chấm sai model. igorbenav là repo "chỉnh prompt", không phải repo đo |
| E3 | Gắn với A1 | Chuỗi `"None"` cần đổi thành `null`, hoặc scorer coi `"None"` như `None` |

### B. Phương án thay thế chấp nhận sai

Không có. Hai gold này không có trường phương án thay thế cho route và lời gọi HTTP.

## Giới hạn

- Không chạy code repository. Chuỗi prefix lần bằng tay, tên model lấy bằng `ast.unparse`. Không so khoảng trắng hay dấu nháy gốc.
- Script so sánh để trong scratchpad, không lưu vào repo.
- Không đọc file judge, check, key, draft trong golden-v2; không đọc HANDOFF, ket-qua-chay, báo cáo review khác.
- Không rà route ở `tests/` (gold đã loại theo scope). Không rà route sinh động từ thư viện (crudauth OAuth, sqladmin, fastapi-pagination); gold đã nêu trong uncertain.
- E2 chưa kiểm bằng lần chạy thật.
