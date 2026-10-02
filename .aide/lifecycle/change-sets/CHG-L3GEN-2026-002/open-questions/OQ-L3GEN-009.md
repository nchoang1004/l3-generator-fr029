---
uid: "01M3XEQNK05MMFX2WXNH96DZ80"
key: "OQ-L3GEN-009"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "closed"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Khiêm"
due: "2026-10-03"
change_set: "CHG-L3GEN-2026-002"
---

# OQ-L3GEN-009 — Model trả phí và trần chi phí mỗi lần chạy

## Câu hỏi

OQ-L3GEN-008 chốt hai model ở gói miễn phí, trần chi phí 0 đồng. Từ 30/09/2026 nhóm chạy thử qua OpenRouter (trả phí) và từ 01/10/2026 dùng `openai/gpt-6-luna`. Model có còn bắt buộc không, và trần chi phí mỗi lần chạy là bao nhiêu?

## Dữ liệu đầu vào

| Nguồn | Số |
|---|---|
| Giá `openai/gpt-6-luna` trên OpenRouter, tra 01/10/2026 | 0,10 USD mỗi triệu token vào, 0,50 USD mỗi triệu token ra |
| Bước gộp nhóm và đặt tên component, 5 repo nhỏ, 02/10/2026 | 7 request, khoảng 25.000 token, 0,008 USD |
| Pipeline v8 cả bộ bước AI, 8 repo × 2 cách, gpt-oss-120b, 30/09/2026 | 93 request, 640.076 token, 0,079 USD |

## Đã quyết (Khiêm, 02/10/2026, CR-L3GEN-2026-004)

- Model **bắt buộc**, **trả phí ít**.
- Provider OpenRouter, model `openai/gpt-6-luna` (đã dùng từ 01/10/2026).

## Trần mỗi lần chạy (Khiêm, 02/10/2026)

Revision 4 của NFR-L3GEN-AI-002 ghi đề xuất của agent: ≤ 0,05 USD và ≤ 100.000 token. Khiêm sửa thành **≤ 0,20 USD và ≤ 300.000 token mỗi lần chạy**. Khiêm chốt thêm ba trần còn lại: ≤ 4 request, câu trả lời ≤ 12.000 token, timeout 300 giây mỗi request (revision 3 của OQ này, theo finding F13 của REVIEW-SCOPE-L3GEN-2026-003). Số ghi tại NFR-L3GEN-AI-002 revision 6; OQ này không đặt số ở chỗ khác.

- **Blocking:** không còn.
- **Trạng thái:** closed.
