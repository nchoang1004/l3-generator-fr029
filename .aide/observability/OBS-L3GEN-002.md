---
uid: "01M2J06Z3ZZA3PA2M5MD80ZGB7"
key: "OBS-L3GEN-002"
type: "observability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"measures":["KPI-L3GEN-001","KPI-L3GEN-002"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# Phương pháp đo trải nghiệm tìm hiểu kiến trúc

## Câu hỏi

Người dùng có tự tìm đúng component, API và dependency có evidence bằng công cụ không? Baseline thời gian đọc tay: chưa đo; không tuyên bố tiết kiệm ngày công theo số node.

## Thử nghiệm đề xuất

- Khi tuyển đủ, dùng ít nhất 5 người mỗi nhóm, chưa dùng tool và không tham gia phát triển; ghi vai trò và mức quen repo. Khiêm và Hoàng không được tính là người dùng mới. Không có người thì giữ `not_evaluated`, không tạo tên giả.
- Mỗi người làm bộ câu hỏi tương đương: tìm handler của API, bảng liên quan, external dependency, config/event binding và chỉ ra bằng chứng.
- Đề xuất chia hai nhóm độc lập có mức kinh nghiệm tương đương: một nhóm đọc tay, một nhóm dùng tool; cùng repository/câu hỏi, không chuyển người giữa hai nhóm. Người chấm dùng đáp án độc lập.
- Thu completion, đúng/sai, thời gian, số lần cần hướng dẫn và vấn đề UI; không loại người thất bại khỏi mẫu.
- KPI-L3GEN-001 = số người hoàn thành đúng toàn bộ nhiệm vụ chính mà không cần hướng dẫn / tổng người tham gia đủ điều kiện.
- KPI-L3GEN-002 = trung vị thời gian hoàn thành bài đọc kiến trúc khi có công cụ, so với trung vị của nhóm làm thủ công trên cùng bộ câu hỏi và cùng repository. Đo trên người chưa dùng sản phẩm; không dùng lại người đã làm bài thủ công cho lượt có công cụ.
- Target của cả hai nằm tại PRD mục II.4; OBS không giữ bản sao của ngưỡng.
- Tỷ lệ giảm = 1 - median thời gian nhóm dùng tool / median thời gian nhóm đọc tay. Chỉ tính kết luận khi hai nhóm đủ mẫu, nhiệm vụ và mức đúng tương đương. Ghi mọi ca không hoàn thành; không bỏ ca thất bại để cải thiện số: nếu có ca chưa hoàn thành ở thời hạn bài được chốt trước thì KPI thời gian là not_evaluated, báo completion riêng. Mục tiêu 50% trong PRD là target đã chốt để đo khi đủ mẫu, không phải kết quả đã đạt.

## Bằng chứng và trạng thái

Consent cho phiên thử; lưu phiếu nhiệm vụ, kết quả ẩn danh và phát hiện usability ở evidence/tests. Không thu PII không cần thiết. Tình trạng: **not_run**, chưa tuyển người, chưa có kết quả nghiệm thu.

NFR-L3GEN-USA-001 quy định ngưỡng setup và accessibility; các threshold đó không được chép thành giá trị khác ở PRD/AC.

## Khi chưa tuyển được người pilot

Pilot so sánh không chặn bàn giao phase đầu. Hoàng vẫn thực hiện UAT chức năng trên build xác định; KPI-L3GEN-001/002 giữ `not_evaluated` và sản phẩm chỉ được mô tả là **technical pilot ready — chưa xác thực hiệu quả với người dùng bên ngoài**. Nếu chỉ có một đến hai người ngoài nhóm, dùng kết quả làm usability định tính và finding, không tính KPI phần trăm hoặc mức giảm thời gian.
