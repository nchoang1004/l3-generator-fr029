# Use Cases — Code → L3 Generator

Tài liệu này mô tả **người dùng muốn làm gì và nhận được gì**. Mục tiêu, KPI và phạm vi
sản phẩm nằm trong [PRD](../.aide/product/prd/PRD-L3GEN-2609-001.md); tài liệu này chỉ
chi tiết hóa hành vi người dùng ở mức use case.

Use case dưới đây là phạm vi sản phẩm mục tiêu. Một use case có trong tài liệu không
đồng nghĩa code hiện tại đã triển khai đầy đủ.

Sơ đồ tổng quan: [usecase-overview.svg](diagrams/usecase-overview.svg). Khi sơ đồ và
tài liệu này khác nhau, sơ đồ là bản chuẩn.

## 1. Hai kênh sử dụng

Sản phẩm có hai kênh, phạm vi khác nhau:

| Kênh | Đầu vào | Làm được gì |
|---|---|---|
| **CLI** | Thư mục cục bộ | Phân tích rồi ghi L3, diagram và JSON ra đĩa |
| **Web UI** | File ZIP, URL GitHub public | Phân tích, khám phá kiến trúc, xem bằng chứng, mở lịch sử, xuất tài liệu |

CLI dừng ở phân tích và xuất file. Nó không cần web server, chạy được khi không có
mạng và khi tắt AI. Đây là điều kiện để dùng công cụ trong môi trường đóng hoặc trong
một bước tự động hóa.

Khám phá kiến trúc, kiểm tra bằng chứng theo từng quan hệ và lịch sử phân tích chỉ có
trên web, vì chúng cần tương tác.

Hai kênh dùng chung một engine phân tích. Cùng một source phải cho cùng kết luận, chỉ
khác cách trình bày.

## 2. Actors

| Actor | Vai trò và nhu cầu |
|---|---|
| **Engineering User** *(trừu tượng)* | Nhóm chung của những người cần đọc và kiểm tra kiến trúc từ source |
| **Developer** | Phân tích codebase chưa quen, tìm application/component và lần theo quan hệ quan trọng |
| **Architect / Reviewer** | Xem mô hình tổng quát, kiểm tra độ phủ, giới hạn và bằng chứng của từng kết luận |
| **CLI** *(kênh)* | Dòng lệnh chạy cục bộ |
| **Web UI** *(kênh)* | Giao diện web |
| **GitHub** *(hệ thống bên ngoài)* | Cung cấp repository khi người dùng nhập URL |

`Developer` và `Architect / Reviewer` kế thừa hành vi chung của `Engineering User`.

Thư mục cục bộ, file ZIP và URL GitHub là **hình thức đầu vào**, không phải actor.

`GitHub` chỉ tham gia đúng một biến thể đầu vào là `Nhập URL GitHub`, không tham gia
mọi lần phân tích.

Hệ thống chỉ đọc source. Hệ thống không chạy source, không sửa source và không ghi
ngược vào repository được phân tích.

## 3. Câu hỏi kiến trúc mà sản phẩm phải trả lời

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
không hiển thị toàn bộ function graph như kết quả kiến trúc chính. Ràng buộc này ở
[NFR-L3GEN-ABST-001](../.aide/requirements/nfr/NFR-L3GEN-ABST-001.md); lý do ở
[ADR-2026-001](../.aide/architecture/adr/ADR-2026-001.md).

## 4. UC1 — Phân tích kho mã

| Thuộc tính | Nội dung |
|---|---|
| Actor chính | Developer |
| Kênh | CLI và Web UI |
| Actor hỗ trợ | `GitHub`, chỉ với biến thể `Nhập URL GitHub` |
| Kích hoạt | Người dùng cung cấp một nguồn mã |
| Tiền điều kiện | Nguồn mã tồn tại và người dùng có quyền truy cập |
| Kết quả chính | Một lần phân tích có L3, mô hình thành phần, sơ đồ phụ thuộc, bằng chứng và giới hạn |

### 4.1 Ba cách cung cấp mã nguồn

`Cung cấp mã nguồn` là use case trừu tượng, có ba biến thể gắn với kênh cụ thể:

| Biến thể | Kênh |
|---|---|
| Chọn thư mục cục bộ | CLI |
| Tải lên file ZIP | Web |
| Nhập URL GitHub public | Web |

Phạm vi phân tích: Python/FastAPI và Java/Spring Boot. Framework Java ngoài Spring Boot
nằm ngoài phạm vi. Chi tiết ở
[NFR-L3GEN-COMP-001](../.aide/requirements/nfr/NFR-L3GEN-COMP-001.md).

Đây là ba cách bắt đầu cùng một quá trình phân tích, không phải ba quy trình sản phẩm
khác nhau.

### 4.2 Luồng chính — Web

1. Developer mở màn hình phân tích và chọn tải ZIP hoặc nhập URL GitHub.
2. Với URL GitHub, hệ thống liên hệ GitHub để lấy source.
3. Hệ thống kiểm tra đầu vào và cho biết phạm vi source sẽ được đọc.
4. Developer bắt đầu phân tích.
5. Hệ thống đọc source bằng phân tích tĩnh và hiển thị trạng thái xử lý.
6. Hệ thống hoàn thành với kết quả đầy đủ, hoặc kết quả một phần có giải thích.
7. Developer được chuyển tới phần tổng quan kiến trúc (UC2).

### 4.3 Luồng chính — CLI

1. Developer chạy lệnh với đường dẫn thư mục source và thư mục output.
2. Hệ thống báo phạm vi đã nhận.
3. Hệ thống phân tích và in tiến trình cùng phần bị bỏ qua.
4. Hệ thống ghi L3, diagram và JSON vào thư mục output rồi kết thúc.
5. Developer mở file kết quả bằng công cụ của mình.

CLI không chuyển sang UC2. Muốn khám phá tương tác thì dùng web.

### 4.4 Luồng thay thế và lỗi

- Thư mục không đọc được hoặc ZIP không hợp lệ: dừng trước khi phân tích và giải thích
  cách sửa.
- URL GitHub không hợp lệ, không truy cập được hoặc yêu cầu quyền: không coi repository
  là rỗng; hiển thị đúng nguyên nhân.
- Mất kết nối khi lấy source GitHub: cho phép thử lại, không tạo kết quả phân tích giả.
- Có file lỗi cú pháp: ghi lỗi của file đó và tiếp tục phần còn lại khi an toàn.
- Có ngôn ngữ/framework chưa hỗ trợ: vẫn kiểm kê và công bố phần chưa hỗ trợ.
- Chạm giới hạn xử lý: trả kết quả `partial` cùng lý do, không im lặng cắt dữ liệu.
- Không tìm thấy thành phần kiến trúc: vẫn trả báo cáo phạm vi và giới hạn thay vì một
  kết quả trống gây hiểu nhầm.

## 5. UC2 — Khám phá kiến trúc

| Thuộc tính | Nội dung |
|---|---|
| Actor chính | Engineering User |
| Kênh | Chỉ Web UI |
| Tiền điều kiện | Có kết quả từ UC1 hoặc một kết quả đã lưu |
| Kết quả chính | Người dùng hiểu cấu trúc L3 và truy được quan hệ quan trọng |

UC2 gồm năm cách xem. Mỗi cách là một dạng cụ thể của UC2:

1. **Xem tổng quan:** application, entry point, component chính và phạm vi phân tích.
2. **Xem ứng dụng và thành phần:** trách nhiệm và dependency giữa các component.
3. **Xem API và luồng yêu cầu:** API/route thuộc component nào và đi qua đâu ở mức L3.
4. **Xem kho dữ liệu và tích hợp:** table/entity, external system, và quan hệ event ở
   phạm vi Kafka gồm producer, consumer, topic. Broker khác Kafka nằm ngoài phạm vi và
   hiện ra ở phần giới hạn, không bị mô tả như repository không có event.
5. **Truy vết phụ thuộc:** đi từ một API/component tới component, dữ liệu hoặc hệ thống
   liên quan.

### 5.1 Kiểm tra bằng chứng nguồn — hành vi mở rộng

`Kiểm tra bằng chứng nguồn` **không phải cách xem thứ sáu**. Nó mở rộng (`extend`)
`Truy vết phụ thuộc`: khi đang truy vết, người dùng có thể dừng ở một quan hệ và yêu
cầu xem vị trí source cùng đường bằng chứng dẫn tới kết luận đó.

