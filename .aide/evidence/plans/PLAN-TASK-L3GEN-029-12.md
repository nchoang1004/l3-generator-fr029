# PLAN-TASK-L3GEN-029-12 — r1

Ghi muộn ngày 12/10/2026: việc đã làm 11–12/10/2026 trước khi có Task (DIARY-CR-L3GEN-2026-009). Chưa phải approval hoặc nghiệm thu độc lập.

**Đây không phải plan viết trước khi code** (EXEC §B.14). Plan đó không tồn tại. File này ghi (1) thứ tự đã làm, (2) việc còn lại, cam kết từ 12/10/2026.

## 1. Thứ tự đã làm (11–12/10/2026)
1. Người dùng chọn cách A: viết `tailieu.py`, test `test_tai_lieu.py`.
2. Nghiên cứu tài liệu còn thiếu (`docs/FR029-tai-lieu-can-bo-sung-20261011.md`), đề xuất 5 đợt.
3. Người dùng: "làm đi". Làm 5 đợt; mỗi đợt test đỏ trước (`test_route_extras`, `test_static_parts`).
4. Test cả luồng bằng agent Claude đóng vai model (tdd-docker, Teamhide); sửa 3 lỗi bộ kiểm tìm được.
5. Held-out orderflow: đóng băng đầu ra, gold + giám khảo; sửa 4 lỗi.

## 2. Việc còn lại (cam kết từ 12/10/2026)
1. Người dùng chốt OQ-L3GEN-019, OQ-L3GEN-020 → kiểm: FR/CMP cập nhật qua CR, hoặc gỡ phần không duyệt.
2. Sửa FIND-L3GEN-179 ('&gt;'), FIND-L3GEN-180 (lặp 'Auth: chưa rõ', thuật ngữ nội bộ), FIND-L3GEN-183 (gateway chuyển tiếp) → kiểm: test.
3. Giám khảo chấm lại orderflow sau sửa → kiểm: REVIEW mới.

## 3. Không làm
- Không sửa FR, NFR, ADR, gold khi OQ chưa đóng.
- Không chạy model trả tiền khi người dùng chưa duyệt trần.
- Không commit hay push khi người dùng chưa yêu cầu.
