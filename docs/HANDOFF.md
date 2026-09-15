# Bàn giao — Code → L3 Generator

Đọc file này là đủ để tiếp tục công việc, không cần hỏi lại từ đầu.

Cập nhật: 14/09/2026, sau khi xong Mốc 6.

---

## 1. Dự án này làm gì

Một công cụ dòng lệnh đọc source code Python/FastAPI (chỉ đọc cú pháp, **không
chạy code**) và sinh ra tài liệu kiến trúc L3, sơ đồ, và file graph. Mọi dòng
trong tài liệu tra ngược được về `file:dòng` trong source thật.

Thuộc chương trình "Platform Satellite Projects" (đề bài mục 3.6), làm theo
Agentic SDLC: người viết spec và tiêu chí, Agent sinh code.

**Chạy thử ngay:**

```bash
pip install -e .
l3gen tests/fixtures/python/fastapi/sample_app --no-ai -o out
```

---

## 2. Hiện trạng — làm được tới đâu

| Mốc | Trạng thái | Số đo thật |
|---|---|---|
| 1. Khung chạy được | Xong | quét + đọc cây cú pháp, bỏ qua file lỗi |
| 2. Nối tham chiếu | Xong | dispatch: nối được 2930/4617 (63%) |
| 3. Ba bộ trích xuất | Xong | route, bảng dữ liệu, gọi ra ngoài |
| 4. Gộp IAM + graph | Xong | dispatch: 8916 node, 9895 cạnh |
| 5. Sinh tài liệu | Xong | 4 file, chạy hai lần giống hệt |
| 6. Hai bước AI | Xong | 15 test khoá ranh giới AI |
| **7. Đo độ chính xác** | **Đang làm — chưa bắt đầu** | |
| 8. Đóng gói | Chưa | |
| 9. Giao diện web | Chưa | |

**Quy mô:** 4.012 dòng code, 947 dòng test, **55 test đạt**, 14 fixture.

### Đã chạy thật trên hai repo mã nguồn mở

| Repo | File | Route | Bảng | Gọi ra ngoài | Thời gian |
|---|---|---|---|---|---|
| `Netflix/dispatch` @ `dd2837e` | 657 (0 lỗi cú pháp) | 290 | 113 | 15 | 1,6 giây |
| `fastapi/full-stack-fastapi-template` @ `cb740b6` | 24 (1 lỗi) | 23 | 2 | 0 | <1 giây |

Cả hai clone sẵn trong `sample-repos/` (thư mục này nằm trong `.gitignore`).

**Kiểm chứng chéo:** đếm tay decorator route trên template ra đúng 23/23. Trên
dispatch grep ra 278, công cụ ra 290 — công cụ đúng, grep thiếu vì chỉ bắt
`@router.` và `@app.`, bỏ sót `@user_router.`, `@auth_router.`, `@api_router.`.

---

## 3. Cơ chế cốt lõi — hiểu cái này là hiểu cả dự án

### Câu then chốt

> **Cây cú pháp cho biết TÊN, không cho biết NGHĨA.**

Nhìn `svc.confirm()`, cây chỉ nói: *có một biến tên `svc`, gọi một method tên
`confirm`*. Nó **không biết** `svc` là cái gì, `confirm` nằm ở file nào. Toàn bộ
phần khó của dự án nằm ở câu này.

### Cách bắc cầu: hai bảng tra cứu

**Bảng 1 — danh bạ.** Duyệt hết file `.py`, ghi ai định nghĩa ở đâu:

```
app.services.order.OrderService          -> app/services/order.py:6
app.services.order.OrderService.confirm  -> app/services/order.py:7
```

**Bảng 2 — tên gọi trong TỪNG file.** Trong `api/orders.py`, tên `OrderService`
nghĩa là `app.services.order.OrderService`.

> **Bảng 2 tuyệt đối không được gộp chung cho cả repo.** File A lấy
> `OrderService` từ `app.services.order`, file B có thể lấy cùng tên đó từ
> `legacy.service`. Gộp chung thì graph vẫn đẹp, test vẫn qua, chỉ có vài cạnh
> trỏ nhầm file và không cách nào phát hiện. `fixture_8` bắt đúng lỗi này.

