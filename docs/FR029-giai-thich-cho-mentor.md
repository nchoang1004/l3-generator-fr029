# FR-029: cơ chế, kỹ thuật và kết quả đo

Cập nhật: 07/10/2026. Tài liệu giải thích công việc FR-029 cho người chưa theo dõi dự án: luồng chạy ra sao, từng kỹ thuật làm gì, vì sao làm vậy, đo được gì. Mọi số liệu là số đo thật; số liệu nằm ở `ket-qua-chay/fr029-pilot-20261007/`. Chỗ nào chưa đo thì ghi "chưa đo".

## 1. Tóm tắt

Mục này nói kết luận trong một màn hình.

- **Đã làm:** một luồng trong đó mô hình ngôn ngữ (gọi là "agent") tự đọc source FastAPI và viết tài liệu API. Code không trích dữ kiện; code kiểm bằng chứng của agent và sinh file.
- **Đo nghiệm thu: chưa đạt.** Theo OBS-001, nghiệm thu tính trên từng repo "kín" cỡ nhỏ và vừa. Đã chạy cả 4 repo, mỗi repo 1 lần, với luna và prompt v13. Gold do agent độc lập dựng bằng oracle `app.openapi()` (riêng `igorbenav` dùng golden v1 do Khiêm duyệt). Chỉ xem số tổng.

  | Repo (cỡ) | Route P/R | Model P/R | HTTP P/R | `exact` sai | Lần chạy |
  |---|---|---|---|---|---|
  | `tdd-docker` (nhỏ) | 1,00 / 1,00 | 1,00 / **0,75** | không có lời gọi | không có dữ kiện `exact` | completed, 0,009 USD |
  | `AgentGPT` (nhỏ) | 1,00 / 1,00 | 0,89 / 1,00 | **0,60 / 0,50** | **18%** | partial (chạm trần), 0,25 USD |
  | `igorbenav` (vừa) | 1,00 / 0,88 | chỉ đo tên model: **6/30** | không có lời gọi | chưa tính | completed, 0,49 USD |
  | `kibo-backend` (vừa) | 0,98 / 1,00 | 0,82 / 0,84 | 1,00 / 1,00, nhưng **đích sai 8/8** | **56%** | partial (chạm trần), 0,40 USD |

  Ngưỡng NFR-ACC-002: P, R ≥ 0,80 mỗi loại và `exact` sai ≤ 5%, trên **từng** repo.
  - **Route đạt trên cả 4 repo.**
  - Không đạt: `exact` sai, HTTP ở `AgentGPT`, model ở `tdd-docker` và `igorbenav`.
  - Thuộc tính yếu nhất: tham số (đúng 5/16 và 11/64), trường model (22/42 ở `kibo-backend`).
  - 2/4 lần chạy dừng vì trần chi phí, nên số đo có thể thấp hơn năng lực thật.
  - Số liệu: `ket-qua-chay/fr029-accept-v13/` (thư mục `private/` chứa chi tiết, không mở khi còn chỉnh prompt).
- **Kiểm toán độc lập (Codex `gpt-6-astra`, mức cao) kết luận chưa đủ, chưa đúng với toàn bộ yêu cầu.**
  - Codex tìm 20 lỗi code (F01–F20): 13 đã sửa xong và có test hồi quy, 6 sửa một phần, 1 còn mở (F07).
  - Báo cáo này đã được sửa theo các câu Codex chỉ ra là sai hoặc thổi phồng. Chi tiết ở mục 8.1.
- **Số đo chính.** Bộ chấm chỉ so những trường đáp án có ghi; xem mục 5.1.

  | Tập kiểm | Đo được gì | Kết quả |
  |---|---|---|
  | 6 fixture tự dựng (`luna5`, prompt v8) | Đủ 8 nhóm yêu cầu, theo các trường mà gold ghi | 18/18 lần, 0 lỗi theo bộ chấm |
  | 19 case phát triển của golden v1 (prompt v7) | Chỉ route | 40 đúng, 2 thừa, 0 thiếu |
  | `teamhide`, repo lộ cỡ nhỏ (prompt v8) | Route, tên model | Route 5/5; tên model 5/5 |
  | `full-stack-fastapi-template`, repo lộ cỡ nhỏ (prompt v8) | Route, tên model | Route 23/23; tên model 19/23 |
  | `igorbenav`, repo kín cỡ vừa (prompt v8) | Route, tên model | Route 30/34, 0 thừa; **tên model chỉ 6/30**; partial vì chạm trần chi phí |
  | `fastapi_best_architecture`, repo kín cỡ lớn (prompt v8) | Route, tên model, HTTP | **Route 1/139; HTTP 0/3**; partial vì chạm trần chi phí. Repo lớn chỉ báo số, không chặn nghiệm thu |
- **Các bản sửa sau v8 (prompt v9–v13) chưa được đo lại.**
- **Chi phí:** OpenAI `gpt-6-luna`. Tổng ước tính theo số token ghi lại là 1,62 USD; phần lớn tiêu vào `igorbenav` (vừa) và `fastapi_best_architecture` (lớn). Request lỗi không có số token nên không được tính.
- **Chờ quyết định:** 3 câu hỏi (mục 11).

## 2. Bài toán

Mục này nói FR-029 đòi gì, bằng ví dụ.

Đầu vào: một repository Python dùng FastAPI. Đầu ra:

| File | Nội dung |
|---|---|
| `tech-specs/<component>/api/API-<hệ thống>-<component>-v1.md` | Bảng endpoint, bảng model, truy vết, khối OpenAPI 3.1 |
| `README.md` | Mục lục, sơ đồ component, cấu trúc component (vai trò từng file), lời gọi HTTP ra ngoài, giới hạn |
| `result.json` | Mọi dữ kiện kèm bằng chứng `file:dòng`, để máy đọc lại và kiểm |

Ví dụ một dòng bảng endpoint mà tool sinh ra:

