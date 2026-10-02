---
uid: "01M36K31QXF9SNPSHE6JDDV4AW"
key: "CMP-L3GEN-008"
type: "component"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"implements":["CAP-L3GEN-012"],"governed_by":["ADR-2026-003","ADR-2026-004"],"constrained_by":["TM-SYS-L3GEN"],"depends_on":["CMP-L3GEN-007"]}
verified_at: 2026-10-02
verified_against: [{"key":"CAP-L3GEN-012","revision":4},{"key":"ADR-2026-003","revision":4},{"key":"ADR-2026-004","revision":2},{"key":"ADR-2026-001","revision":7},{"key":"FR-L3GEN-028","revision":3},{"key":"FR-L3GEN-029","revision":3},{"key":"FR-L3GEN-030","revision":2},{"key":"FR-L3GEN-031","revision":2},{"key":"NFR-L3GEN-ABST-002","revision":5},{"key":"GLOSS-L3GEN-001","revision":10}]
classification: "internal"
ai_assisted: true
---

# CMP-L3GEN-008 — Trình bày và xuất

**Revision 3 (02/10/2026):** viết lại theo code thật và FR-L3GEN-028 đến 031. Thêm `archdia.*`, mục "Cấu trúc component" và "Lời gọi HTTP ra ngoài" trong README. Phần web giữ thiết kế của revision 2 (Khiêm quyết 02/10/2026), chưa có FR. Code ở `experiments/quote-evidence/`.

**Revision 4 (02/10/2026):** sửa theo review REVIEW-ARCH-L3GEN-2026-001 (A4, A10, A15, A17): luôn xuất phần có được, đánh `partial` (Khiêm quyết A4 ngày 02/10/2026); dòng lệnh không sinh lại từng artifact; không che bí mật thêm; escape chuỗi không tin cậy; bỏ cạnh `governed_by` ADR-2026-001 (ADR đó ràng buộc FR).

## 1. Trách nhiệm

Thực hiện [CAP-L3GEN-012](../l1/CAP-L3GEN-012.md). Từ **một** mô hình đã kiểm của [CMP-L3GEN-007](CMP-L3GEN-007.md), sinh mọi output vào một thư mục:

| Output | Nội dung | FR |
|---|---|---|
| `archdia.md`, `archdia.mmd`, `archdia.json` | Sơ đồ component, bảng component, điểm vào, lời gọi giữa component, hệ thống ngoài, cấu hình, thư viện, giới hạn | [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md) |
| `tech-specs/<CMP>/api/`, `schema/`, `events/` | Tài liệu API, TBL, EVT theo component sở hữu; tên file theo FR-L3GEN-029 | [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md) đến 031 |
| `README.md` | Mục lục contract, sơ đồ (cùng sơ đồ `archdia`), cấu trúc component, lời gọi HTTP ra ngoài, contract chưa gán, giới hạn | AC-L3GEN-029-06 |
| `result.json` | Dữ kiện và bằng chứng; cùng mã snapshot và danh sách component với `archdia.json` | AC-L3GEN-028-11 |
| Trang web | Theo dõi lần chạy, tổng quan, đi sâu từng component, mở bằng chứng | Thiết kế revision 2, chưa có FR |

Mọi chuỗi lấy từ repository hoặc do model đặt (tên component, đường dẫn, path route, dòng bằng chứng) được escape trước khi chèn vào Markdown, bảng và Mermaid ([TM-SYS-L3GEN](../threat-model/TM-SYS-L3GEN.md) T-13).

Không làm: không đọc source, không gọi model, không thêm kết luận, không gán lại chủ contract, không che bí mật thêm (in nội dung CMP-007 đã che).

## 2. Cấu trúc bên trong

