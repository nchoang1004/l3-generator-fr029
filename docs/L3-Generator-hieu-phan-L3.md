# Hiểu phần L3 — tài liệu tự học

Ngày 02/10/2026. Viết cho Hoàng, để tự hiểu và tự giải thích phần L3. Số liệu lấy từ code, PRD revision 29 và các lần chạy thật trên 4 repo.

Đọc theo thứ tự. Phần 1–4 là bức tranh chung. Phần 5–9 là cách chạy chi tiết. Phần 10–14 là tiến độ, khó khăn và liên hệ với phần của Khiêm. Cuối file có bảng thuật ngữ và câu hỏi hay gặp.

---

## 1. L3 là gì

Dự án L3 Generator đọc code của một dự án rồi viết tài liệu kiến trúc ban đầu. Có hai phần:

| Phần | Là gì | Ai |
|---|---|---|
| Sơ đồ khối (mức L2) | Gom file thành các khối (component), vẽ khối nào gọi khối nào | Khiêm |
| Tài liệu L3 | Bộ "contract" của hệ thống: các API, các bảng dữ liệu, các sự kiện, chia theo khối sở hữu | Hoàng |

- "Contract" nghĩa là bản mô tả cái mà hệ thống cam kết đưa ra ngoài: API nhận gì, trả gì; bảng có cột gì; sự kiện gửi đi topic nào.
- Định dạng theo mẫu `tech-specs/` của mentor (execution guide mục A.1 và B.10).
- Phase đầu chỉ cam kết Python/FastAPI.
- Phần L3 **chỉ đọc code**, không chạy code của repo, và **không dùng AI**.

## 2. PRD nói gì về L3

PRD: `.aide/product/prd/PRD-L3GEN-2609-001.md`, revision 29, còn nháp, Scope Gate chưa ký. Người ký: Khiêm. Người review và nghiệm thu: Hoàng. Mentor: cố vấn.

### 2.1 Mục tiêu kinh doanh (nguyên văn mục II.3)

Bốn mục tiêu, xếp theo thứ tự: sinh ra được gì, rồi mới tới tin được tới đâu.

| Goal key | Mục tiêu | Liên kết KPI |
|---|---|---|
| GOAL-L3GEN-004 | Dựng được sơ đồ cấu trúc hệ thống ở mức application/component, phản ánh code đang chạy chứ không phải tài liệu cũ | KPI-L3GEN-006 |
| GOAL-L3GEN-005 | Mọi kết luận trên sơ đồ và tài liệu đều lần ngược được về đúng đoạn source sinh ra nó, để người đọc tự kiểm chứng thay vì phải tin | KPI-L3GEN-007 |
| GOAL-L3GEN-006 | Từ repo đó sinh ra tài liệu L3 đủ để người mới đọc hiểu hệ thống mà không cần mở source | KPI-L3GEN-008 |
| GOAL-L3GEN-007 | Nói thật về giới hạn của chính mình: tách rõ phần đọc trực tiếp từ bằng chứng, phần suy ra, và phần không kết luận được, để người đọc biết chỗ nào tin ngay và chỗ nào phải tự kiểm | KPI-L3GEN-009, KPI-L3GEN-010 |

Phần L3 phục vụ trực tiếp nhất GOAL-006, sau đó là GOAL-005 và GOAL-007.

### 2.2 Năm chỉ số (mục II.4)

| KPI | Tên | Target |
|---|---|---|
| 006 | Độ đúng sơ đồ cấu trúc | Đạt NFR-ACC-002 với mẫu đủ |
| 007 | Độ đúng bằng chứng | 100%, không ngoại lệ |
| 008 | Độ đúng dữ kiện L3 (route, model, bảng, HTTP, config, event, thư viện) | Đạt NFR-ACC-002 |
| 009 | Nhãn mức chắc chắn có đúng không | Đạt ngưỡng NFR-ACC-002 với mẫu đủ |
| 010 | Công cụ có tự báo phần nó không đọc được không | 100% |

- Ngưỡng của NFR-ACC-002: P và R ≥ 80% mỗi loại; nhãn `exact` mà sai ≤ 5%.
- P (precision): trong những gì công cụ ghi ra, bao nhiêu phần đúng. R (recall): trong những gì đúng ra phải có, công cụ tìm được bao nhiêu phần.
- Cỡ mẫu tối thiểu (OBS-001): 100 route, 20 bảng, 30 HTTP, 30 config, 20 sự kiện. Chưa đủ thì ghi `not_evaluated`, không báo phần trăm.

