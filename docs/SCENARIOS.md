# Scenarios — Code → L3 Generator

Các scenario dưới đây là tiêu chí hành vi, không phải số đo thực tế. Chúng tập trung
vào mức L3; chi tiết function/call chỉ xuất hiện khi cần làm evidence.

Use case liên quan: [USE_CASES.md](USE_CASES.md). Mỗi scenario ghi use case mà nó kiểm
chứng; bảng đối chiếu đầy đủ ở cuối tài liệu.

Sản phẩm có hai kênh với phạm vi khác nhau: dòng lệnh nhận thư mục cục bộ rồi phân
tích và ghi file; giao diện web nhận ZIP hoặc URL GitHub và cho khám phá kiến trúc.
Mỗi scenario ghi rõ nó thuộc kênh nào.

## Scenario 1a — Hiểu một service chưa quen, qua giao diện web

*UC1 Phân tích kho mã · UC2 Khám phá kiến trúc*

**Tiền điều kiện:** repository có application FastAPI, route, service, repository,
SQLAlchemy entity và một external HTTP call.

**Luồng:**

1. Developer mở màn hình phân tích kho mã và tải lên file ZIP của repository.
2. Hệ thống kiểm tra đầu vào và cho biết phạm vi source sẽ được đọc.
3. Developer bắt đầu phân tích; hệ thống hiển thị trạng thái xử lý.
4. Hệ thống hoàn thành và chuyển Developer tới phần tổng quan kiến trúc.
5. Developer thấy trong kết quả:
   - application/entry point;
   - các component chính;
   - bảng route;
   - data entity/table;
   - external system;
   - dependency giữa các component;
   - coverage và limitations.
6. Developer mở diagram và thấy mô hình tổng quát:

```text
Order API → Order Service → Order Repository → Orders DB
                          └→ Payment Gateway
```

**Kết quả mong đợi:** Developer nắm được cấu trúc mà không phải xem một node cho từng
function. Mỗi quan hệ có thể drill-down về source.

## Scenario 1b — Cùng repository, chạy bằng dòng lệnh

*UC1 Phân tích kho mã · UC3.2 Xuất tài liệu — kênh CLI*

**Tiền điều kiện:** repository nằm trong một thư mục cục bộ. Không có mạng, không có
API key.

**Luồng:**

1. Developer chạy `l3gen <repo> --no-ai -o out`.
2. Tool kiểm kê source và báo phần được/không được hỗ trợ.
3. Tool sinh L3, diagram và architecture model vào thư mục `out` rồi kết thúc.
4. Developer mở file kết quả bằng công cụ của mình.

**Kết quả mong đợi:** cùng một repository cho cùng kết quả phân tích dù chạy qua giao
diện hay dòng lệnh. Dòng lệnh không có thêm hoặc bớt component, quan hệ và limitation
so với Scenario 1a.

CLI dừng ở đây. Nó không có màn hình khám phá, không có drill-down theo từng quan hệ
và không lưu lịch sử phân tích. Người dùng cần các thứ đó thì dùng web.

## Scenario 1c — Ba hình thức cung cấp mã nguồn

*UC1 Phân tích kho mã · biến thể Chọn thư mục / Tải ZIP / Nhập URL GitHub*

Ba hình thức đầu vào bắt đầu cùng một quá trình phân tích. Sau khi source được chấp
nhận, kết quả không phụ thuộc vào cách nguồn được cung cấp hay kênh nào đã nhận nó.

**Luồng thư mục cục bộ — CLI:** Developer truyền đường dẫn thư mục; tool báo phạm vi
source sẽ đọc.

**Luồng ZIP — web:** Developer tải lên file ZIP; hệ thống giải nén trong vùng xử lý
riêng rồi báo phạm vi source.

**Luồng GitHub — web:** Developer nhập URL GitHub public; hệ thống liên hệ GitHub, lấy
source và báo phạm vi cùng phiên bản source đã dùng.

**Luồng thay thế và lỗi:**

