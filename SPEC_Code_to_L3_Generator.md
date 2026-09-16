# SPEC — Code → Architecture / L3 Generator V2

> Trạng thái: đặc tả mục tiêu sau khi thu hẹp lại theo đề bài gốc, ngày 16/09/2026.
> Code hiện tại mới phù hợp một phần; xem mục 13. EVALUATION và examples tạm hoãn
> cho tới khi requirement, use case và architecture ổn định.

## 0. Tổng quan

### 0.1 Một câu về sản phẩm

Một CLI tool đọc source repository bằng static analysis, tổng hợp application/component
và các quan hệ API, DB, external system, event thành tài liệu L3 và dependency diagram;
mỗi kết luận đều có evidence truy về source.

### 0.2 Ranh giới quan trọng nhất

Tool có thể đọc tới function, parameter, assignment và call để tìm bằng chứng. Nhưng:

- function/call graph đầy đủ không phải sản phẩm chính;
- diagram L3 không hiển thị mọi function/class/variable;
- resolver chỉ cần sâu tới mức trả lời câu hỏi kiến trúc đã chốt;
- Repository Knowledge Graph tổng quát là dự án khác.

Nguyên tắc:

> Analyze deep enough; present at L3.

### 0.3 Tài liệu có vai trò gì?

| Tài liệu | Vai trò |
|---|---|
| [Đề bài](Đề%20bài.md) | Mục tiêu gốc |
| [USE_CASES](docs/USE_CASES.md) | Người dùng cần gì |
| [SCENARIOS](docs/SCENARIOS.md) | Hành vi cụ thể cần đạt |
| [ARCHITECTURE_V2_IDEA](docs/ARCHITECTURE_V2_IDEA.md) | Pipeline và quyết định thiết kế |
| File này | Contract để code/test |
| [HANDOFF](docs/HANDOFF.md) | Hiện trạng, kết quả kiểm chứng và việc tiếp theo |

Nếu mâu thuẫn, phải sửa tài liệu đầu nguồn trước rồi mới sửa code. Không dùng code hiện
tại để hợp thức hóa requirement sai.

## 1. Mục tiêu và câu hỏi kiến trúc

### 1.1 Mục tiêu

- Giảm thời gian hiểu một codebase/service chưa quen.
- Tạo bản L3 ban đầu gần với code thực tế.
- Cho người đọc tự kiểm chứng kết luận.
- Phân biệt rõ “không có” với “tool chưa đọc được”.
- Có architecture model để tích hợp về sau.

### 1.2 Câu hỏi bắt buộc

1. Repository có application/component nào?
2. Entry point ở đâu?
3. Application/component cung cấp API nào?
4. API được component nào xử lý?
5. Component nào phụ thuộc component nào?
6. Component nào đọc hoặc ghi data entity/table nào?
7. Component nào gọi external system?
8. Event/queue/configuration quan trọng nào được phát hiện?
9. Coverage và giới hạn của lần phân tích là gì?

Một chức năng resolver mới chỉ thuộc MVP nếu chứng minh nó giúp trả lời ít nhất một
câu hỏi trên hoặc giúp tránh một kết luận sai tương ứng.

## 2. Phạm vi MVP

### 2.1 Trong phạm vi

- Input là thư mục source local.
- Kiểm kê file theo từng file và ngôn ngữ, không theo giả định folder = service.
- Frontend phân tích hiện tại: Python.
- Framework/application: FastAPI/Starlette ở phạm vi rule đã kiểm thử.
- Data model: SQLAlchemy/SQLModel ở phạm vi rule đã kiểm thử.
- External HTTP: httpx/requests ở phạm vi rule đã kiểm thử.
- Module/package và entry point.
- Application/router/route registration.
- Component candidate: application, API-facing component, service/business,
  repository/data-access khi có bằng chứng.
- Data entity/table.
- External system.
- Event/queue/configuration: thuộc mục tiêu gốc nhưng chỉ được công bố cho adapter đã
  triển khai; phần chưa triển khai phải ghi rõ.
- Quan hệ component-level.
- Evidence về module/function/call khi cần giải thích kết luận.
- AI tùy chọn chỉ cho description và diễn đạt finding.
- Markdown, Mermaid, JSON và UI chỉ đọc output.

