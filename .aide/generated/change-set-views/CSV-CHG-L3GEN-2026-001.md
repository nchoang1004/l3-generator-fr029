---
key: CSV-CHG-L3GEN-2026-001
group: derived
non_normative: true
derived_from: [BL-CHG-L3GEN-2026-001-r12]
hand_written: false
status: candidate
generated_by: scripts/prd_package.py render --baseline BL-r12.yaml
---

# Full product — Code → Architecture / L3 Generator

Bản ứng viên chưa duyệt, sinh từ `BL-CHG-L3GEN-2026-001-r12`. Khi view và nguồn bất đồng, **FR/NFR/PRD nguồn thắng**; sửa nguồn rồi chạy lại script render. Không dùng view này như approval.

Gồm 18 FR, 11 NFR và 2 OBS trong baseline.

## 1. Mục tiêu

| Goal key | Mục tiêu | Liên kết OKR/KPI |
|---|---|---|
| GOAL-L3GEN-001 | Giảm thời gian để một kỹ sư hình thành hiểu biết kiến trúc ban đầu về codebase chưa quen | KPI-L3GEN-001, KPI-L3GEN-002. Không áp dụng OKR cấp khối trong đồ án |
| GOAL-L3GEN-002 | Tăng khả năng kiểm chứng tài liệu kiến trúc bằng bằng chứng trực tiếp từ source | KPI-L3GEN-003, KPI-L3GEN-004 |
| GOAL-L3GEN-003 | Giảm công sức tạo bản L3 ban đầu nhưng không đánh đổi bằng các quan hệ suy đoán | KPI-L3GEN-002, KPI-L3GEN-003, KPI-L3GEN-005 |

## 2. Mục tiêu nghiệp vụ đổi

Chưa có baseline đã approved để so diff — đây là baseline candidate đầu tiên của một System mới, nên toàn bộ GOAL/KPI ở PRD đều là bản đầu, không phải thay đổi.

## 3. Tính năng mới

Toàn bộ FR trong candidate baseline; Must/Should và mốc nằm tại từng nguồn.

---

Nguồn: [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md) · revision 5 · status draft · SHA-256 `c5c5e4ace47aeecbea99a24d5390a6398575ddfbe84615468baf9550da61ee0e`

### FR-L3GEN-001 — Nhận thư mục source và bắt đầu phân tích

#### Mô tả

Người dùng chỉ định thư mục source local và nơi lưu kết quả để bắt đầu một lần phân tích.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Phân tích repository |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-001-01

- **Given:** Thư mục tồn tại, đọc được và chứa source thuộc stack hỗ trợ.
- **When:** người dùng chạy l3gen với đường dẫn source và output.
- **Then:** công cụ phân tích đúng thư mục đã chọn và báo đường dẫn bộ kết quả.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-PERF-001, NFR-L3GEN-REL-001, NFR-L3GEN-SEC-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm tra source có dấu cách trong đường dẫn và output ở ngoài source.

##### AC-L3GEN-001-02

- **Given:** Đường dẫn không tồn tại, là file hoặc không có quyền đọc.
- **When:** người dùng yêu cầu phân tích.
- **Then:** công cụ trả lỗi đầu vào, chỉ rõ nguyên nhân và cách sửa; không báo thành công hoặc tạo bộ kết quả hoàn chỉnh.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm exit code và thông báo cho từng trường hợp.

##### AC-L3GEN-001-03

- **Given:** Thư mục đầu ra không ghi được hoặc đã có bộ kết quả.
- **When:** người dùng bắt đầu một lần phân tích mới.
- **Then:** công cụ báo lỗi nếu không ghi được; nếu trùng kết quả thì hoặc từ chối, hoặc yêu cầu người dùng xác nhận trước khi ghi đè. Không bao giờ ghi đè im lặng.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Dùng output có sentinel; xác nhận sentinel nguyên vẹn khi chưa xác nhận, và chỉ bị thay sau khi người dùng xác nhận rõ ràng.

##### AC-L3GEN-001-04

- **Given:** Repository có thư mục loại trừ do người dùng chỉ định.
- **When:** người dùng chạy phân tích.
- **Then:** các thư mục bị loại không đi vào dữ liệu kiến trúc; cấu hình loại trừ được ghi trong thông tin lần chạy.
- `constrained_by:` [NFR-L3GEN-SEC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Dùng mã sentinel trong tests, integration-tests, venv và một thư mục tùy chọn.

##### AC-L3GEN-001-05

- **Given:** Một repository đã pin ở một commit, có bản trên đĩa và bản ZIP của cùng commit đó.
- **When:** người dùng chạy phân tích bằng dòng lệnh trên thư mục local, và chạy lại trên giao diện web bằng bản ZIP, cùng tắt AI.
- **Then:** hai lần cho cùng tập application, component, route, entity, external system, cạnh dependency, nhãn confidence/completeness và cùng danh sách limitation. Khác biệt chỉ được phép ở đường dẫn gốc trong evidence, dấu thời gian, định danh phiên và cách trình bày; vị trí tương đối của evidence trong repository phải giống nhau. Ranh giới đầy đủ ở NFR-L3GEN-DET-001.
- `constrained_by:` [NFR-L3GEN-DET-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** So sánh JSON chuẩn hóa của hai lần chạy sau khi chuẩn hóa đường dẫn gốc. Khác biệt ở bất kỳ dữ kiện, quan hệ, nhãn hoặc limitation nào là lỗi chặn phát hành, không phải khác biệt trình bày.

##### AC-L3GEN-001-06

- **Given:** Thư mục output nằm bên trong thư mục source, hoặc source nằm bên trong output.
- **When:** người dùng bắt đầu phân tích.
- **Then:** công cụ từ chối và giải thích lý do; không đọc lại artifact của chính nó như source đầu vào, và không ghi vào cây source đang phân tích.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-SEC-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm cả hai chiều lồng nhau và trường hợp hai đường dẫn trỏ cùng một chỗ qua symlink hoặc đường dẫn tương đối.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-002](../../requirements/fr/FR-L3GEN-002.md) · revision 3 · status draft · SHA-256 `be40b9d847ffd83c203045cdda3e30ece01b63ce0b2a9178f8db844a739f3e48`

### FR-L3GEN-002 — Nhận diện đơn vị phân tích và phạm vi hỗ trợ

#### Mô tả

Người dùng xem được những phần repository được phân tích, bị bỏ qua hoặc chưa xác định được stack, cùng các điểm khởi động ứng dụng dùng để xác định ranh giới đơn vị.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Phân tích repository |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-002-01

- **Given:** Repository có service Python/FastAPI và service Java với manifest riêng.
- **When:** người dùng phân tích repository.
- **Then:** công cụ phân tích phần Python được hỗ trợ, liệt kê phần Java bị bỏ qua với lý do, không kết luận rằng toàn repository đã được bao phủ.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-REL-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu danh sách đơn vị, file và trạng thái.

##### AC-L3GEN-002-02

- **Given:** Thư mục Python không có manifest nhưng có import FastAPI.
- **When:** người dùng phân tích.
- **Then:** công cụ dùng thư mục đầu vào làm đơn vị tạm, ghi bằng chứng nhận diện và nêu ranh giới service chưa được xác nhận.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không gọi ranh giới suy từ thư mục là deployment boundary chắc chắn.

##### AC-L3GEN-002-03

- **Given:** Không có source hoặc mọi đơn vị đều không thuộc stack hỗ trợ.
- **When:** người dùng phân tích.
- **Then:** công cụ trả lỗi đầu vào và liệt kê stack hỗ trợ; không trả báo cáo rỗng như một lần thành công.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-REL-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm Python rỗng, Java-only và Flask-only.

##### AC-L3GEN-002-04

- **Given:** Một đơn vị chứa FastAPI cùng framework khác chưa hỗ trợ.
- **When:** người dùng phân tích.
- **Then:** công cụ báo tất cả framework phát hiện được và chỉ chạy khả năng đang hỗ trợ; phần bỏ qua được ghi rõ.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-REL-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không hứa chạy extractor chưa tồn tại.

##### AC-L3GEN-002-05

- **Given:** Repository có nhiều thư mục chứa mã thuộc stack hỗ trợ, trong đó một số thư mục có điểm khởi động ứng dụng và một số chỉ chứa mã dùng chung.
- **When:** người dùng phân tích repository.
- **Then:** công cụ liệt kê các điểm khởi động phát hiện được kèm file, vị trí và luật nhận diện đã dùng; mỗi đơn vị phân tích nêu rõ có hay không có điểm khởi động; thư mục chỉ chứa mã dùng chung không bị công bố là ứng dụng riêng.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-REL-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu danh sách điểm khởi động với kiểm tay trên repo mẫu có nhiều ứng dụng. Không suy ra điểm khởi động chỉ từ tên file hoặc tên thư mục; không có điểm khởi động nào phát hiện được thì ghi phần chưa xác định kèm lý do, không chọn bừa một file làm điểm khởi động.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-003](../../requirements/fr/FR-L3GEN-003.md) · revision 5 · status draft · SHA-256 `e1484467227aba58ae0205362af61edad9092362aac13e9213e97c7610dbebfa`

### FR-L3GEN-003 — Liệt kê API routes và handler

#### Mô tả

Người dùng xem method, path, handler, điều kiện đăng ký và nguồn khai báo của route trong phạm vi stack đã công bố. Bản đầu phủ FastAPI; Java/Spring Boot theo mốc M3.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1: route FastAPI; M3: route Spring Boot |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-003-01

- **Given:** FastAPI/APIRouter được khai báo trực tiếp cùng decorator GET, POST, PUT, DELETE hoặc PATCH.
- **When:** người dùng phân tích.
- **Then:** mỗi route xuất hiện đúng method, path, handler và nguồn; HTTP method ngoài phạm vi được báo là chưa hỗ trợ khi phát hiện.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Có fixture dùng alias import và hai router cùng tên ở hai module.

##### AC-L3GEN-003-02