| Tình huống | Hành vi mong đợi |
|---|---|
| Thư mục không tồn tại hoặc không đọc được | Dừng trước khi phân tích; chỉ rõ đường dẫn hoặc quyền cần sửa |
| ZIP hỏng hoặc sai định dạng | Từ chối an toàn; không giải nén ra ngoài vùng xử lý |
| ZIP chứa đường dẫn thoát khỏi thư mục giải nén | Từ chối; không ghi file ra ngoài vùng xử lý |
| URL GitHub sai hoặc repository không tồn tại | Báo lỗi nhập/truy cập; không hiển thị như repository rỗng |
| Repository GitHub yêu cầu quyền | Nói rõ chưa có quyền; không yêu cầu người dùng cung cấp credential |
| Mất kết nối khi đang lấy source GitHub | Cho phép thử lại; không tạo kết quả phân tích giả |

**Kết quả mong đợi:** lỗi đầu vào được phân biệt rõ với kết quả phân tích rỗng. Không
trường hợp nào tạo ra một lần phân tích trống mà không giải thích nguyên nhân.

## Scenario 1d — Lỗi riêng của dòng lệnh

*UC1 Phân tích kho mã — kênh CLI*

Các tình huống này chỉ xảy ra ở CLI, vì CLI nhận đường dẫn trên máy người dùng và tự
ghi file ra đĩa.

| Tình huống | Hành vi mong đợi |
|---|---|
| Đường dẫn source không tồn tại | Dừng ngay, in đường dẫn đã nhận; không tạo thư mục output |
| Không có quyền đọc source | Dừng và nói rõ là vấn đề quyền, không phải repository rỗng |
| Đường dẫn source là file, không phải thư mục | Báo sai kiểu đầu vào; không cố phân tích một file đơn lẻ như cả repository |
| Thư mục output đã tồn tại và có kết quả cũ | Không ghi đè im lặng; hoặc từ chối, hoặc yêu cầu người dùng xác nhận |
| Không có quyền ghi vào thư mục output | Dừng **trước khi** phân tích, không để chạy xong rồi mới hỏng ở bước ghi |
| Source nằm trong chính thư mục output | Từ chối; không để công cụ đọc lại kết quả của chính nó |
| Tiến trình bị ngắt giữa chừng | Không để lại thư mục output có vẻ hoàn chỉnh nhưng thiếu artifact |

**Kết quả mong đợi:** mọi lỗi được phát hiện sớm nhất có thể. Công cụ không phá source
đầu vào và không phá kết quả của lần chạy trước.

## Scenario 2 — Theo route tới database

Source rút gọn:

```python
@router.post("/orders")
def create_order(service: OrderService = Depends(get_service)):
    return service.create()
```

```python
class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create(self):
        return self.repository.save(Order())
```

**Luồng:**

1. Tool nhận route là architectural anchor.
2. Resolver lần theo dependency, parameter, attribute và call có liên quan.
3. Adapter/entity extractor xác nhận repository/entity theo rule đã hỗ trợ.
4. Component synthesis tạo quan hệ ở mức L3.
5. L3 hiển thị route → Order Service → Order Repository → orders table.
6. Evidence ghi các `file:line` tạo nên chuỗi trên.

**Kết quả mong đợi:** phân tích chi tiết được dùng để chứng minh quan hệ, nhưng diagram
không vẽ riêng `get_service`, `__init__`, `create` và `save`.

**Luồng thay thế:** nếu `get_service` phụ thuộc runtime và không xác định được
repository, kết quả dừng ở Order Service, ghi partial và lý do; không tự nối tới bảng.

## Scenario 3 — Kiểm chứng một dependency

*UC2 Truy vết phụ thuộc · `extend` Kiểm tra bằng chứng nguồn*

1. Reviewer đang truy vết phụ thuộc và thấy `Order Service → Payment Gateway`.
2. Reviewer chọn quan hệ này và yêu cầu xem bằng chứng.
3. Evidence chỉ ra route/handler hoặc component call tới HTTP client cùng URL/host và
   vị trí source.
4. Reviewer mở source tại vị trí đó.
5. Reviewer xác nhận kết luận hoặc phát hiện rule cần sửa.

**Kết quả mong đợi:** người đọc không phải tin mô tả AI. Description không được dùng
làm evidence.

