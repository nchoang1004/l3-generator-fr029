# fastapi_best_architecture — tài liệu API

Bản sinh tự động từ source, chưa được chủ repository duyệt. File này dành cho người đọc; dữ liệu đầy đủ cho máy nằm ở `result.json` và các file ở phụ lục.

| Mục | Giá trị |
|---|---|
| Tình trạng | Chưa đủ — model không gọi công cụ, xem mục 11 |
| Đọc source | 66/296 file trong phạm vi |
| Endpoint | 0 |
| Model | 0 |
| Bảng CSDL | 23 |
| Sự kiện, tác vụ nền | 4 điểm gửi/nhận |
| Gọi HTTP ra ngoài | 0 |
| Sinh bởi | model scripted, prompt fr029-agent-prompt-v17; bảng, sự kiện, thư viện, cấu hình, middleware đọc tĩnh từ code |

Cách đọc nhãn: **chắc chắn** — đọc thẳng từ một dòng code; **suy luận** — theo quy tắc mặc định của framework, lý do ở chú thích [n]; **chưa rõ** — source không đủ để kết luận; **AI viết** — câu chữ do model viết, chỉ để đọc nhanh, không phải dữ kiện đã kiểm.

## 1. Danh sách endpoint

Không có endpoint nào được xác nhận.

## 2. Chi tiết từng endpoint

## 3. Model dữ liệu

Không có model nào.

## 4. Bảng CSDL

SQL dialect: chưa rõ (Không có Base.metadata.create_all(engine) nối base này với một engine có URL literal; Metadata của bảng chưa được nối với một engine có URL literal). Kiểu cột ghi như khai trong code, chưa quy ra kiểu SQL.

Mọi bảng thuộc component backend.

Dấu \* sau một giá trị: code không khai, giá trị lấy theo mặc định có tài liệu của ORM.

| Bảng | Lớp model | Số cột | Khóa ngoại tới |
|---|---|---|---|
| code_gen_business | CodeGenBusiness | 17 | — |
| code_gen_column | CodeGenColumn | 11 | — |
| sys_config | Config | 11 | — |
| sys_data_rule | DataRule | 11 | — |
| sys_data_scope | DataScope | 7 | — |
| sys_data_scope_rule | `data_scope_rule = Table(...)` | 3 | — |
| sys_dept | Dept | 12 | — |
| sys_dict_data | DictData | 13 | — |
| sys_dict_type | DictType | 8 | — |
| sys_login_log | LoginLog | 15 | — |
| sys_menu | Menu | 19 | — |
| sys_notice | Notice | 9 | — |
| sys_opera_log | OperaLog | 21 | — |
| sys_role | Role | 9 | — |
| sys_role_data_scope | `role_data_scope = Table(...)` | 3 | — |
| sys_role_menu | `role_menu = Table(...)` | 3 | — |
| sys_user | User | 21 | — |
| sys_user_password_history | UserPasswordHistory | 4 | — |
| sys_user_role | `user_role = Table(...)` | 3 | — |
| sys_user_social | UserSocial | 8 | — |
| task_result | TaskExtended | 12 | — |
| task_scheduler | TaskScheduler | 24 | — |
| task_set_result | TaskSet | 4 | — |

### code_gen_business

Lớp `CodeGenBusiness`, khai ở `backend/plugin/code_generator/model/business.py:8`.

Ràng buộc bảng: unique(table_name, deleted) uk_code_gen_business_table_name_deleted.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_time | TimeZone | không\* | — | không\* | — |
| updated_time | TimeZone | không\* | — | có\* | — |
| deleted | BigInteger | không\* | — | không\* | — |
| deleted_time | TimeZone | không\* | — | có\* | — |
| id | BigInteger | có | — | không\* | unique, index |
| app_name | sa.String(64) | không\* | — | không\* | — |
| table_name | sa.String(256) | không\* | — | không\* | — |
| doc_comment | sa.String(256) | không\* | — | không\* | — |
| table_comment | sa.String(256) | không\* | — | có\* | — |
| class_name | sa.String(64) | không\* | — | có\* | — |
| schema_name | sa.String(64) | không\* | — | có\* | — |
| filename | sa.String(64) | không\* | — | có\* | — |
| datetime_mixin | bool | không\* | — | không\* | — |
| api_version | sa.String(32) | không\* | — | không\* | — |
| tag | sa.String(64) | không\* | — | có\* | — |
| gen_path | sa.String(256) | không\* | — | có\* | — |
| remark | UniversalText | không\* | — | có\* | — |

### code_gen_column

Lớp `CodeGenColumn`, khai ở `backend/plugin/code_generator/model/column.py:8`.

Ràng buộc bảng: unique(code_gen_business_id, name) uk_code_gen_column_business_id_name.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| id | BigInteger | có | — | không\* | unique, index |
| name | sa.String(64) | không\* | — | không\* | — |
| comment | sa.String(256) | không\* | — | có\* | — |
| type | sa.String(32) | không\* | — | không\* | — |
| pd_type | sa.String(32) | không\* | — | không\* | — |
| default | UniversalText | không\* | — | có\* | — |
| sort | int | không\* | — | có\* | — |
| length | int | không\* | — | không\* | — |
| is_pk | bool | không\* | — | không\* | — |
| is_nullable | bool | không\* | — | không\* | — |
| code_gen_business_id | sa.BigInteger | không\* | — | không\* | — |

### sys_config

Lớp `Config`, khai ở `backend/plugin/config/model/config.py:8`.

Ràng buộc bảng: unique(key, deleted) uk_sys_config_key_deleted.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_time | TimeZone | không\* | — | không\* | — |
| updated_time | TimeZone | không\* | — | có\* | — |
| deleted | BigInteger | không\* | — | không\* | — |
| deleted_time | TimeZone | không\* | — | có\* | — |
| id | BigInteger | có | — | không\* | unique, index |
| name | sa.String(32) | không\* | — | không\* | — |
| type | sa.String(32) | không\* | — | có\* | — |
| key | sa.String(64) | không\* | — | không\* | — |
| value | UniversalText | không\* | — | không\* | — |
| is_frontend | bool | không\* | — | không\* | — |
| remark | UniversalText | không\* | — | có\* | — |

### sys_data_rule

Lớp `DataRule`, khai ở `backend/app/admin/model/data_rule.py:8`.

Ràng buộc bảng: unique(name, deleted) uk_sys_data_rule_name_deleted.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_time | TimeZone | không\* | — | không\* | — |
| updated_time | TimeZone | không\* | — | có\* | — |
| deleted | BigInteger | không\* | — | không\* | — |
| deleted_time | TimeZone | không\* | — | có\* | — |
| id | BigInteger | có | — | không\* | unique, index |
| name | sa.String(512) | không\* | — | không\* | — |
| model | sa.String(64) | không\* | — | không\* | — |
| column | sa.String(32) | không\* | — | không\* | — |
| operator | int | không\* | — | không\* | — |
| expression | int | không\* | — | không\* | — |
| value | sa.String(256) | không\* | — | không\* | — |

### sys_data_scope

Lớp `DataScope`, khai ở `backend/app/admin/model/data_scope.py:8`.

Ràng buộc bảng: unique(name, deleted) uk_sys_data_scope_name_deleted.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_time | TimeZone | không\* | — | không\* | — |
| updated_time | TimeZone | không\* | — | có\* | — |
| deleted | BigInteger | không\* | — | không\* | — |
| deleted_time | TimeZone | không\* | — | có\* | — |
| id | BigInteger | có | — | không\* | unique, index |
| name | sa.String(64) | không\* | — | không\* | — |
| status | int | không\* | — | không\* | — |

### sys_data_scope_rule

Khai bằng `data_scope_rule = Table(...)` ở `backend/app/admin/model/m2m.py:33`.

Khóa chính ghép: id, data_scope_id, data_rule_id.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| id | sa.BigInteger | có | — | không\* | unique, index |
| data_scope_id | sa.BigInteger | có | — | không\* | — |
| data_rule_id | sa.BigInteger | có | — | không\* | — |

### sys_dept

Lớp `Dept`, khai ở `backend/app/admin/model/dept.py:8`.

Ràng buộc bảng: unique(name, deleted) uk_sys_dept_name_deleted.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_time | TimeZone | không\* | — | không\* | — |
| updated_time | TimeZone | không\* | — | có\* | — |
| deleted | BigInteger | không\* | — | không\* | — |
| deleted_time | TimeZone | không\* | — | có\* | — |
| id | BigInteger | có | — | không\* | unique, index |
| name | sa.String(64) | không\* | — | không\* | — |
| sort | int | không\* | — | không\* | — |
| leader | sa.String(32) | không\* | — | có\* | — |
| phone | sa.String(11) | không\* | — | có\* | — |
| email | sa.String(64) | không\* | — | có\* | — |
| status | int | không\* | — | không\* | — |
| parent_id | sa.BigInteger | không\* | — | có\* | index |

### sys_dict_data

Lớp `DictData`, khai ở `backend/plugin/dict/model/dict_data.py:8`.

Ràng buộc bảng: unique(type_code, label, deleted) uk_sys_dict_data_type_code_label_deleted.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_time | TimeZone | không\* | — | không\* | — |
| updated_time | TimeZone | không\* | — | có\* | — |
| deleted | BigInteger | không\* | — | không\* | — |
| deleted_time | TimeZone | không\* | — | có\* | — |
| id | BigInteger | có | — | không\* | unique, index |
| type_code | sa.String(32) | không\* | — | không\* | — |
| label | sa.String(32) | không\* | — | không\* | — |
| value | sa.String(32) | không\* | — | không\* | — |
| color | sa.String(32) | không\* | — | có\* | — |
| sort | int | không\* | — | không\* | — |
| status | int | không\* | — | không\* | — |
| remark | UniversalText | không\* | — | có\* | — |
| type_id | sa.BigInteger | không\* | — | không\* | — |

### sys_dict_type

Lớp `DictType`, khai ở `backend/plugin/dict/model/dict_type.py:8`.

Ràng buộc bảng: unique(code, deleted) uk_sys_dict_type_code_deleted.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_time | TimeZone | không\* | — | không\* | — |
| updated_time | TimeZone | không\* | — | có\* | — |
| deleted | BigInteger | không\* | — | không\* | — |
| deleted_time | TimeZone | không\* | — | có\* | — |
| id | BigInteger | có | — | không\* | unique, index |
| name | sa.String(32) | không\* | — | không\* | — |
| code | sa.String(32) | không\* | — | không\* | — |
| remark | UniversalText | không\* | — | có\* | — |

### sys_login_log

Lớp `LoginLog`, khai ở `backend/app/admin/model/login_log.py:11`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| id | BigInteger | có | — | không\* | unique, index |
| user_uuid | sa.String(64) | không\* | — | không\* | — |
| username | sa.String(64) | không\* | — | không\* | — |
| status | int | không\* | — | không\* | — |
| ip | sa.String(64) | không\* | — | không\* | — |
| country | sa.String(64) | không\* | — | có\* | — |
| region | sa.String(64) | không\* | — | có\* | — |
| city | sa.String(64) | không\* | — | có\* | — |
| user_agent | sa.String(512) | không\* | — | có\* | — |
| os | sa.String(64) | không\* | — | có\* | — |
| browser | sa.String(64) | không\* | — | có\* | — |
| device | sa.String(64) | không\* | — | có\* | — |
| msg | UniversalText | không\* | — | không\* | — |
| login_time | TimeZone | không\* | — | không\* | — |
| created_time | TimeZone | không\* | — | không\* | — |

### sys_menu

