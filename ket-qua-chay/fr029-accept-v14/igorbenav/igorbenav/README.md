# igorbenav — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:8f60a2b03aeb4bdbafd2b22c7f352a82e766014d7f02ad97d01578a502ac12f9`
- Trạng thái phân tích: completed
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/TOAN-BO/api/API-IGORBENAV-TOAN-BO-v1.md](tech-specs/TOAN-BO/api/API-IGORBENAV-TOAN-BO-v1.md) — component Toàn bộ

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Toàn bộ

- Package `backend/migrations/`
  - `backend/migrations/env.py` — vai trò unknown: agent chưa xác định
- Package `backend/scripts/`
  - `backend/scripts/create_first_superuser.py` — vai trò unknown: agent chưa xác định
  - `backend/scripts/create_first_tier.py` — vai trò unknown: agent chưa xác định
  - `backend/scripts/create_tables.py` — vai trò unknown: agent chưa xác định
  - `backend/scripts/setup_initial_data.py` — vai trò unknown: agent chưa xác định
- Package `backend/src/infrastructure/`
  - `backend/src/infrastructure/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/__init__.py:3`: `from .config import get_settings`
  - `backend/src/infrastructure/app_factory.py` — Điểm vào (exact) — `backend/src/infrastructure/app_factory.py:269`: `application = FastAPI(lifespan=lifespan, **kwargs)`
  - `backend/src/infrastructure/dependencies.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/dependencies.py:11`: `AsyncSessionDep = Annotated[AsyncSession, Depends(async_session)]`
  - `backend/src/infrastructure/middleware.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/middleware.py:11`: `class ClientCacheMiddleware(BaseHTTPMiddleware):`
  - `backend/src/infrastructure/redis.py` — Hạ tầng (exact) — `backend/src/infrastructure/redis.py:11`: `return Redis(`
- Package `backend/src/infrastructure/auth/`
  - `backend/src/infrastructure/auth/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/auth/__init__.py:1`: `from .dependencies import get_current_superuser, get_current_user, get_optional_user`
  - `backend/src/infrastructure/auth/dependencies.py` — Truy cập dữ liệu (exact) — `backend/src/infrastructure/auth/dependencies.py:62`: `user = await crud_users.get(db=db, id=principal.user_id, is_deleted=False)`
  - `backend/src/infrastructure/auth/http_exceptions.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/auth/http_exceptions.py:36`: `class CSRFException(HTTPException):`
  - `backend/src/infrastructure/auth/password_policy.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/auth/password_policy.py:7`: `password_policy = PasswordPolicy(`
  - `backend/src/infrastructure/auth/routes.py` — Route (exact) — `backend/src/infrastructure/auth/routes.py:21`: `@router.post(`
  - `backend/src/infrastructure/auth/setup.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/auth/setup.py:20`: `from crudauth.utils import client_ip_key, get_client_ip`
- Package `backend/src/infrastructure/cache/`
  - `backend/src/infrastructure/cache/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/cache/__init__.py:10`: `if MEMCACHED_INSTALLED:`
  - `backend/src/infrastructure/cache/base.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/cache/base.py:5`: `class CacheBackend(ABC):`
  - `backend/src/infrastructure/cache/decorator.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/cache/decorator.py:34`: `def cache(`
  - `backend/src/infrastructure/cache/exceptions.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/cache/exceptions.py:1`: `class CacheException(Exception):`
  - `backend/src/infrastructure/cache/initialize.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/cache/initialize.py:16`: `async def initialize_cache() -> None:`
  - `backend/src/infrastructure/cache/provider.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/cache/provider.py:7`: `class CacheProvider:`
  - `backend/src/infrastructure/cache/utils.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/cache/utils.py:7`: `def infer_resource_id(kwargs: dict[str, Any], resource_id_type: type \| tuple[type, ...]) -> int \| str:`
- Package `backend/src/infrastructure/cache/backends/`
  - `backend/src/infrastructure/cache/backends/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/cache/backends/__init__.py:13`: `if MEMCACHED_INSTALLED:`
  - `backend/src/infrastructure/cache/backends/memcached.py` — Hạ tầng (exact) — `backend/src/infrastructure/cache/backends/memcached.py:59`: `self.client = aiomcache.Client(`
  - `backend/src/infrastructure/cache/backends/redis.py` — Hạ tầng (exact) — `backend/src/infrastructure/cache/backends/redis.py:51`: `self.client = client or Redis(`
