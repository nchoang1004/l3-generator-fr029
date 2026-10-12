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

---

## 07–09/10 — Bộ kiểm FR-029 trên nhiều repo

Mục này ghi chỗ spec thiếu, chỗ agent đi sai hướng và chỗ phải sửa tay trong đợt nâng bộ kiểm FR-029. Chi tiết: `docs/FR029-bao-cao-kiem-bo-kiem-20261008.md`, `.aide/evidence/diaries/DIARY-CR-L3GEN-2026-008.md`.

### 17. Spec thiếu: thế nào là "lời gọi HTTP ra ngoài"

AC-L3GEN-029-08 không nói lời gọi qua hàm bọc của dự án có tính không. Ví dụ `http_retry.get(url)` gọi tiếp `httpx.request` (shortlist), hay lớp `HttpxClient` (case_auto_hub). Hai giám khảo hiểu khác nhau. Bộ kiểm hiện chỉ tính lời gọi trực tiếp httpx/requests/aiohttp. Chưa chốt.

### 18. Spec thiếu: phạm vi đọc của `scripts/`

FR-028 chỉ đọc file trong `scripts/` khi nó "import code của repo". Ở caura, 6 script chỉ import một file helper nằm cùng `scripts/`. Code coi là ngoài phạm vi; Codex khi chấm lại coi là trong. Chưa chốt.

### 19. Đính chính mục 5: `except A, B:` không còn là lỗi

Mục 5 (14/09) gọi `except InvalidTokenError, ValidationError:` là cú pháp Python 2. Điều đó chỉ đúng với Python dưới 3.14. Từ 3.14 (PEP 758), cú pháp này hợp lệ. Bộ kiểm chạy Python 3.11 nên không đọc được file dùng nó: PrintStash bị 57 dòng nhiễu vì vậy. Đã sửa bằng cách thử đọc lại sau khi thêm ngoặc, giữ nguyên số dòng.

**Tín hiệu cho quy trình:** repo thật có thể dùng Python mới hơn công cụ. Cần ghi phiên bản Python của công cụ trong giới hạn của báo cáo.

### 20. Agent đi sai hướng: bộ kiểm lớn dần thành extractor

Người dùng đã chọn "agent thuần" (CR-L3GEN-2026-008). Mỗi lần sửa một phản ví dụ, bộ kiểm hiểu thêm một dạng code. Sau 10 vòng, nó dựng đồ thị `include_router`, theo client qua nhiều file và nhắc dependency cấp router. Code vẫn không tự tạo dữ kiện, nhưng ranh giới mờ dần. Agent không dừng để mở OQ như EXEC §B.15 yêu cầu.

**Tín hiệu cho quy trình:** cần một ranh giới kiểm được cho bộ kiểm, ví dụ: "chỉ được từ chối hoặc nhắc, không được tạo mục". Trước mỗi luật mới, hỏi: đây là kiểm bằng chứng hay đang tự trích dữ kiện?

### 21. Lỗi tự mắc: 5 hồi quy do chính bản sửa

Năm bản sửa gây lỗi mới: mất thư viện của client, crash, và ba lần tăng nhiễu (primer +32 dòng; module dự án tên `requests`; chuỗi `.requests.`). Gold bắt được 2 lỗi. Việc so gói held-out trước và sau mỗi lần sửa bắt được 3 lỗi còn lại: chúng không có trong gold.

**Bài học:** sau mỗi nhóm sửa, chạy gold, bộ kiểm giả, và diff dòng nghi ngờ của các repo held-out. Diff rẻ và bắt được nhiễu mà gold không có.

### 22. Lỗi đo: gói đem chấm trình bày khác thứ agent nhận

Gói held-out gom tham số theo tên dependency, không theo route. Vì vậy giám khảo chấm "sai" 4 mục mà bộ kiểm thật làm đúng: `album_id` có trong path route; 3 hàm cùng tên ở 3 module bị gộp. Đã kiểm bằng test trên bộ kiểm thật, rồi sửa công cụ đo.

