---
uid: "01M2J06Z5GY61E2YBB7T18XEN6"
key: "NFR-L3GEN-USA-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-001","FR-L3GEN-008","FR-L3GEN-009","FR-L3GEN-013","FR-L3GEN-017"],"measured_by":["OBS-L3GEN-002"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-USA-001 — Khả năng sử dụng và tiếp cận

- **Nhóm:** Usability.
- **Trạng thái:** ngưỡng và phương pháp đã chốt tại OQ-L3GEN-004; chưa đo nghiệm thu, pilot ngoài nhóm có thể `not_evaluated` trong phase đầu.
- **Áp dụng:** [FR-L3GEN-001](../fr/FR-L3GEN-001.md), [FR-L3GEN-008](../fr/FR-L3GEN-008.md), [FR-L3GEN-009](../fr/FR-L3GEN-009.md), [FR-L3GEN-013](../fr/FR-L3GEN-013.md), [FR-L3GEN-017](../fr/FR-L3GEN-017.md).

## Yêu cầu có thể kiểm chứng

Người mới theo README cài và chạy ví dụ CLI no-AI trong tối đa 10 phút trên môi trường đã có Python và mạng cài package. Web có trạng thái rỗng/tải/lỗi/một phần, thông báo hành động khắc phục. Luồng chính dùng được bằng bàn phím; mọi input có label, focus nhìn thấy; thông tin tin cậy không dựa chỉ vào màu. Review UI kiểm viewport 1366×768 và 390×844; accessibility tự động và kiểm tay, ngưỡng tương phản normal text ≥4.5:1 theo chuẩn nội bộ đề xuất.

## Điều kiện và cách kiểm

Web cung cấp cả chế độ sáng và tối; người dùng chọn được chế độ. Kiểm bàn phím, focus và tương phản ở cả hai chế độ, kể cả trạng thái rỗng/tải/lỗi/một phần. Đây là phạm vi áp dụng theo checklist UI/UX Gate của mentor, không có ngoại lệ một theme.

OBS-L3GEN-002 mô tả thử với người chưa dùng tool; không thay thử người bằng việc tác giả tự demo. Có lỗi input, output trống và graph dài trong buổi thử. Kiểm trên thiết bị chính thật và với chuỗi dài nhất của các ngôn ngữ được hỗ trợ; ghi thiết bị, browser, theme và kết quả. Mock dùng design token thật; thiết kế phải thể hiện một hành động chính rõ cho mỗi màn hình theo checklist gate.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

## Liên kết

- [Phương pháp đo](../../../observability/OBS-L3GEN-002.md).
- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md).

