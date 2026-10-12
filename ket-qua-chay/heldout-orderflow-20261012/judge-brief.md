# Đề bài cho giám khảo độc lập — chấm bộ tài liệu sinh cho orderflow-services

Viết ngày 12/10/2026, **trước khi** có đầu ra; không sửa sau khi có kết quả.

## Bạn là ai, được đọc gì

Bạn là người review độc lập. Một công cụ đã đọc source của repository dưới đây và sinh tài liệu kỹ thuật L3. Việc của bạn: kiểm tài liệu đó có **chính xác, đầy đủ, phù hợp** không, và **đầu vào** mà công cụ nhận có đủ chuẩn không.

Được đọc:
- Source: `D:\VSF\l3-heldout-repos2\AlexGoster_orderflow-services\` (đọc tùy ý, không chạy code).
- Đầu ra đã đóng băng: `D:\VSF\l3-generator-l3\ket-qua-chay\heldout-orderflow-20261012\output\`. File chính cho người đọc là `TAI-LIEU.md`; còn có `README.md`, `tech-specs/**`, `result.json`.
- Đầu vào công cụ đã nhận: thư mục source trên; danh sách component `D:\VSF\l3-heldout-gold2\AlexGoster_orderflow-services\membership.json`; không có `archdia.json`, không có sơ đồ.
- File `hashes.txt` trong thư mục kết quả: hash các file đầu ra lúc đóng băng.

**Không được đọc:** mọi file khác dưới `D:\VSF\l3-generator-l3\` (code của công cụ, tài liệu, ghi chú, kết quả khác); mọi file `gold*.json`; mọi file `answer*.json`, `system.txt`, `user.txt` trong thư mục kết quả. Không dùng mạng.

## Tài liệu cần có (chuẩn để chấm)

Theo đề bài dự án (Code → L3 Generator) và yêu cầu FR-029/030/031, tài liệu L3 cho một repository Python/FastAPI cần cho biết, có bằng chứng `file:dòng`:
- API: mọi endpoint (method, path đầy đủ gồm mọi prefix, tham số, body, response, status, lỗi có thể trả về, dependency/auth), model request/response và trường của chúng (kiểu, bắt buộc, null).
- Bảng CSDL (cột, khóa chính/ngoại, null), sự kiện và tác vụ nền (Kafka/FastStream/Celery/BackgroundTasks: bên gửi, bên nhận).
- Lời gọi HTTP ra ngoài (httpx/requests/aiohttp: method, đích).
- Cấu trúc code: component, file và vai trò (Điểm vào, Route, Model bảng, Hạ tầng, Truy cập dữ liệu, Schema API, Cấu hình, Service, Khác), quan hệ giữa component.
- Cấu hình, thư viện quan trọng, middleware/xử lý lỗi toàn cục.
- Điều chưa biết phải ghi "chưa rõ" kèm lý do; không được đoán.

## Việc cần làm

A. **Chính xác.** Với từng mục trong `TAI-LIEU.md` (mọi endpoint và từng thuộc tính; mọi model và trường; bảng; sự kiện; lời gọi HTTP; thư viện; cấu hình; middleware; quan hệ component; ít nhất 20 vai trò file), đối chiếu với source: `đúng` / `sai` / `không kiểm được`, kèm `file:dòng` của source. Nhãn "chắc chắn/suy luận/chưa rõ" có phù hợp không.

B. **Đầy đủ.** Tự quét source, độc lập với tài liệu: route, model dùng bởi route, lời gọi HTTP ra ngoài, bảng, sự kiện/tác vụ nền, khóa cấu hình, middleware/exception handler, thư viện. Liệt kê mọi thứ có trong source mà tài liệu **thiếu** hoặc ghi sai chỗ.

C. **Phù hợp, dễ dùng.** Một lập trình viên mới chỉ đọc `TAI-LIEU.md` có hiểu và dùng được API, hiểu cấu trúc không? Liệt kê cụ thể chỗ gây hiểu sai, thừa, rối, nhãn sai (trích nguyên văn). Cho điểm 1–5, kèm lý do.

D. **Chuẩn đầu vào.** Đầu vào công cụ nhận (danh sách component trong membership.json, thiếu archdia/sơ đồ, phạm vi file được đọc/bị loại) có đủ để sinh tài liệu tốt không? Thiếu gì, nên quy định gì.

## Cách trả lời

- Ghi `D:\VSF\l3-generator-l3\ket-qua-chay\heldout-orderflow-20261012\judge\report.md` (tiếng Việt, ngắn, theo A–D, mỗi phát hiện có `file:dòng`).
- Ghi `...\judge\summary.json`: `{"accuracy": {"checked": n, "correct": n, "wrong": n, "unverifiable": n}, "missing": [..], "wrong": [..], "usability_score": n, "input_issues": [..]}`.
- Không chắc thì nói không chắc. Không đoán. Không sửa file đầu ra.
