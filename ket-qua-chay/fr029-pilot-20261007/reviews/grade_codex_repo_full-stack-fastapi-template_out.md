```json
{
  "reviewer": "GPT-6",
  "repo": "full-stack-fastapi-template",
  "checked": {
    "routes": 10,
    "files": 15,
    "http_calls": 0
  },
  "errors": [
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "route",
      "item": "DELETE /api/v1/users/me — fact:0d60d6c6",
      "field": "response_model",
      "doc_value": "unknown — Kiểu trả về được khai báo là Any, không phải model của repository.",
      "correct_value": "Message, một object; decorator khai response_model=Message. OpenAPI phải có response application/json tham chiếu Message.",
      "evidence": "backend/app/api/routes/users.py:132; backend/app/models.py:116",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "route",
      "item": "POST /api/v1/password-recovery-html-content/{email} — fact:a0dd8ac9",
      "field": "response",
      "doc_value": "Response unknown; OpenAPI ghi nội dung response chưa xác định và không có content.",
      "correct_value": "Phần đã biết phải ghi HTMLResponse theo decorator và giá trị trả về; OpenAPI mô tả text/html với schema string. Không có model Pydantic cụ thể.",
      "evidence": "backend/app/api/routes/login.py:5; backend/app/api/routes/login.py:103; backend/app/api/routes/login.py:121",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "route",
      "item": "DELETE /api/v1/items/{id} — fact:ddf057be",
      "field": "parameters.id.type",
      "doc_value": "string; OpenAPI không có format.",
      "correct_value": "uuid.UUID; biểu diễn OpenAPI là string với format uuid.",
      "evidence": "backend/app/api/routes/items.py:1; backend/app/api/routes/items.py:101",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "route",
      "item": "PATCH /api/v1/users/{user_id} — fact:653f8651",
      "field": "parameters.user_id.type",
      "doc_value": "string; OpenAPI không có format.",
      "correct_value": "uuid.UUID; biểu diễn OpenAPI là string với format uuid.",
      "evidence": "backend/app/api/routes/users.py:1; backend/app/api/routes/users.py:190",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "model",
      "item": "ItemPublic.id",
      "field": "type",
      "doc_value": "string; OpenAPI không có format.",
      "correct_value": "uuid.UUID; OpenAPI string với format uuid.",
      "evidence": "backend/app/models.py:105",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "model",
      "item": "ItemPublic.owner_id",
      "field": "type",
      "doc_value": "string; OpenAPI không có format.",
      "correct_value": "uuid.UUID; OpenAPI string với format uuid.",
      "evidence": "backend/app/models.py:106",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "model",
      "item": "ItemPublic.created_at",
      "field": "type",
      "doc_value": "string, nullable=true; OpenAPI không có format.",
      "correct_value": "datetime | None; nhánh string trong OpenAPI có format date-time.",
      "evidence": "backend/app/models.py:2; backend/app/models.py:107",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "model",
      "item": "UserPublic.id",
      "field": "type",
      "doc_value": "string; OpenAPI không có format.",
      "correct_value": "uuid.UUID; OpenAPI string với format uuid.",
      "evidence": "backend/app/models.py:64",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "model",
      "item": "UserPublic.created_at",
      "field": "type",
      "doc_value": "string, nullable=true; OpenAPI không có format.",
      "correct_value": "datetime | None; nhánh string trong OpenAPI có format date-time.",
      "evidence": "backend/app/models.py:2; backend/app/models.py:65",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "model",
      "item": "UserPublic.email",
      "field": "type",
      "doc_value": "string; OpenAPI không có format.",
      "correct_value": "EmailStr kế thừa từ UserBase; OpenAPI string với format email.",
      "evidence": "backend/app/models.py:4; backend/app/models.py:15; backend/app/models.py:63",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "model",
      "item": "UserRegister.email",
      "field": "type",
      "doc_value": "string; OpenAPI không có format.",
      "correct_value": "EmailStr; OpenAPI string với format email.",
      "evidence": "backend/app/models.py:4; backend/app/models.py:27",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "model",
      "item": "UserUpdate.email",
      "field": "type",
      "doc_value": "string, nullable=true; OpenAPI không có format.",
      "correct_value": "EmailStr | None; nhánh string trong OpenAPI có format email.",
      "evidence": "backend/app/models.py:4; backend/app/models.py:34",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "model",
      "item": "UserUpdateMe.email",
      "field": "type",
      "doc_value": "string, nullable=true; OpenAPI không có format.",
      "correct_value": "EmailStr | None; nhánh string trong OpenAPI có format email.",
      "evidence": "backend/app/models.py:4; backend/app/models.py:43",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "route",
      "item": "Các route mẫu có auth: fact:ddf057be, fact:dbe43f55, fact:a0dd8ac9, fact:aba3ca42, fact:0d60d6c6, fact:73c5a9bc, fact:c43666f0, fact:653f8651",
      "field": "openapi.security",
      "doc_value": "Bảng ghi OAuth2 bearer và dependency xác thực, nhưng khối OpenAPI không có securitySchemes hoặc security.",
      "correct_value": "Khai security scheme OAuth2 password với tokenUrl=/api/v1/login/access-token và security requirement trên tám operation này; giữ thông tin kiểm tra active/superuser bằng mô tả hoặc extension.",
      "evidence": "backend/app/api/deps.py:16; backend/app/api/deps.py:27; backend/app/api/deps.py:30; backend/app/api/deps.py:49; backend/app/api/deps.py:52; backend/app/core/config.py:22",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "role",
      "item": "backend/app/api/deps.py",
      "field": "evidence",
      "doc_value": "Truy cập dữ liệu; bằng chứng dòng 22: with Session(engine) as session:",
      "correct_value": "Vai trò đúng, nhưng bằng chứng trực tiếp khớp dấu hiệu gọi method trên session là dòng 41: user = session.get(User, token_data.sub). Dòng 22 chỉ tạo và quản lý session.",
      "evidence": "backend/app/api/deps.py:22; backend/app/api/deps.py:41",
      "confidence": "chắc"
    },
    {
      "fixture": "full-stack-fastapi-template",
      "kind": "limitation",
      "item": "backend/app/utils.py::send_email",
      "field": "unsupported_io",
      "doc_value": "README và result.json không nêu giới hạn đối với thư viện emails.",
      "correct_value": "Nêu thư viện I/O emails và nơi gọi message.send(to=email_to, smtp=smtp_options) trong phần giới hạn theo Phạm vi đọc FR-028. Đây là SMTP, không phải lời gọi HTTP.",
      "evidence": "backend/app/utils.py:7; backend/app/utils.py:47; backend/app/utils.py:56",
      "confidence": "chắc"
    }
  ]
}
```