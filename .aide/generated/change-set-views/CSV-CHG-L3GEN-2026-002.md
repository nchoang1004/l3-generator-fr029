---
key: CSV-CHG-L3GEN-2026-002
group: derived
non_normative: true
derived_from: [BL-CHG-L3GEN-2026-002-r6]
hand_written: false
status: candidate
generated_by: scripts/prd_package.py render --baseline BL-r6.yaml
---

# Làm lại phạm vi — mô hình ngôn ngữ đề xuất, code kiểm bằng chứng

Bản ứng viên chưa duyệt, sinh từ `BL-CHG-L3GEN-2026-002-r6`. Khi view và nguồn bất đồng, **FR/NFR/PRD nguồn thắng**; sửa nguồn rồi chạy lại script render. Không dùng view này như approval.

Gồm 4 FR, 5 NFR và 1 OBS trong baseline.

## 1. Mục tiêu

Bốn mục tiêu, xếp theo thứ tự: sinh ra được gì, rồi mới tới tin được tới đâu.

| Goal key | Mục tiêu | Liên kết KPI |
|---|---|---|
| GOAL-L3GEN-004 | Dựng được sơ đồ cấu trúc hệ thống ở mức application/component, phản ánh code đang chạy chứ không phải tài liệu cũ | KPI-L3GEN-006 |
| GOAL-L3GEN-005 | Mọi kết luận trên sơ đồ và tài liệu đều lần ngược được về đúng đoạn source sinh ra nó, để người đọc tự kiểm chứng thay vì phải tin | KPI-L3GEN-007 |
| GOAL-L3GEN-006 | Từ cùng mô hình đó sinh ra tài liệu L3 đủ để người mới đọc hiểu hệ thống mà không cần mở source | KPI-L3GEN-008 |
| GOAL-L3GEN-007 | Nói thật về giới hạn của chính mình: tách rõ phần đọc trực tiếp từ bằng chứng, phần suy ra, và phần không kết luận được, để người đọc biết chỗ nào tin ngay và chỗ nào phải tự kiểm | KPI-L3GEN-009, KPI-L3GEN-010 |

## 2. Mục tiêu nghiệp vụ đổi

Change Set này thay cho `CHG-L3GEN-2026-001`. Mọi GOAL/KPI mang key mới; GOAL/KPI của Change Set cũ không còn hiệu lực. Ánh xạ cũ sang mới ở PRD.

## 3. Tính năng mới

Toàn bộ FR trong candidate baseline; Must/Should và mốc nằm tại từng nguồn.

---

Nguồn: [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md) · revision 1 · status draft · SHA-256 `40d4a9f025690cb4ec5be3124e861899c1e5cbd6fed05dcdb549e9d68e4d9c46`

### FR-L3GEN-028 — Sơ đồ kiến trúc có bằng chứng

#### Mô tả

Developer chạy dòng lệnh trên một thư mục repository Python/FastAPI và nhận sơ đồ component cùng bản mô tả đi kèm. Sơ đồ cho người mới hình dung luồng xử lý của hệ thống: request đi vào đâu, qua component nào, tới dữ liệu và hệ thống ngoài nào. Mỗi khối, mũi tên, điểm vào và hệ thống ngoài có một dòng code làm bằng chứng.

Tài liệu L3 ở FR-L3GEN-029 đến 031 sinh trong cùng lần chạy và dùng đúng cách chia component của FR này.

##### Đầu ra

```text
<thư mục output>/
  archdia.md      sơ đồ Mermaid, bảng component, điểm vào, lời gọi giữa component,
                  hệ thống ngoài, khóa cấu hình, thư viện, phần giới hạn
  archdia.mmd     mã nguồn sơ đồ
  archdia.json    cùng nội dung, cho công cụ khác đọc
```

Bằng chứng ghi dạng `file:dòng| nguyên văn dòng code`, đường dẫn tính từ gốc repository.

##### Component là gì

Theo quy trình mentor, component gánh một trách nhiệm nghiệp vụ và sở hữu contract của nó: API, bảng, sự kiện. Route, service, repository, model là cấu trúc bên trong một component, không phải component riêng.

| Loại | Gồm | Lên sơ đồ |
|---|---|---|
| Nghiệp vụ | Các route cùng trách nhiệm, file chỉ các route đó dùng, bảng do các route đó dùng nhiều nhất | Có |
| Dùng chung | File nhiều component nghiệp vụ cùng dùng, tách theo việc: hạ tầng theo loại kết nối (CSDL, Redis, SMTP...), dữ liệu dùng chung, tiện ích dùng chung | Có |
| Khởi động | File tạo app, gộp router, chạy chương trình | Có |
| Chưa xếp | File có code nhưng không route nào đi tới | Có, kèm dòng ở phần giới hạn |
| Kiểm thử, Migration, Khác | File test; file migration; file không có code (`__init__.py` rỗng, manifest) | Không; vẫn có trong `archdia.json` |

Mỗi file thuộc đúng một component.

##### Ai quyết phần nào

| Việc | Ai làm |
|---|---|
| Lần theo từng route xuống tới bảng và hệ thống ngoài; nhóm route theo file khai báo; xếp file vào nhóm | Code |
| Gộp các nhóm route cùng trách nhiệm nghiệp vụ; đặt tên và viết một câu trách nhiệm cho component | Mô hình ngôn ngữ, kèm mã một dòng code làm bằng chứng |
| Kiểm mỗi nhóm thuộc đúng một component, mã dòng có thật, nguyên văn khớp snapshot | Code |
| Dựng mũi tên giữa component từ lời gọi đã xác định đích | Code |

Model không tách nhóm route và không tự thêm mũi tên.

##### Mũi tên nào được vẽ

Sơ đồ chỉ vẽ luồng xử lý. Lời gọi có thật nhưng không thuộc luồng thì không vẽ.

