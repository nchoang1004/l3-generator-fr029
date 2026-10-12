---
uid: "01M4AR4TVMXZJ302H41MR8GSPA"
key: "OQ-L3GEN-012"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "answered"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Hoàng (cần Khiêm xác nhận vì đổi NFR đã duyệt)"
due: "2026-10-10"
change_set: "CHG-L3GEN-2026-002"
derived_from: ["CR-L3GEN-2026-008"]
---

# OQ-L3GEN-012 — Luồng "agent thuần" của FR-029 trái NFR-SEC-002, NFR-AI-002 và OQ-L3GEN-009

- **Blocking:** FR-L3GEN-029 (mọi việc triển khai và đo tiếp của luồng agent).

## Câu hỏi

Người dùng chọn hướng "agent thuần" cho FR-029 (CR-L3GEN-2026-008): model tự đọc source qua công cụ, code chỉ kiểm bằng chứng. Hướng này đã được cài đặt và chạy trên repo thật. Nó mâu thuẫn với các spec đã duyệt dưới đây. Giữ hướng agent thuần (thì phải sửa NFR qua change request) hay quay về phạm vi gửi dữ liệu mà NFR đang cho phép?

## Mâu thuẫn cụ thể

| Spec đã duyệt | Quy định | Luồng agent đang làm |
|---|---|---|
| NFR-L3GEN-SEC-002 (FR-029 `constrained_by`) | "Không gửi nguyên file source hoặc cả repository"; dữ liệu gửi đúng danh sách của NFR-AI-002 | Gửi nguyên nội dung mọi file trong phạm vi đọc, từng đoạn tối đa 200 dòng (`slice/l3slice/source_tools.py`) |
| NFR-L3GEN-AI-002 | Provider OpenRouter, model `openai/gpt-6-luna`; tối đa 4 request mỗi việc | Gọi OpenAI trực tiếp (Responses API); từ 6 tới 175 lượt mỗi lần chạy |
| OQ-L3GEN-009 (đã đóng) | Trần mỗi lần chạy 0,20 USD và 300.000 token | Repo cỡ vừa tốn tới 0,49 USD; repo lớn dùng hơn 22 triệu token |
| NFR-L3GEN-AI-002 | Model chỉ làm việc chia nhóm/đặt tên cho FR-028 | Model tự xác định dữ kiện API của FR-029 |

## Vì sao chưa phát hiện sớm

Kế hoạch `docs/L3-ke-hoach-agent-sinh-tai-lieu.md` (mục N1) đã ghi "cần đồng bộ NFR-AI/SEC", nhưng không tạo OQ và không dừng trước khi code, trái EXEC §B.15 luật 1 ("Agent không sửa spec. Mâu thuẫn → tạo OQ và dừng").

## Lựa chọn

1. **Giữ agent thuần:** mở change request sửa NFR-SEC-002 (cho gửi nguyên file trong phạm vi đọc, có che bí mật), NFR-AI-002 (provider, số request, việc model được làm), trần chi phí của OQ-009; qua Scope Gate rồi mới đo nghiệm thu lại.
2. **Quay về phạm vi NFR hiện tại:** code trích dữ kiện, model chỉ xử lý phần NFR cho phép; luồng agent giữ làm thí nghiệm, không công bố là sản phẩm.
3. **Kết hợp:** chỉ gửi model các đoạn code liên quan route/model/HTTP thay vì nguyên file; vẫn phải sửa NFR vì vượt danh sách hiện có.

## Trạng thái tạm

Từ 07/10/2026 dừng chạy thêm luồng agent trên repo thật cho tới khi OQ này đóng. Mọi số đo đã có (`ket-qua-chay/fr029-pilot-20261007/`, `ket-qua-chay/fr029-accept-v13/`) ghi là đo trên cấu hình ngoài spec.

## Trả lời ngày 07/10/2026 (revision 2)

Hoàng: "3 quy tắc này bỏ qua hết" (CR-L3GEN-2026-008-decisions-01). Ghi nhận là **waiver** theo EXEC §D.4 cho luồng agent FR-029 trong Change Set này, không phải sửa spec: text của NFR-L3GEN-SEC-002, NFR-L3GEN-AI-002 và OQ-L3GEN-009 giữ nguyên.

Còn thiếu để waiver đủ điều kiện §D.4: lý do khác rỗng, và xác nhận của tầng sở hữu rule (Khiêm, nếu Hoàng không sở hữu hai NFR). Trạng thái để `answered`, chưa `closed`.
