# tdd-docker — tài liệu API

Bản sinh tự động từ source, chưa được chủ repository duyệt. File này dành cho người đọc; dữ liệu đầy đủ cho máy nằm ở `result.json` và các file ở phụ lục.

| Mục | Giá trị |
|---|---|
| Tình trạng | Đủ |
| Đọc source | 15/15 file trong phạm vi |
| Endpoint | 6 |
| Model | 4 |
| Bảng CSDL | 0 |
| Sự kiện, tác vụ nền | 2 điểm gửi/nhận |
| Gọi HTTP ra ngoài | 0 |
| Sinh bởi | model scripted, prompt fr029-oneshot-prompt-v6; bảng, sự kiện, thư viện, cấu hình, middleware đọc tĩnh từ code |

Cách đọc nhãn: **chắc chắn** — đọc thẳng từ một dòng code; **suy luận** — theo quy tắc mặc định của framework, lý do ở chú thích [n]; **chưa rõ** — source không đủ để kết luận; **AI viết** — câu chữ do model viết, chỉ để đọc nhanh, không phải dữ kiện đã kiểm.

## 1. Danh sách endpoint

| # | Method | Path | Vào | Ra | Status | Auth |
|---|---|---|---|---|---|---|
| 1 | GET | /ping | — | — | 200 | chưa rõ |
| 2 | GET | /summaries/ | — | list[SummarySchema] | 200 | chưa rõ |
| 3 | POST | /summaries/ | SummaryPayloadSchema | SummaryResponseSchema | 201 | chưa rõ |
| 4 | DELETE | /summaries/{id}/ | — | SummaryResponseSchema | 200, 404* | chưa rõ |
| 5 | GET | /summaries/{id}/ | — | SummarySchema | 200, 404* | chưa rõ |
| 6 | PUT | /summaries/{id}/ | SummaryUpdatePayloadSchema | SummarySchema | 200, 404* | chưa rõ |

\* mã lỗi suy từ chỗ ném lỗi trong code, xem mục 2.

## 2. Chi tiết từng endpoint

### 1. GET /ping

- Mô tả (AI viết): Kiểm tra dịch vụ còn sống, trả về pong cùng môi trường và cờ testing.
- Hàm xử lý: `pong` tại `app/api/ping.py:8`
- Tham số: không có
- Trả về: —
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_settings
- Auth: chưa rõ — Không thấy cơ chế xác thực nào (không có Security hay lược đồ fastapi.security)
- Mức chắc chắn: suy luận [1]
- Còn thiếu: Trường chưa xác định: auth

### 2. GET /summaries/

- Mô tả (AI viết): Lấy danh sách tất cả bản tóm tắt.
- Hàm xử lý: `read_all_summaries` tại `app/api/summaries.py:27`
- Tham số: không có
- Trả về: list[SummarySchema]
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: không có
- Auth: chưa rõ — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security)
- Nhóm (tags): summaries
- Mức chắc chắn: suy luận [1]
- Còn thiếu: Trường chưa xác định: auth

### 3. POST /summaries/

- Mô tả (AI viết): Tạo bản ghi tóm tắt cho một URL và chạy nền việc sinh nội dung tóm tắt.
- Hàm xử lý: `create_summary` tại `app/api/summaries.py:32`
- Tham số: không có
- Body: SummaryPayloadSchema
- Trả về: SummaryResponseSchema
- Status: 201 (khai trong code)
- Dependency: không có
- Auth: chưa rõ — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security)
- Nhóm (tags): summaries
- Mức chắc chắn: suy luận [2]
- Còn thiếu: Trường chưa xác định: auth

### 4. DELETE /summaries/{id}/

- Mô tả (AI viết): Xóa một bản tóm tắt theo id và trả về bản ghi đã xóa.
- Hàm xử lý: `delete_summary` tại `app/api/summaries.py:55`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | id | path | integer | có |

- Trả về: SummaryResponseSchema
- Status: 200 (mặc định của framework, xem chú thích)
- Lỗi có thể trả về: 404 — HTTPException, ném ở `app/api/summaries.py:59`
- Dependency: không có
- Auth: chưa rõ — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security)
- Nhóm (tags): summaries
- Mức chắc chắn: suy luận [1]
- Còn thiếu: Trường chưa xác định: auth

