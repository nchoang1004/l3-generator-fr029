# Review gold FR-029: tdd-docker và AgentGPT

Ngày: 07/10/2026. Người review: Claude (độc lập, chỉ đọc). Không đọc output sản phẩm, HANDOFF, `docs/FR029-*`, diaries.

## 1. Kết luận

- Không tìm thấy giá trị chính (A) nào sai ở cả hai gold. Route, model, lời gọi HTTP khớp source và khớp oracle.
- Có lỗi ở phần chấm: alternate nới quá (B), thiếu dependency/auth (C), và nhiều chỗ định dạng làm scorer chấm sai dù công cụ đúng (E).
- Lỗi E nặng nhất: 47 file vai trò "Khác" của AgentGPT có số dòng cố định. Scorer chỉ nới khi dòng là `null`. Công cụ đúng vai trò vẫn bị chấm sai dòng.
- Số lỗi: A 0, B 2, C 2, D 8, E 6.

Scorer đọc là bản `fr029_score.py` hiện tại (đã có `FORMAT_NAMES`, `date-time` → `datetime`). Nhờ bản này, `created_at: datetime` của tdd-docker chấm được; không còn là lỗi.

## 2. Phạm vi đã kiểm

| Mục | tdd-docker | AgentGPT |
|---|---|---|
| Route (method, path, handler, dòng, tham số, body, response, status) | 6/6 đủ, đối chiếu source + oracle | 16/16 đủ, đối chiếu source + oracle (cả file, dòng, handler) |
| Model (trường, kiểu, required, nullable, alias) | 4 model, 9 trường đủ | 17 model, 63 trường đủ; script so required/allow_none/alias với oracle: 0 lệch |
| Lời gọi HTTP | 0; grep httpx/requests/aiohttp/urllib toàn repo | 6/6 đủ, đọc từng dòng; grep toàn repo không thấy lời gọi bị sót |
| Giới hạn (limitations) | 2/2 đủ | 0; grep add_api_route/add_route/add_websocket_route/mount |
| Route bị loại (excluded_routes) | grep test: không có route | grep test: không có route |
| Vai trò file | 9/9 đủ | 78/78: grep dấu hiệu trên mọi file; đọc dòng bằng chứng của 31 file không phải Khác; 47 file Khác chỉ kiểm không có dấu hiệu, không kiểm từng dòng |
| non_http_calls (12), other_io (10) | — | Lấy mẫu: đọc 7/22. Scorer không chấm hai mục này |
| out_of_scope | Đủ | Đủ (17 file test) |
| Oracle khớp gold | Đủ ở route, model | Đủ ở route, model |
| alt_* | Đủ 6 alternate | Đủ 11 alt_roles, 5 alt_where, 1 accept_alt_target |

## 3. Phát hiện

### tdd-docker (`D:/VSF/l3-acceptance-gold/tdd-docker/gold.json`, gốc `project/`)

| Mã | Lớp | Đường dẫn gold | Source | Gold | Đúng là | Vì sao |
|---|---|---|---|---|---|---|
| T1 | C | `routes[*]` (không có trường) | `app/api/ping.py:9` `async def pong(settings: Settings = Depends(get_settings))` | Không ghi dependency/auth. Chỉ có trong `notes[13]` | `routes[0]`: dependency `get_settings` (app/config.py:17), không auth. `routes[1..5]`: không dependency, không auth | Bảng Endpoint của FR-029 đòi cột "dependency hoặc auth" |
| T2 | E | `routes[1].response`, `routes[2].response`, `routes[4].response` | `app/models/tortoise.py:14` `SummarySchema = pydantic_model_creator(TextSummary)` | `model: "SummarySchema"`, route không có tên thay thế | Thêm tên thay thế `TextSummary` cho response, giống `models[3].alt_names` | Model chấp nhận `TextSummary`, route thì không. Công cụ dùng tên OpenAPI bị đúng ở model nhưng sai ở 3 route |
| T3 | D | `file_roles[7].alt_roles` | `app/models/tortoise.py:14` (như trên); `app/api/summaries.py:18` `response_model=SummarySchema` | `["Khác"]` | Chỉ `Schema API` | File có dấu hiệu Schema API, nên "Khác" (không dấu hiệu) là sai. Nhưng FR viết "Lớp được route dùng"; lớp tạo bằng phép gán có thể hiểu khác. Cần chốt cách hiểu |
| T4 | D | `limitations[0]`, `limitations[1]` | `app/summarizer.py:9` `article.download()`; `:15` `nltk.download("punkt_tab")` | Hai mục bắt buộc, loại `unsupported_http_library` | Nên `optional`, hoặc thống nhất với AgentGPT (xem G9) | newspaper3k và nltk không phải thư viện HTTP. AgentGPT không ghi tiktoken.get_encoding, cùng kiểu tải qua mạng |
| T5 | D | `limitations[0].alt_where` | `app/summarizer.py:8` `article = Article(url)` | Chấp nhận dòng 8 | Chỉ dòng 9 | Dòng 8 chỉ tạo đối tượng, không gọi mạng. Lỗi nhẹ |