```
| POST | /api/v1/items/ | item (body, ItemIn, bắt buộc) | ItemIn | ItemOut | 201 |
  dependency: (không có); auth: unknown — Không thấy dependency |
  inferred (fastapi.json_body_media, fastapi.return_annotation_response_model) / partial | f:d022884b |
```

Đọc như sau: route `POST`, path đầy đủ đã ghép mọi prefix, nhận body `ItemIn`, trả `ItemOut`, status 201. Nhãn `inferred` kèm tên quy tắc cho biết giá trị nào suy từ mặc định của FastAPI. `f:d022884b` là mã dữ kiện để truy ngược về dòng code.

FR-029 có 8 tiêu chí nghiệm thu (AC); trạng thái từng AC ở mục 10.

## 3. Tổng quan luồng

Mục này cho bức tranh chung trước khi đi vào chi tiết.

```
repo ──► [1] Snapshot + phạm vi đọc          (code: source_tools.py)
     ──► [2] Agent đọc file qua công cụ        (model, vòng lặp: docagent.py)
     ──► [3] Agent nộp dữ kiện kèm file:dòng   (model)
     ──► [4] Bộ kiểm bằng chứng                 (code: docfacts.py) ── sai thì trả lỗi cho agent ─┐
     │         ▲───────────────────────────────────────────────────────────────────────────────┘
     ──► [5] Đổi thành fact, sinh file          (code: docfacts.py, render.py, docpipeline.py)
     ──► [6] Chấm với đáp án độc lập            (code: tools/fr029_score.py, fr029_golden4.py)
```

Nguyên tắc chia việc:

| Việc | Ai làm | Lý do |
|---|---|---|
| Hiểu code: route nào, prefix nào, model nào, vai trò file nào | Agent | Người dùng chọn hướng "agent thuần" |
| Quyết phạm vi đọc, kiểm bằng chứng, sinh file, chấm điểm | Code | Các việc này phải tất định và kiểm được |
| Tạo component, vẽ sơ đồ | Bước kiến trúc FR-028 (không thuộc phần này) | FR-029 nhận chúng làm đầu vào |

Các file code chính:

| File | Vai trò |
|---|---|
| `slice/l3slice/source_tools.py` | Chụp snapshot, chia phạm vi, công cụ đọc, sổ độ phủ, che bí mật |
| `slice/l3slice/docagent.py` | Vòng agent, prompt, adapter gọi model, ngân sách |
| `slice/l3slice/docfacts.py` | Khuôn dữ liệu agent nộp, bộ kiểm bằng chứng, đổi thành fact |
| `slice/l3slice/docpipeline.py` | Ghép mọi bước, đối chiếu kiến trúc, viết README và result.json |
| `slice/l3slice/render.py` | Viết file API (có từ trước, đã sửa thêm) |
| `slice/tools/fr029_*.py` | Chạy thử, chấm điểm, chọn mẫu, gộp kết quả chấm |

## 4. Cơ chế từng bước

### 4.1 Snapshot và phạm vi đọc

Mục này giải thích code chọn file nào cho agent đọc.

Code chụp snapshot: danh sách file `.py` và manifest (`requirements*.txt`, `pyproject.toml`), mỗi file có mã băm SHA-256. Mọi bằng chứng về sau đều trỏ vào snapshot này, nên tài liệu không bị lệch khi source thay đổi.

Phạm vi đọc theo bảng "Phạm vi đọc" của FR-028. Code quyết định phạm vi, không phải agent:

| Loại file | Ví dụ | Agent có đọc không |
|---|---|---|
| Code chính | `app/api/items.py` | Có |
| Manifest | `requirements.txt` | Có, để biết phiên bản Pydantic |
| Kiểm thử | `tests/test_api.py`, `conftest.py`, `test_*.py` | Không |
| Migration | `alembic/...` | Không |
| Môi trường | thư mục ẩn, `site-packages`, thư mục có `pyvenv.cfg` | Không |
| Thư mục có điều kiện | `scripts/`, `examples/`... | Chỉ khi file import code của repo |

Hệ quả: route khai trong file test không bao giờ tới tay agent, nên không thể lọt vào tài liệu (AC-05).

### 4.2 Công cụ đọc và sổ độ phủ

Mục này giải thích agent đọc file thế nào và làm sao biết nó đã đọc hết.

Agent chỉ có 5 công cụ; không có công cụ ghi file, chạy lệnh hay import code:

| Công cụ | Làm gì |
|---|---|
| `list_files` | Liệt kê file được đọc, và file bị loại kèm lý do |
| `read_file(path, start, end)` | Trả tối đa 200 dòng, mỗi dòng có số dòng |
| `search_text(query)` | Tìm chuỗi; kết quả tìm **không** tính là đã đọc |
| `submit_findings(...)` | Nộp dữ kiện; nhận lại lỗi theo từng trường |
| `finish()` | Báo xong; code kiểm rồi mới cho dừng |

**Sổ độ phủ** ghi từng dòng của từng file ở một trong hai trạng thái:

- `delivered`: dòng đã nằm trong kết quả công cụ trả về.
- `processed`: model đã trả lời hợp lệ ở lượt sau đó, tức là chắc chắn đã nhận dòng đó.

Ví dụ: agent đọc dòng 1–200 của file 250 dòng. Ngay sau đó sổ ghi 1–200 là `delivered`. Sau khi model trả lời lượt kế tiếp, 1–200 thành `processed`, còn 201–250 vẫn là "chưa đọc". Agent gọi `finish` thì code từ chối và trả về danh sách khoảng còn thiếu.

Dòng dài hơn 400 ký tự bị cắt; sổ ghi dòng đó là "đọc chưa hết", và lần chạy không được báo `completed`.

**Che bí mật:** trước khi gửi cho model, giá trị giống mật khẩu hoặc khóa bị thay bằng `***`. Số dòng được giữ nguyên, để bằng chứng `file:dòng` vẫn khớp với source thật:

