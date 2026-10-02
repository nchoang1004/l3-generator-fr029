---
uid: "01M36K31QW5H0G8JKV8BZD5H8Y"
key: "CMP-L3GEN-005"
type: "component"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"implements":["CAP-L3GEN-010"],"governed_by":["ADR-2026-003","ADR-2026-004"],"constrained_by":["TM-SYS-L3GEN"],"depends_on":["CMP-L3GEN-004","CMP-L3GEN-006"]}
verified_at: 2026-10-02
verified_against: [{"key":"CAP-L3GEN-010","revision":2},{"key":"ADR-2026-003","revision":4},{"key":"ADR-2026-004","revision":2},{"key":"ADR-2026-001","revision":7},{"key":"FR-L3GEN-028","revision":3},{"key":"FR-L3GEN-029","revision":3},{"key":"NFR-L3GEN-AI-002","revision":6},{"key":"NFR-L3GEN-ABST-002","revision":5},{"key":"GLOSS-L3GEN-001","revision":10}]
classification: "internal"
ai_assisted: true
---

# CMP-L3GEN-005 — Dựng mô hình kiến trúc

**Revision 3 (02/10/2026):** viết lại theo [ADR-2026-004](../adr/ADR-2026-004.md) (chia component theo contract), FR-L3GEN-028 và code thật. Model gộp nhóm route và đặt tên; không còn đề xuất cạnh hay chia repository phẳng. Thêm vai trò file của FR-L3GEN-029. Code ở `experiments/quote-evidence/`.

**Revision 4 (02/10/2026):** sửa theo review REVIEW-ARCH-L3GEN-2026-001 (A5, A11, A13, A15): một mô hình duy nhất cho mọi output (Khiêm quyết A5 ngày 02/10/2026); tập contract lấy từ CMP-004; thêm 3 lệch; bỏ cạnh `governed_by` ADR-2026-001 (ADR đó ràng buộc FR, xem mục Liên quan).

## 1. Trách nhiệm

Thực hiện [CAP-L3GEN-010](../l1/CAP-L3GEN-010.md). Biến tập dữ kiện thành **một** mô hình kiến trúc mà sơ đồ và `tech-specs/` cùng dùng: component, file thành viên, chủ của từng contract, mũi tên, hệ thống ngoài, vai trò file.

| Việc | Ai làm | Luật |
|---|---|---|
| Lần theo từng contract trong tập do [CMP-L3GEN-004](CMP-L3GEN-004.md) lập, xuống tới bảng và hệ thống ngoài, ở mức tên cấp cao nhất | Code | FR-L3GEN-028 "Cách xếp file" |
| Lập nhóm route theo file khai báo; xếp tên và file vào nhóm | Code | FR-L3GEN-028 "Cách xếp file", "Component là gì" |
| Gộp nhóm route cùng trách nhiệm; đặt tên, viết một câu trách nhiệm; chọn tên dùng chung chỉ một component dùng | Model qua [CMP-L3GEN-006](CMP-L3GEN-006.md), mỗi quyết định trỏ mã dòng | [NFR-L3GEN-AI-002](../../requirements/nfr/NFR-L3GEN-AI-002.md) |
| Kiểm đề xuất: mỗi nhóm thuộc đúng một component, tên dùng chung dùng tối đa một lần, mã dòng có trong danh sách đã gửi; quyết gửi lại một lần | Code | NFR-L3GEN-AI-002 "Kiểm câu trả lời" |
| Chủ contract: route theo file khai route, bảng theo file khai model, sự kiện theo file có điểm gửi hoặc nhận | Code | FR-L3GEN-028, 030, 031 |
| Mũi tên: gộp lời gọi thuộc luồng giữa hai component; bỏ lắp ráp, kiểm tra rồi quay về, chỉ truyền session | Code | FR-L3GEN-028 "Mũi tên nào được vẽ" |
| Vai trò file trong component; Service mang nhãn `inferred` | Code | FR-L3GEN-029 "Cấu trúc component", glossary mục 3a |
| Trần 50 node: chọn component lên hình; phần bị cắt vẫn trong mô hình | Code | [NFR-L3GEN-ABST-002](../../requirements/nfr/NFR-L3GEN-ABST-002.md) |

