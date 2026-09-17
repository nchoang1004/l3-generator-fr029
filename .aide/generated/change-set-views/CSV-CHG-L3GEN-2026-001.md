---
key: CSV-CHG-L3GEN-2026-001
group: derived
non_normative: true
derived_from: [BL-CHG-L3GEN-2026-001-r7]
hand_written: false
status: candidate
---

# Full product — Code → Architecture / L3 Generator

> **LỖI THỜI — chưa render lại theo BL-r8.**
> File này được sinh từ BL-r7. Sau đó hồ sơ đã thêm NFR-L3GEN-ABST-001 và ADR-2026-001,
> và bump revision của PRD, FR-006, FR-007, FR-008, FR-011, FR-013, FR-017, NFR-COMP-001,
> NFR-PERF-001, NFR-PRIV-001, OQ-001 và OQ-003. Số liệu và bảng revision dưới đây đang lệch
> so với nguồn. Nguồn thắng. Phải chạy lại script render/check theo BL-r8 trước khi dùng
> file này để review.


Bản ứng viên chưa duyệt. Khi view và nguồn bất đồng, **FR/NFR/PRD nguồn thắng**; sửa nguồn rồi chạy script render. Không dùng view này như approval.

Đọc mục 3 để review FR/AC, mục 6 để review NFR, mục 7 để chốt câu hỏi mở. Chỉ mở file nguồn khi cần góp ý riêng; không cần đọc lại cùng nội dung ở mọi file.

<details>
<summary>Tập revision đề xuất để đối chiếu (chưa duyệt)</summary>

| Tài liệu nguồn | Revision | Trạng thái |
|---|---|---|
| [PRD-L3GEN-2609-001](../../product/prd/PRD-L3GEN-2609-001.md) | 7 | draft |
| [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md) | 2 | draft |
| [FR-L3GEN-002](../../requirements/fr/FR-L3GEN-002.md) | 2 | draft |
| [FR-L3GEN-003](../../requirements/fr/FR-L3GEN-003.md) | 4 | draft |
| [FR-L3GEN-004](../../requirements/fr/FR-L3GEN-004.md) | 3 | draft |
| [FR-L3GEN-005](../../requirements/fr/FR-L3GEN-005.md) | 2 | draft |
| [FR-L3GEN-006](../../requirements/fr/FR-L3GEN-006.md) | 2 | draft |
| [FR-L3GEN-007](../../requirements/fr/FR-L3GEN-007.md) | 2 | draft |
| [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md) | 4 | draft |
| [FR-L3GEN-009](../../requirements/fr/FR-L3GEN-009.md) | 3 | draft |
| [FR-L3GEN-010](../../requirements/fr/FR-L3GEN-010.md) | 3 | draft |
| [FR-L3GEN-011](../../requirements/fr/FR-L3GEN-011.md) | 4 | draft |
| [FR-L3GEN-012](../../requirements/fr/FR-L3GEN-012.md) | 3 | draft |
| [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md) | 2 | draft |
| [FR-L3GEN-014](../../requirements/fr/FR-L3GEN-014.md) | 2 | draft |
| [FR-L3GEN-015](../../requirements/fr/FR-L3GEN-015.md) | 2 | draft |
| [FR-L3GEN-016](../../requirements/fr/FR-L3GEN-016.md) | 2 | draft |
| [FR-L3GEN-017](../../requirements/fr/FR-L3GEN-017.md) | 2 | draft |
| [NFR-L3GEN-ACC-001](../../requirements/nfr/NFR-L3GEN-ACC-001.md) | 1 | draft |
| [NFR-L3GEN-AI-001](../../requirements/nfr/NFR-L3GEN-AI-001.md) | 1 | draft |
| [NFR-L3GEN-COMP-001](../../requirements/nfr/NFR-L3GEN-COMP-001.md) | 3 | draft |
| [NFR-L3GEN-DET-001](../../requirements/nfr/NFR-L3GEN-DET-001.md) | 1 | draft |
| [NFR-L3GEN-PERF-001](../../requirements/nfr/NFR-L3GEN-PERF-001.md) | 1 | draft |
| [NFR-L3GEN-PRIV-001](../../requirements/nfr/NFR-L3GEN-PRIV-001.md) | 1 | draft |
| [NFR-L3GEN-REL-001](../../requirements/nfr/NFR-L3GEN-REL-001.md) | 1 | draft |
| [NFR-L3GEN-SEC-001](../../requirements/nfr/NFR-L3GEN-SEC-001.md) | 1 | draft |
| [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md) | 1 | draft |
| [NFR-L3GEN-USA-001](../../requirements/nfr/NFR-L3GEN-USA-001.md) | 2 | draft |
| [OBS-L3GEN-001](../../observability/OBS-L3GEN-001.md) | 1 | draft |
| [OBS-L3GEN-002](../../observability/OBS-L3GEN-002.md) | 1 | draft |
| [GLOSS-L3GEN-001](../../domain/glossary-core.md) | 1 | draft |
| [OQ-L3GEN-001](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-001.md) | 1 | open |
| [OQ-L3GEN-002](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-002.md) | 3 | open |
| [OQ-L3GEN-003](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-003.md) | 1 | open |
| [OQ-L3GEN-004](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-004.md) | 1 | open |
| [OQ-L3GEN-005](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-005.md) | 1 | open |
| [OQ-L3GEN-006](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-006.md) | 4 | open |

