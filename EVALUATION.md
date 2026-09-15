# Đo độ chính xác

Đo ngày 15/09/2026. Công cụ `l3gen` 0.1.0.

Đo hai lần: lần đầu tìm ra ba lỗi, sau đó sửa cả ba rồi đo lại. Tài liệu này ghi
cả hai lần — số trước khi sửa nằm ở mục 5.

---

## 1. Tóm tắt cho người không đọc bảng số

Chúng tôi kiểm chứng trên hai repo mã nguồn mở không do đội viết: `Netflix/dispatch`
(đo trên 48 file) và `fastapi/full-stack-fastapi-template` (25 file). Trước khi chạy
công cụ, chúng tôi đọc tay toàn bộ source để lập sẵn danh sách đối chiếu gồm 84 API
route, 11 bảng dữ liệu và 14 lời gọi HTTP ra ngoài.

Công cụ tìm đúng cả 84 route, cả 11 bảng dữ liệu, và cả 14 lời gọi ra ngoài. **Không
có trường hợp nào công cụ báo ra một thứ không tồn tại.** Chúng tôi cài sẵn bốn cái
bẫy dễ báo nhầm — ví dụ một biến local trùng tên với thư viện `requests` — và công cụ
tránh được cả bốn.

Lần đo đầu tìm ra ba lỗi. Nặng nhất: mọi đường dẫn của `dispatch` đều thiếu tiền tố
`/api/v1` mà công cụ lại đánh dấu là "đã đầy đủ". Cả ba lỗi đã sửa và đo lại: 61/61
đường dẫn giờ đúng; với 9 bảng mà tên bảng chỉ biết lúc chạy, công cụ ghi thẳng "chưa
đọc được" thay vì đoán — **số lần đoán sai đi từ 7 xuống 0**.

Một điều phải nói rõ ngay: danh sách đối chiếu do **Agent lập, không phải hai kỹ sư
đọc độc lập** như đặc tả yêu cầu. Nghĩa là con số 100% ở trên yếu hơn vẻ ngoài của nó.
Lý do đầy đủ ở mục 2.

---

## 2. Danh sách đối chiếu được lập thế nào — và điểm yếu của nó

SPEC mục 8.5.1 yêu cầu **hai người đọc tay độc lập**, rồi đối chiếu hai danh sách.
Chỗ hai người đọc khác nhau chính là dữ liệu quý nhất, vì nó cho biết đâu là phần mà
ngay cả con người cũng thấy mơ hồ.

**Việc đó đã không được làm.** Danh sách đối chiếu do Agent (Claude Opus 5) đọc source
lập ra, một lượt, một "người".

### Điểm yếu cụ thể

| Rủi ro | Mức độ | Đã giảm bớt bằng cách nào |
|---|---|---|
| Agent và công cụ cùng đọc cây cú pháp Python nên có thể **cùng mù một kiểu code** | Cao | Quét thêm bằng tìm kiếm văn bản thuần cho `add_api_route`, đăng ký route trong vòng lặp, trong `if`, và decorator bọc ngoài. Không có ca nào trong phạm vi. |
| Chỉ một lượt đọc, không ai soát lại | Cao | Đối chiếu chéo tên bảng bằng chuỗi `ForeignKey("<tên>.id")` có thật trong source: 8/9 tên xác nhận được bằng bằng chứng độc lập. |
| Agent tự đặt đề rồi tự chấm | Trung bình | Cài sẵn 4 bẫy báo nhầm trước khi chạy, và ghi trước 1 ca ranh giới để xem công cụ xử lý ra sao. |

### Sai sót đã xảy ra trong chính danh sách đối chiếu

Ghi lại để thấy quy trình có phát hiện lỗi thật:

> Bản đầu tôi ghi lời gọi ở `plugins/dispatch_microsoft_teams/conference/client.py:66`
> là nằm trong `try/except`. Công cụ báo ngược lại. Đọc lại thì khối bao ngoài là
> `if "access_token" in result:`, không phải `try`. **Công cụ đúng, danh sách đối chiếu
> sai.** Đã sửa. Nếu chỉ tin danh sách đối chiếu thì đã ghi oan cho công cụ một lỗi.