### 2.2 Ngoài phạm vi MVP

- Static analysis đầy đủ cho mọi semantics Python.
- Resolve mọi function/method call.
- Toàn bộ Repository Knowledge Graph mức function/class.
- Query/search API hoặc graph database.
- Incremental scan/cache.
- Dynamic execution/import/exec source đầu vào.
- Khẳng định deployment topology khi source/config không đủ.
- Mọi ngôn ngữ/framework ngoài adapter đã triển khai.
- AI tạo fact, relation, edge hoặc framework rule.
- CI integration và architecture drift.
- Change impact/test impact.
- Chỉnh sửa source đầu vào.

### 2.3 Phần tạm hoãn

Trong giai đoạn chốt lại requirement:

- không cập nhật EVALUATION;
- không cập nhật examples;
- không dùng số đo V1 để chứng minh V2;
- chưa tối ưu hiệu năng khi chưa xác định bottleneck theo contract mới.

## 3. Nguyên tắc bắt buộc

### 3.1 Read-only static analysis

Không được:

- import module của repository đầu vào;
- chạy code đầu vào;
- gọi `exec`/`eval`;
- tự cài dependency của repository;
- sửa file đầu vào.

### 3.2 Deterministic facts, optional AI text

| Dữ liệu | Nguồn |
|---|---|
| File/language/scope/import | parser và rule tất định |
| Application/component/route/entity | static analysis + adapter đã duyệt |
| Dependency edge | fact/evidence tất định |
| Confidence/completeness/status | rule tất định |
| Description | AI tùy chọn |
| Finding | detector tất định; AI chỉ được rephrase |

Tắt AI không được thay đổi IAM, graph hoặc diagram.

### 3.3 Không đoán để làm diagram đầy hơn

- Không suy type từ cách viết hoa.
- Không suy framework từ tên biến `app`, `router`.
- Không suy service từ folder.
- Không coi method `mount` là Starlette nếu receiver chưa được xác định.
- Không nối route tới entity chỉ vì tên cùng miền nghiệp vụ.
- Không biến unresolved raw call thành semantic edge nét đứt.

### 3.4 Evidence bắt buộc

Mỗi node/cạnh L3 phải có ít nhất một evidence:

- file;
- dòng bắt đầu/kết thúc;
- loại fact/rule;
- đường suy luận rút gọn nếu kết luận qua nhiều bước.

Nếu evidence bị truncate phải ghi rõ.

### 3.5 Confidence và completeness tách biệt

- `confidence`: mức chắc rằng loại kết luận đúng.
- `completeness`: mức đủ của thuộc tính/đường quan hệ.

Ví dụ route chắc chắn tồn tại nhưng prefix phụ thuộc runtime:

```text
confidence=exact
completeness=partial
reason="prefix phụ thuộc settings.API_PREFIX"
```

### 3.6 Trạng thái thực thi không đồng nghĩa trạng thái resolve

Resolver xác định được `setup` không chứng minh `setup()` được chạy.

Registration dùng các trạng thái:

| Trạng thái | Nghĩa |
|---|---|
| `declared` | Có operation trong source |
| `registered_candidate` | Đã gắn được parent/child/endpoint bằng static evidence |
| `potentially_reachable` | Có bằng chứng call context có thể chạy |
| `runtime_confirmed` | Chỉ có từ runtime data; static-only MVP thường không có |

Output không được gọi `declared` là active route nếu thiếu bằng chứng cần thiết.

## 4. Input và CLI contract

### 4.1 Input

```bash
l3gen <source-dir> [options]
```

Input có thể là repo, monorepo hoặc một thư mục con. File được nhận diện độc lập.

Analysis Context cố thu:

- source root/package root;
- phiên bản ngôn ngữ;
- dependency/framework version;
- manifest/config làm bằng chứng.

Thiếu context không làm crash. Kết quả liên quan phải partial/unresolved.

### 4.2 Tùy chọn đang công khai

| Tùy chọn | Ý nghĩa |
|---|---|
| `-o, --output` | thư mục output |
| `--no-ai` | không gọi AI |
| `--exclude` | tên thư mục bỏ qua |
| `--fail-on-empty` | exit lỗi nếu không có route/entity |
| `-v, --verbose` | hiển thị chi tiết |
| `--version` | phiên bản tool |

