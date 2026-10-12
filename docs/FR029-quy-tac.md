# FR-029: bản quy tắc của luồng agent sinh tài liệu API

Cập nhật: 07/10/2026, ứng với code hiện tại (prompt `fr029-agent-prompt-v13`). Tài liệu này liệt kê mọi quy tắc mà luồng FR-029 đang áp dụng, mỗi quy tắc kèm chỗ nằm trong code. Cơ chế và kết quả đo xem ở [FR029-giai-thich-cho-mentor.md](FR029-giai-thich-cho-mentor.md).

Ký hiệu nơi đặt quy tắc: `ST` = `slice/l3slice/source_tools.py`, `DF` = `docfacts.py`, `DA` = `docagent.py` (gồm prompt), `DP` = `docpipeline.py`, `RD` = `render.py`, `SC` = `slice/tools/fr029_score.py`.

## 1. Phân vai

Mục này nói ai được quyết điều gì.

| # | Quy tắc | Nơi đặt |
|---|---|---|
| 1.1 | Agent (model) quyết dữ kiện: route, path, tham số, model, status, dependency, HTTP, vai trò file | Prompt `DA` |
| 1.2 | Code quyết phạm vi đọc, kiểm bằng chứng, đặt mã, sinh file, chấm điểm | `ST`, `DF`, `DP` |
| 1.3 | Code không tự trích dữ kiện từ AST; không gọi extractor cũ | `DP` (test chặn `extract.extract`) |
| 1.4 | Không tạo, chia, đặt tên component; không vẽ sơ đồ. Component, `archdia.json`, sơ đồ là đầu vào từ FR-028 | `DP.load_components` |
| 1.5 | Agent không có công cụ ghi file, chạy lệnh hay import code; nội dung source là dữ liệu, không phải chỉ dẫn | `DA.TOOL_SPECS`, prompt |

## 2. Phạm vi đọc (theo FR-028)

Mục này nói file nào agent được đọc.

| # | Quy tắc | Nơi đặt |
|---|---|---|
| 2.1 | Snapshot gồm file `.py` và manifest (`pyproject.toml`, `requirements*.txt`); bỏ `.git`, `.venv`, `venv`, `node_modules`, `__pycache__` | `snapshot.py` |
| 2.2 | Thư mục ẩn, `node_modules`, `__pycache__`, `site-packages`, thư mục chứa `pyvenv.cfg` → môi trường, không đọc | `ST.classify` |
| 2.3 | `tests/`, `test/`, `test_*.py`, `*_test.py`, `conftest.py` → kiểm thử, không đọc | `ST.classify` |
| 2.4 | `migrations/`, `alembic/` → migration, không đọc | `ST.classify` |
| 2.5 | `scripts/`, `seeds/`, `docs/`, `examples/`, `build/`, `dist/`, `env/`, `venv/`, `testing/` → chỉ đọc khi file import code của repo (tên gói cấp đầu, gói trong `src/`, hoặc import tương đối) | `ST.classify` |
| 2.6 | Manifest được đọc để biết phiên bản Pydantic | `ST.SourceTools` |
| 2.7 | File ngoài phạm vi được đếm theo loại ở phần giới hạn | `DP._limitations` |

Giới hạn đã biết: `snapshot.py` bỏ `venv/` vô điều kiện, trái với 2.5 (lỗi có từ trước, chưa sửa).

## 3. Đọc và độ phủ

| # | Quy tắc | Nơi đặt |
|---|---|---|
| 3.1 | `read_file` trả tối đa 200 dòng mỗi lần, có số dòng | `ST.LINES_PER_READ` |
| 3.2 | Dòng dài hơn 400 ký tự bị cắt; lần chạy có dòng bị cắt không được `completed` | `ST.MAX_LINE_CHARS`, `DA._dispatch` |
| 3.3 | `list_files` 100 file mỗi trang; `search_text` 30 kết quả mỗi trang; kết quả tìm không tính là đã đọc | `ST` |
| 3.4 | Một dòng là `delivered` khi đã nằm trong kết quả công cụ; thành `processed` khi model trả lời hợp lệ ở lượt sau | `ST.model_answered` |
| 3.5 | Độ phủ đủ khi mọi dòng của mọi file đọc được là `processed` và không có dòng bị cắt | `ST.coverage` |
| 3.6 | Mỗi lượt có thể giới hạn lượng chữ đọc; vượt thì lần đọc sau bị từ chối, không tính là đã gửi | `Budget.max_turn_read_chars` |

