# PLAN-TASK-L3GEN-031-1 — r1

Ghi muộn ngày 12/10/2026: việc đã làm 11–12/10/2026 trước khi có Task (DIARY-CR-L3GEN-2026-009). Chưa phải approval hoặc nghiệm thu độc lập.

**Đây không phải plan viết trước khi code** (EXEC §B.14). Plan đó không tồn tại. File này ghi (1) thứ tự đã làm, (2) việc còn lại, cam kết từ 12/10/2026.

## 1. Thứ tự đã làm (11–12/10/2026)
1. RED: `test_events_tasks.py` (Celery, BackgroundTasks).
2. GREEN: `_task_events`, `_celery_point`, `_background_target` trong `extract.py`; bỏ Celery khỏi danh sách thư viện chưa hỗ trợ.
3. Held-out orderflow: giám khảo tìm Redis pub/sub bị sót → thêm cảnh báo (test `UnsupportedBus`).

## 2. Việc còn lại (cam kết từ 12/10/2026)
1. Đọc bus tự viết (Redis pub/sub) hay để agent đề xuất: chờ người quyết (OQ-L3GEN-019).
2. Gold sự kiện cho ít nhất 1 repo có Celery → kiểm: điểm gửi/nhận khớp.
3. AC-L3GEN-031-04 (archdia.json): hoãn theo người dùng.

## 3. Không làm
- Không sửa FR, NFR, ADR, gold khi OQ chưa đóng.
- Không chạy model trả tiền khi người dùng chưa duyệt trần.
- Không commit hay push khi người dùng chưa yêu cầu.
