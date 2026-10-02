---
uid: "01M34AM2AH38TP25RR4G8E8GGA"
key: "FR-L3GEN-023"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-005","GOAL-L3GEN-007"],"constrained_by":["NFR-L3GEN-ACC-002","NFR-L3GEN-ABST-002"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-023 — Bằng chứng và nhãn mức chắc chắn

## Mô tả

Người đọc lần ngược được mỗi kết luận về đúng dữ kiện code và file trong snapshot đã phân tích, và phân biệt được phần đọc trực tiếp từ bằng chứng, phần suy ra, và phần chưa kết luận được.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Kiểm chứng kết quả |
| Ưu tiên | Must Have |
| Mốc | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-023-01

- **Given:** Người đọc chọn một component, một cạnh dependency hoặc một dữ kiện trong kết quả.
- **When:** người đọc mở phần bằng chứng.
- **Then:** công cụ chỉ ra các dữ kiện code và vị trí của chúng trong snapshot làm cơ sở cho kết luận đó.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-023-02

- **Given:** Một kết luận được công bố trong tài liệu hoặc sơ đồ.
- **When:** công cụ sinh kết quả.
- **Then:** kết luận mang nhãn confidence là exact hoặc inferred và nhãn completeness là full hoặc partial ở hai trường riêng; inferred và partial kèm lý do.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-023-03

- **Given:** Source trên đĩa đã thay đổi so với snapshot đã phân tích.
- **When:** người đọc mở bằng chứng của một kết luận.
- **Then:** công cụ báo snapshot không còn khớp, không dùng nội dung source mới làm bằng chứng cho kết luận cũ.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-023-04

- **Given:** Một kết luận không có bằng chứng là dữ kiện code có thật trong snapshot, hoặc bằng chứng đó không qua bước kiểm ở AC-L3GEN-022-02.
- **When:** công cụ sinh kết quả.
- **Then:** kết luận đó không được công bố trong sơ đồ hoặc tài liệu L3.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../../domain/glossary-core.md)
