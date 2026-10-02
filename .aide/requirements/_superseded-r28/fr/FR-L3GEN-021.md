---
uid: "01M34AM2AG2BQJK7XKJXQHVEGB"
key: "FR-L3GEN-021"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-004","GOAL-L3GEN-006"],"constrained_by":["NFR-L3GEN-ACC-002","NFR-L3GEN-AI-002","NFR-L3GEN-SEC-002"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-021 — Trích dữ kiện code

## Mô tả

Công cụ trích từ source các dữ kiện làm nguyên liệu cho mô hình kiến trúc và tài liệu L3 contract: API route cùng request/response model, mô hình dữ liệu, lời gọi ra ngoài, tham chiếu xuyên file, cấu hình, quan hệ sự kiện và thư viện phụ thuộc. Mỗi dữ kiện kèm vị trí file trong snapshot.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Phân tích repository |
| Ưu tiên | Must Have |
| Mốc | M1 cho route, entity, HTTP và tham chiếu; M3 cho config, event và thư viện |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-021-01

- **Given:** Đơn vị phân tích khai báo API route theo pattern thuộc phạm vi đã công bố.
- **When:** công cụ trích dữ kiện.
- **Then:** mỗi route có method, path, handler và nguồn khai báo; path ghép từ prefix và mount được ghi đầy đủ, phần chưa xác định được mang nhãn partial kèm lý do.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-021-02

- **Given:** Đơn vị phân tích khai báo lớp dữ liệu ánh xạ tới bảng.
- **When:** công cụ trích dữ kiện.
- **Then:** mỗi lớp có tên bảng nếu xác định được, danh sách cột và khóa ngoại; tên bảng sinh lúc chạy để unknown kèm nguồn, không suy từ tên lớp.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-021-03

- **Given:** Đơn vị phân tích gọi HTTP ra ngoài, phát hoặc nhận sự kiện, đọc khóa cấu hình, hoặc khai báo thư viện trong manifest.
- **When:** công cụ trích dữ kiện.
- **Then:** mỗi dữ kiện ghi được nơi sử dụng và mức độ xác định của đích; giá trị bí mật bị che; broker hoặc manifest ngoài phạm vi hỗ trợ hiện ở phần giới hạn thay vì bị bỏ qua.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-021-04

- **Given:** Một lời gọi hoặc tham chiếu có đích không xác định được bằng bảng import và symbol.
- **When:** công cụ trích dữ kiện.
- **Then:** dữ kiện được giữ lại với nhãn unresolved kèm lý do, và không được nâng thành quan hệ kiến trúc ở FR-L3GEN-022.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-AI-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-021-05

- **Given:** Handler của một route khai báo kiểu cho request body, tham số, hoặc response model, ví dụ bằng Pydantic model.
- **When:** công cụ trích dữ kiện.
- **Then:** mỗi route ghi được tên model của request và response cùng danh sách trường, kiểu và trường bắt buộc, kèm vị trí khai báo; status code nếu khai báo trong code. Phần không khai kiểu hoặc sinh lúc chạy để `unknown` kèm lý do, không suy từ tên biến.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../../domain/glossary-core.md)
