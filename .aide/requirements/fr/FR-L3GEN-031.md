---
uid: "01M3XDXBVV03VFGBBEJGV99EDH"
key: "FR-L3GEN-031"
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

# FR-L3GEN-031 — Tài liệu L3 sự kiện và tác vụ nền

## Mô tả

FR này sinh phần sự kiện (EVT) của tài liệu L3, trong cùng lần chạy và cùng thư mục output với FR-L3GEN-029.

Revision 2 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: thêm nhãn mức chắc chắn, đối chiếu với sơ đồ qua `archdia.json`, thêm NFR-L3GEN-SEC-002.

### Đầu ra

```text
tech-specs/<CMP-slug>/events/EVT-<SYS>-<CMP>-<topic>.md
```

`<SYS>`, `<CMP-slug>`, `<CMP>` đặt theo quy tắc của FR-L3GEN-029. `<topic>` là tên topic hoặc tên tác vụ, chuẩn hóa cùng quy tắc; trùng tên file thì thêm `-2`, `-3` theo thứ tự nguồn ổn định. Topic chưa biết dùng nhãn từ mã dữ kiện, không coi nhãn đó là tên topic thật. README của FR-L3GEN-029 có thêm mục lục EVT theo topic.

### Phạm vi đọc

| Loại | Bên gửi | Bên nhận |
|---|---|---|
| Kafka, FastStream | `send`, `publish` tới một topic | Consumer hoặc subscriber của topic |
| Celery | `.delay`, `.apply_async`, `send_task` | Hàm có `@app.task`, `@shared_task` |
| FastAPI `BackgroundTasks` | `add_task(hàm, ...)` | Hàm được truyền vào |

Broker và thư viện hàng đợi khác (RabbitMQ thuần, Redis Streams, taskiq, arq...) ghi ở phần giới hạn.

### Nội dung một file EVT

| Mục | Nội dung |
|---|---|
| Frontmatter | Như file API của FR-L3GEN-029 |
| Sự kiện | Topic hoặc tên tác vụ; broker hoặc thư viện; vai trò của component này (gửi, nhận, hay cả hai) |
| Bên liên quan | Các bên gửi/nhận khác đã xác minh, kèm component của họ |
| Payload | Schema payload nếu khai trong code; không thì `unknown` kèm lý do |
| Truy vết | `file:dòng` của từng điểm gửi và nhận |

### Chia theo component

- EVT đặt ở từng component có điểm gửi hoặc nhận. Mỗi file mô tả vai trò của chính component đó, không có nghĩa component sở hữu độc quyền topic. Ví dụ: component Đơn hàng ghi gửi `order-created`, component Kho ghi nhận `order-created`.
- Trong một component, các điểm cùng topic chỉ gom vào một file khi có bằng chứng cùng broker hoặc cấu hình.
- Chỉ nối bên gửi với bên nhận khi có bằng chứng cùng broker hoặc cùng hàm tác vụ; không nối chỉ vì trùng tên topic.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tài liệu L3 |
| Ưu tiên | Should Have |
| Mốc | M3 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-031-01

- **Given:** Repository gửi hoặc nhận sự kiện theo bảng "Phạm vi đọc".
- **When:** công cụ sinh tài liệu L3.
- **Then:** mỗi component có điểm gửi/nhận có file EVT theo mục "Nội dung một file EVT"; mỗi dòng trỏ về dữ kiện code làm bằng chứng; điểm gửi, điểm nhận và cặp gửi–nhận đã nối mang nhãn `exact`, phần chưa xác minh mang `unknown` kèm lý do.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-031-02

- **Given:** Chỉ thấy một bên, có nhiều bên gửi, hoặc hai bên cùng tên topic nhưng chưa xác định cùng broker.
- **When:** công cụ sinh tài liệu L3.
- **Then:** vẫn xuất tài liệu cho mỗi bên thấy được; bên chưa xác minh ghi `unknown` kèm lý do và file đánh dấu `partial`; không nối hai bên chỉ vì trùng tên.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-031-03

- **Given:** Repository dùng broker hoặc thư viện hàng đợi ngoài bảng "Phạm vi đọc".
- **When:** công cụ chạy phân tích.
- **Then:** phần giới hạn nêu thư viện đó và nơi dùng; không ghi là repository không có sự kiện.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-031-04

- **Given:** Cùng một lần chạy sinh cả sơ đồ của FR-L3GEN-028 và tài liệu EVT.
- **When:** người dùng đối chiếu hai đầu ra.
- **Then:** mỗi mũi tên gửi tác vụ nền trong `archdia.json` có điểm gửi và điểm nhận tương ứng trong tài liệu EVT của hai component đó.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [FR-L3GEN-028](FR-L3GEN-028.md), [FR-L3GEN-029](FR-L3GEN-029.md)
