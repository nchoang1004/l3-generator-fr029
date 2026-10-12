# kibo — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:229c9a746a0b5cc8bd99c7c06529a1a4ebcfd8a4b8fec654a03811edd747a904`
- Trạng thái phân tích: partial — MODEL_ERROR: HTTP 429 credit_balance_exhausted
- Độ phủ đọc source: chưa đủ, xem Giới hạn

## Mục lục contract

- API: [tech-specs/KHOI-DONG/api/API-KIBO-KHOI-DONG-v1.md](tech-specs/KHOI-DONG/api/API-KIBO-KHOI-DONG-v1.md) — component Khởi động
- API: [tech-specs/API/api/API-KIBO-API-v1.md](tech-specs/API/api/API-KIBO-API-v1.md) — component API

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### API

- Package `app/api/v1/`
  - `app/api/v1/test.py` — Route (exact) — `app/api/v1/test.py:24`: `@router.get("/trigger-reminder/{appointment_id}")`
- Package `app/api/v1/appointments/`
  - `app/api/v1/appointments/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/api/v1/appointments/__init__.py:1`: `from app.api.v1.appointments.router import router`
  - `app/api/v1/appointments/router.py` — Route (exact) — `app/api/v1/appointments/router.py:25`: `@router.post("", status_code=status.HTTP_201_CREATED)`
- Package `app/api/v1/auth/`
  - `app/api/v1/auth/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/api/v1/auth/__init__.py:1`: `from app.api.v1.auth.router import router`
  - `app/api/v1/auth/router.py` — Route (exact) — `app/api/v1/auth/router.py:26`: `@router.get("/me", response_model=CurrentSessionResponse)`
- Package `app/api/v1/clients/`
  - `app/api/v1/clients/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/api/v1/clients/__init__.py:1`: `from app.api.v1.clients.router import router`
  - `app/api/v1/clients/router.py` — Route (exact) — `app/api/v1/clients/router.py:16`: `@router.post("", status_code=status.HTTP_201_CREATED)`
- Package `app/api/v1/services/`
  - `app/api/v1/services/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/api/v1/services/__init__.py:1`: `from app.api.v1.services.router import router`
  - `app/api/v1/services/router.py` — Route (exact) — `app/api/v1/services/router.py:16`: `@router.post("", status_code=status.HTTP_201_CREATED)`
- Package `app/api/v1/super_admin/`
  - `app/api/v1/super_admin/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/api/v1/super_admin/__init__.py:1`: `from app.api.v1.super_admin.router import router`
  - `app/api/v1/super_admin/router.py` — Route (exact) — `app/api/v1/super_admin/router.py:13`: `@router.post("", status_code=status.HTTP_201_CREATED)`
- Package `app/api/v1/tenant/`
  - `app/api/v1/tenant/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/api/v1/tenant/__init__.py:1`: `from app.api.v1.tenant.payments_router import router as payments_router`
  - `app/api/v1/tenant/payments_router.py` — Route (exact) — `app/api/v1/tenant/payments_router.py:15`: `@router.post("", status_code=status.HTTP_201_CREATED)`
  - `app/api/v1/tenant/router.py` — Route (exact) — `app/api/v1/tenant/router.py:24`: `@router.post("", status_code=status.HTTP_201_CREATED)`
- Package `app/api/v1/users/`
  - `app/api/v1/users/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/api/v1/users/__init__.py:1`: `from app.api.v1.users.router import router`
  - `app/api/v1/users/router.py` — Route (exact) — `app/api/v1/users/router.py:22`: `@router.post("", status_code=status.HTTP_201_CREATED)`
- Package `app/api/v1/waitlists/`
  - `app/api/v1/waitlists/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/api/v1/waitlists/__init__.py:1`: `from app.api.v1.waitlists.router import router`
  - `app/api/v1/waitlists/router.py` — Route (exact) — `app/api/v1/waitlists/router.py:18`: `@router.post("", response_model=WaitlistResponse, status_code=status.HTTP_201_CREATED)`
