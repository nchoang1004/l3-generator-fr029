# Kế hoạch triển khai FR-029 bằng agent đọc source

Ngày cập nhật: 07/10/2026. **Phạm vi đã được người dùng xác định: FR-L3GEN-029, đủ 8 AC.** Đây là kế hoạch triển khai sau nghiên cứu repo; chưa triển khai code, chưa chạy test sản phẩm hoặc model trong phiên này.

Bản này thay các bản kế hoạch trong cùng file đã hiểu nhầm sang toàn bộ L3, 10 mục phát hiện hoặc 8 nhóm FR cũ. Không còn câu hỏi về phân công 8/10. Các mã N1–N4, A01–A08, V1–V2 chỉ là mã công việc cục bộ, không phải ID Task chính thức.

**Nguồn và ranh giới**

- Nguồn chức năng: [FR-029 revision 3](../.aide/requirements/fr/FR-L3GEN-029.md), gồm 8 AC và các bảng mô tả đi kèm.
- Nguồn chất lượng: [NFR-ACC-002](../.aide/requirements/nfr/NFR-L3GEN-ACC-002.md), [OBS-001](../.aide/observability/OBS-L3GEN-001.md); an toàn/vận hành theo NFR liên quan.
- Agent đọc source, lần theo file và xác định dữ kiện API, model, vai trò file, HTTP. Không lấy facts từ AST extractor cũ làm đầu vào phân tích.
- Code cung cấp nội dung, quản lý snapshot/độ phủ/ngân sách, kiểm dữ liệu và bằng chứng, render đầu ra. Kiểm schema hoặc quote không thay phép đo hiểu đúng ngữ nghĩa.
- **Không tạo/chia/gộp/đặt tên component. Không dựng Mermaid, SVG hoặc sơ đồ kiến trúc.**
- Nhận component, file thành viên và dữ liệu kiến trúc từ phần FR-028. AC-04 là đối chiếu dữ liệu; AC-06 dùng sơ đồ đã được cung cấp. Thiếu đầu vào này phải ghi rõ phần chưa kiểm/thiếu, không tự tạo thay.
- Không triển khai FR-030 TBL/DDL, FR-031 EVT, web hay tiếp nhận GitHub/ZIP trong kế hoạch này. Có thể cần đọc code bảng/config/task để hiểu API hoặc vai trò file; việc đó không mở rộng đầu ra.
- Theo yêu cầu nghiên cứu mới, đã mở rộng từ GitDiagram sang OpenDeepWiki, CodeWiki, RepoAgent và mẫu pnp. [Bản nghiên cứu](L3-nghien-cuu-repo-sinh-tai-lieu.md) ghi commit, phần mã đã kiểm, điểm học và giới hạn. Không áp cơ chế lấy mẫu file để tuyên bố đã đọc đủ source.
- Hướng agent đọc toàn bộ source là yêu cầu trực tiếp của người dùng. N1 ghi rõ chỗ cần đồng bộ tài liệu cũ: NFR-AI hiện áp FR-028; NFR-SEC áp FR-029 nhưng dẫn lại giới hạn gửi source của NFR-AI. Không coi cấu hình model/ngân sách của FR-028 là mặc nhiên đã chốt cho vòng agent FR-029. Chưa sửa spec trong phiên lập kế hoạch.

**Đầu ra cần bàn giao**

| Đầu ra | Nội dung |
|---|---|
| `tech-specs/<CMP-slug>/api/API-<SYS>-<CMP>-v1.md` | Frontmatter; endpoint; request/response model; truy vết; khối OpenAPI 3.1 |
| `README.md` | Mục lục; sơ đồ nhận từ bên ngoài; cấu trúc component; HTTP ra ngoài; contract chưa gán; giới hạn |
| `result.json` | Snapshot/version; dữ kiện; component được cung cấp; evidence; unknown/inferred; độ phủ và kết quả đối chiếu |
| Báo cáo kiểm | Đủ 8 AC; test thực chạy; độ đúng theo gold; phần chưa chạy hoặc thiếu đầu vào tích hợp |

Chủ sở hữu API theo file khai báo route. Model được dùng qua nhiều component vẫn phải có mô tả đầy đủ. Component bị cắt khỏi hình sơ đồ vẫn có tài liệu nếu sở hữu API.

**Hiện trạng code cần tính đến**

| File | Cách xử lý dự kiến |
|---|---|
| `slice/l3slice/__init__.py` | Luồng hiện tại gọi extract/model/annotate. Thêm luồng FR-029 bằng agent, không dùng các bước đó để tạo dữ kiện hoặc component |
| `snapshot.py`, `common.py` | Tận dụng snapshot/hash/che bí mật sau khi kiểm phạm vi và bảo toàn tọa độ dòng |
| `gateway.py` | Giao thức cũ chưa phải vòng đọc source mới; làm adapter phù hợp, có fake transport để kiểm offline |
| `verify.py` | Tái sử dụng helper kiểm evidence phù hợp; tách kiểm contract khỏi kiểm/chỉnh graph |
| `render.py` | Tái sử dụng writer API/README và publish; tách phụ thuộc dựng graph, không tạo verdict giả để qua bộ kiểm cũ |
| `slice/tests/test_fr029.py` | Có hồi quy T1–T5 của đợt trước; giữ và bổ sung test cho pipeline agent. Số test pass cũ không là kết quả mới |
| `slice/evaluation_l3/` | Tận dụng kiểm artifact độc lập; thêm phép chấm dữ kiện agent với gold source, không chỉ so output với input renderer |

Tên module mới dưới đây là dự kiến. Chỉ tách khi ranh giới dữ liệu cần thiết, không chia một module cho mỗi task.

