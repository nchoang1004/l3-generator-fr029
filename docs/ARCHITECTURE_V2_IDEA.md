# Ý tưởng kiến trúc 2.0 — Language-first, Architecture-focused Analysis

> **Lỗi thời một phần từ 23/09/2026.** Tài liệu này viết cho hướng AI tắt hoặc AI chỉ viết mô tả, trên bộ yêu cầu BL-r14. Nguồn đúng hiện nay là [PRD hiện hành](../.aide/product/prd/PRD-L3GEN-2609-001.md) của CHG-L3GEN-2026-002: mô hình ngôn ngữ đề xuất component và quan hệ, code kiểm dữ kiện chứng minh. Mã FR/NFR nhắc ở đây là mã cũ. Khi khác nhau, PRD thắng. Đọc file này để hiểu cơ chế phân tích tĩnh, không dùng làm yêu cầu.

> **Trạng thái trong gói hồ sơ này: ghi chép thiết kế, không phải artifact chuẩn tắc.**
>
> Tài liệu này đến từ một hướng làm song song và được đưa vào để người review thấy cơ chế
> phân tích đã được nghĩ tới đâu. Nó **chưa phải L2**: theo quy trình, L2 là một file CMP
> cho một component, phải có đủ bảy mục gồm transaction boundary, idempotency và
> concurrency, và phải kèm 2–3 phương án có tradeoff. Tài liệu này là một phương án đã
> chọn, mô tả cả pipeline trong một file.
>
> L2 được lập ở bước 7, sau Scope Gate. Khi đó pipeline dưới đây tách thành các CMP riêng.
> Đừng đọc file này như thiết kế đã duyệt, và đừng coi nó là bằng chứng đã có L2.
>
> Phần quyết định kiến trúc duy nhất đã được viết đúng dạng chuẩn tắc là
> [ADR-2026-001](../.aide/architecture/adr/ADR-2026-001.md) — mức trừu tượng của kết quả.

> **Lưu ý — cách hiện tại vẫn là “duyệt trâu”.** Công cụ đi qua toàn bộ file code để
> không bỏ sót vì cách sắp xếp thư mục. Đây là nền móng ưu tiên độ phủ, chưa phải cách
> tối ưu cuối cùng. Về sau có thể lưu kết quả file không đổi và chỉ phân tích phần bị
> ảnh hưởng.

> **Trạng thái ngày 16/09/2026.** Luồng chạy chính đã có File Inventory, Python
> Frontend, Common Semantic IR, Resolver + Dataflow, FastAPI/SQLAlchemy adapters, IAM
> và graph. Tuy nhiên code hiện còn thiên về graph mức function/class. Tài liệu này
> xác định lại đích của V2: dùng chi tiết code làm bằng chứng nội bộ, còn sản phẩm
> chính phải là L3 ở mức application/component. Chưa được coi V2 hoàn tất cho tới khi
> code, test và output được đối chiếu lại với ranh giới này.

---

## 1. Mục tiêu

Công cụ đọc source repository và trả lời các câu hỏi kiến trúc:

1. Repository có những application hoặc component nào?
2. Entry point nằm ở đâu?
3. Application cung cấp API nào?
4. Route được xử lý bởi component nào?
5. Component nào phụ thuộc component nào?
6. Component nào đọc hoặc ghi bảng dữ liệu nào?
7. Component nào gọi hệ thống bên ngoài?
8. Có event, queue hoặc configuration quan trọng nào?
9. Phần nào công cụ chưa đọc được, và vì sao?

Đầu ra chính là:

- tài liệu L3;
- component model;
- dependency diagram;
- quan hệ API, DB, external system và event;
- bằng chứng để truy ngược mỗi kết luận về source.

### 1.1 Không biến V2 thành Repository Knowledge Graph

Repository Knowledge Graph đầy đủ là một bài toán khác. V2 không đặt mục tiêu:

- hiểu chính xác mọi biến trong repository;
- nối được mọi lời gọi hàm;
- hiển thị mọi function/class trong diagram L3;
- xử lý mọi kiểu factory, plugin hoặc code động của Python;
- cung cấp graph query API, graph traversal hoặc incremental graph;
- thay thế static analyzer tổng quát.

Function, class, phép gán và call vẫn có thể xuất hiện trong dữ liệu kỹ thuật nội bộ.
Chúng chỉ là phương tiện để chứng minh quan hệ kiến trúc.

---

