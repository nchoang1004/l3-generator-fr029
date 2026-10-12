---
uid: "01M4FCDAPZSAH535AY4ZQCK0QJ"
key: TASK-L3GEN-029-6
type: task
group: normative
scope: lifecycle
status: draft
story: STORY-L3GEN-029-01
implements: [CMP-L3GEN-007]
change_request: CR-L3GEN-2026-008
---

# TASK-L3GEN-029-6 — Bộ kiểm route và đăng ký của luồng agent

Lập ngày 09/10/2026. Chưa phải approval hoặc nghiệm thu độc lập.

## Việc làm
Kiểm route agent nộp: decorator đúng handler và method, receiver là FastAPI/APIRouter, router nằm dưới app được khai, prefix đủ, đúng thứ tự, đúng literal.

## Xong khi
- `python -m unittest tests.test_checker_counterexamples` (trong `slice/`) qua toàn bộ
- Gold audit (`slice/tools/fr029_checkaudit.py`): `routes_false_rejection`, `routes_false_acceptance`, `registration_false_rejection`, `prefix_missing_accepted`, `prefix_none_rejected` đều bằng 0
- Bộ kiểm giả `--sanity accept` và `--sanity reject` làm các chỉ số trên khác 0

## Hiện trạng (09/10/2026)
Code và test đã có; số đo gold r41: 0/406 route đúng bị từ chối; 0/1.549 route sai được nhận; 0/131 thiếu prefix được nhận; 0/408 route gold bị coi là chưa đăng ký. Bằng chứng: `.aide/evidence/tests/fr029-checker-20261009/`. Review: `REVIEW-CODE-L3GEN-2026-001` … `012`, `REVIEW-HELDOUT-L3GEN-2026-001` … `007`. Chưa qua Component Merge Gate, chưa có MR.

## Bộ ba evidence
`evidence/context/CTX-TASK-L3GEN-029-6.yaml` · `evidence/plans/PLAN-TASK-L3GEN-029-6.md` · `evidence/diaries/DIARY-TASK-L3GEN-029-6.md`