## Thiết kế đề xuất từ nghiên cứu

Luồng mới: **snapshot + membership có sẵn → agent đọc và ghi dữ kiện → kiểm bằng chứng → đối chiếu kiến trúc → đóng băng dữ liệu → sinh API/README/result → chấm nghiệm thu**. Không cần thêm dịch vụ wiki, vector database hoặc thuật toán clustering để làm 8 AC này.

**Cách đọc đủ mà không nhét cả repository vào một request**

1. Code lập danh mục đầy đủ của snapshot trong phạm vi công bố. Chia file lớn thành các phần có tọa độ; không chọn file theo điểm liên quan rồi bỏ phần còn lại.
2. Một vòng agent xử lý lần lượt các phần, ghi dữ kiện ứng viên và danh sách tham chiếu chưa giải quyết. Cách chia lượt là cơ học; việc hiểu code do agent làm.
3. Agent dùng tìm kiếm/đọc bổ sung để lần theo import, đăng ký router, model và client. Có thể đọc file của component khác để hiểu tham chiếu, nhưng không thay owner.
4. Bộ điều phối kiểm phần chưa đọc và các tham chiếu còn hở, yêu cầu xử lý tiếp trong ngân sách. Không nhận lời tự báo “đã đọc hết” làm bằng chứng.
5. Khi đủ dữ liệu hoặc chạm giới hạn, kiểm và xuất phần hợp lệ. Đọc thiếu phải ghi partial; “đã gửi đủ source” vẫn không đồng nghĩa “đã hiểu đúng”.

Khởi đầu với một vòng điều phối tuần tự và một sổ dữ kiện chung. Chưa cần nhiều agent đệ quy; chỉ xem xét tăng đồng thời sau pilot nếu đo được lợi ích và kiểm được dữ kiện trùng/mâu thuẫn.

**Giao diện dữ liệu cần chốt ở N1**

Đây là mô hình logic đề xuất, chưa phải schema đã cài đặt.

| Đối tượng | Trường tối thiểu và bất biến |
|---|---|
| `DocumentInput` | version, snapshot, phạm vi file, component ID/tên/loại/file thành viên, dữ liệu route kiến trúc và artifact sơ đồ được cấp; giữ nguyên membership |
| `ReadReceipt` | ID do code cấp, snapshot/file/hash, khoảng dòng và cột nếu cần, phần đã che/cắt, request đã gửi, trạng thái phản hồi; không tin model tự tạo receipt |
| `FieldValue` | state `known/unknown/not_applicable`; known có value + nhãn `exact/inferred` + evidence; inferred có rule/reason; unknown có reason; null không thay unknown |
| `RouteFact` | vị trí decorator/handler, chuỗi đăng ký router/mount có thứ tự, method/path, parameter/model/status/dependency/auth, owner từ membership |
| `ModelFact` | định danh file + tên đầy đủ; trường/alias/type/required/nullable và nguồn; tham chiếu lồng nhau; phân biệt dùng cho request/response |
| `FileRoleFact`, `HttpCallFact` | vị trí file/call site, owner, thuộc tính theo AC07/08 và evidence; HTTP không gộp chỉ vì cùng URL |
| `DocumentResult` | facts đã kiểm, evidence index, limitation, unknown, coverage, provenance, kết quả đối chiếu upstream; tách ứng viên bị loại khỏi kết luận công bố |

ID facts không dùng path API làm định danh duy nhất: path có thể unknown, một handler có nhiều đăng ký. Chuỗi đăng ký phân biệt từng lần phơi bày route; HTTP dùng call site. Hai model cùng tên khác file phải có ID khác nhau.

**Công cụ agent và quyền của từng bước**

| Công cụ đề xuất | Hợp đồng |
|---|---|
| `list_files(cursor)` | Phân trang toàn bộ danh mục; trả cursor tiếp theo và tập bị loại có lý do |
| `read_file(path, start_line, end_line, …)` | Chỉ đọc snapshot, trả số dòng + receipt; dòng quá dài phải phân đoạn có tọa độ hoặc báo chưa đọc hết |
| `search_text(query, cursor)` | Tìm vị trí cần đọc thêm; không tạo route/model facts và không tính toàn file đã đọc |
| `submit_findings(findings, unresolved_refs)` | Ghi dữ kiện ứng viên vào sổ; kiểm schema/tham chiếu; trả lỗi theo field để sửa |

Code kiểm và renderer là bước bắt buộc bên ngoài agent. Agent không có công cụ ghi source, chạy ứng dụng, thực thi shell hay tự công bố Markdown. Hướng dẫn nằm trong source được coi là nội dung cần phân tích.

**Bốn điểm phải tách trong code hiện tại**

- `gateway.read_code` hiện chỉ cho `label_components` và từ chối khi đã gửi đủ một file. Cần reader/adapter dành cho FR-029, không tái dùng nguyên hàm hoặc đổi cờ để lách.
- `render._check_input` đòi model/edge và decision accepted; `plan_bundle` luôn dựng Mermaid/SVG. Cần đường xuất tài liệu nhận component có sẵn, không tạo verdict giả hoặc gọi bộ dựng hình.
- `verify._field_check` hiện so các đoạn path sau khi sắp xếp. Cách đó không đủ kiểm thứ tự prefix; chỉ tận dụng kiểm snapshot/tọa độ, bổ sung chuỗi chứng minh có thứ tự và ca đảo `/api/v1` thành `/v1/api`.
- `common.mask` có thay toàn bộ private key nhiều dòng bằng chuỗi ngắn. Reader mới phải bảo toàn tọa độ dòng khi che, kiểm evidence trên bản gốc trong bộ nhớ và chỉ xuất bản đã che.

