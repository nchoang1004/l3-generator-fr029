---
key: CSV-CHG-L3GEN-2026-001
group: derived
non_normative: true
derived_from: [BL-CHG-L3GEN-2026-001-r14]
hand_written: false
status: candidate
generated_by: scripts/prd_package.py render --baseline BL-r14.yaml
---

# Full product — Code → Architecture / L3 Generator

Bản ứng viên chưa duyệt, sinh từ `BL-CHG-L3GEN-2026-001-r14`. Khi view và nguồn bất đồng, **FR/NFR/PRD nguồn thắng**; sửa nguồn rồi chạy lại script render. Không dùng view này như approval.

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

Nguồn: [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md) · revision 7 · status draft · SHA-256 `fc1e9d202cef360f3961da7793ade66a0474fd67cb25cca7b767383115ef9bf7`

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

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-002](../../requirements/fr/FR-L3GEN-002.md) · revision 6 · status draft · SHA-256 `44b24603efc0a3afaf93ea0676436702c536ef50f3041bf0ea256f63da33bd26`

### FR-L3GEN-002 — Nhận diện đơn vị phân tích và phạm vi hỗ trợ

#### Mô tả

Người dùng xem được những phần repository được phân tích, bị bỏ qua hoặc chưa xác định được stack, cùng các điểm khởi động ứng dụng dùng để xác định ranh giới đơn vị.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Phân tích repository |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1: Python/FastAPI; phase sau: Java/Spring Boot |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-002-01

- **Given:** Repository có service Python/FastAPI và service Java/Spring Boot thuộc ma trận hỗ trợ với manifest riêng.
- **When:** người dùng phân tích repository.
- **Then:** công cụ phân tích cả hai đơn vị theo capability đã công bố; pattern ngoài phạm vi được ghi rõ cùng lý do, không kết luận bao phủ mọi hành vi runtime.
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
- **Cách kiểm dự kiến:** Kiểm Python rỗng và Flask-only; Java/Spring Boot-only thuộc ma trận hỗ trợ phải được chấp nhận. Java ngoài ma trận phải báo giới hạn hoặc không hỗ trợ.

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

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-003](../../requirements/fr/FR-L3GEN-003.md) · revision 8 · status draft · SHA-256 `c7449d774e6aeb2bedfda100b09ea5f716eee9041242571c155e4e8ccaec94e4`

### FR-L3GEN-003 — Liệt kê API routes và handler

#### Mô tả

Người dùng xem method, path, handler, điều kiện đăng ký và nguồn khai báo của route trong phạm vi stack đã công bố. Phase đầu phủ FastAPI; Java/Spring Boot thuộc phase sau.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1: route FastAPI; phase sau: route Spring Boot |
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
- **Cách kiểm dự kiến:** Dùng ma trận Java roadmap đã chốt tại NFR-L3GEN-COMP-001; annotation ngoài ma trận phải hiện ở phần giới hạn, không im lặng bỏ qua. AC này thuộc phase sau.

#### Trạng thái liên kết triển khai

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-004](../../requirements/fr/FR-L3GEN-004.md) · revision 7 · status draft · SHA-256 `dab6e57d2007370bcce496d2ba6a8ac426a58ffee6e1a9b83c702fc863669c51`

### FR-L3GEN-004 — Liệt kê mô hình dữ liệu

#### Mô tả

Người dùng xem lớp dữ liệu, tên bảng nếu xác định được, cột và khóa ngoại; nhận diện entity không đồng nghĩa biết tên bảng. Phase đầu phủ SQLAlchemy; ORM của Java/Spring Boot thuộc phase sau.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1: entity SQLAlchemy; phase sau: entity Java |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-004-01

- **Given:** Lớp SQLAlchemy có __tablename__ hằng, Column và ForeignKey.
- **When:** người dùng phân tích.
- **Then:** công cụ xuất lớp, bảng, cột, kiểu, khóa chính và khóa ngoại được khai báo cùng nguồn.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Phạm vi phase đầu: `declarative_base`/`Base`, `Column`, `ForeignKey` và `relationship` trực tiếp; SQLModel/`mapped_column` nằm ngoài phase đầu theo NFR-L3GEN-COMP-001.

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
- **Cách kiểm dự kiến:** Dùng Jakarta Persistence trực tiếp theo ma trận Java roadmap ở NFR-L3GEN-COMP-001; ORM ngoài phạm vi phải hiện ở phần giới hạn. AC này thuộc phase sau.

#### Trạng thái liên kết triển khai

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-005](../../requirements/fr/FR-L3GEN-005.md) · revision 5 · status draft · SHA-256 `3611a95ed27624fdea2403a2f87d3b24f8adf96c79705aae1880ea977e8edb6a`

