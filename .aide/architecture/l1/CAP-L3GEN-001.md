---
uid: "01M30ZP2F1K22JZWNM1REYGWW8"
key: "CAP-L3GEN-001"
type: "capability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"covers":["FR-L3GEN-001","FR-L3GEN-010","FR-L3GEN-016","FR-L3GEN-017"]}
verified_at: 2026-09-21
verified_against: [{"key":"FR-L3GEN-001","revision":7},{"key":"FR-L3GEN-010","revision":5},{"key":"FR-L3GEN-016","revision":6},{"key":"FR-L3GEN-017","revision":8},{"key":"GLOSS-L3GEN-001","revision":3}]
classification: "internal"
ai_assisted: true
---

# CAP-L3GEN-001 — Tiếp nhận source và điều phối lần phân tích

## Năng lực này là gì

Biến một đầu vào do người dùng cung cấp thành `source snapshot` bất biến có content
digest, rồi chạy đúng một `analysis run` trên snapshot đó. Năng lực này giữ định danh,
trạng thái và ranh giới tài nguyên của lần chạy, kể cả khi không có AI hoặc không có mạng.

Bốn đầu vào thuộc cùng một năng lực vì chúng khác nhau ở cách lấy source, không khác nhau
ở việc phải tạo ra gì: thư mục cục bộ qua dòng lệnh, URL GitHub public và ZIP qua web,
và trạng thái/định danh phiên để theo dõi lần chạy.

## Ranh giới

- **Không** quyết định phần nào của repository được phân tích — đó là [CAP-L3GEN-002](CAP-L3GEN-002.md).
- **Không** đọc nội dung source để sinh dữ kiện — đó là [CAP-L3GEN-003](CAP-L3GEN-003.md).
- **Không** trình bày kết quả — đó là [CAP-L3GEN-006](CAP-L3GEN-006.md).
- Source đầu vào là read-only (bất biến miền #2). Năng lực này không import, chạy, cài
  dependency hay ghi ngược vào source.
- Giữ trạng thái `completed` / `partial` / `failed` của run. Hết ngân sách thời gian, bộ
  nhớ hoặc trần tiếp nhận thì dừng và đánh dấu `partial` (bất biến miền #10); nội dung
  phạm vi đã mất do [CAP-L3GEN-005](CAP-L3GEN-005.md) mô tả.

## FR được phủ

| FR key | Tên | Ghi chú phạm vi |
|---|---|---|
| [FR-L3GEN-001](../../requirements/fr/FR-L3GEN-001.md) | Nhận thư mục source và bắt đầu phân tích | Kênh dòng lệnh |
| [FR-L3GEN-016](../../requirements/fr/FR-L3GEN-016.md) | Nhận Git URL và bản nén repository | Kênh web |
| [FR-L3GEN-017](../../requirements/fr/FR-L3GEN-017.md) | Theo dõi phiên phân tích và lấy kết quả qua API | Should Have, phase sau |
| [FR-L3GEN-010](../../requirements/fr/FR-L3GEN-010.md) | Chạy phân tích không phụ thuộc AI | Thuộc tính của việc điều phối run, không phải của việc trích xuất |
