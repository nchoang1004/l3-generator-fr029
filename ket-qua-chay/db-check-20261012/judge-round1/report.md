# Báo cáo giám khảo độc lập: phần bảng CSDL

Chấm ngày 12/10/2026. Chỉ đọc `TAI-LIEU.md` mục 4 (và dòng "Bảng CSDL" ở bảng tóm tắt, mục 11), file `TBL-*.md`, và source của 4 repo. Không đọc thư mục bị cấm, không chạy code repo, không dùng mạng. Không sửa đầu ra.

## 0. Kiểm hash

7/7 file khớp `hashes.txt` (`sha256sum -c`: OK). Lưu ý: tdd-docker chỉ có hash cho `TAI-LIEU.md` vì repo này không có file TBL.

## A. Chính xác

Cách làm: dùng `ast.parse` đọc source (không chạy code repo), dựng bảng và cột kỳ vọng, rồi đối chiếu tự động với mục 4 và với file TBL. fastapi_best_architecture, full-stack-fastapi-template và orderflow được duyệt thêm bằng mắt.

| Repo | Bảng đúng | Cột đúng (đủ cả ràng buộc) | Cột đúng (tên, kiểu, PK, FK, nullable) |
|---|---|---|---|
| fastapi_best_architecture | 23/23 | 231/248 | 248/248 |
| full-stack-fastapi-template | 2/2 | 11/12 | 12/12 |
| orderflow | 4/4 | 27/27 | 27/27 |
| tdd-docker | không ghi bảng nào (xem B) | 0 | 0 |
| **Tổng** | **29/29** | **269/287** | **287/287** |

"Bảng đúng" gồm tên bảng, lớp hoặc cách khai, và `file:dòng` khai báo. Mọi `file:dòng` của bảng và cột (cả mục 4 lẫn TBL) khớp source; không lệch dòng nào. Cột "Số cột" khớp. Kiểu cột ghi đúng như khai.

18 chỗ sai, đều ở cột "Ràng buộc" (mục 4):

1. **17 cột `id` của fastapi_best_architecture** ghi "—". Cột này lấy từ `id_key` (`backend/common/model.py:17-40`), khai `unique=True, index=True`. Bốn bảng `Table(...)` trong `m2m.py` thì được ghi đúng "unique, index", nên tài liệu không nhất quán. Dòng khai `id` sai theo bảng:
   - `business.py:17`, `column.py:17`, `config.py:17`
   - `data_rule.py:17`, `data_scope.py:17`, `dept.py:17`
   - `dict_data.py:17`, `dict_type.py:17`, `role.py:17`
   - `login_log.py:16`, `opera_log.py:16`, `user_password_history.py:16`
   - `menu.py:13`, `notice.py:13`
   - `user.py:22`, `user_social.py:18`, `scheduler.py:28`
2. **`item.owner_id`** (full-stack, `backend/app/models.py:97-99`) có `ondelete="CASCADE"` nhưng ghi "—". Orderflow thì ghi đúng `xóa theo: CASCADE`.

Điều chưa chắc: `task_result` ghi lớp `TaskExtended` (`result.py:54`). Lớp cha `Task` (`result.py:14`) cũng khai `__tablename__='task_result'`. Tôi coi cách chọn này là chấp nhận được và vẫn tính đúng.

## B. Đầy đủ

Tự quét độc lập bằng grep và `ast` trên toàn bộ source (`__tablename__`, `table=True`, `Table(`, `Column(`, `mapped_column(`, `create_table`, `CREATE TABLE`, `models.Model`, lớp con của `Base`, `DataClassBase`, `MappedBase`).

- **Không có bảng thiếu hay thừa** trong 3 repo có bảng đọc được:
  - fastapi_best_architecture: 19 lớp + 4 `sa.Table` = 23 bảng. `Task` và `TaskExtended` cùng một bảng.
  - full-stack: 2 bảng.
  - orderflow: 4 bảng.
- **Không có cột thừa.** Cột thừa kế từ `Base` (`created_time`, `updated_time`, `deleted`, `deleted_time`) được liệt kê đúng.
- **Thiếu thông tin** (không tính là lỗi bảng hoặc cột):
  - fastapi_best_architecture: 12 ràng buộc unique ghép trong `__table_args__` (dạng `uk_*_deleted`, ở `data_rule.py:12`, `user.py:16`, `scheduler.py:23`, `user_social.py:12`...) không xuất hiện ở đâu.
  - fastapi_best_architecture: khóa ngoại logic (`parent_id`, `dept_id`, `user_id`, `type_id`...) chỉ nằm trong comment `逻辑外键`. Tài liệu ghi cột "Khóa ngoại" là "—" và không nói gì thêm. Đây không phải lỗi vì source không khai FK thật, nhưng người đọc không thấy quan hệ.
  - tdd-docker: có 2 bảng trong `migrations/models/0_20250421234125_init.py:6-19` (`textsummary`, `aerich`). Mục 11 chỉ ghi "migration: 1 file", không nêu tên bảng.
  - orderflow: 3 service dùng 3 CSDL riêng (`docker-compose.yml:22,40,61`), nhưng mục 4 gộp chung 4 bảng.

