# teamhide-fastapi-boilerplate — tài liệu API

Bản sinh tự động từ source, chưa được chủ repository duyệt. File này dành cho người đọc; dữ liệu đầy đủ cho máy nằm ở `result.json` và các file ở phụ lục.

| Mục | Giá trị |
|---|---|
| Tình trạng | Chưa đủ — model không gọi công cụ, xem mục 11 |
| Đọc source | 29/84 file trong phạm vi |
| Endpoint | 0 |
| Model | 0 |
| Bảng CSDL | 1 |
| Sự kiện, tác vụ nền | 2 điểm gửi/nhận |
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

Mọi bảng thuộc component app.

Dấu \* sau một giá trị: code không khai, giá trị lấy theo mặc định có tài liệu của ORM.

| Bảng | Lớp model | Số cột | Khóa ngoại tới |
|---|---|---|---|
| user | User | 9 | — |

### user

Lớp `User`, khai ở `app/user/domain/entity/user.py:10`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_at | DateTime | không\* | — | không | — |
| updated_at | DateTime | không\* | — | không | — |
| id | int | có | — | không\* | — |
| password | String(255) | không\* | — | không | — |
| email | String(255) | không\* | — | không | unique |
| nickname | String(255) | không\* | — | không | unique |
| is_admin | bool | không\* | — | không\* | — |
| lat | chưa rõ (Chưa xác định SQL dialect từ source) | không\* | — | có\* | — |
| lng | chưa rõ (Chưa xác định SQL dialect từ source) | không\* | — | có\* | — |

## 5. Sự kiện và tác vụ nền

| Vai trò | Tác vụ hoặc topic | Thư viện / broker | Component | Ở đâu |
|---|---|---|---|---|
| gửi | core.fastapi.dependencies.logging.Logging._send_log | fastapi.BackgroundTasks | core | `core/fastapi/dependencies/logging.py:6` |
| nhận | core.fastapi.dependencies.logging.Logging._send_log | fastapi.BackgroundTasks | core | `core/fastapi/dependencies/logging.py:8` |

Bên gửi và bên nhận chỉ được nối khi cùng broker và cùng tác vụ (FR-031); file EVT của từng component ghi bên liên quan.

## 6. Cấu trúc code

Vai trò của từng file theo dấu hiệu trong code (FR-029). Chỉ liệt kê component thường.

### Gốc

Không có vai trò: chưa xác định vai trò: `main.py`.

### app

Không có vai trò: 24 file rỗng; chưa xác định vai trò: `app/auth/adapter/input/api/__init__.py`, `app/auth/adapter/input/api/v1/auth.py`, `app/auth/adapter/input/api/v1/request/__init__.py`, `app/auth/adapter/input/api/v1/response/__init__.py`, `app/auth/application/dto/__init__.py`, `app/auth/application/exception/__init__.py`, `app/auth/application/service/jwt.py`, `app/auth/domain/usecase/jwt.py`, `app/container.py`, `app/server.py`, `app/user/adapter/input/api/__init__.py`, `app/user/adapter/input/api/v1/request/__init__.py`, `app/user/adapter/input/api/v1/response/__init__.py`, `app/user/adapter/input/api/v1/user.py`, `app/user/adapter/output/persistence/repository_adapter.py`, `app/user/adapter/output/persistence/sqlalchemy/user.py`, `app/user/application/dto/__init__.py`, `app/user/application/exception/__init__.py`, `app/user/application/service/user.py`, `app/user/container.py`, `app/user/domain/command/__init__.py`, `app/user/domain/entity/user.py`, `app/user/domain/repository/user.py`, `app/user/domain/usecase/user.py`, `app/user/domain/vo/location.py`.

### celery_task

Không có vai trò: 1 file rỗng; chưa xác định vai trò: `celery_task/__init__.py`.

### core

Không có vai trò: 4 file rỗng; chưa xác định vai trò: `core/config.py`, `core/db/__init__.py`, `core/db/mixins/__init__.py`, `core/db/mixins/timestamp_mixin.py`, `core/db/session.py`, `core/db/transactional.py`, `core/exceptions/__init__.py`, `core/exceptions/base.py`, `core/fastapi/dependencies/__init__.py`, `core/fastapi/dependencies/logging.py`, `core/fastapi/dependencies/permission.py`, `core/fastapi/middlewares/__init__.py`, `core/fastapi/middlewares/authentication.py`, `core/fastapi/middlewares/response_log.py`, `core/fastapi/middlewares/sqlalchemy.py`, `core/helpers/cache/__init__.py`, `core/helpers/cache/base/__init__.py`, `core/helpers/cache/base/backend.py`, `core/helpers/cache/base/key_maker.py`, `core/helpers/cache/cache_manager.py`, `core/helpers/cache/cache_tag.py`, `core/helpers/cache/custom_key_maker.py`, `core/helpers/cache/redis_backend.py`, `core/helpers/redis.py`, `core/helpers/token.py`, `core/repository/base.py`, `core/repository/enum.py`.

### Quan hệ giữa component

Đọc tĩnh từ lời gọi, Depends và chỗ dùng bảng đã nối được tới nơi định nghĩa.

| Từ | Tới | Cách dùng | Số chỗ | Ví dụ |
|---|---|---|---|---|
| app | core | gọi hàm | 12 | `app/server.py:73` |
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
| fastapi | ^0.109.1 | có | `pyproject.toml:11` |
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

