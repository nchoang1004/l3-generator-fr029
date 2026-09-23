---
uid: "01M2Q78PZHQF770QQVQSX3AG9T"
key: "NFR-L3GEN-ABST-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-006","FR-L3GEN-007","FR-L3GEN-008","FR-L3GEN-011","FR-L3GEN-013"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-ABST-001 — Mức trừu tượng của kết quả trình bày

- **Nhóm:** Abstraction level.
- **Trạng thái:** ngưỡng đã chốt tại OQ-L3GEN-004; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-006](../fr/FR-L3GEN-006.md), [FR-L3GEN-007](../fr/FR-L3GEN-007.md), [FR-L3GEN-008](../fr/FR-L3GEN-008.md), [FR-L3GEN-011](../fr/FR-L3GEN-011.md), [FR-L3GEN-013](../fr/FR-L3GEN-013.md).
- **Quyết định nền:** [ADR-2026-001](../../../architecture/adr/ADR-2026-001.md).

## Yêu cầu có thể kiểm chứng

Phân tích và trình bày là hai mức khác nhau. Engine được đọc sâu tới function, tham số, thuộc tính và phép gán để chứng minh một quan hệ; nhưng kết quả mặc định cho người đọc dừng ở application/component.

Ràng buộc đã chốt:

- Sơ đồ và tài liệu L3 mặc định chỉ có node mức application, component và hệ thống ngoài. Node mức function, class hoặc file không xuất hiện ở lớp mặc định.
- Số node trong một sơ đồ mặc định không tỷ lệ với số function của repository. Ngưỡng đề xuất: repository có ≥500 function vẫn cho sơ đồ mặc định ≤50 node; vượt ngưỡng phải rút gọn có thông báo theo AC-L3GEN-008-03, không xuất sơ đồ đầy đủ rồi để người đọc tự lọc.
- Dữ kiện mức function/class vẫn được giữ trong bộ kết quả, nhưng nằm ở lớp evidence hoặc chẩn đoán có nhãn riêng, không trộn vào lớp kiến trúc mặc định.
- Một quan hệ kiến trúc chỉ tồn tại khi đích đã resolve. Lời gọi chưa resolve được giữ như dữ kiện có nhãn unknown, không được nâng thành cạnh giữa hai component.

Ngưỡng 500/50 đã được chốt tại OQ-L3GEN-004 để có thể kiểm chứng; chưa đo trên tập fixture đã pin.

## Điều kiện và cách kiểm

Chạy trên fixture đã pin, đếm node theo lớp trong bộ kết quả máy đọc được của FR-L3GEN-008, không đếm bằng mắt trên hình. Kiểm cả repository nhỏ và repository ≥500 function. Kiểm rằng bỏ lớp evidence đi thì lớp kiến trúc vẫn đọc được, và mọi cạnh kiến trúc đều có đích đã resolve. Không coi việc sơ đồ vẽ được là bằng chứng mức trừu tượng đúng.

## Người chốt và ngoại lệ

Khiêm chốt ở Scope Gate; Hoàng review nội bộ/UAT theo quyết định đã đóng tại OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

## Liên kết

- [ADR-2026-001](../../../architecture/adr/ADR-2026-001.md).
- [Phương pháp đo](../../../observability/OBS-L3GEN-001.md).
- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md).