```
source:   password = "hunter2hunter2"          gửi cho model:   password = "***"
source:   KEY = """-----BEGIN RSA ...          gửi cho model:   ***   (mỗi dòng của khối khóa)
```

Lỗi có từ trước, phát hiện trong lúc làm: mẫu che mật khẩu trong `common.py` có một ký tự hỏng, nên `password = "..."` chưa bao giờ được che. Đã sửa.

### 4.3 Vòng agent

Mục này giải thích một lần chạy diễn ra theo từng lượt như thế nào.

Một **lượt** gồm: code gửi toàn bộ hội thoại cho model; model trả về một hay nhiều lời gọi công cụ; code chạy các công cụ đó và nối kết quả vào hội thoại. Lặp lại tới khi `finish` được chấp nhận, hoặc hết ngân sách.

Ví dụ rút gọn trên một fixture nhỏ:

| Lượt | Model gọi | Code trả |
|---|---|---|
| 1 | `list_files` | 5 file được đọc; 1 file test bị loại |
| 2 | `read_file` × 5 | Nội dung 5 file, có số dòng |
| 3 | `submit_findings` (route có prefix sai) | Lỗi: "không có literal '/v2' tại app/main.py:6" |
| 4 | `submit_findings` (đã sửa) | Chấp nhận; kèm tiến độ: còn 0 file chưa đọc |
| 5 | `finish` | Chấp nhận, lần chạy `completed` |

`finish` chỉ được chấp nhận khi đủ 3 điều kiện:

1. Không còn dòng chưa đọc.
2. Mọi tham chiếu đã đủ: model mà route dùng đã được nộp; mọi file đã có vai trò.
3. Mọi **dòng nghi ngờ** đã được xử lý (mục 4.5).

Quá 4 lần bị từ chối thì lần chạy dừng ở trạng thái `partial`, kèm danh sách việc còn dở.

**Ngân sách:** mỗi lần chạy có trần về số lượt, token, thời gian và USD. Chạm trần nào thì dừng `partial`, và kết quả vẫn được xuất cho phần đã biết.

**Rút gọn ngữ cảnh:** hội thoại dài dần qua các lượt. Khi vượt ngưỡng, code thay nội dung các kết quả `read_file` cũ bằng một dòng "đã rút gọn; đọc lại nếu cần". Code chỉ rút gọn những gì model **đã nhận**; một lỗi đầu tiên của bản cũ là rút gọn cả nội dung model chưa thấy, Codex phát hiện và đã sửa. Dữ kiện đã nộp không mất, vì nó nằm trong sổ của code chứ không nằm trong hội thoại.

**Gọi model:** có hai adapter.

| Adapter | Dùng cho | Điểm đáng chú ý |
|---|---|---|
| Chat completions | Groq | Tự giãn nhịp theo hạn mức token/phút; gặp 429 thì chờ; gặp 413 (request quá lớn) thì rút gọn rồi gửi lại |
| Responses API | OpenAI | Cho dùng công cụ và suy luận cùng lúc; gửi `store: false` (yêu cầu không lưu hội thoại; chính sách lưu giữ còn lại do nhà cung cấp quyết); phần suy luận được gửi lại ở dạng mã hóa để model giữ mạch |

Cả hai đều thử lại khi mạng đứt giữa chừng (lỗi `IncompleteRead` từng làm hỏng 4/6 lần chạy) và tính tiền theo bảng giá.

### 4.4 Khuôn dữ liệu agent nộp

Mục này cho thấy agent phải nộp gì cho một route.

Agent không được tự đặt mã hay tạo bằng chứng. Nó chỉ dẫn vị trí `file:dòng`; code tự tạo mã. Ví dụ một route:

```json
{"method": "POST", "handler": "app/api/items.py::create_item",
 "decorator": "app/api/items.py:9-10",
 "application": "app/main.py:5",
 "path_parts": [
   {"kind": "include_prefix", "value": "/api",   "at": "app/main.py:6"},
   {"kind": "router_prefix",  "value": "/v1",    "at": "app/api/__init__.py:5"},
   {"kind": "include_prefix", "value": "/items", "at": "app/api/__init__.py:6"},
   {"kind": "decorator",      "value": "/",      "at": "app/api/items.py:9"}],
 "params": [],
 "request_body": {"models": ["app/schemas.py::ItemIn"], "param": "item", "media_type": "application/json",
                  "required": true, "embedded": false, "at": "app/api/items.py:10", "rule": "fastapi.json_body_media"},
 "response": {"model": "app/schemas.py::ItemOut", "array": false, "at": "app/api/items.py:10",
              "rule": "fastapi.return_annotation_response_model"},
 "status": {"codes": [201], "at": "app/api/items.py:9", "rule": null},
 "dependencies": [],
 "auth": {"unknown": "Không thấy dependency; không kết luận route công khai"}}
```

Các điểm đáng chú ý:

- **`path_parts`:** chuỗi prefix có thứ tự, từ app xuống decorator. Mỗi phần có bằng chứng riêng; code ghép thành `/api/v1/items/`.
- **Prefix không phải literal ngay tại chỗ đăng ký:** prefix lấy từ Settings, hoặc truyền qua hàm bọc như `attach(app, router, prefix="/api/v1")`. Khi đó phần prefix ghi thêm `used_at`: `at` là dòng chứa giá trị, `used_at` là dòng `include_router` thật sự dùng giá trị đó.
- **Không đoán:** không biết được thì ghi `{"unknown": "lý do"}`, ví dụ prefix đọc từ biến môi trường không có giá trị mặc định.

Khuôn tương tự cho model (trường, alias, kiểu, required, nullable), lời gọi HTTP (thư viện, method, đích), vai trò file, giới hạn và "dòng bác bỏ".

### 4.5 Bộ kiểm bằng chứng

Mục này giải thích code từ chối những gì, và những gì code không kiểm được.

