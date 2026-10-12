# PLAN-TASK-L3GEN-029-10 — r1

Lập ngày 12/10/2026. Chưa phải approval hoặc nghiệm thu độc lập.

File này ghi (1) thứ tự đã làm, (2) việc còn lại.

## 1. Thứ tự đã làm (11–12/10/2026)
1. Đo r3 cũ: 67 request, 0,218 USD; tìm nguyên nhân tốn (nhiều lượt, ngữ cảnh lặp).
2. RED: lớp `OneShot` trong `test_docagent.py` (mock provider).
3. GREEN: `run_oneshot`, `tool_choice`, vòng sửa kèm dòng source, checkpoint.
4. Chạy thật gpt-4.1-mini (trần 0,20 USD) → 0/5 route; đổi prompt v1→v3.
5. Chạy thật gpt-5 (trần 0,30 USD) → 4–5/5 route; tìm 2 lỗi bộ kiểm (chuyển sang TASK-L3GEN-029-11).

## 2. Việc còn lại (cam kết từ 12/10/2026)
1. Chạy thật prompt v6 trên Teamhide khi người dùng duyệt tiền → kiểm: `cost.json` ≤ trần, số route nhận.
2. Chế độ chia gói cho repo lớn (kibo) → kiểm: không còn `SOURCE_TOO_LARGE` trên kibo.
3. Giao diện web hỗ trợ chọn oneshot (TASK-L3GEN-029-13).

## 3. Không làm
- Không sửa FR, NFR, ADR, gold khi OQ chưa đóng.
- Không chạy model trả tiền khi người dùng chưa duyệt trần.
- Không commit hay push khi người dùng chưa yêu cầu.
