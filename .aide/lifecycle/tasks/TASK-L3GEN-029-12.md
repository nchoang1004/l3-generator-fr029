---
uid: "01M4PMXJCW8AX5JAWXVXS0NKN9"
key: TASK-L3GEN-029-12
type: task
group: normative
scope: lifecycle
status: draft
epic: EPIC-L3GEN-029
implements: [CMP-L3GEN-008, CMP-L3GEN-007, CMP-L3GEN-004]
change_request: CR-L3GEN-2026-009
---

# TASK-L3GEN-029-12 — File TAI-LIEU.md và các phần bổ sung của tài liệu

Lập ngày 12/10/2026. Chưa phải approval hoặc nghiệm thu độc lập.

## Việc làm
`slice/l3slice/tailieu.py`: một file `TAI-LIEU.md` 11 mục, có nhãn chắc chắn/suy luận/chưa rõ. Route thêm lỗi trả về, tags, deprecated, summary, ví dụ (bộ kiểm `_route_extras`). `slice/l3slice/docstatic.py`: thư viện, cấu hình, middleware, quan hệ component đọc tĩnh. Kind của component suy từ membership.

## Xong khi
- `slice/tests/test_tai_lieu.py`, `test_route_extras.py`, `test_static_parts.py` qua
- Repo held-out orderflow: giám khảo độc lập chấm, đầu ra đóng băng bằng hash trước khi chấm
- Người dùng chốt OQ-L3GEN-019 và OQ-L3GEN-020 (chưa có)

## Hiện trạng (12/10/2026)
Code và test đã có. Held-out orderflow (12/10, agent Claude đóng vai model): 23/23 route, 9/9 model; giám khảo 202/213 mục đúng, dễ dùng 3/5 trước khi sửa. Phần bổ sung chưa thuộc spec (OQ-L3GEN-020). Bằng chứng: `ket-qua-chay/heldout-orderflow-20261012/`, `docs/FR029-danh-gia-heldout-orderflow-20261012.md`. Chưa qua Component Merge Gate, chưa có MR.

## Bộ ba evidence
`evidence/context/CTX-TASK-L3GEN-029-12.yaml` · `evidence/plans/PLAN-TASK-L3GEN-029-12.md` · `evidence/diaries/DIARY-TASK-L3GEN-029-12.md`
