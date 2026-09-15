# Platform Satellite Projects – Agentic SDLC Program

## 0. Mục tiêu chương trình

Chương trình xây dựng các **dự án vệ tinh / mini-product kỹ thuật độc lập**, có thể được sử dụng thực tế bởi developer, architect, platform team hoặc engineering team ngay sau MVP.

Các dự án được lựa chọn theo các nguyên tắc:

* Có **giá trị sử dụng độc lập**, không chỉ là POC hoặc một module phụ của dự án lớn.
* Scope phù hợp để một team **2–3 người triển khai trong 4–6 tuần**.
* Hạn chế ảnh hưởng tới các hệ thống/platform core đang vận hành.
* Ưu tiên read-only, analysis, recommendation hoặc non-blocking integration ở giai đoạn đầu.
* Có API, data model hoặc contract rõ để có thể tích hợp vào các platform lớn sau này.
* Có engineering depth phù hợp để intern/fresher thực hành một vòng phát triển sản phẩm đầy đủ.
* Đồng thời sử dụng tất cả dự án như các testcase thực tế để thử nghiệm và cải tiến **Agentic SDLC**.

---

# 1. Danh sách dự án

| #  | Project                                                       | Mục tiêu / Bài toán                                                                                                   | Input chính                                                                | Output / Sản phẩm                                                                                | Giá trị & hướng tích hợp                                                    | Capacity                 |
| -- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- | ------------------------ |
| 1  | **Shadow API Detector & API Consumer & Deprecation Explorer** | Phát hiện API có traffic nhưng chưa được quản lý; xác định consumer của API và đánh giá khả năng deprecate/remove API | API Catalog, traffic logs, exception rules, Service Catalog                | Shadow API inventory, API-consumer mapping, unused/deprecated API report, deprecation impact     | API Governance, Service Graph, Compliance, Change Impact Analyzer           | **2–3 người / 4–6 tuần** |
| 2  | **Reference Architecture Kit**                                | Cung cấp executable reference architecture cho các loại ứng dụng và quy mô khác nhau                                  | Application type, workload/sizing, NFR, architecture standards             | Reference architecture, sizing guidance, Diagram-as-Code model, architecture validation findings | Architecture Governance, AI Architecture Design, Diagram-as-Code, V-Builder | **2–3 người / 4–6 tuần** |
| 3  | **ADR Hub + Architecture Decision Miner**                     | Quản lý quyết định kiến trúc và tự phát hiện các decision quan trọng từ hoạt động development                         | ADR, MR, issue, design docs, review discussions                            | ADR registry, decision candidates, lifecycle/superseded relationships                            | Architecture Governance, Engineering Knowledge, AI Architecture context     | **2–3 người / 4–6 tuần** |
| 4  | **Tech Debt Radar (and Risk) + Tech Debt Miner**              | Quản lý technical debt/risk tập trung và tự động phát hiện debt candidates từ engineering artifacts                   | Code, TODO/FIXME, static analysis, MR findings, incidents, dependency data | Debt/risk inventory, severity, owner, aging, trend, automatically mined candidates               | Architecture Governance, Risk Management, planning/prioritization           | **2–3 người / 4–6 tuần** |
| 5  | **Trace → Sequence Diagram**                                  | Chuyển runtime distributed trace thành sequence diagram để hiểu interaction thực tế giữa các service                  | OpenTelemetry/APM traces                                                   | Sequence Diagram-as-Code, service interaction model, latency annotations                         | Observability, Architecture Explorer, runtime-vs-design comparison          | **2–3 người / 4–6 tuần** |
| 6  | **Code → Architecture / L3 Generator**                        | Reverse-engineer codebase để sinh tài liệu kiến trúc kỹ thuật/L3 và dependency model                                  | Source repository, configs, API definitions                                | L3 document, component/dependency diagrams, API/DB/event relationships                           | Engineering Knowledge, Architecture Governance, AI Design                   | **2–3 người / 4–6 tuần** |
| 7  | **Test Impact Analyzer**                                      | Từ code change xác định subset test cần chạy thay vì chạy toàn bộ test suite                                          | Code diff, source dependency graph, test history/coverage                  | Recommended test set, impacted tests, confidence/risk score                                      | Local dev loop, CI acceleration, Agentic SDLC feedback loop                 | **2–3 người / 4–6 tuần** |
| 8  | **Repository Knowledge Graph**                                | Biến source repository thành graph có cấu trúc để con người và AI hiểu codebase                                       | Source code, configuration, API specs, build metadata                      | Graph của modules/classes/functions/APIs/DB/events/dependencies                                  | Agentic SDLC Context, Code→L3, Change Impact, code search/reasoning         | **2–3 người / 4–6 tuần** |
| 9  | **API Traffic Replay Lab**                                    | Capture/sanitize/replay traffic thực tế để test version mới, mock service hoặc reproduce lỗi                          | HTTP traffic, API spec, target environment                                 | Replay scenarios, request datasets, behavior/diff report                                         | API Sandbox, automated testing, debugging, regression testing               | **2–3 người / 4–6 tuần** |
| 10 | **Change Impact Analyzer**                                    | Xác định phạm vi ảnh hưởng của một code/API/DB/config change trước khi merge/release                                  | MR/code diff, Repository Graph, API Catalog, Service Graph, DB metadata    | Impacted services/APIs/DB/events/tests, risk/impact report                                       | MR Review, Test Impact Analyzer, Release Governance, Agentic SDLC           | **2–3 người / 4–6 tuần** |
| 11 | **DB Migration Risk Analyzer**                                | Phân tích schema/migration change trước khi chạy để phát hiện breaking change và operational risk                     | Migration scripts, schema before/after, DB metadata                        | Breaking-change findings, lock/downtime/data-loss risk, rollback recommendations                 | DB Governance, MR Review, Change Impact Analyzer, CI Quality Gate           | **2–3 người / 4–6 tuần** |
| 12 | **Synthetic Test Data Factory**                               | Sinh dữ liệu test realistic nhưng không sử dụng dữ liệu production nhạy cảm                                           | DB schema, constraints, data-generation rules, scenarios                   | Consistent synthetic datasets, scenario packs, reset/seed scripts/APIs                           | Testing, Mock Data API, local dev environment, API Traffic Replay           | **2–3 người / 4–6 tuần** |
| 13 | **Data Lineage Lite**                                         | Tự động xác định luồng dữ liệu giữa database/table/column/pipeline ở mức đủ dùng cho developer                        | SQL, schema, dbt/ETL definitions, source code queries                      | Table/column lineage graph, upstream/downstream impact                                           | Data Architecture, Change Impact, DB Governance, Engineering Knowledge      | **2–3 người / 4–6 tuần** |
| 14 | **Flaky Test Detective**                                      | Phát hiện test không ổn định và phân tích pattern/nguyên nhân gây flaky                                               | CI test history, logs, execution time, environment metadata                | Flaky-test ranking, probability, failure patterns, probable root cause                           | CI/CD quality, Test Impact Analyzer, developer productivity                 | **2–3 người / 4–6 tuần** |
| 15 | **Request Journey Debugger**                                  | Theo dõi một request end-to-end qua service, DB, cache, event và external dependencies để debug nhanh                 | Trace ID/request ID, logs, OpenTelemetry traces, Service Graph             | Interactive request journey, latency/error hotspots, dependency timeline                         | Observability, debugging, Service Graph, Change Impact, AI troubleshooting  | **2–3 người / 4–6 tuần** |

