---
uid: "01M30ZP2F2XFWV4HH259D97B6J"
key: "CAP-L3GEN-003"
type: "capability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"covers":["FR-L3GEN-003","FR-L3GEN-004","FR-L3GEN-005","FR-L3GEN-006","FR-L3GEN-014","FR-L3GEN-015"]}
verified_at: 2026-09-21
verified_against: [{"key":"FR-L3GEN-003","revision":8},{"key":"FR-L3GEN-004","revision":7},{"key":"FR-L3GEN-005","revision":5},{"key":"FR-L3GEN-006","revision":5},{"key":"FR-L3GEN-014","revision":6},{"key":"FR-L3GEN-015","revision":7},{"key":"GLOSS-L3GEN-001","revision":3}]
classification: "internal"
ai_assisted: true
---

# CAP-L3GEN-003 — Trích xuất code fact theo stack

## Năng lực này là gì

Đọc source của một `analysis unit` và sinh ra `code fact` tất định kèm evidence trỏ về
file và dòng. Sáu FR thuộc đây có cùng một hình: mỗi FR là một loại dữ kiện mà một adapter
theo stack đọc được — route, mô hình dữ liệu, lời gọi HTTP, tham chiếu xuyên file, khóa
cấu hình và quan hệ sự kiện Kafka.

Phần nối một tham chiếu tới đích của nó cũng ở đây, và kết quả nối mang đúng một trong
bốn trạng thái `resolved` / `ambiguous` / `unresolved` / `runtime-dependent`.

## Ranh giới

- `Code fact` chưa phải `architecture claim`. Việc nâng fact thành claim mức component
  thuộc [CAP-L3GEN-004](CAP-L3GEN-004.md).
- Quan hệ `unresolved`, `ambiguous` hay `runtime-dependent` **không** được nâng thành
  cạnh kiến trúc của lớp mặc định (bất biến miền #3). Nó ở lại lớp dữ kiện kèm nhãn
  trạng thái và lý do — đủ để [CAP-L3GEN-006](CAP-L3GEN-006.md) dựng lớp phủ quan hệ
  chưa xác minh, nhưng không vào tập cạnh kiến trúc.
- Adapter chỉ diễn giải API bằng luật đã công bố. Ngoài ma trận stack đã chốt thì báo
  `limitation`, không đoán.
- **Không** thực thi source để khám phá runtime (bất biến miền #2).

## FR được phủ

| FR key | Tên | Ghi chú phạm vi |
|---|---|---|
| [FR-L3GEN-003](../../requirements/fr/FR-L3GEN-003.md) | Liệt kê API routes và handler | M1: FastAPI; Spring Boot phase sau |
| [FR-L3GEN-004](../../requirements/fr/FR-L3GEN-004.md) | Liệt kê mô hình dữ liệu | M1: SQLAlchemy; ORM Java phase sau |
| [FR-L3GEN-005](../../requirements/fr/FR-L3GEN-005.md) | Liệt kê lời gọi HTTP và đích bên ngoài | M1: requests/httpx; client Java phase sau |
| [FR-L3GEN-006](../../requirements/fr/FR-L3GEN-006.md) | Truy vết tham chiếu và lời gọi xuyên file | M1 |
| [FR-L3GEN-014](../../requirements/fr/FR-L3GEN-014.md) | Xem cấu hình mà hệ thống sử dụng | M3: Python; Java phase sau. Không lộ giá trị bí mật |
| [FR-L3GEN-015](../../requirements/fr/FR-L3GEN-015.md) | Xem quan hệ phát và nhận sự kiện | M3: Kafka Python; broker khác ngoài phạm vi |