| Phần | Việc | Code hiện tại |
|---|---|---|
| Sơ đồ | Mermaid và bản mô tả từ mô hình; component bị cắt theo trần node vẫn liệt kê | `l3gen.py` (`mermaid`, `markdown`) |
| Tài liệu L3 | Ba bộ sinh API, TBL, EVT; bảng và khối máy (OpenAPI 3.1, DDL) dùng chung dữ liệu; gắn nguồn từng dòng | `l3slice/render.py` (`render_api`, `render_tbl`, `render_evt`) |
| README, JSON | Mục lục, phần giới hạn, bộ dữ liệu máy đọc | `l3slice/render.py` (`readme`, `plan_bundle`) |
| Kiểm bản xuất | Định dạng, tham chiếu, chỗ đặt file; sơ đồ và `tech-specs/` cùng tập component, cùng tập route, lệch thì ghi ở phần giới hạn | `l3slice/render.py` (`check_doc`, `check_placement`, `check_diagram`) |
| Escape | Escape chuỗi không tin cậy trong Markdown và Mermaid | `l3slice/render.py` (`md`, `mermaid_label`); `l3gen.mermaid/markdown` chưa có (lệch 008-6) |
| Ghi file | Từ chối output không rỗng; ghi vào thư mục tạm rồi đổi tên một lần. Sinh lại một artifact lỗi chỉ có trên web | `l3slice/render.py` (`_publish`, `retry_artifact`) |
| Trang web | Đọc từ cùng bộ JSON; mở bằng chứng thì gọi CMP-007 | `l3slice/web.py`, `l3slice/ui/` |

### Sinh tài liệu L3

Đầu vào phải có snapshot, component, dữ kiện contract, nguồn từng trường và phần giới hạn đã qua CMP-007. Lỗi cấu trúc đầu vào và giá trị `unknown` là hai việc khác nhau: lỗi cấu trúc thì báo lỗi; `unknown` có lý do thì sinh bản `partial`.

| Bộ sinh | Cách dựng |
|---|---|
| API | Gom endpoint theo component sở hữu; giữ method, path đầy đủ, handler, tham số, request/response, status, dependency/auth nếu biết. Bảng và OpenAPI dùng chung danh sách endpoint và trường |
| TBL | Gom bảng theo component sở hữu; giữ tên, cột, kiểu, khóa, nullable. Bảng và DDL dùng chung danh sách cột |
| EVT | Mỗi component có điểm gửi hoặc nhận một tài liệu, ghi vai trò và payload nếu biết. Không tự ghép hai bên theo tên topic |

**Dữ liệu thiếu (Khiêm đã chọn):** xuất phần biết được, đánh dấu `partial`, chỉ rõ trường thiếu và lý do. Markdown giữ dòng `unknown`; khối máy chỉ chứa giá trị biểu diễn được đúng định dạng, kèm danh sách phần bị bỏ. Không tạo tên bảng, kiểu cột, path hoặc status giả. Nội dung lấy từ mô hình, không cắt theo số node đang hiện trên sơ đồ.

## 3. Sequence

```mermaid
sequenceDiagram
    participant R as CMP-001 Điều phối
    participant P as CMP-008 Xuất
    R->>P: mô hình đã kiểm + giới hạn
    P->>P: gom contract theo component sở hữu; sinh API, TBL, EVT
    P->>P: sinh sơ đồ, archdia.*, README, result.json từ cùng mô hình
    P->>P: kiểm định dạng, tham chiếu; kiểm chéo tập component và tập route
    P->>P: ghi vào thư mục tạm, đổi tên thành thư mục output
    P-->>R: danh sách file hoặc artifact lỗi
```

## 4. Failure mode

