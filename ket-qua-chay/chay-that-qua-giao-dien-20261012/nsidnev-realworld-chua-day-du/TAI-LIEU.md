# nsidnev_fastapi-realworld-example-app — tài liệu API

Bản sinh tự động từ source, chưa được chủ repository duyệt. File này dành cho người đọc; dữ liệu đầy đủ cho máy nằm ở `result.json` và các file ở phụ lục.

| Mục | Giá trị |
|---|---|
| Tình trạng | Chưa đủ — còn lỗi sau 2 vòng sửa, xem mục 11 |
| Đọc source | 71/71 file trong phạm vi |
| Endpoint | 14 |
| Model | 12 |
| Bảng CSDL | 0; có bảng chưa đọc được, xem mục 11 |
| Sự kiện, tác vụ nền | 0 điểm gửi/nhận |
| Gọi HTTP ra ngoài | 0 |
| Sinh bởi | model gpt-5-2025-08-07, prompt fr029-oneshot-prompt-v6; bảng, sự kiện, thư viện, cấu hình, middleware đọc tĩnh từ code |

Cách đọc nhãn: **chắc chắn** — đọc thẳng từ một dòng code; **suy luận** — theo quy tắc mặc định của framework, lý do ở chú thích [n]; **chưa rõ** — source không đủ để kết luận; **AI viết** — câu chữ do model viết, chỉ để đọc nhanh, không phải dữ kiện đã kiểm.

## 1. Danh sách endpoint

| # | Method | Path | Vào | Ra | Status | Auth |
|---|---|---|---|---|---|---|
| 1 | GET | /api/articles | — | ListOfArticlesInResponse | 200 | Header Authorization qua APIKeyHeader (tùy chọn) |
| 2 | POST | /api/articles | application/json: article | ArticleInResponse | 201 | Header Authorization qua APIKeyHeader |
| 3 | GET | /api/articles/feed | — | ListOfArticlesInResponse | 200 | Header Authorization qua APIKeyHeader |
| 4 | GET | /api/articles/{slug} | — | ArticleInResponse | 200 | Header Authorization qua APIKeyHeader (tùy chọn) |
| 5 | DELETE | /api/articles/{slug}/favorite | — | ArticleInResponse | 200 | Header Authorization qua APIKeyHeader |
| 6 | POST | /api/articles/{slug}/favorite | — | ArticleInResponse | 200 | Header Authorization qua APIKeyHeader |
| 7 | GET | /api/profiles/{username} | — | ProfileInResponse | 200 | Header Authorization qua APIKeyHeader (tùy chọn) |
| 8 | DELETE | /api/profiles/{username}/follow | — | ProfileInResponse | 200 | Header Authorization qua APIKeyHeader |
| 9 | POST | /api/profiles/{username}/follow | — | ProfileInResponse | 200 | Header Authorization qua APIKeyHeader |
| 10 | GET | /api/tags | — | TagsInList | 200 | chưa rõ |
| 11 | GET | /api/user | — | UserInResponse | 200 | Header Authorization qua APIKeyHeader |
| 12 | PUT | /api/user | application/json: user | UserInResponse | 200 | Header Authorization qua APIKeyHeader |
| 13 | POST | /api/users | application/json: user | UserInResponse | 201 | chưa rõ |
| 14 | POST | /api/users/login | application/json: user | UserInResponse | 200 | chưa rõ |

## 2. Chi tiết từng endpoint

### 1. GET /api/articles

- Mô tả (AI viết): Liệt kê bài viết theo bộ lọc truy vấn.
- Hàm xử lý: `list_articles` tại `app/api/routes/articles/articles_resource.py:30`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | tag | query | string | không |
  | author | query | string | không |
  | favorited | query | string | không |
  | limit | query | integer | không |
  | offset | query | integer | không |
  | Authorization | header | string | không |

- Trả về: ListOfArticlesInResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_articles_filters, get_current_user_authorizer, get_repository
- Auth: Header Authorization qua APIKeyHeader (tùy chọn)
- Nhóm (tags): articles
- Mức chắc chắn: suy luận [1][2][3][4][5]

### 2. POST /api/articles

- Mô tả (AI viết): Tạo bài viết mới.
- Hàm xử lý: `create_new_article` tại `app/api/routes/articles/articles_resource.py:53`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | Authorization | header | string | có |

