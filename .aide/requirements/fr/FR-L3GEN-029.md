---
uid: "01M3XDXBVVDE88EXHN9ADHMD5D"
key: "FR-L3GEN-029"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-005","GOAL-L3GEN-006"],"constrained_by":["NFR-L3GEN-ACC-002","NFR-L3GEN-ABST-002","NFR-L3GEN-OPS-001","NFR-L3GEN-SEC-002"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-029 — Tài liệu L3 API và cấu trúc component

## Mô tả

Theo quy trình mentor, L3 là contract: API, bảng dữ liệu (TBL) và sự kiện (EVT), chia theo component sở hữu. FR này sinh phần API, trong cùng lần chạy với sơ đồ của FR-L3GEN-028. FR-L3GEN-030 sinh TBL, FR-L3GEN-031 sinh EVT.

FR này cũng sinh hai mục trong `README.md` cho bốn thứ Đề bài 3.6 yêu cầu phát hiện mà contract không chứa: module/package, service, repository/data access, và lời gọi HTTP ra ngoài.

Revision 2 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: thêm mục "Cấu trúc component" và "Lời gọi HTTP ra ngoài"; đối chiếu với sơ đồ qua `archdia.json`. Revision 3 (02/10/2026) sửa theo recovery review REVIEW-SCOPE-L3GEN-2026-003: route khai không qua decorator ghi ở phần giới hạn; nhãn của lời gọi HTTP; thư mục của component bị cắt khỏi hình.

### Đầu ra

Theo mẫu `tech-specs/` của mentor (execution guide mục A.1 và B.10):

```text
<thư mục output>/
  README.md                                  mục lục contract, sơ đồ, cấu trúc component,
                                             lời gọi HTTP ra ngoài, phần giới hạn
  result.json                                toàn bộ dữ kiện và bằng chứng của lần chạy
  tech-specs/
    <CMP-slug>/                              chỉ component sở hữu ít nhất một contract
      api/API-<SYS>-<CMP>-v1.md
```

| Phần | Lấy từ | Ví dụ |
|---|---|---|
| `<SYS>` | Tên repository: viết hoa, bỏ dấu, ký tự không phải chữ hoặc số đổi thành `-` | `fastapi-shop` → `FASTAPI-SHOP` |
| `<CMP-slug>`, `<CMP>` | Tên component của FR-L3GEN-028, cùng quy tắc; trùng thì thêm `-2`, `-3` | `Dữ liệu dùng chung` → `DU-LIEU-DUNG-CHUNG` |
| `-v1` | Luôn là `v1`: mỗi lần chạy sinh mới toàn bộ, không so với lần chạy trước | `API-FASTAPI-SHOP-ITEMS-v1.md` |

### Nội dung một file API

| Mục | Nội dung |
|---|---|
| Frontmatter | Ghi là bản sinh tự động, chưa được chủ repository duyệt; định danh snapshot; component sở hữu; mã các dữ kiện và bằng chứng dùng trong file |
| Endpoint | Bảng một dòng mỗi route: method, path đầy đủ, tham số (tên, vị trí path/query/header/body, kiểu, bắt buộc), request model, response model, status code, dependency hoặc auth, nhãn mức chắc chắn, mã dữ kiện |
| Model | Mỗi request/response model một bảng: tên trường, kiểu, bắt buộc, nullable; ghi vị trí khai báo. Model lồng nhau có mục riêng |
| Truy vết | Mã dữ kiện đầy đủ và `file:dòng` của từng route và model |
| Khối máy | Một khối OpenAPI 3.1 cùng nội dung với bảng |

### Cấu trúc component trong README

Mỗi component (trừ Kiểm thử, Migration, Khác) liệt kê package (thư mục) và module (file) thành viên. Mỗi file ghi một vai trò theo dấu hiệu trong code, kèm dòng code làm bằng chứng. Xét từ trên xuống, dừng ở dấu hiệu đầu tiên khớp.

| Vai trò | Dấu hiệu |
|---|---|
| Điểm vào | Như mục "Phạm vi đọc" của FR-L3GEN-028 |
| Route | Decorator route của `FastAPI` hoặc `APIRouter` |
| Model bảng | Lớp có `__tablename__`, lớp SQLModel có `table=True`, `Table(...)` |
| Hạ tầng | Dòng tạo engine hoặc client tới hệ thống ngoài, như mục "Phạm vi đọc" của FR-L3GEN-028 |
| Truy cập dữ liệu | Gọi method trên session CSDL hoặc dựng truy vấn |
| Schema API | Lớp được route dùng làm request hoặc response model |
| Cấu hình | Lớp kế thừa `BaseSettings`; đọc `os.environ`, `os.getenv` |
| Service | Không có dấu hiệu trên, nhưng nằm trên đường gọi từ route tới file truy cập dữ liệu hoặc hạ tầng |
| Khác | Không có dấu hiệu nào. Không đoán vai trò theo tên file |

Vai trò Service mang nhãn `inferred`, lý do "nằm trên đường gọi"; các vai trò còn lại mang nhãn `exact`.

### Lời gọi HTTP ra ngoài trong README

Một dòng mỗi lời gọi qua `httpx`, `requests`, `aiohttp`:

| Cột | Nội dung |
|---|---|
| Component | Component chứa dòng gọi |
| Thư viện, method | Ví dụ `httpx`, `GET`; method không đọc được thì `unknown` |
| Đích | URL nguyên văn, hoặc khóa cấu hình chứa URL, nhãn `exact`; đích chỉ biết lúc chạy thì `unknown` kèm lý do |
| Bằng chứng | `file:dòng` kèm nguyên văn |

Thư viện HTTP khác ghi ở phần giới hạn kèm nơi dùng.

### Chia theo component

- API thuộc component chứa file khai báo route, theo cách chia của FR-L3GEN-028. Nơi gọi API không đổi chủ sở hữu.
- Vì cùng cách chia, mỗi thư mục trong `tech-specs/` là một component trong `archdia.json`, và tập route trong tài liệu API bằng tập route trong `archdia.json`. Component bị cắt khỏi hình sơ đồ theo trần node của NFR-L3GEN-ABST-002 vẫn có thư mục nếu sở hữu contract.
- Route khai trong file test hoặc thư mục nằm ngoài phạm vi phân tích không vào tài liệu.
- Route khai không qua decorator (`add_api_route`, `add_route`, `add_websocket_route`) chưa được đọc ở đợt này. Mỗi lời gọi như vậy ghi ở phần giới hạn kèm nơi dùng, không bị bỏ qua im lặng.

### Khi chưa đủ dữ kiện

Xuất phần biết được. Trường không xác định được ghi `unknown` kèm lý do. Giá trị lấy từ mặc định có tài liệu của framework (ví dụ status 200 khi không khai) ghi `inferred` kèm tên quy tắc. Prefix đọc từ cấu hình lấy giá trị mặc định khai trong code nếu có; không có thì ghi `unknown`. Không suy kiểu từ tên biến. Khối OpenAPI chỉ chứa phần biểu diễn được đúng định dạng; route không biểu diễn được thì ghi rõ bị bỏ khỏi khối và lý do.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tài liệu L3 |
| Ưu tiên | Must Have |
| Mốc | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-029-01

- **Given:** Repository khai route FastAPI bằng decorator của `FastAPI` hoặc `APIRouter`, kể cả router gắn qua `include_router` hoặc `mount` có prefix.
- **When:** công cụ sinh tài liệu L3.
- **Then:** mỗi component có route có một file API theo mục "Nội dung một file API". Mỗi route có method, path đầy đủ gồm mọi prefix, handler và vị trí khai báo; mỗi dòng trỏ về dữ kiện code làm bằng chứng.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-029-02

- **Given:** Handler khai tham số path, query, header hoặc khai kiểu Pydantic cho request body hay response.
- **When:** công cụ sinh tài liệu L3.
- **Then:** tài liệu ghi từng tham số với vị trí, kiểu, bắt buộc; ghi tên request/response model cùng các trường, kiểu, bắt buộc, nullable và vị trí khai báo; ghi status code khai trong code.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-029-03

- **Given:** Một trường của route không xác định được từ source, hoặc chỉ biết qua mặc định của framework.
- **When:** công cụ sinh tài liệu L3.
- **Then:** trường đó ghi `unknown` kèm lý do, hoặc `inferred` kèm tên quy tắc, theo mục "Khi chưa đủ dữ kiện"; lần chạy vẫn xuất tài liệu cho phần biết được.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-029-04

- **Given:** Cùng một lần chạy sinh cả sơ đồ của FR-L3GEN-028 và tài liệu API.
- **When:** người dùng đối chiếu hai đầu ra.
- **Then:** tập route trong tài liệu API bằng tập route trong `archdia.json`; mỗi thư mục trong `tech-specs/` ứng với đúng một component trong `archdia.json`.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-029-05

- **Given:** Repository có route khai trong file test, trong thư mục ngoài phạm vi phân tích, hoặc khai qua `add_api_route`, `add_route`, `add_websocket_route`.
- **When:** công cụ sinh tài liệu L3.
- **Then:** các route đó không vào tài liệu API và không vào sơ đồ; mỗi lời gọi `add_api_route`, `add_route`, `add_websocket_route` được nêu ở phần giới hạn kèm `file:dòng`.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-029-06

- **Given:** Lần chạy sinh xong các file API.
- **When:** người dùng mở `README.md`.
- **Then:** README có mục lục trỏ tới từng file contract kèm component sở hữu, sơ đồ component, mục "Cấu trúc component", mục "Lời gọi HTTP ra ngoài", danh sách contract chưa gán được component, và phần giới hạn của lần chạy.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-029-07

- **Given:** Repository có file mang các dấu hiệu ở mục "Cấu trúc component trong README", và có file không mang dấu hiệu nào.
- **When:** công cụ sinh README.
- **Then:** mỗi file của component được liệt kê dưới package của nó với đúng một vai trò và dòng code làm bằng chứng; vai trò Service mang nhãn `inferred` kèm lý do; file không có dấu hiệu ghi "Khác", không có vai trò đoán theo tên.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-029-08

- **Given:** Repository gọi HTTP ra ngoài qua `httpx`, `requests` hoặc `aiohttp`, gồm cả lời gọi có URL chỉ biết lúc chạy.
- **When:** công cụ sinh README.
- **Then:** mỗi lời gọi có một dòng ở mục "Lời gọi HTTP ra ngoài" với component, thư viện, method, đích và bằng chứng; đích chỉ biết lúc chạy ghi `unknown` kèm lý do; lời gọi qua thư viện HTTP khác được nêu ở phần giới hạn.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [FR-L3GEN-028](FR-L3GEN-028.md)
