---
uid: "01M2J06Z436ZPZT4YR8TXRFAQV"
key: "FR-L3GEN-002"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001"],"constrained_by":["NFR-L3GEN-COMP-001","NFR-L3GEN-REL-001","NFR-L3GEN-SEC-001","NFR-L3GEN-TRACE-001"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-002 — Nhận diện đơn vị phân tích và phạm vi hỗ trợ

## Mô tả

Người dùng xem được những phần repository được phân tích, bị bỏ qua hoặc chưa xác định được stack, cùng các điểm khởi động ứng dụng dùng để xác định ranh giới đơn vị.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Phân tích repository |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-002-01

- **Given:** Repository có service Python/FastAPI và service Java với manifest riêng.
- **When:** người dùng phân tích repository.
- **Then:** công cụ phân tích phần Python được hỗ trợ, liệt kê phần Java bị bỏ qua với lý do, không kết luận rằng toàn repository đã được bao phủ.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-REL-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu danh sách đơn vị, file và trạng thái.

### AC-L3GEN-002-02

- **Given:** Thư mục Python không có manifest nhưng có import FastAPI.
- **When:** người dùng phân tích.
- **Then:** công cụ dùng thư mục đầu vào làm đơn vị tạm, ghi bằng chứng nhận diện và nêu ranh giới service chưa được xác nhận.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không gọi ranh giới suy từ thư mục là deployment boundary chắc chắn.

### AC-L3GEN-002-03

- **Given:** Không có source hoặc mọi đơn vị đều không thuộc stack hỗ trợ.
- **When:** người dùng phân tích.
- **Then:** công cụ trả lỗi đầu vào và liệt kê stack hỗ trợ; không trả báo cáo rỗng như một lần thành công.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-REL-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm Python rỗng, Java-only và Flask-only.

### AC-L3GEN-002-04

- **Given:** Một đơn vị chứa FastAPI cùng framework khác chưa hỗ trợ.
- **When:** người dùng phân tích.
- **Then:** công cụ báo tất cả framework phát hiện được và chỉ chạy khả năng đang hỗ trợ; phần bỏ qua được ghi rõ.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-REL-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không hứa chạy extractor chưa tồn tại.

### AC-L3GEN-002-05

- **Given:** Repository có nhiều thư mục chứa mã thuộc stack hỗ trợ, trong đó một số thư mục có điểm khởi động ứng dụng và một số chỉ chứa mã dùng chung.
- **When:** người dùng phân tích repository.
- **Then:** công cụ liệt kê các điểm khởi động phát hiện được kèm file, vị trí và luật nhận diện đã dùng; mỗi đơn vị phân tích nêu rõ có hay không có điểm khởi động; thư mục chỉ chứa mã dùng chung không bị công bố là ứng dụng riêng.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-REL-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu danh sách điểm khởi động với kiểm tay trên repo mẫu có nhiều ứng dụng. Không suy ra điểm khởi động chỉ từ tên file hoặc tên thư mục; không có điểm khởi động nào phát hiện được thì ghi phần chưa xác định kèm lý do, không chọn bừa một file làm điểm khởi động.

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-REL-001](../nfr/NFR-L3GEN-REL-001.md)
- [NFR-L3GEN-TRACE-001](../nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-COMP-001](../nfr/NFR-L3GEN-COMP-001.md)
- [NFR-L3GEN-SEC-001](../nfr/NFR-L3GEN-SEC-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)

