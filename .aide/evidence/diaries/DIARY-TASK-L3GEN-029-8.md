# DIARY-TASK-L3GEN-029-8

Lập ngày 09/10/2026; phần chung của cả đợt ở `DIARY-CR-L3GEN-2026-008.md`, mục "Phiên 07/10 tối – 09/10/2026". Dưới đây chỉ ghi phần riêng của task này.

## Diễn giải
- "Lời gọi HTTP ra ngoài" hiểu là lời gọi trực tiếp httpx/requests/aiohttp, kể cả `super().request` trong lớp con client và method client truyền làm đối số (`to_thread(c.get, url)`).

## Đi chệch
- Ba lần sửa gây nhiễu mới, đều bị bắt khi so gói held-out: luật "đối số là client" (primer +32 dòng), `from . import requests` (PrintStash), chuỗi `.requests.` (shortlist).

## Đánh đổi
- Dòng nghi ngờ dễ dãi (đoán theo tên `session`, `client`) để ít bỏ sót; kiểm claim chặt (tên hàm tự gán cho thứ không rõ thì không mượn client cùng tên ở hàm khác).
- Lời gọi không viết trực tiếp được dựng lại thành "lời gọi ảo" tại dòng đó; `partial(c.get, url)` không tính vì chưa gửi request.
- Chưa xử lý: `self.runtime.session.post`, dict chứa client tra bằng `.get`, `super().send` của HTTPAdapter.

## Câu hỏi mở
- OQ-L3GEN-016 (hàm bọc), OQ-L3GEN-017 (`scripts/` chỉ import helper).
