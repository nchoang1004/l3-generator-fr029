---
uid: 01M2MV1DYCHYZ7KM0F80MDPDKZ
key: FR-L3GEN-003
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
  satisfies: [GOAL-L3GEN-001]
  constrained_by: [NFR-L3GEN-USA-001, NFR-L3GEN-PERF-001, NFR-L3GEN-SEC-001]
  measured_by: [OBS-L3GEN-001, OBS-L3GEN-002]
verified_at: 2026-09-16
verified_against: []
classification: internal
ai_assisted: true
---

# FR-L3GEN-003 — Xem, lưu và truy vết kiến trúc

## Mô tả

Người dùng khám phá kết quả phân tích theo mục tiêu đang cần: nhìn tổng quan, xem
application và component, xem API và luồng yêu cầu, xem dữ liệu và tích hợp, hoặc truy
vết từ một thành phần sang các thành phần liên quan.

Kết quả phân tích được lưu lại để mở lại về sau. Hệ thống giới hạn số lần phân tích giữ
cho mỗi repository và thời hạn lưu mỗi kết quả; người dùng cũng xóa thủ công được trước
khi hết hạn. Ngưỡng cụ thể nằm ở
[NFR-L3GEN-SEC-001](../nfr/NFR-L3GEN-SEC-001.md).

Diagram mặc định trình bày ở mức application/component. Nó không liệt kê mọi function,
class hay biến; chi tiết đó chỉ xuất hiện khi người dùng mở evidence theo FR-L3GEN-004.

Use case liên quan: UC2 và UC3.1 trong [USE_CASES](../../../docs/USE_CASES.md).

## Acceptance Criteria

### AC-L3GEN-003-01 — Xem tổng quan sau khi phân tích xong

- **given** một lần phân tích vừa hoàn thành
- **when** người dùng được đưa tới kết quả
- **then** hệ thống hiển thị tổng quan gồm application, entry point, component chính,
  phạm vi đã phân tích và các giới hạn nổi bật
- `constrained_by:` NFR-L3GEN-USA-001
- `validated_by:` TEST-L3GEN-003-01

### AC-L3GEN-003-02 — Các góc nhìn kiến trúc

- **given** một kết quả phân tích có component, API, data entity và external system
- **when** người dùng chuyển giữa các góc nhìn
- **then** người dùng xem được ứng dụng và thành phần, API và luồng yêu cầu, kho dữ
  liệu và tích hợp, mỗi góc nhìn dựa trên cùng một kết quả phân tích
- `validated_by:` TEST-L3GEN-003-02

### AC-L3GEN-003-03 — Truy vết phụ thuộc

- **given** người dùng đang xem một API hoặc component
- **when** người dùng truy vết phụ thuộc của nó
- **then** hệ thống hiển thị các component, data entity hoặc external system liên quan
  theo quan hệ đã xác định trong mô hình
- `validated_by:` TEST-L3GEN-003-03

### AC-L3GEN-003-04 — Diagram trình bày ở mức component

- **given** một repository có nhiều function nhưng ít component
- **when** hệ thống hiển thị diagram mặc định
- **then** diagram trình bày application, component và quan hệ giữa chúng, và không tạo
  một node cho mỗi function, class hoặc biến
- `validated_by:` TEST-L3GEN-003-04

### AC-L3GEN-003-05 — Lưu lần phân tích

- **given** một lần phân tích hoàn thành
- **when** hệ thống ghi nhận kết quả
- **then** lần phân tích đó xuất hiện trong danh sách lịch sử, kèm repository, thời
  điểm chạy và trạng thái kết quả
- `validated_by:` TEST-L3GEN-003-05

### AC-L3GEN-003-06 — Mở lại một lần phân tích đã lưu

- **given** một lần phân tích đã lưu và chưa hết hạn
- **when** người dùng chọn mở lại
- **then** hệ thống hiển thị đúng mô hình, evidence và limitation của lần chạy đó, kèm
  phiên bản source đã dùng
- `validated_by:` TEST-L3GEN-003-06

### AC-L3GEN-003-07 — Kết quả cũ không trộn với source hiện tại

- **given** source đã thay đổi sau khi một lần phân tích được lưu
- **when** người dùng mở lại lần phân tích đó
- **then** kết quả vẫn là snapshot của lần chạy cũ, và evidence chỉ về phiên bản source
  của lần chạy đó
- `validated_by:` TEST-L3GEN-003-07

### AC-L3GEN-003-08 — Giới hạn 10 lần mỗi repository

- **given** một repository đã có 10 lần phân tích được lưu
- **when** người dùng chạy phân tích lần tiếp theo cho repository đó
- **then** hệ thống giữ 10 kết quả gần nhất và loại kết quả cũ nhất
- `constrained_by:` NFR-L3GEN-SEC-001
- `validated_by:` TEST-L3GEN-003-08

### AC-L3GEN-003-09 — Kết quả hết hạn

- **given** một lần phân tích đã quá thời hạn lưu trữ đã công bố
- **when** người dùng tìm kết quả đó
- **then** kết quả không còn mở lại được, và hệ thống nói rõ lý do hết hạn
- `constrained_by:` NFR-L3GEN-SEC-001
- `validated_by:` TEST-L3GEN-003-09

### AC-L3GEN-003-10 — Xóa thủ công một lần phân tích

- **given** một lần phân tích đã lưu và chưa hết hạn
- **when** người dùng chọn xóa và xác nhận
- **then** kết quả đó bị xóa, không mở lại được, và các lần phân tích khác không bị ảnh
  hưởng
- `constrained_by:` NFR-L3GEN-SEC-001
- `validated_by:` TEST-L3GEN-003-10

### AC-L3GEN-003-11 — Xác nhận trước khi xóa

- **given** người dùng chọn xóa một lần phân tích
- **when** hệ thống nhận yêu cầu
- **then** hệ thống hỏi xác nhận trước khi xóa, để tránh mất kết quả do thao tác nhầm
- `constrained_by:` NFR-L3GEN-USA-001
- `validated_by:` TEST-L3GEN-003-11
