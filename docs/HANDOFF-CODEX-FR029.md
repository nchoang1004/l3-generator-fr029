# Bàn giao cho Codex: FR-L3GEN-029, làm tới bước 14

Ngày 02/10/2026. Người giao: Hoàng. File này nói việc còn lại, luật phải giữ và cách kiểm.

Yêu cầu gốc của Hoàng: "kéo commit evidence về và tiếp tục hoàn thiện cho đến bước 14 của fr29 l3-generator-l3". Bước 14 là "Implementation" trong `Quy_tac/execution-guide-working.md` mục B.0 và B.15.

## 1. Đã xong

| Việc | Kết quả |
|---|---|
| Nhánh | `feature/l3-fr029` tạo từ `origin/feature/quote-evidence` commit `79c8235` (tài liệu kiến trúc của Khiêm). Không có upstream. Chưa commit gì. |
| Chép code L3 | `slice/`, `scripts/check_l3_contracts.py`, `scripts/requirements-l3-check.txt`, `.aide/tech-specs/`, `.aide/generated/contract-checks/` lấy từ nhánh `feature/l3-slice`. Đang ở trạng thái staged. |
| Stash | `stash@{0}` là bản chép `.aide` cũ từ commit `66b1d3c`. Không cần nữa, đừng `pop`. |
| Test | 176/177 qua. Lỗi duy nhất là `test_gateway.Gateway.test_unknown_ids_are_dropped`: lỗi có sẵn của file test (nó chọn `facts[0]`, không thuộc component đang hỏi). **Hoàng quyết để nguyên, không sửa.** |
| `prd_package.py check --change-set CHG-L3GEN-2026-002 --baseline BL-r10.yaml` | Khớp |
| Bước 9 (một phần) | API-L3GEN-004-v1 r5 và API-L3GEN-008-v1 r5 đã thêm phần FR-029. API-001 r5, API-002 r5 chỉ sửa link FR cũ sang `requirements/_superseded-r28/fr/`. |

## 2. Phạm vi Hoàng đã chốt

| Mã | Việc | AC |
|---|---|---|
| T1 | Route khai bằng `add_api_route`, `add_api_websocket_route`, `add_route`, `add_websocket_route` không sinh route; mỗi lời gọi một limitation `ROUTE_NOT_DECORATOR` ghi `file:dòng` | AC-L3GEN-029-05 |
| T2 | File test không sinh route, kể cả app/router khai trong file test | AC-L3GEN-029-05 |
| T3 | Lời gọi HTTP qua client và qua `aiohttp`; thư viện HTTP khác thì ghi limitation `HTTP_LIBRARY_UNSUPPORTED` | AC-L3GEN-029-08 |
| T4 | README có mục "Lời gọi HTTP ra ngoài" | AC-L3GEN-029-06, 029-08 |
| T5 | Response `list[Model]` | AC-L3GEN-029-02 |

**Không làm** (Hoàng đã bỏ):
- AC-029-04: cần `archdia.json` từ code của Khiêm, chưa có trên GitLab.
- AC-029-07 và mục README "Cấu trúc component": vai trò file thuộc CMP-005, đã có ở `l3gen.role` của Khiêm.
- Đọc cú pháp Python 3.14: máy chỉ có Python 3.11, 3.12.
- T6: cho L3 vẫn sinh khi quá 50 component.
- Phần mã lỗi của nhánh thử nghiệm `exp/codegraph-ideas`.
- Giao diện web: PRD rev 31 dời web sang giai đoạn sau.

## 3. Luật bắt buộc

1. **Không commit, không push.** Hoàng tự quyết.
2. **Không sửa spec:** PRD, FR, NFR, CMP, ADR trong `.aide/`. Thấy mâu thuẫn thì tạo OQ trong `.aide/lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/` rồi dừng việc đó. Riêng `.aide/tech-specs/` là contract của bước 9, được sửa.
3. Không sửa tay `.aide/generated/`. Chỉ sinh lại bằng script.
4. Không chạy code của repo đầu vào. Chỉ đọc bằng `ast`.
5. Code L3 chỉ dùng thư viện chuẩn. Viết theo phong cách code xung quanh. Không refactor chỗ không liên quan.
6. Tài liệu viết tiếng Việt, câu ngắn, theo `CLAUDE.md` mục 0.
7. Architecture Gate (BL-r10) **chưa ký**. Mọi file bước 9–13 ghi rõ "nháp, chờ Architecture Gate BL-r10".
8. Không tắt server demo cổng 8765 (PID 7256), vì Hoàng đang dùng để trình bày. Sửa code không ảnh hưởng server cho tới khi nó khởi động lại.

