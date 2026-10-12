# Đánh giá FR-029 và thứ tự cải thiện

Ngày: 07/10/2026. Phạm vi: tài liệu mentor, FR-029 và các NFR/OBS liên quan, luồng agent, renderer, CLI, bộ chấm và test hiện tại tại checkout `feature/l3-fr029`. Đây là đánh giá kỹ thuật, không phải phê duyệt nghiệm thu.

## 1. Kết luận

Luồng agent đã hoạt động và có nền tảng tốt để tiếp tục. Điểm cần giải quyết trước là **độ tin cậy của dữ kiện được xuất và phép đo**, sau đó mới tối ưu cách đọc source hoặc tăng ngân sách.

Những phần nên giữ: source chỉ đọc; snapshot và bằng chứng có vị trí; agent nộp dữ kiện có cấu trúc; không fallback về extractor; xử lý kết quả dở; renderer dùng chung dữ kiện; tách component/sơ đồ thành đầu vào.

Chưa thể kết luận đủ 8 AC. Số đo nhận diện route chưa chứng minh tham số/model/HTTP đúng. Bộ chấm hiện có lỗi làm giảm số `exact` sai trong một số trường hợp. Ngoài ra, pipeline có thể xuất OpenAPI không hợp lệ dù báo `ready`.

## 2. Phạm vi kiểm chứng của phiên này

- Đọc [tài liệu mentor](FR029-giai-thich-cho-mentor.md), [bản quy tắc](FR029-quy-tac.md), FR-029/028, NFR-ACC/AI/SEC, OBS, HANDOFF và OQ-012 cùng evidence quyết định liên quan.
- Đọc đường chạy `source_tools → docagent → docfacts → docpipeline → render`, CLI và bốn script chấm/ghép đánh giá.
- Chạy mới **51/51 test** trong `test_docagent.py`: qua. Toàn suite **238/239**: lỗi `test_gateway.test_unknown_ids_are_dropped`, trùng lỗi log cũ; thời gian lần chạy này 12,523 giây.
- Tái hiện bằng source giả và provider giả. Không gọi model trả phí, không chạy source bên ngoài, không mở đáp án hoặc kết quả chi tiết repo kín.
- Đọc hai summary tổng đang có ở `fr029-accept-v13/tdd-docker/summary.json` và `igorbenav/summary.json`. Số AgentGPT/Kibo trong phần nhận xét tài liệu lấy từ báo cáo mentor, chưa xác minh lại bằng summary gốc trong phiên này.
- Theo yêu cầu người dùng, bổ sung hai reviewer ngữ cảnh riêng, không cung cấp kết luận trước của phiên chính. Kết quả đối chiếu bổ sung ở mục 6.

Script tái hiện: [reproduce.py](../.aide/evidence/tests/fr029-review-20261007/reproduce.py). Chạy từ gốc dự án bằng Python của `scripts/.venv`. Không chỉnh sửa code sản phẩm trong phiên đánh giá.

## 3. Các vấn đề đã tái hiện

Các ca này kiểm hành vi code khi nhận dữ kiện sai; không phải số đo tần suất model mắc lỗi trên repo thật.

| Vấn đề | Bằng chứng thực chạy | Hệ quả | Cải thiện |
|---|---|---|---|
| Evidence trỏ vào nội dung model chưa thấy | Dòng HTTP dài hơn 400 ký tự; URL nằm sau phần bị cắt. `read_file` không trả URL nhưng `add_http` nhận URL đó, không lỗi | Coverage báo thiếu đúng, nhưng fact sai điều kiện bằng chứng vẫn có thể đi vào kết quả partial | Receipt phải ghi phần thực gửi, gồm cột nếu cắt dòng; chỉ cho dẫn đoạn đã gửi và được xử lý. Cung cấp cách đọc tiếp phần đuôi |
| Prefix đảo thứ tự vẫn qua bộ kiểm | Đổi thứ tự hai prefix trong fixture: path thành `/v1/api/items/{item_id}`, claim vẫn được nhận | Có đủ literal không chứng minh đúng đường đăng ký | Agent nộp chuỗi đăng ký với định danh app/router và từng quan hệ sử dụng; code kiểm tính liên tục. Gold đối chứng vẫn cần để kiểm ý nghĩa |
| Thuộc tính model sai vẫn mang `exact` | Field `price` trong fixture bị đổi sang boolean và required=true; claim qua, fact mang `exact` | Nhãn hiện chủ yếu phản ánh có dùng tên quy tắc hay không | Nhãn theo từng thuộc tính; giữ bằng chứng và căn cứ suy luận tương ứng. Không nâng exact chỉ vì không có `rule` |
| OpenAPI không hợp lệ vẫn được xuất | Nộp trùng parameter `item_id`; agent `completed`, API `ready`; validator độc lập báo `ParameterDuplicateError` | `check_doc` không thay được kiểm hợp lệ OpenAPI | Chạy validator trước publish; kiểm trùng parameter/field và `$ref`; lỗi trả về đúng đường dữ liệu, chỉ xuất phần biểu diễn hợp lệ |
| Tỷ lệ `exact` sai bị đếm thiếu khi gold có alias vị trí | Gold cho `a.py:3` là vị trí thay thế của `a.py:2`. Sai method được scorer ghi nhận, nhưng `exact_wrong` trả 0/1 | Số đo nhãn có thể lạc quan hơn thực tế | Dùng chung kết quả matching giữa chấm thuộc tính và chấm nhãn; gắn bằng fact ID thay vì ghép lại chuỗi khóa |

