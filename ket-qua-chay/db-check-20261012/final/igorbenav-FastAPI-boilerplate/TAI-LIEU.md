# igorbenav-FastAPI-boilerplate — tài liệu API

Bản sinh tự động từ source, chưa được chủ repository duyệt. File này dành cho người đọc; dữ liệu đầy đủ cho máy nằm ở `result.json` và các file ở phụ lục.

| Mục | Giá trị |
|---|---|
| Tình trạng | Chưa đủ — model không gọi công cụ, xem mục 11 |
| Đọc source | 7/112 file trong phạm vi |
| Endpoint | 0 |
| Model | 0 |
| Bảng CSDL | 6 |
| Sự kiện, tác vụ nền | 0 điểm gửi/nhận; có kênh chưa đọc được, xem mục 11 |
| Gọi HTTP ra ngoài | 0 |
| Sinh bởi | model scripted, prompt fr029-agent-prompt-v17; bảng, sự kiện, thư viện, cấu hình, middleware đọc tĩnh từ code |

Cách đọc nhãn: **chắc chắn** — đọc thẳng từ một dòng code; **suy luận** — theo quy tắc mặc định của framework, lý do ở chú thích [n]; **chưa rõ** — source không đủ để kết luận; **AI viết** — câu chữ do model viết, chỉ để đọc nhanh, không phải dữ kiện đã kiểm.

## 1. Danh sách endpoint

Không có endpoint nào được xác nhận.

## 2. Chi tiết từng endpoint

## 3. Model dữ liệu

Không có model nào.

## 4. Bảng CSDL

SQL dialect: chưa rõ (Không có Base.metadata.create_all(engine) nối base này với một engine có URL literal). Kiểu cột ghi như khai trong code, chưa quy ra kiểu SQL.

Mọi bảng thuộc component backend.

Dấu \* sau một giá trị: code không khai, giá trị lấy theo mặc định có tài liệu của ORM.

| Bảng | Lớp model | Số cột | Khóa ngoại tới |
|---|---|---|---|
| api_keys | APIKey | 14 | user |
| key_permissions | KeyPermission | 8 | api_keys |
| key_usage | KeyUsage | 15 | api_keys, user |
| rate_limits | RateLimit | 10 | tiers |
| tiers | Tier | 7 | — |
| user | User | 18 | tiers |

### api_keys

Lớp `APIKey`, khai ở `backend/src/modules/api_keys/models.py:19`.

Ràng buộc bảng: index(user_id, is_active) idx_api_keys_user_active; index(key_prefix) idx_api_keys_prefix; index(expires_at) idx_api_keys_expires_at.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_at | DateTime(timezone=True) | không\* | — | không | — |
| updated_at | DateTime(timezone=True) | không\* | — | có | — |
| id | Integer | có | — | không\* | — |
| user_id | Integer | không\* | user.id | không\* | index |
| name | String(100) | không\* | — | không\* | — |
| key_hash | String(255) | không\* | — | không\* | unique, index |
| key_prefix | String(20) | không\* | — | không\* | — |
| permissions | JSON | không\* | — | không\* | — |
| usage_limits | JSON | không\* | — | không\* | — |
| last_used_at | DateTime(timezone=True) | không\* | — | có\* | — |
| last_used_ip | String(45) | không\* | — | có\* | — |
| is_active | Boolean | không\* | — | không\* | — |
| expires_at | DateTime(timezone=True) | không\* | — | có\* | — |
| key_metadata | JSON | không\* | — | có\* | — |

### key_permissions

Lớp `KeyPermission`, khai ở `backend/src/modules/api_keys/models.py:71`.

Ràng buộc bảng: unique index(api_key_id, resource, action) idx_key_permissions_key_resource; index(resource, action) idx_key_permissions_resource_action.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_at | DateTime(timezone=True) | không\* | — | không | — |
| updated_at | DateTime(timezone=True) | không\* | — | có | — |
| id | Integer | có | — | không\* | — |
| api_key_id | Integer | không\* | api_keys.id | không\* | index, xóa theo: CASCADE |
| resource | KeyPermissionResource | không\* | — | không\* | index |
| action | KeyPermissionAction | không\* | — | không\* | index |
| conditions | JSON | không\* | — | có\* | — |
| is_allowed | Boolean | không\* | — | không\* | — |

### key_usage

Lớp `KeyUsage`, khai ở `backend/src/modules/api_keys/models.py:44`.