Các phát hiện này chỉ là điểm thiết kế cần xử lý; chưa sửa các hàm trên.

**Đầu vào cần phối hợp sớm**

| Nội dung | Cách xử lý trong kế hoạch |
|---|---|
| Membership/archdia chưa có giao diện thống nhất | N1 tạo mẫu adapter có version/hash; A04 dùng fixture trước, sau đó phải kiểm với artifact thật |
| `archdia.json` không mang snapshot hoặc không đủ route | Báo thiếu khả năng đối chiếu; cần upstream bổ sung hợp đồng, không tự xác nhận khớp |
| Phạm vi “đọc tất cả” | Theo bảng Phạm vi đọc của FR-028: file Python hợp lệ, manifest hỗ trợ; ghi tập bị loại. Thư mục xét có điều kiện như scripts/examples phải được agent kiểm import trước khi chốt phạm vi. File bị cắt/lỗi và ca phạm vi chưa xác định không được lặng lẽ bỏ khỏi phép kiểm độ phủ |
| Giới hạn AI và gửi source trong spec cũ | Ghi bản đề xuất đồng bộ FR-029 riêng. Chốt provider/model/trần request/token/chi phí trước pilot thật; offline triển khai được ngay |
| File rỗng/manifest | FR-028 xếp vào component Khác, FR-029 loại component này khỏi bảng cấu trúc. Nếu upstream gán khác thì báo bất nhất đầu vào; không tạo dòng code giả |

Không dùng các điểm phối hợp này làm lý do dừng những nhiệm vụ offline độc lập.

## Nền tảng dùng chung — 4 nhiệm vụ

**N1 — Chốt giao diện dữ liệu FR-029**

- Làm: schema route, registration/prefix, parameter, request/response model, dependency/auth/status, file role, HTTP call, limitation và evidence theo từng trường.
- Nhận: mapping component có ID, tên, file thành viên và snapshot; danh sách route kiến trúc; sơ đồ có sẵn. Quy định version và cách kiểm cùng source. Component là input bất biến.
- Đầu ra: mẫu hợp lệ/sai; giao diện agent → bộ kiểm → renderer. Dự kiến `agent_contracts.py`, `document_input.py`. ID/hash chính thức do code sinh.
- Làm rõ: missing/null/unknown/not_applicable; exact/inferred; redacted; phân biệt file đã đọc và dữ kiện đã xác định. Đồng bộ ranh giới gửi source, giới hạn vòng gọi và ngân sách với NFR-AI/SEC.
- Chốt phạm vi theo FR-028 và giữ danh mục snapshot riêng với tập file được phân tích. Không đổi snapshot chỉ vì agent kết luận một file thuộc diện loại. Lập bảng contract/test chính thức theo quy trình dự án trước khi đóng Definition of Ready; các mã công việc trong bản này không thay ID chính thức.
- Xong khi: diễn tả được route có nhiều prefix, nhiều lần đăng ký, model dùng chung, owner thiếu, URL động và bằng chứng nhiều file; không cần tạo component để có input hợp lệ.
- Phụ thuộc: không. Giao diện upstream cần phối hợp, fixture dùng để phát triển trước khi có đầu vào thật.

**N2 — Công cụ đọc và sổ theo dõi độ phủ**

- Làm: `list_files`, `read_file(path, start_line, end_line)`, `search_text` trên snapshot; trả tọa độ, hash, trạng thái cắt và mã lần đọc. Dự kiến `source_tools.py`.
- Theo dõi: khoảng dòng thực tế được gửi vào lượt model xử lý; trạng thái chưa đọc/đọc một phần/đã gửi hết/bị loại/lỗi. Search hit hoặc server nạp file chưa được tính là đã đọc hết.
- Ghi riêng `delivered` và `processed`: request timeout không được coi là xử lý xong dù payload đã gửi. Chỉ đóng một phần sau phản hồi hợp lệ ghi dữ kiện hoặc xác nhận đã xét, kèm receipt. Dòng dài bị cắt còn khoảng chưa phủ; file rỗng được ghi trạng thái riêng, không chia tỷ lệ cho 0.
- Phạm vi: đọc mọi file trong phạm vi FR công bố; đọc từng phần nếu lớn, không chỉ top file. Ghi lý do loại; không chạy/import source; che bí mật và giữ tọa độ đối chiếu.
- Kiểm: Unicode/CRLF, file lớn, khoảng dòng bị hổng, source đổi trên đĩa, symlink/path vượt root, bí mật nhiều dòng, request lỗi và dữ liệu bị cắt.
- Xong khi: mọi phần chưa đọc được phát hiện; không có lỗ độ phủ nhưng báo full. Đọc đủ source không được đồng nhất với phân tích đúng.
- Phụ thuộc: N1.

**N3 — Adapter model và vòng agent**

