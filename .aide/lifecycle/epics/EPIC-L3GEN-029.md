---
uid: "01M3XY32Y5WE1FXA857HFY3AC6"
key: EPIC-L3GEN-029
type: epic
group: normative
scope: lifecycle
status: draft
change_set: CHG-L3GEN-2026-002
accountable_team: TEAM-L3GEN
implements: [FR-L3GEN-029]
affected_components: [CMP-L3GEN-004, CMP-L3GEN-006, CMP-L3GEN-007, CMP-L3GEN-008]
contracts: {produces: [API-L3GEN-004-v1, API-L3GEN-008-v1], consumes: []}
---

# EPIC-L3GEN-029

Nháp, chờ Architecture Gate BL-r10. Chưa phải approval hoặc nghiệm thu độc lập.

## Phạm vi
T1–T5 trong HANDOFF-CODEX-FR029. Giữ nguyên các phần hoãn: archdia.json, vai trò file/component, Python 3.14, trần node và UI.

## Story
- STORY-L3GEN-029-01 (thêm 09/10/2026)
- STORY-L3GEN-029-02
- STORY-L3GEN-029-05
- STORY-L3GEN-029-08

## Bổ sung 09/10/2026

Luồng agent của FR-029 (ADR-2026-006, draft) và bộ kiểm bằng chứng được ghi thành Task muộn, sau khi code đã có. Decomposition do agent đề xuất; người chốt `accountable_team`, thứ tự và `blocked_by` (EXEC §B.12).

| Task | Cha | Việc |
|---|---|---|
| TASK-L3GEN-029-6 | STORY-L3GEN-029-01 | Bộ kiểm route và đăng ký |
| TASK-L3GEN-029-7 | STORY-L3GEN-029-02 | Bộ kiểm và lời nhắc tham số dependency |
| TASK-L3GEN-029-8 | STORY-L3GEN-029-08 | Bộ kiểm lời gọi HTTP và dòng nghi ngờ |
| TASK-L3GEN-029-9 | EPIC (không có AC) | Công cụ đo bộ kiểm |

Vòng agent (CMP-L3GEN-006, `docagent.py`) và prompt của ngày 07/10/2026 chưa có Task; xem DIARY-CR-L3GEN-2026-008.

## Bổ sung 12/10/2026

Ghi muộn (CR-L3GEN-2026-009). Decomposition do agent đề xuất; người chốt (EXEC §B.12). Các task dưới không có AC riêng, gắn thẳng Epic.

| Task | Cha | Việc |
|---|---|---|
| TASK-L3GEN-029-10 | EPIC (không có AC) | Chế độ đọc một lần, checkpoint |
| TASK-L3GEN-029-11 | EPIC (sửa trên AC đã có của STORY-01/02/05/08) | Sửa 8 lỗi bộ kiểm theo review 11/10 |
| TASK-L3GEN-029-12 | EPIC (không có AC; OQ-L3GEN-020) | TAI-LIEU.md và phần bổ sung |
| TASK-L3GEN-029-13 | EPIC (không có AC) | Giao diện web để demo |

Bảng CSDL và sự kiện thuộc EPIC-L3GEN-030, EPIC-L3GEN-031.
