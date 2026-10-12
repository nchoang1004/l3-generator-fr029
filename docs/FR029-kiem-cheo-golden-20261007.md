# Kiểm chéo golden FR-029 — 07/10/2026

**Golden hiện tại có giá trị, nhưng chưa đủ làm chuẩn duy nhất để nghiệm thu toàn bộ FR-029.** Đã xác nhận ba mục đáp án phụ sai trong AgentGPT. Một số điểm chấm sai khác đến từ cách tái sử dụng golden khác phạm vi. Không có căn cứ kết luận người dùng chọn nhầm bản golden đã duyệt.

## Cách kiểm và mức hoàn tất

Theo yêu cầu người dùng, ba session nhận source/spec/gold và tự đối chiếu. Không cung cấp output sản phẩm hoặc kết luận audit cũ. Phiên chính kiểm lại các phát hiện bằng source. Không sửa golden, source, spec hay bộ chấm. Không chạy model sản phẩm, không chạy lại benchmark, không chỉnh prompt.

| Nhóm | Phần đã kiểm | Giới hạn |
|---|---|---|
| Ba gold acceptance mới | 86 route, 105 tham số, 71 model/293 field, 14 HTTP call, 213 file role | 289 field khai tĩnh được đối chiếu; 4 field model sinh động chưa xác minh runtime độc lập. Chưa chứng minh đầy đủ mọi đường gọi và phân chia component |
| Bốn gold v1 đã duyệt | Reviewer xác nhận hash đáp án/commit nguồn khớp; kiểm 201 handler/method/path suffix và 1.139 trích dẫn không rỗng | Không đồng nghĩa toàn bộ ngữ nghĩa/prefix/model đã được xác nhận. Reviewer chưa lưu báo cáo cuối trước khi session bị ngắt |
| Sáu fixture FR029, e2e, 19 ca dev | Lập danh mục, kiểm cấu trúc; reviewer xác nhận vấn đề phạm vi Dispatch | Review ngữ nghĩa toàn nhóm chưa hoàn tất. Không tuyên bố tất cả fixture đúng |
| Toàn danh mục | 33 file gold; 1.759 tham chiếu được kiểm file/dòng/trích dẫn, không thấy lỗi cấu trúc trong các trường đã quét | Không phải chứng nhận đáp án đúng; bỏ qua tham chiếu file có tên chứa `.env`, không đọc nội dung bí mật |

Ba session có lúc bị dừng vì giới hạn sử dụng/quyền mạng. Báo cáo acceptance đã lưu; kết quả hai session còn lại mới có các thông báo tiến độ. Báo cáo này chỉ chốt phát hiện có bằng chứng đã nhận và kiểm lại, không coi phần chưa xong là đã qua.

## Sai ở chính đáp án

JSON path dưới đây dùng chỉ số từ 0. Gold AgentGPT: `D:/VSF/l3-acceptance-gold/agentgpt/gold.json`; source tính từ `D:/VSF/l3-acceptance-repos/reworkd_AgentGPT-18b073a/platform/`.

| ID | Mục sai | Bằng chứng và ảnh hưởng | Đính chính đề xuất |
|---|---|---|---|
| G01 | `http_calls[3].accept_alt_target` chấp nhận literal `https://google.serper.dev/{search_type}` | `reworkd_platform/web/api/agent/tools/search.py:23,35` là tham số và f-string. Chuỗi mẫu không phải URL literal thực thi. Có thể cho điểm đúng một đích ghi sai | Bỏ alternate literal; giữ target chính `unknown` có lý do. Nếu giữ biểu thức URL, lưu như thông tin mô tả |
| G02 | `file_roles[57].alt_roles` cho phép `Khác` ở `open_ai_agent_service.py` | Có đường gọi route → service → truy cập dữ liệu. Primary `Service/inferred` đúng, alternate cho qua một vai trò sai | Bỏ alternate `Khác` |
| G03 | `file_roles[66].alt_roles` cho phép `Khác` ở `tools/tools.py` | Cùng đường gọi đã chứng minh; không phải suy vai trò từ tên file | Bỏ alternate `Khác` |

