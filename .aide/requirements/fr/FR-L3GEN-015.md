---
uid: "01M2J06Z4V772C9RZPC181KR5F"
key: "FR-L3GEN-015"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001","GOAL-L3GEN-002","GOAL-L3GEN-003"],"constrained_by":["NFR-L3GEN-ACC-001","NFR-L3GEN-COMP-001","NFR-L3GEN-TRACE-001"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-001","OQ-L3GEN-002","OQ-L3GEN-003"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-015 — Xem quan hệ phát và nhận sự kiện

## Mô tả

Người dùng xem producer/consumer và topic của Kafka; biết phần thiếu và quan hệ nào chỉ là ứng viên. Broker khác Kafka nằm ngoài phạm vi và phải hiện ra ở phần giới hạn.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M3 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-015-01

- **Given:** Ứng dụng dùng confluent_kafka Producer.produce và Consumer.subscribe với topic literal.
- **When:** người dùng phân tích.
- **Then:** có producer, consumer, topic, component và nguồn của từng quan hệ publishes/consumes.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kafka là adapter event duy nhất trong phạm vi. Python và Java có hai bộ rule riêng, kiểm từng bộ.

### AC-L3GEN-015-02

- **Given:** Topic/broker được tạo động hoặc lấy từ cấu hình chưa resolve.
- **When:** người dùng xem event model.
- **Then:** giữ phần biết được, đánh dấu partial/unknown và lý do; không đoán broker hoặc topic triển khai.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không chạy broker hay code để suy đích.

### AC-L3GEN-015-03

- **Given:** Hai service cùng tên topic nhưng chưa chứng minh cùng broker/namespace.
- **When:** người dùng xem dependency.
- **Then:** công cụ không khẳng định giao tiếp giữa chúng; có thể hiển thị candidate kèm phần cần xác minh.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Khi chứng minh cùng identity thì mới gộp thành topic chung.

### AC-L3GEN-015-04

- **Given:** Repository dùng broker khác Kafka, ví dụ RabbitMQ, Celery hoặc SQS.
- **When:** người dùng phân tích.
- **Then:** giới hạn chỉ ra broker đó ngoài phạm vi khi có bằng chứng nhận diện; phần route/DB còn lại vẫn được xử lý.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm với RabbitMQ, Celery và SQS: phải báo ngoài phạm vi, không mô tả repository như không có event.

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-ACC-001](../nfr/NFR-L3GEN-ACC-001.md)
- [NFR-L3GEN-TRACE-001](../nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-COMP-001](../nfr/NFR-L3GEN-COMP-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)

