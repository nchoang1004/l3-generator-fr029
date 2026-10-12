# orderflow — tài liệu API

Bản sinh tự động từ source, chưa được chủ repository duyệt. File này dành cho người đọc; dữ liệu đầy đủ cho máy nằm ở `result.json` và các file ở phụ lục.

| Mục | Giá trị |
|---|---|
| Tình trạng | Chưa đủ — model không gọi công cụ, xem mục 11 |
| Đọc source | 0/57 file trong phạm vi |
| Endpoint | 0 |
| Model | 0 |
| Bảng CSDL | 4 |
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

Mọi bảng thuộc component services.

Dấu \* sau một giá trị: code không khai, giá trị lấy theo mặc định có tài liệu của ORM.

| Bảng | Lớp model | Số cột | Khóa ngoại tới |
|---|---|---|---|
| notifications | Notification | 7 | — |
| order_items | OrderItem | 6 | orders |
| orders | Order | 8 | — |
| products | Product | 6 | — |

### notifications

Lớp `Notification`, khai ở `services/notification-service/notification_app/models.py:11`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| id | int | có | — | không\* | — |
| order_id | int | không\* | — | không\* | index |
| channel | String(32) | không\* | — | không\* | — |
| subject | String(255) | không\* | — | không\* | — |
| body | Text | không\* | — | không\* | — |
| request_id | String(64) | không\* | — | không\* | index |
| created_at | DateTime(timezone=True) | không\* | — | không\* | — |

### order_items

Lớp `OrderItem`, khai ở `services/order-service/order_app/models.py:32`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| id | int | có | — | không\* | — |
| order_id | int | không\* | orders.id | không\* | index, xóa theo: CASCADE |
| product_id | int | không\* | — | không\* | — |
| name | String(255) | không\* | — | không\* | — |
| quantity | int | không\* | — | không\* | — |
| unit_price | Numeric(10, 2) | không\* | — | không\* | — |

### orders

Lớp `Order`, khai ở `services/order-service/order_app/models.py:13`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| id | int | có | — | không\* | — |
| customer | String(255) | không\* | — | không\* | index |
| status | Enum(OrderStatus, name='order_status') | không\* | — | không\* | — |
| degraded | bool | không\* | — | không\* | — |
| warnings | JSON | không\* | — | không\* | — |
| total | Numeric(10, 2) | không\* | — | không\* | — |
| request_id | String(64) | không\* | — | không\* | index |
| created_at | DateTime(timezone=True) | không\* | — | không\* | — |

### products

Lớp `Product`, khai ở `services/catalog-service/catalog_app/models.py:12`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| id | int | có | — | không\* | — |
| sku | String(64) | không\* | — | không\* | unique, index |
| name | String(255) | không\* | — | không\* | — |
| price | Numeric(10, 2) | không\* | — | không\* | — |
| stock | int | không\* | — | không\* | — |
| created_at | DateTime(timezone=True) | không\* | — | không\* | — |

## 5. Sự kiện và tác vụ nền

Không thấy điểm gửi/nhận qua Kafka, FastStream, Celery hay BackgroundTasks. Có kênh sự kiện chưa đọc được, xem mục 11.

## 6. Cấu trúc code

Vai trò của từng file theo dấu hiệu trong code (FR-029). Chỉ liệt kê component thường.

### Gốc

### services

Không có vai trò: chưa xác định vai trò: `services/catalog-service/catalog_app/__init__.py`, `services/catalog-service/catalog_app/api/__init__.py`, `services/catalog-service/catalog_app/api/router.py`, `services/catalog-service/catalog_app/api/routes/__init__.py`, `services/catalog-service/catalog_app/api/routes/products.py`, `services/catalog-service/catalog_app/core/__init__.py`, `services/catalog-service/catalog_app/core/config.py`, `services/catalog-service/catalog_app/core/database.py`, `services/catalog-service/catalog_app/main.py`, `services/catalog-service/catalog_app/models.py`, `services/catalog-service/catalog_app/services/__init__.py`, `services/catalog-service/catalog_app/services/products.py`, `services/gateway/gateway_app/__init__.py`, `services/gateway/gateway_app/api/__init__.py`, `services/gateway/gateway_app/api/router.py`, `services/gateway/gateway_app/api/routes/__init__.py`, `services/gateway/gateway_app/api/routes/proxy.py`, `services/gateway/gateway_app/core/__init__.py`, `services/gateway/gateway_app/core/clients.py`, `services/gateway/gateway_app/core/config.py`, `services/gateway/gateway_app/core/proxy.py`, `services/gateway/gateway_app/main.py`, `services/notification-service/notification_app/__init__.py`, `services/notification-service/notification_app/api/__init__.py`, `services/notification-service/notification_app/api/router.py`, `services/notification-service/notification_app/api/routes/__init__.py`, `services/notification-service/notification_app/api/routes/notifications.py`, `services/notification-service/notification_app/core/__init__.py`, `services/notification-service/notification_app/core/config.py`, `services/notification-service/notification_app/core/database.py`, `services/notification-service/notification_app/main.py`, `services/notification-service/notification_app/models.py`, `services/notification-service/notification_app/services/__init__.py`, `services/notification-service/notification_app/services/notifications.py`, `services/order-service/order_app/__init__.py`, `services/order-service/order_app/api/__init__.py`, `services/order-service/order_app/api/router.py`, `services/order-service/order_app/api/routes/__init__.py`, `services/order-service/order_app/api/routes/orders.py`, `services/order-service/order_app/core/__init__.py`, `services/order-service/order_app/core/catalog_client.py`, `services/order-service/order_app/core/config.py`, `services/order-service/order_app/core/database.py`, `services/order-service/order_app/core/resilience.py`, `services/order-service/order_app/main.py`, `services/order-service/order_app/models.py`, `services/order-service/order_app/services/__init__.py`, `services/order-service/order_app/services/orders.py`.