- **Given:** Router được include nhiều tầng hoặc app con được mount với prefix chuỗi hằng.
- **When:** người dùng phân tích.
- **Then:** path gồm đủ prefix của chuỗi đăng ký; router được đăng ký tại nhiều path có các route tương ứng.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu cả include_router và app.mount.

##### AC-L3GEN-003-03

- **Given:** Prefix là giá trị động, đăng ký nằm trong if hoặc router chưa nối được tới app gốc.
- **When:** người dùng phân tích.
- **Then:** công cụ giữ phần chưa biết/điều kiện, hạ completeness thành partial và ghi lý do; không tuyên bố URL chạy thật đã đầy đủ.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Fixture kiểm route không được mount và prefix thiếu.

##### AC-L3GEN-003-04

- **Given:** create_app() tạo FastAPI và truyền app qua tham số được khai kiểu tới hàm đăng ký route chứa decorator lồng.
- **When:** người dùng phân tích.
- **Then:** công cụ tìm được các route của mẫu này; phần binding không xác định được phải hiện cảnh báo thay vì kết luận không có route.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Fixture độc lập có hàm tạo app và hàm đăng ký route nhận tham số kiểu FastAPI; không cam kết mọi factory động.

##### AC-L3GEN-003-05

- **Given:** Repo đăng ký route bằng vòng lặp hoặc add_api_route chưa được hỗ trợ.
- **When:** người dùng phân tích.
- **Then:** công cụ ghi nguồn pattern chưa hỗ trợ trong giới hạn; không tự tạo danh sách route suy đoán.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Phân biệt không tìm thấy route với không hỗ trợ cách đăng ký.

##### AC-L3GEN-003-06

- **Given:** Repository Java dùng Spring Boot với controller khai báo route bằng annotation trong phạm vi đã công bố.
- **When:** người dùng phân tích.
- **Then:** route Java hiện ra với cùng cấu trúc dữ liệu và cùng nhãn chất lượng như route Python; không có trường riêng chỉ dành cho một ngôn ngữ.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Ma trận annotation cụ thể của Spring Boot chốt tại OQ-L3GEN-003 trước thiết kế. Annotation ngoài ma trận phải hiện ở phần giới hạn, không im lặng bỏ qua.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-004](../../requirements/fr/FR-L3GEN-004.md) · revision 4 · status draft · SHA-256 `e71f82c2c7277fcef0b7621a7947d8abbee76afb0bd14ac5fb9a893aee460b76`

### FR-L3GEN-004 — Liệt kê mô hình dữ liệu

#### Mô tả

Người dùng xem lớp dữ liệu, tên bảng nếu xác định được, cột và khóa ngoại; nhận diện entity không đồng nghĩa biết tên bảng. Bản đầu phủ SQLAlchemy; ORM của Java/Spring Boot theo mốc M3.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1: entity SQLAlchemy; M3: entity Java |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-004-01

- **Given:** Lớp SQLAlchemy có __tablename__ hằng, Column và ForeignKey.
- **When:** người dùng phân tích.
- **Then:** công cụ xuất lớp, bảng, cột, kiểu, khóa chính và khóa ngoại được khai báo cùng nguồn.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Phạm vi Must: declarative_base/Base, Column; SQLModel/mapped_column theo OQ phạm vi.

##### AC-L3GEN-004-02

- **Given:** Entity kế thừa qua lớp trung gian trong repository.
- **When:** người dùng phân tích.
- **Then:** công cụ nối được chuỗi kế thừa trong khả năng hỗ trợ và không coi lớp __abstract__ là bảng triển khai.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Có fixture lớp cha khác file.

##### AC-L3GEN-004-03

- **Given:** Tên bảng do lớp cơ sở sinh lúc chạy hoặc __tablename__ là biểu thức chưa giải được.
- **When:** người dùng phân tích.
- **Then:** công cụ giữ entity nhưng biểu diễn tên bảng chưa xác định, ghi partial và lý do; không tự lower-case tên class để đoán.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Fixture có tên bảng được sinh lúc chạy; kiểm kết quả giữ entity và báo tên bảng chưa xác định thay vì đoán từ tên lớp.

##### AC-L3GEN-004-04

- **Given:** Khóa ngoại trỏ tới bảng ngoài phần quét.
- **When:** người dùng phân tích.
- **Then:** công cụ giữ nguyên khai báo và nguồn, đánh dấu đích chưa resolve; không tự tạo bảng thật để nối đủ graph.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu cả quan hệ liên bảng đã và chưa giải được.

##### AC-L3GEN-004-05

- **Given:** Repository có thao tác SQLAlchemy đọc bằng query(Model).all()/first()/one() hoặc Session.get(Model, id), và thao tác add/delete với entity xác định được.
- **When:** người dùng xem quan hệ component hoặc hàm tới dữ liệu.
- **Then:** công cụ nối quan hệ đọc hoặc ý định ghi/xóa tới entity cùng bằng chứng callsite; không kết luận giao dịch đã commit hoặc dữ liệu đã thay đổi ở runtime chỉ từ add/delete.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Phân biệt tên entity xuất hiện, query chưa thực thi, thao tác truy vấn và thao tác ghi chờ transaction; SDK/SQL động ngoài pattern phải ghi unknown.

##### AC-L3GEN-004-06

- **Given:** Repository Java dùng ORM thuộc phạm vi đã công bố của Spring Boot.
- **When:** người dùng phân tích.
- **Then:** entity Java hiện ra với cùng cấu trúc dữ liệu và cùng nhãn chất lượng như entity Python; tên bảng chưa xác định được vẫn giữ unknown kèm lý do, không suy từ tên lớp.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** ORM và annotation cụ thể chốt tại OQ-L3GEN-003 trước thiết kế. ORM ngoài phạm vi phải hiện ở phần giới hạn.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-005](../../requirements/fr/FR-L3GEN-005.md) · revision 3 · status draft · SHA-256 `055dcdc58b302c9de131ff2002c8457edf68a7f1a8c375e623de32d1306632f3`

### FR-L3GEN-005 — Liệt kê lời gọi HTTP và đích bên ngoài

#### Mô tả

Người dùng xác định nơi gọi HTTP qua thư viện thuộc phạm vi đã công bố và mức độ biết đích đến; không đồng nhất mọi HTTP call với một hệ thống bên ngoài đã xác nhận. Bản đầu phủ requests/httpx của Python; client HTTP của Java/Spring Boot theo mốc M3.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1: requests/httpx; M3: client HTTP phía Java |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-005-01

- **Given:** Code dùng requests/httpx trực tiếp hoặc client/session được xác định bằng gán và with/async with.
- **When:** người dùng phân tích.
- **Then:** công cụ xuất method, caller, URL biết được và vị trí lời gọi, kể cả async.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm alias import, Client, AsyncClient, Session.

##### AC-L3GEN-005-02

- **Given:** URL ghép từ biến hoặc client dùng base_url chưa giải được.
- **When:** người dùng phân tích.
- **Then:** công cụ giữ biểu thức và phần URL biết được, gán partial; không gọi một path tương đối là host đầy đủ.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm /health và settings.BASE_URL.

##### AC-L3GEN-005-03

- **Given:** Biến local tên requests hoặc httpx che tên thư viện.
- **When:** người dùng phân tích.
- **Then:** công cụ không phân loại lời gọi của biến local thành HTTP của thư viện chỉ vì trùng tên.
- `constrained_by:` [NFR-L3GEN-ACC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Fixture shadowing và method get của object nội bộ.

##### AC-L3GEN-005-04

- **Given:** Test client gọi chính ứng dụng hoặc đích chưa xác định.
- **When:** người dùng xem dependency.
- **Then:** công cụ phân biệt HTTP nội bộ/đích chưa biết với external host đã xác nhận; không tuyên bố thêm external system không có bằng chứng.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Test thư mục integration-tests được loại và test client không bị gộp external host.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-006](../../requirements/fr/FR-L3GEN-006.md) · revision 3 · status draft · SHA-256 `e94208bbdd098f13bc3d00db48703304a6fb5bb014580427ad219e71e90b7f33`

### FR-L3GEN-006 — Truy vết tham chiếu và lời gọi xuyên file

#### Mô tả

Người dùng xem quan hệ gọi hàm, import và kế thừa với đích cụ thể hoặc lý do chưa xác định được.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-006-01

- **Given:** Hai module có class/method trùng tên và caller import từng đích bằng alias hoặc relative import.
- **When:** người dùng phân tích.
- **Then:** quan hệ nối đúng symbol theo scope/import của caller; không chọn tên duy nhất hoặc đầu tiên toàn repository làm exact.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm đích symbol và vị trí định nghĩa.

##### AC-L3GEN-006-02

- **Given:** Receiver có kiểu từ gán Class(), annotation hoặc self.field có khai báo xác định.
- **When:** người dùng phân tích.
- **Then:** lời gọi nối đúng method trong lớp hoặc chuỗi kế thừa được hỗ trợ.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không suy kiểu chỉ từ tên biến db_session.

##### AC-L3GEN-006-03

- **Given:** Có dynamic import, wildcard import mơ hồ, receiver chưa biết kiểu hoặc kế thừa vòng/nhiều đích.
- **When:** người dùng phân tích.
- **Then:** quan hệ chưa giải được hoặc mơ hồ vẫn được giữ với vị trí và lý do; hệ thống không treo, không chọn đích tùy tiện.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Tách external library đã biết tên khỏi unresolved internal.

##### AC-L3GEN-006-04

- **Given:** Hàm chỉ nhắc tên lớp dữ liệu mà không có thao tác DB được chứng minh.
- **When:** người dùng xem graph.
- **Then:** công cụ có thể ghi references_entity nhưng không kết luận reads hoặc writes từ việc xuất hiện tên lớp.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Quan hệ DB đọc/ghi chỉ có khi có rule và bằng chứng thao tác; chưa giải được thì ghi rõ.

##### AC-L3GEN-006-05