UI:

```bash
l3gen ui <output-dir> [-p PORT] [--no-browser]
```

### 4.3 Lỗi dự kiến

- Source không tồn tại/không có source phù hợp: exit 1, không traceback.
- File parse lỗi: ghi lỗi, tiếp tục.
- Một ngôn ngữ chưa hỗ trợ: ghi inventory/coverage, tiếp tục phần khác.
- Mọi phần đều chưa hỗ trợ: sinh thông báo rõ; không giả vờ repo rỗng.
- AI thiếu key/lỗi: tiếp tục static pipeline.
- Lỗi bất ngờ: exit 2 với thông báo gọn.

## 5. Dữ liệu trung gian

### 5.1 Ba lớp dữ liệu

Không gộp ba lớp thành một khái niệm:

1. **Semantic IR:** fact cú pháp/ngữ nghĩa trung lập.
2. **Evidence/Diagnostic Model:** resolution result, raw call, function path, phần chưa
   hiểu và budget.
3. **Architecture IAM:** application/component/API/data/external/event và quan hệ L3.

Implementation có thể lưu chung file trong giai đoạn chuyển đổi, nhưng schema phải phân
biệt vai trò. Public architecture contract không mặc nhiên bao gồm toàn bộ IR.

### 5.2 SourceLocation

```text
file
line_start
line_end
```

Đường dẫn tương đối với input root; không ghi absolute path máy chạy vào artifact công
khai.

### 5.3 Evidence

Tối thiểu:

```text
id
kind
location
rule_or_fact
summary
parent_evidence_ids[]
truncated
```

Một đường evidence dài có thể rút gọn nhưng không được mất vị trí đầu/cuối và lý do.

### 5.4 Resolution result

```text
status: resolved | candidates | unresolved | runtime
targets[]
reason
evidence_ids[]
truncated
```

`resolved` nghĩa là có một target trong phần mô hình đã hỗ trợ; không phải chứng minh
call chắc chắn chạy.

## 6. Architecture IAM contract

### 6.1 Node types

| Loại | Thuộc tính tối thiểu |
|---|---|
| Repository | id, name |
| Application | id, framework/type, boundary status |
| Component | id, name, role, boundary status |
| API | method, path, handler, registration status |
| DataEntity | class/table, key/FK nếu biết |
| ExternalSystem | host/name/protocol nếu biết |
| Event | name/topic, direction nếu biết |
| Configuration | key/source; không xuất secret value |

Mỗi node còn có:

- confidence;
- completeness;
- reason khi không exact/full;
- evidence_ids.

### 6.2 Component role

Giá trị gợi ý:

- `api`;
- `service`;
- `repository`;
- `worker`;
- `integration`;
- `unknown`.

Không gán role chỉ dựa vào tên folder/class. Role cần framework marker, registration,
call/effect hoặc rule convention đã duyệt. Nếu chỉ có tín hiệu yếu, dùng
`unknown` hoặc candidate với lý do.

### 6.3 Edge types

| Edge | Source → target |
|---|---|
| `contains` | repository/application → component |
| `exposes` | application/component → API |
| `handled_by` | API → component |
| `depends_on` | component → component |
| `reads` | component/API → DataEntity |
| `writes` | component/API → DataEntity |
| `calls_external` | component/API → ExternalSystem |
| `publishes` | component → Event |
| `consumes` | component → Event |
| `mounts` | application → application |
| `registers` | application/router component → API/router |

Mỗi edge có:

- source_id/target_id;
- confidence/completeness;
- evidence_ids;
- reason/condition;
- status nếu phụ thuộc registration.

Không có edge `calls` giữa mọi function trong public architecture graph. Call path
nằm ở Evidence/Diagnostic Model.

### 6.4 Application boundary

Giá trị:

- `confirmed_from_config` nếu manifest/runtime config tĩnh đủ rõ;
- `candidate` nếu suy từ framework composition;
- `unknown` nếu thiếu bằng chứng.

Không gọi language group là application hoặc service.

## 7. Pipeline contract

