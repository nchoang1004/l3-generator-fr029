# Độ chính xác của bộ kiểm FR-029 trên nhiều repo — 08/10/2026

Báo cáo trả lời 2 câu hỏi: bộ kiểm có sai khi áp sang repo khác không, và độ chính xác hiện đạt bao nhiêu.

- Mọi phép đo dùng code tĩnh, không gọi LLM sinh tài liệu.
- Giám khảo độc lập: Codex astra high. Có 2 loại phiên: chấm repo chưa dùng, và kiểm cách đo có công bằng không (10 vòng). Khi Codex hết lượt, 3 repo chưa dùng được chấm bằng agent Claude với cùng đề bài, không cho đọc code bộ kiểm.

**Kết luận ngắn:**

- Trên 37 bộ có gold: **0 lỗi** ở mọi phép thử. Bộ kiểm giả "luôn nhận" và "luôn từ chối" đều bị phép đo bắt ở mọi chỉ số.
- Trên 14 repo chưa dùng để chỉnh: bộ kiểm không nhắc sai tham số dependency nào. Các mục giám khảo chấm "sai" đều do cách công cụ đo xuất gói, đã kiểm bằng test trên bộ kiểm thật. Lỗi thật tìm ra (bỏ sót lời gọi HTTP, dòng nhiễu, file Python 3.14 không parse được) đã sửa, mỗi lỗi có test, trừ 2 lời gọi dạng `self.runtime.session.post(...)` ở xianyu (mục 4).
- Mỗi vòng kiểm vẫn tìm ra dạng code mới (25 → 10 → 7 → 8 → 7 → 8 → 8 → 7 → 7 → 6 phản ví dụ của Codex, cộng 9 + 8 ca từ agent Claude ở vòng 7 và 9). Tần suất Codex ước cho các ca mới giảm dần, từ "cao" ở các vòng đầu xuống "vừa"/"thấp" ở vòng 7–10, dù các phản ví dụ của vòng trước đều được Codex xác nhận đã xử lý. Số 0 lỗi chỉ đúng với tập đã đo, không chứng minh 0 lỗi trên mọi repo.

## 1. Bộ kiểm là gì

| Phần | Làm bằng gì | Vai trò |
|---|---|---|
| Agent sinh tài liệu | LLM (`gpt-6-luna`) | Đọc source, nộp mọi dữ kiện: route, tham số, model, lời gọi HTTP |
| Bộ kiểm (`docfacts.py`, `astscan.py`) | Code tĩnh, đọc cây cú pháp Python, không chạy code repo | Không tạo dữ kiện. Làm 3 việc: (1) từ chối câu trả lời khi dòng được dẫn không chứa điều LLM nói; (2) đánh dấu dòng nghi ngờ mà LLM phải giải thích; (3) nhắc tham số dependency còn thiếu |

## 2. Cách đo

Công cụ: `slice/tools/fr029_checkaudit.py`. Nó đóng vai một agent trả lời đúng gold, rồi trả lời sai có chủ ý (mutation), và xem bộ kiểm phản ứng thế nào.

| Phép thử | Cách làm |
|---|---|
| Từ chối nhầm | Nộp đúng câu trả lời của gold |
| Nhận nhầm (mutation) | Route: method, handler, path khác. Prefix: bỏ phần prefix router (mới). Dependency: tên khác. HTTP: URL, thư viện, method khác |
| Ca âm | Route gold ghi "không phải FastAPI"; lời gọi gold ghi "không phải HTTP" |
| Nhắc tham số | Đi qua đúng `open_problems` mà agent nhận; so với tham số gold |
| Dòng nghi ngờ | Mọi route và lời gọi HTTP của gold phải bị đánh dấu; đếm dòng thừa |
| Bộ kiểm giả | Thay bộ kiểm bằng bản "luôn nhận" và "luôn từ chối". Phép đo phải báo lỗi lớn |

Gold gồm 37 bộ: 7 repo thật, 4 repo mới có gold do 2 agent viết độc lập rồi đối chiếu, 7 fixture, 19 ca dev.

Phép đo prefix tính prefix = path gold trừ literal của decorator, đọc bằng cây cú pháp riêng của công cụ đo. Route khai trực tiếp trên app thì bỏ qua (không có prefix router).