Ràng buộc bảng: index(api_key_id, created_at) idx_key_usage_key_created; index(user_id, created_at) idx_key_usage_user_created; index(endpoint) idx_key_usage_endpoint; index(status_code) idx_key_usage_status.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_at | DateTime(timezone=True) | không\* | — | không | — |
| updated_at | DateTime(timezone=True) | không\* | — | có | — |
| id | Integer | có | — | không\* | — |
| api_key_id | Integer | không\* | api_keys.id | không\* | index, xóa theo: CASCADE |
| user_id | Integer | không\* | user.id | không\* | index |
| endpoint | String(255) | không\* | — | không\* | — |
| method | String(10) | không\* | — | không\* | — |
| status_code | Integer | không\* | — | không\* | — |
| tokens_used | Integer | không\* | — | có\* | — |
| cost_microcents | BigInteger | không\* | — | có\* | — |
| response_time_ms | Integer | không\* | — | có\* | — |
| ip_address | String(45) | không\* | — | có\* | — |
| user_agent | Text | không\* | — | có\* | — |
| error_message | Text | không\* | — | có\* | — |
| usage_metadata | JSON | không\* | — | có\* | — |

### rate_limits

Lớp `RateLimit`, khai ở `backend/src/modules/rate_limit/models.py:8`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_at | DateTime(timezone=True) | không\* | — | không | — |
| updated_at | DateTime(timezone=True) | không\* | — | có | — |
| deleted_at | TIMESTAMP(timezone=True) | không\* | — | có | — |
| is_deleted | bool | không\* | — | không\* | — |
| id | int | có | — | không | — |
| tier_id | int | không\* | tiers.id | không\* | index |
| name | String | không\* | — | không | unique |
| path | String | không\* | — | không | — |
| limit | Integer | không\* | — | không | — |
| period | Integer | không\* | — | không | — |

### tiers

Lớp `Tier`, khai ở `backend/src/modules/tier/models.py:13`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_at | DateTime(timezone=True) | không\* | — | không | — |
| updated_at | DateTime(timezone=True) | không\* | — | có | — |
| deleted_at | TIMESTAMP(timezone=True) | không\* | — | có | — |
| is_deleted | bool | không\* | — | không\* | — |
| id | int | có | — | không | — |
| name | String | không\* | — | không | unique |
| description | Text | không\* | — | có\* | — |

### user

Lớp `User`, khai ở `backend/src/modules/user/models.py:15`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_at | DateTime(timezone=True) | không\* | — | không | — |
| updated_at | DateTime(timezone=True) | không\* | — | có | — |
| deleted_at | TIMESTAMP(timezone=True) | không\* | — | có | — |
| is_deleted | bool | không\* | — | không\* | — |
| id | int | có | — | không | — |
| name | String(NAME_MAX_LENGTH) | không\* | — | không\* | — |
| username | String(USERNAME_MAX_LENGTH) | không\* | — | không\* | unique, index |
| email | String(50) | không\* | — | không\* | unique, index |
| hashed_password | String(100) | không\* | — | không\* | — |
| profile_image_url | String | không\* | — | không\* | — |
| tier_id | Integer | không\* | tiers.id | có\* | index |
| is_superuser | bool | không\* | — | không\* | — |
| google_id | String(50) | không\* | — | có\* | unique, index |
| github_id | String(50) | không\* | — | có\* | unique, index |
| oauth_provider | String(20) | không\* | — | có\* | — |
| email_verified | bool | không\* | — | không\* | — |
| oauth_created_at | DateTime(timezone=True) | không\* | — | có\* | — |
| oauth_updated_at | DateTime(timezone=True) | không\* | — | có\* | — |

## 5. Sự kiện và tác vụ nền

Không thấy điểm gửi/nhận qua Kafka, FastStream, Celery hay BackgroundTasks. Có kênh sự kiện chưa đọc được, xem mục 11.

## 6. Cấu trúc code

Vai trò của từng file theo dấu hiệu trong code (FR-029). Chỉ liệt kê component thường.

### Gốc

### backend