```text
File Inventory + Analysis Context
→ Language Frontends
→ Common Semantic IR
→ Architectural Anchor Discovery
→ Targeted Resolver + Dataflow ↔ Library Models
→ Framework Adapters
→ Registration & Composition
→ Component Synthesis + Architecture IAM
→ L3 Projection + Validation + Outputs
```

### 7.1 File Inventory

- Quét theo extension đã biết.
- Sắp xếp kết quả ổn định.
- Ghi excluded/unsupported/error/budget.
- Không mất file vì repo phẳng hoặc trộn ngôn ngữ.

### 7.2 Language Frontend

Python frontend tạo import/definition/scope/assignment/call/return/parameter/
inheritance/decorator/condition/location.

Frontend không kết luận framework semantics.

### 7.3 Anchor Discovery

Tìm candidate cho entry point, app/router, route registration, entity, external/event/
config và layer. Candidate chưa phải architecture fact.

### 7.4 Targeted Resolver + Dataflow

Bắt buộc hỗ trợ trong đường liên quan anchor:

- import alias và name binding theo scope;
- constructor trực tiếp;
- alias qua phép gán;
- type annotation;
- argument → parameter;
- return → call result;
- thuộc tính cần thiết;
- inheritance cần thiết;
- library type/effect summary đã duyệt.

Resolver dùng index/worklist và budget. Không so mọi call với mọi definition bằng vòng
lặp toàn cục nếu có thể index.

Chưa bắt buộc:

- reflection đầy đủ;
- context-sensitive points-to hoàn chỉnh;
- dynamic import/plugin;
- mọi callback;
- phân biệt mọi allocation trong mọi vòng lặp.

### 7.5 Framework Adapters

Chỉ khớp symbol đầy đủ và version range. Mỗi rule có positive/negative test.

Ví dụ operation chuẩn:

- `RegisterEndpoint`;
- `AttachRouter`;
- `MountApplication`;
- `ReadEntity`;
- `WriteEntity`;
- `CallExternal`;
- `PublishEvent`;
- `ConsumeEvent`.

### 7.6 Registration & Composition

Giữ object identity, parent/child, prefix/path, condition, call context và evidence.
Ghép full path theo application tree. Không trộn hai object cùng type.

### 7.7 Component Synthesis

Tổng hợp operation/evidence thành component. Mỗi quyết định grouping phải có rule và
evidence. Nếu chưa đủ, giữ module/application node hoặc role unknown; không ép graph
trông đẹp.

### 7.8 Validation

Trước output:

- node id duy nhất;
- edge target tồn tại;
- edge có evidence;
- không có unresolved semantic edge;
- registration status hợp lệ;
- confidence/completeness có reason khi cần;
- mọi dropped/truncated item được báo;
- architecture projection không chứa node function/variable ngoài contract.

## 8. Output contract

### 8.1 Files

| File | Vai trò |
|---|---|
| `L3.md` | tài liệu đọc bằng mắt |
| `diagram.mmd` | component/dependency diagram tổng quát |
| `graph.json` | public architecture graph |
| `IAM.json` | architecture IAM + evidence/diagnostic theo schema rõ |
| `inventory.json` | coverage theo file |
| `findings.json` | finding tất định |
| `descriptions.json` | text AI tùy chọn |
| `run.json` | thời gian, budgets, version và metrics lần chạy |

Trong giai đoạn code chuyển đổi, file có thể còn trường legacy. README/HANDOFF phải
nói rõ; không coi legacy field là contract mới.

### 8.2 L3.md

Cấu trúc mục tiêu:

1. Tổng quan và coverage.
2. Applications và Components.
3. API Routes.
4. Data Entities/Stores.
5. External Systems.
6. Events/Configurations quan trọng.
7. Component Dependencies.
8. Evidence/Drill-down.
9. Findings.
10. Known Limitations.

Bảng route/entity có thể chi tiết. Call graph mọi function không phải mục chính.

### 8.3 diagram.mmd

- Hiển thị application/component/API group/data store/external/event ở mức đọc được.
- Không hiển thị mọi function/class/variable.
- Với nhiều route, nhóm route theo component/application; bảng L3 giữ chi tiết.
- Không vẽ unresolved semantic edge.
- Nếu phải rút gọn, ghi rõ và dẫn tới JSON/evidence.
- Deterministic: cùng IAM kiến trúc cho cùng diagram.

