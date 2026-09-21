---
uid: "01M30ZP2F37D2MY6HV8KMZJ3B0"
key: "CAP-L3GEN-006"
type: "capability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "approved"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"covers":["FR-L3GEN-008","FR-L3GEN-012","FR-L3GEN-013"],"governed_by":["ADR-2026-001"]}
verified_at: 2026-09-21
verified_against: [{"key":"FR-L3GEN-008","revision":7},{"key":"FR-L3GEN-012","revision":6},{"key":"FR-L3GEN-013","revision":7},{"key":"ADR-2026-001","revision":4},{"key":"GLOSS-L3GEN-001","revision":3}]
classification: "internal"
ai_assisted: true
---

# CAP-L3GEN-006 — Trình bày và xuất kết quả

## Năng lực này là gì

Đưa `architecture model` đến người đọc và đến công cụ khác: khám phá qua giao diện web,
xuất Markdown, diagram-as-code và JSON có schema version, và bổ sung mô tả bằng AI khi
người dùng chủ động bật.

Ba FR ở chung đây vì chúng đều là nơi **tiêu thụ** mô hình, không phải nơi tạo ra nó.

## Ranh giới

- Cùng snapshot, cấu hình, tool version và rule version phải cho cùng deterministic core
  qua cả hai kênh; CLI, web và exporter không tự phân tích source theo luật riêng, mọi
  cấu trúc chúng trình bày phải đến từ cùng một architecture model (bất biến miền #6).
  Run metadata và cách trình bày được phép khác.
- Lớp phủ quan hệ chưa xác minh **mặc định tắt**. Khi người dùng bật, nó vẽ khác hẳn cạnh
  đã xác minh và mỗi quan hệ mang nhãn trạng thái cùng lý do; chỉ đổi nét vẽ mà không kèm
  nhãn là vi phạm bất biến miền #3. Quan hệ trong lớp phủ không vào tập cạnh kiến trúc và
  không tính vào coverage của claim.
- AI mặc định tắt. Khi bật, AI **không** được thay đổi code fact, architecture claim,
  evidence, limitation, finding ID hay artifact cấu trúc (bất biến miền #8). Văn bản AI
  sinh ra phải có nhãn.
- **Không** tạo claim hay evidence mới — đầu vào đến từ [CAP-L3GEN-004](CAP-L3GEN-004.md)
  và [CAP-L3GEN-005](CAP-L3GEN-005.md).
- Xuất evidence, limitation và coverage do [CAP-L3GEN-005](CAP-L3GEN-005.md) tạo ra, theo
  yêu cầu của AC-L3GEN-008-01; **không** tự định nghĩa nội dung của chúng. Năng lực này
  quyết định định dạng và nơi đặt, không quyết định phần nào là giới hạn.
- Ngoài phạm vi: khám phá tương tác và lịch sử phân tích trên dòng lệnh; chỉnh model thủ
  công trên UI; so sánh drift giữa các snapshot.

## FR được phủ

| FR key | Tên | Ghi chú phạm vi |
|---|---|---|
| [FR-L3GEN-008](../../requirements/fr/FR-L3GEN-008.md) | Xuất và sử dụng bộ kết quả | M1 xuất dữ kiện; M2 tích hợp component/L3; M3 nghiệm thu đầy đủ |
| [FR-L3GEN-013](../../requirements/fr/FR-L3GEN-013.md) | Phân tích và khám phá kiến trúc qua giao diện web | M2, kênh web |
| [FR-L3GEN-012](../../requirements/fr/FR-L3GEN-012.md) | Bổ sung mô tả và diễn giải cảnh báo bằng AI | Should Have, stretch M3 |
