# orderflow — tài liệu API

Bản sinh tự động từ source, chưa được chủ repository duyệt. File này dành cho người đọc; dữ liệu đầy đủ cho máy nằm ở `result.json` và các file ở phụ lục.

| Mục | Giá trị |
|---|---|
| Tình trạng | Chưa đủ — còn lỗi sau 0 vòng sửa, xem mục 11 |
| Đọc source | 57/57 file trong phạm vi |
| Endpoint | 7 |
| Model | 5 |
| Bảng CSDL | 4 |
| Sự kiện, tác vụ nền | 0 điểm gửi/nhận |
| Gọi HTTP ra ngoài | 0 |
| Sinh bởi | model scripted, prompt fr029-oneshot-prompt-v6; bảng, sự kiện, thư viện, cấu hình, middleware đọc tĩnh từ code |

Cách đọc nhãn: **chắc chắn** — đọc thẳng từ một dòng code; **suy luận** — theo quy tắc mặc định của framework, lý do ở chú thích [n]; **chưa rõ** — source không đủ để kết luận; **AI viết** — câu chữ do model viết, chỉ để đọc nhanh, không phải dữ kiện đã kiểm.

## 1. Danh sách endpoint

| # | Method | Path | Vào | Ra | Status | Auth |
|---|---|---|---|---|---|---|
| 1 | GET | /api/v1/notifications | — | list[NotificationRead] | 200 | chưa rõ |
| 2 | GET | /api/v1/orders | — | list[OrderRead] | 200 | chưa rõ |
| 3 | GET | /api/v1/products | — | list[ProductRead] | 200 | chưa rõ |
| 4 | GET | /health | — | HealthResponse | 200 | chưa rõ |
| 5 | GET | /health | — | HealthResponse | 200 | chưa rõ |
| 6 | GET | /health | — | HealthResponse | 200 | chưa rõ |
| 7 | GET | /health | — | HealthResponse | 200 | chưa rõ |

## 2. Chi tiết từng endpoint

### 1. GET /api/v1/notifications

- Mô tả (AI viết): Liệt kê thông báo của một đơn hàng theo order_id.
- Hàm xử lý: `list_notifications` tại `services/notification-service/notification_app/api/routes/notifications.py:14`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | order_id | query | integer | có |
  | offset | query | integer | không |
  | limit | query | integer | không |

- Trả về: list[NotificationRead]
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_session
- Auth: chưa rõ — Mã nguồn không khai cơ chế xác thực nào cho route này
- Nhóm (tags): notifications
- Mức chắc chắn: suy luận [1][2]
- Còn thiếu: Trường chưa xác định: auth

### 2. GET /api/v1/orders

- Mô tả (AI viết): Liệt kê đơn hàng theo offset và limit.
- Hàm xử lý: `list_orders` tại `services/order-service/order_app/api/routes/orders.py:51`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | offset | query | integer | không |
  | limit | query | integer | không |

- Trả về: list[OrderRead]
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_session
- Auth: chưa rõ — Mã nguồn không khai cơ chế xác thực nào cho route này
- Nhóm (tags): orders
- Mức chắc chắn: suy luận [1]
- Còn thiếu: Trường chưa xác định: auth

### 3. GET /api/v1/products

- Mô tả (AI viết): Liệt kê sản phẩm trong danh mục theo offset và limit.
- Hàm xử lý: `list_products` tại `services/catalog-service/catalog_app/api/routes/products.py:14`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | offset | query | integer | không |
  | limit | query | integer | không |

- Trả về: list[ProductRead]
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_session
- Auth: chưa rõ — Mã nguồn không khai cơ chế xác thực nào cho route này
- Nhóm (tags): products
- Mức chắc chắn: suy luận [1]
- Còn thiếu: Trường chưa xác định: auth

### 4. GET /health

- Mô tả (AI viết): Kiểm tra tình trạng hoạt động của order-service.
- Hàm xử lý: `health` tại `services/order-service/order_app/main.py:70`
- Tham số: không có
- Trả về: HealthResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: không có
- Auth: chưa rõ — Mã nguồn không khai cơ chế xác thực nào cho route này
- Nhóm (tags): health
- Mức chắc chắn: suy luận [1]
- Còn thiếu: Trường chưa xác định: auth

### 5. GET /health

- Mô tả (AI viết): Kiểm tra tình trạng hoạt động của catalog-service.
- Hàm xử lý: `health` tại `services/catalog-service/catalog_app/main.py:37`
- Tham số: không có
- Trả về: HealthResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: không có
- Auth: chưa rõ — Mã nguồn không khai cơ chế xác thực nào cho route này
- Nhóm (tags): health
- Mức chắc chắn: suy luận [1]
- Còn thiếu: Trường chưa xác định: auth

