# orderflow — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:1652d2f28ed89004513f72827729db18a8da11a302812bc066361cfbafd8abf3`
- Trạng thái phân tích: partial — REPAIR_ROUNDS: còn lỗi sau 0 vòng sửa
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/TOAN-BO/api/API-ORDERFLOW-TOAN-BO-v1.md](tech-specs/TOAN-BO/api/API-ORDERFLOW-TOAN-BO-v1.md) — component Toàn bộ
- TBL: [tech-specs/TOAN-BO/schema/TBL-ORDERFLOW-TOAN-BO.md](tech-specs/TOAN-BO/schema/TBL-ORDERFLOW-TOAN-BO.md) — component Toàn bộ

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Toàn bộ

- Package `services/catalog-service/catalog_app/`
  - `services/catalog-service/catalog_app/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/catalog-service/catalog_app/__init__.py:1`: `"""Catalog Service — каталог товаров с собственной схемой БД."""`
  - `services/catalog-service/catalog_app/main.py` — Điểm vào (exact) — `services/catalog-service/catalog_app/main.py:29`: `app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)`
  - `services/catalog-service/catalog_app/models.py` — Model bảng (exact) — `services/catalog-service/catalog_app/models.py:13`: `__tablename__ = "products"`
- Package `services/catalog-service/catalog_app/api/`
  - `services/catalog-service/catalog_app/api/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/catalog-service/catalog_app/api/__init__.py:1`: `"""HTTP-слой catalog-service."""`
  - `services/catalog-service/catalog_app/api/router.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/catalog-service/catalog_app/api/router.py:5`: `api_router = APIRouter(prefix="/api/v1")`
- Package `services/catalog-service/catalog_app/api/routes/`
  - `services/catalog-service/catalog_app/api/routes/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/catalog-service/catalog_app/api/routes/__init__.py:1`: `"""Маршруты catalog-service."""`
  - `services/catalog-service/catalog_app/api/routes/products.py` — Route (exact) — `services/catalog-service/catalog_app/api/routes/products.py:14`: `@router.get("", response_model=list[ProductRead])`
- Package `services/catalog-service/catalog_app/core/`
  - `services/catalog-service/catalog_app/core/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/catalog-service/catalog_app/core/__init__.py:1`: `"""Ядро catalog-service: конфигурация и доступ к БД."""`
  - `services/catalog-service/catalog_app/core/config.py` — Cấu hình (exact) — `services/catalog-service/catalog_app/core/config.py:6`: `class Settings(BaseSettings):`
  - `services/catalog-service/catalog_app/core/database.py` — Hạ tầng (exact) — `services/catalog-service/catalog_app/core/database.py:28`: `_engine = create_async_engine(get_settings().database_url, pool_pre_ping=True)`
- Package `services/catalog-service/catalog_app/services/`
  - `services/catalog-service/catalog_app/services/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/catalog-service/catalog_app/services/__init__.py:1`: `"""Бизнес-логика catalog-service."""`
  - `services/catalog-service/catalog_app/services/products.py` — Truy cập dữ liệu (exact) — `services/catalog-service/catalog_app/services/products.py:14`: `result = await session.scalars(select(Product).order_by(Product.id).offset(offset).limit(limit))`
- Package `services/gateway/gateway_app/`
  - `services/gateway/gateway_app/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/gateway/gateway_app/__init__.py:1`: `"""Gateway — единая точка входа /api/v1/*."""`
  - `services/gateway/gateway_app/main.py` — Điểm vào (exact) — `services/gateway/gateway_app/main.py:33`: `app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)`
- Package `services/gateway/gateway_app/api/`
  - `services/gateway/gateway_app/api/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/gateway/gateway_app/api/__init__.py:1`: `"""HTTP-слой шлюза."""`
  - `services/gateway/gateway_app/api/router.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/gateway/gateway_app/api/router.py:5`: `api_router = APIRouter(prefix="/api/v1")`
