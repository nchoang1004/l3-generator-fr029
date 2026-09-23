---
uid: "01M2J06Z58YD9FQJ9HHAQ77BX9"
key: "NFR-L3GEN-PERF-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-001","FR-L3GEN-008","FR-L3GEN-013","FR-L3GEN-016","FR-L3GEN-017"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-PERF-001 — Thời gian xử lý và giới hạn tài nguyên

- **Nhóm:** Performance.
- **Trạng thái:** ngưỡng và cấu hình benchmark đã chốt tại OQ-L3GEN-004; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../fr/FR-L3GEN-001.md), [FR-L3GEN-008](../fr/FR-L3GEN-008.md), [FR-L3GEN-013](../fr/FR-L3GEN-013.md), [FR-L3GEN-016](../fr/FR-L3GEN-016.md), [FR-L3GEN-017](../fr/FR-L3GEN-017.md).

## Yêu cầu có thể kiểm chứng

Môi trường benchmark chuẩn: 4 CPU logical, RAM 8 GiB, SSD, Python 3.12, no-AI, dependencies đã cài. Nếu máy thực tế khác thì công bố đầy đủ và không ngoại suy. Thời gian analyzer+ghi output (không gồm clone/AI/cài đặt) tối đa 60 giây cho 5.000 dòng Python, và 300 giây cho 50.000 dòng trong tập fixture/repo đã pin. Trần thời gian cho một lần phân tích là 10 phút; quá hạn thì dừng và báo lý do, không trả kết quả như đã hoàn tất.

Giới hạn tiếp nhận: ZIP nén 100 MB, giải nén 500 MB và 50.000 file; vượt ngưỡng phải từ chối hoặc dừng có lý do. Worker tối đa 2 GiB RAM/phiên, 2 phiên chạy cùng lúc; phiên sau xếp hàng. Git fetch timeout 120 giây; mọi giới hạn có trong thông báo/help.

## Điều kiện và cách kiểm

Đo 5 lần cho mỗi repo trên máy công bố, ghi từng lần và worst-case, peak RSS. Không ngoại suy từ máy khác hoặc repo nhỏ. Kiểm input sát/vượt giới hạn, ZIP bomb và job bị timeout; không báo hoàn tất khi bị dừng. OBS-L3GEN-001 mô tả cách thu số, không lặp ngưỡng.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

## Liên kết

- [Phương pháp đo](../../../observability/OBS-L3GEN-001.md).
- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md).