### FR-L3GEN-005 — Liệt kê lời gọi HTTP và đích bên ngoài

#### Mô tả

Người dùng xác định nơi gọi HTTP qua thư viện thuộc phạm vi đã công bố và mức độ biết đích đến; không đồng nhất mọi HTTP call với một hệ thống bên ngoài đã xác nhận. Phase đầu phủ requests/httpx của Python; client HTTP của Java/Spring Boot thuộc phase sau.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1: requests/httpx; phase sau: client HTTP phía Java |
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

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-006](../../requirements/fr/FR-L3GEN-006.md) · revision 5 · status draft · SHA-256 `b6b93d9f4d3e08b466d22e0f35c474ff9bda24e8ce6be3268ac689585ba5b43e`

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

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-007](../../requirements/fr/FR-L3GEN-007.md) · revision 5 · status draft · SHA-256 `f26c36258ad3ec495d26106227e8a4bd5067b4ea86a3ab37d28fe83f3f3750bd`

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

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md) · revision 7 · status draft · SHA-256 `d0cd7bc40349aef8cbd4da220a7fddd8b81ae098e963c13d0fb876d10f12f16a`

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

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-009](../../requirements/fr/FR-L3GEN-009.md) · revision 5 · status draft · SHA-256 `217d8bba8b68cf42018379c869ae2a27ee1b17fda444983c2a783807b302b171`

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

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-010](../../requirements/fr/FR-L3GEN-010.md) · revision 5 · status draft · SHA-256 `b956dfd1ed64a104902edbd467a884a1cefb2d90acefa0ed29c74098e8f7bcc1`

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

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-011](../../requirements/fr/FR-L3GEN-011.md) · revision 8 · status draft · SHA-256 `5e897c25f552ff7c7de60d1a7d743fa436ed07e6d707ace12ffbc278de40cb91`

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

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-012](../../requirements/fr/FR-L3GEN-012.md) · revision 6 · status draft · SHA-256 `83e4453835c0252a15fbda906f390e0c13be2774858ee1c8d9ef72b181f61e67`

### FR-L3GEN-012 — Bổ sung mô tả và diễn giải cảnh báo bằng AI

#### Mô tả

Sau khi người dùng chủ động cho phép, AI có thể bổ sung mô tả và giải thích giới hạn phân tích theo FR-L3GEN-009. Các cảnh báo này được tạo từ phân tích tĩnh, không cần AI.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tiện ích mở rộng |
| Ưu tiên đề xuất | Should Have |
| Mốc đề xuất | Stretch trong M3; không chặn nghiệm thu phase đầu |
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

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md) · revision 7 · status draft · SHA-256 `d3147cece6050dca7d0163a5562be34cbe6422a5c1719a0593225a91de1f22db`

### FR-L3GEN-013 — Phân tích và khám phá kiến trúc qua giao diện web

#### Mô tả

Người dùng truy cập giao diện web để gửi repository, theo dõi lần phân tích hiện tại, xem tổng quan/component/dependency và truy về nguồn bằng chứng.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Khám phá kiến trúc |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M2; phase đầu không có lịch sử hoặc public job API |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

#### Acceptance Criteria

##### AC-L3GEN-013-01

- **Given:** Người dùng có repository thuộc phạm vi hỗ trợ.
- **When:** người dùng tạo yêu cầu phân tích trên giao diện.
- **Then:** chọn được đầu vào hỗ trợ, cấu hình phạm vi và chế độ AI; theo dõi trạng thái của lần chạy hiện tại; khi xong mở được kết quả đúng lần chạy.
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

#### Ranh giới phase đầu

Web phase đầu hiển thị `running`, `completed`, `partial` hoặc `failed` cho lần chạy hiện tại. Danh sách lịch sử, mở lại kết quả cũ, public job API, retention theo repository và xóa từng phiên thuộc FR-L3GEN-017 ở phase sau. Trạng thái tạm phục vụ UI không được dùng để tuyên bố FR-L3GEN-017 đã đạt.

#### Trạng thái liên kết triển khai

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-014](../../requirements/fr/FR-L3GEN-014.md) · revision 6 · status draft · SHA-256 `d5f43ea19262a8ef4ca43dbd8bccf74cc4d13a56ed1121d0028ce478cc3583ca`

### FR-L3GEN-014 — Xem cấu hình mà hệ thống sử dụng

#### Mô tả