- Package `app/api/v1/whatsapp/`
  - `app/api/v1/whatsapp/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/api/v1/whatsapp/__init__.py:1`: `from app.api.v1.whatsapp.router import router`
  - `app/api/v1/whatsapp/router.py` — Route (exact) — `app/api/v1/whatsapp/router.py:291`: `@router.get("/messaging/outbox/stats", response_model=OutboxStatsResponse)`

### Cơ sở dữ liệu

- Package `app/db/`
  - `app/db/base.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/db/base.py:4`: `class Base(DeclarativeBase):`
  - `app/db/schemas.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/db/schemas.py:5`: `raw = getenv(name, default)`
  - `app/db/session.py` — Hạ tầng (exact) — `app/db/session.py:10`: `engine = create_engine(settings.DATABASE_URL, future=True, pool_pre_ping=True)`

### Dữ liệu mẫu

- Package `app/seeds/`
  - `app/seeds/create_frontend_test_users.py` — vai trò unknown: agent chưa xác định

### Khởi động

- Package `app/`
  - `app/main.py` — Điểm vào (exact) — `app/main.py:50`: `app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)`

### Lõi

- Package `app/core/`
  - `app/core/config.py` — vai trò unknown: agent chưa xác định
  - `app/core/dependencies.py` — Truy cập dữ liệu (exact) — `app/core/dependencies.py:151`: `user = db.query(User).filter(User.id == user_id, User.tenant_id == tenant_id, User.is_active.is_(True)).first()`
  - `app/core/email.py` — Hạ tầng (exact) — `app/core/email.py:29`: `with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:`
  - `app/core/security.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/core/security.py:13`: `def verify_password(plain_password: str, hashed_password: str) -> bool:`
  - `app/core/timezone.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/core/timezone.py:17`: `def now_for_timezone(timezone_identifier: str \| None) -> datetime:`

### Model bảng

- Package `app/models/`
  - `app/models/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/models/__init__.py:1`: `from app.models.appointments import Appointment, AppointmentStatus`
- Package `app/models/appointments/`
  - `app/models/appointments/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/models/appointments/__init__.py:1`: `from app.models.appointments.appointment import Appointment, AppointmentStatus`
  - `app/models/appointments/appointment.py` — Model bảng (exact) — `app/models/appointments/appointment.py:23`: `__tablename__ = "appointments"`
- Package `app/models/auth/`
  - `app/models/auth/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/models/auth/__init__.py:1`: `from app.models.auth.user import User, UserRole`
  - `app/models/auth/user.py` — Model bảng (exact) — `app/models/auth/user.py:20`: `__tablename__ = "users"`
- Package `app/models/clients/`
  - `app/models/clients/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/models/clients/__init__.py:1`: `from app.models.clients.client import Client`
  - `app/models/clients/client.py` — Model bảng (exact) — `app/models/clients/client.py:12`: `__tablename__ = "clients"`
- Package `app/models/conversation_contexts/`
  - `app/models/conversation_contexts/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/models/conversation_contexts/__init__.py:1`: `from app.models.conversation_contexts.conversation_context import ConversationContext`
  - `app/models/conversation_contexts/conversation_context.py` — Model bảng (exact) — `app/models/conversation_contexts/conversation_context.py:13`: `__tablename__ = "conversation_contexts"`
- Package `app/models/services/`
  - `app/models/services/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/models/services/__init__.py:1`: `from app.models.services.service import Service`
  - `app/models/services/service.py` — Model bảng (exact) — `app/models/services/service.py:13`: `__tablename__ = "services"`
- Package `app/models/super_admin/`
  - `app/models/super_admin/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/models/super_admin/__init__.py:1`: `from app.models.super_admin.super_admin import SuperAdmin`
  - `app/models/super_admin/super_admin.py` — Model bảng (exact) — `app/models/super_admin/super_admin.py:12`: `__tablename__ = "super_admins"`
