- **route** — `tech-specs/DON-HANG/api/API-FILE-ROLES-DON-HANG-v1.md:25,181`, `result.json:1180`: GET `/orders/{order_id}` chỉ ghi **200**; đúng là **200 khi thành công, 404 khi không tìm thấy**. Căn cứ: `app/api/orders.py:18–19`.
- **limitation** — `README.md:16`: ghi “Chưa được cấp sơ đồ”, không có sơ đồ component; AC-029-06 yêu cầu có sơ đồ, ghi giới hạn chưa đáp ứng yêu cầu này. Căn cứ source: `app/main.py:5–7`, `app/api/orders.py:12`, `app/services.py:7`, `app/repository.py:9`.

Đã kiểm: **3 route, 2 model API, 0 lời gọi HTTP, 13 file nguồn và 4 file tài liệu; 2 lỗi.**