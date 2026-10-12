# Đề xuất: làm gọn KPI-L3GEN-009

Người đề xuất: Hoàng. Người quyết: Khiêm (Product, ký Scope Gate). Ngày 02/10/2026. Trạng thái: **nháp, chưa sửa file gốc**.

## Vì sao đổi

KPI-009 hiện có hai vế:

1. Tỷ lệ nhãn `exact`/`inferred`/`unresolved` khớp đánh giá người duyệt, ngưỡng ≥ 80%.
2. Tỷ lệ gán `exact` cho kết luận sai, ngưỡng ≤ 5%. Đây là chỉ số chặn.

Vế 1 cần người ngồi chấm từng nhãn. Đáp án KPI-008 không có sẵn thông tin này. Vế 2 tính được bằng máy từ chính đáp án KPI-008: lấy các dữ kiện gắn `exact`, so với đáp án, đếm số sai.

Đề xuất: **bỏ vế 1, giữ vế 2, chấm bằng máy.**

- Giữ được mục đích của GOAL-007: chữ "exact" phải đáng tin.
- Không cần thêm người chấm.
- Ngưỡng 5% giữ nguyên, không hạ.

Mất đi: không còn số đo cho việc nhãn `inferred`/`unresolved` có gán đúng chỗ không. Luật "không nâng inferred thành exact" vẫn còn ở NFR-ACC-002 và PRD dòng 172.

## Cách tính mới

- Tập đếm: mọi dữ kiện trong output gắn nhãn `exact`, thuộc các loại KPI-008 chấm (route, request/response model, entity/table, HTTP, config, event, thư viện).
- Một dữ kiện `exact` là **sai** khi không có trong đáp án KPI-008, hoặc có nhưng sai thuộc tính đã chấm. Ví dụ: route thiếu prefix, tên bảng sai.
- Tỷ lệ = số `exact` sai / tổng số `exact`. Ngưỡng ≤ 5%.
- Cỡ mẫu: dùng cỡ mẫu tối thiểu của KPI-008 theo từng loại. Chưa đủ thì báo số đếm và `not_evaluated`.
- Ai chấm: máy so với đáp án KPI-008.

## Sửa cụ thể ở 3 file

### 1. PRD-L3GEN-2609-001 → revision 29

Dòng 141, bảng KPI, cột Giải thích:

- Cũ: `Tỷ lệ nhãn exact/inferred/unresolved khớp đánh giá người duyệt, và riêng tỷ lệ gán exact cho kết luận thật ra sai. Nghĩa các nhãn ở glossary mục 4`
- Mới: `Trong các dữ kiện gắn nhãn exact, tỷ lệ sai so với đáp án của KPI-L3GEN-008. Nghĩa các nhãn ở glossary mục 4`

Cột Target:

- Cũ: `Đạt ngưỡng NFR-L3GEN-ACC-002 với mẫu đủ`
- Mới: giữ nguyên.

Thêm dòng lịch sử:

| Revision 29 | 2026-10-0x | Khiêm + AI hỗ trợ | KPI-009 chỉ còn đo tỷ lệ `exact` sai, chấm bằng máy theo đáp án KPI-008; bỏ vế nhãn khớp người duyệt. Sửa NFR-ACC-002, OBS-001. Không đổi FR/AC |

### 2. NFR-L3GEN-ACC-002 → revision 3

Mục "Nhãn chất lượng", bỏ câu:

> Tỷ lệ nhãn khớp đánh giá người duyệt phải đạt từ 80% trở lên.

Câu sau sửa thành:

> Tỷ lệ dữ kiện gắn `exact` mà sai so với đáp án phải ở mức 5% trở xuống, và là chỉ số chặn: gán nhãn chắc chắn cho kết luận sai gây hại hơn bỏ sót, vì người đọc tin mà không kiểm lại.

### 3. OBS-L3GEN-001 → revision 7

Bảng "Cách tính từng KPI", dòng KPI-009:

| Cũ | Mới |
|---|---|
| Tỷ lệ nhãn `exact`/`inferred`/`unresolved` khớp đáp án; riêng tỷ lệ kết luận gán `exact` mà thật ra sai. Ai chấm: Người chấm theo đáp án | Số dữ kiện gắn `exact` mà không có trong đáp án KPI-008 hoặc sai thuộc tính đã chấm, chia cho tổng số dữ kiện gắn `exact`. Cỡ mẫu theo KPI-008. Ai chấm: Máy so với đáp án KPI-008 |

## Không cần sửa

- GOAL-007: vẫn liên kết KPI-009 và KPI-010.
- PRD dòng 134 ("cả năm chỉ số đều tính ra số được") và dòng 383 ("năm KPI"): vẫn đúng.
- FR, AC: không đổi.

## Cần Khiêm quyết

1. Đồng ý bỏ vế "nhãn khớp người duyệt ≥ 80%" không.
2. Nếu đồng ý: sửa trong revision 29 cùng các sửa khác, hay làm riêng.
