# Đề bài cho giám khảo độc lập — phần bảng CSDL

Viết ngày 12/10/2026, trước khi chấm; không sửa sau khi có kết quả.

## Việc của bạn

Một công cụ đọc source Python và sinh tài liệu bảng CSDL. Kiểm phần đó có **chính xác, đầy đủ, đúng chuẩn, dễ đọc** không, trên 4 repo.

| Repo | Source | Đầu ra (đã đóng băng, hash ở `D:\VSF\dbcheck\hashes.txt`) |
|---|---|---|
| fastapi_best_architecture | `D:\VSF\l3-generator-golden-v2\sample-repos\fastapi-practices_fastapi_best_architecture-123a44a\` | `D:\VSF\dbcheck\fastapi_best_architecture\out\` |
| orderflow | `D:\VSF\l3-heldout-repos2\AlexGoster_orderflow-services\` | `D:\VSF\dbcheck\orderflow\out\` |
| full-stack-fastapi-template | `D:\VSF\l3-generator-golden-v2\sample-repos\full-stack-fastapi-template-cb740b6\` | `D:\VSF\dbcheck\full-stack-fastapi-template\out\` |
| tdd-docker | `D:\VSF\l3-acceptance-repos\testdrivenio_fastapi-tdd-docker-16433b6\project\` | `D:\VSF\dbcheck\tdd-docker\out\` |

Trong mỗi thư mục đầu ra, chỉ chấm: mục "## 4. Bảng CSDL" (và dòng "Bảng CSDL" ở bảng tóm tắt đầu file, mục 11 nếu nói về bảng) của `TAI-LIEU.md`, và file `tech-specs/*/schema/TBL-*.md`.

**Không được đọc:** mọi file dưới `D:\VSF\l3-generator-l3\`, `D:\VSF\l3-generator-golden-v2\.aide\`, mọi file tên `gold*`, `final-*.json`, `membership.json`. Không chạy code của repo. Không dùng mạng.

## Chuẩn (rút từ yêu cầu FR-L3GEN-030 của dự án)

- Đọc được: lớp SQLAlchemy có `__tablename__`, lớp SQLModel có `table=True`, `Table(...)` của SQLAlchemy. ORM khác (Tortoise, Peewee, Beanie...), SQL viết tay, bảng chỉ có trong migration: phải ghi ở phần giới hạn kèm nơi dùng, **không được** nói repo không có bảng.
- File TBL, mỗi bảng: tên bảng, lớp model và vị trí khai báo; bảng cột: tên, kiểu, khóa chính, khóa ngoại (bảng và cột đích), nullable. Truy vết `file:dòng` của từng bảng và cột. Mỗi dòng mang nhãn exact, inferred kèm tên quy tắc, hoặc unknown kèm lý do. Khối DDL theo biến thể SQL của repo; chưa biết biến thể thì không có DDL và ghi lý do; không mặc định PostgreSQL.
- Giá trị từ mặc định của ORM (cột không khai nullable thì cho null, trừ khóa chính) ghi inferred. Không suy tên bảng từ tên lớp (trừ quy tắc SQLModel đã ghi rõ).

## Cần làm

A. **Chính xác:** với mỗi bảng trong tài liệu, mở model trong source, kiểm tên bảng, lớp/cách khai, vị trí, từng cột (tên, kiểu như khai, khóa chính, khóa ngoại, nullable, ràng buộc unique/index/ondelete nếu có). Đếm đúng/sai, liệt kê mọi chỗ sai kèm `file:dòng`.

B. **Đầy đủ:** tự quét source (grep `__tablename__`, `table=True`, `Table(`, `Column(`, `mapped_column(`, `create_table`, `CREATE TABLE`, `models.Model`, `Document`) tìm bảng hoặc cột bị thiếu, bảng thừa, cột thừa.

C. **Đúng chuẩn:** đi qua từng gạch đầu dòng của mục "Chuẩn", ghi đạt / không đạt kèm dẫn chứng.

D. **Dễ đọc:** một lập trình viên mới đọc mục 4 có hiểu cấu trúc dữ liệu không? Liệt kê chỗ rối, thừa, khó hiểu (trích nguyên văn). Điểm 1–5.

## Cách trả lời

Ghi `D:\VSF\dbcheck\judge\report.md` (tiếng Việt, ngắn, theo A–D) và `D:\VSF\dbcheck\judge\summary.json` dạng `{"tables": {"checked": n, "correct": n}, "columns": {"checked": n, "correct": n, "wrong": [..]}, "missing": [..], "extra": [..], "standard": {"<mục>": "đạt|không đạt: lý do"}, "readability_score": n}`. Kiểm hash trước khi chấm. Không chắc thì nói không chắc; không đoán; không sửa đầu ra.