### 2.3 Chín tính năng (mục IV.3), 36 AC

| FR | Tên | Mốc | Ai |
|---|---|---|---|
| 019 | Nhận source và chạy phân tích | M1 cho CLI; M2 cho web | Hoàng |
| 020 | Xác định phạm vi phân tích | M1 | Hoàng |
| 021 | Trích dữ kiện code | M1 bốn loại đầu; M3 ba loại sau | Hoàng |
| 022 | Dựng component và quan hệ kiến trúc | M2 | Khiêm |
| 023 | Bằng chứng và nhãn mức chắc chắn | M1 | Chung |
| 024 | Công bố giới hạn của lần chạy | M1 | Chung |
| 025 | Xuất kết quả | M1; M2 khi có component | Hoàng |
| 026 | Khám phá kết quả trên web | M2 | Hoàng |
| 027 | Sinh tài liệu L3 contract | M1 API, TBL; M3 EVT | Hoàng |

Cột "Ai" là cách nhóm chia việc, không phải nội dung PRD.

### 2.4 Năm NFR, con số cần nhớ

| NFR | Con số |
|---|---|
| ACC-002 Độ đúng | P, R ≥ 80%; bằng chứng 100%; `exact` sai ≤ 5% |
| ABST-002 Mức trình bày | Sơ đồ ≤ 50 nút, mức khối; lời gọi chưa rõ đích không vẽ thành cạnh |
| AI-002 AI | Model chỉ nhận dữ kiện đã trích; Groq `gpt-oss-120b` và Gemini `gemini-3.5-flash`, gói miễn phí; đọc thêm code tối đa 6 lần mỗi phạm vi |
| SEC-002 An toàn | Chỉ đọc; ZIP ≤ 100 MB nén, ≤ 500 MB giải nén, ≤ 50.000 file; kết quả hết hạn sau 24 giờ |
| OPS-001 Vận hành | Phân tích ≤ 60 giây cho 5.000 dòng; ≤ 2 GiB; một lần chạy ≤ 30 phút; mỗi lúc một lần chạy |

### 2.5 Ràng buộc chính (mục III.3)

1. Chỉ đọc. Không chạy, không import, không sửa repo đầu vào.
2. Kết luận nào cũng có bằng chứng là dòng code thật, do code kiểm.
3. Không đổi `inferred` thành `exact` để trông chắc hơn.
4. Model chỉ dùng gói miễn phí, trần chi phí 0 đồng.
5. Kết quả cho người đọc dừng ở mức khối.

## 3. Đầu vào và đầu ra

**Đầu vào:** một repo Python FastAPI. Web nhận file ZIP. Dòng lệnh nhận thư mục kèm file membership (file nào thuộc khối nào).

**Đầu ra:**

```
<thư mục kết quả>/
  README.md                                   mục lục, sơ đồ khối, giới hạn
  result.json                                 toàn bộ dữ kiện và bằng chứng, cho máy đọc
  manifest.json                               mã hash của từng file
  architecture.mmd, architecture.svg          sơ đồ khối
  tech-specs/
    <KHỐI>/
      api/API-<HỆ THỐNG>-<KHỐI>-v1.md          tài liệu API
      schema/TBL-<HỆ THỐNG>-<KHỐI>.md          tài liệu bảng
      events/EVT-<HỆ THỐNG>-<KHỐI>-<topic>.md  tài liệu sự kiện
```

## 4. Luồng chạy từ đầu đến cuối

```
Bước 0  Gửi ZIP          web.py, engine.py
Bước 1  Nhận file        snapshot.py
Bước 2  Chọn file        snapshot.py
Bước 3  Đọc code         pyindex.py, extract.py      ← bước chính
Bước 4  Chia khối        model.py                     (cách chia do phần của Khiêm cung cấp)
Bước 5  Tự kiểm          verify.py
Bước 6  Viết tài liệu    render.py
Bước 7  Xem trên web     engine.py, web.py, ui/app.js
```

