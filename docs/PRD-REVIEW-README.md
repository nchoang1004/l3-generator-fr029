# Hướng dẫn review PRD L3 Generator

**Candidate BL-r3 của CHG-L3GEN-2026-002 chờ Scope Gate. Chưa approved, chưa có kết quả nghiệm thu sản phẩm.**

Change Set này thay CHG-L3GEN-2026-001, vốn đã qua Scope Gate ngày 18/09/2026 trên BL-r14. Lý do đổi: ngày 22/09 mentor hướng dẫn dùng mô hình ngôn ngữ để đề xuất quan hệ kiến trúc, xem [CR-L3GEN-2026-002](../.aide/evidence/requests/CR-L3GEN-2026-002.yaml). Approval cũ giữ nguyên làm lịch sử, không sửa.

## Thứ tự đọc

1. [PRD revision 27](../.aide/product/prd/PRD-L3GEN-2609-001.md).
2. [Change Set View](../.aide/generated/change-set-views/CSV-CHG-L3GEN-2026-002.md): 9 FR, 36 AC, 5 NFR.
3. [Báo cáo kiểm cấu trúc](../.aide/generated/traceability/PRD-PACKAGE-CHECK.md).

Góp ý bằng mã FR/AC/NFR/OQ. Nguồn thắng bản tổng hợp; không sửa bản tổng hợp bằng tay.

## Điểm cần reviewer xác nhận

| Điểm | Ở đâu | Ghi chú |
|---|---|---|
| Code chia component; model đặt tên, mô tả, đề xuất cạnh bổ sung; repository phẳng thì model chia | FR-L3GEN-022 | Học từ CodeBoarding. Cạnh model đề xuất chỉ được giữ khi có dữ kiện ở cả hai đầu (AC-L3GEN-022-02) |
| L3 là contract API/TBL/EVT, định dạng `tech-specs/` của mentor | FR-L3GEN-027, AC-L3GEN-021-05 | Sơ đồ component là mức L2 |
| Model đọc thêm code qua công cụ, ≤ 6 lần mỗi phạm vi, ≤ 60 dòng mỗi lần | NFR-L3GEN-AI-002, SEC-002 | `gpt-oss-120b` gọi công cụ được không: chưa kiểm |
| Hai model chia theo việc: Groq `gpt-oss-120b` đọc code, đặt tên, mô tả; Google `gemini-3.5-flash` đề xuất cạnh bổ sung, chia nhóm khi repo phẳng | [OQ-L3GEN-008](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/OQ-L3GEN-008.md), NFR-L3GEN-AI-002 | Khiêm chọn sau khi thử 4 model; Gemini miễn phí chỉ 20 request/ngày |
| Trần mỗi lần chạy: 100.000 token, 6.000 token mỗi request, 40 request, toàn bộ lần chạy 30 phút | NFR-L3GEN-AI-002, NFR-L3GEN-OPS-001 | Suy từ giới hạn gói, chưa đo trên repo thật |
| Ngưỡng 80% cho mọi nhóm; `exact` sai ≤ 5% | [OQ-L3GEN-007](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/OQ-L3GEN-007.md), NFR-L3GEN-ACC-002 | Chốt ngày 22/09 |
| Mỗi cấu hình đo 1 lần | OBS-L3GEN-001 | Không biết được mức dao động; báo cáo phải ghi giới hạn này |
| Mọi yêu cầu mang key mới | PRD mục IV.3, IV.4 | FR-019 đến 027; không dùng lại FR-001 đến 018 |

## Công cụ kiểm

Script trong repo, không phải công cụ `aide` chính thức. Trên Windows đặt `PYTHONIOENCODING=utf-8` trước khi chạy để in được tiếng Việt.

```powershell
py -3.12 scripts/prd_package.py check  --change-set CHG-L3GEN-2026-002 --baseline BL-r3.yaml
py -3.12 scripts/prd_package.py render --change-set CHG-L3GEN-2026-002 --baseline BL-r3.yaml
py -3.12 scripts/impact.py --change-set CHG-L3GEN-2026-002 --baseline BL-r3.yaml
py -3.12 scripts/l1_coverage.py
```

`check` kiểm hash, revision, key và UID; không kiểm nội dung đúng hay sai. Sửa một artifact trong baseline thì phải tạo candidate mới (BL-r4), không ghi đè BL-r3. Sau khi có review hoặc approval, `render` từ chối ghi đè view.

[Quy trình mentor](agentic-sdlc-execution-guide.md) và [nguồn](sdlc-sources/) giữ nguyên để đối chiếu.