### 5. GET /summaries/{id}/

- Mô tả (AI viết): Lấy một bản tóm tắt theo id.
- Hàm xử lý: `read_summary` tại `app/api/summaries.py:18`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | id | path | integer | có |

- Trả về: SummarySchema
- Status: 200 (mặc định của framework, xem chú thích)
- Lỗi có thể trả về: 404 — HTTPException, ném ở `app/api/summaries.py:22`
- Dependency: không có
- Auth: chưa rõ — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security)
- Nhóm (tags): summaries
- Mức chắc chắn: suy luận [1]
- Còn thiếu: Trường chưa xác định: auth

### 6. PUT /summaries/{id}/

- Mô tả (AI viết): Cập nhật URL và nội dung của một bản tóm tắt theo id.
- Hàm xử lý: `update_summary` tại `app/api/summaries.py:44`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | id | path | integer | có |

- Body: SummaryUpdatePayloadSchema
- Trả về: SummarySchema
- Status: 200 (mặc định của framework, xem chú thích)
- Lỗi có thể trả về: 404 — HTTPException, ném ở `app/api/summaries.py:50`
- Dependency: không có
- Auth: chưa rõ — Không thấy cơ chế xác thực nào (không có Depends/Security hay lược đồ fastapi.security)
- Nhóm (tags): summaries
- Mức chắc chắn: suy luận [1][2]
- Còn thiếu: Trường chưa xác định: auth

Chú thích:

[1] Decorator không khai status_code; FastAPI dùng status mặc định 200 của JSONResponse  
[2] Tham số kiểu Pydantic model không khai Body; FastAPI coi là body  

## 3. Model dữ liệu

### SummaryPayloadSchema

Khai ở `app/models/pydantic.py:4`. Mức chắc chắn: suy luận [1][2].

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| url | string | có | không |

### SummaryResponseSchema

Khai ở `app/models/pydantic.py:8`. Mức chắc chắn: suy luận [1][2].

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| url | string | có | không |
| id | integer | có | không |

### SummarySchema

Khai ở `app/models/tortoise.py:14`. Mức chắc chắn: chắc chắn.

Trường chỉ biết lúc chạy: Model sinh lúc chạy: SummarySchema được tạo lúc chạy bằng pydantic_model_creator(TextSummary); các trường sinh ra từ model Tortoise nên chỉ biết khi chạy

### SummaryUpdatePayloadSchema

Khai ở `app/models/pydantic.py:12`. Mức chắc chắn: suy luận [1][2].

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| url | string | có | không |
| summary | string | có | không |

Chú thích:

[1] Pydantic v2: trường không có default là bắt buộc, kể cả khi kiểu cho phép None  
[2] Bộ kiểm chưa đối chiếu được kiểu/required/nullable với khai báo của: url  

## 4. Bảng CSDL

Không thấy bảng nào khai bằng SQLAlchemy/SQLModel trong phạm vi đọc.

## 5. Sự kiện và tác vụ nền

| Vai trò | Tác vụ hoặc topic | Thư viện / broker | Component | Ở đâu |
|---|---|---|---|---|
| gửi | app.summarizer.generate_summary | fastapi.BackgroundTasks | Tóm tắt | `app/api/summaries.py:38` |
| nhận | app.summarizer.generate_summary | fastapi.BackgroundTasks | Tóm tắt | `app/summarizer.py:7` |

Bên gửi và bên nhận chỉ được nối khi cùng broker và cùng tác vụ (FR-031); file EVT của từng component ghi bên liên quan.

## 6. Cấu trúc code

Vai trò của từng file theo dấu hiệu trong code (FR-029). Chỉ liệt kê component thường.

### Khởi động

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `app/db.py` | Điểm vào | `app/db.py:44` |
| `app/main.py` | Điểm vào | `app/main.py:12` |

### Ping

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `app/api/ping.py` | Route | `app/api/ping.py:8` |
| `app/config.py` | Cấu hình | `app/config.py:10` |

### Tóm tắt

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `app/api/crud.py` | Truy cập dữ liệu | `app/api/crud.py:12` |
| `app/api/summaries.py` | Route | `app/api/summaries.py:18` |
| `app/models/pydantic.py` | Schema API | `app/models/pydantic.py:4` |
| `app/models/tortoise.py` | Schema API | `app/models/tortoise.py:14` |
| `app/summarizer.py` | Truy cập dữ liệu | `app/summarizer.py:21` |