- Package `services/gateway/gateway_app/api/routes/`
  - `services/gateway/gateway_app/api/routes/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/gateway/gateway_app/api/routes/__init__.py:1`: `"""Маршруты шлюза."""`
  - `services/gateway/gateway_app/api/routes/proxy.py` — Route (exact) — `services/gateway/gateway_app/api/routes/proxy.py:20`: `@router.get("/products", response_model=list[ProductRead])`
- Package `services/gateway/gateway_app/core/`
  - `services/gateway/gateway_app/core/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/gateway/gateway_app/core/__init__.py:1`: `"""Ядро шлюза: конфигурация, клиенты, проксирование."""`
  - `services/gateway/gateway_app/core/clients.py` — Hạ tầng (exact) — `services/gateway/gateway_app/core/clients.py:25`: `CATALOG: httpx.AsyncClient(`
  - `services/gateway/gateway_app/core/config.py` — Cấu hình (exact) — `services/gateway/gateway_app/core/config.py:6`: `class Settings(BaseSettings):`
  - `services/gateway/gateway_app/core/proxy.py` — Hạ tầng (exact) — `services/gateway/gateway_app/core/proxy.py:25`: `upstream = await client.request(request.method, url, content=body or None, headers=headers)`
- Package `services/notification-service/notification_app/`
  - `services/notification-service/notification_app/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/notification-service/notification_app/__init__.py:1`: `"""Notification Service — подписка на order.created и доставка уведомлений."""`
  - `services/notification-service/notification_app/main.py` — Điểm vào (exact) — `services/notification-service/notification_app/main.py:59`: `app = FastAPI(title=resolved_settings.app_name, version="1.0.0", lifespan=lifespan)`
  - `services/notification-service/notification_app/models.py` — Model bảng (exact) — `services/notification-service/notification_app/models.py:12`: `__tablename__ = "notifications"`
- Package `services/notification-service/notification_app/api/`
  - `services/notification-service/notification_app/api/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/notification-service/notification_app/api/__init__.py:1`: `"""HTTP-слой notification-service."""`
  - `services/notification-service/notification_app/api/router.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/notification-service/notification_app/api/router.py:5`: `api_router = APIRouter(prefix="/api/v1")`
- Package `services/notification-service/notification_app/api/routes/`
  - `services/notification-service/notification_app/api/routes/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/notification-service/notification_app/api/routes/__init__.py:1`: `"""Маршруты notification-service."""`
  - `services/notification-service/notification_app/api/routes/notifications.py` — Route (exact) — `services/notification-service/notification_app/api/routes/notifications.py:14`: `@router.get("", response_model=list[NotificationRead])`
- Package `services/notification-service/notification_app/core/`
  - `services/notification-service/notification_app/core/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/notification-service/notification_app/core/__init__.py:1`: `"""Ядро notification-service: конфигурация и доступ к БД."""`
  - `services/notification-service/notification_app/core/config.py` — Cấu hình (exact) — `services/notification-service/notification_app/core/config.py:6`: `class Settings(BaseSettings):`
  - `services/notification-service/notification_app/core/database.py` — Hạ tầng (exact) — `services/notification-service/notification_app/core/database.py:28`: `_engine = create_async_engine(get_settings().database_url, pool_pre_ping=True)`
- Package `services/notification-service/notification_app/services/`
  - `services/notification-service/notification_app/services/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/notification-service/notification_app/services/__init__.py:1`: `"""Бизнес-логика notification-service."""`
  - `services/notification-service/notification_app/services/notifications.py` — Truy cập dữ liệu (exact) — `services/notification-service/notification_app/services/notifications.py:19`: `existing = await session.scalar(`
