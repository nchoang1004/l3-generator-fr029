# nsidnev_fastapi-realworld-example-app — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:cc39d713d4461ba991bd33105c588ea45dec5a7d3d6d8c561c322702b338983c`
- Trạng thái phân tích: partial — REPAIR_ROUNDS: còn lỗi sau 2 vòng sửa
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/DINH-NGHIA-ROUTER-API/api/API-NSIDNEV-FASTAPI-REALWORLD-EXAMPLE-APP-DINH-NGHIA-ROUTER-API-v1.md](tech-specs/DINH-NGHIA-ROUTER-API/api/API-NSIDNEV-FASTAPI-REALWORLD-EXAMPLE-APP-DINH-NGHIA-ROUTER-API-v1.md) — component Định nghĩa router API

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Khởi tạo FastAPI ứng dụng

- Package `app/`
  - `app/__init__.py` — file rỗng, không có vai trò
  - `app/main.py` — Điểm vào (exact) — `app/main.py:18`: `application = FastAPI(**settings.fastapi_kwargs)`
- Package `app/api/`
  - `app/api/__init__.py` — file rỗng, không có vai trò

### Định nghĩa router API

- Package `app/api/errors/`
  - `app/api/errors/__init__.py` — file rỗng, không có vai trò
  - `app/api/errors/http_error.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/api/errors/http_error.py:6`: `async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:`
  - `app/api/errors/validation_error.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/api/errors/validation_error.py:12`: `async def http422_error_handler(`
- Package `app/api/routes/`
  - `app/api/routes/__init__.py` — file rỗng, không có vai trò
  - `app/api/routes/api.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/api/routes/api.py:7`: `router.include_router(authentication.router, tags=["authentication"], prefix="/users")`
  - `app/api/routes/authentication.py` — Route (exact) — `app/api/routes/authentication.py:22`: `@router.post("/login", response_model=UserInResponse, name="auth:login")`
  - `app/api/routes/comments.py` — Route (exact) — `app/api/routes/comments.py:26`: `@router.get(`
  - `app/api/routes/profiles.py` — Route (exact) — `app/api/routes/profiles.py:16`: `@router.get(`
  - `app/api/routes/tags.py` — Route (exact) — `app/api/routes/tags.py:10`: `@router.get("", response_model=TagsInList, name="tags:get-all")`
  - `app/api/routes/users.py` — Route (exact) — `app/api/routes/users.py:18`: `@router.get("", response_model=UserInResponse, name="users:get-current-user")`
- Package `app/api/routes/articles/`
  - `app/api/routes/articles/__init__.py` — file rỗng, không có vai trò
  - `app/api/routes/articles/api.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/api/routes/articles/api.py:7`: `router.include_router(articles_common.router, prefix="/articles")`
  - `app/api/routes/articles/articles_common.py` — Route (exact) — `app/api/routes/articles/articles_common.py:22`: `@router.get(`
  - `app/api/routes/articles/articles_resource.py` — Route (exact) — `app/api/routes/articles/articles_resource.py:30`: `@router.get("", response_model=ListOfArticlesInResponse, name="articles:list-articles")`

### Logic nghiệp vụ dịch vụ

- Package `app/services/`
  - `app/services/__init__.py` — file rỗng, không có vai trò
  - `app/services/articles.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `app/api/routes/articles/articles_resource.py:65`, `app/services/articles.py:9`, `app/db/repositories/articles.py:243`
  - `app/services/authentication.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `app/api/routes/users.py:46`, `app/services/authentication.py:5`, `app/db/repositories/users.py:19`
  - `app/services/comments.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/services/comments.py:5`: `def check_user_can_modify_comment(comment: Comment, user: User) -> bool:`
  - `app/services/jwt.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/services/jwt.py:27`: `def create_access_token_for_user(user: User, secret_key: str) -> str:`
  - `app/services/security.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/services/security.py:11`: `def verify_password(plain_password: str, hashed_password: str) -> bool:`

