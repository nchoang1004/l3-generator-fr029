# teamhide — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:96f8c4c9bb1fbd6f13ba0f2b1a22b3c98fb3e718c6744a39e04ab68535bb4a3f`
- Trạng thái phân tích: partial — MODEL_ERROR: LOCAL_BUDGET_RESERVATION_STOP
- Độ phủ đọc source: đủ

## Mục lục contract

- (không có)

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### (root)

- Package `./`
  - `main.py` — Điểm vào (exact) — `main.py:24`: `uvicorn.run(`
  - `pyproject.toml` — vai trò unknown: agent chưa xác định

### app

- Package `app/`
  - `app/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/container.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/container.py:10`: `class Container(DeclarativeContainer):`
  - `app/server.py` — Điểm vào (exact) — `app/server.py:77`: `app_ = FastAPI(`
- Package `app/auth/`
  - `app/auth/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/adapter/`
  - `app/auth/adapter/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/adapter/input/`
  - `app/auth/adapter/input/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/adapter/input/api/`
  - `app/auth/adapter/input/api/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/auth/adapter/input/api/__init__.py:6`: `router.include_router(auth_v1_router, prefix="/api/v1/auth", tags=["Auth"])`
- Package `app/auth/adapter/input/api/v1/`
  - `app/auth/adapter/input/api/v1/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/auth/adapter/input/api/v1/auth.py` — Route (exact) — `app/auth/adapter/input/api/v1/auth.py:15`: `@auth_router.post(`
- Package `app/auth/adapter/input/api/v1/request/`
  - `app/auth/adapter/input/api/v1/request/__init__.py` — Schema API (exact) — `app/auth/adapter/input/api/v1/request/__init__.py:4`: `class RefreshTokenRequest(BaseModel):`
- Package `app/auth/adapter/input/api/v1/response/`
  - `app/auth/adapter/input/api/v1/response/__init__.py` — Schema API (exact) — `app/auth/adapter/input/api/v1/response/__init__.py:4`: `class RefreshTokenResponse(BaseModel):`
- Package `app/auth/application/`
  - `app/auth/application/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/application/dto/`
  - `app/auth/application/dto/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/auth/application/dto/__init__.py:4`: `class RefreshTokenResponseDTO(BaseModel):`
- Package `app/auth/application/exception/`
  - `app/auth/application/exception/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/auth/application/exception/__init__.py:4`: `class DecodeTokenException(CustomException):`
- Package `app/auth/application/service/`
  - `app/auth/application/service/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/auth/application/service/jwt.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/auth/application/service/jwt.py:11`: `class JwtService(JwtUseCase):`
- Package `app/auth/domain/`
  - `app/auth/domain/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/domain/entity/`
  - `app/auth/domain/entity/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/domain/usecase/`
  - `app/auth/domain/usecase/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/auth/domain/usecase/jwt.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/auth/domain/usecase/jwt.py:6`: `class JwtUseCase(ABC):`
- Package `app/user/`
  - `app/user/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/container.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/user/container.py:9`: `class UserContainer(DeclarativeContainer):`
- Package `app/user/adapter/`
  - `app/user/adapter/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/adapter/input/`
  - `app/user/adapter/input/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/adapter/input/api/`
  - `app/user/adapter/input/api/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/user/adapter/input/api/__init__.py:6`: `router.include_router(user_v1_router, prefix="/api/v1/user", tags=["User"])`
- Package `app/user/adapter/input/api/v1/`
  - `app/user/adapter/input/api/v1/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/adapter/input/api/v1/user.py` — Route (exact) — `app/user/adapter/input/api/v1/user.py:15`: `@user_router.get(`
- Package `app/user/adapter/input/api/v1/request/`
  - `app/user/adapter/input/api/v1/request/__init__.py` — Schema API (exact) — `app/user/adapter/input/api/v1/request/__init__.py:4`: `class LoginRequest(BaseModel):`
- Package `app/user/adapter/input/api/v1/response/`
  - `app/user/adapter/input/api/v1/response/__init__.py` — Schema API (exact) — `app/user/adapter/input/api/v1/response/__init__.py:4`: `class LoginResponse(BaseModel):`
