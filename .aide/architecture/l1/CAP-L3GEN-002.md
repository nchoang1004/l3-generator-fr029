---
uid: "01M30ZP2F2TRCCPT7H34MA4037"
key: "CAP-L3GEN-002"
type: "capability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "approved"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"covers":["FR-L3GEN-002","FR-L3GEN-018"]}
verified_at: 2026-09-21
verified_against: [{"key":"FR-L3GEN-002","revision":6},{"key":"FR-L3GEN-018","revision":4},{"key":"GLOSS-L3GEN-001","revision":3}]
classification: "internal"
ai_assisted: true
---

# CAP-L3GEN-002 — Kiểm kê phạm vi và đơn vị phân tích

## Năng lực này là gì

Trả lời câu hỏi "phân tích cái gì, bỏ cái gì, dựa trên nền công nghệ nào" trước khi đọc
sâu. Năng lực này xác định `analysis unit` và `entry point` từ manifest, source root và
cấu hình, đồng thời liệt kê phần ngoài stack hỗ trợ.

`External library` nằm ở đây chứ không ở nơi dựng mô hình kiến trúc: theo glossary, thư
viện được khai báo nói repository dựa trên nền gì, nó không phải `external system` và
cũng không phải dependency giữa các component.

## Ranh giới

- Manifest, thư mục và entry point là evidence để khoanh phạm vi, **không** tự chứng minh
  deployment boundary. Chưa đủ bằng chứng thì gọi là `analysis unit` hoặc boundary
  candidate, không gọi là service.
- **Không** kết luận quan hệ giữa component — đó là [CAP-L3GEN-004](CAP-L3GEN-004.md).
- Phần không đọc được hoặc ngoài stack hỗ trợ phải thành `limitation`, không thành kết
  quả rỗng (bất biến miền #4). Việc công bố phần đó thuộc [CAP-L3GEN-005](CAP-L3GEN-005.md).

## FR được phủ

| FR key | Tên | Ghi chú phạm vi |
|---|---|---|
| [FR-L3GEN-002](../../requirements/fr/FR-L3GEN-002.md) | Nhận diện đơn vị phân tích và phạm vi hỗ trợ | M1: Python/FastAPI; Java phase sau |
| [FR-L3GEN-018](../../requirements/fr/FR-L3GEN-018.md) | Xem thư viện bên ngoài mà hệ thống phụ thuộc | M1: manifest Python; Maven/Java phase sau |
