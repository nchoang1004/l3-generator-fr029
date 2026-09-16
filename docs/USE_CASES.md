# Use Cases — Code → L3 Generator

Tài liệu này mô tả **người dùng muốn làm gì và nhận được gì**. Cách engine phân tích
source nằm trong [ARCHITECTURE_V2_IDEA.md](ARCHITECTURE_V2_IDEA.md) và
[SPEC](../SPEC_Code_to_L3_Generator.md).

Mục tiêu, KPI và phạm vi sản phẩm nằm trong
[PRD-L3GEN](../.aide/product/prd/PRD-L3GEN.md); tài liệu này chỉ chi tiết hóa hành vi
người dùng ở mức use case.

Use case dưới đây là phạm vi sản phẩm mục tiêu. Một use case có trong tài liệu không
đồng nghĩa code hiện tại đã triển khai đầy đủ.

Sơ đồ tổng quan: [usecase-overview.svg](diagrams/usecase-overview.svg). Khi sơ đồ và
tài liệu này khác nhau, sơ đồ là bản chuẩn.

## 1. Actors

| Actor | Vai trò và nhu cầu |
|---|---|
| **Engineering User** *(actor trừu tượng)* | Nhóm chung của những người cần đọc và kiểm tra kiến trúc từ source code |
| **Developer** | Phân tích codebase chưa quen, tìm application/component và lần theo các quan hệ quan trọng |
| **Architect / Reviewer** | Xem mô hình tổng quát, kiểm tra độ phủ, giới hạn và bằng chứng của từng kết luận |
| **GitHub** *(hệ thống bên ngoài)* | Cung cấp repository khi người dùng nhập URL GitHub |

`Developer` và `Architect / Reviewer` kế thừa các hành vi chung của `Engineering
User`. File ZIP và thư mục cục bộ là **hình thức đầu vào**, không phải actor.

`GitHub` chỉ tham gia đúng một biến thể đầu vào là `Nhập URL GitHub`, không tham gia
mọi lần phân tích. Chọn thư mục cục bộ hoặc tải file ZIP không liên hệ với GitHub.

Hệ thống chỉ đọc source. Hệ thống không chạy source, không sửa source và không ghi
ngược vào repository được phân tích.

## 2. Câu hỏi kiến trúc mà sản phẩm phải trả lời

1. Repository có những application hoặc component nào?
2. Entry point nằm ở đâu?
3. Application/component cung cấp API nào?
4. API hoặc route được component nào xử lý?
5. Component nào phụ thuộc component nào?
6. Component nào đọc hoặc ghi entity/table nào?
7. Component nào gọi hệ thống bên ngoài?
8. Event, queue hoặc configuration quan trọng nào được phát hiện?
9. Phần nào chưa được phân tích hoặc chưa đủ bằng chứng, và vì sao?

Chi tiết function/call chỉ là bằng chứng nội bộ để trả lời các câu hỏi trên. Sản phẩm
không hiển thị toàn bộ function graph như kết quả kiến trúc chính.

## 3. General Use Cases

### UC1 — Phân tích kho mã

| Thuộc tính | Nội dung |
|---|---|
| Actor chính | Developer |
| Actor hỗ trợ | Không có ở mức UC1. `GitHub` chỉ gắn với biến thể `Nhập URL GitHub` |
| Kích hoạt | Developer mở giao diện và cung cấp một nguồn mã |
| Tiền điều kiện | Nguồn mã tồn tại và người dùng có quyền truy cập |
| Kết quả chính | Một lần phân tích có L3, mô hình thành phần, sơ đồ phụ thuộc, bằng chứng và giới hạn |

#### Các cách cung cấp mã nguồn

`Cung cấp mã nguồn` là use case chung, gồm ba biến thể:

1. Chọn thư mục cục bộ.
2. Tải lên file ZIP.
3. Nhập URL GitHub public.

Đây là ba cách bắt đầu cùng một quá trình phân tích, không phải ba quy trình sản phẩm
khác nhau.

#### Luồng chính

1. Developer mở màn hình phân tích kho mã.
2. Developer chọn một trong ba hình thức đầu vào.
3. Hệ thống kiểm tra đầu vào và cho biết phạm vi source sẽ được đọc.
4. Developer bắt đầu phân tích.
5. Hệ thống đọc source bằng static analysis và hiển thị trạng thái xử lý.
6. Hệ thống hoàn thành với kết quả đầy đủ hoặc kết quả một phần có giải thích.
7. Developer được chuyển tới phần tổng quan kiến trúc.

#### Luồng thay thế và lỗi