## 2. Nguyên tắc trung tâm: Analyze Deep Enough, Present at L3

“Phân tích đủ sâu” và “trình bày chi tiết” là hai việc khác nhau.

Ví dụ:

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
        return self.repository.save()
```

Engine có thể phải đọc parameter, dependency injection, thuộc tính và call để chứng
minh chuỗi:

```text
Orders API → Order Service → Order Repository → orders table
```

Nhưng diagram L3 không nên vẽ:

```text
create_order() → get_service() → __init__() → create() → save()
```

Chuỗi function chi tiết chỉ dùng làm evidence (bằng chứng) hoặc dữ liệu chẩn đoán.

### 2.1 Khi nào được phân tích sâu hơn?

Chỉ đi tiếp nếu dữ kiện có thể giúp trả lời một câu hỏi kiến trúc ở mục 1.

Có thể đi tiếp khi:

- bắt đầu từ route, entry point hoặc framework application;
- đang lần theo route tới service/repository;
- đang tìm bảng dữ liệu hoặc external system được sử dụng;
- đang xác định component hoặc application boundary;
- đang chứng minh một dependency quan trọng.

Dừng khi:

- đã tìm thấy quan hệ kiến trúc cần thiết;
- gặp code phụ thuộc runtime;
- vượt giới hạn thời gian, số candidate hoặc độ sâu đã công bố;
- dữ kiện chỉ là logic cục bộ không ảnh hưởng kiến trúc;
- đi tiếp chỉ phục vụ graph mức function nhưng không cải thiện L3.

---

## 3. Pipeline mục tiêu

```text
1. File Inventory + Analysis Context
   File nào tồn tại? Ngôn ngữ nào? Source root và phiên bản nào đã biết?
                              │
                              ▼
2. Language Frontends
   Mỗi ngôn ngữ dùng parser phù hợp
                              │
                              ▼
3. Common Semantic IR
   import · definition · assignment · call · return · decorator · scope
                              │
                              ▼
4. Architectural Anchor Discovery
   entry point · app/router · route · entity · external/event/config candidate
                              │
                              ▼
5. Targeted Resolver + Dataflow  ↔  Deterministic Library Models
   Chỉ lần theo dữ kiện liên quan tới các anchor và câu hỏi kiến trúc
                              │
                              ▼
6. Deterministic Framework Adapters
   Xác nhận ý nghĩa API framework bằng symbol đầy đủ
                              │
                              ▼
7. Registration & Composition
   Route/router/app nào được gắn với nhau? Path và điều kiện là gì?
                              │
                              ▼
8. Component Synthesis + Architecture IAM
   Tổng hợp evidence thành application, component và dependency
                              │
                              ▼
9. L3 Projection + Validation + Outputs
   L3 · component diagram · architecture graph · evidence · limitations