Không có vai trò: 3 file rỗng; chưa xác định vai trò: `backend/src/infrastructure/__init__.py`, `backend/src/infrastructure/app_factory.py`, `backend/src/infrastructure/auth/__init__.py`, `backend/src/infrastructure/auth/dependencies.py`, `backend/src/infrastructure/auth/http_exceptions.py`, `backend/src/infrastructure/auth/password_policy.py`, `backend/src/infrastructure/auth/routes.py`, `backend/src/infrastructure/auth/setup.py`, `backend/src/infrastructure/cache/__init__.py`, `backend/src/infrastructure/cache/backends/__init__.py`, `backend/src/infrastructure/cache/backends/memcached.py`, `backend/src/infrastructure/cache/backends/redis.py`, `backend/src/infrastructure/cache/base.py`, `backend/src/infrastructure/cache/decorator.py`, `backend/src/infrastructure/cache/exceptions.py`, `backend/src/infrastructure/cache/initialize.py`, `backend/src/infrastructure/cache/provider.py`, `backend/src/infrastructure/cache/utils.py`, `backend/src/infrastructure/config/__init__.py`, `backend/src/infrastructure/config/enums.py`, `backend/src/infrastructure/config/settings.py`, `backend/src/infrastructure/database/__init__.py`, `backend/src/infrastructure/database/initialize.py`, `backend/src/infrastructure/database/models.py`, `backend/src/infrastructure/database/session.py`, `backend/src/infrastructure/dependencies.py`, `backend/src/infrastructure/logging/__init__.py`, `backend/src/infrastructure/logging/config.py`, `backend/src/infrastructure/logging/factory.py`, `backend/src/infrastructure/logging/formatters.py`, `backend/src/infrastructure/logging/handlers.py`, `backend/src/infrastructure/middleware.py`, `backend/src/infrastructure/redis.py`, `backend/src/infrastructure/security/__init__.py`, `backend/src/infrastructure/security/production_validator.py`, `backend/src/infrastructure/taskiq/__init__.py`, `backend/src/infrastructure/taskiq/app.py`, `backend/src/infrastructure/taskiq/brokers.py`, `backend/src/infrastructure/taskiq/deps.py`, `backend/src/infrastructure/taskiq/registry.py`, `backend/src/infrastructure/taskiq/worker.py`, `backend/src/interfaces/admin/auth.py`, `backend/src/interfaces/admin/initialize.py`, `backend/src/interfaces/admin/mixins.py`, `backend/src/interfaces/admin/views/__init__.py`, `backend/src/interfaces/admin/views/tiers.py`, `backend/src/interfaces/admin/views/users.py`, `backend/src/interfaces/api/__init__.py`, `backend/src/interfaces/api/v1/__init__.py`, `backend/src/interfaces/main.py`, `backend/src/modules/__init__.py`, `backend/src/modules/api_keys/__init__.py`, `backend/src/modules/api_keys/crud.py`, `backend/src/modules/api_keys/dependencies.py`, `backend/src/modules/api_keys/enums.py`, `backend/src/modules/api_keys/models.py`, `backend/src/modules/api_keys/routes.py`, `backend/src/modules/api_keys/schemas.py`, `backend/src/modules/api_keys/service.py`, `backend/src/modules/common/__init__.py`, `backend/src/modules/common/constants.py`, `backend/src/modules/common/exceptions.py`, `backend/src/modules/common/schemas.py`, `backend/src/modules/common/utils/__init__.py`, `backend/src/modules/common/utils/error_handler.py`, `backend/src/modules/common/utils/logger.py`, `backend/src/modules/rate_limit/__init__.py`, `backend/src/modules/rate_limit/crud.py`, `backend/src/modules/rate_limit/dependencies.py`, `backend/src/modules/rate_limit/models.py`, `backend/src/modules/rate_limit/routes.py`, `backend/src/modules/rate_limit/schemas.py`, `backend/src/modules/rate_limit/service.py`, `backend/src/modules/tier/__init__.py`, `backend/src/modules/tier/crud.py`, `backend/src/modules/tier/dependencies.py`, `backend/src/modules/tier/models.py`, `backend/src/modules/tier/routes.py`, `backend/src/modules/tier/schemas.py`, `backend/src/modules/tier/service.py`, `backend/src/modules/user/__init__.py`, `backend/src/modules/user/constants.py`, `backend/src/modules/user/crud.py`, `backend/src/modules/user/dependencies.py`, `backend/src/modules/user/enums.py`, `backend/src/modules/user/models.py`, `backend/src/modules/user/routes.py`, `backend/src/modules/user/schemas.py`, `backend/src/modules/user/service.py`.

### cli

Không có vai trò: 4 file rỗng; chưa xác định vai trò: `cli/src/cli/__init__.py`, `cli/src/cli/app.py`, `cli/src/cli/commands/deploy.py`, `cli/src/cli/commands/env.py`, `cli/src/cli/features/__init__.py`, `cli/src/cli/features/_builtins/deploy/feature.py`, `cli/src/cli/features/base.py`, `cli/src/cli/features/installer.py`, `cli/src/cli/features/registry.py`, `cli/src/cli/lib/project.py`, `cli/src/cli/lib/prompts.py`, `cli/src/cli/lib/render.py`, `cli/src/cli/plugins.py`.