**Mô hình duy nhất.** Sơ đồ, `tech-specs/`, README và JSON đều dựng từ mô hình này. Không bước nào dựng mô hình thứ hai.

Model không tách nhóm route, không thêm mũi tên, không sửa dữ kiện. Component này không gọi provider trực tiếp, không đọc source mới, không công bố; kiểm lần cuối là việc của [CMP-L3GEN-007](CMP-L3GEN-007.md). [CMP-L3GEN-008](CMP-L3GEN-008.md) dùng chủ contract ở đây để chia thư mục, không tự gán lại.

## 2. Cấu trúc bên trong

| Phần | Việc | Code hiện tại |
|---|---|---|
| Lần theo contract | Lần theo lời gọi từ từng contract; lập nhóm; chủ của từng tên | `contract_trace.py` (`analyse`) |
| Nhờ model | Dựng đầu vào có mã dòng, kiểm câu trả lời, gửi lại một lần | `contract_llm.py` (`prompt`, `check`, `run`); lớp `Lines` lấy từ `ai7.py`, module v7 (lệch 005-8) |
| Xếp file | Mỗi file theo component chiếm nhiều tên nhất; file dùng chung tách theo việc; file không nhóm nào tới theo thư mục | `l3gen.py` (`split`) |
| Vai trò file | Gán một vai trò mỗi file theo dấu hiệu | `l3gen.py` (`role`) |
| Mô hình kiến trúc | Component, file thành viên, chủ contract, mũi tên, hệ thống ngoài, điểm vào, vai trò file; nguồn của mọi output | Đang dựng hai lần: `l3gen.py` (`archdia`) cho sơ đồ và `l3slice/model.py` (`build`) cho L3 (lệch 005-9) |

## 3. Sequence

```mermaid
sequenceDiagram
    participant R as CMP-001 Điều phối
    participant A as CMP-005 Dựng mô hình
    participant M as CMP-006 Cổng gọi model
    R->>A: tập dữ kiện
    A->>A: liệt kê contract, lần theo route và tác vụ, lập nhóm route
    A->>M: nhóm route, tên dùng chung, các dòng mang mã
    M-->>A: đề xuất hoặc lỗi
    A->>A: kiểm đề xuất
    opt sai schema hoặc sai luật
        A->>M: gửi lại một lần kèm danh sách lỗi
        M-->>A: đề xuất mới hoặc lỗi
        A->>A: kiểm lại; vẫn sai thì loại phần vi phạm
    end
    A->>A: xếp file, chủ contract, mũi tên, vai trò file, chọn node
    A-->>R: mô hình + đề xuất bị loại kèm lý do
```

## 4. Failure mode

| Hỏng ở đâu | Hành vi |
|---|---|
| Model lỗi, thiếu khóa, chạm trần; hoặc JSON vẫn sai sau lần gửi lại | Giữ cách chia của code; tên theo đường dẫn, nhãn `inferred` lý do "đặt theo đường dẫn"; `partial` (AC-L3GEN-028-08) |
| Đề xuất đúng schema nhưng vi phạm luật, sau lần gửi lại | Loại phần vi phạm, giữ phần hợp lệ, ghi lý do vào `archdia.json` (AC-L3GEN-028-05) |
| File có code mà không nhóm nào đi tới | Theo component đông file nhất cùng thư mục, nhãn `inferred` "theo thư mục"; không có thì "Chưa xếp", ghi ở phần giới hạn |
| Quá 50 node | Cắt theo luật NFR-L3GEN-ABST-002; component bị cắt vẫn có trong mô hình và trong `tech-specs/` nếu sở hữu contract |
| Lời gọi chưa xác định đích | Không thành mũi tên |

## 5. Transaction boundary

