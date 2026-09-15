# Ý tưởng kiến trúc 2.0 — Language-first Semantic Analysis

## 1. Mục đích

Phiên bản hiện tại có thể làm mất source file khi một thư mục chứa nhiều ngôn ngữ.
Nó cũng đang dựa nhiều vào các mẫu cú pháp riêng lẻ, khiến mỗi cách khai báo framework
mới có thể cần thêm một nhánh xử lý mới.

Kiến trúc 2.0 giải quyết hai vấn đề:

1. Không source file nào biến mất chỉ vì cách người dùng tổ chức thư mục.
2. Resolver và graph dựa trên symbol, scope và dòng chảy dữ liệu, thay vì chủ yếu khớp
   các mẫu cục bộ.

Mục tiêu của 2.0 không phải hiểu được mọi hành vi runtime. Mục tiêu là:

> Giải được mọi quan hệ có đủ bằng chứng trong source; giữ nhiều ứng viên khi chưa thể
> chọn một; nói rõ `unresolved` khi thông tin chỉ xuất hiện lúc chạy.

---

## 2. Các quyết định nền tảng

### 2.1 Ngôn ngữ quyết định parser

Mỗi file được nhận diện ngôn ngữ độc lập:

```text
Repository
    ├── Python files       → Python frontend
    ├── Java files         → Java frontend
    ├── JavaScript files   → JavaScript frontend
    └── Unsupported files  → ghi nhận, không âm thầm loại bỏ
```

Không chọn một ngôn ngữ đại diện cho cả repo hoặc cả thư mục. Không dùng số đông để
loại ngôn ngữ thiểu số.

### 2.2 Framework là lớp semantic trên ngôn ngữ

Sau khi file đã được parser của ngôn ngữ đọc, một hoặc nhiều framework adapter có thể
đọc cùng semantic model:

```text
Python semantic model
    ├── FastAPI adapter
    ├── SQLAlchemy adapter
    ├── httpx/requests adapter
    └── adapter khác nếu được hỗ trợ
```

Framework không phải các rổ loại trừ nhau. Một file Python có thể đồng thời dùng
FastAPI, SQLAlchemy và httpx.

Lý do phân framework là mỗi framework có API, convention và cách biểu diễn khái niệm
khác nhau; không phải vì mỗi framework tương ứng với một service.

### 2.3 Service không quyết định file nào được parse

Service/application boundary chỉ là metadata hoặc một view kiến trúc được dựng sau
khi có graph.

Nó có thể dựa trên:

- application entrypoint;
- Docker Compose, Dockerfile hoặc Kubernetes manifest;
- Maven/Gradle module, Python package, JavaScript workspace;
- dependency graph;
- cấu hình do người dùng cung cấp.

Nếu chưa đủ bằng chứng thì ghi `application_boundary: unknown`. Không được bỏ file.

### 2.4 AI không tham gia đường tạo fact

AI chỉ được:

1. Viết description cho fact đã tồn tại.
2. Viết lại câu chữ của reviewer finding đã được luật deterministic phát hiện.

AI không được:

- phát hiện route/entity;
- resolve symbol hoặc call target;
- tạo candidate edge;
- suy ra framework semantics;
- đề xuất hoặc tự thêm rule trong lúc tool chạy;
- sửa IAM hoặc verified graph.

Framework adapter dùng semantic summary viết sẵn, có version, fixture và test.

---

## 3. Pipeline mục tiêu

```text
┌────────────────────────────────────────────────────────────┐
│ 1. File Inventory                                          │
│ path · language · size · digest · status · reason          │
└──────────────────────────┬─────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────┐
│ 2. Language Frontends                                      │
│ Python parser · Java parser · JavaScript parser             │
└──────────────────────────┬─────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────┐
│ 3. Common Semantic IR                                      │
│ symbol · scope · import · call · assignment · return        │
│ attribute · inheritance · decorator · annotation · source   │
└──────────────────────────┬─────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────┐
│ 4. Resolver + Dataflow                                     │
│ name binding · type/points-to propagation · candidate sets  │
│ resolved/candidates/unresolved · evidence path              │
└──────────────────────────┬─────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────┐
│ 5. Deterministic Framework Adapters                        │
│ FastAPI · Starlette · SQLAlchemy · HTTP clients             │
└──────────────────────────┬─────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────┐
│ 6. Architecture Graph                                     │
│ calls · exposes · reads · writes · mounts · calls_external  │
└──────────────┬───────────────────────────────┬─────────────┘
               ▼                               ▼
       L3/diagram/JSON                 Description + reviewer
                                      AI chỉ sửa câu chữ
```