Vị trí mã: `source_tools.read_file/was_delivered`, `docfacts.loc/add_route/add_model/FactBuilder.fact`, `docpipeline.plan_documents`, `fr029_accept.exact_wrong`. Prefix là vấn đề đã được báo trước ở F03; OpenAPI mở rộng ca F04; không coi toàn bộ bảng là lỗi mới.

**Một ca không lỗi cần giữ:** bỏ parameter path khỏi claim khiến renderer loại route đó khỏi khối OpenAPI kèm lý do. Không quy chụp renderer bỏ qua mọi lỗi; lỗi đã xác nhận ở đây là parameter trùng.

## 4. Những giới hạn thiết kế còn ảnh hưởng chất lượng

### 4.1 Khuôn dữ liệu đang giới hạn những gì agent có thể diễn tả

`Claims.type_` nhận kiểu cơ bản, array và tên class dạng `file.py::Class`. Chưa có biểu diễn đầy đủ cho union nhiều kiểu, dictionary có kiểu giá trị, enum/literal và generic. `add_model` còn yêu cầu dòng khai `class <tên>`; model tạo động khó nộp thành model có cấu trúc. Request body JSON buộc có model; kiểu scalar/array JSON chưa được biểu diễn đầy đủ.

Vì vậy, sửa prompt không giải quyết được hết model recall và field accuracy. Ưu tiên mở schema đúng theo fixture phát triển: kiểu hợp, object có kiểu giá trị, schema request/response riêng và các lớp dùng chung. Khi chưa hỗ trợ phải giữ kiểu nguyên văn, evidence và lý do giới hạn; không đổi thành `any` rồi coi đã hiểu.

### 4.2 Vòng agent cần nhớ việc đã làm sau khi rút gọn hội thoại

`_shrink` rút gọn cả kết quả tool lẫn đối số nộp facts cũ. Dữ kiện còn trong `Claims`, nhưng agent không có công cụ đọc lại sổ; `submit_findings` chỉ trả số lượng và một phần file chưa đọc.

Đề xuất thêm cách xem dữ kiện đã chấp nhận, lỗi đang mở và tham chiếu chưa giải quyết theo ID. Chia tiến độ thành đọc phạm vi → ghép route/model/client → rà thuộc tính → kiểm/xuất. Đây là các bước của một vòng điều phối, chưa cần nhiều agent sinh tài liệu cùng lúc.

Đo trên repo lộ: token lặp, số lần đọc lại, số claim bị từ chối, số model chưa giải quyết và độ đúng thuộc tính trên mỗi đơn vị chi phí. Giảm số ký tự hội thoại không tự chứng minh chi phí giảm tương ứng; phần trạng thái riêng của provider cũng cần tính.

### 4.3 Bộ kiểm đang có luật đọc code, nhưng chưa đủ chứng minh ngữ nghĩa

Luồng mới không gọi extractor AST cũ; tuy nhiên code vẫn quyết phạm vi, quét dấu hiệu bằng regex, đối chiếu literal, ghép path và kiểm loại dòng. Cách mô tả chính xác là **agent đề xuất dữ kiện; code quản lý nguồn, kiểm điều kiện và xuất tài liệu**.

Không nên tăng mã regex cho từng repo để chữa tất cả lỗi ngữ nghĩa. Những kiểm tất định nên tập trung vào schema, tọa độ, tham chiếu, chuỗi liên kết, biểu diễn và trạng thái. Agent cần dẫn đủ ngữ cảnh để chứng minh auth, client HTTP và Service; kiểm chéo độc lập/gold xác định việc diễn giải có đúng hay không.

Đặc biệt, không đổi hàng loạt nhãn sang `inferred` chỉ để giảm KPI exact sai. `inferred` cũng phải có căn cứ; thiếu căn cứ thì unknown hoặc loại kết luận.

