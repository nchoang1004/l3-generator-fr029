---
uid: "01M4AR4TVN4GP7EEMHHP2BD0VA"
key: "OQ-L3GEN-014"
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
due: "2026-10-10"
change_set: "CHG-L3GEN-2026-002"
derived_from: ["CR-L3GEN-2026-008"]
---

# OQ-L3GEN-014 — Status khai trong thân handler có phải "status code khai trong code" của AC-029-02 không

- **Blocking:** AC-L3GEN-029-02 (phần status).

## Câu hỏi

AC-L3GEN-029-02 yêu cầu "ghi status code khai trong code". Status xuất hiện trong thân hàm (`raise HTTPException(status_code=404)`, `return Response(status_code=200)`) có tính không, hay chỉ tính status của decorator và mặc định của FastAPI?

## Dữ liệu đầu vào

| Nguồn | Nói gì |
|---|---|
| Gold fixture `file_roles` (agent G, phán đoán #16) | Không tính |
| Codex chấm mù (07/10/2026, hai lần) | Phải ghi 404 khi không tìm thấy |
| OpenAPI do FastAPI sinh | Không liệt kê status từ `HTTPException` |
| Code hiện tại | Không ghi |

## Lựa chọn

1. Chỉ status của decorator và mặc định (như code hiện tại).
2. Ghi thêm status trong thân hàm, nhãn riêng, không đưa vào khối OpenAPI.
