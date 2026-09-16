---
uid: 01M2MV1DYC7RDWCG6K52QZE964
key: FR-L3GEN-005
type: functional-requirement
group: normative
scope: system
system: SYS-L3GEN
status: draft
revision: 1
ownership:
  accountable_team: TEAM-L3GEN
  accountable_role: product-owner
relations:
  satisfies: [GOAL-L3GEN-003]
  constrained_by: [NFR-L3GEN-COMP-001, NFR-L3GEN-REL-001]
  measured_by: [OBS-L3GEN-001]
verified_at: 2026-09-16
verified_against: []
classification: internal
ai_assisted: true
---

# FR-L3GEN-005 — Xuất tài liệu kiến trúc

## Mô tả

Người dùng xuất kết quả phân tích thành tài liệu dùng được bên ngoài hệ thống: tài liệu
L3 dạng Markdown, sơ đồ dạng Diagram-as-Code, và mô hình kiến trúc có cấu trúc để hệ
thống khác đọc.

Tất cả artifact của cùng một lần phân tích phải được tạo từ cùng một kết quả, để nội
dung trên giao diện và nội dung trong file xuất ra không mâu thuẫn nhau.

Use case liên quan: UC3.2 trong [USE_CASES](../../../docs/USE_CASES.md).

## Acceptance Criteria

### AC-L3GEN-005-01 — Xuất bộ artifact

- **given** một kết quả phân tích đã hoàn thành
- **when** người dùng yêu cầu xuất tài liệu
- **then** hệ thống tạo tài liệu L3 dạng Markdown, sơ đồ dạng Diagram-as-Code và mô
  hình kiến trúc có cấu trúc
- `validated_by:` TEST-L3GEN-005-01

### AC-L3GEN-005-02 — Nội dung L3 đầy đủ mục

- **given** một kết quả phân tích có component, API, data và external system
- **when** người dùng mở tài liệu L3 đã xuất
- **then** tài liệu gồm phạm vi phân tích, application và component, API, data entity,
  external system, event, quan hệ phụ thuộc, bằng chứng và giới hạn đã biết
- `validated_by:` TEST-L3GEN-005-02

### AC-L3GEN-005-03 — Artifact nhất quán với giao diện

- **given** cùng một lần phân tích
- **when** so sánh nội dung trên giao diện với các artifact đã xuất
- **then** component, quan hệ, evidence và limitation giống nhau ở cả hai nơi
- `validated_by:` TEST-L3GEN-005-03

### AC-L3GEN-005-04 — Sơ đồ xuất ra ở mức component

- **given** một kết quả phân tích
- **when** người dùng mở sơ đồ đã xuất
- **then** sơ đồ trình bày application, component và quan hệ giữa chúng, không liệt kê
  mọi function, class hoặc biến
- `validated_by:` TEST-L3GEN-005-04

### AC-L3GEN-005-05 — Một artifact thất bại không mất kết quả

- **given** việc tạo một artifact thất bại
- **when** hệ thống xử lý lỗi đó
- **then** kết quả phân tích được giữ nguyên, hệ thống báo rõ artifact nào thất bại và
  cho phép thử lại
- `constrained_by:` NFR-L3GEN-REL-001
- `validated_by:` TEST-L3GEN-005-05

### AC-L3GEN-005-06 — Artifact không chứa đường dẫn máy người dùng

- **given** một lần phân tích chạy từ một thư mục bất kỳ trên máy người dùng
- **when** hệ thống tạo artifact
- **then** artifact dùng đường dẫn tương đối theo gốc source, không chứa đường dẫn
  tuyệt đối của máy chạy
- `constrained_by:` NFR-L3GEN-SEC-001, NFR-L3GEN-COMP-001
- `validated_by:` TEST-L3GEN-005-06

### AC-L3GEN-005-07 — Artifact ổn định giữa hai lần xuất

- **given** cùng một kết quả phân tích
- **when** người dùng xuất tài liệu hai lần
- **then** nội dung artifact giống nhau giữa hai lần, trừ các trường ghi thời điểm chạy
- `constrained_by:` NFR-L3GEN-COMP-001
- `validated_by:` TEST-L3GEN-005-07