### 4.4 Đường chạy pilot và CLI sản phẩm chưa thống nhất

Pilot có ResponsesProvider, bảng giá và trần USD. Lệnh `document` hiện chỉ tạo OpenAICompatProvider, chưa có lựa chọn adapter Responses hoặc trần USD. Báo cáo thành công bằng script pilot chưa chứng minh trải nghiệm CLI tương đương.

Tách một cấu hình run dùng chung cho CLI/pilot: adapter, model, các trần, phiên bản prompt/tool/schema và ước tính chi phí. Budget hiện kiểm chi phí đã dùng trước lượt mới; chưa bảo đảm trần cứng cho request sắp gửi hoặc retry. Ghi rõ chi phí biết được và phần chưa xác định thay vì xem thiếu usage là miễn phí.

### 4.5 AC04/06 cần hợp đồng đầu vào thật

`compare_architecture` chỉ nhận `schema: archdia-fixture-v1`. Sơ đồ nhận dạng chuỗi rồi nhúng vào README, chưa có kiểm snapshot riêng. Cần adapter cho artifact FR-028 thật và bộ kiểm version/snapshot/component/route. Công việc vẫn chỉ nhận/đối chiếu, không tạo component hay dựng sơ đồ.

## 5. Tài liệu mentor cần sửa trước khi dùng để trình bày

Tài liệu giải thích được cơ chế và nêu nhiều giới hạn thật, nhưng hiện trạng nằm rải rác và mâu thuẫn giữa các mục.

| Chỗ cần sửa | Cách trình bày chính xác hơn |
|---|---|
| Đầu mục 1 có số v13 nhưng cuối mục 1 nói v9–v13 chưa đo | Tách bảng hiện trạng v13 và lịch sử v3–v8; gắn mỗi bảng với run ID và phiên bản bộ chấm |
| Mục 5.2/10 nói exact chưa đo; mục 1 đã có 18%/56% | Ghi “đã có phép đo sơ bộ, bộ chấm còn lỗi/thiếu trường”; chưa coi số đó là toàn bộ độ đúng nhãn |
| Mục 10/11 nói 3 repo nghiệm thu chưa chạy | Cập nhật theo từng run; phân biệt đã chạy với đã có phép đo đủ điều kiện nghiệm thu |
| “Route đạt trên cả 4 repo” | Ghi đúng chỉ số nhận diện route đã vượt ngưỡng; không suy rộng sang đúng hợp đồng API hoặc toàn AC01–03 |
| “Tên model 6/30” | Đây là số route khớp có tên model đúng; không phải model precision/recall và không phải 6 model đúng trên 30 model |
| “Tham số đúng 5/16, 11/64” | Scorer so cả danh sách parameter trên từng route. Mẫu số là route khớp, không phải số tham số; đặt đúng tên chỉ số |
| “Trường model 22/42” | Scorer so cả danh sách fields của một model. Đây là số model có bảng fields khớp, không phải 22 trường trên 42 trường |
| “Code không trích dữ kiện” và “không thể lọt route test” | Mô tả trách nhiệm cụ thể; lọc source giảm khả năng lọt test nhưng không bảo đảm model không bịa khi dẫn source khác |
| Chi phí 1,62/2 USD và câu hỏi tăng trần cũ | Lập sổ theo run; ghi ước tính từ usage, không gộp lịch sử và hạn mức hiện hành |
| “Giảm ngữ cảnh khoảng 4 lần” | Giữ là giả thuyết cần đối chứng, không dùng làm kết quả cải thiện |

Summary tdd-docker xác nhận route 6/6 nhưng response chỉ 3/6 và model recall 0,75. Summary igorbenav xác nhận route 30/34, tên model khớp 6/30 và run completed. Đây là ví dụ rõ cho việc `completed` không đồng nghĩa tài liệu chính xác.

OQ-012 hiện là `answered`, evidence ghi người dùng đã trả lời bỏ qua ba quy tắc. HANDOFF cũ vẫn ghi phải chờ trả lời/đóng OQ. Cần đồng bộ trạng thái hành chính và quyết định đã có; phiên đánh giá này không yêu cầu người dùng duyệt lại và không sửa spec.

## 6. Kiểm bộ chấm bằng nhiều phiên độc lập

Hai reviewer đã hoàn tất. Mỗi reviewer được cung cấp cùng code/spec, không thấy kết luận của phiên chính hoặc của nhau, chỉ thử dữ liệu giả. Đây là kiểm chéo trong các ngữ cảnh riêng; không tự coi là đánh giá của nhiều hãng model hay gold đã được người duyệt. [Biên bản độc lập](../.aide/evidence/reviews/fr029-scorer-20261007-independent.md).

