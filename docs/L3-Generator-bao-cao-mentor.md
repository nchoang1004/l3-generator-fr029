# L3 Generator — Báo cáo tiến độ

Ngày 02/10/2026. Người báo cáo: Hoàng (phần L3 và web). Phần sơ đồ khối do Khiêm báo cáo chi tiết.
Đối chiếu với PRD-L3GEN-2609-001 revision 29 (bản nháp, Scope Gate chưa ký).

## 1. Tóm tắt

| Hạng mục | Tiến độ |
|---|---|
| Tiêu chí nghiệm thu (AC) | 23/36 đạt, 13/36 một phần, 0/36 chưa có code |
| Mốc | M1 gần xong; M2 một phần; M3 chưa làm |
| KPI | Chưa nghiệm thu. KPI-007 đo trên repo dev 4.400/4.400; các KPI khác chưa đủ mẫu hoặc chưa đo |
| Code | Đã đẩy lên GitLab, nhánh `feature/l3-slice`, chờ Merge Request |

"Đạt" = có code, có test tự động, chạy đúng trên 4 repo phát triển. Chưa phải nghiệm thu theo PRD mục VI.

## 2. Mục tiêu kinh doanh và tiến độ đo

Chép nguyên văn PRD mục II.3 "Mục tiêu kinh doanh" (dòng 120–129):

Bốn mục tiêu, xếp theo thứ tự: sinh ra được gì, rồi mới tới tin được tới đâu.

| Goal key | Mục tiêu | Liên kết KPI |
|---|---|---|
| GOAL-L3GEN-004 | Dựng được sơ đồ cấu trúc hệ thống ở mức application/component, phản ánh code đang chạy chứ không phải tài liệu cũ | KPI-L3GEN-006 |
| GOAL-L3GEN-005 | Mọi kết luận trên sơ đồ và tài liệu đều lần ngược được về đúng đoạn source sinh ra nó, để người đọc tự kiểm chứng thay vì phải tin | KPI-L3GEN-007 |
| GOAL-L3GEN-006 | Từ repo đó sinh ra tài liệu L3 đủ để người mới đọc hiểu hệ thống mà không cần mở source | KPI-L3GEN-008 |
| GOAL-L3GEN-007 | Nói thật về giới hạn của chính mình: tách rõ phần đọc trực tiếp từ bằng chứng, phần suy ra, và phần không kết luận được, để người đọc biết chỗ nào tin ngay và chỗ nào phải tự kiểm | KPI-L3GEN-009, KPI-L3GEN-010 |

Tiến độ đo các KPI (PRD mục II.4; timeline: trước nghiệm thu M3):

| KPI | Tên trong PRD | Target | Hiện trạng |
|---|---|---|---|
| KPI-L3GEN-006 | Độ đúng sơ đồ cấu trúc | Đạt NFR-L3GEN-ACC-002 với mẫu đủ | Chưa đo theo KPI. Khiêm đo theo tiêu chí riêng: repo nhỏ đạt, repo lớn chưa |
| KPI-L3GEN-007 | Độ đúng bằng chứng | 100%, không ngoại lệ | 4.400/4.400 trên 4 repo dev |
| KPI-L3GEN-008 | Độ đúng dữ kiện L3 | Đạt NFR-L3GEN-ACC-002 | Route 58/58 trên 4 repo dev; chưa đủ mẫu (58/100 route, 5/20 bảng, 0/20 sự kiện) → `not_evaluated` |
| KPI-L3GEN-009 | Nhãn mức chắc chắn có đúng không | Đạt ngưỡng NFR-L3GEN-ACC-002 với mẫu đủ | Chưa đo. Revision 29 sửa cách đo (chờ Khiêm duyệt) |
| KPI-L3GEN-010 | Công cụ có tự báo phần nó không đọc được không | 100% | Một phần: đã khai file lỗi cú pháp, Celery, bảng trong migration, lời gọi chưa nối. Còn thiếu: lời gọi qua thư viện ngoài chưa hỗ trợ |

## 3. Tiến độ theo tính năng (PRD mục IV.3)