| Vẽ | Không vẽ |
|---|---|
| Gọi service, repository, crud của component khác | Lắp ráp: container DI, tạo app, khởi động và tắt |
| Gọi method trên session CSDL hoặc client Redis | Chỉ nhận session/client rồi truyền đi, không gọi method |
| Tác vụ nền gọi service hoặc dữ liệu | Kiểm tra rồi quay về: xác thực, quyền, captcha |
| Component tới hệ thống ngoài: dòng tạo engine hoặc client có URL, host, DSN | Chỉ dùng model hoặc schema làm kiểu; log, metrics |

Mũi tên ghi số lời gọi gộp lại và tối đa ba dòng code làm bằng chứng.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Sơ đồ kiến trúc |
| Ưu tiên | Must Have |
| Mốc | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

#### Acceptance Criteria

##### AC-L3GEN-028-01

- **Given:** Một thư mục source đọc được, chứa ứng dụng FastAPI, và một thư mục output ghi được.
- **When:** người dùng chạy phân tích qua dòng lệnh.
- **Then:** công cụ ghi `archdia.md`, `archdia.mmd`, `archdia.json` vào thư mục output và in đường dẫn các file. Bản mô tả có: các component cùng số route và tên bảng mỗi component sở hữu; điểm vào; lời gọi giữa component; hệ thống ngoài; khóa cấu hình; thư viện khai trong manifest; phần giới hạn.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-02

- **Given:** Đường dẫn source không tồn tại, không đọc được, thư mục output không ghi được, hoặc hai thư mục lồng nhau.
- **When:** người dùng chạy phân tích.
- **Then:** công cụ dừng trước khi phân tích, nêu nguyên nhân và cách sửa, không tạo output dở dang và không ghi vào cây source.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-03

