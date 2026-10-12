Bạn là người chấm độc lập cho công cụ sinh tài liệu API (FR-029). KHÔNG sửa file nào.
KHÔNG đọc: thư mục .aide/ của repo D:/VSF/l3-generator-golden-v2 (chứa đáp án), file *.score.json, summary.json, thư mục D:/VSF/l3-generator-l3/slice/l3slice/, các file review khác.
Yêu cầu: D:/VSF/l3-generator-l3/.aide/requirements/fr/FR-L3GEN-029.md (8 AC; bảng vai trò file; bảng HTTP; mục "Khi chưa đủ dữ kiện") và mục "Phạm vi đọc" của D:/VSF/l3-generator-l3/.aide/requirements/fr/FR-L3GEN-028.md.

Repo thật: {repo}
Source: {source}
Tài liệu công cụ sinh: {output} (README.md, tech-specs/**/*.md, result.json).

Repo lớn, nên CHỈ kiểm đúng mẫu sau (mọi người chấm kiểm cùng mẫu). Với mỗi mục: tự đọc source liên quan (lần theo import, include_router, Depends, model) rồi so với tài liệu.
{sample}

Với route: method, path đầy đủ (thứ tự prefix), tham số (tên/vị trí/kiểu/required), request body, response model (mảng hay không), status, dependency. Với file: vai trò theo thứ tự FR-029 và dòng bằng chứng. Với lời gọi HTTP: method, đích, có phải HTTP thật không. Ngoài mẫu, nếu thấy route rõ ràng bị THIẾU trong cùng file với route mẫu thì báo kind "route", field "missing".

KHÔNG báo: thiếu sơ đồ component, thiếu archdia.json, ràng buộc giá trị (maximum/minimum), status của HTTPException ném trong thân hàm.

Trả lời DUY NHẤT một khối JSON:
```json
{"reviewer": "<tên model của bạn>", "repo": "{repo}",
 "checked": {"routes": n, "files": n, "http_calls": n},
 "errors": [{"fixture": "{repo}", "kind": "route|model|http|role|limitation|label|other", "item": "...", "field": "...",
             "doc_value": "...", "correct_value": "...", "evidence": "file:dòng", "confidence": "chắc|chưa chắc"}]}
```