**Kết luận về độ tin cậy:** dùng được để tìm lỗi thật (đã tìm ra ba, đều sửa được),
chưa đủ mạnh để tuyên bố "công cụ đúng 100%". Khi có người thứ hai đọc lại, cập nhật
lại mục này.

---

## 3. Repo đã dùng

| | Repo A | Repo B |
|---|---|---|
| Tên | `Netflix/dispatch` | `fastapi/full-stack-fastapi-template` |
| Commit | `dd2837e82a0bf5565b1b4b4b91ea30b7262d4061` | `cb740b656d7a0a6c5e12c7bf8e50343ec94ee9c7` |
| Phạm vi đo route và bảng | `src/dispatch/case/` + `src/dispatch/incident/` — 48 file | `app/` — 25 file |
| Phạm vi đo lời gọi ra ngoài | toàn bộ `src/dispatch/` — 717 file | `app/` |
| Vì sao chọn | Đúng cỡ 30–80 file SPEC yêu cầu. Router lồng 3 tầng, 9 lớp SQLAlchemy, `app.mount()`. | Có ba ca khó mà repo A không có: prefix là biến, route trong khối `if`, một file lỗi cú pháp thật. |

**Vì sao đo lời gọi ra ngoài trên phạm vi rộng hơn:** `case/` và `incident/` không có
lời gọi HTTP nào. Toàn bộ 14 lời gọi của `dispatch` nằm trong `plugins/`. Đo trên phạm
vi 48 file thì chỉ số này sẽ là 0/0, không nói lên điều gì.

Tái lập:

```bash
python -m l3gen.cli sample-repos/dispatch --no-ai -o evaluation/run_dispatch
python evaluation/compare.py evaluation/ground_truth.json \
    evaluation/run_dispatch/IAM.json evaluation/result.json
```

---

## 4. Bảng chỉ số (sau khi sửa ba lỗi)

### 4.1 Đối chiếu ngưỡng (đặt trước khi chạy, SPEC mục 8.5.3)

| Nhóm | Ngưỡng | Repo A | Repo B |
|---|---|---|---|
| Route — recall | ≥ 85% | 100,0% (61/61) | 100,0% (23/23) |
| Route — precision nhóm `exact` | ≥ 95% | 100,0% (61/61) | 100,0% (23/23) |
| Bảng dữ liệu — recall | ≥ 90% | 100,0% (9/9) | 100,0% (2/2) |
| Lời gọi ra ngoài — recall | ≥ 80% | 100,0% (14/14) | không đo được (repo không có lời gọi nào) |

Bốn ngưỡng đều đạt. Ngưỡng không bị sửa sau khi thấy kết quả — bản đặt ngưỡng nằm ở
SPEC mục 8.5.3, viết từ trước khi có dòng code nào.

### 4.2 Route

| | Repo A | Repo B |
|---|---|---|
| Có thật | 61 | 23 |
| Công cụ báo | 61 | 23 |
| Đúng | 61 | 23 |
| Bỏ sót | 0 | 0 |
| Báo thừa | 0 | 0 |
| Vị trí `file:dòng` trỏ sai | 0 | 0 |

**Phân bố nhãn:**

| | `exact` | `inferred` | `full` | `partial` |
|---|---|---|---|---|
| Repo A | 61 | 0 | 61 | 0 |
| Repo B | 23 | 0 | 0 | 23 |

Nhóm `inferred` rỗng ở cả hai repo. **Không thể kết luận "nhãn `exact` chính xác hơn
`inferred`"** như SPEC mục 8.5.2 muốn kiểm — không có mẫu để so.

Hai nhãn `full`/`partial` giờ đều kiểm chứng được:

- **Repo A — 61 route `full`.** Cả 61 đường dẫn đều bắt đầu bằng `/api/v1`, khớp URL
  thật. Trước khi sửa lỗi 1, chúng vẫn mang nhãn `full` nhưng thiếu tiền tố này.
