- **route** — `API-PARAMS-MODELS-MAT-HANG-v1.md:25,308`, `result.json` GET `/items`: `q` ghi `string` → đúng là `string | null`; căn cứ `app/deps.py:11`, `app/routes.py:14`.
- **route** — API:28,479, `result.json` GET `/items/{item_id}`: `x-token` ghi `string` → đúng là `string | null`; căn cứ `app/routes.py:22`.
- **route** — API:34,787, `result.json` POST `/uploads`: `file` ghi `string`, thiếu định dạng → đúng là `UploadFile`, OpenAPI `type: string, format: binary`; căn cứ `app/routes.py:53`, [FastAPI 0.115.6](https://github.com/fastapi/fastapi/blob/0.115.6/fastapi/datastructures.py).
- **route** — API:25, `result.json` GET `/items`: chỉ ghi Auth `unknown`, thiếu dependency → phải ghi `Depends(search_filter)` và dependency lồng `Depends(pagination)`; căn cứ `app/routes.py:14`, `app/deps.py:12`.
- **route** — API:26, `result.json` POST `/items`: chỉ ghi Auth `unknown`, thiếu dependency → phải ghi `Depends(tenant)`; căn cứ `app/routes.py:33`.
- **label** — API:27, `result.json` fact `a442e2a1`: status 204 ghi `inferred/fastapi.status_constant` → phải là `exact`, vì source khai rõ hằng status, không dùng mặc định; căn cứ `app/routes.py:3,47`.
- **label** — API:60: `ItemCreate` ghi `inferred` nhưng không nêu quy tắc → cần kèm `pydantic.v2_required_no_default` như trong `result.json`; căn cứ `app/schemas/items.py:14`, `requirements.txt:2`.
- **label** — `README.md:27`: vai trò `app/deps.py` ghi `Khác` nhưng thiếu nhãn → phải ghi `Khác (exact)`; căn cứ `app/deps.py:6–18`, không có đường gọi tới truy cập dữ liệu/hạ tầng.

Đã kiểm: **11 route, 5 model, 0 lời gọi HTTP, 8 file nguồn và 3 file đầu ra; 8 lỗi.**