</details>

## 1. Mục tiêu

Tạo tài liệu và sơ đồ kiến trúc ban đầu từ source, để developer và architect hiểu hệ thống và kiểm chứng từng kết luận tại mã nguồn.

**Phạm vi tài liệu:** toàn bộ sản phẩm mục tiêu theo đề bài và các đề xuất nêu dưới đây. Code hiện có không quyết định phạm vi hoặc là bằng chứng đã đạt yêu cầu. M1–M3 là mốc nội bộ đề xuất của cùng sản phẩm. Bản này dùng để lấy ý kiến; còn quyết định cần mentor chốt tại mục IX. Chưa approved, chưa có kết quả nghiệm thu.

PRD đầy đủ: [PRD-L3GEN-2609-001](../../product/prd/PRD-L3GEN-2609-001.md).

## 2. Mục tiêu nghiệp vụ đổi

New System: đề xuất GOAL/KPI ban đầu, chưa có baseline nghiệp vụ trước đó.

| Goal key | Mục tiêu | Liên kết OKR/KPI |
|---|---|---|
| GOAL-L3GEN-001 | Giúp người dùng tự trả lời câu hỏi về cấu trúc service từ bộ tài liệu sinh ra | KPI-L3GEN-002; OKR tổ chức chưa được cung cấp |
| GOAL-L3GEN-002 | Cung cấp kết luận có bằng chứng, chỉ rõ phần chưa biết để dùng trong review | KPI-L3GEN-001 |
| GOAL-L3GEN-003 | Cung cấp mô hình và sơ đồ dùng lại được bởi công cụ khác | KPI-L3GEN-003 |

### Chỉ số thành công

| KPI key | KPI | Giải thích | Baseline | Target đề xuất | Timeline | measured_by |
|---|---|---|---|---|---|---|
| KPI-L3GEN-001 | Chất lượng dữ kiện và bằng chứng | Theo loại thực thể/cạnh và phạm vi hỗ trợ; ngưỡng chuẩn nằm ở NFR | Chưa đo nghiệm thu | Đạt NFR-L3GEN-ACC-001 và NFR-L3GEN-TRACE-001 với mẫu đủ | Trước nghiệm thu M3 | [OBS-L3GEN-001](../../observability/OBS-L3GEN-001.md) |
| KPI-L3GEN-002 | Tự hoàn thành nhiệm vụ tìm hiểu kiến trúc | Người dùng mới làm đúng bộ câu hỏi và tìm được evidence không cần tác giả hướng dẫn | Chưa đo | ≥80% người tham gia đủ điều kiện | Pilot trước nghiệm thu M3 | [OBS-L3GEN-002](../../observability/OBS-L3GEN-002.md) |
| KPI-L3GEN-003 | Đầu ra dùng lại được | Bộ đọc độc lập dùng được JSON và renderer dùng được diagram | Chưa đo | Tất cả tình huống export thuộc FR-L3GEN-008/011 đạt AC | Kiểm tra bước đầu tại M2; kết luận đạt tại M3 | [OBS-L3GEN-001](../../observability/OBS-L3GEN-001.md) |

Không báo tỷ lệ tổng hợp hoặc tuyên bố đạt nếu chưa đủ cỡ mẫu tối thiểu tại OBS. Tỷ lệ trước pilot là target dự thảo, không phải kết quả sản phẩm.

## 3. Tính năng mới

Toàn bộ FR trong candidate baseline; Must/Should và mốc nằm tại từng nguồn.

---

Nguồn: [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md) · revision 2 · status draft · SHA-256 `ace9fe9f9947c876454e131c0c94c174c5c326a952411ffeb1074c6649cbf072`

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
- **Then:** công cụ báo lỗi nếu không ghi được; nếu trùng kết quả thì yêu cầu chọn thư mục mới, không âm thầm ghi đè.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Dùng output có sentinel; xác nhận sentinel nguyên vẹn.

##### AC-L3GEN-001-04

