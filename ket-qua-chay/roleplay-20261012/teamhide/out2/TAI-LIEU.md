# teamhide — tài liệu API

Bản sinh tự động từ source, chưa được chủ repository duyệt. File này dành cho người đọc; dữ liệu đầy đủ cho máy nằm ở `result.json` và các file ở phụ lục.

| Mục | Giá trị |
|---|---|
| Tình trạng | Đủ |
| Đọc source | 84/84 file trong phạm vi |
| Endpoint | 5 |
| Model | 8 |
| Bảng CSDL | 1 |
| Sự kiện, tác vụ nền | 2 điểm gửi/nhận |
| Gọi HTTP ra ngoài | 0 |
| Sinh bởi | model scripted, prompt fr029-oneshot-prompt-v6; bảng, sự kiện, thư viện, cấu hình, middleware đọc tĩnh từ code |

Cách đọc nhãn: **chắc chắn** — đọc thẳng từ một dòng code; **suy luận** — theo quy tắc mặc định của framework, lý do ở chú thích [n]; **chưa rõ** — source không đủ để kết luận; **AI viết** — câu chữ do model viết, chỉ để đọc nhanh, không phải dữ kiện đã kiểm.

## 1. Danh sách endpoint

| # | Method | Path | Vào | Ra | Status | Auth |
|---|---|---|---|---|---|---|
| 1 | POST | /api/v1/auth/refresh | RefreshTokenRequest | RefreshTokenResponse | 200, 400* | chưa rõ |
| 2 | POST | /api/v1/auth/verify | VerifyTokenRequest | — | 200, 400* | chưa rõ |
| 3 | GET | /api/v1/user | — | list[GetUserListResponseDTO] | 200 | PermissionDependency([IsAdmin]): chỉ người dùng admin; người dùng lấy từ JWT Bearer trong header Authorization (AuthenticationMiddleware) |
| 4 | POST | /api/v1/user | CreateUserRequest | CreateUserResponseDTO | 200, 400*, 401* | chưa rõ |
| 5 | POST | /api/v1/user/login | LoginRequest | LoginResponse | 200, 404* | chưa rõ |

\* mã lỗi suy từ chỗ ném lỗi trong code, xem mục 2.

## 2. Chi tiết từng endpoint

### 1. POST /api/v1/auth/refresh

- Mô tả (AI viết): Cấp token mới và refresh token mới từ cặp token hiện có.
- Hàm xử lý: `refresh_token` tại `app/auth/adapter/input/api/v1/auth.py:15`
- Tham số: không có
- Body: RefreshTokenRequest
- Trả về: RefreshTokenResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Lỗi có thể trả về: 400 — DecodeTokenException, ném ở `app/auth/application/service/jwt.py:26`, mã khai ở `app/auth/application/exception/__init__.py:5`
- Lỗi có thể trả về: 400 — DecodeTokenException, ném ở `core/helpers/token.py:43`, mã khai ở `core/helpers/token.py:10`
- Lỗi có thể trả về: 400 — ExpiredTokenException, ném ở `core/helpers/token.py:45`, mã khai ở `core/helpers/token.py:16`
- Dependency: Logging, Provide[Container.jwt_service]
- Auth: chưa rõ — Không có Depends/Security kiểm tra quyền; token được gửi trong body và kiểm tra trong service
- Nhóm (tags): Auth
- Mức chắc chắn: suy luận [1][2]
- Còn thiếu: Trường chưa xác định: auth

### 2. POST /api/v1/auth/verify

- Mô tả (AI viết): Kiểm tra token có giải mã được và còn hạn hay không.
- Hàm xử lý: `verify_token` tại `app/auth/adapter/input/api/v1/auth.py:30`
- Tham số: không có
- Body: VerifyTokenRequest
- Trả về: —
- Status: 200 (mặc định của framework, xem chú thích)
- Lỗi có thể trả về: 400 — DecodeTokenException, ném ở `app/auth/application/service/jwt.py:16`, mã khai ở `app/auth/application/exception/__init__.py:5`
- Dependency: Logging, Provide[Container.jwt_service]
- Auth: chưa rõ — Không có Depends/Security kiểm tra quyền; token được gửi trong body và kiểm tra trong service
- Nhóm (tags): Auth
- Mức chắc chắn: suy luận [1][2]
- Còn thiếu: Trường chưa xác định: auth