Có hai bảng rồi thì mọi việc còn lại thành tra bảng. Chi tiết đầy đủ (5 câu hỏi,
5 cơ chế, kèm ví dụ 4 file chạy xuyên suốt) nằm ở plan:
`C:\Users\Khiem\.claude\plans\khi-vi-t-c-c-file-refactored-stonebraker.md` mục 2.

### Đoán kiểu biến — chỉ nhận 5 dạng

| Dạng | Ví dụ |
|---|---|
| Chú thích kiểu | `def f(svc: OrderService)` |
| Gán trực tiếp | `svc = OrderService()` |
| Tiêm phụ thuộc | `svc = Depends(get_service)` → tra kiểu trả về |
| Thuộc tính `__init__` | `self.repo = OrderRepository()` |
| **Bí danh kiểu** | `SessionDep = Annotated[Session, Depends(get_db)]` |

Dạng thứ 5 không có trong SPEC — phát hiện khi chạy trên repo thật. Cả hai repo
mẫu đều dùng.

Dạng khác → `resolved = False`. **Đây là kết quả ĐÚNG, không phải lỗi.**

---

## 4. Các quyết định đã thống nhất — không mở lại

| # | Quyết định | Lý do |
|---|---|---|
| 1 | Mô tả AI ghi ra `descriptions.json`, cảnh báo ra `findings.json` — **không vào `IAM.json`** | Biến "AI không sửa dữ liệu" từ lời hứa thành thứ `diff` kiểm chứng được |
| 2 | Bước rà soát **phát hiện tất định**, AI chỉ viết lại câu tóm tắt | Bốn ràng buộc ở SPEC mục 6b.1 đều là luật đếm được. Để AI tự quyết là mở đường cho nó bịa cảnh báo |
| 3 | Bỏ `core/resolution/orchestrator.py` (SPEC mục 14.1 có) | Logic điều phối gọn trong `resolve_call()` ~30 dòng. Một ngôn ngữ mà tách tầng riêng chỉ thêm chỗ để lạc |
| 4 | Chưa tạo thư mục rỗng `flask/`, `django/`, `java/` (SPEC mục 14.4 muốn) | Thư mục rỗng không tồn tại được trong git |
| 5 | `.gitignore` giữ nguyên, `PROGRESS.md` không commit | Người dùng đã chốt, không bàn lại |
| 6 | Giao diện web làm sau cùng | Lõi chạy đúng trước; xoá thư mục UI đi thì dòng lệnh vẫn chạy |
| 7 | Không đoán khi thiếu thông tin | 37% lời gọi chưa nối được là con số trung thực, không thêm luật đoán để đẩy số lên |

### Bốn trường thêm vào IAM ngoài SPEC

Đều là bổ sung, không sửa cái đã có. Lý do ghi trong docstring của từng trường.

| Trường | Ở đâu | Vì sao cần |
|---|---|---|
| `resolved_symbol` | `Reference` | `resolved_module` chỉ cho biết FILE. Nối cạnh giữa hai hàm cần tên hàm đầy đủ |
| `qualified_name` | `FunctionNode` | Khớp với `resolved_symbol` |
| `entity_refs` | `FunctionNode` | `db.query(Order)` — `Order` là tên trần, không phải lời gọi. Đây là chỗ cho biết route nào đọc bảng nào |
| `inside_try_except` | `ExternalCall` | SPEC mục 6c.3 yêu cầu đánh dấu nhưng không có chỗ chứa |

---

## 5. Quy tắc phải tuân thủ

### 5.1 Cách viết tài liệu (`CLAUDE.md` mục 0)

Lỗi đã xảy ra trong dự án này: **tài liệu quá dài và nói phức tạp những chuyện
đơn giản**. Đọc `CLAUDE.md` mục 0 trước khi viết bất cứ file `.md` nào.

Tóm tắt: viết ngắn, một câu một ý, hạn chế từ tiếng Anh, ví dụ cụ thể thay mô tả
trừu tượng, gọi đúng tên (hàm duyệt cây cú pháp thì gọi là hàm duyệt cây cú pháp,
không gọi là "chuyên viên trích xuất").