## 3. Kết quả trên gold (r41, code cuối)

| Phép thử | Bộ kiểm thật | Giả "luôn nhận" | Giả "luôn từ chối" |
|---|---|---|---|
| Route đúng bị từ chối (406 route) | **0** | 0 | 801 |
| Route sai bị nhận (1549 mutation) | **0** | 1549 | 0 |
| Route thiếu prefix bị nhận (131) | **0** | 131 | 0 |
| Route không prefix bị từ chối (17) | **0** | 0 | 17 |
| Route gold bị coi là "chưa đăng ký" (408) | **0** | 0 | 408 |
| Dependency đúng bị từ chối (169) | **0** | 0 | 169 |
| Dependency sai bị nhận (333 mutation) | **0** | 333 | 0 |
| Nhắc tham số: sai / thiếu (69 tham số gold) | **0 / 0** | 101 / 69 | 0 / 69 |
| HTTP đúng bị từ chối (33) | **0** | 0 | 33 |
| HTTP sai bị nhận (125 mutation) | **0** | 125 | 0 |
| Ca "không phải HTTP" bị nhận (33) | **0** | 33 | 0 |
| Route/HTTP gold không bị đánh dấu (441) | **0** | 0 | 441 |
| Dòng đánh dấu thừa | 4 | 59 362 | 0 |

Phép đo prefix mới bắt được ngay 1 lỗi thật của bộ kiểm: `include_router(router=api_router, prefix="/api")` (AgentGPT) truyền router bằng từ khóa nên bị bỏ qua. Đã sửa.

Kết quả và phiên bản: `ket-qua-chay/fr029-checkaudit-20261009-r41*/summary.json` (hash `docfacts.py` dcc3b0fea3eeda48, `astscan.py` 985d5c92b667a6d7). Số liệu giống r26–r40.

Đo trên gold còn bắt được 1 crash do chính bản sửa vòng 6 gây ra (file không có thư viện HTTP). Đã sửa, có test.

## 4. Kết quả trên repo chưa dùng

Repo chưa từng dùng để chỉnh bộ kiểm. Bộ kiểm xuất "gói" gồm: tham số dependency nó nhắc, dòng nghi ngờ, decorator bị từ chối. Codex đọc source và chấm từng mục.

9 repo mới nhất lấy theo thứ tự kết quả `gh search repos fastapi --sort=updated --stars=">=10"`, bỏ repo trên 60 MB và repo không phải ứng dụng FastAPI (ví dụ SDK). Không chọn tay. Gói đã chấm: `ket-qua-chay/fr029-heldout-20261008-r13/` và `r18/`; đợt 3: `fr029-heldout-20261009-r30/`; gói sau sửa của cả 10 repo: `fr029-heldout-20261009-r32/`.