---

# 2. Yêu cầu chung – Áp dụng Agentic SDLC

Tất cả các dự án trong chương trình được triển khai theo **Agentic SDLC**, coi đây vừa là phương pháp phát triển dự án, vừa là môi trường thực nghiệm để đánh giá và cải tiến quy trình phát triển phần mềm với AI Agent.

Mục tiêu không chỉ là sử dụng AI để hỗ trợ coding, mà để Agent tham gia xuyên suốt vòng đời:

**Requirement → Analyze / Impact Analysis → Solution & Design → Task Planning → Implementation → Testing → Review → MR → Release / Deploy → Verification → Feedback & Learning**

## Nguyên tắc Spec-first: Human không trực tiếp code

Nguyên tắc quan trọng nhất của chương trình là:

> **Developer không trực tiếp viết hoặc sửa production code như cách phát triển truyền thống.**

Vai trò chính của human là làm rõ và nâng chất lượng đầu vào cho AI Agent:

* Requirement / Problem statement.
* Detailed specification.
* Acceptance criteria.
* Examples và edge cases.
* Architecture và technical constraints.
* API/schema/data contracts.
* Test specification.
* Context và knowledge cần thiết.
* Review kết quả và đưa feedback.

AI Agent chịu trách nhiệm chính cho:

* phân tích và lập kế hoạch implementation;
* sinh source code;
* sinh và chạy test;
* xử lý lỗi;
* self-review;
* sửa review findings;
* chuẩn bị commit/MR;
* hỗ trợ release và verification.