- Làm: vòng đọc → ghi dữ kiện → đọc bổ sung → kiểm → sửa có giới hạn. Dự kiến `agent.py`, `agent_provider.py`, `agent_prompts.py`.
- Bổ sung: fake provider; timeout/hủy; theo dõi token/request/chi phí; thiếu usage không báo chi phí 0; lưu phiên bản model/prompt/schema. Mọi lượt sửa tính vào ngân sách.
- Giữ ngữ cảnh: sổ dữ kiện có ID và các điểm chưa giải quyết; khi rút gọn lịch sử vẫn giữ tham chiếu để đọc lại. Tóm tắt không thay source chưa đọc.
- Điều phối: quét đủ phần source → giải tham chiếu xuyên file → xử lý lỗi bộ kiểm. Ghi kết quả từng phần có tính lặp an toàn; retry cùng receipt không sinh fact trùng. Dừng khi đủ việc hoặc đạt trần đã cấu hình; cùng lỗi lặp lại không được tiêu ngân sách vô hạn.
- Kiểm: tool call sai, JSON/output bị cắt, retry, hết ngân sách, lặp không tiến triển, nội dung repo giả làm chỉ dẫn. Agent không có công cụ chạy lệnh hoặc sửa source.
- Xong khi: test offline chạy đầu-cuối khi chặn `extract.extract`, `model.build`, `annotate.annotate`; lỗi model không quay về extractor để tạo kết quả giả hoàn chỉnh.
- Phụ thuộc: N1–N2; tích hợp N4 trước pilot.

**N4 — Kiểm bằng chứng và chuẩn bị phép đo độc lập**

- Làm: kiểm schema, ID, snapshot/hash, tọa độ, evidence đã được cung cấp, tham chiếu model và nguồn cho từng trường. Kết luận nhiều bước giữ toàn bộ chuỗi bằng chứng cần thiết.
- Xử lý: lỗi trả đúng field để agent đọc lại; sau giới hạn sửa, bỏ giá trị không có bằng chứng hợp lệ và ghi lý do. Không nâng nhãn exact chỉ vì quote khớp.
- Phép đo: viết fixture/gold theo từng AC trước khi chỉnh prompt; chấm sự tồn tại và thuộc tính riêng. Các ca cố ý sai prefix, required, nullable, auth, HTTP đích và nhãn phải bị bắt.
- Đầu ra: bộ kiểm contract, audit quyết định và harness chấm source → dữ kiện → tài liệu. Không dùng output extractor làm gold.
- Nguồn gold cho route, tham số, model, status (người dùng duyệt 07/10): chạy `app.openapi()` và liệt kê `app.routes` trong sandbox. Sandbox là venv riêng, tắt mạng sau khi cài dependency, chỉ dùng cho fixture và repo đánh giá, không có trong sản phẩm. Output oracle chỉ để dựng gold, không đưa vào prompt hay input agent. Oracle không có `file:dòng` và vẫn liệt kê route mà FR-029 loại (gắn trong test, `add_api_route`). Người lập gold lọc theo FR, thêm evidence, rồi người khác review. Repo không import được (thiếu biến môi trường, cần DB) thì lập gold tay và ghi lý do. Gold vai trò file và HTTP lập tay.
- Phân tách ba phép kiểm: (1) evidence có thật/đã được gửi; (2) dữ kiện nhất quán về schema/tham chiếu/chuỗi đăng ký; (3) ý nghĩa đúng theo gold độc lập. (1) và (2) chạy mọi lần; (3) chạy khi đánh giá, không biến kết quả (1) thành chứng nhận (3).
- Xong khi: phát hiện quote bịa/khác snapshot, tham chiếu lạc và đầu ra mâu thuẫn; có bộ chấm ngữ nghĩa độc lập. Agent tự rà soát không thay gold.
- Phụ thuộc: N1–N2; chuẩn bị gold song song về tiến độ với N3, không cần chờ gọi model thật.

## Triển khai đúng 8 AC — 8 nhiệm vụ

**A01 — AC-029-01: Sinh tài liệu API và path đầy đủ**

- Agent đọc: FastAPI/APIRouter decorator, handler, import/alias, `include_router`, `mount`, prefix và các lần đăng ký.
- Ghi dữ liệu: method, đường dẫn đầy đủ, handler, vị trí khai báo, chuỗi nguồn tạo path và component theo mapping. Không coi cùng handler đăng ký ở hai path là một route.
- Xuất: một file API cho mỗi component có route; đúng tên file/frontmatter; mã fact và bằng chứng. Writer nhận dữ liệu N1, không đọc source hoặc gọi model.
- Kiểm: prefix nhiều tầng, router dùng lại, mount app, alias, router trong factory, prefix chưa biết. Markdown và OpenAPI cùng route có thể biểu diễn được; omission có lý do.
- Ca bắt buộc thêm: `api_route(methods=[...])` sinh một route cho mỗi method; router gắn hai lần với hai prefix.
- Chuỗi prefix giữ thứ tự từ app tới decorator; có evidence ở từng nơi đăng ký. Ca đối chứng phải gồm hai path có cùng đoạn nhưng đảo thứ tự. Route khai nhiều method/đăng ký nhiều nơi giữ từng trường hợp; không tự gộp theo handler.
- Xong khi: từng route đối chiếu được với gold, đủ chuỗi evidence; không bỏ route chỉ vì path còn thiếu phần động.
- Code chính: agent/prompt/schema mới, `render_api` trong `render.py`.
- Phụ thuộc: N1–N4; A03/A05 đi cùng trước khi đóng nhiệm vụ.

**A02 — AC-029-02: Tham số, model và status**

