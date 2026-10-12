# Kiểm chéo bộ chấm FR-029 — 07/10/2026

Loại: đánh giá tư vấn, chưa là Gate approval hoặc finding ID chính thức.

Người dùng yêu cầu dùng nhiều session để kiểm công bằng. Hai agent `scorer_review_a` và `scorer_review_b` được tạo với ngữ cảnh trống, cùng yêu cầu đọc FR-029/NFR-ACC/OBS và bốn script scorer/accept/golden4/grade_merge. Không gửi kết luận của phiên chính, không đọc review của nhau. Cả hai chỉ chạy dữ liệu giả, không đọc source/gold/output chi tiết repo kín và không gọi model ngoài. Không tuyên bố đây là kiểm chéo nhiều hãng hay người độc lập.

## Kết quả reviewer A

1. `fr029_score.py:158,195,197`: unknown khớp unknown được tính correct; model dynamic rỗng được chấp nhận qua `all([])`. Tái hiện offline. Cần tách đúng thông tin đã biết và unknown được chấp nhận; OBS không cho tính unknown là đã giải đúng.
2. `fr029_score.py:181`, `fr029_accept.py:61`: alias đổi khóa ở scorer nhưng exact dùng khóa gốc; method sai thành exact_wrong 0/1. Tái hiện offline.
3. `fr029_score.py:177`, `fr029_accept.py:57`: thiếu gold HTTP vẫn đưa HTTP exact vào mẫu số, trả 0% sai. Tái hiện offline.
4. `fr029_score.py:148`: array một chiều và hai chiều chuẩn hóa thành cùng tuple, response sai vẫn correct. Tái hiện offline.
5. `fr029_accept.py:119`: runner ghi số đo nhưng không tính verdict theo ngưỡng; nhánh golden-v1 thiếu model P/R và exact. Xác nhận bằng đọc code, không chạy CLI trên repo kín.
6. `fr029_grade_merge.py:28`: cắt field tới đoạn đầu nên hai lỗi con khác nhau ở cùng dòng thành đồng thuận. Tái hiện offline.

Reviewer A chạy test Scorer hiện có: 1/1 qua. Không sửa file dự án.

## Kết quả reviewer B

1. Alias làm exact mất lỗi: cùng ca sai method, canonical cho 1/1 sai còn alias cho 0/1. Tái hiện offline.
2. `fr029_score.py:180`, `fr029_accept.py:59`: hai fact cùng key, một đúng một sai; đổi thứ tự làm exact sai từ 0/2 thành 2/2. Sự tồn tại vẫn TP=1, FP=0. Tái hiện synthetic; chưa chứng minh mọi đường pipeline thực tế đều sinh duplicate.
3. Thiếu gold được xử lý không nhất quán: HTTP not_evaluated nhưng exact 0% sai; model thiếu mục gold bị tính FP. Tái hiện offline.
4. Unknown method/URL và model dynamic không có fields bị tính correct. Cần tách chấp nhận giới hạn và giải đúng giá trị. Tái hiện offline.
5. `fr029_score.py:67`, `fr029_golden4.py:57`: route sai handler có TP=1 theo format FR029 nhưng TP=0/FP=1/FN=1 theo golden-v1. Nhánh golden chỉ kiểm vị trí HTTP và tên model trên route khớp. Tái hiện offline.
6. Grade merge có thể gộp lỗi khác field hoặc cách sửa mâu thuẫn. Giữ full field path/item và phân biệt cùng vị trí với đồng ý kết luận. Tái hiện offline.

Reviewer B chạy test Scorer hiện có: 1/1 qua. Không sửa file dự án. Thử cùng facts với completed/partial/failed cho cùng điểm; bản thân chấm facts không phụ thuộc run status không phải lỗi. Không lấy run status hay exit 0 thay nghiệm thu.

## Đối chiếu của phiên chính

- Hai reviewer đồng ý về alias–exact, mẫu số thiếu gold, unknown và merge đồng thuận giả. Đây là đồng ý về từng cơ chế lỗi cụ thể, không dùng script merge đang bị kiểm để gộp.
- Phiên chính tái hiện alias, duplicate đảo thứ tự, thiếu gold trong exact, mất chiều mảng, model dynamic rỗng và key merge khác field. Script ở `../tests/fr029-review-20261007/reproduce.py` và `reproduce_scorer.py`.
- Chấp nhận đề xuất phân biệt `correct_known`, `acceptable_unknown`, `wrong`, `not_evaluated`. Không buộc tool đoán giá trị chỉ biết lúc chạy để tránh mất điểm.
- Không suy ra mức ảnh hưởng chính xác tới 18%/56% đã công bố; cần chấm lại output bằng scorer sửa xong, chỉ xuất số tổng và giữ phép đo cũ.
- Chưa sửa scorer, prompt, gold, spec hay số đo cũ.
