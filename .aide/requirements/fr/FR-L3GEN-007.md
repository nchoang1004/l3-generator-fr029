---
uid: "01M2J06Z4DYP85ZG39B49BH0P7"
key: "FR-L3GEN-007"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-002"],"constrained_by":["NFR-L3GEN-ABST-001","NFR-L3GEN-DET-001","NFR-L3GEN-PRIV-001","NFR-L3GEN-TRACE-001"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-007 — Kiểm chứng kết luận bằng nguồn và nhãn

## Mô tả

Người đọc truy ngược được dữ kiện và quan hệ về đúng source snapshot, phân biệt bằng chứng trực tiếp, suy theo rule và phần chưa biết.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Kiểm chứng kết quả |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-007-01

- **Given:** Có route, entity, HTTP call hoặc cạnh quan hệ được xuất.
- **When:** người dùng mở chi tiết hoặc link nguồn.
- **Then:** công cụ chỉ ra file và range dòng tạo nên kết luận; nguồn hiển thị khớp phiên bản đã phân tích.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đặt output ngoài source để phát hiện link tương đối hỏng.

### AC-L3GEN-007-02

- **Given:** Kết luận theo cú pháp trực tiếp hoặc quy tắc suy luận đã công bố.
- **When:** người dùng xem kết quả.
- **Then:** confidence thể hiện exact hoặc inferred, completeness thể hiện full hoặc partial ở hai trường riêng; inferred/partial có lý do và nguồn.
- `constrained_by:` [NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** full chỉ nói thuộc tính công bố, không có nghĩa bao phủ mọi runtime behavior.

### AC-L3GEN-007-03

- **Given:** Nguồn đã thay đổi hoặc di chuyển sau lần phân tích.
- **When:** người dùng truy bằng chứng.
- **Then:** công cụ cho biết snapshot không còn khớp hoặc không mở được nguồn; không coi source mới là evidence cũ.
- `constrained_by:` [NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Có source digest; không tạo link Git commit cho cây có thay đổi chưa commit.

### AC-L3GEN-007-04

- **Given:** Một component hoặc cạnh gộp có nhiều dữ kiện hỗ trợ.
- **When:** người dùng xem bằng chứng.
- **Then:** kết quả giữ danh sách nguồn đóng góp; không ép một kết luận tổng hợp về một dòng không đại diện.
- `constrained_by:` [NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu chain component → code entities → source.

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` chưa chốt: component/contract/test IDs được lập ở bước thiết kế và planning sau Scope Gate. Đây là yêu cầu sản phẩm đang review, chưa phải task đủ điều kiện code; không coi các mảng rỗng là coverage đã đạt. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-ABST-001](../nfr/NFR-L3GEN-ABST-001.md)
- [NFR-L3GEN-TRACE-001](../nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-DET-001](../nfr/NFR-L3GEN-DET-001.md)
- [NFR-L3GEN-PRIV-001](../nfr/NFR-L3GEN-PRIV-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)