| Kiểm | Ví dụ bị từ chối |
|---|---|
| Dòng được dẫn đã thật sự được đọc | Dẫn `main.py:20` khi chưa gọi `read_file` cho dòng đó |
| Literal có nguyên văn tại dòng đó | Prefix ghi `/v2` trong khi dòng 6 viết `prefix="/api"` |
| Đúng loại dòng | Phần `include_prefix` dẫn tới một dòng không có `include_router(` |
| Khoảng decorator là đúng một hàm | Khoảng 9–16 chứa hai `def`, dùng để mượn method của route khác |
| Receiver của decorator không phải đối tượng khác tạo trong cùng file | `@db.get("/fake")` với `db = Registry()` (chỉ kiểm khi đối tượng được tạo trong cùng file; import từ file khác thì chưa kiểm) |
| Status nằm trong decorator của chính route đó | Mượn `status_code=201` của route bên cạnh |
| URL là đối số URL của lời gọi | Lấy URL trong `headers={"Referer": ...}` làm đích |
| Giá trị không chứa bí mật | Nộp URL có mật khẩu thật thay vì bản đã che |
| Vai trò có dấu hiệu tại dòng dẫn | Gán "Cấu hình" cho dòng không có `BaseSettings`/`os.environ` |
| Thứ tự vai trò (chỉ cưỡng chế cho Điểm vào, Route, Model bảng; agent có thể giải thích bằng `not_signal`) | File có `FastAPI(` mà gán "Khác" (phải là "Điểm vào") |
| Quy tắc suy luận nằm trong danh sách cố định | `"rule": "fastapi.my_guess"` |

**Danh sách quy tắc suy luận** (12 quy tắc), ví dụ:

- `fastapi.default_status_200`: không khai `status_code` thì status là 200.
- `pydantic.v2_required_no_default`: Pydantic v2, trường không có default là bắt buộc kể cả khi cho phép `None`.
- `pydantic.v1_optional_not_required`: Pydantic v1, trường `Optional` không có default thì không bắt buộc.

Fact nào có giá trị dùng quy tắc thì mang nhãn `inferred` kèm tên các quy tắc; nhãn đặt ở mức cả fact (route hoặc model), chưa gắn riêng cho từng trường. Fact không dùng quy tắc nào mang nhãn `exact`.

**Dòng nghi ngờ:** code quét source bằng biểu thức chính quy, tìm các dòng *trông giống*:

- decorator route;
- `add_api_route`/`add_route`/`add_websocket_route`;
- lời gọi `.get/.post/.request` trong file có import `httpx`/`requests`/`aiohttp`.

Mỗi dòng như vậy phải có một mục agent đã nộp, hoặc một mục `dismissed` kèm lý do (ví dụ "db.get là truy vấn CSDL, không phải HTTP"). Cơ chế này chống bỏ sót. Code không tự tạo route từ biểu thức chính quy; nó chỉ bắt agent phải xem xét.

**Giới hạn của bộ kiểm:** code kiểm được "dẫn đúng chỗ" nhưng không kiểm được "hiểu đúng nghĩa". Ví dụ agent dẫn đúng dòng `price: float | None = None` nhưng ghi `required: true`: bộ kiểm không bắt được. Phần nghĩa do đáp án độc lập đo (mục 5).

### 4.6 Từ dữ kiện tới tài liệu

Mục này giải thích dữ kiện đã kiểm trở thành file như thế nào.

1. Mỗi mục được chấp nhận thành một **fact** theo định dạng có sẵn của dự án (API-004). Mã fact là băm SHA-256 của snapshot, loại và vị trí, nên cùng đầu vào cho cùng mã.
2. Mỗi `file:dòng` thành một **evidence** có mã riêng, kèm mã băm file.
3. `render.py` viết file API: bảng endpoint, bảng model, truy vết (mã fact đầy đủ của route và model), khối OpenAPI 3.1. Route không biểu diễn được trong OpenAPI (ví dụ path `unknown`) bị bỏ khỏi khối, kèm lý do.
4. Trước khi ghi file, `check_doc` đọc ngược một số trường của bảng và khối OpenAPI vừa viết (method, path, status, request body, response mảng) và so với fact. Lệch thì file bị đánh `FORMAT_INVALID` và không xuất. Bước này không kiểm mọi trường, và pipeline không chạy bộ kiểm hợp lệ OpenAPI (validator chỉ có trong test).
5. Mọi file được ghi vào thư mục tạm rồi đổi tên một lần; lỗi giữa chừng không để lại output dở dang.

### 4.7 Đối chiếu kiến trúc (AC-04)

Mục này nói tool so tài liệu với dữ liệu kiến trúc thế nào.

Khi được cấp `archdia.json` của bước FR-028, tool so:

- tập route trong tài liệu với tập route trong `archdia.json`, theo method, path, file và dòng;
- component sở hữu route;
- snapshot của hai bên.

`archdia.json` không ghi snapshot thì kết quả là `not_evaluated`; khác snapshot thì `failed`. Đã có code và test trên dữ liệu giả; chưa chạy với `archdia.json` thật vì bước FR-028 chưa cấp.

## 5. Đo độ chính xác

Mục này giải thích vì sao kết quả đáng tin, và tin tới mức nào.

### 5.1 Ba nguồn đáp án

| Nguồn | Ai lập | Phủ gì | Độ tin |
|---|---|---|---|
| 6 fixture + gold (`slice/tests/fixtures/fr029/`) | Agent G (Claude), không được đọc code của luồng agent; route, tham số và model đối chiếu với `app.openapi()` chạy thật trong môi trường riêng | Đủ 8 nhóm: route, tham số, model, HTTP, vai trò, giới hạn | Codex review một lượt; chưa có người thật review |
| Golden v1, 19 case phát triển | Bộ có sẵn của nhóm | Chỉ route | Trạng thái `candidate`, chưa có người review |
| Golden v1, 4 repo thật | Nhóm, mỗi repo 2 bản lập độc lập + giám khảo | Route, tên model, lời gọi ra ngoài | **Khiêm đã duyệt** (APPROVAL-golden-v1-2026-10-04) |