| FR | Tên trong PRD | Mốc | Đạt / một phần | Còn lại |
|---|---|---|---|---|
| FR-L3GEN-019 | Nhận source và chạy phân tích | M1 cho CLI; M2 cho web | 4 / 1 | GitHub: có code, đang tắt chờ review bảo mật |
| FR-L3GEN-020 | Xác định phạm vi phân tích | M1 | 0 / 3 | Mới một đơn vị phân tích mỗi repo |
| FR-L3GEN-021 | Trích dữ kiện code | M1 bốn loại đầu; M3 ba loại sau | 4 / 1 | Lời gọi HTTP chưa kiểm trên repo thật |
| FR-L3GEN-022 | Dựng component và quan hệ kiến trúc (Khiêm) | M2 | 1 / 4 | Chưa chốt cách chia (D-03); bước model chưa chạy thật trong code sản phẩm |
| FR-L3GEN-023 | Bằng chứng và nhãn mức chắc chắn | M1 | 4 / 0 | |
| FR-L3GEN-024 | Công bố giới hạn của lần chạy | M1 | 3 / 1 | Middleware, DI container, thư viện ngoài chưa khai |
| FR-L3GEN-025 | Xuất kết quả | M1; M2 khi có component | 4 / 0 | |
| FR-L3GEN-026 | Khám phá kết quả trên web | M2 | 2 / 1 | Góc nhìn component tạm ẩn chờ D-03 |
| FR-L3GEN-027 | Sinh tài liệu L3 contract | M1 API, TBL; M3 EVT | 1 / 2 | Chưa có DDL; EVT mới thử trên mẫu Kafka |
| **Tổng** | | | **23 / 13** | |

## 4. Tiến độ theo mốc (PRD mục VIII)

| Mốc | Hiện trạng |
|---|---|
| M0 — Chốt yêu cầu | Chưa xong: PRD còn nháp, Scope Gate chưa ký, các mốc chưa có ngày |
| M1 — Lõi phân tích và dòng lệnh | Gần xong. Còn FR-020 và DDL của FR-027 |
| M2 — Dựng mô hình kiến trúc và web | Một phần. Web xong phần L3; dựng component chưa chốt cách chia |
| M3 — Hoàn thiện dữ kiện và nghiệm thu | Chưa làm. Config, thư viện đã có; sự kiện mới Kafka trên mẫu; chưa đo 5 KPI |

## 5. Số đo hiện có

Đo ngày 02/10/2026 trên 4 repo phát triển, máy dev.

| Repo | Route | Bảng | Bằng chứng |
|---|---:|---:|---:|
| rhoboro | 11 | 2 | 689 |
| fullstack | 23 | 2 | 1.378 |
| realworld | 19 | 0 (7 bảng chỉ trong migration, đã khai giới hạn) | 1.437 |
| teamhide | 5 | 1 | 896 |
| **Tổng** | **58** | **5** | **4.400** |

- Route khớp đáp án đếm tay: 58/58. Bằng chứng qua bước tự kiểm: 4.400/4.400.
- Test tự động: 177/177 qua. Kiểm contract: qua.
- Thời gian phân tích: 0,4–0,6 giây mỗi repo; bộ nhớ dưới 60 MB (chưa đo trên máy chuẩn của NFR-L3GEN-OPS-001).
- Giới hạn: repo dev, đã dùng để sửa lỗi; đáp án do nhóm tự lập.

Phần sơ đồ (Khiêm, nguồn `docs/HANDOFF.md` ngày 01/10, tiêu chí riêng P ≥ 0,8, R ≥ 0,6): 4 repo nhỏ và kibo đạt; boilerplate chưa (P 0,62); lnbits, fba chưa. teamhide: tất cả cạnh P 0,90 / R 0,82; cạnh giữa khối R 0,75.

## 6. Chưa làm

| Việc | Liên quan PRD |
|---|---|
| Nhiều đơn vị phân tích trong một repo | FR-020 |
| Khối DDL trong file TBL | AC-027-02 |
| Response dạng `list[Model]` | AC-021-05 |
| Auth (hiện luôn `unknown`) | AC-027-01, contract API-L3GEN-008 |
| Khai giới hạn cho lời gọi qua thư viện ngoài chưa hỗ trợ | KPI-010 |
| Lấy source từ GitHub (đang tắt) | AC-019-05 |
| Gọi provider model thật | FR-022, NFR-L3GEN-AI-002 |

## 7. Vướng mắc cần mentor góp ý

| # | Vướng mắc | Liên quan PRD | Cần |
|---|---|---|---|
| 1 | Chưa chốt cách chia component (D-03); PRD rev 26 và contract API-L3GEN-005 ghi khác nhau | FR-022, GOAL-004 | Góp ý tiêu chí chọn |
| 2 | Chưa có tài khoản model miễn phí; thí nghiệm dùng dịch vụ trả phí | Mục III.3, NFR-L3GEN-AI-002 | Quyết định giữ trần 0 đồng hay nới |
| 3 | Chưa có bộ dữ liệu nghiệm thu độc lập, đủ cỡ mẫu | Mục II.4, OBS-L3GEN-001 | Gợi ý nguồn repo và người chấm |
| 4 | Scope Gate chưa ký, mốc chưa có ngày | Mục VIII, IX | Nhóm hoàn tất trong tuần |
| 5 | Phần L3 và phần sơ đồ chưa nối | AC-025-04 | Nhóm nối qua file membership |