| Hỏng ở đâu | Hành vi |
|---|---|
| Một artifact sinh lỗi | Ghi artifact nào lỗi ở phần giới hạn, giữ artifact hợp lệ, `partial`. Trên web cho sinh lại riêng artifact đó |
| Sơ đồ và `tech-specs/` lệch tập component hoặc tập route | Vẫn xuất; liệt kê chỗ lệch ở phần giới hạn; `partial` (AC-L3GEN-029-04) |
| Quá 50 node | Sơ đồ cắt theo NFR-L3GEN-ABST-002; `tech-specs/` vẫn đủ mọi component sở hữu contract |
| Trường contract chưa biết, đã có lý do | Xuất phần đã biết, đánh dấu `partial` |
| Không biểu diễn được một phần bằng OpenAPI hoặc DDL hợp lệ | Giữ trong Markdown, liệt kê phần bị bỏ khỏi khối máy kèm lý do |
| Bảng Markdown và khối máy mâu thuẫn, hoặc tham chiếu hỏng | Không công bố artifact đó, ghi lỗi ở phần giới hạn; artifact khác vẫn xuất; `partial` |
| Hai component trùng tên thư mục | Thêm `-2`, `-3` (FR-L3GEN-029) |
| Output không rỗng | Từ chối, không ghi đè |
| Web: output quá 24 giờ, hoặc mở bằng chứng khi file đã đổi | Không phục vụ; báo hết hạn hoặc snapshot không còn khớp |

## 5. Transaction boundary

Đơn vị trọn vẹn là **cả bộ output** của một lần chạy, gồm cả `archdia.*`. Ghi vào thư mục tạm; ghi xong mới đổi tên thành thư mục output, để tiến trình chết giữa chừng không để lại thư mục trông như đã xong. Kết quả `partial` vẫn xuất đủ phần đã có. Trạng thái lần chạy ghi trong `result.json` và `archdia.json` trước khi đổi tên.

## 6. Idempotency

Tất định: cùng mô hình đã kiểm cho cùng bộ file, cùng nội dung. Trên web, sinh lại một artifact lỗi chỉ dùng mô hình của cùng lần chạy và cùng phiên bản bộ sinh; không phân tích lại source, không gọi model, không đổi artifact khác.

## 7. Concurrency

Mỗi lần chạy ghi vào thư mục riêng. Trang web chỉ đọc. Không cần khóa.

## 8. Lệch với code hiện tại

Đếm ngày 02/10/2026 trên `runs/l3gen-v1/` (7 repository). Mỗi dòng là ứng viên Task ở bước 11.

| # | Lệch | Căn cứ |
|---|---|---|
| 008-1 | README là của `l3slice`: thiếu mục "Cấu trúc component" và "Lời gọi HTTP ra ngoài"; sơ đồ trong README là sơ đồ của `l3slice` (có khối "Khác", cạnh `depends_on`), khác `archdia.mmd` | AC-L3GEN-029-06 |
| 008-2 | Hai sơ đồ từ hai mô hình: `architecture.mmd` / `.svg` của `l3slice` và `archdia.mmd` | Glossary bất biến #6 |
| 008-3 | Quá 50 node thì `l3slice` dừng cả phần L3 ("Model vượt 50 node"), thay vì chỉ cắt hình | AC-L3GEN-029-04, NFR-L3GEN-ABST-002 |
| 008-4 | `archdia.*` ghi sau khi `l3slice` đã đổi tên thư mục output, nằm ngoài lần ghi một lần | Mục 5 |
| 008-5 | Chưa kiểm tập route và tập component của `archdia.json` khớp `tech-specs/`, nên chỗ lệch không được ghi ở phần giới hạn. Đếm tay: 6/7 repository khớp; boilerplate lệch 34/33 route, component `interfaces` không có thư mục | AC-L3GEN-029-04 |
| 008-6 | `l3gen.mermaid` và `l3gen.markdown` chèn thẳng tên component, đường dẫn và dòng bằng chứng, không escape | TM-SYS-L3GEN T-13 |

## Liên quan

| Nguồn | Nội dung |
|---|---|
| [CAP-L3GEN-012](../l1/CAP-L3GEN-012.md) | Trình bày và xuất |
| [CMP-L3GEN-007](CMP-L3GEN-007.md) | Kiểm snapshot khi mở bằng chứng |
| [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md), [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md) | Output sơ đồ, tài liệu API, README |
| [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md), [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md) | TBL, EVT |
| [NFR-L3GEN-ABST-002](../../requirements/nfr/NFR-L3GEN-ABST-002.md) | Mức trừu tượng, trần node |
