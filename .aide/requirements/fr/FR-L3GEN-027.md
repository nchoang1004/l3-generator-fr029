---
uid: "01M36700BC0FMT9SAMM7XRR33F"
key: "FR-L3GEN-027"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-006"],"constrained_by":["NFR-L3GEN-ACC-002","NFR-L3GEN-ABST-002"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-027 — Sinh tài liệu L3 contract

## Mô tả

Theo quy trình của mentor, L3 là contract: API, bảng dữ liệu (TBL) và sự kiện (EVT), chia theo component sở hữu. Sơ đồ component là mức L2. FR này sinh tài liệu L3 cho repository được phân tích.

Định dạng theo đúng cấu trúc `tech-specs/` của mentor (execution guide mục A.1 và B.10): thư mục gốc, cách chia theo component và cách đặt tên file. Mỗi contract là một file `.md`: bảng cho người đọc, cộng một khối máy đọc được bên trong.

```text
<thư mục output>/
  README.md                                  mục lục, sơ đồ component, phần giới hạn
  tech-specs/
    <CMP-slug>/                              chỉ component sở hữu ít nhất một API, TBL hoặc EVT
      api/API-<SYS>-<CMP>-v1.md              bảng endpoint + khối OpenAPI 3.1
      schema/TBL-<SYS>-<CMP>.md              bảng cột + khối DDL
      events/EVT-<SYS>-<CMP>-<topic>.md      producer, consumer + schema payload
```

Quy tắc đặt tên:

| Phần | Lấy từ | Ví dụ |
|---|---|---|
| `<SYS>` | Tên repository: viết hoa, bỏ dấu, ký tự không phải chữ hoặc số đổi thành `-` | `fastapi-shop` → `FASTAPI-SHOP` |
| `<CMP-slug>`, `<CMP>` | Tên component, cùng quy tắc; trùng thì thêm `-2`, `-3` | `Order Service` → `ORDER-SERVICE` |
| `-v1` | Luôn là `v1`: mỗi lần chạy sinh mới toàn bộ, không so với lần chạy trước | `API-FASTAPI-SHOP-ORDER-SERVICE-v1.md` |

`README.md` nằm ngoài `tech-specs/` vì mẫu của mentor không có file mục lục. Component không sở hữu contract nào thì không có thư mục.

Mỗi file có frontmatter ghi là bản sinh tự động, định danh snapshot và component sở hữu. Mỗi dòng trỏ về dữ kiện code làm bằng chứng. OpenAPI dựng từ phân tích tĩnh, không chạy code của repository. Nội dung sinh từ cùng mô hình với sơ đồ và JSON.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Sử dụng kết quả |
| Ưu tiên | Must Have |
| Mốc | M1 cho API và TBL; M3 cho EVT |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-027-01

- **Given:** Lần chạy đã trích được route và request/response model theo FR-L3GEN-021.
- **When:** công cụ sinh tài liệu L3.
- **Then:** mỗi component có route sinh một file API gồm bảng endpoint (method, path đầy đủ, handler, request model, response model, status code, dependency hoặc auth nếu xác định được) và một khối OpenAPI 3.1 cùng nội dung. Trường không xác định được ghi `unknown` kèm lý do; mỗi dòng trỏ về dữ kiện code làm bằng chứng.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-027-02

- **Given:** Lần chạy đã trích được lớp dữ liệu ánh xạ tới bảng theo FR-L3GEN-021.
- **When:** công cụ sinh tài liệu L3.
- **Then:** mỗi component sở hữu bảng sinh một file TBL gồm bảng cột (tên, kiểu, khóa chính, khóa ngoại, nullable) và một khối DDL cùng nội dung. Tên bảng hoặc kiểu không xác định được ghi `unknown` kèm lý do, không suy từ tên lớp; mỗi dòng trỏ về dữ kiện code làm bằng chứng.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-027-03

- **Given:** Lần chạy đã trích được quan hệ phát hoặc nhận sự kiện theo FR-L3GEN-021.
- **When:** công cụ sinh tài liệu L3.
- **Then:** mỗi topic sinh một file EVT gồm topic, component phát, component nhận và schema payload nếu biết. Không nối producer với consumer chỉ vì cùng tên topic khi broker hoặc cấu hình chưa xác định; phần đó ghi `unknown` kèm lý do.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)
- [Execution guide](../../../docs/agentic-sdlc-execution-guide.md), mục A.1 và B.10 — định nghĩa L3 và định dạng API/TBL/EVT