- Package `backend/src/infrastructure/config/`
  - `backend/src/infrastructure/config/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/config/__init__.py:1`: `from .enums import CacheBackend, LogFormat, LogLevel, SessionBackend, TaskiqBrokerType`
  - `backend/src/infrastructure/config/enums.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/config/enums.py:6`: `class CacheBackend(StrEnum):`
  - `backend/src/infrastructure/config/settings.py` — Cấu hình (exact) — `backend/src/infrastructure/config/settings.py:7`: `from pydantic_settings import BaseSettings`
- Package `backend/src/infrastructure/database/`
  - `backend/src/infrastructure/database/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/database/__init__.py:1`: `from typing import Any`
  - `backend/src/infrastructure/database/initialize.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/database/initialize.py:6`: `async def close_database() -> None:`
  - `backend/src/infrastructure/database/models.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/database/models.py:10`: `class UUIDMixin(MappedAsDataclass):`
  - `backend/src/infrastructure/database/session.py` — Hạ tầng (exact) — `backend/src/infrastructure/database/session.py:28`: `return create_async_engine(settings.DATABASE_URL, **options)`
- Package `backend/src/infrastructure/logging/`
  - `backend/src/infrastructure/logging/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/logging/__init__.py:27`: `from .config import setup_logging_configuration`
  - `backend/src/infrastructure/logging/config.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/logging/config.py:30`: `def setup_logging_configuration() -> None:`
  - `backend/src/infrastructure/logging/factory.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/logging/factory.py:26`: `def get_logger(name: str \| None = None, **extra_context) -> logging.Logger \| logging.LoggerAdapter:`
  - `backend/src/infrastructure/logging/formatters.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/logging/formatters.py:20`: `class SimpleFormatter(logging.Formatter):`
  - `backend/src/infrastructure/logging/handlers.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/logging/handlers.py:11`: `class ColoredConsoleHandler(logging.StreamHandler):`
- Package `backend/src/infrastructure/security/`
  - `backend/src/infrastructure/security/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/security/__init__.py:3`: `from .production_validator import ProductionSecurityError, ProductionSecurityValidator, validate_production_security`
  - `backend/src/infrastructure/security/production_validator.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/security/production_validator.py:16`: `class ProductionSecurityError(Exception):`
- Package `backend/src/infrastructure/taskiq/`
  - `backend/src/infrastructure/taskiq/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/taskiq/__init__.py:3`: `from .brokers import default_broker`
  - `backend/src/infrastructure/taskiq/app.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/taskiq/app.py:14`: `async def startup_taskiq_worker(state: TaskiqState) -> None:`
  - `backend/src/infrastructure/taskiq/brokers.py` — Hạ tầng (exact) — `backend/src/infrastructure/taskiq/brokers.py:36`: `broker = ListQueueBroker(url=redis_url, queue_name="default").with_result_backend(`
  - `backend/src/infrastructure/taskiq/deps.py` — Hạ tầng (exact) — `backend/src/infrastructure/taskiq/deps.py:20`: `_engine = build_engine(poolclass=NullPool)`
  - `backend/src/infrastructure/taskiq/registry.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/infrastructure/taskiq/registry.py:11`: `class TaskRegistry:`
  - `backend/src/infrastructure/taskiq/worker.py` — Điểm vào (exact) — `backend/src/infrastructure/taskiq/worker.py:11`: `if __name__ == "__main__":`
- Package `backend/src/interfaces/`
  - `backend/src/interfaces/main.py` — Route (exact) — `backend/src/interfaces/main.py:71`: `@app.get("/health", tags=["System"])`
- Package `backend/src/interfaces/admin/`
  - `backend/src/interfaces/admin/auth.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/interfaces/admin/auth.py:18`: `class AdminAuth(AuthenticationBackend):`
  - `backend/src/interfaces/admin/initialize.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/interfaces/admin/initialize.py:27`: `admin = Admin(`
  - `backend/src/interfaces/admin/mixins.py` — Truy cập dữ liệu (exact) — `backend/src/interfaces/admin/mixins.py:60`: `session.add(obj)`
