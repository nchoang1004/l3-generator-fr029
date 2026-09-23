---
uid: "01M2J06Z5EVE034ZTGM0Q8AW50"
key: "NFR-L3GEN-TRACE-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-001","FR-L3GEN-002","FR-L3GEN-003","FR-L3GEN-004","FR-L3GEN-005","FR-L3GEN-006","FR-L3GEN-007","FR-L3GEN-008","FR-L3GEN-011","FR-L3GEN-013","FR-L3GEN-014","FR-L3GEN-015","FR-L3GEN-018"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-TRACE-001 — Nguồn bằng chứng và phiên bản

- **Nhóm:** Traceability.
- **Trạng thái:** ngưỡng và phương pháp đã chốt tại OQ-L3GEN-004; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-002](../fr/FR-L3GEN-002.md), [FR-L3GEN-003](../fr/FR-L3GEN-003.md), [FR-L3GEN-004](../fr/FR-L3GEN-004.md), [FR-L3GEN-005](../fr/FR-L3GEN-005.md), [FR-L3GEN-006](../fr/FR-L3GEN-006.md), [FR-L3GEN-007](../fr/FR-L3GEN-007.md), [FR-L3GEN-008](../fr/FR-L3GEN-008.md), [FR-L3GEN-011](../fr/FR-L3GEN-011.md), [FR-L3GEN-013](../fr/FR-L3GEN-013.md), [FR-L3GEN-014](../fr/FR-L3GEN-014.md), [FR-L3GEN-015](../fr/FR-L3GEN-015.md).

## Yêu cầu có thể kiểm chứng

Mọi thực thể và cạnh khẳng định phải truy về một hoặc nhiều vị trí source trong snapshot đã phân tích; evidence coverage yêu cầu 100% trong tập khẳng định. Inferred ghi rule/reason; unresolved không giả đích. Snapshot có digest, tool/rule/config version; Git commit chỉ đại diện clean snapshot, local dirty tree dùng content digest. Không lấy số dòng hiện tại thay bằng chứng cũ khi source thay đổi.

## Điều kiện và cách kiểm

Đối chiếu toàn bộ evidence về file/range còn trong snapshot; lấy mẫu người đọc xác nhận range thực sự hỗ trợ claim. Kiểm render từ output khác thư mục, source di chuyển, dirty worktree và multi-evidence edges.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

