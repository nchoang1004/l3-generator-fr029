---
uid: "01M2J06Z48P8QPD1NGCBV6SNC6"
key: "FR-L3GEN-004"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 7
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001","GOAL-L3GEN-002"],"constrained_by":["NFR-L3GEN-ACC-001","NFR-L3GEN-COMP-001","NFR-L3GEN-TRACE-001"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-004 — Liệt kê mô hình dữ liệu

## Mô tả

Người dùng xem lớp dữ liệu, tên bảng nếu xác định được, cột và khóa ngoại; nhận diện entity không đồng nghĩa biết tên bảng. Phase đầu phủ SQLAlchemy; ORM của Java/Spring Boot thuộc phase sau.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1: entity SQLAlchemy; phase sau: entity Java |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-004-01

- **Given:** Lớp SQLAlchemy có __tablename__ hằng, Column và ForeignKey.
- **When:** người dùng phân tích.
- **Then:** công cụ xuất lớp, bảng, cột, kiểu, khóa chính và khóa ngoại được khai báo cùng nguồn.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Phạm vi phase đầu: `declarative_base`/`Base`, `Column`, `ForeignKey` và `relationship` trực tiếp; SQLModel/`mapped_column` nằm ngoài phase đầu theo NFR-L3GEN-COMP-001.

### AC-L3GEN-004-02

- **Given:** Entity kế thừa qua lớp trung gian trong repository.
- **When:** người dùng phân tích.
- **Then:** công cụ nối được chuỗi kế thừa trong khả năng hỗ trợ và không coi lớp __abstract__ là bảng triển khai.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Có fixture lớp cha khác file.

### AC-L3GEN-004-03

- **Given:** Tên bảng do lớp cơ sở sinh lúc chạy hoặc __tablename__ là biểu thức chưa giải được.
- **When:** người dùng phân tích.
- **Then:** công cụ giữ entity nhưng biểu diễn tên bảng chưa xác định, ghi partial và lý do; không tự lower-case tên class để đoán.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Fixture có tên bảng được sinh lúc chạy; kiểm kết quả giữ entity và báo tên bảng chưa xác định thay vì đoán từ tên lớp.

### AC-L3GEN-004-04

- **Given:** Khóa ngoại trỏ tới bảng ngoài phần quét.
- **When:** người dùng phân tích.
- **Then:** công cụ giữ nguyên khai báo và nguồn, đánh dấu đích chưa resolve; không tự tạo bảng thật để nối đủ graph.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu cả quan hệ liên bảng đã và chưa giải được.

### AC-L3GEN-004-05

- **Given:** Repository có thao tác SQLAlchemy đọc bằng query(Model).all()/first()/one() hoặc Session.get(Model, id), và thao tác add/delete với entity xác định được.
- **When:** người dùng xem quan hệ component hoặc hàm tới dữ liệu.
- **Then:** công cụ nối quan hệ đọc hoặc ý định ghi/xóa tới entity cùng bằng chứng callsite; không kết luận giao dịch đã commit hoặc dữ liệu đã thay đổi ở runtime chỉ từ add/delete.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Phân biệt tên entity xuất hiện, query chưa thực thi, thao tác truy vấn và thao tác ghi chờ transaction; SDK/SQL động ngoài pattern phải ghi unknown.

### AC-L3GEN-004-06

- **Given:** Repository Java dùng ORM thuộc phạm vi đã công bố của Spring Boot.
- **When:** người dùng phân tích.
- **Then:** entity Java hiện ra với cùng cấu trúc dữ liệu và cùng nhãn chất lượng như entity Python; tên bảng chưa xác định được vẫn giữ unknown kèm lý do, không suy từ tên lớp.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Dùng Jakarta Persistence trực tiếp theo ma trận Java roadmap ở NFR-L3GEN-COMP-001; ORM ngoài phạm vi phải hiện ở phần giới hạn. AC này thuộc phase sau.

## Trạng thái liên kết triển khai

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-ACC-001](../nfr/NFR-L3GEN-ACC-001.md)
- [NFR-L3GEN-TRACE-001](../nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-COMP-001](../nfr/NFR-L3GEN-COMP-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)