Người dùng xem các khóa cấu hình và nơi sử dụng mà không lộ giá trị bí mật.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M3: Python; phase sau: Java |
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
- **Cách kiểm dự kiến:** Chỉ diễn giải file được chỉ định là application config và mapping tĩnh; chuẩn hóa key lồng nhau bằng dấu chấm. YAML tùy ý, anchor/merge, custom tag hoặc template không resolve được phải ghi partial/unsupported theo NFR-L3GEN-COMP-001.

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
- **Cách kiểm dự kiến:** Dùng `@Value` và application properties/YAML dạng key tĩnh theo ma trận Java roadmap ở NFR-L3GEN-COMP-001; cơ chế ngoài phạm vi phải hiện ở phần giới hạn. AC này thuộc phase sau.

#### Trạng thái liên kết triển khai

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-015](../../requirements/fr/FR-L3GEN-015.md) · revision 7 · status draft · SHA-256 `9001d2c7ffa714dc31724aecfbbb6541b1e4267df5729866488b3288d438a78d`

### FR-L3GEN-015 — Xem quan hệ phát và nhận sự kiện

#### Mô tả

Người dùng xem producer/consumer và topic của Kafka; biết phần thiếu và quan hệ nào chỉ là ứng viên. Broker khác Kafka nằm ngoài phạm vi và phải hiện ra ở phần giới hạn.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M3: Kafka Python; phase sau: Spring Kafka |
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

##### AC-L3GEN-015-05

- **Given:** Repository Java dùng KafkaTemplate.send hoặc @KafkaListener với topic literal trong ma trận NFR-L3GEN-COMP-001 được duyệt.
- **When:** người dùng phân tích repository.
- **Then:** kết quả có producer/consumer, topic, component và bằng chứng file/dòng tương ứng; topic chưa resolve ghi partial/unknown, không suy hai service giao tiếp chỉ vì trùng tên topic.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Fixture Java có `KafkaTemplate.send`, `@KafkaListener`, topic động và topic trùng tên nhưng broker khác; đối chiếu đáp án độc lập theo NFR-L3GEN-COMP-001. AC này thuộc phase sau.

#### Trạng thái liên kết triển khai

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-016](../../requirements/fr/FR-L3GEN-016.md) · revision 6 · status draft · SHA-256 `1e3192d651285df33a163431ae9c9fcbc861d87035d978b677de3f452e48d106`

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

#### Ranh giới phase đầu

ZIP và GitHub public được xử lý trong lần chạy web hiện tại. Phase đầu không cam kết public job API, danh sách lịch sử hoặc mở lại kết quả cũ; các năng lực đó thuộc FR-L3GEN-017 ở phase sau. Lỗi lấy source vẫn phải hiển thị trong lần chạy hiện tại và không được dùng snapshot cũ thay thế.

#### Trạng thái liên kết triển khai

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-017](../../requirements/fr/FR-L3GEN-017.md) · revision 8 · status draft · SHA-256 `f4d88ac3525f3255aa6741e62c262da95052befc1626b22fb87160f992296003`

### FR-L3GEN-017 — Theo dõi phiên phân tích và lấy kết quả qua API

#### Mô tả

Mỗi yêu cầu có định danh, trạng thái và kết quả riêng để giao diện hoặc hệ thống tích hợp theo dõi.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tiếp nhận và quản lý phân tích |
| Ưu tiên đề xuất | Should Have — không chặn nghiệm thu phase đầu |
| Mốc đề xuất | Phase sau, chưa cam kết ngày |
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
- **Then:** xem được trạng thái, định danh source snapshot (digest/commit, không phải bản sao source), thời điểm và tải JSON/Markdown/Mermaid; kết quả partial luôn có giới hạn.
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
- **Then:** hệ thống giữ số lần phân tích gần nhất theo ngưỡng ở NFR-L3GEN-PRIV-001 và loại lần cũ nhất khi vượt; UI thông báo chính sách và sự kiện loại phiên khi xảy ra; mục đã xóa không còn link trong danh sách, URL cũ trả trạng thái không khả dụng; không giữ metadata phiên đã xóa chỉ để thông báo.
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
- **Cách kiểm dự kiến:** Kiểm cả xóa thủ công lẫn hết hạn tự động. Khi dịch vụ đang chạy, xác nhận dữ liệu đã dọn thật; khi máy tắt qua hạn, xác nhận lần khởi động kế tiếp cleanup trước khi phục vụ bất kỳ dữ liệu nào.

#### Ranh giới phase

Toàn bộ FR này thuộc phase sau. Trạng thái tạm của lần chạy web hiện tại ở FR-L3GEN-013/016 chỉ phục vụ UI phase đầu; không bao gồm public job API, lịch sử nhiều lần chạy, mở lại kết quả cũ, retention theo repository hoặc xóa từng phiên, và không được tính là FR này đã đạt.

#### Trạng thái liên kết triển khai

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-018](../../requirements/fr/FR-L3GEN-018.md) · revision 4 · status draft · SHA-256 `01b1799534a85395581cb717571dd22d30ac58f64f6db2201153c4b840e69dda`

