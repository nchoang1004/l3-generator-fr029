# Báo cáo giám khảo độc lập: orderflow-services

Ngày chấm: 12/10/2026. Đã đọc toàn bộ source Python, pyproject, requirements, .env.example, docker-compose, Dockerfile, ci.yml, README của repo, cùng output/TAI-LIEU.md và README. Không đọc file bị cấm. Không sửa file đầu ra.

Kiểm hash: 6 file trong output/ khớp 100% với hashes.txt (certutil SHA256).

Đường dẫn source tính từ gốc repo AlexGoster_orderflow-services.

## A. Chính xác

Tổng 213 mục kiểm: đúng 202, sai 9 (1 sự kiện, 8 vai trò file), không kiểm được 2.

| Nhóm | Kiểm | Đúng | Sai | Ghi chú |
|---|---|---|---|---|
| Endpoint (method, path đủ prefix, hàm, dòng, tham số khai báo, body, response, status, dependency, tags) | 23 | 23 | 0 | Khớp. /api/v1/orders ghép từ order_app/api/router.py:5 và orders.py:18. |
| Model: tên, dòng, trường (kiểu, bắt buộc, null) | 47 | 47 | 0 | Khớp shared/contracts.py:33-109. |
| Bảng CSDL: tên, dòng, cột (kiểu, PK, FK, null) | 31 | 31 | 0 | Khớp 3 file models.py. |
| Sự kiện, tác vụ nền | 1 | 0 | 1 | Xem B1. |
| Lời gọi HTTP ra ngoài | 2 | 2 | 0 | gateway_app/core/proxy.py:25; order_app/core/catalog_client.py:98. Nhãn "chưa rõ" cho proxy đúng. |
| Thư viện | 26 | 26 | 0 | Dòng khớp pyproject và requirements. |
| Cấu hình | 18 | 18 | 0 | Khớp 4 file core/config.py. |
| Middleware, xử lý lỗi | 5 | 5 | 0 | shared/errors.py:34; bốn chỗ add_middleware. |
| Vai trò file | 54 | 46 | 8 | Xem dưới. |
| Số đếm đầu tài liệu | 4 | 4 | 0 | 54 file trong phạm vi + 3 file khai thư viện = 57. |
| "Sinh bởi", "18 lần nộp bị từ chối" | 2 | 0 | 0 | Không kiểm được: chỉ có trong result.json. |

Vai trò sai (8, đánh giá có phần chủ quan):
- 4 file api/router.py ghi "Khác"; chúng gắn router con vào prefix /api/v1 (catalog_app/api/router.py:5-6), nên là Route.
- shared/errors.py ghi "Khác"; đăng ký exception handler (errors.py:33), nên là Hạ tầng.
- shared/context.py ghi "Khác"; chứa middleware (context.py:29), nên là Hạ tầng.
- shared/logs.py ghi "Khác"; cấu hình log (logs.py:50), nên là Hạ tầng.
- order_app/core/resilience.py ghi "Khác"; là circuit breaker (resilience.py:23), nên là Hạ tầng hoặc Service.

Ghi chú khác:
- services/orders.py ghi "Truy cập dữ liệu" nhưng còn điều phối gọi catalog và phát sự kiện (orders.py:40, :95). Tính là đúng một phần.
- Vai trò "Service" có trong bảng chuẩn nhưng không dùng lần nào.
- Nhãn chắc chắn/suy luận/chưa rõ nhìn chung phù hợp, thiên về thận trọng (bảng CSDL đọc thẳng từ code vẫn ghi "suy luận").
- "Auth: chưa rõ" đúng câu chữ. Grep không thấy Security, HTTPBearer, jwt, OAuth, nên có thể nói thẳng "không có xác thực".
- "SQL dialect: chưa rõ" chấp nhận được vì docker-compose.yml:22 và .env.example:6 (postgresql+asyncpg) nằm ngoài phạm vi đọc.

## B. Đầy đủ: thiếu hoặc ghi sai

