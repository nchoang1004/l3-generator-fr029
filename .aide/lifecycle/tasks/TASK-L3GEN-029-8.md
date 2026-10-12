---
uid: "01M4FCDAPZ4ZWCPJFVH6MNHNKB"
key: TASK-L3GEN-029-8
type: task
group: normative
scope: lifecycle
status: draft
story: STORY-L3GEN-029-08
implements: [CMP-L3GEN-007]
change_request: CR-L3GEN-2026-008
---

# TASK-L3GEN-029-8 — Bộ kiểm lời gọi HTTP và dòng nghi ngờ

Lập ngày 09/10/2026. Chưa phải approval hoặc nghiệm thu độc lập.

## Việc làm
Kiểm lời gọi HTTP agent nộp (receiver, thư viện, method, URL, khóa cấu hình, config_at); đánh dấu dòng trông như route, đăng ký hay lời gọi HTTP mà agent chưa nộp.

## Xong khi
- `python -m unittest tests.test_checker_counterexamples` qua toàn bộ
- Gold audit: `http_false_rejection`, `http_false_acceptance`, `http_negative_accepted`, `gold_items_not_flagged` đều bằng 0
- So gói held-out trước và sau mỗi lần sửa: không thêm dòng nhiễu chưa giải thích

## Hiện trạng (09/10/2026)
Code và test đã có; số đo gold r41: 0/33 lời gọi đúng bị từ chối; 0/125 lời gọi sai được nhận; 0/33 ca không phải HTTP được nhận; 0/441 mục gold không bị đánh dấu; 4 dòng thừa. Bằng chứng: `.aide/evidence/tests/fr029-checker-20261009/`. Review: `REVIEW-CODE-L3GEN-2026-001` … `012`, `REVIEW-HELDOUT-L3GEN-2026-001` … `007`. Chưa qua Component Merge Gate, chưa có MR.

## Bộ ba evidence
`evidence/context/CTX-TASK-L3GEN-029-8.yaml` · `evidence/plans/PLAN-TASK-L3GEN-029-8.md` · `evidence/diaries/DIARY-TASK-L3GEN-029-8.md`
