---
uid: "01M34AM2AKQQ6MATHFRYM6CRZH"
key: "NFR-L3GEN-ACC-002"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-028","FR-L3GEN-029","FR-L3GEN-030","FR-L3GEN-031"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-ACC-002 — Độ đúng của kết quả và bằng chứng

- **Nhóm:** Accuracy.
- **Trạng thái:** ngưỡng dữ kiện L3 chốt tại OQ-L3GEN-007 ngày 22/09/2026. Ngưỡng sơ đồ theo tiêu chí nhóm dùng khi phát triển (Khiêm, 02/10/2026). Revision 4 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002 và quyết định của Khiêm: chấm trên từng repo kín nhỏ và vừa; thêm lại loại HTTP; nhãn `exact` chấm theo đáp án KPI-L3GEN-008 (đề xuất của Hoàng); bằng chứng của dòng chứa bí mật. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-028](../fr/FR-L3GEN-028.md), [FR-L3GEN-029](../fr/FR-L3GEN-029.md), [FR-L3GEN-030](../fr/FR-L3GEN-030.md), [FR-L3GEN-031](../fr/FR-L3GEN-031.md).

## Yêu cầu có thể kiểm chứng

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

## Điều kiện và cách kiểm

OBS-L3GEN-001 quy định dataset, người lập đáp án độc lập và cách matching. Mọi tỷ lệ báo kèm số đếm; mẫu số bằng 0 thì `not_evaluated`, không báo phần trăm.

Phần bằng chứng kiểm tự động trên mọi lần chạy: đối chiếu từng dữ kiện được trích dẫn với tập dữ kiện, từng đường dẫn với danh sách file của snapshot, và hai đầu của mỗi cạnh với vị trí và đích của dữ kiện. Máy kiểm được bằng chứng có tồn tại và nối đúng; việc dữ kiện có thật sự đủ ý nghĩa cho kết luận thì chấm bằng đáp án của người. Phần nhãn và độ đúng kiểm bằng đáp án do người hoặc subagent lập trước khi xem output. Không loại ca khó ra khỏi mẫu sau khi đã xem kết quả.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