- Body: application/json: article
- Trả về: ArticleInResponse
- Status: 201 (khai trong code)
- Dependency: get_current_user_authorizer, get_repository
- Auth: Header Authorization qua APIKeyHeader
- Nhóm (tags): articles
- Đường gọi tới dữ liệu (suy luận từ vai trò Service): `app/api/routes/articles/articles_resource.py:65` → `app/services/articles.py:9` → `app/db/repositories/articles.py:243`
- Mức chắc chắn: suy luận [2][6][4][7]

### 3. GET /api/articles/feed

- Mô tả (AI viết): Lấy danh sách bài viết trong nguồn tin của người dùng hiện tại.
- Hàm xử lý: `get_articles_for_user_feed` tại `app/api/routes/articles/articles_common.py:22`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | limit | query | integer | không |
  | offset | query | integer | không |
  | Authorization | header | string | có |

- Trả về: ListOfArticlesInResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_current_user_authorizer, get_repository
- Auth: Header Authorization qua APIKeyHeader
- Nhóm (tags): articles
- Mức chắc chắn: suy luận [1][2][4][7]

### 4. GET /api/articles/{slug}

- Mô tả (AI viết): Lấy bài viết theo slug.
- Hàm xử lý: `retrieve_article_by_slug` tại `app/api/routes/articles/articles_resource.py:82`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | slug | path | string | có |
  | Authorization | header | string | không |

- Trả về: ArticleInResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_article_by_slug_from_path
- Auth: Header Authorization qua APIKeyHeader (tùy chọn)
- Nhóm (tags): articles
- Đường gọi tới dữ liệu (suy luận từ vai trò Service): `app/api/routes/articles/articles_resource.py:84` → `app/api/dependencies/articles.py:43` → `app/db/repositories/articles.py:243`
- Mức chắc chắn: suy luận [1][2][4][7]

### 5. DELETE /api/articles/{slug}/favorite

- Mô tả (AI viết): Bỏ đánh dấu yêu thích khỏi bài viết.
- Hàm xử lý: `remove_article_from_favorites` tại `app/api/routes/articles/articles_common.py:77`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | slug | path | string | có |
  | Authorization | header | string | có |

- Trả về: ArticleInResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_article_by_slug_from_path, get_current_user_authorizer, get_repository
- Auth: Header Authorization qua APIKeyHeader
- Nhóm (tags): articles
- Mức chắc chắn: suy luận [1][2][4][7]

### 6. POST /api/articles/{slug}/favorite

- Mô tả (AI viết): Đánh dấu bài viết là yêu thích.
- Hàm xử lý: `mark_article_as_favorite` tại `app/api/routes/articles/articles_common.py:47`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | slug | path | string | có |
  | Authorization | header | string | có |

- Trả về: ArticleInResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_article_by_slug_from_path, get_current_user_authorizer, get_repository
- Auth: Header Authorization qua APIKeyHeader
- Nhóm (tags): articles
- Mức chắc chắn: suy luận [1][2][4][7]

### 7. GET /api/profiles/{username}

- Mô tả (AI viết): Lấy hồ sơ theo username.
- Hàm xử lý: `retrieve_profile_by_username` tại `app/api/routes/profiles.py:16`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | username | path | string | có |
  | Authorization | header | string | không |

- Trả về: ProfileInResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_profile_by_username_from_path
- Auth: Header Authorization qua APIKeyHeader (tùy chọn)
- Nhóm (tags): profiles
- Đường gọi tới dữ liệu (suy luận từ vai trò Service): `app/api/routes/profiles.py:22` → `app/api/dependencies/profiles.py:21` → `app/db/repositories/profiles.py:25`
- Mức chắc chắn: suy luận [1][2][4][7]

### 8. DELETE /api/profiles/{username}/follow

- Mô tả (AI viết): Bỏ theo dõi người dùng theo username.
- Hàm xử lý: `unsubscribe_from_user` tại `app/api/routes/profiles.py:57`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | username | path | string | có |
  | Authorization | header | string | có |

- Trả về: ProfileInResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_profile_by_username_from_path, get_current_user_authorizer, get_repository
- Auth: Header Authorization qua APIKeyHeader
- Nhóm (tags): profiles
- Mức chắc chắn: suy luận [1][2][4][7]

