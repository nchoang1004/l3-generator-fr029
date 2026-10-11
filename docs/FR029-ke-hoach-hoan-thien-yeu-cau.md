# FR-029: Kế hoạch hoàn thiện bộ sinh tài liệu

Ngày lập: 11/10/2026. Đây là kế hoạch triển khai, chưa phải quyết định sửa yêu cầu hoặc xác nhận nghiệm thu.

## 1. Mục tiêu và phạm vi

Sinh tài liệu đúng tám AC của [FR-L3GEN-029](../.aide/requirements/fr/FR-L3GEN-029.md). Agent đọc toàn bộ phần source thuộc phạm vi FR-028 và đề xuất dữ kiện. Code kiểm bằng chứng, điều phối và xuất tài liệu.

Đầu vào gồm source, membership và dữ liệu kiến trúc có sẵn. Đầu ra gồm API theo component, README và `result.json`. Không triển khai chia component, dựng sơ đồ, TBL hoặc EVT trong kế hoạch này.

**Kết luận:** tám AC đã đủ xác định sản phẩm cần làm. Cần chốt các tình huống biên, hợp đồng đầu vào và cách đo trước khi tuyên bố đạt. Việc sinh được file chưa chứng minh nội dung đúng.

## 2. Đối chiếu tám yêu cầu

| AC | Sản phẩm phải đáp ứng | Việc cần hoàn thiện | Nhiệm vụ |
|---|---|---|---|
| 01 | Method, path đủ prefix, handler và bằng chứng | Đo thiếu/thừa route; chứng minh chuỗi đăng ký tới app; xử lý router chưa gắn theo quyết định | T01, T03, T08 |
| 02 | Params, body, response, model, field, required, nullable, status | Kiểm nghĩa thuộc tính; body không dùng model; chặn tham số trùng và OpenAPI sai | T04, T05 |
| 03 | Unknown có lý do; inferred có quy tắc | Không gắn exact chỉ vì trích dẫn có thật; phân biệt mức kiểm chứng với nguồn suy luận | T03, T04, T06 |
| 04 | Khớp route và chủ sở hữu với kiến trúc | Dùng hợp đồng upstream thực, cùng snapshot; hiện mới hỗ trợ `archdia-fixture-v1` | T02 |
| 05 | Loại test/ngoài phạm vi; báo route không decorator | Đồng bộ snapshot và reader; mỗi dạng không hỗ trợ có lý do và vị trí | T01, T03 |
| 06 | README đủ mục lục, sơ đồ được cấp, cấu trúc, HTTP, unassigned, giới hạn | Kiểm liên kết và đủ mục; thiếu đầu vào phải ghi chưa đánh giá | T06, T09 |
| 07 | Package/module và vai trò từng file | Phân loại có bằng chứng; không bịa chuỗi gọi giữa các tầng | T06 |
| 08 | HTTP ra ngoài có bằng chứng | Chốt đơn vị đếm wrapper; đối chiếu receiver, method và target | T01, T06, T08 |

## 3. Các quyết định còn mở

Người phụ trách sản phẩm chốt nội dung; người triển khai chuyển quyết định thành test. Các mã OQ tham chiếu hồ sơ làm việc cục bộ, chưa nằm trong gói code này. Chúng vẫn mở; bảng này không tự ban hành quyết định.

| OQ | Cần chốt | Ảnh hưởng |
|---|---|---|
| OQ-L3GEN-013 | Router không gắn app production: giữ route chưa biết path hay đưa vào giới hạn? | Recall route, API, gold |
| OQ-L3GEN-014 | Status phát sinh trong thân handler ghi ở đâu? | Schema status, OpenAPI, gold |
| OQ-L3GEN-015 | Ai duyệt gold nghiệm thu; xử lý repo kín đã dùng chỉnh prompt? | Tính độc lập và tư cách nghiệm thu |
| OQ-L3GEN-016 | HTTP wrapper và lời gọi thư viện bên trong tính một hay hai mục? | Tránh đếm trùng và kết luận thiếu sai |
| OQ-L3GEN-017 | Script chỉ import helper cạnh nó thuộc phạm vi nào? | Snapshot, coverage, mẫu số đo |
| OQ-L3GEN-018 | Bộ kiểm được phân tích sâu tới đâu khi agent vẫn là bên đề xuất? | ADR-2026-006 và ranh giới kiến trúc |

Đề xuất cho OQ-018: code được từ chối, đánh dấu nghi vấn và yêu cầu đọc lại; không tự thêm dữ kiện vào tài liệu. Cần được chốt thành ràng buộc và có test chứng minh trước khi công bố thiết kế đã duyệt.

## 4. Nhiệm vụ triển khai

