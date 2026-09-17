---
uid: "01M2J06Z4Z79BPX7JC6B86WZA5"
key: "FR-L3GEN-017"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001","GOAL-L3GEN-003"],"constrained_by":["NFR-L3GEN-PERF-001","NFR-L3GEN-PRIV-001","NFR-L3GEN-REL-001","NFR-L3GEN-SEC-001","NFR-L3GEN-USA-001"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-001","OQ-L3GEN-002","OQ-L3GEN-005"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-017 — Theo dõi phiên phân tích và lấy kết quả qua API

## Mô tả

Mỗi yêu cầu có định danh, trạng thái và kết quả riêng để giao diện hoặc hệ thống tích hợp theo dõi.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tiếp nhận và quản lý phân tích |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M2 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-017-01

- **Given:** Đầu vào hợp lệ được chấp nhận.
- **When:** client tạo yêu cầu phân tích.
- **Then:** nhận analysis_id và trạng thái queued; theo dõi được running, completed, partial, failed hoặc cancelled cùng thông tin lỗi.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không hứa phần trăm tiến độ nếu chưa có cơ sở tính.

### AC-L3GEN-017-02

- **Given:** Hai yêu cầu phân tích chạy đồng thời.
- **When:** client đọc trạng thái và kết quả.
- **Then:** mỗi yêu cầu chỉ trả snapshot/output của chính nó, có giới hạn tài nguyên theo NFR.
- `constrained_by:` [NFR-L3GEN-PERF-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-REL-001, NFR-L3GEN-SEC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không dùng một thư mục output chung.

### AC-L3GEN-017-03

- **Given:** Phiên đã hoàn tất và chưa hết hạn lưu.
- **When:** người dùng mở danh sách phiên hoặc API kết quả.
- **Then:** xem được trạng thái, source snapshot, thời điểm và tải JSON/Markdown/Mermaid; kết quả partial luôn có giới hạn.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Lịch sử tối thiểu trong một workspace tin cậy, không có so sánh drift giữa phiên.

### AC-L3GEN-017-04

- **Given:** Phiên bị hủy, lỗi hoặc hết hạn lưu.
- **When:** client yêu cầu kết quả.
- **Then:** nhận trạng thái và thông báo phù hợp; hủy xử lý có kiểm soát, dọn source theo NFR; không hiện artifact thiếu như kết quả hoàn tất.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Hợp đồng endpoint/status cụ thể làm sau Scope Gate.

### AC-L3GEN-017-05

- **Given:** Một repository đã được phân tích nhiều lần và vượt số lần được giữ.
- **When:** người dùng mở danh sách phiên của repository đó.
- **Then:** hệ thống giữ số lần phân tích gần nhất theo ngưỡng ở NFR-L3GEN-PRIV-001 và loại lần cũ nhất khi vượt; người dùng biết kết quả nào đã bị loại và vì sao, không gặp mục trống hoặc link hỏng.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Tạo vượt ngưỡng số lần rồi kiểm số bản còn lại và bản bị loại; kiểm cả mốc hết hạn. Cả hai ngưỡng lấy từ NFR-L3GEN-PRIV-001, không gõ lại ở đây.

### AC-L3GEN-017-06

- **Given:** Một kết quả phân tích còn hạn lưu.
- **When:** người dùng chọn xóa nó.
- **Then:** hệ thống hỏi xác nhận trước khi xóa; xóa xong thì không mở lại được, source tạm và output của riêng phiên đó bị dọn theo NFR-L3GEN-PRIV-001, và các phiên khác không bị ảnh hưởng.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm cả xóa thủ công lẫn hết hạn tự động; xác nhận dữ liệu đã dọn thật, không chỉ ẩn khỏi danh sách.

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-REL-001](../nfr/NFR-L3GEN-REL-001.md)
- [NFR-L3GEN-SEC-001](../nfr/NFR-L3GEN-SEC-001.md)
- [NFR-L3GEN-PERF-001](../nfr/NFR-L3GEN-PERF-001.md)
- [NFR-L3GEN-PRIV-001](../nfr/NFR-L3GEN-PRIV-001.md)
- [NFR-L3GEN-USA-001](../nfr/NFR-L3GEN-USA-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)

