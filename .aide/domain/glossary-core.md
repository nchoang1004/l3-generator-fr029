---
uid: "01M2J06Z3HXPW1MKV9XBWJR7YW"
key: "GLOSS-L3GEN-001"
type: "glossary"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 10
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# Thuật ngữ và bất biến miền sản phẩm

Tài liệu này thống nhất cách gọi trước khi chia capability và component. Nó không chọn
pipeline, framework triển khai hay thứ tự chạy. Khi một ghi chép thiết kế cũ dùng từ khác
với tài liệu này, nghĩa trong baseline yêu cầu và tài liệu này được ưu tiên.

**Revision 4 (23/09/2026):** cập nhật theo PRD revision 25. Mô hình ngôn ngữ nay là bắt
buộc và được đề xuất component, quan hệ. Code vẫn kiểm bằng chứng trước khi công bố.
Revision 3 (approved 21/09/2026) viết cho hướng AI mặc định tắt; các mục đổi là 2, 4, 5,
bất biến #6, #8 và mục 7.

**Revision 5 (23/09/2026):** code chia component tất định, model chỉ chia khi repository phẳng; L3 là contract (API, TBL, EVT), sơ đồ component là mức L2.

**Revision 6 (02/10/2026):** component theo định nghĩa của quy trình mentor (CR-L3GEN-2026-004): gánh một trách nhiệm nghiệp vụ và sở hữu contract. Code lần theo route để nhóm file; model gộp nhóm và đặt tên, code kiểm. Bỏ thuật ngữ "repository phẳng". Đổi mục 3, mục 5 và bất biến #8.

**Revision 7 (02/10/2026):** sửa theo review REVIEW-SCOPE-L3GEN-2026-002. Component dùng chung được sở hữu contract khi file khai báo nằm trong nó. Bỏ việc model chọn chủ bảng. Thêm thuật ngữ: mã dòng, mã dữ kiện, khóa cấu hình, tên dùng chung, loại component, lớp bằng chứng. Sửa bất biến #8 và mục 7.

**Revision 8 (02/10/2026):** sửa theo recovery review REVIEW-SCOPE-L3GEN-2026-003: bỏ `mapped_column` khỏi danh sách không mang sang (FR-L3GEN-030 đọc nó); `add_api_route` ghi ở phần giới hạn; định nghĩa tên dùng chung khớp cách xếp file của FR-L3GEN-028.

**Revision 9 (02/10/2026):** bước 5 (domain design) cho FR-L3GEN-029. Thêm mục 3a (module, package, vai trò file, lời gọi HTTP ra ngoài) và bất biến #11. Mục "Service" cũ đổi tên thành "Đơn vị triển khai" (Khiêm quyết 02/10/2026); chữ Service chỉ còn là vai trò file.

**Revision 10 (02/10/2026):** sửa theo review REVIEW-ARCH-L3GEN-2026-001 (A19): mục 3a đủ chín vai trò của FR-L3GEN-029; định nghĩa Service trỏ đúng thứ tự xét của FR.

## 1. Nguồn và lần phân tích

| Thuật ngữ | Nghĩa dùng trong hệ thống |
|---|---|
| Repository | Tập source và cấu hình được người dùng cung cấp để phân tích. Repository có thể chứa nhiều application, mã dùng chung và phần ngoài stack hỗ trợ |
| Source snapshot | Nội dung đầu vào bất biến của một lần phân tích, có content digest; Git commit/ref chỉ là metadata bổ sung và không thay thế digest |
| Analysis run | Một lần engine xử lý đúng một source snapshot với một bộ cấu hình, tool version và rule version xác định |
| Analysis unit | Phần source được kiểm kê và phân tích chung. Manifest, source root, entry point và cấu trúc thư mục là evidence để xác định phạm vi, không tự chứng minh deployment boundary |
| Application | Điểm hợp thành/chạy ứng dụng được framework hoặc cấu hình hỗ trợ chứng minh. Một analysis unit có thể có không, một hoặc nhiều application |
| Đơn vị triển khai | Phần được triển khai riêng, chỉ khẳng định khi có bằng chứng phù hợp. Khi chưa đủ bằng chứng, sản phẩm dùng `analysis unit` hoặc boundary candidate. Trước revision 9 mục này tên là "Service"; chữ Service nay chỉ dùng cho vai trò file (mục 3a) |
| Entry point | Vị trí source/config có bằng chứng khởi tạo hoặc cấu hình application; không đồng nghĩa mọi code từ đó chắc chắn đã chạy |

