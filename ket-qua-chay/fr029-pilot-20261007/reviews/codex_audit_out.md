**Chưa đủ căn cứ để nghiệm thu FR-029.** Có kết quả fixture và repo thật, nhưng còn lỗi bộ kiểm, rò bí mật, sai bộ chấm và thiếu phép đo bắt buộc. Các kết quả v8 cũng chưa chứng minh chất lượng code/prompt v12 hiện tại.

Tôi không sửa file, không gọi model hoặc chạy oracle. Đã đọc 14 `summary.json`, 104 `result.json`, chấm lại kết quả có gold, chạy 14 test không ghi file và kiểm 53 khối OpenAPI có sẵn. Những kiểm tra này đều qua. Toàn suite hiện có **230 test**, riêng `test_docagent.py` có **42 test**; tôi không chạy các test tạo thư mục tạm nên **không xác nhận lại 229/230**. Không có lỗi test do sandbox trong 14 test đã chạy; lỗi gateway đã biết không được tính vào phát hiện.

Để bảng không quá dài, các đường dẫn dưới đây dùng tiền tố:

- `C/` = [slice/l3slice](D:/VSF/l3-generator-l3/slice/l3slice).
- `T:n` = [slice/tests/test_docagent.py](D:/VSF/l3-generator-l3/slice/tests/test_docagent.py), dòng `n`.
- `M/` = [slice/tools](D:/VSF/l3-generator-l3/slice/tools).
- `P/` = [ket-qua-chay/fr029-pilot-20261007](D:/VSF/l3-generator-l3/ket-qua-chay/fr029-pilot-20261007).
- `B:n` = [docs/FR029-giai-thich-cho-mentor.md](D:/VSF/l3-generator-l3/docs/FR029-giai-thich-cho-mentor.md), dòng `n`.
- `K:n` = [docs/L3-ke-hoach-agent-sinh-tai-lieu.md](D:/VSF/l3-generator-l3/docs/L3-ke-hoach-agent-sinh-tai-lieu.md), dòng `n`.

**1. Bảng 8 AC**

Ngưỡng cần áp: P/R ≥80% **riêng từng loại, từng repo kín nhỏ/vừa**; bằng chứng hợp lệ cho kết luận công bố 100%; dữ kiện `exact` sai ≤5%; mẫu số 0 phải `not_evaluated`. Bốn repo nghiệm thu là tdd-docker, AgentGPT, igorbenav và KIBO — không phải bốn repo của phép đo golden hiện tại. Căn cứ: [NFR-ACC-002:28](D:/VSF/l3-generator-l3/.aide/requirements/nfr/NFR-L3GEN-ACC-002.md:28), [NFR-ACC-002:48](D:/VSF/l3-generator-l3/.aide/requirements/nfr/NFR-L3GEN-ACC-002.md:48), [OBS-001:43](D:/VSF/l3-generator-l3/.aide/observability/OBS-L3GEN-001.md:43), [OBS-001:56](D:/VSF/l3-generator-l3/.aide/observability/OBS-L3GEN-001.md:56).

