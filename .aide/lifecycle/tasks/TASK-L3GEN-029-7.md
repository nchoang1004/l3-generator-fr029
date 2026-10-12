---
uid: "01M4FCDAPZD5081DVXKVHCW2MX"
key: TASK-L3GEN-029-7
type: task
group: normative
scope: lifecycle
status: draft
story: STORY-L3GEN-029-02
implements: [CMP-L3GEN-007]
change_request: CR-L3GEN-2026-008
---

# TASK-L3GEN-029-7 — Bộ kiểm và lời nhắc tham số dependency

Lập ngày 09/10/2026. Chưa phải approval hoặc nghiệm thu độc lập.

## Việc làm
Kiểm tên dependency là đích của Depends; nhắc tham số do dependency khai (lồng, class, instance, partial, model Pydantic, alias, cấp router/app) và dependency agent chưa nộp.

## Xong khi
- `python -m unittest tests.test_checker_counterexamples` qua toàn bộ
- Gold audit: `dependency_false_rejection`, `dependency_false_acceptance`, `reminders_wrong`, `dep_params_missed` đều bằng 0
- Bộ kiểm giả làm các chỉ số trên khác 0

## Hiện trạng (09/10/2026)
Code và test đã có; số đo gold r41: 0/169 dependency đúng bị từ chối; 0/333 dependency sai được nhận; 0 lời nhắc sai, 0/69 tham số gold bị sót. Bằng chứng: `.aide/evidence/tests/fr029-checker-20261009/`. Review: `REVIEW-CODE-L3GEN-2026-001` … `012`, `REVIEW-HELDOUT-L3GEN-2026-001` … `007`. Chưa qua Component Merge Gate, chưa có MR.

## Bộ ba evidence
`evidence/context/CTX-TASK-L3GEN-029-7.yaml` · `evidence/plans/PLAN-TASK-L3GEN-029-7.md` · `evidence/diaries/DIARY-TASK-L3GEN-029-7.md`