- Thư mục không đọc được hoặc ZIP không hợp lệ: dừng trước khi phân tích và giải thích
  cách sửa.
- URL GitHub không hợp lệ, không truy cập được hoặc yêu cầu quyền: không coi repository
  là rỗng; hiển thị đúng nguyên nhân.
- Có file lỗi cú pháp: ghi lỗi của file đó và tiếp tục phần còn lại khi an toàn.
- Có ngôn ngữ/framework chưa hỗ trợ: vẫn kiểm kê và công bố phần chưa hỗ trợ.
- Chạm giới hạn xử lý: trả kết quả `partial` cùng lý do, không im lặng cắt dữ liệu.
- Không tìm thấy thành phần kiến trúc: vẫn trả báo cáo phạm vi và giới hạn thay vì một
  kết quả trống gây hiểu nhầm.

### UC2 — Khám phá kiến trúc

| Thuộc tính | Nội dung |
|---|---|
| Actor chính | Engineering User |
| Tiền điều kiện | Có kết quả từ UC1 hoặc một kết quả phân tích đã lưu |
| Kết quả chính | Người dùng hiểu cấu trúc L3 và truy được quan hệ quan trọng |

UC2 gồm năm cách xem. Mỗi cách là một dạng cụ thể của UC2, người dùng chọn cách nào
tùy mục tiêu đang cần:

1. **Xem tổng quan:** application, entry point, component chính và phạm vi phân tích.
2. **Xem ứng dụng và thành phần:** trách nhiệm và dependency giữa các component.
3. **Xem API và luồng yêu cầu:** API/route thuộc component nào và đi qua đâu ở mức L3.
4. **Xem kho dữ liệu và tích hợp:** table/entity, external system, event hoặc queue đã
   được xác định.
5. **Truy vết phụ thuộc:** đi từ một API/component tới component, dữ liệu hoặc hệ thống
   liên quan.

#### Kiểm tra bằng chứng nguồn — hành vi mở rộng

`Kiểm tra bằng chứng nguồn` **không phải cách xem thứ sáu**. Nó mở rộng
(`extend`) `Truy vết phụ thuộc`: khi đang truy vết, người dùng có thể dừng ở một
quan hệ và yêu cầu xem vị trí source cùng đường bằng chứng dẫn tới kết luận đó.

Phân biệt này có hậu quả thực tế:

- Truy vết phụ thuộc hoàn thành được mà người dùng không cần mở bằng chứng.
- Kiểm tra bằng chứng chỉ chạy khi người dùng chủ động yêu cầu, không tự bật.
- Điểm mở rộng là một quan hệ hoặc kết luận đang được chọn trong lúc truy vết.

Diagram mặc định phải tổng quát hóa ở mức application/component. Nó không hiển thị
mọi function, class, biến hoặc raw call.

Ví dụ kết quả mong muốn:

```text
Order API → Order Service → Order Repository → Orders DB
                          └→ Payment Gateway
```

Nếu không đủ bằng chứng, hệ thống dừng ở phần chắc chắn và ghi rõ phần chưa biết. Hệ
thống không tự nối các thành phần chỉ vì tên class, biến hoặc folder có vẻ liên quan.

### UC3 — Xem xét và sử dụng kết quả

| Thuộc tính | Nội dung |
|---|---|
| Actor chính | Engineering User |
| Tiền điều kiện | Có kết quả phân tích |
| Kết quả chính | Người dùng đánh giá được độ tin cậy và lấy được tài liệu cần sử dụng |

#### UC3.1 — Xem kết quả chi tiết

1. Người dùng mở kết quả vừa tạo hoặc chọn một lần phân tích trong lịch sử.
2. Hệ thống hiển thị nội dung L3, component/dependency diagram và các danh sách API,
   dữ liệu, tích hợp hoặc event đã phát hiện.
3. Người dùng xem coverage, file/ngôn ngữ/framework chưa hỗ trợ, lỗi phân tích, kết
   quả `partial`, trường hợp phụ thuộc runtime và các giới hạn khác.
4. Người dùng chọn một kết luận để xem evidence `file:line` khi cần kiểm chứng.

Kết quả phải phân biệt rõ:

- source không có một thành phần;
- hệ thống chưa hỗ trợ hoặc chưa đủ bằng chứng để tìm thành phần đó.

Một raw call chưa resolve không được biến thành cạnh kiến trúc chỉ để diagram đầy hơn.

##### Mở lần phân tích đã lưu