### 9. POST /api/profiles/{username}/follow

- Mô tả (AI viết): Theo dõi người dùng theo username.
- Hàm xử lý: `follow_for_user` tại `app/api/routes/profiles.py:27`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | username | path | string | có |
  | Authorization | header | string | có |

- Trả về: ProfileInResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_profile_by_username_from_path, get_current_user_authorizer, get_repository
- Auth: Header Authorization qua APIKeyHeader
- Nhóm (tags): profiles
- Mức chắc chắn: suy luận [1][2][4][7]

### 10. GET /api/tags

- Mô tả (AI viết): Lấy toàn bộ thẻ.
- Hàm xử lý: `get_all_tags` tại `app/api/routes/tags.py:10`
- Tham số: không có
- Trả về: TagsInList
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_repository
- Auth: chưa rõ — Endpoint không yêu cầu xác thực
- Nhóm (tags): tags
- Mức chắc chắn: suy luận [1][4][8]
- Còn thiếu: Trường chưa xác định: auth

### 11. GET /api/user

- Mô tả (AI viết): Lấy thông tin người dùng hiện tại.
- Hàm xử lý: `retrieve_current_user` tại `app/api/routes/users.py:18`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | Authorization | header | string | có |

- Trả về: UserInResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_current_user_authorizer, get_app_settings
- Auth: Header Authorization qua APIKeyHeader
- Nhóm (tags): users
- Mức chắc chắn: suy luận [1][2][4][7]

### 12. PUT /api/user

- Mô tả (AI viết): Cập nhật thông tin người dùng hiện tại.
- Hàm xử lý: `update_current_user` tại `app/api/routes/users.py:38`
- Tham số:

  | Tên | Ở đâu | Kiểu | Bắt buộc |
  |---|---|---|---|
  | Authorization | header | string | có |

- Body: application/json: user
- Trả về: UserInResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_current_user_authorizer, get_repository, get_app_settings
- Auth: Header Authorization qua APIKeyHeader
- Nhóm (tags): users
- Đường gọi tới dữ liệu (suy luận từ vai trò Service): `app/api/routes/users.py:46` → `app/services/authentication.py:5` → `app/db/repositories/users.py:19`
- Mức chắc chắn: suy luận [1][2][6][4][5]

### 13. POST /api/users

- Mô tả (AI viết): Đăng ký người dùng mới.
- Hàm xử lý: `register` tại `app/api/routes/authentication.py:56`
- Tham số: không có
- Body: application/json: user
- Trả về: UserInResponse
- Status: 201 (khai trong code)
- Dependency: get_repository, get_app_settings
- Auth: chưa rõ — Endpoint không yêu cầu xác thực
- Nhóm (tags): authentication
- Mức chắc chắn: suy luận [6][4][8]
- Còn thiếu: Trường chưa xác định: auth

### 14. POST /api/users/login

- Mô tả (AI viết): Đăng nhập người dùng bằng email và mật khẩu.
- Hàm xử lý: `login` tại `app/api/routes/authentication.py:22`
- Tham số: không có
- Body: application/json: user
- Trả về: UserInResponse
- Status: 200 (mặc định của framework, xem chú thích)
- Dependency: get_repository, get_app_settings
- Auth: chưa rõ — Endpoint không yêu cầu xác thực
- Nhóm (tags): authentication
- Mức chắc chắn: suy luận [1][6][4][7]
- Còn thiếu: Trường chưa xác định: auth

Chú thích:

[1] Decorator không khai status_code; FastAPI dùng status mặc định 200 của JSONResponse  
[2] Tham số Header: FastAPI đổi dấu _ trong tên biến thành - trong tên header  
[3] Tham số kiểu đơn, không có trong path, không khai Query/Header/Cookie; FastAPI coi là query  
[4] Prefix là giá trị mặc định khai trong lớp Settings; biến môi trường có thể ghi đè lúc chạy  
[5] ; ; ;  
[6] Body là Pydantic model; FastAPI nhận application/json  
[7] ; ;  
[8] ;  

## 3. Model dữ liệu

### ArticleForResponse