### 3. GET /api/v1/user

- Mô tả (AI viết): Lấy danh sách người dùng có phân trang, chỉ dành cho admin.
- Hàm xử lý: `get_user_list` tại `app/user/adapter/input/api/v1/user.py:15`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | limit | query | integer | không |
  | prev | query | integer | không |

- Trả về: list[GetUserListResponseDTO]
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: Logging, PermissionDependency, Provide[Container.user_service]
- Auth: PermissionDependency([IsAdmin]): chỉ người dùng admin; người dùng lấy từ JWT Bearer trong header Authorization (AuthenticationMiddleware)
- Nhóm (tags): User
- Đường gọi tới dữ liệu (suy luận từ vai trò Service): `app/user/adapter/input/api/v1/user.py:26` → `app/user/application/service/user.py:26` → `app/user/adapter/output/persistence/repository_adapter.py:15` → `app/user/adapter/output/persistence/sqlalchemy/user.py:25`; bảng nhắc tới: `user`
- Đường gọi tới dữ liệu (suy luận từ vai trò Service): `app/user/adapter/input/api/v1/user.py:18` → `core/fastapi/dependencies/permission.py:66` → `core/fastapi/dependencies/permission.py:49` → `app/user/application/service/user.py:49` → `app/user/adapter/output/persistence/repository_adapter.py:30` → `app/user/adapter/output/persistence/sqlalchemy/user.py:43`; bảng nhắc tới: `user`
- Mức chắc chắn: suy luận [1]

### 4. POST /api/v1/user

- Mô tả (AI viết): Tạo người dùng mới từ email, mật khẩu, biệt danh và vị trí.
- Hàm xử lý: `create_user` tại `app/user/adapter/input/api/v1/user.py:29`
- Tham số: không có
- Body: CreateUserRequest
- Trả về: CreateUserResponseDTO
- Status: 200 (mặc định của framework, xem chú thích)
- Lỗi có thể trả về: 400 — DuplicateEmailOrNicknameException, ném ở `app/user/application/service/user.py:38`, mã khai ở `app/user/application/exception/__init__.py:11`
- Lỗi có thể trả về: 401 — PasswordDoesNotMatchException, ném ở `app/user/application/service/user.py:31`, mã khai ở `app/user/application/exception/__init__.py:5`
- Dependency: Logging, Provide[Container.user_service]
- Auth: chưa rõ — Không có Depends/Security kiểm tra quyền; AuthenticationMiddleware chỉ gắn request.user, không chặn yêu cầu
- Nhóm (tags): User
- Mức chắc chắn: suy luận [1][2]
- Còn thiếu: Trường chưa xác định: auth

### 5. POST /api/v1/user/login

- Mô tả (AI viết): Đăng nhập bằng email và mật khẩu, trả về token và refresh token.
- Hàm xử lý: `login` tại `app/user/adapter/input/api/v1/user.py:43`
- Tham số: không có
- Body: LoginRequest
- Trả về: LoginResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Lỗi có thể trả về: 404 — UserNotFoundException, ném ở `app/user/application/service/user.py:61`, mã khai ở `app/user/application/exception/__init__.py:17`
- Dependency: Logging, Provide[Container.user_service]
- Auth: chưa rõ — Không có Depends/Security kiểm tra quyền; endpoint đăng nhập nhận email và mật khẩu trong body
- Nhóm (tags): User
- Mức chắc chắn: suy luận [1][2]
- Còn thiếu: Trường chưa xác định: auth

Chú thích:

[1] Decorator không khai status_code; FastAPI dùng status mặc định 200 của JSONResponse  
[2] Tham số kiểu Pydantic model không khai Body; FastAPI coi là body  

## 3. Model dữ liệu

### CreateUserRequest

