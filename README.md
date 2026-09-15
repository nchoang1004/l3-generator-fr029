# l3gen

Đọc source code Python/FastAPI và sinh ra tài liệu kiến trúc L3 — danh sách API route,
bảng dữ liệu, lời gọi ra ngoài — trong đó **mọi dòng đều bấm được về đúng `file:dòng`
trong source thật**.

Công cụ **không chạy code** của repo được phân tích. Chỉ đọc file rồi phân tích cây cú
pháp.

---

## 1. Chạy thử trong 3 lệnh

```bash
pip install -e .
l3gen tests/fixtures/python/fastapi/sample_app --no-ai -o out
cat out/L3.md
```

Muốn xem bằng giao diện web thay vì đọc Markdown thô:

```bash
l3gen ui out
```

Kết quả nằm trong thư mục `out/`:

| File | Nội dung |
|---|---|
| `L3.md` | Tài liệu chính, đọc bằng mắt |
| `diagram.mmd` | Sơ đồ phụ thuộc (Mermaid) |
| `graph.json` | Node và cạnh, để máy đọc |
| `IAM.json` | Toàn bộ dữ liệu đọc được từ code |
| `findings.json` | Cảnh báo từ bước rà soát |
| `ui/` | File giao diện web, chỉ xuất hiện sau khi chạy `l3gen ui` |

Không muốn cài gì? Xem [`examples/`](examples/) — có sẵn kết quả đã chạy trên hai repo
mã nguồn mở thật.

---

## 2. Output thật trông thế nào

Trích từ [`examples/full-stack-fastapi-template/L3.md`](examples/full-stack-fastapi-template/L3.md):

```markdown
## 2. API Routes

| Method | Đường dẫn | Hàm xử lý | Bằng chứng / đầy đủ | Lý do | Vị trí |
|---|---|---|---|---|---|
| GET | `/{settings.API_V1_STR}/items/` | `read_items` | `exact / partial` | đường dẫn có phần phụ thuộc lúc chạy: {settings.API_V1_STR} | app/api/routes/items.py:14 |
| PATCH | `/{settings.API_V1_STR}/users/me/password` | `update_password_me` | `exact / partial` | đường dẫn có phần phụ thuộc lúc chạy: {settings.API_V1_STR} | app/api/routes/users.py:104 |
```

Chú ý cột **Đường dẫn**: công cụ ghi `{settings.API_V1_STR}` chứ **không đoán** ra giá
trị thật `/api/v1`. Giá trị đó chỉ biết khi chạy chương trình. Hai nhãn
`exact / partial` nói: route này chắc chắn có thật, nhưng đường dẫn còn một phần chưa
biết — và cột *Lý do* nói rõ phần nào.

Đây là nguyên tắc xuyên suốt: **không biết thì nói không biết, không đoán cho đẹp.**

---

## 3. Công cụ này KHÔNG làm gì

Đặt ở đây, không giấu xuống cuối.

**Không nhận diện được:**

- ORM khác SQLAlchemy và SQLModel — Tortoise, Django ORM, câu lệnh SQL viết tay.
- Hàng đợi tin nhắn — Celery, Kafka, RabbitMQ.
- Framework khác FastAPI — Flask, Django, Spring. Gặp thì báo rõ, không im lặng trả
  về rỗng.
- Ngôn ngữ khác Python. Gặp thì bỏ qua riêng đơn vị đó, vẫn phân tích phần còn lại.

**Không làm:**

- Không chạy code của repo được phân tích. Chỉ đọc file và phân tích cú pháp.
- Không phân tích hành vi lúc chạy. Giá trị biến môi trường, route đăng ký động trong
  vòng lặp — nằm ngoài tầm với.
- Không đọc sâu vào hàm bên trong `Depends(...)`.
- Không nối tham chiếu tới thư viện ngoài repo. Chỉ ghi nhận "gọi ra ngoài phạm vi".
- Không quét lại theo kiểu tăng dần. Mỗi lần chạy đọc lại toàn bộ.
- Không tích hợp CI. Chạy tay qua dòng lệnh.