## 4. Che bí mật

| # | Quy tắc | Nơi đặt |
|---|---|---|
| 4.1 | Trước khi gửi cho model, thay giá trị giống bí mật bằng `***`; giữ nguyên số dòng | `ST.masked_lines` |
| 4.2 | Mẫu che: khóa AWS/GitHub/OpenAI/Groq/Google; khối private key nhiều dòng; `password/secret/token/api_key = "..."` kể cả có annotation (`password: str = "..."`), khóa dạng chuỗi trong dict, chuỗi ba nháy; mật khẩu trong URL; tham số nhạy cảm trong query string | `common.SECRET_PATTERNS`, `ST.LINE_PATTERNS`, `ST.TRIPLE` |
| 4.3 | Giá trị agent nộp còn chứa bí mật (ví dụ URL có mật khẩu thật) bị từ chối | `DF.add_http` |
| 4.4 | Mục bị từ chối chỉ lưu tên trường và lỗi đã che, không lưu giá trị | `DF.submit` |
| 4.5 | Khóa API không bao giờ được in hay ghi vào file | `DA.KeyHandle`, script chạy |

## 5. Vòng agent, ngân sách, kết thúc

| # | Quy tắc | Nơi đặt |
|---|---|---|
| 5.1 | Mỗi lượt: gửi hội thoại → model gọi công cụ → code chạy công cụ, nối kết quả | `DA.run_agent` |
| 5.2 | `finish` chỉ được nhận khi: không còn dòng chưa đọc; mọi model được tham chiếu đã nộp; mọi file `.py` có nội dung trong component `normal` đã có vai trò; Service có đường gọi hợp lệ; mọi dòng nghi ngờ đã xử lý | `DF.open_problems` |
| 5.3 | `finish` bị từ chối quá 4 lần → dừng `partial`, ghi danh sách việc dở vào `result.json` | `Budget.max_finish_attempts`, `AgentRun.open_problems` |
| 5.4 | Ngân sách mặc định: 200 lượt, 2.000.000 token, 1.800 giây; trần USD tùy chọn. Chạm trần nào cũng dừng `partial` và vẫn xuất phần đã biết | `DA.Budget` |
| 5.5 | Đặt trần USD mà không có bảng giá → không chạy | `DA.run_agent` |
| 5.6 | 3 lượt liên tiếp model không gọi công cụ → dừng `partial` | `DA.run_agent` |
| 5.7 | Lỗi model không bao giờ quay về extractor cũ để tạo kết quả | `DA`, `DP` |
| 5.8 | Rút gọn ngữ cảnh: khi hội thoại vượt ngưỡng ký tự, thay kết quả công cụ cũ và đối số `submit_findings` cũ bằng một dòng "đã rút gọn"; chỉ rút gọn những gì model đã nhận; 6 tin cuối giữ nguyên | `DA._shrink` |
| 5.9 | Thư mục output đã có nội dung → từ chối trước khi gọi model | `DP.run_documents` |

## 6. Gọi model

| # | Quy tắc | Nơi đặt |
|---|---|---|
| 6.1 | Hai adapter: chat completions (Groq và endpoint tương thích); Responses API (OpenAI; dùng khi cần công cụ cùng suy luận) | `DA.OpenAICompatProvider`, `DA.ResponsesProvider` |
| 6.2 | Responses API gửi `store: false`, kèm suy luận mã hóa; phần mới chỉ nối vào bản ghi sau khi request thành công | `DA.ResponsesProvider.chat` |
| 6.3 | Lỗi 429: chờ theo `retry-after`, tối thiểu 15 giây, tối đa 90 giây, tối đa 8 lần | `WAITS`, `MAX_WAIT_S` |
| 6.4 | Mất mạng, cắt kết nối: gửi lại tối đa 3 lần | `NET_RETRIES` |
| 6.5 | Lỗi 413 (request quá lớn): rút gọn mạnh hơn (×0,7) rồi gửi lại | `DA.run_agent` |
| 6.6 | Giới hạn token/phút (Groq): đợi tới khi cửa sổ 60 giây còn chỗ | `DA._pace` |
| 6.7 | Chi phí tính theo token đầu vào, token đã cache, token đầu ra và bảng giá truyền vào; request lỗi không có số token nên không được tính | `cost_usd` |