Khai ở `app/models/schemas/articles.py:12`. Mức chắc chắn: suy luận [1][2].

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| slug | string | có | không |
| title | string | có | không |
| description | string | có | không |
| body | string | có | không |
| tags (tên JSON: tagList) | list[string] | có | không |
| author | Profile | có | không |
| favorited | boolean | có | không |
| favorites_count | integer | có | không |
| created_at | string(date-time) | không | không |
| updated_at | string(date-time) | không | không |
| id_ (tên JSON: id) | integer | không | không |

### ArticleInCreate

Khai ở `app/models/schemas/articles.py:20`. Mức chắc chắn: suy luận [1].

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| title | string | có | không |
| description | string | có | không |
| body | string | có | không |
| tags (tên JSON: tagList) | list[string] | không | không |

### ArticleInResponse

Khai ở `app/models/schemas/articles.py:16`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| article | ArticleForResponse | có | không |

### ListOfArticlesInResponse

Khai ở `app/models/schemas/articles.py:33`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| articles | list[ArticleForResponse] | có | không |
| articles_count | integer | có | không |

### Profile

Khai ở `app/models/domain/profiles.py:6`. Mức chắc chắn: suy luận [1].

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| username | string | có | không |
| bio | string | không | không |
| image | string | không | có |
| following | boolean | không | không |

### ProfileInResponse

Khai ở `app/models/schemas/profiles.py:6`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| profile | Profile | có | không |

### TagsInList

Khai ở `app/models/schemas/tags.py:6`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| tags | list[string] | có | không |

### UserInCreate

Khai ở `app/models/schemas/users.py:14`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| email | string(email) | có | không |
| password | string | có | không |
| username | string | có | không |

### UserInLogin

Khai ở `app/models/schemas/users.py:9`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| email | string(email) | có | không |
| password | string | có | không |

### UserInResponse

Khai ở `app/models/schemas/users.py:30`. Mức chắc chắn: chắc chắn.

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| user | UserWithToken | có | không |

### UserInUpdate

Khai ở `app/models/schemas/users.py:18`. Mức chắc chắn: suy luận [1][3].

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| username | string | không | có |
| email | string(email) | không | có |
| password | string | không | có |
| bio | string | không | có |
| image | string | không | có |

### UserWithToken

Khai ở `app/models/schemas/users.py:26`. Mức chắc chắn: suy luận [1].

| Trường | Kiểu | Bắt buộc | Được null |
|---|---|---|---|
| username | string | có | không |
| email | string | có | không |
| bio | string | không | không |
| image | string | không | có |
| token | string | có | không |

Chú thích:

[1] Pydantic v1: trường Optional không có default được mặc định None, nên không bắt buộc  
[2] ; Bộ kiểm chưa đối chiếu được kiểu/required/nullable với khai báo của: created_at, updated_at  
[3] ; Bộ kiểm chưa đối chiếu được kiểu/required/nullable với khai báo của: image  

## 4. Bảng CSDL

Không thấy bảng nào khai bằng SQLAlchemy/SQLModel trong phạm vi đọc. Có bảng khai theo cách chưa đọc được, xem mục 11.

## 5. Sự kiện và tác vụ nền

Không thấy điểm gửi/nhận qua Kafka, FastStream, Celery hay BackgroundTasks.

## 6. Cấu trúc code

Vai trò của từng file theo dấu hiệu trong code (FR-029). Chỉ liệt kê component thường.

### Khởi tạo FastAPI ứng dụng

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `app/main.py` | Điểm vào | `app/main.py:18` |

Không có vai trò: 2 file rỗng.

### Định nghĩa router API

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `app/api/errors/http_error.py` | Khác | `app/api/errors/http_error.py:6` |
| `app/api/errors/validation_error.py` | Khác | `app/api/errors/validation_error.py:12` |
| `app/api/routes/api.py` | Khác | `app/api/routes/api.py:7` |
| `app/api/routes/articles/api.py` | Khác | `app/api/routes/articles/api.py:7` |
| `app/api/routes/articles/articles_common.py` | Route | `app/api/routes/articles/articles_common.py:22` |
| `app/api/routes/articles/articles_resource.py` | Route | `app/api/routes/articles/articles_resource.py:30` |
| `app/api/routes/authentication.py` | Route | `app/api/routes/authentication.py:22` |
| `app/api/routes/comments.py` | Route | `app/api/routes/comments.py:26` |
| `app/api/routes/profiles.py` | Route | `app/api/routes/profiles.py:16` |
| `app/api/routes/tags.py` | Route | `app/api/routes/tags.py:10` |
| `app/api/routes/users.py` | Route | `app/api/routes/users.py:18` |

