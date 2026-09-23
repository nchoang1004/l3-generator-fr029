---
uid: "01M2J06Z51TQ8D15NB9RQGWD0B"
key: "NFR-L3GEN-ACC-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 5
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-003","FR-L3GEN-004","FR-L3GEN-005","FR-L3GEN-006","FR-L3GEN-011","FR-L3GEN-014","FR-L3GEN-015","FR-L3GEN-018"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-ACC-001 — Độ đúng của dữ kiện và component

- **Nhóm:** Accuracy.
- **Trạng thái:** ngưỡng đã chốt tại OQ-L3GEN-004; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-003](../fr/FR-L3GEN-003.md), [FR-L3GEN-004](../fr/FR-L3GEN-004.md), [FR-L3GEN-005](../fr/FR-L3GEN-005.md), [FR-L3GEN-006](../fr/FR-L3GEN-006.md), [FR-L3GEN-011](../fr/FR-L3GEN-011.md), [FR-L3GEN-014](../fr/FR-L3GEN-014.md), [FR-L3GEN-015](../fr/FR-L3GEN-015.md).

## Yêu cầu có thể kiểm chứng

Ngưỡng trước nghiệm thu: precision nhóm exact ≥90% cho từng loại route, entity, HTTP, config, event và internal call edge; recall lần lượt route ≥85%, entity ≥90%, HTTP ≥80%, config ≥80%, event ≥80%, internal call edge trong pattern công bố ≥70%. Đánh giá đúng thuộc tính riêng: không tính một URL thiếu prefix là URL đầy đủ đúng; không tính tên bảng suy sai là tên bảng đúng. Fixture thuộc pattern cam kết phải thỏa tất cả AC. Component grouping so với mapping người duyệt: precision và recall của membership đều ≥85%; dependency exact ≥90% precision. Không dùng tên role inferred như ground truth nghiệp vụ.

## Điều kiện và cách kiểm

OBS-L3GEN-001 quy định đáp án độc lập, sampling, matching và cỡ mẫu. Mỗi nhóm không đủ mẫu báo counts và `not_evaluated` thay vì 100%; ngoài pattern công bố báo độ phủ riêng, không loại ca khó sau khi xem output. Chưa có kết quả nghiệm thu.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

## Liên kết

- [Phương pháp đo](../../../observability/OBS-L3GEN-001.md).
- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md).


## Thư viện bên ngoài

Đối với FR-L3GEN-018, tên, ràng buộc phiên bản, nhãn declared/usage và bằng chứng phải đạt AC trên fixture đã chốt theo OBS-L3GEN-001. Báo số đúng/sai theo thuộc tính; chưa có ngưỡng phần trăm thống kê cho thư viện, không dùng ngưỡng route thay thế. Ma trận hỗ trợ đã chốt tại OQ-003; fixture và đáp án đo tiếp tục xử lý ở OQ-004.
