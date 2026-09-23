---
uid: "01M2J06Z49Y374WH78RBY19X1Z"
key: "FR-L3GEN-005"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 5
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001","GOAL-L3GEN-002"],"constrained_by":["NFR-L3GEN-ACC-001","NFR-L3GEN-COMP-001","NFR-L3GEN-PRIV-001","NFR-L3GEN-TRACE-001"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-005 — Liệt kê lời gọi HTTP và đích bên ngoài

## Mô tả

Người dùng xác định nơi gọi HTTP qua thư viện thuộc phạm vi đã công bố và mức độ biết đích đến; không đồng nhất mọi HTTP call với một hệ thống bên ngoài đã xác nhận. Phase đầu phủ requests/httpx của Python; client HTTP của Java/Spring Boot thuộc phase sau.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1: requests/httpx; phase sau: client HTTP phía Java |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-005-01

- **Given:** Code dùng requests/httpx trực tiếp hoặc client/session được xác định bằng gán và with/async with.
- **When:** người dùng phân tích.
- **Then:** công cụ xuất method, caller, URL biết được và vị trí lời gọi, kể cả async.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm alias import, Client, AsyncClient, Session.

### AC-L3GEN-005-02

- **Given:** URL ghép từ biến hoặc client dùng base_url chưa giải được.
- **When:** người dùng phân tích.
- **Then:** công cụ giữ biểu thức và phần URL biết được, gán partial; không gọi một path tương đối là host đầy đủ.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-PRIV-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm /health và settings.BASE_URL.

### AC-L3GEN-005-03

- **Given:** Biến local tên requests hoặc httpx che tên thư viện.
- **When:** người dùng phân tích.
- **Then:** công cụ không phân loại lời gọi của biến local thành HTTP của thư viện chỉ vì trùng tên.
- `constrained_by:` [NFR-L3GEN-ACC-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Fixture shadowing và method get của object nội bộ.

### AC-L3GEN-005-04

- **Given:** Test client gọi chính ứng dụng hoặc đích chưa xác định.
- **When:** người dùng xem dependency.
- **Then:** công cụ phân biệt HTTP nội bộ/đích chưa biết với external host đã xác nhận; không tuyên bố thêm external system không có bằng chứng.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Test thư mục integration-tests được loại và test client không bị gộp external host.

## Trạng thái liên kết triển khai

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-ACC-001](../nfr/NFR-L3GEN-ACC-001.md)
- [NFR-L3GEN-TRACE-001](../nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-COMP-001](../nfr/NFR-L3GEN-COMP-001.md)
- [NFR-L3GEN-PRIV-001](../nfr/NFR-L3GEN-PRIV-001.md)
- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../../domain/glossary-core.md)

