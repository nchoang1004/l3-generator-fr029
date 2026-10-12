# teamhide — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:96f8c4c9bb1fbd6f13ba0f2b1a22b3c98fb3e718c6744a39e04ab68535bb4a3f`
- Trạng thái phân tích: partial — BUDGET_TOKENS: hết token
- Độ phủ đọc source: chưa đủ, xem Giới hạn

## Mục lục contract

- API: [tech-specs/APP/api/API-TEAMHIDE-APP-v1.md](tech-specs/APP/api/API-TEAMHIDE-APP-v1.md) — component app

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### (root)

- Package `./`
  - `main.py` — vai trò unknown: agent chưa xác định
  - `pyproject.toml` — vai trò unknown: agent chưa xác định

### app

- Package `app/`
  - `app/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/container.py` — vai trò unknown: agent chưa xác định
  - `app/server.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/`
  - `app/auth/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/adapter/`
  - `app/auth/adapter/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/adapter/input/`
  - `app/auth/adapter/input/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/adapter/input/api/`
  - `app/auth/adapter/input/api/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/adapter/input/api/v1/`
  - `app/auth/adapter/input/api/v1/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/auth/adapter/input/api/v1/auth.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/adapter/input/api/v1/request/`
  - `app/auth/adapter/input/api/v1/request/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/adapter/input/api/v1/response/`
  - `app/auth/adapter/input/api/v1/response/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/application/`
  - `app/auth/application/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/application/dto/`
  - `app/auth/application/dto/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/application/exception/`
  - `app/auth/application/exception/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/application/service/`
  - `app/auth/application/service/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/auth/application/service/jwt.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/domain/`
  - `app/auth/domain/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/domain/entity/`
  - `app/auth/domain/entity/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/auth/domain/usecase/`
  - `app/auth/domain/usecase/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/auth/domain/usecase/jwt.py` — vai trò unknown: agent chưa xác định
- Package `app/user/`
  - `app/user/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/container.py` — vai trò unknown: agent chưa xác định
- Package `app/user/adapter/`
  - `app/user/adapter/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/adapter/input/`
  - `app/user/adapter/input/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/adapter/input/api/`
  - `app/user/adapter/input/api/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/adapter/input/api/v1/`
  - `app/user/adapter/input/api/v1/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/adapter/input/api/v1/user.py` — vai trò unknown: agent chưa xác định
- Package `app/user/adapter/input/api/v1/request/`
  - `app/user/adapter/input/api/v1/request/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/adapter/input/api/v1/response/`
  - `app/user/adapter/input/api/v1/response/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/adapter/output/`
  - `app/user/adapter/output/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/adapter/output/persistence/`
  - `app/user/adapter/output/persistence/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/adapter/output/persistence/repository_adapter.py` — vai trò unknown: agent chưa xác định
- Package `app/user/adapter/output/persistence/sqlalchemy/`
  - `app/user/adapter/output/persistence/sqlalchemy/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/adapter/output/persistence/sqlalchemy/user.py` — vai trò unknown: agent chưa xác định
- Package `app/user/application/`
  - `app/user/application/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/application/dto/`
  - `app/user/application/dto/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/application/exception/`
  - `app/user/application/exception/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/application/service/`
  - `app/user/application/service/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/application/service/user.py` — vai trò unknown: agent chưa xác định
- Package `app/user/domain/`
  - `app/user/domain/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/domain/command/`
  - `app/user/domain/command/__init__.py` — vai trò unknown: agent chưa xác định
- Package `app/user/domain/entity/`
  - `app/user/domain/entity/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/domain/entity/user.py` — vai trò unknown: agent chưa xác định
- Package `app/user/domain/repository/`
  - `app/user/domain/repository/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/domain/repository/user.py` — vai trò unknown: agent chưa xác định
- Package `app/user/domain/usecase/`
  - `app/user/domain/usecase/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/domain/usecase/user.py` — vai trò unknown: agent chưa xác định
- Package `app/user/domain/vo/`
  - `app/user/domain/vo/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/user/domain/vo/location.py` — vai trò unknown: agent chưa xác định

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
  - `celery_task/__init__.py` — vai trò unknown: agent chưa xác định
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
  - `core/config.py` — vai trò unknown: agent chưa xác định
- Package `core/db/`
  - `core/db/__init__.py` — vai trò unknown: agent chưa xác định
  - `core/db/session.py` — vai trò unknown: agent chưa xác định
  - `core/db/transactional.py` — vai trò unknown: agent chưa xác định
- Package `core/db/mixins/`
  - `core/db/mixins/__init__.py` — vai trò unknown: agent chưa xác định
  - `core/db/mixins/timestamp_mixin.py` — vai trò unknown: agent chưa xác định
- Package `core/exceptions/`
  - `core/exceptions/__init__.py` — vai trò unknown: agent chưa xác định
  - `core/exceptions/base.py` — vai trò unknown: agent chưa xác định
- Package `core/fastapi/`
  - `core/fastapi/__init__.py` — vai trò unknown: agent chưa xác định
- Package `core/fastapi/dependencies/`
  - `core/fastapi/dependencies/__init__.py` — vai trò unknown: agent chưa xác định
  - `core/fastapi/dependencies/logging.py` — vai trò unknown: agent chưa xác định
  - `core/fastapi/dependencies/permission.py` — vai trò unknown: agent chưa xác định
