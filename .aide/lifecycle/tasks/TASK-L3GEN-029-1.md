---
uid: "01M3XY32Y8NH7G6MBN4EG6D09J"
key: TASK-L3GEN-029-1
type: task
group: normative
scope: lifecycle
status: draft
story: STORY-L3GEN-029-05
implements: [CMP-L3GEN-004, CMP-L3GEN-008]
---

# TASK-L3GEN-029-1

Nháp, chờ Architecture Gate BL-r10. Chưa phải approval hoặc nghiệm thu độc lập.

## Việc làm
Cảnh báo route không qua decorator.

## Xong khi
`slice/tests/test_fr029.py::test_non_decorator_routes_are_reported_individually` qua. Xem báo cáo và log tại `ket-qua-chay/fr029-20261002/`. Test code không thay review độc lập hoặc quyết định Gate.