| AC | Cài đặt | Test có liên quan | Số đo thật và dữ liệu | Kết luận |
|---|---|---|---|---|
| **029-01** | `C/docfacts.py:222–347,824–851`; `C/docpipeline.py:126–143`; `C/render.py:362–511` | `test_first_case` (`T:218`), `test_literal_at_call_site_with_registration_in_helper` (`T:545`), `test_attached_version_replaces_unattached_one` (`T:530`) | `P/luna5/`: scorer báo route **93/0/0**, nhưng tính cả 3 route path unknown. `P/golden-luna2/summary.json`: **40/2/0**, P=95,24%, R=100%. Hai `golden4-*/summary.json`: teamhide **5/0/0**, full-stack **23/0/0**, igorbenav **30/0/4**, FBA **1/0/138**. | **ĐẠT MỘT PHẦN** — có route đúng trên fixture/repo thật, nhưng bộ kiểm nhận prefix đảo/sai và chưa kiểm ownership với component thật; ngưỡng nghiệm thu chưa được đo đủ. |
| **029-02** | `C/docfacts.py:184–217,349–474,756–955`; `C/render.py:138–200,271–359,400–476` | `test_first_case`, `test_embedded_and_form_bodies_render_inline` (`T:618`), `test_non_model_response_type_is_documented` (`T:566`), `test_08_status_cannot_borrow_another_decorator` (`T:312`) | `P/luna5/`: **24 model TP**, 0 FP/FN và 0 lỗi thuộc tính **được scorer chấm**. Repo thật: chấm lại tên model cho teamhide **5/5**, full-stack **19/23**, igorbenav **6/30**, FBA **0/1**; xem các `golden4-*/…/result.json` và `summary.json`. | **ĐẠT MỘT PHẦN** — fixture chưa đo hết thuộc tính; repo thật chưa có P/R model độc lập, igorbenav sai/unknown tên model ở 24/30 route khớp. |
| **029-03** | `C/docfacts.py:31–45,716–728,824–955`; `C/render.py:78–90,305–321,383–398` | `test_01_unknown_values_do_not_crash` (`T:284`), `test_19_nested_unknown_makes_the_model_partial` (`T:363`), `test_unknown_required_of_inline_body_is_kept` (`T:409`) | `P/luna5/prefix_chain-r1/result.json` có path unknown; `http_calls-r1/result.json` có method/đích unknown. **Không có phép đo tỷ lệ `exact` sai** trong `M/fr029_score.py:129–164`. | **ĐẠT MỘT PHẦN** — có nhãn nhưng mất lý do unknown của required body không inline, nhãn suy luận chủ yếu ở mức fact và chưa đo ngưỡng `exact` sai ≤5%. |
| **029-04** | `C/docpipeline.py:29–85,145–147` | `test_architecture_parity` (`T:254`), `test_13_archdia_without_snapshot_is_not_evaluated` (`T:343`) | **104/104** `P/*/*/result.json` có `architecture_parity.status=not_evaluated`; không có input FR-028 thật trong các phép chạy này. | **CHƯA ĐÁNH GIÁ** — mới có test fixture, đồng thời kiểm version/ID và tính duy nhất component còn thiếu. |
| **029-05** | `C/source_tools.py:31–52,109–113`; `C/docfacts.py:579–658` | `test_scope_follows_fr028` (`T:116`), `test_scope_virtualenv_marker_and_src_layout` (`T:370`), `test_15_suspect_lines_must_be_accounted_for` (`T:348`) | `P/luna5/exclusions-r1..r3/`: mỗi lần scorer ghi **1 route**, **3 limitation**, 0 FP/FN. Chưa có gold phạm vi tương đương trên repo thật. | **ĐẠT MỘT PHẦN** — fixture đã kiểm, nhưng `dismissed` có thể xóa nghĩa vụ ghi limitation; phạm vi bỏ nhầm import tương đối và `venv/`. |
| **029-06** | `C/docpipeline.py:196–297` | `test_first_case`, `test_architecture_parity`, `test_dismissals_are_kept_in_result` (`T:452`) | README có các mục tại `P/luna5/*/README.md` và `P/golden4-*/*/README.md`; tất cả thiếu sơ đồ được cấp. README teamhide dòng 23 còn manifest “vai trò unknown”, nhiều file rỗng không có dòng evidence. | **ĐẠT MỘT PHẦN** — có bố cục/mục lục nhưng chưa có sơ đồ cùng snapshot và chưa bảo đảm nội dung cấu trúc hợp lệ. |
| **029-07** | `C/docfacts.py:537–576,647–656,802–820`; `C/docpipeline.py:245–269` | `test_service_needs_a_call_path` (`T:179`), `test_role_needs_its_signal` (`T:184`), `test_10_role_order_and_khac` (`T:327`) | `P/luna5/file_roles-r1..r3/`: **30/0/0**, không lỗi ở 10 file gold ×3. Repo thật chưa có gold vai trò; teamhide công bố **29 fact vai trò không evidence**, full-stack **4**, igorbenav **1**, trong các `result.json`. | **CHƯA ĐẠT** — đầu ra thật đã vi phạm yêu cầu evidence; bộ kiểm còn nhận Hạ tầng không có dấu hiệu và Service không có cạnh gọi được chứng minh. |
| **029-08** | `C/docfacts.py:478–535,785–801`; `C/docpipeline.py:271–285` | `test_http_keywords` (`T:396`), `test_09_url_must_be_the_url_argument` (`T:317`), `test_raw_secret_is_refused_as_target` (`T:402`) | `P/luna5/http_calls-r1..r3/`: **33/0/0** call site; scorer tính đúng cả method/đích unknown. Golden thật: ba repo có gold HTTP rỗng; FBA **0 TP/0 FP/3 FN**, R=0%, P chưa đánh giá. | **ĐẠT MỘT PHẦN** — fixture có kết quả nhưng bộ kiểm nhận DB.get/URL sai, từ chối HTTP hợp lệ import xuyên file; chưa đạt phép đo HTTP trên repo thật có mẫu. |

