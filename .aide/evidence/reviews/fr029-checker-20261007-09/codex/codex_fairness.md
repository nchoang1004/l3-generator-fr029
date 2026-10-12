Bạn là kiểm toán viên độc lập về phương pháp đo. Chỉ đọc, không sửa file. Mỗi kết luận phải có `file:dòng`.

## Đối tượng

Một bộ kiểm (checker) tự động trong công cụ sinh tài liệu API FastAPI: `d:/VSF/l3-generator-l3/slice/l3slice/docfacts.py` (lớp `Claims`: `_decorator_problems`, `add_http`, `_call_span`, `_url_argument`, `dependency_at`, `_alias_wraps`, `dependency_params`, `_factory_makes_app`, `suspects`, `_http_receivers`, `_string_rows`).

Công cụ đo độ chính xác của bộ kiểm: `d:/VSF/l3-generator-l3/slice/tools/fr029_checkaudit.py`. Kết quả qua 4 vòng: `d:/VSF/l3-generator-l3/ket-qua-chay/fr029-checkaudit-20261008-r{1,2,3,4}/summary.json` và `audit.json`. Đáp án dùng để so là các file gold độc lập (đường dẫn trong `fr029_cases()` và `v1_cases()` của công cụ đo). Giữa các vòng, bộ kiểm được sửa dựa trên lỗi tìm thấy ở chính các repo này.

Không đọc docs/, HANDOFF, .aide/evidence/reviews/ (để giữ độc lập).

## Câu hỏi

1. **Công bằng của phép đo:** công cụ đo có dùng output của chính bộ kiểm làm đáp án ở chỗ nào không (vòng tròn)? Phép "chấp nhận nhầm" (mutation) có đủ mạnh không, hay quá dễ (ví dụ chỉ đổi method sang một method chắc chắn không có)? Có phép đo nào luôn đạt bất kể bộ kiểm đúng hay sai?
2. **Khớp quá mức (overfitting):** các luật mới trong bộ kiểm (alias, factory, `Class.method`, tham số scalar của dependency, receiver của HTTP, bỏ dòng trong docstring, `CLIENT_NAME`) có chỗ nào chỉ đúng cho các repo đã dùng mà sẽ sai ở repo khác? Nêu ví dụ code FastAPI cụ thể làm nó sai (nhận nhầm, từ chối nhầm, nhắc sai tham số, bỏ sót lời gọi HTTP).
3. **Rủi ro bỏ sót HTTP:** `suspects` giờ chỉ đánh dấu `.get(` khi đối tượng gọi là client. Liệt kê các dạng lời gọi httpx/requests/aiohttp thật mà luật mới KHÔNG đánh dấu (để agent có thể bỏ qua mà không ai nhắc).
4. **Đề xuất:** các ca kiểm (mutation hoặc repo mẫu) nên thêm để phép đo đáng tin hơn.

## Đầu ra

Tin nhắn cuối: một khối ```json: {"vong_tron": [...], "mutation_yeu": [...], "overfit": [{"luat","vi_du_code","hau_qua","muc_do": "cao|vua|thap"}], "http_bo_sot": [{"dang","vi_du_code"}], "de_xuat": [...]} rồi tối đa 10 dòng tiếng Việt tóm tắt. Chỉ nêu điều đã kiểm bằng cách đọc code.
