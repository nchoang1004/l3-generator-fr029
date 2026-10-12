# DIARY-TASK-L3GEN-029-7

Lập ngày 09/10/2026; phần chung của cả đợt ở `DIARY-CR-L3GEN-2026-008.md`, mục "Phiên 07/10 tối – 09/10/2026". Dưới đây chỉ ghi phần riêng của task này.

## Diễn giải
- Tham số "do dependency khai" theo đúng cách FastAPI đọc chữ ký: class thì đọc `__init__`, instance thì `__call__`, `partial` bỏ tham số vị trí đã gán nhưng giữ tham số từ khóa, model Pydantic dùng `Depends()` thì các trường đơn là query. Giám khảo kiểm bằng FastAPI 0.115.6 thật.

## Đi chệch
- Thêm lời nhắc mới "route dùng Depends(x) mà agent chưa khai", gồm cả dependency cấp router/app. Đây là hành vi mới agent phải sửa theo; chưa có AC riêng.
- 2 test (`album_id` là path, factory gọi trong alias) qua ngay từ đầu: test khóa hành vi đúng sẵn có, không phải RED-first.

## Đánh đổi
- `alias_generator` không biết (ngoài `to_camel`, `to_pascal`, `to_snake`) thì không nhắc trường nào, thay vì đoán tên.
- Dependency truyền qua alias chỉ nhắc khi tìm được đúng alias: định nghĩa ở file đó, import trực tiếp, hoặc cả snapshot chỉ có một định nghĩa.

## Câu hỏi mở
- OQ-L3GEN-018: lời nhắc ngày càng sâu; còn đúng hướng agent thuần không.