## 2. Dữ kiện, kết luận và bằng chứng

| Thuật ngữ | Nghĩa dùng trong hệ thống |
|---|---|
| Code fact | Quan sát tất định từ source hoặc manifest, ví dụ import, definition, decorator, call hay dependency declaration; chưa mặc nhiên là kết luận kiến trúc |
| Candidate | Đối tượng hoặc quan hệ có tín hiệu ban đầu nhưng chưa đủ điều kiện để công bố thành architecture claim |
| Resolution result | Kết quả nối một tham chiếu/call tới một đích: `resolved`, `ambiguous`, `unresolved` hoặc `runtime-dependent` |
| Architecture claim | Thực thể hoặc quan hệ ở mức application/component được công bố trong architecture model |
| Model proposal | Cách gộp nhóm route, tên và trách nhiệm component, tên dùng chung thuộc riêng một component, do mô hình ngôn ngữ đề xuất kèm mã dòng. Chưa là architecture claim cho tới khi qua bước kiểm của code |
| Evidence | Các code fact trong tập fact của lần chạy, mỗi fact nằm ở file/range thuộc chính source snapshot, kèm lý do khi cần. Với cạnh A→B, evidence phải có ít nhất một fact đã xác định đích, vị trí thuộc A và đích thuộc B. Lời khẳng định của model không phải evidence |
| Mã dòng | Nhãn ngắn, ví dụ `[L12]`, gắn cho mỗi dòng code gửi model. Model trả mã; code tra ra `file:dòng` và nguyên văn. Mã không có trong danh sách đã gửi thì đề xuất đó bị loại |
| Mã dữ kiện | Định danh của một code fact trong `result.json`. Tài liệu L3 trỏ tới mã này làm bằng chứng |
| Khóa cấu hình | Tên một giá trị cấu hình đọc được trong code: trường của lớp kế thừa `BaseSettings`, khóa trong `os.environ[...]` hoặc `os.getenv(...)` |
| Diagnostic | Dữ liệu giải thích quá trình phân tích, candidate, raw call, budget hoặc nguyên nhân không kết luận được; không phải architecture claim |
| Limitation | Phần engine không đọc, không hỗ trợ, không resolve hoặc phải dừng do budget/runtime; không đồng nghĩa repository không có dữ kiện đó |
| Coverage | Bản kê phần đã xét, bị loại, lỗi hoặc ngoài phạm vi. Coverage mô tả phạm vi quan sát, không phải confidence của từng claim |
| Finding | Cảnh báo tất định cần xác minh, có evidence; không phải kết luận lỗi nghiệp vụ hay lỗ hổng bảo mật |

## 3. Mô hình kiến trúc và mức trình bày