### FR-L3GEN-018 — Xem thư viện bên ngoài mà hệ thống phụ thuộc

#### Mô tả

Người dùng xem các thư viện bên ngoài mà đơn vị phân tích khai báo hoặc sử dụng, kèm nơi khai báo làm bằng chứng. Danh sách này nói repository dựa trên nền công nghệ nào; nó không phải quan hệ phụ thuộc giữa các component, vốn thuộc FR-L3GEN-011.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Phân tích repository |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1: manifest Python; phase sau: Maven/Java |
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

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

#### Phạm vi định dạng hỗ trợ

Định dạng phase đầu là `requirements.txt` và `[project].dependencies` trong `pyproject.toml`. Maven `pom.xml` dependency trực tiếp thuộc Java roadmap phase sau; Gradle, dependency bắc cầu và resolution động nằm ngoài phạm vi ban đầu theo NFR-L3GEN-COMP-001.

## 4. Thay đổi hành vi hiện có

Không có baseline sản phẩm đã approved để so diff. PRD không lấy hành vi code hiện tại làm chuẩn.

## 5. NGOÀI phạm vi lần này

**Phạm vi phân tích**

- Trong phase đầu: adapter Java/Spring Boot và các AC chỉ dành cho Java. Các AC này vẫn nằm trong roadmap, không được báo pass ở nghiệm thu ngày 09/10.
- Trong phase đầu: public job API, lịch sử nhiều lần chạy, mở lại kết quả cũ, retention theo repository và xóa từng phiên của FR-L3GEN-017.
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

Nguồn: [NFR-L3GEN-ABST-001](../../requirements/nfr/NFR-L3GEN-ABST-001.md) · revision 4 · status draft · SHA-256 `7b5f9bc140d64ea7c9c8ffec9984d0d1143a31d74a6245d23e99472b03b77502`

### NFR-L3GEN-ABST-001 — Mức trừu tượng của kết quả trình bày

- **Nhóm:** Abstraction level.
- **Trạng thái:** ngưỡng đã chốt tại OQ-L3GEN-004; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-006](../../requirements/fr/FR-L3GEN-006.md), [FR-L3GEN-007](../../requirements/fr/FR-L3GEN-007.md), [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md), [FR-L3GEN-011](../../requirements/fr/FR-L3GEN-011.md), [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md).
- **Quyết định nền:** [ADR-2026-001](../../architecture/adr/ADR-2026-001.md).

#### Yêu cầu có thể kiểm chứng

Phân tích và trình bày là hai mức khác nhau. Engine được đọc sâu tới function, tham số, thuộc tính và phép gán để chứng minh một quan hệ; nhưng kết quả mặc định cho người đọc dừng ở application/component.

Ràng buộc đã chốt:

- Sơ đồ và tài liệu L3 mặc định chỉ có node mức application, component và hệ thống ngoài. Node mức function, class hoặc file không xuất hiện ở lớp mặc định.
- Số node trong một sơ đồ mặc định không tỷ lệ với số function của repository. Ngưỡng đề xuất: repository có ≥500 function vẫn cho sơ đồ mặc định ≤50 node; vượt ngưỡng phải rút gọn có thông báo theo AC-L3GEN-008-03, không xuất sơ đồ đầy đủ rồi để người đọc tự lọc.
- Dữ kiện mức function/class vẫn được giữ trong bộ kết quả, nhưng nằm ở lớp evidence hoặc chẩn đoán có nhãn riêng, không trộn vào lớp kiến trúc mặc định.
- Một quan hệ kiến trúc chỉ tồn tại khi đích đã resolve. Lời gọi chưa resolve được giữ như dữ kiện có nhãn unknown, không được nâng thành cạnh giữa hai component.

Ngưỡng 500/50 đã được chốt tại OQ-L3GEN-004 để có thể kiểm chứng; chưa đo trên tập fixture đã pin.

#### Điều kiện và cách kiểm

Chạy trên fixture đã pin, đếm node theo lớp trong bộ kết quả máy đọc được của FR-L3GEN-008, không đếm bằng mắt trên hình. Kiểm cả repository nhỏ và repository ≥500 function. Kiểm rằng bỏ lớp evidence đi thì lớp kiến trúc vẫn đọc được, và mọi cạnh kiến trúc đều có đích đã resolve. Không coi việc sơ đồ vẽ được là bằng chứng mức trừu tượng đúng.

#### Người chốt và ngoại lệ

Khiêm chốt ở Scope Gate; Hoàng review nội bộ/UAT theo quyết định đã đóng tại OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [ADR-2026-001](../../architecture/adr/ADR-2026-001.md).
- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

