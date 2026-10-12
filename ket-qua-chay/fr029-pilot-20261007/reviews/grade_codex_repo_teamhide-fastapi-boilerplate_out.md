```json
{
  "reviewer": "GPT-6",
  "repo": "teamhide-fastapi-boilerplate",
  "checked": {"routes": 5, "files": 15, "http_calls": 0},
  "errors": [
    {
      "fixture": "teamhide-fastapi-boilerplate",
      "kind": "role",
      "item": "core/fastapi/dependencies/permission.py",
      "field": "role",
      "doc_value": "Khác (exact: Không có dấu hiệu nào của FR-029)",
      "correct_value": "Service (inferred: nằm trên đường gọi). Dependency của GET /api/v1/user gọi IsAdmin.has_permission → UserService.is_admin → UserRepositoryAdapter.get_user_by_id → UserSQLAlchemyRepo.get_user_by_id, nơi thực hiện truy vấn CSDL.",
      "evidence": "app/user/adapter/input/api/v1/user.py:18; core/fastapi/dependencies/permission.py:66; core/fastapi/dependencies/permission.py:49; app/container.py:13; app/container.py:14; app/container.py:15; app/user/application/service/user.py:49; app/user/adapter/output/persistence/repository_adapter.py:30; app/user/adapter/output/persistence/sqlalchemy/user.py:43",
      "confidence": "chắc"
    },
    {
      "fixture": "teamhide-fastapi-boilerplate",
      "kind": "route",
      "item": "GET /api/v1/user (fact:6d1390d5)",
      "field": "openapi.security",
      "doc_value": "Bảng ghi PermissionDependency([IsAdmin]), nhưng OpenAPI không có security hoặc components.securitySchemes.",
      "correct_value": "OpenAPI phải biểu diễn security scheme PermissionDependency với type=apiKey, in=header, name=Authorization và gắn yêu cầu này vào operation GET /api/v1/user; ghi yêu cầu IsAdmin trong mô tả hoặc extension.",
      "evidence": "app/user/adapter/input/api/v1/user.py:18; core/fastapi/dependencies/permission.py:57; core/fastapi/dependencies/permission.py:60; core/fastapi/dependencies/permission.py:61; tech-specs/TOAN-BO/api/API-TEAMHIDE-FASTAPI-BOILERPLATE-TOAN-BO-v1.md:407",
      "confidence": "chắc"
    },
    {
      "fixture": "teamhide-fastapi-boilerplate",
      "kind": "label",
      "item": "POST /api/v1/auth/verify (fact:e90d05cf)",
      "field": "status",
      "doc_value": "200 (suy theo fastapi.default_status_200)",
      "correct_value": "200 được khai trực tiếp trong return Response(status_code=200); bằng chứng và nhãn của riêng status phải là exact.",
      "evidence": "app/auth/adapter/input/api/v1/auth.py:37; tech-specs/TOAN-BO/api/API-TEAMHIDE-FASTAPI-BOILERPLATE-TOAN-BO-v1.md:25",
      "confidence": "chắc"
    }
  ]
}
```