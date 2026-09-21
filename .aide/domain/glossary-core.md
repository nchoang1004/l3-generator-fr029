---
uid: "01M2J06Z3HXPW1MKV9XBWJR7YW"
key: "GLOSS-L3GEN-001"
type: "glossary"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "approved"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: 2026-09-21
verified_against: []
classification: "internal"
ai_assisted: true
---

# Thuật ngữ và bất biến miền sản phẩm

Tài liệu này thống nhất cách gọi trước khi chia capability và component. Nó không chọn
pipeline, framework triển khai hay thứ tự chạy. Khi một ghi chép thiết kế cũ dùng từ khác
với tài liệu này, nghĩa trong baseline yêu cầu và tài liệu này được ưu tiên.

## 1. Nguồn và lần phân tích

| Thuật ngữ | Nghĩa dùng trong hệ thống |
|---|---|
| Repository | Tập source và cấu hình được người dùng cung cấp để phân tích. Repository có thể chứa nhiều application, mã dùng chung và phần ngoài stack hỗ trợ |
| Source snapshot | Nội dung đầu vào bất biến của một lần phân tích, có content digest; Git commit/ref chỉ là metadata bổ sung và không thay thế digest |
| Analysis run | Một lần engine xử lý đúng một source snapshot với một bộ cấu hình, tool version và rule version xác định |
| Analysis unit | Phần source được kiểm kê và phân tích chung. Manifest, source root, entry point và cấu trúc thư mục là evidence để xác định phạm vi, không tự chứng minh deployment boundary |
| Application | Điểm hợp thành/chạy ứng dụng được framework hoặc cấu hình hỗ trợ chứng minh. Một analysis unit có thể có không, một hoặc nhiều application |
| Service | Đơn vị triển khai chỉ khi có bằng chứng phù hợp. Khi chưa đủ bằng chứng, sản phẩm phải dùng `analysis unit` hoặc boundary candidate, không gọi chắc chắn là service |
| Entry point | Vị trí source/config có bằng chứng khởi tạo hoặc cấu hình application; không đồng nghĩa mọi code từ đó chắc chắn đã chạy |

## 2. Dữ kiện, kết luận và bằng chứng

| Thuật ngữ | Nghĩa dùng trong hệ thống |
|---|---|
| Code fact | Quan sát tất định từ source hoặc manifest, ví dụ import, definition, decorator, call hay dependency declaration; chưa mặc nhiên là kết luận kiến trúc |
| Candidate | Đối tượng hoặc quan hệ có tín hiệu ban đầu nhưng chưa đủ điều kiện để công bố thành architecture claim |
| Resolution result | Kết quả nối một tham chiếu/call tới một đích: `resolved`, `ambiguous`, `unresolved` hoặc `runtime-dependent` |
| Architecture claim | Thực thể hoặc quan hệ ở mức application/component được công bố trong architecture model |
| Evidence | Một hoặc nhiều file/range thuộc chính source snapshot, kèm rule/reason và đường suy luận khi cần, hỗ trợ một fact hoặc claim |
| Diagnostic | Dữ liệu giải thích quá trình phân tích, candidate, raw call, budget hoặc nguyên nhân không kết luận được; không phải architecture claim |
| Limitation | Phần engine không đọc, không hỗ trợ, không resolve hoặc phải dừng do budget/runtime; không đồng nghĩa repository không có dữ kiện đó |
| Coverage | Bản kê phần đã xét, bị loại, lỗi hoặc ngoài phạm vi. Coverage mô tả phạm vi quan sát, không phải confidence của từng claim |
| Finding | Cảnh báo tất định cần xác minh, có evidence; không phải kết luận lỗi nghiệp vụ hay lỗ hổng bảo mật |

## 3. Mô hình kiến trúc và mức trình bày

