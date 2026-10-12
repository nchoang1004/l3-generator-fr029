---
key: CSV-CHG-L3GEN-2026-002-r11
group: derived
non_normative: true
derived_from: [BL-CHG-L3GEN-2026-002-r11]
hand_written: false
status: candidate
generated_by: scripts/prd_package.py render --baseline BL-r11.yaml --recovery
---

# Làm lại phạm vi — mô hình ngôn ngữ đề xuất, code kiểm bằng chứng

Bản ứng viên chưa duyệt, sinh từ `BL-CHG-L3GEN-2026-002-r11`. Khi view và nguồn bất đồng, **FR/NFR/PRD nguồn thắng**; sửa nguồn rồi chạy lại script render. Không dùng view này như approval.

Gồm 4 FR, 5 NFR và 1 OBS trong baseline.

## 1. Mục tiêu

Bốn mục tiêu, xếp theo thứ tự: sinh ra được gì, rồi mới tới tin được tới đâu.

| Goal key | Mục tiêu | Liên kết KPI |
|---|---|---|
| GOAL-L3GEN-004 | Dựng sơ đồ component từ source hiện tại, cho người mới hình dung luồng xử lý: request vào đâu, qua component nào, tới dữ liệu và hệ thống ngoài nào | KPI-L3GEN-006 |
| GOAL-L3GEN-005 | Mọi kết luận trên sơ đồ và tài liệu đều lần ngược được về đúng đoạn source sinh ra nó, để người đọc tự kiểm chứng thay vì phải tin | KPI-L3GEN-007 |
| GOAL-L3GEN-006 | Từ cùng cách chia component, sinh tài liệu L3 contract (API, bảng, sự kiện) theo mẫu `tech-specs/` của mentor, để người mới tra contract của từng component ở một chỗ | KPI-L3GEN-008 |
| GOAL-L3GEN-007 | Nói thật về giới hạn của chính mình: tách rõ phần đọc trực tiếp từ bằng chứng, phần suy ra, và phần không kết luận được, để người đọc biết chỗ nào tin ngay và chỗ nào phải tự kiểm | KPI-L3GEN-009, KPI-L3GEN-010 |

## 2. Mục tiêu nghiệp vụ đổi

Change Set này thay cho `CHG-L3GEN-2026-001`. Mọi GOAL/KPI mang key mới; GOAL/KPI của Change Set cũ không còn hiệu lực. GOAL hiện hành ở mục 1, KPI hiện hành dưới đây.

`KPI-L3GEN-xxx` là mã của chỉ số nằm ngay trong PRD này. `OBS-L3GEN-xxx` là tài liệu đo lường riêng, quy định nguồn dữ liệu, cách tính và người chịu trách nhiệm. PRD không giữ bản sao công thức hoặc ngưỡng.

Cả năm chỉ số đều tính ra số được. Không chỉ số nào dựa trên cảm nhận người dùng.

| KPI key | KPI | Giải thích | Baseline | Target | Timeline | measured_by |
|---|---|---|---|---|---|---|
| KPI-L3GEN-006 | Độ đúng sơ đồ cấu trúc | P, P khắt khe và R của mũi tên giữa component, so với đáp án; kèm chấm luồng. Cách chấm ở [NFR-L3GEN-ACC-002](../../requirements/nfr/NFR-L3GEN-ACC-002.md) | Chưa đo theo định nghĩa component mới | Đạt NFR-L3GEN-ACC-002 trên từng repo kín nhỏ và vừa; repo lớn báo số | Trước nghiệm thu M3; chặn nghiệm thu FR-L3GEN-028 | [OBS-L3GEN-001](../../observability/OBS-L3GEN-001.md) |
| KPI-L3GEN-007 | Độ đúng bằng chứng | Tỷ lệ kết luận công bố có bằng chứng hợp lệ: dòng code có thật trong snapshot, nguyên văn khớp; với mũi tên, dòng đó nối đúng hai đầu. Kèm tỷ lệ mã dòng model trỏ hợp lệ. Máy chấm được toàn bộ | Chưa đo | 100% kết luận công bố, không ngoại lệ; mã dòng model trỏ đạt NFR-L3GEN-ACC-002 | Trước nghiệm thu M3 | [OBS-L3GEN-001](../../observability/OBS-L3GEN-001.md) |
| KPI-L3GEN-008 | Độ đúng dữ kiện L3 | Precision/recall riêng từng loại: route, request/response model, entity/table, config, event, thư viện và lời gọi HTTP ra ngoài | Chưa đo | Đạt NFR-L3GEN-ACC-002 trên từng repo kín nhỏ và vừa; repo lớn báo số | Trước nghiệm thu M3 | [OBS-L3GEN-001](../../observability/OBS-L3GEN-001.md) |
| KPI-L3GEN-009 | Nhãn mức chắc chắn có đúng không | Trong các dữ kiện L3 gắn nhãn `exact`, tỷ lệ sai so với đáp án của KPI-L3GEN-008. Máy chấm. Nghĩa các nhãn ở [glossary](../../domain/glossary-core.md) mục 4 | Chưa đo | Đạt ngưỡng NFR-L3GEN-ACC-002 trên từng repo kín nhỏ và vừa | Trước nghiệm thu M3 | [OBS-L3GEN-001](../../observability/OBS-L3GEN-001.md) |
| KPI-L3GEN-010 | Công cụ có tự báo phần nó không đọc được không | Trong số các chỗ công cụ không phân tích được — file lỗi cú pháp, file ngoài phạm vi hỗ trợ, quan hệ không xác định được đích — bao nhiêu phần trăm được nêu ở mục giới hạn của kết quả, thay vì bị bỏ qua im lặng | Chưa đo | 100% | Trước nghiệm thu M3 | [OBS-L3GEN-001](../../observability/OBS-L3GEN-001.md) |

Cách đo, bộ repo và đáp án của cả năm chỉ số nằm ở [OBS-L3GEN-001](../../observability/OBS-L3GEN-001.md). Mọi tỷ lệ báo kèm số đếm; mẫu số bằng 0 thì `not_evaluated`, không báo phần trăm.

# III. BỐI CẢNH VÀ PHÂN TÍCH

## 3. Tính năng mới