- Package `app/user/adapter/output/`
  - `app/user/adapter/output/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/adapter/output/persistence/`
  - `app/user/adapter/output/persistence/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/adapter/output/persistence/repository_adapter.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `app/user/adapter/input/api/v1/user.py:38`, `app/user/application/service/user.py:46`, `app/user/adapter/output/persistence/repository_adapter.py:44`, `app/user/adapter/output/persistence/sqlalchemy/user.py:59`
- Package `app/user/adapter/output/persistence/sqlalchemy/`
  - `app/user/adapter/output/persistence/sqlalchemy/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/adapter/output/persistence/sqlalchemy/user.py` — Truy cập dữ liệu (exact) — `app/user/adapter/output/persistence/sqlalchemy/user.py:24`: `async with session_factory() as read_session:`
- Package `app/user/application/`
  - `app/user/application/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/application/dto/`
  - `app/user/application/dto/__init__.py` — Schema API (exact) — `app/user/application/dto/__init__.py:4`: `class GetUserListResponseDTO(BaseModel):`
- Package `app/user/application/exception/`
  - `app/user/application/exception/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/user/application/exception/__init__.py:4`: `class PasswordDoesNotMatchException(CustomException):`
- Package `app/user/application/service/`
  - `app/user/application/service/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/application/service/user.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `app/user/adapter/input/api/v1/user.py:38`, `app/user/application/service/user.py:46`, `app/user/adapter/output/persistence/repository_adapter.py:44`, `app/user/adapter/output/persistence/sqlalchemy/user.py:59`
- Package `app/user/domain/`
  - `app/user/domain/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/domain/command/`
  - `app/user/domain/command/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/user/domain/command/__init__.py:4`: `class CreateUserCommand(BaseModel):`
- Package `app/user/domain/entity/`
  - `app/user/domain/entity/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/domain/entity/user.py` — Model bảng (exact) — `app/user/domain/entity/user.py:11`: `__tablename__ = "user"`
- Package `app/user/domain/repository/`
  - `app/user/domain/repository/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/domain/repository/user.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/user/domain/repository/user.py:5`: `class UserRepo(ABC):`
- Package `app/user/domain/usecase/`
  - `app/user/domain/usecase/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/domain/usecase/user.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/user/domain/usecase/user.py:7`: `class UserUseCase(ABC):`
- Package `app/user/domain/vo/`
  - `app/user/domain/vo/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/domain/vo/location.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/user/domain/vo/location.py:4`: `@dataclass`

### tests

- Package `tests/`
  - `tests/__init__.py` — vai trò unknown: agent chưa xác định
  - `tests/conftest.py` — vai trò unknown: agent chưa xác định
- Package `tests/app/`
  - `tests/app/__init__.py` — vai trò unknown: agent chưa xác định
- Package `tests/app/auth/`
  - `tests/app/auth/__init__.py` — vai trò unknown: agent chưa xác định
- Package `tests/app/auth/application/`
  - `tests/app/auth/application/__init__.py` — vai trò unknown: agent chưa xác định
- Package `tests/app/auth/application/service/`
  - `tests/app/auth/application/service/__init__.py` — vai trò unknown: agent chưa xác định
  - `tests/app/auth/application/service/test_jwt.py` — vai trò unknown: agent chưa xác định
- Package `tests/app/user/`
  - `tests/app/user/__init__.py` — vai trò unknown: agent chưa xác định
- Package `tests/app/user/adapter/`
  - `tests/app/user/adapter/__init__.py` — vai trò unknown: agent chưa xác định
- Package `tests/app/user/adapter/input/`
  - `tests/app/user/adapter/input/__init__.py` — vai trò unknown: agent chưa xác định
- Package `tests/app/user/adapter/input/api/`
  - `tests/app/user/adapter/input/api/__init__.py` — vai trò unknown: agent chưa xác định
- Package `tests/app/user/adapter/input/api/v1/`
  - `tests/app/user/adapter/input/api/v1/__init__.py` — vai trò unknown: agent chưa xác định
  - `tests/app/user/adapter/input/api/v1/test_user.py` — vai trò unknown: agent chưa xác định
