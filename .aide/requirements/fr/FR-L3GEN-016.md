---
uid: "01M2J06Z4X2C54J4GHDTS37495"
key: "FR-L3GEN-016"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001"],"constrained_by":["NFR-L3GEN-DET-001","NFR-L3GEN-PERF-001","NFR-L3GEN-PRIV-001","NFR-L3GEN-REL-001","NFR-L3GEN-SEC-001"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-001","OQ-L3GEN-002","OQ-L3GEN-005"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-016 — Nhận Git URL và bản nén repository

## Mô tả

Người dùng gửi Git URL công khai hoặc ZIP source qua web để tạo snapshot phân tích; local path chỉ dành CLI hoặc thư mục server được cho phép.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tiếp nhận và quản lý phân tích |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M2 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-016-01

- **Given:** Git URL HTTPS công khai tới GitHub và commit/ref hợp lệ.
- **When:** người dùng gửi yêu cầu phân tích.
- **Then:** dịch vụ lấy snapshot, ghi commit thực tế và ref yêu cầu; trạng thái và lỗi lấy repo hiển thị rõ.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-REL-001, NFR-L3GEN-SEC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** MVP không nhận credential trong URL hoặc private repo.

### AC-L3GEN-016-02

- **Given:** ZIP hợp lệ nằm trong giới hạn NFR.
- **When:** người dùng tải lên.
- **Then:** dịch vụ tạo vùng phân tích riêng, giữ digest của nội dung, báo số file/phạm vi trước khi trả kết quả.
- `constrained_by:` [NFR-L3GEN-PERF-001, NFR-L3GEN-REL-001, NFR-L3GEN-SEC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không dùng tên file khách gửi làm đường dẫn tùy ý.

### AC-L3GEN-016-03

- **Given:** URL trỏ mạng nội bộ/redirect ngoài danh sách cho phép hoặc ZIP chứa traversal/symlink nguy hiểm/bomb.
- **When:** người dùng gửi đầu vào.
- **Then:** yêu cầu bị từ chối an toàn với lý do; không truy cập địa chỉ cấm, không ghi ra ngoài vùng xử lý.
- `constrained_by:` [NFR-L3GEN-PERF-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-REL-001, NFR-L3GEN-SEC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Giới hạn và dọn dữ liệu theo NFR; không chạy hook/submodule/code.

### AC-L3GEN-016-04

- **Given:** Nguồn không truy cập được, bị quá giới hạn hoặc tải thất bại.
- **When:** người dùng theo dõi yêu cầu.
- **Then:** trạng thái failed và lý do xuất hiện; không dùng snapshot cũ thay thế; người dùng có thể gửi lại.
- `constrained_by:` [NFR-L3GEN-PERF-001, NFR-L3GEN-REL-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không khẳng định mọi lỗi mạng là lỗi repository.

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-DET-001](../nfr/NFR-L3GEN-DET-001.md)
- [NFR-L3GEN-SEC-001](../nfr/NFR-L3GEN-SEC-001.md)
- [NFR-L3GEN-PRIV-001](../nfr/NFR-L3GEN-PRIV-001.md)
- [NFR-L3GEN-REL-001](../nfr/NFR-L3GEN-REL-001.md)
- [NFR-L3GEN-PERF-001](../nfr/NFR-L3GEN-PERF-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)

