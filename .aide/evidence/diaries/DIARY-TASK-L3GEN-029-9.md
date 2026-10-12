# DIARY-TASK-L3GEN-029-9

Ghi muộn ngày 09/10/2026; phần chung của cả đợt (CR ghi muộn, không có plan trước, đề bài review có ghi chú tác giả) ở `DIARY-CR-L3GEN-2026-008.md`, mục "Phiên 07/10 tối – 09/10/2026". Dưới đây chỉ ghi phần riêng của task này.

## Diễn giải
- "Không test gian dối" hiểu thành: gold lập độc lập; mutation; bộ kiểm giả "luôn nhận/luôn từ chối"; repo held-out chọn theo thứ tự kết quả tìm kiếm; giám khảo held-out không đọc code bộ kiểm; báo cả số xấu.

## Đi chệch
- Sửa công cụ đo cùng đợt với bộ kiểm (phép đo prefix, cách xuất gói, lọc file đọc alias). Rủi ro "sửa thước cho vừa"; công cụ đo chưa có review riêng.
- Gói held-out gom tham số theo tên dependency nên giám khảo chấm "sai" 4 mục mà bộ kiểm thật làm đúng; đã sửa cách xuất gói.

## Đánh đổi
- Prefix đo bằng path gold trừ literal của decorator, đọc bằng cây cú pháp riêng của công cụ đo; route khai trên chính app thì bỏ qua.
- Phép đo "dòng có 2 lời gọi, nộp thiếu 1" không có mẫu trong gold (0 dòng): ghi not_run, chỉ có unit test.

## Câu hỏi mở
- Gold 4 repo mới (`D:/VSF/l3-heldout-gold2/`) do 2 agent viết, chưa có người duyệt.