## 7. Dữ liệu agent nộp

Mục này nói agent phải nộp những gì; đây cũng là khuôn trong prompt.

| # | Quy tắc |
|---|---|
| 7.1 | Agent chỉ dẫn `file:dòng` hoặc `file:đầu-cuối` (tối đa 60 dòng). Mã fact và evidence do code tạo |
| 7.2 | Không đọc được thì ghi `{"unknown": "lý do tiếng Việt"}`. Không đoán; không suy kiểu từ tên biến |
| 7.3 | Ký pháp kiểu: `integer, number, string, binary, uuid, datetime, date, email, boolean, object, any, array[T], file.py::Class`. Nullable ghi riêng. `UploadFile`/`bytes` → `binary`; `uuid.UUID` → `uuid`; `EmailStr` → `email` |
| 7.4 | Route: method, handler `file.py::hàm`, khoảng decorator (từ `@` tới `def`), application (dòng `FastAPI(`), `path_parts` theo thứ tự từ app xuống decorator, `params`, `request_body`, `response`, `status`, `dependencies`, `auth` |
| 7.5 | Model: `file.py::Class`, dòng `class`, mỗi trường có tên, alias, kiểu, required, nullable, dòng |
| 7.6 | Lời gọi HTTP: dòng gọi, thư viện, method, đích (`literal`/`config`/`unknown`); client tạo ở file khác thì thêm `client_at` |
| 7.7 | Vai trò file: file, vai trò, dòng dấu hiệu; Service thêm `call_path`; có thể thêm `not_signal` khi khớp dấu hiệu sai |
| 7.8 | Giới hạn: `add_api_route`, `add_route`, `add_websocket_route`, `unsupported_http_library`, kèm dòng |
| 7.9 | Dòng nghi ngờ không phải route/HTTP: nộp `dismissed` kèm lý do |
| 7.10 | Nộp lại cùng một route (cùng handler, method, application, vị trí các lần đăng ký) thì bản mới thay bản cũ |

Quy tắc về route (prompt):

| # | Quy tắc |
|---|---|
| 7.11 | Mỗi lần đăng ký là một phần của `path_parts`, kể cả `include_router(r)` không có prefix (`value: ""`) |
| 7.12 | Prefix lấy từ mặc định của Settings → phần `settings_default` kèm `used_at` là dòng đăng ký dùng nó |
| 7.13 | Prefix truyền qua hàm bọc hay biến → `at` là dòng có literal, `used_at` là dòng `include_router` thật |
| 7.14 | `unknown` chỉ dùng khi có prefix nhưng không đọc được giá trị (biến môi trường không mặc định, giá trị tính lúc chạy) |
| 7.15 | Router gắn hai lần hoặc dưới hai app → hai route; `api_route(methods=[A,B])` → mỗi method một route |
| 7.16 | Route của sub-app gắn bằng `app.mount("/p", sub)`: application là app ngoài, `/p` là `mount_prefix` |
| 7.17 | Bỏ route tài liệu tự sinh của FastAPI (`/docs`, `/redoc`, `/openapi.json`) |
| 7.18 | Đã có bản route gắn vào app thì bản "chưa gắn app" của cùng handler và method bị bỏ (`DF.add_route`) |
| 7.19 | Tham số khai trong hàm `Depends(...)`, kể cả lồng nhiều tầng, là tham số của endpoint |
| 7.20 | Tên header theo HTTP: `_` thành `-` (quy tắc `fastapi.header_underscore_to_hyphen`), trừ khi có `alias` hoặc `convert_underscores=False` |
| 7.21 | Tham số path luôn bắt buộc (`DF.params`) |
| 7.22 | Từ hai tham số body JSON trở lên, hoặc `Body(embed=True)` → `embedded: true` và liệt kê `fields` (khóa cấp trên cùng) |
| 7.23 | Form/File → `models: []` và `fields`; có `File` thì `multipart/form-data`, chỉ `Form` thì `application/x-www-form-urlencoded` |
| 7.24 | Response: `response_model=` trong decorator thắng kiểu trả về (kể cả `-> Any`); chỉ có kiểu trả về thì dùng quy tắc `fastapi.return_annotation_response_model`; không có cả hai → `null`; kiểu không phải model (`bool`, `Any`) → `{"type": T}`; `response_class=HTMLResponse` → `{"type": "string", "media_type": "text/html"}` |
| 7.25 | Status: không khai → 200 (`fastapi.default_status_200`), trừ khi có `response_class` hoặc `default_response_class` → mặc định của lớp đó; `HTTPException` trong thân hàm không phải status khai báo |
| 7.26 | `dependencies`: mọi `Depends(...)` của route: chữ ký handler, `dependencies=[...]` của decorator, router và app |
| 7.27 | `auth`: `unknown` trừ khi source chứng minh được cơ chế |
| 7.28 | Pydantic: luật theo lớp `BaseModel` mà model thật sự kế thừa: `pydantic` (theo phiên bản ghim trong manifest) hay `pydantic.v1` (luôn luật v1) |

