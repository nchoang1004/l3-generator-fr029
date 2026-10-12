# full-stack-fastapi-template — tài liệu API

Bản sinh tự động từ source, chưa được chủ repository duyệt. File này dành cho người đọc; dữ liệu đầy đủ cho máy nằm ở `result.json` và các file ở phụ lục.

| Mục | Giá trị |
|---|---|
| Tình trạng | Chưa đủ — model không gọi công cụ, xem mục 11 |
| Đọc source | 4/22 file trong phạm vi |
| Endpoint | 0 |
| Model | 0 |
| Bảng CSDL | 2 |
| Sự kiện, tác vụ nền | 0 điểm gửi/nhận |
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
| item | Item | 5 | user |
| user | User | 7 | — |

### item

Lớp `Item`, khai ở `backend/app/models.py:91`. Suy luận: không khai __tablename__, SQLModel dùng tên class viết thường.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| title | str, max_length=255 | không\* | — | không\* | — |
| description | str, max_length=255 | không\* | — | có\* | — |
| id | uuid.UUID | có | — | không\* | — |
| created_at | DateTime(timezone=True) | không\* | — | có\* | — |
| owner_id | uuid.UUID | không\* | user.id | không | xóa theo: CASCADE |

### user

Lớp `User`, khai ở `backend/app/models.py:52`. Suy luận: không khai __tablename__, SQLModel dùng tên class viết thường.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| email | EmailStr, max_length=255 | không\* | — | không\* | unique, index |
| is_active | bool | không\* | — | không\* | — |
| is_superuser | bool | không\* | — | không\* | — |
| full_name | str, max_length=255 | không\* | — | có\* | — |
| id | uuid.UUID | có | — | không\* | — |
| hashed_password | str | không\* | — | không\* | — |
| created_at | DateTime(timezone=True) | không\* | — | có\* | — |

## 5. Sự kiện và tác vụ nền

Không thấy điểm gửi/nhận qua Kafka, FastStream, Celery hay BackgroundTasks.

## 6. Cấu trúc code

Vai trò của từng file theo dấu hiệu trong code (FR-029). Chỉ liệt kê component thường.

### Gốc

### backend

Không có vai trò: 4 file rỗng; chưa xác định vai trò: `backend/app/api/deps.py`, `backend/app/api/main.py`, `backend/app/api/routes/items.py`, `backend/app/api/routes/login.py`, `backend/app/api/routes/private.py`, `backend/app/api/routes/users.py`, `backend/app/api/routes/utils.py`, `backend/app/core/config.py`, `backend/app/core/db.py`, `backend/app/core/security.py`, `backend/app/crud.py`, `backend/app/initial_data.py`, `backend/app/main.py`, `backend/app/models.py`, `backend/app/utils.py`.

### hooks

Không có vai trò: chưa xác định vai trò: `hooks/post_gen_project.py`.

### scripts

## 7. Gọi HTTP ra ngoài

Không có lời gọi nào qua httpx, requests, aiohttp.

## 8. Thư viện

| Thư viện | Phiên bản | Có import trong code | Khai ở |
|---|---|---|---|
| alembic | &gt;=1.19.1,&lt;2.0.0 | chưa thấy import | `backend/pyproject.toml:13` |
| email-validator | &lt;3.0.0.0,&gt;=2.1.0.post1 | chưa thấy import | `backend/pyproject.toml:9` |
| emails | &gt;=1.1.2,&lt;2.0 | có | `backend/pyproject.toml:11` |
| fastapi | &gt;=0.141.1,&lt;1.0.0 | có | `backend/pyproject.toml:7` |
| httpx | &lt;1.0.0,&gt;=0.25.1 | chưa thấy import | `backend/pyproject.toml:14` |
| jinja2 | &lt;4.0.0,&gt;=3.1.4 | có | `backend/pyproject.toml:12` |
| psycopg | &gt;=3.3.4,&lt;4.0.0 | chưa thấy import | `backend/pyproject.toml:15` |
| pwdlib | &gt;=0.3.1 | có | `backend/pyproject.toml:20` |
| pydantic | &gt;2.0 | có | `backend/pyproject.toml:10` |
| pydantic-settings | &lt;3.0.0,&gt;=2.2.1 | có | `backend/pyproject.toml:17` |
| pyjwt | &lt;3.0.0,&gt;=2.13.0 | có | `backend/pyproject.toml:19` |
| python-multipart | &lt;1.0.0,&gt;=0.0.27 | chưa thấy import | `backend/pyproject.toml:8` |
| sentry-sdk | &gt;=2.68.1,&lt;3.0.0 | có | `backend/pyproject.toml:18` |
| sqlmodel | &gt;=0.0.39,&lt;1.0.0 | có | `backend/pyproject.toml:16` |

"Chưa thấy import": tên gói khác tên import, hoặc gói chỉ dùng gián tiếp (driver, plugin, công cụ).

## 9. Cấu hình

