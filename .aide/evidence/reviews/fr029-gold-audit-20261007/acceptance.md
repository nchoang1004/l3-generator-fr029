# Audit độc lập gold acceptance FR029 — 2026-10-07

Đối chiếu source với gold của `tdd-docker`, `agentgpt`, `kibo`. Không chạy sản phẩm, không đọc output sản phẩm hay báo cáo audit cũ, không import ứng dụng, không gọi mạng. Chỉ ghi file báo cáo này; không sửa source, gold, membership hay HANDOFF.

## Phạm vi và nguồn

Đọc CLAUDE.md, FR-L3GEN-029 revision 3, FR-L3GEN-028 revision 3 và AGENTS.md của Kibo. Dùng Python stdlib `ast`, `json`, `pathlib` để đọc tĩnh; `git rev-parse HEAD` và `git status --porcelain` để kiểm snapshot. Ba HEAD khớp commit trong gold; cả ba working tree sạch tại thời điểm kiểm.

| Bộ | Source / root phân tích | Commit |
|---|---|---|
| tdd-docker | `D:/VSF/l3-acceptance-repos/testdrivenio_fastapi-tdd-docker-16433b6/project` | `16433b6621e9afd801de8eba9738a6bfefb1f601` |
| agentgpt | `D:/VSF/l3-acceptance-repos/reworkd_AgentGPT-18b073a/platform` | `18b073ab05b2902e1d052c3d2799786d8623b5e5` |
| kibo | `D:/VSF/l3-acceptance-repos/KIBO-Agenda_kibo-backend-89eb3bb` | `89eb3bb6d84e64e5af99333cc0c9d39382721581` |

SHA-256 của `D:/VSF/l3-acceptance-gold/<bộ>/gold.json`:

- tdd-docker: `12d7a0bcb18d1e7aa0e7dbb56c7443eadd977e4b6da0e5551bd4516aaf7d5d37`
- agentgpt: `d3916c80766c756fdadb6539ec19566ecb8636367824dfb9883d4057c6e3dd4b`
- kibo: `db831c31453fc5bf365db5f14a154cc8b8986800a30fe67e9fa6576bed7836f1`

Các vị trí source dưới đây tính từ root phân tích trong bảng. JSON path dùng chỉ số bắt đầu từ 0.

## Số mục đã kiểm và giới hạn

| Bộ | Route | Tham số | Model / field | HTTP call | File role | Test / migration |
|---|---:|---:|---:|---:|---:|---:|
| tdd-docker | 6 | 3 | 4 / 9 | 0 | 9 | 5 / 1 |
| agentgpt | 16 | 19 | 17 / 63 | 6 | 78 | 17 / 0 |
| kibo | 64 | 83 | 50 / 221 | 8 | 126 | 13 / 20 |
| Tổng | 86 | 105 | 71 / 293 | 14 | 213 | 35 / 21 |

- Duyệt tất cả 289 file `.py` trong ba root. Tập decorator route đối chiếu đủ 86/86 với handler và dòng khai báo: không thấy route thiếu/thừa. Không gặp `add_api_route`, `add_route`, `add_websocket_route` trong phạm vi.
- Kiểm 86 status và nguồn declared/default; kiểm path với toàn bộ chuỗi prefix. Tdd dùng `app/main.py:13-15`; AgentGPT dùng `web/api/router.py:6-10`, `web/application.py:51`; Kibo dùng `app/main.py:60-70`, prefix router và mặc định `app/core/config.py:36`. Chưa thấy sai các giá trị này.
- Đọc signature, model request/response và các dependency phát sinh body/header. Kiểm 105 tham số, 36 body khác null và 39 response khác null. Chưa thấy sai giá trị chính. Không kiểm mọi ràng buộc validator vì gold không biểu diễn chúng.
- Đối chiếu 289 field khai tĩnh của 70 model bằng annotation/default/alias và kế thừa. Bốn field còn lại thuộc `SummarySchema` sinh động của Tdd: chỉ kiểm source tạo model, không tái chạy Tortoise để xác minh trường `id` ngầm định hoặc luật sinh schema. Không coi 4 field đó là đã xác nhận độc lập hoàn toàn.
- Đọc 14 HTTP call và nguồn tạo client/URL; quét import để tìm call bị bỏ sót. Không thấy thiếu call qua httpx/requests/aiohttp. Tdd dùng thư viện ngoài danh sách; hai limitation gold khớp source `app/summarizer.py:9,15`.
- Kiểm danh sách 213 file role với file tồn tại, dòng được chọn và dấu hiệu ưu tiên tại đó; kiểm riêng các chuỗi Service đáng ngờ. 158 mục có dòng, 55 mục Kibo không có dòng. Đây không phải chứng minh đầy đủ mọi đường gọi hay mọi dấu hiệu trong từng file.
- Đếm lại loại trừ test/migration khớp cả ba gold. `app/api/v1/test.py` của Kibo nằm trong phạm vi theo đúng mẫu tên FR028; `app/scripts/test_whatsapp_connection.py` bị loại bởi `test_*.py`. Hai script/seed Kibo còn lại import code repository nên được xét đúng điều kiện FR028.
- Đọc metadata/notes và membership; chỉ kiểm cấu trúc oracle.json lưu sẵn của Tdd/AgentGPT, không dùng oracle để thay cho source. Kibo không có oracle.json cạnh gold. Không xác nhận lại môi trường từng lần chạy oracle hay dependency bắc cầu. Không audit đầy đủ cách chia component FR028.