**AI trong công cụ này bị giới hạn cứng:** AI chỉ viết thêm cột mô tả cho dễ đọc và
viết lại câu tóm tắt cảnh báo. **AI không được thêm, sửa, hay xoá bất kỳ dữ liệu nào**
trong `IAM.json`. Kiểm chứng được: chạy hai lần có AI và không AI, `diff IAM.json` ra
rỗng.

---

## 4. Kết quả kiểm chứng

Đo trên hai repo mã nguồn mở không do đội viết: `Netflix/dispatch` (48 file) và
`fastapi/full-stack-fastapi-template` (25 file). Trước khi chạy công cụ, chúng tôi đọc
tay toàn bộ source để lập sẵn danh sách đối chiếu gồm 84 API route, 11 bảng dữ liệu và
14 lời gọi HTTP ra ngoài.

Công cụ tìm đúng cả 84 route, cả 11 bảng dữ liệu, cả 14 lời gọi ra ngoài. **Không có
trường hợp nào công cụ báo ra một thứ không tồn tại** — kể cả với bốn cái bẫy cài sẵn,
ví dụ một biến local trùng tên với thư viện `requests`.

Lần đo đầu tìm ra ba lỗi thật, nặng nhất là: mọi đường dẫn của `dispatch` đều thiếu
tiền tố `/api/v1` mà công cụ lại đánh dấu là "đã đầy đủ". Cả ba đã sửa và đo lại —
61/61 đường dẫn giờ đúng, và **số lần đoán sai tên bảng đi từ 7 xuống 0**.

Một điều phải nói rõ: danh sách đối chiếu do **Agent lập, không phải hai kỹ sư đọc độc
lập** như đặc tả yêu cầu. Con số 100% vì thế yếu hơn vẻ ngoài của nó.

→ Bảng số đầy đủ, phân tích từng lỗi, và giải thích vì sao 100% chưa đủ để tin:
**[EVALUATION.md](EVALUATION.md)**

---

## 5. Cấu hình

### Tùy chọn dòng lệnh

```bash
l3gen <đường-dẫn-source> [tùy chọn]
```

| Tùy chọn | Mặc định | Ý nghĩa |
|---|---|---|
| `-o, --output <dir>` | `./l3-output/` | Nơi ghi kết quả |
| `--no-ai` | tắt | Chạy thuần phân tích cú pháp, không gọi AI. Tài liệu vẫn đủ, chỉ thiếu cột mô tả |
| `--exclude <tên>` | `__pycache__`, `.venv`, `venv`, `tests` | Thư mục bỏ qua, lặp lại được nhiều lần |
| `--fail-on-empty` | tắt | Thoát với mã lỗi nếu không tìm thấy route hay bảng nào |
| `-v, --verbose` | tắt | In chi tiết từng bước |
| `--version` | | In phiên bản |

Mã thoát:

| Mã | Khi nào |
|---|---|
| `0` | Thành công |
| `1` | Thư mục không tồn tại; không có file `.py` nào; mọi đơn vị đều dùng stack chưa hỗ trợ; hoặc `--fail-on-empty` bật mà không tìm thấy route/bảng nào |
| `2` | Lỗi không lường trước |

### Xem kết quả bằng giao diện web

```bash
l3gen ui <thư-mục-kết-quả> [-p CỔNG] [--no-browser]
```

Mở một máy chủ tĩnh ở `127.0.0.1` rồi bật trình duyệt. Sáu màn: Tổng quan, API
Routes, Bảng dữ liệu, Đồ thị, Cảnh báo, Giới hạn đã biết.

Vì sao cần máy chủ mà không mở thẳng file HTML: trình duyệt chặn `fetch` trên
`file://`, nên trang sẽ không đọc được `IAM.json`.

Giao diện **chỉ đọc** các file JSON đã sinh, không phân tích lại source. Xoá cả
thư mục `src/l3gen/ui/` thì lệnh phân tích vẫn chạy y nguyên — có test khoá điều
này (`tests/unit/test_ui_boundary.py`). Không tải gì từ mạng, mở được khi ngắt
mạng.

### Biến môi trường

Chỉ cần khi muốn có mô tả do AI viết:

| Biến | Ghi chú |
|---|---|
| `L3GEN_API_KEY` | Ưu tiên trước |
| `ANTHROPIC_API_KEY` | Dùng khi không có biến trên |