| Khóa | Nguồn | Giá trị mặc định | Khai ở |
|---|---|---|---|
| ACCESS_TOKEN_EXPIRE_MINUTES | lớp Settings | đã che (dấu hiệu bí mật) | `backend/app/core/config.py:25` |
| API_V1_STR | lớp Settings | /api/v1 | `backend/app/core/config.py:22` |
| DATABASE_URL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/app/core/config.py:31` |
| EMAILS_FROM_EMAIL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/app/core/config.py:48` |
| EMAILS_FROM_NAME | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/app/core/config.py:49` |
| EMAIL_RESET_TOKEN_EXPIRE_HOURS | lớp Settings | đã che (dấu hiệu bí mật) | `backend/app/core/config.py:57` |
| EMAIL_TEST_USER | lớp Settings | test@example.com | `backend/app/core/config.py:64` |
| FASTAPI_ENV | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/app/core/config.py:27` |
| FIRST_SUPERUSER | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/app/core/config.py:65` |
| FIRST_SUPERUSER_PASSWORD | lớp Settings | đã che (dấu hiệu bí mật) | `backend/app/core/config.py:66` |
| FRONTEND_HOST | lớp Settings | http://localhost:5173 | `backend/app/core/config.py:26` |
| PROJECT_NAME | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/app/core/config.py:29` |
| SECRET_KEY | lớp Settings | đã che (dấu hiệu bí mật) | `backend/app/core/config.py:23` |
| SENTRY_DSN | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/app/core/config.py:30` |
| SMTP_HOST | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/app/core/config.py:45` |
| SMTP_PASSWORD | lớp Settings | đã che (dấu hiệu bí mật) | `backend/app/core/config.py:47` |
| SMTP_PORT | lớp Settings | 587 | `backend/app/core/config.py:44` |
| SMTP_SSL | lớp Settings | False | `backend/app/core/config.py:43` |
| SMTP_TLS | lớp Settings | True | `backend/app/core/config.py:42` |
| SMTP_USER | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/app/core/config.py:46` |

## 10. Middleware và xử lý lỗi toàn cục

| Loại | Tên | Ở đâu |
|---|---|---|
| middleware | `CORSMiddleware` | `backend/app/main.py:27` |

Middleware áp dụng cho mọi request của app. Middleware xác thực chỉ cho biết app đọc thông tin đăng nhập; route có bắt buộc đăng nhập hay không vẫn xem ở cột Auth.

## 11. Chưa biết và giới hạn

- **File lỗi cú pháp, không đọc được.** backend/app/api/deps.py: SyntaxError
- **Chưa có sơ đồ component.** Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- **Chưa đối chiếu với dữ liệu kiến trúc.** Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- **Phân tích chưa xong.** model không gọi công cụ
- **Có phần source chưa đọc.** backend/app/api/deps.py thiếu [[1, 57]]; backend/app/api/main.py thiếu [[1, 14]]; backend/app/api/routes/items.py thiếu [[1, 113]]; backend/app/api/routes/login.py thiếu [[1, 123]]; backend/app/api/routes/private.py thiếu [[1, 38]]; backend/app/api/routes/users.py thiếu [[1, 232]]; backend/app/api/routes/utils.py thiếu [[1, 31]]; backend/app/core/config.py thiếu [[1, 91]]; backend/app/core/db.py thiếu [[1, 33]]; backend/app/core/security.py thiếu [[1, 36]]; backend/app/crud.py thiếu [[1, 68]]; backend/app/initial_data.py thiếu [[1, 23]]; backend/app/main.py thiếu [[1, 36]]; backend/app/models.py thiếu [[1, 133]]; backend/app/utils.py thiếu [[1, 125]]; backend/pyproject.toml thiếu [[1, 82]]; hooks/post_gen_project.py thiếu [[1, 8]]; pyproject.toml thiếu [[1, 36]]
- **File ngoài phạm vi đọc.** conditional_out: 2 file, migration: 6 file, test: 15 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- **Dòng trông giống route hoặc lời gọi HTTP nhưng chưa được xác nhận, nên không có trong tài liệu.** `backend/app/api/routes/items.py:13`, `backend/app/api/routes/items.py:48`, `backend/app/api/routes/items.py:61`, `backend/app/api/routes/items.py:75`, `backend/app/api/routes/items.py:99`, `backend/app/api/routes/login.py:23`, `backend/app/api/routes/login.py:45`, `backend/app/api/routes/login.py:53`, `backend/app/api/routes/login.py:77`, `backend/app/api/routes/login.py:100`, `backend/app/api/routes/private.py:23`, `backend/app/api/routes/users.py:32`, `backend/app/api/routes/users.py:54`, `backend/app/api/routes/users.py:81`, `backend/app/api/routes/users.py:103`, `backend/app/api/routes/users.py:124`, `backend/app/api/routes/users.py:132`, `backend/app/api/routes/users.py:146`, `backend/app/api/routes/users.py:162`, `backend/app/api/routes/users.py:182`, `backend/app/api/routes/users.py:214`, `backend/app/api/routes/utils.py:11`, `backend/app/api/routes/utils.py:29`

## Phụ lục: file cho máy

- TBL (DDL): [tech-specs/BACKEND/schema/TBL-FULL-STACK-FASTAPI-TEMPLATE-BACKEND.md](tech-specs/BACKEND/schema/TBL-FULL-STACK-FASTAPI-TEMPLATE-BACKEND.md) — component backend