Nếu code/output của AI không đạt chất lượng, **không ưu tiên sửa code thủ công ngay**.

Trước tiên cần tìm nguyên nhân ở đầu nguồn:

**Spec chưa đủ → Context thiếu → Constraint chưa rõ → Architecture chưa rõ → Test/Acceptance Criteria thiếu → Agent instruction/tool chưa phù hợp**

sau đó cải thiện các artifact đầu nguồn và yêu cầu Agent thực hiện lại.

Manual code modification chỉ nên được sử dụng như một exception để unblock, và cần ghi nhận lý do để phục vụ việc cải tiến Agentic SDLC.

Mục tiêu là từng bước chuyển:

> **Human writes code → Human specifies intent & constraints → Agent produces implementation → Human validates outcome.**

## Các nguyên tắc khác

* **Human-in-the-loop tại bất kỳ bước nào.** Developer/reviewer có thể chỉnh specification, comment, approve, reject hoặc yêu cầu Agent làm lại.
* **Git là Source of Truth.** Requirements, specs, architecture, ADR, API/schema, implementation plan, tests và các engineering artifacts quan trọng cần được version hóa và reviewable.
* **Context được quản lý có cấu trúc.** Agent cần nhận đúng context từ requirements, architecture, code, API/DB, ADR, standards, historical findings và các artifact liên quan.
* **Mỗi bước phải tạo artifact/evidence kiểm chứng được.** Không coi một task hoàn thành chỉ vì Agent báo `done`.
* Workflow phải hỗ trợ nhiều vòng **implement → test → review → fix → re-test → re-review**, đồng thời giữ context của các vòng trước.
* Cần đảm bảo traceability: **Requirement → Spec → Decision → Task → Code/MR → Test → Finding/Fix → Release.**

## Scope và timebox

Tất cả các project áp dụng chung:

> **2–3 người / 4–6 tuần**

Đây là **timebox/capacity chung của chương trình**, không có nghĩa các project có độ khó tương đương.

Scope MVP được phép **scale down hoặc scale up** tùy theo:

* độ phức tạp của bài toán;
* năng lực của team;
* data/tool readiness;
* tốc độ thực tế khi triển khai bằng Agentic SDLC;
* mức độ tham vọng của team.

Ví dụ với project phức tạp có thể giới hạn:

* một technology stack;
* một repository;
* một database engine;
* một data source;
* một số use case/rule quan trọng;
* read-only analysis;
* best-effort/limited recall.

Ngược lại, nếu project cơ bản hoàn thành sớm, team có thể mở rộng:

* thêm integration;
* thêm data source;
* tăng UX;
* tăng automation;
* hỗ trợ thêm stack/use case;
* pilot với user/data thực tế.

Nguyên tắc là:

> **Fixed time & capacity, variable scope — ưu tiên một MVP nhỏ nhưng hoàn chỉnh và dùng được hơn một scope lớn nhưng dở dang.**

## Feedback loop cho Agentic SDLC

Mỗi project đồng thời là một testcase để đánh giá Agentic SDLC.

Trong quá trình thực hiện cần ghi nhận:

* thiếu specification;
* thiếu context;
* Agent chọn sai solution;
* design/code chưa đạt;
* test thiếu;
* review findings;
* retry/rework;
* human intervention;
* manual code intervention;
* tool limitation;
* workflow stage gây chậm.

Cuối mỗi project/team cần tổng hợp:

**What worked → What failed → Why → What upstream artifact was missing → Human intervention needed → Process/tool/context improvements**

Các feedback này được đưa ngược lại để liên tục cải tiến:

* specification templates;
* context/knowledge layer;
* agent instructions;
* reusable skills/tools;
* quality gates;
* review process;
* mức độ tự động hóa.

Mục tiêu cuối cùng là vừa tạo ra các **sản phẩm có thể sử dụng thực tế**, vừa hình thành và kiểm chứng một **AI-native software development process** có khả năng áp dụng rộng hơn trong tổ chức.

**Capacity chung:** 2–3 người / 4–6 tuần / dự án.
 # 3. Mô tả chi tiết dự án