## 8. Kế hoạch tiếp theo

| # | Việc | Người | Xong khi |
|---|---|---|---|
| 1 | Duyệt PRD rev 29, ký Scope Gate, ghi ngày M1–M3 | Khiêm | PRD mục IX có chữ ký và ngày |
| 2 | Chốt cách chia component | Khiêm, Hoàng | Có bảng so sánh và phương án được chọn |
| 3 | Có model miễn phí hoặc quyết định mới về chi phí | Khiêm | Có số đo với cấu hình đúng PRD |
| 4 | Nối phần L3 với phần sơ đồ | Hoàng | Một lần chạy ra cả sơ đồ và tài liệu L3 đúng component |
| 5 | Bộ repo nghiệm thu, chấm chéo, đo 5 KPI | Khiêm, Hoàng | Có số đo, hết `not_evaluated` |
| 6 | Bổ sung L3: FR-020, DDL, `list[Model]`, khai giới hạn thư viện ngoài | Hoàng | Có test mới, chạy lại 4 repo |

## 9. Nơi xem

- Code: GitLab, nhánh `feature/l3-slice`, thư mục `slice/`.
- PRD, FR, NFR: `.aide/product/prd/`, `.aide/requirements/`. Contract: `.aide/tech-specs/`.
- Demo web: `python -m l3slice.web --workdir <thư mục> --port 8765 --demo-partition` trong `slice/`, mở http://127.0.0.1:8765/.

## Phụ lục: trạng thái 36 AC

| AC | Trạng thái | Bằng chứng |
|---|---|---|
| 019-01 | Đạt | Dòng lệnh chạy 4 repo, mỗi repo 5–7 file |
| 019-02 | Đạt | Đầu vào hỏng: dừng, không tạo output |
| 019-03 | Đạt | `test_cli_exit_codes` |
| 019-04 | Đạt | ZIP hỏng bị từ chối kèm lý do |
| 019-05 | Một phần | Test với kết nối giả; tính năng đang tắt |
| 020-01 | Một phần | Có danh sách phần đã xét và bị bỏ; mới một đơn vị |
| 020-02 | Một phần | Có trạng thái riêng; chưa có test riêng |
| 020-03 | Một phần | Ghi mức `partial` cho Python/FastAPI |
| 021-01 | Đạt | Route 58/58 |
| 021-02 | Đạt | teamhide 9/9 cột |
| 021-03 | Một phần | Che bí mật có; HTTP chưa kiểm trên repo thật |
| 021-04 | Đạt | Giới hạn `REFERENCE_UNRESOLVED` |
| 021-05 | Đạt | Mục Model; ngoại lệ `list[Model]` |
| 022-01 | Một phần | Có kiểm membership; model chưa chạy thật |
| 022-02 | Một phần | Test với model giả |
| 022-03 | Một phần | Test với model giả |
| 022-04 | Đạt | `test_more_than_50_nodes_rejected` |
| 022-05 | Một phần | Có code, chưa nối |
| 023-01 | Đạt | Mở bằng chứng `file:dòng` trên web |
| 023-02 | Đạt | Lý do ghi tên quy ước |
| 023-03 | Đạt | `test_open_evidence_detects_changed_file` |
| 023-04 | Đạt | 4.400/4.400 |
| 024-01 | Đạt | fullstack: `PARSE_FAILED deps.py` |
| 024-02 | Đạt | Nhóm test `Budgets` |
| 024-03 | Một phần | Celery, migration có; middleware chưa |
| 024-04 | Đạt | Trạng thái "một phần" kèm lý do |
| 025-01 | Đạt | Xuất tài liệu, sơ đồ, JSON |
| 025-02 | Đạt | Kiểm schema trên 4 repo |
| 025-03 | Đạt | `test_retry_failed_svg` |
| 025-04 | Đạt | `test_readme_and_diagram_share_nodes` |
| 026-01 | Đạt | Giai đoạn và trạng thái kèm lý do |
| 026-02 | Một phần | Góc nhìn component tạm ẩn |
| 026-03 | Đạt | Lọc và mở bằng chứng |
| 027-01 | Đạt | 58/58 operation OpenAPI hợp lệ |
| 027-02 | Một phần | Chưa có DDL |
| 027-03 | Một phần | Thử trên mẫu Kafka |
