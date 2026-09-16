---
uid: 01M2MV1DYB5ZSGKXGGDVQPEG8P
key: FR-L3GEN-002
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
  satisfies: [GOAL-L3GEN-001, GOAL-L3GEN-003]
  constrained_by: [NFR-L3GEN-SEC-001, NFR-L3GEN-PERF-001, NFR-L3GEN-REL-001]
  measured_by: [OBS-L3GEN-003]
verified_at: 2026-09-16
verified_against: []
classification: internal
ai_assisted: true
---

# FR-L3GEN-002 — Tạo mô hình kiến trúc từ source

## Mô tả

Hệ thống đọc source đã nhận và tạo ra một mô hình kiến trúc ở mức L3, gồm
application, component, API, data entity, external system và event. Việc đọc source là
read-only: hệ thống không chạy, không import và không sửa source đầu vào.

Mỗi quan hệ trong mô hình phải dựa trên bằng chứng tĩnh trong source. Khi không đủ bằng
chứng, hệ thống dừng ở phần chắc chắn và ghi lý do, thay vì đoán để mô hình trông đầy
đủ hơn.

Phạm vi MVP: Python với FastAPI, SQLAlchemy/SQLModel, httpx/requests và Kafka; Java với
Spring Boot và Kafka. Ngôn ngữ và framework ngoài phạm vi này vẫn được kiểm kê nhưng
phải được công bố là chưa hỗ trợ.

Use case liên quan: UC1 trong [USE_CASES](../../../docs/USE_CASES.md). Contract kỹ
thuật ở [SPEC](../../../SPEC_Code_to_L3_Generator.md) mục 6 và 7.

## Acceptance Criteria

### AC-L3GEN-002-01 — Không thực thi source đầu vào

- **given** một repository bất kỳ được đưa vào phân tích
- **when** hệ thống phân tích source
- **then** hệ thống không import, không chạy, không `exec`/`eval` và không sửa file nào
  của repository đầu vào
- `constrained_by:` NFR-L3GEN-SEC-001
- `validated_by:` TEST-L3GEN-002-01

### AC-L3GEN-002-02 — Kiểm kê theo file, không theo folder

- **given** một repository phẳng hoặc trộn nhiều ngôn ngữ trong cùng thư mục
- **when** hệ thống kiểm kê source
- **then** mỗi file được nhận diện ngôn ngữ độc lập, và không folder nào bị kết luận là
  một service chỉ vì vị trí hoặc tên của nó
- `validated_by:` TEST-L3GEN-002-02

### AC-L3GEN-002-03 — Phát hiện thành phần kiến trúc trong phạm vi hỗ trợ

- **given** một repository trong phạm vi stack đã hỗ trợ
- **when** hệ thống phân tích xong
- **then** kết quả gồm module/package, entry point, application/component, API route,
  data entity, external system và important dependency đã phát hiện được
- `validated_by:` TEST-L3GEN-002-03

### AC-L3GEN-002-04 — Quan hệ từ API tới dữ liệu

- **given** một repository có route gọi xuống service, service gọi repository và
  repository đọc/ghi một entity
- **when** hệ thống phân tích
- **then** mô hình thể hiện chuỗi quan hệ từ API qua component tới data entity, và mỗi
  cạnh trong chuỗi có evidence về `file:line`
- `validated_by:` TEST-L3GEN-002-04

### AC-L3GEN-002-05 — Phát hiện quan hệ event Kafka

- **given** một repository dùng Kafka để publish hoặc consume message
- **when** hệ thống phân tích
- **then** mô hình thể hiện component nào publish và component nào consume, kèm tên
  topic khi xác định được từ source
- `validated_by:` TEST-L3GEN-002-05

### AC-L3GEN-002-06 — Topic Kafka phụ thuộc runtime

- **given** tên topic chỉ được xác định khi chương trình chạy, ví dụ lấy từ
  configuration hoặc biến môi trường
- **when** hệ thống phân tích
- **then** quan hệ event được ghi với trạng thái runtime-dependent kèm lý do, và hệ
  thống không chọn một tên topic cụ thể
- `validated_by:` TEST-L3GEN-002-06

### AC-L3GEN-002-07 — Broker khác Kafka

- **given** một repository dùng message broker ngoài Kafka
- **when** hệ thống phân tích
- **then** kết quả ghi rõ broker đó chưa được hỗ trợ trong limitation, và không mô tả
  repository như không có event
- `validated_by:` TEST-L3GEN-002-07

### AC-L3GEN-002-08 — Không tạo quan hệ từ tên gọi giống framework

- **given** source có một method trùng tên với API của framework nhưng thuộc class
  khác, ví dụ `disk_manager.mount(...)`
- **when** hệ thống phân tích
- **then** hệ thống không tạo quan hệ kiến trúc của framework cho lời gọi đó
- `validated_by:` TEST-L3GEN-002-08

### AC-L3GEN-002-09 — Không gộp hai application cùng framework

- **given** source tạo hai application object cùng loại và đăng ký route khác nhau cho
  từng cái
- **when** hệ thống phân tích
- **then** route của mỗi application được gắn đúng application đó, không bị trộn sang
  application còn lại
- `validated_by:` TEST-L3GEN-002-09

### AC-L3GEN-002-10 — Registration có điều kiện

- **given** một route chỉ được đăng ký bên trong một nhánh điều kiện
- **when** hệ thống phân tích
- **then** route được ghi kèm điều kiện đó, và không được mô tả như luôn tồn tại trong
  mọi môi trường
- `validated_by:` TEST-L3GEN-002-10

### AC-L3GEN-002-11 — File lỗi cú pháp không làm hỏng cả lần phân tích

- **given** một repository có một hoặc vài file lỗi cú pháp
- **when** hệ thống phân tích
- **then** hệ thống ghi lỗi của từng file đó, tiếp tục phân tích phần còn lại, và trả
  kết quả partial kèm lý do
- `constrained_by:` NFR-L3GEN-REL-001
- `validated_by:` TEST-L3GEN-002-11

### AC-L3GEN-002-12 — Chạm giới hạn tài nguyên

- **given** một repository lớn hơn giới hạn xử lý đã công bố
- **when** hệ thống phân tích
- **then** hệ thống trả kết quả partial kèm giới hạn đã chạm, thay vì cắt dữ liệu trong
  im lặng hoặc dừng không giải thích
- `constrained_by:` NFR-L3GEN-PERF-001, NFR-L3GEN-REL-001
- `validated_by:` TEST-L3GEN-002-12

### AC-L3GEN-002-13 — Không có thành phần nào được tìm thấy

- **given** một repository không có file nào thuộc stack được hỗ trợ
- **when** hệ thống phân tích
- **then** kết quả trả về phạm vi đã đọc và lý do, và không khẳng định repository không
  có kiến trúc
- `validated_by:` TEST-L3GEN-002-13

### AC-L3GEN-002-14 — AI không ảnh hưởng dữ kiện kiến trúc

- **given** cùng một repository được phân tích hai lần, một lần có AI và một lần không
- **when** so sánh kết quả hai lần chạy
- **then** mô hình kiến trúc, quan hệ và evidence giống nhau; chỉ phần mô tả bằng lời
  do AI sinh là khác hoặc thiếu
- `validated_by:` TEST-L3GEN-002-14

### AC-L3GEN-002-15 — Kết quả ổn định giữa hai lần chạy

- **given** cùng một source và cùng cấu hình
- **when** hệ thống phân tích hai lần
- **then** mô hình kiến trúc và các artifact dữ liệu sinh ra giống nhau giữa hai lần
- `validated_by:` TEST-L3GEN-002-15
