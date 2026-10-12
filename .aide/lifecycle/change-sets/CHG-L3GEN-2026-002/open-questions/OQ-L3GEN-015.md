---
uid: "01M4AR4TVNAVV219GCFCPFS3TV"
key: "OQ-L3GEN-015"
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
owner: "Hoàng (cần Khiêm xác nhận vì liên quan bộ nghiệm thu)"
due: "2026-10-10"
change_set: "CHG-L3GEN-2026-002"
derived_from: ["CR-L3GEN-2026-008"]
---

# OQ-L3GEN-015 — Đáp án nghiệm thu FR-029 cho repo kín: ai lập, ai duyệt, và vai trò của igorbenav

- **Blocking:** Công bố số nghiệm thu FR-029.

## Câu hỏi

Ngày 07/10/2026 đã đo FR-029 trên 4 repo kín nhỏ và vừa của OBS-L3GEN-001. Ba đáp án (tdd-docker, AgentGPT, kibo-backend) do agent Claude độc lập lập bằng oracle `app.openapi()` cộng đọc source, chưa có người review. Đáp án có đủ tư cách nghiệm thu không, và ai phải review?

## Dữ liệu đầu vào

| Vấn đề | Chi tiết |
|---|---|
| Người lập đáp án | OBS-L3GEN-001 rev 8 có quy định người lập và hạn của đáp án mới; ba đáp án mới do agent lập, không có người review |
| Lộ thông tin repo kín | Báo cáo của agent lập đáp án kibo-backend nêu vài loại phán đoán chi tiết, dù được yêu cầu chỉ báo số tổng |
| igorbenav | OBS-L3GEN-001 xếp là repo **kín** cỡ vừa (dùng nghiệm thu); APPROVAL-golden-v1-2026-10-04 xếp là "chỉnh prompt" |
| Phạm vi đáp án igorbenav | Golden v1 chỉ có route và tên model, không có tham số, trường model, vai trò file |

## Lựa chọn

1. Giữ đáp án agent, thêm một người review từng đáp án trước khi công bố số nghiệm thu.
2. Lập lại đáp án theo quy trình golden v1 (hai bản độc lập, giám khảo, người duyệt).
3. Thay igorbenav bằng repo kín khác nếu nó đã được dùng để chỉnh prompt.

Số đo ngày 07/10/2026 (`ket-qua-chay/fr029-accept-v13/`) giữ nguyên, ghi trạng thái chờ OQ này.