### 6. GET /health

- Mô tả (AI viết): Kiểm tra tình trạng hoạt động của notification-service.
- Hàm xử lý: `health` tại `services/notification-service/notification_app/main.py:74`
- Tham số: không có
- Trả về: HealthResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: không có
- Auth: chưa rõ — Mã nguồn không khai cơ chế xác thực nào cho route này
- Nhóm (tags): health
- Mức chắc chắn: suy luận [1]
- Còn thiếu: Trường chưa xác định: auth

### 7. GET /health

- Mô tả (AI viết): Kiểm tra tình trạng hoạt động của gateway.
- Hàm xử lý: `health` tại `services/gateway/gateway_app/main.py:39`
- Tham số: không có
- Trả về: HealthResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: không có
- Auth: chưa rõ — Mã nguồn không khai cơ chế xác thực nào cho route này
- Nhóm (tags): health
- Mức chắc chắn: suy luận [1]
- Còn thiếu: Trường chưa xác định: auth

Chú thích:

[1] Decorator không khai status_code; FastAPI dùng status mặc định 200 của JSONResponse  
[2] Tham số kiểu đơn, không có trong path, không khai Query/Header/Cookie; FastAPI coi là query  

## 3. Model dữ liệu

### HealthResponse

Khai ở `shared/contracts.py:33`. Mức chắc chắn: suy luận [1][2].

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| status | string | không | không |
| service | string | có | không |

### NotificationRead

Khai ở `shared/contracts.py:100`. Mức chắc chắn: suy luận [1].

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| id | integer | có | không |
| order_id | integer | có | không |
| channel | string | có | không |
| subject | string | có | không |
| body | string | có | không |
| request_id | string | có | không |
| created_at | string(date-time) | có | không |

### OrderItemRead

Khai ở `shared/contracts.py:71`. Mức chắc chắn: suy luận [1].

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| product_id | integer | có | không |
| name | string | có | không |
| quantity | integer | có | không |
| unit_price | number | có | không |

### OrderRead

Khai ở `shared/contracts.py:86`. Mức chắc chắn: suy luận [1][2].

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| id | integer | có | không |
| customer | string | có | không |
| status | string | có | không |
| degraded | boolean | có | không |
| warnings | list[string] | có | không |
| total | number | có | không |
| items | list[OrderItemRead] | có | không |
| request_id | string | có | không |
| created_at | string(date-time) | có | không |

### ProductRead

Khai ở `shared/contracts.py:55`. Mức chắc chắn: suy luận [1].

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| sku | string | có | không |
| name | string | có | không |
| price | number | có | không |
| stock | integer | không | không |
| id | integer | có | không |

Chú thích:

[1] Pydantic v2: trường không có default là bắt buộc, kể cả khi kiểu cho phép None  
[2] Bộ kiểm chưa đối chiếu được kiểu/required/nullable với khai báo của: status  

## 4. Bảng CSDL

### notifications

Khai ở `services/notification-service/notification_app/models.py:11`, component Toàn bộ. SQL dialect: chưa rõ (Không có Base.metadata.create_all(engine) nối base này với một engine có URL literal). Mức chắc chắn: suy luận [1][2][3].

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null |
|---|---|---|---|---|
| id | int (chưa quy ra kiểu SQL) | có | — | không |
| order_id | int (chưa quy ra kiểu SQL) | không | — | không |
| channel | String(32) (chưa quy ra kiểu SQL) | không | — | không |
| subject | String(255) (chưa quy ra kiểu SQL) | không | — | không |
| body | Text (chưa quy ra kiểu SQL) | không | — | không |
| request_id | String(64) (chưa quy ra kiểu SQL) | không | — | không |
| created_at | DateTime(timezone=True) (chưa quy ra kiểu SQL) | không | — | không |

### order_items

Khai ở `services/order-service/order_app/models.py:32`, component Toàn bộ. SQL dialect: chưa rõ (Không có Base.metadata.create_all(engine) nối base này với một engine có URL literal). Mức chắc chắn: suy luận [1][2][3].

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null |
|---|---|---|---|---|
| id | int (chưa quy ra kiểu SQL) | có | — | không |
| order_id | int (chưa quy ra kiểu SQL) | không | {'table': 'orders', 'column': 'id'} | không |
| product_id | int (chưa quy ra kiểu SQL) | không | — | không |
| name | String(255) (chưa quy ra kiểu SQL) | không | — | không |
| quantity | int (chưa quy ra kiểu SQL) | không | — | không |
| unit_price | Numeric(10, 2) (chưa quy ra kiểu SQL) | không | — | không |