### 5.2 Cách làm việc

- **Hỏi trước khi làm thêm việc không được giao** (`CLAUDE.md` đầu file).
- **Báo cáo vào chat sau mỗi mốc quan trọng**, chi tiết và dễ hiểu.
- Số liệu phải là số đo thật, hoặc ghi rõ "chưa đo".

### 5.3 Nguyên tắc bất biến của sản phẩm (SPEC mục 0.5)

1. Không bao giờ chạy code của repo đang phân tích — chỉ `read_text()` rồi
   `ast.parse()`.
2. AI không được thêm/sửa/xoá dữ liệu trong IAM.
3. Không đoán khi thiếu thông tin. Ghi `resolved = False` hoặc hạ `partial`.
4. Mọi dòng trong tài liệu tra ngược được về `file:dòng`.
5. Tầng phân tích tĩnh không phụ thuộc tầng AI. AI hỏng chỉ làm giảm chất lượng.
6. Không có con số nào không truy được về nguồn.

---

## 6. Việc tiếp theo

### Mốc 7 — Đo độ chính xác (đang làm, chưa bắt đầu)

Đây là thứ tách dự án này khỏi mọi bài tập khác. Theo SPEC mục 8.5.

**Bước 1 — lập ground truth (việc của người, không giao Agent).**
Chọn repo, hai người **đọc tay độc lập** toàn bộ, mỗi người tự liệt kê route,
bảng dữ liệu, lời gọi ra ngoài. Đối chiếu, chỗ lệch thì bàn tới khi thống nhất.
Chốt thành `ground_truth.json`.

Ước tính 1–1,5 ngày cho 2 người. Nếu chỉ có một người: đọc hai lượt cách nhau, và
**ghi rõ trong `EVALUATION.md` là do một người lập** — nói thật còn hơn giả vờ.

**Bước 2 — đo và viết `EVALUATION.md`.** Precision/recall cho từng loại thực thể,
phân tích từng ca bỏ sót và báo thừa, mở đầu bằng đoạn tóm tắt 3–5 câu không dùng
thuật ngữ thống kê.

**Ngưỡng đặt trước, không được hạ sau khi thấy kết quả** (SPEC mục 8.5.3):
route recall ≥ 85%, route precision nhóm `exact` ≥ 95%, bảng recall ≥ 90%,
gọi ra ngoài recall ≥ 80%.

**Repo nào?** `full-stack-fastapi-template/backend` (24 file) hơi nhỏ so với mức
30–80 SPEC đề ra, nhưng đọc tay được trong ngày. `dispatch` (657 file) quá lớn để
đọc tay. Cần chốt: dùng template và ghi rõ cỡ mẫu nhỏ, hay tìm repo thứ ba.

### Mốc 8 — Đóng gói

`README.md` 7 phần, thư mục `examples/` có kết quả đã chạy và commit,
`pip install` được. Kiểm chứng: xoá môi trường ảo, cài lại theo README, chạy được.

### Mốc 9 — Giao diện web

SPEC mục 13. Thứ tự: tổng quan → bảng route → graph tương tác → cảnh báo → bảng
dữ liệu → giới hạn. Kiểm chứng: xoá cả thư mục giao diện, dòng lệnh vẫn chạy.

### Việc chưa làm, phải xong trước khi demo

**Dọn ngôn từ thổi phồng trong tài liệu cũ.** SPEC gọi năm hàm duyệt cây cú pháp
là "5 chuyên viên độc lập". `docs/COMPETITOR_RESEARCH.md` có "khoảng trống thị
trường đáng chiếm". Vi phạm `CLAUDE.md` mục 0.3.

---

## 7. Vấn đề đang tồn tại

### 7.1 37% lời gọi chưa nối được — và vì sao không nên cố

Phần lớn là code không khai báo kiểu:

```python
def get(*, db_session, case_id: int) -> Case | None:   # db_session không khai kiểu
    return db_session.query(Case)...
```

Không có cách nào biết `db_session` là gì mà không đoán. **Không thêm luật kiểu
"tham số tên `db_session` thì chắc là Session"** — đó là đoán, vi phạm nguyên tắc
gốc. 63% là con số trung thực.

