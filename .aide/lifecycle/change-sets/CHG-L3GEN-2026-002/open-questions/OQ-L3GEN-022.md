---
uid: "01M4PMS40KHMWJ5EBFHT2FWR5V"
key: "OQ-L3GEN-022"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "open"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Hoàng"
due: "2026-10-19"
due_note: "Ngày đề xuất khi mở OQ (12/10/2026); owner chỉnh nếu cần."
change_set: "CHG-L3GEN-2026-002"
derived_from: ["CR-L3GEN-2026-009"]
---

# OQ-L3GEN-022 — Quy tắc nhận biến thể SQL (dialect) và ràng buộc trong file TBL

- **Blocking:** AC-L3GEN-030-02 (khối DDL) trên repo dùng URL tính lúc chạy.

## Câu hỏi

AC-L3GEN-030-02 nói biến thể SQL lấy "qua dòng tạo engine hoặc URL kết nối". Code hiện chỉ nhận khi `create_engine(...)`/`create_all` có URL là chuỗi viết sẵn. Repo full-stack ghi `scheme="postgresql+psycopg"` ở `core/config.py:37` rồi ghép URL lúc chạy; công cụ ghi "chưa rõ" nên không có DDL. Repo orderflow có cả postgres và sqlite. Hai câu hỏi:

1. Có nhận biến thể từ chuỗi scheme trong file cấu hình không, khi có nhiều ứng viên thì ghi gì?
2. File TBL có cần ghi ràng buộc (unique, index, ondelete, ràng buộc nhiều cột) không? Hiện chỉ `TAI-LIEU.md` ghi; FR-030 không đòi.

## Dữ liệu đầu vào

`docs/FR030-kiem-csdl-20261012.md` mục 4; `ket-qua-chay/db-check-20261012/`.

## Lựa chọn

| Câu | Lựa chọn |
|---|---|
| 1 | a) Giữ như hiện tại (chỉ URL viết sẵn). b) Nhận chuỗi scheme khi chỉ có một ứng viên; nhiều ứng viên thì `unknown` kèm danh sách. |
| 2 | a) Không thêm. b) Thêm cột ràng buộc vào TBL; sửa FR-030 và API-008 §6. |