Phân biệt này có hậu quả thực tế:

- Truy vết phụ thuộc hoàn thành được mà người dùng không cần mở bằng chứng.
- Kiểm tra bằng chứng chỉ chạy khi người dùng chủ động yêu cầu, không tự bật.
- Điểm mở rộng là một quan hệ hoặc kết luận đang được chọn trong lúc truy vết.

### 5.2 Mức trình bày

Diagram mặc định tổng quát hóa ở mức application/component. Nó không hiển thị mọi
function, class, biến hoặc raw call.

Ví dụ kết quả mong muốn:

```text
Order API → Order Service → Order Repository → Orders DB
                          └→ Payment Gateway
```

Nếu không đủ bằng chứng, hệ thống dừng ở phần chắc chắn và ghi rõ phần chưa biết. Hệ
thống không tự nối các thành phần chỉ vì tên class, biến hoặc folder có vẻ liên quan.

## 6. UC3 — Xem xét và sử dụng kết quả

| Thuộc tính | Nội dung |
|---|---|
| Actor chính | Engineering User |
| Kênh | UC3.1 chỉ web; UC3.2 cả hai kênh |
| Tiền điều kiện | Có kết quả phân tích |
| Kết quả chính | Người dùng đánh giá được độ tin cậy và lấy được tài liệu cần sử dụng |

### 6.1 UC3.1 — Xem kết quả chi tiết *(chỉ web)*

1. Người dùng mở kết quả vừa tạo hoặc chọn một lần phân tích trong lịch sử.
2. Hệ thống hiển thị nội dung L3, component/dependency diagram và các danh sách API,
   dữ liệu, tích hợp hoặc event đã phát hiện.
3. Người dùng xem coverage, file/ngôn ngữ/framework chưa hỗ trợ, lỗi phân tích, kết
   quả `partial`, trường hợp phụ thuộc runtime và các giới hạn khác.
4. Người dùng chọn một kết luận để xem evidence `file:line` khi cần kiểm chứng.

Kết quả phải phân biệt rõ hai trường hợp:

- source không có một thành phần;
- hệ thống chưa hỗ trợ hoặc chưa đủ bằng chứng để tìm thành phần đó.

Một raw call chưa resolve không được biến thành cạnh kiến trúc chỉ để diagram đầy hơn.

#### Mở lần phân tích đã lưu

UC3.1 `include` use case `Mở lần phân tích đã lưu`: muốn xem kết quả chi tiết thì trước
hết phải chọn được một lần phân tích để xem, dù đó là lần vừa chạy hay một lần đã lưu.

1. Người dùng mở danh sách các lần phân tích đã lưu.
2. Hệ thống liệt kê theo repository, thời điểm chạy và trạng thái kết quả.
3. Người dùng chọn một lần phân tích.
4. Hệ thống mở đúng kết quả đó cùng phiên bản source đã dùng, để evidence không trỏ
   nhầm sang source hiện tại.

Giới hạn lưu trữ theo [NFR-L3GEN-PRIV-001](../.aide/requirements/nfr/NFR-L3GEN-PRIV-001.md)
và AC-L3GEN-017-05/06:

- mỗi repository giữ tối đa 10 lần phân tích gần nhất; vượt quá thì loại lần cũ nhất;
- mỗi kết quả hết hạn sau 14 ngày và không còn mở lại được;
- người dùng xóa thủ công một kết quả trước hạn, có bước xác nhận.

Lịch sử là tính năng của web. CLI ghi kết quả ra thư mục output và người dùng tự quản
lý các thư mục đó.

### 6.2 UC3.2 — Xuất tài liệu kiến trúc *(cả hai kênh)*

1. Người dùng yêu cầu xuất kết quả: trên web là một thao tác, trên CLI là kết quả mặc
   định của lần chạy.
2. Hệ thống tạo các artifact thuộc phạm vi đã hỗ trợ, gồm L3 Markdown, Diagram-as-Code
   và mô hình kiến trúc có cấu trúc.
