---
uid: "01M4AR4TVM4HJW98EEA0NK6V2J"
key: "OQ-L3GEN-013"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "open"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Hoàng"
due: "2026-10-10"
change_set: "CHG-L3GEN-2026-002"
derived_from: ["CR-L3GEN-2026-008"]
---

# OQ-L3GEN-013 — Route khai trong file production nhưng router không được gắn vào app nào

- **Blocking:** AC-L3GEN-029-01, AC-L3GEN-029-05 (gold và cách chấm route không gắn app).

## Câu hỏi

Route khai bằng decorator trong file production, nhưng router của nó không được gắn vào application nào trong phạm vi phân tích (chỉ gắn trong `conftest.py`, hoặc qua hàm không đăng ký thật). Route đó có vào tài liệu API không?

## Dữ liệu đầu vào

| Nguồn | Nói gì |
|---|---|
| FR-L3GEN-029 mục "Chia theo component" | Chỉ loại "route khai trong file test hoặc thư mục nằm ngoài phạm vi phân tích"; mục "Khi chưa đủ dữ kiện": xuất phần biết được |
| Kế hoạch A05 (`docs/L3-ke-hoach-agent-sinh-tai-lieu.md`) | "Không xuất route chỉ được gắn qua registration nằm trong test" |
| Gold fixture `exclusions` (agent G) và golden v1 case `orders-wrapper-fake` | Không ghi route |
| Codex review gold và chấm mù (07/10/2026) | Theo FR-029 thì phải giữ, path `unknown` |

Câu hỏi xuất hiện 4 lần trong phiên 07/10/2026.

## Lựa chọn

1. Giữ route, path `unknown` kèm lý do "router không được gắn vào app nào" (theo chữ FR-029).
2. Loại route, ghi một dòng ở phần giới hạn kèm `file:dòng` (theo kế hoạch A05 và gold hiện có).

Đổi theo lựa chọn nào thì sửa FR-029 (nếu cần) qua Product, rồi sửa gold tương ứng; không sửa gold trước.

## Ghi chú 09/10/2026 (revision 2): code đang quyết thay một phần

Ghi theo EXEC §B.15 luật 1 (agent không tự quyết điều đang chờ OQ). Đợt 07–09/10/2026 (CR-L3GEN-2026-008) thêm vào bộ kiểm `slice/l3slice/docfacts.py` phần kiểm đăng ký (`_registration_problems`). Khi agent khai một route thuộc app X nhưng router của nó không được `include_router`/`mount` vào X trong snapshot, claim bị từ chối với lỗi "không được include_router/mount vào X".

- Không chạm lựa chọn 1 hay 2 ở trên: route vẫn nộp được dạng "chưa gắn app" (`DF.add_route`, quy tắc 7.18 trong `docs/FR029-quy-tac.md`).
- Nhưng nó loại cách ghi route "gắn" vào app khi không có đăng ký thật. Khi chốt OQ này, cần xem lại luật đó cho khớp.
- Code không bị đổi để chờ quyết định; câu hỏi không đổi.

