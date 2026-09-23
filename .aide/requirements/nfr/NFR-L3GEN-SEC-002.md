---
uid: "01M34AM2AKCTWDBD72J4X3R13C"
key: "NFR-L3GEN-SEC-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-001","FR-L3GEN-003","FR-L3GEN-007","FR-L3GEN-008"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-SEC-001 — An toàn khi tiếp nhận source và vòng đời dữ liệu

- **Nhóm:** Security và Privacy.
- **Trạng thái:** phạm vi đã chốt; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../fr/FR-L3GEN-001.md), [FR-L3GEN-003](../fr/FR-L3GEN-003.md), [FR-L3GEN-007](../fr/FR-L3GEN-007.md), [FR-L3GEN-008](../fr/FR-L3GEN-008.md).
- **Threat model:** [TM-SYS-L3GEN](../../architecture/threat-model/TM-SYS-L3GEN.md).

## Yêu cầu có thể kiểm chứng

Gộp NFR-SEC-001 và NFR-PRIV-001 cũ.

**Read-only với source.** Không chạy, không import, không `exec` hay `eval`, không cài dependency, không chạy hook hoặc submodule, và không ghi ngược vào cây source đầu vào.

**Tiếp nhận an toàn.** File nén giải ra phải nằm trong vùng xử lý; đường dẫn thoát khỏi vùng đó bị từ chối. Có trần kích thước và số file cho một lần tiếp nhận. Chỉ nhận repository GitHub public qua HTTPS; công cụ không nhận và không lưu credential truy cập repository.

**Dữ liệu gửi ra ngoài.** Trước khi chạy, người dùng được cho biết dữ liệu nào sẽ được gửi tới provider model. Giá trị cấu hình mang dấu hiệu bí mật bị che trước khi vào bất kỳ đầu ra nào, kể cả payload gửi model.

**Vòng đời.** Phase đầu chỉ giữ dữ liệu cần cho lần chạy hiện tại. Source đã tiếp nhận và output tạm được dọn theo vòng đời đã công bố; không giữ lại bản sao source ngoài phạm vi đó.

## Điều kiện và cách kiểm

Chạy trên bộ dữ liệu chứa file nén độc hại, đường dẫn thoát vùng giải nén, symlink trỏ ra ngoài, repository vượt trần kích thước, và file cấu hình chứa giá trị bí mật. Kiểm cây source trước và sau khi chạy phải giống nhau về nội dung. Kiểm payload gửi model không chứa giá trị bí mật. Kiểm dữ liệu tạm đã được dọn sau vòng đời đã công bố.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