Không có vai trò: 3 file rỗng.

### Logic nghiệp vụ dịch vụ

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `app/services/articles.py` | Service | đường gọi `app/api/routes/articles/articles_resource.py:65` → `app/services/articles.py:9` → `app/db/repositories/articles.py:243` |
| `app/services/authentication.py` | Service | đường gọi `app/api/routes/users.py:46` → `app/services/authentication.py:5` → `app/db/repositories/users.py:19` |
| `app/services/comments.py` | Khác | `app/services/comments.py:5` |
| `app/services/jwt.py` | Khác | `app/services/jwt.py:27` |
| `app/services/security.py` | Khác | `app/services/security.py:11` |

Không có vai trò: 1 file rỗng.

### Truy cập dữ liệu repository

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `app/db/queries/queries.py` | Khác | `app/db/queries/queries.py:5` |
| `app/db/queries/tables.py` | Khác | `app/db/queries/tables.py:12` |
| `app/db/repositories/articles.py` | Truy cập dữ liệu | `app/db/repositories/articles.py:45` |
| `app/db/repositories/base.py` | Khác | `app/db/repositories/base.py:4` |
| `app/db/repositories/comments.py` | Truy cập dữ liệu | `app/db/repositories/comments.py:26` |
| `app/db/repositories/profiles.py` | Truy cập dữ liệu | `app/db/repositories/profiles.py:25` |
| `app/db/repositories/tags.py` | Truy cập dữ liệu | `app/db/repositories/tags.py:9` |
| `app/db/repositories/users.py` | Truy cập dữ liệu | `app/db/repositories/users.py:11` |

Không có vai trò: 2 file rỗng.

### Kết nối cơ sở dữ liệu

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `app/db/events.py` | Hạ tầng | `app/db/events.py:11` |

### Dùng chung

| File | Vai trò | Dấu hiệu |
|---|---|---|
| `app/api/dependencies/articles.py` | Service | đường gọi `app/api/routes/articles/articles_resource.py:84` → `app/api/dependencies/articles.py:43` → `app/db/repositories/articles.py:243` |
| `app/api/dependencies/comments.py` | Service | đường gọi `app/api/routes/comments.py:68` → `app/api/dependencies/comments.py:27` → `app/db/repositories/comments.py:26` |
| `app/api/dependencies/database.py` | Hạ tầng | `app/api/dependencies/database.py:26` |
| `app/api/dependencies/profiles.py` | Service | đường gọi `app/api/routes/profiles.py:22` → `app/api/dependencies/profiles.py:21` → `app/db/repositories/profiles.py:25` |
| `app/core/config.py` | Khác | `app/core/config.py:17` |
| `app/core/events.py` | Khác | `app/core/events.py:10` |
| `app/core/logging.py` | Khác | `app/core/logging.py:8` |
| `app/core/settings/app.py` | Khác | `app/core/settings/app.py:12` |
| `app/core/settings/base.py` | Cấu hình | `app/core/settings/base.py:12` |
| `app/core/settings/development.py` | Khác | `app/core/settings/development.py:6` |
| `app/core/settings/production.py` | Khác | `app/core/settings/production.py:4` |
| `app/core/settings/test.py` | Khác | `app/core/settings/test.py:8` |
| `app/db/errors.py` | Khác | `app/db/errors.py:1` |
| `app/models/common.py` | Schema API | `app/models/common.py:6` |
| `app/models/domain/articles.py` | Schema API | `app/models/domain/articles.py:8` |
| `app/models/domain/comments.py` | Schema API | `app/models/domain/comments.py:6` |
| `app/models/domain/profiles.py` | Schema API | `app/models/domain/profiles.py:6` |
| `app/models/domain/rwmodel.py` | Schema API | `app/models/domain/rwmodel.py:17` |
| `app/models/domain/users.py` | Schema API | `app/models/domain/users.py:8` |
| `app/models/schemas/articles.py` | Schema API | `app/models/schemas/articles.py:12` |
| `app/models/schemas/comments.py` | Schema API | `app/models/schemas/comments.py:7` |
| `app/models/schemas/jwt.py` | Khác | `app/models/schemas/jwt.py:6` |
| `app/models/schemas/profiles.py` | Schema API | `app/models/schemas/profiles.py:6` |
| `app/models/schemas/rwschema.py` | Schema API | `app/models/schemas/rwschema.py:4` |
| `app/models/schemas/tags.py` | Schema API | `app/models/schemas/tags.py:6` |
| `app/models/schemas/users.py` | Schema API | `app/models/schemas/users.py:9` |
| `app/resources/strings.py` | Khác | `app/resources/strings.py:3` |

