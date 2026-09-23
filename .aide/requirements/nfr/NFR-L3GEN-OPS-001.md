---
uid: "01M34AM2AK1P2BVFRM6GYDEDCJ"
key: "NFR-L3GEN-OPS-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-001","FR-L3GEN-002","FR-L3GEN-006","FR-L3GEN-007","FR-L3GEN-008"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-OPS-001 — Hiệu năng, độ tin cậy và phạm vi hỗ trợ

- **Nhóm:** Operability.
- **Trạng thái:** ngưỡng tài nguyên chờ chốt cùng OQ-L3GEN-008 vì phụ thuộc quota model. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../fr/FR-L3GEN-001.md), [FR-L3GEN-002](../fr/FR-L3GEN-002.md), [FR-L3GEN-006](../fr/FR-L3GEN-006.md), [FR-L3GEN-007](../fr/FR-L3GEN-007.md), [FR-L3GEN-008](../fr/FR-L3GEN-008.md).

## Yêu cầu có thể kiểm chứng

Gộp NFR-PERF-001, NFR-REL-001, NFR-COMP-001 và phần còn dùng được của NFR-USA-001.

**Thời gian và tài nguyên.** Mỗi lần chạy ghi lại thời gian lấy source, thời gian phân tích và thời gian sinh artifact riêng, cùng bộ nhớ đỉnh và kích thước output. Trần kích thước repository hỗ trợ được công bố và phụ thuộc quota model; repository vượt trần bị từ chối ngay từ đầu kèm lý do, không chạy dở rồi hỏng.

**Lỗi một phần.** Một đơn vị phân tích hỏng không làm hỏng cả lần chạy. Kết quả partial phải nêu rõ phạm vi đã xử lý được. Trạng thái của lần chạy là completed, partial hoặc failed, và phải phản ánh đúng thực tế: không có bộ output trông như hoàn chỉnh khi thực ra thiếu artifact.

**Phạm vi hỗ trợ.** Có một ma trận khai báo, cho mỗi ngôn ngữ và framework, độ sâu phân tích áp dụng và mức chất lượng đi kèm. Ma trận này là nguồn duy nhất để trả lời câu hỏi công cụ hỗ trợ gì; phase đầu chỉ Python/FastAPI có mức hỗ trợ đầy đủ.

**Thông báo cho người dùng.** Mọi lỗi từ chối đầu vào nêu được nguyên nhân và cách sửa, không chỉ báo thất bại chung chung.

## Điều kiện và cách kiểm

Đo trên bộ dữ liệu đã pin, ghi đủ các trường ở trên cho mỗi lần chạy. Dựng ca lỗi một phần bằng cách cố ý làm hỏng một đơn vị phân tích và kiểm trạng thái trả về. Kiểm ma trận hỗ trợ khớp với hành vi thật: mỗi ô trong ma trận có ít nhất một ca kiểm. Đọc lại toàn bộ thông báo lỗi của ba hình thức đầu vào trước nghiệm thu.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