Chuỗi chứng minh G02/G03: `web/api/agent/views.py:50` → `agent_service/open_ai_agent_service.py:91` → `tools/tools.py:16` → `tools/sidsearch.py:89` → `db/crud/oauth.py:41,47`. Các đường dẫn rút gọn ở giữa nằm dưới `reworkd_platform/web/api/agent/`. Provider chọn `OpenAIAgentService` tại `agent_service/agent_service_provider.py:33-50`. Phiên chính đã đọc lại từng mắt xích.

G01 được hai session phụ và phiên chính xác nhận; G02/G03 được session acceptance và phiên chính xác nhận. Đây là **ba mục sai thuộc hai nhóm**, không phải ba route sai. Chưa thấy sai giá trị chính của 86 route trong phần acceptance đã kiểm.

## Golden không sai theo phạm vi gốc, nhưng đang bị dùng sai khi chấm FR029

| ID | Vấn đề | Bằng chứng | Hướng xử lý |
|---|---|---|---|
| I01 | Dispatch: chấm cả source bằng đáp án chỉ phủ một file | `evaluation/golden/v1/cases/dispatch-case-read/source-manifest.json` khai `scored_scope.exhaustive.route = [src/dispatch/case/views.py]`. `src/dispatch/api.py:256` còn route healthcheck; `main.py:262,268` gắn thành `/api/v1/healthcheck`. `fr029_golden_routes.py` không lọc theo scored_scope | Lọc cả tập cần chấm và tập dự đoán theo phạm vi công bố; hoặc lập gold mở rộng riêng. Không thêm healthcheck vào gold cũ chỉ để hợp script |
| I02 | FBA: nhầm đầu đoạn bằng chứng với dòng gọi HTTP | `final-r2.json` có `external_calls[19]` span 47–49; lời gọi thật ở `backend/utils/request_parse.py:49`. `fr029_golden4.compare` dùng duy nhất `line_from=47` | Chuẩn hóa dòng gọi từ bằng chứng, hoặc so vị trí theo quy tắc có kiểm nghĩa. Không đổi trích dẫn hợp lệ chỉ để khớp matcher |
| I03 | FBA: constructor OAuth bị tính như HTTP call thuộc FR029 | `external_calls[17,18]` là `GitHubOAuth20`/`GoogleOAuth20` ở hai file `backend/plugin/oauth2/api/v1/{github,google}.py:21`. Golden v1 ghi kết nối ngoài; FR029 AC08 chấm lời gọi qua httpx/requests/aiohttp | Adapter tách lời gọi thuộc ba thư viện và phần giới hạn cho thư viện khác; không dùng toàn bộ `system_kind=http_api` làm mẫu số |
| I04 | FBA: placeholder prefix của gold cũ bị so như path đã biết | 25 path chứa `{prefix}`; `uncertain[0]` giải thích prefix lấy từ plugin.toml ngoài scope cũ. `backend/plugin/router.py:34-35,65-67` đọc cấu hình rồi include router | Giữ trạng thái chưa biết và phần path biết được trong chuẩn FR029; không biến placeholder thành path chính xác hoặc path parameter |

I01 đã được phiên fixture/dev và phiên chính kiểm lại cả source-manifest. I02–I04 do phiên full-golden phát hiện, phiên chính đối chiếu các gold/source liên quan. Không gọi các mục này là đáp án v1 đã duyệt bị viết sai.

Probe độc lập cho I02/I03: nộp **dữ liệu giả** chứa đúng HTTP call tại dòng 49, matcher hiện cho TP=0, FP=1, FN=3. Đây là bằng chứng lỗi phép so và phạm vi, **không phải số đo model hoặc kết luận về output cũ**. Chi tiết: [http-anchor-probe.json](../.aide/evidence/reviews/fr029-gold-audit-20261007/http-anchor-probe.json).

## Phần còn thiếu để dùng làm chuẩn nghiệm thu