3. Các artifact cùng một lần phân tích phải nhất quán về component, quan hệ, bằng
   chứng và giới hạn.

## 7. Quan hệ giữa các use case

Bảng này khớp với [usecase-overview.svg](diagrams/usecase-overview.svg); sơ đồ là bản
chuẩn khi hai bên khác nhau.

| Nguồn | Quan hệ | Đích |
|---|---|---|
| UC1 Phân tích kho mã | `include` | Cung cấp mã nguồn *(abstract)* |
| Chọn thư mục cục bộ | `generalization` | Cung cấp mã nguồn |
| Tải lên file ZIP | `generalization` | Cung cấp mã nguồn |
| Nhập URL GitHub | `generalization` | Cung cấp mã nguồn |
| Báo giới hạn phân tích | `extend` | UC1 Phân tích kho mã |
| Xem tổng quan | `generalization` | UC2 Khám phá kiến trúc *(abstract)* |
| Xem ứng dụng và thành phần | `generalization` | UC2 |
| Xem API và luồng yêu cầu | `generalization` | UC2 |
| Xem kho dữ liệu và tích hợp | `generalization` | UC2 |
| Truy vết phụ thuộc | `generalization` | UC2 |
| Kiểm tra bằng chứng nguồn | `extend` | Truy vết phụ thuộc |
| UC3.1 Xem kết quả chi tiết | `generalization` | UC3 *(abstract)* |
| UC3.2 Xuất tài liệu kiến trúc | `generalization` | UC3 |
| UC3.1 Xem kết quả chi tiết | `include` | Mở lần phân tích đã lưu |

Quan hệ giữa actor và use case:

| Nguồn | Quan hệ | Đích |
|---|---|---|
| Developer | `generalization` | Engineering User *(abstract)* |
| Architect / Reviewer | `generalization` | Engineering User |
| CLI | `association` | UC1 Phân tích kho mã |
| CLI | `association` | UC3.2 Xuất tài liệu kiến trúc |
| Web UI | `association` | UC1 Phân tích kho mã |
| Engineering User | `association` | UC2 Khám phá kiến trúc |
| Engineering User | `association` | UC3 Xem xét và sử dụng kết quả |
| GitHub *(external system)* | `association` | Nhập URL GitHub |

CLI không liên kết với UC2 và UC3.1. Đây là ranh giới có chủ ý, không phải thiếu sót
của sơ đồ.

AI không có use case riêng. Nếu được dùng để viết mô tả, đó là chi tiết bên trong quá
trình phân tích và không được thay đổi fact, component hoặc relationship.

## 8. Nguyên tắc tổ chức giao diện

Giao diện web được tổ chức theo mục tiêu người dùng, không theo từng bước của engine:

- nhìn tổng quan trước;
- đi sâu theo thành phần;
- truy vết về source evidence;
- luôn thấy giới hạn phân tích.

Bốn nguyên tắc này áp cho mọi màn hình kết quả, không riêng một use case.

CLI theo nguyên tắc khác: mọi thứ người dùng cần biết phải nằm trong output của lần
chạy, vì không có màn hình nào để quay lại xem.

## 9. Ngoài phạm vi

- Hiểu đầy đủ mọi ngôn ngữ, framework hoặc mọi semantics của Python và Java. Framework
  Java ngoài Spring Boot nằm ngoài phạm vi.
- Message broker khác Kafka trong repository đầu vào, ví dụ RabbitMQ, Celery hoặc SQS.
- Resolve chính xác mọi function/method call.
- Vẽ mọi function, class và variable trong diagram L3.
- Chạy, import hoặc dùng `exec` với source đầu vào.
- Tự sửa source hoặc ghi ngược vào repository đầu vào.
- Khẳng định deployment topology khi source/config không đủ.
- Repository Knowledge Graph đầy đủ với graph query/search API.
- Change impact, test impact và incremental analysis.
- AI tự tạo fact, relation, edge hoặc framework rule.
- Khám phá kiến trúc tương tác và lịch sử phân tích trên CLI.
- Quản trị tài khoản người dùng và phân quyền tổ chức.

Repository GitHub riêng tư nằm ngoài phạm vi. Hệ thống không yêu cầu hoặc lưu
credential để truy cập repository riêng tư.
