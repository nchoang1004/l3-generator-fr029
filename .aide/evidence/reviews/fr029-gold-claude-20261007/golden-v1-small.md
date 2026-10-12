# Kiểm tra độc lập golden v1: teamhide và full-stack-fastapi-template

Ngày 07/10/2026. Người kiểm: Claude (agent con), chỉ đọc. Không chạy code của repository.

## Kết luận

- Không tìm thấy lỗi loại A, B, C, E.
- 4 điểm loại D (cách hiểu spec), đều đã được gold ghi trong `uncertain` hoặc có lý do rõ.
- Hai repo không có lời gọi `httpx`, `requests`, `aiohttp` nào. Gold ghi 0 lời gọi `http_api`, đúng với source. Phần chấm HTTP của `fr029_golden4.py` không có tín hiệu trên hai repo này.

## Đã đọc

| Nguồn | Phần dùng |
|---|---|
| `.aide/requirements/fr/FR-L3GEN-029.md` | Đầu ra, AC-01 đến AC-05 |
| `slice/tools/fr029_golden4.py` | Cách so route, model, lời gọi HTTP |
| `golden-v1/<repo>/final-rN.json` | `repo`, `commit`, `files_reviewed`, `routes`, `external_calls`, `entry_points`, `uncertain` |
| `golden-v1/<repo>/scope.json` | Danh sách file trong phạm vi và thư mục bị loại (không phải file judge/review) |

Không đọc file judge, check, key, draft nào.

## Bảng phủ

| Repo | Commit | Route gold | Route kiểm khớp source | Route thiếu | Route thừa | Lời gọi HTTP (3 thư viện) gold / source |
|---|---|---|---|---|---|---|
| teamhide | df4e6d4 | 5 | 5/5 | 0 | 0 | 0 / 0 |
| full-stack | cb740b6 | 23 | 23/23 | 0 | 0 | 0 / 0 |

Mỗi route đã kiểm: method, path đầy đủ qua chuỗi `include_router`, handler, request model, response model, dòng bằng chứng.

### Chuỗi prefix đã lần

| Repo | Chuỗi | Bằng chứng |
|---|---|---|
| teamhide | `app.include_router(user_router)` không prefix → `router.include_router(user_v1_router, prefix="/api/v1/user")` → `@user_router.get("")` | `app/server.py:25`, `app/user/adapter/input/api/__init__.py:6`, `app/user/adapter/input/api/v1/user.py:15` |
| teamhide | tương tự với `prefix="/api/v1/auth"` | `app/auth/adapter/input/api/__init__.py:6` |
| full-stack | `app.include_router(api_router, prefix=settings.API_V1_STR)`, `API_V1_STR: str = "/api/v1"` → `api_router.include_router(users.router)` → `APIRouter(prefix="/users")` | `backend/app/main.py:35`, `backend/app/core/config.py:22`, `backend/app/api/main.py:8`, `backend/app/api/routes/users.py:29` |

`.env` gốc không khai `API_V1_STR` (đã grep tên khóa, không in giá trị). Nên `/api/v1` là đúng.

### Đã quét để tìm route hoặc lời gọi bị sót

- Decorator `@<x>.get/post/put/patch/delete/api_route/websocket` trên mọi file `.py` ngoài `tests/`: teamhide 5, full-stack 23. Khớp số route gold.
- `add_api_route`, `add_route`, `add_websocket_route`, `mount(`: không có trong cả hai repo.
- `httpx`, `requests`, `aiohttp`, `urllib`: chỉ thấy trong `pyproject.toml` (khai thư viện) và một chuỗi docstring. Không có lời gọi.
- Ứng dụng `FastAPI(...)`: mỗi repo một cái (`app/server.py:77`, `backend/app/main.py:21`).

## Phát hiện

### Loại D: cách hiểu spec

