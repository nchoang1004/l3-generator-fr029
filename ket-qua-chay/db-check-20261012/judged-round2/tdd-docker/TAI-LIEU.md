# tdd-docker — tài liệu API

Bản sinh tự động từ source, chưa được chủ repository duyệt. File này dành cho người đọc; dữ liệu đầy đủ cho máy nằm ở `result.json` và các file ở phụ lục.

| Mục | Giá trị |
|---|---|
| Tình trạng | Chưa đủ — model không gọi công cụ, xem mục 11 |
| Đọc source | 3/15 file trong phạm vi |
| Endpoint | 0 |
| Model | 0 |
| Bảng CSDL | 0; có bảng chưa đọc được, xem mục 11 |
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

Không thấy bảng nào khai bằng SQLAlchemy/SQLModel trong phạm vi đọc. Có bảng khai theo cách chưa đọc được, xem mục 11.

## 5. Sự kiện và tác vụ nền

| Vai trò | Tác vụ hoặc topic | Thư viện / broker | Component | Ở đâu |
|---|---|---|---|---|
| gửi | app.summarizer.generate_summary | fastapi.BackgroundTasks | app | `app/api/summaries.py:38` |
| nhận | app.summarizer.generate_summary | fastapi.BackgroundTasks | app | `app/summarizer.py:7` |

Bên gửi và bên nhận chỉ được nối khi cùng broker và cùng tác vụ (FR-031); file EVT của từng component ghi bên liên quan.

## 6. Cấu trúc code

Vai trò của từng file theo dấu hiệu trong code (FR-029). Chỉ liệt kê component thường.

### Gốc

### app

Không có vai trò: 3 file rỗng; chưa xác định vai trò: `app/api/crud.py`, `app/api/ping.py`, `app/api/summaries.py`, `app/config.py`, `app/db.py`, `app/main.py`, `app/models/pydantic.py`, `app/models/tortoise.py`, `app/summarizer.py`.

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

- **Loại component được suy từ phạm vi đọc.** Membership không ghi loại component; xếp theo phạm vi đọc (FR-028): migrations → migration, tests → test
- **Có bảng chưa đọc được.** Có bảng khai theo cách công cụ chưa đọc (FR-030 Phạm vi đọc), không có trong tài liệu: ORM khác — Tortoise: app/models/tortoise.py:5 (TextSummary); bảng chỉ có trong migration — textsummary (migrations/models/0_20250421234125_init.py:6), aerich (migrations/models/0_20250421234125_init.py:12)
- **Chưa có sơ đồ component.** Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- **Chưa đối chiếu với dữ liệu kiến trúc.** Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- **Phân tích chưa xong.** model không gọi công cụ
- **Có phần source chưa đọc.** app/api/crud.py thiếu [[1, 41]]; app/api/ping.py thiếu [[1, 14]]; app/api/summaries.py thiếu [[1, 63]]; app/config.py thiếu [[1, 19]]; app/db.py thiếu [[1, 45]]; app/main.py thiếu [[1, 23]]; app/models/pydantic.py thiếu [[1, 13]]; app/models/tortoise.py thiếu [[1, 14]]; app/summarizer.py thiếu [[1, 21]]; pyproject.toml thiếu [[1, 4]]; requirements-dev.txt thiếu [[1, 8]]; requirements.txt thiếu [[1, 10]]
- **File ngoài phạm vi đọc.** migration: 1 file, test: 5 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- **Dòng trông giống route hoặc lời gọi HTTP nhưng chưa được xác nhận, nên không có trong tài liệu.** `app/api/ping.py:8`, `app/api/summaries.py:18`, `app/api/summaries.py:27`, `app/api/summaries.py:32`, `app/api/summaries.py:44`, `app/api/summaries.py:55`

## Phụ lục: file cho máy

- EVT: [tech-specs/APP/events/EVT-TDD-DOCKER-APP-APP-SUMMARIZER-GENERATE-SUMMARY.md](tech-specs/APP/events/EVT-TDD-DOCKER-APP-APP-SUMMARIZER-GENERATE-SUMMARY.md) — component app