## 3.1 Shadow API Detector & API Consumer & Deprecation Explorer

### Mục tiêu

Xây dựng công cụ phân tích traffic thực tế để:

1. Phát hiện API đang được sử dụng nhưng chưa đăng ký/quản lý trong API Catalog.
2. Xác định consumer thực tế của từng API.
3. Hỗ trợ đánh giá API nào có thể deprecate/remove và tác động của việc đó.

### Phạm vi MVP

Tool nhận dữ liệu từ:

* API Catalog;
* traffic log từ Cloudflare/API Gateway/Ingress;
* danh sách domain/endpoint ngoại lệ;
* Service Catalog hoặc ownership data nếu có.

Hệ thống normalize:

* domain;
* HTTP method;
* URL path;
* query parameters;
* trailing slash;
* dynamic path parameters.

Ví dụ:

`/users/123`, `/users/456`

được nhận diện thành:

`/users/{id}`

Sau đó đối chiếu với API Catalog để phân loại:

* Registered API;
* Shadow API;
* Exception;
* Unknown / Need Review.

Consumer Explorer sử dụng metadata từ traffic để xác định service/client đang gọi API.

Deprecation Explorer tìm:

* API không còn traffic;
* API rất ít traffic;
* API đã deprecated nhưng vẫn còn consumer;
* consumer cần migrate trước khi remove API.

### Output

Dashboard/inventory gồm:

* endpoint/method/domain;
* traffic volume;
* first seen / last seen;
* catalog status;
* consumer;
* owner;
* confidence score;
* deprecation risk.

### Điểm kỹ thuật chính

* Endpoint pattern inference.
* Catalog matching.
* Consumer identification.
* False-positive handling.
* Exception rule engine.
* Traffic aggregation.
* Confidence scoring.

### Giá trị / hướng tích hợp

Có thể sử dụng trực tiếp trong API Governance và sau này cung cấp dữ liệu cho:

**Service Graph → Change Impact Analyzer → Compliance → API Lifecycle Management.**

**Capacity:** 2–3 người / 4–6 tuần.

---

## 3.2 Reference Architecture Kit

### Mục tiêu

Xây dựng bộ **Reference Architecture có khả năng thực thi bằng code**, thay vì chỉ là tài liệu tham khảo.

Kit hỗ trợ:

* lựa chọn kiến trúc theo loại ứng dụng;
* sizing theo workload;
* sinh architecture model ban đầu;
* kiểm tra một thiết kế có phù hợp với reference architecture và standards hay không.

### Phạm vi MVP

Hỗ trợ khoảng 5 nhóm ứng dụng:

* LMS;
* Chat / Messaging;
* AI Agent;
* E-commerce;
* Internal Knowledge Platform.

Mỗi loại có các workload profile:

* Small;
* Medium;
* Large;
* Custom.

Sizing dimension tùy từng loại ứng dụng, ví dụ:

* DAU;
* peak RPS;
* concurrent connections;
* orders/day;
* documents/search QPS;
* LLM request/token volume.

Reference architecture được định nghĩa bằng YAML/DSL gồm:

* components;
* relationships;
* NFR baseline;
* security baseline;
* sizing rules;
* mandatory rules;
* decision rules;
* alternatives/trade-offs.

Tool có hai luồng chính:

`generate`: requirements/workload → architecture model.

`validate`: current architecture → findings.

### Output

* Reference Architecture.
* Sizing guidance.
* Architecture model.
* Diagram-as-Code input.
* Reference L2 skeleton.
* Validation findings.

### Điểm kỹ thuật chính

* Architecture DSL/schema.
* Sizing model.
* Rules engine.
* Decision tree.
* Architecture validation.
* Integration với Diagram-as-Code.

### Giá trị / hướng tích hợp

Là nguồn deterministic knowledge cho:

**Architecture Governance → AI Architecture Design → AI Review → V-Builder.**

**Capacity:** 2–3 người / 4–6 tuần.

---

## 3.3 ADR Hub + Architecture Decision Miner

### Mục tiêu

Xây dựng nơi quản lý tập trung các **Architecture Decision Record (ADR)** và tự động phát hiện những quyết định kỹ thuật quan trọng đang nằm rải rác trong MR, issue, design document hoặc discussion.

### Phạm vi MVP

ADR Hub hỗ trợ lifecycle:

* Proposed;
* Accepted;
* Rejected;
* Deprecated;
* Superseded.

ADR có thể liên kết với:

* System;
* Service;
* Repository;
* Project;
* Architecture document;
* Other ADR.

Architecture Decision Miner sử dụng rule + AI để scan:

* MR description;
* review discussions;
* issues;
* design documents;
* technical discussions.

Tool tìm các dấu hiệu của architectural decision như:

* lựa chọn database;
* communication protocol;
* caching strategy;
* deployment model;
* consistency model;
* security mechanism;
* framework/platform selection.

Miner chỉ tạo **ADR candidate** cùng evidence; human quyết định có chính thức tạo ADR hay không.

### Output

* ADR Registry.
* Decision history.
* ADR relationship graph.
* Candidate decisions.
* Source/evidence của mỗi decision.

### Điểm kỹ thuật chính

* Decision extraction.
* Candidate scoring.
* Semantic similarity.
* Duplicate detection.
* Superseded relationships.
* Search/indexing.

### Giá trị / hướng tích hợp

Biến architectural decision thành organizational knowledge có cấu trúc, hỗ trợ:

**Architecture Governance → Engineering Knowledge → AI Architecture → Agentic SDLC Context.**

**Capacity:** 2–3 người / 4–6 tuần.

---

## 3.4 Tech Debt Radar (and Risk) + Tech Debt Miner

### Mục tiêu

Xây dựng inventory tập trung cho technical debt và engineering risk, đồng thời tự động tìm debt/risk candidate từ source code và engineering artifacts.

### Phạm vi MVP

Tech Debt Radar quản lý:

* system/service/repository;
* debt/risk category;
* severity;
* owner;
* age;
* due date;
* remediation plan;
* status.

Dashboard thể hiện:

* debt distribution;
* debt aging;
* overdue;
* severity;
* trend theo thời gian.

Tech Debt Miner scan:

* TODO/FIXME;
* static-analysis findings;
* duplicated code;
* deprecated dependencies;
* unresolved MR findings;
* architecture findings;
* repeated incidents.

Có thể mở rộng sang engineering risk như:

* single point of failure;
* unsupported runtime;
* high-risk dependency;
* missing ownership;
* outdated technology;
* unresolved critical finding.

### Output

* Debt/risk inventory.
* Risk score.
* Aging/trend dashboard.
* Automatically mined candidates.
* Owner/remediation tracking.

### Điểm kỹ thuật chính

* Multi-source normalization.
* Duplicate/grouping.
* Candidate mining.
* Risk scoring.
* Lifecycle management.

### Giá trị / hướng tích hợp

Hỗ trợ Architecture Governance và engineering planning; về sau liên kết:

**Debt/Risk ↔ Architecture ↔ ADR ↔ Incident ↔ Change.**

**Capacity:** 2–3 người / 4–6 tuần.

---

## 3.5 Trace → Sequence Diagram

### Mục tiêu

Chuyển distributed runtime trace thành sequence diagram dễ đọc để developer/architect hiểu interaction thực tế giữa các service mà không phải đọc hàng chục hoặc hàng trăm spans.

### Phạm vi MVP

Input:

* OpenTelemetry trace;
* hoặc trace export từ APM.

Tool reconstruct interaction giữa:

* service;
* API;
* database;
* cache;
* message broker;
* external dependency.

Technical span quá chi tiết có thể được collapse để diagram tập trung vào business/system interaction quan trọng.

Ví dụ:

**Checkout → Order → Payment → Redis → Payment Gateway**

được chuyển thành sequence diagram hoàn chỉnh.

Có thể annotate:

* latency;
* error;
* async interaction;
* retries.

### Output

* Sequence Diagram-as-Code.
* Service interaction model.
* Latency annotations.
* Error annotations.
* Runtime dependency list.

### Điểm kỹ thuật chính

* Trace-tree reconstruction.
* Parent-child correlation.
* Span normalization.
* Async trace handling.
* Noise reduction.
* Diagram generation.

### Giá trị / hướng tích hợp

Tạo bridge giữa:

**Observability ↔ Architecture.**

Về sau có thể thực hiện:

**Designed Sequence ↔ Runtime Sequence → Architecture Drift Detection.**

**Capacity:** 2–3 người / 4–6 tuần.

---

## 3.6 Code → Architecture / L3 Generator

### Mục tiêu

