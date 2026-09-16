---
uid: 01M2MV1DYE1VPQFY5XRHSFBH9G
key: NFR-L3GEN-USA-001
type: non-functional-requirement
group: normative
scope: system
system: SYS-L3GEN
status: draft
revision: 1
category: usability
ownership:
  accountable_team: TEAM-L3GEN
  accountable_role: product-owner
relations:
  constrains: [FR-L3GEN-001, FR-L3GEN-003, FR-L3GEN-004]
verified_at: 2026-09-16
verified_against: []
classification: internal
ai_assisted: true
---

# NFR-L3GEN-USA-001 — Dùng được mà không cần người hướng dẫn

## Mục đích

Giá trị của sản phẩm nằm ở chỗ người dùng tự hiểu được kiến trúc. Nếu phải có người
trong nhóm phát triển ngồi cạnh giải thích thì công cụ chưa đạt mục tiêu.

## Yêu cầu

### 1. Hoàn thành luồng chính không cần hướng dẫn

Một kỹ sư chưa từng dùng công cụ phải tự đi được từ cung cấp mã nguồn tới xem kết quả
và xuất tài liệu, không cần tài liệu hướng dẫn riêng và không cần hỏi người phát triển.

### 2. Tổ chức theo mục tiêu người dùng

Giao diện tổ chức theo điều người dùng muốn biết, không theo các bước bên trong của
engine:

- nhìn tổng quan trước;
- đi sâu theo thành phần;
- truy vết về bằng chứng trong source;
- luôn thấy giới hạn của lần phân tích.

Mỗi màn hình có một hành động chính rõ ràng.

### 3. Trạng thái kết quả đọc được bằng lời thường

Người dùng phải hiểu được kết quả là đầy đủ hay một phần, và phần nào chưa đọc được, mà
không cần biết từ chuyên môn của bộ phân tích. Thuật ngữ bắt buộc phải dùng thì giải
thích ngay tại chỗ.

### 4. Trạng thái rỗng, đang tải và lỗi đều có nội dung

Không để màn hình trống không giải thích. Ba trạng thái này phải nói được chuyện gì
đang xảy ra và người dùng làm gì tiếp.

### 5. Thông báo lỗi nói được cách sửa

Lỗi đầu vào phải chỉ ra sai ở đâu và sửa thế nào, thay vì chỉ báo thao tác thất bại.

## Cách đo

Đo bằng pilot: người tham gia chưa từng dùng công cụ, tự thực hiện luồng chính, người
quan sát không được gợi ý. Ghi lại tỷ lệ hoàn thành và những chỗ người dùng mắc kẹt.

Ngưỡng mục tiêu của KPI-L3GEN-001 nằm trong PRD và còn chờ chốt theo OQ-L3GEN-003.

## Điều kiện chấp nhận

- Người dùng pilot hoàn thành luồng chính mà không cần nhóm phát triển hướng dẫn.
- Mọi màn hình kết quả đều hiển thị được phần giới hạn của lần phân tích.
- Mọi thông báo lỗi đầu vào đều nêu được hành động sửa.

## Việc còn lại

Chưa chạy pilot usability. Ngưỡng định lượng chờ OQ-L3GEN-003.
