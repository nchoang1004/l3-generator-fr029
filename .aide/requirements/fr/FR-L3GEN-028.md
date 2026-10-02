---
uid: "01M3XDXBVTM6VAY4XQG18V3T3V"
key: "FR-L3GEN-028"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-004","GOAL-L3GEN-005","GOAL-L3GEN-007"],"constrained_by":["NFR-L3GEN-ACC-002","NFR-L3GEN-ABST-002","NFR-L3GEN-AI-002","NFR-L3GEN-SEC-002","NFR-L3GEN-OPS-001"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-028 — Sơ đồ kiến trúc có bằng chứng

## Mô tả

Developer chạy dòng lệnh trên một thư mục repository Python/FastAPI và nhận sơ đồ component cùng bản mô tả đi kèm. Sơ đồ cho người mới hình dung luồng xử lý của hệ thống: request đi vào đâu, qua component nào, tới dữ liệu và hệ thống ngoài nào. Mỗi khối, mũi tên, điểm vào và hệ thống ngoài có một dòng code làm bằng chứng.

Tài liệu L3 ở FR-L3GEN-029 đến 031 sinh trong cùng lần chạy và dùng đúng cách chia component của FR này.

Revision 2 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: một luật sở hữu bảng, phạm vi đọc, nhãn, JSON, bí mật trong bằng chứng, tách AC-03. Revision 3 (02/10/2026) sửa theo recovery review REVIEW-SCOPE-L3GEN-2026-003: luật xếp file chứa tên dùng chung, gửi tác vụ nền, nhãn trong AC, `result.json` trong AC-11, báo trước khi gửi model, thư mục output phải rỗng.

### Đầu ra

```text
<thư mục output>/
  archdia.md      sơ đồ Mermaid, bảng component, điểm vào, lời gọi giữa component,
                  hệ thống ngoài, khóa cấu hình, thư viện, phần giới hạn
  archdia.mmd     mã nguồn sơ đồ
  archdia.json    mô hình kiến trúc: component và file thành viên, mũi tên, hệ thống ngoài,
                  điểm vào, giới hạn; có schema version và định danh snapshot
```

`archdia.json` là nguồn của sơ đồ và của cách chia component mà FR-L3GEN-029 đến 031 dùng. `result.json` của FR-L3GEN-029 giữ dữ kiện contract và bằng chứng; hai file mang cùng định danh snapshot và cùng danh sách component.

Bằng chứng ghi dạng `file:dòng| nguyên văn dòng code`, đường dẫn tính từ gốc repository.

### Phạm vi đọc

| Mục | Nhận từ | Ngoài danh sách thì |
|---|---|---|
| Phạm vi phân tích | File `.py` của repository, trừ: thư mục `tests/`, `test/`, file `test_*.py`, `*_test.py`, `conftest.py` (Kiểm thử); `migrations/`, `alembic/` (Migration); thư mục ẩn, `node_modules`, `__pycache__`, `site-packages`, thư mục có `pyvenv.cfg` (môi trường ảo). File trong `scripts/`, `seeds/`, `docs/`, `examples/`, `build/`, `dist/`, `env/`, `venv/`, `testing/` chỉ được xét khi import code của repository | Đếm ở phần giới hạn |
| Điểm vào | `FastAPI(`, `uvicorn.run(`, khối `if __name__ == "__main__"`, lệnh Click/Typer | — |
| Hệ thống ngoài | Dòng tạo engine hoặc client có URL, host hoặc DSN: SQLAlchemy/SQLModel engine, Redis, SMTP, broker; lời gọi `httpx`, `requests`, `aiohttp` ra ngoài | Thư viện I/O khác ghi ở phần giới hạn kèm nơi dùng |
| Khóa cấu hình | Trường của lớp kế thừa `BaseSettings`; `os.environ[...]`, `os.getenv(...)` | — |
| Thư viện | `pyproject.toml` (`project.dependencies`, Poetry), `requirements*.txt` | Manifest khác ghi ở phần giới hạn |
| Gửi tác vụ nền | Celery và FastAPI `BackgroundTasks`, dạng gửi và nhận như bảng "Phạm vi đọc" của FR-L3GEN-031 | Thư viện hàng đợi khác ghi ở phần giới hạn |

### Component là gì

Theo quy trình mentor, component gánh một trách nhiệm nghiệp vụ và sở hữu contract của nó: API, bảng, sự kiện. Route, service, repository, model là cấu trúc bên trong một component, không phải component riêng.

| Loại | Gồm | Lên sơ đồ |
|---|---|---|
| Nghiệp vụ | Các route cùng trách nhiệm và file chỉ các route đó dùng | Có |
| Dùng chung | File nhiều component nghiệp vụ cùng dùng, tách theo việc: hạ tầng theo loại kết nối (CSDL, Redis, SMTP...), dữ liệu dùng chung, tiện ích dùng chung | Có |
| Khởi động | File tạo app, gộp router, chạy chương trình | Có |
| Chưa xếp | File có code, không route nào đi tới, không phải điểm vào, và cùng thư mục không có file nào đã xếp | Có, kèm dòng ở phần giới hạn |
| Kiểm thử, Migration, Khác | File test; file migration; file không có code (`__init__.py` rỗng, manifest) | Không; vẫn có trong `archdia.json` |

