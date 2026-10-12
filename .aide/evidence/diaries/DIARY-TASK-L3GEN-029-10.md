# DIARY-TASK-L3GEN-029-10

Lập ngày 12/10/2026; phần chung của cả đợt ở `DIARY-CR-L3GEN-2026-009.md`.

## Diễn giải
- "Đỡ tốn token" hiểu là giảm số request, không phải giảm độ chính xác. So công bằng: cùng snapshot, cùng model với r3.
- "Schema" mới là khuôn mô tả trong prompt cộng `tool_choice`; chưa phải strict schema của API.

## Đi chệch
- Gửi nguyên source trong request đầu: trái NFR-SEC-002; waiver 07/10 không rõ có phủ (OQ-L3GEN-021).
- Runner chạy bằng Python gốc, thiếu `openapi-spec-validator` → file API FORMAT_INVALID ở một lượt gpt-5. Sửa bằng `slice/requirements.txt` và chạy bằng `sys.executable`.

## Đánh đổi
- gpt-4.1-mini rẻ (~0,03 USD) nhưng 0/5 route; gpt-5 đắt hơn ~6 lần nhưng 4–5/5 route.
- Vòng sửa chỉ gửi mục bị từ chối kèm dòng source: rẻ, nhưng model không thấy lại cả file.

## Câu hỏi mở
- OQ-L3GEN-020, OQ-L3GEN-021.