**Không có key cũng chạy được.** Công cụ tự chuyển sang chế độ không AI và báo một
dòng, không dừng lại. Muốn chắc chắn không gọi mạng thì thêm `--no-ai`.

Cài phần AI:

```bash
pip install -e ".[ai]"
```

### Yêu cầu

Python 3.10 trở lên. Phụ thuộc bắt buộc chỉ có `pydantic`.

---

## 6. Hạn chế đã biết

### Không đọc được, và nói thẳng là không đọc được

Đây không phải lỗi mà là ranh giới của phân tích cú pháp. Công cụ ghi rõ ở cột *Lý do*
và ở mục "Giới hạn đã biết" của mỗi `L3.md`:

| Tình huống | Công cụ ghi gì |
|---|---|
| Prefix route là biến config | giữ nguyên `/{settings.API_V1_STR}/users/me`, **không** đoán thành `/api/v1/...` |
| Lớp cơ sở tự sinh tên bảng lúc chạy | cột *Bảng* ghi *chưa đọc được*, kèm lý do |
| Route đăng ký trong khối `if` | nêu rõ điều kiện, cảnh báo route không có ở mọi môi trường |

### Lỗi còn lại chưa sửa

**Lớp cơ sở khai báo bị đếm như một bảng.** Trên `Netflix/dispatch`, lớp `Base` ở
`database/core.py:95` nằm trong danh sách bảng dù nó không phải bảng. Dấu hiệu nhận ra:
nó có 0 cột. Ảnh hưởng 1 trên 113 thực thể của repo đó.

### Chưa đo

**Repo đăng ký route động** — trong vòng lặp, qua `add_api_route`, hay qua decorator
bọc ngoài. Hai repo mẫu không có kiểu này nên chưa có số liệu.

Ngoài ra, khoảng 37% lời gọi hàm chưa nối được về đích. Phần lớn do code không khai báo
kiểu biến:

```python
def get(*, db_session, case_id: int):   # db_session không khai kiểu
    return db_session.query(Case)...
```

Không có cách nào biết `db_session` là gì mà không đoán. Chúng tôi **không** thêm luật
kiểu "tham số tên `db_session` thì chắc là Session" — đó là đoán. 63% là con số trung
thực.

### Hướng phát triển

1. Sửa lỗi lớp cơ sở bị đếm như bảng.
2. Đo trên repo có đăng ký route động, để biết giới hạn thật ở đâu.
3. Thêm Flask và Django. Cùng ngôn ngữ nên chủ yếu là viết luật nhận diện, ước tính
   2–3 ngày mỗi framework.
4. Thêm ngôn ngữ mới thì tốn hơn nhiều. `ast` chỉ đọc được Python; Java cần bộ phân
   tích cú pháp khác, ước tính 1–1,5 tuần.

---

## 7. Tài liệu trong repo

| File | Nội dung |
|---|---|
| [EVALUATION.md](EVALUATION.md) | Kết quả đo độ chính xác, phân tích từng lỗi |
| [SPEC_Code_to_L3_Generator.md](SPEC_Code_to_L3_Generator.md) | Đặc tả gốc |
| [examples/](examples/) | Kết quả đã chạy sẵn trên hai repo thật |
| [docs/USE_CASES.md](docs/USE_CASES.md), [docs/SCENARIOS.md](docs/SCENARIOS.md) | Requirement |
| [docs/AGENTIC_SDLC_LOG.md](docs/AGENTIC_SDLC_LOG.md) | Nhật ký: đặc tả thiếu gì, chỗ nào cố ý làm khác |

### Chạy test

```bash
pip install -e ".[dev]"
python -m pytest -q
```

### Tự kiểm chứng: chạy hai lần ra kết quả giống hệt

```bash
l3gen <repo> --no-ai -o r1
l3gen <repo> --no-ai -o r2
diff r1/IAM.json r2/IAM.json && diff r1/graph.json r2/graph.json && echo "giống hệt"
# IAM.json, graph.json, diagram.mmd, findings.json giống hệt từng byte.
# Riêng L3.md khác hai chỗ cố ý: dòng thời điểm chạy ở đầu file, và con số
# thời lượng chạy ở mục 1.
```
