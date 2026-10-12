---
uid: "01M4FCDAPYBM0YCFC1VQ68A44K"
key: "OQ-L3GEN-017"
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

# OQ-L3GEN-017 — File trong `scripts/` chỉ import helper cùng thư mục có thuộc phạm vi đọc không

- **Blocking:** AC-L3GEN-029-08 (lời gọi HTTP trong script), phạm vi đọc của FR-L3GEN-028.

## Câu hỏi

FR-L3GEN-028 chỉ đọc file trong `scripts/` khi file đó "import code của repo". Script chỉ import một file helper nằm cùng thư mục `scripts/` (không import gói ứng dụng) có tính là import code của repo không?

## Dữ liệu đầu vào

| Nguồn | Nói gì |
|---|---|
| FR-L3GEN-028 "Phạm vi đọc" | Thư mục `scripts/` chỉ đọc khi file import code của repo |
| Code hiện tại (`ST.classify`) | Chỉ tính import gói cấp đầu của ứng dụng; helper cùng `scripts/` không tính |
| REVIEW-HELDOUT-L3GEN-2026-006 | Codex khi chấm lại caura tính 37 lời gọi HTTP trong 6 script `scripts/repro_*.py` là bỏ sót, vì chúng import `scripts/_env_compat.py` |

## Lựa chọn

1. Không tính (như hiện tại): helper trong cùng thư mục ngoài phạm vi thì cả nhóm ngoài phạm vi.
2. Tính: import bất kỳ file nào của repo, kể cả helper trong `scripts/`, là import code của repo.

Chọn 2 thì sửa FR-028 qua Product và `ST.classify`.
