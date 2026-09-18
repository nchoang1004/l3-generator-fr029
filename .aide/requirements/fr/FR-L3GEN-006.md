---
uid: "01M2J06Z4BMQEDGBF3CYFF98RB"
key: "FR-L3GEN-006"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 5
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001","GOAL-L3GEN-002"],"constrained_by":["NFR-L3GEN-ABST-001","NFR-L3GEN-ACC-001","NFR-L3GEN-DET-001","NFR-L3GEN-TRACE-001"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-006 — Truy vết tham chiếu và lời gọi xuyên file

## Mô tả

Người dùng xem quan hệ gọi hàm, import và kế thừa với đích cụ thể hoặc lý do chưa xác định được.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-006-01

- **Given:** Hai module có class/method trùng tên và caller import từng đích bằng alias hoặc relative import.
- **When:** người dùng phân tích.
- **Then:** quan hệ nối đúng symbol theo scope/import của caller; không chọn tên duy nhất hoặc đầu tiên toàn repository làm exact.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm đích symbol và vị trí định nghĩa.

### AC-L3GEN-006-02

- **Given:** Receiver có kiểu từ gán Class(), annotation hoặc self.field có khai báo xác định.
- **When:** người dùng phân tích.
- **Then:** lời gọi nối đúng method trong lớp hoặc chuỗi kế thừa được hỗ trợ.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không suy kiểu chỉ từ tên biến db_session.

### AC-L3GEN-006-03

- **Given:** Có dynamic import, wildcard import mơ hồ, receiver chưa biết kiểu hoặc kế thừa vòng/nhiều đích.
- **When:** người dùng phân tích.
- **Then:** quan hệ chưa giải được hoặc mơ hồ vẫn được giữ với vị trí và lý do; hệ thống không treo, không chọn đích tùy tiện.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Tách external library đã biết tên khỏi unresolved internal.

### AC-L3GEN-006-04

- **Given:** Hàm chỉ nhắc tên lớp dữ liệu mà không có thao tác DB được chứng minh.
- **When:** người dùng xem graph.
- **Then:** công cụ có thể ghi references_entity nhưng không kết luận reads hoặc writes từ việc xuất hiện tên lớp.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Quan hệ DB đọc/ghi chỉ có khi có rule và bằng chứng thao tác; chưa giải được thì ghi rõ.

### AC-L3GEN-006-05

- **Given:** Một lời gọi hoặc tham chiếu chưa resolve được đích, hoặc đích nằm ngoài phạm vi phân tích.
- **When:** công cụ dựng component model và sơ đồ dependency.
- **Then:** dữ kiện đó không trở thành cạnh giữa hai component; nó được giữ ở lớp dữ kiện với nhãn unresolved và lý do. Cạnh kiến trúc chỉ sinh ra từ quan hệ đã resolve về một đích cụ thể.
- `constrained_by:` [NFR-L3GEN-ABST-001, NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu tập cạnh kiến trúc với tập quan hệ unresolved; giao của hai tập phải rỗng. Không dùng tên module hay tên file để đoán đích thay cho resolve.

## Trạng thái liên kết triển khai

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-ABST-001](../nfr/NFR-L3GEN-ABST-001.md)
- [NFR-L3GEN-ACC-001](../nfr/NFR-L3GEN-ACC-001.md)
- [NFR-L3GEN-TRACE-001](../nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-DET-001](../nfr/NFR-L3GEN-DET-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)