Golden v1 4 repo chia vai trò:

- **"Chỉnh prompt"** (`full-stack`, `igorbenav`): được dùng lỗi ở đây để sửa prompt.
- **"Đo"** (`teamhide`, `fastapi_best_architecture`): chỉ dùng để đo; không sửa prompt theo lỗi của chúng.

Tài liệu này giữ đúng quy định đó: lỗi tìm được ở `teamhide` chỉ được ghi nhận, không dùng để sửa prompt.

**Mỗi nguồn kiểm được gì.** Đây là điểm dễ hiểu nhầm nhất: đủ 8 nhóm yêu cầu chỉ được đo theo đáp án trên fixture; trên repo thật, đáp án có người duyệt chủ yếu chỉ phủ route.

| Nguồn | Route | Tham số, trường model, status | HTTP | Vai trò file | Giới hạn |
|---|---|---|---|---|---|
| 6 fixture + gold | Có | Có | Có | Có | Có |
| Golden v1, 19 case dev | Có | Không | Không | Không | Không |
| Golden v1, 4 repo thật | Có | Chỉ tên model | Gold có 3 lời gọi, đều ở `fastapi_best_architecture`; lần chạy partial được 0/3 | Không | Không |
| Chấm đa model (không phải người) | Có | Có | Có | Có | Có; repo thật chỉ kiểm mẫu |

### 5.2 Bộ chấm

So output với đáp án theo khóa:

- Route: fixture theo (method, path, dòng decorator), có so thêm handler như một thuộc tính; golden v1 theo (method, path, handler).
- Model theo (file, tên); lời gọi HTTP theo `file:dòng`; vai trò theo file.

Kết quả gồm:

- **TP** (tìm đúng), **FP** (tìm thừa), **FN** (bỏ sót);
- với mục tìm đúng: đếm riêng từng thuộc tính sai, ví dụ prefix, required, nullable, status, đích HTTP.

`unknown` chỉ được tính là đúng khi đáp án cũng ghi `unknown` (ví dụ prefix đọc từ biến môi trường không có giá trị mặc định); nếu đáp án có giá trị thì `unknown` là sai.

Bộ chấm fixture **không** chấm: dependency/auth, nullable của tham số, nhãn `exact`/`inferred`, bằng chứng của từng trường, AC-04, AC-06. Vì vậy "0 lỗi" chỉ nghĩa là 0 lỗi trên các trường được chấm. Tỷ lệ `exact` sai (ngưỡng ≤5% của NFR-ACC-002) **chưa đo**.

### 5.3 Chấm đa model, không xem đáp án

Đáp án không phủ hết: golden v1 không có tham số, trường model hay vai trò file. Vì vậy có thêm các người chấm đọc source và tài liệu sinh ra, **không xem đáp án**:

| Người chấm | Hãng |
|---|---|
| Codex `gpt-6-astra`, suy luận cao | OpenAI |
| Claude Opus | Anthropic |
| Claude Sonnet | Anthropic |

- Mọi người chấm kiểm cùng một mẫu, chọn cố định bằng seed: repo nhỏ thì kiểm hết; repo lớn thì kiểm 10 route và 15 file.
- Lỗi được ≥2 người chấm cùng báo thì coi là **xác nhận**. Lỗi chỉ 1 người báo thì xem lại với source.
- Lưu ý: model chạy agent (`gpt-6-luna`) và Codex cùng hãng OpenAI; hai người chấm Claude là khác hãng.

## 6. Hai nhà cung cấp model

Mục này giải thích vì sao bỏ Groq và chọn OpenAI `gpt-6-luna`.

**Groq `gpt-oss-120b`, gói miễn phí:** không dùng được.

- Giới hạn 8.000 token mỗi phút, tính cả phần trả lời, mà riêng prompt và mô tả công cụ đã chiếm khoảng 3.000 token. Lịch sử phải rút gọn liên tục, nên agent quên file đã đọc.
- Lượt đầu: agent đọc hết rồi bị lỗi 413 trước khi kịp nộp gì.
- Lượt cuối: cả 6 fixture dừng vì lỗi 429; 3 ca dừng trước lượt đầu, 3 ca sau 1 lượt.
- Lần duy nhất chạy trọn (`pydantic_v1`) sai đúng ca khó: luật `Optional` của Pydantic v1.

**OpenAI:**

- Khóa dùng là biến `open_ai` trong `D:/VSF/VSF-L3 Generator/.env`, theo phép của người dùng. Khóa không bị in ra hay ghi vào file nào.
- `gpt-6.1-sol` không cho dùng công cụ cùng suy luận trên chat completions, nên phải viết thêm adapter Responses API.
- Người dùng chọn dòng luna/terra. Mình chạy `gpt-6-luna` (0,10 USD / 1 triệu token đầu vào, 0,50 USD / 1 triệu token đầu ra), suy luận mức `medium`.

## 7. Kết quả đo

Mục này liệt kê mọi lần chạy, theo thứ tự thời gian.

### 7.1 Fixture (tập phát triển)

| Lần chạy | Prompt | Kết quả | Chi phí |
|---|---|---|---|
| `luna1` | v3 | 2/6 xong; 4 hỏng vì mạng đứt (chưa có thử lại) | 0,005 USD |
| `luna2` | v4 | 6/6 xong; 7 route thừa do bản route nộp sớm "chưa gắn app"; 3 thuộc tính sai | 0,019 USD |
| `luna3` | v5 | 18/18 lần (6 fixture × 3); tìm đủ mọi mục, nhưng 1 lần có 2 lỗi đích HTTP (ghi khóa cấu hình dạng `settings.X`) | 0,047 USD |
| `luna4` | v6 | 6/6 tìm đủ mọi mục; 2 lỗi đích HTTP (`settings.X`); sau đó code tự chuẩn hóa | 0,016 USD |
| `luna5` | v8 | **18/18 lần, 0 lỗi** trên mọi mục và thuộc tính gold chấm | 0,057 USD |