- Package `app/models/tenant/`
  - `app/models/tenant/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/models/tenant/__init__.py:1`: `from app.models.tenant.tenant import PlanTier, SubscriptionStatus, Tenant, max_users_for_plan`
  - `app/models/tenant/tenant.py` — Model bảng (exact) — `app/models/tenant/tenant.py:87`: `__tablename__ = "tenants"`
  - `app/models/tenant/tenant_config.py` — Model bảng (exact) — `app/models/tenant/tenant_config.py:11`: `__tablename__ = "tenant_configs"`
  - `app/models/tenant/tenant_payment.py` — Model bảng (exact) — `app/models/tenant/tenant_payment.py:13`: `__tablename__ = "tenant_payments"`
- Package `app/models/waitlists/`
  - `app/models/waitlists/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/models/waitlists/__init__.py:1`: `from app.models.waitlists.waitlist import Waitlist`
  - `app/models/waitlists/waitlist.py` — Model bảng (exact) — `app/models/waitlists/waitlist.py:12`: `__tablename__ = "waitlists"`
- Package `app/models/whatsapp_events/`
  - `app/models/whatsapp_events/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/models/whatsapp_events/__init__.py:1`: `from app.models.whatsapp_events.processed_webhook import ProcessedWebhook`
  - `app/models/whatsapp_events/processed_webhook.py` — Model bảng (exact) — `app/models/whatsapp_events/processed_webhook.py:13`: `__tablename__ = "processed_webhooks"`
- Package `app/models/whatsapp_outbox/`
  - `app/models/whatsapp_outbox/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/models/whatsapp_outbox/__init__.py:1`: `from app.models.whatsapp_outbox.whatsapp_outbox import WhatsAppOutbox`
  - `app/models/whatsapp_outbox/whatsapp_outbox.py` — Model bảng (exact) — `app/models/whatsapp_outbox/whatsapp_outbox.py:13`: `__tablename__ = "whatsapp_outbox"`
- Package `app/models/whatsapp_sessions/`
  - `app/models/whatsapp_sessions/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/models/whatsapp_sessions/__init__.py:1`: `from app.models.whatsapp_sessions.whatsapp_session import WhatsAppSession`
  - `app/models/whatsapp_sessions/whatsapp_session.py` — Model bảng (exact) — `app/models/whatsapp_sessions/whatsapp_session.py:13`: `__tablename__ = "whatsapp_sessions"`

### Schema API

- Package `app/schemas/appointments/`
  - `app/schemas/appointments/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/schemas/appointments/__init__.py:1`: `from app.schemas.appointments.appointment import (`
  - `app/schemas/appointments/appointment.py` — Schema API (exact) — `app/schemas/appointments/appointment.py:9`: `class AppointmentCreate(BaseModel):`
- Package `app/schemas/auth/`
  - `app/schemas/auth/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/schemas/auth/__init__.py:1`: `from app.schemas.auth.auth import (`
  - `app/schemas/auth/auth.py` — Schema API (exact) — `app/schemas/auth/auth.py:10`: `class UserLoginRequest(BaseModel):`
- Package `app/schemas/clients/`
  - `app/schemas/clients/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/schemas/clients/__init__.py:1`: `from app.schemas.clients.client import ClientCreate, ClientResponse, ClientUpdate`
  - `app/schemas/clients/client.py` — Schema API (exact) — `app/schemas/clients/client.py:7`: `class ClientCreate(BaseModel):`
- Package `app/schemas/services/`
  - `app/schemas/services/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/schemas/services/__init__.py:1`: `from app.schemas.services.service import ServiceCreate, ServiceResponse, ServiceUpdate`
  - `app/schemas/services/service.py` — Schema API (exact) — `app/schemas/services/service.py:8`: `class ServiceCreate(BaseModel):`
