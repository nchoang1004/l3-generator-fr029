---
uid: 01M2MV1DYD64EZ4X9GBDTHKWYN
key: NFR-L3GEN-REL-001
type: non-functional-requirement
group: normative
scope: system
system: SYS-L3GEN
status: draft
revision: 1
category: reliability
ownership:
  accountable_team: TEAM-L3GEN
  accountable_role: tech-lead
relations:
  constrains: [FR-L3GEN-002, FR-L3GEN-004, FR-L3GEN-005]
verified_at: 2026-09-16
verified_against: []
classification: internal
ai_assisted: true
---

# NFR-L3GEN-REL-001 — Suy giảm dần thay vì hỏng toàn bộ

## Mục đích

Repository thật luôn có phần hệ thống chưa đọc được: file lỗi cú pháp, ngôn ngữ chưa hỗ
trợ, cấu trúc phụ thuộc runtime. Yêu cầu này bảo đảm một phần hỏng không làm mất toàn
bộ kết quả, và người dùng luôn biết mình đang cầm kết quả đầy đủ hay một phần.

## Yêu cầu

### 1. Lỗi cục bộ không lan ra toàn lần chạy

| Tình huống | Hành vi bắt buộc |
|---|---|
| Một file lỗi cú pháp | Ghi lỗi của file đó, tiếp tục các file còn lại |
| Một ngôn ngữ chưa có bộ phân tích | Vẫn kiểm kê file, đánh dấu chưa hỗ trợ, tiếp tục ngôn ngữ khác |
| Một adapter framework không khớp | Bỏ qua phần đó, giữ các quan hệ đã xác định được |
| Chạm giới hạn xử lý | Trả kết quả partial kèm giới hạn đã chạm |
| Một artifact xuất ra thất bại | Giữ kết quả phân tích, báo artifact thất bại, cho thử lại |

### 2. Trạng thái kết quả rõ ràng

Mỗi lần phân tích kết thúc ở một trong các trạng thái: hoàn thành, hoàn thành một phần,
hoặc thất bại. Trạng thái một phần phải kèm lý do cụ thể, không được trình bày như
hoàn thành.

### 3. Thất bại phải nói được nguyên nhân

Khi không thể tiếp tục, hệ thống đưa ra thông báo ngắn gọn cho biết hỏng ở đâu và cần
làm gì, không đổ toàn bộ dấu vết lỗi kỹ thuật cho người dùng cuối.

### 4. Không tạo dữ liệu giả để lấp chỗ trống

Phần thiếu phải được ghi là thiếu. Cấm suy đoán một quan hệ, một tên bảng hoặc một đích
gọi chỉ để kết quả trông liền mạch.

## Điều kiện chấp nhận

- Có fixture chứa file lỗi cú pháp; lần chạy vẫn hoàn thành và trả kết quả partial.
- Có fixture trộn ngôn ngữ chưa hỗ trợ; phần được hỗ trợ vẫn cho kết quả.
- Có test cho trường hợp chạm giới hạn xử lý, kết quả là partial có lý do.
- Có test cho trường hợp một artifact xuất ra thất bại, kết quả phân tích không mất.

## Việc còn lại

Contract lỗi và trạng thái kết quả mới ở mức mô tả. Cần chốt danh sách mã lỗi và cách
hiển thị khi thiết kế L2.
