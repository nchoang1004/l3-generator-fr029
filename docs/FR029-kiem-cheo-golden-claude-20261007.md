# Kiểm chéo golden FR-029 bằng agent Claude và đính chính — 07/10/2026

Tài liệu này ghi lượt kiểm thứ hai, do 6 agent Claude làm độc lập với lượt Codex ([FR029-kiem-cheo-golden-20261007.md](FR029-kiem-cheo-golden-20261007.md)). Tài liệu cũng ghi các đính chính đã áp dụng và số đo chấm lại.

**Kết luận:** giá trị chính của gold gần như đúng hết. Lỗi tập trung ở phương án thay thế, dòng bằng chứng và cách bộ chấm đọc gold. Sau khi sửa, gold đủ tin để đo route, tham số, model, HTTP và vai trò file. Dependency/auth vẫn chưa có gold.

## 1. Cách kiểm

- 6 agent, mỗi agent một nhóm gold. Không agent nào được đọc kết luận của Codex, của nhau, hay output sản phẩm.
- Mỗi lỗi phải có: đường dẫn JSON trong gold, `file:dòng` trong source, đoạn code, giá trị đúng.
- Phân loại lỗi:
  - **A:** giá trị chính sai.
  - **B:** phương án thay thế chấp nhận câu sai.
  - **C:** gold thiếu mục.
  - **D:** tùy cách hiểu spec, không tính là lỗi.
  - **E:** lỗi bộ chấm hoặc định dạng.
- Một đính chính chỉ được áp dụng khi có hai bên xác nhận: agent + Codex, hoặc agent + phiên chính tự đọc source.

Báo cáo từng agent: [.aide/evidence/reviews/fr029-gold-claude-20261007/](../.aide/evidence/reviews/fr029-gold-claude-20261007/).

## 2. Kết quả theo bộ gold

| Bộ | Đã kiểm | A | B | C | D | E |
|---|---|---|---|---|---|---|
| 6 fixture + e2e | Mọi mục | 0 | 0 | 0 | 8 | 2 (e2e thiếu `alt_lines`) |
| 19 ca dev | 42 route | 0 | 0 | 0 | 1 | 2 |
| Gold v1 teamhide, full-stack | 28 route | 0 | 0 | 0 | 4 | 0 |
| Gold v1 igorbenav, FBA | 34 + 138 route | 4 | 0 | 0 | 4 | 3 |
| Nghiệm thu tdd-docker, AgentGPT | Mọi mục | 0 | 2 | 2 (auth) | 8 | 6 |
| Nghiệm thu kibo | Mọi mục | 2 | 0 | 0 | 5 | 2 |

Lượt này không thấy route nào sai trong cả 7 bộ.

## 3. Đính chính đã áp dụng

File gốc giữ nguyên. Mỗi đính chính đều kiểm hash của file gốc và giá trị cũ trước khi sửa.

| Nơi | Cách sửa | Nội dung |
|---|---|---|
| AgentGPT | `gold.r2.json` | Bỏ URL f-string được nhận là literal. Bỏ 3 phương án "Khác" cho file Service (có chuỗi gọi tới truy cập dữ liệu). Thêm dòng 69 cho model_factory. Chấp nhận SDK được ghi vào phần giới hạn, đúng như notes của gold. Vai trò Khác không bắt dòng cụ thể (41 mục). |
| kibo | `gold.r2.json` | Thêm dòng bằng chứng `db.close()` và `update(...)` cho 2 file. |
| Gold v1 (đã duyệt) | `ERRATA` trong `fr029_golden4.py` | igorbenav: response `"None"` → null; `/docs`, `/redoc` trả lớp Response → null. FBA: `StreamingResponse` → null; bỏ handler socket.io (không phải route FastAPI). |
| e2e | sửa fixture | Thêm `alt_lines` 15 và 13. |

Script: [make_gold_r2.py](../.aide/evidence/tests/fr029-gold-r2-20261007/make_gold_r2.py). Hash ghi ở `written.json` cùng thư mục.

## 4. Lỗi bộ chấm đã sửa

Các lỗi này có test riêng trong `slice/tests/test_fr029_scorer.py` (25 test). Test được viết trước, chạy đỏ, rồi mới sửa code.

- Kiểu `uuid`/`date`/`datetime`/`email` bị đọc thành `string`, trong khi gold ghi theo ký pháp 7.3.
- Dùng tên model thay thế của gold (`alt_names`) khi so response của route.
- Khoảng dòng bằng chứng HTTP chứa dòng gọi trong gold thì tính là khớp.
- Mục `out_of_scope` có khóa giá trị 0 không còn làm kết quả sai.
- Gold v1:
  - `{prefix}` khớp cả path chưa biết lẫn path đã đọc được prefix thật;
  - `dict[...]` so như `dict`;
  - chỉ tính lời gọi HTTP qua httpx/requests/aiohttp, khớp theo khoảng dòng.
- Ca dev:
  - chỉ chấm trong phạm vi ca đó khai;
  - một router gắn vào hai app thì tính hai route.
- Các lỗi đã báo ở lượt trước: alias, fact trùng, `unknown` bị tính là đúng, chiều mảng, khóa đồng thuận.

## 5. Số đo chấm lại (output v13 cũ, không gọi model)

| Repo | Trước sửa | Sau sửa bộ chấm + gold r2 |
|---|---|---|
| kibo | Trường model 22/42, `exact` sai 56% | Trường model **42/42**, `exact` sai 50% |
| AgentGPT | HTTP 3/2/3 (TP/FP/FN), `exact` sai 18% | HTTP 5/0/1, `exact` sai **9,1%** |
| igorbenav | Tên model 6/30 | Tên model **24/30** |
| tdd-docker | Response 3/6 | Không đổi (lỗi thật của sản phẩm, xem mục 6) |

