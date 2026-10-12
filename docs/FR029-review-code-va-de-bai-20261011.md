# Đánh giá code sinh tài liệu và đề bài — 11/10/2026

**Hướng triển khai phù hợp để sinh tài liệu L3 ban đầu, nhưng code hiện tại chưa đủ để xác nhận tài liệu đúng theo toàn bộ FR-029.** Điểm yếu chính còn ở nghĩa của thông tin được công bố và việc kiểm đầu ra, không phải thiếu thêm các luật nhận diện route.

Đây là kết quả đọc code và chạy kiểm mới ngày 11/10. Không lấy số đo ngày 07–09/10 làm kết quả chạy hôm nay. Không sửa sản phẩm, golden hoặc spec; không chạy model trả phí. Các ca đối kháng dùng source và câu trả lời giả để kiểm ranh giới của bộ kiểm, không phải tỷ lệ lỗi của model thật.

## 1. Đối chiếu đúng phạm vi đề bài

[Đề bài §3.6](../Đề%20bài.md) yêu cầu reverse-engineer repository thành mô hình kiến trúc và tài liệu L3 ban đầu; relationship chính phải được chứng minh từ source/static analysis. Trong phần việc người dùng đã xác định, FR-029 phụ trách tài liệu API, package/module, vai trò file và HTTP ra ngoài. Component và sơ đồ nhận từ FR-028. Không coi việc FR029 không tự dựng component/sơ đồ, TBL hoặc EVT là lỗi của phần việc này.

Luồng hiện tại đúng hướng phân công:

`snapshot → component cho trước → agent đọc file/nộp dữ kiện → Claims kiểm → facts → Markdown/OpenAPI/README/result.json`.

- Agent vẫn đề xuất dữ kiện; code không gọi extractor cũ để tự sinh route trong luồng `document`. Test e2e có chặn extractor, model builder và hàm vẽ sơ đồ cũ.
- Bộ kiểm hiện dùng AST để kiểm route, chuỗi đăng ký, client HTTP và dependency. Cách này phù hợp yêu cầu chứng minh từ source của đề bài. Gọi nó là “agent đọc, code kiểm bằng chứng” chính xác hơn “không phân tích tĩnh”. Ranh giới sâu tới đâu đã được ghi ở ADR-2026-006/OQ-018; review này không tự quyết thay.
- Có snapshot, bằng chứng dòng, giới hạn phạm vi, theo dõi phần đã đọc, output partial và nhãn bản sinh tự động chưa duyệt. Đây là nền tảng hợp lý.
- Nhưng dòng code tồn tại chưa chứng minh nội dung suy ra đúng. Ca Service không có lời gọi thật vẫn được công bố là một ví dụ trực tiếp chưa thỏa tinh thần đề bài.

## 2. Kiểm mới đã chạy

| Phép kiểm | Kết quả ngày 11/10 | Ý nghĩa và giới hạn |
|---|---|---|
| Toàn bộ `unittest discover -s slice/tests -v` | **425/426 qua**, 15,038 giây | Một lỗi `test_gateway.test_unknown_ids_are_dropped`: `[]` thay vì `["Kho"]`; trùng lỗi đã được HANDOFF ghi trước. Không phải test luồng document |
| `fr029_checkaudit.py` trên dữ liệu hiện hành | **37 bộ**, không lỗi chạy; 406 lượt route, 408 lượt đăng ký, 169 dòng dependency, 33 HTTP call | Không nhận sai/loại sai trong các phép đo tương ứng; không phải kiểm đủ thuộc tính model/auth/Service hoặc đủ mọi kiểu code |
| Mutation của bộ kiểm | Chặn 1.549 mutation route, 131 thiếu prefix, 333 dependency, 125 HTTP | Vẫn có 2 mục `http_gold_vs_rule`, 4 suspect không nằm trong gold. Không gọi toàn báo cáo là “mọi chỉ số đều 0 lỗi” |
| Bộ giả luôn nhận | Phép đo phát hiện 1.549 route, 333 dependency, 125 HTTP sai được nhận; 131 thiếu prefix lọt | Chứng minh các chỉ số có khả năng phát hiện bộ kiểm dễ dãi |
| Bộ giả luôn từ chối | Ghi 801 lần từ chối route, 408 đăng ký, 169 dependency, 33 HTTP | Số lần bị từ chối có thể nhiều hơn số mục duy nhất; không cộng làm cỡ mẫu độc lập |
| CLI `python -m l3slice document --script … --json` | Exit 0, sinh API/README/result.json | Dùng provider giả. `architecture_parity=not_evaluated`, thiếu sơ đồ được báo rõ; exit 0 chỉ là chạy xong, không phải đạt tám AC |
| Các probe đối kháng bổ sung | Xác nhận các vấn đề R01–R07 bên dưới; prefix đảo thứ tự đã bị chặn | Lưu cả JSON/OpenAPI/Markdown thật do pipeline sinh với câu trả lời giả |

