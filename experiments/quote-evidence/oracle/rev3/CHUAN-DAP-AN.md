# Chuẩn đáp án (bản 3, 28/09/2026)

File này nói đáp án (ground truth) của một repo phải viết thế nào. Mọi file `oracle/*.json` theo chuẩn này. Khiêm đã duyệt. Bản 2 ở `oracle/rev2/`; bản 3 thêm tầng (quy tắc 6, mục 3), sơ đồ một chiều (quy tắc 7) và các nhãn `"pass"`, `"check"`, `"up"` (mục 2).

**Sơ đồ chỉ vẽ luồng xử lý** (Khiêm chốt 28/09): đường đi của request, tác vụ nền, lệnh CLI. Cạnh lắp ráp (container DI, khởi động, tắt) có thật nhưng không vẽ; ghi ở `acceptable` với nhãn `"wiring"`.

**Khối không cần trùng thư mục.** Thư mục chứa file khác vai trò thì tách theo file; file ở nhiều thư mục cùng vai trò thì gộp. Ví dụ: thư mục gốc `lnbits/` tách thành khởi động, db, decorators; `core/registrar.py` + `app/router.py` là một khối.

## 1. Bảy quy tắc

1. **Giữ mọi luồng có thật.** Luồng chính (điểm vào → dựng app → route → service → dữ liệu → DB và hệ thống ngoài) và luồng phụ (CLI, trang admin, worker, plugin, tool). Chỉ bỏ phần không thuộc luồng nào, ví dụ file không ai import, script sinh template. Bỏ nghĩa là không liệt kê trong `components`; khi chấm, file đó được bỏ qua.
2. **Gộp khối cùng tầng, cùng cơ chế.** Ví dụ: nhiều plugin nạp chung một vòng lặp là một khối; `application` + `domain` của một tính năng là một khối service; `crud` + `models` là một khối dữ liệu; các file khởi động (main, server, app factory) là một khối. Khối khác tầng của cùng tính năng thì tách (api / service / dữ liệu).
3. **Khối dùng chung ghi rõ trong `shared`.** Chỉ gồm cấu hình, log, lớp lỗi chung, hằng số, helper thuần. Không có route, bảng, kết nối ra ngoài, không gọi nghiệp vụ. Khối dùng chung không có cạnh.
4. **Mỗi cạnh bắt buộc có `file:dòng` và đoạn code.** Cạnh không qua import (nạp theo tên, chuỗi `"app.server:app"`) chỉ giữ khi thuộc luồng chính và không có đường import thay thế. Nếu quan hệ đó tầm thường thì gộp hai khối thay vì giữ cạnh.
5. **Cạnh "chấp nhận được" do code sinh** (`oracle_tool.py --finalize`): mọi cạnh import thật giữa hai khối không dùng chung mà không bắt buộc. Cạnh tới hệ thống ngoài phụ thì ghi tay, đánh dấu `"hand"`.
6. **Mỗi khối không dùng chung thuộc đúng một tầng, kèm một dòng code làm bằng chứng.** Ghi trong `layers` (mục 3). Sơ đồ vẽ mỗi tầng thành một khung, xếp từ trên xuống.
7. **Sơ đồ chỉ đi một chiều.** Cạnh bắt buộc đi từ tầng trên xuống tầng dưới, hoặc trong cùng tầng. Cạnh đi ngược lên tầng trên chuyển sang `acceptable`, nhãn `"up"`, giữ `file:dòng`. Sơ đồ để người mới hình dung luồng, không cần mọi lần gọi qua lại.

## 2. Cạnh nào là bắt buộc

| Bắt buộc (luồng xử lý) | Chấp nhận được (không bắt buộc) |
|---|---|
| Định tuyến: `include_router`, gắn router plugin, mount socket/admin, `add_middleware`, `add_exception_handler` | Lắp ráp, nhãn `"wiring"`: container DI (`Factory`, `Provide[...]`), tạo app trong `main.py`, khởi động và tắt (`create_tables()`, `client.init()`, `Cache.init()`, `init_otel()`, đóng kết nối, khởi chạy worker) |
| | Chỉ dùng model/schema làm kiểu, kế thừa `Base`/mixin |
| Gọi service/usecase, gọi DAO/repository/crud | Gọi helper tiện ích, cache cục bộ |
| Dùng DB, Redis thật: gọi method trên session hoặc client (`execute`, `commit`, `get`, `set`...), kể cả khi lấy qua `Depends` | Chỉ nhận hoặc tự mở rồi truyền đi: khối nhận session/client (qua `Depends`, tham số) hoặc tự mở (`async with async_db_session() as db`), không gọi method nào trên nó, chỉ đưa nó làm tham số cho khối khác. Nhãn `"pass"` kèm `file:dòng` |
| | Ghi metrics, log, tracing nội bộ |
| | Kiểm tra rồi quay về: kiểm token, quyền, session, captcha và các dạng tương tự (dependency xác thực, decorator khóa API, `jwt_authentication(token)`). Luồng không đi tiếp qua khối được gọi. Nhãn `"check"` kèm `file:dòng` |
| | Cạnh đi ngược lên tầng trên (quy tắc 7). Nhãn `"up"` kèm `file:dòng` |
| | Import lại (re-export) qua file trung gian |
| Tác vụ nền, worker gọi service/dữ liệu | Kiểm "plugin đã cài chưa" và các kiểm điều kiện tương tự |
| Kết nối hệ thống ngoài: dòng tạo engine/client có URL, host, DSN | Cạnh ngoài phụ (ghi tay, `"hand"`) |