---

Nguồn: [NFR-L3GEN-ACC-001](../../requirements/nfr/NFR-L3GEN-ACC-001.md) · revision 5 · status draft · SHA-256 `691ff299d6171ad65ab52aa1af7d58b123d26bd673fd85ddd490e0fc709f05c1`

### NFR-L3GEN-ACC-001 — Độ đúng của dữ kiện và component

- **Nhóm:** Accuracy.
- **Trạng thái:** ngưỡng đã chốt tại OQ-L3GEN-004; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-003](../../requirements/fr/FR-L3GEN-003.md), [FR-L3GEN-004](../../requirements/fr/FR-L3GEN-004.md), [FR-L3GEN-005](../../requirements/fr/FR-L3GEN-005.md), [FR-L3GEN-006](../../requirements/fr/FR-L3GEN-006.md), [FR-L3GEN-011](../../requirements/fr/FR-L3GEN-011.md), [FR-L3GEN-014](../../requirements/fr/FR-L3GEN-014.md), [FR-L3GEN-015](../../requirements/fr/FR-L3GEN-015.md).

#### Yêu cầu có thể kiểm chứng

Ngưỡng trước nghiệm thu: precision nhóm exact ≥90% cho từng loại route, entity, HTTP, config, event và internal call edge; recall lần lượt route ≥85%, entity ≥90%, HTTP ≥80%, config ≥80%, event ≥80%, internal call edge trong pattern công bố ≥70%. Đánh giá đúng thuộc tính riêng: không tính một URL thiếu prefix là URL đầy đủ đúng; không tính tên bảng suy sai là tên bảng đúng. Fixture thuộc pattern cam kết phải thỏa tất cả AC. Component grouping so với mapping người duyệt: precision và recall của membership đều ≥85%; dependency exact ≥90% precision. Không dùng tên role inferred như ground truth nghiệp vụ.

#### Điều kiện và cách kiểm

OBS-L3GEN-001 quy định đáp án độc lập, sampling, matching và cỡ mẫu. Mỗi nhóm không đủ mẫu báo counts và `not_evaluated` thay vì 100%; ngoài pattern công bố báo độ phủ riêng, không loại ca khó sau khi xem output. Chưa có kết quả nghiệm thu.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).


#### Thư viện bên ngoài

Đối với FR-L3GEN-018, tên, ràng buộc phiên bản, nhãn declared/usage và bằng chứng phải đạt AC trên fixture đã chốt theo OBS-L3GEN-001. Báo số đúng/sai theo thuộc tính; chưa có ngưỡng phần trăm thống kê cho thư viện, không dùng ngưỡng route thay thế. Ma trận hỗ trợ đã chốt tại OQ-003; fixture và đáp án đo tiếp tục xử lý ở OQ-004.

---

Nguồn: [NFR-L3GEN-AI-001](../../requirements/nfr/NFR-L3GEN-AI-001.md) · revision 4 · status draft · SHA-256 `f2168caf5e4e26d135bc55a2e7e918894b0917b3cc2d1ace7a530c31a57a1c08`

### NFR-L3GEN-AI-001 — Giới hạn và ranh giới AI

- **Nhóm:** AI reliability.
- **Trạng thái:** ngưỡng chất lượng, provider và giới hạn chi phí đã chốt tại OQ-L3GEN-004/005; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-010](../../requirements/fr/FR-L3GEN-010.md), [FR-L3GEN-012](../../requirements/fr/FR-L3GEN-012.md).

#### Yêu cầu có thể kiểm chứng

AI không được sửa IAM/architecture model, tạo entity/edge hoặc category finding mới. Chỉ nhận output đúng schema và ID đã có. Mỗi request timeout tối đa 30 giây, retry tối đa 2 lần; mỗi phiên tối đa 20 request. Phase đầu có trần chi phí trả phí bằng 0 đồng, chỉ dùng quota miễn phí; chưa cấu hình được cap tương ứng thì không gọi AI. Hết quota, rate limit, thiếu key/SDK hoặc đạt cap thì tiếp tục trả dữ kiện tĩnh và cảnh báo. Provider là tham số cấu hình, không khóa cứng vào một hãng, nhưng chỉ adapter được công bố là hỗ trợ mới được sử dụng; khóa API do người dùng cung cấp tại thời điểm chạy và không được ghi vào output, log, evidence hay bộ kết quả lưu lại. Công cụ không phát biểu thay người dùng về mức an toàn dữ liệu của provider họ chọn; điều khoản của provider thuộc trách nhiệm người dùng.

#### Điều kiện và cách kiểm