### orders

Khai ở `services/order-service/order_app/models.py:13`, component Toàn bộ. SQL dialect: chưa rõ (Không có Base.metadata.create_all(engine) nối base này với một engine có URL literal). Mức chắc chắn: suy luận [1][2][3].

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null |
|---|---|---|---|---|
| id | int (chưa quy ra kiểu SQL) | có | — | không |
| customer | String(255) (chưa quy ra kiểu SQL) | không | — | không |
| status | Enum(OrderStatus, name='order_status') (chưa quy ra kiểu SQL) | không | — | không |
| degraded | bool (chưa quy ra kiểu SQL) | không | — | không |
| warnings | JSON (chưa quy ra kiểu SQL) | không | — | không |
| total | Numeric(10, 2) (chưa quy ra kiểu SQL) | không | — | không |
| request_id | String(64) (chưa quy ra kiểu SQL) | không | — | không |
| created_at | DateTime(timezone=True) (chưa quy ra kiểu SQL) | không | — | không |

### products

Khai ở `services/catalog-service/catalog_app/models.py:12`, component Toàn bộ. SQL dialect: chưa rõ (Không có Base.metadata.create_all(engine) nối base này với một engine có URL literal). Mức chắc chắn: suy luận [1][2][3].

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null |
|---|---|---|---|---|
| id | int (chưa quy ra kiểu SQL) | có | — | không |
| sku | String(64) (chưa quy ra kiểu SQL) | không | — | không |
| name | String(255) (chưa quy ra kiểu SQL) | không | — | không |
| price | Numeric(10, 2) (chưa quy ra kiểu SQL) | không | — | không |
| stock | int (chưa quy ra kiểu SQL) | không | — | không |
| created_at | DateTime(timezone=True) (chưa quy ra kiểu SQL) | không | — | không |

Chú thích:

[1] không khai primary_key thì là False  
[2] nullable mặc định là not primary_key  
[3] với Mapped/SQLModel theo Optional  

## 5. Sự kiện và tác vụ nền

Không thấy điểm gửi/nhận qua Kafka, FastStream, Celery hay BackgroundTasks.

## 6. Cấu trúc code

Vai trò của từng file theo dấu hiệu trong code (FR-029). Chỉ liệt kê component thường.