---

## 4. File Inventory — không được mất file

Mỗi source file có một record trước khi parser chạy:

```json
{
  "path": "backend/UserController.java",
  "language": "java",
  "status": "unsupported",
  "reason": "Java frontend chưa được triển khai"
}
```

Các trạng thái tối thiểu:

```text
discovered
parsed
unsupported_language
parse_error
excluded
oversized
```

Bất biến bắt buộc:

```text
Tổng file source phát hiện được
= parsed
+ unsupported_language
+ parse_error
+ excluded có lý do
+ oversized có lý do
```

CI phải fail nếu một file không nằm trong đúng một nhóm kết quả.

### Ca repo phẳng

```text
repo/
    api.py
    service.py
    UserController.java
    PaymentService.java
    app.ts
```

Kết quả đúng:

```text
Python frontend:     api.py, service.py
Java frontend:       UserController.java, PaymentService.java
JavaScript frontend: app.ts
```

Cách xếp folder không làm thay đổi file nào được phát hiện.

---

## 5. Common Semantic IR

Parser của mỗi ngôn ngữ có AST khác nhau. Phần sau parser cần một mô hình chung vừa
đủ để resolver và framework adapter sử dụng.

Các fact tối thiểu:

```text
Module
SymbolDefinition
Scope
ImportBinding
ClassDefinition
FunctionDefinition
Parameter
Assignment
CallSite
ReturnValue
AttributeAccess
Inheritance
DecoratorOrAnnotation
LiteralValue
SourceLocation
```

IR không tự gọi một class là database entity hoặc một function là HTTP endpoint. Đó
là việc của framework adapter sau khi symbol đã được resolve.

Mỗi fact phải có:

- ID ổn định;
- ngôn ngữ;
- file và dòng nguồn;
- parser/frontend version;
- trạng thái đầy đủ;
- lý do nếu chỉ đọc được một phần.

---

## 6. Resolver — từ tra tên tới truyền giá trị

### 6.1 Bước 1 — Global Symbol Index

Lập danh bạ mọi định nghĩa:

```text
app.service.OrderService          → service.py:1
app.service.OrderService.confirm  → service.py:2
app.api.confirm_order             → api.py:8
```

Tên đầy đủ gồm module/package/path. Không dùng tên ngắn làm identity toàn repo.

### 6.2 Bước 2 — Name Binding theo scope

Trong từng file và scope, resolve import và alias:

```text
api.py: OrderService → app.service.OrderService
legacy.py: OrderService → legacy.service.OrderService
```

Hai file có thể dùng cùng tên ngắn cho hai symbol khác nhau.

### 6.3 Bước 3 — Sinh dataflow constraints

Thay vì hỏi đoạn code có khớp một mẫu cụ thể không, chuyển semantics ngôn ngữ thành
các quan hệ truyền giá trị:

```text
x = y                 → value(y) chảy sang value(x)
f(x)                  → value(x) chảy sang parameter tương ứng của f
return x              → value(x) chảy sang return value của function
y = f()               → return value của f chảy sang value(y)
self.repo = x         → value(x) chảy sang value(self.repo)
x = SomeClass()       → points-to(x) chứa SomeClass
```

Đây là semantics chung của ngôn ngữ, không phải rule theo tên biến.

### 6.4 Bước 4 — Fixed-point propagation

Dùng worklist. Chỉ xử lý lại node khi có fact mới:

```text
Khởi tạo hàng đợi bằng các fact trực tiếp.

Trong khi còn fact mới:
    lấy một fact;
    truyền qua các cạnh liên quan;
    nếu đích nhận được thông tin chưa từng có:
        lưu evidence;
        đưa đích vào hàng đợi.
```