Không có vai trò: 8 file rỗng; chưa xác định vai trò: `app/api/dependencies/authentication.py`.

### Ngoài sơ đồ: (gốc)

### Quan hệ giữa component

Đọc tĩnh từ lời gọi, Depends và chỗ dùng bảng đã nối được tới nơi định nghĩa.

| Từ | Tới | Cách dùng | Số chỗ | Ví dụ |
|---|---|---|---|---|
| Dùng chung | Kết nối cơ sở dữ liệu | gọi hàm | 2 | `app/core/events.py:15` |
| Dùng chung | Logic nghiệp vụ dịch vụ | gọi hàm | 6 | `app/api/dependencies/comments.py:43` |
| Dùng chung | Truy cập dữ liệu repository | gọi hàm | 4 | `app/api/dependencies/profiles.py:21` |
| Khởi tạo FastAPI ứng dụng | Dùng chung | gọi hàm | 3 | `app/main.py:14` |
| Logic nghiệp vụ dịch vụ | Dùng chung | gọi hàm | 3 | `app/services/jwt.py:23` |
| Logic nghiệp vụ dịch vụ | Truy cập dữ liệu repository | gọi hàm | 3 | `app/services/articles.py:11` |
| Truy cập dữ liệu repository | Dùng chung | gọi hàm | 11 | `app/db/repositories/comments.py:38` |
| Định nghĩa router API | Dùng chung | gọi hàm, Depends | 38 | `app/api/routes/comments.py:32` |
| Định nghĩa router API | Logic nghiệp vụ dịch vụ | gọi hàm | 11 | `app/api/routes/users.py:61` |
| Định nghĩa router API | Truy cập dữ liệu repository | gọi hàm | 16 | `app/api/routes/users.py:59` |

## 7. Gọi HTTP ra ngoài

Không có lời gọi nào qua httpx, requests, aiohttp.

## 8. Thư viện

| Thư viện | Phiên bản | Có import trong code | Khai ở |
|---|---|---|---|
| aiosql | ^6.2 | có | `pyproject.toml:18` |
| alembic | ^1.8 | chưa thấy import | `pyproject.toml:20` |
| asyncpg | ^0.26.0 | có | `pyproject.toml:16` |
| databases | ^0.6.1 | chưa thấy import | `pyproject.toml:15` |
| fastapi | ^0.79.1 | có | `pyproject.toml:11` |
| loguru | ^0.6.0 | có | `pyproject.toml:23` |
| passlib | — | có | `pyproject.toml:13` |
| psycopg2-binary | ^2.9.3 | chưa thấy import | `pyproject.toml:17` |
| pydantic | — | có | `pyproject.toml:12` |
| pyjwt | ^2.4 | có | `pyproject.toml:14` |
| pypika | ^0.48.9 | có | `pyproject.toml:19` |
| python-slugify | ^6.1 | có | `pyproject.toml:21` |
| unidecode | ^1.3 | chưa thấy import | `pyproject.toml:22` |
| uvicorn | ^0.18.2 | chưa thấy import | `pyproject.toml:10` |

"Chưa thấy import": tên gói khác tên import, hoặc gói chỉ dùng gián tiếp (driver, plugin, công cụ).

## 9. Cấu hình

