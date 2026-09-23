# Hướng dẫn review PRD L3 Generator

**Candidate BL-r1 của CHG-L3GEN-2026-002 chờ Scope Gate. Chưa approved, chưa có kết quả nghiệm thu sản phẩm.**

Change Set này thay CHG-L3GEN-2026-001, vốn đã qua Scope Gate ngày 18/09/2026 trên BL-r14. Lý do đổi: ngày 22/09 mentor hướng dẫn dùng mô hình ngôn ngữ để đề xuất quan hệ kiến trúc, xem [CR-L3GEN-2026-002](../.aide/evidence/requests/CR-L3GEN-2026-002.yaml). Approval cũ giữ nguyên làm lịch sử, không sửa.

## Thứ tự đọc

1. [PRD revision 25](../.aide/product/prd/PRD-L3GEN-2609-001.md).
2. [Change Set View](../.aide/generated/change-set-views/CSV-CHG-L3GEN-2026-002.md): 8 FR, 31 AC, 5 NFR.
3. [Báo cáo kiểm cấu trúc](../.aide/generated/traceability/PRD-PACKAGE-CHECK.md).

Góp ý bằng mã FR/AC/NFR/OQ. Nguồn thắng bản tổng hợp; không sửa bản tổng hợp bằng tay.

## Điểm cần reviewer xác nhận

| Điểm | Ở đâu | Ghi chú |
|---|---|---|
| Model chỉ đề xuất; cạnh chỉ được giữ khi có dữ kiện đã xác định đích nối đúng hai đầu | AC-L3GEN-022-02, NFR-L3GEN-ACC-002 | Đây là cách giữ yêu cầu "chứng minh bằng source" của đề bài mục 3.6 |
| Groq, `openai/gpt-oss-120b`, gói miễn phí | [OQ-L3GEN-008](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/OQ-L3GEN-008.md) | Agent chọn theo yêu cầu của Khiêm; Khiêm xác nhận khi ký |
| Trần mỗi lần chạy: 100.000 token, 6.000 token mỗi request, 40 request, toàn bộ lần chạy 30 phút | NFR-L3GEN-AI-002, NFR-L3GEN-OPS-001 | Suy từ giới hạn gói, chưa đo trên repo thật |
| Ngưỡng 80% cho mọi nhóm; `exact` sai ≤ 5% | [OQ-L3GEN-007](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/OQ-L3GEN-007.md), NFR-L3GEN-ACC-002 | Chốt ngày 22/09 |
| Mỗi cấu hình đo 3 lần, báo giá trị thấp nhất | OBS-L3GEN-001 | Vì model không cho cùng kết quả mỗi lần |
| Mọi yêu cầu mang key mới | PRD mục IV.3, IV.4 | FR-019 đến 026; không dùng lại FR-001 đến 018 |

## Công cụ kiểm

Script trong repo, không phải công cụ `aide` chính thức. Trên Windows đặt `PYTHONIOENCODING=utf-8` trước khi chạy để in được tiếng Việt.

```powershell
py -3.12 scripts/prd_package.py check  --change-set CHG-L3GEN-2026-002 --baseline BL-r1.yaml
py -3.12 scripts/prd_package.py render --change-set CHG-L3GEN-2026-002 --baseline BL-r1.yaml
py -3.12 scripts/impact.py --change-set CHG-L3GEN-2026-002 --baseline BL-r1.yaml
```

`check` kiểm hash, revision, key và UID; không kiểm nội dung đúng hay sai. Sửa một artifact trong baseline thì phải tạo candidate mới (BL-r2), không ghi đè BL-r1. Sau khi có review hoặc approval, `render` từ chối ghi đè view.

[Quy trình mentor](agentic-sdlc-execution-guide.md) và [nguồn](sdlc-sources/) giữ nguyên để đối chiếu.
