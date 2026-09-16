# Nhật ký cải tiến quy trình

Đề bài mục 2 yêu cầu ghi lại: spec thiếu chỗ nào, Agent chọn sai hướng ở đâu,
phải sửa tay chỗ nào. Ghi ngay khi phát sinh, không nhớ lại vào cuối.

---

## 14/09 — Mốc 1 và Mốc 2

### 1. Spec thiếu: bí danh kiểu của FastAPI hiện đại

**Phát hiện:** Chạy trên `full-stack-fastapi-template`, 29 lời gọi không nối được.
Nguyên nhân là idiom rất phổ biến mà SPEC mục 15.2 không liệt kê:

```python
SessionDep = Annotated[Session, Depends(get_db)]

def read_items(session: SessionDep): ...
```

SPEC chỉ liệt kê bốn dạng đoán kiểu biến, không có dạng "chú thích kiểu trỏ tới
một bí danh, phải đi tiếp một nhịp nữa".

**Xử lý:** Thêm luật đi theo bí danh, giới hạn 5 nhịp để chặn bí danh vòng.
Thêm `fixture_13_type_alias` — fixture thứ 13, ngoài 12 cái SPEC quy định.

**Tín hiệu cho quy trình:** SPEC được viết từ hiểu biết chung về FastAPI, không
từ việc đọc code thật. Bốn dạng đoán kiểu là đúng nhưng chưa đủ. Bài học: nên
chạy thử trên một repo thật **trước** khi chốt spec cho phần khó.

### 2. Lỗi tự mắc: thông báo lý do sai sự thật

**Phát hiện:** Bản đầu in ra `không biết 'session' là gì trong file này` cho 37
lời gọi. Nhưng code có `session: Session` — ta biết chính xác nó là gì, chỉ là
`Session` thuộc `sqlmodel` nên không đọc được bên trong.

Nói "không biết" là **nói dối về năng lực của chính mình theo hướng khiêm tốn giả
tạo**, và làm người đọc tưởng công cụ yếu hơn thực tế.

**Xử lý:** Tách ba nhóm rõ ràng — nối được trong repo / gọi ra thư viện ngoài /
thật sự không biết. Sau khi sửa, tỷ lệ nối được trên `dispatch` đi từ 57% lên 63%
mà **không đổi một dòng logic nối nào** — chỉ là phân loại lại cho đúng.

**Tín hiệu cho quy trình:** Nguyên tắc trung thực của SPEC (mục 3.3, 5.1) mới chỉ
áp cho trường `resolved` và `confidence`. Nó phải áp cho cả nội dung trường
`reason`. Một lý do sai cũng nguy hiểm như một kết luận sai.

### 3. Cố ý làm khác SPEC

| SPEC nói | Đã làm | Lý do |
|---|---|---|
| Mục 14.1: có `core/resolution/orchestrator.py` | Bỏ | Chỉ có một ngôn ngữ, tạo tầng trung gian rỗng là abstraction thừa. Khi thêm Java thì tách sau |
| Mục 14.4: dựng sẵn thư mục rỗng cho `flask/`, `django/`, `java/` | Chưa tạo | Thư mục rỗng không tồn tại được trong git |

### 4. Spec tự mâu thuẫn

Mục 9 task 6 yêu cầu "đánh dấu function nào có try/except bao quanh lời gọi" để
bước rà soát bằng AI dùng. Nhưng `FunctionNode` ở mục 5 không có trường nào chứa
thông tin đó. Chưa xử lý — sẽ chốt khi làm mốc 6.

### 5. Tìm thấy lỗi thật trong repo mã nguồn mở

`full-stack-fastapi-template` tại commit `cb740b6`, file `backend/app/api/deps.py`
dòng 36:

```python
except InvalidTokenError, ValidationError:
```

Đây là cú pháp Python 2, không chạy được trên Python 3. Công cụ báo đúng vị trí,
bỏ qua file đó và phân tích tiếp thay vì sập.

