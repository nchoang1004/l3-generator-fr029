# DIARY-TASK-L3GEN-029-12

Ghi muộn ngày 12/10/2026; phần chung của cả đợt ở `DIARY-CR-L3GEN-2026-009.md`.

## Diễn giải
- "Đầu ra chỉ được ghi rõ trong 1 file, dễ đọc" → thêm `TAI-LIEU.md`, giữ các file máy đọc theo FR-029 (cách A).
- "Làm đi" sau bản nghiên cứu → làm cả 5 đợt đề xuất. Claude tự chọn đọc tĩnh cho phần không phải API; chưa hỏi lại.

## Đi chệch
- Thêm phần ngoài spec (errors, tags, summary, examples, thư viện, cấu hình, middleware, quan hệ component) mà chưa có CR: OQ-L3GEN-020.
- Test end-to-end cũ cấm gọi `extract.extract` đã được nới cho phần đọc tĩnh; test `test_api_facts_come_only_from_the_agent` giữ ranh giới cho API.

## Đánh đổi
- Đọc tĩnh: không tốn token, đo được với gold; nhưng khác hướng "agent thuần" (OQ-L3GEN-019).
- Agent Claude đóng vai model thay model thật: gần như không tốn tiền, nhưng không đo được model sẽ dùng.

## Câu hỏi mở
- OQ-L3GEN-019, OQ-L3GEN-020.