Không thể lấy “5/5 route” hoặc “23/23 route” làm kết luận toàn bộ AC-01/02: harness tự tạo **một component “Toàn bộ”**, không nhận membership kiến trúc thật (`M/fr029_golden4.py:111–114`).

**2. Kiểm báo cáo**

Các số đếm sau tái lập được từ kết quả lưu:

| Tập | Kết quả đếm lại | Chi phí ghi trong summary |
|---|---|---:|
| `P/luna1/` | 2 completed, 4 lỗi `IncompleteRead` | 0,0053 USD; không có chi phí của 4 ca lỗi |
| `P/luna2/` | Route 31/7/0; 3 lỗi thuộc tính | 0,0185 |
| `P/luna3/` | 18 completed; **2 lỗi thuộc tính target HTTP** trong một lần | 0,0474 |
| `P/luna4/` | 6 completed; **2 lỗi thuộc tính target HTTP** | 0,0158 |
| `P/luna5/` | 18 completed; scorer báo 0 lỗi | 0,0568 |
| `P/golden-luna/` | 39/3/1 | 0,0699 |
| `P/golden-luna2/` | 40/2/0 | 0,0736 |
| `P/golden4-chinh/` | full-stack 23/0/0; igorbenav 30/0/4 | 0,5137 |
| `P/golden4-do/` | teamhide 5/0/0; FBA 1/0/138 | 0,8168 |

Tổng các khoản **được ghi** là **1,6178 USD**. Những sai lệch và khẳng định vượt căn cứ:

