---
uid: "01M4PMXJCX6KN3P49YGDBHXWY7"
key: TASK-L3GEN-029-13
type: task
group: normative
scope: lifecycle
status: draft
epic: EPIC-L3GEN-029
implements: [CMP-L3GEN-008]
change_request: CR-L3GEN-2026-009
---

# TASK-L3GEN-029-13 — Giao diện web để demo

Lập ngày 12/10/2026 trước khi code; plan viết trước (EXEC §B.14). Chưa phải approval hoặc nghiệm thu độc lập.

## Việc làm
Sửa giao diện `slice/l3slice/docweb.py` và `slice/l3slice/docui/` để demo: xem `TAI-LIEU.md`, chọn chế độ agent/oneshot, xem file TBL/EVT. Làm theo skill `taste-skill` (CLAUDE.md). Plan viết trước khi code: PLAN-TASK-L3GEN-029-13.

## Xong khi
- Test DOM `slice/tests/ui/docui.test.cjs` và `slice/tests/test_docweb.py` qua
- Chạy được một lần demo không gọi API (mở kết quả có sẵn) theo `docs/HUONG-DAN-DEMO.md`

## Hiện trạng (12/10/2026)
Đã làm (12/10/2026): xem TAI-LIEU.md dạng tài liệu (bảng, tiêu đề), mở sẵn khi chạy xong, nhóm file theo loại, chọn chế độ agent/oneshot (`mode` ở `docweb.py`). Test DOM 6/6, `test_docweb` 11/11, suite 522/523 (lỗi `test_gateway` cũ). Đã chụp bằng Edge ở 1440/600/390 px. Chế độ oneshot qua giao diện mới chỉ test bằng mock, chưa chạy model thật. Chưa qua Component Merge Gate, chưa có MR.

## Bộ ba evidence
`evidence/context/CTX-TASK-L3GEN-029-13.yaml` · `evidence/plans/PLAN-TASK-L3GEN-029-13.md` · `evidence/diaries/DIARY-TASK-L3GEN-029-13.md`
