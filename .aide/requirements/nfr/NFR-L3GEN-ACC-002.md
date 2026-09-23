---
uid: "01M34AM2AKQQ6MATHFRYM6CRZH"
key: "NFR-L3GEN-ACC-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-002","FR-L3GEN-003","FR-L3GEN-004","FR-L3GEN-005","FR-L3GEN-006"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-ACC-001 — Độ đúng của kết quả và bằng chứng

- **Nhóm:** Accuracy.
- **Trạng thái:** ngưỡng đã chốt tại OQ-L3GEN-007 ngày 22/09/2026. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-002](../fr/FR-L3GEN-002.md), [FR-L3GEN-003](../fr/FR-L3GEN-003.md), [FR-L3GEN-004](../fr/FR-L3GEN-004.md), [FR-L3GEN-005](../fr/FR-L3GEN-005.md), [FR-L3GEN-006](../fr/FR-L3GEN-006.md).

## Yêu cầu có thể kiểm chứng

Gộp hai nhóm ràng buộc trước đây tách ở NFR-ACC-001 và NFR-TRACE-001.

**Độ đúng của dữ kiện và component.** Precision và recall đều phải đạt từ 80% trở lên, đo riêng cho từng loại: route, entity/table, lời gọi HTTP, config, event, thư viện, thành viên component và cạnh dependency. Ngưỡng 80% chốt tại OQ-L3GEN-007, thay cho ngưỡng 90% của revision 23 vốn đặt cho bộ luật tất định; bộ trích xuất dùng mô hình ngôn ngữ không có cùng đặc tính sai số nên không dùng lại con số đó.

Chấm thuộc tính riêng với chấm sự tồn tại: một route thiếu prefix không tính là route đúng, một tên bảng suy sai không tính là tên bảng đúng. Nhóm nào chưa đủ mẫu thì báo TP/FP/FN, không báo đạt.

**Bằng chứng.** Mọi kết luận công bố phải có bằng chứng trỏ tới file có thật trong snapshot đã phân tích. Tỷ lệ này phải đạt 100%, không có ngoại lệ: kết luận không thỏa thì bị loại trước khi xuất, không được hạ thành cảnh báo. Bằng chứng không được trỏ sang snapshot khác hoặc sang source hiện tại trên đĩa.

**Nhãn chất lượng.** Confidence, completeness và coverage là ba trục độc lập, không dùng trục này thay trục kia. Nhãn `exact` chỉ dùng cho kết luận đọc trực tiếp từ bằng chứng; kết luận suy ra mang nhãn `inferred` kèm lý do. Không được nâng `inferred` thành `exact` để kết quả trông chắc chắn hơn. Tỷ lệ nhãn khớp đánh giá người duyệt phải đạt từ 80% trở lên. Riêng tỷ lệ gán `exact` cho kết luận thật ra sai phải ở mức 5% trở xuống, và là chỉ số chặn: gán nhãn chắc chắn cho kết luận sai gây hại hơn bỏ sót, vì người đọc tin mà không kiểm lại.

## Điều kiện và cách kiểm

OBS-L3GEN-001 quy định dataset, người lập đáp án độc lập, cách matching và cỡ mẫu tối thiểu. Nhóm nào chưa đủ mẫu thì báo counts và `not_evaluated`, không báo phần trăm.

Phần bằng chứng kiểm tự động trên mọi lần chạy: đối chiếu từng đường dẫn trong bằng chứng với danh sách file của snapshot. Phần nhãn và độ đúng kiểm bằng đáp án do người lập trước khi xem output. Không loại ca khó ra khỏi mẫu sau khi đã xem kết quả.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
