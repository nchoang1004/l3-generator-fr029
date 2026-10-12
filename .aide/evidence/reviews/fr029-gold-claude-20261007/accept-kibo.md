# Rà soát gold FR-029: kibo-backend

Người rà: Claude (độc lập), ngày 07/10/2026. Chỉ đọc. Không chạy code của repository. Không chạy oracle.

- Gold: `D:/VSF/l3-acceptance-gold/kibo/gold.json` (+ `membership.json`)
- Source: `D:/VSF/l3-acceptance-repos/KIBO-Agenda_kibo-backend-89eb3bb`, `root = "."`
- Đối chiếu với `FR-L3GEN-029.md` (rev 3), mục "Phạm vi đọc" của FR-L3GEN-028, `slice/tools/fr029_score.py` (bản hiện tại trên đĩa, đã có `FORMAT_NAMES` cho uuid/date/datetime/email), `slice/tools/fr029_accept.py`.

## Kết luận

Gold đúng ở hầu hết các mục. Không thấy route, model, lời gọi HTTP hay file nào bị thiếu. Không thấy giá trị chính sai ở route, model, HTTP.

Có 2 lỗi nhỏ ở dòng bằng chứng của file_roles (A). Có 2 lỗi định dạng làm scorer không bao giờ chấm đúng được (E). Có 5 điểm mơ hồ (D).

| Loại | Số | Ý nghĩa |
|---|---|---|
| A | 2 | Giá trị chính của gold sai/thiếu |
| B | 0 | Phương án thay thế nhận đáp án sai |
| C | 0 | Gold bỏ sót mục trong phạm vi |
| D | 5 | Mơ hồ / cách hiểu spec |
| E | 2 | Lỗi scorer / định dạng |

**Không có `oracle.json` cạnh gold.** Gold ghi `oracle_versions`, `oracle_python` và note 1, 2, 20 nói đã chạy `fr029_oracle.py`. Không có file kết quả oracle để kiểm lại. Tôi không chạy oracle. Các khẳng định "khớp app.openapi()" trong gold là chưa kiểm được qua oracle; tôi chỉ đối chiếu bằng đọc source.

## Phạm vi đã kiểm

| Mục | Số trong gold | Kiểm đủ | Lấy mẫu | Chưa kiểm | Cách kiểm |
|---|---|---|---|---|---|
| Route | 64 | 64 | 0 | 0 | Đọc 11 file router + `app/main.py`. Đếm decorator: 64 decorator route + 11 `APIRouter(` + 1 `FastAPI(` = 76 dòng, khớp. Kiểm method, path qua prefix, handler, `declared_at`, tham số, body, response, status |
| Model | 50 | 50 | 0 | 0 | Đọc cả 10 file schema. Kiểm từng trường: kiểu, required, nullable, alias |
| Lời gọi HTTP | 8 | 8 | 0 | 0 | Đọc `evolution_client.py`; grep `httpx/requests/aiohttp/urllib/http.client` trong `app/` |
| file_roles | 126 | 126 | 0 | 0 | Grep dấu hiệu (decorator, `__tablename__`, `create_engine`, `SMTP(`, `httpx.AsyncClient`, method session, `select/update/...(`, `getenv`, `__main__`) trên mọi file; so tập dòng bằng chứng với `line` + `alt_lines` bằng script stdlib. Đọc tay file Service, Khác, worker, scheduler |
| call_path của Service | 11 | 11 dòng đầu/cuối | — | — | Đọc từng dòng trích dẫn |
| Limitations / excluded_routes | 0 / 0 | có | — | — | Grep `add_api_route`, `add_route`, `add_websocket_route`, `mount`: không có. Không có route trong `tests/`, `alembic/`, `app/scripts/test_whatsapp_connection.py` |
| membership.json | 170 file | có | — | — | 126 normal + 13 test + 20 migration + 11 file .py rỗng/chỉ comment + 2 manifest. Tổng 170 file `.py` khớp `find` |
| out_of_scope | 1 | có | — | — | test 13, migration 20: khớp |
| Phụ thuộc/auth của route | không có trong gold | — | — | — | Gold không ghi; xem D5 |

## Phát hiện

