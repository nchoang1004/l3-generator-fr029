---
uid: "01M34AM2AH10NEF8E4RC8GC40Z"
key: "FR-L3GEN-024"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-007"],"constrained_by":["NFR-L3GEN-OPS-001","NFR-L3GEN-ACC-002","NFR-L3GEN-AI-002"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-024 — Công bố giới hạn của lần chạy

## Mô tả

Mỗi lần chạy kèm phần nêu rõ những gì công cụ không đọc được. Bỏ sót có báo là chấp nhận được; bỏ sót im lặng thì không.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Kiểm chứng kết quả |
| Ưu tiên | Must Have |
| Mốc | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-024-01

- **Given:** Một số file trong phạm vi phân tích bị lỗi cú pháp hoặc lỗi encoding.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ vẫn xử lý phần hợp lệ, và nêu từng file lỗi kèm lý do ở phần giới hạn của kết quả.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-024-02

- **Given:** Phân tích chạm giới hạn tài nguyên, hết quota model, hoặc bị ngắt giữa chừng.
- **When:** công cụ kết thúc lần chạy.
- **Then:** công cụ trả kết quả partial kèm lý do và phạm vi đã xử lý được; không để lại bộ output trông như đã hoàn chỉnh.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-AI-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-024-03

- **Given:** Repository dùng framework, broker hoặc manifest nằm ngoài phạm vi hỗ trợ.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ nêu phần ngoài phạm vi ở mục giới hạn, không mô tả repository như thể phần đó không tồn tại.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-024-04

- **Given:** Một phạm vi chưa được xét đầy đủ vì thiếu bộ đọc, thiếu ngữ cảnh hoặc chạm giới hạn.
- **When:** công cụ sinh kết quả.
- **Then:** công cụ ghi trạng thái là giới hạn hoặc partial cho phạm vi đó, không ghi là không phát hiện thấy.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../../domain/glossary-core.md)
