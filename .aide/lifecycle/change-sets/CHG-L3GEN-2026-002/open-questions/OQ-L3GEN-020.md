---
uid: "01M4PMS40J96E65HGY7QMHXTGE"
key: "OQ-L3GEN-020"
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

# OQ-L3GEN-020 — Đầu ra và chế độ chạy mới chưa có trong spec

- **Blocking:** không chặn code; chặn nghiệm thu theo FR-029 và API-L3GEN-008.

## Câu hỏi

Các thứ dưới đây đã có code và test (11–12/10) nhưng FR-029, API-L3GEN-008, CMP-L3GEN-006 chưa ghi. Có đưa vào spec không?

| Thứ đã làm | Nguồn quyết định |
|---|---|
| File `TAI-LIEU.md` 11 mục, một file đọc hết | Người dùng chọn "cách A" (CR-009, 20:42) |
| Chế độ `--mode oneshot`: gửi cả source trong request 1, tối đa 2 vòng sửa; `--checkpoint` để chạy tiếp | Người dùng chọn (CR-009, decisions 19:46) |
| Route có thêm: lỗi trả về (errors), tags, deprecated, summary, ví dụ | Claude thêm khi làm "làm đi" 20:59; chưa duyệt riêng |
| Mục thư viện, cấu hình, middleware, quan hệ component trong `TAI-LIEU.md` và `result.json` | Như trên; xem OQ-L3GEN-019 |
| File TBL có thêm cột Nhãn và Bằng chứng từng dòng | Claude làm theo FR-030 mục "Nội dung một file TBL"; cần đối chiếu API-008 §6 |

## Lựa chọn

1. **Mở CR sửa FR-029/030/031, API-008, CMP-006** cho các mục được giữ; người duyệt từng mục.
2. **Giữ làm phần phụ ngoài chuẩn**: ghi rõ trong README là "chưa thuộc spec", không tính vào nghiệm thu.
3. **Gỡ các mục chưa duyệt** (errors/tags/summary/examples, phần phụ).