### shared

Không có vai trò: chưa xác định vai trò: `shared/__init__.py`, `shared/context.py`, `shared/contracts.py`, `shared/errors.py`, `shared/events.py`, `shared/logs.py`.

### Quan hệ giữa component

Đọc tĩnh từ lời gọi, Depends và chỗ dùng bảng đã nối được tới nơi định nghĩa.

| Từ | Tới | Cách dùng | Số chỗ | Ví dụ |
|---|---|---|---|---|
| services | shared | gọi hàm | 28 | `services/notification-service/notification_app/main.py:66` |

## 7. Gọi HTTP ra ngoài

Không có lời gọi nào qua httpx, requests, aiohttp.

## 8. Thư viện

| Thư viện | Phiên bản | Có import trong code | Khai ở |
|---|---|---|---|
| aiosqlite | &gt;=0.20 | chưa thấy import | `requirements.txt:7`, `pyproject.toml:19` |
| asyncpg | &gt;=0.29 | chưa thấy import | `pyproject.toml:22`, `requirements.txt:10` |
| fakeredis | &gt;=2.26 | chưa thấy import | `requirements-dev.txt:4` |
| fastapi | &gt;=0.115 | có | `pyproject.toml:13`, `requirements.txt:1` |
| httpx | &gt;=0.27 | có | `requirements.txt:3`, `pyproject.toml:15` |
| mypy | &gt;=1.10 | chưa thấy import | `requirements-dev.txt:6` |
| pydantic | &gt;=2.7 | có | `pyproject.toml:20`, `requirements.txt:8` |
| pydantic-settings | &gt;=2.3 | có | `pyproject.toml:21`, `requirements.txt:9` |
| pytest | &gt;=8.0 | chưa thấy import | `requirements-dev.txt:1` |
| pytest-asyncio | &gt;=0.23 | chưa thấy import | `requirements-dev.txt:2` |
| pytest-cov | &gt;=5.0 | chưa thấy import | `requirements-dev.txt:3` |
| redis | &gt;=5.0 | có | `pyproject.toml:17`, `requirements.txt:5` |
| ruff | &gt;=0.5 | chưa thấy import | `requirements-dev.txt:5` |
| sqlalchemy | &gt;=2.0 | có | `pyproject.toml:18`, `requirements.txt:6` |
| tenacity | &gt;=8.2 | có | `pyproject.toml:16`, `requirements.txt:4` |
| uvicorn | &gt;=0.30 | chưa thấy import | `pyproject.toml:14`, `requirements.txt:2` |

"Chưa thấy import": tên gói khác tên import, hoặc gói chỉ dùng gián tiếp (driver, plugin, công cụ).

## 9. Cấu hình

