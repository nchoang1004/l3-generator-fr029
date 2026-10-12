---
uid: "01M4PMS40KKZCBSWPS1WBXFEHK"
key: "OQ-L3GEN-021"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "open"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Hoàng"
due: "2026-10-19"
due_note: "Ngày đề xuất khi mở OQ (12/10/2026); owner chỉnh nếu cần."
change_set: "CHG-L3GEN-2026-002"
derived_from: ["CR-L3GEN-2026-009"]
---

# OQ-L3GEN-021 — Waiver NFR-SEC-002 / NFR-AI-002 có phủ các lần chạy 11/10 và chế độ oneshot không

- **Blocking:** mọi lần chạy thật tiếp theo với model ngoài.

## Câu hỏi

Waiver ở CR-L3GEN-2026-008-decisions-01 ghi phạm vi "các lần chạy thử và đo ngày 07/10/2026". Ngày 11/10 có 5 lần chạy thật với OpenAI (3 lần gpt-4.1-mini, mỗi lần 3 request; 2 lần gpt-5, mỗi lần 2 request, request thứ 3 bị chặn vì trần tiền), tổng 0,442 USD. Chế độ oneshot gửi nguyên source trong request đầu, nên luôn trái NFR-SEC-002 ("không gửi nguyên file"). Người dùng đã duyệt trần tiền từng lần (CR-009) nhưng không nói về waiver.

## Dữ liệu đầu vào

| Nguồn | Nói gì |
|---|---|
| CR-L3GEN-2026-008-decisions-01 | "3 quy tắc này bỏ qua hết"; phạm vi 07/10; `rule_owner_confirmation`: chưa có |
| CR-L3GEN-2026-009 `decisions_verbatim` | Trần 0,20 USD và 0,30 USD; "Chạy (Khuyên)"; "Có, trần 0,30 USD" |
| `ket-qua-chay/oneshot-20261011*` | Số request, token, tiền của từng lần chạy |

## Lựa chọn

1. **Nới waiver**: phủ CHG-L3GEN-2026-002 tới khi đóng; người sở hữu NFR (Khiêm nếu không phải Hoàng) xác nhận.
2. **Sửa NFR qua Product** để hướng agent/oneshot thành chuẩn.
3. **Dừng chạy thật** tới khi có 1 hoặc 2; chỉ test bằng agent đóng vai model (không gọi API).