### AgentGPT (`D:/VSF/l3-acceptance-gold/agentgpt/gold.json`, gốc `platform/`)

| Mã | Lớp | Đường dẫn gold | Source | Gold | Đúng là | Vì sao |
|---|---|---|---|---|---|---|
| G1 | C | `routes[*]` (không có trường) | `web/api/dependencies.py:23` `bearer: HTTPAuthorizationCredentials = Depends(HTTPBearer())` | Không ghi; `notes[8]` nói không chấm | Bảng ở mục 4 | FR-029 đòi cột "dependency hoặc auth" |
| G2 | B | `http_calls[3].accept_alt_target` | `web/api/agent/tools/search.py:35` `f"https://google.serper.dev/{search_type}"` | Chấp nhận `literal` = chuỗi f-string | Bỏ alternate; chỉ `unknown` | Gold tự nói đích chỉ biết lúc chạy. Scorer chấm alternate là `correct`, còn đáp án chính chỉ là `acceptable_unknown`. Đáp án sai được điểm cao hơn đáp án đúng, và tính là `exact` đúng |
| G3 | B | `file_roles[55].alt_roles` | `web/api/agent/views.py:39` `Depends(get_agent_service(agent_start_validator))`; `agent_service_provider.py:31` `oauth_crud: OAuthCrud = Depends(OAuthCrud.inject)` | `["Khác"]` | Chỉ `Service` | Route gọi thẳng `get_agent_service`; hàm trả về dẫn tới `db/crud/oauth.py` (Truy cập dữ liệu). Cùng cơ chế Depends như `file_roles[40]`, `[47]`, nơi gold không cho "Khác" |
| G4 | E | `file_roles[*]` có `role: "Khác"` (47 mục, vd `[2]` constants.py line 1, `[3]` logging.py line 10) | — | `line` là số cụ thể | `line: null` | Scorer chỉ nhận dòng bất kỳ khi gold `line` là `null`. File không dấu hiệu thì không có dòng đúng duy nhất. Công cụ đúng vai trò vẫn sai dòng |
| G5 | E | `file_roles[55]`, `[57]`, `[66]` | — | `label: "inferred"`, `alt_roles: ["Khác"]` | Thêm nhãn thay thế `exact` khi vai trò là Khác | Scorer không có nhãn thay thế. Công cụ trả "Khác" (nhãn `exact`) đúng vai trò nhưng sai nhãn |
| G6 | E | `file_roles[50]` model_factory.py | `model_factory.py:69` `return model(**kwargs)` | `line: 11`, `alt_roles: ["Hạ tầng"]`, không có `alt_lines` | Thêm `alt_lines: [69]` (dòng 44 nếu lấy dòng URL) | Công cụ chọn Hạ tầng sẽ dẫn dòng tạo client, nhưng gold chỉ nhận dòng 11 (`class WrappedChatOpenAI`) |
| G7 | E | `limitations: []` + `notes[19]` | — | Ghi chú nói công cụ ghi SDK vào giới hạn "không tính sai" | Bỏ khóa `limitations`, hoặc thêm mục `optional` | Khóa có mặt nên scorer tính mỗi `HTTP_LIBRARY_UNSUPPORTED` là FP, trái với ghi chú |
| G8 | D | `file_roles[50]` | `model_factory.py:44` `"openai_api_base": base,` | Chính `Khác`, thay `Hạ tầng` | Có thể đảo: chính `Hạ tầng` | FR-028 tính "client có URL". ChatOpenAI được tạo với `openai_api_base`. Cả hai đều được chấp nhận nên không đổi điểm |
| G9 | D | `limitations: []` | `services/tokenizer/lifetime.py:16` `tiktoken.get_encoding(ENCODING_NAME)`; SDK openai/replicate/anthropic | Không ghi | Thống nhất với tdd-docker (T4) | tdd-docker coi nltk.download là "thư viện HTTP khác"; ở đây tiktoken cùng kiểu thì không. Hai gold dùng hai luật |
| G10 | D | `file_roles[26]`, `[63]`, `[64]` | `services/oauth_installers.py:83` `async with aiohttp.ClientSession() as session:` | Dòng 84/114, 34, 28/47 | Thêm dòng tạo client (83, 113 / 33 / 27, 46) và dòng URL (85, 115 / 35 / 29, 48) | FR-029 Hạ tầng là "dòng tạo ... client". `http_calls` đã nhận dòng URL, `file_roles` thì không |
| G11 | D | `file_roles[57]`, `[66]`, `[21]`, `[37]` alt_roles "Khác" | `open_ai_agent_service.py:138`, `tools/tools.py:16`, `schemas/user.py:12`, `web/lifetime.py:22` | Chấp nhận Khác | Giữ được | Đường gọi qua kiểu Protocol hoặc gọi động; model lồng; engine qua hàm bọc không có URL trên dòng. Có lý, nhưng cần ghi luật rõ |