### A — giá trị chính sai hoặc thiếu

| # | Đường dẫn gold | Source | Trích | Gold | Đúng | Lý do |
|---|---|---|---|---|---|---|
| A1 | `file_roles[105]` (`app/services/scheduler/reminder_scheduler.py`) `.line` / `.alt_lines` | `reminder_scheduler.py:38` (và 307, 314, 332) | `            db.close()` | line 53, alt [70, 113, 120, 136, 151, 186, 191] | Thêm 38, 307, 314, 332 vào tập dòng chấp nhận; dòng đầu tiên của file là 38 | Chính gold coi `db.close()` là "gọi method trên session" (note 36, `file_roles[125]` worker.py dòng 31). Ở file này gold lại không nhận dòng `db.close()`. Công cụ trích dòng dấu hiệu đầu tiên (38) sẽ bị chấm sai `line` |
| A2 | `file_roles[55]` (`app/repositories/appointments/appointment_repository.py`) `.alt_lines` | `appointment_repository.py:414`, `:426` | `            update(Appointment)` | không có 414, 426 | Thêm 414, 426 | Đây là dòng "dựng truy vấn" (SQLAlchemy `update()`), cùng loại với các dòng `select(` gold đã nhận. Ảnh hưởng nhỏ vì dòng chính 59 đúng |

### B — phương án thay thế nhận đáp án sai

Không thấy. Đã xét mọi `alt_types` (enum → tên enum, `time` → `time`, `Decimal` → `string`), `alt_methods` (`unknown` cho dòng 162, 182), `alt_lines`. Tất cả đều là cách viết hợp lệ của cùng giá trị.

### C — gold bỏ sót

Không thấy. 64/64 route, 50/50 model dùng làm request/response (kể cả model lồng), 8/8 lời gọi httpx, 126/126 file của component normal.

### D — mơ hồ / cách hiểu spec

| # | Đường dẫn gold | Source | Vấn đề | Đề xuất |
|---|---|---|---|---|
| D1 | `file_roles[125]` (`app/services/whatsapp/worker.py`) `.role` | `worker.py:31` `                db.close()` | Vai trò Truy cập dữ liệu chỉ dựa vào `db.close()`. Gold tự ghi (note 36) nếu không tính `db.close()` thì file là Khác. Spec không nói rõ đóng session có phải "gọi method trên session" không | Thêm `alt_roles: ["Khác"]`, hoặc ghi quyết định vào spec |
| D2 | `file_roles[100,104,108,110,112,113,115,117,119,123,124]` (Service) `.line` | ví dụ `client_service.py:16` `return self.client_repo.create(...)` | Spec không nói dòng nào là bằng chứng cho Service. Gold chỉ nhận dòng gọi repository/client. Công cụ trích dòng `def` hoặc `class` mà route gọi tới sẽ bị chấm sai | Ghi quy tắc chọn dòng vào spec, hoặc nhận thêm dòng `def` của hàm route gọi |
| D3 | `routes[*].declared_at` | ví dụ `tenant/router.py:93` `@router.get(` (decorator nhiều dòng), hàm ở 97 | Gold dùng dòng decorator. Spec ghi "vị trí khai báo", không nói decorator hay `def`. Scorer không có khóa thay thế cho route; lệch dòng thành FN + FP | Ghi rõ trong spec, hoặc thêm `alt_declared_at` |
| D4 | `http_calls[0..7].target.value` | `config.py:47` `EVOLUTION_API_BASE_URL: str \| None = getenv("EVOLUTION_API_BASE_URL") or getenv("WHATSAPP_API_URL")` | Khóa cấu hình có hai biến môi trường. Công cụ có thể ghi `settings.EVOLUTION_API_BASE_URL` hoặc `WHATSAPP_API_URL`. Scorer so chuỗi nguyên văn | Ghi quy ước đặt tên khóa, hoặc thêm `accept_alt_target` |
| D5 | `routes[*]` (không có trường) | ví dụ `waitlists/router.py:22` `Depends(check_plan_permission(PlanTier.PRO))` | FR-029 yêu cầu cột "dependency hoặc auth" và nhãn mức chắc chắn cho mỗi route. Gold không ghi dependency; scorer không chấm dependency hay nhãn route. Hai thứ này chưa được đo | Bổ sung nếu muốn đo; nếu không, ghi rõ là chưa đo |