## 8. Bộ kiểm bằng chứng

Mục này nói code từ chối những gì. Bị từ chối thì agent nhận lỗi theo trường và nộp lại.

| # | Kiểm | Nơi đặt |
|---|---|---|
| 8.1 | Dòng được dẫn có trong file, nằm trong phạm vi đọc, và đã được gửi qua `read_file` | `DF.loc` |
| 8.2 | Literal (path, alias, URL, method của `api_route`) có nguyên văn tại dòng dẫn; so với cả bản gốc lẫn bản đã che | `DF.has_literal` |
| 8.3 | Khoảng decorator: dòng đầu là `@`, có đúng một `def` là handler; method xuất hiện trong decorator | `DF._decorator_problems` |
| 8.4 | Receiver của decorator không được là đối tượng tạo trong cùng file từ thứ khác `FastAPI(`/`APIRouter(` | `DF._decorator_problems` |
| 8.5 | Dòng `application` có `FastAPI(` | `DF.add_route` |
| 8.6 | Mỗi phần prefix nằm trên đúng loại dòng (`include_router(`, `APIRouter(`, `.mount(`, phép gán Settings); có `used_at` thì kiểm `used_at` | `DF.PART_SIGNALS` |
| 8.7 | Phần cuối của `path_parts` là decorator; chỉ phần cuối là decorator; `value: ""` không được dùng trên dòng có prefix khác rỗng; `unknown` không được dùng trên dòng không có prefix | `DF.add_route` |
| 8.8 | Status nằm trong decorator của chính route (trừ `default_response_class`); mã có dạng `status_code=<mã>` hoặc hằng `HTTP_<mã>_…` | `DF.status` |
| 8.9 | Tên model ở request/response xuất hiện tại dòng dẫn; model là `file.py::Class` và dòng có `class Class` | `DF.body`, `DF.response`, `DF.add_model` |
| 8.10 | Tên tham số, trường, dependency xuất hiện tại dòng dẫn | `DF.params`, `DF.add_model` |
| 8.11 | HTTP: file import thư viện hoặc có `client_at`; dòng có lời gọi; method khớp tên lời gọi hay đối số method; URL literal là đối số URL đầu tiên (hoặc `url=`); khóa cấu hình xuất hiện tại dòng | `DF.add_http` |
| 8.12 | Quy tắc suy luận phải nằm trong danh sách mục 9 | `DF.rule` |
| 8.13 | Kiểu phải đúng ký pháp mục 7.3 | `DF.type_` |
| 8.14 | Dữ liệu sai kiểu JSON trả lỗi theo trường, không làm crash | `DF` |

**Bộ kiểm không chứng minh được nghĩa.** Agent có thể dẫn đúng dòng mà ghi sai kiểu, sai required, sai thứ tự prefix, hay dẫn dòng không liên quan cho `auth`. Những lỗi này chỉ đo được bằng đáp án và người chấm (mục 13).