- Package `app/schemas/super_admin/`
  - `app/schemas/super_admin/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/schemas/super_admin/__init__.py:1`: `from app.schemas.super_admin.super_admin import SuperAdminCreate, SuperAdminResponse`
  - `app/schemas/super_admin/super_admin.py` — Schema API (exact) — `app/schemas/super_admin/super_admin.py:7`: `class SuperAdminCreate(BaseModel):`
- Package `app/schemas/tenant/`
  - `app/schemas/tenant/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/schemas/tenant/__init__.py:1`: `from app.schemas.tenant.tenant import (`
  - `app/schemas/tenant/tenant.py` — Schema API (exact) — `app/schemas/tenant/tenant.py:10`: `class TenantCreate(BaseModel):`
  - `app/schemas/tenant/tenant_payment.py` — Schema API (exact) — `app/schemas/tenant/tenant_payment.py:8`: `class PaymentCreate(BaseModel):`
- Package `app/schemas/users/`
  - `app/schemas/users/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/schemas/users/__init__.py:1`: `from app.schemas.users.user import (`
  - `app/schemas/users/user.py` — Schema API (exact) — `app/schemas/users/user.py:9`: `class UserCreate(BaseModel):`
- Package `app/schemas/waitlists/`
  - `app/schemas/waitlists/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/schemas/waitlists/__init__.py:1`: `from app.schemas.waitlists.waitlist import WaitlistCreate, WaitlistResponse`
  - `app/schemas/waitlists/waitlist.py` — Schema API (exact) — `app/schemas/waitlists/waitlist.py:7`: `class WaitlistCreate(BaseModel):`
- Package `app/schemas/whatsapp/`
  - `app/schemas/whatsapp/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/schemas/whatsapp/__init__.py:1`: `from app.schemas.whatsapp.whatsapp import (`
  - `app/schemas/whatsapp/whatsapp.py` — Schema API (exact) — `app/schemas/whatsapp/whatsapp.py:7`: `class OutboxEnqueueRequest(BaseModel):`

### Script

- Package `app/scripts/`
  - `app/scripts/send_tomorrow_reminders.py` — vai trò unknown: agent chưa xác định

### Service

- Package `app/services/appointments/`
  - `app/services/appointments/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/services/appointments/appointment_service.py` — vai trò unknown: agent chưa xác định
- Package `app/services/auth/`
  - `app/services/auth/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/services/auth/auth_service.py` — vai trò unknown: agent chưa xác định
- Package `app/services/clients/`
  - `app/services/clients/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/services/clients/client_service.py` — vai trò unknown: agent chưa xác định
- Package `app/services/scheduler/`
  - `app/services/scheduler/reminder_scheduler.py` — vai trò unknown: agent chưa xác định
  - `app/services/scheduler/worker.py` — vai trò unknown: agent chưa xác định
- Package `app/services/services/`
  - `app/services/services/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/services/services/service_service.py` — vai trò unknown: agent chưa xác định
- Package `app/services/super_admin/`
  - `app/services/super_admin/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/services/super_admin/super_admin_service.py` — vai trò unknown: agent chưa xác định
- Package `app/services/tenant/`
  - `app/services/tenant/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/services/tenant/tenant_payment_service.py` — vai trò unknown: agent chưa xác định
  - `app/services/tenant/tenant_service.py` — vai trò unknown: agent chưa xác định
- Package `app/services/users/`
  - `app/services/users/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/services/users/user_service.py` — vai trò unknown: agent chưa xác định
- Package `app/services/waitlists/`
  - `app/services/waitlists/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/services/waitlists/waitlist_service.py` — vai trò unknown: agent chưa xác định