- **Repo B — 23 route `partial`.** Cả 23 đều ghi `reason` là
  `"đường dẫn có phần phụ thuộc lúc chạy: {settings.API_V1_STR}"`, và giữ nguyên biểu
  thức `/{settings.API_V1_STR}/users/me` chứ không đoán thành `/api/v1/users/me`.
  **0 trên 23 route đoán ra giá trị thật** — đúng nguyên tắc bất biến số 3.

### 4.3 Bảng dữ liệu

| | Repo A | Repo B |
|---|---|---|
| Có thật | 9 | 2 |
| Công cụ tìm thấy | 9 | 2 |
| Bỏ sót / báo thừa | 0 / 0 | 0 / 0 |
| Tên bảng **đọc đúng** | 0 | 2 |
| Tên bảng **đọc sai** | **0** | **0** |
| Tên bảng ghi "chưa đọc được" | 9 | 0 |

Ba cột cuối phải đọc cùng nhau. Repo A không lớp nào khai `__tablename__`; tên bảng do
lớp cơ sở sinh lúc chạy. Công cụ nói thẳng là không đọc được, thay vì đoán. Xem lỗi 2.

Repo B dùng SQLModel, thư viện này có quy tắc mặc định tường minh (tên class viết
thường) nên đọc được cả hai, đánh dấu `inferred` kèm lý do.

Số cột đọc được ở repo A (để thấy công cụ không chỉ đếm class):

| Lớp | Cột | Khoá chính | Khoá ngoại |
|---|---|---|---|
| `Case` | 30 | 1 | 10 |
| `Incident` | 30 | 1 | 12 |
| `IncidentType` | 23 | 1 | 8 |
| `CaseType` | 16 | 1 | 4 |
| `CaseNotes` | 4 | 1 | 2 |

### 4.4 Lời gọi ra ngoài (repo A, toàn bộ 717 file)

| | Số |
|---|---|
| Có thật | 14 |
| Công cụ báo | 15 |
| Đúng | 14 |
| Bỏ sót | 0 |
| Báo ra thứ không phải lời gọi HTTP | **0** |
| Báo đúng nhưng nằm ngoài dạng SPEC liệt kê | 1 |
| Cờ `try/except` đúng | 14/14 |
| HTTP method đúng | 14/14 |

Recall 100%. Precision tính hai cách, vì trộn chung sẽ hiểu sai:

- **93,3%** nếu coi ca thứ 15 là sai (15 cái báo, 14 nằm trong danh sách đối chiếu).
- **100%** nếu hỏi "trong 15 cái công cụ báo, bao nhiêu cái là lời gọi HTTP thật".

Ca thứ 15 là `cli.py:1071`. Đó là `session.post(...)`, với `session` tạo từ
`requests.Session()` ở dòng 1055. Đây là lời gọi HTTP thật. SPEC mục 6c.3 liệt kê
`httpx.Client()` nhưng không nói tới `requests.Session()`, nên khi lập danh sách đối
chiếu tôi xếp nó ra ngoài phạm vi. **Công cụ làm tốt hơn phạm vi đặc tả**, và trừ điểm
nó vì chuyện đó là sai. Con số 93,3% giữ lại để minh bạch, không phải để dùng.

**Bốn bẫy báo nhầm cài trước — công cụ tránh được cả bốn:**

| Chỗ | Vì sao dễ báo nhầm | Kết quả |
|---|---|---|
| `dispatch_google/docs/plugin.py:113` | biến local tên `requests` kiểu list, `requests.append()` | tránh được |
| `dispatch_google/docs/plugin.py:148` | cùng biến local đó | tránh được |
| `cli.py:1087` | `requests.exceptions.RequestException` — lớp exception | tránh được |
| `cli.py:1067` | `session: requests.Session` — chú thích kiểu | tránh được |

Cái bẫy thứ nhất đáng nói nhất: `grep "requests\."` sẽ báo nhầm, công cụ thì không, vì
nó biết `requests` ở file đó là biến local chứ không phải thư viện.

### 4.5 Xử lý file lỗi (repo B)

`app/api/deps.py:36` có lỗi cú pháp thật: `except InvalidTokenError, ValidationError:`
— cú pháp Python 2, không chạy được trên Python 3.

