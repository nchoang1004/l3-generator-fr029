---
uid: "01M4PMXJCTK80DGXSS180ADXYE"
key: TASK-L3GEN-029-11
type: task
group: normative
scope: lifecycle
status: draft
epic: EPIC-L3GEN-029
implements: [CMP-L3GEN-007]
change_request: CR-L3GEN-2026-009
---

# TASK-L3GEN-029-11 — Sửa bộ kiểm theo review 11/10 (8 mục)

Lập ngày 12/10/2026. Chưa phải approval hoặc nghiệm thu độc lập.

## Việc làm
Sửa `slice/l3slice/docfacts.py`, `render.py` theo 8 lỗi của bản review Codex 11/10 mà người dùng duyệt sửa ("1–8 theo thứ tự"): (1) đòi vai trò cho file rỗng; (2) `Depends(Provide[...])` không đặt tên được; (3) tham số trùng, OpenAPI hỏng vẫn ready; (4) giá trị ở phần dòng bị cắt vẫn được nhận; (5) auth không có căn cứ vẫn known; (6) body JSON không có model; (7) đường gọi Service không có cạnh gọi; (8) kiểu/required/nullable của model không so với source. Bảng sửa ở `docs/HANDOFF.md`, mục "Sửa 8 lỗi bộ kiểm theo review 11/10". Không thêm AC; sửa trên AC đã có của STORY-L3GEN-029-01/02/05/08.

## Xong khi
- Mỗi lỗi có test đỏ trước trong `slice/tests/test_review_20261011.py`, nay qua
- `fr029_checkaudit` không đổi số so với trước khi sửa
- Trường model đúng của gold: 0/348 bị từ chối sai

## Hiện trạng (12/10/2026)
Code và test đã có; suite 520/521 (lỗi `test_gateway` có từ trước). Đường gọi Service: 1/16 mục gold bị từ chối sai (ghi ở REVIEW-CODE-L3GEN-2026-013). Bằng chứng: `.aide/evidence/tests/fr029-code-review-20261011/`, `fr029-review-20261011-*.log`. Chưa qua Component Merge Gate, chưa có MR.

## Bộ ba evidence
`evidence/context/CTX-TASK-L3GEN-029-11.yaml` · `evidence/plans/PLAN-TASK-L3GEN-029-11.md` · `evidence/diaries/DIARY-TASK-L3GEN-029-11.md`