Lệnh dùng interpreter `scripts/.venv/Scripts/python.exe`. Evidence tại [.aide/evidence/tests/fr029-code-review-20261011/](../.aide/evidence/tests/fr029-code-review-20261011/). Log gốc PowerShell có bản UTF-16; bản `*-utf8` giữ nguyên nội dung để đọc thuận tiện.

## 3. Vấn đề đã xác nhận trên code hiện tại

### R01 — Cao: model sai nội dung vẫn xuất `exact`, run `completed`

Source fixture `app/schemas.py:10` khai `price: float | None = None`. Probe đổi thành `boolean`, `required=true`, `nullable=false` trong câu trả lời agent. Pipeline không từ chối, xuất OpenAPI đúng các giá trị sai đó; model có confidence `exact`, API `ready`, agent `completed`.

Nguyên nhân: `docfacts.py:add_model` (dòng 201) kiểm tên trường xuất hiện, kiểu dữ liệu đầu vào và vị trí; chưa đối chiếu annotation/default với ba thuộc tính này. `FactBuilder.fact` (2021) chọn `exact` nếu không có rule suy luận. OpenAPI validator vẫn báo valid vì schema hợp cú pháp dù sai source.

Ảnh hưởng AC02/03. Cần kiểm thuộc tính có thể đối chiếu trực tiếp, khai rõ luật framework/version và giữ unknown khi không đủ chứng cứ. Ca không kiểm được phải có nhãn/phương pháp đánh giá phù hợp; không suy ra “đúng nghĩa” chỉ từ citation hợp lệ. Probe này không chứng minh tỷ lệ `exact` sai của model thật vượt 5%.

### R02 — Cao: OpenAPI invalid vẫn được publish là `ready`

Probe nộp hai tham số path cùng tên `item_id` cho một route. Pipeline báo `completed`, API `ready`, không reject. Validator độc lập báo `ParameterDuplicateError: Duplicate parameter item_id`.

`docfacts.py:930` không chặn tham số trùng. `render.py:814` đối chiếu bảng/khối máy với facts, chưa validate đầy đủ OpenAPI. Cần kiểm trùng `(in, name)` và validate OpenAPI 3.1 trước publish. Nếu không biểu diễn được, xuất phần tài liệu còn đúng và ghi rõ phần bỏ/failed theo FR029; không dán `ready` cho khối máy invalid.

### R03 — Cao: auth hoặc quan hệ Service có thể không có căn cứ

Hai probe riêng:

- Ghi `OAuth2 bearer token required`, dẫn dòng signature của route không có auth: được nhận và xuất known, API ready/run completed. `docfacts.py:339` mới kiểm mô tả là chuỗi và vị trí tồn tại.
- Ba hàm trong ba file không gọi nhau. Nộp chuỗi route → helper → db: README vẫn ghi helper là Service/inferred, run completed, không open problem. `add_role` (1420) kiểm vị trí, số mắt xích, có đi qua file; `open_problems` (1553) kiểm loại file đầu/cuối, chưa chứng minh các cạnh gọi.

Ảnh hưởng nội dung Endpoint và AC07, đặc biệt yêu cầu relationship được chứng minh từ source của đề bài. Cần bằng chứng cho từng cạnh và cho cơ chế auth; không dùng chuỗi mô tả hoặc danh sách dòng bất kỳ thay cho chứng minh. Không có chứng cứ thì giữ chưa xác định/không công bố kết luận đó.