| Khóa | Nguồn | Giá trị mặc định | Khai ở |
|---|---|---|---|
| app_name | lớp Settings | OrderFlow Catalog Service | `services/catalog-service/catalog_app/core/config.py:9` |
| app_name | lớp Settings | OrderFlow Gateway | `services/gateway/gateway_app/core/config.py:9` |
| app_name | lớp Settings | OrderFlow Notification Service | `services/notification-service/notification_app/core/config.py:9` |
| app_name | lớp Settings | OrderFlow Order Service | `services/order-service/order_app/core/config.py:9` |
| bus_backend | lớp Settings | redis | `services/notification-service/notification_app/core/config.py:12`, `services/order-service/order_app/core/config.py:12` |
| catalog_failure_threshold | lớp Settings | 3 | `services/order-service/order_app/core/config.py:18` |
| catalog_max_attempts | lớp Settings | 3 | `services/order-service/order_app/core/config.py:17` |
| catalog_recovery_timeout | lớp Settings | 30.0 | `services/order-service/order_app/core/config.py:19` |
| catalog_service_url | lớp Settings | http://localhost:8001 | `services/gateway/gateway_app/core/config.py:11`, `services/order-service/order_app/core/config.py:15` |
| catalog_timeout | lớp Settings | 3.0 | `services/order-service/order_app/core/config.py:16` |
| database_url | lớp Settings | sqlite+aiosqlite:///./catalog.db | `services/catalog-service/catalog_app/core/config.py:10` |
| database_url | lớp Settings | sqlite+aiosqlite:///./notification.db | `services/notification-service/notification_app/core/config.py:10` |
| database_url | lớp Settings | sqlite+aiosqlite:///./order.db | `services/order-service/order_app/core/config.py:10` |
| notification_service_url | lớp Settings | http://localhost:8003 | `services/gateway/gateway_app/core/config.py:13` |
| order_service_url | lớp Settings | http://localhost:8002 | `services/gateway/gateway_app/core/config.py:12` |
| redis_url | lớp Settings | redis://localhost:6379/0 | `services/notification-service/notification_app/core/config.py:13`, `services/order-service/order_app/core/config.py:13` |
| timeout | lớp Settings | 5.0 | `services/gateway/gateway_app/core/config.py:14` |

## 10. Middleware và xử lý lỗi toàn cục

| Loại | Tên | Ở đâu |
|---|---|---|
| xử lý lỗi | `AppError` | `shared/errors.py:34` |
| middleware | `RequestIdMiddleware` | `services/catalog-service/catalog_app/main.py:33` |
| middleware | `RequestIdMiddleware` | `services/gateway/gateway_app/main.py:35` |
| middleware | `RequestIdMiddleware` | `services/notification-service/notification_app/main.py:70` |
| middleware | `RequestIdMiddleware` | `services/order-service/order_app/main.py:66` |

Middleware áp dụng cho mọi request của app. Middleware xác thực chỉ cho biết app đọc thông tin đăng nhập; route có bắt buộc đăng nhập hay không vẫn xem ở cột Auth.

## 11. Chưa biết và giới hạn