Prompt đã được sửa qua nhiều vòng dựa trên chính các fixture này, nên đây là kết quả trên tập phát triển, không phải bằng chứng cho repo lạ.

### 7.2 Golden v1, 19 case phát triển (chỉ route)

| Lần chạy | TP | FP | FN | Chi phí |
|---|---|---|---|---|
| `golden-luna` (prompt v5) | 39 | 3 | 1 | 0,070 USD |
| `golden-luna2` (prompt v7) | 40 | 2 | 0 | 0,074 USD |

Hai route thừa ở lần sau đều chưa phải lỗi chắc chắn của agent:

- `orders-wrapper-fake`: router không được gắn vào app nào. Agent ghi route với path `unknown`; gold không ghi route. Chờ quyết định ở mục 11.
- `dispatch-case-read`: route `/healthcheck` có thật (`api.py:256`, khai `include_in_schema=False`) nhưng gold không ghi. Có thể gold thiếu.

### 7.3 Golden v1, 4 repo thật (Khiêm duyệt)

| Repo | Vai trò | Route | Tên model trên route đúng | Trạng thái | Chi phí |
|---|---|---|---|---|---|
| `teamhide` (84 file đọc được) | đo | 5/5, 0 thừa | 4/5 (lệch còn lại do bộ chấm, đã sửa) | completed | 0,048 USD |
| `full-stack-fastapi-template` (22 file đọc được) | chỉnh prompt | 23/23, 0 thừa | 19/23 | completed | 0,019 USD |
| `igorbenav-FastAPI-boilerplate` (112 file đọc được) | chỉnh prompt theo golden v1; **kín, cỡ vừa theo OBS-001** | 30/34, 0 thừa | 6/30 | partial (chạm trần 0,5 USD) | 0,49 USD |
| `fastapi_best_architecture` (296 file đọc được) | đo; **kín, cỡ lớn theo OBS-001** | **1/139** | 0/1 | partial (chạm trần 0,8 USD) | 0,77 USD |

4 chỗ lệch tên model ở `full-stack`:

| Chỗ lệch | Phân loại | Đã xử lý |
|---|---|---|
| `DELETE /users/me`: agent bỏ qua `response_model=Message` trong decorator | Lỗi thật của agent | Đã sửa prompt |
| `bool` không ghi được | Khuôn dữ liệu chưa hỗ trợ kiểu không phải model | Đã sửa |
| `Any` không ghi được | Cùng nguyên nhân với dòng trên | Đã sửa |
| Request form của OAuth2 ghi `unknown` có lý do | Hợp lệ theo FR-029 | Giữ nguyên |

### 7.4 Vì sao repo lớn thất bại

Mục này phân tích thất bại ở `fastapi_best_architecture`, theo số liệu của lần chạy.

- Agent đọc 143/296 file và nộp 142 vai trò file, nhưng chỉ 1 route.
Hai giả thuyết dưới đây khớp với số liệu, nhưng **chưa được kiểm bằng lần chạy đối chứng**:

- Giả thuyết 1, thứ tự làm việc: prompt bảo "đọc file nào nộp file đó". Vai trò file nộp được ngay, còn route phải chờ biết đủ chuỗi `include_router` từ app xuống, nên bị dồn lại cuối.
- Giả thuyết 2, chi phí ngữ cảnh: 175 lượt, tổng 22 triệu token đầu vào, trung bình khoảng 125.000 token mỗi lượt vì hội thoại giữ quá nhiều nội dung cũ. Tiền hết trước khi kịp nộp route.
- Đã sửa (prompt v11, **chưa chạy lại**):
  - đọc điểm vào và các file đăng ký router trước, rồi nộp route ngay khi đọc file route;
  - ngưỡng ngữ cảnh giảm từ 600.000 xuống 150.000 ký tự.

  Ước tính chi phí mỗi lượt giảm khoảng 4 lần (chưa đo).

### 7.5 Chấm đa model

| Đối tượng chấm | Lỗi được ≥2 người chấm xác nhận | Ghi chú |
|---|---|---|
| 6 fixture (`luna5`) | 1: README hiện `->` thành `-&gt;` trong code (đã sửa) | Ngoài ra 3 điểm "chưa chắc" của 1 người (2 đã sửa) và 1 câu hỏi cần quyết định |
| `teamhide` (mẫu 5 route, 15 file) | 1: `permission.py` phải là Service (nằm trên đường gọi qua `Depends`) | Cả 3 người chấm đều báo. Repo "đo" nên chỉ ghi nhận, không sửa prompt theo nó |
| `full-stack` (mẫu 10 route, 15 file) | 4: bỏ qua `response_model=Message` (3/3); response `HTMLResponse` chưa ghi (3/3); `utils.py` gửi SMTP phải là Hạ tầng (2/3); kiểu `uuid`/`datetime`/`email` mất định dạng (2/3) | Đã sửa prompt (repo "chỉnh prompt") và thêm kiểu `uuid`, `datetime`, `date`, `email` vào khuôn dữ liệu (prompt v12, chưa đo lại). Không sửa: OpenAPI `security` (FR cho phép auth `unknown`), SMTP vào phần giới hạn (FR-029 chỉ yêu cầu ghi thư viện HTTP khác) |

## 8. Các lỗi đã tìm và sửa

Mục này liệt kê lỗi theo người tìm ra, để thấy giá trị của kiểm chéo.

