Route cần kiểm (10/23):
- DELETE /api/v1/items/{id} — handler backend/app/api/routes/items.py::delete_item (fact fact:ddf057be)
- POST /api/v1/items/ — handler backend/app/api/routes/items.py::create_item (fact fact:dbe43f55)
- POST /api/v1/password-recovery-html-content/{email} — handler backend/app/api/routes/login.py::recover_password_html_content (fact fact:a0dd8ac9)
- POST /api/v1/reset-password/ — handler backend/app/api/routes/login.py::reset_password (fact fact:49bb544d)
- PATCH /api/v1/users/me/password — handler backend/app/api/routes/users.py::update_password_me (fact fact:aba3ca42)
- DELETE /api/v1/users/me — handler backend/app/api/routes/users.py::delete_user_me (fact fact:0d60d6c6)
- GET /api/v1/users/me — handler backend/app/api/routes/users.py::read_user_me (fact fact:73c5a9bc)
- PATCH /api/v1/users/me — handler backend/app/api/routes/users.py::update_user_me (fact fact:c43666f0)
- PATCH /api/v1/users/{user_id} — handler backend/app/api/routes/users.py::update_user (fact fact:653f8651)
- POST /api/v1/users/signup — handler backend/app/api/routes/users.py::register_user (fact fact:889edaa8)

File cần kiểm vai trò (15/22):
- backend/app/__init__.py
- backend/app/api/__init__.py
- backend/app/api/main.py
- backend/app/crud.py
- backend/app/api/routes/private.py
- backend/app/core/config.py
- backend/app/api/deps.py
- backend/app/models.py
- backend/app/api/routes/items.py
- backend/app/api/routes/utils.py
- backend/app/api/routes/users.py
- backend/app/api/routes/login.py
- backend/pyproject.toml
- backend/app/utils.py
- backend/app/initial_data.py

Lời gọi HTTP ra ngoài (tất cả 0):
- (không có)
