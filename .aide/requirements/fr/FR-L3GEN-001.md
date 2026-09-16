---
uid: 01M2MV1DYBFBXF15DNW6GZ7NYP
key: FR-L3GEN-001
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
  constrained_by: [NFR-L3GEN-SEC-001, NFR-L3GEN-PERF-001, NFR-L3GEN-USA-001]
  measured_by: [OBS-L3GEN-001]
verified_at: 2026-09-16
verified_against: []
classification: internal
ai_assisted: true
---

# FR-L3GEN-001 — Cung cấp repository đầu vào

## Mô tả

Người dùng cung cấp mã nguồn cần phân tích bằng một trong ba cách: chọn thư mục cục
bộ, tải lên file ZIP, hoặc nhập URL của một repository GitHub public. Trước khi phân
tích bắt đầu, người dùng biết được nguồn nào đã được nhận và phạm vi source sẽ đọc.

Khi đầu vào không dùng được, hệ thống nói rõ nguyên nhân và cách sửa, thay vì bắt đầu
một lần phân tích cho ra kết quả rỗng khó hiểu.

Use case liên quan: UC1 và ba biến thể của `Cung cấp mã nguồn` trong
[USE_CASES](../../../docs/USE_CASES.md).

## Acceptance Criteria

### AC-L3GEN-001-01 — Chọn thư mục cục bộ

- **given** người dùng đang ở màn hình cung cấp mã nguồn
- **when** người dùng chọn một thư mục cục bộ đọc được
- **then** hệ thống nhận thư mục đó và hiển thị phạm vi source sẽ đọc trước khi phân
  tích bắt đầu
- `implementation_target:` giao diện cung cấp mã nguồn, engine inventory
- `validated_by:` TEST-L3GEN-001-01

### AC-L3GEN-001-02 — Tải lên file ZIP hợp lệ

- **given** người dùng có một file ZIP chứa source trong giới hạn kích thước đã công bố
- **when** người dùng tải file ZIP lên
- **then** hệ thống giải nén trong vùng xử lý riêng và hiển thị phạm vi source sẽ đọc
- `constrained_by:` NFR-L3GEN-SEC-001, NFR-L3GEN-PERF-001
- `validated_by:` TEST-L3GEN-001-02

### AC-L3GEN-001-03 — Nhập URL GitHub public

- **given** người dùng có URL của một repository GitHub public
- **when** người dùng nhập URL và yêu cầu lấy source
- **then** hệ thống lấy source từ GitHub và hiển thị phạm vi cùng phiên bản source đã
  lấy
- `validated_by:` TEST-L3GEN-001-03

### AC-L3GEN-001-04 — Ba hình thức đầu vào cho cùng kết quả

- **given** cùng một repository được cung cấp qua thư mục cục bộ, qua file ZIP và qua
  URL GitHub
- **when** người dùng chạy phân tích trên từng nguồn
- **then** ba lần phân tích cho cùng component, quan hệ, evidence và limitation
- `validated_by:` TEST-L3GEN-001-04

### AC-L3GEN-001-05 — Thư mục không đọc được

- **given** người dùng chọn một đường dẫn không tồn tại hoặc không có quyền đọc
- **when** hệ thống kiểm tra đầu vào
- **then** hệ thống không bắt đầu phân tích, và nói rõ đường dẫn hoặc quyền truy cập
  nào cần sửa
- `validated_by:` TEST-L3GEN-001-05

### AC-L3GEN-001-06 — ZIP hỏng hoặc sai định dạng

- **given** người dùng tải lên một file không phải ZIP hợp lệ
- **when** hệ thống kiểm tra đầu vào
- **then** hệ thống từ chối file, không bắt đầu phân tích, và giải thích nguyên nhân
- `validated_by:` TEST-L3GEN-001-06

### AC-L3GEN-001-07 — ZIP chứa đường dẫn thoát khỏi vùng giải nén

- **given** người dùng tải lên một file ZIP có entry trỏ ra ngoài thư mục giải nén
- **when** hệ thống giải nén
- **then** hệ thống từ chối file và không ghi bất kỳ file nào ra ngoài vùng xử lý
- `constrained_by:` NFR-L3GEN-SEC-001
- `validated_by:` TEST-L3GEN-001-07

### AC-L3GEN-001-08 — ZIP vượt giới hạn kích thước

- **given** người dùng tải lên file ZIP vượt giới hạn đã công bố, tính cả kích thước
  nén và kích thước sau giải nén
- **when** hệ thống kiểm tra đầu vào
- **then** hệ thống từ chối trước khi giải nén hết, và nói rõ giới hạn đã chạm
- `constrained_by:` NFR-L3GEN-SEC-001, NFR-L3GEN-PERF-001
- `validated_by:` TEST-L3GEN-001-08

### AC-L3GEN-001-09 — URL GitHub sai hoặc repository không tồn tại

- **given** người dùng nhập một URL sai định dạng hoặc trỏ tới repository không tồn tại
- **when** hệ thống cố lấy source
- **then** hệ thống báo lỗi nhập hoặc lỗi truy cập, và không hiển thị kết quả như một
  repository rỗng
- `validated_by:` TEST-L3GEN-001-09

### AC-L3GEN-001-10 — Repository GitHub yêu cầu quyền

- **given** người dùng nhập URL của một repository private hoặc cần quyền truy cập
- **when** hệ thống cố lấy source
- **then** hệ thống nói rõ chưa có quyền truy cập, và không yêu cầu người dùng cung cấp
  credential
- `constrained_by:` NFR-L3GEN-SEC-001
- `validated_by:` TEST-L3GEN-001-10

### AC-L3GEN-001-11 — Mất kết nối khi lấy source GitHub

- **given** hệ thống đang lấy source từ GitHub
- **when** kết nối bị gián đoạn trước khi lấy xong
- **then** hệ thống cho phép thử lại và không tạo ra một lần phân tích với source không
  đầy đủ
- `validated_by:` TEST-L3GEN-001-11