Không quét lại toàn bộ repo sau mỗi fact.

### 6.5 Bước 5 — Resolve call target

Kết quả không bị ép thành một đích:

```text
resolved    → đúng một đích được chứng minh;
candidates  → nhiều đích hợp lệ;
unresolved  → chưa đủ thông tin tĩnh;
runtime     → đích phụ thuộc dữ liệu lúc chạy.
```

Ví dụ polymorphism:

```python
execute(PaymentHandler())
execute(EmailHandler())

def execute(handler):
    handler.run()
```

Kết quả:

```text
handler.run candidates:
- PaymentHandler.run
- EmailHandler.run
```

### 6.6 Evidence path

Mỗi quan hệ suy ra phải giữ đường chứng minh:

```json
{
  "call_site": "handler.py:14",
  "targets": ["service.OrderService.confirm"],
  "status": "resolved",
  "evidence": [
    "api.py:8 truyền svc vào handle",
    "api.py:7 svc được tạo bởi OrderService"
  ]
}
```

---

## 7. Deterministic Framework Adapter

### 7.1 Semantic summary thay cho chuỗi `if name == ...`

Framework adapter không hỏi AI. Nó dùng bảng semantics được viết và review trước:

```yaml
framework: fastapi-starlette
version: 1
symbols:
  fastapi.FastAPI.include_router:
    operation: AttachRouter
    child_argument: 0
    prefix_keyword: prefix

  starlette.applications.Starlette.mount:
    operation: MountApplication
    path_argument: 0
    child_keyword: app

  fastapi.FastAPI.add_api_route:
    operation: RegisterEndpoint
    path_argument: 0
    endpoint_argument: 1
    methods_keyword: methods
```

Adapter khớp theo symbol đầy đủ đã resolve, không khớp riêng chữ `mount` hoặc
`include_router`.

Ví dụ `foo.mount()` không được coi là Starlette nếu type của `foo` không resolve tới
Starlette/FastAPI application.

### 7.2 Registration IR

Các cách khai báo route khác nhau được chuẩn hóa thành operation chung:

```text
AttachRouter(parent, child, prefix)
MountApplication(parent, child, path)
RegisterEndpoint(owner, endpoint, path, methods)
ConditionalRegistration(condition, registration)
```

Ví dụ:

```python
app.include_router(router, prefix="/api")
```

trở thành:

```text
AttachRouter(app, router, "/api")
```

```python
app.mount("/api", app=sub_app)
```

trở thành:

```text
MountApplication(app, sub_app, "/api")
```

```python
app.add_api_route("/orders", create_order, methods=["POST"])
```

trở thành:

```text
RegisterEndpoint(app, create_order, "/orders", ["POST"])
```

Decorator route cũng được chuyển thành `RegisterEndpoint` trước khi dựng route cuối.

### 7.3 Version và kiểm thử

Mỗi semantic summary phải có:

- framework/library và dải version hỗ trợ;
- symbol đầy đủ;
- operation chuẩn;
- ánh xạ positional/keyword argument;
- fixture positive;
- fixture negative để chống trùng tên;
- test output và evidence;
- changelog khi semantics đổi.

Không summary nào được tự sinh hoặc tự kích hoạt bởi AI.

---

## 8. Architecture Graph

Graph giữ đúng loại quan hệ:

```text
imports
calls
inherits
constructs
exposes
registers
mounts
reads
writes
calls_external
```

Không biến mọi quan hệ thành `calls`.

Ví dụ:

```text
POST /orders
    └── exposes → create_order()
                      ├── calls → OrderService.create()
                      ├── writes → Order
                      └── calls_external → payment.internal
```

Application/service view được tạo từ graph và deployment evidence sau cùng. Nó không
ảnh hưởng bước kiểm kê hoặc parse file.

---

## 9. Độ phức tạp và latency

### 9.1 Không phải mặc định là O(n²)

Gọi:

- `B`: tổng byte hoặc tổng AST node của source;
- `S`: số symbol;
- `I`: số import/binding;
- `E`: số dataflow/call/inheritance edge;
- `F`: số fact kiểu/points-to thực sự được truyền.

Các bước cơ bản:

| Bước | Cách triển khai | Chi phí gần đúng |
|---|---|---|
| Kiểm kê file | Duyệt mỗi path một lần | `O(number_of_files)` |
| Parse | Đọc mỗi byte/node một số lần hữu hạn | `O(B)` |
| Symbol index | Hash map theo qualified name | `O(S)` trung bình |
| Bind import | Tra hash map | `O(I)` trung bình |
| Adapter dispatch | Tra summary bằng resolved symbol | `O(relevant_calls + decorators)` |
| Dựng graph | Duyệt node/cạnh | `O(S + E)` |
| Service/application view | Connected traversal trên graph | `O(V + E)` |

Nếu mỗi framework adapter tự quét lại toàn bộ AST thì chi phí sẽ gần
`O(number_of_adapters × B)`. Thiết kế 2.0 không làm như vậy. Language frontend phát
event/fact một lần; adapter được gọi qua index theo loại fact hoặc resolved symbol.

Ví dụ:

```text
resolved symbol = fastapi.FastAPI.include_router
→ tra thẳng summary bằng hash map
→ không hỏi lần lượt mọi adapter
```

### 9.2 Phần dataflow có thể đắt hơn tuyến tính

Fixed-point không có một cam kết `O(n)` cho mọi chương trình. Chi phí phụ thuộc số
fact được truyền và số candidate target.

Gần đúng:

```text
O(E + số lần fact mới được truyền qua edge)
```

Nếu một biến có thể trỏ tới rất nhiều class và được truyền qua nhiều call site, tập
candidate có thể phình lớn. Một implementation ngây thơ có thể tiến gần `O(n²)` hoặc
tệ hơn ở ca xấu.

Điểm cần tối ưu không phải bỏ dataflow, mà là làm nó sparse và có giới hạn rõ ràng.

### 9.3 Các biện pháp giữ latency

1. **Hash index, không tìm tuyến tính.**
   Qualified symbol, import, call site và summary đều tra bằng map/set.

2. **Worklist theo delta.**
   Chỉ truyền fact mới; không chạy lại toàn bộ graph ở mỗi vòng.

3. **Deduplicate fact.**
   Một cặp `(value, abstract_type)` chỉ được thêm một lần.

4. **Phân tích theo ngôn ngữ song song.**
   Python, Java và JavaScript frontend độc lập cho tới bước nối contract.

5. **Parse file song song.**
   Mỗi file có thể parse độc lập trước khi bind symbol toàn cục.

6. **SCC cho vòng gọi/kế thừa.**
   Gom strongly connected component để tránh đi vòng vô hạn.

7. **Giới hạn candidate set.**
   Nếu vượt ngưỡng, ghi `truncated` kèm tổng số và lý do; không âm thầm bỏ.

8. **Budget theo run.**
   Giới hạn file, byte, AST node, edge, thời gian và bộ nhớ; output phải ghi phần nào
   bị giới hạn.

9. **Content hash cache ở giai đoạn sau.**
   File không đổi có thể dùng lại parse/IR. Kết quả incremental phải được test bằng
   invariant: incremental result bằng cold-build result.

10. **Graph slicing khi render.**
    IAM/graph có thể đầy đủ; Markdown và Mermaid chỉ render phần liên quan hoặc báo
    truncation. Không để chi phí trình bày chi phối phân tích.

### 9.4 Mục tiêu hiệu năng cần đo, không đoán

Trước khi triển khai dataflow cần lưu baseline hiện tại:

- số file và byte;
- parse time;
- index time;
- resolution time;
- adapter time;
- graph/render time;
- peak memory;
- số resolved/candidates/unresolved.

Sau mỗi mốc, chạy cùng fixture và các repo đã pin commit. Không chỉ báo tổng thời gian;
phải biết bước nào tăng latency.

Ngưỡng ban đầu nên được đặt sau khi đo baseline trên ít nhất:

