---
uid: "01M2PV6966JJGJGA2T9DJXQ89H"
key: "FR-L3GEN-018"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001"],"constrained_by":["NFR-L3GEN-ACC-001","NFR-L3GEN-COMP-001","NFR-L3GEN-REL-001","NFR-L3GEN-SEC-001","NFR-L3GEN-TRACE-001"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-001","OQ-L3GEN-003"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-018 — Xem thư viện bên ngoài mà hệ thống phụ thuộc

## Mô tả

Người dùng xem các thư viện bên ngoài mà đơn vị phân tích khai báo hoặc sử dụng, kèm nơi khai báo làm bằng chứng. Danh sách này nói repository dựa trên nền công nghệ nào; nó không phải quan hệ phụ thuộc giữa các component, vốn thuộc FR-L3GEN-011.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Phân tích repository |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-018-01

- **Given:** Đơn vị phân tích có file khai báo thư viện thuộc định dạng hỗ trợ.
- **When:** người dùng phân tích repository.
- **Then:** công cụ liệt kê tên thư viện và phiên bản khai báo, kèm đường dẫn file và vị trí dòng làm bằng chứng; thư viện không có khai báo phiên bản được ghi là chưa ghim phiên bản, không tự điền một phiên bản nào.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu danh sách với nội dung file khai báo trên repo mẫu. Không suy phiên bản đang cài đặt thực tế từ file khai báo.

### AC-L3GEN-018-02

- **Given:** Đơn vị phân tích dùng định dạng khai báo thư viện chưa được hỗ trợ, hoặc không có file khai báo nào.
- **When:** người dùng phân tích repository.
- **Then:** công cụ ghi phần chưa đọc được kèm lý do và đường dẫn, nêu rõ danh sách thư viện của đơn vị đó là không đầy đủ; không trả danh sách rỗng như một kết luận rằng đơn vị không dùng thư viện nào.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-REL-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm đơn vị không có file khai báo và đơn vị dùng định dạng ngoài phạm vi công bố.

### AC-L3GEN-018-03

- **Given:** File khai báo liệt kê nhiều thư viện, trong đó chỉ một phần có dấu vết được dùng trong mã nguồn đã phân tích.
- **When:** người dùng xem danh sách thư viện.
- **Then:** mỗi thư viện mang nhãn phân biệt được khai báo và có dấu vết sử dụng trong mã, kèm bằng chứng cho nhãn có dấu vết sử dụng; thư viện chỉ có trong khai báo không bị công bố là đang được dùng.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu nhãn với import thật trong phạm vi mã đã phân tích. Không đảo ngược: thiếu dấu vết sử dụng không có nghĩa thư viện chắc chắn không được dùng, vì phạm vi phân tích có giới hạn.

### AC-L3GEN-018-04

- **Given:** File khai báo thư viện chứa chuỗi kết nối, mã truy cập hoặc giá trị bí mật khác.
- **When:** người dùng xem danh sách thư viện.
- **Then:** công cụ hiển thị tên và phiên bản thư viện nhưng che giá trị bí mật theo NFR-L3GEN-SEC-001; bằng chứng chỉ trỏ tới vị trí, không chép lại giá trị bí mật vào bộ kết quả.
- `constrained_by:` [NFR-L3GEN-SEC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm trên file khai báo có nhúng thông tin xác thực trong URL nguồn gói.

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

## Phạm vi định dạng hỗ trợ

Danh sách định dạng khai báo được hỗ trợ bám theo hai stack đã chốt ở FR-L3GEN-002 và phụ thuộc kết quả OQ-L3GEN-003; không công bố định dạng nào trước khi có quyết định đó.

## Tài liệu liên quan

- [NFR-L3GEN-COMP-001](../nfr/NFR-L3GEN-COMP-001.md)
- [NFR-L3GEN-REL-001](../nfr/NFR-L3GEN-REL-001.md)
- [NFR-L3GEN-SEC-001](../nfr/NFR-L3GEN-SEC-001.md)
- [NFR-L3GEN-TRACE-001](../nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-ACC-001](../nfr/NFR-L3GEN-ACC-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)