- **Given:** Một lời gọi hoặc tham chiếu chưa resolve được đích, hoặc đích nằm ngoài phạm vi phân tích.
- **When:** công cụ dựng component model và sơ đồ dependency.
- **Then:** dữ kiện đó không trở thành cạnh giữa hai component; nó được giữ ở lớp dữ kiện với nhãn unresolved và lý do. Cạnh kiến trúc chỉ sinh ra từ quan hệ đã resolve về một đích cụ thể.
- `constrained_by:` [NFR-L3GEN-ABST-001, NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu tập cạnh kiến trúc với tập quan hệ unresolved; giao của hai tập phải rỗng. Không dùng tên module hay tên file để đoán đích thay cho resolve.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-007](../../requirements/fr/FR-L3GEN-007.md) · revision 3 · status draft · SHA-256 `d44fcdb3dd4b7968c6fc3cefba481ad9eeff2a9c8a7baa1a783aa4405ef93254`

### FR-L3GEN-007 — Kiểm chứng kết luận bằng nguồn và nhãn

#### Mô tả

Người đọc truy ngược được dữ kiện và quan hệ về đúng source snapshot, phân biệt bằng chứng trực tiếp, suy theo rule và phần chưa biết.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Kiểm chứng kết quả |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-007-01

- **Given:** Có route, entity, HTTP call hoặc cạnh quan hệ được xuất.
- **When:** người dùng mở chi tiết hoặc link nguồn.
- **Then:** công cụ chỉ ra file và range dòng tạo nên kết luận; nguồn hiển thị khớp phiên bản đã phân tích.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đặt output ngoài source để phát hiện link tương đối hỏng.

##### AC-L3GEN-007-02