Reverse-engineer source repository để tự động tạo architecture model và tài liệu L3 ban đầu, giảm effort documentation và giữ thiết kế gần với code thực tế.

### Phạm vi MVP

Ưu tiên hỗ trợ 1–2 technology stack phổ biến trước, ví dụ:

* Java/Spring;
* Go;
* Python/FastAPI.

Tool phát hiện:

* module/package;
* entry point;
* API route;
* service/business layer;
* repository/data access;
* database entity;
* external API;
* queue/event;
* configuration;
* important dependency.

Thông tin được chuyển thành một intermediate architecture model.

AI có thể dùng để bổ sung description, nhưng relationship chính phải được chứng minh từ source/static analysis.

### Output

* L3 Markdown document.
* Component model.
* Dependency diagram.
* API relationships.
* DB relationships.
* Event relationships.
* Diagram-as-Code source.

### Điểm kỹ thuật chính

* AST/static analysis.
* Framework-specific parser.
* Dependency extraction.
* Architecture model normalization.
* Documentation generation.

### Giá trị / hướng tích hợp

Hỗ trợ:

**Engineering Knowledge → Architecture Governance → AI Architecture → Architecture Drift Detection.**

**Capacity:** 2–3 người / 4–6 tuần.

---

## 3.7 Test Impact Analyzer

### Mục tiêu

Giảm feedback time bằng cách xác định **subset test cần chạy** dựa trên code change thay vì luôn chạy toàn bộ test suite.

### Phạm vi MVP

Input:

* Git diff / MR;
* source dependency;
* test mapping;
* coverage hoặc historical data nếu có.

Ví dụ thay đổi:

`OrderService`

tool có thể đề xuất chạy:

* OrderService unit tests;
* Order API tests;
* Checkout integration tests;
* Payment contract tests.

MVP ưu tiên 1–2 language/framework.

Tool trả confidence/risk score. Nếu confidence thấp, hệ thống phải safe fallback sang broader/full test suite.

### Output

* Recommended test set.
* Impacted tests.
* Estimated execution time.
* Confidence/risk score.
* Evidence giải thích tại sao test được chọn.

### Điểm kỹ thuật chính

* Code dependency analysis.
* Coverage mapping.
* Change classification.
* Test history.
* Safe fallback strategy.

### Giá trị / hướng tích hợp

Tăng tốc:

**Developer Local Loop + CI + Agentic SDLC.**

Đặc biệt giúp vòng:

**Agent Code → Test → Fix → Test**

nhanh hơn đáng kể.

**Capacity:** 2–3 người / 4–6 tuần.

---

## 3.8 Repository Knowledge Graph

### Mục tiêu

Chuyển source repository thành knowledge graph có cấu trúc để developer và AI hiểu codebase dựa trên entity/relationship thay vì chỉ search text hoặc embedding.

### Phạm vi MVP

Tạo các entity:

* Repository;
* Module;
* Package;
* Class;
* Function;
* API;
* DB Table;
* Event;
* Configuration;
* External Dependency.

Tạo relationship:

* calls;
* imports;
* implements;
* exposes;
* reads;
* writes;
* publishes;
* consumes;
* depends-on.

MVP tập trung vào một technology stack và graph store đơn giản.

Developer có thể hỏi:

* API này đi tới table nào?
* Module nào gọi service này?
* Những component nào phụ thuộc package X?
* Event này do ai publish và consume?

### Output

* Repository graph.
* Graph visualization.
* Query/search API.
* Context extraction API cho AI Agent.

### Điểm kỹ thuật chính

* AST parsing.
* Entity resolution.
* Graph construction.
* Incremental update.
* Graph traversal.

### Giá trị / hướng tích hợp

Có thể trở thành foundation cho:

**Code→L3 + Change Impact + Test Impact + Agentic SDLC Context.**

**Capacity:** 2–3 người / 4–6 tuần.

---

## 3.9 API Traffic Replay Lab

### Mục tiêu

Capture/import API traffic thực tế, sanitize dữ liệu nhạy cảm và replay vào mock service, version mới hoặc test environment để reproduce issue và kiểm tra regression.

### Phạm vi MVP

Input traffic từ:

* gateway export;
* HTTP logs;
* selected recorded requests.

Tool phải hỗ trợ masking/removal:

* token;
* password;
* PII;
* secret headers;
* configurable sensitive fields.