| Câu/vị trí trong báo cáo | Phán định | Số đúng hoặc giới hạn phải ghi |
|---|---|---|
| **“Đúng trên repo nhỏ và vừa”**, `B:10–18` | **THỔI PHỒNG** | Đây chủ yếu là phép đo route. Igorbenav chỉ khớp tên request/response ở **6/30 route**, không phải đã đúng tài liệu trên repo vừa. `P/golden4-chinh/summary.json`. |
| **“Đúng 100%…18/18”**, `B:14`; “mọi mục”, `B:341` | **THỔI PHỒNG nếu hiểu là đủ yêu cầu** | Chỉ đúng theo trường mà scorer hiện chấm. Scorer không chấm handler, dependency/auth, nullable tham số, nhãn route/model, evidence và AC04/06; còn nhận unknown là đúng. `M/fr029_score.py:68–97,129–158`. |
| **“luna3…mọi mục đúng”**, `B:339`; **“luna4…đúng mọi mục”**, `B:340` | **SAI** | Mỗi tập có **2 lỗi target HTTP**. Câu ghi chú `settings.X` không biến các lỗi đã đo thành 0. Căn cứ: `P/luna3/http_calls-r2.score.json`, `P/luna4/http_calls-r1.score.json`. |
| **“golden-luna prompt v6”**, `B:349` | **SAI** | Cả 19 `P/golden-luna/*/result.json` ghi **`fr029-agent-prompt-v5`**. |
| **“unknown không bao giờ được tính là đúng”**, `B:296` | **SAI** | `prefix_chain` có path `None` được TP; HTTP có method unknown và hai target unknown vẫn được tính thuộc tính đúng. `M/fr029_score.py:69,85–87,107,119–120,142–153`; `P/luna5/prefix_chain-r1/result.json`, `http_calls-r1/result.json`. |
| **Route match theo method/path/handler**, `B:291` | **SAI với scorer fixture** | `fr029_score.py` match **method/path/file:dòng decorator**, không dùng handler. Golden scorers mới dùng handler. `M/fr029_score.py:69,107`; `M/fr029_golden4.py:57,66`. |
| **“URL là đối số URL của lời gọi”**, `B:215` | **SAI** | Bộ kiểm có thể lấy literal trong `headers` khi URL là biến; ca tái hiện F05 bên dưới. `C/docfacts.py:522–534`. |
| **“Receiver…là FastAPI/APIRouter”**, `B:213` | **THỔI PHỒNG** | Chỉ kiểm một số phép gán cùng file; receiver import từ file khác, shadowing và quan hệ app/router không được chứng minh. `C/docfacts.py:337–343`. |
| **“Vai trò có dấu hiệu…thứ tự vai trò”**, `B:217–218` | **THỔI PHỒNG** | Hạ tầng/Truy cập dữ liệu chỉ bị chặn nếu dẫn import; thứ tự cưỡng chế chỉ có ba vai trò đầu, và `not_signal` bất kỳ có thể bỏ chặn. `C/docfacts.py:47–56,550–561`. |
| **“Giá trị nào dùng quy tắc…mang nhãn inferred”**, `B:227` | **THIẾU CHÍNH XÁC** | Rule phần lớn gom vào nhãn **toàn fact**, không gắn rõ từng trường; required body unknown còn mất lý do. `C/docfacts.py:765–780,870–878,892–911`. |
| **“check_doc…so với fact; lệch…không xuất”**, `B:246` | **THỔI PHỒNG** | Chỉ kiểm một tập con. Đổi nullable/required path hoặc nhiều trường bảng/model vẫn có thể qua; không chạy validator OpenAPI trong pipeline. `C/render.py:795–803,820–870`. |
| **Bảng model igorbenav và FBA để “—”**, `B:363–364` | **THIẾU SỐ ĐÃ CÓ** | Summary đã ghi **igorbenav 6/30**, **FBA 0/1** tên model đúng trên route khớp; nên công bố thay vì để trống. |
| **HTTP gold “nằm ở repo chạy hỏng, nên chưa kiểm”**, `B:286` | **SAI** | FBA là **partial**, vẫn có output và scorer đã tính **0/0/3**. Có thể nói chưa có ca thành công đủ độ phủ; không thể nói chưa chấm. `P/golden4-do/summary.json`. |
| **“2 repo lớn”**, `B:20,450` | **SAI theo phân cỡ yêu cầu** | Igorbenav là **vừa**; FBA là **lớn**. OBS-001:28–41. |
| **Groq “cả 6…sau 1 lượt”**, `B:320` | **SAI** | `P/base3/summary.json`: **3 ca 0 lượt, 3 ca 1 lượt**, đều dừng bởi 429. |
| **“nguyên nhân đã rõ”**, `B:19,379–381` | **THỔI PHỒNG mức chắc chắn** | FBA đúng là 175 lượt, 22.008.461 token input, 142 vai trò và 1 route; nhưng chưa có đo đối chứng chứng minh thứ tự nộp vai trò là nguyên nhân quyết định. Coverage thực tế: **143 processed, 66 empty, 3 partial, 84 unread**. `P/golden4-do/fastapi_best_architecture/result.json`. |
| **“đã tiêu 1,62/2 USD”**, `B:450`, HANDOFF:14 | **THIẾU CĂN CỨ cho tiền thực trả** | **1,6178 USD là tổng ước tính được lưu**; ca ném exception không ghi khoản đã tiêu, request lỗi/mất response không có usage để hạch toán. `M/fr029_pilot.py:35–48,57`; `C/docagent.py:331–335`. |
| **“230 test…229 qua”**, `B:419` | **CHƯA XÁC MINH số pass** | Đếm được 230 test, nhưng không có đường dẫn log thực chạy kèm báo cáo. Trong kiểm toán này chỉ chạy lại 14 test chỉ đọc. `T:90–109` cho thấy nhiều test còn lại cần ghi file. |
| Các tỷ lệ **3/3, 2/3**, số lỗi review, tác giả tìm lỗi, `B:269,304–310,392–413` | **THIẾU HỒ SƠ KIỂM TOÁN** | Không tìm thấy bài chấm đầu vào hoặc JSON hợp nhất trong cây kết quả được dẫn. `M/fr029_grade_merge.py` chỉ là công cụ, không chứng minh review đã diễn ra hoặc số đồng thuận đúng. |
| **“store:false nên OpenAI không lưu hội thoại”**, `B:166` | **VƯỢT CĂN CỨ CODE** | Code chứng minh có gửi `store:false`; riêng cờ này không chứng minh toàn bộ chính sách lưu giữ phía nhà cung cấp. `C/docagent.py:308–309`. |