## C. Đúng chuẩn

| Mục chuẩn | Kết quả |
|---|---|
| Đọc SQLAlchemy `__tablename__`, SQLModel `table=True`, `Table(...)` | **Đạt.** Không sót bảng nào. |
| ORM khác, SQL tay, bảng trong migration: ghi ở giới hạn kèm nơi dùng; không nói repo không có bảng | **Đạt một phần.** tdd-docker ghi "Tortoise: app/models/tortoise.py:5 (TextSummary)" và mục 4 không phủ nhận bảng. Nhưng các bảng trong migration không được nêu tên. |
| TBL: tên bảng, lớp, vị trí | **Đạt**, 29/29. |
| TBL: tên, kiểu, PK, FK (bảng và cột đích), nullable | **Đạt**, 287/287. Hai FK đều ghi đúng: `user.id`, `orders.id`. |
| Truy vết `file:dòng` từng bảng, cột | **Đạt.** Khớp 100% dòng đã kiểm. |
| Nhãn exact / inferred kèm quy tắc / unknown kèm lý do | **Không đạt về độ chính xác.** Cả 3 file TBL có 365 dòng cột, tất cả đều ghi `inferred: sqlalchemy-defaults-v1; unknown: type`, và không có nhãn `exact` nào. Nhiều giá trị khai tường minh nên phải là exact: `primary_key=True`, `nullable=False` của `item.owner_id` (`models.py:97`), `nullable=True` của `task_result.result` (`result.py:23`), và `__tablename__`. Hình thức thì đủ: dòng nào cũng có nhãn, và `unknown: type` có lý do dialect chưa rõ. |
| DDL theo biến thể SQL; chưa biết thì không DDL, ghi lý do | **Đạt.** Cả 3 file chỉ có `-- omitted: ... dialect chưa biết`. fba cấu hình được mysql hoặc postgresql (`conf.py:49`), orderflow dùng cả sqlite và postgres, nên "chưa rõ" là hợp lý. |
| Mặc định ORM ghi inferred; không suy tên bảng từ tên lớp, trừ SQLModel có ghi quy tắc | **Đạt một phần.** Nullable mặc định ghi inferred đúng. Quy tắc `sqlmodel-default-tablename-v1` có trong chú thích [1] của `TAI-LIEU.md` (full-stack) nhưng **không có** trong file TBL của repo đó (0 lần xuất hiện). |

## D. Dễ đọc: 3/5

Điểm tốt:
- Có bảng tóm tắt ở đầu mục 4 (bảng, lớp, số cột, FK).
- Mỗi bảng có bảng cột riêng, cột Ràng buộc ngắn gọn.
- Nhắc rõ dialect chưa rõ.

Chỗ rối hoặc thừa (trích nguyên văn):
- Câu mở đầu mục 4 dùng thuật ngữ nội bộ, và ở full-stack/orderflow nhắc `Base` trong khi repo dùng SQLModel hoặc nhiều `Base`: "Không có Base.metadata.create_all(engine) nối base này với một engine có URL literal; Metadata của bảng chưa được nối với một engine có URL literal".
- Chú thích [1] lẫn tên quy tắc và tiếng Anh, khó hiểu với người mới: "không khai primary_key thì là False; sqlalchemy-defaults-v1: nullable mặc định là not primary_key; với Mapped/SQLModel theo Optional". Chú thích [2] cụt: "nullable mặc định là not primary_key; ...".
- Cột "Component" luôn là "backend" (hoặc "services"), không thêm thông tin.
- Dòng "Mức chắc chắn: suy luận [1]" lặp ở mọi bảng, kể cả bảng có `__tablename__` tường minh (mâu thuẫn với cột "Nhãn" của TBL).
- fastapi_best_architecture: mục 4 dài khoảng 440 dòng. 4 cột `created_time`, `updated_time`, `deleted`, `deleted_time` lặp ở 17 bảng, trong khi tên lớp mixin không được nêu.
- Cột "Kiểu" trộn kiểu viết khác nhau trong cùng bảng ("TimeZone", "BigInteger", "sa.String(64)", "int"). Với `UniversalText`, `TimeZone`, `id_key` là kiểu tự định nghĩa, không có giải thích.
- Người mới không biết bảng nào liên quan bảng nào: không có quan hệ logic (`sys_user.dept_id` → `sys_dept`), và các bảng nối m2m không được giải thích.
- Tài liệu bảng của task_result chỉ nhắc `TaskExtended`, người đọc không biết đây là lớp con của `Task`.

## Kết luận ngắn

Thông tin cấu trúc (tên bảng, cột, kiểu, PK, FK, nullable, dòng) chính xác tuyệt đối trên 29 bảng và 287 cột. Điểm yếu nằm ở: bỏ sót ràng buộc unique/index của `id_key` và `ondelete`, bỏ sót ràng buộc unique ghép, nhãn `exact` chưa bao giờ được dùng, bảng trong migration của tdd-docker không được nêu tên, và văn phong mục 4 còn nặng thuật ngữ, lặp.
