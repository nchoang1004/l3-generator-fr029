---
uid: "01M34AM2AGN88WN875NJARJEDP"
key: "FR-L3GEN-020"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-004","GOAL-L3GEN-007"],"constrained_by":["NFR-L3GEN-OPS-001","NFR-L3GEN-ACC-002"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-020 — Xác định phạm vi phân tích

## Mô tả

Người dùng biết phần nào của repository được phân tích, phần nào bị bỏ qua và phần nào nằm ngoài ngôn ngữ hoặc framework được hỗ trợ, trước khi đọc kết quả kiến trúc.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Phân tích repository |
| Ưu tiên | Must Have |
| Mốc | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-020-01

- **Given:** Repository chứa nhiều thư mục, trong đó có phần thuộc stack được hỗ trợ và phần không.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ liệt kê các đơn vị phân tích đã xét kèm đường dẫn, và liệt kê riêng phần bỏ qua kèm lý do.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-020-02

- **Given:** Repository rỗng, hoặc toàn bộ nội dung thuộc ngôn ngữ chưa được hỗ trợ.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ báo trạng thái rỗng hoặc ngoài phạm vi hỗ trợ, không trả về kết quả thành công rỗng.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-020-03

- **Given:** Một đơn vị phân tích thuộc ngôn ngữ được hỗ trợ nhưng ở mức độ sâu thấp hơn Python.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ công bố mức hỗ trợ áp dụng cho đơn vị đó, để người đọc biết nhãn chất lượng của kết luận trong đơn vị này được đặt theo mức nào.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../../domain/glossary-core.md)