- Package `core/fastapi/middlewares/`
  - `core/fastapi/middlewares/__init__.py` — vai trò unknown: agent chưa xác định
  - `core/fastapi/middlewares/authentication.py` — vai trò unknown: agent chưa xác định
  - `core/fastapi/middlewares/response_log.py` — vai trò unknown: agent chưa xác định
  - `core/fastapi/middlewares/sqlalchemy.py` — vai trò unknown: agent chưa xác định
- Package `core/helpers/`
  - `core/helpers/__init__.py` — vai trò unknown: agent chưa xác định
  - `core/helpers/redis.py` — vai trò unknown: agent chưa xác định
  - `core/helpers/token.py` — vai trò unknown: agent chưa xác định
- Package `core/helpers/cache/`
  - `core/helpers/cache/__init__.py` — vai trò unknown: agent chưa xác định
  - `core/helpers/cache/cache_manager.py` — vai trò unknown: agent chưa xác định
  - `core/helpers/cache/cache_tag.py` — vai trò unknown: agent chưa xác định
  - `core/helpers/cache/custom_key_maker.py` — vai trò unknown: agent chưa xác định
  - `core/helpers/cache/redis_backend.py` — vai trò unknown: agent chưa xác định
- Package `core/helpers/cache/base/`
  - `core/helpers/cache/base/__init__.py` — vai trò unknown: agent chưa xác định
  - `core/helpers/cache/base/backend.py` — vai trò unknown: agent chưa xác định
  - `core/helpers/cache/base/key_maker.py` — vai trò unknown: agent chưa xác định
- Package `core/repository/`
  - `core/repository/__init__.py` — vai trò unknown: agent chưa xác định
  - `core/repository/base.py` — vai trò unknown: agent chưa xác định
  - `core/repository/enum.py` — vai trò unknown: agent chưa xác định

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
- `ANALYSIS_PARTIAL`: BUDGET_TOKENS: hết token
- `SOURCE_NOT_FULLY_READ`: app/auth/application/dto/__init__.py thiếu [[1, 6]]; app/auth/application/exception/__init__.py thiếu [[1, 13]]; app/auth/application/service/jwt.py thiếu [[1, 33]]; app/auth/domain/usecase/jwt.py thiếu [[1, 17]]; app/container.py thiếu [[1, 17]]; app/user/adapter/input/api/__init__.py thiếu [[1, 9]]; app/user/adapter/output/persistence/repository_adapter.py thiếu [[1, 44]]; app/user/adapter/output/persistence/sqlalchemy/user.py thiếu [[1, 59]]; app/user/application/exception/__init__.py thiếu [[1, 19]]; app/user/application/service/user.py thiếu [[1, 67]]; app/user/container.py thiếu [[1, 17]]; app/user/domain/command/__init__.py thiếu [[1, 10]]; app/user/domain/entity/user.py thiếu [[1, 38]]; app/user/domain/repository/user.py thiếu [[1, 39]]; app/user/domain/usecase/user.py thiếu [[1, 27]]; app/user/domain/vo/location.py thiếu [[1, 7]]; celery_task/__init__.py thiếu [[1, 12]]; core/config.py thiếu [[1, 45]]; core/db/__init__.py thiếu [[1, 9]]; core/db/mixins/__init__.py thiếu [[1, 1]]; core/db/mixins/timestamp_mixin.py thiếu [[1, 18]]; core/db/session.py thiếu [[1, 76]]; core/db/transactional.py thiếu [[1, 19]]; core/exceptions/__init__.py thiếu [[1, 6]]; core/exceptions/base.py thiếu [[1, 8]]; core/fastapi/dependencies/__init__.py thiếu [[1, 15]]; core/fastapi/dependencies/logging.py thiếu [[1, 9]]; core/fastapi/dependencies/permission.py thiếu [[1, 67]]; core/fastapi/middlewares/__init__.py thiếu [[1, 10]]; core/fastapi/middlewares/authentication.py thiếu [[1, 50]]; core/fastapi/middlewares/response_log.py thiếu [[1, 34]]; core/fastapi/middlewares/sqlalchemy.py thiếu [[1, 22]]; core/helpers/cache/__init__.py thiếu [[1, 11]]; core/helpers/cache/base/__init__.py thiếu [[1, 7]]; core/helpers/cache/base/backend.py thiếu [[1, 16]]; core/helpers/cache/base/key_maker.py thiếu [[1, 8]]; core/helpers/cache/cache_manager.py thiếu [[1, 52]]; core/helpers/cache/cache_tag.py thiếu [[1, 5]]; core/helpers/cache/custom_key_maker.py thiếu [[1, 18]]; core/helpers/cache/redis_backend.py thiếu [[1, 28]]; core/helpers/redis.py thiếu [[1, 5]]; core/helpers/token.py thiếu [[1, 57]]; core/repository/base.py thiếu [[1, 50]]; core/repository/enum.py thiếu [[1, 7]]; pyproject.toml thiếu [[1, 42]]
- `OUT_OF_SCOPE_FILES`: migration: 2 file, test: 39 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- `CLAIMS_REJECTED`: 38 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