Toàn bộ FR trong candidate baseline; Must/Should và mốc nằm tại từng nguồn.

---

Nguồn: [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md) · revision 3 · status draft · SHA-256 `db23514615e131dbdf28ed32538a5ca537cf331bc55618d1c8c3bbf01f3455f5`

### FR-L3GEN-028 — Sơ đồ kiến trúc có bằng chứng

#### Mô tả

Developer chạy dòng lệnh trên một thư mục repository Python/FastAPI và nhận sơ đồ component cùng bản mô tả đi kèm. Sơ đồ cho người mới hình dung luồng xử lý của hệ thống: request đi vào đâu, qua component nào, tới dữ liệu và hệ thống ngoài nào. Mỗi khối, mũi tên, điểm vào và hệ thống ngoài có một dòng code làm bằng chứng.

Tài liệu L3 ở FR-L3GEN-029 đến 031 sinh trong cùng lần chạy và dùng đúng cách chia component của FR này.

Revision 2 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: một luật sở hữu bảng, phạm vi đọc, nhãn, JSON, bí mật trong bằng chứng, tách AC-03. Revision 3 (02/10/2026) sửa theo recovery review REVIEW-SCOPE-L3GEN-2026-003: luật xếp file chứa tên dùng chung, gửi tác vụ nền, nhãn trong AC, `result.json` trong AC-11, báo trước khi gửi model, thư mục output phải rỗng.

##### Đầu ra

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

##### Phạm vi đọc

| Mục | Nhận từ | Ngoài danh sách thì |
|---|---|---|
| Phạm vi phân tích | File `.py` của repository, trừ: thư mục `tests/`, `test/`, file `test_*.py`, `*_test.py`, `conftest.py` (Kiểm thử); `migrations/`, `alembic/` (Migration); thư mục ẩn, `node_modules`, `__pycache__`, `site-packages`, thư mục có `pyvenv.cfg` (môi trường ảo). File trong `scripts/`, `seeds/`, `docs/`, `examples/`, `build/`, `dist/`, `env/`, `venv/`, `testing/` chỉ được xét khi import code của repository | Đếm ở phần giới hạn |
| Điểm vào | `FastAPI(`, `uvicorn.run(`, khối `if __name__ == "__main__"`, lệnh Click/Typer | — |
| Hệ thống ngoài | Dòng tạo engine hoặc client có URL, host hoặc DSN: SQLAlchemy/SQLModel engine, Redis, SMTP, broker; lời gọi `httpx`, `requests`, `aiohttp` ra ngoài | Thư viện I/O khác ghi ở phần giới hạn kèm nơi dùng |
| Khóa cấu hình | Trường của lớp kế thừa `BaseSettings`; `os.environ[...]`, `os.getenv(...)` | — |
| Thư viện | `pyproject.toml` (`project.dependencies`, Poetry), `requirements*.txt` | Manifest khác ghi ở phần giới hạn |
| Gửi tác vụ nền | Celery và FastAPI `BackgroundTasks`, dạng gửi và nhận như bảng "Phạm vi đọc" của FR-L3GEN-031 | Thư viện hàng đợi khác ghi ở phần giới hạn |

##### Component là gì

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

##### Ai quyết phần nào

| Việc | Ai làm |
|---|---|
| Lần theo từng route xuống tới bảng và hệ thống ngoài; nhóm route theo file khai báo; xếp file vào nhóm | Code |
| Gộp các nhóm route cùng trách nhiệm nghiệp vụ; đặt tên và viết một câu trách nhiệm cho component; chọn tên dùng chung nào chỉ một component dùng | Mô hình ngôn ngữ, kèm mã một dòng code làm bằng chứng (NFR-L3GEN-AI-002) |
| Kiểm đề xuất của model; dựng mũi tên từ lời gọi đã xác định đích | Code |

Model không tách nhóm route và không thêm mũi tên.

##### Mũi tên nào được vẽ

Sơ đồ chỉ vẽ luồng xử lý. Lời gọi có thật nhưng không thuộc luồng thì không vẽ.

| Vẽ | Không vẽ |
|---|---|
| Gọi service, repository, crud của component khác | Lắp ráp: container DI, tạo app, khởi động và tắt |
| Gọi method trên session CSDL hoặc client Redis | Chỉ nhận session/client rồi truyền đi, không gọi method |
| Gửi tác vụ nền: từ component gửi tới component chứa hàm nhận việc | Kiểm tra rồi quay về: xác thực, quyền, captcha |
| Component tới hệ thống ngoài | Chỉ dùng model hoặc schema làm kiểu; log, metrics |

Mũi tên ghi số lời gọi gộp lại và tối đa ba dòng code làm bằng chứng.

##### Nhãn mức chắc chắn

| Mục | Nhãn |
|---|---|
| Khối, mũi tên, điểm vào, hệ thống ngoài dựng từ dòng code đã kiểm | `exact` |
| Cách gộp nhóm, tên, câu trách nhiệm do model đề xuất | `inferred`, lý do "do model đề xuất", kèm tên model |
| Tên đặt theo đường dẫn khi không có model | `inferred`, lý do "đặt theo đường dẫn" |
| File xếp vào component theo thư mục | `inferred`, lý do "theo thư mục" |
| Khóa cấu hình, thư viện đọc từ dòng khai báo | `exact` |

##### Bí mật trong bằng chứng

Code kiểm nguyên văn trên snapshot gốc. Khi dòng bằng chứng chứa giá trị mang dấu hiệu bí mật (mật khẩu trong URL, khóa API), đầu ra và payload gửi model hiện dòng đó với giá trị đã che và đánh dấu "đã che".

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
- **Then:** công cụ ghi `archdia.md`, `archdia.mmd`, `archdia.json` vào thư mục output và in đường dẫn các file. Bản mô tả có: các component cùng số route và tên bảng mỗi component sở hữu; điểm vào; lời gọi giữa component; hệ thống ngoài; khóa cấu hình; thư viện; phần giới hạn, theo mục "Phạm vi đọc". Trước request đầu tiên tới model, dòng lệnh in tên provider, tên model và loại dữ liệu sẽ gửi.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-ABST-002, NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-02

