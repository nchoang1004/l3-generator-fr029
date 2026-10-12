Bạn là kiểm toán viên độc lập về phương pháp đo, vòng 2. Chỉ đọc, không sửa file. Mỗi kết luận có `file:dòng`.

Vòng trước bạn (một phiên khác) đã đưa ra góp ý cho bộ kiểm và công cụ đo; góp ý nằm ở:
C:/Users/dell/AppData/Local/Temp/claude/d--VSF-l3-generator-l3/498cf361-d49d-460b-a09e-b56fd4418970/scratchpad/codex_fairness_out.md

Từ đó tác giả đã sửa:
- Bộ kiểm: d:/VSF/l3-generator-l3/slice/l3slice/docfacts.py và module mới d:/VSF/l3-generator-l3/slice/l3slice/astscan.py.
- Test phản ví dụ: d:/VSF/l3-generator-l3/slice/tests/test_checker_counterexamples.py.
- Công cụ đo: d:/VSF/l3-generator-l3/slice/tools/fr029_checkaudit.py. Kết quả: d:/VSF/l3-generator-l3/ket-qua-chay/fr029-checkaudit-20261008-r11/ (bộ kiểm thật) và ...-r8-accept, ...-r8-reject (bộ kiểm giả luôn nhận/luôn từ chối).

Không đọc docs/, HANDOFF, .aide/evidence/reviews/.

Câu hỏi:
1. Với TỪNG góp ý vòng trước (vong_tron, mutation_yeu, overfit, http_bo_sot): đã xử lý thật chưa? Trả lời "da_xu_ly" / "mot_phan" / "chua" kèm bằng chứng file:dòng (code sửa hoặc test). Không nhận lời tác giả; tự đọc code.
2. Phép đo hiện tại còn chỗ nào vòng tròn, mutation yếu, hoặc chỉ số luôn đạt? Bộ kiểm giả có thực sự chứng minh phép đo phân biệt được không?
3. Tìm phản ví dụ MỚI (code FastAPI cụ thể) làm bộ kiểm hiện tại sai: nhận nhầm, từ chối nhầm, nhắc sai/thiếu tham số, bỏ sót lời gọi httpx/requests/aiohttp ngoài thư mục test. Ưu tiên dạng hay gặp trong repo thật.
4. Đánh giá chung: mức tin cậy của các số 0 lỗi trong r11 (cao/vừa/thấp) và vì sao.

Đầu ra: tin nhắn cuối một khối ```json {"gop_y_cu": [{"gop_y","trang_thai","bang_chung"}], "con_lai": [...], "phan_vi_du_moi": [{"loai","vi_du_code","hau_qua","muc_do"}], "muc_tin_cay": "...", "ly_do": "..."} rồi tối đa 10 dòng tiếng Việt.