Khai ở `app/user/adapter/input/api/v1/request/__init__.py:9`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| email | string | có | không |
| password1 | string | có | không |
| password2 | string | có | không |
| nickname | string | có | không |
| lat | number | có | không |
| lng | number | có | không |

### CreateUserResponseDTO

Khai ở `app/user/application/dto/__init__.py:17`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| email | string | có | không |
| nickname | string | có | không |

### GetUserListResponseDTO

Khai ở `app/user/application/dto/__init__.py:4`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| id | integer | có | không |
| email | string | có | không |
| nickname | string | có | không |

### LoginRequest

Khai ở `app/user/adapter/input/api/v1/request/__init__.py:4`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| email | string | có | không |
| password | string | có | không |

### LoginResponse

Khai ở `app/user/adapter/input/api/v1/response/__init__.py:4`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| token | string | có | không |
| refresh_token | string | có | không |

### RefreshTokenRequest

Khai ở `app/auth/adapter/input/api/v1/request/__init__.py:4`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| token | string | có | không |
| refresh_token | string | có | không |

### RefreshTokenResponse

Khai ở `app/auth/adapter/input/api/v1/response/__init__.py:4`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| token | string | có | không |
| refresh_token | string | có | không |

### VerifyTokenRequest

Khai ở `app/auth/adapter/input/api/v1/request/__init__.py:9`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| token | string | có | không |

## 4. Bảng CSDL

### user

Khai ở `app/user/domain/entity/user.py:10`, component app. SQL dialect: chưa rõ (Không có Base.metadata.create_all(engine) nối base này với một engine có URL literal). Mức chắc chắn: suy luận [1][2][3].

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null |
|---|---|---|---|---|
| created_at | DateTime (chưa quy ra kiểu SQL) | không | — | không |
| updated_at | DateTime (chưa quy ra kiểu SQL) | không | — | không |
| id | int (chưa quy ra kiểu SQL) | có | — | không |
| password | String(255) (chưa quy ra kiểu SQL) | không | — | không |
| email | String(255) (chưa quy ra kiểu SQL) | không | — | không |
| nickname | String(255) (chưa quy ra kiểu SQL) | không | — | không |
| is_admin | bool (chưa quy ra kiểu SQL) | không | — | không |
| lat | chưa rõ (Chưa xác định SQL dialect từ source) | không | — | có |
| lng | chưa rõ (Chưa xác định SQL dialect từ source) | không | — | có |

Chú thích:

[1] không khai primary_key thì là False  
[2] nullable mặc định là not primary_key  
[3] với Mapped/SQLModel theo Optional  

## 5. Sự kiện và tác vụ nền

| Vai trò | Tác vụ hoặc topic | Thư viện / broker | Component | Ở đâu |
|---|---|---|---|---|
| gửi | core.fastapi.dependencies.logging.Logging._send_log | fastapi.BackgroundTasks | core | `core/fastapi/dependencies/logging.py:6` |
| nhận | core.fastapi.dependencies.logging.Logging._send_log | fastapi.BackgroundTasks | core | `core/fastapi/dependencies/logging.py:8` |

Bên gửi và bên nhận chỉ được nối khi cùng broker và cùng tác vụ (FR-031); file EVT của từng component ghi bên liên quan.

## 6. Cấu trúc code

Vai trò của từng file theo dấu hiệu trong code (FR-029). Chỉ liệt kê component thường.

### (root)

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `main.py` | Điểm vào | `main.py:24` |

