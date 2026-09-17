---
uid: "01M2J06Z54XVJ0QPKEB14CW1C7"
key: "NFR-L3GEN-COMP-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 5
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-001","FR-L3GEN-002","FR-L3GEN-003","FR-L3GEN-004","FR-L3GEN-005","FR-L3GEN-008","FR-L3GEN-013","FR-L3GEN-014","FR-L3GEN-015","FR-L3GEN-018"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-003","OQ-L3GEN-004"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-COMP-001 — Stack và môi trường được hỗ trợ

- **Nhóm:** Compatibility.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../fr/FR-L3GEN-001.md), [FR-L3GEN-002](../fr/FR-L3GEN-002.md), [FR-L3GEN-003](../fr/FR-L3GEN-003.md), [FR-L3GEN-004](../fr/FR-L3GEN-004.md), [FR-L3GEN-005](../fr/FR-L3GEN-005.md), [FR-L3GEN-008](../fr/FR-L3GEN-008.md), [FR-L3GEN-013](../fr/FR-L3GEN-013.md), [FR-L3GEN-014](../fr/FR-L3GEN-014.md), [FR-L3GEN-015](../fr/FR-L3GEN-015.md).

## Yêu cầu có thể kiểm chứng

Đề bài cho phép ưu tiên 1–2 stack. Product chốt hai stack: Python/FastAPI và Java/Spring Boot. Ma trận phiên bản và thư viện dưới đây còn là đề xuất; Tech Lead/QA đối chiếu repo mẫu tại OQ-L3GEN-003/004 trước khi chốt, không dùng khả năng của code hiện có làm căn cứ duy nhất.

Stack thứ nhất — Python: cú pháp Python 3.10–3.12; FastAPI methods GET/POST/PUT/DELETE/PATCH; SQLAlchemy declarative Column; requests/httpx; Pydantic settings; confluent_kafka. SQLModel, mapped_column, method khác và SDK khác phải có capability riêng trước khi được gọi là hỗ trợ.

Stack thứ hai — Java: Spring Boot. Framework Java ngoài Spring Boot nằm ngoài phạm vi và phải hiện ra ở phần giới hạn. Ma trận annotation, ORM và thư viện Kafka phía Java được chốt ở thiết kế trước khi gọi là hỗ trợ.

Hai stack dùng chung contract kết quả nhưng không dùng chung rule: adapter Kafka của Python và của Java là hai bộ riêng. Event chỉ hỗ trợ Kafka; broker khác nằm ngoài phạm vi.

Phiên bản runtime của chính công cụ được chọn và pin ở thiết kế.

Môi trường sử dụng đề xuất: CLI trên Windows 11 và Ubuntu 24.04, hỗ trợ tên file/path Unicode và có dấu cách; web trên Chrome và Edge. Phiên bản browser ổn định dùng để kiểm được ghi cụ thể tại thời điểm kiểm; Mermaid renderer/version pin ở contract.

## Điều kiện và cách kiểm

Chạy cùng bộ supported fixtures trên cả hai OS; ghi interpreter, package/rule/renderer/browser versions. Lỗi cú pháp do version ngoài phạm vi phải được báo rõ. Có ma trận supported/partial/unsupported thay cho một checkbox hỗ trợ cả ngôn ngữ.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