Hệ quả đo được: **một file hỏng kéo theo 29 lời gọi không nối được**, vì chính
file đó khai báo `SessionDep` và `CurrentUser`. Đây là ví dụ tốt cho phần demo —
công cụ suy giảm dần chứ không chết hẳn, và nói rõ mình mất gì.

---

## 14/09 — Mốc 3, 4, 5

### 6. Spec thiếu chỗ chứa quan hệ "hàm nào chạm bảng nào"

SPEC mục 5.2 định nghĩa cạnh `reads_writes` giữa hàm và bảng dữ liệu. Nhưng IAM
ở mục 5 không có trường nào chứa quan hệ đó, mà graph builder lại không được đọc
lại source. Không có dữ liệu thì không dựng được cạnh.

**Xử lý:** thêm ba trường vào IAM, đều là bổ sung chứ không sửa cái đã có:

| Trường | Ở đâu | Vì sao cần |
|---|---|---|
| `resolved_symbol` | `Reference` | `resolved_module` chỉ cho biết FILE. Muốn nối cạnh giữa hai hàm phải biết tên hàm đầy đủ, nếu không sẽ đoán sai khi một file có hai hàm trùng tên |
| `qualified_name` | `FunctionNode` | để khớp với `resolved_symbol` ở trên |
| `entity_refs` | `FunctionNode` | `db.query(Order)` — `Order` là tên trần, không phải lời gọi, nên phần nối lời gọi bỏ qua nó. Đây lại chính là chỗ cho biết route nào đọc bảng nào |

### 7. Spec thiếu: bí danh kiểu đã ghi ở mục 1, còn đây là các luật phát sinh khác

| Luật thêm | Vì sao |
|---|---|
| `__abstract__ = True` thì không phải bảng | Class trung gian của SQLAlchemy. Không có luật này thì mọi class cơ sở đều bị báo là bảng |
| `Relationship()` / `relationship()` không phải cột | Đó là quan hệ giữa hai bảng |
| SQLModel `table=True` | Cả hai repo mẫu đều dùng SQLModel chứ không phải SQLAlchemy thuần. SPEC mục 2.1 chỉ ghi SQLAlchemy |
| Không khai báo `__tablename__` thì suy theo tên class viết thường | Là hành vi mặc định của SQLModel. Gán `confidence = inferred` kèm lý do, không gán `exact` |

### 8. Lỗi tự mắc: đếm cả file không phải Python

Chạy trên `Netflix/dispatch`, tool báo `playwright.config.ts` là "file Python lỗi
cú pháp". SPEC mục 4.4.3 đã nói rõ: file thuộc ngôn ngữ khác nằm ngoài phạm vi
parser của đơn vị, **không được coi là lỗi cú pháp**. Đã sửa: mỗi đơn vị chỉ giữ
file của ngôn ngữ chính. Sau khi sửa, dispatch đọc 657/657 file, 0 lỗi.

Bài học: một con số "1 file lỗi" trông vô hại nhưng làm người đọc tưởng repo có
vấn đề, trong khi lỗi nằm ở công cụ.

### 9. Cố ý bỏ `core/resolution/orchestrator.py`

Đã ghi ở mục 3. Sau khi viết xong phần nối tham chiếu, xác nhận quyết định này
đúng: toàn bộ logic điều phối bốn bước nằm gọn trong `resolve_call()` khoảng 30
dòng. Tách thành một tầng riêng cho một ngôn ngữ duy nhất sẽ chỉ thêm chỗ để lạc.

---

## 14/09 — Mốc 6 (hai bước AI)

### 10. Diễn giải lại yêu cầu "AI Reviewer" cho an toàn hơn SPEC

SPEC mục 6b gọi bước rà soát là "AI Reviewer". Nhưng đọc kỹ bốn ràng buộc ở mục
6b.1 thì **cả bốn đều là luật đếm được trên IAM**, không cần AI:

| Loại | Ràng buộc SPEC | Bản chất |
|---|---|---|
| `unresolved_reference` | chỉ lấy từ `unresolved_references` đã có | lọc danh sách |
| `empty_handler_calls` | `APIRoute.calls` rỗng hoặc chưa resolve | đếm |
| `orphan_entity` | duyệt hết `calls` không thấy ai trỏ tới | duyệt |
| `external_call_no_error_handling` | không nằm trong try/except | kiểm tra cờ |