- Package `app/services/whatsapp/`
  - `app/services/whatsapp/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/services/whatsapp/connection_service.py` — vai trò unknown: agent chưa xác định
  - `app/services/whatsapp/evolution_client.py` — vai trò unknown: agent chưa xác định
  - `app/services/whatsapp/outbox_service.py` — vai trò unknown: agent chưa xác định
  - `app/services/whatsapp/template_engine.py` — vai trò unknown: agent chưa xác định
  - `app/services/whatsapp/variable_resolver.py` — vai trò unknown: agent chưa xác định
  - `app/services/whatsapp/webhook_service.py` — vai trò unknown: agent chưa xác định
  - `app/services/whatsapp/worker.py` — vai trò unknown: agent chưa xác định

### Truy cập dữ liệu

- Package `app/repositories/appointments/`
  - `app/repositories/appointments/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/repositories/appointments/__init__.py:1`: `from app.repositories.appointments.appointment_repository import AppointmentRepository`
  - `app/repositories/appointments/appointment_repository.py` — Truy cập dữ liệu (exact) — `app/repositories/appointments/appointment_repository.py:59`: `self.db.add(entity)`
- Package `app/repositories/auth/`
  - `app/repositories/auth/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/repositories/auth/__init__.py:1`: `from app.repositories.auth.auth_repository import AuthRepository`
  - `app/repositories/auth/auth_repository.py` — Truy cập dữ liệu (exact) — `app/repositories/auth/auth_repository.py:15`: `stmt = select(User).where(func.lower(User.email) == normalized_email)`
- Package `app/repositories/clients/`
  - `app/repositories/clients/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/repositories/clients/__init__.py:1`: `from app.repositories.clients.client_repository import ClientRepository`
  - `app/repositories/clients/client_repository.py` — Truy cập dữ liệu (exact) — `app/repositories/clients/client_repository.py:23`: `self.db.add(entity)`
- Package `app/repositories/services/`
  - `app/repositories/services/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/repositories/services/__init__.py:1`: `from app.repositories.services.service_repository import ServiceRepository`
  - `app/repositories/services/service_repository.py` — Truy cập dữ liệu (exact) — `app/repositories/services/service_repository.py:15`: `self.db.add(entity)`
- Package `app/repositories/super_admin/`
  - `app/repositories/super_admin/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/repositories/super_admin/__init__.py:1`: `from app.repositories.super_admin.super_admin_repository import SuperAdminRepository`
  - `app/repositories/super_admin/super_admin_repository.py` — Truy cập dữ liệu (exact) — `app/repositories/super_admin/super_admin_repository.py:15`: `stmt = select(SuperAdmin).where(func.lower(SuperAdmin.email) == normalized_email)`
- Package `app/repositories/tenant/`
  - `app/repositories/tenant/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/repositories/tenant/__init__.py:1`: `from app.repositories.tenant.tenant_config_repository import TenantConfigRepository`
  - `app/repositories/tenant/tenant_config_repository.py` — Truy cập dữ liệu (exact) — `app/repositories/tenant/tenant_config_repository.py:13`: `entity = self.db.get(TenantConfig, tenant_id)`
  - `app/repositories/tenant/tenant_payment_repository.py` — Truy cập dữ liệu (exact) — `app/repositories/tenant/tenant_payment_repository.py:31`: `self.db.add(payment)`
  - `app/repositories/tenant/tenant_repository.py` — Truy cập dữ liệu (exact) — `app/repositories/tenant/tenant_repository.py:72`: `self.db.add(tenant)`
- Package `app/repositories/users/`
  - `app/repositories/users/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/repositories/users/__init__.py:1`: `from app.repositories.users.user_repository import UserRepository`
  - `app/repositories/users/user_repository.py` — Truy cập dữ liệu (exact) — `app/repositories/users/user_repository.py:32`: `self.db.add(user)`
- Package `app/repositories/waitlists/`
  - `app/repositories/waitlists/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/repositories/waitlists/__init__.py:1`: `from app.repositories.waitlists.waitlist_repository import WaitlistRepository`
  - `app/repositories/waitlists/waitlist_repository.py` — Truy cập dữ liệu (exact) — `app/repositories/waitlists/waitlist_repository.py:33`: `self.db.add(entity)`