Công cụ bỏ qua đúng một file đó, báo `"app/api/deps.py: lỗi cú pháp dòng 36: multiple
exception types must be parenthesized"`, và đọc tiếp 24 file còn lại. Tìm đủ 23/23
route dù file hỏng nằm ngay trong đường dẫn `app/api/`.

---

## 5. Ba lỗi tìm được — trước và sau khi sửa

### Lỗi 1 — không xử lý `app.mount()`, và đánh dấu sai là "đã đầy đủ"

**Nặng nhất.** Ảnh hưởng 61 trên 61 route của repo A.

`src/dispatch/main.py:268`:

```python
app.mount("/api/v1", app=api)
```

Công cụ chỉ lần theo `include_router`. `app.mount()` là hàm của Starlette, không phải
của FastAPI, và không được đọc.

Phần thiếu không phải vấn đề lớn nhất. **Vấn đề là công cụ đánh dấu 61 route này là
`completeness = "full"`**, nghĩa là "các thuộc tính cần xuất đã đọc được đầy đủ" (SPEC
mục 5.1). Đường dẫn chưa đầy đủ mà nhãn nói là đầy đủ. Người đọc tài liệu gõ thử sẽ
nhận 404 và không có gì báo cho họ biết vì sao.

| | Trước | Sau |
|---|---|---|
| Route có tiền tố `/api/v1` | 0 / 61 | **61 / 61** |
| Đường dẫn ví dụ | `/{organization}/cases/{case_id}` | `/api/v1/{organization}/cases/{case_id}` |
| Nhãn `full` có đúng không | không | có |

**Đã sửa thế nào:** `collect_mounts()` giờ đọc cả `mount()` lẫn `include_router()`, và
`_prefix_chains()` không còn dừng lại khi gặp một `FastAPI()` — vì một app vẫn có thể
được gắn vào app khác. Bỏ qua `mount("/", StaticFiles(...))` vì đó là thư mục tĩnh,
không có route nào.

Khoá bằng `fixture_14_starlette_mount` + 3 test, dựng đúng cấu trúc thật của `dispatch`
(app cha, app con, một `mount` thư mục tĩnh để bẫy).

### Lỗi 2 — suy tên bảng theo quy ước không có trong đặc tả, sai 7 trên 9 ca

`dispatch` không khai `__tablename__` ở đâu cả. Lớp `Base` ở `database/core.py:95`
sinh tên bảng lúc chạy:

```python
def resolve_table_name(name):
    names = re.split("(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])
```

Tức là tách theo chữ hoa rồi nối bằng gạch dưới. Công cụ dùng quy ước khác — viết
thường cả cụm:

| Lớp | Tên bảng thật | Trước khi sửa | Sau khi sửa |
|---|---|---|---|
| `Case` | `case` | `case` ✓ | *chưa đọc được* |
| `Incident` | `incident` | `incident` ✓ | *chưa đọc được* |
| `CaseNotes` | `case_notes` | `casenotes` ✗ | *chưa đọc được* |
| `CasePriority` | `case_priority` | `casepriority` ✗ | *chưa đọc được* |
| `CaseSeverity` | `case_severity` | `caseseverity` ✗ | *chưa đọc được* |
| `CaseType` | `case_type` | `casetype` ✗ | *chưa đọc được* |
| `IncidentPriority` | `incident_priority` | `incidentpriority` ✗ | *chưa đọc được* |
| `IncidentSeverity` | `incident_severity` | `incidentseverity` ✗ | *chưa đọc được* |
| `IncidentType` | `incident_type` | `incidenttype` ✗ | *chưa đọc được* |

Hai ca đúng trước đây là hai lớp tên một từ — đúng do may, không do biết. Mọi lớp
nhiều từ đều sai.

Công cụ cũ có ghi `reason` và hạ `inferred` + `partial`, nên nhãn trung thực về *cách
làm*. Nhưng đây vẫn là vi phạm SPEC mục 5.1 quy tắc 4:

> `inferred` chỉ được dùng cho pattern **đã ghi trong spec**. Pattern chưa được đặc tả
> phải bỏ qua hoặc ghi `unresolved_references`, không tự suy đoán cho đủ.