```

Hai đường hỗ trợ chạy xuyên suốt:

- **Evidence & Diagnostics:** lưu vị trí source, lý do và phần chưa hiểu.
- **Budgets:** giới hạn số candidate, số lần truyền và tài nguyên; chạm giới hạn phải
  báo partial, không im lặng.

AI không nằm trên đường tạo dữ kiện. AI chỉ được viết description hoặc diễn đạt lại
finding đã được phát hiện bằng luật tất định.

---

## 4. File Inventory + Analysis Context

### 4.1 File Inventory

Duyệt file để ghi:

- đường dẫn tương đối;
- phần mở rộng và ngôn ngữ dự kiến;
- trạng thái: discovered, parsed, unsupported, excluded, parse_error hoặc quá giới hạn;
- lý do nếu không phân tích.

Không dùng folder như service boundary. Một folder có thể chứa nhiều ngôn ngữ; một
ngôn ngữ có thể nằm ở nhiều folder.

### 4.2 Analysis Context

Cùng tên module có thể tồn tại ở hai source root:

```text
repo/
├── app_a/src/app/service.py
└── app_b/src/app/service.py
```

Vì vậy phải giữ, khi có thể:

- source root;
- package/module root;
- phiên bản ngôn ngữ;
- phiên bản framework/thư viện;
- file cấu hình hoặc manifest làm bằng chứng.

Nếu thiếu source root, không được gộp hai `app.service` thành một. Đánh dấu import
nhập nhằng và tiếp tục với phần chắc chắn.

---

## 5. Language Frontends + Common Semantic IR

### 5.1 Language Frontends

Frontend dùng parser của ngôn ngữ để chuyển cú pháp thành dữ kiện trung lập.

Ví dụ Python:

```python
app = FastAPI()
```

Frontend chỉ ghi:

```text
Call(Name("FastAPI"))
Assignment(target="app", value=<call>)
location=main.py:3
scope=module:main
```

Nó chưa kết luận `FastAPI` là framework class hoặc `app` là application.

### 5.2 Common Semantic IR

IR cần đủ cho các câu hỏi kiến trúc:

- import;
- module, class, function và method;
- scope;
- parameter và type annotation;
- assignment;
- call;
- return;
- inheritance;
- decorator;
- literal và expression chưa tính được;
- condition bao quanh;
- vị trí source.

IR có thể chứa nhiều dữ kiện hơn IAM kiến trúc. Không phải mọi IR fact đều trở thành
node trong output.

### 5.3 Parse được không có nghĩa hiểu được

AST cho biết cấu trúc cú pháp. Name Binding mới xác định tên nằm trong scope nào;
resolver mới xác định nó có thể trỏ tới đâu; adapter mới biết API framework có ý nghĩa
gì. Mỗi tầng phải giữ riêng trách nhiệm.

---

## 6. Architectural Anchor Discovery

Anchor là điểm bắt đầu có khả năng liên quan trực tiếp đến L3.

| Anchor | Ví dụ |
|---|---|
| Entry point | `main.py`, application factory được cấu hình |
| Application/router | `FastAPI()`, `APIRouter()` |
| Route registration | decorator, `include_router`, `mount`, `add_api_route` |
| Data entity | SQLAlchemy/SQLModel model |
| External interaction | httpx/requests call |
| Event interaction | publish/consume API đã được hỗ trợ |
| Configuration | settings hoặc manifest ảnh hưởng boundary/dependency |
| Layer candidate | class/module có bằng chứng service/repository, không chỉ dựa tên folder |

Anchor mới chỉ là candidate. Framework adapter và resolver phải xác nhận trước khi
đưa thành quan hệ kiến trúc.

Lợi ích của anchor:

- không phải lần theo mọi call trong repo với cùng độ sâu;
- ưu tiên dữ kiện ảnh hưởng trực tiếp tới L3;
- vẫn có thể mở rộng thêm adapter mà không thay parser;
- đo được mỗi loại quan hệ bị mất ở bước nào.

---

## 7. Targeted Resolver + Dataflow

Resolver trả lời “tên/call này có thể trỏ tới symbol nào?”. Dataflow trả lời “giá trị
nào có thể truyền tới biến, parameter, thuộc tính hoặc return này?”.

### 7.1 Nối tên theo scope

```python
from fastapi import FastAPI as Application
app = Application()
```

Trong file này:

```text
Application → fastapi.FastAPI
```

Bảng import phải gắn theo từng module/scope, không dùng một bảng tên chung cho cả repo.

### 7.2 Library Models hỗ trợ resolver

AST không thể tự biết gọi `FastAPI()` trả về loại gì. Kho luật đã duyệt cung cấp:

```text
fastapi.FastAPI
kind: class
constructs: fastapi.FastAPI instance
```

Kho luật là tất định, có phiên bản và dải phiên bản thư viện áp dụng. “Phiên bản bảng
luật” và “phiên bản FastAPI” là hai thông tin khác nhau. Nếu không biết phiên bản
framework, output phải ghi giả định hoặc hạ mức đầy đủ.

### 7.3 Các quan hệ truyền giá trị cần thiết

MVP ưu tiên:

```text
x = A()                    constructor trực tiếp
x: A = value               type annotation
alias = A                  alias qua phép gán
self.repo = repo           thuộc tính
argument → parameter       khi nằm trên đường từ anchor tới dependency
return value → call result khi nằm trên đường từ anchor tới dependency
subclass → base class      khi cần xác định framework/entity/layer
```

Không cam kết points-to analysis đầy đủ cho toàn Python.

### 7.4 Vòng lặp có giới hạn

Một đích call mới có thể tạo thêm quan hệ argument → parameter và return → result.
Do đó Name Binding và Dataflow không phải hai bước chỉ chạy đúng một lượt.

Dùng worklist (hàng đợi công việc):

1. đưa dữ kiện đã biết vào hàng đợi;
2. lấy một dữ kiện và truyền qua các quan hệ liên quan;
3. chỉ thêm dữ kiện mới chưa từng thấy;
4. tiếp tục tới khi không còn thay đổi hoặc chạm budget.

Budget phải được ghi trong kết quả. Chạm budget có nghĩa partial, không có nghĩa
repository không có quan hệ đó.

### 7.5 Trạng thái của một call

| Trạng thái | Nghĩa |
|---|---|
| `resolved` | Có một đích trong phần mô hình đã hỗ trợ |
| `candidates` | Có nhiều khả năng, hoặc còn khả năng chưa biết |
| `unresolved` | Chưa tìm được vì thiếu model, thiếu context hoặc cú pháp chưa hỗ trợ |
| `runtime` | Đích phụ thuộc dữ liệu chỉ có khi chương trình chạy |

`resolved` không chứng minh call chắc chắn được thực thi. Nó chỉ nói nếu biểu thức
này được thực thi thì đích đã xác định trong giới hạn mô hình.

### 7.6 Không tạo semantic edge từ một tên giống framework

```python
disk_manager.mount("/dev/sdb")
```

Không được coi là Starlette mount chỉ vì method tên `mount`.

Nếu receiver chưa xác định:

- lưu raw call và lý do trong evidence/diagnostics;
- không tạo cạnh `mounts` hoặc `registers` trong architecture graph;
- không vẽ cạnh nét đứt như thể nó là quan hệ framework có khả năng đúng.

---

## 8. Deterministic Framework Adapters

Adapter hiểu API của framework sau khi resolver đã xác định symbol.

### 8.1 Hai loại kiến thức

**Library Type/Effect Models** dùng trong resolver:

```text
FastAPI là class
FastAPI() tạo application object
Depends(provider) truyền kết quả provider theo rule đã duyệt
```

**Framework Operations** dùng sau khi call đã được nối:

```text
fastapi.FastAPI.include_router → AttachRouter
starlette.applications.Starlette.mount → MountApplication
fastapi.FastAPI.add_api_route → RegisterEndpoint
```

Vì vậy một phần kiến thức framework tham gia resolver; phần diễn giải operation chạy
sau resolver. Không đặt toàn bộ adapter cứng trước hoặc sau dataflow.

### 8.2 Rule bắt buộc có

Mỗi rule ghi:

- symbol đầy đủ;
- framework và dải phiên bản áp dụng;
- operation chung;
- vị trí positional/keyword arguments;
- tác động lên type/value nếu có;
- ví dụ đúng;
- ví dụ chống nhận nhầm;
- test;
- lịch sử thay đổi.

AI không được sinh hoặc tự bật rule khi chạy.

### 8.3 Tương lai V2.5 — Agent đề xuất rule

Ngoài phạm vi V2 hiện tại:

```text
Engine gặp call đã resolve nhưng chưa có operation
→ lưu call site + definition/stub + phiên bản
→ Agent soạn đề xuất rule và test
→ con người kiểm tra tài liệu chính thức
→ rule chỉ được dùng sau khi review và merge
```

Agent chỉ soạn đề xuất, không tạo dữ kiện trong lần chạy hiện tại.

---

## 9. Registration & Composition

Biết `include_router` là method gì chưa đủ. Cần biết object nào là cha/con và câu
lệnh nằm trong điều kiện hoặc ngữ cảnh nào.

```python
app.include_router(router, prefix="/api")
```

trở thành:

```text
AttachRouter(
  parent=object:app,
  child=object:router,
  prefix="/api",
  condition=[],
  evidence=main.py:8
)
```

Decorator route, `mount` và `add_api_route` cũng được chuẩn hóa thành operation.

Phải phân biệt:

1. **Declared:** source có khai báo operation.
2. **Registered candidate:** operation đã gắn đúng object theo bằng chứng tĩnh.
3. **Potentially reachable:** có bằng chứng call context có thể chạy.
4. **Runtime confirmed:** chỉ có khi dùng dữ liệu runtime; V2 static không khẳng định.

Ví dụ:

```python
def setup():
    app.add_api_route("/orders", handler)