| Bước | Làm gì | Đầu ra | Sai thì |
|---|---|---|---|
| 0 | Kiểm file là ZIP, ≤ 100 MB; lấy tên file làm tên repo; tạo lần chạy, xếp hàng | Lần chạy "đang chờ" | Báo lỗi ngay |
| 1 | Đọc ZIP trong bộ nhớ; chặn `../`, symlink, file có mật khẩu, quá 500 MB hoặc 50.000 file; tính mã hash từng file | Snapshot | Lần chạy thất bại, có lý do |
| 2 | Giữ `.py`, `pyproject.toml`, `requirements*.txt`; ghi file bị bỏ kèm lý do | Phạm vi đã xét | Không có `.py` thì thất bại |
| 3 | Đọc cây cú pháp, rút dữ kiện (phần 5) | Tập dữ kiện kèm bằng chứng | File lỗi cú pháp: ghi `PARSE_FAILED`, đọc tiếp |
| 4 | Nhận membership; gắn route, bảng vào khối sở hữu; dựng cạnh từ lời gọi đã nối | Khối, cạnh, chủ sở hữu | Không có membership thì thất bại (D-03 chưa chốt) |
| 5 | Kiểm từng bằng chứng và giá trị với code gốc (phần 7) | Dữ kiện đã kiểm, danh sách giới hạn | Bằng chứng sai: dừng cả lần chạy. Giá trị sai: thành "chưa biết" |
| 6 | Viết file API, TBL, EVT, README, JSON, sơ đồ; đọc lại để so (phần 8) | Các file tải về | File lệch: riêng file đó lỗi, có nút "Thử lại" |
| 7 | Hiện kết quả, mở bằng chứng, tải file | Trang web | |

Trên 4 repo, bước 3 đến 6 mất 0,4–0,6 giây mỗi repo.

## 5. Bước 3 — đọc code, chi tiết

### 5.1 `ast` là gì

`ast` là thư viện có sẵn của Python. Nó biến một file code thành **cây cú pháp**: cho biết đâu là hàm, đâu là decorator, đâu là chuỗi chữ, mỗi mảnh ở dòng nào.

```python
@user_router.post(                      # dòng 43
    "/login",                           # dòng 44
    response_model=LoginResponse,       # dòng 45
)
@inject
async def login(request: LoginRequest): # dòng 48
```

thành:

```
Hàm "login"                                (dòng 48)
├── Decorator: gọi user_router.post        (dòng 43)
│   ├── đối số đầu: chuỗi "/login"         (dòng 44)
│   └── response_model = LoginResponse     (dòng 45)
└── Tham số "request", kiểu LoginRequest
```

Khác với tìm chữ bằng `Ctrl+F`: cây cho biết chữ `"/login"` này là đường dẫn của route gắn trên hàm `login`, không phải chuỗi trong comment hay log.

### 5.2 Thứ tự công việc trong bước 3

| # | Việc | Ghi chú |
|---|---|---|
| 1 | Biến từng file `.py` thành cây | Lỗi cú pháp: `PARSE_FAILED` |
| 2 | Lập bảng tên | Đọc mọi `import`, kể cả trong hàm, trong `try`, `import *`, `__init__.py` import lại. Biết mỗi tên trỏ tới file nào |
| 3 | Ghi danh sách hàm và lớp | Mỗi cái là một dữ kiện "symbol" kèm chữ ký |
| 4 | Tìm app và router | `x = FastAPI()`, `x = APIRouter()`, kể cả trong hàm tạo app |
| 5 | Tìm chuỗi gắn router vào app | Theo `include_router(prefix=…)`, `mount(…)` qua nhiều tầng. Router không gắn vào app nào: giới hạn `ROUTER_NOT_MOUNTED` |
| 6 | Đọc từng route | Method, đường dẫn, hàm xử lý, status, tham số, model, auth, điều kiện (bảng 5.4) |
| 7 | Đọc bảng | `__tablename__`, `Column`, `mapped_column`, khóa, mixin, `composite`; tìm loại database |
| 8 | Bảng chỉ trong migration | Giới hạn `TABLES_IN_MIGRATIONS_NOT_READ` |
| 9 | Sự kiện | Kafka, FastStream |
| 10 | Gọi HTTP và cấu hình | `httpx`, `requests`; lớp Settings, `os.environ`; che bí mật |
| 11 | Thư viện | `pyproject.toml`, `requirements.txt`; có import không |
| 12 | Hàng đợi chưa hỗ trợ | Celery, RabbitMQ: giới hạn `QUEUE_LIBRARY_UNSUPPORTED` |
| 13 | Lời gọi giữa các hàm | Nối được thì giữ; không nối được: giới hạn `REFERENCE_UNRESOLVED`, không vẽ cạnh |
| 14 | Kết thúc | Che giá trị giống mật khẩu (`VALUE_REDACTED`); kiểm không trùng mã; sắp xếp để chạy lại ra giống hệt |