Các mã Txx chỉ dùng trong kế hoạch này, không thay mã yêu cầu chính thức.

### T01. Khóa phạm vi và tình huống biên

- Phụ trách: sản phẩm cùng người triển khai và người chấm. Làm trước các task phụ thuộc OQ.
- Lập một bảng cho router rời, mount, status trong thân hàm, HTTP wrapper, scripts/examples và route không decorator: đưa vào đâu, bằng chứng nào, đếm thế nào.
- Sau khi quyết định được duyệt, cập nhật FR/ADR/OQ liên quan và phiên bản gold. Không sửa gold chỉ để khớp output hiện tại.
- Hoàn thành khi mỗi tình huống có ví dụ đúng/sai và kỳ vọng kiểm thử, không còn hai cách hiểu trong cùng phiên bản nghiệm thu.

### T02. Chuẩn hóa đầu vào từ FR-028

- Phụ trách: người triển khai FR-029 phối hợp bên sinh kiến trúc. Phụ thuộc hợp đồng upstream.
- Sửa `slice/l3slice/docpipeline.py`: xác thực version, snapshot, component ID, membership và route ID/key. Quy định cách kiểm nguồn của sơ đồ được cấp.
- Thêm fixture đầu vào thực từ FR-028. Kiểm thiếu/thừa route, sai owner, khác snapshot, schema không hỗ trợ và thiếu sơ đồ.
- Hoàn thành khi đối chiếu cùng dữ liệu thực trả đúng passed/failed/not_evaluated; không coi thiếu đầu vào là passed.

### T03. Chứng minh phạm vi đọc và bằng chứng

- Phụ trách: người triển khai. Phụ thuộc T01 cho quy tắc phạm vi.
- Đồng bộ `snapshot.py`, `source_tools.py`, `docfacts.py`: ghi file bị loại và lý do; phân biệt đã gửi cho model, đã xử lý, dòng thiếu và dòng bị cắt.
- Chặn việc lấy nội dung chưa được giao đầy đủ làm bằng chứng đã kiểm chứng. Làm rõ trường hợp thư mục tên `venv` nhưng chứa code dự án.
- Hoàn thành khi đọc phân trang, dòng dài, budget hết và scope loại trừ đều có test; coverage không báo đủ khi còn thiếu/cắt.

### T04. Kiểm đúng nghĩa của params và model

- Phụ trách: người triển khai. Phụ thuộc ranh giới bộ kiểm ở T01.
- Sửa `docfacts.py` và phần schema liên quan: đối chiếu type, required, nullable, alias, default, kế thừa và model lồng nhau; hỗ trợ hoặc ghi giới hạn cho body primitive/container.
- Tách bằng chứng tồn tại khỏi bằng chứng chứng minh thuộc tính. Thuộc tính chưa chứng minh được không được nâng thành exact.
- Hoàn thành khi sửa sai từng thuộc tính trên claim đều bị phát hiện; claim hợp lệ vẫn được giữ. Bao phủ Pydantic v1/v2 trong các phiên bản hỗ trợ.

### T05. Kiểm OpenAPI trước khi xuất

- Phụ trách: người triển khai; người chấm kiểm tra phản ví dụ. Phụ thuộc T04.
- Sửa `render.py` và điểm publish trong `docpipeline.py`: kiểm trùng `(in, name)`, tham số path, response, schema/ref và tính hợp lệ của khối OpenAPI.
- Quyết định cách xuất phần đọc được khi khối OpenAPI không hợp lệ: giữ nội dung cùng thông báo hoặc đánh dấu artifact lỗi. Không để nhãn ready che lỗi định dạng.
- Hoàn thành khi parameter trùng và ref sai không tạo khối OpenAPI invalid mang trạng thái hợp lệ; unknown vẫn xuất đúng giới hạn.

### T06. Kiểm auth, vai trò file và HTTP

- Phụ trách: người triển khai. Phụ thuộc T01 và T03.
- Mỗi mô tả auth phải có bằng chứng đúng nội dung; không suy “public” chỉ vì không thấy dependency.
- Chuỗi route → service → repository phải có cạnh gọi tương ứng; nếu chỉ xác định được vai trò file thì chỉ ghi vai trò.
- Kiểm HTTP receiver, alias, method, target và wrapper theo đơn vị đếm đã chốt. README nêu rõ phần chưa xác định.
- Hoàn thành khi auth bịa, chuỗi gọi bịa và nhầm HTTP client bị từ chối hoặc hạ mức kiểm chứng; đủ mục README và liên kết tới file thực.

### T07. Khóa quy tắc vận hành agent