Mô hình chỉ giao đi khi nhất quán: mỗi file thuộc đúng một component, mỗi contract có đúng một chủ, mũi tên có đủ hai đầu. Phần model hỏng thì mô hình vẫn nhất quán, chỉ mang tên theo đường dẫn.

## 6. Idempotency

Phần do code làm (lần theo, lập nhóm, xếp file, mũi tên, vai trò) tất định với cùng tập dữ kiện; hòa thì chọn theo thứ tự cố định. Phần do model làm có thể khác giữa hai lần chạy; mỗi lần ghi provenance (NFR-L3GEN-AI-002).

## 7. Concurrency

Chạy một luồng, vì lần theo và xếp file là phép toàn cục. Mỗi lần chạy gửi model một việc, cộng tối đa một lần gửi lại.

## 8. Lệch với code hiện tại

Đếm ngày 02/10/2026 trên `runs/l3gen-v1/` (7 repository). Mỗi dòng là ứng viên Task ở bước 11.

| # | Lệch | Căn cứ |
|---|---|---|
| 005-1 | Vai trò file: tên lệch FR ("API", "Bảng (entity)" thay "Route", "Model bảng"); file không dấu hiệu thành "Nghiệp vụ" thay "Khác"; chưa có luật Service; chưa có nhãn; chỉ có trong `archdia.md`, chưa liệt kê theo package | AC-L3GEN-029-07 |
| 005-2 | Còn luật chủ bảng "nhóm có nhiều route chạm hơn" và model chọn chủ bảng hòa (`table_owners`); FR mới: bảng theo file khai model | AC-L3GEN-028-03, NFR-L3GEN-AI-002 |
| 005-3 | Gửi lại vẫn sai thì dùng nguyên câu trả lời kèm `errors_left`, không loại phần vi phạm | NFR-L3GEN-AI-002 |
| 005-4 | Mũi tên tính mọi `Depends(...)` và `dependencies=[...]`, kể cả kiểm tra quyền; luật "kiểm tra rồi quay về" có ở `flow.py` nhưng không dùng | AC-L3GEN-028-06 |
| 005-5 | `archdia.json` thiếu schema version, mã snapshot, nhãn `exact` / `inferred`, đề xuất bị loại | AC-L3GEN-028-04, 05, 11 |
| 005-6 | Chưa áp trần 50 node và luật chọn node | NFR-L3GEN-ABST-002 |
| 005-7 | `contract_llm.py` chưa có test với provider giả (JSON hỏng, mã dòng lạ, nhóm dùng hai lần, lỗi mạng) | NFR-L3GEN-AI-002 "Điều kiện và cách kiểm" |
| 005-8 | `contract_llm.py` import cả `ai7.py` (v7, 1.101 dòng, kéo theo `flow.py`, `draft.py`, `graph.py`) chỉ để dùng lớp `Lines` | ADR-2026-004 mục 6 |
| 005-9 | Hai mô hình: `l3gen.archdia` và `l3slice/model.build` dựng riêng từ cùng cách chia | Mục 1 "Mô hình duy nhất" |
| 005-10 | Mũi tên còn vẽ lời gọi tắt kết nối (boilerplate: `close_database()` trong `backend/scripts/`) và lời gọi log (`get_logger`, `logger.info`); FR-028 xếp hai loại này vào cột "Không vẽ" | AC-L3GEN-028-06 |

## Liên quan

| Nguồn | Nội dung |
|---|---|
| [CAP-L3GEN-010](../l1/CAP-L3GEN-010.md) | Dựng mô hình kiến trúc |
| [ADR-2026-004](../adr/ADR-2026-004.md) | Chia component theo contract |
| [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md) | Component, cách xếp file, mũi tên, nhãn |
| [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md) | Vai trò file, chia contract theo component |
| [ADR-2026-001](../adr/ADR-2026-001.md) | Phân tích sâu, trình bày mức component |
| [NFR-L3GEN-ABST-002](../../requirements/nfr/NFR-L3GEN-ABST-002.md) | Trần 50 node |
