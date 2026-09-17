---
uid: "01M2J06Z53NZ07VJNMHBDS8DR1"
key: "NFR-L3GEN-AI-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-010","FR-L3GEN-012"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-004","OQ-L3GEN-005"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-AI-001 — Giới hạn và ranh giới AI

- **Nhóm:** AI reliability.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-010](../fr/FR-L3GEN-010.md), [FR-L3GEN-012](../fr/FR-L3GEN-012.md).

## Yêu cầu có thể kiểm chứng

AI không được sửa IAM/architecture model, tạo entity/edge hoặc category finding mới. Chỉ nhận output đúng schema và ID đã có. Mỗi request timeout tối đa 30 giây, retry tối đa 2 lần; mỗi phiên tối đa 20 request. Chi phí/token cap phải cấu hình trước khi bật với provider được chọn; chưa có cấu hình cap thì không gọi AI. Rate limit, thiếu key/SDK hoặc cap đạt thì tiếp tục trả dữ kiện tĩnh và cảnh báo.

## Điều kiện và cách kiểm

Mock provider trả JSON hỏng, ID lạ, chèn route, timeout, 429 và trả mô tả khác; so sánh model trước/sau. Kiểm request count và logging. Ngân sách thật/provider chờ OQ, không dùng giá hay model giả.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

