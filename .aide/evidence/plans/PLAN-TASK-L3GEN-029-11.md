# PLAN-TASK-L3GEN-029-11 — r1

Lập ngày 12/10/2026. Chưa phải approval hoặc nghiệm thu độc lập.

File này ghi (1) thứ tự đã làm, (2) việc còn lại.

## 1. Thứ tự đã làm (11–12/10/2026)
1. Kiểm lại 8 ý của bản review Codex trên bản sao phép thử; cả 8 tái hiện được.
2. Người dùng duyệt sửa 1–8.
3. Mỗi ý: RED trong `test_review_20261011.py` → GREEN trong `docfacts.py`/`render.py`.
4. Chạy suite, `fr029_checkaudit`, đo trường model và Service trên gold (script scratchpad `measure_fields_service.py`).
5. Cập nhật prompt agent v16, oneshot v5.

## 2. Việc còn lại (cam kết từ 12/10/2026)
1. Đường gọi Service truyền qua tham số (1/16 gold) → kiểm: test mới hoặc ghi giới hạn trong CMP-L3GEN-007.
2. Giám khảo độc lập xác nhận 8 bản sửa → kiểm: REVIEW mới đổi `fixed_by_test` thành `fixed_confirmed`.

## 3. Không làm
- Không sửa FR, NFR, ADR, gold khi OQ chưa đóng.
- Không chạy model trả tiền khi người dùng chưa duyệt trần.
- Không commit hay push khi người dùng chưa yêu cầu.
