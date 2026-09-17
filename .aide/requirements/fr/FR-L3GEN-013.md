---
uid: "01M2J06Z4RTMCQVV3677SVT4XB"
key: "FR-L3GEN-013"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 5
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001","GOAL-L3GEN-003"],"constrained_by":["NFR-L3GEN-DET-001","NFR-L3GEN-ABST-001","NFR-L3GEN-COMP-001","NFR-L3GEN-PERF-001","NFR-L3GEN-TRACE-001","NFR-L3GEN-USA-001"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-001","OQ-L3GEN-002"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-013 — Phân tích và khám phá kiến trúc qua giao diện web

## Mô tả

Người dùng truy cập giao diện web để gửi repository, theo dõi phân tích, xem tổng quan/component/dependency và truy về nguồn bằng chứng.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Khám phá kiến trúc |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M2 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-013-01

- **Given:** Người dùng có repository thuộc phạm vi hỗ trợ.
- **When:** người dùng tạo yêu cầu phân tích trên giao diện.
- **Then:** chọn được đầu vào hỗ trợ, cấu hình phạm vi và chế độ AI; theo dõi trạng thái; khi xong mở được kết quả đúng lần chạy.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-PERF-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Giao diện dùng cùng dịch vụ phân tích và model; không tự suy cấu trúc riêng.

### AC-L3GEN-013-02

- **Given:** Người dùng chọn một thực thể hoặc cạnh.
- **When:** giao diện mở chi tiết.
- **Then:** hiện nguồn và hai loại nhãn độc lập; mô tả AI khác dữ kiện source bằng nhãn rõ.
- `constrained_by:` [NFR-L3GEN-TRACE-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Có keyboard navigation và không chỉ phân biệt bằng màu.

### AC-L3GEN-013-03

- **Given:** Output rỗng, hỏng hoặc schema không hỗ trợ.
- **When:** người dùng mở giao diện.
- **Then:** hiện trạng thái rỗng/lỗi phù hợp và cách xử lý; không crash hoặc hiện graph cũ như kết quả mới.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm riêng ba trường hợp output rỗng, output hỏng và schema version không hỗ trợ; xác nhận mỗi trường hợp có trạng thái và cách xử lý riêng. Sau khi mở một kết quả lỗi, giao diện không giữ lại graph của lần chạy trước.

### AC-L3GEN-013-04

- **Given:** Kết quả có nhiều component và quan hệ.
- **When:** người dùng tìm tên hoặc lọc theo service/loại thành phần/nhãn.
- **Then:** giao diện hiển thị phần khớp, cho thu phóng/chọn node và tải output; phần bị ẩn do lọc được báo rõ.
- `constrained_by:` [NFR-L3GEN-PERF-001, NFR-L3GEN-TRACE-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Mỗi sơ đồ có đường tới evidence của node và cạnh.

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-DET-001](../nfr/NFR-L3GEN-DET-001.md)
- [NFR-L3GEN-ABST-001](../nfr/NFR-L3GEN-ABST-001.md)
- [NFR-L3GEN-USA-001](../nfr/NFR-L3GEN-USA-001.md)
- [NFR-L3GEN-TRACE-001](../nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-COMP-001](../nfr/NFR-L3GEN-COMP-001.md)
- [NFR-L3GEN-PERF-001](../nfr/NFR-L3GEN-PERF-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)