```

Nếu không thấy `setup()` được gọi, không được mô tả route là chắc chắn active. Có thể
giữ nó như declared/conditional với lý do.

Object identity cũng quan trọng:

```python
public_app = FastAPI()
admin_app = FastAPI()
public_app.add_api_route("/orders", handler)
```

Route thuộc `public_app`, không phải mọi object có cùng type FastAPI.

---

## 10. Component Synthesis + Architecture IAM

### 10.1 Component không đồng nghĩa folder

Component boundary được tổng hợp từ bằng chứng như:

- framework application/router;
- entry point và registration tree;
- package/module;
- quan hệ route → handler → service/repository;
- entity/external/event được sử dụng;
- manifest/configuration;
- convention framework đã được review.

Tên folder chỉ là một tín hiệu, không phải kết luận.

### 10.2 Application boundary là candidate

Static source thường không đủ để biết deployment boundary thật. IAM ghi:

- boundary candidate;
- evidence;
- confidence/completeness;
- phần chưa biết.

Không gọi một nhóm ngôn ngữ là service.

### 10.3 IAM kiến trúc

IAM chính nên ưu tiên:

- repository/application/component;
- entry point;
- route;
- data entity/table;
- external system;
- event/configuration quan trọng;
- dependency giữa các thành phần trên;
- evidence, confidence, completeness và limitations.

Function-level facts có thể nằm trong evidence hoặc diagnostic model. Chúng không mặc
nhiên trở thành public architecture node.

---

## 11. Architecture Graph và L3 Projection

### 11.1 Hai cách nhìn khác nhau

**Evidence graph nội bộ/diagnostic** có thể chứa module, class, function và call cần để
giải thích kết luận.

**Architecture graph công khai** chỉ chứa những node/cạnh phục vụ L3:

| Node | Ví dụ |
|---|---|
| Application | Public API |
| Component | Order Service, Order Repository |
| API | POST /orders |
| Data store/entity | orders table |
| External system | Payment Gateway |
| Event/config | OrderCreated, DATABASE_URL |

| Edge | Ý nghĩa |
|---|---|
| `exposes` | application/component cung cấp API |
| `handled_by` | API được component xử lý |
| `depends_on` | component phụ thuộc component |
| `reads` / `writes` | component dùng dữ liệu |
| `calls_external` | component gọi hệ thống ngoài |
| `publishes` / `consumes` | component tương tác event |
| `mounts` / `registers` | composition đã được xác nhận |

### 11.2 Diagram phải tổng quát hóa

Diagram mặc định nhóm ở mức component:

```text
Order API
   → Order Service
   → Order Repository
   → Orders Database
   → Payment Gateway
