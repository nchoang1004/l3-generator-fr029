# teamhide — tài liệu API

Bản sinh tự động từ source, chưa được chủ repository duyệt. File này dành cho người đọc; dữ liệu đầy đủ cho máy nằm ở `result.json` và khối OpenAPI trong các file ở phụ lục.

| Mục | Giá trị |
|---|---|
| Tình trạng | Chưa đủ — còn lỗi sau 1 vòng sửa, xem mục 6 |
| Đọc source | 84/84 file trong phạm vi |
| Endpoint | 4 |
| Model | 7 |
| Gọi HTTP ra ngoài | 0 |

## 1. Danh sách endpoint

| # | Method | Path | Vào | Ra | Status | Auth |
|---|---|---|---|---|---|---|
| 1 | POST | /api/v1/auth/refresh | RefreshTokenRequest | RefreshTokenResponse | 200 | chưa rõ |
| 2 | POST | /api/v1/auth/verify | VerifyTokenRequest | — | 200 | chưa rõ |
| 3 | POST | /api/v1/user | CreateUserRequest | CreateUserResponseDTO | 200 | chưa rõ |
| 4 | POST | /api/v1/user/login | LoginRequest | LoginResponse | 200 | chưa rõ |

## 2. Chi tiết từng endpoint

### 1. POST /api/v1/auth/refresh

- Hàm xử lý: `refresh_token` tại `app/auth/adapter/input/api/v1/auth.py:15`
- Tham số: không có
- Body: RefreshTokenRequest
- Trả về: RefreshTokenResponse
- Status: 200 (Decorator không khai status_code; FastAPI dùng status mặc định 200 của JSONResponse)
- Dependency: Provide[Container.jwt_service], Logging
- Auth: chưa rõ — Không có Security/Depends auth trong mã route; middleware xác thực không phải là Security phụ thuộc của FastAPI
- Mức chắc chắn: suy luận: Decorator không khai status_code; FastAPI dùng status mặc định 200 của JSONResponse; Tham số kiểu Pydantic model không khai Body; FastAPI coi là body
- Còn thiếu: Trường chưa xác định: auth

### 2. POST /api/v1/auth/verify

- Hàm xử lý: `verify_token` tại `app/auth/adapter/input/api/v1/auth.py:30`
- Tham số: không có
- Body: VerifyTokenRequest
- Trả về: —
- Status: 200 (Decorator không khai status_code; FastAPI dùng status mặc định 200 của JSONResponse)
- Dependency: Provide[Container.jwt_service], Logging
- Auth: chưa rõ — Không có Security/Depends auth trong mã route; middleware xác thực không phải là Security phụ thuộc của FastAPI
- Mức chắc chắn: suy luận: Decorator không khai status_code; FastAPI dùng status mặc định 200 của JSONResponse; Tham số kiểu Pydantic model không khai Body; FastAPI coi là body
- Còn thiếu: Trường chưa xác định: auth

### 3. POST /api/v1/user

- Hàm xử lý: `create_user` tại `app/user/adapter/input/api/v1/user.py:29`
- Tham số: không có
- Body: CreateUserRequest
- Trả về: CreateUserResponseDTO
- Status: 200 (Decorator không khai status_code; FastAPI dùng status mặc định 200 của JSONResponse)
- Dependency: Provide[Container.user_service], Logging
- Auth: chưa rõ — Không có Security/Depends auth trong mã route; middleware xác thực không phải là Security phụ thuộc của FastAPI
- Mức chắc chắn: suy luận: Decorator không khai status_code; FastAPI dùng status mặc định 200 của JSONResponse; Tham số kiểu Pydantic model không khai Body; FastAPI coi là body
- Còn thiếu: Trường chưa xác định: auth

### 4. POST /api/v1/user/login

- Hàm xử lý: `login` tại `app/user/adapter/input/api/v1/user.py:43`
- Tham số: không có
- Body: LoginRequest
- Trả về: LoginResponse
- Status: 200 (Decorator không khai status_code; FastAPI dùng status mặc định 200 của JSONResponse)
- Dependency: Provide[Container.user_service], Logging
- Auth: chưa rõ — Không có Security/Depends auth trong mã route; middleware xác thực không phải là Security phụ thuộc của FastAPI
- Mức chắc chắn: suy luận: Decorator không khai status_code; FastAPI dùng status mặc định 200 của JSONResponse; Tham số kiểu Pydantic model không khai Body; FastAPI coi là body
- Còn thiếu: Trường chưa xác định: auth