### E — lỗi scorer / định dạng

| # | Đường dẫn gold | Source | Vấn đề | Hệ quả |
|---|---|---|---|---|
| E1 | `routes[59].request_body`, `routes[60].request_body` | `whatsapp/router.py:397`, `:453` `payload: dict[str, Any] = Body(default_factory=dict),` | Giá trị gold đúng về nghĩa: có body JSON kiểu object, không bắt buộc, không model, không trường. Scorer biến gold thành `([], "application/json", False, False, [])`. Phía result, dạng này chỉ có được khi `request_inline` tồn tại với danh sách trường rỗng. Tôi xem `slice/l3slice/docfacts.py:905-935` chỉ để biết dạng result: `request_inline` chỉ được ghi khi có trường. Không model, không trường thì scorer đọc ra `None` | Hai route này luôn bị chấm sai `request_body`, kể cả khi công cụ đúng. Cần cho phép trường `type` của body (gold đã có `type: object` nhưng scorer bỏ qua) |
| E2 | `out_of_scope` | — | Gold có khóa giá trị 0: `environment: 0`, `conditional_out: 0`. Scorer dựng `counts` chỉ từ các mục có thật, nên không bao giờ có khóa giá trị 0. `counts == gold["out_of_scope"]` luôn sai | `out_of_scope.ok` luôn `false`. Sửa: bỏ khóa 0 khỏi gold, hoặc so sau khi lọc giá trị 0 |

## Điểm đã kiểm và thấy đúng (tóm tắt)

- Prefix `/api/v1` lấy mặc định từ `config.py:36`; router whatsapp không có prefix (`router.py:27`); `/health` gắn thẳng trên app (`main.py:73`).
- Header `Authorization` (`required=false`) đúng ở mọi route có dependency đọc header, kể cả lồng qua `require_owner`, `check_plan_permission`. Không có ở route `/auth` (trừ `/me`, `/change-password`), `/super-admins`, `/webhooks/*`, `/test/*`, `/health`.
- Query alias `date` (`appointments/router.py:98`), `test_key` mặc định `"test123"` nên không bắt buộc.
- `response=null` cho route không khai `response_model` và không có kiểu trả về; `response_model=dict` → object; `list[...]` → `array=true`.
- Status 201/204 khai bằng hằng `status.HTTP_*`; còn lại 200 mặc định.
- 50 model: mọi trường, kiểu, required, nullable khớp source (Pydantic v2: `X | None` không default vẫn bắt buộc).
- HTTP: 8 dòng `client.post/get/request` trong `evolution_client.py`; method dòng 204 là `unknown` (DELETE/POST); dòng 162, 182 là GET.
- `smtplib` không phải HTTP; `app/scripts/test_whatsapp_connection.py` khớp `test_*.py` nên ngoài phạm vi; `app/api/v1/test.py` không khớp luật tên test nên trong phạm vi.
- file_roles: 11 file route, 13 file model bảng, 3 file hạ tầng, 2 file cấu hình, 3 điểm vào, 10 file schema, 11 file Service, 18 file truy cập dữ liệu, 55 file Khác. Ngoài A1, A2 và D1, D2: vai trò, nhãn và dòng đều khớp.

## Giới hạn

- Không có `oracle.json`; không chạy oracle. Hành vi FastAPI (gộp tham số header trùng, body không bắt buộc khi có `default_factory`, schema `Decimal`) suy từ hiểu biết về FastAPI 0.135/Pydantic 2.12, chưa chạy để xác nhận.
- Không chạy scorer với result thật. E1 suy từ đọc `fr029_score.py` và một đoạn `docfacts.py`.
- `fr029_score.py` đã đổi trên đĩa trong lúc rà (thêm `FORMAT_NAMES`). Nhận định dựa trên bản hiện tại. Với bản cũ, mọi trường `email`, `uuid`, `date`, `datetime` sẽ bị chấm sai.
- Không đọc `ket-qua-chay/`, `docs/HANDOFF.md`, `docs/FR029-*.md`, các review khác, diaries.
