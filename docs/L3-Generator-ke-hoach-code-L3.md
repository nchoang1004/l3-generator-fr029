# Kế hoạch code phần còn lại của L3 Generator

Ngày 01/10/2026. Trạng thái: **kế hoạch, chưa code**. File này là kế hoạch code duy nhất. Nó thay hai bản nháp cùng ngày: bản phủ toàn sản phẩm và bản "hoàn thiện bộ sinh tài liệu G0–G8".

- **Phạm vi:** code theo 8 contract revision 4 ở [.aide/tech-specs](../.aide/tech-specs/README.md). Không gồm UI cấp 4.
- **Điểm xuất phát:** lát cắt đầu ở [slice/](../slice/README.md), 27 test pass. Nhánh `docs/l3-align-gate2`, chưa commit.
- **D-03 vẫn mở.** Kế hoạch có khung thí nghiệm, không tự chọn thuật toán chia component.

## 1. Đã có và còn thiếu

| Component | Đã có trong `slice/` | Còn thiếu |
|---|---|---|
| CMP-001 Điều phối | CLI, exit code 0/2/3 | Vòng đời run, hàng đợi FIFO, retry, hạn 24 giờ, HTTP facade |
| CMP-002/003 Tiếp nhận, kiểm kê | Thư mục local, file `.py`, một unit | ZIP, GitHub public, giới hạn, nhiều unit theo manifest, mức hỗ trợ |
| CMP-004 Trích dữ kiện | Route của router cấp module; bảng `Column` | Xét import, `include_router`, model, tham số, status, body; SQLAlchemy 2.0, SQLModel; http, config, event, library, reference |
| CMP-005 Mô hình | Membership fixture, owner | Cạnh tĩnh; đặt tên và đề xuất cạnh bằng LLM; repo phẳng; D-03 |
| CMP-006 Cổng LLM | Chưa có | Client Groq/Gemini, ngân sách, đọc code giới hạn, che bí mật |
| CMP-007 Kiểm bằng chứng | 4 rule: CONTRACT-FIELD, CONTRACT-OWNER, MEMBER-SOURCE, event-binding | resolved-target, http-binding, config-binding, LABEL-DIRECT; kiểm theo range hẹp; kiểm lại khi mở evidence |
| CMP-008 Xuất | JSON, README, Mermaid, API/TBL/EVT, kiểm bản xuất | Kiểm theo ID thay vì tìm chuỗi; link evidence; SVG thật; publish an toàn; retry; DDL có tham số kiểu |

## 2. Hai quyết định đặt sẵn

Hai lựa chọn dưới đây là mặc định của kế hoạch. Muốn đổi thì sửa mục này trước khi bắt đầu đợt liên quan.

| Câu hỏi | Mặc định | Lý do | Nếu đổi |
|---|---|---|---|
| Ai viết bộ trích dữ kiện (CMP-004)? | Người làm L3 viết, dùng lại code của `l3gen` 0.1 | `l3gen` 0.1 đã có cây `include_router`, bảng tên và nhận diện ORM. `graph.json` của pipeline v8 chưa có dữ kiện route/bảng/event | Nếu pipeline của Khiêm cấp dữ kiện: Đợt 1 đổi thành bộ chuyển sang `VerifiedResult` (API-008 §1); các đợt khác giữ nguyên |
| SVG vẽ bằng gì? | Tự sinh SVG từ danh sách node và cạnh, bố cục lưới | Không cần Node.js và trình duyệt; không chạy JavaScript trên chữ lấy từ repo không tin cậy | Mermaid CLI: phải cài Node ≥22 và trình duyệt, chặn mạng, lọc SVG. Bỏ hẳn SVG: phải sửa API-008, vì contract bắt buộc artifact `diagram_image` |

## 3. Nguyên tắc

- **Không import, không chạy code của repo đầu vào.** Loại mọi cách dùng `app.openapi()`, `alembic`, import model ORM, kết nối DB.
- **Lõi chỉ dùng thư viện chuẩn.** `jsonschema`, `openapi-spec-validator`, `sqlglot` chỉ dùng trong test.
- **Output của mỗi đợt phải qua schema contract và `check_bundle_invariants`.** Muốn đổi hành vi so với contract thì sửa contract trước, tăng revision.
- **Thiếu dữ kiện thì ghi `unknown` kèm lý do.** Không bịa status, body, auth, kiểu SQL, quan hệ event.
- **Không dùng tập held-out của golden khi phát triển.** Chỉ chạy một lần ở Đợt 10. Kết quả lần đó là kết quả chính thức; muốn đo lại sau khi sửa thì cần một tập held-out mới.
- **Mỗi số đo ghi kèm tên tập** (dev hoặc held-out) và trạng thái gold. Gold chưa review thì chỉ báo TP/FP/FN, không báo tỷ lệ (quy định D12 của bộ chấm).

