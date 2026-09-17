---
uid: "01M2J06Z56APEKQQ79N6N073Q8"
key: "NFR-L3GEN-DET-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-001","FR-L3GEN-006","FR-L3GEN-007","FR-L3GEN-008","FR-L3GEN-010","FR-L3GEN-011","FR-L3GEN-012","FR-L3GEN-013","FR-L3GEN-016"],"measured_by":["OBS-L3GEN-001"],"blocked_by":["OQ-L3GEN-004"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-DET-001 — Tái lập dữ kiện và định danh

- **Nhóm:** Determinism.
- **Trạng thái:** ngưỡng và phạm vi đề xuất, chưa được mentor duyệt, chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../fr/FR-L3GEN-001.md), [FR-L3GEN-006](../fr/FR-L3GEN-006.md), [FR-L3GEN-007](../fr/FR-L3GEN-007.md), [FR-L3GEN-008](../fr/FR-L3GEN-008.md), [FR-L3GEN-010](../fr/FR-L3GEN-010.md), [FR-L3GEN-011](../fr/FR-L3GEN-011.md), [FR-L3GEN-012](../fr/FR-L3GEN-012.md), [FR-L3GEN-013](../fr/FR-L3GEN-013.md), [FR-L3GEN-016](../fr/FR-L3GEN-016.md).

## Yêu cầu có thể kiểm chứng

Cùng snapshot source, cấu hình phân tích, rule version và tool version phải cho cùng cấu trúc, cạnh, nhãn và ID trong JSON chuẩn hóa, độc lập output directory, chế độ AI và **kênh sử dụng**. Timestamp, duration, analysis_id và đường dẫn workspace tuyệt đối thuộc run metadata, không làm đổi ID dữ kiện. L3 phần diễn giải AI không nằm trong cam kết byte-identical.

**Độc lập kênh.** CLI nhận thư mục local (FR-L3GEN-001), web nhận Git URL hoặc ZIP (FR-L3GEN-016). Cùng một source đi qua hai kênh phải cho cùng tập application, component, route, entity, external system, cạnh dependency, nhãn confidence/completeness và cùng danh sách limitation. Được phép khác: đường dẫn gốc trong evidence, vì hai kênh đặt source ở vị trí khác nhau; vị trí tương đối trong repository phải giống nhau. Web có thêm màn hình khám phá và lịch sử, nhưng không được sinh thêm hoặc bớt dữ kiện so với CLI.

## Điều kiện và cách kiểm

Chạy 3 lần vào các output khác nhau, trong đó bật AI stub với mô tả khác; so sánh canonical JSON sau phép chuẩn hóa công bố. Không sửa timestamp/duration thành hằng để làm test pass. Chạy lại sau source edit phải đổi digest và phần liên quan.

Kiểm độc lập kênh: pin một repository ở một commit, chạy CLI trên bản trên đĩa và chạy web trên bản ZIP của cùng commit đó, cùng tắt AI; so sánh canonical JSON sau khi chuẩn hóa đường dẫn gốc. Khác biệt ở bất kỳ fact, quan hệ, nhãn hoặc limitation nào là lỗi chặn phát hành, không phải khác biệt về trình bày.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