Lớp `Menu`, khai ở `backend/app/admin/model/menu.py:8`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_time | TimeZone | không\* | — | không\* | — |
| updated_time | TimeZone | không\* | — | có\* | — |
| deleted | BigInteger | không\* | — | không\* | — |
| deleted_time | TimeZone | không\* | — | có\* | — |
| id | BigInteger | có | — | không\* | unique, index |
| title | sa.String(64) | không\* | — | không\* | — |
| name | sa.String(64) | không\* | — | không\* | — |
| path | sa.String(200) | không\* | — | có\* | — |
| sort | int | không\* | — | không\* | — |
| icon | sa.String(128) | không\* | — | có\* | — |
| type | int | không\* | — | không\* | — |
| component | sa.String(256) | không\* | — | có\* | — |
| perms | sa.String(128) | không\* | — | có\* | — |
| status | int | không\* | — | không\* | — |
| display | int | không\* | — | không\* | — |
| cache | int | không\* | — | không\* | — |
| link | UniversalText | không\* | — | có\* | — |
| remark | UniversalText | không\* | — | có\* | — |
| parent_id | sa.BigInteger | không\* | — | có\* | index |

### sys_notice

Lớp `Notice`, khai ở `backend/plugin/notice/model/notice.py:8`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_time | TimeZone | không\* | — | không\* | — |
| updated_time | TimeZone | không\* | — | có\* | — |
| deleted | BigInteger | không\* | — | không\* | — |
| deleted_time | TimeZone | không\* | — | có\* | — |
| id | BigInteger | có | — | không\* | unique, index |
| title | sa.String(64) | không\* | — | không\* | — |
| type | int | không\* | — | không\* | — |
| status | int | không\* | — | không\* | — |
| content | UniversalText | không\* | — | không\* | — |

### sys_opera_log

Lớp `OperaLog`, khai ở `backend/app/admin/model/opera_log.py:11`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| id | BigInteger | có | — | không\* | unique, index |
| trace_id | sa.String(32) | không\* | — | không\* | — |
| username | sa.String(64) | không\* | — | có\* | — |
| method | sa.String(32) | không\* | — | không\* | — |
| title | sa.String(256) | không\* | — | không\* | — |
| path | sa.String(512) | không\* | — | không\* | — |
| ip | sa.String(64) | không\* | — | không\* | — |
| country | sa.String(64) | không\* | — | có\* | — |
| region | sa.String(64) | không\* | — | có\* | — |
| city | sa.String(64) | không\* | — | có\* | — |
| user_agent | sa.String(512) | không\* | — | có\* | — |
| os | sa.String(64) | không\* | — | có\* | — |
| browser | sa.String(64) | không\* | — | có\* | — |
| device | sa.String(64) | không\* | — | có\* | — |
| args | sa.JSON() | không\* | — | có\* | — |
| status | int | không\* | — | không\* | — |
| code | sa.String(32) | không\* | — | không\* | — |
| msg | UniversalText | không\* | — | có\* | — |
| cost_time | float | không\* | — | không\* | — |
| opera_time | TimeZone | không\* | — | không\* | — |
| created_time | TimeZone | không\* | — | không\* | — |

### sys_role

Lớp `Role`, khai ở `backend/app/admin/model/role.py:8`.

Ràng buộc bảng: unique(name, deleted) uk_sys_role_name_deleted.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_time | TimeZone | không\* | — | không\* | — |
| updated_time | TimeZone | không\* | — | có\* | — |
| deleted | BigInteger | không\* | — | không\* | — |
| deleted_time | TimeZone | không\* | — | có\* | — |
| id | BigInteger | có | — | không\* | unique, index |
| name | sa.String(32) | không\* | — | không\* | — |
| status | int | không\* | — | không\* | — |
| is_filter_scopes | bool | không\* | — | không\* | — |
| remark | UniversalText | không\* | — | có\* | — |

### sys_role_data_scope

Khai bằng `role_data_scope = Table(...)` ở `backend/app/admin/model/m2m.py:24`.

Khóa chính ghép: id, role_id, data_scope_id.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| id | sa.BigInteger | có | — | không\* | unique, index |
| role_id | sa.BigInteger | có | — | không\* | — |
| data_scope_id | sa.BigInteger | có | — | không\* | — |

### sys_role_menu

Khai bằng `role_menu = Table(...)` ở `backend/app/admin/model/m2m.py:15`.

Khóa chính ghép: id, role_id, menu_id.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| id | sa.BigInteger | có | — | không\* | unique, index |
| role_id | sa.BigInteger | có | — | không\* | — |
| menu_id | sa.BigInteger | có | — | không\* | — |

### sys_user

Lớp `User`, khai ở `backend/app/admin/model/user.py:12`.

Ràng buộc bảng: unique(username, deleted) uk_sys_user_username_deleted; unique(email, deleted) uk_sys_user_email_deleted.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_time | TimeZone | không\* | — | không\* | — |
| updated_time | TimeZone | không\* | — | có\* | — |
| deleted | BigInteger | không\* | — | không\* | — |
| deleted_time | TimeZone | không\* | — | có\* | — |
| id | BigInteger | có | — | không\* | unique, index |
| uuid | sa.String(64) | không\* | — | không\* | unique |
| username | sa.String(64) | không\* | — | không\* | index |
| nickname | sa.String(64) | không\* | — | không\* | — |
| password | sa.String(256) | không\* | — | có\* | — |
| salt | sa.LargeBinary(256) | không\* | — | có\* | — |
| email | sa.String(256) | không\* | — | có\* | index |
| phone | sa.String(11) | không\* | — | có\* | — |
| avatar | sa.String(256) | không\* | — | có\* | — |
| status | int | không\* | — | không\* | index |
| is_superuser | bool | không\* | — | không\* | — |
| is_staff | bool | không\* | — | không\* | — |
| is_multi_login | bool | không\* | — | không\* | — |
| join_time | TimeZone | không\* | — | không\* | — |
| last_login_time | TimeZone | không\* | — | có\* | — |
| last_password_changed_time | TimeZone | không\* | — | có\* | — |
| dept_id | sa.BigInteger | không\* | — | có\* | — |

### sys_user_password_history

Lớp `UserPasswordHistory`, khai ở `backend/app/admin/model/user_password_history.py:11`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| id | BigInteger | có | — | không\* | unique, index |
| user_id | sa.BigInteger | không\* | — | không\* | index |
| password | sa.String(256) | không\* | — | không\* | — |
| created_time | TimeZone | không\* | — | không\* | — |

### sys_user_role

Khai bằng `user_role = Table(...)` ở `backend/app/admin/model/m2m.py:6`.

Khóa chính ghép: id, user_id, role_id.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| id | sa.BigInteger | có | — | không\* | unique, index |
| user_id | sa.BigInteger | có | — | không\* | — |
| role_id | sa.BigInteger | có | — | không\* | — |

### sys_user_social

Lớp `UserSocial`, khai ở `backend/plugin/oauth2/model/user_social.py:8`.

Ràng buộc bảng: unique(user_id, source, deleted) uk_sys_user_social_user_id_source_deleted; unique(sid, source, deleted) uk_sys_user_social_sid_source_deleted.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_time | TimeZone | không\* | — | không\* | — |
| updated_time | TimeZone | không\* | — | có\* | — |
| deleted | BigInteger | không\* | — | không\* | — |
| deleted_time | TimeZone | không\* | — | có\* | — |
| id | BigInteger | có | — | không\* | unique, index |
| sid | sa.String(256) | không\* | — | không\* | — |
| source | sa.String(32) | không\* | — | không\* | — |
| user_id | sa.BigInteger | không\* | — | không\* | — |

### task_result

Lớp `TaskExtended`, khai ở `backend/app/task/model/result.py:54`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| id | sa.Integer | có | — | không\* | — |
| task_id | sa.String(155) | không\* | — | có\* | unique |
| status | sa.String(64) | không\* | — | có\* | — |
| result | PickleType | không\* | — | có | — |
| date_done | TimeZone | không\* | — | có | — |
| traceback | sa.Text | không\* | — | có | — |
| name | sa.String(155) | không\* | — | có | — |
| args | sa.LargeBinary | không\* | — | có | — |
| kwargs | sa.LargeBinary | không\* | — | có | — |
| worker | sa.String(155) | không\* | — | có | — |
| retries | sa.Integer | không\* | — | có | — |
| queue | sa.String(155) | không\* | — | có | — |

### task_scheduler

Lớp `TaskScheduler`, khai ở `backend/app/task/model/scheduler.py:19`.

Ràng buộc bảng: unique(name, deleted) uk_task_scheduler_name_deleted.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| created_time | TimeZone | không\* | — | không\* | — |
| updated_time | TimeZone | không\* | — | có\* | — |
| deleted | BigInteger | không\* | — | không\* | — |
| deleted_time | TimeZone | không\* | — | có\* | — |
| id | BigInteger | có | — | không\* | unique, index |
| name | sa.String(64) | không\* | — | không\* | — |
| task | sa.String(256) | không\* | — | không\* | — |
| args | sa.JSON() | không\* | — | có\* | — |
| kwargs | sa.JSON() | không\* | — | có\* | — |
| queue | sa.String(256) | không\* | — | có\* | — |
| exchange | sa.String(256) | không\* | — | có\* | — |
| routing_key | sa.String(256) | không\* | — | có\* | — |
| start_time | TimeZone | không\* | — | có\* | — |
| expire_time | TimeZone | không\* | — | có\* | — |
| expire_seconds | int | không\* | — | có\* | — |
| type | int | không\* | — | không\* | — |
| interval_every | int | không\* | — | có\* | — |
| interval_period | sa.String(256) | không\* | — | có\* | — |
| crontab | sa.String(64) | không\* | — | có\* | — |
| one_off | bool | không\* | — | không\* | — |
| status | int | không\* | — | không\* | — |
| total_run_count | int | không\* | — | không\* | — |
| last_run_time | TimeZone | không\* | — | có\* | — |
| remark | UniversalText | không\* | — | có\* | — |

### task_set_result

Lớp `TaskSet`, khai ở `backend/app/task/model/result.py:80`.

| Cột | Kiểu | Khóa chính | Khóa ngoại | Được null | Ràng buộc |
|---|---|---|---|---|---|
| id | sa.Integer | có | — | không\* | — |
| taskset_id | sa.String(155) | không\* | — | có\* | unique |
| result | PickleType | không\* | — | có | — |
| date_done | TimeZone | không\* | — | có | — |

## 5. Sự kiện và tác vụ nền

| Vai trò | Tác vụ hoặc topic | Thư viện / broker | Component | Ở đâu |
|---|---|---|---|---|
| nhận | backend.app.task.tasks.db_log.tasks.delete_db_login_log | chưa rõ (shared_task: app Celery chọn lúc chạy) | backend | `backend/app/task/tasks/db_log/tasks.py:16` |
| nhận | backend.app.task.tasks.db_log.tasks.delete_db_opera_log | chưa rõ (shared_task: app Celery chọn lúc chạy) | backend | `backend/app/task/tasks/db_log/tasks.py:8` |
| gửi | chưa rõ (Tên tác vụ không đọc được từ source) | fastapi.BackgroundTasks | backend | `backend/app/admin/service/auth_service.py:158` |
| gửi | chưa rõ (Tên tác vụ không đọc được từ source) | fastapi.BackgroundTasks | backend | `backend/plugin/oauth2/service/oauth2_service.py:116` |

Bên gửi và bên nhận chỉ được nối khi cùng broker và cùng tác vụ (FR-031); file EVT của từng component ghi bên liên quan.

## 6. Cấu trúc code

Vai trò của từng file theo dấu hiệu trong code (FR-029). Chỉ liệt kê component thường.

### Gốc

### backend