## 3. Model dữ liệu

### CreateUserRequest

Khai ở `app/user/adapter/input/api/v1/request/__init__.py:9`. Mức chắc chắn: suy luận: Pydantic v2: trường không có default là bắt buộc, kể cả khi kiểu cho phép None.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| email | string | có | không |
| password1 | string | có | không |
| password2 | string | có | không |
| nickname | string | có | không |
| lat | number | có | không |
| lng | number | có | không |

### CreateUserResponseDTO

Khai ở `app/user/application/dto/__init__.py:17`. Mức chắc chắn: suy luận: Pydantic v2: trường không có default là bắt buộc, kể cả khi kiểu cho phép None.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| email | string | có | không |
| nickname | string | có | không |

### LoginRequest

Khai ở `app/user/adapter/input/api/v1/request/__init__.py:4`. Mức chắc chắn: suy luận: Pydantic v2: trường không có default là bắt buộc, kể cả khi kiểu cho phép None.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| email | string | có | không |
| password | string | có | không |

### LoginResponse

Khai ở `app/user/adapter/input/api/v1/response/__init__.py:4`. Mức chắc chắn: suy luận: Pydantic v2: trường không có default là bắt buộc, kể cả khi kiểu cho phép None.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| token | string | có | không |
| refresh_token | string | có | không |

### RefreshTokenRequest

Khai ở `app/auth/adapter/input/api/v1/request/__init__.py:4`. Mức chắc chắn: suy luận: Pydantic v2: trường không có default là bắt buộc, kể cả khi kiểu cho phép None.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| token | string | có | không |
| refresh_token | string | có | không |

### RefreshTokenResponse

Khai ở `app/auth/adapter/input/api/v1/response/__init__.py:4`. Mức chắc chắn: suy luận: Pydantic v2: trường không có default là bắt buộc, kể cả khi kiểu cho phép None.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| token | string | có | không |
| refresh_token | string | có | không |

### VerifyTokenRequest

Khai ở `app/auth/adapter/input/api/v1/request/__init__.py:9`. Mức chắc chắn: suy luận: Pydantic v2: trường không có default là bắt buộc, kể cả khi kiểu cho phép None.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| token | string | có | không |

## 4. Cấu trúc code

Vai trò của từng file theo dấu hiệu trong code (FR-029). Chỉ liệt kê component thường.

### (root)

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `main.py` | Điểm vào | `main.py:9` |