- **Given:** Đường dẫn source không tồn tại, không đọc được, thư mục output không ghi được hoặc đã có file, hoặc hai thư mục lồng nhau.
- **When:** người dùng chạy phân tích.
- **Then:** công cụ dừng trước khi phân tích, nêu nguyên nhân và cách sửa, không tạo output dở dang và không ghi vào cây source.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-03

- **Given:** Repository có route, bảng và lời gọi giữa các file.
- **When:** công cụ chia component.
- **Then:** mỗi file trong phạm vi phân tích thuộc đúng một component theo bảng "Component là gì" và mục "Cách xếp file"; route và bảng thuộc component chứa file khai báo chúng; file xếp theo thư mục mang nhãn `inferred` lý do "theo thư mục".
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-04

- **Given:** Model trả về đề xuất hợp lệ.
- **When:** công cụ sinh kết quả.
- **Then:** mỗi component nghiệp vụ có tên, một câu trách nhiệm và một dòng code làm bằng chứng; các nhóm route model gộp nằm trong cùng component; tên, câu trách nhiệm và cách gộp mang nhãn `inferred` kèm tên model.
- `constrained_by:` [NFR-L3GEN-AI-002, NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-05

- **Given:** Model đề xuất tách một nhóm route, đưa một nhóm vào hai component, trỏ mã dòng không có trong danh sách đã gửi, hoặc thêm mũi tên.
- **When:** công cụ kiểm đề xuất.
- **Then:** phần đề xuất đó không vào kết quả; lý do loại được ghi trong `archdia.json`.
- `constrained_by:` [NFR-L3GEN-AI-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-06

- **Given:** Hai component có lời gọi qua lại.
- **When:** công cụ dựng mũi tên.
- **Then:** chỉ lời gọi thuộc cột "Vẽ" thành mũi tên; lời gọi thuộc cột "Không vẽ" không lên sơ đồ; lời gọi chưa xác định được đích không thành mũi tên mà được đếm ở phần giới hạn.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-07

- **Given:** Một khối, mũi tên, điểm vào hoặc hệ thống ngoài sắp được đưa lên sơ đồ.
- **When:** công cụ sinh kết quả.
- **Then:** mục đó có bằng chứng `file:dòng| nguyên văn` khớp đúng dòng trong snapshot gốc và mang nhãn `exact`; dòng chứa giá trị bí mật hiện với giá trị đã che và đánh dấu "đã che". Mục không có bằng chứng hợp lệ không được đưa lên.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-08

- **Given:** Model không khả dụng, hết ngân sách, vượt trần, hoặc vẫn trả sai schema sau lần gửi lại của NFR-L3GEN-AI-002.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ vẫn ghi sơ đồ do code chia; component đặt tên theo đường dẫn, nhãn `inferred` lý do "đặt theo đường dẫn"; trạng thái lần chạy là partial kèm nguyên nhân.
- `constrained_by:` [NFR-L3GEN-AI-002, NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-09

- **Given:** Có file lỗi cú pháp, file "Chưa xếp", lời gọi không xác định được đích, thư viện I/O hay manifest ngoài "Phạm vi đọc", công cụ phân giải tên không chạy được, hoặc repository rỗng hay ngoài stack hỗ trợ.
- **When:** công cụ sinh kết quả.
- **Then:** từng phần đó hiện ở phần giới hạn kèm lý do và số lượng; không trả kết quả thành công rỗng.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-10

- **Given:** Repository có file test, migration, file không có code, hoặc nhiều component hơn trần số node.
- **When:** công cụ vẽ sơ đồ.
- **Then:** sơ đồ chỉ có node mức component và hệ thống ngoài, trong trần và theo luật chọn node của NFR-L3GEN-ABST-002; component Kiểm thử, Migration, Khác và component bị cắt khỏi sơ đồ vẫn có trong `archdia.json` và được liệt kê trong `archdia.md`.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-028-11

- **Given:** Một công cụ khác đọc `archdia.json`.
- **When:** công cụ đó nạp file.
- **Then:** `archdia.json` và `result.json` đều có schema version và cùng định danh snapshot; danh sách component của hai file trùng nhau, với định danh component ổn định giữa sơ đồ và tài liệu L3; `archdia.json` không có mũi tên trỏ tới component không có trong file.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md) · revision 3 · status draft · SHA-256 `6996ad38a106aeb38ee97826ba14cd9d0404188f2bfbd80fcaf623090793a847`

### FR-L3GEN-029 — Tài liệu L3 API và cấu trúc component

#### Mô tả

Theo quy trình mentor, L3 là contract: API, bảng dữ liệu (TBL) và sự kiện (EVT), chia theo component sở hữu. FR này sinh phần API, trong cùng lần chạy với sơ đồ của FR-L3GEN-028. FR-L3GEN-030 sinh TBL, FR-L3GEN-031 sinh EVT.

FR này cũng sinh hai mục trong `README.md` cho bốn thứ Đề bài 3.6 yêu cầu phát hiện mà contract không chứa: module/package, service, repository/data access, và lời gọi HTTP ra ngoài.

Revision 2 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: thêm mục "Cấu trúc component" và "Lời gọi HTTP ra ngoài"; đối chiếu với sơ đồ qua `archdia.json`. Revision 3 (02/10/2026) sửa theo recovery review REVIEW-SCOPE-L3GEN-2026-003: route khai không qua decorator ghi ở phần giới hạn; nhãn của lời gọi HTTP; thư mục của component bị cắt khỏi hình.

##### Đầu ra

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

##### Nội dung một file API

| Mục | Nội dung |
|---|---|
| Frontmatter | Ghi là bản sinh tự động, chưa được chủ repository duyệt; định danh snapshot; component sở hữu; mã các dữ kiện và bằng chứng dùng trong file |
| Endpoint | Bảng một dòng mỗi route: method, path đầy đủ, tham số (tên, vị trí path/query/header/body, kiểu, bắt buộc), request model, response model, status code, dependency hoặc auth, nhãn mức chắc chắn, mã dữ kiện |
| Model | Mỗi request/response model một bảng: tên trường, kiểu, bắt buộc, nullable; ghi vị trí khai báo. Model lồng nhau có mục riêng |
| Truy vết | Mã dữ kiện đầy đủ và `file:dòng` của từng route và model |
| Khối máy | Một khối OpenAPI 3.1 cùng nội dung với bảng |

##### Cấu trúc component trong README

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

##### Lời gọi HTTP ra ngoài trong README

Một dòng mỗi lời gọi qua `httpx`, `requests`, `aiohttp`:

| Cột | Nội dung |
|---|---|
| Component | Component chứa dòng gọi |
| Thư viện, method | Ví dụ `httpx`, `GET`; method không đọc được thì `unknown` |
| Đích | URL nguyên văn, hoặc khóa cấu hình chứa URL, nhãn `exact`; đích chỉ biết lúc chạy thì `unknown` kèm lý do |
| Bằng chứng | `file:dòng` kèm nguyên văn |

Thư viện HTTP khác ghi ở phần giới hạn kèm nơi dùng.

##### Chia theo component

- API thuộc component chứa file khai báo route, theo cách chia của FR-L3GEN-028. Nơi gọi API không đổi chủ sở hữu.
- Vì cùng cách chia, mỗi thư mục trong `tech-specs/` là một component trong `archdia.json`, và tập route trong tài liệu API bằng tập route trong `archdia.json`. Component bị cắt khỏi hình sơ đồ theo trần node của NFR-L3GEN-ABST-002 vẫn có thư mục nếu sở hữu contract.
- Route khai trong file test hoặc thư mục nằm ngoài phạm vi phân tích không vào tài liệu.
- Route khai không qua decorator (`add_api_route`, `add_route`, `add_websocket_route`) chưa được đọc ở đợt này. Mỗi lời gọi như vậy ghi ở phần giới hạn kèm nơi dùng, không bị bỏ qua im lặng.

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
- **Then:** tập route trong tài liệu API bằng tập route trong `archdia.json`; mỗi thư mục trong `tech-specs/` ứng với đúng một component trong `archdia.json`.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-029-05

- **Given:** Repository có route khai trong file test, trong thư mục ngoài phạm vi phân tích, hoặc khai qua `add_api_route`, `add_route`, `add_websocket_route`.
- **When:** công cụ sinh tài liệu L3.
- **Then:** các route đó không vào tài liệu API và không vào sơ đồ; mỗi lời gọi `add_api_route`, `add_route`, `add_websocket_route` được nêu ở phần giới hạn kèm `file:dòng`.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-029-06

- **Given:** Lần chạy sinh xong các file API.
- **When:** người dùng mở `README.md`.
- **Then:** README có mục lục trỏ tới từng file contract kèm component sở hữu, sơ đồ component, mục "Cấu trúc component", mục "Lời gọi HTTP ra ngoài", danh sách contract chưa gán được component, và phần giới hạn của lần chạy.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-029-07

- **Given:** Repository có file mang các dấu hiệu ở mục "Cấu trúc component trong README", và có file không mang dấu hiệu nào.
- **When:** công cụ sinh README.
- **Then:** mỗi file của component được liệt kê dưới package của nó với đúng một vai trò và dòng code làm bằng chứng; vai trò Service mang nhãn `inferred` kèm lý do; file không có dấu hiệu ghi "Khác", không có vai trò đoán theo tên.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-029-08

- **Given:** Repository gọi HTTP ra ngoài qua `httpx`, `requests` hoặc `aiohttp`, gồm cả lời gọi có URL chỉ biết lúc chạy.
- **When:** công cụ sinh README.
- **Then:** mỗi lời gọi có một dòng ở mục "Lời gọi HTTP ra ngoài" với component, thư viện, method, đích và bằng chứng; đích chỉ biết lúc chạy ghi `unknown` kèm lý do; lời gọi qua thư viện HTTP khác được nêu ở phần giới hạn.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md) · revision 2 · status draft · SHA-256 `f4fde7fe2afbbc8d691208b78d5248bdefc40c97ef937163c238bfa90ae7dcb4`

### FR-L3GEN-030 — Tài liệu L3 bảng dữ liệu

#### Mô tả

FR này sinh phần bảng dữ liệu (TBL) của tài liệu L3, trong cùng lần chạy và cùng thư mục output với FR-L3GEN-029.

Revision 2 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: thêm nhãn mức chắc chắn, đối chiếu với sơ đồ qua `archdia.json`, thêm NFR-L3GEN-SEC-002.

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

Giá trị đọc trực tiếp từ khai báo mang nhãn `exact`. Giá trị lấy từ mặc định có tài liệu của ORM (ví dụ cột không khai `nullable` thì cho phép null, trừ khóa chính) ghi `inferred` kèm tên quy tắc. Tên bảng sinh lúc chạy ghi `unknown` kèm nguồn; không suy tên bảng từ tên lớp. Biến thể SQL lấy từ dòng tạo engine hoặc URL kết nối trong source; chưa xác định thì kiểu cột ghi `unknown` kèm kiểu khai trong code, và không có khối DDL, ghi rõ lý do. Không mặc định PostgreSQL.

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
- **Then:** mỗi component sở hữu bảng có một file TBL theo mục "Nội dung một file TBL"; mỗi dòng trỏ về dữ kiện code làm bằng chứng và mang nhãn `exact`, `inferred` kèm tên quy tắc, hoặc `unknown` kèm lý do.
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
- **Then:** mỗi bảng của một component trong `archdia.json` nằm trong file TBL của đúng component đó, và ngược lại.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md) · revision 2 · status draft · SHA-256 `82764f1e36a637210bac18e40949204025af3630bfb6397ca2f8f8302a844db1`