- **Given:** Kết luận theo cú pháp trực tiếp hoặc quy tắc suy luận đã công bố.
- **When:** người dùng xem kết quả.
- **Then:** confidence thể hiện exact hoặc inferred, completeness thể hiện full hoặc partial ở hai trường riêng; inferred/partial có lý do và nguồn.
- `constrained_by:` [NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** full chỉ nói thuộc tính công bố, không có nghĩa bao phủ mọi runtime behavior.

##### AC-L3GEN-007-03

- **Given:** Nguồn đã thay đổi hoặc di chuyển sau lần phân tích.
- **When:** người dùng truy bằng chứng.
- **Then:** công cụ cho biết snapshot không còn khớp hoặc không mở được nguồn; không coi source mới là evidence cũ.
- `constrained_by:` [NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Có source digest; không tạo link Git commit cho cây có thay đổi chưa commit.

##### AC-L3GEN-007-04

- **Given:** Một component hoặc cạnh gộp có nhiều dữ kiện hỗ trợ.
- **When:** người dùng xem bằng chứng.
- **Then:** kết quả giữ danh sách nguồn đóng góp; không ép một kết luận tổng hợp về một dòng không đại diện.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu chain component → code entities → source.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md) · revision 5 · status draft · SHA-256 `501d2ec15fd9424a9c8a2083824847b80dbf5818c57e077c2c61e532859c712e`

### FR-L3GEN-008 — Xuất và sử dụng bộ kết quả

#### Mô tả

Người dùng nhận tài liệu đọc được và JSON có cấu trúc cho công cụ khác, cùng thông tin phiên bản và phạm vi lần chạy.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tài liệu và tích hợp |
| Ưu tiên đề xuất | Must Have |
| Mốc bắt đầu đề xuất | M1: xuất dữ kiện ban đầu; M2: tích hợp component/L3 |
| Mốc nghiệm thu đầy đủ đề xuất | M3: sau khi tích hợp config/event từ FR-L3GEN-014/015; tất cả AC của FR này phải đạt |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-008-01

- **Given:** Phân tích hoàn tất ở chế độ không AI.
- **When:** người dùng mở output.
- **Then:** có tài liệu L3 Markdown, mô hình kiến trúc dạng JSON và mã nguồn sơ đồ Mermaid; biểu diễn được component cùng quan hệ API/DB/event theo FR-L3GEN-011. Bộ kết quả có bằng chứng, giới hạn phân tích và thông tin lần chạy phân biệt với dữ kiện chuẩn; danh sách cảnh báo có thể rỗng.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu nội dung theo FR-L3GEN-011 và cảnh báo theo FR-L3GEN-009. Tên, số lượng file và schema chi tiết chốt ở contract; không bắt buộc tách mô hình thành nhiều file JSON.

##### AC-L3GEN-008-02

- **Given:** Người dùng nhập mô hình kiến trúc vào bộ đọc JSON và mã nguồn sơ đồ vào renderer Mermaid mục tiêu.
- **When:** người dùng đọc/xem kết quả.
- **Then:** JSON hợp lệ, ID không trùng, cạnh không treo đích, khai phiên bản schema; Mermaid render được với tên có dấu/ký tự đặc biệt.
- `constrained_by:` [NFR-L3GEN-COMP-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Renderer/version và schema cụ thể chốt ở contract sau Scope Gate.

##### AC-L3GEN-008-03

- **Given:** Graph có nhiều thành phần.
- **When:** người dùng xem sơ đồ rút gọn.
- **Then:** báo rõ quy tắc rút gọn và phần bị ẩn; JSON giữ dữ liệu đầy đủ trong phạm vi đã phân tích.
- `constrained_by:` [NFR-L3GEN-TRACE-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không dùng sơ đồ rút gọn để tính coverage.

##### AC-L3GEN-008-04

- **Given:** Người dùng chạy lại cùng source snapshot và cấu hình ở thư mục output khác.
- **When:** người dùng so sánh dữ liệu chuẩn.
- **Then:** nội dung cấu trúc và ID ổn định theo NFR determinism; timestamp/duration của từng lần chạy không bị làm giả để đạt byte equality.
- `constrained_by:` [NFR-L3GEN-DET-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm hash chuẩn hóa, giữ metrics thật trong metadata.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-009](../../requirements/fr/FR-L3GEN-009.md) · revision 3 · status draft · SHA-256 `aa3c01fe130012d7e4a823d3892f37ebf6061d5e20a11f693c06d7c448f545bb`

### FR-L3GEN-009 — Báo lỗi và giới hạn theo từng lần phân tích

#### Mô tả

Người dùng biết phần đã phân tích, bị bỏ qua và chưa hỗ trợ trước khi tin vào tài liệu.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Kiểm chứng kết quả |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-009-01

- **Given:** Một file lỗi cú pháp/encoding trong repo còn file hợp lệ.
- **When:** người dùng chạy phân tích.
- **Then:** công cụ tiếp tục với phần hợp lệ, báo file lỗi và nguyên nhân, giữ số đếm nhất quán.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** files_found bằng analyzed cộng skipped trong tập file đã chọn.

##### AC-L3GEN-009-02

- **Given:** Không tìm được route dù có pattern FastAPI chưa được xử lý.
- **When:** người dùng xem kết quả.
- **Then:** báo chưa đủ khả năng kết luận, liệt kê pattern/nguồn; không viết kết quả đầy đủ chỉ vì parse được mọi file.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Case factory/nested route.

##### AC-L3GEN-009-03

- **Given:** Một tham chiếu nội bộ chưa giải được hoặc thư viện nằm ngoài phạm vi.
- **When:** người dùng xem tóm tắt.
- **Then:** công cụ thống kê riêng hai trường hợp; tỷ lệ resolve không trộn external library thành lỗi nội bộ.
- `constrained_by:` [NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Ghi mẫu số và danh sách giới hạn.

##### AC-L3GEN-009-04

- **Given:** Có lỗi ghi output hoặc bị ngắt giữa quá trình.
- **When:** người dùng mở thư mục kết quả.
- **Then:** không có dấu hiệu hoàn tất cho bộ thiếu file; dữ liệu từ lần chạy thành công trước đó không bị phá.
- `constrained_by:` [NFR-L3GEN-REL-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Cách atomic write/staging quyết định ở L2, hành vi này là yêu cầu.

##### AC-L3GEN-009-05

- **Given:** Có tham chiếu nội bộ chưa xác định được đích, đích mơ hồ hoặc thuộc tính kiến trúc chưa giải được trong phần source đã phân tích.
- **When:** công cụ tạo findings ở chế độ không AI.
- **Then:** mỗi cảnh báo chỉ rõ loại giới hạn, thực thể hoặc quan hệ bị ảnh hưởng, nguồn và lý do chưa kết luận được. Phần dữ kiện đã xác định vẫn được giữ; không biến giới hạn của công cụ thành kết luận code có lỗi. Không có cảnh báo thì danh sách rỗng.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Fixture có đích thiếu, nhiều đích và thuộc tính động; đối chiếu từng cảnh báo với dữ kiện và nguồn tương ứng. Phạm vi FR này là độ đầy đủ của kết quả kiến trúc, không bao gồm rà code không dùng hoặc kiểm cách xử lý lỗi HTTP.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-010](../../requirements/fr/FR-L3GEN-010.md) · revision 3 · status draft · SHA-256 `9f40fff78ecde4f8f0539274185636fededeea8c13b0e36604dafd1e17756f14`

### FR-L3GEN-010 — Chạy phân tích không phụ thuộc AI

#### Mô tả

Người dùng phân tích đầy đủ phần cốt lõi khi không có API key, không có mạng hoặc chủ động tắt AI.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Phân tích repository |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-010-01

- **Given:** Không có API key hoặc dùng --no-ai.
- **When:** người dùng phân tích repo.
- **Then:** công cụ sinh toàn bộ dữ kiện và output cốt lõi, thông báo chế độ tĩnh, không gọi LLM.
- `constrained_by:` [NFR-L3GEN-AI-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-SEC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu dữ kiện và kiểm network.

##### AC-L3GEN-010-02

- **Given:** AI provider lỗi hoặc thiếu SDK AI.
- **When:** người dùng đã chọn bổ sung AI và bắt đầu phân tích.
- **Then:** công cụ giữ kết quả tĩnh, báo phần mô tả chưa có và nguyên nhân; không làm mất báo cáo.
- `constrained_by:` [NFR-L3GEN-AI-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không retry vô hạn; giới hạn theo NFR AI nếu chọn extension.

##### AC-L3GEN-010-03

- **Given:** Cùng input với AI bật/tắt.
- **When:** người dùng so sánh dữ kiện.
- **Then:** route/entity/quan hệ/ID không đổi do nội dung AI; cảnh báo deterministic vẫn có khi tắt AI.
- `constrained_by:` [NFR-L3GEN-AI-001, NFR-L3GEN-DET-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Cảnh báo về giới hạn phân tích theo FR-L3GEN-009 vẫn được xuất khi tắt AI, theo contract đầu ra được duyệt.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-011](../../requirements/fr/FR-L3GEN-011.md) · revision 6 · status draft · SHA-256 `eeb10f9a68f3f0d47b486890ba995c205a0ea36f2ee766869749e4f414c35ef5`

### FR-L3GEN-011 — Xem component và tài liệu L3 của service

#### Mô tả

Người dùng xem các component bên trong service và quan hệ có chứng cứ giữa chúng. Lớp trình bày mặc định dừng ở mức component; từ một component hoặc một quan hệ, người dùng mở được bằng chứng ở mức module/class/function và nguồn.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tài liệu và tích hợp |
| Ưu tiên đề xuất | Must Have |
| Mốc bắt đầu đề xuất | M2: tạo component model và tài liệu L3 ban đầu |
| Mốc nghiệm thu đầy đủ đề xuất | M3: tài liệu tích hợp config/event và tất cả AC của FR này đạt |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-011-01

- **Given:** Repo có API, business module, data access và integration với ranh giới nhóm đã công bố.
- **When:** người dùng sinh tài liệu L3.
- **Then:** có component model gồm định danh, thành viên code, vai trò, interface và dependency; mỗi nhóm chỉ ra rule/evidence.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-DET-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Cho phép nhóm theo module/package; không mặc định mọi services/ đều là deployment service.

##### AC-L3GEN-011-02

- **Given:** Nhiều lời gọi code liên kết hai component.
- **When:** người dùng xem sơ đồ component.
- **Then:** các cạnh code được gộp thành dependency giữa component với danh sách nguồn; từ component mở được danh sách code entities và source làm bằng chứng, nhưng sơ đồ mặc định không hiển thị các cạnh code rời rạc đó.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không suy causal request flow chỉ từ việc cùng xuất hiện trong module.

##### AC-L3GEN-011-03

- **Given:** Không đủ căn cứ xác định business/repository role hoặc có nhiều cách nhóm.
- **When:** người dùng xem model.
- **Then:** giữ nhóm module trung tính/UNKNOWN và lý do; không đặt trách nhiệm nghiệp vụ như một sự thật đã biết.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Role inference là inferred, không exact.

##### AC-L3GEN-011-04

- **Given:** Người dùng mở tài liệu L3 Markdown và sơ đồ component.
- **When:** người dùng tìm API, DB và external dependency của một component.
- **Then:** có danh sách liên quan, bằng chứng, giới hạn và phần diễn giải tách riêng; L3 có component, API, DB, cấu hình và event trong khả năng hỗ trợ.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Bộ kết quả theo FR-L3GEN-008 chứa mô hình component đọc được bằng máy và mã nguồn sơ đồ; đối chiếu chúng với nội dung tài liệu, không phụ thuộc tên file.

##### AC-L3GEN-011-05

- **Given:** Repository có số function trong phạm vi hỗ trợ đạt hoặc vượt ngưỡng ở NFR-L3GEN-ABST-001.
- **When:** người dùng xem sơ đồ và tài liệu L3 mặc định.
- **Then:** node trong sơ đồ mặc định là application, component và hệ thống ngoài; số node không vượt trần quy định ở NFR-L3GEN-ABST-001, không tăng theo số function, và không có một node cho mỗi function. Vượt trần thì rút gọn có thông báo theo AC-L3GEN-008-03, không xuất sơ đồ đầy đủ rồi để người đọc tự lọc. Dữ kiện mức function/class vẫn truy được ở lớp bằng chứng có nhãn riêng.
- `constrained_by:` [NFR-L3GEN-ABST-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đếm node theo lớp trong bộ kết quả máy đọc được của FR-L3GEN-008, không đếm trên hình; đối chiếu số đếm với trần ở NFR-L3GEN-ABST-001. Cả ngưỡng số function lẫn trần số node lấy từ NFR đó, không gõ lại ở đây.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-012](../../requirements/fr/FR-L3GEN-012.md) · revision 3 · status draft · SHA-256 `baa9d93570df8421dde0866015b291e11a73e9edb2dd5e8b67ccaebe8e83cc95`

### FR-L3GEN-012 — Bổ sung mô tả và diễn giải cảnh báo bằng AI

#### Mô tả

Sau khi người dùng chủ động cho phép, AI có thể bổ sung mô tả và giải thích giới hạn phân tích theo FR-L3GEN-009. Các cảnh báo này được tạo từ phân tích tĩnh, không cần AI.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tiện ích mở rộng |
| Ưu tiên đề xuất | Should Have |
| Mốc đề xuất | M3 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-012-01

- **Given:** Người dùng chưa chọn bật AI dù máy có key.
- **When:** người dùng phân tích.
- **Then:** công cụ không tự gửi dữ liệu tới provider; thông báo rõ dữ liệu nào sẽ được gửi khi chọn bật.
- `constrained_by:` [NFR-L3GEN-AI-001, NFR-L3GEN-PRIV-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Quyền gửi dữ liệu và provider phải được chốt ở Scope Gate.

##### AC-L3GEN-012-02

- **Given:** Có mô hình kiến trúc và danh sách cảnh báo về giới hạn phân tích được tạo không cần AI.
- **When:** AI sinh phần diễn giải.
- **Then:** chỉ nhận mô tả gắn ID đã tồn tại, schema chặn sửa/thêm/xóa thực thể và quan hệ; giải thích AI mang nhãn AI.
- `constrained_by:` [NFR-L3GEN-AI-001, NFR-L3GEN-DET-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Enrichment và giải thích finding đọc dữ kiện độc lập.

##### AC-L3GEN-012-03

- **Given:** AI trả ID lạ, payload sai schema, timeout hoặc vượt giới hạn.
- **When:** công cụ nhận phản hồi.
- **Then:** bỏ phần không hợp lệ, ghi nguyên nhân và giữ kết quả tĩnh; không bỏ giới hạn chi phí để hoàn tất mô tả.
- `constrained_by:` [NFR-L3GEN-AI-001, NFR-L3GEN-DET-001, NFR-L3GEN-PRIV-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Bí mật không vào log/payload.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md) · revision 5 · status draft · SHA-256 `b73567265cc5f6d97300c385058e9e1bca606d0502164e6b30338ed11b4d85b3`

### FR-L3GEN-013 — Phân tích và khám phá kiến trúc qua giao diện web

#### Mô tả

Người dùng truy cập giao diện web để gửi repository, theo dõi phân tích, xem tổng quan/component/dependency và truy về nguồn bằng chứng.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Khám phá kiến trúc |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M2 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-013-01

- **Given:** Người dùng có repository thuộc phạm vi hỗ trợ.
- **When:** người dùng tạo yêu cầu phân tích trên giao diện.
- **Then:** chọn được đầu vào hỗ trợ, cấu hình phạm vi và chế độ AI; theo dõi trạng thái; khi xong mở được kết quả đúng lần chạy.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-PERF-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Giao diện dùng cùng dịch vụ phân tích và model; không tự suy cấu trúc riêng.

##### AC-L3GEN-013-02

- **Given:** Người dùng chọn một thực thể hoặc cạnh.
- **When:** giao diện mở chi tiết.
- **Then:** hiện nguồn và hai loại nhãn độc lập; mô tả AI khác dữ kiện source bằng nhãn rõ.
- `constrained_by:` [NFR-L3GEN-TRACE-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Có keyboard navigation và không chỉ phân biệt bằng màu.

##### AC-L3GEN-013-03

- **Given:** Output rỗng, hỏng hoặc schema không hỗ trợ.
- **When:** người dùng mở giao diện.
- **Then:** hiện trạng thái rỗng/lỗi phù hợp và cách xử lý; không crash hoặc hiện graph cũ như kết quả mới.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm riêng ba trường hợp output rỗng, output hỏng và schema version không hỗ trợ; xác nhận mỗi trường hợp có trạng thái và cách xử lý riêng. Sau khi mở một kết quả lỗi, giao diện không giữ lại graph của lần chạy trước.

##### AC-L3GEN-013-04

- **Given:** Kết quả có nhiều component và quan hệ.
- **When:** người dùng tìm tên hoặc lọc theo service/loại thành phần/nhãn.
- **Then:** giao diện hiển thị phần khớp, cho thu phóng/chọn node và tải output; phần bị ẩn do lọc được báo rõ.
- `constrained_by:` [NFR-L3GEN-PERF-001, NFR-L3GEN-TRACE-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Mỗi sơ đồ có đường tới evidence của node và cạnh.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-014](../../requirements/fr/FR-L3GEN-014.md) · revision 3 · status draft · SHA-256 `b4b2734f1d0ade745567de52b3d3b16f422026fa5b295fcc126b4289310ca573`

### FR-L3GEN-014 — Xem cấu hình mà hệ thống sử dụng

#### Mô tả

Người dùng xem các khóa cấu hình và nơi sử dụng mà không lộ giá trị bí mật.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M3 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-014-01

- **Given:** Python đọc os.getenv/os.environ hoặc trường settings được định nghĩa bằng Pydantic BaseSettings.
- **When:** người dùng phân tích.
- **Then:** công cụ liệt kê khóa/trường, nơi khai báo/sử dụng và component liên quan nếu resolve được.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không thực thi settings hoặc đọc môi trường thật của server.

##### AC-L3GEN-014-02

- **Given:** Có .env.example hoặc YAML cấu hình ứng dụng với schema/key công bố trong ma trận hỗ trợ.
- **When:** người dùng phân tích.
- **Then:** công cụ liên kết tên khóa khi có mapping rõ, nêu nguồn; key trùng tên không đủ để nối dependency.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** YAML tùy ý chưa có schema chỉ được coi là dữ liệu chưa hiểu.

##### AC-L3GEN-014-03

- **Given:** Giá trị là token/password hoặc chuỗi kết nối có credential.
- **When:** người dùng xem/export kết quả.
- **Then:** giá trị bị che hoặc không thu thập; vẫn biết tên khóa và vị trí sử dụng.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không đọc .env thật hoặc in source snippet chứa secret.

##### AC-L3GEN-014-04

- **Given:** Không resolve được tên khóa động.
- **When:** người dùng xem cấu hình.
- **Then:** giữ biểu thức và nguồn với nhãn partial; không đoán tên hoặc giá trị.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kể cả có key cùng tên trong file khác.

##### AC-L3GEN-014-05

- **Given:** Repository Java đọc cấu hình qua cơ chế thuộc phạm vi đã công bố của Spring Boot.
- **When:** người dùng phân tích.
- **Then:** khóa cấu hình Java hiện ra cùng nơi sử dụng và cùng quy tắc che giá trị bí mật như phía Python; không lộ giá trị thật.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Cơ chế cấu hình và schema YAML được phép diễn giải chốt tại OQ-L3GEN-003. Cơ chế ngoài phạm vi phải hiện ở phần giới hạn.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-015](../../requirements/fr/FR-L3GEN-015.md) · revision 3 · status draft · SHA-256 `391f9f9ad3071729e33fd72f7b8e7e0d68567b551fddab535de4efe6028ea212`

### FR-L3GEN-015 — Xem quan hệ phát và nhận sự kiện

#### Mô tả

Người dùng xem producer/consumer và topic của Kafka; biết phần thiếu và quan hệ nào chỉ là ứng viên. Broker khác Kafka nằm ngoài phạm vi và phải hiện ra ở phần giới hạn.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M3 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-015-01

- **Given:** Ứng dụng dùng confluent_kafka Producer.produce và Consumer.subscribe với topic literal.
- **When:** người dùng phân tích.
- **Then:** có producer, consumer, topic, component và nguồn của từng quan hệ publishes/consumes.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kafka là adapter event duy nhất trong phạm vi. Python và Java có hai bộ rule riêng, kiểm từng bộ.

##### AC-L3GEN-015-02

- **Given:** Topic/broker được tạo động hoặc lấy từ cấu hình chưa resolve.
- **When:** người dùng xem event model.
- **Then:** giữ phần biết được, đánh dấu partial/unknown và lý do; không đoán broker hoặc topic triển khai.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không chạy broker hay code để suy đích.

##### AC-L3GEN-015-03

- **Given:** Hai service cùng tên topic nhưng chưa chứng minh cùng broker/namespace.
- **When:** người dùng xem dependency.
- **Then:** công cụ không khẳng định giao tiếp giữa chúng; có thể hiển thị candidate kèm phần cần xác minh.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Khi chứng minh cùng identity thì mới gộp thành topic chung.

##### AC-L3GEN-015-04

- **Given:** Repository dùng broker khác Kafka, ví dụ RabbitMQ, Celery hoặc SQS.
- **When:** người dùng phân tích.
- **Then:** giới hạn chỉ ra broker đó ngoài phạm vi khi có bằng chứng nhận diện; phần route/DB còn lại vẫn được xử lý.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm với RabbitMQ, Celery và SQS: phải báo ngoài phạm vi, không mô tả repository như không có event.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-016](../../requirements/fr/FR-L3GEN-016.md) · revision 3 · status draft · SHA-256 `f272193022b4f2e18cb38452911d4a73e6bc6948eea34a4279a17cda71127eb9`

### FR-L3GEN-016 — Nhận Git URL và bản nén repository

#### Mô tả

Người dùng gửi Git URL công khai hoặc ZIP source qua web để tạo snapshot phân tích; local path chỉ dành CLI hoặc thư mục server được cho phép.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tiếp nhận và quản lý phân tích |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M2 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-016-01

- **Given:** Git URL HTTPS công khai tới GitHub và commit/ref hợp lệ.
- **When:** người dùng gửi yêu cầu phân tích.
- **Then:** dịch vụ lấy snapshot, ghi commit thực tế và ref yêu cầu; trạng thái và lỗi lấy repo hiển thị rõ.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-REL-001, NFR-L3GEN-SEC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** MVP không nhận credential trong URL hoặc private repo.

##### AC-L3GEN-016-02

- **Given:** ZIP hợp lệ nằm trong giới hạn NFR.
- **When:** người dùng tải lên.
- **Then:** dịch vụ tạo vùng phân tích riêng, giữ digest của nội dung, báo số file/phạm vi trước khi trả kết quả.
- `constrained_by:` [NFR-L3GEN-PERF-001, NFR-L3GEN-REL-001, NFR-L3GEN-SEC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không dùng tên file khách gửi làm đường dẫn tùy ý.

##### AC-L3GEN-016-03

- **Given:** URL trỏ mạng nội bộ/redirect ngoài danh sách cho phép hoặc ZIP chứa traversal/symlink nguy hiểm/bomb.
- **When:** người dùng gửi đầu vào.
- **Then:** yêu cầu bị từ chối an toàn với lý do; không truy cập địa chỉ cấm, không ghi ra ngoài vùng xử lý.
- `constrained_by:` [NFR-L3GEN-PERF-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-REL-001, NFR-L3GEN-SEC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Giới hạn và dọn dữ liệu theo NFR; không chạy hook/submodule/code.

##### AC-L3GEN-016-04

- **Given:** Nguồn không truy cập được, bị quá giới hạn hoặc tải thất bại.
- **When:** người dùng theo dõi yêu cầu.
- **Then:** trạng thái failed và lý do xuất hiện; không dùng snapshot cũ thay thế; người dùng có thể gửi lại.
- `constrained_by:` [NFR-L3GEN-PERF-001, NFR-L3GEN-REL-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không khẳng định mọi lỗi mạng là lỗi repository.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-017](../../requirements/fr/FR-L3GEN-017.md) · revision 4 · status draft · SHA-256 `da789e38294e0405eed6df56994eb11acfce9ede53caa5b47474fc79b32a2442`

### FR-L3GEN-017 — Theo dõi phiên phân tích và lấy kết quả qua API

#### Mô tả

Mỗi yêu cầu có định danh, trạng thái và kết quả riêng để giao diện hoặc hệ thống tích hợp theo dõi.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tiếp nhận và quản lý phân tích |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M2 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-017-01

- **Given:** Đầu vào hợp lệ được chấp nhận.
- **When:** client tạo yêu cầu phân tích.
- **Then:** nhận analysis_id và trạng thái queued; theo dõi được running, completed, partial, failed hoặc cancelled cùng thông tin lỗi.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không hứa phần trăm tiến độ nếu chưa có cơ sở tính.

##### AC-L3GEN-017-02

- **Given:** Hai yêu cầu phân tích chạy đồng thời.
- **When:** client đọc trạng thái và kết quả.
- **Then:** mỗi yêu cầu chỉ trả snapshot/output của chính nó, có giới hạn tài nguyên theo NFR.
- `constrained_by:` [NFR-L3GEN-PERF-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-REL-001, NFR-L3GEN-SEC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không dùng một thư mục output chung.

##### AC-L3GEN-017-03

- **Given:** Phiên đã hoàn tất và chưa hết hạn lưu.
- **When:** người dùng mở danh sách phiên hoặc API kết quả.
- **Then:** xem được trạng thái, source snapshot, thời điểm và tải JSON/Markdown/Mermaid; kết quả partial luôn có giới hạn.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Lịch sử tối thiểu trong một workspace tin cậy, không có so sánh drift giữa phiên.

##### AC-L3GEN-017-04

- **Given:** Phiên bị hủy, lỗi hoặc hết hạn lưu.
- **When:** client yêu cầu kết quả.
- **Then:** nhận trạng thái và thông báo phù hợp; hủy xử lý có kiểm soát, dọn source theo NFR; không hiện artifact thiếu như kết quả hoàn tất.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Hợp đồng endpoint/status cụ thể làm sau Scope Gate.

##### AC-L3GEN-017-05

- **Given:** Một repository đã được phân tích nhiều lần và vượt số lần được giữ.
- **When:** người dùng mở danh sách phiên của repository đó.
- **Then:** hệ thống giữ số lần phân tích gần nhất theo ngưỡng ở NFR-L3GEN-PRIV-001 và loại lần cũ nhất khi vượt; người dùng biết kết quả nào đã bị loại và vì sao, không gặp mục trống hoặc link hỏng.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Tạo vượt ngưỡng số lần rồi kiểm số bản còn lại và bản bị loại; kiểm cả mốc hết hạn. Cả hai ngưỡng lấy từ NFR-L3GEN-PRIV-001, không gõ lại ở đây.

##### AC-L3GEN-017-06

- **Given:** Một kết quả phân tích còn hạn lưu.
- **When:** người dùng chọn xóa nó.
- **Then:** hệ thống hỏi xác nhận trước khi xóa; xóa xong thì không mở lại được, source tạm và output của riêng phiên đó bị dọn theo NFR-L3GEN-PRIV-001, và các phiên khác không bị ảnh hưởng.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm cả xóa thủ công lẫn hết hạn tự động; xác nhận dữ liệu đã dọn thật, không chỉ ẩn khỏi danh sách.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-018](../../requirements/fr/FR-L3GEN-018.md) · revision 1 · status draft · SHA-256 `d0db685b15b8edd8dd9c46ecd0b21756aca556077c161651944a244888885d53`

### FR-L3GEN-018 — Xem thư viện bên ngoài mà hệ thống phụ thuộc

#### Mô tả

Người dùng xem các thư viện bên ngoài mà đơn vị phân tích khai báo hoặc sử dụng, kèm nơi khai báo làm bằng chứng. Danh sách này nói repository dựa trên nền công nghệ nào; nó không phải quan hệ phụ thuộc giữa các component, vốn thuộc FR-L3GEN-011.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Phân tích repository |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-018-01

- **Given:** Đơn vị phân tích có file khai báo thư viện thuộc định dạng hỗ trợ.
- **When:** người dùng phân tích repository.
- **Then:** công cụ liệt kê tên thư viện và phiên bản khai báo, kèm đường dẫn file và vị trí dòng làm bằng chứng; thư viện không có khai báo phiên bản được ghi là chưa ghim phiên bản, không tự điền một phiên bản nào.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu danh sách với nội dung file khai báo trên repo mẫu. Không suy phiên bản đang cài đặt thực tế từ file khai báo.

##### AC-L3GEN-018-02

- **Given:** Đơn vị phân tích dùng định dạng khai báo thư viện chưa được hỗ trợ, hoặc không có file khai báo nào.
- **When:** người dùng phân tích repository.
- **Then:** công cụ ghi phần chưa đọc được kèm lý do và đường dẫn, nêu rõ danh sách thư viện của đơn vị đó là không đầy đủ; không trả danh sách rỗng như một kết luận rằng đơn vị không dùng thư viện nào.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-REL-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm đơn vị không có file khai báo và đơn vị dùng định dạng ngoài phạm vi công bố.

##### AC-L3GEN-018-03

- **Given:** File khai báo liệt kê nhiều thư viện, trong đó chỉ một phần có dấu vết được dùng trong mã nguồn đã phân tích.
- **When:** người dùng xem danh sách thư viện.
- **Then:** mỗi thư viện mang nhãn phân biệt được khai báo và có dấu vết sử dụng trong mã, kèm bằng chứng cho nhãn có dấu vết sử dụng; thư viện chỉ có trong khai báo không bị công bố là đang được dùng.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu nhãn với import thật trong phạm vi mã đã phân tích. Không đảo ngược: thiếu dấu vết sử dụng không có nghĩa thư viện chắc chắn không được dùng, vì phạm vi phân tích có giới hạn.

##### AC-L3GEN-018-04

- **Given:** File khai báo thư viện chứa chuỗi kết nối, mã truy cập hoặc giá trị bí mật khác.
- **When:** người dùng xem danh sách thư viện.
- **Then:** công cụ hiển thị tên và phiên bản thư viện nhưng che giá trị bí mật theo NFR-L3GEN-SEC-001; bằng chứng chỉ trỏ tới vị trí, không chép lại giá trị bí mật vào bộ kết quả.
- `constrained_by:` [NFR-L3GEN-SEC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm trên file khai báo có nhúng thông tin xác thực trong URL nguồn gói.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

#### Phạm vi định dạng hỗ trợ

Danh sách định dạng khai báo được hỗ trợ bám theo hai stack đã chốt ở FR-L3GEN-002 và phụ thuộc kết quả OQ-L3GEN-003; không công bố định dạng nào trước khi có quyết định đó.

## 4. Thay đổi hành vi hiện có

Không có baseline sản phẩm đã approved để so diff. PRD không lấy hành vi code hiện tại làm chuẩn.

## 5. NGOÀI phạm vi lần này

**Phạm vi phân tích**

- Hỗ trợ đầy đủ mọi ngôn ngữ, framework, mọi kiểu SQL/ORM hoặc mọi semantics của Python và Java. Trong phạm vi chỉ có Python/FastAPI và Java/Spring Boot.
- Framework Java ngoài Spring Boot.
- Message broker khác Kafka trong repository đầu vào, ví dụ RabbitMQ, Celery hoặc SQS. Gặp thì báo ngoài phạm vi, không mô tả repository như không có event.
- Resolve chính xác mọi function/method call.
- Thực thi source để khám phá runtime, trace/sequence thực thi, dynamic import và metaprogramming tổng quát.
- Suy luận deployment topology khi source và config không đủ bằng chứng.

**Mức trình bày**

- Sơ đồ hoặc tài liệu vẽ toàn bộ function/class của repository, và call graph đầy đủ ở mức function như một đầu ra cho người đọc.
- Repository Knowledge Graph nói chung: graph query API, graph traversal, incremental graph và nối mọi tham chiếu trong repository. Đây là phạm vi của một dự án khác (đề bài mục 3.8); muốn đưa vào cần đề xuất phạm vi và AC riêng.

**Ghi ngược và phân tích thay đổi**

- Sửa code hoặc tài liệu nguồn tự động, tạo pull request, ghi ngược vào repository đầu vào.
- Rà code không dùng, cách xử lý lỗi HTTP, kết luận lỗ hổng bảo mật hoặc lỗi nghiệp vụ.
- Change impact, test impact, architecture drift và incremental analysis.
- Chỉnh model thủ công trên UI, so sánh drift giữa các snapshot, trigger CI tự động.

**Truy cập và vận hành**

- GitHub private repository và mọi cơ chế nhận hoặc lưu credential truy cập.
- Git submodules, đăng nhập/SSO và multi-tenant public hosting.
- Quản trị tài khoản người dùng và phân quyền tổ chức.
- Khám phá kiến trúc tương tác và lịch sử phân tích trên dòng lệnh; đây là phạm vi của kênh web.
- SLA production cấp doanh nghiệp; bằng chứng release và vận hành sẽ được thiết kế phù hợp cách triển khai được duyệt.

**AI**

- AI tự tạo dữ kiện, quan hệ, cạnh, framework rule hoặc thay đổi kết quả phân tích.

Các mục trên muốn đưa vào phạm vi đều cần đề xuất phạm vi và AC riêng.

Không có FR chuẩn tắc nào bị giấu khỏi candidate.

## 6. Ràng buộc mới

---

Nguồn: [NFR-L3GEN-ABST-001](../../requirements/nfr/NFR-L3GEN-ABST-001.md) · revision 1 · status draft · SHA-256 `8254e33535e6e225261b7f506cbb3ece027fe67ff69703888ccd919acce42f5d`

### NFR-L3GEN-ABST-001 — Mức trừu tượng của kết quả trình bày

- **Nhóm:** Abstraction level.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-006](../../requirements/fr/FR-L3GEN-006.md), [FR-L3GEN-007](../../requirements/fr/FR-L3GEN-007.md), [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md), [FR-L3GEN-011](../../requirements/fr/FR-L3GEN-011.md), [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md).
- **Quyết định nền:** [ADR-2026-001](../../architecture/adr/ADR-2026-001.md).

#### Yêu cầu có thể kiểm chứng

Phân tích và trình bày là hai mức khác nhau. Engine được đọc sâu tới function, tham số, thuộc tính và phép gán để chứng minh một quan hệ; nhưng kết quả mặc định cho người đọc dừng ở application/component.

Ràng buộc đề xuất:

- Sơ đồ và tài liệu L3 mặc định chỉ có node mức application, component và hệ thống ngoài. Node mức function, class hoặc file không xuất hiện ở lớp mặc định.
- Số node trong một sơ đồ mặc định không tỷ lệ với số function của repository. Ngưỡng đề xuất: repository có ≥500 function vẫn cho sơ đồ mặc định ≤50 node; vượt ngưỡng phải rút gọn có thông báo theo AC-L3GEN-008-03, không xuất sơ đồ đầy đủ rồi để người đọc tự lọc.
- Dữ kiện mức function/class vẫn được giữ trong bộ kết quả, nhưng nằm ở lớp evidence hoặc chẩn đoán có nhãn riêng, không trộn vào lớp kiến trúc mặc định.
- Một quan hệ kiến trúc chỉ tồn tại khi đích đã resolve. Lời gọi chưa resolve được giữ như dữ kiện có nhãn unknown, không được nâng thành cạnh giữa hai component.

Ngưỡng 500/50 là con số đề xuất để có thể kiểm chứng, chưa đo trên tập fixture đã pin; chốt tại OQ-L3GEN-004.

#### Điều kiện và cách kiểm

Chạy trên fixture đã pin, đếm node theo lớp trong bộ kết quả máy đọc được của FR-L3GEN-008, không đếm bằng mắt trên hình. Kiểm cả repository nhỏ và repository ≥500 function. Kiểm rằng bỏ lớp evidence đi thì lớp kiến trúc vẫn đọc được, và mọi cạnh kiến trúc đều có đích đã resolve. Không coi việc sơ đồ vẽ được là bằng chứng mức trừu tượng đúng.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [ADR-2026-001](../../architecture/adr/ADR-2026-001.md).
- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

---

Nguồn: [NFR-L3GEN-ACC-001](../../requirements/nfr/NFR-L3GEN-ACC-001.md) · revision 2 · status draft · SHA-256 `d5fe86cad17bdd4197aeb9e566ea3558b353c5091592fc29f7f64b4dc96f3b9a`

### NFR-L3GEN-ACC-001 — Độ đúng của dữ kiện và component

- **Nhóm:** Accuracy.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-003](../../requirements/fr/FR-L3GEN-003.md), [FR-L3GEN-004](../../requirements/fr/FR-L3GEN-004.md), [FR-L3GEN-005](../../requirements/fr/FR-L3GEN-005.md), [FR-L3GEN-006](../../requirements/fr/FR-L3GEN-006.md), [FR-L3GEN-011](../../requirements/fr/FR-L3GEN-011.md), [FR-L3GEN-014](../../requirements/fr/FR-L3GEN-014.md), [FR-L3GEN-015](../../requirements/fr/FR-L3GEN-015.md).

#### Yêu cầu có thể kiểm chứng

Ngưỡng đề xuất trước nghiệm thu: precision nhóm exact ≥95% cho từng loại route, entity, HTTP, config, event và internal call edge; recall lần lượt route ≥85%, entity ≥90%, HTTP ≥80%, config ≥80%, event ≥80%, internal call edge trong pattern công bố ≥70%. Đánh giá đúng thuộc tính riêng: không tính một URL thiếu prefix là URL đầy đủ đúng; không tính tên bảng suy sai là tên bảng đúng. Fixture thuộc pattern cam kết phải thỏa tất cả AC. Component grouping so với mapping người duyệt: precision và recall của membership đều ≥85%; dependency exact ≥95% precision. Không dùng tên role inferred như ground truth nghiệp vụ.

#### Điều kiện và cách kiểm

OBS-L3GEN-001 quy định đáp án độc lập, sampling, matching và cỡ mẫu. Mỗi nhóm không đủ mẫu báo counts và not_evaluated thay vì 100%; ngoài pattern công bố báo độ phủ riêng, không loại ca khó sau khi xem output. Ngưỡng đang đề xuất, chưa có kết quả nghiệm thu.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

---

Nguồn: [NFR-L3GEN-AI-001](../../requirements/nfr/NFR-L3GEN-AI-001.md) · revision 2 · status draft · SHA-256 `632ca59768328144cba3b841929564d1f3a837a50cb6756d80ba206033c35cdd`

### NFR-L3GEN-AI-001 — Giới hạn và ranh giới AI

- **Nhóm:** AI reliability.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-010](../../requirements/fr/FR-L3GEN-010.md), [FR-L3GEN-012](../../requirements/fr/FR-L3GEN-012.md).

#### Yêu cầu có thể kiểm chứng

AI không được sửa IAM/architecture model, tạo entity/edge hoặc category finding mới. Chỉ nhận output đúng schema và ID đã có. Mỗi request timeout tối đa 30 giây, retry tối đa 2 lần; mỗi phiên tối đa 20 request. Chi phí/token cap phải cấu hình trước khi bật với provider được chọn; chưa có cấu hình cap thì không gọi AI. Rate limit, thiếu key/SDK hoặc cap đạt thì tiếp tục trả dữ kiện tĩnh và cảnh báo. Provider là tham số cấu hình, không khóa cứng vào một hãng; khóa API do người dùng cung cấp tại thời điểm chạy và không được ghi vào output, log, evidence hay bộ kết quả lưu lại. Công cụ không phát biểu thay người dùng về mức an toàn dữ liệu của provider họ chọn; điều khoản của provider thuộc trách nhiệm người dùng.

#### Điều kiện và cách kiểm

Mock provider trả JSON hỏng, ID lạ, chèn route, timeout, 429 và trả mô tả khác; so sánh model trước/sau. Kiểm request count và logging. Đặt khóa API dạng canary rồi kiểm toàn bộ output, log và evidence không chứa giá trị đó; kiểm đổi provider bằng cấu hình mà không sửa code. Ngân sách thật/provider chờ OQ, không dùng giá hay model giả.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

---

Nguồn: [NFR-L3GEN-COMP-001](../../requirements/nfr/NFR-L3GEN-COMP-001.md) · revision 5 · status draft · SHA-256 `78cafd2939ba82a034a38638c58e128057dc6f46fb6d6176a8a406d013b1203e`

### NFR-L3GEN-COMP-001 — Stack và môi trường được hỗ trợ

- **Nhóm:** Compatibility.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md), [FR-L3GEN-002](../../requirements/fr/FR-L3GEN-002.md), [FR-L3GEN-003](../../requirements/fr/FR-L3GEN-003.md), [FR-L3GEN-004](../../requirements/fr/FR-L3GEN-004.md), [FR-L3GEN-005](../../requirements/fr/FR-L3GEN-005.md), [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md), [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md), [FR-L3GEN-014](../../requirements/fr/FR-L3GEN-014.md), [FR-L3GEN-015](../../requirements/fr/FR-L3GEN-015.md).

#### Yêu cầu có thể kiểm chứng

Đề bài cho phép ưu tiên 1–2 stack. Product chốt hai stack: Python/FastAPI và Java/Spring Boot. Ma trận phiên bản và thư viện dưới đây còn là đề xuất; Tech Lead/QA đối chiếu repo mẫu tại OQ-L3GEN-003/004 trước khi chốt, không dùng khả năng của code hiện có làm căn cứ duy nhất.

Stack thứ nhất — Python: cú pháp Python 3.10–3.12; FastAPI methods GET/POST/PUT/DELETE/PATCH; SQLAlchemy declarative Column; requests/httpx; Pydantic settings; confluent_kafka. SQLModel, mapped_column, method khác và SDK khác phải có capability riêng trước khi được gọi là hỗ trợ.

Stack thứ hai — Java: Spring Boot. Framework Java ngoài Spring Boot nằm ngoài phạm vi và phải hiện ra ở phần giới hạn. Ma trận annotation, ORM và thư viện Kafka phía Java được chốt ở thiết kế trước khi gọi là hỗ trợ.

Hai stack dùng chung contract kết quả nhưng không dùng chung rule: adapter Kafka của Python và của Java là hai bộ riêng. Event chỉ hỗ trợ Kafka; broker khác nằm ngoài phạm vi.

Phiên bản runtime của chính công cụ được chọn và pin ở thiết kế.

Môi trường sử dụng đề xuất: CLI trên Windows 11 và Ubuntu 24.04, hỗ trợ tên file/path Unicode và có dấu cách; web trên Chrome và Edge. Phiên bản browser ổn định dùng để kiểm được ghi cụ thể tại thời điểm kiểm; Mermaid renderer/version pin ở contract.

#### Điều kiện và cách kiểm

Chạy cùng bộ supported fixtures trên cả hai OS; ghi interpreter, package/rule/renderer/browser versions. Lỗi cú pháp do version ngoài phạm vi phải được báo rõ. Có ma trận supported/partial/unsupported thay cho một checkbox hỗ trợ cả ngôn ngữ.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

---

Nguồn: [NFR-L3GEN-DET-001](../../requirements/nfr/NFR-L3GEN-DET-001.md) · revision 2 · status draft · SHA-256 `031959aba7200e5b32f728f1f76312c6638d79f0e4b399e2dbf314136b61efea`

### NFR-L3GEN-DET-001 — Tái lập dữ kiện và định danh

- **Nhóm:** Determinism.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md), [FR-L3GEN-006](../../requirements/fr/FR-L3GEN-006.md), [FR-L3GEN-007](../../requirements/fr/FR-L3GEN-007.md), [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md), [FR-L3GEN-010](../../requirements/fr/FR-L3GEN-010.md), [FR-L3GEN-011](../../requirements/fr/FR-L3GEN-011.md), [FR-L3GEN-012](../../requirements/fr/FR-L3GEN-012.md), [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md), [FR-L3GEN-016](../../requirements/fr/FR-L3GEN-016.md).

#### Yêu cầu có thể kiểm chứng

Cùng snapshot source, cấu hình phân tích, rule version và tool version phải cho cùng cấu trúc, cạnh, nhãn và ID trong JSON chuẩn hóa, độc lập output directory, chế độ AI và **kênh sử dụng**. Timestamp, duration, analysis_id và đường dẫn workspace tuyệt đối thuộc run metadata, không làm đổi ID dữ kiện. L3 phần diễn giải AI không nằm trong cam kết byte-identical.

**Độc lập kênh.** CLI nhận thư mục local (FR-L3GEN-001), web nhận Git URL hoặc ZIP (FR-L3GEN-016). Cùng một source đi qua hai kênh phải cho cùng tập application, component, route, entity, external system, cạnh dependency, nhãn confidence/completeness và cùng danh sách limitation. Được phép khác: đường dẫn gốc trong evidence, vì hai kênh đặt source ở vị trí khác nhau; vị trí tương đối trong repository phải giống nhau. Web có thêm màn hình khám phá và lịch sử, nhưng không được sinh thêm hoặc bớt dữ kiện so với CLI.

#### Điều kiện và cách kiểm

Chạy 3 lần vào các output khác nhau, trong đó bật AI stub với mô tả khác; so sánh canonical JSON sau phép chuẩn hóa công bố. Không sửa timestamp/duration thành hằng để làm test pass. Chạy lại sau source edit phải đổi digest và phần liên quan.

Kiểm độc lập kênh: pin một repository ở một commit, chạy CLI trên bản trên đĩa và chạy web trên bản ZIP của cùng commit đó, cùng tắt AI; so sánh canonical JSON sau khi chuẩn hóa đường dẫn gốc. Khác biệt ở bất kỳ fact, quan hệ, nhãn hoặc limitation nào là lỗi chặn phát hành, không phải khác biệt về trình bày.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

---

Nguồn: [NFR-L3GEN-PERF-001](../../requirements/nfr/NFR-L3GEN-PERF-001.md) · revision 2 · status draft · SHA-256 `0fa48f9b5e0a981664f9ae1f1976e52caa441a9e411c4afaf900c24d9a59eba4`

### NFR-L3GEN-PERF-001 — Thời gian xử lý và giới hạn tài nguyên

- **Nhóm:** Performance.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md), [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md), [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md), [FR-L3GEN-016](../../requirements/fr/FR-L3GEN-016.md), [FR-L3GEN-017](../../requirements/fr/FR-L3GEN-017.md).

#### Yêu cầu có thể kiểm chứng

Môi trường benchmark đề xuất: 4 CPU logical, RAM 8 GiB, SSD, Python 3.12, no-AI, dependencies đã cài. Thời gian analyzer+ghi output (không gồm clone/AI/cài đặt) tối đa 60 giây cho 5.000 dòng Python, và 300 giây cho 50.000 dòng trong tập fixture/repo đã pin. Trần thời gian cho một lần phân tích là 10 phút; quá hạn thì dừng và báo lý do, không trả kết quả như đã hoàn tất.

Giới hạn tiếp nhận: ZIP nén 100 MB, giải nén 500 MB và 50.000 file; vượt ngưỡng phải từ chối hoặc dừng có lý do. Worker tối đa 2 GiB RAM/phiên, 2 phiên chạy cùng lúc; phiên sau xếp hàng. Git fetch timeout 120 giây; mọi giới hạn có trong thông báo/help.

#### Điều kiện và cách kiểm

Đo 5 lần cho mỗi repo trên máy công bố, ghi từng lần và worst-case, peak RSS. Không ngoại suy từ máy khác hoặc repo nhỏ. Kiểm input sát/vượt giới hạn, ZIP bomb và job bị timeout; không báo hoàn tất khi bị dừng. OBS-L3GEN-001 mô tả cách thu số, không lặp ngưỡng.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

---

Nguồn: [NFR-L3GEN-PRIV-001](../../requirements/nfr/NFR-L3GEN-PRIV-001.md) · revision 3 · status draft · SHA-256 `6b843918be87295a3f6a68830db4c7055da0e5df07ce6ad96b117b58bdaeb523`

### NFR-L3GEN-PRIV-001 — Quyền riêng tư và vòng đời dữ liệu

- **Nhóm:** Privacy.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-005](../../requirements/fr/FR-L3GEN-005.md), [FR-L3GEN-007](../../requirements/fr/FR-L3GEN-007.md), [FR-L3GEN-010](../../requirements/fr/FR-L3GEN-010.md), [FR-L3GEN-012](../../requirements/fr/FR-L3GEN-012.md), [FR-L3GEN-014](../../requirements/fr/FR-L3GEN-014.md), [FR-L3GEN-016](../../requirements/fr/FR-L3GEN-016.md), [FR-L3GEN-017](../../requirements/fr/FR-L3GEN-017.md).

#### Yêu cầu có thể kiểm chứng

AI mặc định tắt; phải chủ động bật và biết provider, loại dữ liệu gửi. --no-ai không có outbound ở analyzer; CLI local no-AI không cần mạng; Git URL vẫn cần mạng để lấy repo đã được yêu cầu. Không đọc .env thật, private key hoặc gửi credentials. AI chỉ nhận model tối thiểu đã lọc giá trị nhạy cảm; source snippet cần đồng ý riêng và không thuộc bản đầu. Source tạm của web được xóa trong 24 giờ sau trạng thái cuối; output và metadata giữ tối đa 14 ngày. Mỗi repository giữ tối đa 10 lần phân tích gần nhất, vượt thì loại lần cũ nhất. Người dùng xóa được một kết quả trước hạn. Hành vi cụ thể ở AC-L3GEN-017-05 và AC-L3GEN-017-06. CLI output do người dùng quản lý và ghi rõ khác biệt này.

#### Điều kiện và cách kiểm

Dùng canary secrets ở .env, YAML và URL, kiểm log/output/payload không có giá trị; kiểm no-AI bằng network interception và phân biệt ingestion/analyzer. Test clock/cleanup sau hạn, hủy/lỗi và xóa sớm. Không coi bộ lọc secret là chứng minh phát hiện mọi bí mật tùy ý.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

---

Nguồn: [NFR-L3GEN-REL-001](../../requirements/nfr/NFR-L3GEN-REL-001.md) · revision 2 · status draft · SHA-256 `3f3ff2932d3806bba32c1a2e6589daf90a728bcd607ad7343129b597f9906b95`

### NFR-L3GEN-REL-001 — Hoàn tất, lỗi một phần và cách ly phiên

- **Nhóm:** Reliability.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md), [FR-L3GEN-002](../../requirements/fr/FR-L3GEN-002.md), [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md), [FR-L3GEN-009](../../requirements/fr/FR-L3GEN-009.md), [FR-L3GEN-016](../../requirements/fr/FR-L3GEN-016.md), [FR-L3GEN-017](../../requirements/fr/FR-L3GEN-017.md).

#### Yêu cầu có thể kiểm chứng

Parse lỗi một file không phá phần hợp lệ. Trạng thái partial dựa trên phạm vi mất hoặc thuộc tính/quan hệ chưa giải được, không chỉ files_skipped. Một bộ output chỉ được đánh dấu hoàn tất khi mọi artifact bắt buộc cho phase đã ghi và kiểm cấu trúc thành công. Source gốc và output lần trước không bị sửa. Job song song có workspace riêng; hủy/lỗi không để job running vĩnh viễn.

#### Điều kiện và cách kiểm

Fault injection tại scan, parse, clone, ghi output, worker crash, cancel; xác nhận trạng thái cuối, file nguồn không đổi và phiên khác không lẫn dữ liệu. Các số đếm phải có định nghĩa tập file rõ.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

---

Nguồn: [NFR-L3GEN-SEC-001](../../requirements/nfr/NFR-L3GEN-SEC-001.md) · revision 2 · status draft · SHA-256 `f07a9c3d9549d7b617ca4ae8c04b5317bbce25e337e2035a6055785c450cbe65`

### NFR-L3GEN-SEC-001 — An toàn khi tiếp nhận và phân tích source

- **Nhóm:** Security.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md), [FR-L3GEN-002](../../requirements/fr/FR-L3GEN-002.md), [FR-L3GEN-010](../../requirements/fr/FR-L3GEN-010.md), [FR-L3GEN-016](../../requirements/fr/FR-L3GEN-016.md), [FR-L3GEN-017](../../requirements/fr/FR-L3GEN-017.md).

#### Yêu cầu có thể kiểm chứng

Không import, exec, eval, chạy entrypoint, cài dependency, hook Git hoặc submodule của repository đầu vào. Đọc/giải nén chỉ trong vùng được cấp; không đi theo symlink ra ngoài. Input Git ban đầu chỉ HTTPS GitHub public; từ chối host khác, địa chỉ private/loopback/link-local và redirect trái allowlist; kiểm lại đích kết nối sau DNS/redirect. Web local/workspace tin cậy, không công khai Internet khi chưa có authentication, phân quyền và threat model tương ứng.

#### Điều kiện và cách kiểm

Repo có sentinel tạo file/gọi mạng khi import, ZIP traversal/symlink, URL nội bộ và redirect cấm đều không gây thực thi/truy cập/ghi ngoài phạm vi. Kiểm input trả lỗi rõ và cleanup. Threat model/kiểm thử an toàn bắt buộc trước web release; chưa có kết quả kiểm.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

---

Nguồn: [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md) · revision 2 · status draft · SHA-256 `37b5501c27aba492b2cfe39fd0415ef521c3a66ccfaa1ec6558b94ab4e17cec8`

### NFR-L3GEN-TRACE-001 — Nguồn bằng chứng và phiên bản

- **Nhóm:** Traceability.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-002](../../requirements/fr/FR-L3GEN-002.md), [FR-L3GEN-003](../../requirements/fr/FR-L3GEN-003.md), [FR-L3GEN-004](../../requirements/fr/FR-L3GEN-004.md), [FR-L3GEN-005](../../requirements/fr/FR-L3GEN-005.md), [FR-L3GEN-006](../../requirements/fr/FR-L3GEN-006.md), [FR-L3GEN-007](../../requirements/fr/FR-L3GEN-007.md), [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md), [FR-L3GEN-011](../../requirements/fr/FR-L3GEN-011.md), [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md), [FR-L3GEN-014](../../requirements/fr/FR-L3GEN-014.md), [FR-L3GEN-015](../../requirements/fr/FR-L3GEN-015.md).