teamhide sau bước 3: 297 symbol, 5 route, 4 model gửi lên, 3 model trả về, 1 bảng (9 cột), 19 config, 20 thư viện, 214 lời gọi (114 chưa nối được).

### 5.3 Ví dụ: ghép đường dẫn qua 3 file

```
server.py:77    app_ = FastAPI(                          ← app, tạo trong create_app
server.py:86    init_routers(app_=app_)                  ← app truyền vào init_routers
server.py:25    app_.include_router(user_router)         ← gắn router của user
api/__init__.py:5   router = APIRouter()
api/__init__.py:6   router.include_router(user_v1_router, prefix="/api/v1/user")
api/v1/user.py:12   user_router = APIRouter()
api/v1/user.py:43-44  @user_router.post("/login")
```

Ghép: `/api/v1/user` + `/login` = `/api/v1/user/login`. Mỗi mắt xích là một bằng chứng, nên route này có 12 nút bằng chứng trên web.

### 5.4 Mỗi ô của một route lấy từ đâu

| Ô | Lấy từ | Không đọc được thì |
|---|---|---|
| Method | Tên decorator: `.post` → POST | — |
| Đường dẫn | Prefix theo chuỗi gắn + chuỗi trong decorator. Prefix từ Settings: quy ước `settings-default-v1` | Ghép từ biến: "chưa biết" |
| Hàm xử lý | Tên đầy đủ của hàm | — |
| Status | `status_code=201`; `status.HTTP_201_CREATED` → 201 (suy ra); không ghi → 200 (suy ra) | — |
| Tham số | `Query()`, `Path()`, `{id}` trong đường dẫn, tham số trong `Depends(…)` sâu tối đa 3 tầng | Kiểu ở file không đọc được: vị trí "chưa biết" |
| Gửi lên | Tham số kiểu model Pydantic; field: tên, kiểu, bắt buộc, để trống được; định dạng uuid, email, ngày giờ | — |
| Trả về | `response_model=X`; kiểu trả về `-> X`; `-> None` là không trả gì | `list[…]`, `Any`, `JSONResponse`: "chưa biết" |
| Auth | Ghi tên dependency tìm được | **Luôn "chưa biết"** (chưa có quy tắc) |
| Điều kiện | Route nằm trong `if` thì ghi điều kiện | Không có `if`: "không áp dụng" |

## 6. Dữ kiện, bằng chứng, nhãn

### 6.1 Bốn trạng thái của một ô

| Trạng thái | Nghĩa | Ví dụ teamhide |
|---|---|---|
| biết (`known`) | Có giá trị và có dòng code | method POST, `user.py:43` |
| chưa biết (`unknown`) | Code không cho thấy; luôn có lý do | Auth: "Có dependency Provide[Container.user_service]; không kết luận cơ chế xác thực" |
| đã che (`redacted`) | Giống mật khẩu, bị che | giá trị `WRITER_DB_URL` |
| không áp dụng (`not_applicable`) | Ô không có nghĩa ở đây | route không nằm trong `if` |

### 6.2 Bằng chứng

Mỗi bằng chứng gồm: đường dẫn file, dòng bắt đầu và kết thúc, mã hash của file, mã snapshot.

### 6.3 Hai nhãn

| Nhãn | Giá trị | Nghĩa |
|---|---|---|
| Độ tin (confidence) | `exact` | Đọc thẳng từ code |
| | `inferred` | Suy ra theo một quy ước có tên |
| Độ đủ (completeness) | `full` | Mọi ô đã biết |
| | `partial` | Còn ô chưa biết |

### 6.4 Năm quy ước suy ra

| Code viết | Công cụ ghi | Tên |
|---|---|---|
| Body là model Pydantic | Gửi dạng JSON | `fastapi-defaults-v1` |
| Không ghi `status_code` | 200 | `fastapi-status-default-v1` |
| `status.HTTP_201_CREATED` | 201 | `starlette-status-constant-v1` |
| `prefix=settings.API_V1_STR` | Giá trị mặc định trong lớp Settings | `settings-default-v1` |
| Cột không ghi `primary_key`, `nullable` | Mặc định của SQLAlchemy | `sqlalchemy-defaults-v1` |