| Thuật ngữ | Nghĩa dùng trong hệ thống |
|---|---|
| Component | Theo quy trình mentor: phần của hệ thống gánh một trách nhiệm nghiệp vụ và sở hữu contract của nó (API, bảng, sự kiện). Route, service, repository, model là cấu trúc bên trong một component. Phần nhiều component cùng dùng (kết nối CSDL, cấu hình, gửi email...) là component dùng chung; nó sở hữu contract khi file khai báo nằm trong nó, ví dụ bảng khai trong `models.py` dùng chung. Mỗi file thuộc đúng một component. Cách chia ở FR-L3GEN-028 |
| Loại component | Nghiệp vụ, Dùng chung, Khởi động, Chưa xếp, Kiểm thử, Migration, Khác. Nghĩa từng loại ở FR-L3GEN-028 mục "Component là gì". Ba loại cuối không vẽ trên sơ đồ |
| Nhóm route | Các route khai trong cùng một file, cùng các file chỉ những route đó dùng tới. Code lập nhóm bằng cách lần theo lời gọi từ handler xuống; model gộp các nhóm cùng trách nhiệm thành component |
| Tên dùng chung | Tên cấp cao nhất (hàm, lớp, biến) mà nhóm route của nhiều component cùng đi tới. Tên đó thuộc component dùng chung theo vai trò file, trừ khi model chọn được một component duy nhất dùng nó và code kiểm được. File theo component chiếm nhiều tên của file nhất (FR-L3GEN-028, mục "Cách xếp file") |
| Luồng xử lý | Đường đi của request, tác vụ nền hoặc lệnh dòng lệnh qua các component. Sơ đồ chỉ vẽ lời gọi thuộc luồng; lắp ráp (DI, tạo app, khởi động), kiểm tra rồi quay về (xác thực, quyền) và chỉ truyền session không vẽ |
| Architecture model | Tập application, component, interface, data, external system, event, configuration và quan hệ L3; đây là nguồn cấu trúc chung cho CLI, web và artifact xuất |
| Lớp bằng chứng | Phần của bộ kết quả giữ dữ kiện mức file, class, function, lời gọi, và component bị cắt khỏi hình sơ đồ. Không vẽ ở sơ đồ mặc định (NFR-L3GEN-ABST-002) |
| Evidence/diagnostic model | Dữ kiện chi tiết mức file/class/function/call dùng để kiểm chứng hoặc chẩn đoán; không được UI/diagram coi là lớp kiến trúc mặc định |
| IAM | Tên lịch sử của mô hình trung gian. Trong thiết kế mới phải nói rõ đang chỉ architecture model hay evidence/diagnostic model; không dùng `IAM` như một schema gộp mơ hồ cả hai |
| L2 | Mức component: sơ đồ component và dependency bên trong một application. Theo quy trình mentor, L2 nằm ở `architecture/l2/` |
| L3 | Mức contract, theo quy trình mentor: API, bảng dữ liệu (TBL) và sự kiện (EVT), chia theo component sở hữu, đặt ở `tech-specs/<component>/`. Sản phẩm sinh bản L3 ban đầu để review cho repository được phân tích (FR-L3GEN-029 đến 031) |
| Dependency | Architecture claim có hướng giữa hai thực thể kiến trúc, được tổng hợp từ evidence; không tự đồng nghĩa thứ tự thực thi hay mọi hành vi runtime |
| External system | Đích tích hợp bên ngoài application/component, ví dụ HTTP service, datastore hay broker đã xác định đủ để lập quan hệ kiến trúc |
| External library | Gói phụ thuộc được khai báo hoặc có dấu vết sử dụng trong code; không phải external system và không phải component dependency |
| Export artifact | Biểu diễn Markdown, diagram-as-code hoặc JSON được sinh từ cùng architecture model; không phải một lần phân tích độc lập |

## 3a. Cấu trúc bên trong component

Mục này đặt tên cho những gì nằm bên trong một component. Đề bài 3.6 yêu cầu phát hiện chúng nhưng chúng không phải contract. FR-L3GEN-029 ghi chúng ở mục "Cấu trúc component" của README.

| Thuật ngữ | Nghĩa dùng trong hệ thống |
|---|---|
| Module | Một file `.py` |
| Package | Thư mục chứa module. Trong README, module của một component được liệt kê dưới package của nó |
| Vai trò file | Việc một file làm bên trong component, lấy từ dấu hiệu trong code kèm một dòng bằng chứng. Mỗi file đúng một vai trò. Danh sách vai trò, dấu hiệu và thứ tự xét ở FR-L3GEN-029 mục "Cấu trúc component trong README" |
| Điểm vào (vai trò) | Vai trò file: file tạo app, chạy chương trình hoặc khai lệnh dòng lệnh; dấu hiệu như mục "Phạm vi đọc" của FR-L3GEN-028 |
| Route | Vai trò file: file khai route bằng decorator của `FastAPI` hoặc `APIRouter` |
| Schema API | Vai trò file: file khai lớp mà route dùng làm request hoặc response model |
| Cấu hình | Vai trò file: file khai lớp kế thừa `BaseSettings` hoặc đọc `os.environ`, `os.getenv` |
| Model bảng | Vai trò file: file khai model ánh xạ bảng dữ liệu |
| Hạ tầng | Vai trò file: file có dòng tạo engine hoặc client tới hệ thống ngoài |
| Truy cập dữ liệu | Vai trò file: file gọi method trên session CSDL hoặc dựng truy vấn. Đề bài 3.6 gọi là repository/data access |
| Service | Vai trò file: file không mang dấu hiệu của bảy vai trò xét trước nó (thứ tự ở FR-L3GEN-029), nhưng nằm trên đường gọi từ route tới file truy cập dữ liệu hoặc hạ tầng. Luôn mang nhãn `inferred`. Không phải đơn vị triển khai |
| Khác (vai trò) | Vai trò file khi file không mang dấu hiệu nào. Khác với loại component "Khác" (file không có code) |
| Lời gọi HTTP ra ngoài | Lời gọi qua `httpx`, `requests` hoặc `aiohttp` tới một URL. Ghi trong README kèm đích và bằng chứng; không phải contract L3 |