| Repo | Route | Tham số dependency | Dòng nghi ngờ | Bỏ sót HTTP trực tiếp |
|---|---|---|---|---|
| primer | 224 | 4 đúng, 0 sai, 0 thiếu | 26 HTTP thật, 1 đăng ký, **1 nhiễu** | 0 |
| caura | 343 | 0 sai, 0 thiếu | 19 HTTP, 2 urllib, 4 đăng ký, 0 nhiễu | 2 (`super().request`), **đã sửa** |
| shortlist | 163 | 0 sai, 0 thiếu | 43 HTTP thật, 7 session CSDL, 0 nhiễu | 0 |
| case_auto_hub | 301 | Codex thấy thiếu `Authorization` và 3 model làm dependency, **đã sửa** | 2 HTTP thật | 0 |
| facet (agent Claude) | 197 | 5 đúng; 1 "sai" do gói, bộ kiểm đúng | 5 urllib, 1 đăng ký, 0 nhiễu | 0 |
| spatiumddi (agent Claude) | 1184 | 4 đúng; 2 "sai", 2 "thiếu" do gói, bộ kiểm đúng | 216 HTTP, 5 http.client, 4 đăng ký, **6 nhiễu**, **đã sửa** | 2, **đã sửa** |
| PrintStash (agent Claude) | 436 | 2 đúng, 0 sai, 0 thiếu | 21 HTTP, 16 hợp lý, **57 nhiễu**, **đã sửa** (94 → 37 dòng) | 0 |
| PrintStash, chấm lại sau sửa (Codex) | 436 | 2 đúng, 0 sai, 0 thiếu | 21 HTTP, 3 đăng ký, 11 hợp lý, **2 nhiễu** | 0 |
| caura, chấm lại sau sửa (Codex) | 343 | 0 sai, 0 thiếu | 31 HTTP, 2 urllib, 4 đăng ký, 0 nhiễu | 0 theo FR-028 hiện tại (xem ghi chú) |
| ai-pdf-autofiller (Codex, code vòng 10) | 8 | 0 sai | 4 HTTP thật, 0 nhiễu | 0 |
| creatorhub (Codex, code vòng 10) | 184 | 0 sai | 7 HTTP, 2 urllib, 2 đăng ký, 39 hợp lý, 0 nhiễu | 0 |
| xianyu-auto-bot (Codex, code vòng 10) | 274 | 1 đúng, 0 sai | 66 HTTP thật, **13 nhiễu**, **đã sửa 11** | **7**, **đã sửa 5** |
| dispatch, nsidnev, rhoboro, rafsaf (lần trước) | — | 19 đúng, 0 sai | 15 HTTP thật | 0 |

Ghi chú:

- caura: Codex liệt kê thêm 44 lời gọi trong `scripts/` và file `*_test.py`. Các file này nằm ngoài phạm vi đọc theo FR-028, nên không tính là bỏ sót. Lần chấm lại, Codex tính 37 lời gọi trong 6 script `scripts/repro_*.py` vì chúng import một file helper cùng thư mục `scripts/`. Theo FR-028 hiện tại (chỉ tính import code ứng dụng), các file này nằm ngoài phạm vi. Đây là câu hỏi diễn giải phạm vi, chưa đổi luật.
- Gói của case_auto_hub và caura sau khi sửa khớp đúng những gì Codex nêu, nhưng Codex chưa chấm lại bản sửa.
- "Sai do gói": gói gom tham số theo tên dependency, không theo route. Ví dụ `album_id` có trong path route nên agent thật được nhắc `path`, còn gói ghi `query`. Hay 3 hàm `_require_bootstrap_key` cùng tên ở 3 module bị gộp làm một. Bộ kiểm thật xử lý đúng các ca này (test `HeldOutFindings`). Công cụ đo đã sửa để gói không còn gộp sai.
- PrintStash: 57 dòng nhiễu vì file dùng cú pháp Python 3.14 (`except A, B:`). Python 3.11 của bộ kiểm không parse được, nên rơi vào luật dự phòng đánh dấu mọi `.get(`. Đã sửa: thử parse lại sau khi thêm ngoặc.
- xianyu: nhiễu là `self.sessions.get(k)` với `self.sessions: Dict[...] = {}`. Các lời gọi bị sót: alias `request = session.post if ... else session.put`; `_host.aiohttp.ClientSession()`; mixin dùng `self.session` do lớp con ở file khác tạo. Còn sót 2 dòng `self.runtime.session.post(...)` (client nằm trên một đối tượng khác), chưa xử lý.
- spatiumddi: 6 dòng nhiễu là chữ `http.client` trong import và kiểu trả về. 2 lời gọi bị sót là thuộc tính giữ hàm tạo client (`self._client_factory = ... or self._default_client`) và `getattr(client, method)(...)`. Đã sửa cả hai.
- Thời gian chạy: 5–53 giây mỗi repo (spatiumddi 1184 route: 53 giây; caura trước khi tối ưu là 95 giây). Gói ra giống hệt trước và sau mỗi lần tối ưu.

## 5. Các vòng sửa