Đã quét độc lập: route, include_router, BaseModel, httpx/requests/aiohttp, __tablename__, kafka/faststream/celery/BackgroundTasks, BaseSettings/os.getenv, add_middleware/exception_handler, pyproject.

1. Sự kiện Redis pub/sub bị bỏ sót hoàn toàn (nghiêm trọng nhất). Đầu tài liệu ghi "Sự kiện: 0 điểm gửi/nhận"; mục 5 ghi "Không thấy điểm gửi/nhận". Thực tế:
   - Bên gửi: order_app/api/routes/orders.py:42 gọi services/orders.py:84-95, rồi bus.publish("order.created").
   - Cài đặt: shared/events.py:63-65, kênh orderflow:order.created (events.py:60-61).
   - Bên nhận: notification_app/main.py:44 (subscribe), handler main.py:27-38, shared/events.py:67-80.
   - Topic shared/contracts.py:16. Payload OrderCreated contracts.py:112-123.
   - bus_backend khác "redis" chạy bus in-memory (events.py:99-103); tài liệu không nói.
2. Model thiếu ở mục 3: ErrorBody, ErrorEnvelope (contracts.py:19,27), OrderCreated (:112), enum OrderStatus (:80; created/shipped/cancelled). OrderRead.status chỉ ghi "string".
3. Ràng buộc trường bị bỏ hết: min_length, max_length, gt=0, max_digits=10, decimal_places=2 (contracts.py:41-44,50-52); items 1..50, quantity 1..1000 (:62-68); query offset>=0, limit 1..200 mặc định 50 (products.py:16-17, orders.py:53-54, notifications.py:17-18).
4. Lỗi trả về hoàn toàn thiếu: 404 (catalog_app/services/products.py:21, order_app/services/orders.py:106, notification_app/services/notifications.py:70); 409 trùng SKU (products.py:28); 503 ở gateway (gateway_app/core/proxy.py:27,29); 422 của FastAPI (tests/test_orders.py:83); dạng thân lỗi {"error": {code, message, request_id}} (shared/errors.py:36-43); gateway chuyển nguyên status và thân upstream (proxy.py:31-35).
5. Ràng buộc bảng bị bỏ: products.sku unique+index (catalog_app/models.py:16); index notifications.order_id (:15), request_id (:19), orders.customer (:17), request_id (:24), order_items.order_id (:36); ondelete CASCADE của FK order_items.order_id (order_app/models.py:36); giá trị mặc định cột. Không có migration và không có create_all trong code chạy, chỉ tests/conftest.py:40 tạo bảng; tài liệu không nêu.
6. Không có quan hệ giữa component: gateway gọi 3 service qua HTTP; order gọi catalog qua HTTP (retry tenacity, circuit breaker, catalog_client.py:81-91, resilience.py); order gửi sự kiện cho notification qua Redis; mọi service dùng shared/. Mục 6 chỉ có một component "Toàn bộ" phẳng 54 file; bốn service không được tách.
7. Cấu hình: không nói tên biến môi trường (pydantic-settings đọc DATABASE_URL, BUS_BACKEND... không phân biệt hoa thường) và env_file=".env" (core/config.py:7).
8. Thư viện: bỏ extras uvicorn[standard], sqlalchemy[asyncio]; thiếu requires-python >=3.12 (pyproject.toml:11); starlette được import (shared/context.py:8-11) nhưng không khai; Redis là hạ tầng bắt buộc ở prod nhưng không nêu.
9. Middleware: chỉ ghi nơi dùng. Thiếu nơi định nghĩa RequestIdMiddleware (shared/context.py:29) và hành vi: đọc hoặc sinh X-Request-ID, gắn vào response (:37,45), ghi access log (:46-54). Thiếu lifespan.
10. Hành vi quan trọng thiếu: chế độ degraded khi catalog lỗi (đơn vẫn 201, warnings, unit_price=0, services/orders.py:41-63); publish lỗi không làm hỏng response (routes/orders.py:41-47); thông báo idempotent theo order_id (notifications.py:19-23).
11. Gateway không có GET /notifications/{id} dù notification-service có; tài liệu không nói.