- Package `tests/app/user/adapter/output/`
  - `tests/app/user/adapter/output/__init__.py` — vai trò unknown: agent chưa xác định
- Package `tests/app/user/adapter/output/persistence/`
  - `tests/app/user/adapter/output/persistence/__init__.py` — vai trò unknown: agent chưa xác định
  - `tests/app/user/adapter/output/persistence/test_repository_adapter.py` — vai trò unknown: agent chưa xác định
- Package `tests/app/user/adapter/output/persistence/sqlalchemy/`
  - `tests/app/user/adapter/output/persistence/sqlalchemy/__init__.py` — vai trò unknown: agent chưa xác định
  - `tests/app/user/adapter/output/persistence/sqlalchemy/test_user.py` — vai trò unknown: agent chưa xác định
- Package `tests/app/user/application/`
  - `tests/app/user/application/__init__.py` — vai trò unknown: agent chưa xác định
- Package `tests/app/user/application/service/`
  - `tests/app/user/application/service/__init__.py` — vai trò unknown: agent chưa xác định
  - `tests/app/user/application/service/test_user.py` — vai trò unknown: agent chưa xác định
- Package `tests/core/`
  - `tests/core/__init__.py` — vai trò unknown: agent chưa xác định
- Package `tests/core/exceptions/`
  - `tests/core/exceptions/__init__.py` — vai trò unknown: agent chưa xác định
  - `tests/core/exceptions/test_base.py` — vai trò unknown: agent chưa xác định
- Package `tests/core/fastapi/`
  - `tests/core/fastapi/__init__.py` — vai trò unknown: agent chưa xác định
- Package `tests/core/fastapi/dependencies/`
  - `tests/core/fastapi/dependencies/__init__.py` — vai trò unknown: agent chưa xác định
  - `tests/core/fastapi/dependencies/test_permission.py` — vai trò unknown: agent chưa xác định
- Package `tests/core/fastapi/middlewares/`
  - `tests/core/fastapi/middlewares/__init__.py` — vai trò unknown: agent chưa xác định
  - `tests/core/fastapi/middlewares/test_authentication.py` — vai trò unknown: agent chưa xác định
  - `tests/core/fastapi/middlewares/test_sqlalchemy.py` — vai trò unknown: agent chưa xác định
- Package `tests/core/helpers/`
  - `tests/core/helpers/__init__.py` — vai trò unknown: agent chưa xác định
  - `tests/core/helpers/test_token.py` — vai trò unknown: agent chưa xác định
- Package `tests/core/helpers/cache/`
  - `tests/core/helpers/cache/__init__.py` — vai trò unknown: agent chưa xác định
  - `tests/core/helpers/cache/test_custom_key_maker.py` — vai trò unknown: agent chưa xác định
  - `tests/core/helpers/cache/test_redis_backend.py` — vai trò unknown: agent chưa xác định
- Package `tests/support/`
  - `tests/support/__init__.py` — vai trò unknown: agent chưa xác định
  - `tests/support/test_db_coordinator.py` — vai trò unknown: agent chưa xác định
  - `tests/support/token.py` — vai trò unknown: agent chưa xác định
  - `tests/support/user_fixture.py` — vai trò unknown: agent chưa xác định

### celery_task

- Package `celery_task/`
  - `celery_task/__init__.py` — Hạ tầng (exact) — `celery_task/__init__.py:5`: `celery_app = Celery(`
- Package `celery_task/tasks/`
  - `celery_task/tasks/__init__.py` — vai trò unknown: agent chưa xác định

### migrations

- Package `migrations/`
  - `migrations/env.py` — vai trò unknown: agent chưa xác định
- Package `migrations/versions/`
  - `migrations/versions/59628dea39ff_init.py` — vai trò unknown: agent chưa xác định

### core

- Package `core/`
  - `core/__init__.py` — vai trò unknown: agent chưa xác định
  - `core/config.py` — Cấu hình (exact) — `core/config.py:6`: `class Config(BaseSettings):`
- Package `core/db/`
  - `core/db/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/db/__init__.py:1`: `from .session import Base, session, session_factory`
  - `core/db/session.py` — Hạ tầng (exact) — `core/db/session.py:37`: `engines = {`
  - `core/db/transactional.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/db/transactional.py:6`: `class Transactional:`
