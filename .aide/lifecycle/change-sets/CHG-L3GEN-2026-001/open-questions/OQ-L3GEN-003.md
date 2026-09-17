---
uid: "01M2J06Z3PC3FFNMP5HZX88KZV"
key: "OQ-L3GEN-003"
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
owner: "Tech Lead được mentor chỉ định"
due: "2026-09-19"
change_set: "CHG-L3GEN-2026-001"
---

# OQ-L3GEN-003 — Chốt ma trận pattern và adapter hỗ trợ

## Câu hỏi cần người quyết định

Product đã chốt hai stack: Python/FastAPI là stack thứ nhất, Java/Spring Boot là stack thứ hai, event giới hạn ở Kafka. Phần này đã vào NFR-L3GEN-COMP-001, FR-L3GEN-015 và PRD mục IV.

Phần chưa chốt là **ma trận pattern cụ thể** trong từng stack:

1. Phía Python: SQLModel, `mapped_column` và `add_api_route` thuộc phạm vi bắt buộc hay phase mở rộng.
2. Phía Java: annotation nào của Spring Boot, ORM nào và thư viện Kafka nào được coi là hỗ trợ.
3. Schema YAML cấu hình nào được phép diễn giải.

- **Owner theo vai:** Tech Lead được mentor chỉ định.
- **Hạn trả lời đề xuất:** 19/09/2026, trước Scope Gate. Hạn cũ 17/09 đã qua mà chưa có câu trả lời; đây là hạn do nhóm tự đặt, không phải ngày mentor đã cam kết.
- **Blocking:** FR-L3GEN-003, FR-L3GEN-004, FR-L3GEN-014, FR-L3GEN-015 và NFR-L3GEN-COMP-001.
- **Cách xử lý trong bản nháp:** Không nói hỗ trợ mọi repo; công bố pattern cụ thể và cảnh báo phần chưa hỗ trợ.
- **Trả lời một phần, ngày 17/09/2026.** Product đã chốt phần chọn stack và phạm vi event như nêu ở trên. Phần ma trận pattern trong từng stack vẫn cần Tech Lead quyết.

## Ảnh hưởng nếu chưa chốt

FR-L3GEN-003 và FR-L3GEN-004 hiện có AC cho Java (AC-003-06, AC-004-06) nhưng cố ý viết ở mức nguyên tắc, vì ma trận annotation chưa có. Không thể lập implementation target cho phần Java trước khi Tech Lead chốt mục 2 ở trên.

Pattern ngoài ma trận phải hiện ở phần giới hạn của kết quả, không im lặng bỏ qua.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.