### Chung cho hai gold

| Mã | Lớp | Đường dẫn gold | Gold | Đúng là | Vì sao |
|---|---|---|---|---|---|
| X1 | E | `out_of_scope` | tdd: `{"test":5,"migration":1,"environment":0,"conditional_out":0}`; AgentGPT: `{"test":17,...0}` | So bỏ khóa bằng 0 và bỏ scope `manifest` | Scorer so `==` với số đếm từ `coverage.not_readable`. Số đếm không bao giờ có khóa 0, và có thể có `manifest` (`source_tools.classify`). Mục này luôn "sai". `fr029_accept` không dùng nên không ảnh hưởng kết luận |
| X2 | D | `routes[*].status_source` | Có `default`/`declared` | Scorer không chấm nhãn `inferred`/`exact` của thuộc tính route | AC-029-03 đòi nhãn. Gold có dữ liệu nhưng không ai chấm. Ghi để biết, không phải lỗi gold |

## 4. Dependency/auth đúng theo từng route

tdd-docker: `GET /ping` → `Depends(get_settings)`. Năm route `/summaries*` không có dependency. Không route nào có auth.

AgentGPT (auth = `HTTPBearer` qua `get_current_user`, web/api/dependencies.py:21-23):

| Route | Dependency | Auth |
|---|---|---|
| GET /api/monitoring/health, /error | Không | Không |
| POST /api/agent/start, analyze, execute, create, summarize, chat | `agent_<x>_validator` (Body + `agent_crud` → `get_current_user`, `get_db_session`); `get_agent_service(...)` → `get_current_user`, `get_token_service`, `OAuthCrud.inject` | Bearer |
| GET /api/agent/tools | Không | Không |
| GET /api/models | `get_current_user` | Bearer |
| GET /api/auth/organization/{name} | `OrganizationCrud.inject` → `get_db_session`, `get_current_user` | Bearer |
| GET /api/auth/{provider}, /{provider}/uninstall | `get_current_user`, `installer_factory` (path `provider`, `OAuthCrud.inject`) | Bearer |
| GET /api/auth/{provider}/callback | `installer_factory` | Không |
| GET /api/auth/sid/info | `get_current_user`, `OAuthCrud.inject` | Bearer |
| GET /api/metadata | Không | Không |

## 5. Giới hạn của review

- Không chạy code repository, không chạy scorer trên output thật. Kết luận về scorer là đọc code.
- 47 file "Khác" của AgentGPT: chỉ kiểm bằng grep là không có dấu hiệu; không đọc hết từng file.
- `non_http_calls` và `other_io`: đọc 7/22 mục. Scorer không chấm.
- Không kiểm `membership.json` theo FR-028 (gold nói đây không phải đáp án FR-028).
- Thứ tự trường model không kiểm vì scorer sắp xếp trước khi so.