### Toàn bộ

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `services/catalog-service/catalog_app/__init__.py` | Khác | `services/catalog-service/catalog_app/__init__.py:1` |
| `services/catalog-service/catalog_app/api/__init__.py` | Khác | `services/catalog-service/catalog_app/api/__init__.py:1` |
| `services/catalog-service/catalog_app/api/router.py` | Khác | `services/catalog-service/catalog_app/api/router.py:5` |
| `services/catalog-service/catalog_app/api/routes/__init__.py` | Khác | `services/catalog-service/catalog_app/api/routes/__init__.py:1` |
| `services/catalog-service/catalog_app/api/routes/products.py` | Route | `services/catalog-service/catalog_app/api/routes/products.py:14` |
| `services/catalog-service/catalog_app/core/__init__.py` | Khác | `services/catalog-service/catalog_app/core/__init__.py:1` |
| `services/catalog-service/catalog_app/core/config.py` | Cấu hình | `services/catalog-service/catalog_app/core/config.py:6` |
| `services/catalog-service/catalog_app/core/database.py` | Hạ tầng | `services/catalog-service/catalog_app/core/database.py:28` |
| `services/catalog-service/catalog_app/main.py` | Điểm vào | `services/catalog-service/catalog_app/main.py:29` |
| `services/catalog-service/catalog_app/models.py` | Model bảng | `services/catalog-service/catalog_app/models.py:13` |
| `services/catalog-service/catalog_app/services/__init__.py` | Khác | `services/catalog-service/catalog_app/services/__init__.py:1` |
| `services/catalog-service/catalog_app/services/products.py` | Truy cập dữ liệu | `services/catalog-service/catalog_app/services/products.py:14` |
| `services/gateway/gateway_app/__init__.py` | Khác | `services/gateway/gateway_app/__init__.py:1` |
| `services/gateway/gateway_app/api/__init__.py` | Khác | `services/gateway/gateway_app/api/__init__.py:1` |
| `services/gateway/gateway_app/api/router.py` | Khác | `services/gateway/gateway_app/api/router.py:5` |
| `services/gateway/gateway_app/api/routes/__init__.py` | Khác | `services/gateway/gateway_app/api/routes/__init__.py:1` |
| `services/gateway/gateway_app/api/routes/proxy.py` | Route | `services/gateway/gateway_app/api/routes/proxy.py:20` |
| `services/gateway/gateway_app/core/__init__.py` | Khác | `services/gateway/gateway_app/core/__init__.py:1` |
| `services/gateway/gateway_app/core/clients.py` | Hạ tầng | `services/gateway/gateway_app/core/clients.py:25` |
| `services/gateway/gateway_app/core/config.py` | Cấu hình | `services/gateway/gateway_app/core/config.py:6` |
| `services/gateway/gateway_app/core/proxy.py` | Hạ tầng | `services/gateway/gateway_app/core/proxy.py:25` |
| `services/gateway/gateway_app/main.py` | Điểm vào | `services/gateway/gateway_app/main.py:33` |
| `services/notification-service/notification_app/__init__.py` | Khác | `services/notification-service/notification_app/__init__.py:1` |
| `services/notification-service/notification_app/api/__init__.py` | Khác | `services/notification-service/notification_app/api/__init__.py:1` |
| `services/notification-service/notification_app/api/router.py` | Khác | `services/notification-service/notification_app/api/router.py:5` |
| `services/notification-service/notification_app/api/routes/__init__.py` | Khác | `services/notification-service/notification_app/api/routes/__init__.py:1` |
| `services/notification-service/notification_app/api/routes/notifications.py` | Route | `services/notification-service/notification_app/api/routes/notifications.py:14` |
| `services/notification-service/notification_app/core/__init__.py` | Khác | `services/notification-service/notification_app/core/__init__.py:1` |
| `services/notification-service/notification_app/core/config.py` | Cấu hình | `services/notification-service/notification_app/core/config.py:6` |
| `services/notification-service/notification_app/core/database.py` | Hạ tầng | `services/notification-service/notification_app/core/database.py:28` |
| `services/notification-service/notification_app/main.py` | Điểm vào | `services/notification-service/notification_app/main.py:59` |
| `services/notification-service/notification_app/models.py` | Model bảng | `services/notification-service/notification_app/models.py:12` |
| `services/notification-service/notification_app/services/__init__.py` | Khác | `services/notification-service/notification_app/services/__init__.py:1` |
| `services/notification-service/notification_app/services/notifications.py` | Truy cập dữ liệu | `services/notification-service/notification_app/services/notifications.py:19` |
| `services/order-service/order_app/__init__.py` | Khác | `services/order-service/order_app/__init__.py:1` |
| `services/order-service/order_app/api/__init__.py` | Khác | `services/order-service/order_app/api/__init__.py:1` |
| `services/order-service/order_app/api/router.py` | Khác | `services/order-service/order_app/api/router.py:5` |
| `services/order-service/order_app/api/routes/__init__.py` | Khác | `services/order-service/order_app/api/routes/__init__.py:1` |
| `services/order-service/order_app/api/routes/orders.py` | Route | `services/order-service/order_app/api/routes/orders.py:31` |
| `services/order-service/order_app/core/__init__.py` | Khác | `services/order-service/order_app/core/__init__.py:1` |
| `services/order-service/order_app/core/catalog_client.py` | Hạ tầng | `services/order-service/order_app/core/catalog_client.py:98` |
| `services/order-service/order_app/core/config.py` | Cấu hình | `services/order-service/order_app/core/config.py:6` |
| `services/order-service/order_app/core/database.py` | Hạ tầng | `services/order-service/order_app/core/database.py:28` |
| `services/order-service/order_app/core/resilience.py` | Khác | `services/order-service/order_app/core/resilience.py:23` |
| `services/order-service/order_app/main.py` | Điểm vào | `services/order-service/order_app/main.py:42` |
| `services/order-service/order_app/models.py` | Model bảng | `services/order-service/order_app/models.py:14` |
| `services/order-service/order_app/services/__init__.py` | Khác | `services/order-service/order_app/services/__init__.py:1` |
| `services/order-service/order_app/services/orders.py` | Truy cập dữ liệu | `services/order-service/order_app/services/orders.py:99` |
| `shared/__init__.py` | Khác | `shared/__init__.py:5` |
| `shared/context.py` | Khác | `shared/context.py:13` |
| `shared/contracts.py` | Schema API | `shared/contracts.py:38` |
| `shared/errors.py` | Khác | `shared/errors.py:10` |
| `shared/events.py` | Hạ tầng | `shared/events.py:102` |
| `shared/logs.py` | Khác | `shared/logs.py:17` |

## 7. Gọi HTTP ra ngoài

Không có lời gọi nào qua httpx, requests, aiohttp.

