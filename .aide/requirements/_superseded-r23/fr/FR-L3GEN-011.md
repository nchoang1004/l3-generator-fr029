---
uid: "01M2J06Z4K1JWY5C2V6V7RJ6ZH"
key: "FR-L3GEN-011"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 8
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001","GOAL-L3GEN-003"],"constrained_by":["NFR-L3GEN-ABST-001","NFR-L3GEN-ACC-001","NFR-L3GEN-DET-001","NFR-L3GEN-TRACE-001"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-011 — Xem component và tài liệu L3 của service

## Mô tả

Người dùng xem các component bên trong service và quan hệ có chứng cứ giữa chúng. Lớp trình bày mặc định dừng ở mức component; từ một component hoặc một quan hệ, người dùng mở được bằng chứng ở mức module/class/function và nguồn.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tài liệu và tích hợp |
| Ưu tiên đề xuất | Must Have |
| Mốc bắt đầu đề xuất | M2: tạo component model và tài liệu L3 ban đầu |
| Mốc nghiệm thu đầy đủ đề xuất | M3: tài liệu tích hợp config/event và tất cả AC của FR này đạt |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-011-01

- **Given:** Repo có API, business module, data access và integration với ranh giới nhóm đã công bố.
- **When:** người dùng sinh tài liệu L3.
- **Then:** có component model gồm định danh, thành viên code, vai trò, interface và dependency; mỗi nhóm chỉ ra rule/evidence.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-DET-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Cho phép nhóm theo module/package; không mặc định mọi services/ đều là deployment service.

### AC-L3GEN-011-02

- **Given:** Nhiều lời gọi code liên kết hai component.
- **When:** người dùng xem sơ đồ component.
- **Then:** các cạnh code được gộp thành dependency giữa component với danh sách nguồn; từ component mở được danh sách code entities và source làm bằng chứng, nhưng sơ đồ mặc định không hiển thị các cạnh code rời rạc đó.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không suy causal request flow chỉ từ việc cùng xuất hiện trong module.

### AC-L3GEN-011-03

- **Given:** Không đủ căn cứ xác định business/repository role hoặc có nhiều cách nhóm.
- **When:** người dùng xem model.
- **Then:** giữ nhóm module trung tính/UNKNOWN và lý do; không đặt trách nhiệm nghiệp vụ như một sự thật đã biết.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Role inference là inferred, không exact.

### AC-L3GEN-011-04

- **Given:** Người dùng mở tài liệu L3 Markdown và sơ đồ component.
- **When:** người dùng tìm API, DB và external dependency của một component.
- **Then:** có danh sách liên quan, bằng chứng, giới hạn và phần diễn giải tách riêng; L3 có component, API, DB, cấu hình và event trong khả năng hỗ trợ.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Bộ kết quả theo FR-L3GEN-008 chứa mô hình component đọc được bằng máy và mã nguồn sơ đồ; đối chiếu chúng với nội dung tài liệu, không phụ thuộc tên file.

### AC-L3GEN-011-05

- **Given:** Repository có số function trong phạm vi hỗ trợ đạt hoặc vượt ngưỡng ở NFR-L3GEN-ABST-001.
- **When:** người dùng xem sơ đồ và tài liệu L3 mặc định.
- **Then:** node trong sơ đồ mặc định là application, component và hệ thống ngoài; số node không vượt trần quy định ở NFR-L3GEN-ABST-001, không tăng theo số function, và không có một node cho mỗi function. Vượt trần thì rút gọn có thông báo theo AC-L3GEN-008-03, không xuất sơ đồ đầy đủ rồi để người đọc tự lọc. Dữ kiện mức function/class vẫn truy được ở lớp bằng chứng có nhãn riêng.
- `constrained_by:` [NFR-L3GEN-ABST-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đếm node theo lớp trong bộ kết quả máy đọc được của FR-L3GEN-008, không đếm trên hình; đối chiếu số đếm với trần ở NFR-L3GEN-ABST-001. Cả ngưỡng số function lẫn trần số node lấy từ NFR đó, không gõ lại ở đây.

## Trạng thái liên kết triển khai

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-ABST-001](../nfr/NFR-L3GEN-ABST-001.md)
- [NFR-L3GEN-ACC-001](../nfr/NFR-L3GEN-ACC-001.md)
- [NFR-L3GEN-TRACE-001](../nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-DET-001](../nfr/NFR-L3GEN-DET-001.md)
- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../../domain/glossary-core.md)