## 7. Gọi HTTP ra ngoài

Không có lời gọi nào qua httpx, requests, aiohttp.

## 8. Thư viện

| Thư viện | Phiên bản | Có import trong code | Khai ở |
|---|---|---|---|
| aiomcache | &gt;=0.8.2 | có | `backend/pyproject.toml:14` |
| aiosqlite | &gt;=0.21.0 | chưa thấy import | `backend/pyproject.toml:15` |
| alembic | &gt;=1.16.4 | chưa thấy import | `backend/pyproject.toml:16` |
| asyncpg | &gt;=0.30.0 | chưa thấy import | `backend/pyproject.toml:17` |
| crudauth | &gt;=0.7.1,&lt;0.8.0 | có | `backend/pyproject.toml:18` |
| faker | &gt;=37.1.0 | chưa thấy import | `backend/pyproject.toml:19` |
| fastapi | &gt;=0.115.8 | có | `backend/pyproject.toml:20` |
| fastapi-boilerplate | — | có | `cli/pyproject.toml:16` |
| fastcrud | &gt;=0.21.0 | có | `backend/pyproject.toml:21` |
| greenlet | &gt;=3.1.1 | chưa thấy import | `backend/pyproject.toml:22` |
| httpx | &gt;=0.28.1 | chưa thấy import | `backend/pyproject.toml:23` |
| itsdangerous | &gt;=2.2.0 | chưa thấy import | `backend/pyproject.toml:24` |
| jinja2 | &gt;=3.1 | có | `cli/pyproject.toml:15` |
| jinja2 | &gt;=3.1.6 | có | `backend/pyproject.toml:25` |
| pydantic | &gt;=2.10.6 | có | `backend/pyproject.toml:26` |
| pydantic-settings | &gt;=2.7.1 | có | `backend/pyproject.toml:27` |
| redis | &gt;=6.1.0 | có | `backend/pyproject.toml:28` |
| sqladmin | &gt;=0.22.0 | có | `backend/pyproject.toml:29` |
| sqlalchemy | &gt;=2.0.37 | có | `backend/pyproject.toml:30` |
| taskiq | &gt;=0.11.20 | có | `backend/pyproject.toml:31` |
| taskiq-aio-pika | &gt;=0.4.3 | có | `backend/pyproject.toml:33` |
| taskiq-redis | &gt;=1.1.2 | có | `backend/pyproject.toml:32` |
| typer | &gt;=0.12 | có | `cli/pyproject.toml:14` |
| user-agents | &gt;=2.2.0 | chưa thấy import | `backend/pyproject.toml:34` |

"Chưa thấy import": tên gói khác tên import, hoặc gói chỉ dùng gián tiếp (driver, plugin, công cụ).

## 9. Cấu hình

