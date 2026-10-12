# PLAN-TASK-L3GEN-030-1 — r1

Ghi muộn ngày 12/10/2026: việc đã làm 11–12/10/2026 trước khi có Task (DIARY-CR-L3GEN-2026-009). Chưa phải approval hoặc nghiệm thu độc lập.

**Đây không phải plan viết trước khi code** (EXEC §B.14). Plan đó không tồn tại. File này ghi (1) thứ tự đã làm, (2) việc còn lại, cam kết từ 12/10/2026.

## 1. Thứ tự đã làm (11–12/10/2026)
1. Đo gold 4 repo bằng `measure_tables.py`; tìm crash IDENTITY_COLLISION, khóa chính qua alias, bảng extend_existing.
2. Đối chiếu từng mục FR-030 và API-008 §6 trên đầu ra thật.
3. RED/GREEN trong `test_tables_db.py` cho từng lỗi.
4. Giám khảo vòng 1 (đầu ra đóng băng) → sửa ràng buộc, migration.
5. Giám khảo vòng 2 (mới, không xem vòng 1) → sửa `sa_type`/`max_length`, khóa chính ghép.

## 2. Việc còn lại (cam kết từ 12/10/2026)
1. Chờ OQ-L3GEN-022 (dialect, ràng buộc trong TBL).
2. Giám khảo chấm lại sau hai bản sửa cuối → kiểm: REVIEW mới.
3. AC-L3GEN-030-05 (archdia.json): hoãn theo người dùng.

## 3. Không làm
- Không sửa FR, NFR, ADR, gold khi OQ chưa đóng.
- Không chạy model trả tiền khi người dùng chưa duyệt trần.
- Không commit hay push khi người dùng chưa yêu cầu.
