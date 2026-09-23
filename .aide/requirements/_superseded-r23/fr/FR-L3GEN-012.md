---
uid: "01M2J06Z4NZ8914RN5ZJQ9625K"
key: "FR-L3GEN-012"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 6
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001"],"constrained_by":["NFR-L3GEN-AI-001","NFR-L3GEN-DET-001","NFR-L3GEN-PRIV-001"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-012 — Bổ sung mô tả và diễn giải cảnh báo bằng AI

## Mô tả

Sau khi người dùng chủ động cho phép, AI có thể bổ sung mô tả và giải thích giới hạn phân tích theo FR-L3GEN-009. Các cảnh báo này được tạo từ phân tích tĩnh, không cần AI.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tiện ích mở rộng |
| Ưu tiên đề xuất | Should Have |
| Mốc đề xuất | Stretch trong M3; không chặn nghiệm thu phase đầu |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-012-01

- **Given:** Người dùng chưa chọn bật AI dù máy có key.
- **When:** người dùng phân tích.
- **Then:** công cụ không tự gửi dữ liệu tới provider; thông báo rõ dữ liệu nào sẽ được gửi khi chọn bật.
- `constrained_by:` [NFR-L3GEN-AI-001, NFR-L3GEN-PRIV-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Quyền gửi dữ liệu và provider phải được chốt ở Scope Gate.

### AC-L3GEN-012-02

- **Given:** Có mô hình kiến trúc và danh sách cảnh báo về giới hạn phân tích được tạo không cần AI.
- **When:** AI sinh phần diễn giải.
- **Then:** chỉ nhận mô tả gắn ID đã tồn tại, schema chặn sửa/thêm/xóa thực thể và quan hệ; giải thích AI mang nhãn AI.
- `constrained_by:` [NFR-L3GEN-AI-001, NFR-L3GEN-DET-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Enrichment và giải thích finding đọc dữ kiện độc lập.

### AC-L3GEN-012-03

- **Given:** AI trả ID lạ, payload sai schema, timeout hoặc vượt giới hạn.
- **When:** công cụ nhận phản hồi.
- **Then:** bỏ phần không hợp lệ, ghi nguyên nhân và giữ kết quả tĩnh; không bỏ giới hạn chi phí để hoàn tất mô tả.
- `constrained_by:` [NFR-L3GEN-AI-001, NFR-L3GEN-DET-001, NFR-L3GEN-PRIV-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Bí mật không vào log/payload.

## Trạng thái liên kết triển khai

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-PRIV-001](../nfr/NFR-L3GEN-PRIV-001.md)
- [NFR-L3GEN-AI-001](../nfr/NFR-L3GEN-AI-001.md)
- [NFR-L3GEN-DET-001](../nfr/NFR-L3GEN-DET-001.md)
- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../../domain/glossary-core.md)