## 9. Quy tắc suy luận (danh sách đóng)

Mục này là danh sách tên duy nhất được dùng cho giá trị `inferred`.

| Tên | Nghĩa |
|---|---|
| `fastapi.default_status_200` | Không khai `status_code`, không có `response_class` → 200 |
| `fastapi.response_class_default_status` | Không khai `status_code` nhưng có `response_class`/`default_response_class` → mặc định của lớp đó |
| `fastapi.header_underscore_to_hyphen` | Tên tham số Header đổi `_` thành `-` |
| `fastapi.status_constant` | Status khai bằng hằng `HTTP_<mã>_…`; ghi tên quy tắc nhưng **nhãn vẫn `exact`** |
| `fastapi.return_annotation_response_model` | Không khai `response_model`; dùng kiểu trả về |
| `fastapi.json_body_media` | Body là Pydantic model → `application/json` |
| `fastapi.scalar_param_query` | Tham số kiểu đơn, không có trong path, không khai Query/Header/Cookie → query |
| `fastapi.model_param_body` | Tham số kiểu Pydantic model không khai Body → body |
| `fastapi.multiple_body_embed` | Từ hai tham số body → body được bọc theo tên tham số |
| `settings.default_prefix` | Prefix là giá trị mặc định trong Settings; biến môi trường có thể ghi đè |
| `pydantic.v2_required_no_default` | Pydantic v2: không có default thì bắt buộc, kể cả khi cho phép `None` |
| `pydantic.v1_optional_not_required` | Pydantic v1: `Optional` không có default thì không bắt buộc |

Thêm quy tắc mới: sửa `DF.RULES`; prompt tự nhận danh sách mới.

## 10. Nhãn

| # | Quy tắc | Nơi đặt |
|---|---|---|
| 10.1 | `exact`: đọc thẳng từ code. `inferred`: fact có ít nhất một giá trị dùng quy tắc mục 9; nhãn ghi kèm tên các quy tắc | `DF.FactBuilder.fact`, `RD._label` |
| 10.2 | Nhãn đặt ở mức cả fact (route, model), chưa gắn riêng từng trường | `DF` |
| 10.3 | `partial`: fact có ít nhất một trường `unknown`, kể cả trường lồng bên trong | `DF._has_unknown` |
| 10.4 | Vai trò Service luôn `inferred`, lý do "nằm trên đường gọi"; vai trò khác `exact` | `DF.build_facts` |
| 10.5 | `unknown` luôn kèm lý do; không thay `unknown` bằng `null` | `DF` |

## 11. Vai trò file

| # | Quy tắc | Nơi đặt |
|---|---|---|
| 11.1 | Xét theo thứ tự, dừng ở dấu hiệu đầu tiên khớp: Điểm vào → Route → Model bảng → Hạ tầng → Truy cập dữ liệu → Schema API → Cấu hình → Service → Khác | `DF.ROLES`, prompt |
| 11.2 | Dấu hiệu bắt buộc tại dòng dẫn: Điểm vào (`FastAPI(`, `uvicorn.run(`, `__main__`, lệnh Click/Typer); Route (decorator route); Model bảng (`__tablename__`, `table=True`, `Table(`); Cấu hình (`BaseSettings`, `os.environ`, `os.getenv`); Schema API (`class X(`) | `DF.ROLE_SIGNALS` |
| 11.3 | Hạ tầng: dòng tạo engine/client có URL, host hoặc DSN (SQLAlchemy/SQLModel, Redis, SMTP/gửi mail, broker) hoặc lời gọi HTTP ra ngoài; dòng import không được dùng làm dấu hiệu | Prompt, `DF.add_role` |
| 11.4 | Truy cập dữ liệu: dẫn dòng gọi method của session hoặc dựng truy vấn, không dẫn dòng chỉ mở session | Prompt, `DF.add_role` |
| 11.5 | File có dấu hiệu Điểm vào, Route hoặc Model bảng thì không được gán vai trò sau đó, trừ khi agent giải thích bằng `not_signal` | `DF.ORDER_SIGNALS` |
| 11.6 | Service: `call_path` ≥ 2 vị trí, đi qua chính file đó, bắt đầu ở file route, kết thúc ở file Truy cập dữ liệu/Hạ tầng | `DF.add_role`, `DF.open_problems` |
| 11.7 | Khác: vẫn phải dẫn một dòng code của file | `DF.add_role` |
| 11.8 | File rỗng không có vai trò (thuộc component Khác theo FR-028); chỉ liệt kê vai trò cho component loại `normal` | `DF.add_role`, `DP.readme` |
| 11.9 | Không đoán vai trò theo tên file | Prompt |

