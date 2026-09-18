---
uid: "01M2J06Z3RBJQZQ8V7FFBSMPGG"
key: "OQ-L3GEN-004"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "closed"
revision: 5
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Khiêm và Hoàng"
due: "2026-09-19"
change_set: "CHG-L3GEN-2026-001"
---

# OQ-L3GEN-004 — Duyệt ngưỡng chất lượng và đáp án nghiệm thu

## Quyết định cuối cùng ngày 18/09/2026

**Người quyết định:** Khiêm và Hoàng trong phạm vi quyền mentor đã trao cho nhóm.

1. Precision exact cho route, entity, HTTP, config, event và internal call edge là **≥90%**. Recall giữ nguyên: route ≥85%, entity ≥90%, HTTP/config/event ≥80%, internal call edge ≥70%.
2. Component membership giữ precision và recall ≥85%; component dependency dùng precision exact **≥90%**.
3. Phase đầu chỉ đo Python/FastAPI. Java phải có dataset và báo cáo riêng ở phase sau; không lấy điểm Python làm bằng chứng Java.
4. Dataset kỹ thuật cần ít nhất ba repository Python public có cấu trúc khác nhau và pin commit, cộng micro fixture/negative case theo pattern. Danh sách repo/commit là checklist bắt buộc trước lần đo đầu tiên, không phải dữ kiện phải bịa để qua Scope Gate.
5. Khiêm và Hoàng lập ground truth độc lập trước khi xem output, giữ hai bản ban đầu, ghi disagreement rồi tạo bản adjudicated. Hoàng điều phối dataset/phiếu chấm/báo cáo; Khiêm chuẩn bị fixture và hỗ trợ kỹ thuật.
6. Benchmark chấp nhận cấu hình chuẩn 4 CPU logical, RAM 8 GiB, SSD, Python 3.12, no-AI; chạy năm lần mỗi repo, ghi từng lần, worst-case và peak RSS. Máy thực tế khác phải công bố, không ngoại suy.
7. Pilot so sánh giữ thiết kế hai nhóm độc lập, tối thiểu năm người mỗi nhóm, là phép đo sau phase đầu khi tuyển đủ người. Khiêm và Hoàng không được tính là người dùng mới.
8. Nếu chưa có người ngoài nhóm: Hoàng vẫn thực hiện UAT chức năng; KPI-L3GEN-001/002 ghi `not_evaluated`; phase đầu có thể bàn giao ở trạng thái **technical pilot ready — chưa xác thực hiệu quả với người dùng bên ngoài**. Không tuyên bố tỷ lệ hoàn thành hoặc giảm thời gian.
9. Nếu chỉ tuyển được một đến hai người, được làm usability định tính và lưu finding nhưng không tính KPI phần trăm.
10. Giữ ngưỡng repository ≥500 function thì sơ đồ mặc định ≤50 node. FR-L3GEN-018 nghiệm thu bằng AC và raw counts, không dùng ngưỡng route thay thế.

**Kết quả:** OQ được đóng. Các phép đo vẫn là `not_run` cho đến khi có evidence thật; đóng câu hỏi không đồng nghĩa sản phẩm đã đạt ngưỡng.

## Câu hỏi gốc — đã giải quyết

Product đã chốt các ngưỡng vận hành, đã vào NFR và không còn là câu hỏi mở:

| Nội dung | Giá trị | Nơi ghi |
|---|---|---|
| Giới hạn tiếp nhận | ZIP nén 100 MB, giải nén 500 MB, 50.000 file | NFR-L3GEN-PERF-001 |
| Trần thời gian một lần phân tích | 10 phút | NFR-L3GEN-PERF-001 |
| Lịch sử phân tích | 10 lần gần nhất cho mỗi repository, hết hạn 14 ngày, xóa thủ công được | NFR-L3GEN-PRIV-001 |
| Mức trừu tượng kết quả | Repository từ 500 function trở lên vẫn cho sơ đồ mặc định tối đa 50 node | NFR-L3GEN-ABST-001 |

Phần chưa chốt cần Product và QA quyết:

1. Ngưỡng precision và recall của NFR-L3GEN-ACC-001 có được chấp nhận không.
2. Cỡ mẫu theo từng nhóm dữ kiện ở OBS-001 và theo người tham gia ở OBS-002 có đủ không.
3. Máy benchmark công bố trong NFR-L3GEN-PERF-001 có đại diện không.
4. Cách người đọc phân nhóm component thành ground truth.
5. Ai là hai người lập đáp án nghiệm thu độc lập, và ai là người thử pilot chưa từng dùng sản phẩm.
6. Repository và commit dùng để đo, phải chốt trước khi benchmark.

Ngưỡng 500 function và 50 node là con số đề xuất để kiểm chứng được, chưa đo trên fixture đã pin.

- **Owner theo vai:** Product và QA được mentor chỉ định.
- **Hạn trả lời đề xuất:** 19/09/2026, trước Scope Gate. Hạn cũ 17/09 đã qua mà chưa có câu trả lời; đây là hạn do nhóm tự đặt, không phải ngày mentor đã cam kết.
- **Blocking:** NFR-L3GEN-ACC-001, toàn bộ KPI và việc nghiệm thu. Các ngưỡng vận hành ở PERF/PRIV/ABST đã chốt nên không còn bị chặn, nhưng vẫn cần duyệt cùng lúc với phần còn lại.
- **Cách xử lý trong bản nháp:** Giữ ngưỡng là proposed. Chưa có phép đo nào được coi là kết quả đạt sản phẩm.
- **Trả lời một phần, ngày 17/09/2026.** Product đã chốt bốn ngưỡng vận hành nêu trên. Sáu mục còn lại chưa có quyết định.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.


## Phương án chuẩn bị review ngày 17/09/2026 — lịch sử

Nguồn chuẩn của cỡ mẫu là OBS-001/002, không giữ bộ số khác trong OQ. OBS-001 đề xuất ít nhất ba repo độc lập, có cả Python và Java, pin commit; thống kê riêng mỗi stack/pattern. OBS-002 đề xuất hai nhóm độc lập, ít nhất năm người mỗi nhóm; thời gian và completion báo riêng. Mục tiêu giảm 50% là target xin duyệt, chưa có kết quả.

Đề xuất Hoàng điều phối dataset và phiếu chấm, Khiêm hỗ trợ fixture; không coi đề xuất là hai người đã đồng ý làm đáp án độc lập. Mentor xác nhận người chấm/giải quyết bất đồng và tuyển người pilot. Danh sách repo, commit, quyền sử dụng, cấu hình máy và người chấm còn chờ xác nhận; phải điền trước đo. Không tạo tên hoặc SHA giả.

Phương án đã được thay thế bởi quyết định ngày 18/09/2026. Repo/commit và người pilot chưa có vẫn phải ghi `not_run`/`not_evaluated`; đây là dữ kiện thực thi cần có trước phép đo, không còn là blocker của Scope Gate.