## 4. Nguồn tham khảo

"Dùng code" là đưa code vào sản phẩm, "ý tưởng" là chỉ học cách làm, "đo" là chỉ dùng làm đáp án. Trước khi chép code của nguồn ngoài phải kiểm giấy phép và ghi commit nguồn.

| Nguồn | Dùng cho | Cách dùng | Lưu ý |
|---|---|---|---|
| `l3gen` 0.1 (nhánh `feat/language-first-semantic-v2`, `src/l3gen/`) | Đợt 1–2 | Dùng code: `routes.py`, `resolution.py`, `literals.py`, `orm/sqlalchemy.py`, `external.py`, `callgraph.py`, `discovery.py` | Sửa 4 lỗi đã biết: chỉ nhận router cấp module; bỏ unit không có FastAPI; bỏ lời gọi cấp module; suy tên bảng từ tên class (trái AC-021-02) |
| Golden v1 (`evaluation/golden/v1`, thư mục `D:\VSF\VSF-L3 Generator`) | Đợt 1, 2, 10 | Đo: 38 case dev, 27 case held-out | Cần bộ chuyển FactSet → định dạng gold |
| [CodeQL FastApi.qll](https://codeql.github.com/codeql-standard-libraries/python/semmle/python/frameworks/FastApi.qll/module.FastApi.html) | Đợt 1 | Ý tưởng: danh sách cách khai báo route/router | Không chạy CodeQL |
| [FastStream](https://github.com/ag2ai/faststream), tài liệu kafka-python/aiokafka | Đợt 1 | Ý tưởng: mẫu khai báo event | Không chạy app để sinh AsyncAPI |
| [Pydantic mypy plugin](https://docs.pydantic.dev/latest/integrations/mypy/) | Đợt 1 | Ý tưởng: đọc trường model từ annotation | Không chạy mypy |
| [PyCG](https://github.com/vitsalis/PyCG) | Đợt 2 | Đo: 30 case golden lấy đáp án từ PyCG | Đã archive từ 26/11/2023 |
| [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator/blob/ea65d43d9bd997867a536b09799195810b7d88a4/modules/openapi-generator/src/main/resources/markdown-documentation/api.mustache) | Đợt 4 | Ý tưởng: bố cục trang endpoint/tham số/response | Template mặc định ghi "No authorization required" khi thiếu auth, tức là bịa; không dùng |
| [tbls](https://github.com/k1LoW/tbls/blob/aa7e7326b3555205148c20cd4702ccdacf9af7c4/output/md/md_pipe_escape_test.go) | Đợt 4 | Ý tưởng: trình bày bảng; test dấu `\|` làm vỡ ô Markdown | Kết nối DB để đọc schema; không dùng phần đó |
| [CodeBoarding](https://github.com/CodeBoarding/CodeBoarding/blob/eea883fed36a67d7fc286b7b1ffb25c21f366696/output_generators/rendering.py) | Đợt 4, 5, 7 | Ý tưởng: lập danh sách file trước khi ghi; manifest; LLM chỉ đặt tên, nhóm do phân tích tĩnh lập | Gộp cạnh theo cấp và xóa file cũ khi render lại; trái contract |
| [DeepWiki-Open](https://github.com/AsyncFuncAI/deepwiki-open/blob/d92819a9c9f3b99416e3580ff235fc9d3adf8b89/api/services/wiki/content.py) | Đợt 4 | Ý tưởng: link nguồn theo host và range | Link phải đi từ evidence ID và commit đã pin, không từ regex |
| [AsyncAPI Generator](https://github.com/asyncapi/generator/blob/a1f05260d53f0703bc45aff6ec4fadacc1dd7eed/apps/generator/lib/parser.js) | Đợt 4 | Ý tưởng: kiểm payload schema trước khi render | EVT vẫn là Markdown + JSON Schema, không đổi sang AsyncAPI |
| [sqlglot](https://github.com/tobymao/sqlglot) | Đợt 4 | Dùng code, chỉ trong test: parse DDL theo dialect | Parse được chưa chắc DB nhận |
| [Groq Structured Outputs](https://console.groq.com/docs/structured-outputs) | Đợt 6 | Xác nhận: không dùng chung `json_schema` với tool trong một request, nên gọi hai pha | — |
| [LiteLLM](https://docs.litellm.ai/docs/proxy/users) | Đợt 6 | Ý tưởng: đếm request/token theo phút | Không dùng: tự chuyển provider, trái NFR-AI-002 |
| [detect-secrets](https://github.com/Yelp/detect-secrets) | Đợt 6 | Dùng code hoặc chép plugin regex + entropy | Kiểm giấy phép trước khi chép |
| [arcade-agent](https://github.com/arcade-agent/arcade-agent) | Đợt 7 | Ý tưởng: thuật toán PKG/WCA/ACDC/LIMBO để so cho D-03 | MIT; chỉ dùng trong thí nghiệm |
| [GitHub REST — repository archive](https://docs.github.com/en/rest/repos/contents) | Đợt 8 | Lấy default branch → commit SHA → tải zipball theo SHA | Server trả 302 sang `codeload.github.com` |

Không chọn: grimp (README yêu cầu cài package cần phân tích), merm (ít người dùng, giấy phép WTFPL), RepoDoc (GitHub trả `license: null`).

## 5. Các đợt code

Ước lượng tính bằng ngày công của một người, **chưa đo**. Mỗi đợt có mục "Xong khi"; chưa đạt thì chưa tính là xong.

Trạng thái 01/10/2026 (bản 2) và số đo: xem [báo cáo tổng thể](L3-Generator-bao-cao-tong-the.md). "Đã code" nghĩa là có code và test, chưa phải đã nghiệm thu.

### Đợt 0 — Sửa lỗi đã biết trong lát cắt (0,5–1 ngày) — **đã xong 01/10/2026**

Kết quả: 5 lỗi có test tái hiện trong `slice/tests/test_known_bugs.py`; 39 test pass; môi trường mới dựng từ `scripts/requirements-l3-check.txt` chạy được (thử trên cùng máy, Python 3.11.9).

1. `render._publish` đang xóa thư mục `<output>.staging` nếu đã có, nên có thể xóa nhầm thư mục của người dùng. Đổi sang thư mục tạm riêng của run, chỉ dọn thứ do run tạo.
2. `extract.py` gán dialect cho mọi bảng chỉ vì snapshot có đúng một `create_engine`. Đổi thành `unknown`, trừ khi có liên kết đã chứng minh giữa engine và `Base`.
3. `check_parity` tìm fact ID bằng tìm chuỗi; kiểm cạnh Mermaid bằng đếm `-->`. Đổi sang so tập ID và bộ ba `(nguồn, đích, loại)`.
4. Rule CONTRACT-FIELD chưa kiểm `status_codes`. Thêm kiểm theo đúng range của tham số `status_code`, để chữ `200` trong comment không được tính là bằng chứng.
5. Viết hướng dẫn dựng môi trường test trên máy sạch.

**Xong khi:** mỗi lỗi có một test tái hiện, fail trước khi sửa và pass sau khi sửa; 27 test cũ vẫn pass.

### Đợt 1 — Bộ trích dữ kiện CMP-004 (4–5 ngày) — **đã code, đo trên dev**

1. Chuyển `routes.py`, `resolution.py`, `literals.py` của `l3gen` 0.1 sang fact `route` theo API-004: xét import và alias; cây `include_router` và prefix; router tạo trong hàm; method `head`/`options`.
2. Request/response model: class kế thừa `BaseModel`, trường lấy từ annotation, phân biệt required và nullable. Tham số path/query/header/cookie lấy từ chữ ký handler. `Depends(...)` ghi thành reference, không kết luận auth.
3. **Sửa API-004 trước:** thêm phần ghép body với model, status và media type, mỗi phần kèm evidence. Chưa có phần này thì không sinh `content` trong OpenAPI.
4. Bảng: chuyển `orm/sqlalchemy.py`; thêm `Mapped[...]`/`mapped_column`; bỏ suy tên bảng từ tên class; giữ tham số của `String(n)`, `Numeric(p,s)`.
5. `http_call` (từ `external.py`), `config`, `event` (kafka-python, aiokafka, confluent-kafka, FastStream), `library` (`pyproject.toml`, `requirements*.txt`).
6. Mỗi giá trị ghi evidence là range hẹp của đúng node trong cây cú pháp, có cột bắt đầu/kết thúc. Verifier ở Đợt 3 dựa vào range này.
7. Viết bộ chuyển FactSet → định dạng gold, chạy bộ chấm trên tập dev.

**Xong khi:** mỗi mẫu có test; FactSet qua schema API-004; có số đo route/entity trên tập dev, so với `l3gen` 0.1; một route có body đi từ source tới khối OpenAPI hợp lệ; ít nhất một điểm gửi và một điểm nhận event được trích tự động.

### Đợt 2 — Cạnh dependency tĩnh, CMP-005 (2 ngày) — **đã code, đo trên dev**

1. Fact `reference` từ import và lời gọi đã nối được đích (`callgraph.py`; sửa chỗ bỏ lời gọi cấp module).
2. Gộp cạnh giữa hai component theo `(nguồn, đích, loại)`, giữ mọi fact (API-005 §4).

**Xong khi:** đo fact `reference` trên **15 case PyCG thuộc tập dev** (26 reference); 15 case held-out để dành cho Đợt 10. PyCG đo cạnh lời gọi hàm, không đo cạnh giữa component. Mẫu dưới ngưỡng 100 của OBS nên chỉ báo TP/FP/FN. Lời gọi chưa nối được đích không thành cạnh (AC-021-04).

### Đợt 3 — Kiểm bằng chứng đủ, CMP-007 (2 ngày) — **một phần** (`http-binding`, `config-binding` chưa có)

1. Rule `resolved-target`, `http-binding`, `config-binding`, `LABEL-DIRECT` theo API-007 §2.
2. CONTRACT-FIELD kiểm giá trị trong range hẹp của Đợt 1, không trong cả khối code.
3. Kiểm hash khi mở evidence (AC-023-03).

**Xong khi:** mỗi ca ở API-007 §4 có một test; cùng chữ đúng nhưng nằm sai vị trí thì bị loại.

### Đợt 4 — Bộ sinh tài liệu, CMP-008 (2–3 ngày) — **đã code** (không tách module)

1. Tách `render.py` thành các module: lập danh sách artifact, API, TBL, EVT, README, sơ đồ, kiểm, ghi file. Giữ hàm `render()` cũ để 27 test cũ vẫn chạy.
2. Lập danh sách mọi đường dẫn trước khi ghi; kiểm trùng tên không phân biệt hoa thường, tên dành riêng của Windows, độ dài.
3. Mỗi bộ sinh trả về bảng: fact/trường nào đã trình bày, bị bỏ vì lý do gì. Bước kiểm bản xuất so bảng này, không tìm chuỗi.
4. Escape riêng cho ô Markdown, code fence, HTML, nhãn Mermaid. Test các ký tự `|`, backtick, xuống dòng, ngoặc kép, Unicode, `<script>`.
5. Evidence ghi `path:dòng`, snapshot và ID. Chỉ tạo link khi có URL repo + commit; repo từ ZIP hoặc thư mục local thì không bịa link.
6. DDL PostgreSQL thêm `VARCHAR(n)`, `NUMERIC(p,s)`; test parse DDL bằng sqlglot.

**Xong khi:** cố ý sửa sai một cạnh, owner hoặc trường trong output thì bước kiểm báo lỗi; file ngoài danh sách và đường dẫn thoát vùng bị từ chối.

### Đợt 5 — SVG, ghi file an toàn, retry (3 ngày) — **đã code**

1. SVG theo quyết định ở mục 2. Node và cạnh lấy từ cùng model với Mermaid; nhãn được escape; không có script hay link ngoài.
2. Phân biệt lỗi làm hỏng cả bộ (input, parity, JSON) với lỗi của một artifact. Manifest ghi cả artifact `failed`.
3. Retry một artifact `failed`: kiểm input và version → kiểm hash các file ready → sinh lại vào thư mục tạm → thay file → thay manifest sau cùng (API-008 §7). Không gọi LLM, không đọc lại source.
4. Thử lỗi giả ở từng bước: trước khi thay file, sau khi thay file nhưng trước manifest, hết đĩa, không có quyền ghi.

**Xong khi:** có SVG thật, đúng tập node/cạnh; một artifact lỗi retry thành ready mà hash của `result.json` và các file ready khác không đổi; tiến trình dừng giữa chừng không để lại bộ output nửa vời.

### Đợt 6 — Cổng LLM, CMP-006 (3 ngày) — **đã code, chưa gọi provider thật**

1. Client tự viết cho Groq và Gemini. Groq gọi hai pha: đọc code bằng tool, rồi trả JSON theo schema.
2. Ledger request và token theo API-006: 40 request mỗi run, Gemini 2, giới hạn theo phút; giữ chỗ trước khi gửi.
3. Công cụ đọc code: 6 lần mỗi phạm vi, 60 dòng mỗi lần; hợp các đoạn đã gửi không được phủ cả file; che bí mật trước khi gửi.
4. Khóa nhập qua prompt không hiện chữ; provider giả cho test.

**Xong khi:** test biên 40/41, 2/3, 6/7 của NFR-AI-002 pass; khóa đánh dấu không xuất hiện trong output và log. Trước đợt này gửi một request thật để kiểm `gpt-oss-120b` dùng được tool.

### Đợt 7 — LLM trong CMP-005 và thí nghiệm D-03 (3–4 ngày) — **đã code; D-03 chờ người phụ trách chọn**

1. Tác vụ `label_components`, `propose_edges`, `group_flat` qua CMP-006; đề xuất sai thì loại (API-005 §5).
2. Khung thí nghiệm so ít nhất ba ứng viên: (A) theo thư mục; (B) nhiều tín hiệu từ code, tham khảo PKG/WCA/ACDC; (C) cách chia nhóm của pipeline v8. Dữ liệu có nhãn kiến trúc chỉ có ở **7 case dev**: 20 component, 28 membership, 13 cạnh. Held-out không có nhãn kiến trúc. Mẫu dưới ngưỡng OBS (membership 30, cạnh component 20), nên chỉ báo TP/FP/FN. Muốn có tỷ lệ thì phải gán thêm nhãn kiến trúc trong golden trước.
3. Người phụ trách chọn ứng viên, ghi `partition_version`, rồi thay `fixture-membership-v1`.

**Xong khi:** có báo cáo so sánh TP/FP/FN theo OBS-L3GEN-001, ghi rõ tập và cỡ mẫu; trần 50 node được giữ ở ứng viên được chọn.

### Đợt 8 — Tiếp nhận và kiểm kê, CMP-002/003 (2–3 ngày) — **ZIP đã code; GitHub có code, tắt mặc định, chờ Security review; nhiều unit bị chặn chờ review**

1. ZIP: kiểm từng entry trước khi giải; đường dẫn thoát vùng, link, tên trùng thì từ chối cả gói; đếm byte khi đọc; trần 100 MB nén / 500 MB giải nén / 50.000 file.
2. GitHub: kiểm URL; lấy default branch → commit SHA; tải zipball theo SHA; giới hạn 120 giây; không nhận credential.
3. Nhiều unit theo manifest (`discovery.py`). Unit không có FastAPI thì ghi mức hỗ trợ, **không bỏ qua im lặng**.

**Xong khi:** các ca ZIP độc hại trong threat model bị từ chối; repo private hoặc không tồn tại báo đúng lỗi; đạt AC-020-01…03.

### Đợt 9 — Điều phối và HTTP facade, CMP-001 (3 ngày) — **đã code** (trần 30 phút/2 GiB kiểm giữa các giai đoạn)

Vòng đời run theo API-001 §3–4; hàng đợi FIFO; mỗi run chỉ một thao tác ghi; hạn 24 giờ và dọn dữ liệu khi khởi động; HTTP facade theo OpenAPI của API-001 §6 (chỉ nghe loopback, kiểm `Host`/`Origin`). Không làm giao diện.

**Xong khi:** test gọi đủ các endpoint, response qua schema của API-001; retry trùng nhau chỉ chạy một lần.

### Đợt 10 — Tích hợp repo thật và đo (2–3 ngày) — **một phần; held-out `blocked`; UI web đã có code**

1. Chạy trên một repo thật đã pin commit. Ghi rõ LLM có chạy hay không.
2. Người review kiểm từng file API/TBL/EVT của mẫu chọn trước: owner, trường, range nguồn, notice, khối máy. Chọn mẫu trước khi chạy, không chọn sau khi thấy kết quả.
3. **Điều kiện trước:** gold đã được review (hiện 65/65 case là `candidate`, `human_review_complete: false`). Chưa review thì chỉ báo TP/FP/FN, không kết luận đạt hay không đạt ngưỡng.
4. Chạy tập dev rồi held-out một lần theo OBS-L3GEN-001; ghi độ đúng theo từng tập, tỷ lệ `false_exact`, thời gian chạy. Không đạt ngưỡng 80% thì ghi đúng số, không sửa gold. Membership và cạnh component không đo được trên held-out vì tập này không có nhãn kiến trúc.
5. Hướng dẫn chạy trên máy sạch; báo cáo ghi commit, lệnh, exit code, checksum artifact, trạng thái `passed`/`failed`/`not_run`/`blocked`.

**Xong khi:** người khác chạy lại được và ra cùng kết quả.

**Tổng ước lượng:** 27–33 ngày công, chưa gồm thời gian chờ quyết định D-03.

## 6. Thứ tự và phụ thuộc

```text
Đợt 0 → Đợt 1 → Đợt 2 → Đợt 3 ─┐
            └→ Đợt 4 → Đợt 5 ──┼→ Đợt 9 → Đợt 10
Đợt 6 → Đợt 7 (cần Đợt 2) ─────┘
Đợt 8 làm song song được
```

Nếu thời gian ngắn, bàn giao sớm một **lát cắt kỹ thuật** gồm: một route có body và một bảng trích từ source thật; SVG; manifest; retry. Phần event chưa xong thì ghi là chưa xong, không bỏ AC-027-03 khỏi cam kết cuối.

## 7. Ca test tối thiểu

| Nhóm | Ca bắt buộc |
|---|---|
| Input | Sai version/snapshot; ID trùng; tham chiếu treo; owner sai; thiếu trường bắt buộc (khác với `unknown`) |
| API | Alias import; router mount hai lần; prefix động; hai application cùng path; body ở nhiều status; thiếu auth |
| TBL | Hai engine; kiểu có tham số; FK không rõ bảng đích; khóa chính nhiều cột; tên có dấu nháy hoặc `\|` |
| EVT | Gửi/nhận trích từ source thật; cùng topic khác broker; chỉ thấy bên nhận; payload mâu thuẫn hoặc chưa biết |
| Bằng chứng | Chữ đúng nhưng sai vị trí; giá trị nằm trong comment; path/hash/range sai |
| Sơ đồ | 0, 1, 50, 51 node; cạnh đảo chiều nhưng cùng số lượng; tên trùng; Unicode; nhãn phá cú pháp |
| Ghi file | Tên dành riêng; đường dẫn thoát vùng; trùng tên; output hoặc thư mục tạm không thuộc run; không có quyền ghi |
| Retry | Dependency failed; thiếu version; file ready không bị sinh lại; hết hạn; dừng giữa chừng ở từng bước |
| LLM | JSON hỏng; ID lạ; timeout; hết quota; vượt trần 40/2/6; khóa lộ ra output |
| Tiếp nhận | ZIP có `..`, link, tên trùng, vượt trần; GitHub private, timeout, redirect |

Đáp án của test lấy từ contract và source, không lấy output hiện tại làm đáp án.

## 8. Điều kiện bàn giao

**Được gọi là xong khi:**

- API, TBL và EVT đều có ca chạy từ dữ kiện trích tự động.
- Khối máy hợp lệ và cùng nội dung với bảng; phần thiếu có lý do và có notice.
- Fact, owner, evidence, snapshot, phiên bản nhất quán; mọi artifact cùng tập node và cạnh.
- SVG vẽ thật; retry giữ nguyên input và các artifact ready.
- Có kết quả chạy trên repo thật và hướng dẫn chạy lại. Số đo độ đúng chỉ công bố khi đo theo OBS-L3GEN-001.

**Lỗi chặn bàn giao:**
- bịa body, status, auth hoặc DDL;
- nối event chỉ vì trùng tên topic;
- lấy chữ trong comment làm bằng chứng;
- mất contract mà không có notice;
- bước xuất đổi membership hoặc cạnh;
- ghi hoặc xóa ngoài vùng output;
- retry làm đổi fact;
- báo `passed` cho phần chưa chạy.

## 9. Rủi ro

| Rủi ro | Cách xử lý |
|---|---|
| Code `l3gen` 0.1 nằm ở nhánh khác, cấu trúc dữ liệu khác | Chuyển từng module kèm test cũ của nó; chưa qua test thì chưa dùng |
| Pipeline của Khiêm cũng trích dữ kiện, thành hai nguồn | Chốt quyết định ở mục 2 trước Đợt 1 |
| `gpt-oss-120b` trên Groq không dùng được tool như mong đợi | Thử một request thật trước Đợt 6 |
| D-03 chưa có quyết định | Mọi đợt trừ Đợt 7 không phụ thuộc; dùng membership fixture tới khi có quyết định |
| Độ đúng trên dev dưới 80% | Báo đúng số; tách lỗi theo nguồn bằng `summarize.py` của bộ chấm |
