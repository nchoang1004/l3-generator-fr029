# DIARY-TASK-L3GEN-029-5

## Diễn giải
02/10/2026 — Đọc response danh sách model, theo phạm vi Hoàng đã giao.

## Đi chệch
Thêm add_api_websocket_route theo bàn giao. Chỉ lọc file test cho route/HTTP. Bản plan r1 bị lỗi encoding, có r2 đính chính.

## Đánh đổi
Không gọi mạng hoặc chạy source đầu vào. Header/credential trong call_text được redacted. Để nguyên test gateway lỗi sẵn theo quyết định người dùng.

## Kiểm chứng
Test `test_array_response_decorator_and_annotation` và các log ở ket-qua-chay/fr029-20261002. Đây là kiểm tự động của người triển khai, chưa là review độc lập.

## Câu hỏi mở
AC-029-04 và AC-029-07 còn chờ tích hợp; chưa chốt component hoặc Gate.