- Package `core/db/mixins/`
  - `core/db/mixins/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/db/mixins/__init__.py:1`: `from .timestamp_mixin import *`
  - `core/db/mixins/timestamp_mixin.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/db/mixins/timestamp_mixin.py:7`: `class TimestampMixin:`
- Package `core/exceptions/`
  - `core/exceptions/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/exceptions/__init__.py:1`: `from .base import CustomException`
  - `core/exceptions/base.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/exceptions/base.py:1`: `class CustomException(Exception):`
- Package `core/fastapi/`
  - `core/fastapi/__init__.py` — vai trò unknown: agent chưa xác định
- Package `core/fastapi/dependencies/`
  - `core/fastapi/dependencies/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/fastapi/dependencies/__init__.py:1`: `from .logging import Logging`
  - `core/fastapi/dependencies/logging.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/fastapi/dependencies/logging.py:4`: `class Logging:`
  - `core/fastapi/dependencies/permission.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/fastapi/dependencies/permission.py:57`: `class PermissionDependency(SecurityBase):`
- Package `core/fastapi/middlewares/`
  - `core/fastapi/middlewares/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/fastapi/middlewares/__init__.py:1`: `from .authentication import AuthenticationMiddleware, AuthBackend`
  - `core/fastapi/middlewares/authentication.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/fastapi/middlewares/authentication.py:16`: `class AuthBackend(AuthenticationBackend):`
  - `core/fastapi/middlewares/response_log.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/fastapi/middlewares/response_log.py:14`: `class ResponseLogMiddleware:`
  - `core/fastapi/middlewares/sqlalchemy.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/fastapi/middlewares/sqlalchemy.py:8`: `class SQLAlchemyMiddleware:`
- Package `core/helpers/`
  - `core/helpers/__init__.py` — vai trò unknown: agent chưa xác định
  - `core/helpers/redis.py` — Hạ tầng (exact) — `core/helpers/redis.py:5`: `redis_client = redis.from_url(url=f"redis://{config.REDIS_HOST}", decode_responses=True)`
  - `core/helpers/token.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/helpers/token.py:21`: `class TokenHelper:`
- Package `core/helpers/cache/`
  - `core/helpers/cache/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/helpers/cache/__init__.py:1`: `from .cache_manager import Cache`
  - `core/helpers/cache/cache_manager.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/helpers/cache/cache_manager.py:7`: `class CacheManager:`
  - `core/helpers/cache/cache_tag.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/helpers/cache/cache_tag.py:4`: `class CacheTag(Enum):`
  - `core/helpers/cache/custom_key_maker.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/helpers/cache/custom_key_maker.py:7`: `class CustomKeyMaker(BaseKeyMaker):`
  - `core/helpers/cache/redis_backend.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/helpers/cache/redis_backend.py:10`: `class RedisBackend(BaseBackend):`
- Package `core/helpers/cache/base/`
  - `core/helpers/cache/base/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/helpers/cache/base/__init__.py:1`: `from .backend import BaseBackend`
  - `core/helpers/cache/base/backend.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/helpers/cache/base/backend.py:5`: `class BaseBackend(ABC):`
  - `core/helpers/cache/base/key_maker.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/helpers/cache/base/key_maker.py:5`: `class BaseKeyMaker(ABC):`
- Package `core/repository/`
  - `core/repository/__init__.py` — vai trò unknown: agent chưa xác định
  - `core/repository/base.py` — Truy cập dữ liệu (exact) — `core/repository/base.py:31`: `await session.execute(query)`
  - `core/repository/enum.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `core/repository/enum.py:4`: `class SynchronizeSessionEnum(BaseModel):`

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `DIAGRAM_NOT_PROVIDED`: Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- `ARCHITECTURE_NOT_EVALUATED`: Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- `ANALYSIS_PARTIAL`: MODEL_ERROR: LOCAL_BUDGET_RESERVATION_STOP
- `OUT_OF_SCOPE_FILES`: migration: 2 file, test: 39 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- `CLAIMS_REJECTED`: 41 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