Ba quy ước giữa thêm vào contract ngày 02/10, chờ Khiêm duyệt.

## 7. Bước 5 — tự kiểm

| Lớp | Kiểm gì | Sai thì |
|---|---|---|
| 1. Bằng chứng | Đúng snapshot, file có thật, mã hash khớp, dòng nằm trong file | Dừng cả lần chạy |
| 2. Giá trị | Có nguyên văn ở dòng được chỉ (`20` không tính là có trong `200`); đường dẫn kiểm từng mảnh; status suy ra kiểm theo quy ước | Ô thành "chưa biết", giới hạn `CONTRACT_FIELD_UNPROVEN` |
| 3. Khối, cạnh | Khối có bằng chứng; cạnh A → B có lời gọi trong A, đích trong B; cạnh `exact` chỉ khi mọi dữ kiện `exact` | Bỏ cạnh, `EDGE_REJECTED` |
| 4. Chủ sở hữu | File khai báo thuộc đúng khối | Không có chủ |

Bước 6 còn kiểm thêm một lần (đọc lại file vừa viết). Bước 7 kiểm lại mã hash mỗi lần mở bằng chứng.

**Kiểm được:** dòng code có thật, chưa bị sửa, chứa đúng giá trị.
**Không kiểm được:** cách hiểu có đúng không, có bỏ sót không. Hai việc này phải chấm với đáp án người lập (KPI-006, 008, 009).

## 8. Bước 6 — file kết quả

| # | Việc |
|---|---|
| 1 | Kiểm sơ đồ ≤ 50 nút |
| 2 | Đặt tên: hệ thống từ tên repo (`TEAMHIDE`); khối viết hoa, bỏ dấu, trùng thì thêm `-2` |
| 3 | Gắn file theo chủ sở hữu; khối không sở hữu gì thì không có thư mục |
| 4 | File API: frontmatter, bảng Endpoint, Model, Truy vết, khối OpenAPI 3.1 |
| 5 | File TBL: bảng cột; khối DDL chỉ khi biết loại database |
| 6 | File EVT: mỗi khối có chỗ gửi/nhận; chỉ gom cùng topic khi có bằng chứng cùng broker |
| 7 | Sơ đồ Mermaid và SVG cùng một kế hoạch; README phải chứa đúng sơ đồ |
| 8 | Đọc lại từng file, so với dữ kiện |
| 9 | Ghi tất cả cùng lúc, kèm `manifest.json` |

Ví dụ một ô: status của route login.

| Nơi | Viết |
|---|---|
| Bảng Endpoint | `200 (suy theo fastapi-status-default-v1)` |
| Bảng Truy vết | `200` + mã dữ kiện + mã bằng chứng + `inferred / partial` |
| OpenAPI | `"200": {"description": "… (suy theo fastapi-status-default-v1)"}` |

teamhide ra 7 file. File API 538 dòng: 5 route, 7 model. File TBL: bảng `user` 9 cột; DDL chỉ có dòng `-- omitted: dialect chưa biết`.

## 9. Web

### 9.1 Màn hình và code (`ui/app.js`)

| Trên màn hình | Hàm |
|---|---|
| Trang gửi ZIP | `showHome`, `submit` |
| Trang kết quả, cứ 2 giây hỏi trạng thái | `showRun`, `refresh` |
| Tên repo, "một phần", lý do, thanh giai đoạn | `renderStatus` |
| Tài liệu tải về, Thử lại | `artifactsPanel`, `retry` |
| 5 ô số, ô Lọc, các mục | `renderResult` |
| Bảng API, cột Auth, cột Độ chắc chắn | `drawApi`, `authCell`, `certaintyCell` |
| Chi tiết route, field của model | `routeDetail`, `modelTable` |
| Nút `file:dòng`, đoạn code | `evidenceButtons`, `openEvidence` |
| Bảng dữ liệu | `drawTables` |

### 9.2 API của server (`web.py`)

| Đường dẫn | Làm gì |
|---|---|
| `POST /api/v1/runs/zip` | Nhận ZIP |
| `GET /api/v1/runs/{id}` | Trạng thái |
| `GET /api/v1/runs/{id}/result` | Toàn bộ kết quả |
| `GET /api/v1/runs/{id}/evidence/{ev}` | Đoạn code của một bằng chứng |
| `GET /api/v1/runs/{id}/artifacts/{a}` | Tải một file |
| `POST …/artifacts/{a}/retry` | Thử lại một file |

