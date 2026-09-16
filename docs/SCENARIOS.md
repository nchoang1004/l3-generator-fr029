# Scenarios — Code → L3 Generator

Các scenario dưới đây là tiêu chí hành vi, không phải số đo thực tế. Chúng tập trung
vào mức L3; chi tiết function/call chỉ xuất hiện khi cần làm evidence.

Use case liên quan: [USE_CASES.md](USE_CASES.md).

## Scenario 1 — Hiểu một service chưa quen

**Tiền điều kiện:** repository có application FastAPI, route, service, repository,
SQLAlchemy entity và một external HTTP call.

**Luồng:**

1. Developer chạy `l3gen <repo> --no-ai -o out`.
2. Tool kiểm kê source và báo phần được/không được hỗ trợ.
3. Tool sinh L3, diagram và architecture model.
4. Developer mở L3 và thấy:
   - application/entry point;
   - các component chính;
   - bảng route;
   - data entity/table;
   - external system;
   - dependency giữa các component;
   - coverage và limitations.
5. Developer mở diagram và thấy mô hình tổng quát:

```text
Order API → Order Service → Order Repository → Orders DB
                          └→ Payment Gateway
```

**Kết quả mong đợi:** Developer nắm được cấu trúc mà không phải xem một node cho từng
function. Mỗi quan hệ có thể drill-down về source.

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

1. Reviewer thấy `Order Service → Payment Gateway`.
2. Reviewer mở evidence.
3. Evidence chỉ ra route/handler hoặc component call tới HTTP client cùng URL/host và
   vị trí source.
4. Reviewer mở source tại vị trí đó.
5. Reviewer xác nhận kết luận hoặc phát hiện rule cần sửa.

**Kết quả mong đợi:** người đọc không phải tin mô tả AI. Description không được dùng
làm evidence.

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

1. Developer không đặt API key hoặc dùng `--no-ai`.
2. Static analysis vẫn chạy.
3. L3, diagram, IAM/evidence và architecture graph vẫn được sinh.
4. Output chỉ thiếu description/rephrased findings do AI.
5. Số route/component/entity/dependency không thay đổi vì tắt AI.

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

## Bảng liên kết

| Scenario | Use case chính |
|---|---|
| 1 | UC1, UC2 |
| 2 | UC3, UC4 |
| 3 | UC4 |
| 4, 5 | UC1, UC5 |
| 6 | UC5 |
| 7, 8 | UC1, UC2, UC5 |
| 9 | UC5 |
| 10 | UC6 |
| 11 | UC2, UC7 |
