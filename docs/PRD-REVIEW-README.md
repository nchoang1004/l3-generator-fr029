# Hướng dẫn review PRD L3 Generator

**Trạng thái: bản nháp full product, candidate BL-r12; chưa qua Scope Gate.**

> **Change Set View đã render lại theo BL-r12.** `scripts/prd_package.py` nay có trong repo; chạy `render` rồi `check` sau mỗi lần đổi nguồn. Báo cáo kiểm gói trong `generated/traceability/` vẫn là bản cũ, chưa render lại.
Code hiện có không quyết định phạm vi hoặc chứng minh yêu cầu đã đạt.

## Mentor đọc gì?

| Thứ tự | Tài liệu | Nội dung cần xem |
|---|---|---|
| 1 | [PRD](../.aide/product/prd/PRD-L3GEN-2609-001.md) | I: nguồn yêu cầu và đề xuất; II–IV: mục tiêu/phạm vi; V: luồng; VIII–IX: lịch và quyết định |
| 2 | [Change Set View](../.aide/generated/change-set-views/CSV-CHG-L3GEN-2026-001.md) | Mục 3: toàn bộ 18 FR/83 AC; mục 6: 11 NFR; mục 7: 5 câu hỏi còn mở |
| Khi cần | [Kiểm tra cấu trúc](../.aide/generated/traceability/PRD-PACKAGE-CHECK.md) | Phần đã kiểm và giới hạn; không phải bằng chứng sản phẩm đạt |

Không cần mở từng FR/NFR để đọc lại. Change Set View được sinh từ nguồn;
khi có bất đồng, PRD/FR/NFR nguồn thắng. Góp ý nên ghi key FR/AC/NFR hoặc OQ liên quan.

## Cần chốt gì?

| Câu hỏi | Người xử lý đề xuất | Nguồn chi tiết |
|---|---|---|
| Ai chịu trách nhiệm, review và ký; mã tổ chức nào được dùng? | Người phụ trách PRD + mentor | [OQ-001](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-001.md) |
| Full scope, mức Must/Should và lịch có phù hợp năng lực nhóm? | Product + mentor | [OQ-002](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-002.md) |
| Chốt stack và các pattern/adapter hỗ trợ nào? | Tech Lead | [OQ-003](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-003.md) |
| Ngưỡng chất lượng, dataset và người lập đáp án có phù hợp? | Product + QA | [OQ-004](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-004.md) |
| Môi trường web, dữ liệu gửi/lưu và AI được phép tới đâu? | Tech Lead/Security + Product | [OQ-005](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-005.md) |
| Áp dụng tooling, registry và điều kiện từng gate thế nào? | Mentor/người phụ trách quy trình | [OQ-006](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-001/open-questions/OQ-L3GEN-006.md) |

## Phân biệt bản nháp và hồ sơ được duyệt

- Intake và impact đã chạy ở mức nhóm, tier chốt T1. Người thực hiện là Khiêm, tự nhận vai product-owner; `role_confirmed: false` cho tới khi mentor xác nhận phân vai tại OQ-L3GEN-001. `impact.yaml` dựng từ graph cục bộ bằng frontmatter, `confidence: low` — không thay việc mentor rà soát phạm vi.
- Owner theo vai và hạn trả lời OQ là đề xuất; chưa có xác nhận của cá nhân.
- Chưa có review receipt, approval hoặc kết quả nghiệm thu sản phẩm. Không approve FR còn bị OQ mở chặn.
- PRD VI và IX ghi điều kiện hoàn thành và cách ký đúng revision; không coi việc upload Git là qua Scope Gate.

## Tài liệu tham khảo

- [Quy trình mentor đã ghép](agentic-sdlc-execution-guide.md), [mẫu PRD](sdlc-sources/05-prd-template.md), [đề bài mục 3.6](sdlc-sources/06-project-brief.md).
- [Nguồn yêu cầu](../.aide/evidence/requests/CR-L3GEN-2026-001.yaml), [bổ sung truy nguồn](../.aide/evidence/requests/CR-L3GEN-2026-001-sources-01.yaml), [manifest nguồn mentor](sdlc-sources/manifest.json).
- [BL-r12](../.aide/lifecycle/change-sets/CHG-L3GEN-2026-001/baseline/BL-r12.yaml) xác định tập revision đang review. Baseline cũ giữ lại để tra cứu, không đưa vào gói review mới.

Các file nguồn mentor giữ nguyên để đối chiếu, không phải nội dung phải đọc lại trong lần review này.

<details>
<summary>Dành cho người soạn: quy trình và công cụ kiểm</summary>

Theo A.2, mỗi artifact một file, AC nằm trong FR và evidence append-only. Theo D.1b,
Change Set View bảy mục là bản dùng để review; không thay bằng một PRD gộp có thể sửa độc lập.
Giữ glossary và OBS vì AC/KPI tham chiếu tới chúng.

Trước Scope Gate: CR → intake/impact/tier → rà FR/NFR → candidate mới → kiểm hồ sơ →
commit → review đúng revision. `impact.yaml` sinh từ graph, không viết tay. Theo B.3,
cần CR, touches, stale_artifacts, affected_teams, external_consumers, risk_signals,
path_signals, tier, flow, confidence và `skipped_with_reason` không rỗng. Bản hiện tại do
`scripts/impact.py` sinh từ graph cục bộ dựng bằng frontmatter trong `.aide/`, không phải
metadata graph tập trung; bốn giới hạn đã khai ở `skipped_with_reason` và `confidence` ghi
`local-frontmatter-only`. Cách áp dụng khi thiếu tooling chính thức vẫn xử lý tại OQ-006.

PROC/registry chính thức chưa đầy đủ. Mẫu DoD yêu cầu mapping triển khai trong khi thiết kế/planning
nằm sau Scope Gate; cách áp dụng đang ở OQ-006. Mảng mapping rỗng không phải được miễn.
Sau Scope Gate mới thực hiện các bước domain, thiết kế, contracts và planning theo dependency.

Các script chỉ có trong môi trường soạn, không nằm trong gói tài liệu gửi mentor.
Cần Python 3.12 và PyYAML:

```powershell
py -3.12 scripts/prd_package.py check  --baseline BL-r12.yaml
py -3.12 scripts/prd_package.py render --baseline BL-r12.yaml
py -3.12 scripts/impact.py --baseline BL-r12.yaml
```

Sửa nguồn thì tăng revision artifact đổi nội dung và chọn candidate mới (r8 trở đi).
Không sửa tay view hoặc ghi đè baseline cũ. Snapshot/render từ chối ghi khi có file trong
`evidence/reviews/` hoặc `evidence/approvals/`; khi đó dùng quy trình re-review chính thức,
không xóa evidence để vượt kiểm. Helper không cấp approval hoặc tự commit/push.

</details>