### 8.4 graph.json

Public node/edge chỉ theo mục 6. Diagnostic function graph nếu còn cần phải:

- nằm trong namespace/file riêng; hoặc
- được gắn rõ `diagnostic=true` và không được UI/diagram coi là L3 mặc định.

Đích mong muốn là file riêng để contract không nhập nhằng.

### 8.5 Known Limitations

Luôn có, kể cả rỗng. Bao gồm:

- unsupported language/framework/version;
- parse errors;
- missing analysis context;
- unresolved/candidates/runtime;
- conditional/unreached registration;
- truncated/budget exceeded;
- adapter/domain chưa triển khai;
- boundary candidate/unknown.

## 9. AI contract

### 9.1 Description

Input chỉ gồm architecture fact đã xác minh và evidence summary cần thiết. Output chỉ
gồm id + text. Không có field để sửa fact.

### 9.2 Reviewer

Detector tất định tạo finding type + evidence. AI, nếu dùng, chỉ rephrase summary.
Tắt AI vẫn giữ cùng finding ids và facts.

### 9.3 V2.5 rule proposal

Agent đề xuất rule là tương lai, không thuộc V2. Rule chỉ được dùng sau human review,
test và commit. Agent không tự kích hoạt rule trong lần phân tích.

## 10. Acceptance Criteria

### 10.1 Inventory/context

- Repo phẳng/trộn ngôn ngữ không mất file hỗ trợ.
- Hai source root cùng module name không bị gộp.
- Unsupported và parse errors xuất hiện trong coverage.
- Không có folder = service heuristic cứng.

### 10.2 Framework semantics

- `FastAPI()`, `APIRouter()`, decorator, `include_router`, `mount`,
  `add_api_route` được xử lý trong phạm vi version/test.
- Object cùng type không bị trộn.
- Method cùng tên trên class khác không kích hoạt framework operation.
- Conditional registration giữ condition.
- Declared operation chưa reachable không bị gọi active mà không có lý do.

### 10.3 Component relations

Fixture tối thiểu chứng minh:

```text
Route → API Component → Service → Repository → DataEntity
Service/Integration → ExternalSystem
Component → Event (khi adapter event được triển khai)
```

Mỗi edge phải có evidence path. Nếu một đoạn không resolve, chuỗi dừng đúng chỗ và
ghi limitation; không nối tắt bằng đoán.

### 10.4 Presentation

- Diagram không có node function/variable mặc định.
- 500 function không biến thành 500 node L3.
- Route/entity table vẫn tra cứu được.
- Architecture graph chỉ có node/edge contract.
- Evidence drill-down mở được `file:line`.

### 10.5 AI boundary

Chạy cùng source có/không AI:

- Architecture IAM bằng nhau.
- graph.json bằng nhau.
- diagram.mmd bằng nhau.
- chỉ description/rephrased text khác hoặc thiếu.

### 10.6 Determinism và safety

- Không import/execute source.
- Hai lần chạy cùng input/config tạo cùng deterministic artifacts; `run.json` có thể
  khác thời gian.
- File lỗi không kéo sập toàn run.
- Budget được kiểm thử bằng fixture gây nhiều candidate/cycle.

### 10.7 Quality gate trước khi tuyên bố hoàn thành

- Requirement, scenario, spec, code và test cùng contract.
- Full test suite chạy trên đúng source hiện tại.
- Không dùng số đo V1 cho V2.
- EVALUATION chỉ thực hiện sau khi contract ổn định.
- Known gaps được ghi thẳng.

## 11. Non-functional requirements

### 11.1 Hiệu năng

Không cam kết O(n) cho toàn pipeline. Phải đo theo stage:

- inventory;
- parse/frontend;
- anchor discovery;
- resolution/dataflow;
- adapters/composition;
- synthesis/validation;
- output.

Metrics gồm số file/byte/fact/anchor/call candidate/propagation, thời gian và peak memory
với cách đo được mô tả.

### 11.2 Budgets

Có giới hạn cấu hình hoặc hằng số rõ cho:

- file count/size;
- source bytes;
- candidates/call;
- values/slot;
- propagation;
- evidence path;
- output node/edge nếu cần.

Chạm budget không crash hoặc im lặng; phải ghi partial.

### 11.3 Bảo mật và riêng tư

- Không ghi secret value từ config.
- Không gửi source tới AI nếu chưa có contract/consent phù hợp; mặc định chỉ gửi fact
  tối thiểu cần cho description.
- Output không chứa absolute path máy người dùng.
- Không tải dependency của repo đầu vào.

### 11.4 Khả năng mở rộng

Thêm ngôn ngữ: frontend → Common Semantic IR.
Thêm framework: library model + adapter + tests.
Thêm output: đọc Architecture IAM, không parse source lại.

## 12. Cấu trúc implementation mục tiêu

Tên folder có thể thay đổi khi refactor; dependency direction mới là contract:

```text
inventory/context
      ↓
language_frontends → semantic_ir
      ↓
anchors → resolver/dataflow ↔ library_models
      ↓
framework_adapters → registration/composition
      ↓
component_synthesis → architecture_iam
      ↓
validation → markdown/diagram/architecture_graph/ui
```

Output/UI không import parser/AST. Adapter không tự quét filesystem. AI không được
import hoặc thay đổi analysis core.

## 13. Hiện trạng code và migration

Đây là snapshot tài liệu, không thay cho kiểm thử.

| Phần | Hiện trạng 16/09/2026 | Việc cần làm |
|---|---|---|
| Inventory | Có code kiểm kê đa ngôn ngữ | Bổ sung/chuẩn hóa Analysis Context |
| Python frontend/IR | Có code | Đối chiếu scope/source-root cases |
| Resolver/dataflow | Có worklist và budgets, chạy toàn program | Đo đóng góp, chuyển trọng tâm sang anchor-targeted |
| Library registry | Có builtin registry | Tách registry version và framework version range |
| FastAPI/SQLAlchemy/HTTP | Có adapter/extractor V2 | Kiểm thử composition/context/version |
| IAM | Còn trộn dữ liệu kiến trúc và kỹ thuật | Tách vai trò/schema |
| Graph | Có function/class/call nodes | Thêm architecture projection; diagnostic graph không là L3 chính |
| Component synthesis | Chưa hoàn chỉnh | Thiết kế rule/evidence và fixture |
| Event/config | Chưa hoàn chỉnh | Làm sau core relation nhưng phải báo unsupported |
| Mermaid | Hiện chủ yếu route/entity/external | Chuyển thành component diagram |
| Markdown/UI | Đã có code | Đồng bộ contract và cách hiển thị |
| Tests | Có suite lịch sử | Chạy lại sau khi code được đổi; không ghi số mới trước khi chạy |
| Evaluation/examples | Có artifact cũ | Tạm hoãn, không dùng làm bằng chứng V2 |

### 13.1 Thứ tự migration

1. Viết/đổi test theo mục 10.
2. Tạo Architecture IAM/projection mà chưa xóa diagnostic data cũ.
3. Thêm component synthesis tối thiểu.
4. Chuyển Mermaid/Markdown/UI sang architecture projection.
5. Giữ resolver hiện có, đo và chỉ đơn giản hóa phần không đóng góp.
6. Khi output mới ổn định, đánh dấu legacy schema và lên kế hoạch loại bỏ riêng.
7. Sau đó mới làm EVALUATION/examples.

Không xóa ồ ạt code resolver chỉ vì scope đổi. Cũng không tiếp tục mở rộng resolver
tổng quát nếu chưa có acceptance criterion L3 yêu cầu.

## 14. Definition of Done

MVP/V2 hoàn tất khi:

- trả lời được chín câu hỏi ở mục 1 trong phạm vi stack đã công bố;
- diagram là component/dependency diagram, không phải function graph;
- API/DB/external/event relations có evidence;
- unresolved/runtime/budget được trình bày trung thực;
- không có semantic edge dựa trên tên giống framework;
- AI không ảnh hưởng structural artifacts;
- test xác nhận safety, determinism, object identity và boundaries;
- code và tất cả tài liệu chính cùng một contract;
- giới hạn còn lại được ghi rõ, không dùng từ “hoàn tất” nếu chưa đo.
