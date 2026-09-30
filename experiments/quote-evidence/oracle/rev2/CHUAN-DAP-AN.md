# Chuẩn đáp án (bản 2, 28/09/2026)

File này nói đáp án (ground truth) của một repo phải viết thế nào. Mọi file `oracle/*.json` theo chuẩn này. Khiêm đã duyệt.

**Sơ đồ chỉ vẽ luồng xử lý** (Khiêm chốt 28/09): đường đi của request, tác vụ nền, lệnh CLI. Cạnh lắp ráp (container DI, khởi động, tắt) có thật nhưng không vẽ; ghi ở `acceptable` với nhãn `"wiring"`.

**Khối không cần trùng thư mục.** Thư mục chứa file khác vai trò thì tách theo file; file ở nhiều thư mục cùng vai trò thì gộp. Ví dụ: thư mục gốc `lnbits/` tách thành khởi động, db, decorators; `core/registrar.py` + `app/router.py` là một khối.

## 1. Năm quy tắc

1. **Giữ mọi luồng có thật.** Luồng chính (điểm vào → dựng app → route → service → dữ liệu → DB và hệ thống ngoài) và luồng phụ (CLI, trang admin, worker, plugin, tool). Chỉ bỏ phần không thuộc luồng nào, ví dụ file không ai import, script sinh template. Bỏ nghĩa là không liệt kê trong `components`; khi chấm, file đó được bỏ qua.
2. **Gộp khối cùng tầng, cùng cơ chế.** Ví dụ: nhiều plugin nạp chung một vòng lặp là một khối; `application` + `domain` của một tính năng là một khối service; `crud` + `models` là một khối dữ liệu; các file khởi động (main, server, app factory) là một khối. Khối khác tầng của cùng tính năng thì tách (api / service / dữ liệu).
3. **Khối dùng chung ghi rõ trong `shared`.** Chỉ gồm cấu hình, log, lớp lỗi chung, hằng số, helper thuần. Không có route, bảng, kết nối ra ngoài, không gọi nghiệp vụ. Khối dùng chung không có cạnh.
4. **Mỗi cạnh bắt buộc có `file:dòng` và đoạn code.** Cạnh không qua import (nạp theo tên, chuỗi `"app.server:app"`) chỉ giữ khi thuộc luồng chính và không có đường import thay thế. Nếu quan hệ đó tầm thường thì gộp hai khối thay vì giữ cạnh.
5. **Cạnh "chấp nhận được" do code sinh** (`oracle_tool.py --finalize`): mọi cạnh import thật giữa hai khối không dùng chung mà không bắt buộc. Cạnh tới hệ thống ngoài phụ thì ghi tay, đánh dấu `"hand"`.

## 2. Cạnh nào là bắt buộc

| Bắt buộc (luồng xử lý) | Chấp nhận được (không bắt buộc) |
|---|---|
| Định tuyến: `include_router`, gắn router plugin, mount socket/admin, `add_middleware`, `add_exception_handler` | Lắp ráp, nhãn `"wiring"`: container DI (`Factory`, `Provide[...]`), tạo app trong `main.py`, khởi động và tắt (`create_tables()`, `client.init()`, `Cache.init()`, `init_otel()`, đóng kết nối, khởi chạy worker) |
| | Chỉ dùng model/schema làm kiểu, kế thừa `Base`/mixin |
| Gọi service/usecase, gọi DAO/repository/crud | Gọi helper tiện ích, cache cục bộ |
| Lấy session DB, client Redis để dùng (kể cả qua `Depends`) | Ghi metrics, log, tracing nội bộ |
| Kiểm quyền (dependency xác thực, decorator khóa API) | Import lại (re-export) qua file trung gian |
| Tác vụ nền, worker gọi service/dữ liệu | Kiểm "plugin đã cài chưa" và các kiểm điều kiện tương tự |
| Kết nối hệ thống ngoài: dòng tạo engine/client có URL, host, DSN | Cạnh ngoài phụ (ghi tay, `"hand"`) |

## 3. Định dạng JSON

```json
{
 "repo": "owner/name", "source": "commit <sha>", "local_dir": "sample-repos/<thư mục>",
 "set": "held-out | tuning", "rev": 2, "written": "<ngày> ...",
 "note": "Luồng chính, luồng phụ, phần bỏ và lý do, điểm không chắc",
 "components": {"<key>": ["đường/dẫn/thư_mục/", "đường/dẫn/file.py"]},
 "shared": ["<key>"],
 "externals": {"<key>": ["alias thường gặp trong tên hệ thống", "..."]},
 "required": [["<nguồn>", "<đích hoặc ext:key>", "<file>:<dòng> <đoạn code>"]],
 "acceptable": [["<nguồn>", "<đích>", "wiring", "<file>:<dòng> <đoạn code>"], ["<nguồn>", "<đích>", "hand"], ["<nguồn>", "<đích>"]]
}
```

Đường dẫn dài hơn thắng đường dẫn ngắn hơn khi một file khớp nhiều khối.

## 4. Quy trình

1. Đọc cấu trúc repo, điểm vào, file dựng app, file gộp router.
2. Viết `components` và `shared` theo quy tắc 1–3.
3. Chạy `python oracle/oracle_tool.py <repo> <oracle.json>`: xem file nào ngoài khối (cố ý hay quên), và danh sách cạnh import kèm dòng code.
4. Chọn cạnh bắt buộc theo mục 2 (chỉ luồng xử lý); đọc lại đúng dòng code; ghi `file:dòng`. Cạnh lắp ráp ghi vào `acceptable` với nhãn `"wiring"` kèm `file:dòng`.
5. Thêm cạnh ngoài: tìm dòng tạo kết nối (`create_async_engine`, `Redis(`, `httpx.AsyncClient(base_url=...)`, `SMTP(`, broker URL...).
6. Chạy lại với `--finalize` để sinh cạnh "chấp nhận được". Dòng `required without import` phải trống, hoặc có lý do ghi trong `note`.