- **Given:** Repository có route, bảng và lời gọi giữa các file.
- **When:** công cụ chia component.
- **Then:** công cụ chia theo bảng "Ai quyết phần nào": code nhóm và xếp file, mô hình ngôn ngữ gộp nhóm và đặt tên kèm mã dòng, code kiểm. Vi phạm thì gửi lại model một lần; vẫn sai thì loại phần sai kèm lý do. Mỗi file thuộc đúng một component theo bảng "Component là gì".
- `constrained_by:` [NFR-L3GEN-AI-002, NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-04

- **Given:** Hai component có lời gọi qua lại.
- **When:** công cụ dựng mũi tên.
- **Then:** chỉ lời gọi thuộc cột "Vẽ" thành mũi tên; lời gọi thuộc cột "Không vẽ" không lên sơ đồ. Lời gọi chưa xác định được đích không thành mũi tên mà được đếm ở phần giới hạn.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-05

- **Given:** Một khối, mũi tên, điểm vào hoặc hệ thống ngoài sắp được đưa lên sơ đồ.
- **When:** công cụ sinh kết quả.
- **Then:** mục đó có bằng chứng `file:dòng| nguyên văn`, và code kiểm nguyên văn khớp đúng dòng trong snapshot. Mục không có bằng chứng hợp lệ không được đưa lên.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-06

- **Given:** Model không khả dụng, hết ngân sách, vượt trần token, hoặc trả payload sai schema.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ vẫn ghi sơ đồ do code chia; component đặt tên theo đường dẫn và ghi rõ chưa được model gộp, đặt tên; trạng thái lần chạy là partial kèm nguyên nhân.
- `constrained_by:` [NFR-L3GEN-AI-002, NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-07

- **Given:** Có file lỗi cú pháp, file "Chưa xếp", lời gọi không xác định được đích, công cụ phân giải tên không chạy được, hoặc repository rỗng hay ngoài stack hỗ trợ.
- **When:** công cụ sinh kết quả.
- **Then:** từng phần đó hiện ở phần giới hạn kèm lý do và số lượng; không trả kết quả thành công rỗng.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-08

- **Given:** Repository có file test, migration và file không có code.
- **When:** công cụ vẽ sơ đồ.
- **Then:** sơ đồ chỉ có node mức component và hệ thống ngoài, trong trần số node của NFR-L3GEN-ABST-002; component Kiểm thử, Migration, Khác không lên sơ đồ nhưng có trong `archdia.json`.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md) · revision 1 · status draft · SHA-256 `561bc6866c4df317921b6a96e9cd1dd025f74d7668ca12ebe21008490ee8d063`

### FR-L3GEN-029 — Tài liệu L3 API theo component

#### Mô tả

Theo quy trình mentor, L3 là contract: API, bảng dữ liệu (TBL) và sự kiện (EVT), chia theo component sở hữu. FR này sinh phần API, trong cùng lần chạy với sơ đồ của FR-L3GEN-028. FR-L3GEN-030 sinh TBL, FR-L3GEN-031 sinh EVT.

##### Đầu ra

Theo mẫu `tech-specs/` của mentor (execution guide mục A.1 và B.10):

```text
<thư mục output>/
  README.md                                  mục lục contract, sơ đồ, phần giới hạn
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

##### Nội dung một file API

| Mục | Nội dung |
|---|---|
| Frontmatter | Ghi là bản sinh tự động, chưa được chủ repository duyệt; định danh snapshot; component sở hữu; mã các dữ kiện và bằng chứng dùng trong file |
| Endpoint | Bảng một dòng mỗi route: method, path đầy đủ, tham số (tên, vị trí path/query/header/body, kiểu, bắt buộc), request model, response model, status code, dependency hoặc auth, nhãn mức chắc chắn, mã dữ kiện |
| Model | Mỗi request/response model một bảng: tên trường, kiểu, bắt buộc, nullable; ghi vị trí khai báo. Model lồng nhau có mục riêng |
| Truy vết | Mã dữ kiện đầy đủ và `file:dòng` của từng route và model |
| Khối máy | Một khối OpenAPI 3.1 cùng nội dung với bảng |

##### Chia theo component

- API thuộc component chứa file khai báo route, theo cách chia của FR-L3GEN-028. Nơi gọi API không đổi chủ sở hữu.
- Vì cùng cách chia, mỗi thư mục trong `tech-specs/` là một khối trên sơ đồ, và tập route trong tài liệu API bằng tập route trên sơ đồ.
- Route khai trong file test hoặc thư mục nằm ngoài phạm vi phân tích không vào tài liệu.

##### Khi chưa đủ dữ kiện

Xuất phần biết được. Trường không xác định được ghi `unknown` kèm lý do. Giá trị lấy từ mặc định có tài liệu của framework (ví dụ status 200 khi không khai) ghi `inferred` kèm tên quy tắc. Prefix đọc từ cấu hình lấy giá trị mặc định khai trong code nếu có; không có thì ghi `unknown`. Không suy kiểu từ tên biến. Khối OpenAPI chỉ chứa phần biểu diễn được đúng định dạng; route không biểu diễn được thì ghi rõ bị bỏ khỏi khối và lý do.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tài liệu L3 |
| Ưu tiên | Must Have |
| Mốc | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

#### Acceptance Criteria

##### AC-L3GEN-029-01

- **Given:** Repository khai route FastAPI bằng decorator của `FastAPI` hoặc `APIRouter`, kể cả router gắn qua `include_router` hoặc `mount` có prefix.
- **When:** công cụ sinh tài liệu L3.
- **Then:** mỗi component có route có một file API theo mục "Nội dung một file API". Mỗi route có method, path đầy đủ gồm mọi prefix, handler và vị trí khai báo; mỗi dòng trỏ về dữ kiện code làm bằng chứng.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-029-02

- **Given:** Handler khai tham số path, query, header hoặc khai kiểu Pydantic cho request body hay response.
- **When:** công cụ sinh tài liệu L3.
- **Then:** tài liệu ghi từng tham số với vị trí, kiểu, bắt buộc; ghi tên request/response model cùng các trường, kiểu, bắt buộc, nullable và vị trí khai báo; ghi status code khai trong code.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-029-03

- **Given:** Một trường của route không xác định được từ source, hoặc chỉ biết qua mặc định của framework.
- **When:** công cụ sinh tài liệu L3.
- **Then:** trường đó ghi `unknown` kèm lý do, hoặc `inferred` kèm tên quy tắc, theo mục "Khi chưa đủ dữ kiện"; lần chạy vẫn xuất tài liệu cho phần biết được.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-029-04

- **Given:** Cùng một lần chạy sinh cả sơ đồ của FR-L3GEN-028 và tài liệu API.
- **When:** người dùng đối chiếu hai đầu ra.
- **Then:** tập route trong tài liệu API bằng tập route trên sơ đồ; mỗi thư mục trong `tech-specs/` ứng với đúng một component trên sơ đồ.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-029-05

- **Given:** Repository có route khai trong file test hoặc trong thư mục ngoài phạm vi phân tích.
- **When:** công cụ sinh tài liệu L3.
- **Then:** các route đó không vào tài liệu API và không vào sơ đồ.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-029-06

- **Given:** Lần chạy sinh xong các file API.
- **When:** người dùng mở `README.md`.
- **Then:** README có mục lục trỏ tới từng file contract kèm component sở hữu, sơ đồ component, danh sách contract chưa gán được component, và phần giới hạn của lần chạy.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md) · revision 1 · status draft · SHA-256 `01843e64ea7380077356b65ecd8f90098a461aca13d1bec84c3e804d0becf9a9`

### FR-L3GEN-030 — Tài liệu L3 bảng dữ liệu theo component

#### Mô tả

FR này sinh phần bảng dữ liệu (TBL) của tài liệu L3, trong cùng lần chạy và cùng thư mục output với FR-L3GEN-029.

##### Đầu ra

```text
tech-specs/<CMP-slug>/schema/TBL-<SYS>-<CMP>.md
```

`<SYS>`, `<CMP-slug>`, `<CMP>` đặt theo quy tắc của FR-L3GEN-029. Một component có một file TBL, chứa mọi bảng nó sở hữu.

##### Nội dung một file TBL

| Mục | Nội dung |
|---|---|
| Frontmatter | Như file API của FR-L3GEN-029 |
| Mỗi bảng | Tên bảng, lớp model và vị trí khai báo; bảng cột: tên, kiểu, khóa chính, khóa ngoại (bảng và cột đích), nullable |
| Truy vết | Mã dữ kiện đầy đủ và `file:dòng` của từng bảng và cột |
| Khối máy | Một khối DDL cùng nội dung, theo biến thể SQL của repository |

##### Phạm vi đọc

| Đọc được | Ghi ở phần giới hạn |
|---|---|
| Lớp SQLAlchemy có `__tablename__`, lớp SQLModel có `table=True`, `Table(...)` của SQLAlchemy | ORM khác (Tortoise, Peewee, Beanie...), SQL viết tay, bảng chỉ khai trong file migration |

##### Chia theo component

- Bảng thuộc component chứa file khai báo model, theo cách chia của FR-L3GEN-028. Nơi đọc hoặc ghi bảng không đổi chủ sở hữu.
- Một file khai nhiều bảng thì mọi bảng trong file theo component của file đó.

##### Khi chưa đủ dữ kiện

Tên bảng sinh lúc chạy ghi `unknown` kèm nguồn; không suy tên bảng từ tên lớp. Biến thể SQL lấy từ dòng tạo engine hoặc URL kết nối trong source; chưa xác định thì kiểu cột ghi `unknown` kèm kiểu khai trong code, và không có khối DDL, ghi rõ lý do. Không mặc định PostgreSQL.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tài liệu L3 |
| Ưu tiên | Must Have |
| Mốc | M2 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

#### Acceptance Criteria

##### AC-L3GEN-030-01

- **Given:** Repository khai bảng theo cột "Đọc được" của mục "Phạm vi đọc".
- **When:** công cụ sinh tài liệu L3.
- **Then:** mỗi component sở hữu bảng có một file TBL theo mục "Nội dung một file TBL"; mỗi dòng trỏ về dữ kiện code làm bằng chứng.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-030-02

- **Given:** Source cho biết biến thể SQL qua dòng tạo engine hoặc URL kết nối.
- **When:** công cụ sinh tài liệu L3.
- **Then:** kiểu cột ghi theo biến thể đó và file có khối DDL cùng nội dung với bảng cột.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-030-03

- **Given:** Tên bảng sinh lúc chạy, kiểu cột không xác định, hoặc chưa biết biến thể SQL.
- **When:** công cụ sinh tài liệu L3.
- **Then:** trường đó ghi `unknown` kèm lý do theo mục "Khi chưa đủ dữ kiện"; thiếu dữ kiện cho DDL thì ghi rõ không có khối DDL và lý do.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-030-04

- **Given:** Repository dùng cách khai bảng thuộc cột "Ghi ở phần giới hạn".
- **When:** công cụ sinh tài liệu L3.
- **Then:** phần giới hạn nêu thư viện hoặc cách khai đó và nơi dùng; không ghi là repository không có bảng.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-030-05

- **Given:** Cùng một lần chạy sinh cả sơ đồ của FR-L3GEN-028 và tài liệu TBL.
- **When:** người dùng đối chiếu hai đầu ra.
- **Then:** mỗi bảng trên sơ đồ nằm trong file TBL của đúng component đó, và ngược lại.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md) · revision 1 · status draft · SHA-256 `92054489a162bf9c587a75d1714a7f50ff90b25d41a1cfb9dd83f673b1ff4afd`

### FR-L3GEN-031 — Tài liệu L3 sự kiện và tác vụ nền theo component

#### Mô tả

FR này sinh phần sự kiện (EVT) của tài liệu L3, trong cùng lần chạy và cùng thư mục output với FR-L3GEN-029.

##### Đầu ra

```text
tech-specs/<CMP-slug>/events/EVT-<SYS>-<CMP>-<topic>.md
```

`<SYS>`, `<CMP-slug>`, `<CMP>` đặt theo quy tắc của FR-L3GEN-029. `<topic>` là tên topic hoặc tên tác vụ, chuẩn hóa cùng quy tắc; trùng tên file thì thêm `-2`, `-3` theo thứ tự nguồn ổn định. Topic chưa biết dùng nhãn từ mã dữ kiện, không coi nhãn đó là tên topic thật. README của FR-L3GEN-029 có thêm mục lục EVT theo topic.

##### Phạm vi đọc

| Loại | Bên gửi | Bên nhận |
|---|---|---|
| Kafka, FastStream | `send`, `publish` tới một topic | Consumer hoặc subscriber của topic |
| Celery | `.delay`, `.apply_async`, `send_task` | Hàm có `@app.task`, `@shared_task` |
| FastAPI `BackgroundTasks` | `add_task(hàm, ...)` | Hàm được truyền vào |

Broker và thư viện hàng đợi khác (RabbitMQ thuần, Redis Streams, taskiq, arq...) ghi ở phần giới hạn.

##### Nội dung một file EVT

| Mục | Nội dung |
|---|---|
| Frontmatter | Như file API của FR-L3GEN-029 |
| Sự kiện | Topic hoặc tên tác vụ; broker hoặc thư viện; vai trò của component này (gửi, nhận, hay cả hai) |
| Bên liên quan | Các bên gửi/nhận khác đã xác minh, kèm component của họ |
| Payload | Schema payload nếu khai trong code; không thì `unknown` kèm lý do |
| Truy vết | `file:dòng` của từng điểm gửi và nhận |

##### Chia theo component

- EVT đặt ở từng component có điểm gửi hoặc nhận. Mỗi file mô tả vai trò của chính component đó, không có nghĩa component sở hữu độc quyền topic. Ví dụ: component Đơn hàng ghi gửi `order-created`, component Kho ghi nhận `order-created`.
- Trong một component, các điểm cùng topic chỉ gom vào một file khi có bằng chứng cùng broker hoặc cấu hình.
- Chỉ nối bên gửi với bên nhận khi có bằng chứng cùng broker hoặc cùng hàm tác vụ; không nối chỉ vì trùng tên topic.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tài liệu L3 |
| Ưu tiên | Should Have |
| Mốc | M3 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

#### Acceptance Criteria

##### AC-L3GEN-031-01

- **Given:** Repository gửi hoặc nhận sự kiện theo bảng "Phạm vi đọc".
- **When:** công cụ sinh tài liệu L3.
- **Then:** mỗi component có điểm gửi/nhận có file EVT theo mục "Nội dung một file EVT"; mỗi dòng trỏ về dữ kiện code làm bằng chứng.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-031-02

- **Given:** Chỉ thấy một bên, có nhiều bên gửi, hoặc hai bên cùng tên topic nhưng chưa xác định cùng broker.
- **When:** công cụ sinh tài liệu L3.
- **Then:** vẫn xuất tài liệu cho mỗi bên thấy được; bên chưa xác minh ghi `unknown` kèm lý do và file đánh dấu `partial`; không nối hai bên chỉ vì trùng tên.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-031-03

- **Given:** Repository dùng broker hoặc thư viện hàng đợi ngoài bảng "Phạm vi đọc".
- **When:** công cụ chạy phân tích.
- **Then:** phần giới hạn nêu thư viện đó và nơi dùng; không ghi là repository không có sự kiện.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-031-04

- **Given:** Cùng một lần chạy sinh cả sơ đồ của FR-L3GEN-028 và tài liệu EVT.
- **When:** người dùng đối chiếu hai đầu ra.
- **Then:** mũi tên tác vụ nền trên sơ đồ có điểm gửi và điểm nhận tương ứng trong tài liệu EVT của hai component đó.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## 4. Thay đổi hành vi hiện có

Không có FR nào bump revision: mọi FR trong baseline này mang key mới. FR của `CHG-L3GEN-2026-001` đã deprecated; ánh xạ cũ sang mới ở PRD mục IV.3. PRD không lấy hành vi code hiện tại làm chuẩn.

## 5. NGOÀI phạm vi lần này

**Giao diện web.** Nhận ZIP hoặc URL GitHub, theo dõi lần chạy, khám phá kết quả và mở bằng chứng trên giao diện. Thuộc phase sau; mock giao diện đã có giữ làm đầu vào.

**Phạm vi phân tích.** Ngôn ngữ và framework ngoài Python/FastAPI, kể cả Java/Spring Boot. Broker ngoài Kafka và thư viện hàng đợi ngoài Celery, `BackgroundTasks`. ORM ngoài SQLAlchemy/SQLModel. Thực thi source để khám phá runtime, dynamic import và metaprogramming tổng quát. Suy luận deployment topology.

**Mức trình bày.** Sơ đồ vẽ toàn bộ function hoặc class, call graph đầy đủ mức function. Repository Knowledge Graph nói chung (đề bài mục 3.8).

**Lịch sử và tích hợp.** Danh sách nhiều lần chạy, mở lại kết quả cũ, public API theo dõi trạng thái.

**Ghi ngược và phân tích thay đổi.** Sửa code hoặc tài liệu nguồn, tạo pull request. Rà code không dùng, kết luận lỗ hổng bảo mật hoặc lỗi nghiệp vụ. Change impact, test impact, architecture drift, incremental analysis.

**Truy cập và vận hành.** Repository private và mọi cơ chế nhận hoặc lưu credential. Đăng nhập, multi-tenant, SLA production.

**Mô hình ngôn ngữ.** Model chạy cục bộ; chi phí vượt trần của NFR-L3GEN-AI-002.

Các mục trên muốn đưa vào phạm vi đều cần đề xuất phạm vi và AC riêng.

Không có FR chuẩn tắc nào bị giấu khỏi candidate.

## 6. Ràng buộc mới

---

Nguồn: [NFR-L3GEN-ABST-002](../../requirements/nfr/NFR-L3GEN-ABST-002.md) · revision 3 · status draft · SHA-256 `baebe4e179d5b1395ab1ec162b61d057427e7186a87c0d8a5257af13b4157401`

### NFR-L3GEN-ABST-002 — Mức trừu tượng của kết quả trình bày

- **Nhóm:** Abstraction level.
- **Trạng thái:** thay cho NFR-L3GEN-ABST-001 của BL-r14, giữ nguyên phạm vi và ngưỡng. Ngưỡng 500/50 đã chốt tại OQ-L3GEN-004 (CHG-L3GEN-2026-001); revision 3 (02/10/2026) chỉ đổi phần áp dụng sang FR-L3GEN-028 đến 031; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md), [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md), [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md), [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md).
- **Quyết định nền:** [ADR-2026-001](../../architecture/adr/ADR-2026-001.md).

#### Yêu cầu có thể kiểm chứng

Phân tích và trình bày là hai mức khác nhau. Công cụ được đọc sâu tới function, tham số và phép gán để chứng minh một quan hệ, nhưng kết quả mặc định cho người đọc dừng ở application/component.

- Sơ đồ mặc định (mức L2) chỉ có node mức application, component và hệ thống ngoài. Node mức function, class hoặc file không xuất hiện ở lớp mặc định.
- Tài liệu L3 liệt kê contract: endpoint, bảng, sự kiện, chia theo component. Function và class chỉ xuất hiện khi là handler hoặc model được nêu trong contract, hoặc ở lớp bằng chứng.
- Số node của sơ đồ mặc định không tỷ lệ với số function của repository. Repository có từ 500 function trở lên vẫn cho sơ đồ mặc định không quá 50 node. Phần vượt trần không bị loại khỏi bộ kết quả mà nằm ở lớp bằng chứng; không xuất sơ đồ đầy đủ rồi để người đọc tự lọc.
- Dữ kiện mức function và class vẫn nằm trong bộ kết quả, nhưng ở lớp bằng chứng có nhãn riêng, không trộn vào lớp kiến trúc mặc định.
- Một quan hệ kiến trúc chỉ tồn tại khi đích đã xác định. Lời gọi chưa xác định được đích giữ ở lớp dữ kiện với nhãn unresolved, không nâng thành cạnh giữa hai component.

#### Điều kiện và cách kiểm

Chạy trên bộ dữ liệu đã pin, đếm node theo lớp trong `archdia.json` của FR-L3GEN-028, không đếm bằng mắt trên hình. Kiểm cả repository nhỏ và repository từ 500 function trở lên. Kiểm rằng bỏ lớp bằng chứng đi thì lớp kiến trúc vẫn đọc được, và mọi cạnh kiến trúc đều có đích đã xác định. Sơ đồ vẽ được không phải bằng chứng mức trừu tượng đúng.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)

---

Nguồn: [NFR-L3GEN-ACC-002](../../requirements/nfr/NFR-L3GEN-ACC-002.md) · revision 3 · status draft · SHA-256 `0355d3362d601cae5ab139fe82003594d51191df926dbdd0dcbb390054ffde35`

### NFR-L3GEN-ACC-002 — Độ đúng của kết quả và bằng chứng

- **Nhóm:** Accuracy.
- **Trạng thái:** ngưỡng dữ kiện L3 chốt tại OQ-L3GEN-007 ngày 22/09/2026. Ngưỡng sơ đồ theo tiêu chí nhóm dùng khi phát triển (Khiêm, 02/10/2026). Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md), [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md), [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md), [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md).

#### Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-ACC-001 và NFR-L3GEN-TRACE-001 của BL-r14.

**Độ đúng của dữ kiện L3.** Precision và recall đều phải đạt từ 80% trở lên, đo riêng cho từng loại: route, request/response model, entity/table, config, event, thư viện. Ngưỡng 80% chốt tại OQ-L3GEN-007.

**Độ đúng của sơ đồ (FR-L3GEN-028).** Đo trên cạnh giữa component, so với đáp án vẽ tay.

| Chỉ số | Ngưỡng |
|---|---|
| P: tỷ lệ mũi tên vẽ ra mà đúng | ≥ 0,8 |
| R: tỷ lệ mũi tên bắt buộc của đáp án mà sơ đồ có | ≥ 0,6 |
| Pk (P khắt khe): như P, nhưng mũi tên "chấp nhận được" của đáp án cũng tính sai | Luôn báo, không có ngưỡng |
| Bằng chứng do model trỏ (mã dòng) mà code kiểm hợp lệ | ≥ 90% |

Cách chấm:
- Mỗi component của công cụ được coi là component đáp án có nhiều file chung nhất với nó.
- Đáp án chia cạnh làm hai loại theo luật vẽ của FR-L3GEN-028: bắt buộc (luồng xử lý) và chấp nhận được (lắp ráp, chỉ truyền session, kiểm tra rồi quay về). Cạnh trùng bắt buộc là đúng; trùng chấp nhận được thì không tính ở P nhưng tính sai ở Pk; cạnh khác là sai.
- File không thuộc component nào của đáp án thì bỏ qua. File chỉ khai báo dạng dữ liệu (schema, enum, hằng số) mà đáp án không nhắc thì để ngoài đáp án.
- Báo kèm chấm luồng để thấy trường hợp đúng nhưng chia khác đáp án: R luồng (cạnh bắt buộc có hiện qua tối đa 3 mũi tên), P luồng (mũi tên ứng với luồng thật, trực tiếp hoặc qua một component trung gian), ARI (độ giống cách chia file). Chấm luồng chỉ đi kèm, không thay cách chấm trên.

Chấm thuộc tính riêng với chấm sự tồn tại: một route thiếu prefix không tính là route đúng, một tên bảng suy sai không tính là tên bảng đúng. Nhóm nào chưa đủ mẫu thì báo TP/FP/FN, không báo đạt.

**Bằng chứng.** Bằng chứng của một kết luận là các dữ kiện code trong tập dữ kiện của lần chạy, mỗi dữ kiện nằm ở file có thật trong snapshot đã phân tích. Với cạnh A→B, phải có ít nhất một dữ kiện đã xác định đích, vị trí thuộc A và đích thuộc B. Trên sơ đồ, bằng chứng ghi dạng `file:dòng| nguyên văn`, và code kiểm nguyên văn khớp đúng dòng trong snapshot. Code kiểm điều này; lời khẳng định của model không được tính là bằng chứng. Tỷ lệ kết luận công bố có bằng chứng hợp lệ phải đạt 100%, không có ngoại lệ: kết luận không thỏa thì bị loại trước khi xuất, không được hạ thành cảnh báo. Bằng chứng không được trỏ sang snapshot khác hoặc sang source hiện tại trên đĩa.

**Nhãn chất lượng.** Confidence, completeness và coverage là ba trục độc lập, không dùng trục này thay trục kia. Nhãn `exact` chỉ dùng cho kết luận đọc trực tiếp từ bằng chứng; kết luận suy ra mang nhãn `inferred` kèm lý do. Không được nâng `inferred` thành `exact` để kết quả trông chắc chắn hơn. Tỷ lệ nhãn khớp đánh giá người duyệt phải đạt từ 80% trở lên. Riêng tỷ lệ gán `exact` cho kết luận thật ra sai phải ở mức 5% trở xuống, và là chỉ số chặn: gán nhãn chắc chắn cho kết luận sai gây hại hơn bỏ sót, vì người đọc tin mà không kiểm lại.

#### Điều kiện và cách kiểm

OBS-L3GEN-001 quy định dataset, người lập đáp án độc lập, cách matching và cỡ mẫu tối thiểu. Nhóm nào chưa đủ mẫu thì báo counts và `not_evaluated`, không báo phần trăm.

Phần bằng chứng kiểm tự động trên mọi lần chạy: đối chiếu từng dữ kiện được trích dẫn với tập dữ kiện, từng đường dẫn với danh sách file của snapshot, và hai đầu của mỗi cạnh với vị trí và đích của dữ kiện. Máy kiểm được bằng chứng có tồn tại và nối đúng; việc dữ kiện có thật sự đủ ý nghĩa cho kết luận thì chấm bằng đáp án của người. Phần nhãn và độ đúng kiểm bằng đáp án do người lập trước khi xem output. Không loại ca khó ra khỏi mẫu sau khi đã xem kết quả.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)

---

Nguồn: [NFR-L3GEN-AI-002](../../requirements/nfr/NFR-L3GEN-AI-002.md) · revision 4 · status draft · SHA-256 `41ac1a1d98f3f70850ea61bd8d3c611a9763c8e220b681a72e222b885993dd83`

### NFR-L3GEN-AI-002 — Ranh giới, chi phí và truy vết của mô hình ngôn ngữ

- **Nhóm:** AI reliability.
- **Trạng thái:** revision 4 theo quyết định của Khiêm ngày 02/10/2026 (CR-L3GEN-2026-004, OQ-L3GEN-009): model bắt buộc, trả phí ít, qua OpenRouter. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md).

#### Yêu cầu có thể kiểm chứng

Thay revision 3 (Groq và Google, gói miễn phí, trần chi phí 0 đồng).

**Việc của model.** Model nhận kết quả code đã lần theo và trả về: các nhóm route cùng trách nhiệm nghiệp vụ cần gộp; tên và một câu trách nhiệm cho mỗi component; tên dùng chung nào thuộc riêng một component; chủ của bảng mà hai nhóm dùng ngang nhau. Mỗi quyết định trỏ một mã dòng code đã hiện cho model. Model không tách nhóm route, không thêm mũi tên, không sửa dữ kiện code và không tự công bố kết luận.

**Đầu vào gửi cho model.** Danh sách nhóm route (method, path, bảng và hệ thống ngoài mỗi route chạm, dòng khai báo route), tên dùng chung kèm dòng khai báo, bảng có chủ hòa, số lời gọi giữa các nhóm. Mỗi dòng code gửi đi mang một mã `[L12]`; model trả mã, code tra ra `file:dòng` và nguyên văn. Không gửi nguyên file source hoặc cả repository.

**Kiểm câu trả lời.** Câu trả lời phải đúng schema. Code kiểm: mỗi nhóm route thuộc đúng một component, tên dùng chung dùng tối đa một lần, mã dòng có trong danh sách đã gửi, chỉ khai chủ cho bảng có chủ hòa. Vi phạm thì gửi lại model một lần kèm danh sách lỗi; vẫn sai thì loại phần sai và ghi lý do.

**Provider và model.**

| Thuộc tính | Giá trị |
|---|---|
| Provider | OpenRouter |
| Model | `openai/gpt-6-luna` |
| Mức suy luận | trung bình |
| Tham số `temperature` | không gửi (model không nhận) |

Đổi model hoặc provider bằng cấu hình, không sửa code; mỗi lần đổi ghi vào provenance và chạy lại phép đo của OBS-L3GEN-001.

**Trần mỗi lần chạy.**

| Trần | Giá trị |
|---|---|
| Chi phí | ≤ 0,05 USD |
| Token vào và ra cộng lại | ≤ 100.000 |
| Request | ≤ 4 (một lần hỏi, một lần gửi lại, mỗi lần thử lại tối đa một lần khi lỗi mạng) |
| Độ dài câu trả lời | ≤ 12.000 token mỗi request |
| Timeout | 300 giây mỗi request |

Công cụ ước tính token trước request đầu tiên; vượt trần thì không gọi model và xử lý theo AC-L3GEN-028-06. Số tham khảo khi phát triển: 7 request trên 5 repo nhỏ, khoảng 25.000 token, 0,008 USD (02/10/2026).

**Thiếu model.** Thiếu khóa, hết ngân sách, chạm trần, provider lỗi hoặc trả sai schema thì dừng bước dùng model, giữ kết quả do code chia, trạng thái partial kèm nguyên nhân (AC-L3GEN-028-06). Không tự đổi sang model khác, không đoán để lấp chỗ trống.

**Bí mật.** Khóa API do người dùng cung cấp lúc chạy, không được ghi vào output, log, bằng chứng hay bộ kết quả lưu lại. Giá trị cấu hình mang dấu hiệu bí mật bị che trước khi vào payload gửi model.

**Tái lập.** Kết quả không bắt buộc giống hệt giữa các lần chạy. Mỗi lần chạy ghi provider, tên model, phiên bản prompt, phiên bản tool, định danh snapshot, số request, token và chi phí. Đây là yêu cầu ghi nhận, không phải ngưỡng chặn phát hành.

#### Điều kiện và cách kiểm

Dùng provider giả trả về JSON hỏng, mã dòng lạ, nhóm route dùng hai lần, timeout và lỗi mạng; kiểm phần không hợp lệ bị loại, lý do được ghi, và lần gửi lại có kèm lỗi. Đặt khóa API dạng đánh dấu rồi kiểm toàn bộ output, log và bằng chứng không chứa giá trị đó. Kiểm mỗi bộ kết quả có đủ trường truy vết. Chi phí lấy từ số provider trả về, không ước bằng giá giả định.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [OQ-L3GEN-009](../../lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/OQ-L3GEN-009.md)

---

Nguồn: [NFR-L3GEN-OPS-001](../../requirements/nfr/NFR-L3GEN-OPS-001.md) · revision 2 · status draft · SHA-256 `9f9dca65bb92d94bb5df6fbf42b128064adab2aa7dfa8832e99da7bd62878dd5`

### NFR-L3GEN-OPS-001 — Hiệu năng, độ tin cậy và phạm vi hỗ trợ

- **Nhóm:** Operability.
- **Trạng thái:** ngưỡng đã chốt; revision 2 (02/10/2026) đổi phần áp dụng sang FR-L3GEN-028 đến 031 và thêm công cụ phân giải tên vào ma trận hỗ trợ. Trần của model ở NFR-L3GEN-AI-002. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md), [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md), [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md), [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md).

#### Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-PERF-001, REL-001, COMP-001 và phần còn dùng được của USA-001 của BL-r14. Key OPS-001 chưa từng dùng trước đây.

**Thời gian và tài nguyên.** Mỗi lần chạy ghi lại riêng thời gian lấy source, phân tích tĩnh, gọi model và sinh artifact, cùng bộ nhớ đỉnh và kích thước output.

| Ngưỡng | Giá trị | Nguồn |
|---|---|---|
| Phân tích tĩnh và ghi output, không gồm lấy source và gọi model | ≤ 60 giây cho 5.000 dòng Python; ≤ 300 giây cho 50.000 dòng | Giữ từ BL-r14 |
| Máy đo chuẩn | 4 CPU logical, RAM 8 GiB, SSD, Python 3.12; máy khác thì công bố, không ngoại suy | Giữ từ BL-r14 |
| Bộ nhớ | ≤ 2 GiB mỗi lần chạy | Giữ từ BL-r14 |
| Toàn bộ một lần chạy | ≤ 30 phút; quá hạn thì dừng, trả partial kèm lý do | Mới. 100.000 token ở 8.000 token/phút cần ít nhất 12,5 phút; trần 10 phút của BL-r14 không còn đủ |
| Số lần chạy cùng lúc | 1; lần sau xếp hàng | Mới, vì các lần chạy dùng chung một quota model |

Trần tiếp nhận ở NFR-L3GEN-SEC-002; trần token ở NFR-L3GEN-AI-002. Vượt trần thì từ chối trước bước tương ứng, kèm lý do, không chạy dở rồi hỏng.

**Lỗi một phần.** Một đơn vị phân tích hỏng không làm hỏng cả lần chạy. Kết quả partial phải nêu rõ phạm vi đã xử lý được. Trạng thái của lần chạy là completed, partial hoặc failed, và phải phản ánh đúng thực tế: không có bộ output trông như hoàn chỉnh khi thực ra thiếu artifact.

**Phạm vi hỗ trợ.** Có một ma trận khai báo, cho mỗi ngôn ngữ và framework, độ sâu phân tích áp dụng và mức chất lượng đi kèm. Ma trận này là nguồn duy nhất để trả lời câu hỏi công cụ hỗ trợ gì; phase đầu chỉ Python/FastAPI có mức hỗ trợ đầy đủ. Ma trận ghi cả công cụ phân giải tên: có Pyright (scip-python) thì dùng; không có thì công cụ chạy bằng phần tự đọc và ghi lý do ở phần giới hạn.

**Thông báo cho người dùng.** Mọi lỗi từ chối đầu vào nêu được nguyên nhân và cách sửa, không chỉ báo thất bại chung chung.

#### Điều kiện và cách kiểm

Đo trên bộ dữ liệu đã pin, ghi đủ các trường ở trên cho mỗi lần chạy. Dựng ca lỗi một phần bằng cách cố ý làm hỏng một đơn vị phân tích và kiểm trạng thái trả về. Kiểm ma trận hỗ trợ khớp với hành vi thật: mỗi ô trong ma trận có ít nhất một ca kiểm. Đọc lại toàn bộ thông báo lỗi của ba hình thức đầu vào trước nghiệm thu.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)

---

Nguồn: [NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md) · revision 4 · status draft · SHA-256 `1128a9c8f9876fa0c5c0a2de243400c41606449818def081322c62b19ad422a3`

### NFR-L3GEN-SEC-002 — An toàn khi tiếp nhận source và vòng đời dữ liệu

- **Nhóm:** Security và Privacy.
- **Trạng thái:** revision 4 (02/10/2026): provider đổi sang OpenRouter theo NFR-L3GEN-AI-002; đợt này chỉ có dòng lệnh. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md), [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md), [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md), [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md).
- **Threat model:** [TM-SYS-L3GEN](../../architecture/threat-model/TM-SYS-L3GEN.md).

#### Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-SEC-001 và NFR-L3GEN-PRIV-001 của BL-r14.

**Read-only với source.** Không chạy, không import, không `exec` hay `eval`, không cài dependency, không chạy hook hoặc submodule, và không ghi ngược vào cây source đầu vào.

**Tiếp nhận an toàn.** Đợt này chỉ nhận thư mục cục bộ qua dòng lệnh: thư mục source và output không được lồng nhau, công cụ không ghi vào cây source. Các ngưỡng dưới đây áp khi có FR nhận ZIP hoặc GitHub: file nén giải ra phải nằm trong vùng xử lý; đường dẫn thoát khỏi vùng đó bị từ chối. Trần một lần tiếp nhận, giữ từ BL-r14: ZIP nén 100 MB, giải nén 500 MB, 50.000 file. Lấy source từ GitHub timeout 120 giây. Vượt trần thì từ chối kèm lý do. Chỉ nhận repository GitHub public qua HTTPS; công cụ không nhận và không lưu credential truy cập repository.

**Dữ liệu gửi ra ngoài.** Trước khi chạy, người dùng được cho biết dữ liệu nào sẽ được gửi tới provider model. Dữ liệu gửi đi theo mục "Đầu vào gửi cho model" của NFR-L3GEN-AI-002: method và path của route, tên bảng, đường dẫn file, tên hàm và lớp cấp cao nhất, các dòng code khai báo route và tên dùng chung. Không gửi nguyên file source hoặc cả repository. Dữ liệu đi tới OpenRouter, chuyển tiếp tới nhà cung cấp model; dòng lệnh báo tên provider và model trước khi gửi. Điều khoản dùng dữ liệu là của provider; công cụ nêu tên, không phát biểu thay họ. Giá trị cấu hình mang dấu hiệu bí mật bị che trước khi vào bất kỳ đầu ra nào, kể cả payload gửi model.

**Vòng đời.** Phase đầu chỉ giữ dữ liệu cần cho lần chạy hiện tại. Trên web, source đã tiếp nhận và output hết hạn 24 giờ sau trạng thái cuối của lần chạy, và không được phục vụ sau hạn. Mốc 24 giờ cho source giữ từ BL-r14; áp cho output là mới, vì lịch sử 14 ngày của BL-r14 thuộc phase sau. Nếu máy tắt qua hạn, lần khởi động kế tiếp phải dọn trước khi phục vụ dữ liệu. Output của dòng lệnh do người dùng quản lý.

#### Điều kiện và cách kiểm

Chạy trên bộ dữ liệu chứa file nén độc hại, đường dẫn thoát vùng giải nén, symlink trỏ ra ngoài, repository vượt trần kích thước, và file cấu hình chứa giá trị bí mật. Kiểm cây source trước và sau khi chạy phải giống nhau về nội dung. Kiểm payload gửi model không chứa giá trị bí mật. Kiểm dữ liệu tạm đã được dọn sau vòng đời đã công bố.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)

## 7. Câu hỏi mở còn lại

| OQ | Câu hỏi | Owner | Due | Status |
|---|---|---|---|---|
| [OQ-L3GEN-009](../../lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/OQ-L3GEN-009.md) | Model trả phí và trần chi phí mỗi lần chạy | Khiêm | 2026-10-03 | open |
