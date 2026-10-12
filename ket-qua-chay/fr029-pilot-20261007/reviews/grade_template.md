Bạn là người chấm độc lập cho công cụ sinh tài liệu API (FR-029). KHÔNG sửa file nào trong repo.
KHÔNG đọc: file *.gold.json, *.oracle.json, *.score.json, summary.*, thư mục slice/l3slice/, slice/tests/*.py, các file review khác. Phải đánh giá độc lập.

Yêu cầu: D:/VSF/l3-generator-l3/.aide/requirements/fr/FR-L3GEN-029.md (8 AC; bảng vai trò file; bảng HTTP; mục "Khi chưa đủ dữ kiện") và mục "Phạm vi đọc" của D:/VSF/l3-generator-l3/.aide/requirements/fr/FR-L3GEN-028.md.

Với MỖI fixture dưới đây: đọc toàn bộ source, rồi kiểm tài liệu công cụ sinh ra (README.md, tech-specs/**/*.md, result.json trong thư mục output).
{fixtures}

Kiểm: route (thiếu/thừa, method, path đầy đủ, tham số tên/vị trí/kiểu/required, request body, response model, status), model (trường, alias, kiểu, required, nullable theo đúng phiên bản Pydantic ghim trong manifest), lời gọi HTTP (httpx/requests/aiohttp: thiếu/thừa, method, đích), vai trò từng file theo thứ tự FR-029, giới hạn (add_api_route/add_route/add_websocket_route có file:dòng), nhãn exact/inferred/unknown.

KHÔNG báo các điều sau (đã biết, ngoài phạm vi tool): thiếu sơ đồ component và thiếu archdia.json (đầu vào từ bước khác); ràng buộc giá trị như maximum/minimum; status của HTTPException ném trong thân hàm.

Trả lời DUY NHẤT một khối JSON (không thêm chữ ngoài khối), dạng:
```json
{"reviewer": "<tên model của bạn>",
 "checked": {"<fixture>": {"routes": n, "models": n, "http_calls": n, "files": n}},
 "errors": [{"fixture": "...", "kind": "route|model|http|role|limitation|label|other",
             "item": "định danh ngắn, ví dụ 'GET /items/{item_id}' hoặc 'app/db.py' hoặc 'Item.price'",
             "field": "trường sai, ví dụ path|params|required|nullable|role|target|missing|extra",
             "doc_value": "tài liệu ghi gì", "correct_value": "đúng là gì",
             "evidence": "file:dòng trong source", "confidence": "chắc|chưa chắc"}]}
```
Nếu một fixture không có lỗi thì không có mục nào của fixture đó trong errors.
