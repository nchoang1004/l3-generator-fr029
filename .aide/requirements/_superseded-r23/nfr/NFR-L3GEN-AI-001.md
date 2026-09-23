---
uid: "01M2J06Z53NZ07VJNMHBDS8DR1"
key: "NFR-L3GEN-AI-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-010","FR-L3GEN-012"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-AI-001 — Giới hạn và ranh giới AI

- **Nhóm:** AI reliability.
- **Trạng thái:** ngưỡng chất lượng, provider và giới hạn chi phí đã chốt tại OQ-L3GEN-004/005; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-010](../fr/FR-L3GEN-010.md), [FR-L3GEN-012](../fr/FR-L3GEN-012.md).

## Yêu cầu có thể kiểm chứng

AI không được sửa IAM/architecture model, tạo entity/edge hoặc category finding mới. Chỉ nhận output đúng schema và ID đã có. Mỗi request timeout tối đa 30 giây, retry tối đa 2 lần; mỗi phiên tối đa 20 request. Phase đầu có trần chi phí trả phí bằng 0 đồng, chỉ dùng quota miễn phí; chưa cấu hình được cap tương ứng thì không gọi AI. Hết quota, rate limit, thiếu key/SDK hoặc đạt cap thì tiếp tục trả dữ kiện tĩnh và cảnh báo. Provider là tham số cấu hình, không khóa cứng vào một hãng, nhưng chỉ adapter được công bố là hỗ trợ mới được sử dụng; khóa API do người dùng cung cấp tại thời điểm chạy và không được ghi vào output, log, evidence hay bộ kết quả lưu lại. Công cụ không phát biểu thay người dùng về mức an toàn dữ liệu của provider họ chọn; điều khoản của provider thuộc trách nhiệm người dùng.

## Điều kiện và cách kiểm

Mock provider trả JSON hỏng, ID lạ, chèn route, timeout, 429 và trả mô tả khác; so sánh model trước/sau. Kiểm request count và logging. Đặt khóa API dạng canary rồi kiểm toàn bộ output, log và evidence không chứa giá trị đó; kiểm đổi provider bằng cấu hình mà không sửa code. Ngân sách thật/provider chờ OQ, không dùng giá hay model giả.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

## Liên kết

- [Phương pháp đo](../../../observability/OBS-L3GEN-001.md).
- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md).