### app

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `app/auth/adapter/input/api/__init__.py` | Khác | `app/auth/adapter/input/api/__init__.py:5` |
| `app/auth/adapter/input/api/v1/auth.py` | Route | `app/auth/adapter/input/api/v1/auth.py:15` |
| `app/auth/adapter/input/api/v1/request/__init__.py` | Schema API | `app/auth/adapter/input/api/v1/request/__init__.py:4` |
| `app/auth/adapter/input/api/v1/response/__init__.py` | Schema API | `app/auth/adapter/input/api/v1/response/__init__.py:4` |
| `app/auth/application/dto/__init__.py` | Schema API | `app/auth/application/dto/__init__.py:4` |
| `app/auth/application/exception/__init__.py` | Khác | `app/auth/application/exception/__init__.py:4` |
| `app/auth/application/service/jwt.py` | Khác | `app/auth/application/service/jwt.py:11` |
| `app/auth/domain/usecase/jwt.py` | Khác | `app/auth/domain/usecase/jwt.py:6` |
| `app/container.py` | Khác | `app/container.py:10` |
| `app/server.py` | Điểm vào | `app/server.py:77` |
| `app/user/adapter/input/api/__init__.py` | Khác | `app/user/adapter/input/api/__init__.py:5` |
| `app/user/adapter/input/api/v1/request/__init__.py` | Schema API | `app/user/adapter/input/api/v1/request/__init__.py:4` |
| `app/user/adapter/input/api/v1/response/__init__.py` | Schema API | `app/user/adapter/input/api/v1/response/__init__.py:4` |
| `app/user/adapter/input/api/v1/user.py` | Route | `app/user/adapter/input/api/v1/user.py:15` |
| `app/user/adapter/output/persistence/repository_adapter.py` | Service | đường gọi `app/user/adapter/input/api/v1/user.py:26` → `app/user/application/service/user.py:26` → `app/user/adapter/output/persistence/repository_adapter.py:15` → `app/user/adapter/output/persistence/sqlalchemy/user.py:25` |
| `app/user/adapter/output/persistence/sqlalchemy/user.py` | Truy cập dữ liệu | `app/user/adapter/output/persistence/sqlalchemy/user.py:15` |
| `app/user/application/dto/__init__.py` | Schema API | `app/user/application/dto/__init__.py:4` |
| `app/user/application/exception/__init__.py` | Khác | `app/user/application/exception/__init__.py:4` |
| `app/user/application/service/user.py` | Service | đường gọi `app/user/adapter/input/api/v1/user.py:26` → `app/user/application/service/user.py:26` → `app/user/adapter/output/persistence/repository_adapter.py:15` → `app/user/adapter/output/persistence/sqlalchemy/user.py:25` |
| `app/user/container.py` | Khác | `app/user/container.py:9` |
| `app/user/domain/command/__init__.py` | Khác | `app/user/domain/command/__init__.py:4` |
| `app/user/domain/entity/user.py` | Model bảng | `app/user/domain/entity/user.py:11` |
| `app/user/domain/repository/user.py` | Khác | `app/user/domain/repository/user.py:5` |
| `app/user/domain/usecase/user.py` | Khác | `app/user/domain/usecase/user.py:7` |
| `app/user/domain/vo/location.py` | Khác | `app/user/domain/vo/location.py:4` |

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
| `core/db/transactional.py` | Khác | `core/db/transactional.py:6` |
| `core/exceptions/__init__.py` | Khác | `core/exceptions/__init__.py:1` |
| `core/exceptions/base.py` | Khác | `core/exceptions/base.py:1` |
| `core/fastapi/dependencies/__init__.py` | Khác | `core/fastapi/dependencies/__init__.py:1` |
| `core/fastapi/dependencies/logging.py` | Khác | `core/fastapi/dependencies/logging.py:4` |
| `core/fastapi/dependencies/permission.py` | Khác | `core/fastapi/dependencies/permission.py:57` |
| `core/fastapi/middlewares/__init__.py` | Khác | `core/fastapi/middlewares/__init__.py:1` |
| `core/fastapi/middlewares/authentication.py` | Khác | `core/fastapi/middlewares/authentication.py:16` |
| `core/fastapi/middlewares/response_log.py` | Khác | `core/fastapi/middlewares/response_log.py:14` |
| `core/fastapi/middlewares/sqlalchemy.py` | Khác | `core/fastapi/middlewares/sqlalchemy.py:8` |
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
| `core/repository/base.py` | Truy cập dữ liệu | `core/repository/base.py:16` |
| `core/repository/enum.py` | Khác | `core/repository/enum.py:4` |

Không có vai trò: 4 file rỗng.

## 5. Gọi HTTP ra ngoài

Không có lời gọi nào qua httpx, requests, aiohttp.

## 6. Chưa biết và giới hạn

- **Loại component được suy từ phạm vi đọc.** Membership không ghi loại component; xếp theo phạm vi đọc (FR-028): tests → test, migrations → migration
- **Chưa có sơ đồ component.** Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- **Chưa đối chiếu với dữ liệu kiến trúc.** Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- **Phân tích chưa xong.** còn lỗi sau 1 vòng sửa
- **File ngoài phạm vi đọc.** migration: 2 file, test: 39 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- **Có đề xuất của model bị bộ kiểm từ chối.** 8 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
- **Dòng trông giống route hoặc lời gọi HTTP nhưng chưa được xác nhận, nên không có trong tài liệu.** `app/user/adapter/input/api/v1/user.py:15`

## Phụ lục: OpenAPI cho máy

- [tech-specs/APP/api/API-TEAMHIDE-APP-v1.md](tech-specs/APP/api/API-TEAMHIDE-APP-v1.md) — component app