- Chỉ nhận yêu cầu từ chính máy (127.0.0.1); POST phải có header riêng của giao diện; trang không chạy script lạ.
- Code của repo giữ trong bộ nhớ: server khởi động lại thì phải tải ZIP lên lại mới mở được bằng chứng.

## 10. Code và cách chạy

### 10.1 Các file (`slice/l3slice/`, chỉ dùng thư viện chuẩn, Python ≥ 3.11)

| File | Dòng | Vai trò | Contract |
|---|---:|---|---|
| `__main__.py` | 169 | Chạy dòng lệnh | |
| `web.py` | 290 | Server web | API-L3GEN-001 |
| `engine.py` | 408 | Hàng đợi, trạng thái, gọi các bước, xóa sau 24 giờ | API-L3GEN-001 |
| `snapshot.py` | 175 | Bước 1–2 | API-L3GEN-002, 003 |
| `github.py` | 119 | Nhận repo GitHub (đang tắt) | API-L3GEN-002 |
| `pyindex.py` | 582 | Bảng tên qua import | API-L3GEN-004 |
| `extract.py` | 1.425 | Bước 3 | API-L3GEN-004 |
| `model.py` | 136 | Bước 4 | API-L3GEN-005 |
| `annotate.py` | 170 | Bước AI cho khối (chưa nối) | API-L3GEN-005, 006 |
| `gateway.py` | 519 | Cổng gọi Groq/Gemini (chưa chạy thật) | API-L3GEN-006 |
| `verify.py` | 278 | Bước 5 | API-L3GEN-007 |
| `render.py` | 1.081 | Bước 6 | API-L3GEN-008 |
| `common.py` | 65 | Hash, che bí mật, tạo ô 4 trạng thái | |
| `ui/` | 618 | Giao diện | |

Contract nằm ở `.aide/tech-specs/CMP-L3GEN-00x/api/API-L3GEN-00x-v1.md`.

### 10.2 Lệnh

```
cd D:\VSF\l3-generator-l3\slice
:: web
python -m l3slice.web --workdir <thư mục làm việc> --port 8765 --demo-partition
:: dòng lệnh
python -m l3slice --source <thư mục repo> --output <thư mục ra> --membership <file membership>
:: test (ở D:\VSF\l3-generator-l3)
scripts\.venv\Scripts\python.exe -m unittest discover -s slice\tests
scripts\.venv\Scripts\python.exe scripts\check_l3_contracts.py
```

### 10.3 Git

Nhánh `feature/l3-slice` trên GitLab, 3 commit: `7339e15` code, `d59b348` contract, `2eb8f18` PRD rev 29 (chờ Khiêm duyệt). Merge Request nên vào `docs/gate-2` (develop không có chung lịch sử).

## 11. Chỗ ast không trả lời được, và LLM

| Nhóm | Ví dụ | Xử lý |
|---|---|---|
| ast đọc thẳng | `@router.post("/login")`, `__tablename__`, `Column(String(255))` | Đã làm |
| ast đọc được, code chưa xử lý | `list[Model]`, chuỗi kết nối `postgresql://` để biết loại database | Viết thêm code |
| Cần hiểu ý nghĩa | `PermissionDependency([IsAdmin])` nghĩa là "chỉ admin"; `stripe`, `boto3` là gọi ra ngoài | LLM đề xuất kèm dòng code, code kiểm, nhãn `inferred` (chưa làm, chưa đo) |
| Chỉ có lúc chạy | `prefix=f"/api/{os.environ['VERSION']}"` | Ghi "chưa biết" |

Code L3 hiện tại: chỗ không đọc được thì ghi "chưa biết" kèm lý do hoặc ghi giới hạn. **Lỗ hổng:** lời gọi qua thư viện ngoài khác `httpx`, `requests` đang bị bỏ qua mà không khai (trái KPI-010).

PRD cho phép dùng model ở bước trích dữ kiện: NFR-AI-002 áp lên FR-021.

## 12. Tiến độ

### 12.1 Số đo (02/10/2026, 4 repo dev, máy dev)

| Repo | Dòng Python | Route | Bảng | Bằng chứng |
|---|---:|---:|---:|---:|
| rhoboro | 1.338 | 11 | 2 | 689 |
| fullstack | 2.908 | 23 | 2 | 1.378 |
| realworld | 3.841 | 19 | 0 (7 chỉ trong migration, đã khai) | 1.437 |
| teamhide | 2.750 | 5 | 1 | 896 |
| **Tổng** | **10.837** | **58** | **5** | **4.400** |