- Package `services/order-service/order_app/`
  - `services/order-service/order_app/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/order-service/order_app/__init__.py:1`: `"""Order Service — заказы, вызов catalog-service и публикация order.created."""`
  - `services/order-service/order_app/main.py` — Điểm vào (exact) — `services/order-service/order_app/main.py:42`: `app = FastAPI(title=resolved_settings.app_name, version="1.0.0", lifespan=lifespan)`
  - `services/order-service/order_app/models.py` — Model bảng (exact) — `services/order-service/order_app/models.py:14`: `__tablename__ = "orders"`
- Package `services/order-service/order_app/api/`
  - `services/order-service/order_app/api/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/order-service/order_app/api/__init__.py:1`: `"""HTTP-слой order-service."""`
  - `services/order-service/order_app/api/router.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/order-service/order_app/api/router.py:5`: `api_router = APIRouter(prefix="/api/v1")`
- Package `services/order-service/order_app/api/routes/`
  - `services/order-service/order_app/api/routes/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/order-service/order_app/api/routes/__init__.py:1`: `"""Маршруты order-service."""`
  - `services/order-service/order_app/api/routes/orders.py` — Route (exact) — `services/order-service/order_app/api/routes/orders.py:31`: `@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)`
- Package `services/order-service/order_app/core/`
  - `services/order-service/order_app/core/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/order-service/order_app/core/__init__.py:1`: `"""Ядро order-service: конфигурация, БД, устойчивость вызовов."""`
  - `services/order-service/order_app/core/catalog_client.py` — Hạ tầng (exact) — `services/order-service/order_app/core/catalog_client.py:98`: `response = await self._client.get(f"/api/v1/products/{product_id}", headers=headers)`
  - `services/order-service/order_app/core/config.py` — Cấu hình (exact) — `services/order-service/order_app/core/config.py:6`: `class Settings(BaseSettings):`
  - `services/order-service/order_app/core/database.py` — Hạ tầng (exact) — `services/order-service/order_app/core/database.py:28`: `_engine = create_async_engine(get_settings().database_url, pool_pre_ping=True)`
  - `services/order-service/order_app/core/resilience.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/order-service/order_app/core/resilience.py:23`: `class CircuitBreaker:`
- Package `services/order-service/order_app/services/`
  - `services/order-service/order_app/services/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `services/order-service/order_app/services/__init__.py:1`: `"""Бизнес-логика order-service."""`
  - `services/order-service/order_app/services/orders.py` — Truy cập dữ liệu (exact) — `services/order-service/order_app/services/orders.py:99`: `result = await session.scalars(select(Order).order_by(Order.id).offset(offset).limit(limit))`
- Package `shared/`
  - `shared/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `shared/__init__.py:5`: `__version__ = "1.0.0"`
  - `shared/context.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `shared/context.py:13`: `_request_id: ContextVar[str] = ContextVar("request_id", default="")`
  - `shared/contracts.py` — Schema API (exact) — `shared/contracts.py:38`: `class ProductCreate(BaseModel):`
  - `shared/errors.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `shared/errors.py:10`: `class AppError(Exception):`
  - `shared/events.py` — Hạ tầng (exact) — `shared/events.py:102`: `return RedisEventBus(aioredis.from_url(redis_url))`
  - `shared/logs.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `shared/logs.py:17`: `class RequestIdFilter(logging.Filter):`
- Package `tests/`
  - `tests/conftest.py` — ngoài phạm vi đọc (test)
  - `tests/test_catalog.py` — ngoài phạm vi đọc (test)
  - `tests/test_contracts.py` — ngoài phạm vi đọc (test)
  - `tests/test_gateway.py` — ngoài phạm vi đọc (test)
  - `tests/test_notifications.py` — ngoài phạm vi đọc (test)
  - `tests/test_orders.py` — ngoài phạm vi đọc (test)
  - `tests/test_resilience.py` — ngoài phạm vi đọc (test)

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
- `ANALYSIS_PARTIAL`: REPAIR_ROUNDS: còn lỗi sau 0 vòng sửa
- `OUT_OF_SCOPE_FILES`: test: 8 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- `CLAIMS_REJECTED`: 18 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
