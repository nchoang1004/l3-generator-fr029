---
uid: "01M2J06Z3RBJQZQ8V7FFBSMPGG"
key: "OQ-L3GEN-004"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "open"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Product và QA được mentor chỉ định"
due: "2026-09-19"
change_set: "CHG-L3GEN-2026-001"
---

# OQ-L3GEN-004 — Duyệt ngưỡng chất lượng và đáp án nghiệm thu

## Câu hỏi cần người quyết định

Product đã chốt các ngưỡng vận hành, đã vào NFR và không còn là câu hỏi mở:

| Nội dung | Giá trị | Nơi ghi |
|---|---|---|
| Giới hạn tiếp nhận | ZIP nén 100 MB, giải nén 500 MB, 50.000 file | NFR-L3GEN-PERF-001 |
| Trần thời gian một lần phân tích | 10 phút | NFR-L3GEN-PERF-001 |
| Lịch sử phân tích | 10 lần gần nhất cho mỗi repository, hết hạn 14 ngày, xóa thủ công được | NFR-L3GEN-PRIV-001 |
| Mức trừu tượng kết quả | Repository từ 500 function trở lên vẫn cho sơ đồ mặc định tối đa 50 node | NFR-L3GEN-ABST-001 |

Phần chưa chốt cần Product và QA quyết:

1. Ngưỡng precision và recall của NFR-L3GEN-ACC-001 có được chấp nhận không.
2. Cỡ mẫu tại OBS: 20 repository pilot và 100 quan hệ đã được reviewer đánh giá có đủ không.
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

