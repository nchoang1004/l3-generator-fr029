---
uid: 01M2MV1DYC98JQ48XYGWEN90DA
key: FR-L3GEN-004
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
  satisfies: [GOAL-L3GEN-002, GOAL-L3GEN-003]
  constrained_by: [NFR-L3GEN-USA-001, NFR-L3GEN-REL-001]
  measured_by: [OBS-L3GEN-003, OBS-L3GEN-004]
verified_at: 2026-09-16
verified_against: []
classification: internal
ai_assisted: true
---

# FR-L3GEN-004 — Kiểm tra evidence và giới hạn

## Mô tả

Người dùng kiểm chứng được từng kết luận trong mô hình kiến trúc thay vì phải tin vào
mô tả. Với một quan hệ hoặc thành phần bất kỳ, người dùng mở được vị trí source và
đường bằng chứng dẫn tới kết luận đó.

Kết quả phải phân biệt rõ hai điều khác nhau: source thực sự không có một thành phần,
và hệ thống chưa đủ khả năng hoặc chưa đủ bằng chứng để tìm ra nó. Nhầm hai điều này
khiến người đọc hiểu sai hệ thống được phân tích.

Use case liên quan: `Kiểm tra bằng chứng nguồn` và UC3.1 trong
[USE_CASES](../../../docs/USE_CASES.md).

## Acceptance Criteria

### AC-L3GEN-004-01 — Mở evidence của một quan hệ

- **given** người dùng đang xem một quan hệ trong mô hình, ví dụ một component gọi một
  external system
- **when** người dùng yêu cầu xem bằng chứng của quan hệ đó
- **then** hệ thống hiển thị vị trí `file:line` và đường bằng chứng dẫn tới kết luận
- `validated_by:` TEST-L3GEN-004-01

### AC-L3GEN-004-02 — Mọi quan hệ công khai đều có evidence

- **given** một kết quả phân tích bất kỳ
- **when** kiểm tra các quan hệ trong mô hình kiến trúc
- **then** mỗi quan hệ có ít nhất một evidence, hoặc được đánh dấu rõ là partial/unknown
  kèm lý do
- `validated_by:` TEST-L3GEN-004-02

### AC-L3GEN-004-03 — Xem coverage của lần phân tích

- **given** một lần phân tích đã hoàn thành
- **when** người dùng xem phần chất lượng kết quả
- **then** hệ thống hiển thị phạm vi đã đọc, file bị bỏ qua, ngôn ngữ hoặc framework
  chưa hỗ trợ và lỗi phân tích đã gặp
- `validated_by:` TEST-L3GEN-004-03

### AC-L3GEN-004-04 — Phân biệt không có với chưa đọc được

- **given** hệ thống không tìm thấy một loại thành phần trong repository
- **when** người dùng xem kết quả
- **then** kết quả nói rõ đây là trường hợp source không có, hay trường hợp hệ thống
  chưa hỗ trợ hoặc chưa đủ bằng chứng
- `validated_by:` TEST-L3GEN-004-04

### AC-L3GEN-004-05 — Trường hợp phụ thuộc runtime

- **given** một kết luận phụ thuộc dữ liệu chỉ có khi chương trình chạy
- **when** người dùng xem kết quả
- **then** phần đó được đánh dấu runtime-dependent kèm lý do và evidence, và hệ thống
  không chọn một khả năng cụ thể để trình bày như kết luận chắc chắn
- `validated_by:` TEST-L3GEN-004-05

### AC-L3GEN-004-06 — Lời gọi chưa xác định không thành quan hệ kiến trúc

- **given** một lời gọi trong source mà hệ thống chưa xác định được đích
- **when** hệ thống dựng mô hình kiến trúc
- **then** lời gọi đó xuất hiện trong phần giới hạn hoặc bằng chứng, và không trở thành
  một quan hệ trong mô hình kiến trúc
- `validated_by:` TEST-L3GEN-004-06

### AC-L3GEN-004-07 — Giới hạn luôn được công bố

- **given** một lần phân tích bất kỳ, kể cả khi chạy trọn vẹn
- **when** người dùng xem kết quả
- **then** phần giới hạn luôn có mặt, gồm cả trường hợp không có giới hạn nào, thay vì
  bị ẩn đi
- `constrained_by:` NFR-L3GEN-USA-001
- `validated_by:` TEST-L3GEN-004-07

### AC-L3GEN-004-08 — Mô tả do AI không dùng làm bằng chứng

- **given** một kết luận có kèm mô tả do AI sinh
- **when** người dùng mở phần bằng chứng của kết luận đó
- **then** bằng chứng là vị trí source và rule đã áp dụng, không phải đoạn mô tả do AI
  viết
- `validated_by:` TEST-L3GEN-004-08