## Sai đã xác nhận

### A1 — AgentGPT cho phép URL mẫu biến động thành literal

- Gold: `$.http_calls[3].accept_alt_target` chấp nhận `{kind: "literal", value: "https://google.serper.dev/{search_type}"}`.
- Source: `reworkd_platform/web/api/agent/tools/search.py:22-24` nhận `search_type` làm tham số; dòng 35 gọi `f"https://google.serper.dev/{search_type}"`.
- FR029 yêu cầu đích chỉ biết lúc chạy ghi `unknown` kèm lý do. Chuỗi có `{search_type}` không phải URL literal thực sự được gửi. Giá trị chính `$.http_calls[3].target.kind = unknown` đang đúng; sai nằm ở nhánh chấp nhận thay thế.
- Đính chính: bỏ `accept_alt_target` này. Nếu muốn giữ mẫu URL để người đọc xem, đặt trong trường mô tả riêng, không chấm như literal/exact. Việc call site dòng 69 dùng mặc định `search` cũng không biến chuỗi chứa dấu ngoặc thành URL literal hợp lệ.

### A2 — Hai alternate role cho phép Khác dù có đường gọi tới dữ liệu/hạ tầng

- Gold: `$.file_roles[57].alt_roles = ["Khác"]` (`open_ai_agent_service.py`) và `$.file_roles[66].alt_roles = ["Khác"]` (`tools/tools.py`). Primary role `Service`, label `inferred` đang phù hợp.
- Chuỗi source có thể kiểm: `reworkd_platform/web/api/agent/views.py:50` gọi `analyze_task_agent`; `agent_service/agent_service_provider.py:33-50` chọn `OpenAIAgentService`; `agent_service/open_ai_agent_service.py:91` gọi `get_user_tools`; `tools/tools.py:15-16,27-33,65-68` chọn được `SID`; `tools/sidsearch.py:88-91` gọi `OAuthCrud.get_installation_by_user_id`; `reworkd_platform/db/crud/oauth.py:41,47` dựng select và gọi session.execute.
- Có thêm đường thực thi `views.py:64` → `open_ai_agent_service.py:137-138` → `sidsearch.py:141,103,116,28`. Cấu hình mặc định không chọn mock (`reworkd_platform/settings.py:101`).
- Theo FR029, Service là file trên đường gọi từ route tới dữ liệu/hạ tầng; Khác là không có dấu hiệu nào. Khó phân giải lời gọi động không làm mất dấu hiệu đã chứng minh từ source.
- Đính chính: bỏ alternate Khác ở hai mục này. Nếu benchmark muốn chấp nhận giới hạn phân giải tĩnh, tách thành tiêu chí giới hạn/unknown có lý do; không chấm vai trò Khác là sự thật tương đương. Mục provider `[55]` được giữ ở phần mơ hồ bên dưới vì có vấn đề riêng về Depends/lắp ráp.

## Thiếu coverage hoặc provenance, chưa phải sai giá trị chính

### C1 — Kibo có 55 file role không có bằng chứng dòng

- Gold: 55 mục `$.file_roles[*].line = null`, đều role Khác. Ví dụ `[23] app/core/security.py`, `[25] app/db/base.py`, `[106] app/services/scheduler/worker.py`, `[122] app/services/whatsapp/template_engine.py`.
- Source có code để trỏ tới, ví dụ `app/core/security.py:13` (`verify_password`), `app/services/scheduler/worker.py:16` (`get_scheduler`), `app/services/whatsapp/template_engine.py:22` (`select_variant`).
- FR029 AC07 yêu cầu mỗi file có dòng code làm bằng chứng. Gold hiện không giúp chấm tính hợp lệ của bằng chứng cho 55 mục này. Không kết luận 55 vai trò sai.
- Đính chính: bổ sung dòng đại diện và tiêu chí kiểm bằng chứng; nếu vai trò Khác dựa trên việc không có dấu hiệu, ghi rõ rằng một dòng đại diện chứng minh file tồn tại, còn việc không có dấu hiệu cần kiểm toàn file.

### C2 — Dependency/auth chưa được chấm