### R04 — Vừa: nhận bằng chứng ở phần dòng agent chưa được xem

Source có URL nằm sau ký tự 400 của một dòng. `read_file` cắt đuôi, không gửi URL; `add_http` vẫn nhận chính URL đó. `source_tools.py:159` cắt dòng, nhưng `was_delivered` và `Claims.loc` (101) chỉ theo dõi số dòng; kiểm literal dùng toàn source.

Coverage cuối vẫn false, nên code đã báo partial đúng. Lỗi còn lại là nhận claim như thể bằng chứng đã được giao đủ cho agent. Cần cho đọc tiếp theo cột/chunk, hoặc từ chối cite vùng bị cắt. Không thể đạt yêu cầu agent đọc đầy đủ với dòng dài nếu chỉ có API đọc theo dòng hiện tại.

### R05 — Vừa: chưa biểu diễn được body JSON không phải model

Ca `payload: dict = Body(...)` là JSON body không có Pydantic model. Hợp đồng nộp `models=[]` bị từ chối bởi `docfacts.py:985`: rỗng chỉ dùng Form/File. Trong khi bảng tham số phải ghi body, code chỉ hỗ trợ inline fields cho form hoặc embedded body.

Cần một schema body độc lập với danh sách model, dùng cho object/scalar/array và trường chưa biết. Hiện có thể báo unknown để tiếp tục nhưng mất phần đã biết từ source. Đây là giới hạn diễn đạt dữ kiện, không giải quyết được chỉ bằng sửa prompt.

### R06 — Vừa: AC04/06 mới nối theo format fixture

`docpipeline.py:61` chỉ nhận `archdia-fixture-v1`. Kiểm snapshot/tập route/chủ sở hữu trong format đó đã có, nhưng chưa đủ bằng chứng tích hợp với contract kiến trúc thực. Sơ đồ đầu vào được nhúng nguyên văn, chưa có kiểm gắn sơ đồ với cùng snapshot.

Không cần viết bộ vẽ sơ đồ trong phần này. Cần chốt adapter/contract đầu vào FR028 và test từ dữ liệu upstream thực, kiểm owner/snapshot. CLI smoke thiếu cả archdia/diagram vẫn exit 0 và có warnings: hành vi xuất bản nháp có lý, nhưng không dùng exit 0 làm kết luận nghiệm thu AC04/06.

### R07 — Vừa: snapshot bỏ thư mục `venv/` trước khi xét luật phạm vi

Probe tạo `venv/business.py` import `main` của repository, không có `pyvenv.cfg`: snapshot vẫn loại cả thư mục. `snapshot.py:19` bỏ `venv` vô điều kiện, trong khi `SourceTools.classify` và FR028 có quy tắc thư mục có điều kiện khi import code repo.

Cần thống nhất quyết định phạm vi ngay từ snapshot, rồi để reader và membership dùng cùng một danh mục. Không xử lý được ở prompt vì file đã bị bỏ khỏi đầu vào. Đây khác OQ017 về helper cùng thư mục scripts; câu hỏi đó vẫn cần phân xử riêng.

## 4. Mức đáp ứng tám AC

| AC | Đánh giá hiện tại | Căn cứ |
|---|---|---|
| 01 — Route/method/path/handler/evidence | Có nền tảng tốt, chưa chứng minh đầy đủ | Kiểm AST/registration mới mạnh hơn; probe đảo prefix bị chặn; giới hạn dòng và phạm vi còn ảnh hưởng |
| 02 — Tham số/model/status | **Chưa đáp ứng tin cậy** | R01, R02, R05; auth chưa kiểm nghĩa |
| 03 — Unknown/inferred | Có cơ chế, **chưa tin cậy ở nhãn** | Model sai vẫn exact; evidence chưa xem vẫn được nhận |
| 04 — Đối chiếu kiến trúc | Đã kiểm trong fixture, **chưa hoàn tất tích hợp** | Chỉ hỗ trợ schema fixture; chưa test đầu vào upstream thực |
| 05 — Loại test/non-decorator, ghi giới hạn | Có triển khai và test | Các case test/non-decorator có kiểm; R07 là thiếu nhất quán phạm vi |
| 06 — README | Đã có các mục và cảnh báo | Thiếu upstream thì báo rõ; chưa thể chốt đủ sơ đồ/đối chiếu cho lần chạy thực |
| 07 — Package/module/vai trò file | Có render, **chưa chứng minh đúng vai trò Service** | R03 nhận chuỗi không có cạnh gọi |
| 08 — HTTP ra ngoài | Bộ kiểm cải thiện rõ, **chưa chứng minh bao phủ mọi repo** | 33 call và 125 mutation đã kiểm; R04 còn; giới hạn wrapper/receiver phức tạp cần công bố |