| Vấn đề bộ chấm | Xác nhận | Cách sửa cần kiểm |
|---|---|---|
| Alias vị trí/tên làm exact mất lỗi | Cả hai; phiên chính tái hiện | Một mapping fact → gold dùng chung cho mọi chỉ số |
| Hai fact cùng key bị ghi đè; đảo thứ tự đổi exact 0/2 thành 2/2 | Reviewer B; phiên chính tái hiện | Từ chối duplicate mâu thuẫn hoặc matching một-một; chấm theo từng fact |
| Loại không có gold vẫn vào mẫu số exact và được coi đúng | Cả hai; phiên chính tái hiện | Báo số đã chấm/chưa chấm; thiếu gold khác danh sách gold rỗng |
| Unknown khớp unknown và model dynamic rỗng bị tính correct | Cả hai; phiên chính tái hiện nhánh model rỗng | Tách đúng giá trị đã biết và unknown được chấp nhận; tránh `all([])` làm bảng rỗng thành đúng |
| Array một chiều/hai chiều thành cùng kiểu | Reviewer A; phiên chính tái hiện | So kiểu đệ quy, giữ số chiều và nullable |
| Hai format dùng matching khác nhau và phủ khác chỉ số | Reviewer B tái hiện; cả hai đọc nhánh acceptance | Chuẩn hóa format; công bố ma trận gold/metric; không so hai tỷ lệ khác nghĩa |
| Hai lỗi con khác field cùng dòng bị gọi là đồng thuận | Cả hai; phiên chính tái hiện | Giữ item + full field path; cách sửa trái nhau phải chuyển sang kiểm lại |

Điểm cần diễn giải công bằng: unknown đúng với giới hạn runtime là hành vi hợp lệ của sản phẩm, nhưng không được gọi là đã giải đúng giá trị. Giữ riêng `correct_known`, `acceptable_unknown`, `wrong`, `not_evaluated`. Không yêu cầu model đoán để cải thiện điểm.

Runner acceptance còn thiếu verdict ngưỡng riêng. Đề xuất ba trạng thái độc lập: chạy xong hay dở, phép đo đủ hay thiếu, nghiệm thu đạt hay không. Dùng số đếm gốc khi so ngưỡng, chỉ làm tròn lúc trình bày. Các kết quả duplicate là kiểm tính vững của scorer với dữ liệu giả; chưa khẳng định mọi output thực tế chứa duplicate.

Các phát hiện cho thấy phép đo chưa đủ tin để kết luận mức cải thiện; không đủ để tính lại chính xác số liệu repo kín bằng suy đoán. Chưa đọc chi tiết repo kín hoặc chạy lại model trong lần kiểm này.

## 7. Thứ tự thực hiện đề xuất

Các việc này là đề xuất; chưa triển khai sửa sản phẩm trong phiên đánh giá.

| Ưu tiên | Việc | Điều kiện xong |
|---|---|---|
| 1 | Sửa bộ chấm và khóa định nghĩa matching/chỉ số | Các ca alias, trùng/đảo thứ tự, unknown, thiếu gold, chiều mảng, failed và đồng thuận đều có đáp án kiểm độc lập; số exact dùng cùng matching với thuộc tính |
| 2 | Chặn kết luận không đủ evidence; kiểm OpenAPI trước xuất | Nội dung bị cắt không được dẫn như đã đọc; parameter trùng không thể xuất ready; thêm test đối chứng đúng/sai |
| 3 | Mở schema API/model và nhãn theo field | Agent có cách diễn tả kiểu cần hỗ trợ; từng thuộc tính có evidence/rule/unknown; không đánh đồng không-rule với exact |
| 4 | Chia lượt phân tích và cung cấp sổ trạng thái cho agent | Đo trên repo lộ với cùng cấu hình; tăng độ đúng tham số/model/HTTP, giảm đọc lại và token lặp |
| 5 | Đồng bộ CLI, ngân sách và đầu vào FR-028 | Lệnh người dùng chạy dùng đúng adapter đã thử; AC04/06 kiểm trên artifact thật cùng snapshot |
| 6 | Đo lại cấu hình đã khóa và cập nhật báo cáo mentor | Đủ từng chỉ số trên mỗi repo nghiệm thu; giữ kết quả cũ, ghi scorer version/gold digest; không sửa prompt theo lỗi chi tiết repo kín |

Sửa scorer có thể chấm lại output đã lưu mà không gọi model mới. Việc này cần chạy qua công cụ chỉ xuất số tổng cho repo kín, giữ phép chấm cũ và bản đính chính riêng. Chưa chấm lại dữ liệu kín trong phiên này.
