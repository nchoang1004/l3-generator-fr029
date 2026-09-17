---
uid: "01M2J06Z4S3VBN7NXTP8DSCCE1"
key: "FR-L3GEN-014"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001","GOAL-L3GEN-002"],"constrained_by":["NFR-L3GEN-ACC-001","NFR-L3GEN-COMP-001","NFR-L3GEN-PRIV-001","NFR-L3GEN-TRACE-001"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-001","OQ-L3GEN-002","OQ-L3GEN-003"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-014 — Xem cấu hình mà hệ thống sử dụng

## Mô tả

Người dùng xem các khóa cấu hình và nơi sử dụng mà không lộ giá trị bí mật.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M3 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-014-01

- **Given:** Python đọc os.getenv/os.environ hoặc trường settings được định nghĩa bằng Pydantic BaseSettings.
- **When:** người dùng phân tích.
- **Then:** công cụ liệt kê khóa/trường, nơi khai báo/sử dụng và component liên quan nếu resolve được.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không thực thi settings hoặc đọc môi trường thật của server.

### AC-L3GEN-014-02

- **Given:** Có .env.example hoặc YAML cấu hình ứng dụng với schema/key công bố trong ma trận hỗ trợ.
- **When:** người dùng phân tích.
- **Then:** công cụ liên kết tên khóa khi có mapping rõ, nêu nguồn; key trùng tên không đủ để nối dependency.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** YAML tùy ý chưa có schema chỉ được coi là dữ liệu chưa hiểu.

### AC-L3GEN-014-03

- **Given:** Giá trị là token/password hoặc chuỗi kết nối có credential.
- **When:** người dùng xem/export kết quả.
- **Then:** giá trị bị che hoặc không thu thập; vẫn biết tên khóa và vị trí sử dụng.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không đọc .env thật hoặc in source snippet chứa secret.

### AC-L3GEN-014-04

- **Given:** Không resolve được tên khóa động.
- **When:** người dùng xem cấu hình.
- **Then:** giữ biểu thức và nguồn với nhãn partial; không đoán tên hoặc giá trị.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kể cả có key cùng tên trong file khác.

### AC-L3GEN-014-05

- **Given:** Repository Java đọc cấu hình qua cơ chế thuộc phạm vi đã công bố của Spring Boot.
- **When:** người dùng phân tích.
- **Then:** khóa cấu hình Java hiện ra cùng nơi sử dụng và cùng quy tắc che giá trị bí mật như phía Python; không lộ giá trị thật.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Cơ chế cấu hình và schema YAML được phép diễn giải chốt tại OQ-L3GEN-003. Cơ chế ngoài phạm vi phải hiện ở phần giới hạn.

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-ACC-001](../nfr/NFR-L3GEN-ACC-001.md)
- [NFR-L3GEN-TRACE-001](../nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-PRIV-001](../nfr/NFR-L3GEN-PRIV-001.md)
- [NFR-L3GEN-COMP-001](../nfr/NFR-L3GEN-COMP-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)

