---
uid: "01M2J06Z5BFR4D9T1GN1BJ2EW0"
key: "NFR-L3GEN-REL-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-001","FR-L3GEN-002","FR-L3GEN-008","FR-L3GEN-009","FR-L3GEN-016","FR-L3GEN-017","FR-L3GEN-018"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-004"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-REL-001 — Hoàn tất, lỗi một phần và cách ly phiên

- **Nhóm:** Reliability.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../fr/FR-L3GEN-001.md), [FR-L3GEN-002](../fr/FR-L3GEN-002.md), [FR-L3GEN-008](../fr/FR-L3GEN-008.md), [FR-L3GEN-009](../fr/FR-L3GEN-009.md), [FR-L3GEN-016](../fr/FR-L3GEN-016.md), [FR-L3GEN-017](../fr/FR-L3GEN-017.md).

## Yêu cầu có thể kiểm chứng

Parse lỗi một file không phá phần hợp lệ. Trạng thái partial dựa trên phạm vi mất hoặc thuộc tính/quan hệ chưa giải được, không chỉ files_skipped. Một bộ output chỉ được đánh dấu hoàn tất khi mọi artifact bắt buộc cho phase đã ghi và kiểm cấu trúc thành công. Source gốc và output lần trước không bị sửa. Job song song có workspace riêng; hủy/lỗi không để job running vĩnh viễn.

## Điều kiện và cách kiểm

Fault injection tại scan, parse, clone, ghi output, worker crash, cancel; xác nhận trạng thái cuối, file nguồn không đổi và phiên khác không lẫn dữ liệu. Các số đếm phải có định nghĩa tập file rõ.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