### FR-L3GEN-031 — Tài liệu L3 sự kiện và tác vụ nền

#### Mô tả

FR này sinh phần sự kiện (EVT) của tài liệu L3, trong cùng lần chạy và cùng thư mục output với FR-L3GEN-029.

Revision 2 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: thêm nhãn mức chắc chắn, đối chiếu với sơ đồ qua `archdia.json`, thêm NFR-L3GEN-SEC-002.

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
- **Then:** mỗi component có điểm gửi/nhận có file EVT theo mục "Nội dung một file EVT"; mỗi dòng trỏ về dữ kiện code làm bằng chứng; điểm gửi, điểm nhận và cặp gửi–nhận đã nối mang nhãn `exact`, phần chưa xác minh mang `unknown` kèm lý do.
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
- **Then:** mỗi mũi tên gửi tác vụ nền trong `archdia.json` có điểm gửi và điểm nhận tương ứng trong tài liệu EVT của hai component đó.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## 4. Thay đổi hành vi hiện có

Không có FR nào bump revision: mọi FR trong baseline này mang key mới. FR của `CHG-L3GEN-2026-001` đã deprecated; ánh xạ cũ sang mới ở PRD mục IV.3.

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

Nguồn: [NFR-L3GEN-ABST-002](../../requirements/nfr/NFR-L3GEN-ABST-002.md) · revision 5 · status draft · SHA-256 `ce9c4a4f9bac6c369f049f5fd3dfa8336c4f70a3ecce2acb5d1d80079cbbe6be`

