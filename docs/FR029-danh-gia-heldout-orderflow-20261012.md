# Đánh giá đầu vào và đầu ra trên repo chưa dùng (orderflow-services) — 12/10/2026

File này trả lời: tài liệu sinh ra đã **chính xác, phù hợp, đầy đủ** chưa, và **đầu vào** đã chuẩn chưa. Đánh giá trên một repo không dùng khi phát triển các phần mới. Bằng chứng: [ket-qua-chay/heldout-orderflow-20261012/](../ket-qua-chay/heldout-orderflow-20261012/).

## 1. Cách làm để công bằng

| Bước | Làm gì | Vì sao |
|---|---|---|
| Chọn repo | `AlexGoster/orderflow-services`: 4 service, 23 route, gateway gọi HTTP sang service khác, Redis pub/sub. Gold do hai agent độc lập viết từ 08/10 | Repo lạ với phần mới; có đáp án viết trước |
| Model | Agent Claude mới đóng vai model, chỉ đọc đúng prompt + request (chế độ đọc một lần, prompt v6), không đọc code hay gold | Không tốn API; không biết luật chấm |
| Quy trình | Như model thật: nộp → bộ kiểm trả lỗi → 1 vòng sửa | Không can thiệp tay |
| Đóng băng | Hash 6 file đầu ra (`hashes.txt`) **trước khi chấm**; đề bài giám khảo viết trước khi có đầu ra (`judge-brief.md`) | Không sửa đầu ra hay tiêu chí theo kết quả |
| Chấm lớp 1 | `fr029_score.py` so với gold: route, model, HTTP | Tự động, đáp án có sẵn |
| Chấm lớp 2 | Giám khảo độc lập: agent Claude **Sonnet**, model khác với agent đóng vai. Đọc source, chấm mọi mục, tự quét phần thiếu, chấm đầu vào; không được đọc code công cụ, gold hay ghi chú | Phủ phần gold không có |
| Kiểm giám khảo | Claude (phiên chính) tự kiểm lại các phát hiện chính của giám khảo trên source | Giám khảo cũng có thể sai |

Giới hạn của cách chấm:
- Codex không dùng được: phiên chưa đăng nhập, báo 401. Không dùng khóa API thay, vì tốn tiền và chưa được duyệt. Cả agent đóng vai lẫn giám khảo đều là Claude, nên vẫn có thể thiên vị cùng họ model.
- Chỉ 1 repo.
- Không đo model thật sẽ dùng.

## 2. Kết quả trước khi sửa (đầu ra đóng băng)

| Phần | Kết quả |
|---|---|
| So gold | Route **23/23**, đúng cả handler, tham số, body, response, status. Model **9/9** (trường đúng hết). HTTP **2/2**: method 1/2 và đích 0/2 được ghi "chưa rõ"; gold chấp nhận, nhưng một bản gold ghi được khóa cấu hình |
| Giám khảo — chính xác | **202/213 đúng**, 9 sai, 2 không kiểm được. 8 trong 9 mục sai là vai trò file: giám khảo không đồng ý bảng vai trò của FR-029. Claude kiểm lại: công cụ làm **đúng spec** (`api/router.py` không có decorator route, nên là "Khác"); đây là vấn đề của spec |
| Giám khảo — dễ dùng | **3/5** |
| Quy trình | Lần nộp đầu bị từ chối 18 mục; 16/23 route chưa vào tài liệu. Sau 1 vòng sửa: đủ |

## 3. Lỗi tìm được và đã sửa (code chưa commit)

| # | Lỗi | Ai tìm | Sửa |
|---|---|---|---|
| 1 | Bộ kiểm từ chối nhầm mã lỗi truyền qua `super().__init__(..., status_code=404)`. 15 route mất lỗi 404/409/503; lần nộp đầu cả route bị loại | Claude, khi phát lại | Nhận đối số từ khóa trong lời gọi `__init__`; vẫn kiểm lớp con ghi đè. Test `StatusThroughInit` |
| 2 | Bỏ sót sự kiện Redis pub/sub (`order.created`) **mà không cảnh báo**; tài liệu ghi "0 điểm gửi/nhận" (FR-031 đòi ghi broker chưa hỗ trợ ở phần giới hạn) | Giám khảo; Claude kiểm lại đúng | Cảnh báo `QUEUE_LIBRARY_UNSUPPORTED` kèm `file:dòng`; bảng tóm tắt và mục 5 dẫn tới mục 11. **Chưa đọc được** bên gửi/nhận. Test `UnsupportedBus` |
| 3 | Khóa ngoại in dạng dict `{'table': 'orders', 'column': 'id'}` | Giám khảo | Ghi `orders.id` |
| 4 | Thư viện lặp dòng (khai ở cả `pyproject.toml` và `requirements.txt`) | Giám khảo | Một dòng, liệt kê mọi nơi khai |