- **Loại component được suy từ phạm vi đọc.** Membership không ghi loại component; xếp theo phạm vi đọc (FR-028): tests → test
- **Thư viện hàng đợi chưa hỗ trợ, chưa đọc bên gửi/nhận.** Dùng Redis pub/sub làm kênh sự kiện; chưa trích bên gửi/nhận, tài liệu không liệt kê các sự kiện này: shared/events.py:65, shared/events.py:68
- **Chưa có sơ đồ component.** Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- **Chưa đối chiếu với dữ liệu kiến trúc.** Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- **Phân tích chưa xong.** model không gọi công cụ
- **Có phần source chưa đọc.** pyproject.toml thiếu [[1, 78]]; requirements-dev.txt thiếu [[1, 6]]; requirements.txt thiếu [[1, 10]]; services/catalog-service/catalog_app/__init__.py thiếu [[1, 1]]; services/catalog-service/catalog_app/api/__init__.py thiếu [[1, 1]]; services/catalog-service/catalog_app/api/router.py thiếu [[1, 6]]; services/catalog-service/catalog_app/api/routes/__init__.py thiếu [[1, 1]]; services/catalog-service/catalog_app/api/routes/products.py thiếu [[1, 47]]; services/catalog-service/catalog_app/core/__init__.py thiếu [[1, 1]]; services/catalog-service/catalog_app/core/config.py thiếu [[1, 15]]; services/catalog-service/catalog_app/core/database.py thiếu [[1, 50]]; services/catalog-service/catalog_app/main.py thiếu [[1, 41]]; services/catalog-service/catalog_app/models.py thiếu [[1, 20]]; services/catalog-service/catalog_app/services/__init__.py thiếu [[1, 1]]; services/catalog-service/catalog_app/services/products.py thiếu [[1, 49]]; services/gateway/gateway_app/__init__.py thiếu [[1, 1]]; services/gateway/gateway_app/api/__init__.py thiếu [[1, 1]]; services/gateway/gateway_app/api/router.py thiếu [[1, 6]]; services/gateway/gateway_app/api/routes/__init__.py thiếu [[1, 1]]; services/gateway/gateway_app/api/routes/proxy.py thiếu [[1, 84]]; services/gateway/gateway_app/core/__init__.py thiếu [[1, 1]]; services/gateway/gateway_app/core/clients.py thiếu [[1, 47]]; services/gateway/gateway_app/core/config.py thiếu [[1, 19]]; services/gateway/gateway_app/core/proxy.py thiếu [[1, 35]]; services/gateway/gateway_app/main.py thiếu [[1, 43]]; services/notification-service/notification_app/__init__.py thiếu [[1, 1]]; services/notification-service/notification_app/api/__init__.py thiếu [[1, 1]]; services/notification-service/notification_app/api/router.py thiếu [[1, 6]]; services/notification-service/notification_app/api/routes/__init__.py thiếu [[1, 1]]; services/notification-service/notification_app/api/routes/notifications.py thiếu [[1, 30]]; services/notification-service/notification_app/core/__init__.py thiếu [[1, 1]]; services/notification-service/notification_app/core/config.py thiếu [[1, 18]]; services/notification-service/notification_app/core/database.py thiếu [[1, 50]]; services/notification-service/notification_app/main.py thiếu [[1, 78]]; services/notification-service/notification_app/models.py thiếu [[1, 20]]; services/notification-service/notification_app/services/__init__.py thiếu [[1, 1]]; services/notification-service/notification_app/services/notifications.py thiếu [[1, 71]]; services/order-service/order_app/__init__.py thiếu [[1, 1]]; services/order-service/order_app/api/__init__.py thiếu [[1, 1]]; services/order-service/order_app/api/router.py thiếu [[1, 6]]; services/order-service/order_app/api/routes/__init__.py thiếu [[1, 1]]; services/order-service/order_app/api/routes/orders.py thiếu [[1, 62]]; services/order-service/order_app/core/__init__.py thiếu [[1, 1]]; services/order-service/order_app/core/catalog_client.py thiếu [[1, 105]]; services/order-service/order_app/core/config.py thiếu [[1, 24]]; services/order-service/order_app/core/database.py thiếu [[1, 50]]; services/order-service/order_app/core/resilience.py thiếu [[1, 56]]; services/order-service/order_app/main.py thiếu [[1, 74]]; services/order-service/order_app/models.py thiếu [[1, 42]]; services/order-service/order_app/services/__init__.py thiếu [[1, 1]]; services/order-service/order_app/services/orders.py thiếu [[1, 107]]; shared/__init__.py thiếu [[1, 5]]; shared/context.py thiếu [[1, 55]]; shared/contracts.py thiếu [[1, 123]]; shared/errors.py thiếu [[1, 43]]; shared/events.py thiếu [[1, 103]]; shared/logs.py thiếu [[1, 65]]
- **File ngoài phạm vi đọc.** test: 8 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- **Dòng trông giống route hoặc lời gọi HTTP nhưng chưa được xác nhận, nên không có trong tài liệu.** `services/catalog-service/catalog_app/api/routes/products.py:14`, `services/catalog-service/catalog_app/api/routes/products.py:23`, `services/catalog-service/catalog_app/api/routes/products.py:28`, `services/catalog-service/catalog_app/api/routes/products.py:35`, `services/catalog-service/catalog_app/api/routes/products.py:44`, `services/catalog-service/catalog_app/main.py:37`, `services/gateway/gateway_app/api/routes/proxy.py:20`, `services/gateway/gateway_app/api/routes/proxy.py:27`, `services/gateway/gateway_app/api/routes/proxy.py:34`, `services/gateway/gateway_app/api/routes/proxy.py:41`, `services/gateway/gateway_app/api/routes/proxy.py:48`, `services/gateway/gateway_app/api/routes/proxy.py:58`, `services/gateway/gateway_app/api/routes/proxy.py:65`, `services/gateway/gateway_app/api/routes/proxy.py:70`, `services/gateway/gateway_app/api/routes/proxy.py:80`, `services/gateway/gateway_app/core/proxy.py:25`, `services/gateway/gateway_app/main.py:39`, `services/notification-service/notification_app/api/routes/notifications.py:14`, `services/notification-service/notification_app/api/routes/notifications.py:26`, `services/notification-service/notification_app/main.py:74`, `services/order-service/order_app/api/routes/orders.py:31`, `services/order-service/order_app/api/routes/orders.py:51`, `services/order-service/order_app/api/routes/orders.py:60`, `services/order-service/order_app/core/catalog_client.py:98`, `services/order-service/order_app/main.py:70`

## Phụ lục: file cho máy

- TBL (DDL): [tech-specs/SERVICES/schema/TBL-ORDERFLOW-SERVICES.md](tech-specs/SERVICES/schema/TBL-ORDERFLOW-SERVICES.md) — component services