- **Loại component được suy từ phạm vi đọc.** Membership không ghi loại component; xếp theo phạm vi đọc (FR-028): migrations → migration, tests → test
- **Giá trị có dấu hiệu bí mật đã được che.** Giá trị có dấu hiệu credential đã được che trước khi lưu
- **Chưa có sơ đồ component.** Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- **Chưa đối chiếu với dữ liệu kiến trúc.** Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- **Phân tích chưa xong.** model không gọi công cụ
- **Có phần source chưa đọc.** app/auth/adapter/input/api/__init__.py thiếu [[1, 9]]; app/auth/adapter/input/api/v1/auth.py thiếu [[1, 37]]; app/auth/adapter/input/api/v1/request/__init__.py thiếu [[1, 10]]; app/auth/adapter/input/api/v1/response/__init__.py thiếu [[1, 6]]; app/auth/application/dto/__init__.py thiếu [[1, 6]]; app/auth/application/exception/__init__.py thiếu [[1, 13]]; app/auth/application/service/jwt.py thiếu [[1, 33]]; app/auth/domain/usecase/jwt.py thiếu [[1, 17]]; app/container.py thiếu [[1, 17]]; app/server.py thiếu [[1, 92]]; app/user/adapter/input/api/__init__.py thiếu [[1, 9]]; app/user/adapter/input/api/v1/request/__init__.py thiếu [[1, 15]]; app/user/adapter/input/api/v1/response/__init__.py thiếu [[1, 6]]; app/user/adapter/input/api/v1/user.py thiếu [[1, 53]]; app/user/adapter/output/persistence/repository_adapter.py thiếu [[1, 44]]; app/user/adapter/output/persistence/sqlalchemy/user.py thiếu [[1, 59]]; app/user/application/dto/__init__.py thiếu [[1, 24]]; app/user/application/exception/__init__.py thiếu [[1, 19]]; app/user/application/service/user.py thiếu [[1, 67]]; app/user/container.py thiếu [[1, 17]]; app/user/domain/command/__init__.py thiếu [[1, 10]]; app/user/domain/entity/user.py thiếu [[1, 38]]; app/user/domain/repository/user.py thiếu [[1, 39]]; app/user/domain/usecase/user.py thiếu [[1, 27]]; app/user/domain/vo/location.py thiếu [[1, 7]]; celery_task/__init__.py thiếu [[1, 12]]; core/config.py thiếu [[1, 45]]; core/db/__init__.py thiếu [[1, 9]]; core/db/mixins/__init__.py thiếu [[1, 1]]; core/db/mixins/timestamp_mixin.py thiếu [[1, 18]]; core/db/session.py thiếu [[1, 76]]; core/db/transactional.py thiếu [[1, 19]]; core/exceptions/__init__.py thiếu [[1, 6]]; core/exceptions/base.py thiếu [[1, 8]]; core/fastapi/dependencies/__init__.py thiếu [[1, 15]]; core/fastapi/dependencies/logging.py thiếu [[1, 9]]; core/fastapi/dependencies/permission.py thiếu [[1, 67]]; core/fastapi/middlewares/__init__.py thiếu [[1, 10]]; core/fastapi/middlewares/authentication.py thiếu [[1, 50]]; core/fastapi/middlewares/response_log.py thiếu [[1, 34]]; core/fastapi/middlewares/sqlalchemy.py thiếu [[1, 22]]; core/helpers/cache/__init__.py thiếu [[1, 11]]; core/helpers/cache/base/__init__.py thiếu [[1, 7]]; core/helpers/cache/base/backend.py thiếu [[1, 16]]; core/helpers/cache/base/key_maker.py thiếu [[1, 8]]; core/helpers/cache/cache_manager.py thiếu [[1, 52]]; core/helpers/cache/cache_tag.py thiếu [[1, 5]]; core/helpers/cache/custom_key_maker.py thiếu [[1, 18]]; core/helpers/cache/redis_backend.py thiếu [[1, 28]]; core/helpers/redis.py thiếu [[1, 5]]; core/helpers/token.py thiếu [[1, 57]]; core/repository/base.py thiếu [[1, 50]]; core/repository/enum.py thiếu [[1, 7]]; main.py thiếu [[1, 34]]; pyproject.toml thiếu [[1, 42]]
- **File ngoài phạm vi đọc.** migration: 2 file, test: 39 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- **Dòng trông giống route hoặc lời gọi HTTP nhưng chưa được xác nhận, nên không có trong tài liệu.** `app/auth/adapter/input/api/v1/auth.py:15`, `app/auth/adapter/input/api/v1/auth.py:30`, `app/user/adapter/input/api/v1/user.py:15`, `app/user/adapter/input/api/v1/user.py:29`, `app/user/adapter/input/api/v1/user.py:43`

## Phụ lục: file cho máy

- TBL (DDL): [tech-specs/APP/schema/TBL-TEAMHIDE-FASTAPI-BOILERPLATE-APP.md](tech-specs/APP/schema/TBL-TEAMHIDE-FASTAPI-BOILERPLATE-APP.md) — component app
- EVT: [tech-specs/CORE/events/EVT-TEAMHIDE-FASTAPI-BOILERPLATE-CORE-CORE-FASTAPI-DEPENDENCIES-LOGGING-LOGGING-SEND-LOG.md](tech-specs/CORE/events/EVT-TEAMHIDE-FASTAPI-BOILERPLATE-CORE-CORE-FASTAPI-DEPENDENCIES-LOGGING-LOGGING-SEND-LOG.md) — component core