**Đã làm:** phần tĩnh phát hiện (tất định), AI chỉ viết lại câu tóm tắt cho dễ
đọc. Để AI tự quyết định gắn cờ chỗ nào là mở đường cho nó bịa cảnh báo không có
bằng chứng — đúng thứ mục 3.1 cấm.

Hệ quả có ích ngoài dự kiến: cảnh báo vẫn chạy được khi không có AI, chỉ khác câu
chữ. Chạy `--no-ai` vẫn ra đủ mục 8 trong tài liệu.

### 11. Ranh giới AI: chặn bằng thiết kế, không chặn bằng kỷ luật

SPEC mục 8.3 yêu cầu test rằng schema output của AI không có trường nào chèn được
route mới. Làm vậy là đủ theo SPEC, nhưng vẫn còn một đường: code sau đó có thể
nhét mô tả vào IAM.

**Đã làm thêm một lớp:** mô tả do AI viết ghi ra `descriptions.json`, cảnh báo ghi
ra `findings.json`. Không thứ nào nằm trong `IAM.json`.

Nhờ vậy câu "AI không sửa dữ liệu" đi từ **lời hứa** thành **điều kiểm chứng được
bằng `diff`**: chạy có AI và không AI cho ra `IAM.json`, `graph.json`,
`diagram.mmd` giống hệt từng byte. Đã khoá bằng test.

### 12. Thêm trường thứ tư vào IAM: `inside_try_except`

SPEC mục 6c.3 yêu cầu đánh dấu lời gọi ra ngoài có nằm trong try/except không,
nhưng không nói cất ở đâu — `ExternalCall` ở mục 5 không có trường nào chứa. Đây
là chỗ SPEC tự mâu thuẫn lần thứ hai (lần đầu ghi ở mục 4 phần trên).

---

## 16/09 — Reset phạm vi V2 về đúng Code → L3

### 13. Phát hiện requirement đã lấn sang một dự án khác

Đề bài tách **Code → L3 Generator** và **Repository Knowledge Graph** thành hai dự
án. Bản SPEC cũ lại đưa `FunctionNode`, full call graph và Repository Knowledge
Graph vào contract chính của Code → L3. Điều này kéo kiến trúc sang mục tiêu hiểu
mọi function/call, trong khi output gốc cần component model và dependency diagram.

**Quyết định mới:** phân tích mức function vẫn được dùng làm evidence, nhưng public
L3/diagram/architecture graph tập trung application, component, API, data, external
system, event và configuration quan trọng.

### 14. Bài học: độ sâu phân tích khác độ sâu trình bày

Route → Service → Repository → DB có thể cần lần qua parameter, return, attribute và
call. Vì vậy không xóa resolver chỉ vì L3 cần tổng quát. Ngược lại, việc resolver biết
500 function không có nghĩa diagram phải vẽ 500 function.

Nguyên tắc chốt:

> Analyze deep enough; present at L3.

Resolver chỉ tiếp tục được mở rộng khi có use case/acceptance criterion chứng minh nó
giúp tìm hoặc tránh báo sai một quan hệ kiến trúc.

### 15. Không biến unresolved thành cạnh kiến trúc

Raw call chưa xác định receiver được giữ trong evidence/limitations. Không vẽ cạnh
framework nét đứt chỉ vì method có tên `mount`, `post` hoặc `include_router`. Chỉ khi
adapter khớp symbol đầy đủ mới được tạo semantic edge.

### 16. Artifact đã đồng bộ

Đã viết lại Architecture V2, Use Cases, Scenarios, SPEC và README theo contract mới;
HANDOFF cũng được cập nhật. COMPETITOR_RESEARCH được đánh dấu rõ là snapshot lịch sử
để roadmap cũ không bị đọc như requirement hiện hành. Chưa sửa code, chưa chạy
test/benchmark và chưa cập nhật EVALUATION/examples. Bước implementation kế tiếp phải
bắt đầu từ acceptance test cho Architecture IAM/projection và component relation.