Developer chọn một tập request và tạo replay scenario.

Replay chạy vào target environment khác và so sánh với baseline theo:

* HTTP status;
* response structure;
* selected fields;
* headers;
* latency.

Dynamic values như timestamps/request IDs có ignore rules.

### Output

* Replay datasets.
* Reusable scenarios.
* Execution reports.
* Baseline vs target behavioral diff.

### Điểm kỹ thuật chính

* Traffic sanitization.
* Parameterization.
* Replay engine.
* Dynamic field handling.
* Semantic response comparison.

### Giá trị / hướng tích hợp

Hỗ trợ:

**API Sandbox → Regression Testing → Incident Reproduction → Migration Validation.**

Có thể kết hợp với Shadow API Detector để lấy scenario từ traffic thực tế.

**Capacity:** 2–3 người / 4–6 tuần.

---

## 3.10 Change Impact Analyzer

### Mục tiêu

Trả lời trước mỗi thay đổi:

**“Change này có khả năng ảnh hưởng những gì?”**

Không chỉ trong code mà xuyên:

* API;
* service;
* database;
* event;
* repository;
* test.

### Phạm vi MVP

Input chính:

* Git/MR diff;
* Repository Knowledge Graph;
* API Catalog;
* Service Graph;
* DB metadata nếu có.

Ví dụ:

API response changed

→ identify known consumers.

DB column changed

→ identify query/API/service sử dụng.

Event schema changed

→ identify consumers.

MVP cần tập trung một số impact type rõ ràng thay vì cố giải mọi dependency.

Cần phân biệt:

* Direct impact.
* Transitive impact.
* Possible impact.

### Output

* Impacted services.
* APIs.
* DB objects.
* Events.
* Repositories.
* Tests.
* Risk/confidence.
* Recommended review/test actions.

### Điểm kỹ thuật chính

* Diff classification.
* Dependency traversal.
* Risk scoring.
* Confidence.
* Evidence/explainability.

### Giá trị / hướng tích hợp

Có thể trở thành capability trung tâm cho:

**MR Review → Test Impact → Release Governance → Agentic SDLC Planning.**

**Capacity:** 2–3 người / 4–6 tuần.

---

## 3.11 DB Migration Risk Analyzer

### Mục tiêu

Phân tích database migration/schema change trước khi chạy production để phát hiện breaking change và operational risk.

### Phạm vi MVP

Input:

* migration script;
* hoặc schema before/after.

Tool phân loại:

* add/drop column;
* rename;
* type change;
* index;
* constraint;
* table alteration.

Rules phát hiện các tình huống như:

* drop column;
* narrowing type;
* add NOT NULL không có default;
* destructive change;
* expensive index creation;
* possible table lock;
* missing rollback strategy.

Nếu có DB metadata như table size hoặc row count, có thể sử dụng để cải thiện risk assessment.

### Output

* Migration risk report.
* Breaking-change findings.
* Severity.
* Locking/downtime risk.
* Data-loss risk.
* Remediation recommendation.

### Điểm kỹ thuật chính

* SQL parsing.
* Schema diff.
* Database-specific rules.
* Risk scoring.
* MR integration.

### Giá trị / hướng tích hợp

Có thể chạy độc lập ngay từ MVP, sau đó tích hợp:

**DB Governance → MR Review → Change Impact → CI Quality Gate.**

**Capacity:** 2–3 người / 4–6 tuần.

---

## 3.12 Synthetic Test Data Factory

### Mục tiêu

Sinh dữ liệu test realistic, giữ đúng relationship và constraint của database nhưng không cần copy dữ liệu production nhạy cảm.

### Phạm vi MVP

Tool đọc:

* schema;
* data types;
* PK/FK;
* unique constraints;
* relationships.

Sau đó generate synthetic data theo configurable rules.

Ngoài random data, developer có thể định nghĩa business scenario:

* 100 customers;
* 500 active orders;
* 20 failed payments;
* 5 expired subscriptions.

Một số field phổ biến có generator:

* name;
* email;
* address;
* dates;
* amount;
* identifiers.

Foreign-key relationships phải được đảm bảo.

### Output

* Synthetic datasets.
* Reusable scenarios.
* SQL/CSV/JSON export.
* Seed/reset script.
* CLI/API generation.

### Điểm kỹ thuật chính

* Dependency-aware generation.
* Constraint solving.
* Deterministic seed.
* Domain-specific generators.
* Referential integrity.

