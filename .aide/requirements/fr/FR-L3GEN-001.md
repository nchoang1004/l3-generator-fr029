---
uid: "01M2J06Z42VS531TS0VGKEFQX3"
key: "FR-L3GEN-001"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 5
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001"],"constrained_by":["NFR-L3GEN-COMP-001","NFR-L3GEN-DET-001","NFR-L3GEN-PERF-001","NFR-L3GEN-REL-001","NFR-L3GEN-SEC-001","NFR-L3GEN-TRACE-001","NFR-L3GEN-USA-001"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-001 — Nhận thư mục source và bắt đầu phân tích

## Mô tả

Người dùng chỉ định thư mục source local và nơi lưu kết quả để bắt đầu một lần phân tích.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Phân tích repository |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-001-01

- **Given:** Thư mục tồn tại, đọc được và chứa source thuộc stack hỗ trợ.
- **When:** người dùng chạy l3gen với đường dẫn source và output.
- **Then:** công cụ phân tích đúng thư mục đã chọn và báo đường dẫn bộ kết quả.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-PERF-001, NFR-L3GEN-REL-001, NFR-L3GEN-SEC-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm tra source có dấu cách trong đường dẫn và output ở ngoài source.

### AC-L3GEN-001-02

- **Given:** Đường dẫn không tồn tại, là file hoặc không có quyền đọc.
- **When:** người dùng yêu cầu phân tích.
- **Then:** công cụ trả lỗi đầu vào, chỉ rõ nguyên nhân và cách sửa; không báo thành công hoặc tạo bộ kết quả hoàn chỉnh.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm exit code và thông báo cho từng trường hợp.

### AC-L3GEN-001-03

- **Given:** Thư mục đầu ra không ghi được hoặc đã có bộ kết quả.
- **When:** người dùng bắt đầu một lần phân tích mới.
- **Then:** công cụ báo lỗi nếu không ghi được; nếu trùng kết quả thì hoặc từ chối, hoặc yêu cầu người dùng xác nhận trước khi ghi đè. Không bao giờ ghi đè im lặng.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Dùng output có sentinel; xác nhận sentinel nguyên vẹn khi chưa xác nhận, và chỉ bị thay sau khi người dùng xác nhận rõ ràng.

### AC-L3GEN-001-04

- **Given:** Repository có thư mục loại trừ do người dùng chỉ định.
- **When:** người dùng chạy phân tích.
- **Then:** các thư mục bị loại không đi vào dữ liệu kiến trúc; cấu hình loại trừ được ghi trong thông tin lần chạy.
- `constrained_by:` [NFR-L3GEN-SEC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Dùng mã sentinel trong tests, integration-tests, venv và một thư mục tùy chọn.

### AC-L3GEN-001-05

- **Given:** Một repository đã pin ở một commit, có bản trên đĩa và bản ZIP của cùng commit đó.
- **When:** người dùng chạy phân tích bằng dòng lệnh trên thư mục local, và chạy lại trên giao diện web bằng bản ZIP, cùng tắt AI.
- **Then:** hai lần cho cùng tập application, component, route, entity, external system, cạnh dependency, nhãn confidence/completeness và cùng danh sách limitation. Khác biệt chỉ được phép ở đường dẫn gốc trong evidence, dấu thời gian, định danh phiên và cách trình bày; vị trí tương đối của evidence trong repository phải giống nhau. Ranh giới đầy đủ ở NFR-L3GEN-DET-001.
- `constrained_by:` [NFR-L3GEN-DET-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** So sánh JSON chuẩn hóa của hai lần chạy sau khi chuẩn hóa đường dẫn gốc. Khác biệt ở bất kỳ dữ kiện, quan hệ, nhãn hoặc limitation nào là lỗi chặn phát hành, không phải khác biệt trình bày.

### AC-L3GEN-001-06

- **Given:** Thư mục output nằm bên trong thư mục source, hoặc source nằm bên trong output.
- **When:** người dùng bắt đầu phân tích.
- **Then:** công cụ từ chối và giải thích lý do; không đọc lại artifact của chính nó như source đầu vào, và không ghi vào cây source đang phân tích.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-SEC-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm cả hai chiều lồng nhau và trường hợp hai đường dẫn trỏ cùng một chỗ qua symlink hoặc đường dẫn tương đối.

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-TRACE-001](../nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-DET-001](../nfr/NFR-L3GEN-DET-001.md)
- [NFR-L3GEN-SEC-001](../nfr/NFR-L3GEN-SEC-001.md)
- [NFR-L3GEN-REL-001](../nfr/NFR-L3GEN-REL-001.md)
- [NFR-L3GEN-USA-001](../nfr/NFR-L3GEN-USA-001.md)
- [NFR-L3GEN-COMP-001](../nfr/NFR-L3GEN-COMP-001.md)
- [NFR-L3GEN-PERF-001](../nfr/NFR-L3GEN-PERF-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)