## 4. Nhãn chất lượng và trạng thái

| Thuật ngữ | Nghĩa dùng trong hệ thống |
|---|---|
| exact / inferred | `exact`: đọc trực tiếp từ code fact đã xác định đích, và bước kiểm của code xác nhận được. `inferred`: có code fact làm căn cứ nhưng cần một bước diễn giải, bởi luật đã công bố hoặc bởi mô hình ngôn ngữ, và phải kèm lý do. `inferred` không có nghĩa phỏng đoán không căn cứ |
| full / partial | Biết đủ / còn thiếu thuộc tính hoặc binding trong phạm vi contract đã công bố; không phải mức bao phủ tuyệt đối của repository |
| unresolved / ambiguous | Chưa xác định được đích / có nhiều đích nhưng chưa đủ bằng chứng để chọn |
| runtime-dependent | Kết luận phụ thuộc dữ liệu hoặc hành vi chỉ có khi chạy source; phase đầu không chạy source để xác nhận |
| declared | Operation có trong source nhưng chưa đủ bằng chứng để nói nó được gắn hoặc có thể được thực thi |
| registered candidate | Đã nối được quan hệ đăng ký cha/con/endpoint bằng static evidence, nhưng chưa khẳng định runtime active |
| potentially reachable | Có call/config context tĩnh cho thấy registration có thể được thực hiện; vẫn không phải runtime-confirmed |
| completed / partial / failed | Trạng thái toàn analysis run: đủ artifact bắt buộc / có kết quả dùng được nhưng thiếu phạm vi / không tạo được bộ kết quả hợp lệ |

## 5. Tác nhân tạo kết quả

| Thuật ngữ | Nghĩa dùng trong hệ thống |
|---|---|
| Tầng tất định | Phần không dùng AI: tạo code fact, kiểm evidence của model proposal, ghi limitation và xuất artifact. Cùng snapshot và cùng phiên bản tool thì cho cùng tập code fact |
| Mô hình ngôn ngữ | Phần dùng AI, bắt buộc. Nhận kết quả code đã lần theo (nhóm route, tên dùng chung) kèm các dòng code mang mã; gộp nhóm, đặt tên, viết trách nhiệm và trỏ mã dòng làm bằng chứng. Không nhận toàn bộ source. Chỉ tạo model proposal; không sửa code fact và không tự công bố claim. Provider, model, trần ở NFR-L3GEN-AI-002 |
| Provenance | Thông tin cho biết một claim đến từ đâu: provider, model, phiên bản prompt, phiên bản tool và snapshot. Ghi cho mỗi lần chạy |

`FR`, `AC`, `NFR`, `OBS` và `Baseline` là thuật ngữ quy trình, không phải thuật ngữ miền
sản phẩm. Nghĩa của chúng ở tài liệu quy trình, không lặp lại ở đây.

## 6. Bất biến miền

Các bất biến sau phải giữ dù sau này chọn phương án kiến trúc nào:

1. Một analysis run chỉ đọc một source snapshot; evidence của run không được trỏ sang
   source hiện tại hoặc snapshot khác.
2. Source đầu vào là read-only: không import, chạy, `exec`/`eval`, cài dependency, chạy
   hook/submodule hoặc ghi ngược vào source.
