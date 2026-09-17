---
uid: "01M2J06Z4GG8QMRXNQRFATPVQQ"
key: "FR-L3GEN-009"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-002"],"constrained_by":["NFR-L3GEN-REL-001","NFR-L3GEN-USA-001"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-009 — Báo lỗi và giới hạn theo từng lần phân tích

## Mô tả

Người dùng biết phần đã phân tích, bị bỏ qua và chưa hỗ trợ trước khi tin vào tài liệu.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Kiểm chứng kết quả |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-009-01

- **Given:** Một file lỗi cú pháp/encoding trong repo còn file hợp lệ.
- **When:** người dùng chạy phân tích.
- **Then:** công cụ tiếp tục với phần hợp lệ, báo file lỗi và nguyên nhân, giữ số đếm nhất quán.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** files_found bằng analyzed cộng skipped trong tập file đã chọn.

### AC-L3GEN-009-02

- **Given:** Không tìm được route dù có pattern FastAPI chưa được xử lý.
- **When:** người dùng xem kết quả.
- **Then:** báo chưa đủ khả năng kết luận, liệt kê pattern/nguồn; không viết kết quả đầy đủ chỉ vì parse được mọi file.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Case factory/nested route.

### AC-L3GEN-009-03

- **Given:** Một tham chiếu nội bộ chưa giải được hoặc thư viện nằm ngoài phạm vi.
- **When:** người dùng xem tóm tắt.
- **Then:** công cụ thống kê riêng hai trường hợp; tỷ lệ resolve không trộn external library thành lỗi nội bộ.
- `constrained_by:` [NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Ghi mẫu số và danh sách giới hạn.

### AC-L3GEN-009-04

- **Given:** Có lỗi ghi output hoặc bị ngắt giữa quá trình.
- **When:** người dùng mở thư mục kết quả.
- **Then:** không có dấu hiệu hoàn tất cho bộ thiếu file; dữ liệu từ lần chạy thành công trước đó không bị phá.
- `constrained_by:` [NFR-L3GEN-REL-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Cách atomic write/staging quyết định ở L2, hành vi này là yêu cầu.

### AC-L3GEN-009-05

- **Given:** Có tham chiếu nội bộ chưa xác định được đích, đích mơ hồ hoặc thuộc tính kiến trúc chưa giải được trong phần source đã phân tích.
- **When:** công cụ tạo findings ở chế độ không AI.
- **Then:** mỗi cảnh báo chỉ rõ loại giới hạn, thực thể hoặc quan hệ bị ảnh hưởng, nguồn và lý do chưa kết luận được. Phần dữ kiện đã xác định vẫn được giữ; không biến giới hạn của công cụ thành kết luận code có lỗi. Không có cảnh báo thì danh sách rỗng.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Fixture có đích thiếu, nhiều đích và thuộc tính động; đối chiếu từng cảnh báo với dữ kiện và nguồn tương ứng. Phạm vi FR này là độ đầy đủ của kết quả kiến trúc, không bao gồm rà code không dùng hoặc kiểm cách xử lý lỗi HTTP.

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-REL-001](../nfr/NFR-L3GEN-REL-001.md)
- [NFR-L3GEN-USA-001](../nfr/NFR-L3GEN-USA-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)

