# Hướng dẫn review PRD L3 Generator

**BL-r14 đã qua Scope Gate — chưa có kết quả nghiệm thu sản phẩm.**

Hoàng đã review đồng ý và Khiêm duyệt Gate 1 ngày 18/09/2026. Xem [review record](../.aide/evidence/reviews/REVIEW-SCOPE-L3GEN-2026-001.yaml) và [approval record](../.aide/evidence/approvals/APPROVAL-SCOPE-L3GEN-2026-001.yaml). Baseline khóa commit `1c283509c3ec1eec5e65de1005f00a8d4e3cbc91`.

PRD và Change Set View trong snapshot giữ nguyên câu chữ tại thời điểm trước khi ký để không làm đổi hash sau review. Trạng thái Gate sau ký đọc từ BL-r14, `change-set.yaml` và approval record; muốn đổi nội dung normative phải mở change request/baseline mới.

## Thứ tự đọc

1. [PRD](../.aide/product/prd/PRD-L3GEN-2609-001.md).
2. [Change Set View](../.aide/generated/change-set-views/CSV-CHG-L3GEN-2026-001.md): 18 FR / 84 AC / 11 NFR; OQ open và answered nhưng chưa closed đều hiển thị.
3. [Báo cáo kiểm cấu trúc](../.aide/generated/traceability/PRD-PACKAGE-CHECK.md).

Góp ý bằng mã FR/AC/NFR/OQ. Nguồn thắng bản tổng hợp; không sửa bản tổng hợp bằng tay.

## Các quyết định xin review

| OQ | Phương án đã chuẩn bị | Người cần xác nhận |
|---|---|---|
| [001](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-001.md) | Closed: Khiêm ký Scope Gate; Hoàng reviewer/UAT mặc định; hai mentor reviewer/cố vấn | Không còn xác nhận |
| [002](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-002.md) | Closed: phase bốn tuần dùng Python qua CLI và web; giữ FR-013/016; Java và FR-017 đầy đủ ở phase sau | Không còn xác nhận |
| [003](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-003.md) | Closed: ma trận Python phase đầu, YAML tĩnh và Java roadmap đã chốt | Không còn xác nhận |
| [004](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-004.md) | Closed: precision exact 90%; dataset/benchmark/ground truth đã chốt; pilot ngoài nhóm không chặn phase đầu | Repo/commit điền trước benchmark; thiếu pilot thì KPI not_evaluated |
| [005](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-005.md) | Closed: web local; GitHub public/ZIP an toàn; AI mặc định tắt và chi phí trả phí 0 đồng; expiry/cleanup đã chốt | Không còn xác nhận |
| [006](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-006.md) | Closed: chấp nhận schema, UID, script và impact cục bộ có công bố giới hạn cho Gate 1; mapping hoàn tất trước Definition of Ready | Không còn xác nhận |

Hạn 19/09 là đề xuất xin ý kiến của nhóm, không phải mentor đã cam kết. Không có dữ liệu giờ khả dụng, tên người thử hay SHA repo được bịa để đóng câu hỏi. Việc chuẩn bị phương án không đồng nghĩa approved.

## Công cụ kiểm

Script hiện có trong repo, không phải công cụ aide chính thức:

```powershell
py -3.12 scripts/prd_package.py check --baseline BL-r14.yaml
py -3.12 scripts/prd_package.py render --baseline BL-r14.yaml
py -3.12 scripts/impact.py --baseline BL-r14.yaml
```

Check kiểm hash/revision/key/UID; báo cáo bổ sung kiểm AC và file links có phạm vi riêng. Không có lệnh snapshot trong helper hiện tại. Khi đổi nguồn: tăng revision, tạo candidate mới từ bytes nguồn, kiểm rồi render; không ghi đè baseline cũ. Nếu có review/approval phải follow re-review, không xóa evidence để vượt guard. Impact local không xác nhận consumer ngoài repo hoặc ảnh hưởng code. PII/financial chưa đánh giá, không coi null là false.

[Quy trình mentor](agentic-sdlc-execution-guide.md) và [nguồn](sdlc-sources/) giữ nguyên để đối chiếu. Design/test mapping được lập sau Scope Gate và phải hoàn tất trước Definition of Ready cho code theo OQ-006.
