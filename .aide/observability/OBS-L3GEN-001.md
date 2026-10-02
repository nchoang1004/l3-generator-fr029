---
uid: "01M2J06Z3X86Z4VPQF6ZNKY1QT"
key: "OBS-L3GEN-001"
type: "observability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 9
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

Revision 5 (23/09/2026) viết lại cho PRD revision 25: đo KPI-L3GEN-006 đến 010 thay cho KPI-001 đến 005 cũ. Revision 6 (23/09/2026): đo 1 lần mỗi cấu hình; bỏ so sánh với bộ luật tĩnh cũ. Revision 7 (02/10/2026): bộ repo là các repo mẫu nhóm đã pin; đáp án và cách chấm sơ đồ theo chuẩn nhóm dùng khi phát triển; KPI-006 tính theo NFR-L3GEN-ACC-002 revision 3; KPI-008 bỏ loại HTTP. Revision 8 (02/10/2026), sửa theo review REVIEW-SCOPE-L3GEN-2026-002 và quyết định của Khiêm: chấm từng repo kín nhỏ và vừa; bỏ cỡ mẫu tối thiểu; người lập và hạn của đáp án mới; cách tính tỷ lệ mã dòng model trỏ hợp lệ; KPI-008 thêm lại HTTP; KPI-009 chỉ đo `exact` sai theo đáp án KPI-008 (đề xuất của Hoàng). Revision 9 (02/10/2026), theo recovery review REVIEW-SCOPE-L3GEN-2026-003: ghi nguồn và commit đầy đủ của từng repo ngay trong file này. Không dùng số test hay benchmark của code cũ làm bằng chứng đạt PRD.

## Dataset và đáp án

