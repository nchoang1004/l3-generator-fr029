---
uid: "01M36700BC0FMT9SAMM7XRR33F"
key: "FR-L3GEN-027"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 3
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

### Chia tài liệu theo component

- API đặt ở component chứa nơi khai báo route; bảng đặt ở component chứa khai báo bảng/model ánh xạ. Nơi gọi API hoặc dùng bảng chỉ tham chiếu, không đổi chủ sở hữu.
- EVT đặt ở từng component có điểm gửi hoặc nhận. Mỗi file mô tả vai trò của chính component đó; không có nghĩa component sở hữu độc quyền topic. Ví dụ: mục Đơn hàng ghi gửi `order-created`, mục Kho ghi nhận `order-created`.
- Trong một component, các điểm gửi/nhận cùng topic chỉ gom khi có bằng chứng cùng broker/cấu hình. Khác broker hoặc chưa chứng minh được thì giữ riêng. Tên topic dùng quy tắc chuẩn hóa như tên component; trùng tên file thì thêm `-2`, `-3` theo thứ tự nguồn ổn định. Topic chưa biết dùng nhãn file từ mã dữ kiện, không coi nhãn đó là tên topic thật.
- Chỉ liên kết tài liệu hai bên khi có bằng chứng nối được chúng. Chỉ thấy bên nhận vẫn xuất EVT, ghi bên gửi `unknown` kèm lý do. Nhiều bên phát không phải chọn một bên làm chủ; mỗi bên có tài liệu về phần mình. README lập mục lục để tra cứu các file.

### Khi chưa đủ dữ kiện

Xuất phần biết được; tài liệu và kết quả ghi rõ `partial`, trường thiếu và lý do. Markdown ghi `unknown`; khối máy chỉ chứa phần biểu diễn được đúng định dạng. Nếu không dựng được khối máy hợp lệ, ghi rõ không có khối đó và lý do, không tạo giá trị giả. SQL dialect (biến thể SQL) lấy từ source; chưa xác định thì ghi chưa biết, không mặc định PostgreSQL.

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
- **Then:** mỗi component có điểm gửi/nhận sinh file EVT theo quy tắc chia tài liệu ở trên. File ghi topic, vai trò gửi/nhận của component, các bên liên quan đã xác minh và schema payload nếu biết. Chỉ thấy bên nhận hoặc có nhiều bên phát vẫn xuất được tài liệu. Không nối producer với consumer chỉ vì cùng tên topic khi broker hoặc cấu hình chưa xác định; phần đó ghi `unknown` kèm lý do và đánh dấu `partial`.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)
- [Quyết định về chia tài liệu và dữ liệu thiếu](../../evidence/requests/CR-L3GEN-2026-003-decisions-01.yaml)
- [Execution guide](../../../docs/agentic-sdlc-execution-guide.md), mục A.1 và B.10 — định nghĩa L3 và định dạng API/TBL/EVT