SPEC mục 6c.2 chỉ đặc tả hai ca: `__tablename__` là chuỗi hằng, và `__tablename__`
ghép từ biến. Ca "không khai `__tablename__`" không được đặc tả.

**Đã sửa thế nào:** `table_name` đổi kiểu thành `str | None`. SQLAlchemy thuần không
tự sinh `__tablename__`; lớp nào thiếu mà vẫn chạy được thì lớp cơ sở của repo đó có
`declared_attr` riêng — mỗi repo một quy tắc, không đọc được bằng cú pháp. Giờ ghi
`None` kèm lý do.

Giữ nguyên nhánh SQLModel: thư viện đó **có** quy tắc mặc định tường minh (tên class
viết thường), nên đọc quy tắc của thư viện không phải là đoán. Repo B vẫn đúng 2/2.

| | Trước | Sau |
|---|---|---|
| Đọc đúng | 2 / 9 | 0 / 9 |
| **Đọc sai** | **7 / 9** | **0 / 9** |
| Ghi "chưa đọc được" | 0 / 9 | 9 / 9 |

Đánh đổi rõ ràng: mất 2 câu trả lời đúng-do-may, đổi lấy việc bỏ hẳn 7 câu trả lời sai.
Với một công cụ mà toàn bộ giá trị nằm ở chỗ "không bịa", đây là đổi có lợi.

Khoá bằng `fixture_15_tablename_tu_sinh` + 3 test.

### Lỗi 3 — route đăng ký trong khối `if` không được nêu điều kiện

`app/api/main.py:13-14` của repo B:

```python
if settings.FASTAPI_ENV == "development":
    api_router.include_router(private.router)
```

Route `POST /private/users/` chỉ tồn tại khi chạy ở chế độ development. Trên môi
trường production nó không có.

Công cụ **có** báo route này — đúng, vì nó có thật trong code. Nhưng `reason` chỉ ghi
về prefix động, không nhắc gì tới điều kiện `if`. Người đọc tài liệu không có cách nào
biết route này không tồn tại trên production.

**Đã sửa thế nào:** thay `ast.walk` bằng một hàm duyệt mang theo điều kiện của mọi khối
`if` bao ngoài — `ast.walk` làm phẳng cây nên nhìn thấy lời gọi mà mất thông tin nó
nằm trong `if`. Điều kiện lan theo chuỗi gắn router và vào `reason` của route.

`reason` sau khi sửa:

```
đường dẫn có phần phụ thuộc lúc chạy: {settings.API_V1_STR};
chỉ được đăng ký khi settings.FASTAPI_ENV == 'development'
  — route này không tồn tại ở mọi môi trường
```

Mục "Giới hạn đã biết" của `L3.md` cũng liệt kê riêng các route loại này.

Khoá bằng `fixture_16_route_co_dieu_kien` + 2 test — một route vô điều kiện trong cùng
fixture để chắc chắn nhãn không bị hạ lan sang route khác.

### Bảng gộp

| Lỗi | Trước | Sau | Khoá bằng |
|---|---|---|---|
| 1. Không đọc `app.mount()` | 61 route sai đường dẫn, nhãn `full` sai | 61/61 đúng | fixture 14, 3 test |
| 2. Đoán tên bảng | 7/9 sai | 0/9 sai | fixture 15, 3 test |
| 3. Route trong `if` | không nêu điều kiện | có nêu | fixture 16, 2 test |

Tổng: 63 test đạt (trước khi sửa là 55).

---

## 6. Vì sao 100% không có nghĩa là công cụ đã tốt

Bốn chỉ số đều 100%. Ba lý do khiến con số đó nhỏ hơn vẻ ngoài:

1. **Hai repo này không có ca khó nhất.** Ngưỡng route recall 85% đặt ra với giả định
   sẽ bỏ sót vì đăng ký route động. Chúng tôi đã quét tìm: trong phạm vi đo không có
   route nào đăng ký trong vòng lặp, qua `add_api_route`, hay qua decorator bọc ngoài.
   100% ở đây nghĩa là **"công cụ xử lý tốt ca thường gặp"**, không phải "công cụ xử lý
   được mọi ca".

2. **Danh sách đối chiếu do một Agent lập.** Xem mục 2.

