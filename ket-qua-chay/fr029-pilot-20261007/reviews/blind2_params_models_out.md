- **route** — API, OpenAPI dòng 319; `result.json`, GET `/items`: `q` ghi `string` → đúng là `string | null`, không bắt buộc. Căn cứ `app/deps.py:11`.
- **route** — API, OpenAPI dòng 495; `result.json`, GET `/items/{item_id}`: `x-token` ghi `string` → đúng là `string | null`, không bắt buộc. Căn cứ `app/routes.py:22`.
- **route** — API, OpenAPI tham số `limit` của GET `/items`; `result.json`: ghi `integer` không giới hạn → phải có `maximum: 100`. Căn cứ `app/deps.py:6`.
- **route** — API dòng 34, 808–810; `result.json`, POST `/uploads`: `file` ghi `string` → đúng là `UploadFile`, OpenAPI `type: string, format: binary`. Căn cứ `app/routes.py:53`; [FastAPI 0.115.6](https://raw.githubusercontent.com/fastapi/fastapi/0.115.6/fastapi/datastructures.py).
- **model** — API dòng 82: ghi `Tag (request)` → phải ghi cả request và response, vì `ItemPublic.tags` trả về `list[Tag]`. Căn cứ `app/schemas/items.py:24`, `app/routes.py:13`, `app/routes.py:43`.
- **limitation** — `README.md:15`: ghi “Chưa được cấp sơ đồ” → vẫn thiếu sơ đồ component bắt buộc theo AC-029-06, dù đã công bố giới hạn. Căn cứ cấu trúc ứng dụng `app/main.py:5–6` và component đầu vào trong `params_models.membership.json`.

Đã kiểm: **11 route, 5 model, 0 lời gọi HTTP, 8 file source/manifest và 3 file đầu ra; 6 lỗi.**