**Luồng thay thế:** Reviewer truy vết xong chuỗi phụ thuộc mà không mở bằng chứng lần
nào. Việc truy vết vẫn hoàn thành; kiểm tra bằng chứng chỉ chạy khi được yêu cầu.

## Scenario 4 — Repo phẳng hoặc trộn ngôn ngữ

Repository:

```text
repo/
├── api.py
├── PaymentService.java
├── worker.py
└── ui.ts
```

**Luồng:**

1. Inventory ghi nhận từng file theo ngôn ngữ, không chọn ngôn ngữ theo folder hoặc
   số đông.
2. Python frontend phân tích file Python.
3. Java/TypeScript được ghi nhận nhưng đánh dấu unsupported nếu chưa có frontend.
4. Output nói rõ coverage.
5. Không có application/service nào được kết luận chỉ từ tên folder.

**Kết quả mong đợi:** phần hỗ trợ được không bị bỏ mất; phần chưa hỗ trợ không bị mô tả
như “không tồn tại”.

## Scenario 5 — Hai source root có module trùng tên

Repository:

```text
repo/
├── public/src/app/main.py
└── admin/src/app/main.py
```

Cả hai file đều có thể mang tên module `app.main` trong môi trường riêng.

**Luồng:**

1. Inventory giữ đường dẫn file độc lập.
2. Analysis Context cố xác định source root từ config/manifest đã hỗ trợ.
3. Nếu xác định được, mỗi import resolve trong root tương ứng.
4. Nếu chưa xác định được, resolver giữ hai namespace riêng và báo nhập nhằng.
5. Tool không gộp route của public/admin vào cùng application chỉ vì module trùng tên.

**Kết quả mong đợi:** an toàn trước kết luận sai; output có thể partial nhưng không
trộn hai application.

## Scenario 6 — Method trùng tên framework

```python
disk_manager.mount("/dev/sdb")
```

**Luồng:**

1. Frontend ghi raw call.
2. Resolver xác định receiver là `DiskManager`, hoặc để unresolved nếu thiếu dữ liệu.
3. FastAPI/Starlette adapter không khớp symbol này.
4. Architecture graph không có cạnh `mounts application`.
5. Nếu unresolved, call xuất hiện trong diagnostics/limitations chứ không thành cạnh
   kiến trúc nét đứt.

**Kết quả mong đợi:** không báo sai framework operation chỉ vì method cùng tên.

## Scenario 7 — Registration có điều kiện hoặc chưa được gọi

```python
app = FastAPI()

def setup():
    app.add_api_route("/orders", handler)
```

**Luồng:**

1. Adapter nhận ra câu lệnh có dạng RegisterEndpoint.
2. Engine ghi nó là declared operation.
3. Engine tìm call context của `setup`.
4. Nếu không thấy `setup()` được gọi, route không được khẳng định là active.
5. L3 ghi declared/conditional hoặc limitation với evidence.

Biến thể:

```python
if settings.ENABLE_ADMIN:
    app.include_router(admin_router)
```

Route giữ điều kiện `settings.ENABLE_ADMIN`; không mô tả nó tồn tại trong mọi môi
trường.

## Scenario 8 — Hai application cùng framework

```python
public_app = FastAPI()
admin_app = FastAPI()

public_app.include_router(public_router)
admin_app.include_router(admin_router)
```

**Kết quả mong đợi:**

- có hai application object riêng;
- public route không bị gắn vào admin app và ngược lại;
- component/diagram có thể nhóm theo hai application boundary candidate;
- cùng type `FastAPI` không có nghĩa cùng object.

## Scenario 9 — Runtime-dependent call

```python
handler_name = config["handler"]
handler = getattr(module, handler_name)
handler()
```

**Kết quả mong đợi:**

- trạng thái `runtime`;
- lý do nói đích phụ thuộc configuration;
- có evidence `file:line`;
- không chọn một handler tùy ý;
- không sinh architecture edge từ call này nếu chưa biết loại relation.

## Scenario 10 — Chạy không có AI

*UC1 Phân tích kho mã · UC3.2 Xuất tài liệu — cả hai kênh*

