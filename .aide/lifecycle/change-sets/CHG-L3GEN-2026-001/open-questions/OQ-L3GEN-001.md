---
uid: "01M2J06Z3KK1KYTZ2RZ1QQESJF"
key: "OQ-L3GEN-001"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "open"
revision: 5
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Khiêm"
due: "2026-09-19"
change_set: "CHG-L3GEN-2026-001"
---

# OQ-L3GEN-001 — Xác nhận mã tổ chức và người chịu trách nhiệm

## Câu hỏi cần người quyết định

Mã SYS-L3GEN, TEAM-L3GEN và key PRD-L3GEN-2609-001 đang dùng làm mã dự thảo, chưa đối chiếu với registry chính thức.

Hai mentor đã xác định là Nguyễn Chí Thức và Đinh Thái Hà, ghi tại PRD mục I. Nhóm có hai developer là Khiêm và Hoàng. Phần chưa biết là **ai giữ vai ký nào**:

1. Ai ký vai Product, Tech Lead và QA tại Scope Gate.
2. Ai nghiệm thu độc lập với người sở hữu AC.
3. Scope Gate cần một hay cả hai mentor duyệt.
4. Có registry, template hoặc công cụ cấp UID chính thức để đối chiếu mã dự thảo không.

- **Owner:** Khiêm (nhận ngày 17/09/2026), phối hợp hai mentor cho phần còn mở.
- **Hạn trả lời đề xuất:** 19/09/2026, trước Scope Gate. Hạn cũ 17/09 đã qua mà chưa có câu trả lời; đây là hạn do nhóm tự đặt, không phải ngày mentor đã cam kết.
- **Blocking:** Toàn bộ metadata và Scope Gate.
- **Cách xử lý trong bản nháp:** Giữ mã dự thảo, không ghi tên hoặc chữ ký chưa được cung cấp.
- **Trả lời một phần, ngày 17/09/2026.** Xem mục dưới.

## Trả lời một phần, ngày 17/09/2026

**Người trả lời:** Khiêm.

**Câu 1 — vai Product.** Khiêm nhận vai `product-owner` cho Change Set này: tiếp nhận yêu cầu,
chốt tier, sở hữu FR/AC và ký Scope Gate. Đã ghi vào `change-set.yaml` mục `intake` với
`role_confirmed: false`. Vai Tech Lead và QA **chưa có người**; Hoàng đang được đề xuất cho Test/QA
tại PRD mục I nhưng chưa xác nhận.

**Câu 2 — nghiệm thu độc lập.** Chưa trả lời được. Quy trình yêu cầu người nghiệm thu khác với
`accountable_role` của FR đang test. Khiêm giữ vai Product nên **không được tự nghiệm thu**; trong
nhóm chỉ còn Hoàng. Cần mentor xác nhận Hoàng đủ độc lập hay phải có người ngoài nhóm.

**Câu 3 — một hay hai mentor duyệt.** Chưa trả lời được; thuộc thẩm quyền mentor.

**Câu 4 — registry và công cụ cấp UID.** Chưa có trong repo. Mã `SYS-L3GEN`, `TEAM-L3GEN` và
`PRD-L3GEN-2609-001` vẫn là mã dự thảo. ULID hiện sinh bằng Python standard library, không phải
công cụ chính thức. Cần mentor cho biết có registry để đối chiếu không.

**Hệ quả nếu mentor không đồng ý việc Khiêm giữ vai Product:** các quyết định đã ghi dựa trên vai
này phải rà lại — gồm tier T1, intake, và câu trả lời OQ-L3GEN-005. Nội dung quyết định không đổi
theo người ký, nhưng thẩm quyền thì có.

**Vẫn `open`.** Ba trong bốn câu chưa có câu trả lời và đều cần mentor.

## Vì sao chưa tự trả lời được

Nhóm có hai developer, trong khi bảng phê duyệt ở PRD mục IX cần ba vai ký cộng một người nghiệm thu độc lập. Con số không khớp, nên phải có người quyết: một người kiêm được những vai nào, và vai nào bắt buộc do người ngoài nhóm đảm nhiệm.

Việc một người viết tài liệu không phải căn cứ để gán người đó vào vai ký.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.