## 8. Thư viện

| Thư viện | Phiên bản | Có import trong code | Khai ở |
|---|---|---|---|
| aiosqlite | &gt;=0.20 | chưa thấy import | `requirements.txt:7` |
| aiosqlite | &gt;=0.20 | chưa thấy import | `pyproject.toml:19` |
| asyncpg | &gt;=0.29 | chưa thấy import | `pyproject.toml:22` |
| asyncpg | &gt;=0.29 | chưa thấy import | `requirements.txt:10` |
| fakeredis | &gt;=2.26 | chưa thấy import | `requirements-dev.txt:4` |
| fastapi | &gt;=0.115 | có | `pyproject.toml:13` |
| fastapi | &gt;=0.115 | có | `requirements.txt:1` |
| httpx | &gt;=0.27 | có | `requirements.txt:3` |
| httpx | &gt;=0.27 | có | `pyproject.toml:15` |
| mypy | &gt;=1.10 | chưa thấy import | `requirements-dev.txt:6` |
| pydantic | &gt;=2.7 | có | `pyproject.toml:20` |
| pydantic | &gt;=2.7 | có | `requirements.txt:8` |
| pydantic-settings | &gt;=2.3 | có | `pyproject.toml:21` |
| pydantic-settings | &gt;=2.3 | có | `requirements.txt:9` |
| pytest | &gt;=8.0 | chưa thấy import | `requirements-dev.txt:1` |
| pytest-asyncio | &gt;=0.23 | chưa thấy import | `requirements-dev.txt:2` |
| pytest-cov | &gt;=5.0 | chưa thấy import | `requirements-dev.txt:3` |
| redis | &gt;=5.0 | có | `pyproject.toml:17` |
| redis | &gt;=5.0 | có | `requirements.txt:5` |
| ruff | &gt;=0.5 | chưa thấy import | `requirements-dev.txt:5` |
| sqlalchemy | &gt;=2.0 | có | `pyproject.toml:18` |
| sqlalchemy | &gt;=2.0 | có | `requirements.txt:6` |
| tenacity | &gt;=8.2 | có | `pyproject.toml:16` |
| tenacity | &gt;=8.2 | có | `requirements.txt:4` |
| uvicorn | &gt;=0.30 | chưa thấy import | `pyproject.toml:14` |
| uvicorn | &gt;=0.30 | chưa thấy import | `requirements.txt:2` |

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

- **Chưa có sơ đồ component.** Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- **Chưa đối chiếu với dữ liệu kiến trúc.** Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- **Phân tích chưa xong.** còn lỗi sau 0 vòng sửa
- **File ngoài phạm vi đọc.** test: 8 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- **Có đề xuất của model bị bộ kiểm từ chối.** 18 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
- **Dòng trông giống route hoặc lời gọi HTTP nhưng chưa được xác nhận, nên không có trong tài liệu.** `services/catalog-service/catalog_app/api/routes/products.py:23`, `services/catalog-service/catalog_app/api/routes/products.py:28`, `services/catalog-service/catalog_app/api/routes/products.py:35`, `services/catalog-service/catalog_app/api/routes/products.py:44`, `services/gateway/gateway_app/api/routes/proxy.py:20`, `services/gateway/gateway_app/api/routes/proxy.py:27`, `services/gateway/gateway_app/api/routes/proxy.py:34`, `services/gateway/gateway_app/api/routes/proxy.py:41`, `services/gateway/gateway_app/api/routes/proxy.py:48`, `services/gateway/gateway_app/api/routes/proxy.py:58`, `services/gateway/gateway_app/api/routes/proxy.py:65`, `services/gateway/gateway_app/api/routes/proxy.py:70`, `services/gateway/gateway_app/api/routes/proxy.py:80`, `services/gateway/gateway_app/core/proxy.py:25`, `services/notification-service/notification_app/api/routes/notifications.py:26`, `services/order-service/order_app/api/routes/orders.py:31`, `services/order-service/order_app/api/routes/orders.py:60`, `services/order-service/order_app/core/catalog_client.py:98`

## Phụ lục: file cho máy

- API (OpenAPI): [tech-specs/TOAN-BO/api/API-ORDERFLOW-TOAN-BO-v1.md](tech-specs/TOAN-BO/api/API-ORDERFLOW-TOAN-BO-v1.md) — component Toàn bộ
- TBL (DDL): [tech-specs/TOAN-BO/schema/TBL-ORDERFLOW-TOAN-BO.md](tech-specs/TOAN-BO/schema/TBL-ORDERFLOW-TOAN-BO.md) — component Toàn bộ
