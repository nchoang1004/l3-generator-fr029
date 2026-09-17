---
uid: "01M2J06Z3NE8FQCAJRGQXZMWKA"
key: "OQ-L3GEN-002"
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
owner: "Người phụ trách PRD phối hợp mentor"
due: "2026-09-19"
change_set: "CHG-L3GEN-2026-001"
---

# OQ-L3GEN-002 — Chốt phạm vi đầy đủ và lịch giao

## Câu hỏi cần người quyết định

PRD mô tả full product gồm hai kênh, hai stack, component/L3, config/event, lịch sử và job/API. Nhóm đã chốt khung thời gian: hai người, bắt đầu 11/09/2026, 4 tuần, kết thúc 09/10/2026, chia bốn mốc M0–M3 tại PRD mục VIII.

Câu hỏi cho mentor:

1. Khung 4 tuần với **toàn bộ Must** của M0–M3 có được chấp nhận không, khi M0 đã trễ so với dự kiến 16/09.
2. Nếu không đủ capacity, phần nào được phép giao sau: Java/Spring Boot ở M3, job/API ở M2, hay thu hẹp phạm vi màn hình.
3. M1 và M2 là mốc kiểm tra nội bộ, hay là các lần phát hành riêng. Nếu phát hành riêng, phải tách phạm vi Change Set và baseline tương ứng trước khi chốt.
4. Mức ưu tiên Must/Should đang đề xuất tại PRD mục IV.3 có đúng không.

**Phần không do đề bài chỉ định.** Đề bài mục 3.6 không bắt buộc cụ thể hai kênh, job/API hay định dạng JSON/Mermaid. Đây là lựa chọn của nhóm để có phạm vi kiểm chứng được; căn cứ ghi tại PRD mục I. Cảnh báo trong sản phẩm chỉ phục vụ hiểu giới hạn phân tích kiến trúc; rà code không dùng và cách xử lý lỗi HTTP nằm ngoài phạm vi.

- **Owner theo vai:** Người phụ trách PRD phối hợp mentor.
- **Hạn trả lời đề xuất:** 19/09/2026, trước Scope Gate. Hạn cũ 17/09 đã qua mà chưa có câu trả lời; đây là hạn do nhóm tự đặt, không phải ngày mentor đã cam kết.
- **Blocking:** Cam kết scope và milestone của toàn hệ thống.
- **Cách xử lý trong bản nháp:** Giữ đầy đủ yêu cầu; M0–M3 là mốc kiểm tra tiến độ nội bộ, không tự loại tính năng để khớp code đang có.
- **Trả lời:** Chưa có.

## Rủi ro lịch, ghi ngày 17/09/2026

Bốn tuần cho hai người, phủ hai stack, hai kênh và bảy nhóm màn hình là lịch chặt. M0 đã trễ. Khung thời gian trên là **đề xuất của nhóm**, chưa phải cam kết được duyệt.

Nếu mentor kết luận không đủ capacity, Product điều chỉnh phase và baseline qua review. Không tự đổi Must thành Done hoặc Out of Scope, và không lặng lẽ đẩy Java sang sau pilot.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.

