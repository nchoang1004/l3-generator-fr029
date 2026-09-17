---
uid: "01M2J06Z3SMZD88VJ6YYGF4Y68"
key: "OQ-L3GEN-005"
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
owner: "Tech Lead/Security phối hợp người phụ trách PRD"
due: "2026-09-19"
change_set: "CHG-L3GEN-2026-001"
---

# OQ-L3GEN-005 — Chốt môi trường web, dữ liệu và AI

## Câu hỏi cần người quyết định

Product đã chốt, đã vào PRD mục IV và các NFR liên quan:

- Chỉ hỗ trợ GitHub public. Repository private và mọi cơ chế nhận hoặc lưu credential nằm ngoài phạm vi.
- Không có đăng nhập, SSO hoặc multi-tenant public hosting.
- AI mặc định tắt, phải chủ động bật. Phần lõi chạy đầy đủ khi không có AI.
- Dòng lệnh chạy cục bộ, không cần web server và không cần mạng.
- Hạn giữ dữ liệu và giới hạn lịch sử theo NFR-L3GEN-PRIV-001; Product đã chốt con số.

Phần chưa chốt cần Tech Lead và Security quyết:

1. Web triển khai ở đâu: máy cá nhân, máy nội bộ của nhóm, hay môi trường được cấp. Việc này ảnh hưởng NFR-L3GEN-SEC-001 và cách đo NFR-L3GEN-PERF-001.
2. Allowlist domain khi lấy source từ GitHub, và threat model cho luồng tiếp nhận ZIP.
3. Provider AI nào được phép, ai trả chi phí và trần chi phí là bao nhiêu.
4. Môi trường được chọn có đáp ứng được hạn giữ dữ liệu đã chốt không. Nếu không, phải đổi môi trường chứ không hạ yêu cầu riêng tư.

- **Owner theo vai:** Tech Lead/Security phối hợp người phụ trách PRD.
- **Hạn trả lời đề xuất:** 19/09/2026, trước Scope Gate. Hạn cũ 17/09 đã qua mà chưa có câu trả lời; đây là hạn do nhóm tự đặt, không phải ngày mentor đã cam kết.
- **Blocking:** FR-L3GEN-012, FR-L3GEN-016, FR-L3GEN-017; NFR SEC/PRIV/AI.
- **Cách xử lý trong bản nháp:** Giả định workspace tin cậy hoặc local. Không viết thông số môi trường cụ thể vào NFR khi chưa biết web chạy ở đâu.
- **Trả lời một phần, ngày 17/09/2026.** Product đã chốt năm điểm về phạm vi truy cập và AI nêu trên. Bốn mục còn lại chưa có quyết định.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.

