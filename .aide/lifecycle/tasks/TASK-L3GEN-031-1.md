---
uid: "01M4PMXJD3YDK7TMH5NYN61PTV"
key: TASK-L3GEN-031-1
type: task
group: normative
scope: lifecycle
status: draft
story: STORY-L3GEN-031-01
implements: [CMP-L3GEN-004, CMP-L3GEN-008]
change_request: CR-L3GEN-2026-009
---

# TASK-L3GEN-031-1 — Đọc sự kiện Celery, BackgroundTasks và xuất EVT

Ghi muộn ngày 12/10/2026: việc đã làm 11–12/10/2026 trước khi có Task (DIARY-CR-L3GEN-2026-009). Chưa phải approval hoặc nghiệm thu độc lập.

## Việc làm
`slice/l3slice/extract.py`: `_task_events` (Celery `@task`/`@shared_task`, `.delay`, `.apply_async`, `send_task`; `BackgroundTasks.add_task`); Redis pub/sub ghi cảnh báo `QUEUE_LIBRARY_UNSUPPORTED`. `docstatic.event_edges` nối bên gửi với bên nhận khi cùng hàm tác vụ.

## Xong khi
- `slice/tests/test_events_tasks.py` qua
- Held-out orderflow: điểm gửi/nhận khớp source (giám khảo)

## Hiện trạng (12/10/2026)
Code và test đã có. Held-out orderflow: giám khảo ghi 1 mục sự kiện sai (REVIEW-HELDOUT-L3GEN-2026-008). Chưa so gold sự kiện riêng (gold 4 repo không có sự kiện). Chưa qua Component Merge Gate, chưa có MR.

## Bộ ba evidence
`evidence/context/CTX-TASK-L3GEN-031-1.yaml` · `evidence/plans/PLAN-TASK-L3GEN-031-1.md` · `evidence/diaries/DIARY-TASK-L3GEN-031-1.md`