File có code mà không route nào đi tới và không phải điểm vào thì theo component có nhiều file nhất trong cùng thư mục, trừ Kiểm thử và Khởi động. Thư mục không có file nào đã xếp thì file vào Chưa xếp.

**Cách xếp file.** Code lần theo từng route xuống tới mức tên cấp cao nhất (hàm, lớp, biến) và ghi tên đó thuộc nhóm route nào.

1. Tên chỉ một nhóm route chạm thuộc nhóm đó.
2. Tên nhiều nhóm chạm là tên dùng chung. Model được chọn một component cho tên đó khi chỉ component đó dùng nó (NFR-L3GEN-AI-002).
3. Tên dùng chung còn lại thuộc component dùng chung theo vai trò file: file có dòng tạo kết nối hoặc I/O vào "Hạ tầng <loại kết nối>"; file khai model bảng hoặc truy cập dữ liệu vào "Dữ liệu dùng chung"; còn lại vào "Tiện ích dùng chung".
4. Mỗi file theo component chiếm nhiều tên của file nhất; mã cấp module tính nửa phiếu; hòa thì chọn theo một thứ tự cố định, để cùng đầu vào cho cùng kết quả.

Mỗi file thuộc đúng một component. Contract thuộc component chứa file khai báo nó: route theo file khai báo route, bảng theo file khai báo model (FR-L3GEN-030), sự kiện theo file có điểm gửi hoặc nhận (FR-L3GEN-031). Component dùng chung cũng sở hữu contract nếu file khai báo nằm trong nó, ví dụ bảng khai trong `models.py` dùng chung.

### Ai quyết phần nào

| Việc | Ai làm |
|---|---|
| Lần theo từng route xuống tới bảng và hệ thống ngoài; nhóm route theo file khai báo; xếp file vào nhóm | Code |
| Gộp các nhóm route cùng trách nhiệm nghiệp vụ; đặt tên và viết một câu trách nhiệm cho component; chọn tên dùng chung nào chỉ một component dùng | Mô hình ngôn ngữ, kèm mã một dòng code làm bằng chứng (NFR-L3GEN-AI-002) |
| Kiểm đề xuất của model; dựng mũi tên từ lời gọi đã xác định đích | Code |

Model không tách nhóm route và không thêm mũi tên.

### Mũi tên nào được vẽ

Sơ đồ chỉ vẽ luồng xử lý. Lời gọi có thật nhưng không thuộc luồng thì không vẽ.

| Vẽ | Không vẽ |
|---|---|
| Gọi service, repository, crud của component khác | Lắp ráp: container DI, tạo app, khởi động và tắt |
| Gọi method trên session CSDL hoặc client Redis | Chỉ nhận session/client rồi truyền đi, không gọi method |
| Gửi tác vụ nền: từ component gửi tới component chứa hàm nhận việc | Kiểm tra rồi quay về: xác thực, quyền, captcha |
| Component tới hệ thống ngoài | Chỉ dùng model hoặc schema làm kiểu; log, metrics |

Mũi tên ghi số lời gọi gộp lại và tối đa ba dòng code làm bằng chứng.

### Nhãn mức chắc chắn

| Mục | Nhãn |
|---|---|
| Khối, mũi tên, điểm vào, hệ thống ngoài dựng từ dòng code đã kiểm | `exact` |
| Cách gộp nhóm, tên, câu trách nhiệm do model đề xuất | `inferred`, lý do "do model đề xuất", kèm tên model |
| Tên đặt theo đường dẫn khi không có model | `inferred`, lý do "đặt theo đường dẫn" |
| File xếp vào component theo thư mục | `inferred`, lý do "theo thư mục" |
| Khóa cấu hình, thư viện đọc từ dòng khai báo | `exact` |

### Bí mật trong bằng chứng

Code kiểm nguyên văn trên snapshot gốc. Khi dòng bằng chứng chứa giá trị mang dấu hiệu bí mật (mật khẩu trong URL, khóa API), đầu ra và payload gửi model hiện dòng đó với giá trị đã che và đánh dấu "đã che".

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Sơ đồ kiến trúc |
| Ưu tiên | Must Have |
| Mốc | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-028-01

