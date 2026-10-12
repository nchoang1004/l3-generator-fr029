Route cần kiểm (5/5):
- POST /api/v1/auth/verify — handler app/auth/adapter/input/api/v1/auth.py::verify_token (fact fact:e90d05cf)
- POST /api/v1/auth/refresh — handler app/auth/adapter/input/api/v1/auth.py::refresh_token (fact fact:af7b4be0)
- GET /api/v1/user — handler app/user/adapter/input/api/v1/user.py::get_user_list (fact fact:6d1390d5)
- POST /api/v1/user/login — handler app/user/adapter/input/api/v1/user.py::login (fact fact:a1310982)
- POST /api/v1/user — handler app/user/adapter/input/api/v1/user.py::create_user (fact fact:cc2f2fe5)

File cần kiểm vai trò (15/83):
- core/fastapi/middlewares/authentication.py
- app/user/domain/repository/user.py
- celery_task/tasks/__init__.py
- core/db/__init__.py
- app/auth/adapter/__init__.py
- app/auth/adapter/input/api/__init__.py
- app/auth/application/service/jwt.py
- core/db/session.py
- app/user/adapter/output/__init__.py
- core/repository/enum.py
- app/auth/application/dto/__init__.py
- core/fastapi/dependencies/permission.py
- app/user/domain/entity/user.py
- core/helpers/cache/__init__.py
- core/repository/__init__.py

Lời gọi HTTP ra ngoài (tất cả 0):
- (không có)