- **Given:** Repository có thư mục loại trừ do người dùng chỉ định.
- **When:** người dùng chạy phân tích.
- **Then:** các thư mục bị loại không đi vào dữ liệu kiến trúc; cấu hình loại trừ được ghi trong thông tin lần chạy.
- `constrained_by:` [NFR-L3GEN-SEC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Dùng mã sentinel trong tests, integration-tests, venv và một thư mục tùy chọn.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

#### Tài liệu liên quan

- [NFR-L3GEN-SEC-001](../../requirements/nfr/NFR-L3GEN-SEC-001.md)
- [NFR-L3GEN-REL-001](../../requirements/nfr/NFR-L3GEN-REL-001.md)
- [NFR-L3GEN-USA-001](../../requirements/nfr/NFR-L3GEN-USA-001.md)
- [NFR-L3GEN-COMP-001](../../requirements/nfr/NFR-L3GEN-COMP-001.md)
- [NFR-L3GEN-PERF-001](../../requirements/nfr/NFR-L3GEN-PERF-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


---

Nguồn: [FR-L3GEN-002](../../requirements/fr/FR-L3GEN-002.md) · revision 2 · status draft · SHA-256 `f4b2cadf57000909eba03bebc8df254d32e557169afc203833b5a7093768186f`

### FR-L3GEN-002 — Nhận diện đơn vị phân tích và phạm vi hỗ trợ

#### Mô tả

Người dùng xem được những phần repository được phân tích, bị bỏ qua hoặc chưa xác định được stack.

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

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

#### Tài liệu liên quan

- [NFR-L3GEN-REL-001](../../requirements/nfr/NFR-L3GEN-REL-001.md)
- [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-COMP-001](../../requirements/nfr/NFR-L3GEN-COMP-001.md)
- [NFR-L3GEN-SEC-001](../../requirements/nfr/NFR-L3GEN-SEC-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


---

Nguồn: [FR-L3GEN-003](../../requirements/fr/FR-L3GEN-003.md) · revision 4 · status draft · SHA-256 `d66f69335a719721baa2e39781b8fce0252b57f19b573d3b688d8547666d41a5`

### FR-L3GEN-003 — Liệt kê API routes và handler

#### Mô tả

Người dùng xem method, path, handler, điều kiện đăng ký và nguồn khai báo của route FastAPI trong phạm vi đã công bố.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
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

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

#### Tài liệu liên quan

- [NFR-L3GEN-ACC-001](../../requirements/nfr/NFR-L3GEN-ACC-001.md)
- [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-COMP-001](../../requirements/nfr/NFR-L3GEN-COMP-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


---

Nguồn: [FR-L3GEN-004](../../requirements/fr/FR-L3GEN-004.md) · revision 3 · status draft · SHA-256 `b4d0c9a86b79e6bd886671dc03653d6ea1322071e7e75180bc5125cd853df1e9`

### FR-L3GEN-004 — Liệt kê mô hình dữ liệu

#### Mô tả

Người dùng xem lớp SQLAlchemy, tên bảng nếu xác định được, cột và khóa ngoại; nhận diện entity không đồng nghĩa biết tên bảng.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
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

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

#### Tài liệu liên quan

- [NFR-L3GEN-ACC-001](../../requirements/nfr/NFR-L3GEN-ACC-001.md)
- [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-COMP-001](../../requirements/nfr/NFR-L3GEN-COMP-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


---

Nguồn: [FR-L3GEN-005](../../requirements/fr/FR-L3GEN-005.md) · revision 2 · status draft · SHA-256 `08a333b6f325965eb55d60484c83051dc34f66a049bad7ec83da68301a1565c6`

### FR-L3GEN-005 — Liệt kê lời gọi HTTP và đích bên ngoài

#### Mô tả

Người dùng xác định nơi gọi HTTP qua requests/httpx và mức độ biết đích đến; không đồng nhất mọi HTTP call với một hệ thống bên ngoài đã xác nhận.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
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

#### Tài liệu liên quan

- [NFR-L3GEN-ACC-001](../../requirements/nfr/NFR-L3GEN-ACC-001.md)
- [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-COMP-001](../../requirements/nfr/NFR-L3GEN-COMP-001.md)
- [NFR-L3GEN-PRIV-001](../../requirements/nfr/NFR-L3GEN-PRIV-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


---

Nguồn: [FR-L3GEN-006](../../requirements/fr/FR-L3GEN-006.md) · revision 2 · status draft · SHA-256 `6a713c5caec0060194e6975f42341df9a98c2e8460da10380af985fe6484aaf3`

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

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

#### Tài liệu liên quan

- [NFR-L3GEN-ACC-001](../../requirements/nfr/NFR-L3GEN-ACC-001.md)
- [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-DET-001](../../requirements/nfr/NFR-L3GEN-DET-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


---

Nguồn: [FR-L3GEN-007](../../requirements/fr/FR-L3GEN-007.md) · revision 2 · status draft · SHA-256 `d629e5db06f6dc66a1bc5dde1d93f6619b20920f95d717ab7f67fde1471a8edc`

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

#### Tài liệu liên quan

- [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-DET-001](../../requirements/nfr/NFR-L3GEN-DET-001.md)
- [NFR-L3GEN-PRIV-001](../../requirements/nfr/NFR-L3GEN-PRIV-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


---

Nguồn: [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md) · revision 4 · status draft · SHA-256 `d6a03945ac9f37b299652fa5eeb7936709b112a0ec10d11c9c9a01204af31581`

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

#### Tài liệu liên quan

- [NFR-L3GEN-DET-001](../../requirements/nfr/NFR-L3GEN-DET-001.md)
- [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-REL-001](../../requirements/nfr/NFR-L3GEN-REL-001.md)
- [NFR-L3GEN-USA-001](../../requirements/nfr/NFR-L3GEN-USA-001.md)
- [NFR-L3GEN-COMP-001](../../requirements/nfr/NFR-L3GEN-COMP-001.md)
- [NFR-L3GEN-PERF-001](../../requirements/nfr/NFR-L3GEN-PERF-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


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

#### Tài liệu liên quan

- [NFR-L3GEN-REL-001](../../requirements/nfr/NFR-L3GEN-REL-001.md)
- [NFR-L3GEN-USA-001](../../requirements/nfr/NFR-L3GEN-USA-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


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

#### Tài liệu liên quan

- [NFR-L3GEN-SEC-001](../../requirements/nfr/NFR-L3GEN-SEC-001.md)
- [NFR-L3GEN-PRIV-001](../../requirements/nfr/NFR-L3GEN-PRIV-001.md)
- [NFR-L3GEN-DET-001](../../requirements/nfr/NFR-L3GEN-DET-001.md)
- [NFR-L3GEN-AI-001](../../requirements/nfr/NFR-L3GEN-AI-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


---

Nguồn: [FR-L3GEN-011](../../requirements/fr/FR-L3GEN-011.md) · revision 4 · status draft · SHA-256 `b21c4ef25b4690c2513a6807ce253a830486bbdd1e880f4031133bad47f93b6e`

### FR-L3GEN-011 — Xem component và tài liệu L3 của service

#### Mô tả

Người dùng xem các component bên trong service và quan hệ có chứng cứ giữa chúng; có thể đi từ sơ đồ tổng quan tới module/class/function và nguồn.

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
- **Then:** các cạnh code được gộp thành dependency giữa component với danh sách nguồn; có thể đi từ component tới code và source.
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

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

#### Tài liệu liên quan

- [NFR-L3GEN-ACC-001](../../requirements/nfr/NFR-L3GEN-ACC-001.md)
- [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-DET-001](../../requirements/nfr/NFR-L3GEN-DET-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


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

#### Tài liệu liên quan

- [NFR-L3GEN-PRIV-001](../../requirements/nfr/NFR-L3GEN-PRIV-001.md)
- [NFR-L3GEN-AI-001](../../requirements/nfr/NFR-L3GEN-AI-001.md)
- [NFR-L3GEN-DET-001](../../requirements/nfr/NFR-L3GEN-DET-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


---

Nguồn: [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md) · revision 2 · status draft · SHA-256 `ca1524f616bccf738d91380f58867817c6ff1483fd814265f590f0c2f4345472`

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
- **Cách kiểm dự kiến:** Giao diện không sửa IAM và vẫn cho tải file nguồn hợp lệ.

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

#### Tài liệu liên quan

- [NFR-L3GEN-USA-001](../../requirements/nfr/NFR-L3GEN-USA-001.md)
- [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-COMP-001](../../requirements/nfr/NFR-L3GEN-COMP-001.md)
- [NFR-L3GEN-PERF-001](../../requirements/nfr/NFR-L3GEN-PERF-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


---

Nguồn: [FR-L3GEN-014](../../requirements/fr/FR-L3GEN-014.md) · revision 2 · status draft · SHA-256 `dc2c794d0c91cc5bb106e38ea4dac812d8827a7c1212078766ed29783d099cd7`

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

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

#### Tài liệu liên quan

- [NFR-L3GEN-ACC-001](../../requirements/nfr/NFR-L3GEN-ACC-001.md)
- [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-PRIV-001](../../requirements/nfr/NFR-L3GEN-PRIV-001.md)
- [NFR-L3GEN-COMP-001](../../requirements/nfr/NFR-L3GEN-COMP-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


---

Nguồn: [FR-L3GEN-015](../../requirements/fr/FR-L3GEN-015.md) · revision 2 · status draft · SHA-256 `5df9530ede875811c4f4a8cdd53331d73c9e7d24304afd07c1184882ea1c6a14`

### FR-L3GEN-015 — Xem quan hệ phát và nhận sự kiện

#### Mô tả

Người dùng xem producer/consumer và topic của queue/event thuộc adapter hỗ trợ; biết phần thiếu và quan hệ nào chỉ là ứng viên.

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
- **Cách kiểm dự kiến:** Đây là adapter đề xuất ban đầu; chốt theo OQ trước thiết kế.

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

- **Given:** Repository dùng queue SDK khác adapter đã hỗ trợ.
- **When:** người dùng phân tích.
- **Then:** giới hạn chỉ ra adapter chưa hỗ trợ khi có bằng chứng nhận diện; phần route/DB còn lại vẫn được xử lý.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không tuyên bố hỗ trợ mọi event framework.

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

#### Tài liệu liên quan

- [NFR-L3GEN-ACC-001](../../requirements/nfr/NFR-L3GEN-ACC-001.md)
- [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-COMP-001](../../requirements/nfr/NFR-L3GEN-COMP-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


---

Nguồn: [FR-L3GEN-016](../../requirements/fr/FR-L3GEN-016.md) · revision 2 · status draft · SHA-256 `c4d705d329124b5e6622fd3e0c000fe715ecf312e29571c9894fd3495ad214bc`

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

#### Tài liệu liên quan

- [NFR-L3GEN-SEC-001](../../requirements/nfr/NFR-L3GEN-SEC-001.md)
- [NFR-L3GEN-PRIV-001](../../requirements/nfr/NFR-L3GEN-PRIV-001.md)
- [NFR-L3GEN-REL-001](../../requirements/nfr/NFR-L3GEN-REL-001.md)
- [NFR-L3GEN-PERF-001](../../requirements/nfr/NFR-L3GEN-PERF-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


---

Nguồn: [FR-L3GEN-017](../../requirements/fr/FR-L3GEN-017.md) · revision 2 · status draft · SHA-256 `2dc27a739c680d0803ed0d9a0c539118b2e67fffcee5290cc43cf78343f3cab6`

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

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

#### Tài liệu liên quan

- [NFR-L3GEN-REL-001](../../requirements/nfr/NFR-L3GEN-REL-001.md)
- [NFR-L3GEN-SEC-001](../../requirements/nfr/NFR-L3GEN-SEC-001.md)
- [NFR-L3GEN-PERF-001](../../requirements/nfr/NFR-L3GEN-PERF-001.md)
- [NFR-L3GEN-PRIV-001](../../requirements/nfr/NFR-L3GEN-PRIV-001.md)
- [NFR-L3GEN-USA-001](../../requirements/nfr/NFR-L3GEN-USA-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)


## 4. Thay đổi hành vi hiện có

Không có baseline sản phẩm đã approved để so diff. PRD không lấy hành vi code hiện tại làm chuẩn.

## 5. NGOÀI phạm vi lần này

- Phân tích mọi ngôn ngữ/framework, mọi kiểu SQL/ORM/queue SDK; stack đầu tiên được chốt tại OQ-L3GEN-003.
- Thực thi source để khám phá runtime, trace/sequence thực thi, dynamic import/metaprogramming tổng quát.
- Sửa code/tài liệu nguồn tự động; rà code không dùng hoặc cách xử lý lỗi HTTP; kết luận lỗ hổng bảo mật hoặc lỗi nghiệp vụ. Muốn thêm các chức năng này cần đề xuất phạm vi và AC riêng.
- Private Git credentials, Git submodules, đăng nhập/SSO và multi-tenant public hosting.
- Chỉnh model thủ công trên UI, so sánh drift giữa các snapshot, trigger CI tự động.
- SLA production cấp doanh nghiệp; bằng chứng release và vận hành sẽ được thiết kế phù hợp cách triển khai được duyệt.

Không có FR chuẩn tắc nào bị giấu khỏi candidate; FR AI là Should, phải quyết việc giao/hoãn trước nghiệm thu.

## 6. Ràng buộc mới

---

Nguồn: [NFR-L3GEN-ACC-001](../../requirements/nfr/NFR-L3GEN-ACC-001.md) · revision 1 · status draft · SHA-256 `76cb41ccaeac457ccdcb9ccc2a72d0d7972aada5b1573848649aa18ebbd6a249`

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

Nguồn: [NFR-L3GEN-AI-001](../../requirements/nfr/NFR-L3GEN-AI-001.md) · revision 1 · status draft · SHA-256 `aa29a432e9b12d71db16eeaa818b53e7304b1b1d6af07a10d6e3d724d844b3d3`

### NFR-L3GEN-AI-001 — Giới hạn và ranh giới AI

- **Nhóm:** AI reliability.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-010](../../requirements/fr/FR-L3GEN-010.md), [FR-L3GEN-012](../../requirements/fr/FR-L3GEN-012.md).

#### Yêu cầu có thể kiểm chứng

AI không được sửa IAM/architecture model, tạo entity/edge hoặc category finding mới. Chỉ nhận output đúng schema và ID đã có. Mỗi request timeout tối đa 30 giây, retry tối đa 2 lần; mỗi phiên tối đa 20 request. Chi phí/token cap phải cấu hình trước khi bật với provider được chọn; chưa có cấu hình cap thì không gọi AI. Rate limit, thiếu key/SDK hoặc cap đạt thì tiếp tục trả dữ kiện tĩnh và cảnh báo.

#### Điều kiện và cách kiểm

Mock provider trả JSON hỏng, ID lạ, chèn route, timeout, 429 và trả mô tả khác; so sánh model trước/sau. Kiểm request count và logging. Ngân sách thật/provider chờ OQ, không dùng giá hay model giả.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).


---

Nguồn: [NFR-L3GEN-COMP-001](../../requirements/nfr/NFR-L3GEN-COMP-001.md) · revision 3 · status draft · SHA-256 `0d50be81a0e7313ed701dc7705c83785a1b9a1f89e971c233d45e552763a909a`

### NFR-L3GEN-COMP-001 — Stack và môi trường được hỗ trợ

- **Nhóm:** Compatibility.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md), [FR-L3GEN-002](../../requirements/fr/FR-L3GEN-002.md), [FR-L3GEN-003](../../requirements/fr/FR-L3GEN-003.md), [FR-L3GEN-004](../../requirements/fr/FR-L3GEN-004.md), [FR-L3GEN-005](../../requirements/fr/FR-L3GEN-005.md), [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md), [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md), [FR-L3GEN-014](../../requirements/fr/FR-L3GEN-014.md), [FR-L3GEN-015](../../requirements/fr/FR-L3GEN-015.md).

#### Yêu cầu có thể kiểm chứng

Đề bài cho phép ưu tiên 1–2 stack, không chỉ định phiên bản hay thư viện cụ thể. Ma trận dưới đây là đề xuất để kiểm chứng một stack Python/FastAPI; Tech Lead/QA phải đối chiếu nhu cầu và repo mẫu tại OQ-L3GEN-003/004 trước khi chốt, không dùng khả năng của code hiện có làm căn cứ duy nhất.

Phạm vi phân tích đề xuất: cú pháp Python 3.10–3.12; FastAPI methods GET/POST/PUT/DELETE/PATCH; SQLAlchemy declarative Column; requests/httpx; Pydantic settings; confluent_kafka. SQLModel, mapped_column, method khác và SDK khác phải có capability riêng trước khi được gọi là hỗ trợ. Phiên bản runtime của chính công cụ được chọn và pin ở thiết kế.

Môi trường sử dụng đề xuất: CLI trên Windows 11 và Ubuntu 24.04, hỗ trợ tên file/path Unicode và có dấu cách; web trên Chrome và Edge. Phiên bản browser ổn định dùng để kiểm được ghi cụ thể tại thời điểm kiểm; Mermaid renderer/version pin ở contract.

#### Điều kiện và cách kiểm

Chạy cùng bộ supported fixtures trên cả hai OS; ghi interpreter, package/rule/renderer/browser versions. Lỗi cú pháp do version ngoài phạm vi phải được báo rõ. Có ma trận supported/partial/unsupported thay cho một checkbox hỗ trợ cả ngôn ngữ.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).


---

Nguồn: [NFR-L3GEN-DET-001](../../requirements/nfr/NFR-L3GEN-DET-001.md) · revision 1 · status draft · SHA-256 `42a56c37688383c7af0df79e7ab872555d7723b14d1b62e924df9723c0386b1e`

### NFR-L3GEN-DET-001 — Tái lập dữ kiện và định danh

- **Nhóm:** Determinism.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-006](../../requirements/fr/FR-L3GEN-006.md), [FR-L3GEN-007](../../requirements/fr/FR-L3GEN-007.md), [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md), [FR-L3GEN-010](../../requirements/fr/FR-L3GEN-010.md), [FR-L3GEN-011](../../requirements/fr/FR-L3GEN-011.md), [FR-L3GEN-012](../../requirements/fr/FR-L3GEN-012.md).

#### Yêu cầu có thể kiểm chứng

Cùng snapshot source, cấu hình phân tích, rule version và tool version phải cho cùng cấu trúc, cạnh, nhãn và ID trong JSON chuẩn hóa, độc lập output directory và chế độ AI. Timestamp, duration, analysis_id và đường dẫn workspace tuyệt đối thuộc run metadata, không làm đổi ID dữ kiện. L3 phần diễn giải AI không nằm trong cam kết byte-identical.

#### Điều kiện và cách kiểm

Chạy 3 lần vào các output khác nhau, trong đó bật AI stub với mô tả khác; so sánh canonical JSON sau phép chuẩn hóa công bố. Không sửa timestamp/duration thành hằng để làm test pass. Chạy lại sau source edit phải đổi digest và phần liên quan.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).


---

Nguồn: [NFR-L3GEN-PERF-001](../../requirements/nfr/NFR-L3GEN-PERF-001.md) · revision 1 · status draft · SHA-256 `5b0a569392fcb18f7a0a14279b060d32bfaa07521ff7df6ac4ef9491f805c429`

### NFR-L3GEN-PERF-001 — Thời gian xử lý và giới hạn tài nguyên

- **Nhóm:** Performance.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md), [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md), [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md), [FR-L3GEN-016](../../requirements/fr/FR-L3GEN-016.md), [FR-L3GEN-017](../../requirements/fr/FR-L3GEN-017.md).

#### Yêu cầu có thể kiểm chứng

Môi trường benchmark đề xuất: 4 CPU logical, RAM 8 GiB, SSD, Python 3.12, no-AI, dependencies đã cài. Thời gian analyzer+ghi output (không gồm clone/AI/cài đặt) tối đa 60 giây cho 5.000 dòng Python, và 300 giây cho 50.000 dòng trong tập fixture/repo đã pin. Giới hạn tiếp nhận: ZIP nén 50 MiB, giải nén 200 MiB, 5.000 file và 100.000 dòng Python; vượt ngưỡng phải từ chối hoặc dừng có lý do. Worker tối đa 2 GiB RAM/phiên, 2 phiên chạy cùng lúc; phiên sau xếp hàng. Git fetch timeout 120 giây; mọi giới hạn có trong thông báo/help.

#### Điều kiện và cách kiểm

Đo 5 lần cho mỗi repo trên máy công bố, ghi từng lần và worst-case, peak RSS. Không ngoại suy từ máy khác hoặc repo nhỏ. Kiểm input sát/vượt giới hạn, ZIP bomb và job bị timeout; không báo hoàn tất khi bị dừng. OBS-L3GEN-001 mô tả cách thu số, không lặp ngưỡng.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).


---

Nguồn: [NFR-L3GEN-PRIV-001](../../requirements/nfr/NFR-L3GEN-PRIV-001.md) · revision 1 · status draft · SHA-256 `e3f077a48b7787f0975a523d6b09ca95879b7975b92fdbb69563f87eda09541a`

### NFR-L3GEN-PRIV-001 — Quyền riêng tư và vòng đời dữ liệu

- **Nhóm:** Privacy.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-005](../../requirements/fr/FR-L3GEN-005.md), [FR-L3GEN-007](../../requirements/fr/FR-L3GEN-007.md), [FR-L3GEN-010](../../requirements/fr/FR-L3GEN-010.md), [FR-L3GEN-012](../../requirements/fr/FR-L3GEN-012.md), [FR-L3GEN-014](../../requirements/fr/FR-L3GEN-014.md), [FR-L3GEN-016](../../requirements/fr/FR-L3GEN-016.md), [FR-L3GEN-017](../../requirements/fr/FR-L3GEN-017.md).

#### Yêu cầu có thể kiểm chứng

AI mặc định tắt; phải chủ động bật và biết provider, loại dữ liệu gửi. --no-ai không có outbound ở analyzer; CLI local no-AI không cần mạng; Git URL vẫn cần mạng để lấy repo đã được yêu cầu. Không đọc .env thật, private key hoặc gửi credentials. AI chỉ nhận model tối thiểu đã lọc giá trị nhạy cảm; source snippet cần đồng ý riêng và không thuộc bản đầu. Source tạm của web được xóa trong 24 giờ sau trạng thái cuối; output và metadata giữ tối đa 7 ngày, có tùy chọn xóa sớm. CLI output do người dùng quản lý và ghi rõ khác biệt này.

#### Điều kiện và cách kiểm

Dùng canary secrets ở .env, YAML và URL, kiểm log/output/payload không có giá trị; kiểm no-AI bằng network interception và phân biệt ingestion/analyzer. Test clock/cleanup sau hạn, hủy/lỗi và xóa sớm. Không coi bộ lọc secret là chứng minh phát hiện mọi bí mật tùy ý.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).


---

Nguồn: [NFR-L3GEN-REL-001](../../requirements/nfr/NFR-L3GEN-REL-001.md) · revision 1 · status draft · SHA-256 `71a4353e64563e12322b42838f5c8859c902d83a152753d8813360164b7d99ea`

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

Nguồn: [NFR-L3GEN-SEC-001](../../requirements/nfr/NFR-L3GEN-SEC-001.md) · revision 1 · status draft · SHA-256 `b6803846e8133182a42a7e7a4199338ae593a4a34e23cad27aff5d815cdc29a9`

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

Nguồn: [NFR-L3GEN-TRACE-001](../../requirements/nfr/NFR-L3GEN-TRACE-001.md) · revision 1 · status draft · SHA-256 `772e2e62be2953374fce6335e08bfbe66cfeaf9b35f7e82feff9cebc8b4438cf`

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

---

Nguồn: [OQ-L3GEN-001](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-001.md) · revision 1 · status open · SHA-256 `c91fa73ea141ea192f6af03eec48301ebc07025b87c7ffebf113e29933a1b507`

### OQ-L3GEN-001 — Xác nhận mã tổ chức và người chịu trách nhiệm

#### Câu hỏi cần người quyết định

Mã SYS-L3GEN/TEAM-L3GEN và key PRD-L3GEN-2609-001 đang dùng làm mã dự thảo. Anh Hà và reviewer thứ hai là ai, ai ký Product/Tech Lead/QA, ai nghiệm thu độc lập? Có registry/template/UID tool chính thức để đối chiếu không?

- **Owner theo vai:** Người phụ trách PRD (bạn) phối hợp mentor.
- **Hạn trả lời đề xuất:** 17/09/2026, trước Scope Gate. Đây không phải ngày mentor đã cam kết.
- **Blocking:** Toàn bộ metadata và Scope Gate.
- **Cách xử lý trong bản nháp:** Giữ mã dự thảo, không ghi tên hoặc chữ ký chưa được cung cấp.
- **Trả lời:** Chưa có.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.


---

Nguồn: [OQ-L3GEN-002](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-002.md) · revision 3 · status open · SHA-256 `cacb77d93aeb4f4130bbafbbba1510b13a5bd07aa36f4a594184e0450cdec89e`

### OQ-L3GEN-002 — Chốt phạm vi đầy đủ và lịch giao

#### Câu hỏi cần người quyết định

PRD mô tả full product gồm CLI, Git/ZIP, jobs/API, UI, component/L3, config/event. Timebox 2–3 người/4–6 tuần có áp dụng cho toàn bộ Must của M1–M3 không? Nếu không đủ capacity, phần nào được phép giao sau? Ngày bắt đầu và release thực tế là ngày nào? M1–M3 hiện chỉ là mốc kiểm tra nội bộ; nếu phát hành riêng từng mốc, Product/Tech Lead phải tách phạm vi Change Set và baseline tương ứng trước khi chốt.

**Làm rõ phạm vi cần chốt:** CLI, web nhận Git/ZIP, jobs/API và JSON/Mermaid là đề xuất cách dùng/tích hợp cho full product, không phải tất cả đều được đề bài chỉ định. Mentor có đồng ý mức ưu tiên đang đề xuất không? Cảnh báo trong bản này chỉ phục vụ hiểu giới hạn phân tích kiến trúc; rà code không dùng và cách xử lý lỗi HTTP nằm ngoài phạm vi. Căn cứ lựa chọn được ghi tại PRD mục I.

- **Owner theo vai:** Người phụ trách PRD phối hợp mentor.
- **Hạn trả lời đề xuất:** 17/09/2026, trước Scope Gate. Đây không phải ngày mentor đã cam kết.
- **Blocking:** Cam kết scope và milestone của toàn hệ thống.
- **Cách xử lý trong bản nháp:** Giữ đầy đủ yêu cầu; M1/M2/M3 là đề xuất thứ tự, không tự loại tính năng để khớp code đang có.
- **Trả lời:** Chưa có.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.


---

Nguồn: [OQ-L3GEN-003](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-003.md) · revision 1 · status open · SHA-256 `39b0d278dde8d9f06e47723ce1ee659313c032025c39cb035b9168d4258f0213`

### OQ-L3GEN-003 — Chốt ma trận pattern và adapter hỗ trợ

#### Câu hỏi cần người quyết định

Đồng ý Python/FastAPI + SQLAlchemy Column, requests/httpx, Pydantic settings và confluent_kafka làm stack đầu tiên? SQLModel/mapped_column, add_api_route và SDK event khác để phase mở rộng hay phải đưa vào Must? Những schema YAML cấu hình nào được phép diễn giải?

- **Owner theo vai:** Tech Lead được mentor chỉ định.
- **Hạn trả lời đề xuất:** 17/09/2026, trước Scope Gate. Đây không phải ngày mentor đã cam kết.
- **Blocking:** FR-L3GEN-003, FR-L3GEN-004, FR-L3GEN-014, FR-L3GEN-015 và NFR-L3GEN-COMP-001.
- **Cách xử lý trong bản nháp:** Không nói hỗ trợ mọi repo; công bố pattern cụ thể và cảnh báo phần chưa hỗ trợ.
- **Trả lời:** Chưa có.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.


---

Nguồn: [OQ-L3GEN-004](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-004.md) · revision 1 · status open · SHA-256 `945c1d5ccb56920298e9726f1dcfb6407bc2259163e7dc53a0ae961f4c74cc10`

### OQ-L3GEN-004 — Duyệt ngưỡng chất lượng và đáp án nghiệm thu

#### Câu hỏi cần người quyết định

Các ngưỡng NFR, cỡ mẫu OBS, máy benchmark và cách người đọc phân nhóm component có được chấp nhận không? Ai là hai người lập đáp án độc lập? Chốt repo/commit trước khi đo và kiểm baseline trải nghiệm người dùng.

- **Owner theo vai:** Product và QA được mentor chỉ định.
- **Hạn trả lời đề xuất:** 17/09/2026, trước Scope Gate. Đây không phải ngày mentor đã cam kết.
- **Blocking:** Tất cả NFR, KPI và nghiệm thu.
- **Cách xử lý trong bản nháp:** Giữ ngưỡng là proposed. Chưa có phép đo nào được coi là kết quả đạt sản phẩm.
- **Trả lời:** Chưa có.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.


---

Nguồn: [OQ-L3GEN-005](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-005.md) · revision 1 · status open · SHA-256 `45486e2956de761f44c9dee76cce9d7b753082799ec8b693326f5fdbd1fba447`

### OQ-L3GEN-005 — Chốt môi trường web, dữ liệu và AI

#### Câu hỏi cần người quyết định

Bản đầu chạy trong workspace tin cậy/local hay cần nhiều người dùng trên Internet? Có yêu cầu private Git repo/SSO không? Duyệt retention và Git allowlist; provider AI, consent và cost cap nào được cho phép?

- **Owner theo vai:** Tech Lead/Security phối hợp người phụ trách PRD.
- **Hạn trả lời đề xuất:** 17/09/2026, trước Scope Gate. Đây không phải ngày mentor đã cam kết.
- **Blocking:** FR-L3GEN-012, FR-L3GEN-016, FR-L3GEN-017; NFR SEC/PRIV/AI.
- **Cách xử lý trong bản nháp:** Đề xuất workspace tin cậy, public GitHub, không credential, AI opt-in; public multi-tenant chưa nằm trong scope.
- **Trả lời:** Chưa có.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.


---

Nguồn: [OQ-L3GEN-006](../../lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-006.md) · revision 4 · status open · SHA-256 `e60ee836e985e3ca9aea6c8521fb49707a548cfff1489427110fb3aa0c9697d7`

### OQ-L3GEN-006 — Xác nhận quy trình và schema khi thiếu tooling

#### Câu hỏi cần người quyết định

Chưa có bản PROC-SDLC-001, registry hay mẫu NFR/OBS đầy đủ trong attachment. File Quy_tac/process-working.md thực tế chứa mẫu PRD. Xác nhận bộ schema tạm, trình tự Scope Gate trước design/test mapping, quy tắc hash/UID và cách lưu evidence khi không có aide.

1. Ai cung cấp registry/policy và xác nhận type/edge, mã, `coordination.mode`, checklist và quyền ký trước Scope Gate?
2. New System chưa có graph đầy đủ thì khởi tạo và sinh impact thế nào? Nếu dùng cách thay thế, ai chấp nhận và lưu bằng chứng ra sao? Hiện intake/impact chưa chạy; không tự viết `impact.yaml` rồi đánh dấu hoàn tất.
3. Mẫu PRD DoD yêu cầu AC→implementation_target, trong khi trình tự B/C đặt thiết kế/planning sau Scope Gate. Mentor xác nhận coverage nào cần tại từng gate; mapping hiện rỗng là chưa đạt, không phải ngoại lệ đã được chấp nhận. Helper local không thay check-sdlc chính thức.
4. Chốt cách làm vertical slice/golden example phù hợp giới hạn human production code của đề bài.

**Lịch sử cập nhật:** ở revision 2 từng hỏi về NFR một theme. Bản dự thảo NFR-USA revision 2 đã bỏ đề xuất này và theo checklist sáng/tối của mentor. Đây là sửa hồ sơ theo nguồn, không phải câu trả lời hoặc waiver do mentor cấp; OQ-006 vẫn mở cho các vấn đề trên.

- **Owner theo vai:** Người phụ trách PRD phối hợp mentor.
- **Hạn trả lời đề xuất:** 17/09/2026, trước Scope Gate. Đây không phải ngày mentor đã cam kết.
- **Blocking:** Hoàn tất intake và kết luận tuân thủ/qua Scope Gate; không ngăn lấy ý kiến bản nháp PRD.
- **Cách xử lý trong bản nháp:** Giữ intake/impact/tier chưa xác nhận; xem [ghi chú intake và checklist gate](../../../docs/PRD-REVIEW-README.md). Mapping design/test còn trống được ghi chưa đủ điều kiện code. Không tuyên bố đã pass check-sdlc hoặc có approval.
- **Trả lời:** Chưa có.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.

