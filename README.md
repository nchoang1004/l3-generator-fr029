# L3 Generator — Hồ sơ PRD để mentor review

L3 Generator phân tích source repository để tạo mô hình và tài liệu kiến trúc L3 ban đầu.
Người đọc có thể truy các kết luận về bằng chứng trong source.

**Bản nháp full product · Candidate BL-r12 · Chưa qua Scope Gate.**
Gói này chỉ chứa tài liệu; chưa có code sản phẩm hoặc kết quả nghiệm thu.

## Bắt đầu tại đây

| Thứ tự | Mở tài liệu | Cần review |
|---|---|---|
| 1 | [PRD — mục tiêu, phạm vi và luồng](.aide/product/prd/PRD-L3GEN-2609-001.md) | Sản phẩm làm gì, cho ai, phần nào thuộc đề bài và phần nào là đề xuất |
| 2 | [Change Set View — FR/AC, NFR và câu hỏi mở](.aide/generated/change-set-views/CSV-CHG-L3GEN-2026-001.md) | Mục 3: hành vi/tiêu chí chấp nhận; mục 6: chất lượng; mục 7: quyết định còn thiếu |

**Không cần đọc lại từng file nguồn.** Chúng được giữ để góp ý và quản lý từng yêu cầu theo quy trình mentor.
Khi có bất đồng, PRD/FR/NFR nguồn thắng bản tổng hợp.

## Nhờ mentor chốt

Phạm vi và lịch giao; stack hỗ trợ; ngưỡng chất lượng và dataset; môi trường web/dữ liệu/AI;
người chịu trách nhiệm và cách áp dụng các gate. [Sáu câu hỏi cụ thể và người xử lý đề xuất](docs/PRD-REVIEW-README.md).

Góp ý nên ghi mã liên quan, ví dụ `AC-L3GEN-008-01` hoặc `OQ-L3GEN-002`, cùng điểm cần sửa.
Hiện chưa hoàn tất intake/impact và chưa có quyết định phê duyệt; upload tài liệu không đồng nghĩa qua gate.

## Chỉ mở khi cần đối chiếu

- [Kết quả kiểm cấu trúc và giới hạn](.aide/generated/traceability/PRD-PACKAGE-CHECK.md).
- [Quy trình mentor](docs/agentic-sdlc-execution-guide.md) và [tài liệu nguồn](docs/sdlc-sources/).
- [Candidate hiện tại](.aide/lifecycle/change-sets/CHG-L3GEN-2026-001/baseline/BL-r12.yaml) chứa revision/hash của bộ hồ sơ.

Bản gộp thứ hai và baseline cũ không nằm trong gói review này; lịch sử cũ vẫn được giữ để tra cứu.