### NFR-L3GEN-ABST-002 — Mức trừu tượng của kết quả trình bày

- **Nhóm:** Abstraction level.
- **Trạng thái:** thay cho NFR-L3GEN-ABST-001 của BL-r14, giữ nguyên phạm vi và ngưỡng. Ngưỡng 500/50 đã chốt tại OQ-L3GEN-004 (CHG-L3GEN-2026-001); revision 3 (02/10/2026) chỉ đổi phần áp dụng sang FR-L3GEN-028 đến 031. Revision 4 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: định nghĩa node và luật chọn node khi vượt trần. Revision 5 (02/10/2026) sửa theo recovery review REVIEW-SCOPE-L3GEN-2026-003: component bị cắt chỉ có thư mục `tech-specs/` khi sở hữu contract. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md), [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md), [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md), [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md).
- **Quyết định nền:** [ADR-2026-001](../../architecture/adr/ADR-2026-001.md).

#### Yêu cầu có thể kiểm chứng

Phân tích và trình bày là hai mức khác nhau. Công cụ được đọc sâu tới function, tham số và phép gán để chứng minh một quan hệ, nhưng kết quả mặc định cho người đọc dừng ở application/component.

- Sơ đồ mặc định (mức L2) chỉ có node mức application, component và hệ thống ngoài. Node mức function, class hoặc file không xuất hiện ở lớp mặc định.
- Tài liệu L3 liệt kê contract: endpoint, bảng, sự kiện, chia theo component. Function và class chỉ xuất hiện khi là handler hoặc model được nêu trong contract, hoặc ở lớp bằng chứng.
- Số node của sơ đồ mặc định không tỷ lệ với số function của repository. Repository có từ 500 function trở lên vẫn cho sơ đồ mặc định không quá 50 node. Phần vượt trần không bị loại khỏi bộ kết quả mà nằm ở lớp bằng chứng; không xuất sơ đồ đầy đủ rồi để người đọc tự lọc.
- Node của sơ đồ là component (trừ Kiểm thử, Migration, Khác) và hệ thống ngoài. Route, bảng, sự kiện là nội dung ghi trong khối component, không phải node.
- Khi vượt 50 node: giữ mọi hệ thống ngoài; xếp component theo tổng số contract sở hữu và số mũi tên nối với nó, giảm dần, hòa thì theo số file rồi theo tên; lấy từ đầu cho tới đủ trần. Component bị cắt và mũi tên của nó không vẽ, nhưng vẫn có trong `archdia.json`, được liệt kê trong `archdia.md`, và vẫn có thư mục `tech-specs/` nếu sở hữu contract.
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

Nguồn: [NFR-L3GEN-ACC-002](../../requirements/nfr/NFR-L3GEN-ACC-002.md) · revision 4 · status draft · SHA-256 `0cf4515263185292dcd32a424dae6fc9cc317bac200855fc3932cf11d5b32014`

### NFR-L3GEN-ACC-002 — Độ đúng của kết quả và bằng chứng

- **Nhóm:** Accuracy.
- **Trạng thái:** ngưỡng dữ kiện L3 chốt tại OQ-L3GEN-007 ngày 22/09/2026. Ngưỡng sơ đồ theo tiêu chí nhóm dùng khi phát triển (Khiêm, 02/10/2026). Revision 4 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002 và quyết định của Khiêm: chấm trên từng repo kín nhỏ và vừa; thêm lại loại HTTP; nhãn `exact` chấm theo đáp án KPI-L3GEN-008 (đề xuất của Hoàng); bằng chứng của dòng chứa bí mật. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md), [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md), [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md), [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md).

#### Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-ACC-001 và NFR-L3GEN-TRACE-001 của BL-r14.

**Phạm vi áp ngưỡng.** Mọi ngưỡng dưới đây áp cho **từng** repo kín cỡ nhỏ và vừa. Repo lớn chỉ báo số, không chặn nghiệm thu (Khiêm, 02/10/2026). Danh sách repo và cỡ ở OBS-L3GEN-001.

**Độ đúng của dữ kiện L3.** Precision và recall đều phải đạt từ 80% trở lên, đo riêng cho từng loại: route, request/response model, entity/table, config, event, thư viện, lời gọi HTTP ra ngoài. Ngưỡng 80% chốt tại OQ-L3GEN-007.

**Độ đúng của sơ đồ (FR-L3GEN-028).** Đo trên cạnh giữa component, so với đáp án vẽ tay.

| Chỉ số | Ngưỡng |
|---|---|
| P: tỷ lệ mũi tên vẽ ra mà đúng | ≥ 0,8 |
| R: tỷ lệ mũi tên bắt buộc của đáp án mà sơ đồ có | ≥ 0,6 |
| Pk (P khắt khe): như P, nhưng mũi tên "chấp nhận được" của đáp án cũng tính sai | Luôn báo, không có ngưỡng |
| P, R của mũi tên tới hệ thống ngoài | Luôn báo, không có ngưỡng |
| Bằng chứng do model trỏ (mã dòng) mà code kiểm hợp lệ | ≥ 90%, cách tính ở OBS-L3GEN-001 |

