---
uid: "01M2J06Z5C2VHS90HG20DBH25N"
key: "NFR-L3GEN-SEC-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-001","FR-L3GEN-002","FR-L3GEN-010","FR-L3GEN-016","FR-L3GEN-017","FR-L3GEN-018"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-SEC-001 — An toàn khi tiếp nhận và phân tích source

- **Nhóm:** Security.
- **Trạng thái:** ngưỡng chất lượng và phạm vi môi trường/an toàn đã chốt tại OQ-L3GEN-004/005; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-001](../fr/FR-L3GEN-001.md), [FR-L3GEN-002](../fr/FR-L3GEN-002.md), [FR-L3GEN-010](../fr/FR-L3GEN-010.md), [FR-L3GEN-016](../fr/FR-L3GEN-016.md), [FR-L3GEN-017](../fr/FR-L3GEN-017.md).

## Yêu cầu có thể kiểm chứng

Không import, exec, eval, chạy entrypoint, cài dependency, hook Git hoặc submodule của repository đầu vào. Đọc/giải nén chỉ trong vùng được cấp; không đi theo symlink ra ngoài. Input Git ban đầu chỉ HTTPS GitHub public; từ chối host khác, địa chỉ private/loopback/link-local và redirect trái allowlist; kiểm lại đích kết nối sau DNS/redirect. Web local/workspace tin cậy, không công khai Internet khi chưa có authentication, phân quyền và threat model tương ứng.

## Điều kiện và cách kiểm

Repo có sentinel tạo file/gọi mạng khi import, ZIP traversal/symlink, URL nội bộ và redirect cấm đều không gây thực thi/truy cập/ghi ngoài phạm vi. Kiểm input trả lỗi rõ và cleanup. Threat model/kiểm thử an toàn bắt buộc trước web release; chưa có kết quả kiểm.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate; Security tham gia phần SEC/PRIV. Danh tính theo OQ-L3GEN-001. Không có waiver nào được cấp. Nếu chưa đạt: ghi kết quả failed/not_run, thu hẹp phạm vi qua review hoặc sửa sản phẩm; không tự hạ ngưỡng sau benchmark.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md).
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md).

