---
uid: "01M4PMS40JV94HCJ0RGZZF3FDX"
key: "OQ-L3GEN-019"
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

# OQ-L3GEN-019 — Phần bảng, sự kiện, thư viện, cấu hình do code đọc tĩnh: có được không

- **Blocking:** không chặn code đang chạy; chặn việc ghi phần này vào CMP-L3GEN-006/007 và ADR.

## Câu hỏi

Ngày 11/10, khi làm "làm đi", Claude cho code đọc tĩnh (không qua model) các phần: bảng CSDL (FR-030), sự kiện (FR-031), thư viện, cấu hình, middleware, quan hệ giữa component. File: `slice/l3slice/docstatic.py`, `extract.py`. Phần API vẫn do model đề xuất, code kiểm (ADR-2026-006). CR-L3GEN-2026-008 ghi "tôi nghĩ là agent thuần" cho FR-029. Cách chia này có được chấp nhận không?

## Dữ liệu đầu vào

| Nguồn | Nói gì |
|---|---|
| CR-L3GEN-2026-008 `decisions_verbatim` | "tôi nghĩ là agent thuần" (nói về luồng API FR-029) |
| FR-L3GEN-030, FR-L3GEN-031 | Không nói phần này do model hay code làm |
| `docs/FR030-kiem-csdl-20261012.md` | Đọc tĩnh: 32/32 bảng, 341/341 cột khớp gold trên 4 repo; không tốn token |
| OQ-L3GEN-018 | Câu hỏi gần: bộ kiểm phân tích tĩnh sâu tới đâu |

## Lựa chọn

1. **Giữ đọc tĩnh cho FR-030/031 và các phần phụ** (cách đang làm). Ghi vào CMP-L3GEN-007 và một ADR: model chỉ làm phần API.
2. **Chuyển sang model đề xuất, code kiểm** như API. Tốn token; phải viết thêm bộ kiểm cho bảng và sự kiện.
3. **Bỏ các phần phụ** (thư viện, cấu hình, middleware, quan hệ component); chỉ giữ bảng và sự kiện vì có FR.