Sau sửa, phát lại câu trả lời gốc của agent; vòng sửa dùng nguyên văn bản sửa của agent cho 3 mục còn bị từ chối đúng luật (`after-fix/`):
- gold vẫn route 23/23, model 9/9, HTTP 2/2;
- có lỗi trả về cho 15 route;
- có cảnh báo Redis pub/sub;
- 500/501 test qua; `fr029_checkaudit` không đổi.

**Chưa chấm lại bằng giám khảo** sau khi sửa.

## 4. Còn thiếu (chưa sửa)

| Thiếu | Loại | Gợi ý |
|---|---|---|
| Sự kiện qua bus tự viết (Redis pub/sub `EventBus.publish/subscribe`) | Đầy đủ | Đọc `redis.publish(channel)` / `pubsub().subscribe(channel)`, hoặc để agent đề xuất có kiểm |
| Ràng buộc trường (`Field(ge=1, le=200)`, độ dài), enum (`OrderStatus` ghi `string`), `unique`/`index`/`ondelete` của bảng | Đầy đủ | Thêm vào khuôn model/TBL; FR-029/030 hiện không đòi |
| Dạng thân lỗi (`ErrorEnvelope {error:{code,message,request_id}}`) | Đầy đủ | Gắn schema body cho mã lỗi khi handler trả model |
| Gateway chuyển tiếp query/body nhưng ghi "Tham số: không có" | Dễ hiểu sai | Ghi chú "chuyển tiếp nguyên yêu cầu" khi handler proxy |
| `GET /health` ×4, path trùng giữa service | Dễ dùng | Cần cột service; phụ thuộc đầu vào (mục 5) |
| Bảng vai trò file chưa có loại cho router tổng, middleware, xử lý lỗi | Spec | Xem lại bảng vai trò FR-029 (cần CR) |

## 5. Chuẩn đầu vào

| Vấn đề | Hậu quả | Đề xuất |
|---|---|---|
| Membership gộp 4 service + `shared/` thành **một** component "Toàn bộ" | Không có quan hệ giữa component; không tách endpoint theo service | Đầu vào FR-028 phải là component thật. Khi không có, công cụ nên cảnh báo "chỉ 1 component cho N ứng dụng FastAPI" |
| 7 file test nằm trong component thường | Mâu thuẫn 61 file / 57 file đọc | Đã có cảnh báo `MEMBERSHIP_KIND_SUSPECT` khi cả component là test; chưa có khi lẫn một phần |
| Không có `archdia.json`, sơ đồ | AC-04, AC-06 không đạt | Phụ thuộc FR-028 (người dùng quyết để nguyên) |
| Phạm vi đọc bỏ `docker-compose.yml`, `.env.example`, `README.md` | Mất dialect PostgreSQL, cổng, tên biến môi trường | Cân nhắc đọc thêm các file này ở mức "chỉ để tham khảo"; cần sửa FR-028 phần "Phạm vi đọc" |

## 6. Kết luận

- **Chính xác:** cao. Phần API (route, model, tham số, status) khớp gold hoàn toàn. Các phần đọc tĩnh được giám khảo xác nhận đúng.
- **Đầy đủ:** chưa đủ.
  - Lỗ lớn nhất: sự kiện qua bus tự viết. Nay đã được cảnh báo, nhưng chưa được đọc.
  - Ràng buộc dữ liệu, enum và dạng thân lỗi chưa có.
- **Phù hợp:** dùng được cho việc tra cứu API (3/5 trước khi sửa); các lỗi trình bày giám khảo nêu đã sửa phần lớn.
- **Đầu vào:** là điểm yếu nhất. Chất lượng phần cấu trúc và quan hệ phụ thuộc vào membership của FR-028; membership hiện có của repo này không đủ.