## 4. Việc còn lại theo bước

### Bước 9: hoàn tất contract

1. `scripts/check_l3_contracts.py` đang lỗi ở `docs/L3-Generator-ke-hoach-trien-khai-L3.md`, link `../.aide/requirements/fr/FR-L3GEN-027.md`. Script đọc file này ở dòng 461. Đổi mọi link FR-019 đến 027 trong file đó sang `../.aide/requirements/_superseded-r28/fr/…`.
2. Khi làm T4: thêm thuộc tính `call_text` (nguyên văn biểu thức gọi, đã che bí mật) vào dòng `http_call` ở mục 2 của API-004 r5. README cần "bằng chứng kèm nguyên văn", mà renderer không có source.
3. Chạy lại cho tới khi qua, rồi sinh báo cáo:
   ```powershell
   $env:PYTHONIOENCODING='utf-8'
   scripts/.venv/Scripts/python.exe scripts/check_l3_contracts.py
   scripts/.venv/Scripts/python.exe scripts/check_l3_contracts.py --report
   ```

### Bước 11: Epic, Story, Task

Viết theo mẫu `Quy_tac/execution-guide-working.md` mục B.12. Story không viết given/when/then. Artifact khác có `uid` thì chạy `scripts/gen_uid.py` để sinh, không tự bịa.

| File | Cha | Nội dung |
|---|---|---|
| `.aide/lifecycle/epics/EPIC-L3GEN-029.md` | `change_set: CHG-L3GEN-2026-002` | `implements: [FR-L3GEN-029]`, `affected_components: [CMP-L3GEN-004, CMP-L3GEN-008]`, `contracts.produces: [API-L3GEN-004-v1, API-L3GEN-008-v1]`; mục Phạm vi ghi phần bỏ ở mục 2 file này |
| `.aide/lifecycle/stories/STORY-L3GEN-029-02.md` | EPIC-L3GEN-029 | `satisfies: [AC-L3GEN-029-02]`; Task: T5 |
| `.aide/lifecycle/stories/STORY-L3GEN-029-05.md` | EPIC-L3GEN-029 | `satisfies: [AC-L3GEN-029-05]`; Task: T1, T2 |
| `.aide/lifecycle/stories/STORY-L3GEN-029-08.md` | EPIC-L3GEN-029 | `satisfies: [AC-L3GEN-029-06, AC-L3GEN-029-08]`; Task: T3, T4 |
| `.aide/lifecycle/tasks/TASK-L3GEN-029-1.md` đến `-5.md` | story tương ứng | `implements: [CMP-L3GEN-004]` (T1–T3, T5) hoặc `[CMP-L3GEN-008]` (T4, T5); mục "Xong khi" lấy từ mục 5 file này |

Không ghi `implementation_target` hay `validated_by` vào FR, vì đó là spec. Ghi tên test vào mục "Xong khi" của Task.

### Bước 12: Context package

Mỗi Task một file `.aide/evidence/context/CTX-TASK-L3GEN-029-N.yaml`, theo mẫu mục C.1:
- `requirements`: FR-L3GEN-029 và AC của Task.
- `design`: CMP-L3GEN-004 hoặc 008.
- `decisions`: ADR-2026-003, ADR-2026-004.
- `contracts`: API-L3GEN-004-v1 r5, API-L3GEN-008-v1 r5.
- `constraints`: NFR-L3GEN-ACC-002, NFR-L3GEN-OPS-001, NFR-L3GEN-SEC-002.
- `code_scope`: `slice/l3slice/extract.py`, `slice/l3slice/render.py`, `slice/tests/**`.
- `inputs`: revision và SHA-256 của từng file đầu vào, tính bằng script.
- `authority.baseline`: `BL-CHG-L3GEN-2026-002-r10`, kèm ghi chú "chưa ký".

### Bước 13: Plan

Mỗi Task một file `.aide/evidence/plans/PLAN-TASK-L3GEN-029-N.md`, viết **trước** khi sửa code. Chỉ thêm, không sửa lại. Đổi hướng thì viết revision mới.

