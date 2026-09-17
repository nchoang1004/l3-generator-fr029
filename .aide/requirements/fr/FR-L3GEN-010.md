---
uid: "01M2J06Z4JD4ZB33358NS15YWH"
key: "FR-L3GEN-010"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001","GOAL-L3GEN-002"],"constrained_by":["NFR-L3GEN-AI-001","NFR-L3GEN-DET-001","NFR-L3GEN-PRIV-001","NFR-L3GEN-SEC-001"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-010 — Chạy phân tích không phụ thuộc AI

## Mô tả

Người dùng phân tích đầy đủ phần cốt lõi khi không có API key, không có mạng hoặc chủ động tắt AI.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Phân tích repository |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-010-01

- **Given:** Không có API key hoặc dùng --no-ai.
- **When:** người dùng phân tích repo.
- **Then:** công cụ sinh toàn bộ dữ kiện và output cốt lõi, thông báo chế độ tĩnh, không gọi LLM.
- `constrained_by:` [NFR-L3GEN-AI-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-SEC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu dữ kiện và kiểm network.

### AC-L3GEN-010-02

- **Given:** AI provider lỗi hoặc thiếu SDK AI.
- **When:** người dùng đã chọn bổ sung AI và bắt đầu phân tích.
- **Then:** công cụ giữ kết quả tĩnh, báo phần mô tả chưa có và nguyên nhân; không làm mất báo cáo.
- `constrained_by:` [NFR-L3GEN-AI-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không retry vô hạn; giới hạn theo NFR AI nếu chọn extension.

### AC-L3GEN-010-03

- **Given:** Cùng input với AI bật/tắt.
- **When:** người dùng so sánh dữ kiện.
- **Then:** route/entity/quan hệ/ID không đổi do nội dung AI; cảnh báo deterministic vẫn có khi tắt AI.
- `constrained_by:` [NFR-L3GEN-AI-001, NFR-L3GEN-DET-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Cảnh báo về giới hạn phân tích theo FR-L3GEN-009 vẫn được xuất khi tắt AI, theo contract đầu ra được duyệt.

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-SEC-001](../nfr/NFR-L3GEN-SEC-001.md)
- [NFR-L3GEN-PRIV-001](../nfr/NFR-L3GEN-PRIV-001.md)
- [NFR-L3GEN-DET-001](../nfr/NFR-L3GEN-DET-001.md)
- [NFR-L3GEN-AI-001](../nfr/NFR-L3GEN-AI-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)

