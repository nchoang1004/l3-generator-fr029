---
uid: "01M2J06Z3X86Z4VPQF6ZNKY1QT"
key: "OBS-L3GEN-001"
type: "observability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 6
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"measures":["KPI-L3GEN-006","KPI-L3GEN-007","KPI-L3GEN-008","KPI-L3GEN-009","KPI-L3GEN-010"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# Phương pháp đo chất lượng kết quả

## Phạm vi

Tài liệu này quy định cách đo năm KPI ở PRD mục II.4. Ngưỡng nằm trong NFR; OBS chỉ định nghĩa dữ liệu, cách tính và cỡ mẫu. Kết quả hiện tại: **not_run**.

Revision 5 (23/09/2026) viết lại cho PRD revision 25: đo KPI-L3GEN-006 đến 010 thay cho KPI-001 đến 005 cũ. Revision 6 (23/09/2026): đo 1 lần mỗi cấu hình; bỏ so sánh với bộ luật tĩnh cũ. Không dùng số test hay benchmark của code cũ làm bằng chứng đạt PRD.

## Dataset và đáp án

- Trước lần đo đầu, chọn ít nhất 3 repo Python/FastAPI public, cấu trúc khác nhau: app đơn giản, app factory hoặc chia tầng, monorepo. Ghi quyền sử dụng và pin commit hoặc digest. Chưa có danh sách thật thì trạng thái là `not_run`; không tạo tên hoặc SHA giả.
- Khiêm và Hoàng lập hai đáp án độc lập, **trước khi xem output**: route, request/response model, entity/table, HTTP, config, event, thư viện, thành viên component và cạnh dependency. Giữ cả hai bản, ghi chỗ bất đồng và bản đã đối chiếu.
- Tách repo dùng để viết prompt khỏi repo dùng để đo. Repo đã dùng để chỉnh prompt không được tính vào kết quả.
- Không lấy output của công cụ làm đáp án. Ghi phạm vi file trước khi chạy; mọi phần loại trừ phải có lý do.
- Cỡ mẫu tối thiểu để báo tỷ lệ: route ≥ 100, entity ≥ 20, HTTP ≥ 30, config ≥ 30, event ≥ 20, thành viên component ≥ 30, cạnh dependency ≥ 20. Chưa đủ thì báo TP/FP/FN và `not_evaluated`.
- Có bộ fixture nhỏ cho từng mẫu trong AC, kèm ca âm: tên giống route nhưng không phải route, mount, prefix động, tên bảng sinh lúc chạy, config chứa bí mật, lời gọi không xác định được đích.

## Cách tính từng KPI

| KPI | Cách tính | Ai chấm |
|---|---|---|
| KPI-L3GEN-006 — độ đúng sơ đồ cấu trúc | Precision và recall của cặp (component, thành viên) và của cạnh (đầu, cuối, loại) so với đáp án. Ghép một-một | Máy so với đáp án người lập |
| KPI-L3GEN-007 — độ đúng bằng chứng | Số kết luận công bố có bằng chứng hợp lệ theo NFR-L3GEN-ACC-002, chia cho tổng kết luận công bố | Máy, trên mọi lần chạy |
| KPI-L3GEN-008 — độ đúng dữ kiện L3 | Precision và recall riêng từng loại: route, request/response model, entity/table, HTTP, config, event, thư viện. Chấm thuộc tính riêng: route thiếu prefix không tính là route đúng | Máy so với đáp án người lập |
| KPI-L3GEN-009 — nhãn mức chắc chắn | Tỷ lệ nhãn `exact`/`inferred`/`unresolved` khớp đáp án; riêng tỷ lệ kết luận gán `exact` mà thật ra sai | Người chấm theo đáp án |
| KPI-L3GEN-010 — tự báo phần không đọc được | Số ca cài sẵn trong fixture (file lỗi cú pháp, file ngoài phạm vi hỗ trợ, quan hệ không xác định đích) xuất hiện ở mục giới hạn, chia cho tổng số ca đã cài. Mẫu số lấy từ fixture, không lấy từ output | Máy |

Công thức chung: precision = TP/(TP+FP); recall = TP/(TP+FN). Mẫu số bằng 0 thì `not_evaluated`, không ghi 100%. Với kết quả partial, chấm phần đã biết và việc nêu phần thiếu; không tính giá trị chưa biết là đã giải đúng.

## Số lần chạy

- Một cấu hình gồm: snapshot, provider và model, phiên bản prompt, phiên bản tool. Mỗi cấu hình đo **1 lần**.
- Lần chạy dùng để đo là lần đầu tiên sau khi khóa cấu hình. Chạy lại vì lỗi hạ tầng (mất mạng, hết quota) thì ghi lý do; không chạy lại chỉ vì kết quả xấu.
- Mỗi lần chạy ghi provenance theo NFR-L3GEN-AI-002.
- Model không cho cùng kết quả mỗi lần, nên số đo 1 lần chưa cho biết mức dao động. Báo cáo ghi rõ giới hạn này.

## Thời gian và tài nguyên

Mỗi lần chạy ghi: digest snapshot, commit nếu có, phiên bản tool, hệ điều hành, interpreter, phần cứng, loại đầu vào, thời gian từng chặng (lấy source, phân tích tĩnh, gọi model, sinh artifact), số request và token, bộ nhớ đỉnh, kích thước output và trạng thái cuối. NFR-L3GEN-OPS-001 và NFR-L3GEN-AI-002 giữ ngưỡng.

## Lưu bằng chứng

Mỗi lần đo lưu ở `.aide/evidence/tests/<run-id>/`, chỉ thêm, không ghi đè. Có hash đầu vào, kết quả passed/failed/not_run và số đếm thô. Không lưu khóa API hoặc bí mật. Sửa đáp án sau khi đo phải có revision và lý do; không xóa kết quả cũ.
