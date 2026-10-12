---
uid: "01M4FCDAPX2B8HPX8QZ5EXE8FX"
key: "OQ-L3GEN-016"
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

# OQ-L3GEN-016 — Lời gọi qua hàm bọc của dự án có tính là "lời gọi HTTP ra ngoài" không

- **Blocking:** AC-L3GEN-029-08 (danh sách lời gọi HTTP ra ngoài và cách chấm).

## Câu hỏi

AC-L3GEN-029-08 yêu cầu ghi các lời gọi HTTP ra ngoài kèm bằng chứng. Khi dự án tự viết hàm hoặc lớp bọc, ví dụ `http_retry.get(url)` gọi tiếp `httpx.request(...)`, thì ghi lời gọi ở dòng nào: dòng gọi hàm bọc (có URL thật), dòng bên trong hàm bọc (gọi thư viện, URL là biến), hay cả hai?

## Dữ liệu đầu vào

| Nguồn | Nói gì |
|---|---|
| FR-L3GEN-029, AC-08 | "Lời gọi HTTP ra ngoài cùng bằng chứng"; không nói về hàm bọc |
| Bộ kiểm hiện tại (`slice/l3slice/astscan.py`) | Chỉ tính lời gọi trực tiếp httpx/requests/aiohttp; lời gọi bên trong hàm bọc bị đánh dấu nghi ngờ |
| REVIEW-HELDOUT-L3GEN-2026-001, -003, -004 | Giám khảo gặp hàm bọc ở dispatch (`ZoomClient`), case_auto_hub (`HttpxClient`), shortlist (`http_retry`); hai phiên chấm hiểu khác nhau |

## Lựa chọn

1. Chỉ tính lời gọi trực tiếp thư viện (như hiện tại). URL ở dòng gọi hàm bọc không có trong tài liệu.
2. Tính cả dòng gọi hàm bọc khi truy được tới lời gọi thư viện trong snapshot; ghi cả hai vị trí.
3. Chỉ tính dòng gọi hàm bọc; dòng bên trong hàm bọc ghi là chi tiết cài đặt.

Chọn 2 hoặc 3 thì sửa FR-029 qua Product, thêm luật cho bộ kiểm và gold, rồi đo lại.
