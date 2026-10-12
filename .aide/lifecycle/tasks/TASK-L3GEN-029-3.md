---
uid: "01M3XY32YE5FF619EEVK37K895"
key: TASK-L3GEN-029-3
type: task
group: normative
scope: lifecycle
status: draft
story: STORY-L3GEN-029-08
implements: [CMP-L3GEN-004, CMP-L3GEN-008]
---

# TASK-L3GEN-029-3

Nháp, chờ Architecture Gate BL-r10. Chưa phải approval hoặc nghiệm thu độc lập.

## Việc làm
Đọc HTTP client theo phạm vi biến.

## Xong khi
`slice/tests/test_fr029.py::test_client_scopes_do_not_turn_database_get_into_http` qua. Xem báo cáo và log tại `ket-qua-chay/fr029-20261002/`. Test code không thay review độc lập hoặc quyết định Gate.