- Agent đọc: path/query/header/body, tên, kiểu, required; request/response model, trường lồng nhau, nullable và nơi khai báo; status; dependency/auth theo bảng nội dung của FR.
- Giữ chính xác: Optional không tự đồng nghĩa có default; request và response không bị gộp; danh sách model giữ kiểu mảng; model dùng chung được tham chiếu đúng.
- Xuất: bảng tham số, bảng từng model, khối OpenAPI 3.1 đồng nghĩa. Dependency chưa chứng minh auth không được mô tả là đã xác định cơ chế auth.
- Kiểm: nested/list model, alias, required nhưng nullable, body tùy chọn, model cùng tên khác file, reference vòng, status khai rõ/default, auth ở app/router/handler.
- Ca bắt buộc theo luật framework. Mỗi luật có ít nhất một fixture, gold lấy từ oracle N4:
  - Tham số khai trong hàm `Depends` (kể cả lồng nhiều tầng) cũng là tham số của endpoint.
  - `Annotated[..., Query()/Header()/Body()]` quyết định vị trí tham số.
  - Có từ hai tham số body trở lên, hoặc có `Body(embed=True)`, thì body được bọc thêm một tầng theo tên tham số.
  - `Form`/`File` dùng content type khác JSON.
  - `response_model` ưu tiên hơn kiểu trả về khai trên hàm.
  - Status mặc định lấy từ `response_class`.
  - `Optional[X]` không có default: Pydantic v1 coi là không bắt buộc, v2 coi là bắt buộc nhưng nhận null. Agent phải xác định version Pydantic từ manifest; không xác định được thì `unknown`.
- Nguồn luật: source FastAPI và Pydantic ở version ghim trong N1 (xem [bản nghiên cứu](L3-nghien-cuu-repo-sinh-tai-lieu.md) mục 7). Chưa đọc lại source ở version ghim; phải xác nhận trước khi viết gold.
- Xong khi: đúng từng thuộc tính so với gold; `$ref` hợp lệ; có lý do cho phần chưa biểu diễn được, không viết "không cần auth" vì thiếu dữ kiện.
- Code chính: schema/prompt agent, writer API, test renderer.
- Phụ thuộc: A01, A03.

**A03 — AC-029-03: Unknown, inferred và phần biết được**

- Làm: áp nhãn đến từng trường, không chỉ toàn route. Unknown có lý do; suy ra mặc định framework có tên quy tắc và nguồn phù hợp version.
- Prefix: dùng default khai trong code khi có; thiếu thì unknown. Không suy kiểu từ tên biến. Không tự áp kiến thức framework khi không xác định đủ điều kiện.
- Xuất: giữ phần đã biết trong Markdown/result; OpenAPI chỉ có phần đúng định dạng, ghi rõ route/field bị bỏ và lý do. Retry không điền mặc định mới.
- Kiểm: prefix động, type không rõ, thiếu auth, unknown khác null, default status, model/schema không thể biểu diễn.
- Xong khi: không thay unknown bằng giá trị đoán; không giấu omission; quote khớp không là căn cứ duy nhất cho nhãn exact.
- Code chính: schema/validator, helper field, writer API/README.
- Phụ thuộc: N1, N4; xây từ đầu cùng A01–A02.

**A04 — AC-029-04: Đối chiếu với dữ liệu kiến trúc được cung cấp**

- Nhận: `archdia.json` thật hoặc fixture cùng snapshot, có component/file thành viên và route. Không gọi thuật toán tạo component/cạnh, không render hình.
- Kiểm: tập route tài liệu và JSON kiến trúc bằng nhau; thư mục tài liệu ứng với đúng component; owner theo file khai báo; component bị cắt khỏi hình vẫn giữ tài liệu.
- Báo: thiếu/thừa route, sai owner, ID/version/snapshot không khớp. Không sửa dữ kiện hoặc lén lọc route để hai phía trông giống nhau.
- Khóa đối chiếu chốt trong N1 gồm vị trí khai báo/đăng ký, method, path và owner phù hợp schema upstream. Path unknown không được coi bằng một path cụ thể. Agent phân tích source trước; tập route upstream chỉ đưa vào bước đối chiếu, tránh dùng nó để che route bị bỏ sót.
- Kiểm thử: bộ khớp; thiếu/thừa route; sai owner; component đổi tên/ID; khác snapshot; hơn 50 component; không có input upstream.
- Xong khi: adapter/test fixture qua và có phép đối chiếu trên đầu vào thật. Chưa có input thật thì AC này là not_evaluated; các AC độc lập vẫn làm và kiểm được.
- Code chính: `document_input.py` và hàm đối chiếu; tách kiểm tài liệu khỏi `model.build`/graph checks cũ.
- Phụ thuộc: N1, A01; hoàn tất tích hợp khi upstream cung cấp dữ liệu. Đây là kiểm tính nhất quán, không nghiệm thu chất lượng sơ đồ.

**A05 — AC-029-05: Loại route ngoài phạm vi và ghi giới hạn**

- Làm: không xuất route từ test hoặc thư mục ngoài phạm vi. Không xuất route chỉ được gắn qua registration nằm trong test.
- Agent nhận diện và ghi từng lời gọi `add_api_route`, `add_route`, `add_websocket_route` thành limitation có file:dòng; không sinh route cho các dạng này theo FR.
- Kiểm: test file ở nhiều cấp, app/router khai trong test, router production chỉ được test đăng ký, decorator có tên giống route nhưng không phải FastAPI, nhiều lời gọi non-decorator.
- Xong khi: route không hợp lệ không vào tài liệu/result route set; từng dạng ngoài hỗ trợ có nơi dùng, không mất im lặng. Không tự sửa graph upstream; sai khác được A04 báo.
- Code chính: metadata phạm vi reader, prompt/dữ kiện agent, validator output và regression `test_fr029.py`.
- Phụ thuộc: N2–N4; triển khai cùng A01.

**A06 — AC-029-06: README đầy đủ và liên kết đúng**