Không có vai trò: 66 file rỗng; chưa xác định vai trò: `backend/__init__.py`, `backend/app/admin/api/router.py`, `backend/app/admin/api/v1/auth/__init__.py`, `backend/app/admin/api/v1/auth/auth.py`, `backend/app/admin/api/v1/auth/captcha.py`, `backend/app/admin/api/v1/log/__init__.py`, `backend/app/admin/api/v1/log/login_log.py`, `backend/app/admin/api/v1/log/opera_log.py`, `backend/app/admin/api/v1/monitor/__init__.py`, `backend/app/admin/api/v1/monitor/online.py`, `backend/app/admin/api/v1/monitor/redis.py`, `backend/app/admin/api/v1/monitor/server.py`, `backend/app/admin/api/v1/sys/__init__.py`, `backend/app/admin/api/v1/sys/data_rule.py`, `backend/app/admin/api/v1/sys/data_scope.py`, `backend/app/admin/api/v1/sys/dept.py`, `backend/app/admin/api/v1/sys/file.py`, `backend/app/admin/api/v1/sys/menu.py`, `backend/app/admin/api/v1/sys/plugin.py`, `backend/app/admin/api/v1/sys/role.py`, `backend/app/admin/api/v1/sys/user.py`, `backend/app/admin/crud/crud_data_rule.py`, `backend/app/admin/crud/crud_data_scope.py`, `backend/app/admin/crud/crud_dept.py`, `backend/app/admin/crud/crud_login_log.py`, `backend/app/admin/crud/crud_menu.py`, `backend/app/admin/crud/crud_opera_log.py`, `backend/app/admin/crud/crud_role.py`, `backend/app/admin/crud/crud_user.py`, `backend/app/admin/crud/crud_user_password_history.py`, `backend/app/admin/model/__init__.py`, `backend/app/admin/model/data_rule.py`, `backend/app/admin/model/data_scope.py`, `backend/app/admin/model/dept.py`, `backend/app/admin/model/login_log.py`, `backend/app/admin/model/m2m.py`, `backend/app/admin/model/menu.py`, `backend/app/admin/model/opera_log.py`, `backend/app/admin/model/role.py`, `backend/app/admin/model/user.py`, `backend/app/admin/model/user_password_history.py`, `backend/app/admin/schema/captcha.py`, `backend/app/admin/schema/data_rule.py`, `backend/app/admin/schema/data_scope.py`, `backend/app/admin/schema/dept.py`, `backend/app/admin/schema/login_log.py`, `backend/app/admin/schema/menu.py`, `backend/app/admin/schema/monitor.py`, `backend/app/admin/schema/opera_log.py`, `backend/app/admin/schema/role.py`, `backend/app/admin/schema/token.py`, `backend/app/admin/schema/user.py`, `backend/app/admin/schema/user_password_history.py`, `backend/app/admin/service/auth_service.py`, `backend/app/admin/service/data_rule_service.py`, `backend/app/admin/service/data_scope_service.py`, `backend/app/admin/service/dept_service.py`, `backend/app/admin/service/login_log_service.py`, `backend/app/admin/service/menu_service.py`, `backend/app/admin/service/opera_log_service.py`, `backend/app/admin/service/plugin_service.py`, `backend/app/admin/service/role_service.py`, `backend/app/admin/service/user_password_history_service.py`, `backend/app/admin/service/user_service.py`, `backend/app/admin/utils/cache.py`, `backend/app/admin/utils/password_security.py`, `backend/app/router.py`, `backend/app/task/__init__.py`, `backend/app/task/actions.py`, `backend/app/task/api/router.py`, `backend/app/task/api/v1/control.py`, `backend/app/task/api/v1/result.py`, `backend/app/task/api/v1/scheduler.py`, `backend/app/task/celery.py`, `backend/app/task/crud/crud_result.py`, `backend/app/task/crud/crud_scheduler.py`, `backend/app/task/database.py`, `backend/app/task/enums.py`, `backend/app/task/model/__init__.py`, `backend/app/task/model/result.py`, `backend/app/task/model/scheduler.py`, `backend/app/task/schema/control.py`, `backend/app/task/schema/result.py`, `backend/app/task/schema/scheduler.py`, `backend/app/task/service/result_service.py`, `backend/app/task/service/scheduler_service.py`, `backend/app/task/session.py`, `backend/app/task/tasks/base.py`, `backend/app/task/tasks/beat.py`, `backend/app/task/tasks/db_log/tasks.py`, `backend/app/task/tasks/tasks.py`, `backend/app/task/utils/schedulers.py`, `backend/app/task/utils/tzcrontab.py`, `backend/cli.py`, `backend/common/cache/decorator.py`, `backend/common/cache/local.py`, `backend/common/cache/pubsub.py`, `backend/common/context.py`, `backend/common/dataclasses.py`, `backend/common/enums.py`, `backend/common/exception/errors.py`, `backend/common/exception/exception_handler.py`, `backend/common/i18n.py`, `backend/common/lifespan.py`, `backend/common/log.py`, `backend/common/model.py`, `backend/common/observability/otel.py`, `backend/common/observability/prometheus/fastapi.py`, `backend/common/observability/prometheus/queue.py`, `backend/common/observability/prometheus/sqlalchemy.py`, `backend/common/pagination.py`, `backend/common/queue.py`, `backend/common/response/response_code.py`, `backend/common/response/response_schema.py`, `backend/common/schema.py`, `backend/common/security/jwt.py`, `backend/common/security/permission.py`, `backend/common/security/rbac.py`, `backend/common/security/token.py`, `backend/common/socketio/__init__.py`, `backend/common/socketio/actions.py`, `backend/common/socketio/server.py`, `backend/core/conf.py`, `backend/core/path_conf.py`, `backend/core/registrar.py`, `backend/database/db.py`, `backend/database/redis.py`, `backend/main.py`, `backend/middleware/access_middleware.py`, `backend/middleware/i18n_middleware.py`, `backend/middleware/jwt_auth_middleware.py`, `backend/middleware/opera_log_middleware.py`, `backend/middleware/state_middleware.py`, `backend/plugin/code_generator/api/router.py`, `backend/plugin/code_generator/api/v1/business.py`, `backend/plugin/code_generator/api/v1/code_gen.py`, `backend/plugin/code_generator/api/v1/column.py`, `backend/plugin/code_generator/crud/crud_business.py`, `backend/plugin/code_generator/crud/crud_code_gen.py`, `backend/plugin/code_generator/crud/crud_column.py`, `backend/plugin/code_generator/enums.py`, `backend/plugin/code_generator/model/__init__.py`, `backend/plugin/code_generator/model/business.py`, `backend/plugin/code_generator/model/column.py`, `backend/plugin/code_generator/path_conf.py`, `backend/plugin/code_generator/schema/business.py`, `backend/plugin/code_generator/schema/code_gen.py`, `backend/plugin/code_generator/schema/column.py`, `backend/plugin/code_generator/service/business_service.py`, `backend/plugin/code_generator/service/code_gen_service.py`, `backend/plugin/code_generator/service/column_service.py`, `backend/plugin/code_generator/utils/format_code.py`, `backend/plugin/code_generator/utils/gen_template.py`, `backend/plugin/code_generator/utils/type_conversion.py`, `backend/plugin/config/api/v1/sys/config.py`, `backend/plugin/config/crud/crud_config.py`, `backend/plugin/config/enums.py`, `backend/plugin/config/model/__init__.py`, `backend/plugin/config/model/config.py`, `backend/plugin/config/schema/config.py`, `backend/plugin/config/service/config_service.py`, `backend/plugin/core.py`, `backend/plugin/dict/api/v1/sys/dict_data.py`, `backend/plugin/dict/api/v1/sys/dict_type.py`, `backend/plugin/dict/crud/crud_dict_data.py`, `backend/plugin/dict/crud/crud_dict_type.py`, `backend/plugin/dict/model/__init__.py`, `backend/plugin/dict/model/dict_data.py`, `backend/plugin/dict/model/dict_type.py`, `backend/plugin/dict/schema/dict_data.py`, `backend/plugin/dict/schema/dict_type.py`, `backend/plugin/dict/service/dict_data_service.py`, `backend/plugin/dict/service/dict_type_service.py`, `backend/plugin/email/api/router.py`, `backend/plugin/email/api/v1/email.py`, `backend/plugin/email/utils/dynamic_config.py`, `backend/plugin/email/utils/send.py`, `backend/plugin/errors.py`, `backend/plugin/hooks.py`, `backend/plugin/installer.py`, `backend/plugin/notice/api/v1/sys/notice.py`, `backend/plugin/notice/crud/crud_notice.py`, `backend/plugin/notice/enums.py`, `backend/plugin/notice/model/__init__.py`, `backend/plugin/notice/model/notice.py`, `backend/plugin/notice/schema/notice.py`, `backend/plugin/notice/service/notice_service.py`, `backend/plugin/oauth2/api/router.py`, `backend/plugin/oauth2/api/v1/github.py`, `backend/plugin/oauth2/api/v1/google.py`, `backend/plugin/oauth2/api/v1/user_social.py`, `backend/plugin/oauth2/crud/crud_user_social.py`, `backend/plugin/oauth2/enums.py`, `backend/plugin/oauth2/model/__init__.py`, `backend/plugin/oauth2/model/user_social.py`, `backend/plugin/oauth2/schema/user_social.py`, `backend/plugin/oauth2/service/oauth2_service.py`, `backend/plugin/oauth2/service/user_social_service.py`, `backend/plugin/patching.py`, `backend/plugin/requirements.py`, `backend/plugin/router.py`, `backend/plugin/settings_source.py`, `backend/plugin/sql.py`, `backend/plugin/status.py`, `backend/plugin/validator.py`, `backend/run.py`, `backend/utils/async_helper.py`, `backend/utils/build_tree.py`, `backend/utils/console.py`, `backend/utils/demo_mode.py`, `backend/utils/dynamic_config.py`, `backend/utils/dynamic_import.py`, `backend/utils/encrypt.py`, `backend/utils/file_ops.py`, `backend/utils/format.py`, `backend/utils/limiter.py`, `backend/utils/locks.py`, `backend/utils/openapi.py`, `backend/utils/pattern_validate.py`, `backend/utils/performance.py`, `backend/utils/request_parse.py`, `backend/utils/serializers.py`, `backend/utils/snowflake.py`, `backend/utils/sql_parser.py`, `backend/utils/timezone.py`, `backend/utils/trace_id.py`.

## 7. Gọi HTTP ra ngoài

Không có lời gọi nào qua httpx, requests, aiohttp.

## 8. Thư viện