Theo thứ tự TDD (RED rồi GREEN). Mỗi bước ghi: file nào đổi, đổi gì, kiểm bằng cách nào. Có mục "Không làm".

### Bước 14: Code

Số dòng dưới đây là của nhánh hiện tại.

**T2 trước** (T1 và T3 dùng chung hàm này):
- Thêm `_is_test_file(path)` trong `slice/l3slice/extract.py`, theo FR-028 "Phạm vi phân tích":
  - có một thư mục tên `tests` hoặc `test`;
  - hoặc tên file là `test_*.py`, `*_test.py`, `conftest.py`.
- Trong `extract()` (dòng 1389), truyền cho `_routes` (dòng 495, gọi `_Routers` ở dòng 269) bộ `files` đã bỏ file test. Như vậy app/router và `include_router` khai trong test cũng không tạo đường gắn.
- Bảng, sự kiện, cấu hình, symbol, reference giữ nguyên. Ghi điều này vào nhật ký.
- Test: fixture có `tests/conftest.py` tạo `FastAPI()` và `include_router` router thật, cộng một `@app.get` trong file test. Kỳ vọng:
  - không có route của file test;
  - route thật chỉ có `registration_context` từ app thật.

**T1:**
- Hàm mới, gọi trong `extract()`. Duyệt `ast.Call` có `func` là `Attribute` mang một trong bốn tên ở mục 2, bỏ file test.
- Mỗi lời gọi một `b.limit("ROUTE_NOT_DECORATOR", f"{path}:{dòng}: {ast.unparse(node.func)}(…) khai route không qua decorator; chưa đọc ở đợt này", [file_id])`.
- Test:
  - 2 lời gọi cho ra 2 limitation, đúng dòng;
  - không sinh route fact;
  - README có 2 dòng này ở mục Giới hạn.

**T3:** sửa `_http_and_config` (dòng 1146), `HTTP_LIBS` (dòng 37).
- Hàm của module: `httpx.*`, `requests.*`, `aiohttp.request(method, url)`.
- Client: `httpx.Client`, `httpx.AsyncClient`, `requests.Session`, `requests.session`, `aiohttp.ClientSession`.
- Biến là client khi một trong các điều sau đúng. **Không nhận theo tên biến.**
  - được gán trong khối `with`/`async with` bao quanh lời gọi;
  - được gán trong cùng hàm;
  - là tham số có chú thích kiểu là client;
  - được gán ở mức module, và hàm không gán lại tên đó;
  - là `self.x`, được gán trong một method của cùng class.
- Method lấy từ tên hàm. Riêng `.request(...)` thì lấy đối số đầu nếu là literal, không thì `unknown`.
- Thuộc tính:
  - `method`, `url` (như cũ: literal thì bỏ query; không literal thì `unknown` kèm lý do), `target_unit_id`;
  - `library`, `call_text` (che bí mật bằng luật có sẵn trong `common.py`);
  - `url_config_key` khi URL là `settings.X` (nhận `settings` như `_settings_default`, dòng 232), `os.getenv("X")` hoặc `os.environ["X"]`.
- Bỏ file test.
- Import `urllib.request`, `http.client`, `urllib3`, `httpcore`, `pycurl`, `treq`, `niquests`, `grequests`, `tornado.httpclient` thì ghi một limitation `HTTP_LIBRARY_UNSUPPORTED` kèm `file:dòng`, giống cách làm của `_unsupported_queues` (dòng 1204). `_imports` chỉ giữ tên module cấp đầu, nên cần quét tên đầy đủ.
- Test, mỗi ca một test:

  | # | Code đầu vào | Kỳ vọng |
  |---|---|---|
  | 1 | `async with httpx.AsyncClient() as c: await c.get("https://a.x/y?q=1")` | `url` = `https://a.x/y`, `library` = httpx |
  | 2 | `aiohttp.ClientSession()` rồi `session.post(...)` | Có http_call, `library` = aiohttp |
  | 3 | Cùng file có hàm khác dùng `session.get(Item, 1)` của SQLAlchemy | **Không** sinh http_call |
  | 4 | `self.client = httpx.AsyncClient()` trong `__init__`, `self.client.get(...)` trong method khác | Có http_call |
  | 5 | `requests.get(settings.PAYMENT_URL)` | `url` unknown, `url_config_key` = `PAYMENT_URL` |
  | 6 | `client.request("GET", u)` | `method` = GET |
  | 7 | Lời gọi client trong `tests/` | Không có fact |
  | 8 | `import urllib.request` | Có limitation `HTTP_LIBRARY_UNSUPPORTED` |

