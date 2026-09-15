"""Dựng ground_truth_template.json — repo thứ hai, chọn vì có ba ca khó.

Ba ca khó mà repo dispatch không có:

1. Prefix cấp ứng dụng là BIẾN, không phải chuỗi hằng:
   `app.include_router(api_router, prefix=settings.API_V1_STR)` (app/main.py:35).
   Theo SPEC mục 6c.1, công cụ phải ghi `{settings.API_V1_STR}` và hạ `partial`,
   KHÔNG được đoán ra giá trị "/api/v1".
2. Route đăng ký trong khối `if`:
   `if settings.FASTAPI_ENV == "development": api_router.include_router(private.router)`
   (app/api/main.py:13-14). SPEC mục 8.5.4 nêu đây là nguồn báo thừa điển hình.
3. Một file lỗi cú pháp thật: app/api/deps.py:36 dùng cú pháp `except A, B:` của
   Python 2. Công cụ phải bỏ qua file đó và chạy tiếp.

Chạy: python evaluation/_build_ground_truth_template.py
"""

import json
import pathlib

MOUNT_EXPR = "/{settings.API_V1_STR}"

# (file, dòng, METHOD, đường dẫn sau khi ghép prefix của router, tên hàm, prefix router)
ROUTES_RAW = [
    ("items.py", 13, "GET", "/items/", "read_items", "/items"),
    ("items.py", 48, "GET", "/items/{id}", "read_item", "/items"),
    ("items.py", 61, "POST", "/items/", "create_item", "/items"),
    ("items.py", 75, "PUT", "/items/{id}", "update_item", "/items"),
    ("items.py", 99, "DELETE", "/items/{id}", "delete_item", "/items"),
    ("login.py", 23, "POST", "/login/access-token", "login_access_token", ""),
    ("login.py", 45, "POST", "/login/test-token", "test_token", ""),
    ("login.py", 53, "POST", "/password-recovery/{email}", "recover_password", ""),
    ("login.py", 77, "POST", "/reset-password/", "reset_password", ""),
    ("login.py", 100, "POST", "/password-recovery-html-content/{email}",
     "recover_password_html_content", ""),
    ("private.py", 23, "POST", "/private/users/", "create_user", "/private"),
    ("users.py", 32, "GET", "/users/", "read_users", "/users"),
    ("users.py", 54, "POST", "/users/", "create_user", "/users"),
    ("users.py", 81, "PATCH", "/users/me", "update_user_me", "/users"),
    ("users.py", 103, "PATCH", "/users/me/password", "update_password_me", "/users"),
    ("users.py", 124, "GET", "/users/me", "read_user_me", "/users"),
    ("users.py", 132, "DELETE", "/users/me", "delete_user_me", "/users"),
    ("users.py", 146, "POST", "/users/signup", "register_user", "/users"),
    ("users.py", 162, "GET", "/users/{user_id}", "read_user_by_id", "/users"),
    ("users.py", 182, "PATCH", "/users/{user_id}", "update_user", "/users"),
    ("users.py", 214, "DELETE", "/users/{user_id}", "delete_user", "/users"),
    ("utils.py", 11, "POST", "/utils/test-email/", "test_email", "/utils"),
    ("utils.py", 29, "GET", "/utils/health-check/", "health_check", "/utils"),
]

routes = []
for short, line, method, path, func, rp in ROUTES_RAW:
    r = {
        "method": method,
        "path": path,
        "path_with_mount": "/api/v1" + path,
        "file": "app/api/routes/" + short,
        "line": line,
        "function": func,
        "router_prefix": rp,
    }
    if short == "private.py":
        r["conditional"] = (
            'chỉ đăng ký khi settings.FASTAPI_ENV == "development" '
            "(app/api/main.py:13-14). Vẫn tính là route có thật vì nó tồn tại trong "
            "code; kiểm tra riêng xem công cụ có nêu điều kiện này không."
        )
    routes.append(r)

entities = [
    {
        "class_name": "User",
        "file": "app/models.py",
        "line": 52,
        "table_name": "user",
        "table_name_source": "SQLModel sinh mặc định = tên class viết thường",
        "table_name_evidence": "không khai __tablename__; class một từ nên quy ước viết thường ra đúng",
    },
    {
        "class_name": "Item",
        "file": "app/models.py",
        "line": 91,
        "table_name": "item",
        "table_name_source": "SQLModel sinh mặc định = tên class viết thường",
        "table_name_evidence": "không khai __tablename__; class một từ",
    },
]

gt = {
    "meta": {
        "repo": "fastapi/full-stack-fastapi-template",
        "commit": "cb740b656d7a0a6c5e12c7bf8e50343ec94ee9c7",
        "local_path": "sample-repos/full-stack-fastapi-template/backend",
        "ngay_lap": "2026-09-15",
        "nguoi_lap": (
            "Agent (Claude Opus 5) đọc tay source. KHÔNG phải hai kỹ sư đọc độc lập "
            "như SPEC mục 8.5.1 yêu cầu."
        ),
        "quy_trinh": "Lập ground truth trước khi chạy công cụ trên repo này.",
        "ly_do_chon": (
            "Repo dispatch không có route đăng ký trong if, không có prefix là biến, "
            "và không có file lỗi cú pháp. Repo này có cả ba."
        ),
        "scope_dirs": ["app/"],
        "so_file_trong_pham_vi": 25,
        "pham_vi_external_call": "app/ — repo này không có lời gọi HTTP ra ngoài nào",
        "app_prefix_expr": MOUNT_EXPR,
        "app_prefix_note": (
            "app/main.py:35 có app.include_router(api_router, prefix=settings.API_V1_STR). "
            "Giá trị thật là /api/v1 (app/core/config.py:22) nhưng chỉ biết khi chạy. "
            "Công cụ ĐÚNG khi ghi /{settings.API_V1_STR} và hạ partial; "
            "công cụ SAI nếu đoán ra /api/v1."
        ),
        "parse_error_expected": {
            "file": "app/api/deps.py",
            "line": 36,
            "why": "except InvalidTokenError, ValidationError: — cú pháp Python 2",
        },
    },
    "routes": routes,
    "entities": entities,
    "external_calls": [],
    "external_calls_borderline": [],
    "false_positive_traps": [],
    "ngoai_dinh_nghia_spec": {},
    "thong_ke": {"routes": len(routes), "entities": len(entities), "external_calls": 0},
}

out = pathlib.Path("evaluation/ground_truth_template.json")
out.write_text(json.dumps(gt, indent=2, ensure_ascii=False), encoding="utf-8")
print("Da ghi", out, gt["thong_ke"])