```

Không hiển thị mọi function. Người đọc có thể truy evidence để xem đường call chi tiết.

### 11.3 Unresolved không phải architecture edge

Unresolved raw call được đưa vào limitations/evidence. Chỉ edge đã xác định đúng loại
quan hệ mới xuất hiện trong architecture graph. Điều này tránh một cạnh nét đứt vẫn
khiến người đọc hiểu nhầm rằng quan hệ framework có khả năng tồn tại.

### 11.4 Validation trước khi xuất

Kiểm tra:

- mỗi edge trỏ tới node hợp lệ;
- mỗi kết luận có evidence;
- không có route bị gắn nhầm application;
- confidence/completeness khớp lý do;
- phần bị drop hoặc truncate được báo;
- diagram chỉ dùng architecture projection, không lấy toàn bộ graph kỹ thuật.

---

## 12. Độ phức tạp và hiệu năng

Quét file và parse thường tăng gần theo số file/kích thước source. Resolver không thể
cam kết luôn O(n), vì chi phí còn phụ thuộc:

- số quan hệ truyền giá trị;
- số candidate mỗi call;
- số lần một fact được truyền;
- số anchor và đường phụ thuộc cần lần theo.

Cách kiểm soát:

- parse mỗi file một lần và dùng lại IR;
- chỉ kích hoạt phân tích sâu quanh architectural anchor;
- dùng index thay vì so mọi call với mọi definition;
- mỗi fact chỉ đưa vào worklist khi mới;
- giới hạn candidate/value/propagation;
- đo thời gian và bộ nhớ theo stage;
- về sau cache theo file và dependency.

Không dùng số dòng của resolver làm thước đo đúng/sai. Phải đo coverage L3, thời gian,
bộ nhớ và chi phí bảo trì.

---

## 13. Giới hạn của static analysis

Không thể xác định chắc chắn khi source không chứa dữ liệu quyết định:

```python
handler_name = config["handler"]
handler = getattr(module, handler_name)
handler()
```

Nếu không có configuration:

```text
status: runtime
reason: đích gọi phụ thuộc config["handler"]
evidence: app.py:12
```

Hoặc:

```python
plugin = load_plugin_from_database()
plugin.execute()
```

Source không cho biết plugin cụ thể. Người đọc code cũng phải xem database/runtime.
Kết quả đúng là nói chưa biết, không phải chọn một class có vẻ hợp lý.

Các giới hạn khác:

- monkey patching;
- import động;
- reflection;
- code generation;
- dependency injection tùy runtime;
- framework/plugin chưa có rule;
- source root hoặc version không xác định.

---

## 14. Hiện trạng và khoảng cách tới đích

Code hiện tại đã có các khối V2 nhưng chưa đồng nghĩa đã đạt kiến trúc trong tài liệu.

| Phần | Hiện trạng cần hiểu |
|---|---|
| Inventory/frontend/IR | Đã có code |
| Resolver + Dataflow | Đã có code toàn chương trình và budgets; cần đo lại theo câu hỏi L3 |
| Framework adapters | Đã có FastAPI, SQLAlchemy/SQLModel và HTTP client ở mức hiện tại |
| Registration | Đã có operation/object data; cần kiểm chứng execution context và object precision |
| Graph | Hiện còn node/cạnh function/class; cần tách architecture projection khỏi diagnostic detail |
| Component synthesis | Chưa có contract và kiểm chứng đầy đủ cho service/business/repository layer |
| Event/config relationships | Chưa hoàn thành theo đề bài gốc |
| Output | Đã sinh Markdown/Mermaid/JSON/UI; diagram hiện chủ yếu route/entity/external, chưa phải component diagram hoàn chỉnh |
| Evaluation/examples | Tạm hoãn theo quyết định hiện tại |

Không xóa resolver chỉ vì nó sâu. Trước tiên:

1. khóa câu hỏi kiến trúc và output contract;
2. viết fixture theo quan hệ L3;
3. đo phần resolver nào thực sự đóng góp;
4. giữ, đơn giản hóa hoặc chuyển sang diagnostic dựa trên bằng chứng.

---

## 15. Thứ tự triển khai tiếp theo

### Giai đoạn A — Chốt requirement

- chốt node/cạnh được phép có trong architecture graph;
- chốt mức chi tiết L3 Markdown và diagram;
- cập nhật use case/scenario/spec;
- xác định component synthesis tối thiểu.

### Giai đoạn B — Khóa bằng test

- route → application/component;
- route → service → repository → entity;
- component → external system;
- unresolved không tạo semantic edge;
- hai application cùng type không bị trộn;
- conditional/unreached registration không bị khẳng định quá mức;
- graph chi tiết không tràn vào diagram L3.

### Giai đoạn C — Điều chỉnh implementation

- thêm architectural anchors và targeted traversal;
- tách diagnostic/evidence graph khỏi architecture projection;
- bổ sung component synthesis;
- giữ budgets và diagnostics;
- không refactor phần không phục vụ acceptance criteria.

### Giai đoạn D — Đồng bộ output

- L3 tập trung vào application/component và quan hệ;
- bảng route/entity vẫn có thể chi tiết để tra cứu;
- diagram tổng quát;
- graph JSON có contract kiến trúc rõ;
- drill-down dẫn về evidence.

### Giai đoạn E — Đo và tối ưu

- chỉ thực hiện sau khi requirement/output đã ổn định;
- đo precision/recall theo từng loại quan hệ kiến trúc;
- đo thời gian/bộ nhớ;
- tối ưu dựa trên bottleneck thật.

---

## 16. Tiêu chí hoàn thành V2

V2 chỉ hoàn thành khi:

1. Repo phẳng, trộn ngôn ngữ hoặc chia folder khác nhau không làm mất file.
2. Nhóm ngôn ngữ không bị gọi nhầm là service.
3. Route được gắn đúng application/router và path có evidence.
4. Component model trả lời được các câu hỏi đã chốt ở mục 1.
5. Diagram chỉ trình bày mức L3, không liệt kê mọi function/variable.
6. Function-level analysis chỉ chạy/được giữ khi phục vụ evidence hoặc diagnostic.
7. Unresolved không biến thành semantic edge suy đoán.
8. Runtime-dependent và budget-truncated được báo rõ.
9. Framework rules là tất định, có version/test và do người review.
10. AI không tạo hoặc sửa fact, edge hay rule.
11. Mọi quan hệ L3 truy ngược được về source.
12. Code, tài liệu và test cùng phản ánh một output contract.
13. Kết quả chất lượng/hiệu năng chỉ được công bố sau khi đo trên đúng phiên bản.
