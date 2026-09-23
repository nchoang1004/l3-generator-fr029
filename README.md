# L3 Generator — hồ sơ yêu cầu, chờ Scope Gate lần 2

Công cụ đọc source Python/FastAPI và sinh tài liệu kiến trúc ở mức component: L3 Markdown, sơ đồ và JSON. Phân tích tĩnh trích dữ kiện code kèm vị trí. Mô hình ngôn ngữ đề xuất component và quan hệ. Code kiểm từng đề xuất với dữ kiện trước khi công bố.

**Trạng thái:** chưa có baseline được duyệt. Candidate `BL-r1` của [CHG-L3GEN-2026-002](.aide/lifecycle/change-sets/CHG-L3GEN-2026-002/change-set.yaml) chờ Hoàng review và Khiêm ký. Chưa có code sản phẩm trên nhánh này, chưa có kết quả đo.

1. [PRD revision 25](.aide/product/prd/PRD-L3GEN-2609-001.md): mục tiêu, phạm vi, luồng, lịch và phê duyệt.
2. [Change Set View](.aide/generated/change-set-views/CSV-CHG-L3GEN-2026-002.md): 8 FR, 31 AC, 5 NFR; không còn câu hỏi mở.
3. [Hướng dẫn review](docs/PRD-REVIEW-README.md): đọc gì, kiểm gì.

Nguồn PRD/FR/NFR thắng bản tổng hợp. Tài liệu khác ở gốc repo và trong `docs/` chỉ để tham khảo.

**Lịch sử.** Scope Gate lần 1 duyệt ngày 18/09/2026 trên BL-r14 của CHG-L3GEN-2026-001 (18 FR, 84 AC, 11 NFR). Ngày 22/09 mentor đổi hướng sang dùng mô hình ngôn ngữ, nên bộ đó đã superseded. Approval cũ giữ nguyên trong `.aide/evidence/`; FR/NFR cũ ở `.aide/requirements/_superseded-r23/`.
