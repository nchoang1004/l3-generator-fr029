# Chạy thật qua giao diện, 12/10/2026

Hai lần chạy `docweb` với model thật `gpt-5-2025-08-07`, chế độ đọc một lần, effort low. Khóa API nằm ở biến môi trường, không có trong thư mục này.

| Thư mục | Repo | Kết quả | Request | Chi phí tính từ `result.json` |
|---|---|---|---|---|
| `tdd-docker-hoan-tat` | tdd-docker (6 file đọc) | agent `completed` | 2 | khoảng 0,077 USD |
| `nsidnev-realworld-chua-day-du` | nsidnev/fastapi-realworld (71 file đọc) | agent `partial`, `REPAIR_ROUNDS`; 14 route, 12 model; 57 lần nộp bị từ chối, 13 vấn đề còn mở | 3 | 0,462 USD |

Lần nsidnev vượt trần dừng 0,35 USD đã đặt, vì trần chỉ chặn request kế tiếp; request thứ 3 bắt đầu khi mới tốn 0,326 USD.

Chưa làm: so kết quả nsidnev với gold; chưa phân loại 57 lần từ chối thành lỗi model hay bộ kiểm quá chặt (ví dụ `tags` dẫn dòng `api.py:12`).

`drive.py` gọi API của giao diện. Các file `*.checkpoint.json` là tiến độ của chế độ đọc một lần.