Hai điểm báo cáo ghi đúng nhưng cần giữ giới hạn:

- Approval bốn đáp án tồn tại tại `D:/VSF/l3-generator-golden-v2/.aide/evidence/approvals/APPROVAL-golden-v1-2026-10-04.yaml`; **approval đó không thay bộ nghiệm thu OBS-001**.
- Chấm lại teamhide bằng scorer hiện tại được **5/5 tên model**, xác nhận lỗi 4/5 trong summary cũ là lỗi scorer; full-stack vẫn **19/23**. Căn cứ: `M/fr029_golden4.py:60–75` và hai `result.json` tương ứng.

**3. Lỗi còn lại trong code**

Các ca sau được tái hiện trong bộ nhớ hoặc xác nhận trực tiếp trên artifact có sẵn. Không ca nào cần sửa source.

| Mã/mức | Vị trí | Input tái hiện và hậu quả |
|---|---|---|
| **F01 — Cao: lọt bí mật qua reader** | `C/common.py:13`; `C/source_tools.py:24–27,55–76` | Source `password: str = "audit_dummy_secret"`: `SourceTools.read_file()` trả nguyên giá trị. Regex không xử lý annotation giữa tên và `=`; kiểu khai báo này thường gặp ở Settings. |
| **F02 — Cao: bí mật bị từ chối vẫn được publish** | `C/docfacts.py:173–177,504–505`; `C/docpipeline.py:163` | Nộp HTTP target `https://alice:audit_dummy_secret@example.com`: claim bị từ chối, nhưng **toàn item nguyên văn** được giữ trong `rejected_claims` rồi ghi vào `result.json`. |
| **F03 — Cao: nhận prefix sai và không thay bản sai khi sửa** | `C/docfacts.py:246–280,311–319,839–841` | Lấy `CREATE` tại `T:46`, đảo hai phần đầu của `CHAIN`: bộ kiểm nhận và xuất **`/v1/api/items/`**. Nộp lại bản đúng giữ **cả hai route**, vì key chứa chuỗi prefix. Đặt prefix `/api` thành `""` cũng được nhận do điều kiện `value and …`. |
| **F04 — Cao: OpenAPI sai vẫn qua kiểm cuối** | `C/docfacts.py:349–373`; `C/render.py:181–200,795–803,820–870` | Lấy `READ` tại `T:56`, đổi `item_id.required=False`: claim được nhận, `check_doc()` trả `None`, nhưng OpenAPI validator báo **`True was expected`**. Pipeline không có bước validator để chặn artifact này. |
| **F05 — Cao: HTTP giả và URL sai được gắn exact** | `C/docfacts.py:485–488,522–534` | `import httpx; db.get("https://fake.example")` được nhận là HTTP. Với `httpx.get(runtime_url, headers=dict(Referer="https://wrong.example"))`, khai target `https://wrong.example` cũng được nhận. Kiểm import/literal không xác minh receiver và vị trí đối số. |
| **F06 — Vừa: từ chối HTTP hợp lệ** | `C/docfacts.py:485–490`; `C/docfacts.py:624–630` | `clients.py` tạo `httpx.Client`; `m.py` chỉ `from clients import client; client.get("https://real.example")`: bị từ chối vì `m.py` không import httpx. Dạng `from requests import get; get(url)` cũng không có `.get(` để vượt kiểm. Phạm vi A08 yêu cầu theo alias/client xuyên file (`K:235–239`). |
| **F07 — Cao: evidence không liên quan vẫn chứng nhận claim** | `C/docfacts.py:305–306,550–576,650–656` | Đổi auth của `CREATE` thành `{"value":"NO AUTH REQUIRED","at":"app/schemas.py:5"}`: được nhận dù đó là dòng schema. File chỉ có `x = 1`, nộp vai trò Hạ tầng tại dòng 1 cũng được nhận. Service chỉ kiểm file đầu/cuối, chưa kiểm các cạnh gọi. |
| **F08 — Cao: bỏ limitation bằng lời bác không kiểm chứng** | `C/docfacts.py:593–618`; `T:348–355` | Với fixture e2e, bỏ limitation `app/main.py:13`, thay bằng dismissed có lý do “not a registration”: **11 item accepted, `open_problems=[]`**, dù source thật có `add_api_route`. AC05 có thể mất limitation mà agent vẫn finish. |
| **F09 — Vừa: mất unknown và lý do** | `C/docfacts.py:893–898`; `C/render.py:289–292,445–451` | `CREATE.request_body.required={"unknown":"AUDIT_REASON_REQUIRED"}`: sau `build_facts`, required thành `None`; chuỗi lý do biến mất khỏi route. Đây là body model không inline; test inline hiện tại không bắt ca này. |
| **F10 — Cao: sai phạm vi dẫn đến thiếu route nhưng độ phủ vẫn đủ** | `C/source_tools.py:46–51`; `C/snapshot.py:19,55–62` | `app/scripts/tool.py` có `from ..models import Item`: bị loại dù import code repo. `venv/tool.py` có import app cũng bị snapshot loại vô điều kiện trước khi reader xét; phần sau là lỗi cũ nhưng luồng mới vẫn chịu tác động. |
| **F11 — Cao: component ID trùng làm sai ownership/artifact** | `C/docpipeline.py:37–49,119–143`; `C/render.py:50–61` | Đổi bốn component của `fr029_e2e.membership.json` thành cùng `id="same"`: input được nhận; đầu ra chỉ còn **một đường dẫn API dưới KHAC**, README tạo bốn liên kết cùng file cho bốn owner khác nhau. |
| **F12 — Vừa: parity bỏ qua version/ID; diagram không ràng snapshot** | `C/docpipeline.py:53–85,101–102,240–244` | Archdia cùng file/route nhưng `schema="INVALID-V999"`, đổi toàn bộ ID/tên component vẫn trả **passed** nếu tự nhất quán nội bộ. Diagram là text bất kỳ, không kiểm snapshot hoặc component trước khi nhúng. Trái yêu cầu kiểm ID/version của `K:196–199,216–217`. |
| **F13 — Cao: công bố exact không evidence trên dữ liệu thật** | `C/docfacts.py:545,804–817`; `C/docpipeline.py:29–49`; `M/fr029_golden4.py:113–114` | Harness gom file rỗng/manifest vào normal; validator không báo upstream sai. Kết quả thật: **29/96 fact teamhide**, **4/60 full-stack**, **1/149 igorbenav** không có evidence; các fact này là vai trò được xuất. Ví dụ `P/golden4-do/teamhide-fastapi-boilerplate/README.md:25`. |
| **F14 — Vừa: JSON tool hợp lệ nhưng sai kiểu làm crash** | `C/docfacts.py:247,579–583`; `C/docagent.py:523–524` | `submit_findings({"limitations":[{"kind":[]}]})` gây **`TypeError: unhashable type: 'list'`**; `path_parts[].kind=[]` tương tự. Không chuyển thành lỗi field/partial để giữ kết quả đã biết. |
| **F15 — Cao: scorer làm số đo đẹp hơn thực tế** | `M/fr029_score.py:68–97,101–130,140–153` | Path unknown khớp `None` vẫn TP; unknown HTTP khớp unknown gold vẫn “correct”. Đổi **mọi handler** của `params_models-r1/result.json` thành tên bịa và mọi nullable tham số thành true: scorer vẫn **11 TP, 0 FP/FN, 0 lỗi thuộc tính**. Auth/dependency/nhãn/evidence cũng không được chấm. |
| **F16 — Vừa: bỏ mất FN của ca chạy lỗi** | `M/fr029_golden_routes.py:79–94` | Một case có 5 route gold ném exception trước khi có bundle: row chỉ ghi failed/error; tổng FN lấy `r.get("fn",[])` nên ca đó đóng góp **0 FN**. Nếu báo P/R tổng thì thất bại không nằm trong mẫu số. |
| **F17 — Vừa: “đồng thuận” có thể ghép hai lỗi khác nhau** | `M/fr029_grade_merge.py:25–27,41–46` | Reviewer A báo sai `required`, B báo sai `nullable`, cùng fixture/kind/evidence line: được gộp thành **ĐỒNG THUẬN 2/2**, dù hai người không xác nhận cùng lỗi. `field`, `doc_value`, `correct_value` không tham gia key. |
| **F18 — Vừa: retry Responses nhân đôi tool output** | `C/docagent.py:302–319,485–499` | Sau một lượt thành công, `_post()` ném `ProviderError("HTTP 500",True)` rồi thành công khi retry: cùng `function_call_output/call_id` xuất hiện **hai lần** trong request retry, do `self.items` đã bị sửa nhưng `self.sent` chưa tăng. |
| **F19 — Vừa: trần tiền không bảo đảm khi thiếu usage/price** | `C/docagent.py:199,331–335,474–475`; `M/fr029_pilot.py:120–121` | Đặt `max_cost_usd` nhưng không truyền giá, hoặc provider trả usage rỗng: `cost_usd` vẫn 0, giới hạn USD không dừng vòng. `result.json` cũng không lưu cached token/giá/chi phí để đối chiếu lại (`C/docpipeline.py:155–159`). |
| **F20 — Vừa: kiểm output không rỗng quá muộn** | `C/docpipeline.py:95–112`; `C/render.py:1177–1180`; `C/__main__.py:155–179` | Chạy `document` với output là thư mục `docs` đã có nội dung: agent vẫn được gọi, đến publish mới từ chối. Tái hiện với scripted provider đã có **4 lượt gọi** trước điểm publish; provider thật có thể tốn tiền rồi không giữ được artifact. |