- Package `app/repositories/whatsapp_events/`
  - `app/repositories/whatsapp_events/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/repositories/whatsapp_events/__init__.py:1`: `from app.repositories.whatsapp_events.processed_webhook_repository import ProcessedWebhookRepository`
  - `app/repositories/whatsapp_events/processed_webhook_repository.py` — Truy cập dữ liệu (exact) — `app/repositories/whatsapp_events/processed_webhook_repository.py:16`: `return self.db.execute(stmt).first() is not None`
- Package `app/repositories/whatsapp_outbox/`
  - `app/repositories/whatsapp_outbox/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/repositories/whatsapp_outbox/whatsapp_outbox_repository.py` — vai trò unknown: agent chưa xác định
- Package `app/repositories/whatsapp_sessions/`
  - `app/repositories/whatsapp_sessions/__init__.py` — vai trò unknown: agent chưa xác định
  - `app/repositories/whatsapp_sessions/whatsapp_session_repository.py` — vai trò unknown: agent chưa xác định

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
- `ANALYSIS_PARTIAL`: MODEL_ERROR: HTTP 429 credit_balance_exhausted
- `SOURCE_NOT_FULLY_READ`: app/repositories/whatsapp_outbox/__init__.py thiếu [[1, 3]]; app/repositories/whatsapp_outbox/whatsapp_outbox_repository.py thiếu [[1, 186]]; app/repositories/whatsapp_sessions/__init__.py thiếu [[1, 3]]; app/repositories/whatsapp_sessions/whatsapp_session_repository.py thiếu [[1, 70]]; app/scripts/send_tomorrow_reminders.py thiếu [[1, 46]]; app/seeds/create_frontend_test_users.py thiếu [[1, 154]]; app/services/appointments/__init__.py thiếu [[1, 3]]; app/services/appointments/appointment_service.py thiếu [[1, 673]]; app/services/auth/__init__.py thiếu [[1, 3]]; app/services/auth/auth_service.py thiếu [[1, 337]]; app/services/clients/__init__.py thiếu [[1, 3]]; app/services/clients/client_service.py thiếu [[1, 64]]; app/services/scheduler/__init__.py thiếu [[1, 1]]; app/services/scheduler/reminder_scheduler.py thiếu [[1, 336]]; app/services/scheduler/worker.py thiếu [[1, 68]]; app/services/services/__init__.py thiếu [[1, 3]]; app/services/services/service_service.py thiếu [[1, 53]]; app/services/super_admin/__init__.py thiếu [[1, 3]]; app/services/super_admin/super_admin_service.py thiếu [[1, 28]]; app/services/tenant/__init__.py thiếu [[1, 4]]; app/services/tenant/tenant_payment_service.py thiếu [[1, 61]]; app/services/tenant/tenant_service.py thiếu [[1, 161]]; app/services/users/__init__.py thiếu [[1, 3]]; app/services/users/user_service.py thiếu [[1, 191]]; app/services/waitlists/__init__.py thiếu [[1, 3]]; app/services/waitlists/waitlist_service.py thiếu [[1, 40]]; app/services/whatsapp/__init__.py thiếu [[1, 20]]; app/services/whatsapp/connection_service.py thiếu [[1, 353]]; app/services/whatsapp/evolution_client.py thiếu [[1, 286]]; app/services/whatsapp/outbox_service.py thiếu [[1, 182]]; app/services/whatsapp/template_engine.py thiếu [[1, 60]]; app/services/whatsapp/variable_resolver.py thiếu [[1, 128]]; app/services/whatsapp/webhook_service.py thiếu [[1, 1033]]; app/services/whatsapp/worker.py thiếu [[1, 41]]; pyproject.toml thiếu [[1, 25]]
- `OUT_OF_SCOPE_FILES`: conditional_out: 1 file, migration: 20 file, test: 13 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- `CLAIMS_REJECTED`: 9 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