### app

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `app/auth/adapter/input/api/__init__.py` | Khác | `app/auth/adapter/input/api/__init__.py:6` |
| `app/auth/adapter/input/api/v1/auth.py` | Route | `app/auth/adapter/input/api/v1/auth.py:15` |
| `app/auth/adapter/input/api/v1/request/__init__.py` | Schema API | `app/auth/adapter/input/api/v1/request/__init__.py:4` |
| `app/auth/adapter/input/api/v1/response/__init__.py` | Schema API | `app/auth/adapter/input/api/v1/response/__init__.py:4` |
| `app/auth/application/dto/__init__.py` | Khác | `app/auth/application/dto/__init__.py:4` |
| `app/auth/application/exception/__init__.py` | Khác | `app/auth/application/exception/__init__.py:4` |
| `app/auth/application/service/jwt.py` | Khác | `app/auth/application/service/jwt.py:11` |
| `app/auth/domain/usecase/jwt.py` | Khác | `app/auth/domain/usecase/jwt.py:6` |
| `app/container.py` | Khác | `app/container.py:10` |
| `app/server.py` | Điểm vào | `app/server.py:77` |
| `app/user/adapter/input/api/__init__.py` | Khác | `app/user/adapter/input/api/__init__.py:6` |
| `app/user/adapter/input/api/v1/request/__init__.py` | Schema API | `app/user/adapter/input/api/v1/request/__init__.py:4` |
| `app/user/adapter/input/api/v1/response/__init__.py` | Schema API | `app/user/adapter/input/api/v1/response/__init__.py:4` |
| `app/user/adapter/input/api/v1/user.py` | Route | `app/user/adapter/input/api/v1/user.py:15` |
| `app/user/adapter/output/persistence/repository_adapter.py` | Service | đường gọi `app/user/adapter/input/api/v1/user.py:26` → `app/user/application/service/user.py:26` → `app/user/adapter/output/persistence/repository_adapter.py:15` → `app/user/adapter/output/persistence/sqlalchemy/user.py:25` |
| `app/user/adapter/output/persistence/sqlalchemy/user.py` | Truy cập dữ liệu | `app/user/adapter/output/persistence/sqlalchemy/user.py:25` |
| `app/user/application/dto/__init__.py` | Schema API | `app/user/application/dto/__init__.py:4` |
| `app/user/application/exception/__init__.py` | Khác | `app/user/application/exception/__init__.py:4` |
| `app/user/application/service/user.py` | Service | đường gọi `app/user/adapter/input/api/v1/user.py:26` → `app/user/application/service/user.py:26` → `app/user/adapter/output/persistence/repository_adapter.py:15` → `app/user/adapter/output/persistence/sqlalchemy/user.py:25` |
| `app/user/container.py` | Khác | `app/user/container.py:9` |
| `app/user/domain/command/__init__.py` | Khác | `app/user/domain/command/__init__.py:4` |
| `app/user/domain/entity/user.py` | Model bảng | `app/user/domain/entity/user.py:11` |
| `app/user/domain/repository/user.py` | Khác | `app/user/domain/repository/user.py:5` |
| `app/user/domain/usecase/user.py` | Khác | `app/user/domain/usecase/user.py:7` |
| `app/user/domain/vo/location.py` | Khác | `app/user/domain/vo/location.py:5` |

Không có vai trò: 24 file rỗng.

### celery_task

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `celery_task/__init__.py` | Hạ tầng | `celery_task/__init__.py:5` |

Không có vai trò: 1 file rỗng.