#### Yêu cầu có thể kiểm chứng

Mọi thực thể và cạnh khẳng định phải truy về một hoặc nhiều vị trí source trong snapshot đã phân tích; evidence coverage yêu cầu 100% trong tập khẳng định. Inferred ghi rule/reason; unresolved không giả đích. Snapshot có digest, tool/rule/config version; Git commit chỉ đại diện clean snapshot, local dirty tree dùng content digest. Không lấy số dòng hiện tại thay bằng chứng cũ khi source thay đổi.

#### Điều kiện và cách kiểm

Đối chiếu toàn bộ evidence về file/range còn trong snapshot; lấy mẫu người đọc xác nhận range thực sự hỗ trợ claim. Kiểm render từ output khác thư mục, source di chuyển, dirty worktree và multi-evidence edges.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

---

Nguồn: [NFR-L3GEN-USA-001](../../requirements/nfr/NFR-L3GEN-USA-001.md) · revision 2 · status draft · SHA-256 `5d01746fffe1881a8ee67c49acf6e97415721a09d3259791448f38e95baf9a45`

### NFR-L3GEN-USA-001 — Khả năng sử dụng và tiếp cận

- **Nhóm:** Usability.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md), [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md), [FR-L3GEN-009](../../requirements/fr/FR-L3GEN-009.md), [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md), [FR-L3GEN-017](../../requirements/fr/FR-L3GEN-017.md).