- Package `backend/src/interfaces/admin/views/`
  - `backend/src/interfaces/admin/views/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/interfaces/admin/views/__init__.py:15`: `def register_admin_views(admin: Admin) -> None:`
  - `backend/src/interfaces/admin/views/tiers.py` — Truy cập dữ liệu (exact) — `backend/src/interfaces/admin/views/tiers.py:53`: `tier = await crud_tiers.get(db=db, id=int(pk))`
  - `backend/src/interfaces/admin/views/users.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/interfaces/admin/views/users.py:21`: `class UserAdmin(DataclassModelMixin, ModelView, model=User):`
- Package `backend/src/interfaces/api/`
  - `backend/src/interfaces/api/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/interfaces/api/__init__.py:6`: `router = APIRouter()`
- Package `backend/src/interfaces/api/v1/`
  - `backend/src/interfaces/api/v1/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/interfaces/api/v1/__init__.py:11`: `router = APIRouter(prefix="/v1")`
- Package `backend/src/modules/`
  - `backend/src/modules/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/__init__.py:3`: `from .api_keys.models import APIKey, KeyPermission, KeyUsage`
- Package `backend/src/modules/api_keys/`
  - `backend/src/modules/api_keys/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/api_keys/__init__.py:15`: `from .crud import crud_api_keys, crud_key_permissions, crud_key_usage`
  - `backend/src/modules/api_keys/crud.py` — Truy cập dữ liệu (exact) — `backend/src/modules/api_keys/crud.py:5`: `crud_api_keys: FastCRUD = FastCRUD(APIKey)`
  - `backend/src/modules/api_keys/dependencies.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/api_keys/dependencies.py:12`: `APIKeyServiceDep = Annotated[APIKeyService, Depends(get_api_key_service)]`
  - `backend/src/modules/api_keys/enums.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/api_keys/enums.py:6`: `class KeyStatus(StrEnum):`
  - `backend/src/modules/api_keys/models.py` — Model bảng (exact) — `backend/src/modules/api_keys/models.py:22`: `__tablename__ = "api_keys"`
  - `backend/src/modules/api_keys/routes.py` — Route (exact) — `backend/src/modules/api_keys/routes.py:20`: `@router.post(`
  - `backend/src/modules/api_keys/schemas.py` — Schema API (exact) — `backend/src/modules/api_keys/schemas.py:24`: `class APIKeyCreate(APIKeyBase):`
  - `backend/src/modules/api_keys/service.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `backend/src/modules/api_keys/routes.py:88`, `backend/src/modules/api_keys/service.py:167`, `backend/src/modules/api_keys/crud.py:5`
- Package `backend/src/modules/common/`
  - `backend/src/modules/common/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/common/__init__.py:1`: `"""Common utilities and shared functionality across features."""`
  - `backend/src/modules/common/constants.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/common/constants.py:28`: `# Generic error message for client-facing responses (never leak internal details)`
  - `backend/src/modules/common/exceptions.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/common/exceptions.py:4`: `class DomainError(Exception):`
  - `backend/src/modules/common/schemas.py` — Schema API (exact) — `backend/src/modules/common/schemas.py:7`: `class TimestampSchema(BaseModel):`
- Package `backend/src/modules/common/utils/`
  - `backend/src/modules/common/utils/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/common/utils/__init__.py:1`: `"""Utility functions and helpers."""`
  - `backend/src/modules/common/utils/error_handler.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/common/utils/error_handler.py:60`: `def register_exception_handlers(app: FastAPI) -> None:`
  - `backend/src/modules/common/utils/logger.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/common/utils/logger.py:15`: `def get_logger(name: str, level: int \| None = None) -> logging.Logger \| logging.LoggerAdapter[logging.Logger]:`