3. **Recall cao mà tên bảng từng sai 7/9.** Chỉ số "tìm thấy hay không" không đo được
   chất lượng của thứ tìm thấy. Nếu chỉ đọc bảng recall thì bỏ lỡ lỗi số 2 hoàn toàn.
   Đây là lý do mục 4.3 tách riêng cột "đọc đúng / đọc sai / chưa đọc được".

---

## 7. Lỗi còn lại, chưa sửa

**Lớp cơ sở bị đếm như một bảng.** Trên repo A, `Base` ở `database/core.py:95` được
liệt kê trong 113 thực thể, dù nó là lớp cơ sở khai báo chứ không phải bảng. Dấu hiệu
nhận ra: nó có **0 cột**.

| | Số |
|---|---|
| Thực thể `dispatch` báo ra | 113 |
| Trong đó là lớp cơ sở, không phải bảng | 1 (`Base`) |

Nằm ngoài phạm vi 48 file đã đo nên không ảnh hưởng con số ở mục 4. Đây là lỗi có sẵn
từ trước, chỉ lộ ra khi mục "Giới hạn đã biết" bắt đầu liệt kê từng lớp. Chưa sửa.

---

## 8. Kết luận — dùng được vào việc gì, chưa dùng được vào việc gì

### Dùng được

- **Liệt kê API route của một dịch vụ FastAPI khai báo bằng decorator.** 84/84 đúng
  trên hai repo, vị trí `file:dòng` không sai ca nào, kể cả khi đường dẫn đi qua
  `include_router` lồng nhiều tầng rồi qua `app.mount()`.
- **Tìm chỗ code gọi HTTP ra ngoài.** 14/14, và quan trọng hơn: không báo ra thứ không
  có, kể cả khi gặp biến local trùng tên thư viện.
- **Liệt kê lớp dữ liệu và các cột.** 11/11 lớp, đọc được cả khoá chính và khoá ngoại.
- **Biết chỗ nào mình không biết.** Prefix là biến thì giữ nguyên biểu thức; tên bảng
  sinh lúc chạy thì ghi "chưa đọc được"; route trong `if` thì nêu điều kiện.
- **Chạy trên repo có file hỏng.** Bỏ qua đúng file hỏng, không kéo sập phần còn lại.

### Chưa dùng được

- **Tên bảng trong cơ sở dữ liệu, khi lớp cơ sở tự sinh tên.** Công cụ nói thẳng là
  không biết — dùng được để biết *có* bảng đó, không dùng được để viết câu lệnh SQL.
- **Đếm chính xác số bảng, nếu repo có lớp cơ sở khai báo riêng.** Xem mục 7.
- **Repo đăng ký route động** (vòng lặp, `add_api_route`, decorator bọc ngoài). Chưa
  đo vì hai repo mẫu không có. Chưa có dữ liệu để nói gì.
- **Ngôn ngữ không phải Python.** Ngoài phạm vi bản này.

### Câu nên nhớ

Công cụ không bịa ra thứ không có — đo được, và là thứ đáng giá nhất với người đọc tài
liệu. Lần đo đầu cho thấy nó **nói chắc hơn mức nó biết** ở hai chỗ; cả hai đã sửa và
khoá bằng test. Cách đo này có giá trị đúng ở điểm đó: nó biến "hình như chạy ổn" thành
ba lỗi cụ thể, có địa chỉ, sửa được.

---

## 9. File liên quan

| File | Nội dung |
|---|---|
| `evaluation/ground_truth.json` | Danh sách đối chiếu repo A — 61 route, 9 bảng, 14 lời gọi, 4 bẫy |
| `evaluation/ground_truth_template.json` | Danh sách đối chiếu repo B — 23 route, 2 bảng |
| `evaluation/_build_ground_truth*.py` | Dữ liệu đọc tay + ghi rõ cách đọc |
| `evaluation/compare.py` | Script so khớp, in từng ca lệch |
| `evaluation/result*.json` | Kết quả đo dạng máy đọc được |
| `tests/fixtures/python/fastapi/fixture_1[456]_*` | Ba fixture khoá ba lỗi ở mục 5 |
