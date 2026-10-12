# full-stack-fastapi-template — tài liệu L3 API (bản sinh tự động)

Bản sinh tự động, chưa được chủ repository duyệt.

- Snapshot: `snap:1a1322d5ce21372235dd6e938b9861e72ecb4d92d97f3554d1e8434cb5ab594f`
- Trạng thái phân tích: completed
- Độ phủ đọc source: đủ

## Mục lục contract

- API: [tech-specs/TOAN-BO/api/API-FULL-STACK-FASTAPI-TEMPLATE-TOAN-BO-v1.md](tech-specs/TOAN-BO/api/API-FULL-STACK-FASTAPI-TEMPLATE-TOAN-BO-v1.md) — component Toàn bộ

## Sơ đồ component

Chưa được cấp sơ đồ từ bước kiến trúc (FR-028); công cụ này không tự dựng sơ đồ.

## Cấu trúc component

### Toàn bộ

- Package `./`
  - `pyproject.toml` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `pyproject.toml:1`: `[dependency-groups]`
- Package `backend/`
  - `backend/pyproject.toml` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/pyproject.toml:1`: `[project]`
- Package `backend/app/`
  - `backend/app/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file)
  - `backend/app/crud.py` — Truy cập dữ liệu (exact) — `backend/app/crud.py:14`: `session.add(db_obj)`
  - `backend/app/initial_data.py` — Điểm vào (exact) — `backend/app/initial_data.py:22`: `if __name__ == "__main__":`
  - `backend/app/main.py` — Điểm vào (exact) — `backend/app/main.py:21`: `app = FastAPI(`
  - `backend/app/models.py` — Model bảng (exact) — `backend/app/models.py:52`: `class User(UserBase, table=True):`
  - `backend/app/utils.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/app/utils.py:34`: `def send_email(`
- Package `backend/app/alembic/`
  - `backend/app/alembic/env.py` — vai trò unknown: agent chưa xác định
- Package `backend/app/alembic/versions/`
  - `backend/app/alembic/versions/1a31ce608336_add_cascade_delete_relationships.py` — vai trò unknown: agent chưa xác định
  - `backend/app/alembic/versions/9c0a54914c78_add_max_length_for_string_varchar_.py` — vai trò unknown: agent chưa xác định
  - `backend/app/alembic/versions/d98dd8ec85a3_edit_replace_id_integers_in_all_models_.py` — vai trò unknown: agent chưa xác định
  - `backend/app/alembic/versions/e2412789c190_initialize_models.py` — vai trò unknown: agent chưa xác định
  - `backend/app/alembic/versions/fe56fa70289e_add_created_at_to_user_and_item.py` — vai trò unknown: agent chưa xác định
- Package `backend/app/api/`
  - `backend/app/api/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file)
  - `backend/app/api/deps.py` — Truy cập dữ liệu (exact) — `backend/app/api/deps.py:22`: `with Session(engine) as session:`
  - `backend/app/api/main.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/app/api/main.py:6`: `api_router = APIRouter()`
- Package `backend/app/api/routes/`
  - `backend/app/api/routes/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file)
  - `backend/app/api/routes/items.py` — Route (exact) — `backend/app/api/routes/items.py:13`: `@router.get("/", response_model=ItemsPublic)`
  - `backend/app/api/routes/login.py` — Route (exact) — `backend/app/api/routes/login.py:23`: `@router.post("/login/access-token")`
  - `backend/app/api/routes/private.py` — Route (exact) — `backend/app/api/routes/private.py:23`: `@router.post("/users/", response_model=UserPublic)`
  - `backend/app/api/routes/users.py` — Route (exact) — `backend/app/api/routes/users.py:214`: `@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])`
  - `backend/app/api/routes/utils.py` — Route (exact) — `backend/app/api/routes/utils.py:11`: `@router.post(`
- Package `backend/app/core/`
  - `backend/app/core/__init__.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file)
  - `backend/app/core/config.py` — Cấu hình (exact) — `backend/app/core/config.py:15`: `class Settings(BaseSettings):`
  - `backend/app/core/db.py` — Hạ tầng (exact) — `backend/app/core/db.py:7`: `engine = create_engine(str(settings.DATABASE_URL), pool_pre_ping=True)`
  - `backend/app/core/security.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `backend/app/core/security.py:11`: `password_hash = PasswordHash(`
- Package `backend/tests/`
  - `backend/tests/__init__.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/conftest.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/api/`
  - `backend/tests/api/__init__.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/api/routes/`
  - `backend/tests/api/routes/__init__.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/api/routes/test_items.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/api/routes/test_login.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/api/routes/test_private.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/api/routes/test_users.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/crud/`
  - `backend/tests/crud/__init__.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/crud/test_user.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/scripts/`
  - `backend/tests/scripts/__init__.py` — vai trò unknown: agent chưa xác định
- Package `backend/tests/utils/`
  - `backend/tests/utils/__init__.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/utils/item.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/utils/user.py` — vai trò unknown: agent chưa xác định
  - `backend/tests/utils/utils.py` — vai trò unknown: agent chưa xác định
- Package `hooks/`
  - `hooks/post_gen_project.py` — Khác (exact: Không có dấu hiệu nào của FR-029; không đoán vai trò theo tên file) — `hooks/post_gen_project.py:5`: `for path in Path(".").glob("**/*.sh"):`
- Package `scripts/`
  - `scripts/add_latest_release_date.py` — vai trò unknown: agent chưa xác định
  - `scripts/prepare_release.py` — vai trò unknown: agent chưa xác định

## Lời gọi HTTP ra ngoài

- (không có)

## Contract chưa gán được component

- (không có)

## Đối chiếu với dữ liệu kiến trúc

- Trạng thái: not_evaluated
- reason: Chưa được cấp archdia.json cùng snapshot

## Giới hạn

- `DIAGRAM_NOT_PROVIDED`: Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- `ARCHITECTURE_NOT_EVALUATED`: Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- `OUT_OF_SCOPE_FILES`: conditional_out: 2 file, migration: 6 file, test: 15 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- `CLAIMS_REJECTED`: 4 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