**Bài học:** thứ đem chấm phải giống thứ người dùng cuối nhận. Nếu không, giám khảo đang chấm công cụ đo chứ không chấm sản phẩm.

### 23. Kiểm đối kháng không hội tụ nhanh

Số phản ví dụ mỗi vòng Codex: 25 → 10 → 7 → 8 → 7 → 8 → 8 → 7 → 7 → 6. Mỗi vòng xác nhận gần hết ca cũ đã sửa, nhưng luôn còn dạng mới. Mức tin cậy Codex đánh giá không đổi qua 6 vòng.

**Bài học:** số vòng đối kháng không thay được phép đo trên repo chọn ngẫu nhiên. Muốn ước tỉ lệ lỗi thật trên repo mới thì phải đo trên repo held-out, không chỉ đếm phản ví dụ.

### 24. Phải sửa tay và thay giám khảo

- Heredoc trong Bash làm hỏng `\n`, `\s` trong script vá code nhiều lần. Phải ghi script bằng công cụ Write hoặc sửa bằng Edit.
- Codex và agent Claude hết lượt nhiều lần. Một đợt chấm held-out (3 repo) và hai vòng đối kháng phải dùng agent Claude; hai agent bị dừng giữa chừng. Agent ghi phát hiện ra file (`notes.md`) sau mỗi bước nên không mất việc đã làm.

## 11–12/10 — Giảm token, TAI-LIEU.md, bảng và sự kiện

Hồ sơ: CR-L3GEN-2026-009, DIARY-CR-L3GEN-2026-009, OQ-L3GEN-019 đến 022.

### 25. Giảm số request không đủ, phải đổi model

Chế độ đọc một lần giảm từ 67 request (0,218 USD) xuống 3 request. Với gpt-4.1-mini, chi phí còn ~0,03 USD nhưng 0/5 route được nhận. gpt-5 cho 4–5/5 route, 0,17–0,19 USD.

**Bài học:** đo chi phí phải đi cùng số mục được nhận. Rẻ mà không ra kết quả thì không phải cải thiện.

### 26. Agent tự mở rộng phạm vi khi người dùng nói "làm đi"

Claude làm cả 5 đợt đề xuất, tự chọn đọc tĩnh cho bảng, sự kiện, thư viện, cấu hình, và thêm đầu ra ngoài FR. Code có test, nhưng spec chưa ghi và người dùng chưa duyệt từng quyết định.

**Bài học:** "làm đi" duyệt danh sách việc, không duyệt các quyết định thiết kế bên trong. Quyết định đó phải mở OQ trước khi làm.

### 27. Test không tốn tiền bằng agent đóng vai model

Agent Claude đọc đúng prompt và request như model thật, nộp câu trả lời; bộ kiểm chấm offline. Lần đầu dùng (12/10) tìm được 3 lỗi bộ kiểm từ chối nhầm: prefix trên dòng sau của `include_router(`, `pydantic_model_creator`, `Depends(LớpGọiĐược(...))`.

**Bài học:** kiểm được bộ kiểm và prompt gần như miễn phí. Không đo được model thật, nên vẫn cần một lần nghiệm thu bằng model thật.

### 28. Đóng băng đầu ra trước khi chấm

Với repo held-out và phần CSDL: đề giám khảo viết trước khi có đầu ra; hash đầu ra trước khi chấm; vòng 2 dùng giám khảo mới không xem vòng 1. Giám khảo tìm ra lỗi mà gold không có (Redis pub/sub bị sót không cảnh báo; ràng buộc bảng).

**Bài học:** gold chỉ chấm được thứ gold có. Cần giám khảo đọc source để tìm phần thiếu.

### 29. Hồ sơ quy trình lại ghi muộn

CR, Task, PLAN của đợt này ghi ngày 12/10, sau khi code xong. Chỉ task giao diện (TASK-L3GEN-029-13) có plan trước khi code.

**Bài học:** như mục 20: phải ghi CR và plan ngay khi nhận yêu cầu, kể cả khi người dùng giục "làm đi".