| Vòng | Ai tìm | Lỗi chính đã sửa |
|---|---|---|
| 1–17 | Công cụ đo, Codex vòng 1–3 | Xem báo cáo các lượt trước. Bộ kiểm chuyển sang đọc cây cú pháp |
| 18–20 | Codex vòng 4 (8 phản ví dụ) | Route phải nằm dưới đúng app, đủ prefix của `include_router`; config key phải nằm trong đối số URL; client theo annotation; dependency là instance có `__call__`; `Literal`/`Enum`; client trên `app.state` |
| 21–26 | Codex vòng 5 (7) và repo chưa dùng | Prefix trong `APIRouter(prefix=...)`; `config_at` phải tạo đúng client được gọi; thư viện của client theo từng hàm; `import clients` rồi `clients.wire.get`; alias `Annotated[httpx.Client, Depends(...)]` import từ file khác; `functools.partial`; `Annotated[X, Depends()]`; model Pydantic làm dependency; `Depends(Class())` đọc `__call__`; `Union[int, str]`; `include_router(router=...)`; `super().request` trong lớp con client; lớp con client mang theo thư viện gốc |
| 27 | Codex vòng 6 (8) | Thứ tự prefix phải đúng thứ tự áp dụng; hàm `attach` không ai gọi không làm tắt kiểm prefix; `self.app.include_router` không còn bị coi là "chưa đăng ký"; URL tuyệt đối bỏ qua `base_url`; `self.client` xét theo từng class; client xuất lại qua `__init__.py`; `__init__` kế thừa; `Field(alias=...)`; `partial` theo từ khóa vẫn là tham số |
| 28–30 | 3 repo chưa dùng (agent Claude) | Cú pháp Python 3.14 `except A, B:`; `http.client` chỉ tính khi gọi `HTTPSConnection(`; thuộc tính giữ hàm tạo client; `getattr(client, method)` với tên động |
| 31 | Agent Claude vòng 7 (9) | Lớp con `APIRouter` và `import APIRouter as Router` bị **từ chối nhầm**; prefix phải nằm trên đường đăng ký, không lặp, đúng literal; helper đăng ký được gọi thì lần theo lời gọi; tên dependency phải là đích của `Depends`, không phải tên tham số hay kiểu; config key phải là tên trọn vẹn; `config_at` của `self.client` class khác; `self._client().get`; nhắc khi handler dùng `Depends(x)` mà agent không khai |
| 32–33 | Codex vòng 7 (8) | Thứ tự `include_router` (FastAPI chép route lúc include); handler nhiều decorator; `.get().json()` không phải client; `to_thread(c.get, url)`; client sau `@property`; model query `Annotated[M, Query()]`; `Depends(dependency=f)`; `Header as H` |
| 34–35 | Codex vòng 8 (7) | Prefix router trong hàm factory; `wire = self._wire`; `dict[str, httpx.Client]` không phải client; `self.fetch = self._wire.get`; claim cho `to_thread(c.get, url)`; trường `list[str]` của model query; `alias_generator=to_camel`; `__call__` kế thừa của instance |
| 36–37 | Agent Claude vòng 9 (8) | `from . import items`; `include_router` trong vòng `for`; dependency cấp router/app chưa khai; alias dependency chưa khai; client từ `app.state` qua provider không annotation; tên `client` là redis ở hàm khác (**nhận nhầm**); `self._client` của lớp cha file khác; `deps.common` trùng tên ở 2 module. Thêm: module dự án tên `requests` bị coi là thư viện (do chính bản sửa gây ra, đã sửa) |
| 38 | Codex vòng 9 (7) | `include_router` trong nhánh `if FLAG:` với `FLAG = False`; `wire: httpx.Client = ...` giữ thư viện; `Depends(dependency=provide)` cho client; `clients['a'].get`; `partial(wire.get, url)` chưa gửi request; alias kiểu `UserId = UUID`; path converter `{id:int}` |
| 39 | Codex vòng 10 (6) | `routers = [r]; for router in routers`; tham số che client toàn cục cùng tên (**nhận nhầm**); `AsyncExitStack.enter_async_context`; provider qua `partial`; `alias=HẰNG`; marker dùng lại qua biến; dòng chỉ tạo `partial` không còn bị đánh dấu |
| 40–41 | 3 repo chưa dùng đợt 3 (Codex) | Thuộc tính dict khai có annotation; alias method qua biểu thức điều kiện; thư viện qua module khác; mixin dùng client do lớp con tạo. Thêm: chuỗi/thuộc tính tên `requests` không còn làm file bị coi là dùng thư viện HTTP (do chính bản sửa gây ra, đã sửa) |