**Trên CLI:**

1. Developer không đặt API key hoặc dùng `--no-ai`.
2. Phân tích tĩnh vẫn chạy, không có kết nối ra ngoài.
3. L3, diagram, evidence và architecture graph vẫn được sinh.

**Trên web:**

1. Người dùng để AI ở trạng thái tắt, là mặc định.
2. Giao diện cho biết AI đang tắt và dữ liệu nào không được gửi đi đâu.
3. Phân tích và khám phá kiến trúc vẫn dùng được đầy đủ.

**Kết quả mong đợi chung:**

- Output chỉ thiếu phần mô tả do AI viết.
- Số route, component, entity và dependency không thay đổi vì tắt AI.
- Không kênh nào coi việc không có AI là lỗi hoặc là kết quả một phần.

## Scenario 11 — Graph kỹ thuật không tràn vào diagram L3

Giả sử repository có 500 function nhưng chỉ có:

- 2 application;
- 6 component;
- 20 route;
- 4 table;
- 3 external system.

**Kết quả mong đợi:**

- IR/evidence có thể chứa function cần thiết;
- public architecture graph chỉ chứa node/cạnh thuộc contract L3;
- diagram ưu tiên 2 application, 6 component và dependency quan trọng;
- không đưa 500 function vào diagram;
- bảng route chi tiết vẫn có đủ 20 route.

## Scenario 12 — Mở lại một lần phân tích đã lưu

*UC3.1 Xem kết quả chi tiết · `include` Mở lần phân tích đã lưu — chỉ web*

Hệ thống giữ tối đa 10 lần phân tích cho mỗi repository; mỗi kết quả hết hạn sau 14
ngày. Người dùng xóa thủ công được một kết quả trước hạn.

Lịch sử là tính năng của giao diện web. CLI ghi kết quả ra thư mục output và người
dùng tự quản lý các thư mục đó.

**Luồng:**

1. Người dùng mở danh sách các lần phân tích đã lưu.
2. Người dùng chọn một lần phân tích theo repository và thời điểm chạy.
3. Hệ thống mở đúng kết quả đó, gồm mô hình, evidence và limitations của lần chạy ấy.
4. Kết quả ghi rõ phiên bản source đã dùng để evidence không trỏ nhầm.

**Luồng thay thế:**

| Tình huống | Hành vi mong đợi |
|---|---|
| Repository đã có 10 lần phân tích, người dùng chạy lần thứ 11 | Giữ 10 kết quả gần nhất, loại kết quả cũ nhất |
| Kết quả đã quá 14 ngày | Không còn mở lại được; nói rõ lý do hết hạn |
| Source đã thay đổi sau lần phân tích | Kết quả vẫn là snapshot của lần chạy cũ, không tự cập nhật theo source mới |
| Người dùng xóa thủ công một kết quả | Hỏi xác nhận trước khi xóa; xóa xong không mở lại được và không ảnh hưởng các lần khác |

**Kết quả mong đợi:** mở lại kết quả cũ cho đúng nội dung tại thời điểm chạy. Hệ thống
không trộn kết quả cũ với source hiện tại.

## Scenario 13 — Xuất tài liệu kiến trúc

*UC3.2 Xuất tài liệu kiến trúc — cả hai kênh*

**Luồng:**

1. Người dùng yêu cầu xuất kết quả của một lần phân tích: trên web là một thao tác,
   trên CLI là kết quả mặc định của lần chạy.
2. Hệ thống tạo L3 Markdown, Diagram-as-Code và architecture model có cấu trúc.
3. Các artifact được tạo từ cùng một analysis result.

**Kết quả mong đợi:** artifact xuất ra và nội dung trên giao diện nhất quán về
component, quan hệ, evidence và limitation. Không có quan hệ nào chỉ xuất hiện ở một
trong hai nơi.

**Luồng thay thế:** nếu một artifact tạo thất bại, analysis result được giữ nguyên, hệ
thống báo rõ artifact nào thất bại và cho phép thử lại.

## Scenario 14 — Hai kênh cho cùng một kết quả