Mock provider trả JSON hỏng, ID lạ, chèn route, timeout, 429 và trả mô tả khác; so sánh model trước/sau. Kiểm request count và logging. Đặt khóa API dạng canary rồi kiểm toàn bộ output, log và evidence không chứa giá trị đó; kiểm đổi provider bằng cấu hình mà không sửa code. Ngân sách thật/provider chờ OQ, không dùng giá hay model giả.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

---

Nguồn: [NFR-L3GEN-COMP-001](../../requirements/nfr/NFR-L3GEN-COMP-001.md) · revision 9 · status draft · SHA-256 `3b142d6bd1231cf3283df3dc6a3a3291199dd79900b56dfba5ec76c658b60ec5`

### NFR-L3GEN-COMP-001 — Stack và môi trường được hỗ trợ

- **Nhóm:** Compatibility.
- **Trạng thái:** phạm vi pattern đã chốt tại OQ-L3GEN-003; chưa có kết quả kiểm capability hoặc nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md), [FR-L3GEN-002](../../requirements/fr/FR-L3GEN-002.md), [FR-L3GEN-003](../../requirements/fr/FR-L3GEN-003.md), [FR-L3GEN-004](../../requirements/fr/FR-L3GEN-004.md), [FR-L3GEN-005](../../requirements/fr/FR-L3GEN-005.md), [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md), [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md), [FR-L3GEN-014](../../requirements/fr/FR-L3GEN-014.md), [FR-L3GEN-015](../../requirements/fr/FR-L3GEN-015.md).

#### Yêu cầu có thể kiểm chứng

Ma trận pattern là hợp đồng phạm vi của analyzer: mỗi hàng nêu cú pháp/API/dạng file được cam kết nhận diện, phần chỉ nhận diện có giới hạn và phần không hỗ trợ. `supported` vẫn phải qua fixture và ngưỡng NFR trước khi được báo đạt; ma trận không phải bằng chứng implementation.

OQ-L3GEN-002 chốt Python/FastAPI là stack nghiệm thu phase đầu. Java/Spring Boot nằm trong roadmap phase sau và không được báo đạt ngày 09/10.

| Phase / nhóm | Supported | Partial | Unsupported hoặc để phase sau |
|---|---|---|---|
| Python runtime | Cú pháp Python 3.10–3.12 | Cấu trúc động giữ source/evidence nếu đọc được | Cú pháp ngoài dải đã công bố |
| FastAPI route | `@app`/`@router.get/post/put/patch/delete`; `include_router` và `app.mount` khi target/prefix resolve tĩnh | Factory hoặc prefix biểu thức nhưng còn giữ được evidence | `add_api_route`, registration/reflection không resolve tĩnh |
| Python data | SQLAlchemy declarative `Base`/`declarative_base`, `Column`, `ForeignKey`, `relationship` trực tiếp | Tên bảng/quan hệ biểu thức được giữ unknown kèm evidence | SQLModel, `mapped_column`, XML hoặc ORM khác trong phase đầu |
| HTTP outbound | `requests` và `httpx` | URL ghép được một phần giữ biểu thức và nhãn partial | SDK/client khác chưa có adapter |
| Config Python | `os.getenv`, `os.environ[...]`, Pydantic `BaseSettings`; `.env.example` chỉ lấy tên khóa | Key động giữ biểu thức; không đọc giá trị môi trường thật | Đọc `.env` thật hoặc suy giá trị secret |
| YAML application config | File được người dùng/cấu hình chỉ định là application config; mapping tĩnh; key lồng nhau chuẩn hóa bằng dấu chấm | Sequence hoặc template còn giữ được đường dẫn/evidence | Tự diễn giải YAML tùy ý; anchor/merge, custom tag hoặc template động không resolve |
| Kafka Python | `confluent_kafka` producer/consumer với topic literal | Topic động giữ biểu thức và nhãn partial | Broker khác Kafka hoặc Kafka SDK khác chưa có adapter |
| Manifest Python | `requirements.txt`; `[project].dependencies` trong `pyproject.toml`; giữ nguyên constraint khai báo | Import-to-package mapping không chắc chắn ghi unknown | Dependency bắc cầu hoặc resolution động |
| Java roadmap | Java 17, Spring Boot 3.x; annotation route trực tiếp; Jakarta Persistence; `@Value`; Spring Kafka; Maven `pom.xml` dependency trực tiếp | Giá trị annotation/property biểu thức nhưng còn evidence | Reflection, custom annotation, registration động, Gradle, Maven profile/property động và ORM/broker khác |

Hai stack dùng chung contract kết quả nhưng không dùng chung rule. Pattern ngoài ma trận phải hiện trong phần giới hạn, không được im lặng bỏ qua. Event chỉ hỗ trợ Kafka; broker khác nằm ngoài phạm vi.

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