Không quy đổi bảng này thành “x/8 đạt”: test fixture qua, code có tính năng, và sản phẩm được nghiệm thu là ba mức khác nhau.

## 5. Hướng cải thiện hợp lý với đề bài

1. **Ưu tiên trước: độ đúng đầu ra.** Thêm các probe R01–R03 vào regression; kiểm model/param trực tiếp và nhãn; chặn tham số trùng; validate OpenAPI trước xuất. Các test phải chứng minh bản cũ sai và bản sửa đúng.
2. **Chứng minh quan hệ.** Agent nộp evidence theo từng cạnh gọi/auth; checker xác nhận hoặc ghi chưa biết. Giữ agent là nơi đề xuất, không bắt buộc biến toàn bộ hệ thống thành extractor tĩnh.
3. **Đọc đầy đủ và biểu diễn được phần đã biết.** Sửa đọc dòng dài; hỗ trợ JSON body không có model; thống nhất scope từ snapshot tới reader. Không mở rộng ngôn ngữ/framework trước các sửa này.
4. **Hoàn tất điểm nối FR028.** Nhận component/archdia/diagram cùng snapshot bằng contract ổn định, có test đúng/sai thực tế. Đây là tích hợp, không phải tạo component hoặc dựng sơ đồ mới.
5. **Đo cả tài liệu, không chỉ bộ kiểm.** Chấm model fields, auth, call path, nhãn theo thuộc tính, Markdown/OpenAPI tương đương và tám AC. Chạy end-to-end cấu hình mới trên tập giữ riêng sau khi khóa gold/scorer. “37 bộ checker không có false acceptance” không thay được việc này.

Các phép chạy v14 cũ là dữ kiện tham khảo. HANDOFF gọi “bốn lần chạy tốt nhất”, đồng thời nói không mù; không dùng chúng làm bằng chứng một lần chạy đầu theo OBS đã đạt nghiệm thu. Code bộ kiểm hiện tại cũng đã thay đổi sau các lần chạy đó. Phiên này chưa chạy model mới nên không kết luận chất lượng model tăng hay giảm.

## 6. Bằng chứng và việc chưa làm

- [Log suite](../.aide/evidence/tests/fr029-code-review-20261011/suite-utf8.log).
- [Bộ kiểm 37 case](../.aide/evidence/tests/fr029-code-review-20261011/checkaudit/summary.json), [bộ giả luôn nhận](../.aide/evidence/tests/fr029-code-review-20261011/sanity-accept/summary.json), [bộ giả luôn từ chối](../.aide/evidence/tests/fr029-code-review-20261011/sanity-reject/summary.json).
- [Probe nội dung/OpenAPI](../.aide/evidence/tests/fr029-code-review-20261011/probes.py), [kết quả](../.aide/evidence/tests/fr029-code-review-20261011/probes-observed-utf8.json).
- [Probe Service/CLI/scope](../.aide/evidence/tests/fr029-code-review-20261011/integration_probes.py), [kết quả](../.aide/evidence/tests/fr029-code-review-20261011/integration-probes-observed.json). Các thư mục con giữ API/OpenAPI/result do probe sinh; README Service giả cũng được giữ.

Chưa sửa các lỗi, chưa đo end-to-end bằng model thật, chưa chạy ứng dụng nguồn, chưa kiểm UI thủ công, không commit/push. Review này tập trung luồng sinh tài liệu `document`; suite rộng hơn được chạy để kiểm hồi quy xung quanh, không có nghĩa mọi module khác đã được review thủ công.