## 3. Xếp khối vào tầng

Mỗi khối không dùng chung thuộc một trong năm tầng. Bằng chứng là một dòng code trong khối có dấu hiệu của tầng đó.

| Tầng | Key | Dấu hiệu (dòng làm bằng chứng) |
|---|---|---|
| Điểm vào | `entry` | Tạo app hoặc chạy chương trình: `FastAPI(`, `uvicorn.run(`, `if __name__ == "__main__"`. Lệnh CLI (`@click.command`). Định nghĩa middleware |
| API | `api` | Nhận request: `@router.get/post...`, `APIRouter(`, gộp router (`include_router`), trang admin, handler socket (`@sio.event`) |
| Nghiệp vụ | `service` | Không có dấu hiệu của tầng nào khác. Bằng chứng là dòng một khối tầng trên gọi nó (lấy từ cạnh bắt buộc). Worker tác vụ nền (Celery, taskiq) cũng ở tầng này, vì service gửi việc cho nó, kể cả khi khối có dòng tạo kết nối tới broker |
| Dữ liệu | `data` | Đọc ghi một bảng cụ thể: định nghĩa model ORM (`class User(Base)`), hàm CRUD chạy truy vấn (`select(User)`) |
| Hạ tầng | `infra` | Tạo kết nối ra ngoài: `create_async_engine(`, `Redis(`, `httpx.AsyncClient(base_url=`, SMTP, exporter tracing. Lớp bọc kết nối chung (ví dụ `fetchall` không gắn với bảng nào) cũng thuộc tầng này |

- Khối có dấu hiệu của nhiều tầng thì lấy tầng đứng trên trong bảng. Ví dụ: plugin có cả route và model → `api`.
- Khối dùng chung không xếp tầng.
- Chỗ phải chọn giữa hai tầng thì ghi lý do trong `note`.
- Xếp tầng xong mới xét quy tắc 7: cạnh bắt buộc nào đi lên thì chuyển sang `"up"`. `oracle_tool.py` báo các cạnh này (dòng `upward`).

## 4. Định dạng JSON

```json
{
 "repo": "owner/name", "source": "commit <sha>", "local_dir": "sample-repos/<thư mục>",
 "set": "held-out | tuning", "rev": 3, "written": "<ngày> ...",
 "note": "Luồng chính, luồng phụ, phần bỏ và lý do, điểm không chắc",
 "components": {"<key>": ["đường/dẫn/thư_mục/", "đường/dẫn/file.py"]},
 "shared": ["<key>"],
 "layers": {"<key>": ["entry | api | service | data | infra", "<file>:<dòng> <đoạn code>"]},
 "externals": {"<key>": ["alias thường gặp trong tên hệ thống", "..."]},
 "required": [["<nguồn>", "<đích hoặc ext:key>", "<file>:<dòng> <đoạn code>"]],
 "acceptable": [["<nguồn>", "<đích>", "wiring | pass | check | up", "<file>:<dòng> <đoạn code>"],
                ["<nguồn>", "<đích>", "hand"], ["<nguồn>", "<đích>"]]
}
```

Đường dẫn dài hơn thắng đường dẫn ngắn hơn khi một file khớp nhiều khối.

## 5. Quy trình

1. Đọc cấu trúc repo, điểm vào, file dựng app, file gộp router.
2. Viết `components` và `shared` theo quy tắc 1–3.
3. Chạy `python oracle/oracle_tool.py <repo> <oracle.json>`: xem file nào ngoài khối (cố ý hay quên), và danh sách cạnh import kèm dòng code.
4. Chọn cạnh bắt buộc theo mục 2 (chỉ luồng xử lý); đọc lại đúng dòng code; ghi `file:dòng`. Cạnh lắp ráp ghi vào `acceptable` với nhãn `"wiring"`, cạnh chỉ truyền session/client với nhãn `"pass"`, cạnh kiểm tra rồi quay về với nhãn `"check"`, đều kèm `file:dòng`.
5. Thêm cạnh ngoài: tìm dòng tạo kết nối (`create_async_engine`, `Redis(`, `httpx.AsyncClient(base_url=...)`, `SMTP(`, broker URL...).
6. Xếp tầng theo mục 3, mỗi khối một dòng bằng chứng. Cạnh bắt buộc đi lên chuyển sang `"up"` (quy tắc 7).
7. Chạy lại với `--finalize` để sinh cạnh "chấp nhận được". Dòng `required without import`, `no layer` và `upward` phải trống, hoặc có lý do ghi trong `note`.