Dễ hiểu sai:
- Mục 1 và 2 không có cột "service". Bốn dòng GET /health và các cặp /api/v1/orders, /products trông hệt nhau.
- Endpoint gateway #2, 5, 7, 11, 13, 19 ghi "Tham số: không có" và "Vào —". Đúng theo khai báo, nhưng gateway chuyển tiếp toàn bộ query và body (proxy.py:13-25). Ví dụ #2 thực sự cần order_id query, #7 cần body OrderCreate. Tôi tính là đúng, chỉ ghi chú.

## C. Phù hợp, dễ dùng: 3/5

- Tốt: mọi route có file:dòng, nhãn nguồn gốc rõ, trung thực khi không biết.
- Người mới biết có 23 route nhưng không biết service nào làm gì, cổng nào, lỗi nào, ràng buộc dữ liệu nào, và không biết có sự kiện Redis.
- Không hiểu được kiến trúc 4 service + shared vì chỉ có một component phẳng.

Chỗ gây hiểu sai, thừa, rối (trích nguyên văn):
- "Sự kiện, tác vụ nền | 0 điểm gửi/nhận" và "Không thấy điểm gửi/nhận qua Kafka, FastStream, Celery hay BackgroundTasks." Gây hiểu sai; endpoint #6 trong cùng tài liệu viết "rồi phát sự kiện order.created". Tự mâu thuẫn.
- "int (chưa quy ra kiểu SQL)" lặp ở 27 cột. Thừa.
- Cột khóa ngoại in {'table': 'orders', 'column': 'id'}. Lộ cấu trúc nội bộ.
- Mục 8: "&gt;=0.20" (lỗi escape HTML); mỗi thư viện hai dòng nên bảng dài gấp đôi.
- "Bộ kiểm chưa đối chiếu được kiểu/required/nullable với khai báo của: status" (mục 3, chú thích [2]) là thuật ngữ nội bộ.
- Mục 11: "18 lần nộp bị bộ kiểm từ chối ... chi tiết ở result.json" là nhật ký nội bộ.
- "Auth: chưa rõ" và "Còn thiếu: Trường chưa xác định: auth" lặp 23 lần. Nên nói một lần: không có xác thực trong source.
- Cột "Dấu hiệu" ở mục 6 chỉ lặp file:dòng, không có code (code chỉ có trong README).
- 20 file __init__.py vai trò "Khác" chiếm gần 40% bảng mục 6.

## D. Chuẩn đầu vào

Đầu vào: component "Toàn bộ" (61 file, gồm 7 file test) và "Khác" (4 file); không archdia, không sơ đồ. Chưa đủ:
- Repo là 4 service độc lập (pyproject.toml:8, docker-compose.yml) cộng shared/. Membership gộp thành một, nên không có quan hệ component, không biết route thuộc service nào, cấu hình và middleware bị trộn. Nên chia component theo gói: catalog_app, gateway_app, notification_app, order_app, shared.
- 7 file test nằm trong "Toàn bộ" nhưng ngoài phạm vi đọc, gây mâu thuẫn "61 file" với "57/57". Nên tách test thành component kind "test".
- Phạm vi đọc loại docker-compose.yml, .env.example, Dockerfile, ci.yml, README.md. Các file này có thông tin mà source Python không có: PostgreSQL, cổng 8000-8003, tên biến môi trường, topology, sơ đồ mermaid. Nên cho đọc nhóm "triển khai/cấu hình" làm bằng chứng.
- Thiếu archdia: nên quy định dựng quan hệ component từ import và lời gọi (gateway -> 3 service qua httpx, order -> catalog, bus Redis), nhãn "suy luận".
- Bộ trích tĩnh cần thêm: nhận diện bus tự viết (EventBus.publish/subscribe) chứ không chỉ Kafka/FastStream/Celery/BackgroundTasks; trích Field(...), unique/index/ondelete; ánh xạ exception handler -> mã lỗi.

Không chắc: 8 vai trò file (chủ quan); số liệu 213 mục là đếm theo nhóm, không theo từng ô thuộc tính.