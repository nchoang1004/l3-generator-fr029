# Báo cáo giám khảo độc lập — phần bảng CSDL (12/10/2026)

Hash 7 file đóng băng: **cả 7 khớp** (`sha256sum -c hashes.txt` đều OK). `hashes.txt` không có hash cho TBL của tdd-docker vì repo đó không có file TBL. Không mở `judge-round1\`, không đọc `l3-generator-l3\`, `.aide`, `gold*`, `final-*.json`, `membership.json`. Không chạy code của repo. Không sửa đầu ra.

Cách làm: đọc tay mọi file model trong source (mixin, alias `Annotated` `id_key`, `__table_args__`, `sa.Table`, migration). Dùng script chỉ để so mục 4 với file TBL và kiểm dòng bằng chứng (script đọc markdown và source, không chạy repo).

## A. Chính xác

| Repo | Bảng trong tài liệu | Bảng đúng | Cột | Cột đúng |
|---|---|---|---|---|
| fastapi_best_architecture | 23 | 23 | 248 | 248 |
| orderflow | 4 | 4 | 27 | 27 |
| full-stack-fastapi-template | 2 | 2 | 12 | 10 |
| tdd-docker | 0 (ghi ở giới hạn) | không áp dụng | — | — |
| **Tổng** | **29** | **29** | **287** | **285** |

Đã kiểm cho mọi bảng: tên bảng, lớp hoặc `Table(...)`, dòng khai, từng cột (tên, kiểu như khai, khóa chính, khóa ngoại, nullable, unique/index/ondelete), ràng buộc cấp bảng (14 `UniqueConstraint`, đều đúng tên và cột), số cột ở bảng tóm tắt.

Chỗ sai (nhỏ), full-stack-fastapi-template:
1. `user.created_at` (`backend/app/models.py:55`) và `item.created_at` (`:93`): tài liệu ghi kiểu `datetime`. Code khai `sa_type=DateTime(timezone=True)` (dòng 57 và 95). Kiểu SQL khai rõ bị bỏ, chỉ còn kiểu Python.

Thiếu chi tiết nhưng không tính là sai:
- `email`, `full_name`, `title`, `description` có `max_length=255` (`models.py:15, 18, 75, 76`); tài liệu ghi `str`/`EmailStr`, mất độ dài.
- fastapi: bảng `task_result` khai đầu tiên ở lớp cha `Task` (`result.py:14`, tên bảng dòng 17). Tài liệu nêu `TaskExtended` ở `:54` (lớp mở rộng, `extend_existing`). Cột đã gộp đủ 12. Không sai, nhưng người đọc không thấy lớp `Task`.
- File TBL **không có** unique, index, ondelete (chỉ mục 4 của `TAI-LIEU.md` có). Ví dụ `order_items.order_id` trong TBL chỉ ghi `orders.id`, mất `CASCADE`.

Kiểm chéo: mục 4 và TBL khớp nhau hoàn toàn (tập cột, khóa chính, nullable) ở cả 3 repo có bảng. Dòng bằng chứng `file:dòng` của 287 cột: 287/287 trỏ đúng dòng có tên cột (hoặc dòng mixin/alias tương ứng).

Dấu `*`: đã kiểm từng nhóm. Cột có `nullable=True/False` khai thẳng (task_result.result, date_done, name, args...; item.owner_id) không có `*`: đúng. Cột chỉ có `Mapped[X | None]` hoặc không khai có `*`: đúng. Không thấy chỗ gắn `*` sai.

## B. Đầy đủ

- fastapi_best_architecture: 23 bảng = 9 lớp admin + 4 `sa.Table` (`m2m.py`) + 7 lớp plugin + 3 bảng task. Grep `__tablename__`, `Table(`, `ForeignKey`, `CREATE TABLE`, `create_table`: không thiếu, không thừa. Source **không có** `ForeignKey` nào; cột khóa ngoại "—" là đúng. Không có migration (chỉ `alembic/env.py`). `backend/sql/*.sql` chỉ nạp dữ liệu.
- orderflow: 4 bảng, đủ. Không có migration.
- full-stack: 2 bảng `table=True` (`User`, `Item`), đủ. Migration alembic chỉ tạo `user`, `item`.
- tdd-docker: 2 bảng thật (`textsummary` từ Tortoise `TextSummary`, `aerich` chỉ có trong migration). Mục 11 liệt kê cả hai kèm dòng (`tortoise.py:5`, `0_...init.py:6` và `:12`, đã đối chiếu đúng). Không nói "không có bảng". Không bảng thừa.

Chưa nêu (nhẹ, không bắt buộc): tdd-docker có `project/db/create.sql` (`CREATE DATABASE web_dev/web_test`). Đó là tạo database, không phải bảng.

## C. Đúng chuẩn

| Mục | Kết quả |
|---|---|
| Đọc SQLAlchemy / SQLModel / `Table(...)` | Đạt. Đọc được `__tablename__`, `table=True`, `sa.Table`. |
| ORM khác và bảng chỉ có trong migration ghi ở giới hạn kèm nơi dùng | Đạt (tdd-docker, mục 11). |
| Tên bảng, lớp, vị trí khai | Đạt. Không có dòng sai. |
| Cột: tên, kiểu, PK, FK (bảng và cột đích), nullable | Đạt về dữ kiện: 285/287. Hai chỗ `created_at` thiếu kiểu SQL khai. |
| Truy vết `file:dòng` từng bảng và cột | Đạt: 287/287. |
| Nhãn mỗi dòng | Đạt trong file TBL (inferred kèm tên quy tắc `sqlalchemy-defaults-v1` / `sqlmodel-default-tablename-v1`, hoặc unknown kèm lý do). Mục 4 dùng dấu `*` thay nhãn từng dòng. |
| DDL theo biến thể SQL; chưa biết thì không có DDL kèm lý do | Đạt về hình thức: cả 3 repo không có DDL, ghi "dialect chưa biết". Nội dung lý do chưa chính xác hẳn, xem dưới. |
| Không mặc định PostgreSQL | Đạt. |
| Mặc định ORM ghi inferred; không suy tên bảng từ tên lớp (trừ SQLModel) | Đạt. `user`, `item` ghi suy luận kèm quy tắc SQLModel. |

Lưu ý về dialect (không chắc nên không kết luận là lỗi):
- full-stack: `backend/app/core/config.py:37-39` đổi URL sang `postgresql+psycopg://`; migration dùng `sqlalchemy.dialects.postgresql`. Dialect xác định được là PostgreSQL, tài liệu lại ghi "chưa rõ" và không có DDL.
- orderflow: `docker-compose.yml` và `.env.example` dùng `postgresql+asyncpg`; `config.py` mặc định `sqlite+aiosqlite`. Có hai biến thể, nên "chưa rõ" hợp lý; nhưng lý do ghi trong tài liệu (thiếu `create_all`) không nói điều này.
- fastapi_best_architecture: loại DB nằm ở `settings.DATABASE_TYPE` (mysql hoặc postgresql), "chưa rõ" là đúng.

## D. Dễ đọc — 3/5

Tốt: bảng tóm tắt đầu mục (bảng, lớp, số cột, khóa ngoại tới); mỗi bảng một bảng cột 6 cột cố định; chú thích `*` một lần ở đầu; ràng buộc cấp bảng ghi riêng.

Chỗ rối, thừa, khó hiểu:
- Mục 4 của fastapi dài ~470 dòng. 4 cột mixin lặp ở 13 bảng (`| created_time | TimeZone | không\* | — | không\* | — |` ...) mà không nói chúng đến từ lớp `Base`.
- `TimeZone`, `UniversalText` không được giải thích (lớp tự định nghĩa ở `backend/common/model.py`). Kiểu trộn `BigInteger` (từ alias `id_key`) với `sa.BigInteger` (khai tại chỗ): cùng một kiểu, hai cách viết.
- Cột "Khóa ngoại tới" của bảng tóm tắt fastapi toàn "—" ở 23 bảng, trong khi source có nhiều khóa ngoại logic (`dept_id`, `type_id`, `user_id`, `parent_id`, `code_gen_business_id`, các bảng m2m; source ghi chú "逻辑外键"). Người đọc không thấy quan hệ giữa bảng.
- Dấu `\*` hiện thô trong ô (`không\*`); cột PK ghi "không\*" cho mọi cột thường: nhiều nhiễu, ít thông tin.
- Bốn bảng m2m ghi PK "có" cho cả 3 cột nhưng không nói đây là khóa chính ghép.
- File TBL: ô kiểu lặp nguyên văn "unknown — Chưa xác định SQL dialect từ source; khai trong code: sa.BigInteger" ở mọi dòng; ô nhãn lặp "inferred: primary_key, nullable (sqlalchemy-defaults-v1); unknown: type"; đoạn đầu mỗi bảng chứa hàng chục `ev:<hash>` rất dài. Khó đọc với người, hợp với máy.
- Cột mixin đứng trước `id` (fastapi), khác thứ tự thật trong DB (`sort_order`) và khác thói quen người đọc.
- Hai repo nhỏ (orderflow, full-stack) đọc dễ, khoảng 4/5.

## Tóm tắt lỗi quan trọng

1. Không có lỗi nặng: 29/29 bảng, 285/287 cột đúng, không bảng thiếu hay thừa.
2. Sai nhẹ: kiểu `created_at` của full-stack (bỏ `DateTime(timezone=True)`); mất `max_length=255` ở 4 cột.
3. File TBL thiếu unique, index, ondelete (chỉ có ở mục 4).
4. Dialect PostgreSQL của full-stack xác định được nhưng tài liệu ghi "chưa rõ"; lý do cho orderflow chưa chính xác.
5. Dễ đọc kém ở repo lớn: lặp mixin, kiểu tự định nghĩa không giải thích, quan hệ logic giữa bảng không hiện.