- Xuất: mục lục từng file API kèm owner, sơ đồ có sẵn do phần kiến trúc cấp, cấu trúc component, HTTP ra ngoài, contract chưa gán và giới hạn.
- Chỉ dùng dữ kiện đã kiểm; số route/file và owner khớp result. Thiếu owner thì giữ dữ kiện và danh sách chưa gán, không tự tạo component. Không viết README bằng một lượt model độc lập làm phát sinh kết luận mới.
- Sơ đồ: nhúng/dẫn đúng artifact được cấp cùng snapshot; không dựng hình. Chưa được cấp thì ghi thiếu đầu vào; chưa báo AC-06 hoàn thành toàn bộ.
- Kiểm: mục lục/link, slug trùng, Unicode/escaping, không có HTTP, có unknown/limitation, owner thiếu, thiếu hoặc khác snapshot của sơ đồ.
- Xong khi: tất cả mục bắt buộc có nội dung/trạng thái phù hợp, không có link hỏng, số liệu đối chiếu được; phần upstream thiếu được báo chính xác.
- Code chính: `readme`/bundle writer và test đọc artifact độc lập.
- Phụ thuộc: A01–A03, A05, A07–A08; hợp đồng artifact từ N1.

**A07 — AC-029-07: Package/module và đúng một vai trò mỗi file**

- Nhận component/file thành viên từ bên ngoài. Agent đọc dấu hiệu trong file và quan hệ source để xác định vai trò, không đổi membership.
- Thứ tự xét theo FR: Điểm vào → Route → Model bảng → Hạ tầng → Truy cập dữ liệu → Schema API → Cấu hình → Service → Khác.
- Service: cần căn cứ nằm trên đường gọi từ route tới data access/hạ tầng, mang inferred và lý do. Không suy vai trò từ tên `services.py`/`repository.py`. Các nhãn khác theo FR và evidence; không coi model tự nói exact là đủ.
- Xuất: liệt kê file dưới package trong component, trừ component Kiểm thử/Migration/Khác theo FR; mỗi file một vai trò, evidence/giới hạn tương ứng. Phân biệt vai trò "Khác" của file với loại component "Khác".
- Kiểm: file có nhiều dấu hiệu, tên đánh lừa, service không có đường gọi chứng minh, schema dùng chung, file không có dấu hiệu. File rỗng/manifest phải theo component Khác và được loại đúng; upstream gán sai thì báo, không tạo evidence dòng giả.
- Xong khi: không sót/trùng file trong tập cần liệt kê; đúng thứ tự vai trò; Service luôn inferred; tác vụ này không sinh tài liệu bảng/DDL dù có nhận diện vai trò model bảng.
- Code chính: schema/prompt file role, validator và mục README cấu trúc.
- Phụ thuộc: N1–N4, A01 cho nguồn đường gọi; không cần thuật toán chia component.

**A08 — AC-029-08: Lời gọi HTTP ra ngoài**

- Agent đọc lời gọi qua `httpx`, `requests`, `aiohttp`; import/alias, client, base URL và cấu hình liên quan.
- Ghi một dòng mỗi lời gọi: owner theo file, thư viện, method, URL nguyên văn hoặc khóa cấu hình chứa URL, evidence. Method/đích runtime chưa xác định là unknown kèm lý do; che bí mật.
- Thư viện HTTP ngoài phạm vi: ghi limitation và nơi dùng. Không suy mọi `get()`/`post()` là HTTP.
- Checklist dạng gọi lấy từ CodeQL `Httpx.qll`/`Requests.qll`/`Aiohttp.qll` (bản nghiên cứu mục 7): hàm cấp module, method của Client/AsyncClient/Session và lớp con, `request(method, url)` và `stream`. URL nằm ở `url=`, hoặc đối số thứ hai với `request`/`stream`, còn lại là đối số đầu.
- Kiểm: async client, session/context manager, alias/shadowing, database.get, client tạo ở file khác, request method động, URL ghép, key cấu hình, credential trong URL, thư viện chưa hỗ trợ.
- Xong khi: gold có đủ từng call site; không nhầm DB thành HTTP; đích động không bị đoán; README và result đồng nhất.
- Code chính: schema/prompt HTTP, validator và writer README. Tái dùng ca hồi quy hiện có nhưng chạy qua luồng agent.
- Phụ thuộc: N1–N4, A03; phát triển độc lập với A02/A07 khi đã có schema.

## Kiểm cuối và bàn giao — 2 nhiệm vụ

**V1 — Đánh giá độ chính xác FR-029**

- Offline: tools, fake agent/provider, evidence/schema, ownership, các ca từng AC, validator OpenAPI 3.1 và phép đối chiếu Markdown/OpenAPI/result độc lập.
- Model thật: pilot repo phát triển nhỏ trước; ghi model/prompt/schema/snapshot, dữ kiện, độ phủ, token, chi phí và thời gian. Rà lại thiếu sót bằng lượt agent riêng có giới hạn, đo trước/sau thay vì mặc định tốt hơn.
- Nghiệm thu: gold độc lập theo OBS, P/R ≥80% riêng route, request/response model và HTTP trên từng repo kín nhỏ/vừa; bằng chứng kết luận công bố hợp lệ 100%; exact sai ≤5%. Không dùng unknown để tính là đã giải đúng; mẫu số 0 là not_evaluated.
- Vai trò file/package: bổ sung matching và ca theo AC-07; NFR chưa ghi riêng ngưỡng số cho loại này, không tự tuyên bố ngưỡng đã được phê duyệt. Báo độ đầy đủ và lỗi từng vai trò.
- Trạng thái: test fixture qua không đồng nghĩa model thật đúng; 8/8 AC chỉ công bố khi có bằng chứng cho từng AC, kể cả input tích hợp A04 và sơ đồ được cấp cho A06.
- Kiểm nội bộ khi phát triển (người dùng duyệt 07/10). Hai phép kiểm này không phải phép đo nghiệm thu, vì OBS-001 quy định đo 1 lần mỗi cấu hình và bỏ so với bộ luật tĩnh cũ:
  - **Sàn:** trên golden dev, route của agent không kém extractor hiện có (TP/FP/FN 61/0/0, đo 02/10). Extractor chỉ dùng để so, không làm input hay gold. Kém hơn thì chưa chuyển luồng mặc định sang agent.
  - **Dao động:** ở pilot, mỗi cấu hình chạy 3 lần trên cùng snapshot. Báo P/R từng lần và danh sách fact không xuất hiện đủ 3/3. Fact dao động là ca cần sửa bước đọc hoặc prompt.
