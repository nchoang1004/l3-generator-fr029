---
uid: "01M34AM2AGHC8W6DVPXV8GN0WN"
key: "FR-L3GEN-019"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-004"],"constrained_by":["NFR-L3GEN-SEC-002","NFR-L3GEN-OPS-001"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-019 — Nhận source và chạy phân tích

## Mô tả

Người dùng chỉ định source rồi bắt đầu một lần phân tích. Dòng lệnh nhận thư mục cục bộ và thư mục output; web nhận file ZIP hoặc URL GitHub public. Công cụ kiểm đầu vào trước khi phân tích và giải thích lỗi thay vì trả kết quả rỗng.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tiếp nhận đầu vào |
| Ưu tiên | Must Have |
| Mốc | M1 cho CLI; M2 cho web |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-019-01

- **Given:** Người dùng chỉ định một thư mục source đọc được và một thư mục output ghi được.
- **When:** người dùng chạy phân tích qua dòng lệnh.
- **Then:** công cụ phân tích rồi ghi tài liệu L3, diagram và JSON vào thư mục output, và in ra đường dẫn các file đã tạo.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-019-02

- **Given:** Đường dẫn source không tồn tại, là file, không có quyền đọc, hoặc thư mục output không ghi được.
- **When:** người dùng chạy phân tích.
- **Then:** công cụ dừng trước khi phân tích, nêu rõ nguyên nhân và cách sửa, và không tạo thư mục output dở dang.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-019-03

- **Given:** Thư mục source nằm trong thư mục output, hoặc ngược lại.
- **When:** người dùng chạy phân tích.
- **Then:** công cụ từ chối; không đọc lại artifact của chính nó và không ghi vào cây source.
- `constrained_by:` [NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-019-04

- **Given:** Người dùng gửi file ZIP hỏng, sai định dạng, chứa đường dẫn thoát khỏi vùng giải nén, hoặc vượt ngưỡng kích thước.
- **When:** web tiếp nhận file.
- **Then:** công cụ từ chối và nêu lý do; không ghi file ra ngoài vùng xử lý.
- `constrained_by:` [NFR-L3GEN-SEC-002, NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-019-05

- **Given:** Người dùng nhập URL GitHub sai, repository không tồn tại, hoặc repository yêu cầu quyền truy cập.
- **When:** web lấy source.
- **Then:** công cụ báo đúng nguyên nhân truy cập, không hiển thị như repository rỗng và không yêu cầu credential.
- `constrained_by:` [NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../../domain/glossary-core.md)