| Thư viện | Phiên bản | Có import trong code | Khai ở |
|---|---|---|---|
| aiosmtplib | — | có | `backend/plugin/email/requirements.txt:1` |
| alembic | &gt;=1.19.1 | chưa thấy import | `pyproject.toml:11` |
| alembic | ==1.19.1 | chưa thấy import | `requirements.txt:4` |
| amqp | ==5.3.1 | chưa thấy import | `requirements.txt:6` |
| annotated-doc | ==0.0.5 | chưa thấy import | `requirements.txt:8` |
| annotated-types | ==0.8.0 | chưa thấy import | `requirements.txt:12` |
| anyio | ==4.14.2 | có | `requirements.txt:14` |
| asgiref | ==3.12.1 | chưa thấy import | `requirements.txt:19` |
| asgiref | &gt;=3.12.1 | chưa thấy import | `pyproject.toml:12` |
| async-timeout | ==5.0.1 ; python_full_version &lt; '3.11.3' | chưa thấy import | `requirements.txt:23` |
| asyncmy | ==0.2.13 | chưa thấy import | `requirements.txt:27` |
| asyncmy | &gt;=0.2.13 | chưa thấy import | `pyproject.toml:13` |
| asyncpg | ==0.31.0 | chưa thấy import | `requirements.txt:29` |
| asyncpg | &gt;=0.31.0 | chưa thấy import | `pyproject.toml:14` |
| bcrypt | &gt;=5.0.0 | có | `pyproject.toml:15` |
| bcrypt | ==5.0.0 | có | `requirements.txt:31` |
| bidict | ==0.23.1 | chưa thấy import | `requirements.txt:33` |
| billiard | ==4.2.4 | chưa thấy import | `requirements.txt:35` |
| cachebox | &gt;=6.2.5 | có | `pyproject.toml:17` |
| cachebox | ==6.2.5 | có | `requirements.txt:37` |
| cappa | ==0.32.2 | có | `requirements.txt:39` |
| cappa | &gt;=0.32.2 | có | `pyproject.toml:18` |
| celery | ==5.6.3 | có | `requirements.txt:41` |
| celery | &gt;=5.6.3 | có | `pyproject.toml:19` |
| celery-aio-pool | ==0.1.0rc8 | có | `requirements.txt:43` |
| celery-aio-pool | &gt;=0.1.0rc8 | có | `pyproject.toml:22` |
| certifi | ==2026.7.22 | chưa thấy import | `requirements.txt:48` |
| cffi | ==2.1.1 ; platform_python_implementation != 'PyPy' | chưa thấy import | `requirements.txt:52` |
| click | ==8.4.2 | chưa thấy import | `requirements.txt:56` |
| click-didyoumean | ==0.3.1 | chưa thấy import | `requirements.txt:59` |
| click-plugins | ==1.1.1.2 | chưa thấy import | `requirements.txt:60` |
| click-repl | ==0.3.0 | chưa thấy import | `requirements.txt:61` |
| colorama | ==0.4.6 ; sys_platform == 'win32' | chưa thấy import | `requirements.txt:71` |
| cryptography | ==50.0.0 | có | `requirements.txt:77` |
| cryptography | &gt;=47.0.0 | có | `pyproject.toml:23` |
| dnspython | ==2.8.0 | chưa thấy import | `requirements.txt:79` |
| dulwich | &gt;=1.2.12 | có | `pyproject.toml:24` |
| dulwich | ==1.2.12 | có | `requirements.txt:81` |
| ecdsa | ==0.19.2 | chưa thấy import | `requirements.txt:83` |
| email-validator | ==2.3.0 | có | `requirements.txt:85` |
| exceptiongroup | ==1.3.1 ; python_full_version &lt; '3.11' | chưa thấy import | `requirements.txt:87` |
| fast-captcha | ==0.3.2 | có | `requirements.txt:92` |
| fast-captcha | &gt;=0.3.2 | có | `pyproject.toml:25` |
| fastapi | &gt;=0.141.1 | có | `pyproject.toml:27` |
| fastapi | ==0.141.1 | có | `requirements.txt:93` |
| fastapi-cli | ==0.0.32 | có | `requirements.txt:98` |
| fastapi-oauth20 | &gt;=0.0.2 | có | `backend/plugin/oauth2/requirements.txt:1` |
| fastapi-pagination | ==0.15.16 | có | `requirements.txt:100` |
| fastapi-pagination | &gt;=0.15.16 | có | `pyproject.toml:26` |
| flower | ==2.0.1 | chưa thấy import | `requirements.txt:102` |
| flower | &gt;=2.0.1 | chưa thấy import | `pyproject.toml:28` |
| gevent | &gt;=26.8.0 | chưa thấy import | `pyproject.toml:29` |
| gevent | ==26.8.0 | chưa thấy import | `requirements.txt:104` |
| googleapis-common-protos | ==1.75.1 | chưa thấy import | `requirements.txt:106` |
| granian | ==2.8.1 | có | `requirements.txt:108` |
| granian | &gt;=2.8.1 | có | `pyproject.toml:30` |
| greenlet | ==3.5.5 | chưa thấy import | `requirements.txt:110` |
| grpcio | ==1.83.0 | chưa thấy import | `requirements.txt:114` |
| h11 | ==0.16.0 | chưa thấy import | `requirements.txt:116` |
| hiredis | ==3.4.1 | chưa thấy import | `requirements.txt:121` |
| httpcore | ==1.0.9 | chưa thấy import | `requirements.txt:123` |
| httptools | ==0.8.0 | chưa thấy import | `requirements.txt:125` |
| httpx | ==0.28.1 | có | `requirements.txt:127` |
| humanize | ==4.16.0 | chưa thấy import | `requirements.txt:129` |
| idna | ==3.18 | chưa thấy import | `requirements.txt:131` |
| iniconfig | ==2.3.0 | chưa thấy import | `requirements.txt:136` |
| itsdangerous | &gt;=2.2.0 | có | `pyproject.toml:31` |
| itsdangerous | ==2.2.0 | có | `requirements.txt:138` |
| jinja2 | ==3.1.6 | có | `requirements.txt:140` |
| jinja2 | &gt;=3.1.6 | có | `pyproject.toml:32` |
| kombu | ==5.6.2 | chưa thấy import | `requirements.txt:144` |
| loguru | ==0.7.3 | có | `requirements.txt:146` |
| loguru | &gt;=0.7.3 | có | `pyproject.toml:33` |
| mako | ==1.4.1 | chưa thấy import | `requirements.txt:148` |
| markdown-it-py | ==4.2.0 | chưa thấy import | `requirements.txt:150` |
| markupsafe | ==3.0.3 | chưa thấy import | `requirements.txt:152` |
| mdurl | ==0.1.2 | chưa thấy import | `requirements.txt:156` |
| msgspec | &gt;=0.21.1 | có | `pyproject.toml:34` |
| msgspec | ==0.21.1 | có | `requirements.txt:158` |
| opentelemetry-api | ==1.44.0 | có | `requirements.txt:160` |
| opentelemetry-exporter-otlp-proto-common | ==1.44.0 | có | `requirements.txt:174` |
| opentelemetry-exporter-otlp-proto-grpc | &gt;=1.44.0 | có | `pyproject.toml:35` |
| opentelemetry-exporter-otlp-proto-grpc | ==1.44.0 | có | `requirements.txt:175` |
| opentelemetry-instrumentation | ==0.65b0 | có | `requirements.txt:178` |
| opentelemetry-instrumentation-asgi | ==0.65b0 | có | `requirements.txt:180` |
| opentelemetry-instrumentation-asyncio | &gt;=0.65b0 | có | `pyproject.toml:36` |
| opentelemetry-instrumentation-asyncio | ==0.65b0 | có | `requirements.txt:181` |
| opentelemetry-instrumentation-celery | &gt;=0.65b0 | có | `pyproject.toml:37` |
| opentelemetry-instrumentation-celery | ==0.65b0 | có | `requirements.txt:182` |
| opentelemetry-instrumentation-fastapi | ==0.65b0 | có | `requirements.txt:183` |
| opentelemetry-instrumentation-fastapi | &gt;=0.65b0 | có | `pyproject.toml:38` |
| opentelemetry-instrumentation-httpx | &gt;=0.65b0 | có | `pyproject.toml:39` |
| opentelemetry-instrumentation-httpx | ==0.65b0 | có | `requirements.txt:184` |
| opentelemetry-instrumentation-logging | &gt;=0.65b0 | có | `pyproject.toml:40` |
| opentelemetry-instrumentation-logging | ==0.65b0 | có | `requirements.txt:185` |
| opentelemetry-instrumentation-redis | &gt;=0.65b0 | có | `pyproject.toml:41` |
| opentelemetry-instrumentation-redis | ==0.65b0 | có | `requirements.txt:186` |
| opentelemetry-instrumentation-sqlalchemy | &gt;=0.65b0 | có | `pyproject.toml:42` |
| opentelemetry-instrumentation-sqlalchemy | ==0.65b0 | có | `requirements.txt:187` |
| opentelemetry-proto | ==1.44.0 | có | `requirements.txt:204` |
| opentelemetry-sdk | ==1.44.0 | có | `requirements.txt:208` |
| opentelemetry-sdk | &gt;=1.44.0 | có | `pyproject.toml:43` |
| opentelemetry-semantic-conventions | ==0.65b0 | có | `requirements.txt:212` |
| opentelemetry-util-http | ==0.65b0 | có | `requirements.txt:224` |
| packaging | ==26.3 | có | `requirements.txt:229` |
| pillow | ==12.3.0 | chưa thấy import | `requirements.txt:236` |
| pluggy | ==1.6.0 | chưa thấy import | `requirements.txt:238` |
| prek | ==0.4.13 | chưa thấy import | `requirements.txt:240` |
| prometheus-client | ==0.26.0 | có | `requirements.txt:241` |
| prometheus-client | &gt;=0.25.0 | có | `pyproject.toml:44` |
| prompt-toolkit | ==3.0.53 | chưa thấy import | `requirements.txt:245` |
| protobuf | ==7.35.1 | chưa thấy import | `requirements.txt:247` |
| psutil | ==7.2.2 | có | `requirements.txt:251` |
| psutil | &gt;=7.2.2 | có | `pyproject.toml:45` |
| psycopg | ==3.2.10 | chưa thấy import | `pyproject.toml:47`, `requirements.txt:253` |
| psycopg-binary | ==3.2.10 ; implementation_name != 'pypy' | chưa thấy import | `requirements.txt:255` |
| pwdlib | &gt;=0.3.0 | có | `pyproject.toml:48` |
| pwdlib | ==0.3.0 | có | `requirements.txt:257` |
| py-ip2region | ==3.0.4 | chưa thấy import | `requirements.txt:259` |
| py-ip2region | &gt;=3.0.4 | chưa thấy import | `pyproject.toml:49` |
| pyasn1 | ==0.6.4 | chưa thấy import | `requirements.txt:261` |
| pycparser | ==3.0 ; implementation_name != 'PyPy' and platform_python_implementation != 'PyPy' | chưa thấy import | `requirements.txt:265` |
| pydantic | ==2.13.4 | có | `requirements.txt:267` |
| pydantic | &gt;=2.13.4 | có | `pyproject.toml:50` |
| pydantic-core | ==2.46.4 | có | `requirements.txt:275` |
| pydantic-extra-types | ==2.11.1 | có | `requirements.txt:277` |
| pydantic-settings | &gt;=2.15.0 | có | `pyproject.toml:51` |
| pydantic-settings | ==2.15.0 | có | `requirements.txt:279` |
| pygments | ==2.20.0 | chưa thấy import | `requirements.txt:283` |
| pymysql | &gt;=1.1.2 | chưa thấy import | `pyproject.toml:52` |
| pymysql | ==1.2.0 | chưa thấy import | `requirements.txt:287` |
| pyrate-limiter | ==4.4.0 | có | `requirements.txt:289` |
| pyrate-limiter | &gt;=4.4.0 | có | `pyproject.toml:53` |
| pytest | ==9.1.1 | chưa thấy import | `requirements.txt:291` |
| pytest-sugar | ==1.1.1 | chưa thấy import | `requirements.txt:292` |
| python-dateutil | ==2.9.0.post0 | chưa thấy import | `requirements.txt:294` |
| python-dotenv | ==1.2.2 | chưa thấy import | `requirements.txt:298` |
| python-engineio | ==4.13.4 | chưa thấy import | `requirements.txt:302` |
| python-jose | &gt;=3.5.0 | có | `pyproject.toml:54` |
| python-jose | ==3.5.0 | có | `requirements.txt:304` |
| python-multipart | ==0.0.32 | chưa thấy import | `requirements.txt:306` |
| python-socketio | &gt;=5.16.4 | có | `pyproject.toml:55` |
| python-socketio | ==5.16.4 | có | `requirements.txt:308` |
| pytz | ==2026.3.post1 | chưa thấy import | `requirements.txt:310` |
| pyyaml | ==6.0.3 | có | `requirements.txt:312` |
| redis | ==8.1.0 | có | `requirements.txt:314` |
| redis | &gt;=8.1.0 | có | `pyproject.toml:56` |
| rich | ==15.0.0 | có | `requirements.txt:316` |
| rich-toolkit | ==0.20.3 | có | `requirements.txt:319` |
| rsa | ==4.9.1 | chưa thấy import | `requirements.txt:323` |
| rtoml | &gt;=0.13.0 | có | `pyproject.toml:57` |
| rtoml | ==0.13.0 | có | `requirements.txt:325` |
| shellingham | ==1.5.4 | chưa thấy import | `requirements.txt:327` |
| simple-websocket | ==1.1.0 | chưa thấy import | `requirements.txt:329` |
| six | ==1.17.0 | chưa thấy import | `requirements.txt:331` |
| sqlakeyset | ==2.0.1775222100 | chưa thấy import | `requirements.txt:335` |
| sqlalchemy | ==2.0.52 | có | `requirements.txt:337` |
| sqlalchemy | &gt;=2.0.52 | có | `pyproject.toml:59` |
| sqlalchemy-crud-plus | &gt;=1.13.3 | có | `pyproject.toml:58` |
| sqlalchemy-crud-plus | ==1.13.3 | có | `requirements.txt:343` |
| sqlparse | ==0.5.5 | có | `requirements.txt:346` |
| sqlparse | &gt;=0.5.5 | có | `pyproject.toml:60` |
| starlette | ==1.6.0 | có | `requirements.txt:348` |
| starlette-context | &gt;=0.5.1 | có | `pyproject.toml:61` |
| starlette-context | ==0.5.1 | có | `requirements.txt:351` |
| termcolor | ==3.3.0 | chưa thấy import | `requirements.txt:354` |
| tomli | ==2.4.1 ; python_full_version &lt; '3.11' | chưa thấy import | `requirements.txt:356` |
| tornado | ==6.5.8 | chưa thấy import | `requirements.txt:361` |
| type-lens | ==0.2.6 | chưa thấy import | `requirements.txt:363` |
| typer | ==0.27.1 | chưa thấy import | `requirements.txt:365` |
| typing-extensions | ==4.16.0 | có | `requirements.txt:367` |
| typing-inspection | ==0.4.3 | có | `requirements.txt:392` |
| tzdata | ==2026.3 | chưa thấy import | `requirements.txt:399` |
| tzlocal | ==5.4.4 | chưa thấy import | `requirements.txt:403` |
| ua-parser | ==1.0.2 | chưa thấy import | `requirements.txt:406` |
| ua-parser-builtins | ==202606 | chưa thấy import | `requirements.txt:408` |
| urllib3 | ==2.7.0 | chưa thấy import | `requirements.txt:410` |
| user-agents | &gt;=2.2.0 | có | `pyproject.toml:62` |
| user-agents | ==2.2.0 | có | `requirements.txt:412` |
| uvicorn | ==0.52.1 | có | `requirements.txt:414` |
| uvloop | ==0.22.1 ; platform_python_implementation != 'PyPy' and sys_platform != 'cygwin' and sys_platform != 'win32' | chưa thấy import | `requirements.txt:418` |
| vine | ==5.1.0 | chưa thấy import | `requirements.txt:420` |
| watchfiles | ==1.2.0 | có | `requirements.txt:425` |
| wcwidth | ==0.8.2 | chưa thấy import | `requirements.txt:427` |
| websockets | ==17.0.1 ; python_full_version &gt;= '3.11' | chưa thấy import | `requirements.txt:431` |
| websockets | ==16.1.1 ; python_full_version &lt; '3.11' | chưa thấy import | `requirements.txt:429` |
| win32-setctime | ==1.2.0 ; sys_platform == 'win32' | chưa thấy import | `requirements.txt:433` |
| wrapt | ==2.3.0 | chưa thấy import | `requirements.txt:435` |
| wsproto | ==1.3.2 | chưa thấy import | `requirements.txt:442` |
| zope-event | ==6.2 | chưa thấy import | `requirements.txt:444` |
| zope-interface | ==8.5 | chưa thấy import | `requirements.txt:446` |