### core

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `core/config.py` | Cấu hình | `core/config.py:6` |
| `core/db/__init__.py` | Khác | `core/db/__init__.py:1` |
| `core/db/mixins/__init__.py` | Khác | `core/db/mixins/__init__.py:1` |
| `core/db/mixins/timestamp_mixin.py` | Khác | `core/db/mixins/timestamp_mixin.py:7` |
| `core/db/session.py` | Hạ tầng | `core/db/session.py:38` |
| `core/db/transactional.py` | Truy cập dữ liệu | `core/db/transactional.py:12` |
| `core/exceptions/__init__.py` | Khác | `core/exceptions/__init__.py:1` |
| `core/exceptions/base.py` | Khác | `core/exceptions/base.py:1` |
| `core/fastapi/dependencies/__init__.py` | Khác | `core/fastapi/dependencies/__init__.py:1` |
| `core/fastapi/dependencies/logging.py` | Khác | `core/fastapi/dependencies/logging.py:4` |
| `core/fastapi/dependencies/permission.py` | Service | đường gọi `app/user/adapter/input/api/v1/user.py:18` → `core/fastapi/dependencies/permission.py:66` → `core/fastapi/dependencies/permission.py:49` → `app/user/application/service/user.py:49` → `app/user/adapter/output/persistence/repository_adapter.py:30` → `app/user/adapter/output/persistence/sqlalchemy/user.py:43` |
| `core/fastapi/middlewares/__init__.py` | Khác | `core/fastapi/middlewares/__init__.py:1` |
| `core/fastapi/middlewares/authentication.py` | Khác | `core/fastapi/middlewares/authentication.py:16` |
| `core/fastapi/middlewares/response_log.py` | Khác | `core/fastapi/middlewares/response_log.py:14` |
| `core/fastapi/middlewares/sqlalchemy.py` | Truy cập dữ liệu | `core/fastapi/middlewares/sqlalchemy.py:21` |
| `core/helpers/cache/__init__.py` | Khác | `core/helpers/cache/__init__.py:1` |
| `core/helpers/cache/base/__init__.py` | Khác | `core/helpers/cache/base/__init__.py:1` |
| `core/helpers/cache/base/backend.py` | Khác | `core/helpers/cache/base/backend.py:5` |
| `core/helpers/cache/base/key_maker.py` | Khác | `core/helpers/cache/base/key_maker.py:5` |
| `core/helpers/cache/cache_manager.py` | Khác | `core/helpers/cache/cache_manager.py:7` |
| `core/helpers/cache/cache_tag.py` | Khác | `core/helpers/cache/cache_tag.py:4` |
| `core/helpers/cache/custom_key_maker.py` | Khác | `core/helpers/cache/custom_key_maker.py:7` |
| `core/helpers/cache/redis_backend.py` | Khác | `core/helpers/cache/redis_backend.py:10` |
| `core/helpers/redis.py` | Hạ tầng | `core/helpers/redis.py:5` |
| `core/helpers/token.py` | Khác | `core/helpers/token.py:21` |
| `core/repository/base.py` | Truy cập dữ liệu | `core/repository/base.py:17` |
| `core/repository/enum.py` | Khác | `core/repository/enum.py:4` |

Không có vai trò: 4 file rỗng.

### Quan hệ giữa component

Đọc tĩnh từ lời gọi, Depends và chỗ dùng bảng đã nối được tới nơi định nghĩa.

| Từ | Tới | Cách dùng | Số chỗ | Ví dụ |
|---|---|---|---|---|
| app | core | gọi hàm | 12 | `app/user/adapter/input/api/v1/user.py:18` |
| core | app | gọi hàm | 1 | `core/fastapi/dependencies/permission.py:49` |

## 7. Gọi HTTP ra ngoài

Không có lời gọi nào qua httpx, requests, aiohttp.

## 8. Thư viện

| Thư viện | Phiên bản | Có import trong code | Khai ở |
|---|---|---|---|
| aiomysql | ^0.2.0 | chưa thấy import | `pyproject.toml:17` |
| alembic | ^1.13.1 | chưa thấy import | `pyproject.toml:9` |
| celery | ^5.3.6 | có | `pyproject.toml:12` |
| click | ^8.1.7 | có | `pyproject.toml:18` |
| coverage | ^7.4.0 | chưa thấy import | `pyproject.toml:24` |
| cryptography | ^41.0.7 | chưa thấy import | `pyproject.toml:23` |
| dependency-injector | ^4.41.0 | có | `pyproject.toml:27` |
| fastapi | ^0.109.1 | có | `pyproject.toml:2` |
| fastapi-event | ^0.1.3 | có | `pyproject.toml:14` |
| gunicorn | ^23.0.0 | chưa thấy import | `pyproject.toml:13` |
| httpx | ^0.26.0 | chưa thấy import | `pyproject.toml:28` |
| pydantic-settings | ^2.1.0 | có | `pyproject.toml:20` |
| pyjwt | ^2.8.0 | có | `pyproject.toml:21` |
| pymysql | ^1.1.0 | chưa thấy import | `pyproject.toml:26` |
| pytest-asyncio | ^0.23.3 | chưa thấy import | `pyproject.toml:22` |
| pythondi | ^1.2.4 | chưa thấy import | `pyproject.toml:15` |
| redis | ^5.0.1 | có | `pyproject.toml:19` |
| sqlalchemy | — | có | `pyproject.toml:25` |
| ujson | ^5.9.0 | có | `pyproject.toml:16` |
| uvicorn | ^0.25.0 | có | `pyproject.toml:10` |

