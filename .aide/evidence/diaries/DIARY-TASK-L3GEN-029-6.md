# DIARY-TASK-L3GEN-029-6

Ghi muộn ngày 09/10/2026; phần chung của cả đợt (CR ghi muộn, không có plan trước, đề bài review có ghi chú tác giả) ở `DIARY-CR-L3GEN-2026-008.md`, mục "Phiên 07/10 tối – 09/10/2026". Dưới đây chỉ ghi phần riêng của task này.

## Diễn giải
- "Route đúng app" hiểu là router của decorator phải nằm dưới app được khai qua chuỗi `include_router`/`mount` trong snapshot. Prefix áp từ app vào tới router (`/api` của include trước `/v1` của `APIRouter(prefix=)`).
- Route khai trên chính app (`@app.get`) không có prefix router để kiểm.

## Đi chệch
- Kiểm đăng ký từ chối route khai thuộc app mà router không đăng ký vào app đó, trong khi OQ-L3GEN-013 còn mở. Đã ghi vào OQ-013 revision 2; code không đổi.
- Hai lần sửa gây lỗi mới, đều bị gold bắt: `include_router(router=...)` bị bỏ qua (phép đo prefix tìm ra), `self.app.include_router` làm router bị coi là chưa đăng ký.

## Đánh đổi
- Thứ tự `include_router` chỉ xét trong cùng file ở cấp module; khác file thì không kết luận.
- Helper nhận prefix qua tham số (`attach(app, router, prefix=...)`) thì coi đồ thị là mở, không kết luận.
- Đồ thị không giải được thì không từ chối: ưu tiên không từ chối nhầm.

## Câu hỏi mở
- OQ-L3GEN-013.