- Phụ trách: người triển khai. Phụ thuộc T01 và T03.
- Đồng bộ prompt, tool schema, `RULES` và tài liệu theo cùng phiên bản. Chốt số lượt, thời gian, token, retry, điều kiện finish và cách công bố partial.
- Thêm kiểm chứng bộ kiểm không tự tạo route/param/HTTP nếu đây là lựa chọn của OQ-018. Test không có `submit_findings` phải không sinh dữ kiện mới.
- Hoàn thành khi mất provider, hết budget, đọc thiếu và nộp sai đều kết thúc có lý do; không báo completed sai.

### T08. Củng cố golden và bộ chấm

- Phụ trách: người lập gold độc lập, người phản biện và người duyệt. Phụ thuộc T01, T04–T06.
- Đóng phiên bản source commit, dependency, phạm vi, gold và scorer; tách tập chỉnh prompt với tập nghiệm thu.
- Gold phủ cả tám AC: route/params/model/status, nhãn unknown/inferred, owner, loại trừ, README, vai trò file, HTTP. Oracle runtime cần môi trường riêng; không xem kết quả runtime là toàn bộ yêu cầu tài liệu.
- Thêm sai lệch có chủ đích cho từng thuộc tính; đo cả nhận sai và loại nhầm. Giữ kết quả chấm mù trước khi sửa.
- Hoàn thành khi gold có người duyệt và bằng chứng nguồn; bộ chấm bắt được các phản ví dụ đã biết, báo riêng từng nhóm thay vì một điểm tổng che lỗi.

### T09. Giao diện cơ bản và trạng thái kết quả

- Phụ trách: người triển khai. Bản cơ bản đã được thêm trong đợt này ở `docweb.py` và `docui/`.
- Nhập đường dẫn source/membership, tùy chọn kiến trúc; chạy agent nền; xem độ phủ, giới hạn, nội dung và tải tài liệu. Khóa model ở server, không nhập API key trong trình duyệt.
- Hiển thị riêng trạng thái công việc, agent, coverage và parity. Hoàn tất công việc không đồng nghĩa đạt đủ tám AC.
- Kiểm HTTP/API và tương tác DOM; còn cần kiểm trực quan trên trình duyệt ở desktop/mobile. Bản cơ bản chỉ dùng loopback và đường dẫn cục bộ; lịch sử trong phiên server.

### T10. Đo toàn luồng và bàn giao nghiệm thu

- Phụ trách: người chấm độc lập và chủ sản phẩm. Sau T01–T08, dùng T09 nếu nghiệm thu qua UI.
- Chạy model thật trên bộ được duyệt, ghi cấu hình/provider/prompt/code/gold/scorer và budget; đo theo NFR hiện hành. Số đo bộ kiểm offline không thay số đo sản phẩm.
- Ghi từng AC: đạt, không đạt hoặc chưa đánh giá, kèm tài liệu và bằng chứng. Nêu lỗi còn lại, chi phí và thời gian thực đo.
- Hoàn thành khi đủ tám kết luận có bằng chứng và người có trách nhiệm duyệt. Chưa đủ đầu vào hoặc gold chưa duyệt thì chưa công bố đạt FR-029.

## 5. Thứ tự làm và điểm dừng

1. **Đợt 1:** T01, hợp đồng T02 và phản ví dụ tái hiện cho T03–T06. Chốt cách hiểu trước khi thay chuẩn.
2. **Đợt 2:** T03–T05. Ưu tiên nội dung sai đang được coi là đúng và OpenAPI invalid.
3. **Đợt 3:** T06–T07 và tích hợp đầy đủ T02. Khóa ranh giới agent/bộ kiểm.
4. **Đợt 4:** T08 rồi T10. Chỉ công bố số nghiệm thu sau khi gold độc lập được duyệt.

T09 có thể làm song song với các đợt trên vì chỉ trình bày kết quả của pipeline. UI không giải quyết thay các lỗi độ chính xác.

## 6. Trạng thái kiểm chứng của đợt UI

- Đã chạy 9 test backend UI: đều qua, gồm pipeline thật với scripted provider, tải file, lỗi đầu vào, origin và một lần chạy tại một thời điểm.
- Toàn suite Python: 434/435 qua; còn lỗi cũ `test_gateway.Gateway.test_unknown_ids_are_dropped`.
- 4/4 test tương tác DOM qua: sinh/xem/tải/tải lại, lỗi đầu vào, preview an toàn và mất kết nối/kết nối lại. JavaScript qua kiểm tra cú pháp. Phiên này không có trình duyệt kết nối để kiểm bố cục bằng mắt.
- Chưa gọi model trả phí trong đợt này. Kịch bản offline chỉ kiểm luồng chạy, không chứng minh khả năng đọc code của model.
- Các task sửa độ chính xác và quyết định OQ ở trên vẫn là kế hoạch, chưa được thực hiện bởi việc thêm UI.
