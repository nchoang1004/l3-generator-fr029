---
uid: "01M34AM2AJ19YNBG8NA25DMWSG"
key: "NFR-L3GEN-ABST-002"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 5
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-028","FR-L3GEN-029","FR-L3GEN-030","FR-L3GEN-031"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-ABST-002 — Mức trừu tượng của kết quả trình bày

- **Nhóm:** Abstraction level.
- **Trạng thái:** thay cho NFR-L3GEN-ABST-001 của BL-r14, giữ nguyên phạm vi và ngưỡng. Ngưỡng 500/50 đã chốt tại OQ-L3GEN-004 (CHG-L3GEN-2026-001); revision 3 (02/10/2026) chỉ đổi phần áp dụng sang FR-L3GEN-028 đến 031. Revision 4 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: định nghĩa node và luật chọn node khi vượt trần. Revision 5 (02/10/2026) sửa theo recovery review REVIEW-SCOPE-L3GEN-2026-003: component bị cắt chỉ có thư mục `tech-specs/` khi sở hữu contract. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-028](../fr/FR-L3GEN-028.md), [FR-L3GEN-029](../fr/FR-L3GEN-029.md), [FR-L3GEN-030](../fr/FR-L3GEN-030.md), [FR-L3GEN-031](../fr/FR-L3GEN-031.md).
- **Quyết định nền:** [ADR-2026-001](../../architecture/adr/ADR-2026-001.md).

## Yêu cầu có thể kiểm chứng

Phân tích và trình bày là hai mức khác nhau. Công cụ được đọc sâu tới function, tham số và phép gán để chứng minh một quan hệ, nhưng kết quả mặc định cho người đọc dừng ở application/component.

- Sơ đồ mặc định (mức L2) chỉ có node mức application, component và hệ thống ngoài. Node mức function, class hoặc file không xuất hiện ở lớp mặc định.
- Tài liệu L3 liệt kê contract: endpoint, bảng, sự kiện, chia theo component. Function và class chỉ xuất hiện khi là handler hoặc model được nêu trong contract, hoặc ở lớp bằng chứng.
- Số node của sơ đồ mặc định không tỷ lệ với số function của repository. Repository có từ 500 function trở lên vẫn cho sơ đồ mặc định không quá 50 node. Phần vượt trần không bị loại khỏi bộ kết quả mà nằm ở lớp bằng chứng; không xuất sơ đồ đầy đủ rồi để người đọc tự lọc.
- Node của sơ đồ là component (trừ Kiểm thử, Migration, Khác) và hệ thống ngoài. Route, bảng, sự kiện là nội dung ghi trong khối component, không phải node.
- Khi vượt 50 node: giữ mọi hệ thống ngoài; xếp component theo tổng số contract sở hữu và số mũi tên nối với nó, giảm dần, hòa thì theo số file rồi theo tên; lấy từ đầu cho tới đủ trần. Component bị cắt và mũi tên của nó không vẽ, nhưng vẫn có trong `archdia.json`, được liệt kê trong `archdia.md`, và vẫn có thư mục `tech-specs/` nếu sở hữu contract.
- Dữ kiện mức function và class vẫn nằm trong bộ kết quả, nhưng ở lớp bằng chứng có nhãn riêng, không trộn vào lớp kiến trúc mặc định.
- Một quan hệ kiến trúc chỉ tồn tại khi đích đã xác định. Lời gọi chưa xác định được đích giữ ở lớp dữ kiện với nhãn unresolved, không nâng thành cạnh giữa hai component.

## Điều kiện và cách kiểm

Chạy trên bộ dữ liệu đã pin, đếm node theo lớp trong `archdia.json` của FR-L3GEN-028, không đếm bằng mắt trên hình. Kiểm cả repository nhỏ và repository từ 500 function trở lên. Kiểm rằng bỏ lớp bằng chứng đi thì lớp kiến trúc vẫn đọc được, và mọi cạnh kiến trúc đều có đích đã xác định. Sơ đồ vẽ được không phải bằng chứng mức trừu tượng đúng.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