- Bộ repo: 10 repo Python/FastAPI public, pin theo commit trong bảng dưới. Số file đếm trong phạm vi phân tích của FR-L3GEN-028 (`inventory.py`, 02/10/2026). Cỡ: nhỏ ≤ 90 file, vừa 91–150, lớn trên 150.

  | Repo | Số file | Cỡ | Loại | Commit |
  |---|---:|---|---|---|
  | [rhoboro/async-fastapi-sqlalchemy](https://github.com/rhoboro/async-fastapi-sqlalchemy) | 19 | nhỏ | lộ | `6c08827241e9737487905c62d8834edc2a0da8e7` |
  | [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) | 20 | nhỏ | lộ | `cb740b656d7a0a6c5e12c7bf8e50343ec94ee9c7` |
  | [nsidnev/fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app) | 70 | nhỏ | lộ | `029eb7781c60d5f563ee8990a0cbfb79b244538c` |
  | [teamhide/fastapi-boilerplate](https://github.com/teamhide/fastapi-boilerplate) | 83 | nhỏ | lộ | `df4e6d4f817ec187eeaf2d1c5a877b27c06bb77b` |
  | [testdrivenio/fastapi-tdd-docker](https://github.com/testdrivenio/fastapi-tdd-docker) | 12 | nhỏ | kín | `16433b6621e9afd801de8eba9738a6bfefb1f601` |
  | [reworkd/AgentGPT](https://github.com/reworkd/AgentGPT) | 84 | nhỏ | kín | `18b073ab05b2902e1d052c3d2799786d8623b5e5` |
  | [igorbenav/fastapi-boilerplate](https://github.com/igorbenav/FastAPI-boilerplate) | 113 | vừa | kín | `765efecb466e343d5254cff66da4f9f84d4c8fd0` |
  | [KIBO-Agenda/kibo-backend](https://github.com/KIBO-Agenda/kibo-backend) | 136 | vừa | kín | `89eb3bb6d84e64e5af99333cc0c9d39382721581` |
  | [lnbits/lnbits](https://github.com/lnbits/lnbits) | 176 | lớn | kín | `958e4dab56564ce7a72777ac457c6fe08f903882` |
  | [fastapi-practices/fastapi_best_architecture](https://github.com/fastapi-practices/fastapi_best_architecture) | 292 | lớn | kín | `123a44aed02daf5ea60d2a7469625c933d3bb759` |

- Repo **lộ** được xem chi tiết khi chỉnh pipeline và prompt; repo **kín** chỉ xem số tổng. Nghiệm thu tính trên **từng** repo kín nhỏ và vừa (tdd-docker, AgentGPT, igorbenav/FastAPI-boilerplate, KIBO-Agenda/kibo-backend): mỗi repo phải đạt ngưỡng. Repo kín lớn báo số, không chặn. Repo lộ báo riêng.
- Đáp án sơ đồ vẽ tay theo luật vẽ của FR-L3GEN-028: mỗi cạnh bắt buộc có `file:dòng` và nguyên văn; cạnh lắp ráp, chỉ truyền session, kiểm tra rồi quay về ghi là chấp nhận được. Đáp án do subagent ngữ cảnh trống viết mù (không nhận output, HANDOFF, memory hay hội thoại của người phát triển), Khiêm duyệt. Sửa đáp án sau khi đo phải có lý do và giữ bản cũ.
- Đáp án dữ kiện L3 (route, request/response model, entity/table, config, event, thư viện, HTTP) lập theo từng loại, trước khi xem output. Chưa có. Người lập: subagent ngữ cảnh trống viết mù cho từng repo, như đáp án sơ đồ; Khiêm duyệt (Khiêm, 02/10/2026). Hạn: trước nghiệm thu M3, lập thành Task ở bước 11.
- Đáp án sơ đồ hiện có (8 repo, ngày 30/09/2026) chia khối theo tầng, không dùng để nghiệm thu. Đáp án theo định nghĩa component của FR-L3GEN-028 chưa có; hạn: trước nghiệm thu M3, lập thành Task ở bước 11. Tới khi có, KPI-006 là `not_run` và FR-L3GEN-028 chưa nghiệm thu được.
- Không lấy output của công cụ làm đáp án. Ghi phạm vi file trước khi chạy; mọi phần loại trừ phải có lý do.
- Không đặt cỡ mẫu tối thiểu. Ngưỡng áp cho từng repo, nên repo nhỏ có ít mục (ví dụ 5 cạnh) và một lỗi đổi tỷ lệ nhiều. Vì vậy mọi tỷ lệ báo kèm TP/FP/FN. Bảng cỡ mẫu của revision 7 do AI đề xuất ngày 15/09, chưa từng có quyết định riêng; Khiêm bỏ ngày 02/10/2026.
- Có bộ fixture nhỏ cho từng mẫu trong AC, kèm ca âm: tên giống route nhưng không phải route, mount, prefix động, tên bảng sinh lúc chạy, config chứa bí mật, lời gọi không xác định được đích.

## Cách tính từng KPI

| KPI | Cách tính | Ai chấm |
|---|---|---|
| KPI-L3GEN-006 — độ đúng sơ đồ cấu trúc | P, Pk, R của cạnh giữa component theo cách chấm ở NFR-L3GEN-ACC-002, tính riêng từng repo; kèm P, R của mũi tên tới hệ thống ngoài và chấm luồng (R luồng, P luồng, ARI) | Máy (`evaluate.py`) so với đáp án |
| KPI-L3GEN-007 — độ đúng bằng chứng | (a) Số kết luận công bố có bằng chứng hợp lệ theo NFR-L3GEN-ACC-002, chia cho tổng kết luận công bố. (b) Số mã dòng model trả mà có trong danh sách đã gửi, chia cho tổng mã dòng model trả; đếm trên mọi request của lần chạy, trước bước loại, kể cả câu trả lời bị loại | Máy, trên mọi lần chạy |
| KPI-L3GEN-008 — độ đúng dữ kiện L3 | Precision và recall riêng từng loại và từng repo: route, request/response model, entity/table, config, event, thư viện, lời gọi HTTP ra ngoài. Chấm thuộc tính riêng: route thiếu prefix không tính là route đúng | Máy so với đáp án |
| KPI-L3GEN-009 — nhãn mức chắc chắn | Số dữ kiện L3 gắn `exact` mà không có trong đáp án KPI-L3GEN-008 hoặc sai thuộc tính đã chấm, chia cho tổng số dữ kiện L3 gắn `exact`; tính riêng từng repo | Máy so với đáp án KPI-L3GEN-008 |
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
