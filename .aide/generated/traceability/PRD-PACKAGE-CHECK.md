# Kiểm tra bộ PRD

> **LỖI THỜI — kết quả dưới đây ứng với BL-r7, chưa chạy lại theo BL-r8.**
> Sau lần chạy này, hồ sơ đã thêm NFR-L3GEN-ABST-001 và ADR-2026-001, và bump revision của
> PRD, FR-006, FR-007, FR-008, FR-011, FR-013, FR-017, NFR-COMP-001, NFR-PERF-001,
> NFR-PRIV-001, OQ-001 và OQ-003. Kết luận "passed" dưới đây **không áp dụng cho trạng thái
> hiện tại**. Phải chạy lại check theo BL-r8 trước khi dùng file này làm bằng chứng.

**Local structural validation: passed (theo BL-r7, đã lỗi thời)**.

Đây là kiểm máy của tài liệu, không phải review độc lập hoặc kiểm thử sản phẩm.

**Phạm vi: môi trường soạn đầy đủ.** Số liên kết dưới đây bao gồm nguồn, cả CSV lẫn bản gộp nội bộ và hướng dẫn cho người soạn. Không dùng số này làm số liên kết của gói gửi rút gọn; gói gửi cần được kiểm riêng sau khi chọn file.

| Hạng mục | Số lượng |
|---|---|
| normative_documents | 37 |
| fr | 17 |
| ac | 69 |
| nfr | 10 |
| oq | 6 |
| links_checked | 840 |

## Phạm vi đã kiểm

YAML frontmatter, UID/key không trùng, FR có AC và Given/When/Then, liên kết GOAL/NFR/OBS/OQ, đối chiếu hai chiều FR/NFR, danh sách NFR của từng AC hợp lệ và nằm trong phạm vi FR, PRD I–IX, bốn user flows với participant đã khai, CSV bảy mục, file links, source/brief snapshot hashes, Change Set trỏ đúng candidate, candidate baseline và view khớp nguồn. Đây không phải kiểm ý nghĩa đầy đủ của từng liên kết.

## Kết quả chưa được phép gọi là đạt

- Helper chỉ kiểm bản nháp: có kiểm các ID FR/NFR ghi tường minh ở dòng Blocking của OQ; chưa suy toàn bộ blocker từ văn xuôi hoặc kiểm registry. snapshot không ghi đè candidate; render kiểm nguồn theo hash/revision của candidate đã chọn.
- snapshot/render từ chối ghi khi có file trong evidence/reviews hoặc evidence/approvals. Đây là giới hạn bảo thủ của helper trước review, không phải engine review-freeze/gate chính thức.
- Official registry / check-sdlc: **not_run** (thiếu registry/PROC/tooling chính thức).
- Intake / graph impact: **not_run**; tier còn là đề xuất. Ghi chú intake thủ công không thay báo cáo impact.
- Independent review / Scope Gate: **not_run**; chưa có reviewer receipt/approval.
- AC→implementation_target / validated_by: **pending_design_planning** cho 69 AC; chưa đủ điều kiện code.
- Product tests, benchmark, runtime/visual Mermaid rendering, accessibility và UAT: **not_run**. Mermaid trong PRD chỉ được kiểm fence và cấu trúc văn bản, chưa xác nhận renderer.
- OQ blocking còn mở; owners theo vai và ngày dự kiến chưa phải cam kết của cá nhân.
- Hash là SHA-256 toàn file của helper nội bộ; chưa thay thế hash-artifact/captured_against của tổ chức.

Không phát hiện lỗi trong phạm vi kiểm đã nêu. Các trạng thái pending/not_run ở trên vẫn còn.

## Kiểm riêng gói gửi mentor — BL-r7

**Kết quả: passed.** Đây là kiểm độc lập trên tập file đã chọn để gửi, không phải review độc lập bởi người khác.

| Phạm vi | Kết quả |
|---|---|
| File tài liệu/cấu hình | 55; không có code hoặc script |
| Tài liệu trong candidate | 37 hash khớp BL-r7 và nguồn |
| Liên kết nội bộ trong hồ sơ và README | 506; không phụ thuộc file ngoài gói |
| Change Set View | Khớp bản sinh từ nguồn |
| Nguồn mentor và evidence | Giữ nguyên byte so với môi trường soạn |

Con số 840 ở phần trên thuộc môi trường soạn đầy đủ; 506 ở bảng này thuộc gói gửi rút gọn. Phép kiểm liên kết của gói không kiểm URL ngoài, anchor trong trang hoặc các đường dẫn minh họa trong đề bài/quy trình gốc. Chưa kiểm hiển thị trực tiếp trên GitLab hoặc render Mermaid. Các trạng thái not_run và câu hỏi mở nêu trên vẫn áp dụng.