#### Yêu cầu có thể kiểm chứng

Người mới theo README cài và chạy ví dụ CLI no-AI trong tối đa 10 phút trên môi trường đã có Python và mạng cài package. Web có trạng thái rỗng/tải/lỗi/một phần, thông báo hành động khắc phục. Luồng chính dùng được bằng bàn phím; mọi input có label, focus nhìn thấy; thông tin tin cậy không dựa chỉ vào màu. Review UI kiểm viewport 1366×768 và 390×844; accessibility tự động và kiểm tay, ngưỡng tương phản normal text ≥4.5:1 theo chuẩn nội bộ đề xuất.

#### Điều kiện và cách kiểm

Web cung cấp cả chế độ sáng và tối; người dùng chọn được chế độ. Kiểm bàn phím, focus và tương phản ở cả hai chế độ, kể cả trạng thái rỗng/tải/lỗi/một phần. Đây là phạm vi áp dụng theo checklist UI/UX Gate của mentor, không có ngoại lệ một theme.

OBS-L3GEN-002 mô tả thử với người chưa dùng tool; không thay thử người bằng việc tác giả tự demo. Có lỗi input, output trống và graph dài trong buổi thử. Kiểm trên thiết bị chính thật và với chuỗi dài nhất của các ngôn ngữ được hỗ trợ; ghi thiết bị, browser, theme và kết quả. Mock dùng design token thật; thiết kế phải thể hiện một hành động chính rõ cho mỗi màn hình theo checklist gate.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-002.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

## 7. Câu hỏi mở còn lại

| OQ | Câu hỏi | Owner | Due |
|---|---|---|---|
| [OQ-L3GEN-001](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-001.md) | Xác nhận mã tổ chức và người chịu trách nhiệm | Khiêm | 2026-09-19 |
| [OQ-L3GEN-002](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-002.md) | Chốt phạm vi đầy đủ và lịch giao | Người phụ trách PRD phối hợp mentor | 2026-09-19 |
| [OQ-L3GEN-003](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-003.md) | Chốt ma trận pattern và adapter hỗ trợ | Tech Lead được mentor chỉ định | 2026-09-19 |
| [OQ-L3GEN-004](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-004.md) | Duyệt ngưỡng chất lượng và đáp án nghiệm thu | Product và QA được mentor chỉ định | 2026-09-19 |
| [OQ-L3GEN-006](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-006.md) | Xác nhận quy trình và schema khi thiếu tooling | Người phụ trách PRD phối hợp mentor | 2026-09-19 |