| Khóa | Nguồn | Giá trị mặc định | Khai ở |
|---|---|---|---|
| allowed_hosts | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `app/core/settings/app.py:31` |
| api_prefix | lớp Settings | /api | `app/core/settings/app.py:27` |
| app_env | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `app/core/settings/base.py:13` |
| database_url | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `app/core/settings/app.py:21`, `app/core/settings/test.py:15` |
| debug | lớp Settings | False | `app/core/settings/app.py:13` |
| debug | lớp Settings | True | `app/core/settings/development.py:7`, `app/core/settings/test.py:9` |
| docs_url | lớp Settings | /docs | `app/core/settings/app.py:14` |
| jwt_token_prefix | lớp Settings | đã che (dấu hiệu bí mật) | `app/core/settings/app.py:29` |
| loggers | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `app/core/settings/app.py:34` |
| logging_level | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `app/core/settings/app.py:33`, `app/core/settings/development.py:11`, `app/core/settings/test.py:19` |
| max_connection_count | lớp Settings | 10 | `app/core/settings/app.py:22` |
| max_connection_count | lớp Settings | 5 | `app/core/settings/test.py:16` |
| min_connection_count | lớp Settings | 10 | `app/core/settings/app.py:23` |
| min_connection_count | lớp Settings | 5 | `app/core/settings/test.py:17` |
| openapi_prefix | lớp Settings | — | `app/core/settings/app.py:15` |
| openapi_url | lớp Settings | /openapi.json | `app/core/settings/app.py:16` |
| redoc_url | lớp Settings | /redoc | `app/core/settings/app.py:17` |
| secret_key | lớp Settings | đã che (dấu hiệu bí mật) | `app/core/settings/app.py:25`, `app/core/settings/test.py:13` |
| title | lớp Settings | FastAPI example application | `app/core/settings/app.py:18` |
| title | lớp Settings | Dev FastAPI example application | `app/core/settings/development.py:9` |
| title | lớp Settings | Test FastAPI example application | `app/core/settings/test.py:11` |
| version | lớp Settings | 0.0.0 | `app/core/settings/app.py:19` |

## 10. Middleware và xử lý lỗi toàn cục

| Loại | Tên | Ở đâu |
|---|---|---|
| xử lý lỗi | `HTTPException` | `app/main.py:37` |
| xử lý lỗi | `RequestValidationError` | `app/main.py:38` |
| middleware | `CORSMiddleware` | `app/main.py:20` |

Middleware áp dụng cho mọi request của app. Middleware xác thực chỉ cho biết app đọc thông tin đăng nhập; route có bắt buộc đăng nhập hay không vẫn xem ở cột Auth.

## 11. Chưa biết và giới hạn

- **Loại component được suy từ phạm vi đọc.** Membership không ghi loại component; xếp theo phạm vi đọc (FR-028): Ngoài sơ đồ: tests → test
- **Có bảng chưa đọc được.** Có bảng khai theo cách công cụ chưa đọc (FR-030 Phạm vi đọc), không có trong tài liệu: bảng chỉ có trong migration — tags (app/db/migrations/versions/fdf8821871d7_main_tables.py:124)
- **Chưa có sơ đồ component.** Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- **Chưa đối chiếu với dữ liệu kiến trúc.** Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- **Phân tích chưa xong.** còn lỗi sau 2 vòng sửa
- **File ngoài phạm vi đọc.** migration: 2 file, test: 23 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- **Có đề xuất của model bị bộ kiểm từ chối.** 57 lần nộp bị bộ kiểm từ chối (agent có thể đã nộp lại bản đúng); chi tiết ở result.json
- **Dòng trông giống route hoặc lời gọi HTTP nhưng chưa được xác nhận, nên không có trong tài liệu.** `app/api/routes/articles/articles_resource.py:89`, `app/api/routes/articles/articles_resource.py:109`, `app/api/routes/comments.py:26`, `app/api/routes/comments.py:40`, `app/api/routes/comments.py:60`

## Phụ lục: file cho máy

- API (OpenAPI): [tech-specs/DINH-NGHIA-ROUTER-API/api/API-NSIDNEV-FASTAPI-REALWORLD-EXAMPLE-APP-DINH-NGHIA-ROUTER-API-v1.md](tech-specs/DINH-NGHIA-ROUTER-API/api/API-NSIDNEV-FASTAPI-REALWORLD-EXAMPLE-APP-DINH-NGHIA-ROUTER-API-v1.md) — component Định nghĩa router API
