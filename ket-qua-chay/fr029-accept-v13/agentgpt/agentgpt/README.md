# agentgpt — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:e4165f3a98b552337d7cda0a275136581555ea99b60a6a5cfeedd44532cd86af`
- Trạng thái phân tích: partial — BUDGET_COST: chạm trần chi phí
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/MODEL-LLM/api/API-AGENTGPT-MODEL-LLM-v1.md](tech-specs/MODEL-LLM/api/API-AGENTGPT-MODEL-LLM-v1.md) — component Model LLM
- API: [tech-specs/METADATA-TRANG/api/API-AGENTGPT-METADATA-TRANG-v1.md](tech-specs/METADATA-TRANG/api/API-AGENTGPT-METADATA-TRANG-v1.md) — component Metadata trang
- API: [tech-specs/XAC-THUC/api/API-AGENTGPT-XAC-THUC-v1.md](tech-specs/XAC-THUC/api/API-AGENTGPT-XAC-THUC-v1.md) — component Xác thực
- API: [tech-specs/AGENT/api/API-AGENTGPT-AGENT-v1.md](tech-specs/AGENT/api/API-AGENTGPT-AGENT-v1.md) — component Agent
- API: [tech-specs/GIAM-SAT/api/API-AGENTGPT-GIAM-SAT-v1.md](tech-specs/GIAM-SAT/api/API-AGENTGPT-GIAM-SAT-v1.md) — component Giám sát

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Khởi động

- Package `reworkd_platform/`
  - `reworkd_platform/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/__init__.py:1`: `"""reworkd_platform package."""`
  - `reworkd_platform/__main__.py` — Điểm vào (exact) — `reworkd_platform/__main__.py:8`: `uvicorn.run(`
  - `reworkd_platform/logging.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/logging.py:44`: `def configure_logging() -> None:  # pragma: no cover`
- Package `reworkd_platform/web/`
  - `reworkd_platform/web/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/__init__.py:1`: `"""WEB API for reworkd_platform."""`
  - `reworkd_platform/web/application.py` — Điểm vào (exact) — `reworkd_platform/web/application.py:28`: `app = FastAPI(`
  - `reworkd_platform/web/lifetime.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/lifetime.py:41`: `def register_startup_event(`
- Package `reworkd_platform/web/api/`
  - `reworkd_platform/web/api/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/__init__.py:1`: `"""reworkd_platform API package."""`
  - `reworkd_platform/web/api/router.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/router.py:5`: `api_router = APIRouter()`

### Agent

- Package `reworkd_platform/web/api/agent/`
  - `reworkd_platform/web/api/agent/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/agent/__init__.py:2`: `from reworkd_platform.web.api.agent.views import router`
  - `reworkd_platform/web/api/agent/analysis.py` — Schema API (exact) — `reworkd_platform/web/api/agent/analysis.py:15`: `class Analysis(AnalysisArguments):`
  - `reworkd_platform/web/api/agent/dependancies.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `reworkd_platform/web/api/agent/views.py:38`, `reworkd_platform/web/api/agent/dependancies.py:44`
  - `reworkd_platform/web/api/agent/helpers.py` — vai trò unknown: agent chưa xác định
  - `reworkd_platform/web/api/agent/model_factory.py` — Hạ tầng (exact) — `reworkd_platform/web/api/agent/model_factory.py:69`: `return model(**kwargs)  # type: ignore`
  - `reworkd_platform/web/api/agent/prompts.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/agent/prompts.py:5`: `start_goal_prompt = PromptTemplate(`
  - `reworkd_platform/web/api/agent/stream_mock.py` — Điểm vào (exact) — `reworkd_platform/web/api/agent/stream_mock.py:8`: `app = FastAPI()`
  - `reworkd_platform/web/api/agent/task_output_parser.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/agent/task_output_parser.py:8`: `class TaskOutputParser(BaseOutputParser[List[str]]):`
  - `reworkd_platform/web/api/agent/views.py` — Route (exact) — `reworkd_platform/web/api/agent/views.py:34`: `@router.post(`
