# PLAN-TASK-L3GEN-029-7 — r1

Lập ngày 09/10/2026. Chưa phải approval hoặc nghiệm thu độc lập.

File này ghi (1) thứ tự đã làm, (2) việc còn lại.

## 1. Thứ tự đã làm (07–09/10/2026)
Lặp theo từng vòng review:
1. Nhận phản ví dụ từ giám khảo (Codex hoặc agent Claude), hoặc từ chấm repo held-out.
2. RED: viết test tái hiện trong `slice/tests/test_checker_counterexamples.py`, chạy để thấy test đỏ.
3. GREEN: sửa `docfacts.py` / `astscan.py` (task 9: `fr029_checkaudit.py`).
4. Chạy toàn bộ test, gold audit, hai bộ kiểm giả, và so gói held-out trước/sau.
5. Hồi quy do chính bản sửa thì quay lại bước 2 cho hồi quy đó.

## 2. Việc còn lại (cam kết từ 09/10/2026)
1. Chờ OQ-L3GEN-018; nếu chọn ranh giới "không tạo mục", thêm test chặn → kiểm: test mới qua.
2. Giám khảo độc lập kiểm các bản sửa vòng 10 và đợt held-out 7 → kiểm: REVIEW mới, finding `fixed_unconfirmed` chuyển `fixed_confirmed` hoặc mở lại.
3. Đo lại cả sản phẩm bằng model trên 4 repository nghiệm thu → kiểm: NFR-ACC-002 trên từng repository.
4. Component Merge Gate: MR khai `implements: [CMP-L3GEN-007]`, `satisfies: [AC-L3GEN-029-02]` → kiểm: Tech Lead duyệt.

## 3. Không làm
- Không sửa FR, NFR, gold khi OQ chưa đóng.
- Không đổi prompt hay model trong task này.
- Không commit hay push khi người dùng chưa yêu cầu.
