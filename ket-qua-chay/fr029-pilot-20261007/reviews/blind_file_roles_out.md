- **route** — `API-FILE-ROLES-DON-HANG-v1.md:25,173`, `result.json:1112`: chỉ ghi status `200` → thiếu `404` khi không tìm thấy đơn hàng; căn cứ `app/api/orders.py:18–19`.
- **route** — Hai file API, bảng Endpoint; `result.json`, cả 3 route: chỉ ghi Auth `unknown`, bỏ dependency → phải ghi `db=Depends(get_db)`; căn cứ `app/api/orders.py:11,16`, `app/api/reports.py:11`.
- **label** — `README.md:31`: vai trò `Khác` của `service_utils.py` không có nhãn → phải ghi `exact` theo FR-029; căn cứ `app/service_utils.py:1–7` chỉ chứa hàm tiện ích, không có dấu hiệu vai trò khác.
- **role** — `README.md:23–49`: bằng chứng vai trò chỉ có `file:dòng` → thiếu nguyên văn dòng code theo định dạng bằng chứng FR-028; ví dụ phải kèm `engine = create_engine(DATABASE_URL)` tại `app/db.py:8`, `__tablename__ = "orders"` tại `app/models.py:10`.
- **model** — `API-FILE-ROLES-DON-HANG-v1.md:49–54`: mục Truy vết chỉ có route → thiếu dòng truy vết riêng với fact ID đầy đủ và vị trí cho `OrderIn`, `OrderOut`; căn cứ `app/schemas.py:4,9`.
- **limitation** — `README.md:16,66`: sơ đồ ghi “Chưa được cấp”, nhưng giới hạn ghi “(không có)” → thiếu sơ đồ bắt buộc theo AC-06 và chưa đưa thiếu hụt này vào phần giới hạn; source có app và hai router tại `app/main.py:5–7`.

Đã kiểm: **3 route, 2 model API, 0 lời gọi HTTP, 13 file nguồn và 4 file đầu ra; 6 lỗi.**