| Khóa | Nguồn | Giá trị mặc định | Khai ở |
|---|---|---|---|
| ADMIN_EMAIL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:291` |
| ADMIN_ENABLED | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:300` |
| ADMIN_NAME | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:290` |
| ADMIN_PASSWORD | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:293` |
| ADMIN_USERNAME | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:292` |
| API_CONTACT_EMAIL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:222` |
| API_CONTACT_NAME | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:220` |
| API_CONTACT_URL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:221` |
| API_DESCRIPTION | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:216` |
| API_LICENSE_IDENTIFIER | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:226` |
| API_LICENSE_NAME | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:224` |
| API_LICENSE_URL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:225` |
| API_PREFIX | lớp Settings | /api | `backend/src/infrastructure/config/settings.py:271` |
| API_SUMMARY | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:215` |
| API_TAGS_METADATA | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:228` |
| API_TERMS_OF_SERVICE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:218` |
| API_TITLE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:214` |
| API_VERSION | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:217` |
| APP_DESCRIPTION | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:279` |
| APP_NAME | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:278` |
| CACHE_BACKEND | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:120` |
| CACHE_ENABLED | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:119` |
| CACHE_MEMCACHED_CONNECT_TIMEOUT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:125` |
| CACHE_MEMCACHED_HOST | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:122` |
| CACHE_MEMCACHED_POOL_SIZE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:124` |
| CACHE_MEMCACHED_PORT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:123` |
| CACHE_REDIS_CONNECT_TIMEOUT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:131` |
| CACHE_REDIS_DB | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:129` |
| CACHE_REDIS_HOST | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:127` |
| CACHE_REDIS_PASSWORD | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:130` |
| CACHE_REDIS_POOL_SIZE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:132` |
| CACHE_REDIS_PORT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:128` |
| CLIENT_CACHE_ENABLED | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:136` |
| CLIENT_CACHE_MAX_AGE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:137` |
| CONTACT_EMAIL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:283` |
| CONTACT_NAME | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:282` |
| CORS_ALLOW_CREDENTIALS | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:185` |
| CORS_ALLOW_HEADERS | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:195` |
| CORS_ALLOW_METHODS | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:194` |
| CORS_ENABLED | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:183` |
| CORS_ORIGINS | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:184` |
| CREATE_TABLES_ON_STARTUP | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:60` |
| CSRF_ENABLED | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:248` |
| DATABASE_URL_OVERRIDE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:67` |
| DEBUG | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:280` |
| DEFAULT_CACHE_EXPIRATION | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:134` |
| DEFAULT_RATE_LIMIT_LIMIT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:169` |
| DEFAULT_RATE_LIMIT_PERIOD | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:170` |
| DEFAULT_TIER_NAME | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:294` |
| DOCS_URL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:210` |
| ENABLE_DOCS_IN_PRODUCTION | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:208` |
| ENVIRONMENT | biến môi trường | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:27` |
| ENVIRONMENT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:47` |
| GZIP_ENABLED | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:201` |
| GZIP_MINIMUM_SIZE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:202` |
| LICENSE_NAME | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:284` |
| LOG_CONSOLE_ENABLED | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:317` |
| LOG_CORRELATION_ID | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:323` |
| LOG_DEVELOPMENT_VERBOSE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:330` |
| LOG_FILE_BACKUP_COUNT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:321` |
| LOG_FILE_ENABLED | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:318` |
| LOG_FILE_MAX_SIZE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:320` |
| LOG_FILE_PATH | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:319` |
| LOG_FORMAT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:315` |
| LOG_INCLUDE_STACKTRACE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:328` |
| LOG_LEVEL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:314` |
| LOG_PERFORMANCE_METRICS | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:325` |
| LOG_PRODUCTION_OPTIMIZE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:331` |
| LOG_SQL_QUERIES | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:327` |
| LOG_STRUCTURED_CONTEXT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:324` |
| MAX_SESSIONS_PER_USER | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:238` |
| OAUTH_GITHUB_CLIENT_ID | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:263` |
| OAUTH_GITHUB_CLIENT_SECRET | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:264` |
| OAUTH_GOOGLE_CLIENT_ID | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:261` |
| OAUTH_GOOGLE_CLIENT_SECRET | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:262` |
| OAUTH_REDIRECT_BASE_URL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:265` |
| OPENAPI_PREFIX | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:209` |
| OPENAPI_URL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:212` |
| PASSWORD_MIN_LENGTH | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:255` |
| PASSWORD_REQUIRE_DIGIT | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:258` |
| PASSWORD_REQUIRE_LOWERCASE | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:257` |
| PASSWORD_REQUIRE_SPECIAL | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:259` |
| PASSWORD_REQUIRE_UPPERCASE | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:256` |
| POSTGRES_ASYNC_PREFIX | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:59` |
| POSTGRES_DB | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:57` |
| POSTGRES_MAX_OVERFLOW | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:63` |
| POSTGRES_PASSWORD | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:54` |
| POSTGRES_POOL_PRE_PING | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:64` |
| POSTGRES_POOL_RECYCLE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:65` |
| POSTGRES_POOL_SIZE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:62` |
| POSTGRES_PORT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:56` |
| POSTGRES_SERVER | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:55` |
| POSTGRES_SYNC_PREFIX | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:58` |
| POSTGRES_USER | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:53` |
| PRODUCTION_SECURITY_STRICT_MODE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:307` |
| PRODUCTION_SECURITY_VALIDATION_ENABLED | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:306` |
| RATE_LIMITER_BACKEND | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:167` |
| RATE_LIMITER_ENABLED | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:166` |
| RATE_LIMITER_REDIS_CONNECT_TIMEOUT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:176` |
| RATE_LIMITER_REDIS_DB | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:174` |
| RATE_LIMITER_REDIS_HOST | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:172` |
| RATE_LIMITER_REDIS_PASSWORD | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:175` |
| RATE_LIMITER_REDIS_POOL_SIZE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:177` |
| RATE_LIMITER_REDIS_PORT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:173` |
| REDOC_URL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:211` |
| SECRET_KEY | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:234` |
| SECURITY_HEADERS_ENABLED | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:308` |
| SESSION_BACKEND | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:240` |
| SESSION_CLEANUP_INTERVAL_MINUTES | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:237` |
| SESSION_REDIS_DB | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:242` |
| SESSION_REDIS_URL_OVERRIDE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:243` |
| SESSION_SECURE_COOKIES | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:239` |
| SESSION_TIMEOUT_MINUTES | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:236` |
| TASKIQ_BROKER_TYPE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:350` |
| TASKIQ_ENABLED | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:349` |
| TASKIQ_MAX_TASKS_PER_WORKER | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:364` |
| TASKIQ_RABBITMQ_HOST | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:357` |
| TASKIQ_RABBITMQ_PASSWORD | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:360` |
| TASKIQ_RABBITMQ_PORT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:358` |
| TASKIQ_RABBITMQ_USER | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:359` |
| TASKIQ_RABBITMQ_VHOST | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:361` |
| TASKIQ_REDIS_DB | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:354` |
| TASKIQ_REDIS_HOST | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:352` |
| TASKIQ_REDIS_PASSWORD | lớp Settings | đã che (dấu hiệu bí mật) | `backend/src/infrastructure/config/settings.py:355` |
| TASKIQ_REDIS_PORT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:353` |
| TASKIQ_WORKER_CONCURRENCY | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:363` |
| TRUSTED_PROXY_HOPS | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:253` |
| VERSION | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/src/infrastructure/config/settings.py:281` |

