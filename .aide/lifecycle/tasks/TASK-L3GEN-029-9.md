---
uid: "01M4FCDAQ0S8B4EM0DS5NJ405Y"
key: TASK-L3GEN-029-9
type: task
group: normative
scope: lifecycle
status: draft
epic: EPIC-L3GEN-029
implements: [CMP-L3GEN-007]
change_request: CR-L3GEN-2026-008
---

# TASK-L3GEN-029-9 — Công cụ đo bộ kiểm (gold audit, bộ kiểm giả, gói held-out)

Ghi muộn ngày 09/10/2026: việc đã làm 07–09/10/2026 trước khi có Task (DIARY-CR-L3GEN-2026-008, mục 'Đi chệch'). Chưa phải approval hoặc nghiệm thu độc lập.

## Việc làm
Công cụ `slice/tools/fr029_checkaudit.py`: đóng vai agent trả lời đúng gold rồi trả lời sai có chủ ý; chạy bộ kiểm giả; xuất gói cho giám khảo độc lập chấm repo chưa dùng.

## Xong khi
- Mỗi chỉ số lỗi của gold audit khác 0 khi chạy `--sanity accept` hoặc `--sanity reject`
- `summary.json` ghi hash của docfacts.py, astscan.py, fr029_checkaudit.py
- `--heldout` xuất gói không gộp sai (dependency cùng tên ở hai module tách mục)

## Hiện trạng (09/10/2026)
Code và test đã có; số đo gold r41: Bộ kiểm giả bị bắt ở mọi chỉ số (r41); không có task AC nên không có AC đo. Bằng chứng: `.aide/evidence/tests/fr029-checker-20261009/`. Review: `REVIEW-CODE-L3GEN-2026-001` … `012`, `REVIEW-HELDOUT-L3GEN-2026-001` … `007`. Chưa qua Component Merge Gate, chưa có MR.

## Bộ ba evidence
`evidence/context/CTX-TASK-L3GEN-029-9.yaml` · `evidence/plans/PLAN-TASK-L3GEN-029-9.md` · `evidence/diaries/DIARY-TASK-L3GEN-029-9.md`