- **Given:** Một thư mục source đọc được, chứa ứng dụng FastAPI, và một thư mục output ghi được.
- **When:** người dùng chạy phân tích qua dòng lệnh.
- **Then:** công cụ ghi `archdia.md`, `archdia.mmd`, `archdia.json` vào thư mục output và in đường dẫn các file. Bản mô tả có: các component cùng số route và tên bảng mỗi component sở hữu; điểm vào; lời gọi giữa component; hệ thống ngoài; khóa cấu hình; thư viện; phần giới hạn, theo mục "Phạm vi đọc". Trước request đầu tiên tới model, dòng lệnh in tên provider, tên model và loại dữ liệu sẽ gửi.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-ABST-002, NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-028-02

- **Given:** Đường dẫn source không tồn tại, không đọc được, thư mục output không ghi được hoặc đã có file, hoặc hai thư mục lồng nhau.
- **When:** người dùng chạy phân tích.
- **Then:** công cụ dừng trước khi phân tích, nêu nguyên nhân và cách sửa, không tạo output dở dang và không ghi vào cây source.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-028-03

- **Given:** Repository có route, bảng và lời gọi giữa các file.
- **When:** công cụ chia component.
- **Then:** mỗi file trong phạm vi phân tích thuộc đúng một component theo bảng "Component là gì" và mục "Cách xếp file"; route và bảng thuộc component chứa file khai báo chúng; file xếp theo thư mục mang nhãn `inferred` lý do "theo thư mục".
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-028-04

- **Given:** Model trả về đề xuất hợp lệ.
- **When:** công cụ sinh kết quả.
- **Then:** mỗi component nghiệp vụ có tên, một câu trách nhiệm và một dòng code làm bằng chứng; các nhóm route model gộp nằm trong cùng component; tên, câu trách nhiệm và cách gộp mang nhãn `inferred` kèm tên model.
- `constrained_by:` [NFR-L3GEN-AI-002, NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-028-05

- **Given:** Model đề xuất tách một nhóm route, đưa một nhóm vào hai component, trỏ mã dòng không có trong danh sách đã gửi, hoặc thêm mũi tên.
- **When:** công cụ kiểm đề xuất.
- **Then:** phần đề xuất đó không vào kết quả; lý do loại được ghi trong `archdia.json`.
- `constrained_by:` [NFR-L3GEN-AI-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-028-06

- **Given:** Hai component có lời gọi qua lại.
- **When:** công cụ dựng mũi tên.
- **Then:** chỉ lời gọi thuộc cột "Vẽ" thành mũi tên; lời gọi thuộc cột "Không vẽ" không lên sơ đồ; lời gọi chưa xác định được đích không thành mũi tên mà được đếm ở phần giới hạn.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-028-07

- **Given:** Một khối, mũi tên, điểm vào hoặc hệ thống ngoài sắp được đưa lên sơ đồ.
- **When:** công cụ sinh kết quả.
- **Then:** mục đó có bằng chứng `file:dòng| nguyên văn` khớp đúng dòng trong snapshot gốc và mang nhãn `exact`; dòng chứa giá trị bí mật hiện với giá trị đã che và đánh dấu "đã che". Mục không có bằng chứng hợp lệ không được đưa lên.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-028-08

- **Given:** Model không khả dụng, hết ngân sách, vượt trần, hoặc vẫn trả sai schema sau lần gửi lại của NFR-L3GEN-AI-002.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ vẫn ghi sơ đồ do code chia; component đặt tên theo đường dẫn, nhãn `inferred` lý do "đặt theo đường dẫn"; trạng thái lần chạy là partial kèm nguyên nhân.
- `constrained_by:` [NFR-L3GEN-AI-002, NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-028-09

- **Given:** Có file lỗi cú pháp, file "Chưa xếp", lời gọi không xác định được đích, thư viện I/O hay manifest ngoài "Phạm vi đọc", công cụ phân giải tên không chạy được, hoặc repository rỗng hay ngoài stack hỗ trợ.
- **When:** công cụ sinh kết quả.
- **Then:** từng phần đó hiện ở phần giới hạn kèm lý do và số lượng; không trả kết quả thành công rỗng.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-028-10

- **Given:** Repository có file test, migration, file không có code, hoặc nhiều component hơn trần số node.
- **When:** công cụ vẽ sơ đồ.
- **Then:** sơ đồ chỉ có node mức component và hệ thống ngoài, trong trần và theo luật chọn node của NFR-L3GEN-ABST-002; component Kiểm thử, Migration, Khác và component bị cắt khỏi sơ đồ vẫn có trong `archdia.json` và được liệt kê trong `archdia.md`.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-028-11

- **Given:** Một công cụ khác đọc `archdia.json`.
- **When:** công cụ đó nạp file.
- **Then:** `archdia.json` và `result.json` đều có schema version và cùng định danh snapshot; danh sách component của hai file trùng nhau, với định danh component ổn định giữa sơ đồ và tài liệu L3; `archdia.json` không có mũi tên trỏ tới component không có trong file.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)
- [FR-L3GEN-029](FR-L3GEN-029.md), [FR-L3GEN-030](FR-L3GEN-030.md), [FR-L3GEN-031](FR-L3GEN-031.md)