### 7.2 Ba nhóm cần phân biệt khi báo số

Đây là chỗ tôi từng làm sai và đã sửa:

| Nhóm | Nghĩa |
|---|---|
| Nối được | Tìm thấy định nghĩa trong repo |
| Gọi thư viện ngoài | Biết chính xác nó đi đâu, chỉ không đọc được bên trong. **Phân loại đúng, không phải thất bại** |
| Chưa biết | Thật sự không xác định được |

Bản đầu tôi in "không biết `session` là gì" cho 37 lời gọi, trong khi code có
`session: Session` rõ ràng. Nói vậy là **nói dối về năng lực của chính mình theo
hướng khiêm tốn giả tạo**. Sau khi phân loại lại, tỷ lệ đi từ 57% lên 63% mà
không đổi một dòng logic nào.

### 7.3 Lỗi thật trong repo mẫu

`full-stack-fastapi-template` @ `cb740b6`, file `backend/app/api/deps.py` dòng 36:

```python
except InvalidTokenError, ValidationError:   # cú pháp Python 2, không chạy được
```

Công cụ báo đúng vị trí và chạy tiếp thay vì sập. Hệ quả đo được: **một file hỏng
kéo theo 29 lời gọi không nối được**, vì chính nó khai báo `SessionDep`. Tư liệu
demo tốt.

### 7.4 Cỡ mẫu cho Mốc 7 chưa chốt

Xem mục 6 ở trên.

---

## 8. Cấu trúc code

```
src/l3gen/
├── cli.py                    lệnh dòng lệnh, xử lý lỗi
├── pipeline.py               điều phối 8 bước
├── models/
│   ├── iam.py                cấu trúc dữ liệu trung gian (SPEC mục 5)
│   ├── stack.py              ServiceUnit, DetectedStack
│   ├── graph.py              GraphNode, GraphEdge
│   └── findings.py           ReviewFinding (4 loại, khoá bằng Literal)
├── detection/discovery.py    chia repo thành service theo file manifest
├── languages/python/
│   ├── parser.py             quét file + ast.parse
│   ├── literals.py           đọc chuỗi, giữ nguyên phần là biến
│   ├── resolution.py         hai bảng tra cứu + đoán kiểu + nối lời gọi
│   ├── common/callgraph.py   duyệt hàm, thu lời gọi và tham chiếu bảng
│   └── frameworks/fastapi/
│       ├── routes.py         ghép đường dẫn qua cây gắn router
│       └── external.py       httpx / requests + cờ try/except
├── orm/sqlalchemy.py         SQLAlchemy + SQLModel
├── core/
│   ├── resolution/           symbol_table.py, inheritance.py
│   ├── builder.py            gộp thành IAM
│   └── graph_builder.py      IAM -> node/cạnh
├── ai/
│   ├── schemas.py            khoá cứng dạng dữ liệu AI trả về
│   ├── client.py             gọi claude-opus-5, hỏng thì bỏ qua
│   ├── enrichment.py         viết mô tả
│   └── reviewer.py           phát hiện tất định + AI viết lại câu
└── output/                   markdown.py, mermaid.py, json_export.py
```

### File đầu ra

| File | Nội dung | Giống hệt qua hai lần chạy? |
|---|---|---|
| `L3.md` | Tài liệu chính | Chỉ khác con số thời lượng chạy |
| `diagram.mmd` | Sơ đồ Mermaid rút gọn | Có |
| `graph.json` | Node và cạnh | Có |
| `IAM.json` | Toàn bộ dữ liệu đọc từ code | Có |
| `findings.json` | Cảnh báo | Có |
| `descriptions.json` | Mô tả do AI viết (chỉ khi có AI) | — |
| `run.json` | Thời điểm và thời lượng chạy | Không (cố ý tách ra) |

---

## 9. Fixture

14 cái. SPEC mục 8.1 quy định 12, phát sinh thêm 2.

