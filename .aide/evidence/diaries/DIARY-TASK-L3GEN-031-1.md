# DIARY-TASK-L3GEN-031-1

Lập ngày 12/10/2026; phần chung của cả đợt ở `DIARY-CR-L3GEN-2026-009.md`.

## Diễn giải
- Celery và BackgroundTasks đã có trong bảng "Phạm vi đọc" của FR-031, nên không phải mở rộng phạm vi.

## Đi chệch
- Redis pub/sub nằm ngoài bảng phạm vi: chỉ cảnh báo, đúng AC-L3GEN-031-03; giám khảo vẫn coi là thiếu.

## Đánh đổi
- Nối gửi↔nhận chỉ khi cùng hàm tác vụ hoặc cùng broker/topic, không nối theo tên.

## Câu hỏi mở
- OQ-L3GEN-019.