| Lỗi | Ai tìm | Loại |
|---|---|---|
| Mẫu che mật khẩu hỏng (có từ trước) | Claude khi viết test | Bảo mật |
| Rút gọn cả nội dung model chưa nhận, khiến tool báo "đã đọc đủ" sai | Codex review code | Độ phủ |
| Giá trị `unknown` hợp lệ làm crash | Codex review code | Ổn định |
| Thiếu model làm crash khi chạy dở | Codex review code | Ổn định |
| Body Form/File bị bộ kiểm cuối từ chối, mất cả file API | Codex review lượt 2 | Đầu ra |
| `archdia.json` thiếu snapshot vẫn ra `passed` | Codex review code | AC-04 |
| Bản route "chưa gắn app" sót lại | Bộ chấm (7 route thừa) | Điều phối |
| Bộ kiểm chặn câu trả lời đúng khi prefix truyền qua hàm bọc | Golden v1 dev | Bộ kiểm |
| Thiếu dependency, thiếu tham số body, thiếu truy vết model | Codex review mù | Trình bày |
| Nhãn `inferred` không ghi tên quy tắc | Codex review mù | AC-03 |
| Response kiểu `bool`/`Any` không ghi được | Golden v1 4 repo | Khuôn dữ liệu |
| Groq chặn User-Agent mặc định (403); mạng đứt giữa chừng | Lần chạy thật | Hạ tầng gọi model |

### 8.1 Kiểm toán độc lập của Codex

Mục này ghi kết quả kiểm toán toàn bộ (code, test, số đo, báo cáo) do Codex `gpt-6-astra` mức suy luận cao làm, ở chế độ chỉ đọc. Kết luận của Codex: **chưa đủ và chưa đúng với toàn bộ yêu cầu**. Claude đã tái hiện lại các lỗi nặng (F01–F04, F14) trước khi sửa. Bản kiểm toán đầy đủ: `ket-qua-chay/fr029-pilot-20261007/reviews/codex_audit_out.md`.

| Mã | Lỗi | Trạng thái |
|---|---|---|
| F01 | Bí mật dạng `password: str = "..."` không được che | Đã sửa |
| F02 | Bí mật nằm lại trong danh sách mục bị từ chối, rồi ghi vào `result.json` | Đã sửa: chỉ giữ lỗi đã che, không giữ giá trị |
| F03 | Prefix đảo thứ tự vẫn được nhận; nộp lại bản đúng thì giữ cả hai; prefix rỗng che được prefix thật | Một phần: nộp lại thì thay bản cũ; prefix rỗng bị chặn. Thứ tự prefix vẫn chỉ đo được bằng gold |
| F04 | Tham số path ghi `required=false`, khiến OpenAPI không hợp lệ | Một phần: chặn ca này. Pipeline vẫn chưa chạy bộ kiểm hợp lệ OpenAPI |
| F05 | HTTP giả (`db.get`) và URL lấy nhầm từ `headers` | Một phần: URL phải là đối số đầu. `db.get` trong file có import httpx vẫn chỉ được bắt bằng gold và người chấm |
| F06 | Client tạo ở file khác bị từ chối | Đã sửa: dẫn thêm `client_at` |
| F07 | Bằng chứng auth/vai trò có thể là dòng không liên quan | **Còn mở**, giới hạn của hướng agent thuần |
| F08 | Bác bỏ được lời gọi `add_api_route` thật | Đã sửa: không cho bác bỏ trên app/router tạo trong file |
| F09 | Mất lý do `unknown` của required ở body | Đã sửa |
| F10 | Phạm vi bỏ sót import tương đối; `venv/` bị loại vô điều kiện | Một phần: sửa import tương đối; `venv/` là lỗi có từ trước của `snapshot.py`, chưa sửa |
| F11 | Component trùng tên hoặc trùng id | Đã sửa: từ chối đầu vào |
| F12 | `archdia.json` không kiểm định dạng; sơ đồ không kiểm snapshot | Một phần: kiểm định dạng; sơ đồ chưa kiểm |
| F13 | Vai trò không có bằng chứng (file rỗng bị xếp vào component thường) | Đã sửa cả script chạy thử lẫn bộ kiểm |
| F14 | Dữ liệu sai kiểu gây crash | Đã sửa |
| F15 | Bộ chấm không chấm handler, dependency, nullable tham số, nhãn | Một phần: thêm handler; các trường còn lại ghi rõ là chưa chấm (mục 5.2) |
| F16 | Case chạy lỗi không bị tính là bỏ sót | Đã sửa |
| F17 | Gộp kết quả chấm coi hai lỗi khác trường là "đồng thuận" | Đã sửa: khóa gộp có thêm trường |
| F18 | Thử lại trên Responses API nhân đôi kết quả công cụ | Đã sửa |
| F19 | Trần USD không có tác dụng khi thiếu bảng giá | Đã sửa: dừng ngay với lỗi rõ |
| F20 | Thư mục output không rỗng chỉ bị phát hiện sau khi đã gọi model | Đã sửa: kiểm trước |

Các bài chấm đa model và review của Codex được lưu ở `ket-qua-chay/fr029-pilot-20261007/reviews/`.

## 9. Kiểm thử tự động

Mục này nói phần test chạy không cần model.

- 239 test chạy offline. 238 qua; lỗi duy nhất là `test_gateway.test_unknown_ids_are_dropped`, có từ trước. Log: `ket-qua-chay/fr029-pilot-20261007/tests-after-audit.log`.
- Test mới (`slice/tests/test_docagent.py`) dùng "provider giả": một kịch bản gọi công cụ viết sẵn. Chúng kiểm phạm vi, độ phủ, che bí mật, từng luật của bộ kiểm, ngân sách, rút gọn ngữ cảnh, giãn nhịp, adapter Responses, bộ chấm, và có hồi quy cho từng lỗi Codex tìm ra.
- Test offline chứng minh cơ chế chạy đúng; chúng không chứng minh model thật đọc đúng. Phần đó do mục 7 đo.

## 10. Trạng thái 8 AC

