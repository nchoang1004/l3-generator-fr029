**prefix_chain**

- **ĐÁNG NGỜ** — [gold:309](D:/VSF/l3-generator-l3/slice/tests/fixtures/fr029/prefix_chain.gold.json:309), `limitations: []`: chưa ghi route admin bị bỏ khỏi khối OpenAPI. Cần kỳ vọng rõ việc bỏ route này, lý do prefix không xác định (`app/main.py:22`). `path: null` đúng, nhưng chưa đủ kiểm yêu cầu “route không biểu diễn được thì ghi rõ bị bỏ khỏi khối và lý do” của FR-029.

**params_models**

- **ĐÁNG NGỜ** — `request_body.embedded` của `/uploads` và `/login` ([gold:260](D:/VSF/l3-generator-l3/slice/tests/fixtures/fr029/params_models.gold.json:260), dòng 291): `false` → **`true` nếu dùng nghĩa embedding của FastAPI**. Hai handler đều có nhiều trường body (`app/routes.py:53,58`); oracle cũng ghi object chứa các trường theo tên. [FastAPI 0.115.6](https://github.com/fastapi/fastapi/blob/0.115.6/fastapi/dependencies/utils.py#L771-L790) xác định các trường hợp này là embedded. Chưa đồng ý README phán đoán **#8**; nếu cờ chỉ dành cho JSON thì phải định nghĩa rõ.

**pydantic_v1**

Không có mục SAI/ĐÁNG NGỜ.

**exclusions**

- **SAI** — [gold:41](D:/VSF/l3-generator-l3/slice/tests/fixtures/fr029/exclusions.gold.json:41), loại `app/routers/internal.py:6` với `reason: "test"` → **giữ khai báo route trong phạm vi đọc; chỉ bỏ registration trong `conftest.py:10`**. File khai báo là production, không thuộc danh sách loại của FR-028. AC-029-05 không có quy tắc “chỉ gắn trong test thì loại cả khai báo production”. Phần đường dẫn chưa xác định phải xử lý theo “Khi chưa đủ dữ kiện”. Không đồng ý README **#12**, phần nói về `internal.py`.
- **SAI** — [gold:56](D:/VSF/l3-generator-l3/slice/tests/fixtures/fr029/exclusions.gold.json:56), `limitations` chỉ có ba lời gọi đăng ký route → **thiếu thống kê file ngoài phạm vi: 3 file kiểm thử và 1 file example**. Các file là `tests/test_api.py`, `app/routers/test_selfcheck.py`, `conftest.py`, `examples/standalone.py`; bảng “Phạm vi đọc” FR-028 yêu cầu “Đếm ở phần giới hạn”.

**http_calls**

Không có mục SAI/ĐÁNG NGỜ.

**file_roles**

- **SAI** — [gold:205](D:/VSF/l3-generator-l3/slice/tests/fixtures/fr029/file_roles.gold.json:205), `app/service_utils.py`, `line: null` → **cần dòng code, chẳng hạn dòng 1**, giữ `role: "Khác"`, `label: "exact"`. AC-029-07 yêu cầu mỗi file có vai trò **và dòng code làm bằng chứng**, không miễn cho vai trò Khác trong component nghiệp vụ. Không đồng ý phần `line: null` của README **#19**.

Đã kiểm: **42 nhóm mục (6 fixture × 7)**; **3 mục sai**, **2 mục đáng ngờ**.