**T4:**
- Trong `readme()` (`render.py` dòng 632), sau mục "Contract chưa gán được component", thêm mục `## Lời gọi HTTP ra ngoài`.
- Bảng có các cột: Component | Thư viện, method | Đích | Bằng chứng.
- Component là component có `member_file_ids` chứa `evidence[0].file_id` của fact, trong `verified["model"]["components"]`.
- Đích:
  - `url` nếu known;
  - không có thì "khóa cấu hình `X`";
  - không có cả hai thì `unknown — lý do`.
- Bằng chứng là `path:dòng` và `call_text`. Mọi chuỗi đi qua `md()`.
- Không có lời gọi nào thì ghi `- (không có)`.
- Test:
  - README có đúng một dòng cho mỗi http_call;
  - escape đúng khi URL có `|`.

**T5:** sửa `extract.py` dòng 611–627.
- Khi `response_model` hoặc kiểu trả về là `list[M]`, `List[M]`, `Sequence[M]`, `set[M]` với `M` là Pydantic model của repo:
  - `response_model_ids` known `[M]`;
  - body response thêm `"array": True`;
  - kiểu trả về thì vẫn ghi luật `fastapi-defaults-v1`.
- Trong `render.py`:
  - `_models_cell` (dòng 233) hiện `list[M]`. Hàm cần biết body là mảng, nên truyền thêm `bodies`.
  - Ở dòng 333, schema thành `{"type": "array", "items": <ref>}` khi `b.get("array")`.
- Test:
  - `response_model=list[UserOut]` và `-> list[UserOut]`;
  - bảng ghi `list[UserOut]`;
  - khối OpenAPI qua `openapi_spec_validator`, `items` là `$ref` tới UserOut.

**Nhật ký:** mỗi Task một file `.aide/evidence/diaries/DIARY-TASK-L3GEN-029-N.md`, theo mẫu B.15: Diễn giải, Đi chệch, Đánh đổi, Câu hỏi mở, có giờ. Ghi sẵn các điểm sau:
- Có thêm `add_api_websocket_route`, ngoài danh sách 3 tên của FR.
- Chỉ loại file test cho route và HTTP.
- Test `test_unknown_ids_are_dropped` lỗi từ trước, để nguyên theo quyết định của Hoàng.
- `satisfies` của API-004 và API-008 đã đổi sang FR mới.

## 5. Kiểm cuối (Definition of Done)

| # | Kiểm | Đạt khi |
|---|---|---|
| 1 | `scripts/.venv/Scripts/python.exe -m unittest discover -s slice/tests` | Mọi test qua, trừ `test_unknown_ids_are_dropped`; có test mới cho T1–T5 |
| 2 | `scripts/check_l3_contracts.py`, rồi `--report` | Qua |
| 3 | `scripts/prd_package.py check --change-set CHG-L3GEN-2026-002 --baseline BL-r10.yaml` | Khớp toàn bộ |
| 4 | `slice/tools/run_golden.py --golden-root "D:/VSF/VSF-L3 Generator" --out <thư mục mới>`, chạy trước và sau khi sửa | Route vẫn 58/58. Số khác đi đều giải thích được. |
| 5 | So trước và sau trên 4 repo `D:/VSF/l3-generator-quote-evidence/sample-repos/*` (dùng output của bước 4) | teamhide `GET /api/v1/user` có response `list[GetUserListResponseDTO]`. Ghi số `http_call`, `ROUTE_NOT_DECORATOR`, `HTTP_LIBRARY_UNSUPPORTED` mỗi repo vào nhật ký. |
| 6 | `git status` | Chỉ có file trong phạm vi mục 4. Không commit. |

Lệnh `analyze` bắt buộc có `--membership`. Vì vậy dùng `run_golden.py` để chạy trên repo thật, không tự viết file membership.

## 6. Báo lại cho Hoàng

Báo ngắn bằng tiếng Việt:
- Task nào xong, kèm test nào chứng minh.
- Số trước và sau ở mục 5.
- OQ đã tạo, nếu có.
- Chỗ nào làm khác file này, và vì sao.