| AC | Nội dung | Trạng thái |
|---|---|---|
| 01 | Route: method, path đầy đủ, handler, bằng chứng | **Đạt một phần.** Đúng trên fixture, golden dev, 2 repo lộ; repo kín vừa 30/34 (partial); repo kín lớn 1/139. Thứ tự prefix chỉ đo bằng gold (F03). Chưa đo trên 3/4 repo nghiệm thu |
| 02 | Tham số, model, kiểu, required, nullable, status | **Đạt một phần.** Đạt trên fixture với các trường được chấm; trên repo thật chỉ đo được tên model: 5/5, 19/23, **6/30 ở repo kín vừa** |
| 03 | `unknown` kèm lý do, `inferred` kèm tên quy tắc | **Đạt một phần.** Có và được kiểm; nhãn đặt ở mức fact, chưa gắn từng trường; tỷ lệ `exact` sai chưa đo |
| 04 | Đối chiếu `archdia.json` | **Chưa đánh giá.** Có code và test; chưa có file thật từ FR-028 |
| 05 | Loại route test; ghi `add_api_route` vào giới hạn | **Đạt một phần.** Đạt trên fixture; chưa có gold phạm vi trên repo thật |
| 06 | README đủ mục | **Đạt một phần.** Đủ mục, trừ sơ đồ: chưa được cấp |
| 07 | Vai trò từng file | **Chưa đạt trên repo thật.** Đạt trên fixture; trên repo thật có vai trò không bằng chứng (đã sửa F13, chưa đo lại), lỗi Service qua `Depends`, Hạ tầng SMTP |
| 08 | Lời gọi HTTP ra ngoài | **Đạt một phần.** Đạt trên fixture; repo kín lớn 0/3 (lần chạy partial); chưa có số đo trên repo nghiệm thu |

## 11. Giới hạn, việc còn lại, quyết định chờ

Mục này nói rõ phần chưa chứng minh được.

**Giới hạn:**

- Repo lớn (khoảng 300 file) chưa chạy được trong trần chi phí. Bản sửa đã viết, chưa đo.
- Gold fixture do agent viết và Codex review; gold golden v1 dev chưa có người review. Chỉ golden v1 4 repo có người duyệt, và nó chỉ phủ route và tên model.
- Mỗi cấu hình trên repo thật mới chạy 1 lần; độ dao động chỉ mới đo trên fixture.

**Quyết định chờ người dùng:**

1. Route khai trong file production mà router không được gắn vào app nào: giữ (path `unknown`) hay loại? FR-029 chỉ loại route *khai trong file test*; kế hoạch A05 và gold golden v1 thì loại. Câu hỏi này đã xuất hiện 4 lần.
2. `HTTPException(404)` hay `Response(status_code=200)` trong thân hàm có tính là status "khai trong code" không?
3. Có nâng trần chi phí không? Cần chạy 4 repo kín nhỏ và vừa theo OBS-001 (3 repo chưa chạy lần nào) và chạy lại `igorbenav` bằng bản hiện tại. Đã tiêu khoảng 1,62/2 USD theo ước tính.

**Chưa làm:** retry riêng cho bộ tài liệu FR-029; commit/push.

## 12. Thuật ngữ

| Từ | Nghĩa |
|---|---|
| Agent | Mô hình ngôn ngữ được dùng công cụ (đọc file, nộp kết quả) qua nhiều lượt |
| Lượt | Một lần gửi hội thoại cho model và nhận lại lời gọi công cụ |
| Fixture | Repo nhỏ dựng sẵn để kiểm một nhóm trường hợp |
| Gold / đáp án | Kết quả đúng, lập độc lập với phần được kiểm |
| Oracle | Chạy thật `app.openapi()` của FastAPI để lấy đáp án |
| Fact | Một dữ kiện đã qua kiểm, có mã và bằng chứng |
| Evidence | Vị trí `file:dòng` chứng minh một giá trị |
| TP / FP / FN | Tìm đúng / tìm thừa / bỏ sót |
| `exact` / `inferred` / `unknown` | Đọc thẳng từ code / suy từ quy tắc mặc định có tên / không xác định được, kèm lý do |
| Dòng nghi ngờ | Dòng trông giống route hoặc lời gọi HTTP, mà agent phải xử lý hoặc bác bỏ kèm lý do |
| Độ phủ | Phần dòng source model đã thật sự nhận |

## 13. Chạy lại

```powershell
# test offline
scripts/.venv/Scripts/python.exe -m unittest discover -s slice/tests
# 6 fixture, chấm với gold (cần OPENAI_API_KEY)
scripts/.venv/Scripts/python.exe slice/tools/fr029_pilot.py --out <thư mục mới> --base-url https://api.openai.com/v1 --api responses --model gpt-6-luna --key-env OPENAI_API_KEY --max-request-tokens 0 --tokens-per-minute 0 --max-turn-read-chars 0 --max-context-chars 1000000 --max-output-tokens 16000 --price 0.1 0.01 0.5 --max-cost-usd 0.5
# golden v1 dev, chỉ route
scripts/.venv/Scripts/python.exe slice/tools/fr029_golden_routes.py --golden-root "D:/VSF/VSF-L3 Generator" --out <thư mục mới> --model gpt-6-luna --key-env OPENAI_API_KEY --price 0.1 0.01 0.5
# golden v1 4 repo thật
scripts/.venv/Scripts/python.exe slice/tools/fr029_golden4.py --golden-repo D:/VSF/l3-generator-golden-v2 --out <thư mục mới> --model gpt-6-luna --key-env OPENAI_API_KEY --price 0.1 0.01 0.5 --max-cost-usd 1
# chọn mẫu và gộp kết quả chấm đa model
scripts/.venv/Scripts/python.exe slice/tools/fr029_sample.py <thư mục output>/result.json
scripts/.venv/Scripts/python.exe slice/tools/fr029_grade_merge.py <file JSON của từng người chấm> ...
```
