SPEC = {
 "file": "fastapi-realworld.json",
 "written": "28/09/2026 bản 4: đồng bộ theo oracle/ve-tay/realworld.md (bản 3 cũ ở oracle/rev3/)",
 "note": "Theo ve-tay/realworld.md. Luồng: main.py -> api (routes, dependencies, errors) -> db/repositories + db/queries (aiosql) -> pool asyncpg (db/events.py) -> PostgreSQL. services/ chỉ có hàm kiểm và helper thuần (JWT, băm, slug): giữ là khối tầng Nghiệp vụ không có cạnh luồng, để người mới thấy route gọi thẳng repository. models/ (domain, schemas) là kiểu Pydantic, dùng chung. Cạnh repos -> pool không qua import: pool gắn vào app.state lúc khởi động, lấy ra theo request (api/dependencies/database.py:12), đây là luồng chính, không có đường import thay thế.",
 "components": {
  "app": ["app/main.py", "app/core/events.py"],
  "routes": ["app/api/"],
  "services": ["app/services/"],
  "repos": ["app/db/repositories/", "app/db/queries/"],
  "pool": ["app/db/events.py"],
  "common": ["app/core/config.py", "app/core/settings/", "app/core/logging.py", "app/models/",
             "app/resources/", "app/db/errors.py"],
 },
 "shared": ["common"],
 "layers": {
  "app": ("entry", "app/main.py:18", "application = FastAPI(**settings.fastapi_kwargs)"),
  "routes": ("api", "app/api/routes/articles/articles_resource.py:27", "router = APIRouter()"),
  "services": ("service", "app/api/routes/articles/articles_resource.py:65", "if await check_article_exists(articles_repo, slug):"),
  "repos": ("data", "app/db/repositories/users.py:11", "user_row = await queries.get_user_by_email(self.connection, email=email)"),
  "pool": ("infra", "app/db/events.py:11", "app.state.pool = await asyncpg.create_pool("),
 },
 "externals": {"postgres": ["postgres", "cơ sở dữ liệu", "database", "csdl"]},
 "required": [
  ("app", "routes", "app/main.py:40", "application.include_router(api_router, prefix=settings.api_prefix)"),
  ("routes", "repos", "app/api/routes/articles/articles_resource.py:71", "article = await articles_repo.create_article("),
  ("repos", "pool", "app/db/repositories/users.py:11", "user_row = await queries.get_user_by_email(self.connection, email=email)"),
  ("pool", "ext:postgres", "app/db/events.py:11", "app.state.pool = await asyncpg.create_pool("),
 ],
 "acceptable": [
  ("routes", "services", "check", "app/api/routes/articles/articles_resource.py:65", "if await check_article_exists(articles_repo, slug):"),
  ("routes", "pool", "pass", "app/api/dependencies/database.py:12", "return request.app.state.pool"),
  ("app", "pool", "wiring", "app/core/events.py:15", "await connect_to_db(app, settings)"),
 ],
}
