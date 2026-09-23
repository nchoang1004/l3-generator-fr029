---
uid: "01M34AM2AJ4XSZ1WJAPKEDP167"
key: "FR-L3GEN-026"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-004","GOAL-L3GEN-005"],"constrained_by":["NFR-L3GEN-ABST-002","NFR-L3GEN-OPS-001","NFR-L3GEN-SEC-002"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-026 — Khám phá kết quả trên web

## Mô tả

Trên web, người dùng theo dõi lần chạy hiện tại rồi xem tổng quan kiến trúc, đi sâu theo component, và mở bằng chứng của từng quan hệ.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Sử dụng kết quả |
| Ưu tiên | Must Have |
| Mốc | M2 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-026-01

- **Given:** Một lần phân tích đang chạy trên web.
- **When:** người dùng mở màn hình trạng thái.
- **Then:** công cụ hiển thị giai đoạn đang chạy và trạng thái running, completed, partial hoặc failed kèm lý do lỗi.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-026-02

- **Given:** Một lần phân tích đã có kết quả.
- **When:** người dùng mở kết quả.
- **Then:** công cụ hiển thị tổng quan kiến trúc, các góc nhìn component, API, dữ liệu, tích hợp và dependency, cùng phần giới hạn của lần chạy.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-026-03

- **Given:** Người dùng cần tìm một component hoặc quan hệ cụ thể trong kết quả.
- **When:** người dùng tìm và lọc.
- **Then:** công cụ trả về kết quả khớp và cho mở phần bằng chứng theo FR-L3GEN-023 từ đó.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)