Ngoài ra, công cụ chọn mẫu chỉ lấy từ **facts đã xuất**, nên không thể tự phát hiện route/HTTP bị bỏ sót hoàn toàn; đó là giới hạn phép đo recall, không phải nguồn gold độc lập (`M/fr029_sample.py:25–29,37–38`).

**4. Đối chiếu kế hoạch**

“XONG” dưới đây phải thỏa điều kiện kết thúc trong kế hoạch, không chỉ có hàm hoặc test.

| Mục | Trạng thái | Phần còn thiếu/căn cứ |
|---|---|---|
| **N1** | **MỘT PHẦN** | Chưa có giao diện upstream kiểm version/ID duy nhất và diagram cùng snapshot; thiếu nhãn theo field, missing/null/unknown còn mất nghĩa. FR029 vẫn để mapping triển khai/test trống tại dòng 181–183; `K:108–115`; F09/F11/F12. |
| **N2** | **MỘT PHẦN** | Reader/ledger có, nhưng phạm vi import tương đối/venv sai; annotation bí mật lọt; receipt lưu path/range, chưa đủ hợp đồng request/hash/processed như kế hoạch. `K:118–125`; `C/source_tools.py:138–159`; F01/F10. |
| **N3** | **MỘT PHẦN** | Có vòng agent/fake provider/ngân sách; còn retry nhân đôi, chi phí thiếu usage, tool sai kiểu gây crash. `K:128–135`; F14/F18/F19. |
| **N4** | **MỘT PHẦN** | Có gold/oracle/scorer nhưng chưa kiểm chuỗi prefix, evidence liên quan, conflict; scorer thiếu thuộc tính và KPI evidence/exact. `K:138–146`; F03/F07/F15. Oracle subprocess không tự chặn mạng (`M/fr029_oracle.py:21–31`). |
| **A01** | **MỘT PHẦN** | Có kết quả route nhưng chuỗi prefix sai vẫn qua, sửa route giữ bản sai, membership thật chưa kiểm. `K:151–159`; F03/F11. |
| **A02** | **MỘT PHẦN** | Chưa chứng minh toàn bộ kiểu/required/nullable/auth; repo thật còn sai model, OpenAPI invalid có thể xuất. `K:163–178`; F04/F07/F15. |
| **A03** | **MỘT PHẦN** | Unknown body mất lý do; inferred chưa gắn từng field; chưa đo exact sai. `K:182–188`; F09 và `C/docfacts.py:716–728`. |
| **A04** | **MỘT PHẦN** | Có adapter/test fixture; **nghiệm thu AC chưa đánh giá**, chưa input thật, version/ID chưa chặt. `K:192–200`; 104 result parity not_evaluated; F12. |
| **A05** | **MỘT PHẦN** | Fixture exclusions có kết quả, nhưng dismissal bỏ được registration thật và phạm vi còn sai. `K:203–208`; F08/F10. |
| **A06** | **MỘT PHẦN** | README có mục; thiếu sơ đồ thật/cùng snapshot, còn vai trò thiếu/evidence rỗng, ownership hỏng nếu ID trùng. `K:212–218`; F11–F13. |
| **A07** | **MỘT PHẦN** | Có 10 file gold, chưa kiểm đủ thứ tự/dấu hiệu/cạnh Service; chưa từ chối upstream xếp file rỗng sai. `K:222–229`; F07/F13. |
| **A08** | **MỘT PHẦN** | Có 11 call site fixture; chưa xử lý đúng cross-file/direct import, lọt DB.get và URL không phải đối số. `K:233–240`; F05/F06. |
| **V1** | **MỘT PHẦN** | Chưa đủ bốn repo kín nhỏ/vừa; chưa P/R model/HTTP riêng, evidence 100%, exact sai ≤5%; chưa chứng minh sàn **61/0/0** trên cùng tập; ba lần chỉ có fixture. `K:246–256`; OBS-001:43–66. |
| **V2** | **MỘT PHẦN** | CLI có nhưng không nối Responses/giá/trần USD như harness; chưa retry bộ FR029; output check muộn; chưa có kết quả đủ 8 AC tách riêng. `C/__main__.py:131–179`; `K:259–266`; `B:452`. |