UC3.1 `include` use case `Mở lần phân tích đã lưu`: muốn xem kết quả chi tiết thì trước
hết phải chọn được một lần phân tích để xem, dù đó là lần vừa chạy hay một lần đã lưu.

1. Người dùng mở danh sách các lần phân tích đã lưu.
2. Hệ thống liệt kê theo repository, thời điểm chạy và trạng thái kết quả.
3. Người dùng chọn một lần phân tích.
4. Hệ thống mở đúng kết quả đó cùng phiên bản source đã dùng, để evidence không trỏ
   nhầm sang source hiện tại.

Giới hạn lưu trữ đã chốt trong [PRD-L3GEN](../.aide/product/prd/PRD-L3GEN.md):

- mỗi repository giữ tối đa 10 lần phân tích gần nhất; vượt quá thì loại lần cũ nhất;
- mỗi kết quả hết hạn sau 14 ngày và không còn mở lại được.

#### UC3.2 — Xuất tài liệu kiến trúc

1. Người dùng chọn xuất kết quả.
2. Hệ thống tạo các artifact thuộc phạm vi đã hỗ trợ, gồm L3 Markdown, Diagram-as-Code
   và mô hình kiến trúc có cấu trúc.
3. Các artifact cùng một lần phân tích phải nhất quán về component, quan hệ, bằng
   chứng và giới hạn.

## 4. Quan hệ giữa các use case

Bảng này khớp với [usecase-overview.svg](diagrams/usecase-overview.svg); sơ đồ là bản
chuẩn khi hai bên khác nhau.

| Nguồn | Quan hệ | Đích |
|---|---|---|
| UC1 Phân tích kho mã | `include` | Cung cấp mã nguồn *(abstract)* |
| Chọn thư mục cục bộ | `generalization` | Cung cấp mã nguồn |
| Tải lên file ZIP | `generalization` | Cung cấp mã nguồn |
| Nhập URL GitHub | `generalization` | Cung cấp mã nguồn |
| Xem tổng quan | `generalization` | UC2 Khám phá kiến trúc *(abstract)* |
| Xem ứng dụng và thành phần | `generalization` | UC2 |
| Xem API và luồng yêu cầu | `generalization` | UC2 |
| Xem kho dữ liệu và tích hợp | `generalization` | UC2 |
| Truy vết phụ thuộc | `generalization` | UC2 |
| Kiểm tra bằng chứng nguồn | `extend` | Truy vết phụ thuộc |
| UC3.1 Xem kết quả chi tiết | `generalization` | UC3 *(abstract)* |
| UC3.2 Xuất tài liệu kiến trúc | `generalization` | UC3 |
| UC3.1 Xem kết quả chi tiết | `include` | Mở lần phân tích đã lưu |

Quan hệ giữa actor:

| Nguồn | Quan hệ | Đích |
|---|---|---|
| Developer | `generalization` | Engineering User *(abstract)* |
| Architect / Reviewer | `generalization` | Engineering User |
| Developer | `association` | UC1 Phân tích kho mã |
| Engineering User | `association` | UC2 Khám phá kiến trúc |
| Engineering User | `association` | UC3 Xem xét và sử dụng kết quả |
| GitHub *(external system)* | `association` | Nhập URL GitHub |

AI không có use case riêng. Nếu được dùng để viết mô tả, đó là chi tiết bên trong quá
trình phân tích và không được thay đổi fact, component hoặc relationship.

## 5. Nguyên tắc tổ chức giao diện

Giao diện được tổ chức theo mục tiêu người dùng, không theo từng bước của engine:

- nhìn tổng quan trước;
- đi sâu theo thành phần;
- truy vết về source evidence;
- luôn thấy giới hạn phân tích.

Bốn nguyên tắc này áp cho mọi màn hình kết quả, không riêng một use case.

## 6. Ngoài phạm vi MVP

- Hiểu đầy đủ mọi ngôn ngữ, framework hoặc mọi semantics của Python.
- Resolve chính xác mọi function/method call.
- Vẽ mọi function, class và variable trong diagram L3.
- Chạy, import hoặc dùng `exec` với source đầu vào.
- Tự sửa source hoặc ghi ngược vào repository đầu vào.
- Khẳng định deployment topology khi source/config không đủ.
- Repository Knowledge Graph đầy đủ với graph query/search API.
- Change impact, test impact và incremental analysis.
- AI tự tạo fact, relation, edge hoặc framework rule.
- Quản trị tài khoản người dùng và phân quyền tổ chức trong MVP hiện tại.

Repository GitHub riêng tư nằm ngoài MVP. Hệ thống không yêu cầu hoặc lưu credential
để truy cập repository riêng tư.
