---
uid: "01M3XDXBVVN3Q457YGXWBQE39F"
key: "FR-L3GEN-030"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-005","GOAL-L3GEN-006"],"constrained_by":["NFR-L3GEN-ACC-002","NFR-L3GEN-ABST-002","NFR-L3GEN-OPS-001","NFR-L3GEN-SEC-002"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-030 — Tài liệu L3 bảng dữ liệu

## Mô tả

FR này sinh phần bảng dữ liệu (TBL) của tài liệu L3, trong cùng lần chạy và cùng thư mục output với FR-L3GEN-029.

Revision 2 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: thêm nhãn mức chắc chắn, đối chiếu với sơ đồ qua `archdia.json`, thêm NFR-L3GEN-SEC-002.

### Đầu ra

```text
tech-specs/<CMP-slug>/schema/TBL-<SYS>-<CMP>.md
```

`<SYS>`, `<CMP-slug>`, `<CMP>` đặt theo quy tắc của FR-L3GEN-029. Một component có một file TBL, chứa mọi bảng nó sở hữu.

### Nội dung một file TBL

| Mục | Nội dung |
|---|---|
| Frontmatter | Như file API của FR-L3GEN-029 |
| Mỗi bảng | Tên bảng, lớp model và vị trí khai báo; bảng cột: tên, kiểu, khóa chính, khóa ngoại (bảng và cột đích), nullable |
| Truy vết | Mã dữ kiện đầy đủ và `file:dòng` của từng bảng và cột |
| Khối máy | Một khối DDL cùng nội dung, theo biến thể SQL của repository |

### Phạm vi đọc

| Đọc được | Ghi ở phần giới hạn |
|---|---|
| Lớp SQLAlchemy có `__tablename__`, lớp SQLModel có `table=True`, `Table(...)` của SQLAlchemy | ORM khác (Tortoise, Peewee, Beanie...), SQL viết tay, bảng chỉ khai trong file migration |

### Chia theo component

- Bảng thuộc component chứa file khai báo model, theo cách chia của FR-L3GEN-028. Nơi đọc hoặc ghi bảng không đổi chủ sở hữu.
- Một file khai nhiều bảng thì mọi bảng trong file theo component của file đó.

### Khi chưa đủ dữ kiện

Giá trị đọc trực tiếp từ khai báo mang nhãn `exact`. Giá trị lấy từ mặc định có tài liệu của ORM (ví dụ cột không khai `nullable` thì cho phép null, trừ khóa chính) ghi `inferred` kèm tên quy tắc. Tên bảng sinh lúc chạy ghi `unknown` kèm nguồn; không suy tên bảng từ tên lớp. Biến thể SQL lấy từ dòng tạo engine hoặc URL kết nối trong source; chưa xác định thì kiểu cột ghi `unknown` kèm kiểu khai trong code, và không có khối DDL, ghi rõ lý do. Không mặc định PostgreSQL.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tài liệu L3 |
| Ưu tiên | Must Have |
| Mốc | M2 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-030-01

- **Given:** Repository khai bảng theo cột "Đọc được" của mục "Phạm vi đọc".
- **When:** công cụ sinh tài liệu L3.
- **Then:** mỗi component sở hữu bảng có một file TBL theo mục "Nội dung một file TBL"; mỗi dòng trỏ về dữ kiện code làm bằng chứng và mang nhãn `exact`, `inferred` kèm tên quy tắc, hoặc `unknown` kèm lý do.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-030-02

- **Given:** Source cho biết biến thể SQL qua dòng tạo engine hoặc URL kết nối.
- **When:** công cụ sinh tài liệu L3.
- **Then:** kiểu cột ghi theo biến thể đó và file có khối DDL cùng nội dung với bảng cột.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-030-03

- **Given:** Tên bảng sinh lúc chạy, kiểu cột không xác định, hoặc chưa biết biến thể SQL.
- **When:** công cụ sinh tài liệu L3.
- **Then:** trường đó ghi `unknown` kèm lý do theo mục "Khi chưa đủ dữ kiện"; thiếu dữ kiện cho DDL thì ghi rõ không có khối DDL và lý do.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-030-04

- **Given:** Repository dùng cách khai bảng thuộc cột "Ghi ở phần giới hạn".
- **When:** công cụ sinh tài liệu L3.
- **Then:** phần giới hạn nêu thư viện hoặc cách khai đó và nơi dùng; không ghi là repository không có bảng.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-030-05

- **Given:** Cùng một lần chạy sinh cả sơ đồ của FR-L3GEN-028 và tài liệu TBL.
- **When:** người dùng đối chiếu hai đầu ra.
- **Then:** mỗi bảng của một component trong `archdia.json` nằm trong file TBL của đúng component đó, và ngược lại.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [FR-L3GEN-028](FR-L3GEN-028.md), [FR-L3GEN-029](FR-L3GEN-029.md)