*UC1 Phân tích kho mã · UC3.2 Xuất tài liệu — cả hai kênh*

Đây là scenario chứng minh hai kênh dùng chung một engine. Scenario 1b chỉ phát biểu
điều đó; scenario này kiểm chứng nó.

**Tiền điều kiện:** một repository đã pin ở một commit cụ thể, dùng được cho cả hai
kênh: có bản trên đĩa để chạy CLI và bản ZIP để tải lên web.

**Luồng:**

1. Chạy CLI trên thư mục cục bộ, tắt AI, ghi kết quả ra `out-cli`.
2. Tải cùng repository đó lên web dưới dạng ZIP, tắt AI, chờ phân tích xong.
3. Xuất kết quả từ web ra `out-web`.
4. So sánh hai bộ kết quả.

**Kết quả mong đợi — phải giống nhau:**

| Thành phần | Yêu cầu |
|---|---|
| Application và component | Cùng tập, cùng định danh |
| Route | Cùng số lượng, cùng method và path |
| Entity/table và external system | Cùng tập |
| Dependency giữa component | Cùng tập cạnh |
| Nhãn confidence và completeness | Giống nhau cho từng kết luận |
| Limitation | Cùng danh sách phần chưa hỗ trợ và lý do |
| Evidence `file:line` | Trỏ về cùng vị trí trong source |

**Được phép khác:**

- Đường dẫn gốc trong evidence, vì CLI đọc thư mục còn web giải nén ZIP vào vùng xử lý
  riêng. Vị trí tương đối trong repository phải giống nhau.
- Dấu thời gian chạy và định danh phiên.
- Cách trình bày: web có trang tương tác, CLI chỉ có file.

**Không được khác:** bất kỳ fact, quan hệ, nhãn chất lượng hoặc limitation nào. Nếu hai
kênh cho hai kết luận khác nhau về cùng một source thì ít nhất một bên sai, và đó là
lỗi chặn phát hành.

## Bảng liên kết

| Scenario | Use case kiểm chứng | Kênh |
|---|---|---|
| 1a | UC1, UC2 | Web |
| 1b | UC1, UC3.2 | CLI |
| 1c | UC1 — Cung cấp mã nguồn và ba biến thể đầu vào | Cả hai |
| 1d | UC1 — lỗi đầu vào và lỗi ghi output | CLI |
| 2 | UC2 Truy vết phụ thuộc | Web |
| 3 | UC2 Truy vết phụ thuộc, `extend` Kiểm tra bằng chứng nguồn | Web |
| 4, 5 | UC1, UC3.1 | Cả hai |
| 6 | UC2, UC3.1 | Web |
| 7, 8 | UC1, UC2, UC3.1 | Cả hai |
| 9 | UC3.1 | Cả hai |
| 10 | UC1, UC3.2 | Cả hai |
| 11 | UC2 Xem ứng dụng và thành phần | Web |
| 12 | UC3.1 *(mở lại lịch sử)* | Web |
| 13 | UC3.2 | Cả hai |
| 14 | UC1, UC3.2 — hai kênh cho cùng kết quả | Cả hai |

Scenario ghi "Cả hai" nghĩa là hành vi phải giống nhau ở hai kênh; khác nhau chỉ ở
cách hiển thị.

Độ phủ theo chiều ngược lại:

| Use case | Scenario |
|---|---|
| UC1 Phân tích kho mã | 1a, 1b, 1c, 1d, 4, 5, 7, 8, 10, 14 |
| UC2 Xem tổng quan | 1a |
| UC2 Xem ứng dụng và thành phần | 1a, 11 |
| UC2 Xem API và luồng yêu cầu | 2, 7, 8 |
| UC2 Xem kho dữ liệu và tích hợp | 2 |
| UC2 Truy vết phụ thuộc | 2, 3 |
| `extend` Kiểm tra bằng chứng nguồn | 3 |
| UC3.1 Xem kết quả chi tiết | 4, 5, 6, 9, 12 |
| `include` Mở lần phân tích đã lưu | 12 |
| UC3.2 Xuất tài liệu kiến trúc | 1b, 10, 13, 14 |