"Chưa thấy import": tên gói khác tên import, hoặc gói chỉ dùng gián tiếp (driver, plugin, công cụ).

## 9. Cấu hình

| Khóa | Nguồn | Giá trị mặc định | Khai ở |
|---|---|---|---|
| CACHE_CONFIG_REDIS_PREFIX | lớp Settings | fba:cache:config | `backend/core/conf.py:79` |
| CACHE_DICT_REDIS_PREFIX | lớp Settings | fba:cache:dict | `backend/core/conf.py:80` |
| CACHE_LOCAL_ENABLED | lớp Settings | True | `backend/core/conf.py:75` |
| CACHE_LOCAL_MAXSIZE | lớp Settings | 100000 | `backend/core/conf.py:76` |
| CACHE_LOCAL_TTL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:77` |
| CACHE_PUBSUB_CHANNEL | lớp Settings | fba:cache:invalidate | `backend/core/conf.py:81` |
| CACHE_PUBSUB_MAX_RECONNECT_ATTEMPTS | lớp Settings | 10 | `backend/core/conf.py:83` |
| CACHE_PUBSUB_POLL_TIMEOUT | lớp Settings | 1.0 | `backend/core/conf.py:84` |
| CACHE_PUBSUB_RECONNECT_DELAY | lớp Settings | 5 | `backend/core/conf.py:82` |
| CACHE_REDIS_TTL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:78` |
| CELERY_BROKER | lớp Settings | redis | `backend/core/conf.py:292` |
| CELERY_BROKER_REDIS_DATABASE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:282` |
| CELERY_RABBITMQ_HOST | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:286` |
| CELERY_RABBITMQ_PASSWORD | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:289` |
| CELERY_RABBITMQ_PORT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:287` |
| CELERY_RABBITMQ_USERNAME | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:288` |
| CELERY_RABBITMQ_VHOST | lớp Settings | — | `backend/core/conf.py:293` |
| CELERY_REDIS_PREFIX | lớp Settings | fba:celery | `backend/core/conf.py:294` |
| CELERY_TASK_MAX_RETRIES | lớp Settings | 5 | `backend/core/conf.py:295` |
| CODE_GENERATOR_DOWNLOAD_ZIP_FILENAME | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:300` |
| COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:140` |
| COOKIE_REFRESH_TOKEN_KEY | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:139` |
| CORS_ALLOWED_ORIGINS | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:174` |
| CORS_EXPOSE_HEADERS | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:178` |
| DATABASE_CHARSET | lớp Settings | utf8mb4 | `backend/core/conf.py:60` |
| DATABASE_ECHO | lớp Settings | False | `backend/core/conf.py:57` |
| DATABASE_HOST | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:50` |
| DATABASE_PASSWORD | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:53` |
| DATABASE_PK_MODE | lớp Settings | autoincrement | `backend/core/conf.py:61` |
| DATABASE_POOL_ECHO | lớp Settings | False | `backend/core/conf.py:58` |
| DATABASE_PORT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:51` |
| DATABASE_SCHEMA | lớp Settings | fba | `backend/core/conf.py:59` |
| DATABASE_SOURCES | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:54` |
| DATABASE_TYPE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:49` |
| DATABASE_USER | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:52` |
| DATA_PERMISSION_COLUMN_EXCLUDE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:149` |
| DATA_PERMISSION_COLUMN_TEMPLATE_VARIABLES | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:160` |
| DATA_PERMISSION_MODEL_EXCLUDE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:143` |
| DATA_PERMISSION_MODEL_TEMPLATE_VARIABLES | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:157` |
| DATA_PERMISSION_TEMPLATE_VARIABLES | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:164` |
| DATETIME_FORMAT | lớp Settings | %Y-%m-%d %H:%M:%S | `backend/core/conf.py:190` |
| DATETIME_TIMEZONE | lớp Settings | Asia/Shanghai | `backend/core/conf.py:189` |
| DEMO_MODE | lớp Settings | False | `backend/core/conf.py:200` |
| DEMO_MODE_EXCLUDE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:201` |
| EMAIL_CAPTCHA_EXPIRE_SECONDS | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:331` |
| EMAIL_CAPTCHA_REDIS_PREFIX | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:330` |
| EMAIL_HOST | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:327` |
| EMAIL_PASSWORD | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:324` |
| EMAIL_PORT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:328` |
| EMAIL_SSL | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:329` |
| EMAIL_USERNAME | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:323` |
| ENVIRONMENT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:37` |
| FASTAPI_API_V1_PATH | lớp Settings | /api/v1 | `backend/core/conf.py:40` |
| FASTAPI_DESCRIPTION | lớp Settings | FastAPI Best Architecture | `backend/core/conf.py:42` |
| FASTAPI_DOCS_URL | lớp Settings | /docs | `backend/core/conf.py:43` |
| FASTAPI_OPENAPI_URL | lớp Settings | /openapi | `backend/core/conf.py:45` |
| FASTAPI_REDOC_URL | lớp Settings | /redoc | `backend/core/conf.py:44` |
| FASTAPI_STATIC_FILES | lớp Settings | True | `backend/core/conf.py:46` |
| FASTAPI_TITLE | lớp Settings | fba | `backend/core/conf.py:41` |
| GRAFANA_CELERY_OTEL_SERVICE_NAME | lớp Settings | fba_celery_worker | `backend/core/conf.py:274` |
| GRAFANA_METRICS_ENABLE | lớp Settings | False | `backend/core/conf.py:264` |
| GRAFANA_METRICS_PATH | lớp Settings | /metrics | `backend/core/conf.py:275` |
| GRAFANA_OTLP_GRPC_ENDPOINT | lớp Settings | fba_alloy:4317 | `backend/core/conf.py:265` |
| GRAFANA_PROMETHEUS_APP_NAME | lớp Settings | fba_server | `backend/core/conf.py:273` |
| GRAFANA_PROMETHEUS_EXEMPLAR_TRACE_ID_KEY | lớp Settings | TraceID | `backend/core/conf.py:276` |
| I18N_DEFAULT_LANGUAGE | lớp Settings | zh-CN | `backend/core/conf.py:261` |
| IP_LOCATION_EXPIRE_SECONDS | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:211` |
| IP_LOCATION_PARSE | lớp Settings | offline | `backend/core/conf.py:209` |
| IP_LOCATION_REDIS_PREFIX | lớp Settings | fba:ip:location | `backend/core/conf.py:210` |
| JWT_USER_REDIS_PREFIX | lớp Settings | fba:user | `backend/core/conf.py:132` |
| LOGIN_CAPTCHA_ENABLED | lớp Settings | True | `backend/core/conf.py:126` |
| LOGIN_CAPTCHA_EXPIRE_SECONDS | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:128` |
| LOGIN_CAPTCHA_REDIS_PREFIX | lớp Settings | fba:login:captcha | `backend/core/conf.py:127` |
| LOGIN_FAILURE_PREFIX | lớp Settings | fba:login:failure | `backend/core/conf.py:129` |
| LOG_ACCESS_FILENAME | lớp Settings | fba_access.log | `backend/core/conf.py:229` |
| LOG_ERROR_FILENAME | lớp Settings | fba_error.log | `backend/core/conf.py:230` |
| LOG_FILE_ACCESS_LEVEL | lớp Settings | INFO | `backend/core/conf.py:227` |
| LOG_FILE_ERROR_LEVEL | lớp Settings | ERROR | `backend/core/conf.py:228` |
| LOG_FORMAT | lớp Settings | &lt;green&gt;{time:YYYY-MM-DD HH:mm:ss.SSS}&lt;/&gt; \| &lt;lvl&gt;{level: &lt;8}&lt;/&gt; \| &lt;cyan&gt;{request_id}&lt;/&gt; \| &lt;lvl&gt;{message}&lt;/&gt; | `backend/core/conf.py:219` |
| LOG_STD_LEVEL | lớp Settings | INFO | `backend/core/conf.py:224` |
| MIDDLEWARE_CORS | lớp Settings | True | `backend/core/conf.py:183` |
| OAUTH2_FRONTEND_BINDING_REDIRECT_URI | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:317` |
| OAUTH2_FRONTEND_LOGIN_REDIRECT_URI | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:316` |
| OAUTH2_GITHUB_CLIENT_ID | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:306` |
| OAUTH2_GITHUB_CLIENT_SECRET | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:307` |
| OAUTH2_GITHUB_REDIRECT_URI | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:314` |
| OAUTH2_GOOGLE_CLIENT_ID | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:308` |
| OAUTH2_GOOGLE_CLIENT_SECRET | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:309` |
| OAUTH2_GOOGLE_REDIRECT_URI | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:315` |
| OAUTH2_STATE_EXPIRE_SECONDS | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:313` |
| OAUTH2_STATE_REDIS_PREFIX | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:312` |
| OPERA_LOG_BODY_MAX_SIZE | lớp Settings | 10240 | `backend/core/conf.py:251` |
| OPERA_LOG_PATH_EXCLUDE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:233` |
| OPERA_LOG_QUEUE_BATCH_CONSUME_SIZE | lớp Settings | 100 | `backend/core/conf.py:249` |
| OPERA_LOG_QUEUE_MAXSIZE | lớp Settings | 100000 | `backend/core/conf.py:248` |
| OPERA_LOG_QUEUE_TIMEOUT | lớp Settings | 60 | `backend/core/conf.py:250` |
| OPERA_LOG_REDACT_KEYS | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:242` |
| PLUGIN_PIP_CHINA | lớp Settings | True | `backend/core/conf.py:255` |
| PLUGIN_PIP_INDEX_URL | lớp Settings | https://mirrors.aliyun.com/pypi/simple/ | `backend/core/conf.py:256` |
| PLUGIN_PIP_MAX_RETRY | lớp Settings | 3 | `backend/core/conf.py:257` |
| PLUGIN_REDIS_PREFIX | lớp Settings | fba:plugin | `backend/core/conf.py:258` |
| PLUGIN_REQUIRED | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:254` |
| RBAC_ROLE_MENU_EXCLUDE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:136` |
| RBAC_ROLE_MENU_MODE | lớp Settings | True | `backend/core/conf.py:135` |
| REDIS_DATABASE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:67` |
| REDIS_HOST | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:64` |
| REDIS_MAX_CONNECTIONS | lớp Settings | 100 | `backend/core/conf.py:71` |
| REDIS_PASSWORD | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:66` |
| REDIS_POOL_TIMEOUT | lớp Settings | 20 | `backend/core/conf.py:72` |
| REDIS_PORT | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:65` |
| REDIS_TIMEOUT | lớp Settings | 5 | `backend/core/conf.py:70` |
| REQUEST_LIMITER_REDIS_PREFIX | lớp Settings | fba:limiter | `backend/core/conf.py:186` |
| SNOWFLAKE_DATACENTER_ID | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:88` |
| SNOWFLAKE_ENABLED | lớp Settings | False | `backend/core/conf.py:87` |
| SNOWFLAKE_HEARTBEAT_INTERVAL_SECONDS | lớp Settings | 30 | `backend/core/conf.py:93` |
| SNOWFLAKE_NODE_TTL_SECONDS | lớp Settings | 60 | `backend/core/conf.py:94` |
| SNOWFLAKE_REDIS_PREFIX | lớp Settings | fba:snowflake | `backend/core/conf.py:92` |
| SNOWFLAKE_WORKER_ID | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:89` |
| TOKEN_ALGORITHM | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:100` |
| TOKEN_EXPIRE_SECONDS | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:101` |
| TOKEN_EXTRA_INFO_REDIS_PREFIX | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:104` |
| TOKEN_ONLINE_REDIS_PREFIX | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:105` |
| TOKEN_REDIS_PREFIX | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:103` |
| TOKEN_REFRESH_EXPIRE_SECONDS | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:102` |
| TOKEN_REFRESH_REDIS_PREFIX | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:106` |
| TOKEN_REQUEST_PATH_EXCLUDE | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:109` |
| TOKEN_REQUEST_PATH_EXCLUDE_PATTERN | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:112` |
| TOKEN_REQUEST_UNDERLYING_SECURITY | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:108` |
| TOKEN_SECRET_KEY | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:97` |
| TOKEN_SESSION_REDIS_PREFIX | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:107` |
| TRACE_ID_LOG_DEFAULT_VALUE | lớp Settings | - | `backend/core/conf.py:216` |
| TRACE_ID_LOG_LENGTH | lớp Settings | 32 | `backend/core/conf.py:215` |
| TRACE_ID_REQUEST_HEADER_KEY | lớp Settings | X-Request-ID | `backend/core/conf.py:214` |
| UPLOAD_IMAGE_EXT_INCLUDE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:194` |
| UPLOAD_IMAGE_SIZE_MAX | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:195` |
| UPLOAD_READ_SIZE | lớp Settings | 1024 | `backend/core/conf.py:193` |
| UPLOAD_VIDEO_EXT_INCLUDE | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:196` |
| UPLOAD_VIDEO_SIZE_MAX | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:197` |
| USER_LOCK_REDIS_PREFIX | lớp Settings | fba:user:lock | `backend/core/conf.py:115` |
| USER_LOCK_SECONDS | lớp Settings | chưa rõ (Giá trị đọc lúc chạy) | `backend/core/conf.py:117` |
| USER_LOCK_THRESHOLD | lớp Settings | 5 | `backend/core/conf.py:116` |
| USER_PASSWORD_EXPIRY_DAYS | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:118` |
| USER_PASSWORD_HISTORY_CHECK_COUNT | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:120` |
| USER_PASSWORD_MAX_LENGTH | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:122` |
| USER_PASSWORD_MIN_LENGTH | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:121` |
| USER_PASSWORD_REMINDER_DAYS | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:119` |
| USER_PASSWORD_REQUIRE_SPECIAL_CHAR | lớp Settings | đã che (dấu hiệu bí mật) | `backend/core/conf.py:123` |
| WS_NO_AUTH_MARKER | lớp Settings | internal | `backend/core/conf.py:171` |

## 10. Middleware và xử lý lỗi toàn cục

| Loại | Tên | Ở đâu |
|---|---|---|
| xử lý lỗi | `RequestValidationError` | `backend/common/exception/exception_handler.py:106` |
| xử lý lỗi | `ValidationError` | `backend/common/exception/exception_handler.py:117` |
| xử lý lỗi | `AssertionError` | `backend/common/exception/exception_handler.py:128` |
| xử lý lỗi | `BaseExceptionError` | `backend/common/exception/exception_handler.py:153` |
| xử lý lỗi | `Exception` | `backend/common/exception/exception_handler.py:175` |
| xử lý lỗi | `StandardResponseCode.HTTP_500` | `backend/common/exception/exception_handler.py:202` |
| xử lý lỗi | `HTTPException` | `backend/common/exception/exception_handler.py:80` |
| middleware | `OperaLogMiddleware` | `backend/core/registrar.py:156` |
| middleware | `StateMiddleware` | `backend/core/registrar.py:159` |
| middleware | `AuthenticationMiddleware` | `backend/core/registrar.py:162` |
| middleware | `I18nMiddleware` | `backend/core/registrar.py:169` |
| middleware | `AccessMiddleware` | `backend/core/registrar.py:172` |
| middleware | `ContextMiddleware` | `backend/core/registrar.py:176` |
| middleware | `CORSMiddleware` | `backend/core/registrar.py:189` |
| middleware | `replacement_middleware_cls` | `backend/plugin/patching.py:22` |

Middleware áp dụng cho mọi request của app. Middleware xác thực chỉ cho biết app đọc thông tin đăng nhập; route có bắt buộc đăng nhập hay không vẫn xem ở cột Auth.

## 11. Chưa biết và giới hạn

- **Chưa có sơ đồ component.** Chưa được cấp sơ đồ component từ bước kiến trúc (FR-028); README chưa đủ mục sơ đồ của AC-029-06
- **Chưa đối chiếu với dữ liệu kiến trúc.** Chưa đối chiếu được với archdia.json (AC-029-04): Chưa được cấp archdia.json cùng snapshot
- **Phân tích chưa xong.** model không gọi công cụ
- **Có phần source chưa đọc.** backend/__init__.py thiếu [[1, 17]]; backend/app/admin/api/router.py thiếu [[1, 14]]; backend/app/admin/api/v1/auth/__init__.py thiếu [[1, 9]]; backend/app/admin/api/v1/auth/auth.py thiếu [[1, 58]]; backend/app/admin/api/v1/auth/captcha.py thiếu [[1, 39]]; backend/app/admin/api/v1/log/__init__.py thiếu [[1, 9]]; backend/app/admin/api/v1/log/login_log.py thiếu [[1, 61]]; backend/app/admin/api/v1/log/opera_log.py thiếu [[1, 61]]; backend/app/admin/api/v1/monitor/__init__.py thiếu [[1, 11]]; backend/app/admin/api/v1/monitor/online.py thiếu [[1, 119]]; backend/app/admin/api/v1/monitor/redis.py thiếu [[1, 42]]; backend/app/admin/api/v1/monitor/server.py thiếu [[1, 134]]; backend/app/admin/api/v1/sys/__init__.py thiếu [[1, 21]]; backend/app/admin/api/v1/sys/data_rule.py thiếu [[1, 119]]; backend/app/admin/api/v1/sys/data_scope.py thiếu [[1, 128]]; backend/app/admin/api/v1/sys/dept.py thiếu [[1, 83]]; backend/app/admin/api/v1/sys/file.py thiếu [[1, 25]]; backend/app/admin/api/v1/sys/menu.py thiếu [[1, 82]]; backend/app/admin/api/v1/sys/plugin.py thiếu [[1, 74]]; backend/app/admin/api/v1/sys/role.py thiếu [[1, 154]]; backend/app/admin/api/v1/sys/user.py thiếu [[1, 172]]; backend/app/admin/crud/crud_data_rule.py thiếu [[1, 110]]; backend/app/admin/crud/crud_data_scope.py thiếu [[1, 167]]; backend/app/admin/crud/crud_dept.py thiếu [[1, 143]]; backend/app/admin/crud/crud_login_log.py thiếu [[1, 64]]; backend/app/admin/crud/crud_menu.py thiếu [[1, 132]]; backend/app/admin/crud/crud_opera_log.py thiếu [[1, 74]]; backend/app/admin/crud/crud_role.py thiếu [[1, 215]]; backend/app/admin/crud/crud_user.py thiếu [[1, 418]]; backend/app/admin/crud/crud_user_password_history.py thiếu [[1, 34]]; backend/app/admin/model/__init__.py thiếu [[1, 13]]; backend/app/admin/model/data_rule.py thiếu [[1, 25]]; backend/app/admin/model/data_scope.py thiếu [[1, 19]]; backend/app/admin/model/dept.py thiếu [[1, 26]]; backend/app/admin/model/login_log.py thiếu [[1, 35]]; backend/app/admin/model/m2m.py thiếu [[1, 39]]; backend/app/admin/model/menu.py thiếu [[1, 29]]; backend/app/admin/model/opera_log.py thiếu [[1, 38]]; backend/app/admin/model/role.py thiếu [[1, 21]]; backend/app/admin/model/user.py thiếu [[1, 44]]; backend/app/admin/model/user_password_history.py thiếu [[1, 24]]; backend/app/admin/schema/captcha.py thiếu [[1, 12]]; backend/app/admin/schema/data_rule.py thiếu [[1, 55]]; backend/app/admin/schema/data_scope.py thiếu [[1, 57]]; backend/app/admin/schema/dept.py thiếu [[1, 44]]; backend/app/admin/schema/login_log.py thiếu [[1, 46]]; backend/app/admin/schema/menu.py thiếu [[1, 49]]; backend/app/admin/schema/monitor.py thiếu [[1, 102]]; backend/app/admin/schema/opera_log.py thiếu [[1, 54]]; backend/app/admin/schema/role.py thiếu [[1, 74]]; backend/app/admin/schema/token.py thiếu [[1, 50]]; backend/app/admin/schema/user.py thiếu [[1, 121]]; backend/app/admin/schema/user_password_history.py thiếu [[1, 14]]; backend/app/admin/service/auth_service.py thiếu [[1, 272]]; backend/app/admin/service/data_rule_service.py thiếu [[1, 156]]; backend/app/admin/service/data_scope_service.py thiếu [[1, 146]]; backend/app/admin/service/dept_service.py thiếu [[1, 119]]; backend/app/admin/service/login_log_service.py thiếu [[1, 90]]; backend/app/admin/service/menu_service.py thiếu [[1, 137]]; backend/app/admin/service/opera_log_service.py thiếu [[1, 72]]; backend/app/admin/service/plugin_service.py thiếu [[1, 135]]; backend/app/admin/service/role_service.py thiếu [[1, 193]]; backend/app/admin/service/user_password_history_service.py thiếu [[1, 122]]; backend/app/admin/service/user_service.py thiếu [[1, 315]]; backend/app/admin/utils/cache.py thiếu [[1, 98]]; backend/app/admin/utils/password_security.py thiếu [[1, 68]]; backend/app/router.py thiếu [[1, 9]]; backend/app/task/__init__.py thiếu [[1, 7]]; backend/app/task/actions.py thiếu [[1, 11]]; backend/app/task/api/router.py thiếu [[1, 12]]; backend/app/task/api/v1/control.py thiếu [[1, 48]]; backend/app/task/api/v1/result.py thiếu [[1, 55]]; backend/app/task/api/v1/scheduler.py thiếu [[1, 129]]; backend/app/task/celery.py thiếu [[1, 92]]; backend/app/task/crud/crud_result.py thiếu [[1, 49]]; backend/app/task/crud/crud_scheduler.py thiếu [[1, 125]]; backend/app/task/database.py thiếu [[1, 176]]; backend/app/task/enums.py thiếu [[1, 18]]; backend/app/task/model/__init__.py thiếu [[1, 2]]; backend/app/task/model/result.py thiếu [[1, 109]]; backend/app/task/model/scheduler.py thiếu [[1, 80]]; backend/app/task/schema/control.py thiếu [[1, 10]]; backend/app/task/schema/result.py thiếu [[1, 41]]; backend/app/task/schema/scheduler.py thiếu [[1, 50]]; backend/app/task/service/result_service.py thiếu [[1, 57]]; backend/app/task/service/scheduler_service.py thiếu [[1, 159]]; backend/app/task/session.py thiếu [[1, 13]]; backend/app/task/tasks/base.py thiếu [[1, 46]]; backend/app/task/tasks/beat.py thiếu [[1, 34]]; backend/app/task/tasks/db_log/tasks.py thiếu [[1, 21]]; backend/app/task/tasks/tasks.py thiếu [[1, 26]]; backend/app/task/utils/schedulers.py thiếu [[1, 458]]; backend/app/task/utils/tzcrontab.py thiếu [[1, 36]]; backend/cli.py thiếu [[1, 1025]]; backend/common/cache/decorator.py thiếu [[1, 240]]; backend/common/cache/local.py thiếu [[1, 62]]; backend/common/cache/pubsub.py thiếu [[1, 119]]; backend/common/context.py thiếu [[1, 36]]; backend/common/dataclasses.py thiếu [[1, 85]]; backend/common/enums.py thiếu [[1, 156]]; backend/common/exception/errors.py thiếu [[1, 124]]; backend/common/exception/exception_handler.py thiếu [[1, 254]]; backend/common/i18n.py thiếu [[1, 94]]; backend/common/lifespan.py thiếu [[1, 79]]; backend/common/log.py thiếu [[1, 162]]; backend/common/model.py thiếu [[1, 162]]; backend/common/observability/otel.py thiếu [[1, 122]]; backend/common/observability/prometheus/fastapi.py thiếu [[1, 75]]; backend/common/observability/prometheus/queue.py thiếu [[1, 47]]; backend/common/observability/prometheus/sqlalchemy.py thiếu [[1, 37]]; backend/common/pagination.py thiếu [[1, 189]]; backend/common/queue.py thiếu [[1, 85]]; backend/common/response/response_code.py thiếu [[1, 144]]; backend/common/response/response_schema.py thiếu [[1, 166]]; backend/common/schema.py thiếu [[1, 49]]; backend/common/security/jwt.py thiếu [[1, 171]]; backend/common/security/permission.py thiếu [[1, 202]]; backend/common/security/rbac.py thiếu [[1, 86]]; backend/common/security/token.py thiếu [[1, 329]]; backend/common/socketio/__init__.py thiếu [[1, 1]]; backend/common/socketio/actions.py thiếu [[1, 11]]; backend/common/socketio/server.py thiếu [[1, 118]]; backend/core/conf.py thiếu [[1, 360]]; backend/core/path_conf.py thiếu [[1, 37]]; backend/core/registrar.py thiếu [[1, 256]]; backend/database/db.py thiếu [[1, 207]]; backend/database/redis.py thiếu [[1, 190]]; backend/main.py thiếu [[1, 46]]; backend/middleware/access_middleware.py thiếu [[1, 97]]; backend/middleware/i18n_middleware.py thiếu [[1, 55]]; backend/middleware/jwt_auth_middleware.py thiếu [[1, 106]]; backend/middleware/opera_log_middleware.py thiếu [[1, 265]]; backend/middleware/state_middleware.py thiếu [[1, 33]]; backend/plugin/code_generator/api/router.py thiếu [[1, 12]]; backend/plugin/code_generator/api/v1/business.py thiếu [[1, 109]]; backend/plugin/code_generator/api/v1/code_gen.py thiếu [[1, 77]]; backend/plugin/code_generator/api/v1/column.py thiếu [[1, 78]]; backend/plugin/code_generator/crud/crud_business.py thiếu [[1, 99]]; backend/plugin/code_generator/crud/crud_code_gen.py thiếu [[1, 197]]; backend/plugin/code_generator/crud/crud_column.py thiếu [[1, 81]]; backend/plugin/code_generator/enums.py thiếu [[1, 157]]; backend/plugin/code_generator/model/__init__.py thiếu [[1, 2]]; backend/plugin/code_generator/model/business.py thiếu [[1, 29]]; backend/plugin/code_generator/model/column.py thiếu [[1, 29]]; backend/plugin/code_generator/path_conf.py thiếu [[1, 4]]; backend/plugin/code_generator/schema/business.py thiếu [[1, 50]]; backend/plugin/code_generator/schema/code_gen.py thiếu [[1, 11]]; backend/plugin/code_generator/schema/column.py thiếu [[1, 47]]; backend/plugin/code_generator/service/business_service.py thiếu [[1, 103]]; backend/plugin/code_generator/service/code_gen_service.py thiếu [[1, 300]]; backend/plugin/code_generator/service/column_service.py thiếu [[1, 124]]; backend/plugin/code_generator/utils/format_code.py thiếu [[1, 43]]; backend/plugin/code_generator/utils/gen_template.py thiếu [[1, 122]]; backend/plugin/code_generator/utils/type_conversion.py thiếu [[1, 64]]; backend/plugin/config/api/v1/sys/config.py thiếu [[1, 108]]; backend/plugin/config/crud/crud_config.py thiếu [[1, 139]]; backend/plugin/config/enums.py thiếu [[1, 10]]; backend/plugin/config/model/__init__.py thiếu [[1, 1]]; backend/plugin/config/model/config.py thiếu [[1, 23]]; backend/plugin/config/schema/config.py thiếu [[1, 40]]; backend/plugin/config/service/config_service.py thiếu [[1, 141]]; backend/plugin/core.py thiếu [[1, 223]]; backend/plugin/dict/api/v1/sys/dict_data.py thiếu [[1, 117]]; backend/plugin/dict/api/v1/sys/dict_type.py thiếu [[1, 98]]; backend/plugin/dict/crud/crud_dict_data.py thiếu [[1, 169]]; backend/plugin/dict/crud/crud_dict_type.py thiếu [[1, 105]]; backend/plugin/dict/model/__init__.py thiếu [[1, 2]]; backend/plugin/dict/model/dict_data.py thiếu [[1, 27]]; backend/plugin/dict/model/dict_type.py thiếu [[1, 20]]; backend/plugin/dict/schema/dict_data.py thiếu [[1, 43]]; backend/plugin/dict/schema/dict_type.py thiếu [[1, 37]]; backend/plugin/dict/service/dict_data_service.py thiếu [[1, 149]]; backend/plugin/dict/service/dict_type_service.py thiếu [[1, 103]]; backend/plugin/email/api/router.py thiếu [[1, 8]]; backend/plugin/email/api/v1/email.py thiếu [[1, 32]]; backend/plugin/email/requirements.txt thiếu [[1, 1]]; backend/plugin/email/utils/dynamic_config.py thiếu [[1, 20]]; backend/plugin/email/utils/send.py thiếu [[1, 73]]; backend/plugin/errors.py thiếu [[1, 10]]; backend/plugin/hooks.py thiếu [[1, 148]]; backend/plugin/installer.py thiếu [[1, 235]]; backend/plugin/notice/api/v1/sys/notice.py thiếu [[1, 90]]; backend/plugin/notice/crud/crud_notice.py thiếu [[1, 96]]; backend/plugin/notice/enums.py thiếu [[1, 8]]; backend/plugin/notice/model/__init__.py thiếu [[1, 1]]; backend/plugin/notice/model/notice.py thiếu [[1, 17]]; backend/plugin/notice/schema/notice.py thiếu [[1, 40]]; backend/plugin/notice/service/notice_service.py thiếu [[1, 100]]; backend/plugin/oauth2/api/router.py thiếu [[1, 12]]; backend/plugin/oauth2/api/v1/github.py thiếu [[1, 72]]; backend/plugin/oauth2/api/v1/google.py thiếu [[1, 72]]; backend/plugin/oauth2/api/v1/user_social.py thiếu [[1, 27]]; backend/plugin/oauth2/crud/crud_user_social.py thiếu [[1, 98]]; backend/plugin/oauth2/enums.py thiếu [[1, 15]]; backend/plugin/oauth2/model/__init__.py thiếu [[1, 1]]; backend/plugin/oauth2/model/user_social.py thiếu [[1, 23]]; backend/plugin/oauth2/requirements.txt thiếu [[1, 1]]; backend/plugin/oauth2/schema/user_social.py thiếu [[1, 29]]; backend/plugin/oauth2/service/oauth2_service.py thiếu [[1, 221]]; backend/plugin/oauth2/service/user_social_service.py thiếu [[1, 101]]; backend/plugin/patching.py thiếu [[1, 25]]; backend/plugin/requirements.py thiếu [[1, 156]]; backend/plugin/router.py thiếu [[1, 120]]; backend/plugin/settings_source.py thiếu [[1, 49]]; backend/plugin/sql.py thiếu [[1, 55]]; backend/plugin/status.py thiếu [[1, 83]]; backend/plugin/validator.py thiếu [[1, 267]]; backend/run.py thiếu [[1, 21]]; backend/utils/async_helper.py thiếu [[1, 82]]; backend/utils/build_tree.py thiếu [[1, 132]]; backend/utils/console.py thiếu [[1, 28]]; backend/utils/demo_mode.py thiếu [[1, 22]]; backend/utils/dynamic_config.py thiếu [[1, 84]]; backend/utils/dynamic_import.py thiếu [[1, 73]]; backend/utils/encrypt.py thiếu [[1, 119]]; backend/utils/file_ops.py thiếu [[1, 66]]; backend/utils/format.py thiếu [[1, 22]]; backend/utils/limiter.py thiếu [[1, 324]]; backend/utils/locks.py thiếu [[1, 32]]; backend/utils/openapi.py thiếu [[1, 29]]; backend/utils/pattern_validate.py thiếu [[1, 89]]; backend/utils/performance.py thiếu [[1, 39]]; backend/utils/request_parse.py thiếu [[1, 129]]; backend/utils/serializers.py thiếu [[1, 388]]; backend/utils/snowflake.py thiếu [[1, 242]]; backend/utils/sql_parser.py thiếu [[1, 42]]; backend/utils/timezone.py thiếu [[1, 77]]; backend/utils/trace_id.py thiếu [[1, 31]]; pyproject.toml thiếu [[1, 293]]; requirements.txt thiếu [[1, 447]]
- **File ngoài phạm vi đọc.** migration: 1 file, test: 7 file. Route trong các file này không vào tài liệu (FR-028 Phạm vi đọc)
- **Dòng trông giống route hoặc lời gọi HTTP nhưng chưa được xác nhận, nên không có trong tài liệu.** `backend/app/admin/api/v1/auth/auth.py:19`, `backend/app/admin/api/v1/auth/auth.py:27`, `backend/app/admin/api/v1/auth/auth.py:43`, `backend/app/admin/api/v1/auth/auth.py:49`, `backend/app/admin/api/v1/auth/auth.py:55`, `backend/app/admin/api/v1/auth/captcha.py:19`, `backend/app/admin/api/v1/log/login_log.py:17`, `backend/app/admin/api/v1/log/login_log.py:36`, `backend/app/admin/api/v1/log/login_log.py:51`, `backend/app/admin/api/v1/log/opera_log.py:17`, `backend/app/admin/api/v1/log/opera_log.py:36`, `backend/app/admin/api/v1/log/opera_log.py:51`, `backend/app/admin/api/v1/monitor/online.py:22`, `backend/app/admin/api/v1/monitor/online.py:109`, `backend/app/admin/api/v1/monitor/redis.py:12`, `backend/app/admin/api/v1/monitor/server.py:30`, `backend/app/admin/api/v1/sys/data_rule.py:24`, `backend/app/admin/api/v1/sys/data_rule.py:30`, `backend/app/admin/api/v1/sys/data_rule.py:38`, `backend/app/admin/api/v1/sys/data_rule.py:44`, `backend/app/admin/api/v1/sys/data_rule.py:50`, `backend/app/admin/api/v1/sys/data_rule.py:59`, `backend/app/admin/api/v1/sys/data_rule.py:75`, `backend/app/admin/api/v1/sys/data_rule.py:88`, `backend/app/admin/api/v1/sys/data_rule.py:107`, `backend/app/admin/api/v1/sys/data_scope.py:24`, `backend/app/admin/api/v1/sys/data_scope.py:30`, `backend/app/admin/api/v1/sys/data_scope.py:39`, `backend/app/admin/api/v1/sys/data_scope.py:48`, `backend/app/admin/api/v1/sys/data_scope.py:65`, `backend/app/admin/api/v1/sys/data_scope.py:78`, `backend/app/admin/api/v1/sys/data_scope.py:97`, `backend/app/admin/api/v1/sys/data_scope.py:116`, `backend/app/admin/api/v1/sys/dept.py:18`, `backend/app/admin/api/v1/sys/dept.py:26`, `backend/app/admin/api/v1/sys/dept.py:41`, `backend/app/admin/api/v1/sys/dept.py:54`, `backend/app/admin/api/v1/sys/dept.py:71`, `backend/app/admin/api/v1/sys/file.py:14`, `backend/app/admin/api/v1/sys/menu.py:16`, `backend/app/admin/api/v1/sys/menu.py:22`, `backend/app/admin/api/v1/sys/menu.py:30`, `backend/app/admin/api/v1/sys/menu.py:40`, `backend/app/admin/api/v1/sys/menu.py:53`, `backend/app/admin/api/v1/sys/menu.py:70`, `backend/app/admin/api/v1/sys/plugin.py:16`, `backend/app/admin/api/v1/sys/plugin.py:22`, `backend/app/admin/api/v1/sys/plugin.py:28`, `backend/app/admin/api/v1/sys/plugin.py:48`, `backend/app/admin/api/v1/sys/plugin.py:61`, `backend/app/admin/api/v1/sys/plugin.py:67`, `backend/app/admin/api/v1/sys/role.py:26`, `backend/app/admin/api/v1/sys/role.py:32`, `backend/app/admin/api/v1/sys/role.py:41`, `backend/app/admin/api/v1/sys/role.py:49`, `backend/app/admin/api/v1/sys/role.py:57`, `backend/app/admin/api/v1/sys/role.py:74`, `backend/app/admin/api/v1/sys/role.py:87`, `backend/app/admin/api/v1/sys/role.py:104`, `backend/app/admin/api/v1/sys/role.py:123`, `backend/app/admin/api/v1/sys/role.py:142`, `backend/app/admin/api/v1/sys/user.py:25`, `backend/app/admin/api/v1/sys/user.py:31`, `backend/app/admin/api/v1/sys/user.py:40`, `backend/app/admin/api/v1/sys/user.py:48`, `backend/app/admin/api/v1/sys/user.py:67`, `backend/app/admin/api/v1/sys/user.py:76`, `backend/app/admin/api/v1/sys/user.py:88`, `backend/app/admin/api/v1/sys/user.py:101`, `backend/app/admin/api/v1/sys/user.py:111`, `backend/app/admin/api/v1/sys/user.py:123`, `backend/app/admin/api/v1/sys/user.py:135`, `backend/app/admin/api/v1/sys/user.py:147`, `backend/app/admin/api/v1/sys/user.py:160`, `backend/app/task/api/v1/control.py:17`, `backend/app/task/api/v1/control.py:35`, `backend/app/task/api/v1/result.py:17`, `backend/app/task/api/v1/result.py:26`, `backend/app/task/api/v1/result.py:43`, `backend/app/task/api/v1/scheduler.py:21`, `backend/app/task/api/v1/scheduler.py:27`, `backend/app/task/api/v1/scheduler.py:36`, `backend/app/task/api/v1/scheduler.py:53`, `backend/app/task/api/v1/scheduler.py:66`, `backend/app/task/api/v1/scheduler.py:85`, `backend/app/task/api/v1/scheduler.py:102`, `backend/app/task/api/v1/scheduler.py:119`, `backend/plugin/code_generator/api/v1/business.py:23`, `backend/plugin/code_generator/api/v1/business.py:29`, `backend/plugin/code_generator/api/v1/business.py:38`, `backend/plugin/code_generator/api/v1/business.py:54`, `backend/plugin/code_generator/api/v1/business.py:63`, `backend/plugin/code_generator/api/v1/business.py:76`, `backend/plugin/code_generator/api/v1/business.py:95`, `backend/plugin/code_generator/api/v1/code_gen.py:18`, `backend/plugin/code_generator/api/v1/code_gen.py:27`, `backend/plugin/code_generator/api/v1/code_gen.py:40`, `backend/plugin/code_generator/api/v1/code_gen.py:48`, `backend/plugin/code_generator/api/v1/code_gen.py:56`, `backend/plugin/code_generator/api/v1/code_gen.py:70`, `backend/plugin/code_generator/api/v1/column.py:20`, `backend/plugin/code_generator/api/v1/column.py:26`, `backend/plugin/code_generator/api/v1/column.py:34`, `backend/plugin/code_generator/api/v1/column.py:47`, `backend/plugin/code_generator/api/v1/column.py:64`, `backend/plugin/config/api/v1/sys/config.py:22`, `backend/plugin/config/api/v1/sys/config.py:31`, `backend/plugin/config/api/v1/sys/config.py:39`, `backend/plugin/config/api/v1/sys/config.py:56`, `backend/plugin/config/api/v1/sys/config.py:69`, `backend/plugin/config/api/v1/sys/config.py:77`, `backend/plugin/config/api/v1/sys/config.py:94`, `backend/plugin/dict/api/v1/sys/dict_data.py:22`, `backend/plugin/dict/api/v1/sys/dict_data.py:28`, `backend/plugin/dict/api/v1/sys/dict_data.py:37`, `backend/plugin/dict/api/v1/sys/dict_data.py:46`, `backend/plugin/dict/api/v1/sys/dict_data.py:73`, `backend/plugin/dict/api/v1/sys/dict_data.py:86`, `backend/plugin/dict/api/v1/sys/dict_data.py:105`, `backend/plugin/dict/api/v1/sys/dict_type.py:22`, `backend/plugin/dict/api/v1/sys/dict_type.py:28`, `backend/plugin/dict/api/v1/sys/dict_type.py:37`, `backend/plugin/dict/api/v1/sys/dict_type.py:54`, `backend/plugin/dict/api/v1/sys/dict_type.py:67`, `backend/plugin/dict/api/v1/sys/dict_type.py:86`, `backend/plugin/email/api/v1/email.py:18`, `backend/plugin/notice/api/v1/sys/notice.py:22`, `backend/plugin/notice/api/v1/sys/notice.py:30`, `backend/plugin/notice/api/v1/sys/notice.py:48`, `backend/plugin/notice/api/v1/sys/notice.py:61`, `backend/plugin/notice/api/v1/sys/notice.py:78`, `backend/plugin/oauth2/api/v1/github.py:24`, `backend/plugin/oauth2/api/v1/github.py:38`, `backend/plugin/oauth2/api/v1/google.py:24`, `backend/plugin/oauth2/api/v1/google.py:38`, `backend/plugin/oauth2/api/v1/user_social.py:12`, `backend/plugin/oauth2/api/v1/user_social.py:18`, `backend/plugin/oauth2/api/v1/user_social.py:24`, `backend/utils/request_parse.py:49`, `backend/utils/request_parse.py:92`

## Phụ lục: file cho máy

- TBL (DDL): [tech-specs/BACKEND/schema/TBL-FASTAPI-BEST-ARCHITECTURE-BACKEND.md](tech-specs/BACKEND/schema/TBL-FASTAPI-BEST-ARCHITECTURE-BACKEND.md) — component backend
- EVT: [tech-specs/BACKEND/events/EVT-FASTAPI-BEST-ARCHITECTURE-BACKEND-UNKNOWN-5B1745FDB84B.md](tech-specs/BACKEND/events/EVT-FASTAPI-BEST-ARCHITECTURE-BACKEND-UNKNOWN-5B1745FDB84B.md) — component backend
- EVT: [tech-specs/BACKEND/events/EVT-FASTAPI-BEST-ARCHITECTURE-BACKEND-BACKEND-APP-TASK-TASKS-DB-LOG-TASKS-DELETE-DB-OPERA-LOG.md](tech-specs/BACKEND/events/EVT-FASTAPI-BEST-ARCHITECTURE-BACKEND-BACKEND-APP-TASK-TASKS-DB-LOG-TASKS-DELETE-DB-OPERA-LOG.md) — component backend
- EVT: [tech-specs/BACKEND/events/EVT-FASTAPI-BEST-ARCHITECTURE-BACKEND-BACKEND-APP-TASK-TASKS-DB-LOG-TASKS-DELETE-DB-LOGIN-LOG.md](tech-specs/BACKEND/events/EVT-FASTAPI-BEST-ARCHITECTURE-BACKEND-BACKEND-APP-TASK-TASKS-DB-LOG-TASKS-DELETE-DB-LOGIN-LOG.md) — component backend
- EVT: [tech-specs/BACKEND/events/EVT-FASTAPI-BEST-ARCHITECTURE-BACKEND-UNKNOWN-D0AB78CAF236.md](tech-specs/BACKEND/events/EVT-FASTAPI-BEST-ARCHITECTURE-BACKEND-UNKNOWN-D0AB78CAF236.md) — component backend