Nguồn: [NFR-L3GEN-DET-001](../../requirements/nfr/NFR-L3GEN-DET-001.md) · revision 3 · status draft · SHA-256 `43e99d3355f0e541b0938be7b24f00a00d23474ab37bf814c30f705f8b65c824`

### NFR-L3GEN-DET-001 — Tái lập dữ kiện và định danh

- **Nhóm:** Determinism.
- **Trạng thái:** ngưỡng và phương pháp đã chốt tại OQ-L3GEN-004; chưa đo nghiệm thu.
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

Nguồn: [NFR-L3GEN-PERF-001](../../requirements/nfr/NFR-L3GEN-PERF-001.md) · revision 3 · status draft · SHA-256 `d5d5b43cf0b7e519d69778feb1c4bc46a2cf5427899deeabd1dd05a3158e9766`

### NFR-L3GEN-PERF-001 — Thời gian xử lý và giới hạn tài nguyên

- **Nhóm:** Performance.
- **Trạng thái:** ngưỡng và cấu hình benchmark đã chốt tại OQ-L3GEN-004; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md), [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md), [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md), [FR-L3GEN-016](../../requirements/fr/FR-L3GEN-016.md), [FR-L3GEN-017](../../requirements/fr/FR-L3GEN-017.md).

#### Yêu cầu có thể kiểm chứng

Môi trường benchmark chuẩn: 4 CPU logical, RAM 8 GiB, SSD, Python 3.12, no-AI, dependencies đã cài. Nếu máy thực tế khác thì công bố đầy đủ và không ngoại suy. Thời gian analyzer+ghi output (không gồm clone/AI/cài đặt) tối đa 60 giây cho 5.000 dòng Python, và 300 giây cho 50.000 dòng trong tập fixture/repo đã pin. Trần thời gian cho một lần phân tích là 10 phút; quá hạn thì dừng và báo lý do, không trả kết quả như đã hoàn tất.

Giới hạn tiếp nhận: ZIP nén 100 MB, giải nén 500 MB và 50.000 file; vượt ngưỡng phải từ chối hoặc dừng có lý do. Worker tối đa 2 GiB RAM/phiên, 2 phiên chạy cùng lúc; phiên sau xếp hàng. Git fetch timeout 120 giây; mọi giới hạn có trong thông báo/help.

#### Điều kiện và cách kiểm

Đo 5 lần cho mỗi repo trên máy công bố, ghi từng lần và worst-case, peak RSS. Không ngoại suy từ máy khác hoặc repo nhỏ. Kiểm input sát/vượt giới hạn, ZIP bomb và job bị timeout; không báo hoàn tất khi bị dừng. OBS-L3GEN-001 mô tả cách thu số, không lặp ngưỡng.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

---

Nguồn: [NFR-L3GEN-PRIV-001](../../requirements/nfr/NFR-L3GEN-PRIV-001.md) · revision 6 · status draft · SHA-256 `c5143681e84da63baeefb7956c22024b5b772a4e37fa77e386083ec71ae0156f`

### NFR-L3GEN-PRIV-001 — Quyền riêng tư và vòng đời dữ liệu

- **Nhóm:** Privacy.
- **Trạng thái:** ngưỡng chất lượng và vòng đời dữ liệu đã chốt tại OQ-L3GEN-004/005; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-005](../../requirements/fr/FR-L3GEN-005.md), [FR-L3GEN-007](../../requirements/fr/FR-L3GEN-007.md), [FR-L3GEN-010](../../requirements/fr/FR-L3GEN-010.md), [FR-L3GEN-012](../../requirements/fr/FR-L3GEN-012.md), [FR-L3GEN-014](../../requirements/fr/FR-L3GEN-014.md), [FR-L3GEN-016](../../requirements/fr/FR-L3GEN-016.md), [FR-L3GEN-017](../../requirements/fr/FR-L3GEN-017.md).

#### Yêu cầu có thể kiểm chứng

AI mặc định tắt; phải chủ động bật và biết provider, loại dữ liệu gửi. --no-ai không có outbound ở analyzer; CLI local no-AI không cần mạng; Git URL vẫn cần mạng để lấy repo đã được yêu cầu. Không đọc .env thật, private key hoặc gửi credentials. AI chỉ nhận model tối thiểu đã lọc giá trị nhạy cảm; source snippet cần đồng ý riêng và không thuộc bản đầu. Source tạm của web hết hạn trong 24 giờ sau trạng thái cuối và không được phục vụ sau hạn; output và metadata giữ tối đa 14 ngày. Khi dịch vụ đang chạy, dữ liệu hết hạn phải được dọn đúng hạn; nếu máy tắt qua hạn, lần khởi động kế tiếp phải cleanup trước khi phục vụ dữ liệu. Mỗi repository giữ tối đa 10 lần phân tích gần nhất, vượt thì loại lần cũ nhất. Người dùng xóa được một kết quả trước hạn. Hành vi cụ thể ở AC-L3GEN-017-05 và AC-L3GEN-017-06. CLI output do người dùng quản lý và ghi rõ khác biệt này.