## 7. Gọi HTTP ra ngoài

Không có lời gọi nào qua httpx, requests, aiohttp.

## 8. Thư viện

| Thư viện | Phiên bản | Có import trong code | Khai ở |
|---|---|---|---|
| aerich | ==0.8.2 | chưa thấy import | `requirements.txt:1` |
| asyncpg | ==0.30.0 | chưa thấy import | `requirements.txt:2` |
| black | ==25.1.0 | chưa thấy import | `requirements-dev.txt:1` |
| fastapi | ==0.115.12 | có | `requirements.txt:3` |
| flake8 | ==7.2.0 | chưa thấy import | `requirements-dev.txt:2` |
| gunicorn | ==22.0.0 | chưa thấy import | `requirements.txt:4` |
| httpx | ==0.28.1 | chưa thấy import | `requirements.txt:5` |
| isort | ==6.0.1 | chưa thấy import | `requirements-dev.txt:3` |
| lxml-html-clean | ==0.4.2 | chưa thấy import | `requirements.txt:6` |
| newspaper3k | ==0.2.8 | chưa thấy import | `requirements.txt:7` |
| pydantic-settings | ==2.8.1 | có | `requirements.txt:8` |
| pytest | ==8.3.5 | chưa thấy import | `requirements-dev.txt:4` |
| pytest-cov | ==6.1.1 | chưa thấy import | `requirements-dev.txt:5` |
| pytest-xdist | ==3.6.1 | chưa thấy import | `requirements-dev.txt:6` |
| tortoise-orm | ==0.25.0 | có | `requirements.txt:9` |
| uvicorn | ==0.34.1 | chưa thấy import | `requirements.txt:10` |

"Chưa thấy import": tên gói khác tên import, hoặc gói chỉ dùng gián tiếp (driver, plugin, công cụ).

## 9. Cấu hình

| Khóa | Nguồn | Giá trị mặc định | Khai ở |
|---|---|---|---|
| DATABASE_URL | biến môi trường | chưa rõ (Giá trị đọc lúc chạy) | `app/db.py:12`, `app/db.py:25`, `app/db.py:36` |
| database_url | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `app/config.py:13` |
| environment | lớp Settings | dev | `app/config.py:11` |
| testing | lớp Settings | 0 | `app/config.py:12` |

## 10. Middleware và xử lý lỗi toàn cục

Không thấy middleware hay hàm xử lý lỗi đăng ký trên app.

## 11. Chưa biết và giới hạn

- **Chưa có sơ đồ component.** Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- **Chưa đối chiếu với dữ liệu kiến trúc.** Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- **Lời gọi HTTP qua thư viện chưa hỗ trợ.** unsupported_http_library tại app/summarizer.py:9 — article.download() của thư viện newspaper tải nội dung URL qua HTTP; thư viện này không thuộc httpx/requests/aiohttp nên không ghi thành http_call
- **Lời gọi HTTP qua thư viện chưa hỗ trợ.** unsupported_http_library tại app/summarizer.py:15 — nltk.download("punkt_tab") tải dữ liệu từ Internet qua thư viện nltk, không thuộc httpx/requests/aiohttp
- **File ngoài phạm vi đọc.** migration: 1 file, test: 5 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)

## Phụ lục: file cho máy

- API (OpenAPI): [tech-specs/TOM-TAT/api/API-TDD-DOCKER-TOM-TAT-v1.md](tech-specs/TOM-TAT/api/API-TDD-DOCKER-TOM-TAT-v1.md) — component Tóm tắt
- API (OpenAPI): [tech-specs/PING/api/API-TDD-DOCKER-PING-v1.md](tech-specs/PING/api/API-TDD-DOCKER-PING-v1.md) — component Ping
- EVT: [tech-specs/TOM-TAT/events/EVT-TDD-DOCKER-TOM-TAT-APP-SUMMARIZER-GENERATE-SUMMARY.md](tech-specs/TOM-TAT/events/EVT-TDD-DOCKER-TOM-TAT-APP-SUMMARIZER-GENERATE-SUMMARY.md) — component Tóm tắt