3. Mọi architecture claim công bố phải có evidence. Candidate, unresolved, ambiguous và
   runtime-dependent không được nâng thành semantic edge của lớp mặc định để làm kết quả
   đầy hơn.

   Chúng được phép hiện ra ở một **lớp phủ quan hệ chưa xác minh** mà người dùng chủ động
   bật: lớp này mặc định tắt, vẽ khác hẳn cạnh đã xác minh, và mỗi quan hệ trong đó mang
   nhãn trạng thái cùng lý do chưa kết luận được. Bật lớp phủ không biến chúng thành
   architecture claim: chúng không vào tập cạnh kiến trúc, không tính vào coverage của
   claim, và không xuất hiện khi lớp phủ tắt. Chỉ dùng nét vẽ khác mà không kèm nhãn và
   lý do là vi phạm bất biến này, vì ký hiệu đồ họa rơi mất khi đổi công cụ xem.
4. `Không phát hiện thấy` chỉ hợp lệ khi phạm vi tương ứng đã được xét đầy đủ. Nếu parser,
   adapter, context hoặc budget thiếu, kết quả phải là limitation/partial, không phải rỗng.
5. Confidence của claim, completeness của thuộc tính và coverage của run là ba trục độc
   lập; không dùng một trục thay cho trục khác.
6. CLI và web dùng cùng một engine. Cùng snapshot và cùng phiên bản tool thì cho cùng tập
   code fact. Model proposal có thể khác giữa hai lần chạy; mỗi lần chạy ghi provenance.
   CLI, web và exporter không tự phân tích source theo luật riêng; mọi cấu trúc chúng
   trình bày phải đến từ cùng architecture model của lần chạy đó.
7. Phân tích có thể đi xuống file/class/function/call, nhưng lớp mặc định cho người đọc
   dừng ở application/component theo ADR-2026-001.
8. Mô hình ngôn ngữ chỉ đề xuất. Code lập nhóm route và xếp file; model gộp nhóm và đặt tên,
   không tách nhóm và không thêm cạnh. Một model proposal chỉ thành architecture claim khi
   tầng tất định kiểm được evidence của nó. Model không được sửa code fact, evidence hoặc
   limitation, và không được bỏ qua bước kiểm. Hết quota hoặc lỗi model thì dừng bước
   dùng model, giữ cách chia của code với tên theo đường dẫn, trạng thái partial kèm nguyên
   nhân, không đoán để lấp chỗ trống.
9. Lỗi một file hoặc một adapter không được che mất phần hợp lệ của run; kết quả phải giữ
   phần dùng được và nói chính xác phạm vi đã mất.
10. Khi run dừng vì hết ngân sách thời gian, bộ nhớ hoặc trần tiếp nhận, kết quả phải là
    `partial` kèm phạm vi đã mất và nguyên nhân dừng. Không đánh dấu `completed` cho bộ
    kết quả thiếu phạm vi, và không đánh dấu `failed` khi phần đã xét vẫn dùng được.
11. Vai trò file chỉ lấy từ dấu hiệu trong code, kèm dòng làm bằng chứng. Không suy vai trò
    từ tên file hay tên thư mục. File không mang dấu hiệu nào ghi "Khác".

## 7. Ghi chú về tài liệu thiết kế cũ

Các ý vẫn dùng được từ `SPEC_Code_to_L3_Generator.md` và
`docs/ARCHITECTURE_V2_IDEA.md` là: tách fact/evidence/architecture, phân tích sâu nhưng
trình bày L3, resolver có trạng thái rõ và unresolved không tạo edge. Hai tài liệu đó viết
cho hướng AI tắt; phần "AI chỉ viết mô tả" và "chế độ không AI cho kết quả đầy đủ" không còn
đúng. Các nội dung sau không được mang sang thiết kế phase đầu nếu không có quyết định mới:

- lịch sử nhiều phiên và retention của FR-L3GEN-017 cũ;
- đọc route khai qua `add_api_route` (phase đầu chỉ ghi ở phần giới hạn, FR-L3GEN-029) và resolution động ngoài ma trận phase đầu;
- local folder như đầu vào web hoặc Git/ZIP như đầu vào CLI;
- một schema `IAM` gộp dữ liệu kỹ thuật với public architecture contract;
- pipeline/component split của spec cũ như thể đã qua Architecture Gate.

Key GLOSS và type metadata đang dùng theo tooling cục bộ được chấp nhận tại
OQ-L3GEN-006; chưa tự nhận là registry cấp tổ chức.