- Ba gold acceptance chưa chấm dependency/auth dù FR029 yêu cầu ở bảng Endpoint. Có tham số Authorization không có nghĩa đã kiểm đúng cơ chế xác thực/quyền.
- Kibo có 55 mục vai trò `Khác` với `line=null`: chưa có chuẩn để chấm bằng chứng dòng cho các mục đó. Không kết luận 55 vai trò sai. Dòng đại diện cũng không tự chứng minh cả file không có dấu hiệu khác.
- Kibo hiện chỉ có `gold.json` và `membership.json`, không có `oracle.json` cạnh gold dù notes và bàn giao trước mô tả đã lưu oracle. Cần khôi phục artifact/môi trường để tái lập; không vì vậy phủ định kết quả đối chiếu tĩnh.
- Golden v1 không chứa đầy đủ tham số, trường model, required/nullable và file role. Không dùng điểm cao trên format này để kết luận đạt đủ tám AC.
- Cần kiểm riêng đầu ra README/OpenAPI, liên kết contract, đối chiếu component/snapshot và phần giới hạn. Danh sách route/model đúng không thay thế những kiểm này.
- Một số alternate còn phụ thuộc cách diễn giải spec: model sinh bằng factory, schema lồng, Service qua dependency provider, SDK qua wrapper. Giữ chúng trong mục cần phân xử; chưa gán lỗi chắc chắn hoặc tự sửa spec.

## Thứ tự xử lý đề xuất

1. **Đính chính golden có phiên bản mới:** bỏ ba alternate G01–G03, giữ gold gốc và hash. Reviewer độc lập kiểm lại diff với source trước khi dùng chấm.
2. **Sửa adapter/scorer:** xử lý I01–I04 và các lỗi scorer đã ghi ở [báo cáo trước](FR029-danh-gia-va-huong-cai-thien-20261007.md). Kiểm bằng ca đúng/sai tối thiểu, có cả dữ kiện nằm ngoài phạm vi chấm.
3. **Hoàn thiện chuẩn đo:** phục hồi oracle Kibo; bổ sung dependency/auth, bằng chứng file role, coverage tám AC; ghi rõ phần nào chưa đánh giá được thay vì tính như đúng.
4. **Hoàn tất vòng audit còn dở:** kiểm ngữ nghĩa đủ sáu fixture/e2e/19 ca dev; kiểm sâu prefix và model của bốn gold v1; kiểm runtime model sinh động trong môi trường được ghim. Có bảng từng mục và reviewer xác nhận.
5. **Chấm lại output đã lưu sau khi chuẩn đo ổn định:** ghi phiên bản gold/scorer và tách thay đổi điểm do sửa phép chấm khỏi thay đổi sản phẩm. Phiên này chưa chấm lại nên không đưa tỷ lệ tăng/giảm giả định.

Đã mở chi tiết gold/source của các repo trước đây gọi là kín theo yêu cầu audit. Không dùng phát hiện riêng của repo để chỉnh prompt. Nếu dùng chúng để phát triển sản phẩm về sau, phải ghi nhận việc đã biết đáp án; cần tập giữ riêng mới cho phép đo mù tiếp theo.

## Hồ sơ kiểm chứng

- [Báo cáo độc lập acceptance](../.aide/evidence/reviews/fr029-gold-audit-20261007/acceptance.md): số mục, source, các điểm mơ hồ và giới hạn.
- [Danh mục/hash/kết quả kiểm cấu trúc](../.aide/evidence/reviews/fr029-gold-audit-20261007/inventory.json), [script kiểm](../.aide/evidence/reviews/fr029-gold-audit-20261007/inventory.py).
- [Kiểm lại tính nguyên vẹn](../.aide/evidence/reviews/fr029-gold-audit-20261007/integrity-recheck.json): 401 lượt kiểm file gold/source đã lập hash, không thấy thay đổi. Đây không phải hash toàn bộ mọi file trong repository.

Đã thêm tài liệu/evidence và cập nhật HANDOFF. Chưa sửa sản phẩm/scorer/golden/spec, chưa chạy lại oracle, không commit/push.
