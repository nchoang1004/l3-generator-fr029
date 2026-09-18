---
uid: "01M2J06Z3NE8FQCAJRGQXZMWKA"
key: "OQ-L3GEN-002"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "closed"
revision: 7
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

# OQ-L3GEN-002 — Chốt phạm vi đầy đủ và lịch giao

## Quyết định cuối cùng ngày 18/09/2026

**Người quyết định:** Khiêm, sau khi thống nhất ranh giới phase đầu với Hoàng trong phạm vi quyền mentor đã trao cho nhóm.

1. Phase đầu giữ khung bốn tuần từ 11/09 đến 09/10/2026. M0–M3 là checkpoint nội bộ, không phải các release độc lập.
2. Phạm vi Must của phase đầu là một vertical slice Python/FastAPI hoàn chỉnh qua cả CLI và web: nhận thư mục local, ZIP hoặc GitHub public; phân tích tĩnh; route/data/HTTP/reference/dependency/config/Kafka Python; evidence; component/L3; JSON/Markdown/Mermaid; lỗi và giới hạn; chạy đầy đủ khi không có AI.
3. Giữ FR-L3GEN-013 và FR-L3GEN-016 trong phase đầu. Web chỉ cam kết xử lý và hiển thị trạng thái của lần chạy hiện tại, xem kết quả/evidence và tải output.
4. FR-L3GEN-017 đầy đủ — public job API, lịch sử nhiều lần chạy, mở lại kết quả cũ, retention và xóa từng phiên — chuyển sang phase sau. Trạng thái tạm của lần chạy hiện tại thuộc luồng web của FR-013/016, không được diễn giải là đã đạt FR-017.
5. Toàn bộ adapter Java/Spring Boot chuyển sang phase sau. Các AC Java được giữ trong roadmap nhưng không thuộc nghiệm thu ngày 09/10.
6. FR-L3GEN-012 về AI tiếp tục là Should/Stretch; không chặn nghiệm thu phase đầu.
7. M3 dành cho tích hợp config/event Python, hardening, đo NFR và nghiệm thu; không bắt đầu thêm Java hoặc lịch sử/job API trong mốc này.

**Kết quả:** OQ được đóng. Full product vẫn là roadmap của PRD, nhưng cam kết ngày 09/10 chỉ gồm phase đầu nêu trên. Mọi mở rộng phase sau phải có baseline/change decision riêng trước khi trở thành cam kết.

## Câu hỏi gốc — đã giải quyết

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

## Rủi ro lịch, ghi ngày 17/09/2026 — lịch sử trước quyết định

Bốn tuần cho hai người, phủ hai stack, hai kênh và bảy nhóm màn hình là lịch chặt. M0 đã trễ. Khung thời gian trên là **đề xuất của nhóm**, chưa phải cam kết được duyệt.

Nếu mentor kết luận không đủ capacity, Product điều chỉnh phase và baseline qua review. Không tự đổi Must thành Done hoặc Out of Scope, và không lặng lẽ đẩy Java sang sau pilot.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.


## Phương án chuẩn bị review ngày 17/09/2026 — lịch sử

Ưu tiên đề xuất: đầu vào an toàn → lõi phân tích và evidence → component/L3/export → UI/history → Java/config/event → pilot. Giữ full product và các Must hiện tại tới khi mentor quyết; AI là Should, chỉ làm sau lõi.

| Mốc | Đề xuất công việc | Điều kiện kiểm |
|---|---|---|
| M0 | Đồng bộ PRD/FR/NFR, chốt pattern và phương pháp đo | Mentor review phạm vi, xử lý blocker |
| M1 | Python CLI, inventory/entry point, FR-018, API/DB/HTTP, evidence và output ban đầu | Fixture Python, no-AI, partial/error đúng |
| M2 | Component/L3 và web Git/ZIP, phiên phân tích, lịch sử | AC tích hợp và an toàn đầu vào |
| M3 | Java/Spring Boot, Kafka hai stack, config và pilot | Toàn bộ Must theo AC/NFR đã duyệt |

Đề xuất phân công: Khiêm điều phối/engine, Hoàng fixture/đánh giá và tích hợp UI; hai người phải xác nhận trước khi thành cam kết. Chưa có dữ liệu giờ rảnh hoặc ước lượng được thành viên xác nhận, không suy rằng lịch đủ capacity.

Trước xác nhận lịch, mỗi người ghi số giờ/tuần có thể dành và ước lượng giờ còn lại theo mốc; dành phần dự phòng rõ ràng. Nếu tổng nhu cầu vượt giờ khả dụng: phương án B đề xuất lùi mốc nghiệm thu full product; nếu hạn 09/10 cố định, trình mentor chọn pilot Python trước, Java và API tích hợp sau. Không tự đổi Must/ngoài phạm vi trước duyệt.

Phương án này đã được thay thế bởi quyết định cuối cùng ngày 18/09/2026: giữ hạn 09/10, chốt vertical slice Python qua CLI và web, giữ FR-013/016, chuyển Java và FR-017 đầy đủ sang phase sau.