Mỗi lỗi có một test riêng: 137 test trong `slice/tests/test_checker_counterexamples.py`. Test viết trước và chạy đỏ rồi mới sửa. Riêng 2 test (`album_id` là path, factory gọi trong alias) qua ngay từ đầu: đó là test khóa hành vi đúng sẵn có, viết để xác minh nhận xét của giám khảo. Toàn bộ test: 425/426, lỗi duy nhất là `test_gateway` có từ trước.

## 6. Mức tin cậy

| Phần | Codex vòng 5 | vòng 6 | vòng 7 | vòng 8 | vòng 9 | vòng 10 |
|---|---|---|---|---|---|---|
| Nhận diện route | vừa | vừa | vừa | vừa | vừa | vừa |
| Kiểm claim HTTP | thấp | thấp | thấp | thấp | thấp | thấp |
| Quét lời gọi HTTP bị sót | thấp | thấp | thấp | thấp | thấp | thấp |
| Nhắc tham số dependency | vừa | vừa | vừa | vừa | vừa | vừa |

Mỗi vòng Codex xác nhận gần hết phản ví dụ của vòng trước đã xử lý (vòng 9: 8/8; vòng 10: 6/7, ca còn lại đã sửa nốt), nhưng vẫn tìm thêm dạng mới, nên mức đánh giá không đổi. Các bản sửa vòng 10 chưa có Codex kiểm lại.

Trên repo thật, kết quả sau sửa tốt hơn mức "thấp" này gợi ý: PrintStash từ 57 dòng nhiễu còn 2, caura từ 2 lời gọi bị sót còn 0 (Codex chấm lại). Mức "thấp" phản ánh việc vẫn còn dạng code chưa xử lý, không phải tỉ lệ lỗi đo được.

Lý do Codex vẫn để mức "thấp" cho HTTP: còn dạng chưa xử lý (client là tham số không annotation, `getattr(wire, "get")(url)` được đánh dấu nhưng claim bị từ chối), và phép đo recall theo dòng có thể che việc thiếu một trong hai lời gọi trên cùng dòng.

Hậu quả khi bộ kiểm sai:

- **Nhận nhầm:** một dữ kiện sai lọt vào tài liệu.
- **Từ chối nhầm:** agent phải nộp lại hoặc ghi `unknown`.
- **Bỏ sót dòng nghi ngờ:** không ai nhắc agent. Agent vẫn đọc toàn bộ file, nên chưa chắc thành lỗi.

## 7. Giới hạn và việc cần anh/chị quyết

**Cần quyết:**

1. **Lời gọi qua hàm bọc của dự án** (`http_retry.get(url)` gọi tiếp `httpx.request`) có tính là lời gọi HTTP không. Hiện chỉ tính lời gọi trực tiếp httpx/requests/aiohttp; lời gọi bên trong hàm bọc vẫn bị đánh dấu. Dạng này gặp ở shortlist và case_auto_hub. Nếu tính, cần thêm luật và gold mới.
2. **Agent thuần hay kết hợp.** Phần (2) và (3) của bộ kiểm ngày càng giống phân tích tĩnh. Dữ kiện vẫn do LLM nộp.

**Giới hạn đã biết:**

- Công cụ đo chưa theo dependency gắn ở cấp router/app, và tên dependency truyền qua tham số factory. Codex xác nhận các trường hợp gặp đều không có tham số request.
- Mutation HTTP chưa đổi `config_at`/`client_at`; bộ kiểm giả chưa đi trọn `add_route`.
- Gold phủ ít lời gọi HTTP: 33 lời gọi, 12 có URL literal. Nhắc tham số đo được trên 14/37 bộ.
- Gold không có dòng nào chứa 2 lời gọi HTTP, nên tính chất "dòng còn lời gọi chưa nộp vẫn bị đánh dấu" chỉ có unit test, chưa đo trên gold.
- Gold của 4 repo mới do 2 agent viết, chưa có người duyệt.
- Chưa đo lại toàn bộ sản phẩm bằng LLM sau các sửa này (tài khoản OpenAI hết tiền).