#### Điều kiện và cách kiểm

Dùng canary secrets ở .env, YAML và URL, kiểm log/output/payload không có giá trị; kiểm no-AI bằng network interception và phân biệt ingestion/analyzer. Test clock/cleanup sau hạn, hủy/lỗi và xóa sớm. Không coi bộ lọc secret là chứng minh phát hiện mọi bí mật tùy ý.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).


#### Chi tiết vòng đời đã chốt tại OQ-005

GitHub repository được nhận diện bằng host/owner/name đã chuẩn hóa, không dùng branch/commit làm identity repository. ZIP dùng digest nội dung các file được tiếp nhận: ZIP khác nội dung là repository khác; không tự gộp ZIP với GitHub. UI nói rõ giới hạn này.

Giới hạn số lần áp dụng cho phiên terminal (completed/partial/failed/cancelled), theo thời điểm kết thúc; phiên đang chạy không bị eviction. Hạn ngày tính từ thời điểm terminal, áp cho cả metadata lỗi. Eviction thực hiện ngay khi phiên chuyển terminal; quá hạn không được trả kết quả. Máy tắt không bảo đảm xóa vật lý đúng giờ: lần khởi động sau phải cleanup trước khi phục vụ dữ liệu, và UI/help công khai giới hạn này. Phase đầu không cam kết SLA xóa vật lý tuyệt đối khi máy tắt; nếu về sau cần SLA đó thì phải chuyển sang dịch vụ luôn chạy và duyệt lại NFR.

Output chỉ giữ source digest, định danh commit nếu có và file/range dòng; không giữ bản sao toàn source hoặc snippet. Sau khi source tạm bị dọn, vẫn xem được vị trí bằng chứng nhưng không hứa mở nội dung source: dùng permalink commit GitHub nếu hợp lệ, hoặc yêu cầu cung cấp lại source đúng digest. Không mở source mới như bằng chứng cũ. Xóa thủ công/eviction dọn output, metadata phiên và source tạm của phiên đó; không giữ tombstone source hay dữ liệu nhạy cảm.

---

Nguồn: [NFR-L3GEN-REL-001](../../requirements/nfr/NFR-L3GEN-REL-001.md) · revision 3 · status draft · SHA-256 `a6425d4b46ecbbd246aa99a8cbae2670da5cf6d2ae776ddf8c487b814f03017e`

### NFR-L3GEN-REL-001 — Hoàn tất, lỗi một phần và cách ly phiên

- **Nhóm:** Reliability.
- **Trạng thái:** ngưỡng và phương pháp đã chốt tại OQ-L3GEN-004; chưa đo nghiệm thu.
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

Nguồn: [NFR-L3GEN-SEC-001](../../requirements/nfr/NFR-L3GEN-SEC-001.md) · revision 4 · status draft · SHA-256 `6e7e1c99acf01d692019847fe3cfed4e62394a7865abb75cdc3d19bff8166542`

### NFR-L3GEN-SEC-001 — An toàn khi tiếp nhận và phân tích source

- **Nhóm:** Security.
- **Trạng thái:** ngưỡng chất lượng và phạm vi môi trường/an toàn đã chốt tại OQ-L3GEN-004/005; chưa đo nghiệm thu.
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

Nguồn: [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md) · revision 3 · status draft · SHA-256 `f4d0ec841234a6ca1d8d5ad96f15b7788c2cfee8d92dfec8be8ed0dd2eac0033`

### NFR-L3GEN-TRACE-001 — Nguồn bằng chứng và phiên bản

- **Nhóm:** Traceability.
- **Trạng thái:** ngưỡng và phương pháp đã chốt tại OQ-L3GEN-004; chưa đo nghiệm thu.
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

Nguồn: [NFR-L3GEN-USA-001](../../requirements/nfr/NFR-L3GEN-USA-001.md) · revision 3 · status draft · SHA-256 `68b43ecd687ead418e41dd0f2d8105d113c4341c0f6488b9372f83769d24a0ec`

### NFR-L3GEN-USA-001 — Khả năng sử dụng và tiếp cận

- **Nhóm:** Usability.
- **Trạng thái:** ngưỡng và phương pháp đã chốt tại OQ-L3GEN-004; chưa đo nghiệm thu, pilot ngoài nhóm có thể `not_evaluated` trong phase đầu.
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

Không còn câu hỏi mở.