- Cả ba `$.routes[*]` không có mục đánh giá dependency/auth; AgentGPT notes nói rõ không chấm phần này.
- Ví dụ cần coverage: Tdd `app/api/ping.py:9` Depends(get_settings); AgentGPT `reworkd_platform/web/api/dependencies.py:23` HTTPBearer; Kibo `app/core/dependencies.py:175,187-188` require_owner/check_plan_permission.
- FR029 phần Endpoint yêu cầu dependency hoặc auth. Header đã có trong gold không thay thế ý nghĩa cơ chế xác thực/quyền.
- Đính chính: thêm dữ kiện dependency/auth cùng nơi khai báo và nguồn suy luận. Đây là thiếu kiểm chứng của bộ gold, không phải lỗi tham số header hiện có.

### C3 — AgentGPT other_io không được chấm ở phần giới hạn

- Gold: `$.limitations = []`; `$.other_io` có 10 mục nhưng notes xác định không chấm. FR028 yêu cầu thư viện I/O ngoài danh sách xuất hiện ở phần giới hạn; FR029 README chứa giới hạn lần chạy.
- Ví dụ source: `reworkd_platform/services/aws/s3.py:26` tạo boto3 S3 client; `reworkd_platform/services/anthropic.py:24` tạo AsyncAnthropic; `reworkd_platform/web/api/agent/tools/image.py:37` gọi OpenAI image API.
- Đính chính: giữ phân biệt HTTP SDK với httpx/requests/aiohttp, nhưng thêm kiểm có limitation I/O ngoài danh sách. Không tự chuyển 10 SDK thành 10 direct HTTP calls.
- Quét riêng còn thấy `reworkd_platform/web/api/agent/stream_mock.py:19` gọi `tiktoken.get_encoding` ngoài mục `other_io` tokenizer/lifetime.py:16. Chưa xác minh hành vi mạng của SDK tại phiên bản pin, nên đây chỉ là ứng viên bổ sung coverage, không khẳng định HTTP call thiếu.

### C4 — Provenance oracle Kibo chưa có artifact tại thư mục gold

- `$.oracle_versions`, `$.oracle_python`, notes mô tả oracle đã chạy, nhưng thư mục Kibo chỉ có gold.json và membership.json. Không thể tái đối chiếu kết quả oracle đã lưu từ ba file hiện có.
- Đính chính: lưu oracle.json cùng metadata môi trường/command. Source pin đã đúng; thiếu artifact oracle không phủ định 64 route được đối chiếu tĩnh ở audit này.

## Điểm cần thống nhất spec/chuẩn chấm

- AgentGPT `$.file_roles[55]` provider: source `agent_service_provider.py:28-31` là Depends và lắp ráp đối tượng. FR028 loại lắp ráp khỏi mũi tên; FR029 không nói ranh giới đó có áp dụng cho Service hay không. Không gộp mục này vào A2; cần chốt cách tính đường gọi qua dependency provider.
- AgentGPT `$.file_roles[21].alt_roles` cho phép Khác với schema lồng `UserBase`. FR029 bắt ghi model lồng, nhưng định nghĩa role chỉ nói lớp route dùng làm request/response model, không nói trực tiếp hay bắc cầu. Nên ghi rõ schema lồng cũng là dấu hiệu Schema API; sau đó bỏ alternate Khác.
- Tdd `$.file_roles[7]` (SummarySchema sinh bằng factory) cho phép Schema API/Khác. Cần làm rõ chữ “lớp” có bao gồm model được factory tạo hay chỉ class statement; source `app/models/tortoise.py:14`, route `app/api/summaries.py:18`.
- AgentGPT các alternate Hạ tầng cho SDK và wrapper create_engine cần quy định cùng một ranh giới nhận diện: URL/host khai tại call site hay được truy qua wrapper. Không gọi đây là primary role sai khi FR028 chưa chốt độ sâu.
- Kibo Decimal được ghi number và chấp nhận string; `datetime.time` ghi string và chấp nhận time; enum ghi string và chấp nhận tên enum. Các kiểu nguồn được bảo toàn trong notes/alt_types, nhưng FR029 không định nghĩa cú pháp chuẩn hóa kiểu. Không kết luận chúng sai; cần tránh tuyên bố OpenAPI đầy đủ nếu phép chuẩn hóa làm mất union/format.

## Kết luận trong phạm vi audit

Phát hiện hai nhóm sai ở nhánh chấp nhận thay thế của AgentGPT: một URL động và hai vai trò Service. Chưa thấy sai giá trị chính của 86 route, 105 tham số, 289 field khai tĩnh hoặc 14 HTTP call sau các phép đối chiếu nêu trên. Có bốn khoảng trống coverage/provenance cần bổ sung. Không đủ căn cứ xác nhận toàn bộ ba golden hoàn toàn đúng: bốn field sinh động, toàn bộ phân chia component, mọi đường gọi và tính tái lập oracle chưa được kiểm đầy đủ.