"Chưa thấy import": tên gói khác tên import, hoặc gói chỉ dùng gián tiếp (driver, plugin, công cụ).

## 9. Cấu hình

| Khóa | Nguồn | Giá trị mặc định | Khai ở |
|---|---|---|---|
| APP_HOST | lớp Settings | 0.0.0.0 | `core/config.py:9` |
| APP_PORT | lớp Settings | 8000 | `core/config.py:10` |
| CELERY_BACKEND_URL | lớp Settings | đã che (dấu hiệu bí mật) | `core/config.py:17` |
| CELERY_BROKER_URL | lớp Settings | đã che (dấu hiệu bí mật) | `core/config.py:16` |
| DEBUG | lớp Settings | True | `core/config.py:8` |
| DEBUG | lớp Settings | False | `core/config.py:32` |
| DEBUG | biến môi trường | chưa rõ (Giá trị đọc lúc chạy) | `main.py:23` |
| ENV | lớp Settings | development | `core/config.py:7` |
| ENV | biến môi trường | chưa rõ (Giá trị đọc lúc chạy) | `core/config.py:36`, `main.py:22` |
| JWT_ALGORITHM | lớp Settings | HS256 | `core/config.py:14` |
| JWT_SECRET_KEY | lớp Settings | đã che (dấu hiệu bí mật) | `core/config.py:13` |
| READER_DB_URL | lớp Settings | đã che (dấu hiệu bí mật) | `core/config.py:12`, `core/config.py:24` |
| REDIS_HOST | lớp Settings | localhost | `core/config.py:18` |
| REDIS_PORT | lớp Settings | 6379 | `core/config.py:19` |
| SENTRY_SDN | lớp Settings | — | `core/config.py:15` |
| WRITER_DB_URL | lớp Settings | đã che (dấu hiệu bí mật) | `core/config.py:11`, `core/config.py:23` |

## 10. Middleware và xử lý lỗi toàn cục

| Loại | Tên | Ở đâu |
|---|---|---|
| xử lý lỗi | `CustomException` | `app/server.py:31` |
| middleware | `CORSMiddleware` | `app/server.py:54` |
| middleware | `AuthenticationMiddleware` | `app/server.py:61` |
| middleware | `SQLAlchemyMiddleware` | `app/server.py:66` |
| middleware | `ResponseLogMiddleware` | `app/server.py:67` |

Middleware áp dụng cho mọi request của app. Middleware xác thực chỉ cho biết app đọc thông tin đăng nhập; route có bắt buộc đăng nhập hay không vẫn xem ở cột Auth.

## 11. Chưa biết và giới hạn

- **Loại component được suy từ phạm vi đọc.** Membership không ghi loại component; xếp theo phạm vi đọc (FR-028): tests → test, migrations → migration
- **Giá trị có dấu hiệu bí mật đã được che.** Giá trị có dấu hiệu credential đã được che trước khi lưu
- **Chưa có sơ đồ component.** Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- **Chưa đối chiếu với dữ liệu kiến trúc.** Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- **File ngoài phạm vi đọc.** migration: 2 file, test: 39 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- **Có đề xuất của model bị bộ kiểm từ chối.** 2 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json

## Phụ lục: file cho máy

- API (OpenAPI): [tech-specs/APP/api/API-TEAMHIDE-APP-v1.md](tech-specs/APP/api/API-TEAMHIDE-APP-v1.md) — component app
- TBL (DDL): [tech-specs/APP/schema/TBL-TEAMHIDE-APP.md](tech-specs/APP/schema/TBL-TEAMHIDE-APP.md) — component app
- EVT: [tech-specs/CORE/events/EVT-TEAMHIDE-CORE-CORE-FASTAPI-DEPENDENCIES-LOGGING-LOGGING-SEND-LOG.md](tech-specs/CORE/events/EVT-TEAMHIDE-CORE-CORE-FASTAPI-DEPENDENCIES-LOGGING-LOGGING-SEND-LOG.md) — component core