## 10. Middleware và xử lý lỗi toàn cục

| Loại | Tên | Ở đâu |
|---|---|---|
| xử lý lỗi | `RequestValidationError` | `backend/src/modules/common/utils/error_handler.py:72` |
| xử lý lỗi | `DomainError` | `backend/src/modules/common/utils/error_handler.py:81` |
| middleware | `RateLimitHeadersMiddleware` | `backend/src/infrastructure/app_factory.py:274` |
| middleware | `ClientCacheMiddleware` | `backend/src/infrastructure/app_factory.py:279` |
| middleware | `CORSMiddleware` | `backend/src/infrastructure/app_factory.py:296` |
| middleware | `GZipMiddleware` | `backend/src/infrastructure/app_factory.py:300` |
| middleware | `SecurityHeadersMiddleware` | `backend/src/infrastructure/app_factory.py:305` |
| middleware | `SessionMiddleware` | `backend/src/interfaces/main.py:67` |
| middleware | `CatchAllErrorMiddleware` | `backend/src/modules/common/utils/error_handler.py:70` |

Middleware áp dụng cho mọi request của app. Middleware xác thực chỉ cho biết app đọc thông tin đăng nhập; route có bắt buộc đăng nhập hay không vẫn xem ở cột Auth.

## 11. Chưa biết và giới hạn