### Giá trị / hướng tích hợp

Có thể phục vụ trực tiếp:

**Developer Testing → Mock Data API → API Replay → Ephemeral Environment.**

**Capacity:** 2–3 người / 4–6 tuần.

---

## 3.13 Data Lineage Lite

### Mục tiêu

Cung cấp data lineage ở mức developer-friendly để biết dữ liệu từ đâu đến, đi đâu và thành phần nào bị ảnh hưởng khi thay đổi table/column/query.

### Phạm vi MVP

Parse:

* SQL;
* views;
* ETL definitions;
* dbt;
* SQL query trong source code.

Tool phát hiện:

* source table;
* target table;
* source column;
* target column;
* transformation relationship.

MVP không nhằm thay thế enterprise data governance platform mà tập trung lineage kỹ thuật có thể extract tự động và có evidence.

Developer có thể query:

* Column này đến từ đâu?
* Pipeline nào sử dụng table này?
* Nếu rename column này ảnh hưởng đâu?
* Data này downstream tới system nào?

### Output

* Table-level lineage.
* Partial column-level lineage.
* Upstream/downstream graph.
* Impact report.

### Điểm kỹ thuật chính

* SQL parsing.
* Alias resolution.
* Subquery handling.
* Column resolution.
* Graph construction.

### Giá trị / hướng tích hợp

Phục vụ trực tiếp data/backend developer và cung cấp context cho:

**Change Impact → DB Governance → Engineering Knowledge.**

**Capacity:** 2–3 người / 4–6 tuần.

---

## 3.14 Flaky Test Detective

### Mục tiêu

Tự động phát hiện test không ổn định, giúp developer phân biệt regression thực sự với CI noise và ưu tiên xử lý các flaky test gây ảnh hưởng lớn nhất.

### Phạm vi MVP

Thu lịch sử CI:

* test name;
* pass/fail;
* duration;
* retry;
* branch;
* runner;
* error;
* execution environment.

Tool phát hiện các pattern:

* fail lần đầu, pass khi retry;
* fail theo runner;
* fail khi parallel;
* intermittent timeout;
* execution duration bất thường.

Có thể cluster error messages và đưa ra probable cause:

* timing;
* shared state;
* test isolation;
* external dependency;
* race condition.

AI có thể hỗ trợ explanation nhưng flaky scoring phải dựa trên execution history.

### Output

* Flaky test leaderboard.
* Stability score.
* Failure history.
* Pattern analysis.
* Candidate root cause.

### Điểm kỹ thuật chính

* Historical analytics.
* Flaky probability.
* Statistical scoring.
* Error clustering.
* Environment correlation.

### Giá trị / hướng tích hợp

Giảm CI noise và hỗ trợ:

**Developer Productivity → CI Reliability → Test Impact Analyzer.**

**Capacity:** 2–3 người / 4–6 tuần.

---

## 3.15 Request Journey Debugger

### Mục tiêu

Xây dựng developer-facing debugging tool cho phép nhập `trace-id` hoặc `request-id` và xem toàn bộ hành trình của request qua distributed system.

### Phạm vi MVP

Input từ:

* OpenTelemetry;
* APM traces;
* logs nếu có correlation.

Tool dựng journey qua:

* API/service;
* database;
* cache;
* message broker;
* external dependencies.

Khác raw tracing UI, product tập trung vào câu hỏi của developer:

* request đi qua đâu?
* đâu là critical path?
* bước nào lỗi?
* bước nào chậm?
* dependency nào đóng góp latency lớn nhất?

Ví dụ:

`Checkout → Order → Payment → Redis → External Gateway`

mỗi node hiển thị:

* latency;
* timestamp;
* status;
* error;
* relevant metadata.

### Output

* Interactive request journey.
* Latency breakdown.
* Error hotspot.
* Dependency timeline.
* Shareable debugging report.

### Điểm kỹ thuật chính

* Trace reconstruction.
* Visualization.
* Critical-path analysis.
* Latency attribution.
* Log correlation.
* Noise reduction.

### Giá trị / hướng tích hợp

Có khả năng trở thành tool được developer sử dụng thường xuyên và kết hợp tự nhiên với:

**Trace→Sequence Diagram → Service Graph → Change Impact → AI Troubleshooting.**

**Capacity:** 2–3 người / 4–6 tuần.