58/58 route khớp đáp án đếm tay; 4.400/4.400 bằng chứng qua tự kiểm; 177/177 test; 0,4–0,6 giây mỗi repo.

### 12.2 AC: 23 đạt, 13 một phần

| FR | Đạt | Một phần |
|---|---|---|
| 019 | 01, 02, 03, 04 | 05 |
| 020 | — | 01, 02, 03 |
| 021 | 01, 02, 04, 05 | 03 |
| 022 | 04 | 01, 02, 03, 05 |
| 023 | 01, 02, 03, 04 | — |
| 024 | 01, 02, 04 | 03 |
| 025 | 01, 02, 03, 04 | — |
| 026 | 01, 03 | 02 |
| 027 | 01 | 02, 03 |

"Đạt" = có code, có test, chạy đúng trên 4 repo. Chưa phải nghiệm thu.

### 12.3 Mốc và KPI

| Mốc | Hiện trạng |
|---|---|
| M0 Chốt yêu cầu | Chưa ký Scope Gate, chưa có ngày |
| M1 Lõi phân tích và dòng lệnh | Gần xong; còn FR-020, DDL |
| M2 Dựng mô hình kiến trúc và web | Web xong phần L3; chia khối chưa chốt |
| M3 Hoàn thiện dữ kiện và nghiệm thu | Chưa làm |

| KPI | Hiện trạng |
|---|---|
| 006 | Chưa đo theo KPI |
| 007 | 4.400/4.400 trên repo dev |
| 008 | 58/58 route trên repo dev; chưa đủ mẫu |
| 009 | Chưa đo |
| 010 | Một phần (lỗ hổng thư viện ngoài) |

## 13. Còn thiếu và khó khăn

**Còn thiếu ở phần L3** (tự sửa được): nhiều đơn vị phân tích mỗi repo (FR-020); DDL; `list[Model]`; auth; khai giới hạn thư viện ngoài; Celery; GitHub đang tắt.

**Khó khăn lớn** (cần mentor góp ý):

1. **Chưa chốt cách chia component (D-03).** Cùng repo có thể chia theo tính năng hoặc theo tầng. Repo lớn sai nhiều. PRD rev 26 và contract API-L3GEN-005 ghi khác nhau.
2. **Chưa có model miễn phí đúng PRD.** Thí nghiệm dùng dịch vụ trả phí; gói miễn phí giới hạn token.
3. **Chưa nghiệm thu được.** Chưa đủ cỡ mẫu (58/100 route, 5/20 bảng, 0/20 sự kiện); repo đã dùng để sửa lỗi; đáp án do nhóm tự lập.

**Khó khăn nhỏ** (nhóm tự xử lý): Scope Gate chưa ký; mốc chưa có ngày; phần L3 và phần sơ đồ chưa nối.

## 14. Liên hệ với phần của Khiêm

- Repo: `D:\VSF\l3-generator-quote-evidence`, nhánh `feature/quote-evidence`, code ở `experiments/quote-evidence/`.
- Đầu vào: 8 repo FastAPI công khai cố định commit (4 nhỏ là repo "lộ", 4 lớn "kín") + 2 repo mới; đáp án tự vẽ tay ở `oracle/`.
- Cách làm (v8): `ast` + Pyright lấy dữ kiện → code dựng nháp chia khối → AI sửa nháp, mỗi quyết định trỏ mã dòng `[L7]` → code chép nguyên văn và kiểm.
- Kết quả (tiêu chí riêng P ≥ 0,8, R ≥ 0,6): repo nhỏ và kibo đạt; boilerplate P 0,62; lnbits, fba chưa. teamhide: 10 khối, cạnh giữa khối R 0,75 (dưới 80% của PRD).
- Hai phần dùng **hai bộ đọc code riêng**. Nối với nhau qua file membership; lệnh dòng lệnh của L3 đã nhận file này.

10 mục "Tool phát hiện" của đề bài (mục 3.6):

