---
uid: "01M4FCDAPYECX9MCT059JTCMSB"
key: "OQ-L3GEN-018"
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
due: "2026-10-16"
due_note: "Ngày đề xuất khi mở OQ (09/10/2026); owner chỉnh nếu cần."
change_set: "CHG-L3GEN-2026-002"
derived_from: ["CR-L3GEN-2026-008"]
---

# OQ-L3GEN-018 — Bộ kiểm bằng chứng được phân tích tĩnh sâu tới đâu mà vẫn là "agent thuần"

- **Blocking:** ADR-2026-006 (chờ quyết định này trước khi đem ra Architecture Gate).

## Câu hỏi

CR-L3GEN-2026-008 ghi người dùng chọn "agent thuần": model xác định mọi dữ kiện API, code chỉ kiểm bằng chứng. Qua đợt 07–09/10/2026, bộ kiểm (`docfacts.py`, `astscan.py`) đã dựng đồ thị `include_router`, theo client HTTP qua nhiều file, và nhắc tham số, dependency mà agent chưa nộp. Code vẫn không tự tạo mục nào, nhưng ranh giới với một bộ trích dữ kiện tĩnh đang mờ dần. Ranh giới nào là đúng?

## Dữ liệu đầu vào

| Nguồn | Nói gì |
|---|---|
| CR-L3GEN-2026-008 `decisions_verbatim` | "tôi nghĩ là agent thuần" |
| CHG-L3GEN-2026-002 `label` | "mô hình ngôn ngữ đề xuất, code kiểm bằng chứng" |
| CR-L3GEN-2026-008-requests-02 | 08/10: "chương trình này của tôi là cho agent đcọ repo đúng không chứ không phải code tĩnh đúng k ?" (chưa có câu trả lời quyết định) |
| `docs/FR029-bao-cao-kiem-bo-kiem-20261008.md` | Bộ kiểm làm 3 việc: từ chối bằng chứng sai, đánh dấu dòng nghi ngờ, nhắc tham số |

## Lựa chọn

1. **Chỉ từ chối hoặc nhắc, không tạo mục** (cách đang làm). Ghi thành ràng buộc trong ADR-2026-006 và CMP-L3GEN-007, kèm một test chặn: không đường code nào của bộ kiểm tạo route, tham số hay lời gọi HTTP.
2. **Lai:** cho code trích sẵn dữ kiện để agent xác nhận hoặc sửa. Nhanh và rẻ hơn, nhưng là bỏ hướng agent thuần; cần sửa CR-008 và NFR liên quan.
3. **Thu hẹp:** bỏ dòng nghi ngờ và lời nhắc sâu, chỉ giữ kiểm dòng dẫn như bản ngày 07/10. Sát "agent thuần" hơn, nhưng mất phần lớn khả năng chống bỏ sót đã đo được.