Cách chấm:
- Mỗi component của công cụ được coi là component đáp án có nhiều file chung nhất với nó.
- Đáp án chia cạnh làm hai loại theo luật vẽ của FR-L3GEN-028: bắt buộc (luồng xử lý) và chấp nhận được (lắp ráp, chỉ truyền session, kiểm tra rồi quay về). Cạnh trùng bắt buộc là đúng; trùng chấp nhận được thì không tính ở P nhưng tính sai ở Pk; cạnh khác là sai.
- File không thuộc component nào của đáp án thì bỏ qua. File chỉ khai báo dạng dữ liệu (schema, enum, hằng số) mà đáp án không nhắc thì để ngoài đáp án.
- Báo kèm chấm luồng để thấy trường hợp đúng nhưng chia khác đáp án: R luồng (cạnh bắt buộc có hiện qua tối đa 3 mũi tên), P luồng (mũi tên ứng với luồng thật, trực tiếp hoặc qua một component trung gian), ARI (độ giống cách chia file). Chấm luồng chỉ đi kèm, không thay cách chấm trên.

Chấm thuộc tính riêng với chấm sự tồn tại: một route thiếu prefix không tính là route đúng, một tên bảng suy sai không tính là tên bảng đúng. Mọi tỷ lệ báo kèm TP/FP/FN.

**Bằng chứng.** Bằng chứng của một kết luận là các dữ kiện code trong tập dữ kiện của lần chạy, mỗi dữ kiện nằm ở file có thật trong snapshot đã phân tích. Với cạnh A→B, phải có ít nhất một dữ kiện đã xác định đích, vị trí thuộc A và đích thuộc B. Trên sơ đồ, bằng chứng ghi dạng `file:dòng| nguyên văn`, và code kiểm nguyên văn khớp đúng dòng trong snapshot. Dòng chứa giá trị bí mật vẫn kiểm trên snapshot gốc; đầu ra hiện bản đã che theo NFR-L3GEN-SEC-002 và vẫn tính là bằng chứng hợp lệ. Code kiểm điều này; lời khẳng định của model không được tính là bằng chứng. Tỷ lệ kết luận công bố có bằng chứng hợp lệ phải đạt 100%, không có ngoại lệ: kết luận không thỏa thì bị loại trước khi xuất, không được hạ thành cảnh báo. Bằng chứng không được trỏ sang snapshot khác hoặc sang source hiện tại trên đĩa.

**Nhãn chất lượng.** Confidence, completeness và coverage là ba trục độc lập, không dùng trục này thay trục kia. Nhãn `exact` chỉ dùng cho kết luận đọc trực tiếp từ bằng chứng; kết luận suy ra mang nhãn `inferred` kèm lý do. Không được nâng `inferred` thành `exact` để kết quả trông chắc chắn hơn. Trong các dữ kiện L3 gắn `exact`, tỷ lệ sai so với đáp án của KPI-L3GEN-008 phải ở mức 5% trở xuống, và là chỉ số chặn: gán nhãn chắc chắn cho kết luận sai gây hại hơn bỏ sót, vì người đọc tin mà không kiểm lại. Trên sơ đồ, `exact` nghĩa là dòng code làm bằng chứng có thật và nối đúng hai đầu (phần "Bằng chứng" ở trên); mũi tên đúng hay sai so với đáp án đo bằng P, R.

#### Điều kiện và cách kiểm

OBS-L3GEN-001 quy định dataset, người lập đáp án độc lập và cách matching. Mọi tỷ lệ báo kèm số đếm; mẫu số bằng 0 thì `not_evaluated`, không báo phần trăm.

Phần bằng chứng kiểm tự động trên mọi lần chạy: đối chiếu từng dữ kiện được trích dẫn với tập dữ kiện, từng đường dẫn với danh sách file của snapshot, và hai đầu của mỗi cạnh với vị trí và đích của dữ kiện. Máy kiểm được bằng chứng có tồn tại và nối đúng; việc dữ kiện có thật sự đủ ý nghĩa cho kết luận thì chấm bằng đáp án của người. Phần nhãn và độ đúng kiểm bằng đáp án do người hoặc subagent lập trước khi xem output. Không loại ca khó ra khỏi mẫu sau khi đã xem kết quả.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)

---

Nguồn: [NFR-L3GEN-AI-002](../../requirements/nfr/NFR-L3GEN-AI-002.md) · revision 6 · status draft · SHA-256 `5fa8afd22df52b42f8d8c97e8abd18a465c6c58c5847e87378c968b634f2e30a`

### NFR-L3GEN-AI-002 — Ranh giới, chi phí và truy vết của mô hình ngôn ngữ

- **Nhóm:** AI reliability.
- **Trạng thái:** revision 4 theo quyết định của Khiêm ngày 02/10/2026 (CR-L3GEN-2026-004, OQ-L3GEN-009): model bắt buộc, trả phí ít, qua OpenRouter. Revision 5 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: trần chi phí và token do Khiêm chốt khi đóng OQ-L3GEN-009; bỏ việc chọn chủ bảng (bảng theo file khai báo model, FR-L3GEN-028); mỗi loại lỗi câu trả lời một đường xử lý. Revision 6 (02/10/2026): Khiêm chốt số request, độ dài câu trả lời và timeout (finding F13 của REVIEW-SCOPE-L3GEN-2026-003). Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md).

#### Yêu cầu có thể kiểm chứng

Thay revision 3 (Groq và Google, gói miễn phí, trần chi phí 0 đồng).

**Việc của model.** Model nhận kết quả code đã lần theo và trả về: các nhóm route cùng trách nhiệm nghiệp vụ cần gộp; tên và một câu trách nhiệm cho mỗi component; tên dùng chung nào thuộc riêng một component. Mỗi quyết định trỏ một mã dòng code đã hiện cho model. Model không tách nhóm route, không thêm mũi tên, không sửa dữ kiện code và không tự công bố kết luận.

**Đầu vào gửi cho model.** Danh sách nhóm route (method, path, bảng và hệ thống ngoài mỗi route chạm, dòng khai báo route), tên dùng chung kèm dòng khai báo, số lời gọi giữa các nhóm. Mỗi dòng code gửi đi mang một mã `[L12]`; model trả mã, code tra ra `file:dòng` và nguyên văn. Không gửi nguyên file source hoặc cả repository.

**Kiểm câu trả lời.** Code kiểm: câu trả lời đúng schema; mỗi nhóm route thuộc đúng một component và không bị tách; tên dùng chung dùng tối đa một lần; mã dòng có trong danh sách đã gửi. Mỗi loại lỗi một đường xử lý:

| Lỗi | Xử lý |
|---|---|
| JSON hỏng hoặc sai schema | Gửi lại một lần kèm lỗi. Vẫn sai thì bỏ cả câu trả lời, giữ cách chia của code, trạng thái partial (AC-L3GEN-028-08) |
| Đúng schema nhưng vi phạm luật kiểm | Gửi lại một lần kèm danh sách lỗi. Vẫn sai thì loại phần vi phạm, giữ phần hợp lệ, ghi lý do (AC-L3GEN-028-05) |

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
| Chi phí | ≤ 0,20 USD |
| Token vào và ra cộng lại | ≤ 300.000 |
| Request | ≤ 4 (một lần hỏi, một lần gửi lại, mỗi lần thử lại tối đa một lần khi lỗi mạng) |
| Độ dài câu trả lời | ≤ 12.000 token mỗi request |
| Timeout | 300 giây mỗi request |

Chi phí và token do Khiêm chốt tại OQ-L3GEN-009 ngày 02/10/2026. Số request, độ dài câu trả lời và timeout: Khiêm chốt ngày 02/10/2026, giữ như revision 4. Công cụ ước tính token trước request đầu tiên; vượt trần thì không gọi model và xử lý theo AC-L3GEN-028-08. Số tham khảo khi phát triển: 7 request trên 5 repo nhỏ, khoảng 25.000 token, 0,008 USD (02/10/2026).

**Thiếu model.** Thiếu khóa, hết ngân sách, chạm trần, provider lỗi, hoặc vẫn sai schema sau lần gửi lại thì dừng bước dùng model, giữ kết quả do code chia, trạng thái partial kèm nguyên nhân (AC-L3GEN-028-08). Không tự đổi sang model khác, không đoán để lấp chỗ trống.

**Bí mật.** Khóa API do người dùng cung cấp lúc chạy, không được ghi vào output, log, bằng chứng hay bộ kết quả lưu lại. Dòng code chứa giá trị bí mật được che trước khi vào payload gửi model, theo NFR-L3GEN-SEC-002.

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

Nguồn: [NFR-L3GEN-OPS-001](../../requirements/nfr/NFR-L3GEN-OPS-001.md) · revision 3 · status draft · SHA-256 `729ebf4c64409370457b0811eff00c0a58934c767820cdfb520b1efcad95b646`

### NFR-L3GEN-OPS-001 — Hiệu năng, độ tin cậy và phạm vi hỗ trợ

- **Nhóm:** Operability.
- **Trạng thái:** ngưỡng đã chốt; revision 2 (02/10/2026) đổi phần áp dụng sang FR-L3GEN-028 đến 031 và thêm công cụ phân giải tên vào ma trận hỗ trợ. Trần của model ở NFR-L3GEN-AI-002. Revision 3 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: bỏ phần viết cho quota Groq và cho web (xếp hàng, ba hình thức đầu vào). Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md), [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md), [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md), [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md).

#### Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-PERF-001, REL-001, COMP-001 và phần còn dùng được của USA-001 của BL-r14. Key OPS-001 chưa từng dùng trước đây.

**Thời gian và tài nguyên.** Mỗi lần chạy ghi lại riêng thời gian lấy source, phân tích tĩnh, gọi model và sinh artifact, cùng bộ nhớ đỉnh và kích thước output.

| Ngưỡng | Giá trị | Nguồn |
|---|---|---|
| Phân tích tĩnh và ghi output, không gồm lấy source và gọi model | ≤ 60 giây cho 5.000 dòng Python; ≤ 300 giây cho 50.000 dòng | Giữ từ BL-r14 |
| Máy đo chuẩn | 4 CPU logical, RAM 8 GiB, SSD, Python 3.12; máy khác thì công bố, không ngoại suy | Giữ từ BL-r14 |
| Bộ nhớ | ≤ 2 GiB mỗi lần chạy | Giữ từ BL-r14 |
| Toàn bộ một lần chạy | ≤ 30 phút; quá hạn thì dừng, trả partial kèm lý do | Mới. Trần 10 phút của BL-r14 chưa tính thời gian gọi model |

Trần tiếp nhận ở NFR-L3GEN-SEC-002; trần token ở NFR-L3GEN-AI-002. Vượt trần thì từ chối trước bước tương ứng, kèm lý do, không chạy dở rồi hỏng.

**Lỗi một phần.** Một đơn vị phân tích hỏng không làm hỏng cả lần chạy. Kết quả partial phải nêu rõ phạm vi đã xử lý được. Trạng thái của lần chạy là completed, partial hoặc failed, và phải phản ánh đúng thực tế: không có bộ output trông như hoàn chỉnh khi thực ra thiếu artifact.

**Phạm vi hỗ trợ.** Có một ma trận khai báo, cho mỗi ngôn ngữ và framework, độ sâu phân tích áp dụng và mức chất lượng đi kèm. Ma trận này là nguồn duy nhất để trả lời câu hỏi công cụ hỗ trợ gì; phase đầu chỉ Python/FastAPI có mức hỗ trợ đầy đủ. Ma trận ghi cả công cụ phân giải tên: có Pyright (scip-python) thì dùng; không có thì công cụ chạy bằng phần tự đọc và ghi lý do ở phần giới hạn.

**Thông báo cho người dùng.** Mọi lỗi từ chối đầu vào nêu được nguyên nhân và cách sửa, không chỉ báo thất bại chung chung.

#### Điều kiện và cách kiểm

Đo trên bộ dữ liệu đã pin, ghi đủ các trường ở trên cho mỗi lần chạy. Dựng ca lỗi một phần bằng cách cố ý làm hỏng một đơn vị phân tích và kiểm trạng thái trả về. Kiểm ma trận hỗ trợ khớp với hành vi thật: mỗi ô trong ma trận có ít nhất một ca kiểm. Đọc lại toàn bộ thông báo lỗi của dòng lệnh trước nghiệm thu.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)

---

Nguồn: [NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md) · revision 6 · status draft · SHA-256 `0602984693938e706c9f8af5320d74e0dfbabca7b3172197b5f642ce3274d5af`

### NFR-L3GEN-SEC-002 — An toàn khi tiếp nhận source và vòng đời dữ liệu

