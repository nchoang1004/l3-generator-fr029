---
uid: "01M34AM2AJZBAF4QHY33Z5909H"
key: "FR-L3GEN-025"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-006"],"constrained_by":["NFR-L3GEN-ABST-002","NFR-L3GEN-OPS-001","NFR-L3GEN-SEC-002"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-025 — Xuất kết quả

## Mô tả

Người dùng lấy được sơ đồ component (mức L2), tài liệu L3 contract theo FR-L3GEN-027, và bộ dữ liệu có cấu trúc để công cụ khác dùng lại, cùng thông tin phiên bản và phạm vi của lần chạy.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Sử dụng kết quả |
| Ưu tiên | Must Have |
| Mốc | M1 cho bản đầu; M2 khi có component |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-025-01

- **Given:** Một lần phân tích kết thúc với trạng thái hoàn tất hoặc partial.
- **When:** người dùng xuất kết quả.
- **Then:** công cụ tạo tài liệu L3 contract theo FR-L3GEN-027, sơ đồ component và dependency, mã nguồn sơ đồ, và bộ dữ liệu JSON.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-025-02

- **Given:** Một hệ thống khác đọc bộ dữ liệu JSON.
- **When:** hệ thống đó nạp file.
- **Then:** file có schema version, định danh của snapshot đã phân tích, và không chứa cạnh trỏ tới thực thể không tồn tại trong cùng file.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-025-03

- **Given:** Một artifact trong bộ kết quả sinh lỗi.
- **When:** công cụ xuất kết quả.
- **Then:** công cụ nêu rõ artifact nào lỗi và cho phép thử lại, giữ nguyên các artifact hợp lệ.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-025-04

- **Given:** Cùng một mô hình kiến trúc được xuất ra nhiều dạng artifact.
- **When:** người dùng đối chiếu giữa các artifact.
- **Then:** không artifact nào chứa component hoặc quan hệ mà artifact khác không có; mọi artifact giữ mức application/component.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)