| Mục | Phần L3 | Phần sơ đồ |
|---|---|---|
| Module/package | — | Có |
| Entry point | Ghi ứng dụng của route | Có |
| API route | Có đầy đủ | Mức khối |
| Service/business | — | Có |
| Repository/data access | — | Mức khối |
| Database entity | Có (chưa DDL) | Chỉ nhận file |
| External API | Một phần | Một phần |
| Queue/event | Một phần (Kafka) | Một phần (Celery) |
| Configuration | Có | Không |
| Important dependency | Có (thư viện) | Có (phụ thuộc khối) |

## 15. Thuật ngữ

| Từ | Nghĩa |
|---|---|
| `ast` | Thư viện Python biến code thành cây cú pháp |
| Snapshot | Bộ file của một lần chạy, kèm mã hash |
| Mã hash | Chuỗi tính từ nội dung file; đổi một chữ là đổi mã |
| Dữ kiện (fact) | Một điều đọc được từ code, gồm nhiều ô |
| Bằng chứng (evidence) | File + dòng + mã hash làm căn cứ cho một ô |
| `exact` / `inferred` | Đọc thẳng / suy ra theo quy ước |
| `full` / `partial` | Đủ ô / còn ô chưa biết |
| Component, khối | Nhóm file cùng một trách nhiệm |
| Membership | Danh sách file nào thuộc khối nào |
| Contract | Mô tả API, bảng, sự kiện hệ thống đưa ra ngoài |
| OpenAPI 3.1 | Định dạng chuẩn mô tả API cho máy đọc |
| DDL, dialect | Lệnh SQL tạo bảng; loại database (PostgreSQL, MySQL…) |
| Scope Gate | Bước ký duyệt phạm vi PRD |
| D-03 | Quyết định cách chia component, đang mở |
| Repo lộ / kín | Đã xem đáp án khi làm / chỉ xem điểm tổng |
| P / R | Tỉ lệ đúng trong cái ghi ra / tỉ lệ tìm được trong cái phải có |

## 16. Câu hỏi hay gặp

| Hỏi | Trả lời ngắn |
|---|---|
| Có dùng AI không? | Phần L3 không. AI chỉ ở phần chia khối, và đề xuất của AI cũng phải qua kiểm bằng chứng |
| Sao biết không bịa? | Mỗi giá trị phải nằm nguyên văn ở dòng code nó chỉ; máy kiểm 4.400/4.400 |
| FastAPI có `/docs` rồi, công cụ này hơn gì? | `/docs` cần chạy được app; công cụ chỉ cần code, ghi thêm bảng, config, thư viện, chỉ về dòng code. App chạy được thì `/docs` đủ hơn ở thứ sinh ra lúc chạy |
| Status 200 lấy ở đâu? | Quy ước của FastAPI khi code không ghi; ô có nhãn "suy ra" |
| Sao Auth luôn "chưa biết"? | Chưa có quy tắc; đoán sai về bảo mật nguy hiểm hơn để trống |
| Sao "một phần"? | Còn giới hạn, ví dụ Celery chưa đọc |
| Đúng bao nhiêu %? | Trên 4 repo dev: route 58/58, bằng chứng 4.400/4.400. Chưa phải số nghiệm thu |
| Kiểm được gì? | Bằng chứng là thật. Cách hiểu đúng hay không phải chấm với đáp án |
| Làm Java thì sao? | PRD để phase sau; chỉ bước đọc code phải viết mới |
| Code ở đâu? | GitLab nhánh `feature/l3-slice`, thư mục `slice/` |

## 17. Đường dẫn cần nhớ

| Gì | Ở đâu |
|---|---|
| PRD rev 29 | `.aide/product/prd/PRD-L3GEN-2609-001.md` |
| FR, NFR | `.aide/requirements/fr/`, `.aide/requirements/nfr/` |
| Cách đo KPI | `.aide/observability/OBS-L3GEN-001.md` |
| Contract | `.aide/tech-specs/` |
| Đề bài | `Đề bài.md`, mục 3.6 |
| Code L3, test | `slice/l3slice/`, `slice/tests/` |
| ZIP demo | `ket-qua-chay/8-repo-khiem/teamhide.zip` |
| Kết quả chạy sẵn | `ket-qua-chay/8-repo-khiem/l3-teamhide/` |
| Báo cáo tiến độ cho mentor | `docs/L3-Generator-bao-cao-mentor.md` |
| Phần của Khiêm | `D:\VSF\l3-generator-quote-evidence\docs\HANDOFF.md` |

Đường dẫn tương đối tính từ `D:\VSF\l3-generator-l3\`.
