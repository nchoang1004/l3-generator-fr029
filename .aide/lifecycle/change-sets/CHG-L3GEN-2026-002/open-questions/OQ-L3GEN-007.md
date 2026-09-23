---
uid: "01M3632TDCAVXX8ND5BB6F53M0"
key: "OQ-L3GEN-007"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "closed"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Khiêm và Hoàng"
due: "2026-09-22"
change_set: "CHG-L3GEN-2026-002"
---

# OQ-L3GEN-007 — Ngưỡng độ đúng khi dùng mô hình ngôn ngữ

## Câu hỏi

BL-r14 đặt precision 90% cho bộ luật tĩnh, vốn cho cùng kết quả mỗi lần chạy. Khi mô hình ngôn ngữ đề xuất component và quan hệ, sai số có dạng khác. Ngưỡng precision và recall, và ngưỡng cho nhãn mức chắc chắn, là bao nhiêu?

## Quyết định ngày 22/09/2026

**Người quyết định:** Khiêm và Hoàng.

- Precision và recall từ 80% trở lên cho mọi nhóm: route, entity/table, HTTP, config, event, thư viện, thành viên component, cạnh dependency.
- Nhãn khớp đáp án từ 80% trở lên.
- Tỷ lệ gán `exact` cho kết luận sai ở mức 5% trở xuống; đây là chỉ số chặn.

Ngưỡng ghi tại [NFR-L3GEN-ACC-002](../../../../requirements/nfr/NFR-L3GEN-ACC-002.md). OQ này không đặt số ở chỗ khác.

- **Blocking:** không còn.
- **Trạng thái:** closed.
