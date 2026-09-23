---
uid: "01M34AM2AKQQ6MATHFRYM6CRZH"
key: "NFR-L3GEN-ACC-002"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-020","FR-L3GEN-021","FR-L3GEN-022","FR-L3GEN-023","FR-L3GEN-024"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-ACC-002 — Độ đúng của kết quả và bằng chứng

- **Nhóm:** Accuracy.
- **Trạng thái:** ngưỡng đã chốt tại OQ-L3GEN-007 ngày 22/09/2026. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-020](../fr/FR-L3GEN-020.md), [FR-L3GEN-021](../fr/FR-L3GEN-021.md), [FR-L3GEN-022](../fr/FR-L3GEN-022.md), [FR-L3GEN-023](../fr/FR-L3GEN-023.md), [FR-L3GEN-024](../fr/FR-L3GEN-024.md).

## Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-ACC-001 và NFR-L3GEN-TRACE-001 của BL-r14.

**Độ đúng của dữ kiện và component.** Precision và recall đều phải đạt từ 80% trở lên, đo riêng cho từng loại: route, entity/table, lời gọi HTTP, config, event, thư viện, thành viên component và cạnh dependency. Ngưỡng 80% chốt tại OQ-L3GEN-007, thay cho ngưỡng 90% của revision 23 vốn đặt cho bộ luật tất định; bộ trích xuất dùng mô hình ngôn ngữ không có cùng đặc tính sai số nên không dùng lại con số đó.

Chấm thuộc tính riêng với chấm sự tồn tại: một route thiếu prefix không tính là route đúng, một tên bảng suy sai không tính là tên bảng đúng. Nhóm nào chưa đủ mẫu thì báo TP/FP/FN, không báo đạt.

**Bằng chứng.** Bằng chứng của một kết luận là các dữ kiện code trong tập dữ kiện của lần chạy, mỗi dữ kiện nằm ở file có thật trong snapshot đã phân tích. Với cạnh dependency A→B, phải có ít nhất một dữ kiện đã xác định đích, vị trí thuộc A và đích thuộc B. Code kiểm điều này; lời khẳng định của model không được tính là bằng chứng. Tỷ lệ kết luận công bố có bằng chứng hợp lệ phải đạt 100%, không có ngoại lệ: kết luận không thỏa thì bị loại trước khi xuất, không được hạ thành cảnh báo. Bằng chứng không được trỏ sang snapshot khác hoặc sang source hiện tại trên đĩa.

**Nhãn chất lượng.** Confidence, completeness và coverage là ba trục độc lập, không dùng trục này thay trục kia. Nhãn `exact` chỉ dùng cho kết luận đọc trực tiếp từ bằng chứng; kết luận suy ra mang nhãn `inferred` kèm lý do. Không được nâng `inferred` thành `exact` để kết quả trông chắc chắn hơn. Tỷ lệ nhãn khớp đánh giá người duyệt phải đạt từ 80% trở lên. Riêng tỷ lệ gán `exact` cho kết luận thật ra sai phải ở mức 5% trở xuống, và là chỉ số chặn: gán nhãn chắc chắn cho kết luận sai gây hại hơn bỏ sót, vì người đọc tin mà không kiểm lại.

## Điều kiện và cách kiểm

OBS-L3GEN-001 quy định dataset, người lập đáp án độc lập, cách matching và cỡ mẫu tối thiểu. Nhóm nào chưa đủ mẫu thì báo counts và `not_evaluated`, không báo phần trăm.

Phần bằng chứng kiểm tự động trên mọi lần chạy: đối chiếu từng dữ kiện được trích dẫn với tập dữ kiện, từng đường dẫn với danh sách file của snapshot, và hai đầu của mỗi cạnh với vị trí và đích của dữ kiện. Máy kiểm được bằng chứng có tồn tại và nối đúng; việc dữ kiện có thật sự đủ ý nghĩa cho kết luận thì chấm bằng đáp án của người. Phần nhãn và độ đúng kiểm bằng đáp án do người lập trước khi xem output. Không loại ca khó ra khỏi mẫu sau khi đã xem kết quả.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