- Báo thêm lỗi từng thuộc tính: prefix, vị trí tham số, required, nullable, status, dependency/auth, URL và vai trò. Đo một lần mỗi cấu hình theo OBS; không lấy lần tốt nhất. Không đọc đáp án repo kín để chỉnh prompt; không dùng bộ gold sơ đồ thay gold dữ kiện FR-029.
- Phụ thuộc: N4 chuẩn bị từ đầu; đo từng tính năng khi hoàn thành, tổng hợp sau A01–A08. Chưa chạy thử thật trong phiên lập kế hoạch.

**V2 — CLI, xuất an toàn, retry và bàn giao**

- Nối luồng FR-029 agent với CLI, schema và writer; giữ nguồn bất biến; từ chối output không rỗng; publish staging/manifest; retry render dùng dữ liệu đã đóng băng, không gọi model.
- Đề xuất lệnh riêng `l3slice document` và hàm `run_documents` để triển khai từng bước; tên tham số chốt ở N1. Thay thông báo/provider cũ của luồng này bằng cấu hình FR-029 đã chốt. Trạng thái artifact, độ phủ phân tích và kết quả 8 AC là ba trường riêng; file ghi thành công không tự chuyển AC thành passed.
- Tách graph dependency: tài liệu không bị chặn bởi lệnh dựng hình hoặc trần 50 node. Không tự xóa pipeline/test cũ, không mở rộng sang TBL/EVT/web.
- Trạng thái: hết ngân sách, source đọc thiếu, model lỗi, artifact lỗi và thiếu upstream đều có lý do; không ghi completed giả hoặc âm thầm dùng extractor cũ.
- Bàn giao: bảng AC → task → test → kết quả thực chạy; hướng dẫn cấu hình/chạy/giới hạn; cập nhật HANDOFF. Lỗi gateway cũ chỉ ghi baseline thực kiểm, không tự sửa ngoài phạm vi.
- Xong khi: tái chạy được một ca API/README/result; retry giữ dữ kiện; chỉ đổi mặc định khi đạt tiêu chí liên quan và công bố rõ phần tích hợp chưa kiểm nếu có.
- Phụ thuộc: nối CLI tối thiểu từ A01; hoàn thiện sau A06/V1. Không commit/push tự động.

**Mapping đủ 8 AC**

| AC | Task chính | Phụ thuộc dùng chung | Đầu ra kiểm được |
|---|---|---|---|
| 029-01 | A01 | N1–N4, A03, A05 | File API, route/path/handler/evidence |
| 029-02 | A02 | A01, A03 | Tham số/model/status, bảng và OpenAPI |
| 029-03 | A03 | N1, N4 | Nhãn theo field, unknown/inferred, omission có lý do |
| 029-04 | A04 | N1, A01, input FR-028 | Báo tập route/owner/component khớp hoặc khác |
| 029-05 | A05 | N2–N4 | Route set đã loại test; limitation non-decorator |
| 029-06 | A06 | A01–A03, A05, A07–A08, sơ đồ có sẵn | README đủ mục và link đúng |
| 029-07 | A07 | N1–N4, A01 | Package/module/vai trò/evidence, Service inferred |
| 029-08 | A08 | N1–N4, A03 | HTTP call site, đích hoặc unknown, giới hạn |

**Thứ tự thực hiện**

| Đợt | Công việc | Mốc xem kết quả |
|---|---|---|
| 1 | N1–N4; chốt giao diện component/route/sơ đồ được cấp | Schema, fixture/gold, vòng agent offline |
| 2 | A03 + A05 cùng A01; CLI tối thiểu của V2 | Source → route/path → API nháp có bằng chứng |
| 3 | A02; đo pilot V1 | API Markdown/OpenAPI đủ model/tham số/status |
| 4 | A07 và A08; ghép A06 | README cấu trúc file và HTTP có bằng chứng |
| 5 | A04 và hoàn tất nhận sơ đồ cho A06 | Kiểm dữ liệu upstream; không dựng sơ đồ |
| 6 | Tổng hợp V1; hoàn thiện V2 | Báo cáo từng AC và gói bàn giao |

Chuẩn bị A04 bằng fixture ngay từ đợt 1, không đợi cuối mới phát hiện giao diện lệch. Đo chất lượng sau từng đợt; không dồn tất cả sang đợt 6. Chưa ước lượng số ngày trước khi pilot xác định chi phí/ngữ cảnh và lỗi thực tế.

## Chia phần code và bộ kiểm khi thực hiện

Tên file mới là đề xuất. Mỗi dòng là một phần có thể review độc lập; không cần tạo nhiều tầng class hoặc đưa framework mới vào trước khi cần.

