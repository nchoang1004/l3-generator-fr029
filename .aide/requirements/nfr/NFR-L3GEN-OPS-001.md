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
relations: {"constrains":["FR-L3GEN-019","FR-L3GEN-020","FR-L3GEN-024","FR-L3GEN-025","FR-L3GEN-026"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-OPS-001 — Hiệu năng, độ tin cậy và phạm vi hỗ trợ

- **Nhóm:** Operability.
- **Trạng thái:** ngưỡng đã chốt; trần token của model ở NFR-L3GEN-AI-002 theo OQ-L3GEN-008. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-019](../fr/FR-L3GEN-019.md), [FR-L3GEN-020](../fr/FR-L3GEN-020.md), [FR-L3GEN-024](../fr/FR-L3GEN-024.md), [FR-L3GEN-025](../fr/FR-L3GEN-025.md), [FR-L3GEN-026](../fr/FR-L3GEN-026.md).

## Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-PERF-001, REL-001, COMP-001 và phần còn dùng được của USA-001 của BL-r14. Key OPS-001 chưa từng dùng trước đây.

**Thời gian và tài nguyên.** Mỗi lần chạy ghi lại riêng thời gian lấy source, phân tích tĩnh, gọi model và sinh artifact, cùng bộ nhớ đỉnh và kích thước output.

| Ngưỡng | Giá trị | Nguồn |
|---|---|---|
| Phân tích tĩnh và ghi output, không gồm lấy source và gọi model | ≤ 60 giây cho 5.000 dòng Python; ≤ 300 giây cho 50.000 dòng | Giữ từ BL-r14 |
| Máy đo chuẩn | 4 CPU logical, RAM 8 GiB, SSD, Python 3.12; máy khác thì công bố, không ngoại suy | Giữ từ BL-r14 |
| Bộ nhớ | ≤ 2 GiB mỗi lần chạy | Giữ từ BL-r14 |
| Toàn bộ một lần chạy | ≤ 30 phút; quá hạn thì dừng, trả partial kèm lý do | Mới. 100.000 token ở 8.000 token/phút cần ít nhất 12,5 phút; trần 10 phút của BL-r14 không còn đủ |
| Số lần chạy cùng lúc | 1; lần sau xếp hàng | Mới, vì các lần chạy dùng chung một quota model |

Trần tiếp nhận ở NFR-L3GEN-SEC-002; trần token ở NFR-L3GEN-AI-002. Vượt trần thì từ chối trước bước tương ứng, kèm lý do, không chạy dở rồi hỏng.

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