- Package `reworkd_platform/web/api/agent/agent_service/`
  - `reworkd_platform/web/api/agent/agent_service/agent_service.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/agent/agent_service/agent_service.py:8`: `class AgentService(Protocol):`
  - `reworkd_platform/web/api/agent/agent_service/agent_service_provider.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `reworkd_platform/web/api/agent/views.py:39`, `reworkd_platform/web/api/agent/agent_service/agent_service_provider.py:36`
  - `reworkd_platform/web/api/agent/agent_service/mock_agent_service.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/agent/agent_service/mock_agent_service.py:13`: `class MockAgentService(AgentService):`
  - `reworkd_platform/web/api/agent/agent_service/open_ai_agent_service.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `reworkd_platform/web/api/agent/views.py:38`, `reworkd_platform/web/api/agent/agent_service/open_ai_agent_service.py:91`, `reworkd_platform/web/api/agent/tools/tools.py:16`, `reworkd_platform/web/api/agent/tools/sidsearch.py:89`, `reworkd_platform/db/crud/oauth.py:54`
- Package `reworkd_platform/web/api/agent/tools/`
  - `reworkd_platform/web/api/agent/tools/code.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/agent/tools/code.py:19`: `chain = LLMChain(llm=self.model, prompt=code_prompt)`
  - `reworkd_platform/web/api/agent/tools/conclude.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/agent/tools/conclude.py:9`: `class Conclude(Tool):`
  - `reworkd_platform/web/api/agent/tools/image.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/agent/tools/image.py:19`: `client = replicate.Client(settings.replicate_api_key)`
  - `reworkd_platform/web/api/agent/tools/open_ai_function.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/agent/tools/open_ai_function.py:18`: `def get_tool_function(tool: Type[Tool]) -> FunctionDescription:`
  - `reworkd_platform/web/api/agent/tools/reason.py` — vai trò unknown: agent chưa xác định
  - `reworkd_platform/web/api/agent/tools/search.py` — Hạ tầng (exact) — `reworkd_platform/web/api/agent/tools/search.py:34`: `async with session.post(`
  - `reworkd_platform/web/api/agent/tools/sidsearch.py` — Hạ tầng (exact) — `reworkd_platform/web/api/agent/tools/sidsearch.py:28`: `async with session.post(`
  - `reworkd_platform/web/api/agent/tools/tool.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/agent/tools/tool.py:11`: `class Tool(ABC):`
  - `reworkd_platform/web/api/agent/tools/tools.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `reworkd_platform/web/api/agent/views.py:38`, `reworkd_platform/web/api/agent/agent_service/open_ai_agent_service.py:91`, `reworkd_platform/web/api/agent/tools/tools.py:16`, `reworkd_platform/web/api/agent/tools/sidsearch.py:89`, `reworkd_platform/db/crud/oauth.py:54`
  - `reworkd_platform/web/api/agent/tools/utils.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/agent/tools/utils.py:42`: `chain = LLMChain(llm=model, prompt=summarize_prompt)`
  - `reworkd_platform/web/api/agent/tools/wikipedia_search.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/agent/tools/wikipedia_search.py:28`: `wikipedia_search = wikipedia_client.run(input_str)`

### Xác thực

- Package `reworkd_platform/services/`
  - `reworkd_platform/services/oauth_installers.py` — Hạ tầng (exact) — `reworkd_platform/services/oauth_installers.py:84`: `async with session.post(`
  - `reworkd_platform/services/security.py` — vai trò unknown: agent chưa xác định
- Package `reworkd_platform/web/api/auth/`
  - `reworkd_platform/web/api/auth/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/auth/__init__.py:1`: `from .views import router`
  - `reworkd_platform/web/api/auth/views.py` — Route (exact) — `reworkd_platform/web/api/auth/views.py:16`: `@router.get("/organization/{name}")`

### Model LLM

- Package `reworkd_platform/web/api/models/`
  - `reworkd_platform/web/api/models/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/models/__init__.py:2`: `from reworkd_platform.web.api.models.views import router`
  - `reworkd_platform/web/api/models/views.py` — Route (exact) — `reworkd_platform/web/api/models/views.py:26`: `@router.get("")`

### Giám sát

- Package `reworkd_platform/web/api/monitoring/`
  - `reworkd_platform/web/api/monitoring/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/monitoring/__init__.py:2`: `from reworkd_platform.web.api.monitoring.views import router`
  - `reworkd_platform/web/api/monitoring/views.py` — Route (exact) — `reworkd_platform/web/api/monitoring/views.py:6`: `@router.get("/health")`

### Metadata trang

- Package `reworkd_platform/web/api/`
  - `reworkd_platform/web/api/metadata.py` — Route (exact) — `reworkd_platform/web/api/metadata.py:20`: `@router.get(`

### Dữ liệu dùng chung

- Package `reworkd_platform/db/`
  - `reworkd_platform/db/base.py` — Truy cập dữ liệu (exact) — `reworkd_platform/db/base.py:29`: `return await session.get(cls, id_)`
  - `reworkd_platform/db/dependencies.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/db/dependencies.py:14`: `session: AsyncSession = request.app.state.db_session_factory()`
  - `reworkd_platform/db/meta.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/db/meta.py:3`: `meta = sa.MetaData()`
  - `reworkd_platform/db/utils.py` — Hạ tầng (exact) — `reworkd_platform/db/utils.py:17`: `return create_async_engine(`
- Package `reworkd_platform/db/crud/`
  - `reworkd_platform/db/crud/agent.py` — Truy cập dữ liệu (exact) — `reworkd_platform/db/crud/agent.py:32`: `if not await AgentRun.get(self.session, run_id):`
  - `reworkd_platform/db/crud/base.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/db/crud/base.py:8`: `class BaseCrud:`
  - `reworkd_platform/db/crud/oauth.py` — Truy cập dữ liệu (exact) — `reworkd_platform/db/crud/oauth.py:36`: `return (await self.session.execute(query)).scalar_one_or_none()`
  - `reworkd_platform/db/crud/organization.py` — Schema API (exact) — `reworkd_platform/db/crud/organization.py:24`: `class OrganizationUsers(BaseModel):`
  - `reworkd_platform/db/crud/user.py` — Truy cập dữ liệu (exact) — `reworkd_platform/db/crud/user.py:18`: `return (await self.session.execute(query)).scalar_one()`
- Package `reworkd_platform/db/models/`
  - `reworkd_platform/db/models/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/db/models/__init__.py:6`: `def load_all_models() -> None:`
  - `reworkd_platform/db/models/agent.py` — Model bảng (exact) — `reworkd_platform/db/models/agent.py:8`: `__tablename__ = "agent_run"`
  - `reworkd_platform/db/models/auth.py` — Model bảng (exact) — `reworkd_platform/db/models/auth.py:8`: `__tablename__ = "organization"`
  - `reworkd_platform/db/models/user.py` — Model bảng (exact) — `reworkd_platform/db/models/user.py:10`: `__tablename__ = "Session"`
- Package `reworkd_platform/schemas/`
  - `reworkd_platform/schemas/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/schemas/__init__.py:1`: `from .agent import ModelSettings`
  - `reworkd_platform/schemas/agent.py` — Schema API (exact) — `reworkd_platform/schemas/agent.py:43`: `class AgentRunCreate(BaseModel):`
  - `reworkd_platform/schemas/user.py` — Schema API (exact) — `reworkd_platform/schemas/user.py:12`: `class UserBase(BaseModel):`

### Tiện ích dùng chung

- Package `reworkd_platform/`
  - `reworkd_platform/constants.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/constants.py:1`: `ENV_PREFIX = "REWORKD_PLATFORM_"`
  - `reworkd_platform/settings.py` — Cấu hình (exact) — `reworkd_platform/settings.py:34`: `class Settings(BaseSettings):`
  - `reworkd_platform/timer.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/timer.py:18`: `def timed_function(level: Log_Level = "INFO") -> Callable[..., Any]:`
- Package `reworkd_platform/services/`
  - `reworkd_platform/services/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/services/__init__.py:1`: `"""Services for reworkd_platform."""`
  - `reworkd_platform/services/anthropic.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/services/anthropic.py:24`: `self.claude = AsyncAnthropic(api_key=api_key)`
  - `reworkd_platform/services/ssl.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/services/ssl.py:10`: `def get_ssl_context(`
- Package `reworkd_platform/services/aws/`
  - `reworkd_platform/services/aws/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/services/aws/__init__.py:5`: `boto3.setup_default_session(profile_name="dev")`
  - `reworkd_platform/services/aws/s3.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/services/aws/s3.py:26`: `self._client = boto3_client("s3", region_name=REGION)`
- Package `reworkd_platform/services/pinecone/`
  - `reworkd_platform/services/pinecone/lifetime.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/services/pinecone/lifetime.py:8`: `pinecone.init(`
  - `reworkd_platform/services/pinecone/pinecone.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/services/pinecone/pinecone.py:36`: `self.index = Index(settings.pinecone_index_name)`
- Package `reworkd_platform/services/tokenizer/`
  - `reworkd_platform/services/tokenizer/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/services/tokenizer/__init__.py:1`: `"""Token Service"""`
  - `reworkd_platform/services/tokenizer/dependencies.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/services/tokenizer/dependencies.py:6`: `def get_token_service(request: Request) -> TokenService:`
  - `reworkd_platform/services/tokenizer/lifetime.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/services/tokenizer/lifetime.py:7`: `def init_tokenizer(app: FastAPI) -> None:  # pragma: no cover`
  - `reworkd_platform/services/tokenizer/token_service.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/services/tokenizer/token_service.py:7`: `class TokenService:`
- Package `reworkd_platform/web/api/`
  - `reworkd_platform/web/api/dependencies.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `reworkd_platform/web/api/agent/views.py:38`, `reworkd_platform/web/api/agent/agent_service/agent_service_provider.py:29`, `reworkd_platform/web/api/dependencies.py:29`, `reworkd_platform/db/crud/user.py:18`
  - `reworkd_platform/web/api/error_handling.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/error_handling.py:15`: `return JSONResponse(`
  - `reworkd_platform/web/api/errors.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/errors.py:1`: `class PlatformaticError(Exception):`
  - `reworkd_platform/web/api/http_responses.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/http_responses.py:5`: `return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)`
- Package `reworkd_platform/web/api/memory/`
  - `reworkd_platform/web/api/memory/memory.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/memory/memory.py:7`: `class AgentMemory(ABC):`
  - `reworkd_platform/web/api/memory/memory_with_fallback.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/memory/memory_with_fallback.py:10`: `class MemoryWithFallback(AgentMemory):`
  - `reworkd_platform/web/api/memory/null.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `reworkd_platform/web/api/memory/null.py:6`: `class NullAgentMemory(AgentMemory):`

## Lời gọi HTTP ra ngoài

| Component | Thư viện, method | Đích | Bằng chứng |
|---|---|---|---|
| Xác thực | aiohttp, POST | https://auth.sid.ai/oauth/token (exact) | reworkd_platform/services/oauth_installers.py:83: `async with aiohttp.ClientSession() as session:` |
| Xác thực | aiohttp, POST | https://auth.sid.ai/oauth/revoke (exact) | reworkd_platform/services/oauth_installers.py:113: `async with aiohttp.ClientSession() as session:` |
| Agent | aiohttp, POST | unknown — URL là f-string gồm host literal và giá trị search_type; không có URL hoàn toàn literal hay setting | reworkd_platform/web/api/agent/tools/search.py:34: `async with session.post(` |
| Agent | aiohttp, POST | https://api.sid.ai/v1/users/me/query (exact) | reworkd_platform/web/api/agent/tools/sidsearch.py:28: `async with session.post(` |
| Agent | aiohttp, POST | https://auth.sid.ai/oauth/token (exact) | reworkd_platform/web/api/agent/tools/sidsearch.py:47: `async with session.post(` |

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `DIAGRAM_NOT_PROVIDED`: Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- `ARCHITECTURE_NOT_EVALUATED`: Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- `HTTP_LIBRARY_UNSUPPORTED`: unsupported_http_library tại reworkd_platform/web/api/agent/agent_service/open_ai_agent_service.py:73 — LangChain/OpenAI SDK thực hiện lời gọi mô hình ra ngoài; đây không phải httpx, requests hoặc aiohttp.
- `HTTP_LIBRARY_UNSUPPORTED`: unsupported_http_library tại reworkd_platform/web/api/agent/agent_service/open_ai_agent_service.py:105 — LangChain/OpenAI SDK gọi mô hình qua apredict_messages; snapshot không dùng thư viện HTTP được hỗ trợ.
- `HTTP_LIBRARY_UNSUPPORTED`: unsupported_http_library tại reworkd_platform/web/api/agent/tools/code.py:19 — LangChain LLMChain dùng SDK ngoài để gọi mô hình; không phải httpx, requests hoặc aiohttp.
- `HTTP_LIBRARY_UNSUPPORTED`: unsupported_http_library tại reworkd_platform/web/api/agent/tools/image.py:21 — Replicate SDK thực hiện yêu cầu HTTP ra ngoài; không dùng httpx, requests hoặc aiohttp.
- `HTTP_LIBRARY_UNSUPPORTED`: unsupported_http_library tại reworkd_platform/web/api/agent/tools/image.py:37 — OpenAI SDK gửi yêu cầu tạo ảnh ra ngoài; đây không phải thư viện HTTP được hỗ trợ.
- `HTTP_LIBRARY_UNSUPPORTED`: unsupported_http_library tại reworkd_platform/web/api/agent/tools/reason.py:21 — LangChain LLMChain dùng SDK ngoài để gọi mô hình; không phải thư viện HTTP được hỗ trợ.
- `HTTP_LIBRARY_UNSUPPORTED`: unsupported_http_library tại reworkd_platform/web/api/agent/tools/utils.py:42 — LangChain LLMChain gọi mô hình qua SDK ngoài; không dùng httpx, requests hoặc aiohttp.
- `HTTP_LIBRARY_UNSUPPORTED`: unsupported_http_library tại reworkd_platform/web/api/agent/tools/utils.py:64 — LangChain LLMChain gọi mô hình qua SDK ngoài; không dùng thư viện HTTP được hỗ trợ.
- `HTTP_LIBRARY_UNSUPPORTED`: unsupported_http_library tại reworkd_platform/web/api/agent/tools/utils.py:87 — LangChain LLMChain gọi mô hình qua SDK ngoài; không dùng thư viện HTTP được hỗ trợ.
- `HTTP_LIBRARY_UNSUPPORTED`: unsupported_http_library tại reworkd_platform/web/api/agent/tools/wikipedia_search.py:28 — WikipediaAPIWrapper (LangChain) có lời gọi ra ngoài qua thư viện không thuộc httpx, requests hoặc aiohttp.
- `ANALYSIS_PARTIAL`: BUDGET_COST: chạm trần chi phí
- `OUT_OF_SCOPE_FILES`: test: 17 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- `CLAIMS_REJECTED`: 15 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