| Fixture | Kiểm cái gì |
|---|---|
| 1 | Route khai báo thẳng trên `FastAPI()` |
| 2 | Router lồng 3 tầng, một tầng prefix là biến |
| 3 | Bảng SQLAlchemy: khoá chính, khoá ngoại, tên bảng ghép từ biến |
| 4 | Gọi `httpx` và `requests`, URL ghép từ biến |
| 5 | File lỗi cú pháp không kéo sập file khác |
| 6 | Gọi hàm xuyên file + import thư viện ngoài |
| 7 | Bảng kế thừa qua class trung gian ở file khác |
| **8** | **Cùng tên class, khác module — bắt lỗi thiết kế âm thầm** |
| 9 | Kế thừa sâu 3 tầng qua 3 file |
| 10 | Class cha thuộc thư viện ngoài → `resolved=False` là đúng |
| **11** | **Kế thừa vòng `A(B)`, `B(A)` — tool không được treo** |
| 12 | Đa kế thừa, method có ở cả hai cha |
| 13 | Bí danh kiểu `Annotated[...]` (phát sinh thêm) |
| `sample_app` | Ví dụ 4 file trong plan, chạy xuyên suốt |
| `detection/multi_service` | Repo có Java + FastAPI |

---

## 10. Kịch bản demo (10 phút)

Thứ tạo cảm giác dự án được đầu tư nhiều **không phải công nghệ cao siêu**, mà là
chạy thật trước mặt người xem, trên code họ tự kiểm chứng được, và tự nói giới
hạn trước khi bị hỏi.

| Phút | Làm gì |
|---|---|
| 0:30 | Mở tài liệu kiến trúc viết tay của repo mẫu, chỉ hai chỗ đã lệch với code |
| 1:30 | `l3gen ./dispatch --no-ai` chạy trực tiếp, đếm giây (1,6 giây / 657 file) |
| 3:00 | **Mời mentor tự chọn một dòng bất kỳ** trong `L3.md`, bấm vào, mở đúng chỗ trong source. Khoảnh khắc mạnh nhất — không phải mình chọn dòng đẹp để khoe |
| 4:00 | Chạy lần hai, `diff` → rỗng. Chạy có AI, so `IAM.json` → giống hệt, chỉ khác mô tả |
| 5:30 | Mở `EVALUATION.md`, nói thẳng số bỏ sót và số báo thừa |
| 6:30 | Chạy trên repo có Java + FastAPI, tự chia, nói rõ phần bỏ qua |
| 8:00 | Giao diện web |
| 8:30 | Tự liệt kê ba thứ chưa làm được, kèm lý do kỹ thuật |

**Chuẩn bị:** repo clone sẵn không phụ thuộc mạng; một bản chạy sẵn dự phòng;
câu trả lời cho *"tool này khác gì hỏi thẳng AI đọc code?"*.

---

## 11. Tài liệu liên quan

| File | Nội dung |
|---|---|
| `CLAUDE.md` | **Đọc mục 0 trước khi viết tài liệu** |
| `SPEC_Code_to_L3_Generator.md` | Đặc tả gốc, 1689 dòng |
| `Đề bài.md` | Đề bài chương trình, mục 3.6 là dự án này |
| `docs/AGENTIC_SDLC_LOG.md` | **Sản phẩm bàn giao bắt buộc.** Spec thiếu gì, tôi sai gì, chỗ nào cố ý khác SPEC |
| `docs/USE_CASES.md`, `docs/SCENARIOS.md` | Requirement |
| `docs/COMPETITOR_RESEARCH.md` | Khảo sát đối thủ (còn ngôn từ cần dọn) |
| `PROGRESS.md` | Nhật ký + bảng số đo (không commit) |

---

## 12. Lệnh hay dùng

```bash
python -m pytest -q                                    # 55 test
l3gen <đường-dẫn> --no-ai -o out                       # chạy không AI
l3gen <đường-dẫn> -o out                               # có AI (cần L3GEN_API_KEY)
l3gen <đường-dẫn> --no-ai -o out -v                    # in chi tiết

# Chứng minh chạy hai lần giống hệt
l3gen <repo> --no-ai -o r1 && l3gen <repo> --no-ai -o r2
diff r1/IAM.json r2/IAM.json && diff r1/graph.json r2/graph.json
```