### Truy cập dữ liệu repository

- Package `app/db/queries/`
  - `app/db/queries/__init__.py` — file rỗng, không có vai trò
  - `app/db/queries/queries.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/db/queries/queries.py:5`: `queries = aiosql.from_path(pathlib.Path(__file__).parent / "sql", "asyncpg")`
  - `app/db/queries/tables.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/db/queries/tables.py:12`: `class TypedTable(Table):`
- Package `app/db/repositories/`
  - `app/db/repositories/__init__.py` — file rỗng, không có vai trò
  - `app/db/repositories/articles.py` — Truy cập dữ liệu (exact) — `app/db/repositories/articles.py:45`: `article_row = await queries.create_new_article(`
  - `app/db/repositories/base.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/db/repositories/base.py:4`: `class BaseRepository:`
  - `app/db/repositories/comments.py` — Truy cập dữ liệu (exact) — `app/db/repositories/comments.py:26`: `comment_row = await queries.get_comment_by_id_and_slug(`
  - `app/db/repositories/profiles.py` — Truy cập dữ liệu (exact) — `app/db/repositories/profiles.py:25`: `user = await self._users_repo.get_user_by_username(username=username)`
  - `app/db/repositories/tags.py` — Truy cập dữ liệu (exact) — `app/db/repositories/tags.py:9`: `tags_row = await queries.get_all_tags(self.connection)`
  - `app/db/repositories/users.py` — Truy cập dữ liệu (exact) — `app/db/repositories/users.py:11`: `user_row = await queries.get_user_by_email(self.connection, email=email)`

### Kết nối cơ sở dữ liệu

- Package `app/db/`
  - `app/db/events.py` — Hạ tầng (exact) — `app/db/events.py:11`: `app.state.pool = await asyncpg.create_pool(`

### Dùng chung

- Package `app/api/dependencies/`
  - `app/api/dependencies/__init__.py` — file rỗng, không có vai trò
  - `app/api/dependencies/articles.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `app/api/routes/articles/articles_resource.py:84`, `app/api/dependencies/articles.py:43`, `app/db/repositories/articles.py:243`
  - `app/api/dependencies/authentication.py` — vai trò unknown: agent chưa xác định
  - `app/api/dependencies/comments.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `app/api/routes/comments.py:68`, `app/api/dependencies/comments.py:27`, `app/db/repositories/comments.py:26`
  - `app/api/dependencies/database.py` — Hạ tầng (exact) — `app/api/dependencies/database.py:26`: `conn: Connection = Depends(_get_connection_from_pool),`
  - `app/api/dependencies/profiles.py` — Service (inferred: Nằm trên đường gọi từ route tới truy cập dữ liệu/hạ tầng) — đường gọi `app/api/routes/profiles.py:22`, `app/api/dependencies/profiles.py:21`, `app/db/repositories/profiles.py:25`
- Package `app/core/`
  - `app/core/__init__.py` — file rỗng, không có vai trò
  - `app/core/config.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/core/config.py:17`: `@lru_cache`
  - `app/core/events.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/core/events.py:10`: `def create_start_app_handler(`
  - `app/core/logging.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/core/logging.py:8`: `class InterceptHandler(logging.Handler):`
- Package `app/core/settings/`
  - `app/core/settings/__init__.py` — file rỗng, không có vai trò
  - `app/core/settings/app.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/core/settings/app.py:12`: `class AppSettings(BaseAppSettings):`
  - `app/core/settings/base.py` — Cấu hình (exact) — `app/core/settings/base.py:12`: `class BaseAppSettings(BaseSettings):`
  - `app/core/settings/development.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/core/settings/development.py:6`: `class DevAppSettings(AppSettings):`
  - `app/core/settings/production.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/core/settings/production.py:4`: `class ProdAppSettings(AppSettings):`
  - `app/core/settings/test.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/core/settings/test.py:8`: `class TestAppSettings(AppSettings):`