| # | Đường dẫn gold | Source | Gold ghi | Nhận xét |
|---|---|---|---|---|
| D1 | full-stack `routes[22]` (`POST /api/v1/private/users/`) | `backend/app/api/main.py:13-14` `if settings.FASTAPI_ENV == "development":` / `api_router.include_router(private.router)`; `core/config.py:27` mặc định `None` | Có route, kèm `uncertain[0]` | Mặc định trong code thì route không được gắn. Nhưng `.env` gốc dòng 2 đặt `FASTAPI_ENV` bằng `development` (đã kiểm bằng `grep -q`, không in file), và `compose.override.yml:66` cũng vậy. Ghi route là hợp lý. Spec không nói route gắn có điều kiện thì xử lý thế nào. |
| D2 | full-stack `routes[4].response_model` = `"Any"` | `backend/app/api/routes/login.py:103-105` `response_class=HTMLResponse,` ... `-> Any:` | `"Any"`, kèm `uncertain[2]` | Không có `response_model=`. Kiểu trả về là `Any`, không phải model. FastAPI vẫn lấy `Any` làm response_model nên gold đúng theo luật "kiểu trả về". Nhưng tool ghi `null` hoặc `unknown` cũng có lý. Scorer sẽ chấm sai nếu tool không ghi đúng chữ `Any`. |
| D3 | full-stack `routes[0].request_model` = `null` | `backend/app/api/routes/login.py:25` `form_data: Annotated[OAuth2PasswordRequestForm, Depends()]` | `null` | Body là form, khai qua lớp dependency, không phải model Pydantic. `null` khớp chữ "kiểu Pydantic" của AC-02. Tool ghi `OAuth2PasswordRequestForm` sẽ bị chấm sai dù không vô lý. |
| D4 | full-stack `uncertain[3]` (không thành route) | `backend/app/main.py:36` `app.frontend("/", directory=FRONTEND_DIR)` | Không ghi route | Không có handler trong repo. Không phải `mount`, `add_route`. Bỏ ra khỏi `routes` là hợp lý. Không xác minh được method này của FastAPI làm gì (không có mạng, không chạy code). |

### Loại A, B, C, E

Không có.

- A: 28/28 route đúng method, path, handler, tên model. Các tên `list[GetUserListResponseDTO]`, `UsersPublic`, `ItemsPublic`, `bool` đúng nguyên văn source.
- B: golden v1 không có trường đáp án thay thế. Scorer chỉ đọc `request_model`, `response_model`.
- C: không có route hay lời gọi HTTP trong phạm vi bị sót.
- E: không thấy lỗi định dạng làm scorer chấm sai trên hai repo này. Hai handler cùng tên `create_user` ở full-stack (`users.py`, `private.py`) có chuỗi handler khác nhau nên khóa không trùng.

### Ghi chú phụ (không tính là lỗi)

- teamhide `/docs`, `/redoc` (`app/server.py:81-82`) và full-stack `openapi_url` (`backend/app/main.py:23`): gold không ghi vì không có handler trong repo. Cách xử lý nhất quán giữa hai repo.
- Kiểm thêm `external_calls` không phải HTTP: dòng bằng chứng DB, Redis, Celery (teamhide) và DB, email `utils.py:42-56`, Sentry `main.py:19` (full-stack) khớp source. Các mục này scorer không chấm.

## Giới hạn

- Chưa kiểm: `status_code`, `auth`, `entities`, `data_access`, `events`, `config`, `dependencies`, `entry_points` ngoài phần liên quan route. Scorer không dùng các trường này.
- Không kiểm trường của model (kiểu, bắt buộc). Golden v1 không có.
- Không chạy ứng dụng để lấy `app.routes` thật. Kết quả dựa trên đọc source và grep.
- Không xác minh `app.frontend(...)` ở FastAPI `>=0.141.1` sinh endpoint gì.
- Không kiểm hai repo còn lại (`fastapi_best_architecture`, `igorbenav-FastAPI-boilerplate`).
