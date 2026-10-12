Bạn là kiểm toán viên độc lập về phương pháp đo, vòng 6. Chỉ đọc, không sửa file trong repo. Mỗi kết luận có `file:dòng`. Có thể tự chạy thử bằng Python (đọc code, không sửa file repo; nếu cần file tạm, chỉ dùng thư mục tạm của hệ thống).

Vòng 5 (một phiên khác) đã nêu góp ý và 7 phản ví dụ, ở:
C:/Users/dell/AppData/Local/Temp/claude/d--VSF-l3-generator-l3/498cf361-d49d-460b-a09e-b56fd4418970/scratchpad/codex_fairness5_out.md

Tác giả đã sửa bộ kiểm (d:/VSF/l3-generator-l3/slice/l3slice/docfacts.py, astscan.py), thêm test (d:/VSF/l3-generator-l3/slice/tests/test_checker_counterexamples.py, lớp RoundFive và HeldOutFindings; công cụ đo thêm mutation bỏ prefix và bộ giả cho _registration_problems) và sửa công cụ đo (d:/VSF/l3-generator-l3/slice/tools/fr029_checkaudit.py). Kết quả mới: d:/VSF/l3-generator-l3/ket-qua-chay/fr029-checkaudit-20261008-r26/ (cùng 37 bộ gold như r20, thêm phép đo prefix), bộ kiểm giả ở r26-sanity-accept và r26-sanity-reject.

Không đọc docs/, HANDOFF, .aide/evidence/reviews/.

Việc:
1. Với từng phản ví dụ và từng mục "mot_phan"/"chua" của vòng 5: chạy lại hoặc đọc code để xác nhận "da_xu_ly"/"mot_phan"/"chua", kèm bằng chứng.
2. Tìm tối đa 8 phản ví dụ MỚI, ưu tiên dạng hay gặp trong repo FastAPI thật (không cố tìm dạng hiếm). Mỗi cái phải tự chạy tái hiện. Ghi "tan_suat_uoc": cao/vua/thap trong repo thật.
3. Mức tin cậy (cao/vua/thap) của bộ kiểm khi dùng cho repo FastAPI mới, tách theo: nhận diện route; kiểm HTTP claim; quét lời gọi HTTP bị sót; nhắc tham số dependency. Nêu lý do.

Đầu ra: tin nhắn cuối một khối ```json {"vong5": [{"muc","trang_thai","bang_chung"}], "phan_vi_du_moi": [{"loai","vi_du_code","hau_qua","tan_suat_uoc","da_tai_hien"}], "tin_cay": {"route": "...", "http_claim": "...", "http_suspects": "...", "dependency_params": "..."}, "ly_do": "..."} rồi tối đa 10 dòng tiếng Việt.

Ghi chú của tác giả về các mục "mot_phan" vòng 5 chưa sửa: các mục về công cụ đo (sanity chưa đi trọn add_route, mutation application/prefix/config_at/client_at, recall theo dòng) chưa sửa trong lượt này; hãy xác nhận lại trạng thái, không cần lặp lại chi tiết nếu không đổi.