- **Thư viện hàng đợi chưa hỗ trợ, chưa đọc bên gửi/nhận.** Dùng thư viện hàng đợi/sự kiện chưa hỗ trợ, chưa trích bên gửi/nhận: taskiq (backend/src/infrastructure/taskiq/app.py:5)
- **Chưa có sơ đồ component.** Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- **Chưa đối chiếu với dữ liệu kiến trúc.** Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- **Phân tích chưa xong.** model không gọi công cụ
- **Có phần source chưa đọc.** backend/pyproject.toml thiếu [[1, 134]]; backend/src/infrastructure/__init__.py thiếu [[1, 10]]; backend/src/infrastructure/app_factory.py thiếu [[1, 332]]; backend/src/infrastructure/auth/__init__.py thiếu [[1, 7]]; backend/src/infrastructure/auth/dependencies.py thiếu [[1, 88]]; backend/src/infrastructure/auth/http_exceptions.py thiếu [[1, 82]]; backend/src/infrastructure/auth/password_policy.py thiếu [[1, 13]]; backend/src/infrastructure/auth/routes.py thiếu [[1, 226]]; backend/src/infrastructure/auth/setup.py thiếu [[1, 137]]; backend/src/infrastructure/cache/__init__.py thiếu [[1, 38]]; backend/src/infrastructure/cache/backends/__init__.py thiếu [[1, 32]]; backend/src/infrastructure/cache/backends/memcached.py thiếu [[1, 155]]; backend/src/infrastructure/cache/backends/redis.py thiếu [[1, 150]]; backend/src/infrastructure/cache/base.py thiếu [[1, 243]]; backend/src/infrastructure/cache/decorator.py thiếu [[1, 124]]; backend/src/infrastructure/cache/exceptions.py thiếu [[1, 199]]; backend/src/infrastructure/cache/initialize.py thiếu [[1, 72]]; backend/src/infrastructure/cache/provider.py thiếu [[1, 166]]; backend/src/infrastructure/cache/utils.py thiếu [[1, 111]]; backend/src/infrastructure/config/__init__.py thiếu [[1, 12]]; backend/src/infrastructure/config/enums.py thiếu [[1, 63]]; backend/src/infrastructure/config/settings.py thiếu [[1, 422]]; backend/src/infrastructure/database/__init__.py thiếu [[1, 23]]; backend/src/infrastructure/database/initialize.py thiếu [[1, 8]]; backend/src/infrastructure/database/models.py thiếu [[1, 172]]; backend/src/infrastructure/database/session.py thiếu [[1, 188]]; backend/src/infrastructure/dependencies.py thiếu [[1, 19]]; backend/src/infrastructure/logging/__init__.py thiếu [[1, 34]]; backend/src/infrastructure/logging/config.py thiếu [[1, 350]]; backend/src/infrastructure/logging/factory.py thiếu [[1, 240]]; backend/src/infrastructure/logging/formatters.py thiếu [[1, 189]]; backend/src/infrastructure/logging/handlers.py thiếu [[1, 77]]; backend/src/infrastructure/middleware.py thiếu [[1, 53]]; backend/src/infrastructure/redis.py thiếu [[1, 38]]; backend/src/infrastructure/security/__init__.py thiếu [[1, 5]]; backend/src/infrastructure/security/production_validator.py thiếu [[1, 786]]; backend/src/infrastructure/taskiq/__init__.py thiếu [[1, 12]]; backend/src/infrastructure/taskiq/app.py thiếu [[1, 43]]; backend/src/infrastructure/taskiq/brokers.py thiếu [[1, 52]]; backend/src/infrastructure/taskiq/deps.py thiếu [[1, 58]]; backend/src/infrastructure/taskiq/registry.py thiếu [[1, 65]]; backend/src/infrastructure/taskiq/worker.py thiếu [[1, 13]]; backend/src/interfaces/admin/auth.py thiếu [[1, 45]]; backend/src/interfaces/admin/initialize.py thiếu [[1, 36]]; backend/src/interfaces/admin/mixins.py thiếu [[1, 64]]; backend/src/interfaces/admin/views/__init__.py thiếu [[1, 18]]; backend/src/interfaces/admin/views/tiers.py thiếu [[1, 57]]; backend/src/interfaces/admin/views/users.py thiếu [[1, 72]]; backend/src/interfaces/api/__init__.py thiếu [[1, 10]]; backend/src/interfaces/api/v1/__init__.py thiếu [[1, 16]]; backend/src/interfaces/main.py thiếu [[1, 74]]; backend/src/modules/__init__.py thiếu [[1, 15]]; backend/src/modules/api_keys/__init__.py thiếu [[1, 74]]; backend/src/modules/api_keys/crud.py thiếu [[1, 7]]; backend/src/modules/api_keys/dependencies.py thiếu [[1, 12]]; backend/src/modules/api_keys/enums.py thiếu [[1, 70]]; backend/src/modules/api_keys/models.py thiếu [[1, 86]]; backend/src/modules/api_keys/routes.py thiếu [[1, 322]]; backend/src/modules/api_keys/schemas.py thiếu [[1, 189]]; backend/src/modules/api_keys/service.py thiếu [[1, 632]]; backend/src/modules/common/__init__.py thiếu [[1, 1]]; backend/src/modules/common/constants.py thiếu [[1, 48]]; backend/src/modules/common/exceptions.py thiếu [[1, 73]]; backend/src/modules/common/schemas.py thiếu [[1, 35]]; backend/src/modules/common/utils/__init__.py thiếu [[1, 1]]; backend/src/modules/common/utils/error_handler.py thiếu [[1, 109]]; backend/src/modules/common/utils/logger.py thiếu [[1, 43]]; backend/src/modules/rate_limit/__init__.py thiếu [[1, 17]]; backend/src/modules/rate_limit/crud.py thiếu [[1, 5]]; backend/src/modules/rate_limit/dependencies.py thiếu [[1, 12]]; backend/src/modules/rate_limit/models.py thiếu [[1, 24]]; backend/src/modules/rate_limit/routes.py thiếu [[1, 174]]; backend/src/modules/rate_limit/schemas.py thiếu [[1, 97]]; backend/src/modules/rate_limit/service.py thiếu [[1, 116]]; backend/src/modules/tier/__init__.py thiếu [[1, 27]]; backend/src/modules/tier/crud.py thiếu [[1, 5]]; backend/src/modules/tier/dependencies.py thiếu [[1, 12]]; backend/src/modules/tier/models.py thiếu [[1, 31]]; backend/src/modules/tier/routes.py thiếu [[1, 51]]; backend/src/modules/tier/schemas.py thiếu [[1, 95]]; backend/src/modules/tier/service.py thiếu [[1, 106]]; backend/src/modules/user/__init__.py thiếu [[1, 34]]; backend/src/modules/user/constants.py thiếu [[1, 5]]; backend/src/modules/user/crud.py thiếu [[1, 5]]; backend/src/modules/user/dependencies.py thiếu [[1, 12]]; backend/src/modules/user/enums.py thiếu [[1, 15]]; backend/src/modules/user/models.py thiếu [[1, 64]]; backend/src/modules/user/routes.py thiếu [[1, 400]]; backend/src/modules/user/schemas.py thiếu [[1, 190]]; backend/src/modules/user/service.py thiếu [[1, 637]]; cli/pyproject.toml thiếu [[1, 53]]; cli/src/cli/__init__.py thiếu [[1, 12]]; cli/src/cli/app.py thiếu [[1, 55]]; cli/src/cli/commands/deploy.py thiếu [[1, 91]]; cli/src/cli/commands/env.py thiếu [[1, 111]]; cli/src/cli/features/__init__.py thiếu [[1, 25]]; cli/src/cli/features/_builtins/deploy/feature.py thiếu [[1, 78]]; cli/src/cli/features/base.py thiếu [[1, 98]]; cli/src/cli/features/installer.py thiếu [[1, 87]]; cli/src/cli/features/registry.py thiếu [[1, 44]]; cli/src/cli/lib/project.py thiếu [[1, 70]]; cli/src/cli/lib/prompts.py thiếu [[1, 32]]; cli/src/cli/lib/render.py thiếu [[1, 33]]; cli/src/cli/plugins.py thiếu [[1, 109]]; pyproject.toml thiếu [[1, 25]]
- **File ngoài phạm vi đọc.** conditional_out: 4 file, migration: 1 file, test: 61 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- **Dòng trông giống route hoặc lời gọi HTTP nhưng chưa được xác nhận, nên không có trong tài liệu.** `backend/src/infrastructure/app_factory.py:313`, `backend/src/infrastructure/app_factory.py:317`, `backend/src/infrastructure/app_factory.py:321`, `backend/src/infrastructure/auth/routes.py:21`, `backend/src/infrastructure/auth/routes.py:78`, `backend/src/infrastructure/auth/routes.py:107`, `backend/src/infrastructure/auth/routes.py:144`, `backend/src/infrastructure/auth/routes.py:184`, `backend/src/interfaces/main.py:71`, `backend/src/modules/api_keys/routes.py:20`, `backend/src/modules/api_keys/routes.py:59`, `backend/src/modules/api_keys/routes.py:103`, `backend/src/modules/api_keys/routes.py:136`, `backend/src/modules/api_keys/routes.py:172`, `backend/src/modules/api_keys/routes.py:207`, `backend/src/modules/api_keys/routes.py:253`, `backend/src/modules/api_keys/routes.py:293`, `backend/src/modules/rate_limit/routes.py:16`, `backend/src/modules/rate_limit/routes.py:58`, `backend/src/modules/rate_limit/routes.py:95`, `backend/src/modules/rate_limit/routes.py:138`, `backend/src/modules/tier/routes.py:13`, `backend/src/modules/tier/routes.py:35`, `backend/src/modules/user/routes.py:23`, `backend/src/modules/user/routes.py:55`, `backend/src/modules/user/routes.py:85`, `backend/src/modules/user/routes.py:111`, `backend/src/modules/user/routes.py:138`, `backend/src/modules/user/routes.py:168`, `backend/src/modules/user/routes.py:209`, `backend/src/modules/user/routes.py:247`, `backend/src/modules/user/routes.py:294`, `backend/src/modules/user/routes.py:330`, `backend/src/modules/user/routes.py:367`

## Phụ lục: file cho máy

- TBL (DDL): [tech-specs/BACKEND/schema/TBL-IGORBENAV-FASTAPI-BOILERPLATE-BACKEND.md](tech-specs/BACKEND/schema/TBL-IGORBENAV-FASTAPI-BOILERPLATE-BACKEND.md) — component backend