| Phần | Nơi triển khai dự kiến | Bằng chứng hoàn thành |
|---|---|---|
| N1 | `slice/l3slice/agent_contracts.py`, `document_input.py` | Schema và fixture hợp lệ/sai; mapping version/snapshot/owner; tài liệu dữ liệu gửi model |
| N2 | `slice/l3slice/source_tools.py`; tận dụng phần snapshot phù hợp | `test_source_tools.py`: đủ khoảng nội dung, không đọc ngoài root, che giữ tọa độ, lỗi không báo đủ |
| N3 | `slice/l3slice/agent.py`, `agent_provider.py`, `agent_prompts.py` | `test_document_agent.py`: fake provider, retry/trần/hủy, tham chiếu xuyên file, không gọi extractor |
| N4 | `slice/l3slice/document_verify.py`; helper evidence hiện có sau khi kiểm | `test_document_verify.py`: quote/hash/receipt sai, prefix đảo thứ tự, field thiếu evidence, conflict |
| A01–A03/A05 | Schema + prompt; `render_api` và các helper OpenAPI phù hợp | `test_document_api.py`: source fixture → facts → Markdown/OpenAPI, các ca lỗi của từng AC |
| A04 | `document_input.py`, `document_verify.py` | `test_document_parity.py`: route/owner/snapshot khớp và lệch; kiểm input thật khi có |
| A07–A08 | Prompt/dữ kiện vai trò và HTTP; không dựng call graph bằng AST | `test_document_structure_http.py`: vai trò ưu tiên, Service có đường gọi, HTTP alias/dynamic/DB.get |
| A06/V2 | `slice/l3slice/document_pipeline.py`, `document_render.py`; nối `__main__.py` | `test_document_pipeline.py`: README đủ mục, artifact đầu vào, publish/retry, trạng thái partial |
| V1 | Mở rộng `slice/evaluation_l3/` bằng scorer dữ kiện riêng | Báo cáo TP/FP/FN và thuộc tính theo repo, lỗi nhãn, bằng chứng; parser artifact độc lập |

Giữ test cũ để bảo vệ luồng hiện tại; fixture phù hợp được dùng lại. Test agent offline chỉ chứng minh điều phối/kiểm/xuất, không chứng minh model thật nhận diện đúng. Các test mới trên chưa được tạo hay chạy.

**Phân vai agent khi phát triển (người dùng duyệt 07/10)**

Mục này nói về các agent lập trình viết code và gold. Nó không đổi vòng agent tuần tự lúc chạy sản phẩm (mục Thiết kế). Mỗi agent làm trong một git worktree riêng. Phiên điều phối tự gộp code, không agent nào commit hay push.

| Agent | Task | Không được làm |
|---|---|---|
| G — Gold | Fixture, gold và oracle của N4 cho cả 8 AC | Không đọc code hay prompt của luồng agent, để gold độc lập |
| C1 — Nền | N1–N3, ca xuyên suốt đầu tiên | Không sửa fixture hay gold |
| C2 — API | A01, A02, A03, A05 | Như trên |
| C3 — Cấu trúc và HTTP | A07, A08 | Như trên |
| C4 — Tích hợp | A04, A06, V2 | Không tạo component, không dựng sơ đồ |
| K — Kiểm | Chạy test, review code, chấm theo gold (V1) | Không sửa code |

Thứ tự: G và C1 chạy song song. C2 và C3 chạy song song sau khi C1 xong ca xuyên suốt. C4 chạy sau cùng. K kiểm sau mỗi lần gộp. Gold phải có trước khi chỉnh prompt của task tương ứng.

**Ca xuyên suốt đầu tiên — làm trước khi mở rộng**

- Fixture nhỏ có app → include_router hai tầng → handler; Pydantic model lồng nhau; một lời gọi httpx; một route test; một add_api_route phải vào giới hạn.
- Membership và artifact kiến trúc được viết sẵn cùng snapshot. Không dùng code phân tích hoặc sinh sơ đồ để tạo đầu vào trong luồng tài liệu.
- Fake provider đi qua công cụ đọc và nộp facts; bộ kiểm cố tình nhận thêm một evidence sai để chứng minh có loại. Kết quả giữ phần đúng và ghi phần thiếu.
- Xuất một API Markdown có OpenAPI 3.1, README và result; chặn lời gọi `extract.extract`, `model.build`, `annotate.annotate`, `mermaid` và `svg` trong test.
- Sau khi ca offline qua, chạy pilot thật trên fixture/repo phát triển bằng cấu hình đã chốt. So với gold trước khi mở rộng prompt; chưa đạt thì sửa bước đọc/giải tham chiếu hoặc bộ dữ liệu, không chỉ sửa văn phong.

**Điều kiện kết thúc kế hoạch triển khai**

1. Mỗi AC có test và kết quả thực chạy; A04/A06 có đầu vào thật đúng snapshot. Thiếu bằng chứng thì `not_evaluated`, sai thì `failed`.
2. V1 đạt ngưỡng đã nêu trên từng repo kín nhỏ/vừa; không dùng số trung bình che repo không đạt.
3. Có báo cáo riêng về source chưa đọc, thông tin unknown, dữ kiện bị loại, lỗi render và chi phí. Không lấy file viết thành công làm tiêu chí duy nhất.
4. Hướng dẫn CLI và HANDOFF ghi đúng phiên bản đã chạy; giữ kết quả offline, pilot và nghiệm thu tách nhau.

**Trạng thái:** đã nghiên cứu các phần mã liên quan của 4 repo, bổ sung thiết kế và kế hoạch gồm 14 nhiệm vụ (4 nền tảng + 8 theo AC + 2 kiểm/bàn giao). Chưa hoàn thành nhiệm vụ triển khai nào; phiên này chỉ sửa tài liệu, chưa sửa code/spec, chưa chạy test sản phẩm/model.