- **Nhóm:** Security và Privacy.
- **Trạng thái:** revision 4 (02/10/2026): provider đổi sang OpenRouter theo NFR-L3GEN-AI-002; đợt này chỉ có dòng lệnh. Revision 5 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: bằng chứng kiểm trên snapshot gốc, đầu ra hiện bản đã che; phần ZIP, GitHub, web chỉ áp khi có FR tương ứng. Revision 6 (02/10/2026) sửa theo recovery review REVIEW-SCOPE-L3GEN-2026-003: dữ liệu gửi model dẫn về một chỗ (NFR-L3GEN-AI-002); thông báo trước khi gửi có AC. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md), [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md), [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md), [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md).
- **Threat model:** [TM-SYS-L3GEN](../../architecture/threat-model/TM-SYS-L3GEN.md).

#### Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-SEC-001 và NFR-L3GEN-PRIV-001 của BL-r14.

**Read-only với source.** Không chạy, không import, không `exec` hay `eval`, không cài dependency, không chạy hook hoặc submodule, và không ghi ngược vào cây source đầu vào.

**Tiếp nhận an toàn.** Đợt này chỉ nhận thư mục cục bộ qua dòng lệnh: thư mục source và output không được lồng nhau, công cụ không ghi vào cây source, symlink trỏ ra ngoài thư mục source không được đọc. Phần còn lại của đoạn này chỉ áp khi có FR nhận ZIP hoặc GitHub (phase sau): file nén giải ra phải nằm trong vùng xử lý; đường dẫn thoát khỏi vùng đó bị từ chối. Trần một lần tiếp nhận, giữ từ BL-r14: ZIP nén 100 MB, giải nén 500 MB, 50.000 file. Lấy source từ GitHub timeout 120 giây. Vượt trần thì từ chối kèm lý do. Chỉ nhận repository GitHub public qua HTTPS; công cụ không nhận và không lưu credential truy cập repository.

**Dữ liệu gửi ra ngoài.** Dữ liệu gửi tới provider model đúng như mục "Đầu vào gửi cho model" của NFR-L3GEN-AI-002, không thêm gì ngoài danh sách đó. Không gửi nguyên file source hoặc cả repository. Trước request đầu tiên, dòng lệnh in tên provider, tên model và loại dữ liệu sẽ gửi (AC-L3GEN-028-01). Dữ liệu đi tới OpenRouter, chuyển tiếp tới nhà cung cấp model; dòng lệnh báo tên provider và model trước khi gửi. Điều khoản dùng dữ liệu là của provider; công cụ nêu tên, không phát biểu thay họ.

**Bí mật trong dòng code.** Code kiểm bằng chứng nguyên văn trên snapshot gốc. Dòng chứa giá trị mang dấu hiệu bí mật (mật khẩu trong URL kết nối, khóa API, token) hiện ở mọi đầu ra và trong payload gửi model với giá trị đã che, kèm đánh dấu "đã che". Giá trị gốc không xuất hiện trong output, log hay payload.

**Vòng đời.** Phase đầu chỉ giữ dữ liệu cần cho lần chạy hiện tại. Dòng lệnh không giữ source hay dữ liệu tạm ngoài thư mục output người dùng chỉ định; dữ liệu tạm xóa khi lần chạy kết thúc. Khi có FR web: source đã tiếp nhận và output hết hạn 24 giờ sau trạng thái cuối của lần chạy, và không được phục vụ sau hạn. Mốc 24 giờ cho source giữ từ BL-r14; áp cho output là mới, vì lịch sử 14 ngày của BL-r14 thuộc phase sau. Nếu máy tắt qua hạn, lần khởi động kế tiếp phải dọn trước khi phục vụ dữ liệu. Output của dòng lệnh do người dùng quản lý.

#### Điều kiện và cách kiểm

Đợt này chạy trên bộ dữ liệu chứa symlink trỏ ra ngoài, source và output lồng nhau, file cấu hình và URL kết nối chứa giá trị bí mật. Kiểm cây source trước và sau khi chạy phải giống nhau về nội dung. Kiểm dòng lệnh in thông báo trước request đầu tiên, và payload chỉ chứa các mục của NFR-L3GEN-AI-002. Kiểm dòng chứa bí mật vẫn qua bước kiểm nguyên văn, còn output, log và payload gửi model chỉ có bản đã che. Kiểm dữ liệu tạm đã được dọn khi lần chạy kết thúc. Khi có FR ZIP hoặc GitHub, thêm file nén độc hại, đường dẫn thoát vùng giải nén và repository vượt trần.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)

## 7. Câu hỏi mở còn lại

| OQ | Câu hỏi | Owner | Due | Status |
|---|---|---|---|---|
| [OQ-L3GEN-012](../../lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/OQ-L3GEN-012.md) | Luồng "agent thuần" của FR-029 trái NFR-SEC-002, NFR-AI-002 và OQ-L3GEN-009 | Hoàng (cần Khiêm xác nhận vì đổi NFR đã duyệt) | 2026-10-10 | answered |
| [OQ-L3GEN-013](../../lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/OQ-L3GEN-013.md) | Route khai trong file production nhưng router không được gắn vào app nào | Hoàng | 2026-10-10 | open |
| [OQ-L3GEN-014](../../lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/OQ-L3GEN-014.md) | Status khai trong thân handler có phải "status code khai trong code" của AC-029-02 không | Hoàng | 2026-10-10 | open |
| [OQ-L3GEN-015](../../lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/OQ-L3GEN-015.md) | Đáp án nghiệm thu FR-029 cho repo kín: ai lập, ai duyệt, và vai trò của igorbenav | Hoàng (cần Khiêm xác nhận vì liên quan bộ nghiệm thu) | 2026-10-10 | open |
| [OQ-L3GEN-016](../../lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/OQ-L3GEN-016.md) | Lời gọi qua hàm bọc của dự án có tính là "lời gọi HTTP ra ngoài" không | Hoàng | 2026-10-16 | open |
| [OQ-L3GEN-017](../../lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/OQ-L3GEN-017.md) | File trong `scripts/` chỉ import helper cùng thư mục có thuộc phạm vi đọc không | Hoàng | 2026-10-16 | open |
| [OQ-L3GEN-018](../../lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/OQ-L3GEN-018.md) | Bộ kiểm bằng chứng được phân tích tĩnh sâu tới đâu mà vẫn là "agent thuần" | Hoàng | 2026-10-16 | open |