| Thuật ngữ | Nghĩa dùng trong hệ thống |
|---|---|
| Component | Nhóm thành viên code có cùng trách nhiệm kiến trúc, được tạo bởi rule grouping công bố và có evidence membership; tên thư mục hoặc tên class riêng lẻ không đủ chứng minh |
| Component role | Nhãn như API, service/business, repository/data-access hoặc integration dựa trên framework marker, registration hay effect đã hỗ trợ; khi thiếu bằng chứng dùng unknown/candidate |
| Architecture model | Tập application, component, interface, data, external system, event, configuration và quan hệ L3; đây là nguồn cấu trúc chung cho CLI, web và artifact xuất |
| Evidence/diagnostic model | Dữ kiện chi tiết mức file/class/function/call dùng để kiểm chứng hoặc chẩn đoán; không được UI/diagram coi là lớp kiến trúc mặc định |
| IAM | Tên lịch sử của mô hình trung gian. Trong thiết kế mới phải nói rõ đang chỉ architecture model hay evidence/diagnostic model; không dùng `IAM` như một schema gộp mơ hồ cả hai |
| L3 | Trong sản phẩm này: mô tả cấu trúc bên trong application/service ở mức component, interface, data, config, event và dependency; là bản ban đầu để review, không tuyên bố chứng nhận C4 |
| Dependency | Architecture claim có hướng giữa hai thực thể kiến trúc, được tổng hợp từ evidence; không tự đồng nghĩa thứ tự thực thi hay mọi hành vi runtime |
| External system | Đích tích hợp bên ngoài application/component, ví dụ HTTP service, datastore hay broker đã xác định đủ để lập quan hệ kiến trúc |
| External library | Gói phụ thuộc được khai báo hoặc có dấu vết sử dụng trong code; không phải external system và không phải component dependency |
| Export artifact | Biểu diễn Markdown, diagram-as-code hoặc JSON được sinh từ cùng architecture model; không phải một lần phân tích độc lập |

## 4. Nhãn chất lượng và trạng thái

| Thuật ngữ | Nghĩa dùng trong hệ thống |
|---|---|
| exact / inferred | Claim/thuộc tính đọc trực tiếp từ bằng chứng / suy bằng rule tất định đã công bố. `inferred` không có nghĩa phỏng đoán tự do |
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
| Deterministic core | Phần tạo code fact, architecture claim, evidence, limitation, finding và artifact cấu trúc mà không phụ thuộc AI |
| AI description | Văn bản tùy chọn, có nhãn, chỉ diễn đạt dữ kiện/finding đã có; không có quyền sửa hoặc bổ sung cấu trúc |

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
6. Cùng snapshot, cấu hình, tool version và rule version phải cho cùng deterministic core
   qua CLI và web. Run metadata và cách trình bày có thể khác theo contract. Hệ quả bắt
   buộc: CLI, web và exporter không tự phân tích source theo luật riêng; mọi cấu trúc
   chúng trình bày phải đến từ cùng architecture model.
7. Phân tích có thể đi xuống file/class/function/call, nhưng lớp mặc định cho người đọc
   dừng ở application/component theo ADR-2026-001.
8. AI mặc định tắt trong phase đầu. Khi được người dùng bật, AI không được thay đổi code
   fact, architecture claim, evidence, limitation, finding ID hoặc artifact cấu trúc.
9. Lỗi một file hoặc một adapter không được che mất phần hợp lệ của run; kết quả phải giữ
   phần dùng được và nói chính xác phạm vi đã mất.
10. Khi run dừng vì hết ngân sách thời gian, bộ nhớ hoặc trần tiếp nhận, kết quả phải là
    `partial` kèm phạm vi đã mất và nguyên nhân dừng. Không đánh dấu `completed` cho bộ
    kết quả thiếu phạm vi, và không đánh dấu `failed` khi phần đã xét vẫn dùng được.

## 7. Ghi chú về tài liệu thiết kế cũ

Các ý vẫn dùng được từ `SPEC_Code_to_L3_Generator.md` và
`docs/ARCHITECTURE_V2_IDEA.md` là: tách fact/evidence/architecture, phân tích sâu nhưng
trình bày L3, resolver có trạng thái rõ, framework rule tất định và unresolved không tạo
edge. Các nội dung sau không được mang sang thiết kế phase đầu nếu không có quyết định mới:

- lịch sử nhiều phiên và retention của FR-L3GEN-017;
- SQLModel, `mapped_column`, `add_api_route` và resolution động ngoài ma trận phase đầu;
- local folder như đầu vào web hoặc Git/ZIP như đầu vào CLI;
- một schema `IAM` gộp dữ liệu kỹ thuật với public architecture contract;
- pipeline/component split của spec cũ như thể đã qua Architecture Gate.

Key GLOSS và type metadata đang dùng theo tooling cục bộ được chấp nhận tại
OQ-L3GEN-006; chưa tự nhận là registry cấp tổ chức.