- Package `backend/src/modules/rate_limit/`
  - `backend/src/modules/rate_limit/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/rate_limit/__init__.py:7`: `from .crud import crud_rate_limits`
  - `backend/src/modules/rate_limit/crud.py` — Truy cập dữ liệu (exact) — `backend/src/modules/rate_limit/crud.py:5`: `crud_rate_limits: FastCRUD = FastCRUD(RateLimit)`
  - `backend/src/modules/rate_limit/dependencies.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/rate_limit/dependencies.py:8`: `def get_rate_limit_service() -> RateLimitService:`
  - `backend/src/modules/rate_limit/models.py` — Model bảng (exact) — `backend/src/modules/rate_limit/models.py:11`: `__tablename__ = "rate_limits"`
  - `backend/src/modules/rate_limit/routes.py` — Route (exact) — `backend/src/modules/rate_limit/routes.py:16`: `@router.get(`
  - `backend/src/modules/rate_limit/schemas.py` — Schema API (exact) — `backend/src/modules/rate_limit/schemas.py:43`: `class RateLimitRead(RateLimitBase):`
  - `backend/src/modules/rate_limit/service.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `backend/src/modules/rate_limit/routes.py:49`, `backend/src/modules/rate_limit/service.py:54`, `backend/src/modules/rate_limit/crud.py:5`
- Package `backend/src/modules/tier/`
  - `backend/src/modules/tier/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/tier/__init__.py:1`: `from .models import Tier as TierModel`
  - `backend/src/modules/tier/crud.py` — Truy cập dữ liệu (exact) — `backend/src/modules/tier/crud.py:5`: `crud_tiers: FastCRUD = FastCRUD(Tier)`
  - `backend/src/modules/tier/dependencies.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/tier/dependencies.py:8`: `def get_tier_service() -> TierService:`
  - `backend/src/modules/tier/models.py` — Model bảng (exact) — `backend/src/modules/tier/models.py:16`: `__tablename__ = "tiers"`
  - `backend/src/modules/tier/routes.py` — Route (exact) — `backend/src/modules/tier/routes.py:13`: `@router.get(`
  - `backend/src/modules/tier/schemas.py` — Schema API (exact) — `backend/src/modules/tier/schemas.py:36`: `class TierRead(TierBase):`
  - `backend/src/modules/tier/service.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `backend/src/modules/tier/routes.py:27`, `backend/src/modules/tier/service.py:45`, `backend/src/modules/tier/crud.py:5`
- Package `backend/src/modules/user/`
  - `backend/src/modules/user/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/user/__init__.py:3`: `from .enums import OAuthProvider`
  - `backend/src/modules/user/constants.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/user/constants.py:3`: `NAME_MAX_LENGTH = 30`
  - `backend/src/modules/user/crud.py` — Truy cập dữ liệu (exact) — `backend/src/modules/user/crud.py:5`: `crud_users: FastCRUD = FastCRUD(User)`
  - `backend/src/modules/user/dependencies.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/user/dependencies.py:12`: `UserServiceDep = Annotated[UserService, Depends(get_user_service)]`
  - `backend/src/modules/user/enums.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/src/modules/user/enums.py:6`: `class OAuthProvider(StrEnum):`
  - `backend/src/modules/user/models.py` — Model bảng (exact) — `backend/src/modules/user/models.py:18`: `__tablename__ = "user"`
  - `backend/src/modules/user/routes.py` — Route (exact) — `backend/src/modules/user/routes.py:23`: `@router.post(`
  - `backend/src/modules/user/schemas.py` — Schema API (exact) — `backend/src/modules/user/schemas.py:46`: `class UserProfileRead(BaseModel):`
  - `backend/src/modules/user/service.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `backend/src/modules/user/routes.py:80`, `backend/src/modules/user/service.py:131`, `backend/src/modules/user/crud.py:5`
- Package `backend/tests/`
  - `backend/tests/conftest.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/integration/`
  - `backend/tests/integration/conftest.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/integration/test_api_rate_limits.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/integration/api/v1/`
  - `backend/tests/integration/api/v1/test_read_endpoint_auth.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/integration/api/v1/users/`
  - `backend/tests/integration/api/v1/users/helpers.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/integration/api/v1/users/test_create.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/integration/api/v1/users/test_delete.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/integration/api/v1/users/test_read.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/integration/api/v1/users/test_update.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/integration/auth/`
  - `backend/tests/integration/auth/test_endpoints.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/integration/auth/test_oauth.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/unit/infrastructure/`
  - `backend/tests/unit/infrastructure/__init__.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/infrastructure/test_app_factory.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/infrastructure/test_middleware.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/unit/infrastructure/auth/`
  - `backend/tests/unit/infrastructure/auth/test_dependencies.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/infrastructure/auth/test_setup.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/unit/infrastructure/cache/`
  - `backend/tests/unit/infrastructure/cache/test_decorator.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/infrastructure/cache/test_integration.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/infrastructure/cache/test_provider.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/infrastructure/cache/test_utils.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/unit/infrastructure/cache/backends/`
  - `backend/tests/unit/infrastructure/cache/backends/test_memcached.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/infrastructure/cache/backends/test_redis.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/unit/infrastructure/config/`
  - `backend/tests/unit/infrastructure/config/test_settings.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/unit/infrastructure/database/`
  - `backend/tests/unit/infrastructure/database/test_engine.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/infrastructure/database/test_initialize.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/infrastructure/database/test_session.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/unit/infrastructure/logging/`
  - `backend/tests/unit/infrastructure/logging/test_correlation_id.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/unit/infrastructure/security/`
  - `backend/tests/unit/infrastructure/security/__init__.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/infrastructure/security/test_production_validator.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/unit/infrastructure/taskiq/`
  - `backend/tests/unit/infrastructure/taskiq/test_deps.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/unit/interfaces/admin/`
  - `backend/tests/unit/interfaces/admin/test_auth.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/interfaces/admin/test_tier_view.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/unit/modules/api_keys/`
  - `backend/tests/unit/modules/api_keys/test_service.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/unit/modules/common/`
  - `backend/tests/unit/modules/common/__init__.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/modules/common/test_error_handler.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/modules/common/test_persistence_failures.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/unit/modules/tier/`
  - `backend/tests/unit/modules/tier/test_models.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/modules/tier/test_service.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/unit/modules/user/`
  - `backend/tests/unit/modules/user/test_models.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/unit/modules/user/test_schemas.py` — vai trò unknown: agent chưa xác định
- Package `cli/src/cli/`
  - `cli/src/cli/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `cli/src/cli/__init__.py:1`: `"""bp — the FastAPI-boilerplate command-line tool.`
  - `cli/src/cli/app.py` — Điểm vào (exact) — `cli/src/cli/app.py:16`: `app = typer.Typer(`
  - `cli/src/cli/plugins.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `cli/src/cli/plugins.py:32`: `def _safe_load(ep: EntryPoint) -> object \| None:`
- Package `cli/src/cli/commands/`
  - `cli/src/cli/commands/deploy.py` — Điểm vào (exact) — `cli/src/cli/commands/deploy.py:29`: `@app.command("generate")`
  - `cli/src/cli/commands/env.py` — Điểm vào (exact) — `cli/src/cli/commands/env.py:35`: `@app.command("gen-secret")`
- Package `cli/src/cli/features/`
  - `cli/src/cli/features/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `cli/src/cli/features/__init__.py:13`: `from .base import Codemod, Feature, FeatureManifest, FeaturePlan, FileOp, Hook`
  - `cli/src/cli/features/base.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `cli/src/cli/features/base.py:86`: `class Feature(ABC):`
  - `cli/src/cli/features/installer.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `cli/src/cli/features/installer.py:38`: `def apply(self, plan: FeaturePlan) -> InstallResult:`
  - `cli/src/cli/features/registry.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `cli/src/cli/features/registry.py:24`: `def all_features() -> dict[str, Feature]:`
- Package `cli/src/cli/features/_builtins/deploy/`
  - `cli/src/cli/features/_builtins/deploy/feature.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `cli/src/cli/features/_builtins/deploy/feature.py:27`: `class DeployFeature(Feature):`
- Package `cli/src/cli/lib/`
  - `cli/src/cli/lib/project.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `cli/src/cli/lib/project.py:35`: `def discover_project(start: Path \| None = None) -> ProjectContext:`
  - `cli/src/cli/lib/prompts.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `cli/src/cli/lib/prompts.py:12`: `def confirm_overwrite(path: str, *, assume_yes: bool) -> bool:`
  - `cli/src/cli/lib/render.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `cli/src/cli/lib/render.py:16`: `class Renderer:`

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
- `OUT_OF_SCOPE_FILES`: conditional_out: 4 file, migration: 1 file, test: 61 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- `CLAIMS_REJECTED`: 33 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