- repo nhỏ;
- repo trung bình;
- repo lớn;
- repo phẳng đa ngôn ngữ;
- monorepo có nhiều application.

---

## 10. Giới hạn không thể loại bỏ

Static analysis không thể biết chắc giá trị chỉ xuất hiện lúc chạy:

```python
handler_name = config["handler"]
handler = getattr(module, handler_name)
handler()
```

Hoặc:

```python
plugin = load_plugin_from_database()
plugin.execute()
```

Kết quả đúng là:

```text
status: runtime
reason: call target phụ thuộc configuration/database lúc chạy
```

Không dùng AI để lấp khoảng trống này.

---

## 11. Kế hoạch triển khai đề xuất

### Mốc V2.1 — File Inventory

- Bỏ majority-language filtering.
- Phân loại từng file.
- Giữ record cho ngôn ngữ chưa hỗ trợ.
- Thêm invariant bảo toàn file.
- Test repo phẳng, mixed-language, không manifest và nested module.

**Xong khi:** không file source nào biến mất khỏi coverage report.

### Mốc V2.2 — Tách language frontend và adapter

- Python frontend sinh Common Semantic IR.
- FastAPI, SQLAlchemy và HTTP client đọc IR.
- Một file có thể được nhiều adapter xử lý.
- Output hiện tại không đổi trên fixture cũ, trừ lỗi đã được xác định.

**Xong khi:** extractor không cần tự quét lại AST thô theo cách riêng.

### Mốc V2.3 — Dataflow nội hàm và liên hàm cơ bản

- Assignment propagation.
- Argument-to-parameter propagation.
- Return-to-receiver propagation.
- Attribute propagation.
- Worklist và evidence path.
- Kết quả `resolved/candidates/unresolved/runtime`.

**Xong khi:** các ca truyền dependency qua nhiều hàm resolve được mà không dựa vào tên
biến.

### Mốc V2.4 — Registration IR

- Semantic summary FastAPI/Starlette v1.
- Chuẩn hóa decorator, `include_router`, `mount`, `add_api_route`, `Route`.
- Giữ điều kiện đăng ký trong `if`.
- Thêm positive/negative/version fixtures.

**Xong khi:** sửa được ba lỗi route đã biết mà không thêm chuỗi `if method_name` rải
rác trong engine.

### Mốc V2.5 — Graph và application view

- Mở rộng edge type.
- Service/application grouping chạy sau graph.
- Hỗ trợ boundary `unknown` và nhiều evidence source.
- Không ảnh hưởng coverage file.

### Mốc V2.6 — Performance và evaluation

- Benchmark từng pipeline stage.
- Peak memory.
- Repo lớn và repo đa ngôn ngữ.
- Regression precision/recall.
- So sánh cold build với cache/incremental nếu triển khai cache.

---

## 12. Những điều không làm trong 2.0 lõi

- Không dùng AI để tạo fact, edge, candidate hoặc framework rule.
- Không chọn ngôn ngữ bằng bỏ phiếu đa số.
- Không coi folder là service nếu không có bằng chứng.
- Không cài hoặc chạy code của repository mục tiêu.
- Không ép call site đa hình về một target duy nhất.
- Không giấu file, edge hoặc candidate bị cắt vì budget.
- Không mở rộng nhiều ngôn ngữ trước khi Python semantic pipeline ổn định.

---

## 13. Tiêu chí thành công

Kiến trúc 2.0 được coi là đạt khi:

1. Mọi source file đều có trạng thái và lý do rõ ràng.
2. Folder phẳng hoặc trộn Java/Python không làm mất phần Python.
3. Framework adapter deterministic, versioned và có test.
4. AI không nằm trên đường tạo IAM/graph.
5. Resolver giữ nhiều candidate khi cần và có evidence path.
6. Các quan hệ route/function/entity có edge type đúng nghĩa.
7. Kết quả chạy lại trên cùng input/config ổn định.
8. Latency và memory được đo theo từng bước.
9. Khi vượt budget, tool báo `partial/truncated`, không giả vờ đầy đủ.

