---
uid: "01M2J06Z3ZZA3PA2M5MD80ZGB7"
key: "OBS-L3GEN-002"
type: "observability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"measures":["KPI-L3GEN-001","KPI-L3GEN-002"],"blocked_by":["OQ-L3GEN-004"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# Phương pháp đo trải nghiệm tìm hiểu kiến trúc

## Câu hỏi

Người dùng có tự tìm đúng component, API và dependency có evidence bằng công cụ không? Baseline thời gian đọc tay: chưa đo; không tuyên bố tiết kiệm ngày công theo số node.

## Thử nghiệm đề xuất

- Ít nhất 5 người chưa dùng tool, ghi vai trò và mức quen repo. Cần mentor xác nhận người tham gia, không tạo tên giả.
- Mỗi người làm bộ câu hỏi tương đương: tìm handler của API, bảng liên quan, external dependency, config/event binding và chỉ ra bằng chứng.
- Đo đọc source thủ công và dùng tool trên hai bộ repo/câu hỏi tương đương; đổi thứ tự giữa người để giảm hiệu ứng học. Người chấm có đáp án độc lập.
- Thu completion, đúng/sai, thời gian, số lần cần hướng dẫn và vấn đề UI; không loại người thất bại khỏi mẫu.
- KPI-L3GEN-001 = số người hoàn thành đúng toàn bộ nhiệm vụ chính mà không cần hướng dẫn / tổng người tham gia đủ điều kiện.
- KPI-L3GEN-002 = trung vị thời gian hoàn thành bài đọc kiến trúc khi có công cụ, so với trung vị của nhóm làm thủ công trên cùng bộ câu hỏi và cùng repository. Đo trên người chưa dùng sản phẩm; không dùng lại người đã làm bài thủ công cho lượt có công cụ.
- Target của cả hai nằm tại PRD mục II.4; OBS không giữ bản sao của ngưỡng.
- Median thời gian và thay đổi so với baseline là chỉ số thăm dò tới khi đủ dữ liệu; không đặt phần trăm tiết kiệm tùy ý.

## Bằng chứng và trạng thái

Consent cho phiên thử; lưu phiếu nhiệm vụ, kết quả ẩn danh và phát hiện usability ở evidence/tests. Không thu PII không cần thiết. Tình trạng: **not_run**, chưa tuyển người, chưa có kết quả nghiệm thu.

NFR-L3GEN-USA-001 quy định ngưỡng setup và accessibility; các threshold đó không được chép thành giá trị khác ở PRD/AC.