## 12. Dòng nghi ngờ

Mục này nói code bắt agent xem xét những dòng nào để chống bỏ sót.

| # | Mẫu | Phải xử lý bằng |
|---|---|---|
| 12.1 | Decorator route `@x.get(`… `api_route(`, `websocket(` | Route nộp có decorator đó, cùng method |
| 12.2 | `.add_api_route(`, `.add_route(`, `.add_websocket_route(` | Giới hạn |
| 12.3 | `.get/.post/…/.request/.stream(` trong file có import httpx/requests/aiohttp | Lời gọi HTTP |
| 12.4 | `urlopen(`, `urllib3 … .request(`, `http.client`, `HTTPConnection(` | Giới hạn `unsupported_http_library` |
| 12.5 | Mọi dòng trên có thể bác bằng `dismissed` kèm lý do, **trừ** lời gọi `add_*_route` trên app/router tạo từ `FastAPI(`/`APIRouter(` trong cùng file | `DF.add_dismissed` |
| 12.6 | Lý do bác được lưu vào `result.json` | `DP` |

## 13. Xuất tài liệu

| # | Quy tắc | Nơi đặt |
|---|---|---|
| 13.1 | Route thuộc component chứa file khai báo route (dòng decorator) | `DP.plan_documents` |
| 13.2 | Mỗi component có route được một file `tech-specs/<CMP>/api/API-<SYS>-<CMP>-v1.md`; tên viết hoa, bỏ dấu; trùng thì thêm số | `RD.slug`, `RD.unique_slugs` |
| 13.3 | Component phải có tên và id duy nhất; mỗi file đúng một component | `DP.load_components` |
| 13.4 | File API gồm: frontmatter (bản sinh tự động, snapshot, owner, mã fact và evidence), bảng endpoint, bảng model, truy vết route và model, khối OpenAPI 3.1 | `RD.render_api`, `DP` |
| 13.5 | Route không biểu diễn được trong OpenAPI (method lạ, path `unknown`, thiếu status, thiếu application) bị bỏ khỏi khối, kèm lý do | `RD.render_api` |
| 13.6 | Model trùng tên ở hai file: ghi kèm tên file | `RD._model_label` |
| 13.7 | Code trong README hiện nguyên văn (không thoát HTML bên trong code span) | `RD.code` |
| 13.8 | Đọc ngược một số trường của file vừa viết (method, path, status, request body, response mảng) và so với fact; lệch thì không xuất file đó | `RD.check_doc` |
| 13.9 | README: mục lục (chỉ file xuất được), sơ đồ (đầu vào hoặc ghi "chưa được cấp"), cấu trúc component, lời gọi HTTP, contract chưa gán, đối chiếu kiến trúc, giới hạn | `DP.readme` |
| 13.10 | Giới hạn luôn ghi: lời gọi đăng ký không qua decorator, thư viện HTTP khác, phân tích dở, source chưa đọc hết, file ngoài phạm vi, lần nộp bị từ chối, thiếu sơ đồ, chưa đối chiếu kiến trúc | `DP._limitations` |
| 13.11 | Khóa cấu hình ghi tên trường (`settings.X` → `X`); biểu thức đầy đủ lưu riêng | `DF.build_facts` |
| 13.12 | Ghi file vào thư mục tạm rồi đổi tên một lần; lỗi giữa chừng không để lại output dở | `RD._publish` |

Chưa có: bộ kiểm hợp lệ OpenAPI trong pipeline (mới có trong test); retry riêng cho bộ tài liệu FR-029.

