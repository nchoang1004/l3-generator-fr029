---
uid: "01M4PMXJCTWGM7F36FG22K6EDD"
key: TASK-L3GEN-029-10
type: task
group: normative
scope: lifecycle
status: draft
epic: EPIC-L3GEN-029
implements: [CMP-L3GEN-006, CMP-L3GEN-001]
change_request: CR-L3GEN-2026-009
---

# TASK-L3GEN-029-10 — Chế độ đọc một lần (oneshot), schema nộp dữ kiện, checkpoint

Ghi muộn ngày 12/10/2026: việc đã làm 11–12/10/2026 trước khi có Task (DIARY-CR-L3GEN-2026-009). Chưa phải approval hoặc nghiệm thu độc lập.

## Việc làm
`run_oneshot` trong `slice/l3slice/docagent.py`: gửi cả source trong request 1, ép model gọi `submit_findings` (`tool_choice`), tối đa 2 vòng sửa chỉ gửi mục bị từ chối kèm dòng source được trích. `--mode oneshot`, `--checkpoint` trong `__main__.py` và `docpipeline.run_documents`. Chạy tiếp từ checkpoint thì kiểm lại mọi mục đã lưu.

## Xong khi
- Test `OneShot` trong `slice/tests/test_docagent.py` qua (mock provider, không gọi API)
- Một lần chạy thật trên Teamhide trong trần người dùng duyệt (0,20 rồi 0,30 USD) có `cost.json`, `checkpoint.json`
- Chạy lại từ checkpoint không gọi lại model cho mục đã nhận

## Hiện trạng (12/10/2026)
Code và test đã có. Đo thật 11/10 (Teamhide): gpt-4.1-mini 0/5 route; gpt-5 4/5 route, 0,168–0,192 USD, 2 request mỗi lần (request thứ 3 bị chặn vì trần). Prompt v6 (sau sửa) chưa chạy thật. Bằng chứng: `ket-qua-chay/oneshot-20261011*`. Chưa qua Component Merge Gate, chưa có MR.

## Bộ ba evidence
`evidence/context/CTX-TASK-L3GEN-029-10.yaml` · `evidence/plans/PLAN-TASK-L3GEN-029-10.md` · `evidence/diaries/DIARY-TASK-L3GEN-029-10.md`