Không mục nào đủ căn cứ để đánh **XONG** theo tiêu chí kết thúc tại `K:338–341`. Điều này không phủ nhận các phần đã cài đặt; nó phản ánh phần điều kiện bắt buộc còn thiếu.

**5. Kết luận**

**Chưa đủ và chưa đúng với toàn bộ yêu cầu.** Ba nhóm chặn chính là: đầu ra có thể chứa bí mật hoặc claim sai đã qua kiểm; phép đo hiện tại bỏ qua lỗi quan trọng và tính unknown là đúng; chưa có tích hợp FR-028 và bộ nghiệm thu theo OBS. Các bước ưu tiên:

1. **Chặn rò bí mật** ở reader và mọi nhánh xuất, kể cả rejected/error/reason — F01–F02.
2. **Sửa bộ chấm trước khi công bố lại tỷ lệ**: unknown, handler, nullable, auth/dependency, evidence, exact, ca lỗi và đồng thuận — F15–F17.
3. **Sửa kiểm claim và OpenAPI**: chuỗi prefix, thay thế/conflict, HTTP receiver/URL, vai trò/auth, dismissal, unknown — F03–F09.
4. **Sửa phạm vi và hợp đồng upstream**: import tương đối/venv, ID duy nhất, file rỗng, version/snapshot diagram — F10–F13.
5. **Hoàn thiện vận hành**: JSON lỗi không crash, retry Responses, kiểm output trước gọi model, hạch toán tiền và retry artifact — F14/F18–F20, V2.
6. **Khóa cấu hình rồi đo lại bản hiện tại**, với gold độc lập và đủ bốn repo kín nhỏ/vừa; báo P/R từng loại, evidence 100%, exact sai ≤5%, cùng AC04/06 trên artifact thật — NFR-ACC-002:28–58; OBS-001:43–76.
7. **Sửa báo cáo/HANDOFF theo số đã kiểm**, công bố cả 6/30 model igorbenav, 0/3 HTTP FBA, các lỗi scorer và đường dẫn log/review — bảng kiểm báo cáo ở trên.