## 14. Đối chiếu kiến trúc (AC-04)

| # | Quy tắc | Nơi đặt |
|---|---|---|
| 14.1 | Chỉ nhận `archdia.json` có `schema: archdia-fixture-v1`; khác → `not_evaluated` | `DP.compare_architecture` |
| 14.2 | Thiếu `snapshot_id` → `not_evaluated`; khác snapshot → `failed` | như trên |
| 14.3 | So tập route theo (method, path, file, dòng decorator), component sở hữu, và thư mục tài liệu ↔ component; chỉ tính route của file API xuất được | như trên |
| 14.4 | Không sửa hay lọc dữ kiện để hai phía khớp | như trên |

## 15. Đo và chấm

Mục này nói kết quả được đo và công bố thế nào.

| # | Quy tắc | Nguồn |
|---|---|---|
| 15.1 | Nghiệm thu tính trên **từng** repo kín cỡ nhỏ và vừa: tdd-docker, AgentGPT, igorbenav, kibo-backend; repo kín lớn chỉ báo số; repo lộ báo riêng | OBS-001 |
| 15.2 | Repo lộ được xem chi tiết để chỉnh prompt; repo kín chỉ xem số tổng | OBS-001 |
| 15.3 | Mỗi cấu hình (snapshot, model, prompt, công cụ) đo 1 lần; chạy lại chỉ khi lỗi hạ tầng, ghi lý do | OBS-001 |
| 15.4 | Ngưỡng: P và R ≥ 80% riêng từng loại dữ kiện; bằng chứng hợp lệ 100%; `exact` sai ≤ 5% | NFR-ACC-002 |
| 15.5 | Chạy lặp 3 lần chỉ là kiểm nội bộ để xem dao động, không phải số nghiệm thu | Kế hoạch V1 |
| 15.6 | Không dùng output của tool làm đáp án | OBS-001 |
| 15.7 | Bộ chấm: TP/FP/FN theo khóa; thuộc tính chỉ chấm trên mục khớp; `unknown` đúng chỉ khi đáp án cũng `unknown`; ca chạy lỗi tính mọi mục đáp án là bỏ sót | `SC`, `fr029_golden_routes.py` |
| 15.8 | Bộ chấm fixture chưa chấm: dependency/auth, nullable tham số, nhãn, bằng chứng từng trường, AC-04, AC-06 | `SC` |
| 15.9 | Chấm đa model: người chấm không xem đáp án; cùng mẫu chọn cố định (seed 29, tối đa 10 route, 15 file); lỗi được ≥2 người chấm báo cùng trường, cùng dòng mới là "xác nhận" | `fr029_sample.py`, `fr029_grade_merge.py` |
| 15.10 | Lỗi tìm ở repo kín không dùng để chỉnh prompt | OBS-001 |

## 16. Chi phí và khóa

| # | Quy tắc |
|---|---|
| 16.1 | Model được dùng: OpenAI `gpt-6-luna` và `gpt-5.6-terra` (người dùng chọn). Groq miễn phí không dùng được vì giới hạn 8K token/phút |
| 16.2 | Mỗi lần chạy có trần USD; trần chung do người dùng duyệt (hiện 2 USD) |
| 16.3 | Khóa OpenAI lấy từ biến `open_ai` trong `D:/VSF/VSF-L3 Generator/.env` theo phép của người dùng; không in, không ghi ra file |

## 17. Quy tắc chưa chốt

Mục này liệt kê chỗ code đang theo một cách nhưng chưa được duyệt.

| # | Câu hỏi | Code đang làm |
|---|---|---|
| 17.1 | Route ở file production mà router không được gắn vào app nào | Không cấm; agent thường ghi route với path `unknown` hoặc bỏ qua; gold fixture và golden v1 không ghi route |
| 17.2 | Status ở thân hàm (`HTTPException(404)`, `Response(status_code=...)`) | Không ghi |
| 17.3 | Ràng buộc giá trị (`le`, `ge`, `max_length`) | Không ghi |
| 17.4 | Security scheme trong OpenAPI | Không ghi; `auth` để `unknown` nếu chưa chứng minh được |