Thư mục: `ket-qua-chay/fr029-rescore-20261007-gold-r2/`.

## 6. Lỗi thật của sản phẩm còn lại và cách đã sửa

| Lỗi | Ví dụ | Sửa (prompt v14 + bộ kiểm) |
|---|---|---|
| Thiếu header khai trong dependency | kibo `Authorization` (51 route), AgentGPT `x-organization-id` (11) | Bộ kiểm báo việc còn mở khi dependency có `Header/Query/Cookie/Path` mà route chưa ghi |
| Model sinh lúc chạy không nộp được | tdd-docker `SummarySchema = pydantic_model_creator(...)` | Cho nộp `dynamic`, trường ghi `unknown` kèm lý do |
| Model không được route dùng vẫn được ghi | kibo 9 model `XResponse` chỉ qua `model_validate` | Prompt dặn không nộp; code không đưa vào fact, nhưng ghi tên vào `result.json` |
| Kiểu trả về là lớp Response bị ghi `unknown` | AgentGPT `-> StreamingResponse` | Prompt: ghi `null` |
| Đích HTTP qua `base_url=settings.X` | kibo 8/8 | Cho nộp `config` kèm `config_at` |

Sau lượt đo đầu, đã sửa thêm:

- lời gọi HTTP nhiều dòng (URL ở dòng sau);
- app tạo qua hàm factory;
- model generic `Page[Item]`;
- route docs do repo tự khai;
- dependency khai qua alias `Annotated`;
- dependency factory;
- route trùng có cùng path;
- tên header so không phân biệt hoa thường (sửa ở bộ chấm).

## 6b. Số đo prompt v14 (luna, không mù)

Đáp án đã bị mở khi kiểm gold, nên đây không phải phép đo nghiệm thu mù. Thư mục `ket-qua-chay/fr029-accept-v14/`.

| Repo | Lần chạy | Kết luận NFR-ACC-002 | Số chính | Chi phí |
|---|---|---|---|---|
| tdd-docker | `tdd-docker-r2` | **đạt** | Route 6/0/0 (TP/FP/FN); model 4/0/0; response 6/6; `exact` sai 0/4 | 0,009 USD |
| AgentGPT | `agentgpt-r2` | **đạt** | Route 16/1/0 (1 route trùng, đã sửa sau đó); tham số 16/16; HTTP 6/0/0; `exact` sai 1/21 (4,8%) | 0,45 USD |
| kibo | `kibo` | **đạt** | Route 64/0/0; model 49/0/1; tham số 61/64; HTTP đích 8/8; `exact` sai 0/20 | 0,71 USD |
| igorbenav | `igorbenav-r3` | **đạt** | Route 31/3/3 (P = R = 0,912); model 10/0/2, trường 10/10; `exact` sai 0/10 | 0,24 USD |

So với v13:

- `exact` sai: AgentGPT 18% → 4,8%; kibo 56% → 0%.
- Tham số: AgentGPT 5/16 → 16/16; kibo 11/64 → 61/64.

Còn lại ở igorbenav (đều có lý do, không đoán):

- 3 route docs: path ghi `unknown` vì `_docs_url` có thể bị ghi đè qua tham số hoặc settings.
- 5 response: dùng `PaginatedListResponse` của thư viện `fastcrud` nằm ngoài snapshot.

Lần chạy `kibo-r3` dừng giữa chừng vì tài khoản OpenAI hết tiền (`credit_balance_exhausted`, sau 0,50 USD), nên không dùng. Bản sửa dependency factory cho 3 route `waitlists` của kibo mới được kiểm offline trên source thật (tìm ra đúng `Authorization`), chưa đo bằng model.

## 7. Còn mở

- Dependency/auth: chưa có gold. Agent đã liệt kê đáp án đúng cho tdd-docker và AgentGPT, nhưng chưa đưa vào gold.
- Điều kiện đăng ký route (ca `orders-conditional-route`) chưa được chấm.
- Các điểm D cần quyết định spec, nhất là router không gắn app (OQ-013) và status trong thân hàm (OQ-014).
- Gold r2 và errata chưa có người duyệt. Theo OBS, cần Khiêm duyệt trước khi dùng làm số nghiệm thu chính thức.
- Cần một tập repo giữ riêng mới để đo mù.

## 6c. Gold model cho igorbenav và chấm lần cuối (08/10/2026)

Gold v1 của igorbenav không có trường model. Hai agent độc lập lập phần này từ source và không xem output sản phẩm: một agent Opus, một agent Sonnet. Hai bản **khớp hoàn toàn**: 12 model, 90 trường, request/response của cả 34 route. File: `.aide/evidence/tests/fr029-igorbenav-models-20261008/gold-models-{A,B}.json`. Bộ đo dùng bản A, vì bản A có thêm `alt_types` cho trường timestamp. Hai bản chưa có người duyệt.

Chấm lại 4 lần chạy tốt nhất của v14 bằng bộ chấm cuối, không gọi model (`ket-qua-chay/fr029-rescore-20261008-final/`): **cả 4 repo đạt NFR-ACC-002**. Bảng số ở mục 6b.

Đã sửa sau lần chạy cuối, có test, nhưng **chưa đo bằng model** vì tài khoản OpenAI hết tiền:

- response là lớp generic của thư viện (`fastcrud.PaginatedListResponse[X]`). Đây là lý do 2 model igorbenav bị thiếu và 5 response bị ghi `unknown`;
- tham số qua dependency factory (3 route `waitlists` của kibo; đã kiểm offline trên source thật).