- Package `app/db/`
  - `app/db/__init__.py` — file rỗng, không có vai trò
  - `app/db/errors.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/db/errors.py:1`: `class EntityDoesNotExist(Exception):`
- Package `app/db/migrations/`
  - `app/db/migrations/env.py` — ngoài phạm vi đọc (migration)
- Package `app/db/migrations/versions/`
  - `app/db/migrations/versions/fdf8821871d7_main_tables.py` — ngoài phạm vi đọc (migration)
- Package `app/models/`
  - `app/models/__init__.py` — file rỗng, không có vai trò
  - `app/models/common.py` — Schema API (exact) — `app/models/common.py:6`: `class DateTimeModelMixin(BaseModel):`
- Package `app/models/domain/`
  - `app/models/domain/__init__.py` — file rỗng, không có vai trò
  - `app/models/domain/articles.py` — Schema API (exact) — `app/models/domain/articles.py:8`: `class Article(IDModelMixin, DateTimeModelMixin, RWModel):`
  - `app/models/domain/comments.py` — Schema API (exact) — `app/models/domain/comments.py:6`: `class Comment(IDModelMixin, DateTimeModelMixin, RWModel):`
  - `app/models/domain/profiles.py` — Schema API (exact) — `app/models/domain/profiles.py:6`: `class Profile(RWModel):`
  - `app/models/domain/rwmodel.py` — Schema API (exact) — `app/models/domain/rwmodel.py:17`: `class RWModel(BaseModel):`
  - `app/models/domain/users.py` — Schema API (exact) — `app/models/domain/users.py:8`: `class User(RWModel):`
- Package `app/models/schemas/`
  - `app/models/schemas/__init__.py` — file rỗng, không có vai trò
  - `app/models/schemas/articles.py` — Schema API (exact) — `app/models/schemas/articles.py:12`: `class ArticleForResponse(RWSchema, Article):`
  - `app/models/schemas/comments.py` — Schema API (exact) — `app/models/schemas/comments.py:7`: `class ListOfCommentsInResponse(RWSchema):`
  - `app/models/schemas/jwt.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/models/schemas/jwt.py:6`: `class JWTMeta(BaseModel):`
  - `app/models/schemas/profiles.py` — Schema API (exact) — `app/models/schemas/profiles.py:6`: `class ProfileInResponse(BaseModel):`
  - `app/models/schemas/rwschema.py` — Schema API (exact) — `app/models/schemas/rwschema.py:4`: `class RWSchema(RWModel):`
  - `app/models/schemas/tags.py` — Schema API (exact) — `app/models/schemas/tags.py:6`: `class TagsInList(BaseModel):`
  - `app/models/schemas/users.py` — Schema API (exact) — `app/models/schemas/users.py:9`: `class UserInLogin(RWSchema):`
- Package `app/resources/`
  - `app/resources/__init__.py` — file rỗng, không có vai trò
  - `app/resources/strings.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `app/resources/strings.py:3`: `USER_DOES_NOT_EXIST_ERROR = "user does not exist"`

### Ngoài sơ đồ: (gốc)

- Package `./`
  - `pyproject.toml` — vai trò unknown: agent chưa xác định

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `MEMBERSHIP_KIND_DERIVED`: Membership không ghi loại component; xếp theo phạm vi đọc (FR-028): Ngoài sơ đồ: tests → test
- `TABLES_NOT_READ`: Có bảng khai theo cách công cụ chưa đọc (FR-030 Phạm vi đọc), không có trong tài liệu: bảng chỉ có trong migration — tags (app/db/migrations/versions/fdf8821871d7_main_tables.py:124)
- `DIAGRAM_NOT_PROVIDED`: Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- `ARCHITECTURE_NOT_EVALUATED`: Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- `ANALYSIS_PARTIAL`: REPAIR_ROUNDS: còn lỗi sau 2 vòng sửa
- `OUT_OF_SCOPE_FILES`: migration: 2 file, test: 23 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- `CLAIMS_REJECTED`: 57 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
