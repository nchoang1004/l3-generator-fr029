---
uid: "01M4PMXJCXNSZ31A1M9WQVREXS"
key: TASK-L3GEN-030-1
type: task
group: normative
scope: lifecycle
status: draft
story: STORY-L3GEN-030-01
implements: [CMP-L3GEN-004, CMP-L3GEN-008]
change_request: CR-L3GEN-2026-009
---

# TASK-L3GEN-030-1 — Đọc bảng CSDL và xuất TBL

Ghi muộn ngày 12/10/2026: việc đã làm 11–12/10/2026 trước khi có Task (DIARY-CR-L3GEN-2026-009). Chưa phải approval hoặc nghiệm thu độc lập.

## Việc làm
`slice/l3slice/extract.py` (bảng, cột, khóa, ràng buộc, alias `Annotated`, `extend_existing`, `sa_type`), `docstatic.tables_not_read` (ORM khác, migration, SQL viết tay → `TABLES_NOT_READ`), `render.py` (file TBL có lớp model, nhãn, bằng chứng từng dòng), mục CSDL của `tailieu.py`.

## Xong khi
- `slice/tests/test_tables_db.py` qua (mỗi lỗi có test đỏ trước)
- So gold 4 repo: bảng, cột, khóa chính, khóa ngoại khớp
- Giám khảo độc lập 2 vòng, đầu ra đóng băng

## Hiện trạng (12/10/2026)
Code và test đã có. Gold: 32/32 bảng, 341/341 cột/khóa chính/khóa ngoại. Giám khảo vòng 2: 285/287 cột (2 lỗi `sa_type`, đã sửa sau, chưa chấm lại). AC-030-02 chỉ đạt khi URL viết sẵn (OQ-L3GEN-022). Bằng chứng: `ket-qua-chay/db-check-20261012/`, `docs/FR030-kiem-csdl-20261012.md`. Chưa qua Component Merge Gate, chưa có MR.

## Bộ ba evidence
`evidence/context/CTX-TASK-L3GEN-030-1.yaml` · `evidence/plans/PLAN-TASK-L3GEN-030-1.md` · `evidence/diaries/DIARY-TASK-L3GEN-030-1.md`
