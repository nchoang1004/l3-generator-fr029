# SPEC — Code → Architecture / L3 Generator (MVP)

> Tài liệu này là đặc tả (spec) để giao cho AI Agent triển khai theo mô hình Agentic SDLC.
> Con người (bạn) chịu trách nhiệm làm rõ và chốt nội dung file này; Agent chịu trách nhiệm sinh code, test, tài liệu dựa trên đây.
> Mỗi mục kỹ thuật có kèm đoạn "Giải thích dễ hiểu" để dùng làm căn cứ review mà không cần đọc code.

---

## 0. Tổng quan — đọc mục này trước

### 0.1 Một câu về sản phẩm

Một **CLI tool** đọc source code Python/FastAPI (chỉ đọc cú pháp, không chạy code) và sinh ra tài liệu kiến trúc L3 + sơ đồ + graph, trong đó **mọi dòng đều tra ngược được về `file:line` trong source thật**.

### 0.2 Toàn bộ pipeline trong một hình

```
        thư mục source code (input)
                   │
    ┌──────────────▼──────────────┐
    │  [1] Scanner  →  [2] Parser │   liệt kê file .py, parse AST
    └──────────────┬──────────────┘   file lỗi cú pháp → bỏ qua, ghi nhận
                   │
    ┌──────────────▼──────────────────────────────┐
    │  [3] Extractors — 5 "chuyên viên" độc lập   │
    │   3a Route   3b Entity   3c ExternalCall    │   TẦNG
    │   3d CallGraph          3e Import           │   SỰ THẬT
    └──────────────┬──────────────────────────────┘   (không AI)
                   │
    ┌──────────────▼──────────────┐
    │  [4]  Model Builder         │   gộp thành IAM
    │  [4b] Cross-file Resolver   │   "tên này ở file nào?"
    │  [4c] Graph Builder         │   IAM → node/edge
    └──────────────┬──────────────┘
                   │
         IAM hoàn chỉnh (mục 5)
                   │
         ┌─────────┴─────────┐
         │                   │
    ┌────▼─────┐      ┌──────▼──────┐
    │[5] AI    │      │[6b] AI      │   TẦNG DIỄN GIẢI (có AI)
    │ Enrich   │      │  Reviewer   │   2 bước ĐỘC LẬP, cùng
    │ viết mô  │      │ gắn cờ nghi │   đọc IAM, không đọc
    │ tả       │      │ ngờ thiếu   │   output của nhau
    └────┬─────┘      └──────┬──────┘
         └─────────┬─────────┘
                   │
        ┌──────────▼──────────┐
        │  [6] Doc Generator  │
        └──────────┬──────────┘
                   │
        L3.md  +  diagram.mmd  +  graph.json  +  IAM.json
```

**Điều quan trọng nhất trong hình trên:** đường kẻ ngang giữa "tầng sự thật" và "tầng diễn giải". Mọi thứ phía trên là dữ liệu chứng minh được từ AST — cùng input và cấu hình phải cho cùng cấu trúc, quan hệ và ID (không tính thời điểm/thời lượng chạy). Mọi thứ phía dưới là lời văn do AI viết thêm — hữu ích để đọc, nhưng không bao giờ được phép sửa ngược lên tầng trên. Toàn bộ spec này tồn tại chủ yếu để bảo vệ ranh giới đó (chi tiết ở mục 3.1).

### 0.3 Ba khái niệm cần nắm trước

| Khái niệm | Là gì | Chi tiết ở |
|---|---|---|
| **IAM** (Intermediate Architecture Model) | Cấu trúc dữ liệu trung gian chứa mọi thứ tìm được: route, entity, external call, call graph. Mọi bước sau đều đọc từ đây, không đọc lại source. | mục 5 |
| **Reference** | Một lời gọi hàm/kế thừa class, kèm câu trả lời "nó trỏ tới file nào trong repo" — hoặc thừa nhận không resolve được. | mục 5, 6 (bước 4b) |
| **Confidence + Completeness** | Tách hai câu hỏi: dữ liệu được xác nhận trực tiếp hay suy ra (`exact`/`inferred`), và thuộc tính đã biết đủ hay mới biết một phần (`full`/`partial`). | mục 5.1 |

### 0.4 Muốn biết X thì đọc mục nào

| Câu hỏi | Mục |
|---|---|
| Tool này làm được gì, không làm được gì? | 2.1, 2.2 |
| Vì sao AI bị hạn chế chặt như vậy? | 3.1 |
| Dữ liệu đầu ra có cấu trúc thế nào? | 5, 5.1, 5.2 |
| Từng bước xử lý làm gì? | 6 |
| **Tôi sắp code một extractor, cần biết gì?** | **6c (bảng tra cứu gom sẵn)** |
| Thế nào là "làm xong"? | 8 (đặc biệt 8.5) |
| Chạy tool thế nào, có tùy chọn gì? | 4.2 |
| Lỗi thì tool xử lý ra sao? | 4.3 |
| Trình bày giá trị cho khách thế nào? | 5.3, 8.5.5 |
| Repo cần có những file gì? | 12 |
| Giao diện web gồm những màn nào? | 13 |
| Tool nhận biết repo dùng framework gì bằng cách nào? | 4.4 |
| Code tổ chức thư mục ra sao, thêm framework mới thế nào? | 14 |
| **Làm sao biết `svc.create` trỏ tới file nào?** | **15 (phần khó nhất)** |
| Làm theo thứ tự nào? | 9 |

### 0.5 Nguyên tắc bất biến (vi phạm = sai spec, không phải "tùy hoàn cảnh")

1. **Không bao giờ chạy code của repo đang phân tích** — chỉ đọc như văn bản (mục 3.2).
2. **AI không được thêm/sửa/xoá dữ liệu trong IAM** — chỉ được viết mô tả và gắn cờ cảnh báo (mục 3.1).
3. **Không đoán khi thiếu thông tin** — ghi vào `unresolved_references`, dùng `inferred`, hoặc hạ `completeness` xuống `partial`; không bịa cho đủ (mục 5.1).
4. **Mọi dòng trong tài liệu phải tra ngược được về `file:line`** (mục 7).
5. **Tầng static analysis không phụ thuộc tầng AI** — LLM hỏng thì output giảm chất lượng, không bao giờ mất (mục 4.3).
6. **Không có con số nào trong báo cáo mà không truy được về IAM, `RunMetrics`, `EVALUATION.md`, hoặc hệ số quy đổi được ghi rõ ngay cạnh con số** (mục 5.3).

---

## 1. Problem Statement

**Vấn đề:** Tài liệu kiến trúc mức chi tiết (L3 — mô tả module/class/API/DB bên trong một service) thường được viết tay lúc mới thiết kế, sau đó không ai cập nhật khi code thay đổi. Sau một thời gian, tài liệu và code thực tế lệch nhau, khiến tài liệu trở nên vô dụng hoặc gây hiểu lầm cho người đọc (dev mới, người review kiến trúc).

**Giải pháp:** Xây dựng công cụ tự động đọc source code (không chạy code, chỉ đọc cú pháp) và sinh ra tài liệu L3 + sơ đồ, sao cho tài liệu **luôn khớp với code thật tại thời điểm chạy công cụ**.

**Giải thích dễ hiểu:** Thay vì bắt con người nhớ cập nhật tài liệu mỗi khi sửa code (mà thực tế không ai làm), ta để máy đọc lại code mỗi lần cần và tự vẽ lại bức tranh — giống như chụp ảnh X-quang bộ máy thay vì tin vào bản vẽ tay từ 2 năm trước.

---

## 2. Phạm vi MVP (Scope)

### 2.1 Trong phạm vi (In-scope)

- Ngôn ngữ/framework **giai đoạn hiện tại**: Python 3.10+ với FastAPI.
- **Mục tiêu dài hạn là đa ngôn ngữ** (Flask, Django, Java/Spring). Kiến trúc và cấu trúc thư mục (mục 14) được thiết kế sẵn cho việc này ngay từ đầu; ma trận hỗ trợ ở mục 4.4.5.
- Service Discovery + Stack Detection: chia repo thành các đơn vị phân tích theo file manifest, nhận diện ngôn ngữ + framework cho **từng đơn vị** độc lập. Hỗ trợ repo đa ngôn ngữ/đa framework (ví dụ Java mobile + FastAPI AI service trong cùng một repo); đơn vị dùng stack chưa hỗ trợ thì bỏ qua riêng đơn vị đó và ghi rõ, không bỏ cả repo (mục 4.4).
- ORM: **SQLAlchemy** (declarative model, kế thừa `Base`/`declarative_base()`).
- HTTP client để phát hiện external call: **`httpx`** và **`requests`**.
- Cách khai báo route được nhận diện:
  - `@app.get/post/put/delete/patch(...)` trực tiếp trên instance `FastAPI()`.
  - `APIRouter()` + decorator tương ứng + `app.include_router(...)`.
- Dependency injection qua `Depends(...)`: nhận diện **có tồn tại**, không phân tích sâu logic bên trong hàm được inject.
- Input: một thư mục chứa source code (1 repo hoặc 1 service con trong monorepo).
- Output: 1 bộ tài liệu Markdown + 1 file Mermaid diagram + `graph.json` + `IAM.json` cho toàn bộ thư mục input.

- Cross-file resolution: theo dõi `import` để biết một lời gọi hàm/kế thừa class trỏ tới **file/module nào khác trong cùng repo**, không chỉ ghi tên chuỗi như bản đầu.
- Repository Knowledge Graph: xuất thêm 1 file `graph.json` (node/edge có cấu trúc) bên cạnh Markdown + Mermaid, làm nền tảng dữ liệu chứng minh được cho các bước sau (không thay thế Mermaid, chỉ bổ sung).
- AI Reviewer: một bước AI **thứ hai**, tách biệt AI Enrichment, chuyên phát hiện và gắn cờ chỗ nghi ngờ thiếu sót trong IAM (xem mục 6b).
- Confidence + Completeness: mỗi route/entity/external call ghi riêng mức bằng chứng (`exact`/`inferred`) và độ đầy đủ (`full`/`partial`) để không trộn lẫn “biết chắc” với “biết đủ” (xem mục 5.1).
- Evaluation: đo precision/recall trên 1 repo open-source thật với ground truth do người đọc tay, kết quả commit thành `EVALUATION.md` (xem mục 8.5).
- CLI hoàn chỉnh + xử lý lỗi mức "chạy được trước mặt người khác" (mục 4.2, 4.3).
- Value Metrics: tool tự báo cáo quy mô đã phân tích và ước tính công sức tương đương, có ghi rõ giả định (mục 5.3).
- Đóng gói cài được bằng `pip install` + `README.md` + thư mục `examples/` (mục 12).
- **Web UI (phần mở rộng)**: giao diện tĩnh đọc kết quả đã sinh, dùng để xem trực quan và trình bày. Là lớp phủ lên trên, xoá đi thì CLI vẫn chạy nguyên vẹn (mục 13).

### 2.2 Ngoài phạm vi (Out-of-scope cho MVP — ghi rõ để không bị hiểu nhầm là thiếu sót)

- Các ORM khác (Tortoise, raw SQL, Django ORM).
- Message queue/event (Celery, Kafka, RabbitMQ) — để lại cho phiên bản sau.
- Phân tích sâu bên trong hàm được `Depends(...)` (ví dụ logic chọn DB theo tenant).
- Đa ngôn ngữ/đa framework khác ngoài Python+FastAPI **trong giai đoạn hiện tại** — kiến trúc đã chuẩn bị sẵn (mục 14), nhưng extractor cho Flask/Django/Spring chưa được viết. Tool phải báo rõ khi gặp các stack này, không im lặng trả về rỗng.
- Phân tích code chạy động (dynamic analysis) — chỉ dùng static AST.
- Tự động cập nhật liên tục (CI integration) — MVP chạy thủ công qua CLI.
- Incremental re-scan / cache: mỗi lần chạy vẫn quét lại toàn bộ repo từ đầu — không tối ưu cho lần chạy tiếp theo.
- Hardened ingestion (đọc đầu vào không tin cậy với giới hạn tài nguyên, archive, symlink và file kích thước bất thường): chưa thuộc MVP. MVP chỉ nhận thư mục source local đáng tin cậy; giới hạn tài nguyên chi tiết để giai đoạn sau.
- Import bên ngoài repo (thư viện thứ 3, stdlib) không được resolve xuyên file — chỉ ghi nhận là "gọi ra ngoài phạm vi", theo đúng tinh thần `unresolved_references`.
- AI đề xuất extractor pattern mới hoặc AI tự sửa IAM — AI Reviewer (mục 6b) chỉ được **gắn cờ cảnh báo kèm evidence**, tuyệt đối không được thêm/sửa/xoá bất kỳ route/entity/quan hệ nào trong IAM.

**Giải thích dễ hiểu:** Đây là ranh giới "được làm tới đâu, chưa làm tới đâu" — bắt buộc phải nói rõ trước, để khi công cụ không nhận diện được raw SQL hay Celery, đó là **giới hạn đã biết trước**, không phải lỗi.

---

## 3. Nguyên tắc thiết kế bắt buộc

### 3.1 Ranh giới Deterministic vs AI (nguyên tắc quan trọng nhất của toàn bộ spec)

| Loại thông tin | Nguồn xác lập | Có được dùng AI không? |
|---|---|---|
| Route tồn tại, path, method | AST parsing | **Không** — bắt buộc từ static analysis |
| DB entity, tên bảng, cột, kiểu dữ liệu, FK | AST parsing | **Không** |
| Quan hệ gọi hàm/class (call graph) | AST parsing | **Không** |
| External API được gọi (URL, method) | AST parsing | **Không** |
| Cross-file resolution (import trỏ tới module/class/hàm nào) | AST parsing (đọc `import`/`from...import` như cú pháp, không `import` thật) | **Không** |
| Repository Knowledge Graph (node/edge) | Suy ra trực tiếp từ IAM đã có (không phát sinh dữ liệu mới) | **Không** |
| Confidence + Completeness của route/entity/external call | AST parsing (extractor biết dữ liệu là bằng chứng trực tiếp hay suy ra, và đã đọc đủ thuộc tính hay chưa) | **Không** — xem mục 5.1, quy tắc 3 |
| Mô tả bằng lời cho mỗi thành phần (1-2 câu) | AI (LLM) | Có — chỉ dùng cho phần này |
| Tổng hợp/tóm tắt cấp cao (ví dụ đoạn mở đầu tài liệu) | AI (LLM), dựa trên dữ liệu đã có từ AST | Có |
| Cảnh báo "nghi ngờ thiếu sót" (AI Reviewer) | AI (LLM), chỉ được suy luận trên dữ liệu đã có trong IAM, phải trỏ evidence cụ thể | Có — nhưng chỉ tạo cảnh báo mới, **không được sửa/thêm/xoá bất kỳ trường nào của IAM** |

**Quy tắc cứng:** AI **không bao giờ được phép tự thêm, tự sửa, hoặc tự suy luận** một route/entity/quan hệ nào không xuất hiện trong kết quả AST parsing. Nếu AST không phát hiện được, tài liệu phải ghi "không phát hiện được" hoặc liệt kê vào mục "known limitations" — không được để AI "đoán cho đủ".

**Giải thích dễ hiểu:** Hai loại thông tin phải tách bạch: *sự thật đo được* (đọc cú pháp code — ai đo cũng ra cùng kết quả) và *lời diễn giải* (caption cho bức ảnh — hữu ích, nhưng không phải bằng chứng). AI chỉ được viết caption, không được sửa nội dung bức ảnh, vì AI có thể đoán sai mà không tự biết mình sai (hiện tượng "ảo giác" — hallucination).

### 3.2 Nguyên tắc an toàn khi đọc code

Công cụ **chỉ được phép đọc cú pháp tĩnh** (parse bằng module `ast` của Python), **tuyệt đối không được**:
- `import` hoặc `exec()` bất kỳ file nào trong repo đang phân tích,
- chạy bất kỳ đoạn code nào của repo đó,
- tự chạy `pip install`, `poetry install`, build script hoặc công cụ cài dependency của repo mục tiêu.

**Giới hạn MVP:** chưa triển khai bộ giới hạn tài nguyên và cơ chế đọc archive/symlink cho đầu vào không tin cậy. MVP chỉ được công bố là chạy trên thư mục source local đáng tin cậy; không được ngầm quảng bá là đã được gia cố để nhận mọi repository lạ.

**Giải thích dễ hiểu:** Nếu công cụ "chạy thử" code để tìm hiểu cấu trúc (thay vì chỉ đọc chữ), mà code đó lỡ có đoạn tự động kết nối database thật hoặc gọi API thật ngay lúc được nạp vào bộ nhớ (import), công cụ tài liệu vô hại sẽ vô tình gây ra hành động thật ngoài ý muốn. Để tránh rủi ro này, công cụ chỉ được đọc file như đọc một văn bản, không được "bật" nó lên chạy.

**Lưu ý riêng cho cross-file resolution (mục 6, bước 4b):** "Resolve import" trong spec này nghĩa là đọc `ast.Import`/`ast.ImportFrom` như dữ liệu cú pháp (tên module, alias, `from X import Y`) rồi **so khớp bằng string/path với danh sách file đã quét**, tuyệt đối không phải là gọi `importlib.import_module(...)` hay Python `import` thật. Nếu quá trình so khớp không tìm được file tương ứng trong phạm vi repo (ví dụ import thư viện thứ 3), phải ghi vào `unresolved_references`, không được đoán.

### 3.3 Nguyên tắc gắn nhãn nguồn gốc trong output

Mọi thông tin trong tài liệu sinh ra phải được gắn nhãn ngầm định theo 3.1: người đọc phải phân biệt được đâu là dữ liệu đã chứng minh (AST), đâu là mô tả do AI viết thêm.

**Giải thích dễ hiểu:** Giống như trong báo cáo khoa học, phải phân biệt rõ "số liệu đo được" và "nhận định của người viết" — không được trộn lẫn khiến người đọc tưởng nhận định cũng là số liệu.

---

## 4. Input Contract & CLI

### 4.1 Input

```
Input: đường dẫn tới 1 thư mục chứa source code Python/FastAPI
Ví dụ: ./services/order-service/

Yêu cầu:
- Thư mục phải chứa ít nhất 1 file .py hợp lệ về cú pháp Python (parse được bằng ast.parse).
- Không yêu cầu cài đặt dependencies của repo đó (vì công cụ không import/chạy code).
- Nếu 1 file bị lỗi cú pháp (không parse được), công cụ phải:
  * Bỏ qua file đó,
  * Ghi rõ trong output là "file X bị bỏ qua do lỗi cú pháp",
  * Không được dừng toàn bộ quá trình vì 1 file lỗi.
```

**Giải thích dễ hiểu:** Công cụ không cần "cài đặt" dự án để chạy được (không cần các thư viện phụ thuộc thật) vì nó không chạy code, chỉ đọc chữ trong file — giống đọc một cuốn sách không cần phải là tác giả cuốn sách đó. Nếu gặp 1 trang sách rách (file lỗi), bỏ qua trang đó và đọc tiếp, không vứt cả cuốn sách.

### 4.2 CLI Contract

```bash
l3gen <đường-dẫn-source> [tùy chọn]    # phân tích và sinh tài liệu
l3gen ui <đường-dẫn-output>            # mở giao diện web xem kết quả (mục 13)
```

| Tùy chọn | Mặc định | Ý nghĩa |
|---|---|---|
| `-o, --output <dir>` | `./l3-output/` | Nơi ghi `L3.md`, `diagram.mmd`, `graph.json`, `IAM.json` |
| `--no-ai` | tắt | Chạy thuần static analysis, bỏ qua cả AI Enrichment lẫn AI Reviewer. Tài liệu vẫn sinh đầy đủ, chỉ thiếu cột "Mô tả" và mục "Review Findings" |
| `--exclude <pattern>` | `__pycache__`, `.venv`, `venv`, `tests` | Thư mục bỏ qua khi quét (lặp lại được nhiều lần) |
| `--fail-on-empty` | tắt | Thoát với mã lỗi nếu không tìm thấy route/entity nào — dùng khi chạy tự động |
| `-v, --verbose` | tắt | In tiến trình từng bước |
| `--version` | | In phiên bản |

**`--no-ai` là bắt buộc phải có từ sớm**, không phải tùy chọn thêm vào cuối: toàn bộ giai đoạn đầu của dự án (trước khi AI Enrichment tồn tại) đều cần chạy được pipeline mà không gọi LLM. Nó cũng là đường thoát khi demo mà không có mạng.

**Cấu hình LLM** đọc từ biến môi trường, theo thứ tự ưu tiên: `L3GEN_API_KEY` → `ANTHROPIC_API_KEY`. Nếu không có biến nào, xem mục 4.3.

**Exit code:** `0` thành công; `1` lỗi đầu vào (thư mục không tồn tại, không có file `.py`); `2` lỗi không mong đợi.

### 4.3 Xử lý lỗi — chuẩn "chạy được trước mặt người khác"

Tool có thể được chạy trong buổi demo hoặc bởi người chưa quen. Yêu cầu: **không bao giờ in Python traceback ra màn hình cho lỗi đã lường trước được.** Mọi thông báo phải nói rõ chuyện gì xảy ra và làm gì tiếp theo.

| Tình huống | Hành vi bắt buộc |
|---|---|
| Thư mục không tồn tại | Báo lỗi rõ ràng + exit 1. Không traceback. |
| Thư mục không có file `.py` nào | Báo "không tìm thấy file Python nào trong `<path>`" + exit 1 |
| **Không có API key** | **Không được crash.** Tự động chạy như `--no-ai`, in cảnh báo rõ: "Chưa cấu hình API key — đang chạy chế độ static analysis. Tài liệu sẽ không có mô tả AI." Tiếp tục sinh đầy đủ output. |
| Gọi LLM thất bại (mạng, rate limit, timeout) | Retry tối đa 2 lần. Vẫn hỏng → tiếp tục pipeline không có phần AI đó, ghi vào Known Limitations. **Không mất toàn bộ kết quả static analysis chỉ vì LLM hỏng.** |
| File lỗi cú pháp | Bỏ qua, ghi `parse_errors`, chạy tiếp (mục 4.1) |
| Không tìm thấy route/entity nào | Vẫn sinh tài liệu (ghi rõ "không phát hiện được"), exit 0 — trừ khi có `--fail-on-empty` |

**Nguyên tắc bao trùm:** tầng static analysis không được phụ thuộc vào tầng AI. Mọi hỏng hóc ở phần LLM chỉ làm **giảm** chất lượng output, không bao giờ làm **mất** output.

**Giải thích dễ hiểu:** Hãy tưởng tượng máy in bị hết mực màu. Máy tốt sẽ in tiếp bằng mực đen và báo "đã hết mực màu"; máy tệ thì từ chối in cả trang. Tool này phải là loại thứ nhất — phần AI hỏng thì tài liệu vẫn ra, chỉ thiếu phần mô tả, và nói rõ là đang thiếu.

### 4.4 Service Discovery & Stack Detection

Trước khi trích xuất bất cứ thứ gì, tool phải trả lời hai câu hỏi theo đúng thứ tự:

1. **Repo này gồm mấy đơn vị phân tích?** (một service, hay nhiều service trong monorepo)
2. **Mỗi đơn vị viết bằng gì?**

Câu hỏi thứ nhất dễ bị bỏ qua, và bỏ qua nó dẫn tới sai lầm nghiêm trọng. Ví dụ thực tế: một hệ thống có ứng dụng mobile viết bằng Java và một AI service viết bằng FastAPI, giao tiếp qua REST. Nếu coi cả repo là **một** stack rồi chọn theo số file chiếm đa số, tool sẽ kết luận "đây là project Java" và **bỏ qua hoàn toàn** service FastAPI — im lặng, không cảnh báo. Đó là kiểu thất bại tệ nhất: người dùng không biết mình đang thiếu gì.

#### 4.4.1 Đơn vị phân tích là "service", không phải "repo"

```
repo/                          ← KHÔNG phải đơn vị phân tích
├── mobile-app/
│   ├── pom.xml                ← manifest → đơn vị #1: Java + Spring
│   └── src/main/java/...
├── ai-service/
│   ├── requirements.txt       ← manifest → đơn vị #2: Python + FastAPI
│   └── app/main.py
└── docs/                      ← không manifest, không source → bỏ qua
```

Mỗi đơn vị được nhận diện, parse và trích xuất **hoàn toàn độc lập**. Kết quả gộp lại thành một IAM chung, nhưng mỗi thực thể đều biết nó thuộc service nào.

#### 4.4.2 Cách xác định ranh giới service

Duyệt cây thư mục, đánh dấu mọi thư mục chứa **file manifest**:

| Manifest | Ngôn ngữ |
|---|---|
| `requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.py` | Python |
| `pom.xml`, `build.gradle`, `build.gradle.kts` | Java |
| `package.json` | JavaScript/TypeScript |
| `go.mod` | Go |

**Quy tắc:**
1. Mỗi thư mục có manifest → một đơn vị phân tích. Phạm vi của nó là thư mục đó và toàn bộ thư mục con, **trừ** phần thuộc về một manifest lồng bên trong.
2. Manifest lồng nhau → đơn vị con thắng. Ví dụ `repo/pom.xml` và `repo/service-a/pom.xml` thì `service-a/` là đơn vị riêng, `repo/pom.xml` chỉ quản phần còn lại.
3. **Không tìm thấy manifest nào** → coi toàn bộ thư mục đầu vào là một đơn vị duy nhất, nhận diện ngôn ngữ theo phần mở rộng file. Ghi `confidence = exact`, `completeness = partial` với lý do "không tìm thấy file khai báo phụ thuộc" — ngôn ngữ được đọc trực tiếp từ phần mở rộng, nhưng bằng chứng nhận diện stack chưa đầy đủ.
4. Thư mục không có source code (chỉ `docs/`, `assets/`...) → không phải đơn vị, bỏ qua im lặng.

**Vì sao dựa vào manifest thay vì đếm file:** manifest là **tuyên bố tường minh của người viết code** rằng "đây là một đơn vị triển khai độc lập". Đếm tỷ lệ file chỉ là suy đoán thống kê — và suy đoán đó sai ngay khi một service nhỏ nằm cạnh một service lớn.

#### 4.4.3 Nhận diện ngôn ngữ của một đơn vị

Trong phạm vi một đơn vị, ngôn ngữ suy ra từ loại manifest (quy tắc 1-2) — không cần đếm file. Chỉ khi rơi vào quy tắc 3 (không manifest) mới đếm phần mở rộng file và lấy ngôn ngữ chiếm đa số.

Đơn vị có nhiều ngôn ngữ lẫn lộn (ví dụ Python kèm vài script `.sh`): chỉ file của ngôn ngữ chính đi vào `files_found`; phần mở rộng khác nằm ngoài phạm vi parser của đơn vị và không được coi là lỗi cú pháp. Tài liệu phải luôn nêu ngôn ngữ đã phân tích để người đọc không hiểu nhầm phạm vi.

#### 4.4.4 Nhận diện framework của một đơn vị

Hai nguồn bằng chứng độc lập, xét **trong phạm vi đơn vị đó**:

**Nguồn 1 — nội dung manifest:**

| Framework | Dấu hiệu |
|---|---|
| FastAPI | `fastapi` trong requirements/pyproject |
| Flask | `flask` |
| Django | `django` |
| Spring Boot | `spring-boot-starter-web`, `org.springframework` trong pom/gradle |

**Nguồn 2 — câu lệnh import trong source của đơn vị:**

| Framework | Dấu hiệu |
|---|---|
| FastAPI | `from fastapi import ...`, `FastAPI()`, `APIRouter()` |
| Flask | `from flask import ...`, `Flask(__name__)`, `Blueprint(...)` |
| Django | `from django...`, có `urls.py` + `settings.py` |
| Spring Boot | `org.springframework.*`, `@SpringBootApplication`, `@RestController` |

**Quy tắc kết luận:**

| Manifest | Import | Kết luận |
|---|---|---|
| Có | Có | Framework đó, `confidence = exact`, `completeness = full` |
| Không | Có | Framework đó, `confidence = exact`, `completeness = partial` — "không có khai báo phụ thuộc" |
| Có | Không | Framework đó, `confidence = exact`, `completeness = partial` — "có khai báo nhưng chưa thấy dùng trong source" |
| Không | Không | Không kết luận được → đơn vị này bị bỏ qua, ghi rõ lý do |

**Một đơn vị dùng nhiều framework** (ví dụ FastAPI cho API + Django cho trang admin, cùng một service): ghi nhận tất cả, chạy extractor của từng cái. Đây khác với **nhiều đơn vị mỗi cái một framework** — trường hợp sau đã xử lý ở 4.4.2.

#### 4.4.5 Ma trận hỗ trợ

Ngôn ngữ và framework là hai trục độc lập:

| Ngôn ngữ | Parser | Trạng thái |
|---|---|---|
| Python | `ast` (thư viện chuẩn) | **Hỗ trợ** |
| Java | `tree-sitter` / `javalang` | Dự kiến |

| Framework | Ngôn ngữ | ORM đi kèm | Trạng thái |
|---|---|---|---|
| FastAPI | Python | SQLAlchemy | **Hỗ trợ đầy đủ — phạm vi hiện tại** |
| Flask | Python | SQLAlchemy | Dự kiến |
| Django | Python | Django ORM | Dự kiến |
| Spring Boot | Java | JPA/Hibernate | Dự kiến |

**Hai loại mở rộng, khối lượng khác hẳn nhau:**

- **Framework mới, ngôn ngữ đã có** (Flask, Django): dùng lại toàn bộ parser `ast`, `Reference`, cross-file resolver, quy tắc confidence/completeness và graph builder. Chỉ viết bộ rule nhận diện pattern. Đây thực sự chủ yếu là rule/mapping.
- **Ngôn ngữ mới** (Java): `ast` chỉ đọc được Python. Cần thư viện parse riêng, cây cú pháp hình dạng khác hẳn, phải viết lớp ánh xạ về IAM. Thêm nữa cross-file resolver hiện resolve theo module path kiểu Python — Java dùng package/classpath, cần xử lý riêng. Tầng trên IAM dùng lại được, tầng parser thì không.

#### 4.4.6 Hành vi khi gặp đơn vị chưa hỗ trợ

**Nguyên tắc: bỏ qua đơn vị đó, không bỏ qua cả repo.**

Ví dụ với hệ thống Java mobile + FastAPI AI service, khi mới chỉ hỗ trợ FastAPI:

```
Phát hiện 2 đơn vị phân tích:

  [v] ai-service/        Python + FastAPI       -> sẽ phân tích
  [x] mobile-app/        Java + Spring Boot     -> BỎ QUA (chưa hỗ trợ)

Đang phân tích 1/2 đơn vị...

[kết quả của ai-service]

Cảnh báo: 1 đơn vị bị bỏ qua. Tài liệu này KHÔNG bao gồm mobile-app/.
Xem mục "Known Limitations" để biết chi tiết.
```

Trường hợp **mọi đơn vị đều chưa hỗ trợ** → dừng, exit 1, liệt kê từng đơn vị kèm stack đã phát hiện và stack đang được hỗ trợ.

Trường hợp **không tìm thấy đơn vị nào** (không manifest, không source) → dừng, exit 1, báo rõ đã quét những thư mục nào.

#### 4.4.7 Ghi vào IAM

```python
class ServiceUnit(BaseModel):
    # Một đơn vị phân tích — thường là một service triển khai độc lập.
    name: str                      # tên thư mục, ví dụ "ai-service"
    root_path: str                 # đường dẫn tương đối từ thư mục đầu vào
    manifest_file: str | None      # "requirements.txt"; None nếu suy ra từ file
    language: str                  # "python"
    frameworks: list[str]          # ["fastapi"]
    orm: str | None                # "sqlalchemy"
    confidence: Confidence
    completeness: Completeness
    detection_reason: str          # "fastapi trong requirements.txt + import ở 12 file"
    file_count: int
    analyzed: bool                 # False nếu bị bỏ qua do chưa hỗ trợ
    skip_reason: str | None        # "Java + Spring Boot chưa được hỗ trợ"

class DetectedStack(BaseModel):
    services: list[ServiceUnit]    # TẤT CẢ đơn vị tìm thấy, kể cả bị bỏ qua
    analyzed_count: int
    skipped_count: int
```

**Mọi thực thể trong IAM phải mang trường `service` chỉ rõ nó thuộc đơn vị nào** — nếu không, một repo hai service sẽ trộn lẫn route của cả hai mà không phân biệt được.

Cụ thể, thêm vào các model đã có ở mục 5: `APIRoute.service`, `DBEntity.service`, `ExternalCall.service`, `FunctionNode.service`.

#### 4.4.8 Vì sao điều này quan trọng hơn vẻ ngoài của nó

Kiến trúc microservice là chuẩn mực phổ biến, và gần như mọi hệ thống thật đều có ít nhất hai stack khác nhau. Một công cụ chỉ chấp nhận "một repo = một framework" sẽ dùng được cho project mẫu nhưng vô dụng với hệ thống thật.

Quan trọng hơn: khi tool bỏ qua một service mà **không nói ra**, nó tạo ra tài liệu trông có vẻ đầy đủ nhưng thực chất khuyết một mảng, và người đọc không có cách nào biết. Điều này vi phạm trực tiếp nguyên tắc nền tảng của cả spec (mục 3.3: người đọc phải luôn biết tài liệu đáng tin tới đâu).

**Giải thích dễ hiểu:** Giống như một người kiểm định toà nhà. Nếu anh ta chỉ kiểm tra tầng 1 rồi viết "toà nhà an toàn" mà không ghi rõ mình chưa lên các tầng trên, bản báo cáo đó nguy hiểm hơn là không có báo cáo — vì nó tạo cảm giác yên tâm sai. Bước này buộc tool phải liệt kê đủ "toà nhà có mấy tầng", kiểm tầng nào, bỏ tầng nào và vì sao.

---

## 5. Output Contract — Intermediate Architecture Model (IAM)

Đây là cấu trúc dữ liệu trung gian mà mọi bước xử lý phải tạo ra **trước khi** sinh tài liệu Markdown. Định nghĩa bằng Pydantic model.

```python
from datetime import datetime
from pydantic import BaseModel
from typing import Literal

class SourceLocation(BaseModel):
    file: str          # đường dẫn tương đối trong repo
    line_start: int
    line_end: int

Confidence = Literal["exact", "inferred"]
"""Nguồn bằng chứng: đọc trực tiếp được từ cú pháp, hay suy ra từ một pattern
đã được đặc tả. Xem mục 5.1 — KHÔNG được gán theo cảm tính."""

Completeness = Literal["full", "partial"]
"""Độ đầy đủ của thuộc tính: đã biết đủ, hay còn phần phụ thuộc runtime."""

class Reference(BaseModel):
    """Một tham chiếu tới function/class khác, đã cố gắng resolve xuyên file.
    Đây là điểm khác biệt so với bản MVP đầu (trước đây chỉ lưu tên chuỗi trần)."""
    name: str                      # tên như xuất hiện trong code, ví dụ "OrderService.create_order"
    resolved_module: str | None    # đường dẫn file trong repo nếu resolve được, ví dụ "services/order_service.py"
    resolved: bool                 # True nếu tìm thấy định nghĩa trong phạm vi repo đang quét
    confidence: Confidence | None  # None nếu unresolved; exact hoặc inferred nếu đã chọn được đích
    completeness: Completeness     # partial nếu chỉ xác định được một phần tham chiếu
    reason: str | None             # bắt buộc nếu inferred, partial hoặc unresolved

class APIRoute(BaseModel):
    service: str                   # tên ServiceUnit chứa route này (mục 4.4.7)
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
    path: str                      # ví dụ "/orders/{order_id}"; nếu có phần không phải literal,
                                   # giữ nguyên biểu thức, ví dụ "{settings.API_PREFIX}/orders"
    handler_function: str          # tên hàm xử lý
    calls: list[Reference]         # function/class được gọi bên trong handler, đã cố resolve xuyên file
    confidence: Confidence         # xem mục 5.1
    completeness: Completeness     # xem mục 5.1
    reason: str | None             # BẮT BUỘC nếu inferred hoặc partial
    location: SourceLocation

class DBColumn(BaseModel):
    name: str
    type: str                      # kiểu dữ liệu, ví dụ "Integer", "String"
    is_primary_key: bool
    foreign_key_ref: str | None    # ví dụ "customers.id", None nếu không phải FK

class DBEntity(BaseModel):
    service: str                   # tên ServiceUnit chứa entity này
    class_name: str
    table_name: str
    columns: list[DBColumn]
    base_class: Reference | None   # class cha (declarative_base/Base hoặc class trung gian), resolve xuyên file
    confidence: Confidence         # xem mục 5.1
    completeness: Completeness     # xem mục 5.1
    reason: str | None             # BẮT BUỘC nếu inferred hoặc partial
    location: SourceLocation

class ExternalCall(BaseModel):
    service: str                   # tên ServiceUnit chứa lời gọi này
    caller_function: str
    url_or_host: str               # có thể là URL literal hoặc biến (ghi rõ nếu là biến, không suy đoán giá trị)
    http_method: str | None
    confidence: Confidence         # xem mục 5.1
    completeness: Completeness     # xem mục 5.1
    reason: str | None             # BẮT BUỘC nếu inferred hoặc partial
    location: SourceLocation

class FunctionNode(BaseModel):
    service: str                   # tên ServiceUnit chứa hàm này
    name: str
    class_name: str | None         # None nếu là hàm tự do, không thuộc class nào
    module: str                    # đường dẫn file chứa hàm này, ví dụ "services/order_service.py"
    calls: list[Reference]         # function/method khác được gọi trực tiếp bên trong, đã cố resolve xuyên file
    location: SourceLocation

class UnresolvedReference(BaseModel):
    """Trường hợp phát hiện có tham chiếu nhưng không xác định được đích
    (ví dụ FK trỏ tới bảng không có trong phạm vi thư mục đang quét,
    hoặc import không tìm thấy module tương ứng trong repo)."""
    description: str
    location: SourceLocation

class ParseError(BaseModel):
    file: str
    error_message: str

class RunMetrics(BaseModel):
    """Số liệu về chính lần chạy này. Dùng cho mục "Tổng quan" của tài liệu
    và để trả lời câu hỏi "tool tiết kiệm được gì" (xem mục 5.3)."""
    scanned_at: datetime
    files_found: int               # file source thuộc service được phân tích, sau --exclude
    files_analyzed: int            # parse và đưa vào phân tích thành công
    files_skipped: int             # file thuộc phạm vi nhưng không phân tích được, ví dụ lỗi cú pháp
    is_partial: bool               # có file parse lỗi hoặc có ServiceUnit bị bỏ qua
    lines_of_code: int             # tổng số dòng đã đọc qua
    duration_seconds: float
    ai_enabled: bool               # False nếu chạy --no-ai hoặc thiếu API key
    tool_version: str

class IntermediateArchitectureModel(BaseModel):
    detected_stack: DetectedStack  # kết quả bước 1b, xem mục 4.4.7
    routes: list[APIRoute]
    entities: list[DBEntity]
    external_calls: list[ExternalCall]
    functions: list[FunctionNode]
    unresolved_references: list[UnresolvedReference]
    parse_errors: list[ParseError]
    metrics: RunMetrics
```

**Coverage tối giản trong `RunMetrics`:** không tạo thêm model hoặc ma trận theo từng khả năng. Scanner chỉ đếm file source thuộc các service được chọn để phân tích, sau khi áp dụng `--exclude`; parser tăng `files_analyzed` khi parse thành công; file lỗi làm tăng `files_skipped` và đã có chi tiết trong `parse_errors`. Service bị bỏ qua đã có `ServiceUnit.analyzed = False` và `skip_reason`. `is_partial` chỉ là cờ tổng hợp từ các số liệu này, không có logic suy đoán riêng.

Các bất biến phải kiểm tra bằng test:

```text
files_found = files_analyzed + files_skipped
len(detected_stack.services) = detected_stack.analyzed_count + detected_stack.skipped_count
is_partial = (files_skipped > 0) hoặc (detected_stack.skipped_count > 0)
```

File thuộc service chưa được hỗ trợ cũng không nằm trong `files_found`; phần thiếu đó đã được phản ánh bằng `DetectedStack.analyzed_count/skipped_count`. File do người dùng chủ động loại bằng `--exclude` không nằm trong `files_found`, vì nó không thuộc phạm vi lần chạy. Cách này tránh đếm hai lần và tránh việc một repo có thư mục `tests/` hoặc `.venv/` luôn bị báo `is_partial = true`.

**Giải thích dễ hiểu:** Trước khi vẽ tranh (tài liệu Markdown), hoạ sĩ phải lập danh sách chi tiết: có ai trong tranh, đứng ở đâu, nhìn ai. Tách riêng "lập danh sách" (IAM) và "vẽ tranh" cho phép kiểm tra hai việc độc lập: danh sách có đúng không, và tranh có vẽ đúng danh sách không (không tự thêm người ngoài danh sách).

**Về `Reference` (mới):** Ở bản MVP đầu, `calls: list[str]` chỉ lưu tên chuỗi trần (ví dụ `"create_order"`), không biết hàm đó định nghĩa ở đâu nếu nó nằm ở file khác — đây chính là giới hạn cần nâng cấp. `Reference` buộc extractor phải trả lời rõ: "tên này resolve được tới file nào trong repo, hay không resolve được" — không được im lặng bỏ qua câu hỏi đó.

### 5.1 Confidence và Completeness — định nghĩa và quy tắc gán

Static analysis có hai loại giới hạn khác nhau, không được trộn thành một nhãn:

1. **Độ chắc chắn (`confidence`)**: kết luận được đọc trực tiếp từ cú pháp hay được suy ra từ một pattern?
2. **Độ đầy đủ (`completeness`)**: các thuộc tính của kết luận đã biết đủ hay còn phần phụ thuộc runtime?

Ví dụ `@app.get(f"{settings.PREFIX}/orders")` chứng minh trực tiếp rằng route tồn tại, nên `confidence = "exact"`; nhưng tool không biết giá trị thật của prefix, nên `completeness = "partial"`.

**Confidence:**

| Mức | Định nghĩa | Ví dụ điển hình |
|---|---|---|
| `exact` | Sự tồn tại của thực thể hoặc đích tham chiếu được xác nhận bằng cú pháp/import/type trực tiếp. | `@app.get(...)`, `__tablename__ = ...`, hoặc class được xác định từ `svc = OrderService()`. |
| `inferred` | Kết luận được suy ra từ một pattern đã ghi rõ trong spec; có khả năng sai cao hơn `exact`. | Route được tạo qua factory đã có rule tường minh, hoặc chọn method đầu tiên theo quy tắc đa kế thừa đơn giản hoá. |

**Completeness:**

| Mức | Định nghĩa | Ví dụ điển hình |
|---|---|---|
| `full` | Các thuộc tính cần xuất đã đọc được đầy đủ. | Route path là literal `"/orders"`; `__tablename__ = "orders"`. |
| `partial` | Thực thể chắc chắn tồn tại nhưng một hoặc nhiều thuộc tính chưa biết đầy đủ. | Prefix route là biến config; URL có host lấy từ biến; tên bảng ghép từ hằng số chưa resolve được giá trị. |

**Quy tắc gán (cứng, không được diễn giải lỏng):**

1. Mặc định là `confidence = "exact"`, `completeness = "full"`.
2. `reason` bắt buộc có giá trị khi `confidence = "inferred"`, `completeness = "partial"`, hoặc `Reference.resolved = False`. Lý do phải nêu *cái gì* chưa biết hoặc đã suy theo rule nào. Đạt: `"prefix từ biến settings.API_PREFIX, không resolve được giá trị"`. Không đạt: `"không chắc chắn"`.
3. Không được dùng AI để gán hai trường này. Extractor/resolver gán từ bằng chứng static.
4. `inferred` chỉ được dùng cho pattern đã ghi trong spec. Pattern chưa được đặc tả phải bỏ qua hoặc ghi `unresolved_references`, không tự suy đoán cho đủ.
5. Confidence và completeness không lan truyền giữa các thực thể. Một route có `completeness = "partial"` gọi một function không làm function đó tự động thành `partial`.
6. `Reference.resolved` trả lời một câu hỏi riêng: có tìm được đích trong repo hay không. Nếu `resolved = False`, `confidence = None`, `completeness = "partial"` và phải có `reason`.

**Giải thích dễ hiểu:** Một nhãn sản phẩm có thể đọc rất rõ nhưng bị thiếu nửa dòng. “Đọc rõ” là độ chắc chắn; “thiếu nửa dòng” là độ đầy đủ. Vì vậy trường hợp này phải là `exact + partial`, không thể ép vào một nhãn duy nhất. Tách hai trường giúp người đọc biết tool đang **đoán** hay chỉ đang **thiếu một phần giá trị**.

**Vì sao điều này quan trọng với dự án:** nếu chỉ có một nhãn, route có prefix động dễ bị hiểu là bản thân route không chắc tồn tại. Hai trường riêng cho phép nói chính xác hơn: route có thật, nhưng path chưa đầy đủ.

---

### 5.2 Repository Knowledge Graph (output phụ, suy ra từ IAM)

Graph không phải là nguồn dữ liệu mới — nó là một **view khác** của cùng IAM đã có ở mục 5, chuyển từ dạng bảng sang dạng node/edge. Không được thêm bất kỳ thông tin nào vào graph mà không có nguồn gốc trực tiếp từ IAM.

```python
class GraphNode(BaseModel):
    id: str                        # duy nhất và ổn định; quy tắc ngay bên dưới
    type: Literal["Module", "Class", "Function", "Route", "Entity", "ExternalHost", "Unresolved"]
    label: str                     # tên hiển thị, ví dụ "OrderService"
    location: SourceLocation | None

class GraphEdge(BaseModel):
    source_id: str
    target_id: str
    type: Literal["calls", "imports", "inherits", "exposes", "reads_writes", "calls_external"]
    resolved: bool                 # False nếu target chỉ suy ra được tên, không resolve được file (tương ứng Reference.resolved = False)

class RepositoryKnowledgeGraph(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]
```

**Quy tắc xây dựng graph:** Graph Builder (bước 4c trong pipeline, mục 6) chỉ được đọc IAM đã hoàn chỉnh (sau Model Builder) để sinh `nodes`/`edges` — không được tự phân tích lại source code, không được dùng AI. Mỗi edge phải trace ngược được về đúng 1 field cụ thể trong IAM (ví dụ edge `calls` giữa 2 Function tương ứng đúng 1 phần tử trong `FunctionNode.calls`). Reference chưa resolve vẫn được giữ bằng node `Unresolved` tại vị trí phát hiện và edge có `resolved = False`; không được âm thầm loại khỏi graph.

**Quy tắc ID ổn định (bắt buộc):** ID là chuỗi dễ đọc, tạo từ dữ liệu đã có; không dùng số tự tăng của database, thứ tự duyệt AST, timestamp hoặc giá trị ngẫu nhiên.

| Loại node | Dạng ID |
|---|---|
| Module | `module:<service>:<relative-path>` |
| Class | `class:<service>:<relative-path>:<qualified-name>` |
| Function | `function:<service>:<relative-path>:<qualified-name>` |
| Route | `route:<service>:<relative-path>:<METHOD>:<normalized-path>:<qualified-handler>` |
| Entity | `entity:<service>:<relative-path>:<class-name>` |
| ExternalHost | `external:<service>:<host-or-expression>` |
| Đích chưa resolve | `unresolved:<service>:<relative-path>:<line-start>:<raw-name>` |

Trong các mẫu trên, `<service>` là `ServiceUnit.root_path` đã chuẩn hoá, không phải tên hiển thị có thể bị trùng. Chuẩn hoá mọi đường dẫn sang dấu `/`; `qualified-name` bao gồm class cha nếu có, ví dụ `OrderService.create_order`. Nếu hai node vẫn tạo cùng ID, đó là lỗi dữ liệu phải báo trong test, không được tự nối thêm số phụ thuộc thứ tự duyệt.

`GraphEdge` không cần ID riêng trong MVP. Một edge được xác định ổn định bằng bộ ba `(source_id, type, target_id)`. Trước khi ghi `graph.json`, sắp `nodes` theo `id` và `edges` theo `(source_id, type, target_id)`; edge trùng hoàn toàn được gộp một lần. Vì vậy cùng IAM phải sinh cùng graph theo đúng thứ tự.

**Giải thích dễ hiểu:** Nếu IAM ở mục 5 giống một "bảng thống kê" (liệt kê route, entity, hàm...), thì Repository Knowledge Graph là "bản đồ" vẽ lại đúng những thông tin đó theo dạng nút và đường nối — hữu ích khi cần trả lời nhanh kiểu "hàm A gọi tới những gì" bằng cách duyệt đồ thị, thay vì đọc lướt cả bảng. Vì graph chỉ là cách trình bày khác của cùng dữ liệu, nó không được phép "biết" điều gì mà IAM không biết.

### 5.3 Value Metrics — trình bày giá trị mà không bịa số

Tài liệu sinh ra cần trả lời được câu hỏi của người đọc không viết code: *"cái này giúp tôi tiết kiệm được gì?"*. Nhưng đây chính là chỗ dễ trượt vào số liệu vô căn cứ nhất, nên spec quy định rõ ranh giới.

**Được phép in (đo trực tiếp, từ IAM và `RunMetrics`):**

```
Đã phân tích 47/49 file Python (8.432 dòng) trong 18,3 giây; 2 file lỗi cú pháp đã được ghi rõ.
Phát hiện: 23 API route, 11 DB entity, 6 external dependency.
Mức bằng chứng: 39 exact, 1 inferred.
Độ đầy đủ: 36 full, 4 partial.
```

**Được phép in kèm giả định ghi rõ (quy đổi công sức):**

```
Ước tính công sức tương đương nếu viết tay: ~1,5–2 ngày công.
(Giả định: 15–20 phút cho mỗi route/entity để đọc code, viết mô tả và vẽ sơ đồ.
 Đây là ước tính theo hệ số cố định, không phải số đo thực nghiệm.)
```

**Quy tắc cứng cho phần quy đổi:**
1. **Luôn kèm giả định ngay cạnh con số**, không tách xuống footnote. Người đọc phải thấy ngay đây là ước tính.
2. **Dùng khoảng, không dùng số đơn lẻ.** "~1,5–2 ngày" chứ không phải "1,7 ngày" — độ chính xác giả tạo làm mất uy tín cả báo cáo.
3. **Hệ số quy đổi là hằng số cấu hình được, ghi rõ trong tài liệu.** Không được để AI sinh ra hệ số này.
4. **Không quy đổi ra tiền.** Tool không biết mức lương, và một con số tiền sai sẽ phá hỏng độ tin cậy của mọi số liệu khác trong báo cáo.

**Nghiêm cấm:** so sánh với sản phẩm khác, phát biểu kiểu "chính xác 99%" nếu không có số đo từ mục 8.5, hoặc bất kỳ con số nào không truy được về IAM, `RunMetrics`, `EVALUATION.md` hay hệ số quy đổi đã ghi rõ ngay cạnh nó.

**Giải thích dễ hiểu:** Một báo cáo nói "tiết kiệm 80% thời gian" mà không nói đo thế nào sẽ bị người nghe kỹ tính bác bỏ ngay, và kéo theo nghi ngờ toàn bộ phần còn lại. Ngược lại, "phân tích 47 file trong 18 giây; ước tính 1,5–2 ngày công nếu làm tay, giả định 15–20 phút mỗi thành phần" là phát biểu mà người nghe có thể tự kiểm chứng — và chính sự kiểm chứng được đó mới tạo ra niềm tin. Thà đưa con số khiêm tốn có cơ sở còn hơn con số ấn tượng không ai kiểm được.

---

## 6. Kiến trúc xử lý (Pipeline)

```
[1] Repo Scanner
     → Duyệt thư mục, lọc ra danh sách file source cần xử lý
     → Bỏ qua: __pycache__, .venv, venv, tests/, target/, build/ (có thể cấu hình)

[1b] Service Discovery + Stack Detection (xem mục 4.4)
     → CHIA repo thành các ĐƠN VỊ PHÂN TÍCH ("service"), mỗi đơn vị là một
       thư mục có file manifest riêng (requirements.txt, pom.xml, package.json...)
       · repo một service   → 1 đơn vị (chính là thư mục gốc)
       · monorepo nhiều svc → N đơn vị, mỗi service một đơn vị
     → Với TỪNG đơn vị, nhận diện độc lập: ngôn ngữ + framework + ORM
     → Một repo CÓ THỂ chứa nhiều ngôn ngữ/framework khác nhau — đây là
       trường hợp BÌNH THƯỜNG, không phải lỗi
     → Đơn vị nào dùng stack chưa hỗ trợ → BỎ QUA ĐƠN VỊ ĐÓ, ghi vào
       skipped_services, VẪN TIẾP TỤC phân tích các đơn vị còn lại

[2] Parser (chạy riêng cho từng đơn vị, theo ngôn ngữ của đơn vị đó)
     → Python: module `ast` chuẩn
     → Ngôn ngữ khác: parser riêng của ngôn ngữ đó (xem mục 4.4.5)
     → nếu lỗi cú pháp → ghi vào parse_errors, bỏ qua file, tiếp tục

[3] Pattern Extractors (chạy độc lập trên từng file đã parse)
     3a. RouteExtractor        → tìm decorator @app.get/post/... và APIRouter
     3b. EntityExtractor       → tìm class kế thừa Base/declarative_base
     3c. ExternalCallExtractor → tìm lời gọi httpx.Client()/requests.get/post...
     3d. CallGraphExtractor    → tìm lời gọi hàm/method bên trong mỗi function
     3e. ImportExtractor       → đọc ast.Import/ast.ImportFrom của mỗi file,
                                  lập bảng "tên cục bộ → module nguồn" (chưa resolve,
                                  chỉ ghi nhận khai báo import — dùng ở bước 4b)

     Ràng buộc chung cho 3a/3b/3c: mỗi thực thể sinh ra phải được gán `confidence`
     và `completeness` NGAY tại thời điểm trích xuất (mục 5.1) — vì chỉ extractor
     mới biết kết luận được đọc trực tiếp hay suy ra, và thuộc tính nào còn phụ
     thuộc biến runtime. Không được để bước sau "đoán lại".

     → Chi tiết từng extractor (nhiệm vụ, ví dụ code, fixture, bẫy hay gặp)
       đã gom sẵn ở MỤC 6c — đọc mục đó khi bắt tay code, không cần lần
       ngược lại các mục 5/5.1/8.1.

[4] Model Builder
     → gộp kết quả từ tất cả extractor thành 1 IntermediateArchitectureModel
     → đối chiếu FK giữa các entity đã tìm thấy; FK trỏ ra ngoài phạm vi
       → ghi vào unresolved_references (KHÔNG suy đoán bảng đó là gì)

[4b] Cross-file Resolver (mới)
     → input: bảng import từ 3e + toàn bộ FunctionNode/APIRoute/DBEntity từ bước 4
     → với mỗi tên gọi hàm/class (calls, base_class) chưa rõ nguồn gốc trong cùng file:
        1. tra bảng import xem tên đó được import từ module nào,
        2. kiểm tra module đó có nằm trong danh sách file đã quét ở bước 1 không,
        3. nếu có → set Reference.resolved = True, resolved_module = đường dẫn file đó,
        4. nếu không (import thư viện ngoài, hoặc không tìm thấy định nghĩa)
           → Reference.resolved = False, resolved_module = None,
             ghi thêm 1 UnresolvedReference nếu cần làm rõ trong tài liệu
     → ràng buộc: chỉ so khớp bằng dữ liệu cú pháp (tên module/alias), TUYỆT ĐỐI
       không được `import` hoặc thực thi file đang phân tích (xem mục 3.2)

[4c] Graph Builder (mới)
     → input: IntermediateArchitectureModel đã đầy đủ (sau bước 4b)
     → chuyển routes/entities/functions/external_calls và mọi Reference
       thành RepositoryKnowledgeGraph (mục 5.2): mỗi route/entity/function/module
       → 1 GraphNode, mỗi quan hệ (calls/imports/inherits/exposes...) → 1 GraphEdge;
       Reference chưa resolve dùng node Unresolved, không bị bỏ khỏi graph
     → không phân tích lại source code, không dùng AI — chỉ là phép biến đổi
        dữ liệu thuần (IAM → graph)
     → tạo ID theo mục 5.2, gộp edge trùng và sắp xếp ổn định trước khi ghi JSON

[5] AI Enrichment
     → input: IntermediateArchitectureModel đã hoàn chỉnh (bước 4b)
     → output: mô tả text ngắn cho từng Route/Entity/ExternalCall
     → ràng buộc cứng: AI KHÔNG được trả về bất kỳ trường nào ngoài "description"
       (nghĩa là schema đầu ra của bước này chỉ có 1 trường mô tả, không có chỗ
       để AI "chèn" thêm route/entity mới)

[6] Doc Generator
     → từ IAM (đã có mô tả bổ sung) + RepositoryKnowledgeGraph → sinh:
        - L3.md (theo template ở mục 7)
        - diagram.mmd (Mermaid graph)
        - graph.json (RepositoryKnowledgeGraph, mục 5.2)
        - IAM.json (toàn bộ IAM — nguồn dữ liệu cho Web UI, mục 13)

[6b] AI Reviewer (mới, bước AI thứ hai — độc lập với bước 5)
     → input: IntermediateArchitectureModel đã hoàn chỉnh (bước 4b) — KHÔNG nhận
       output của bước 5, để tránh mô tả AI ở bước 5 làm lệch nhận định của bước 6b
     → nhiệm vụ: rà soát IAM và tạo danh sách ReviewFinding (mục 6b.1) cho 4 loại
       nghi ngờ thiếu sót đã chốt trong scope (mục 2.1)
     → ràng buộc cứng: output chỉ là list[ReviewFinding] phụ trợ, KHÔNG được thêm/
       sửa/xoá bất kỳ trường nào trong IAM gốc; mỗi finding bắt buộc trỏ evidence
       (location cụ thể) về đúng phần tử trong IAM đã sinh ra cảnh báo đó
```

**Giải thích dễ hiểu mỗi bước:**
- **Bước 1-2 (Scanner + Parser):** giống việc quét toàn bộ tủ hồ sơ, mở từng tờ giấy ra đọc — nhưng chỉ đọc, không viết gì vào giấy gốc.
- **Bước 3 (Extractors):** các "chuyên viên" khác nhau, mỗi người chỉ giỏi tìm một loại thông tin cụ thể — tách riêng để mỗi người có thể được kiểm tra/sửa độc lập mà không ảnh hưởng người còn lại. Chuyên viên mới (3e) chỉ ghi chép "ai import ai" giống một cuốn sổ tham chiếu, chưa kết luận gì.
- **Bước 4 (Model Builder):** người tổng hợp, gom báo cáo của các chuyên viên thành 1 bộ hồ sơ thống nhất, và **thẳng thắn ghi "không rõ"** khi có chỗ thiếu thông tin, thay vì đoán bừa.
- **Bước 4b (Cross-file Resolver):** người tra cứu, cầm cuốn sổ import (bước 3e) để trả lời "cái tên này, nếu không định nghĩa trong file hiện tại, thì nó nằm ở file nào khác trong bộ hồ sơ?" — nếu tra không ra (ví dụ tên đó đến từ thư viện ngoài), phải ghi rõ "không tra được", không đoán bừa.
- **Bước 4c (Graph Builder):** người vẽ sơ đồ tổ chức từ chính hồ sơ đã có — không phỏng vấn thêm ai, chỉ vẽ lại đúng những gì hồ sơ đã ghi dưới dạng nút và đường nối.
- **Bước 5 (AI Enrichment):** được phép "nhờ" AI ngôn ngữ — nhưng chỉ nhờ viết lời văn mô tả, giống nhờ ai đó viết chú thích cho ảnh đã chụp sẵn, không nhờ họ "chụp lại" ảnh theo trí tưởng tượng.
- **Bước 6 (Doc Generator):** trình bày lại hồ sơ đã có sẵn thành văn bản đẹp, sơ đồ và file graph — không phát sinh thông tin mới.
- **Bước 6b (AI Reviewer):** một người kiểm toán độc lập, chỉ đọc hồ sơ gốc (không đọc phần chú thích của bước 5, để không bị "mượn" nhận định của người viết caption) và chỉ ra chỗ nào hồ sơ có vẻ thiếu — nhưng kiểm toán viên không có quyền sửa hồ sơ, chỉ có quyền ghi phiếu cảnh báo kèm bằng chứng.

### 6b.1 Schema ReviewFinding (output của bước 6b, tách biệt hoàn toàn khỏi IAM)

```python
class ReviewFinding(BaseModel):
    category: Literal[
        "unresolved_reference",      # FK/reference không resolve được
        "empty_handler_calls",       # route có calls rỗng hoặc handler không resolve được
        "orphan_entity",             # entity không có route/function nào reference tới
        "external_call_no_error_handling",  # gọi external call không thấy try/except bao quanh
    ]
    summary: str                     # 1 câu mô tả ngắn, không suy diễn xa hơn category
    evidence_location: SourceLocation  # bắt buộc trỏ về vị trí cụ thể trong source đã sinh ra IAM
    related_iam_ref: str             # mô tả phần tử IAM liên quan, ví dụ "APIRoute[3].handler_function"

class ReviewFindings(BaseModel):
    findings: list[ReviewFinding]
```

**Ràng buộc cứng cho từng category (để tránh AI suy diễn quá xa):**
- `unresolved_reference`: chỉ được tạo cho các mục **đã có sẵn** trong `unresolved_references` của IAM (bước 6b diễn giải rõ hơn bằng lời, không tự phát hiện thêm case mới ngoài IAM).
- `empty_handler_calls`: chỉ dựa trên `APIRoute.calls` rỗng hoặc chứa `Reference.resolved == False` — không suy đoán handler "chắc chắn có lỗi".
- `orphan_entity`: chỉ dựa trên việc duyệt toàn bộ `functions[].calls` và `routes[].calls` trong IAM, không tìm thấy `Reference` nào trỏ tới entity đó — nếu phạm vi quét chỉ là 1 phần của monorepo, phải ghi rõ trong `summary` đây là "trong phạm vi đã quét", không khẳng định toàn hệ thống.
- `external_call_no_error_handling`: chỉ dựa trên việc `caller_function` của `ExternalCall` không xuất hiện trong bất kỳ try/except nào mà AST Parser đã ghi nhận (cần CallGraphExtractor hoặc 1 extractor nhỏ bổ sung đánh dấu function nào có try/except bao ngoài lời gọi tương ứng — xem Task breakdown mục 9). Đây là **cảnh báo**, câu chữ trong `summary` phải dùng giọng "có thể thiếu xử lý lỗi", không dùng giọng khẳng định "sẽ lỗi".

**Giải thích dễ hiểu:** Mỗi `ReviewFinding` giống một tờ phiếu cảnh báo có đính kèm bằng chứng — không có tờ phiếu nào được viết ra nếu không trỏ được về đúng chỗ cụ thể trong hồ sơ IAM đã có. Đây chính là điểm khác với việc "hỏi AI xem có gì đáng ngờ không" một cách mở — 4 category đã liệt kê là toàn bộ những gì AI Reviewer được phép tìm, không được tự tạo category mới.

---

## 6c. Bảng tra cứu cho người code extractor (gom sẵn, không phải đọc rải rác)

Mục này **không thêm quy tắc mới** — nó gom lại những gì đã nói ở mục 5, 5.1, 6, 8.1 thành từng khối theo đúng đơn vị công việc. Khi bắt tay code một extractor, đọc đúng khối của nó là đủ.

### 6c.0 StackDetector (bước 1b)

| | |
|---|---|
| **Nhiệm vụ** | Chia repo thành các đơn vị phân tích, rồi nhận diện stack của **từng đơn vị** |
| **Nhận diện** | Ranh giới service theo vị trí file manifest; ngôn ngữ theo loại manifest; framework theo nội dung manifest + import |
| **Sinh ra** | `DetectedStack` (mục 4.4.7) |
| **Fixture test** | `tests/fixtures/detection/` — mỗi stack một repo mẫu nhỏ |
| **Task số** | 2b (mục 9) |

```python
# → exact + full: cả manifest lẫn import đều xác nhận
# requirements.txt chứa "fastapi==0.109.0"
# api/main.py chứa "from fastapi import FastAPI"

# → exact + partial: framework có bằng chứng trực tiếp, nhưng thiếu manifest
# (repo không commit requirements.txt)
# detection_reason: "không tìm thấy file khai báo phụ thuộc"

# → dừng, báo lỗi: không nguồn nào xác nhận
# (xem mẫu thông báo ở mục 4.4.6)
```

**Bẫy hay gặp nhất — coi cả repo là một stack:** hệ thống thật thường có nhiều service với stack khác nhau (mobile Java + AI service FastAPI, chẳng hạn). Nếu chọn ngôn ngữ theo số file chiếm đa số, service nhỏ hơn sẽ bị bỏ qua im lặng. Luôn chia theo manifest trước, nhận diện sau.

**Bẫy thứ hai:** một đơn vị dùng nhiều framework (FastAPI cho API + Django cho admin) — ghi nhận **tất cả**, không chọn bừa một cái.

**Quan trọng nhất:** đơn vị nào chưa hỗ trợ thì **bỏ qua đơn vị đó và nói rõ**, vẫn phân tích các đơn vị còn lại. Chỉ dừng hẳn khi không đơn vị nào phân tích được. Không bao giờ trả về kết quả trông có vẻ đầy đủ trong khi đã âm thầm bỏ sót một service.

### 6c.1 RouteExtractor (bước 3a)

| | |
|---|---|
| **Nhiệm vụ** | Tìm mọi API route được khai báo |
| **Nhận diện** | `@app.get/post/put/delete/patch(...)` trên instance `FastAPI()`; `APIRouter()` + decorator + `app.include_router(...)` |
| **Sinh ra** | `APIRoute` (mục 5) |
| **Fixture test** | `fixture_1_simple_route.py`, `fixture_2_nested_router.py` |
| **Task số** | 3 (mục 9) |

**Confidence + Completeness gán thế nào:**

```python
# → exact + full: route và path đều đọc thẳng từ cú pháp
@app.get("/orders")

# → exact + partial: route có thật, nhưng prefix là biến runtime
router = APIRouter(prefix=settings.API_PREFIX)
@router.get("/orders")
# path ghi: "{settings.API_PREFIX}/orders"
# reason: "prefix từ biến settings.API_PREFIX, không resolve được giá trị"

# → KHÔNG tạo entry, ghi unresolved_references
for name in ["order", "payment"]:
    app.include_router(make_router(name))
# (trừ khi pattern này được ghi thành rule cụ thể trong spec — xem mục 5.1 quy tắc 4)
```

**Bẫy hay gặp:** `include_router` lồng nhiều tầng — path cuối là ghép của mọi prefix trên đường đi. Nếu **bất kỳ** tầng nào là biến thì route vẫn có `confidence = exact`, nhưng `completeness = partial`.

### 6c.2 EntityExtractor (bước 3b)

| | |
|---|---|
| **Nhiệm vụ** | Tìm DB entity và cấu trúc bảng |
| **Nhận diện** | Class kế thừa `Base`/`declarative_base()` (kể cả qua class trung gian ở file khác) |
| **Sinh ra** | `DBEntity` + `DBColumn` (mục 5) |
| **Fixture test** | `fixture_3_sqlalchemy_entity.py`, `fixture_7_cross_file_inherit/` |
| **Task số** | 4 (mục 9) |

**Confidence + Completeness gán thế nào:**

```python
# → exact + full
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)

# → exact + partial: entity có thật, tên bảng không giải được
class Order(Base):
    __tablename__ = TABLE_PREFIX + "orders"
    # reason: "__tablename__ ghép từ biến TABLE_PREFIX"
```

**Bẫy hay gặp:** entity kế thừa class trung gian (`class Order(BaseModel)` mà `BaseModel` mới là cái kế thừa `Base`, định nghĩa ở file khác) — phải resolve qua bước 4b mới biết đây có phải entity không. Đây chính là `fixture_7`.

### 6c.3 ExternalCallExtractor (bước 3c)

| | |
|---|---|
| **Nhiệm vụ** | Tìm chỗ code gọi HTTP ra ngoài |
| **Nhận diện** | `httpx.Client()`, `httpx.get/post/...`, `requests.get/post/...` |
| **Sinh ra** | `ExternalCall` (mục 5) |
| **Fixture test** | `fixture_4_external_call.py` |
| **Task số** | 5 (mục 9) |

**Confidence + Completeness gán thế nào:**

```python
# → exact + full
requests.get("https://api.payment.com/charge")

# → exact + partial: có gọi ra ngoài thật, không biết đầy đủ đích đến
requests.get(f"{settings.PAYMENT_URL}/charge")
# url_or_host ghi: "{settings.PAYMENT_URL}/charge"  ← KHÔNG đoán giá trị thật
```

**Lưu ý riêng:** extractor này còn phải đánh dấu **lời gọi có nằm trong `try/except` không** — AI Reviewer cần dữ liệu đó cho category `external_call_no_error_handling` (mục 6b.1). Việc đánh dấu thuộc CallGraphExtractor (task 6), nhưng hai bên phải thống nhất cách biểu diễn.

### 6c.4 CallGraphExtractor (bước 3d)

| | |
|---|---|
| **Nhiệm vụ** | Tìm quan hệ hàm nào gọi hàm nào; đánh dấu try/except |
| **Sinh ra** | `FunctionNode` với `calls: list[Reference]` (mục 5) |
| **Fixture test** | `order_service_example.py` |
| **Task số** | 6 (mục 9) |

Ở bước này `Reference` mới chỉ có `name`; việc điền `resolved`/`resolved_module` là của bước 4b.

### 6c.5 ImportExtractor (bước 3e)

| | |
|---|---|
| **Nhiệm vụ** | Lập bảng "tên cục bộ → module nguồn" cho từng file |
| **Nhận diện** | `ast.Import`, `ast.ImportFrom` — **đọc như cú pháp, không `import` thật** |
| **Sinh ra** | Bảng tra cứu nội bộ (không nằm trong IAM), dùng ở bước 4b |
| **Fixture test** | `fixture_6_cross_file_call/`, `fixture_7_cross_file_inherit/` |
| **Task số** | 7 (mục 9) |

```python
from services.order import OrderService   # "OrderService" → "services/order.py"
import httpx                              # "httpx"        → (ngoài repo)
from .base import BaseEntity              # "BaseEntity"   → "<thư mục hiện tại>/base.py"
```

**Bước này chỉ ghi chép, không kết luận.** Việc đối chiếu với danh sách file đã quét để biết resolve được hay không là của bước 4b.

**Quan trọng:** bảng import phải gắn với **từng file**, không phải bảng toàn cục dùng chung. Xem mục 15.3 để biết vì sao — đây là lỗi thiết kế âm thầm cho ra kết quả sai mà test cấu trúc không phát hiện được.

### 6c.6 Checklist chung cho mọi extractor

- [ ] Chỉ đọc AST, không `import`/`exec` file đang phân tích (mục 3.2)
- [ ] Mỗi thực thể có `location` trỏ đúng `file` + `line_start` + `line_end`
- [ ] Có gán cả `confidence` và `completeness`; `reason` bắt buộc khi `inferred`, `partial` hoặc unresolved (mục 5.1)
- [ ] Gặp pattern lạ → `unresolved_references`, **không tự tạo entry `inferred`**
- [ ] Output khớp 100% JSON expected của fixture tương ứng, so sánh tự động

---

## 7. Template tài liệu L3 output

```markdown
# L3 — {Tên thư mục/service}

> Sinh tự động bởi Code → L3 Generator vào {ngày giờ chạy}.
> Route/Entity/External Call/Call Graph trích từ static AST analysis (chứng minh được, xem cột "Vị trí").
> Cột "Mô tả" do AI sinh thêm để dễ đọc — KHÔNG dùng làm căn cứ xác lập cấu trúc.
> Mục "Review Findings" do AI Reviewer sinh thêm — là cảnh báo cần con người xác nhận, KHÔNG phải kết luận chắc chắn.
> Cột "Bằng chứng / đầy đủ" ghi gọn hai nhãn, ví dụ `exact / partial`: kết luận có bằng chứng trực tiếp nhưng còn thiếu một phần giá trị — xem mục 5.1 của SPEC.
> Dòng có `inferred`, `partial` hoặc tham chiếu chưa resolve LUÔN kèm lý do; hãy tự xác minh tại vị trí source trước khi dựa vào nó.

## 1. Tổng quan

**Các đơn vị phân tích đã phát hiện** (từ `DetectedStack`, mục 4.4.7):

| Service | Ngôn ngữ | Framework | Số file | Bằng chứng / đầy đủ | Trạng thái |
|---|---|---|---|---|---|
| ai-service | Python | FastAPI | 31 | exact / full | Đã phân tích |
| mobile-app | Java | Spring Boot | 84 | exact / full | **Bỏ qua — chưa hỗ trợ** |

*(Bảng này luôn liệt kê **tất cả** đơn vị tìm thấy, kể cả đơn vị bị bỏ qua — để người đọc biết ngay tài liệu này bao phủ phần nào của hệ thống.)*

**Kết quả lần chạy này** (từ IAM và `RunMetrics`, mục 5.3):
- Đã phân tích {N_analyzed}/{N_found} file Python ({L} dòng) trong {T} giây
- Đã phân tích {S_analyzed}/{S_found} đơn vị; trạng thái: {đầy đủ/một phần}
- Phát hiện: {R} API route, {E} DB entity, {X} external dependency
- Mức bằng chứng: {a} exact, {b} inferred
- Độ đầy đủ: {c} full, {d} partial
- Chế độ: {có/không} mô tả AI

**Ước tính công sức tương đương nếu viết tay:** ~{lo}–{hi} ngày công
*(giả định {p} phút mỗi thành phần — ước tính theo hệ số cố định, không phải số đo thực nghiệm)*

## 2. API Routes
| Method | Path | Handler | Gọi tới (đã resolve module) | Bằng chứng / đầy đủ | Lý do | Vị trí | Mô tả (AI) |

## 3. DB Entities
| Entity | Bảng | Cột | FK | Base class (đã resolve module) | Bằng chứng / đầy đủ | Lý do | Vị trí |

## 4. External Dependencies
| Tên/Host | Method | Gọi từ | Bằng chứng / đầy đủ | Lý do | Vị trí | Mô tả (AI) |

## 5. Call Graph (rút gọn, chỉ hiển thị các hàm liên quan trực tiếp tới Route/Entity/External Call)

## 6. Dependency Diagram (Mermaid)

## 7. Repository Knowledge Graph
- Tóm tắt số node/edge theo từng loại (xem file `graph.json` đầy đủ đi kèm).

## 8. Review Findings (AI Reviewer)
| Category | Mô tả | Vị trí evidence |
(nếu rỗng: ghi "Không có cảnh báo nào trong lần chạy này")

## 9. Known Limitations
- **Đơn vị/service bị bỏ qua do stack chưa hỗ trợ** (từ `DetectedStack`) — nêu rõ tên, stack đã phát hiện, và phần hệ thống nào do đó không có trong tài liệu này
- Danh sách file bị bỏ qua do lỗi cú pháp (từ parse_errors)
- Danh sách tham chiếu chưa xác định được đích (từ unresolved_references)
```

**Ràng buộc trình bày (vì `L3.md` là thứ được mở ra cho người khác xem):**
- Bảng không quá 8 cột; cột "Mô tả (AI)" đặt cuối cùng để khi tràn ngang thì phần dữ liệu quan trọng vẫn đọc được.
- Mermaid phải render được trên GitLab/GitHub — nếu graph quá lớn (>40 node), sinh sơ đồ rút gọn ở mục 6 và để graph đầy đủ trong `graph.json`.
- Path dài phải cắt ngắn có dấu `…` nhưng giữ nguyên trong `graph.json`.
- Tiêu đề và mọi nhãn dùng cùng một ngôn ngữ, không trộn Việt–Anh trong cùng một bảng.

**Giải thích dễ hiểu:** Mục 9 "Known Limitations" **bắt buộc phải luôn xuất hiện**, kể cả khi rỗng (ghi "Không có giới hạn nào được ghi nhận trong lần chạy này") — để người đọc luôn biết chắc tài liệu này đáng tin tới mức nào, không phải đoán. Mục 8 "Review Findings" tách riêng khỏi mục 9 vì bản chất khác nhau: Known Limitations là **giới hạn của chính công cụ** (không phát hiện được gì), còn Review Findings là **cảnh báo về chính codebase** (có thể có vấn đề thật trong code, cần người xác nhận).

---

## 8. Acceptance Criteria (điều kiện để coi MVP là "xong")

### 8.1 Bộ fixture bắt buộc (viết tay trước khi giao Agent code)

Chuẩn bị tối thiểu 7 file Python mẫu, mỗi file kèm 1 file JSON "expected output" tương ứng đúng theo schema IAM ở mục 5. Fixture 6 và 7 dùng **2 file liên kết với nhau** (không phải 1 file đơn) vì mục đích là kiểm tra cross-file resolution.

| Fixture | Pattern cần bao phủ |
|---|---|
| `fixture_1_simple_route.py` | 1 route đơn giản khai báo trực tiếp trên `FastAPI()` |
| `fixture_2_nested_router.py` | `APIRouter` + `include_router`, có prefix |
| `fixture_3_sqlalchemy_entity.py` | Entity có PK, FK trỏ tới bảng trong cùng file |
| `fixture_4_external_call.py` | Gọi `httpx` và `requests` ra ngoài |
| `fixture_5_broken_syntax.py` | Cố tình có lỗi cú pháp → kiểm tra công cụ bỏ qua đúng cách, không crash toàn bộ |
| `fixture_6_cross_file_call/` (2 file: `handler.py` + `service.py`) | Route ở `handler.py` gọi hàm định nghĩa ở `service.py` qua `from service import ...` — kiểm tra `Reference.resolved = True, resolved_module = "service.py"` |
| `fixture_7_cross_file_inherit/` (2 file: `base.py` + `entity.py`) | Entity ở `entity.py` kế thừa class trung gian định nghĩa ở `base.py` (chính class trung gian đó mới kế thừa `Base`) — kiểm tra `base_class` resolve đúng xuyên file, đồng thời phải resolve tiếp 1 tầng để biết đây vẫn là SQLAlchemy entity |

**Tiêu chí đạt:** Chạy công cụ trên từng fixture, output IAM phải khớp **chính xác 100%** với file JSON expected output tương ứng (so sánh tự động, không phải "nhìn thấy hợp lý").

Khi Graph Builder đã được triển khai, lấy **cùng một IAM đã lưu** làm đầu vào và chạy hai lần. Hai file `graph.json` phải giống nhau từng byte; mọi `GraphNode.id` phải duy nhất, và các mảng `nodes`/`edges` phải đúng thứ tự quy định ở mục 5.2. Đây là test nhỏ, không cần tạo thêm fixture hay tài liệu.

**Fixture bổ sung cho import không resolve được (bắt buộc, không cần file JSON riêng — có thể gộp vào fixture 6):** 1 dòng `import` trỏ tới thư viện ngoài phạm vi repo (ví dụ `import os`) → xác nhận `Reference.resolved = False, resolved_module = None`, không bị nhầm là lỗi.

**Fixture cho các trường hợp khó của resolution (mục 15.4) — thêm khi làm task 9:**

| Fixture | Trường hợp | Kỳ vọng |
|---|---|---|
| `fixture_8_same_name_diff_module/` | Hai file cùng import tên `OrderService` nhưng từ hai module khác nhau | Mỗi lời gọi resolve về **đúng module của file gọi nó** (mục 15.3) |
| `fixture_9_deep_inheritance/` | Kế thừa 3 tầng qua 3 file, method nằm ở tầng cao nhất | Leo đúng chuỗi, `resolved_module` trỏ tới file chứa định nghĩa thật |
| `fixture_10_external_base/` | Class kế thừa base class từ thư viện ngoài | `resolved = False`, lý do "class cha thuộc thư viện ngoài", **không báo lỗi** |
| `fixture_11_circular_inherit/` | `A(B)` và `B(A)` | Dừng đúng cách, ghi `unresolved_references`, **tool không treo** |
| `fixture_12_multiple_inherit/` | `class A(B, C)` với method có ở cả B lẫn C | Lấy B (khai báo trước), `confidence = inferred`, `completeness = full`, lý do nêu rõ quy tắc đa kế thừa đã dùng |

Năm fixture này kiểm chính xác năm chỗ mà resolution dễ sai nhất. `fixture_8` và `fixture_11` quan trọng nhất: cái đầu bắt lỗi thiết kế âm thầm, cái sau đảm bảo tool không treo khi gặp code hỏng.

### 8.1b Kiểm tra Stack Detection (mục 4.4)

Chuẩn bị các repo mẫu nhỏ trong `tests/fixtures/detection/`, mỗi cái chỉ cần vài file:

**Nhóm A — một đơn vị:**

| Repo mẫu | Kỳ vọng |
|---|---|
| FastAPI có `requirements.txt` và có import | 1 đơn vị, `python` + `fastapi`, `exact / full` |
| FastAPI không có manifest | 1 đơn vị, `exact / partial`, lý do nêu rõ thiếu manifest |
| Flask | 1 đơn vị, nhận đúng `flask`, `analyzed = False`, `skip_reason` nêu rõ chưa hỗ trợ |
| Chỉ có file `.js` | Không đơn vị nào phân tích được → exit 1, thông báo rõ |
| Thư mục rỗng | Báo "không tìm thấy đơn vị phân tích nào", exit 1 |
| Một service dùng cả FastAPI + Django | 1 đơn vị, `frameworks = ["fastapi", "django"]` — không chọn bừa một cái |

**Nhóm B — nhiều đơn vị (quan trọng nhất, dễ sai nhất):**

| Repo mẫu | Kỳ vọng |
|---|---|
| `mobile-app/` (pom.xml, Java) + `ai-service/` (requirements.txt, FastAPI) | Phát hiện **2 đơn vị**. `ai-service` được phân tích; `mobile-app` có `analyzed = False`. Tài liệu vẫn sinh ra, kèm cảnh báo rõ về đơn vị bị bỏ qua |
| Monorepo 3 service FastAPI | Phát hiện **3 đơn vị**, phân tích cả ba. Mọi route/entity mang đúng trường `service` |
| Manifest lồng nhau: `repo/pom.xml` + `repo/svc-a/pom.xml` | `svc-a` là đơn vị riêng; `repo/pom.xml` chỉ quản phần còn lại |
| 2 service Java (đều chưa hỗ trợ) | Không đơn vị nào phân tích được → exit 1, liệt kê **cả hai** kèm stack đã phát hiện |
| Service FastAPI + thư mục `docs/` | Chỉ 1 đơn vị; `docs/` bị bỏ qua im lặng, không tính là đơn vị lỗi |

**Tiêu chí đạt:**
1. Với mỗi repo mẫu, `DetectedStack.services` khớp đúng kỳ vọng về **số lượng đơn vị**, tên, ngôn ngữ, framework và cờ `analyzed` (so sánh tự động).
2. Với repo nhiều đơn vị: mọi `APIRoute`/`DBEntity`/`ExternalCall` sinh ra đều có trường `service` đúng — **không có thực thể nào của service này bị gán nhầm sang service kia**.
3. Với repo có đơn vị bị bỏ qua: tài liệu vẫn được sinh cho các đơn vị còn lại, và mục "Known Limitations" liệt kê đầy đủ đơn vị bị bỏ qua kèm lý do.
4. Các trường hợp báo lỗi: thông báo nêu đủ ba điều — phát hiện được gì, tool hỗ trợ gì, người dùng nên làm gì tiếp.
5. `RunMetrics` tuân thủ ba bất biến ở mục 5; repo có service bị bỏ qua hoặc file parse lỗi phải có `is_partial = True`, còn repo phân tích đủ phải có `is_partial = False`.

### 8.2 Kiểm tra trên codebase mẫu lớn hơn

Chạy trên 1 repo FastAPI mẫu (open-source hoặc tự dựng, quy mô vài chục file, **bắt buộc có ít nhất vài chỗ gọi hàm/kế thừa xuyên file** để cross-file resolution có dữ liệu thật để kiểm) — không yêu cầu khớp 100% (vì không có "đáp án đúng" viết sẵn ở quy mô này), nhưng phải đảm bảo:
- Không crash giữa chừng.
- Số route/entity nhận diện được không lệch quá xa so với đếm thủ công (do người review tự đếm nhanh để đối chiếu).
- Mục "Known Limitations" phản ánh đúng thực tế (không rỗng nếu thực sự có phần bị bỏ sót).
- Tỷ lệ `Reference.resolved = True` trên các lời gọi xuyên file đã biết chắc là nội bộ repo (người review tự xác minh vài trường hợp cụ thể bằng mắt) phải khớp — nếu resolver bỏ sót nhiều, đây là lỗi cần sửa trước khi sang bước Graph Builder/AI Reviewer.
- `graph.json` sinh ra không có edge nào không trace ngược được về IAM (kiểm tra bằng script, lấy mẫu ngẫu nhiên một số edge để đối chiếu).

### 8.3 Kiểm tra ranh giới AI (quan trọng nhất, dễ bị bỏ qua nhất)

Viết 1 test riêng: chạy bước AI Enrichment (mục 6, bước 5) và xác nhận **schema đầu ra của AI chỉ có trường mô tả text**, không có khả năng chèn thêm route/entity mới vào IAM — kiểm tra bằng code (schema validation), không kiểm tra bằng cách "đọc thấy hợp lý".

**Giải thích dễ hiểu:** Đây là bài kiểm tra "khóa cửa" — đảm bảo AI dù có cố "sáng tạo" đến đâu cũng không có cách nào len được vào phần dữ liệu đã được đóng dấu là "sự thật đã chứng minh".

### 8.4 Kiểm tra ranh giới AI Reviewer (bước 6b — tương tự 8.3, áp dụng cho bước AI thứ hai)

- Test schema: xác nhận output của AI Reviewer chỉ là `list[ReviewFinding]` (mục 6b.1), không có trường nào cho phép sửa/thêm/xoá route/entity/quan hệ trong IAM gốc — kiểm tra bằng schema validation.
- Test evidence: với mỗi `ReviewFinding` sinh ra trên bộ fixture (mục 8.1), `evidence_location` phải trỏ đúng tới vị trí đã biết trước trong fixture đó (so khớp tự động, không đọc bằng mắt).
- Test category: xác nhận AI Reviewer không tự tạo `category` nào ngoài 4 loại đã liệt kê ở mục 6b.1 (schema `Literal` đã chặn ở tầng Pydantic, nhưng vẫn cần test để chắc chắn Agent không đổi schema để "lách").
- Chạy trên codebase mẫu (mục 8.2): người review đọc thủ công toàn bộ `ReviewFinding` sinh ra, xác nhận không có finding nào rơi vào tình huống "đọc evidence xong vẫn không hiểu vì sao bị flag" — nếu có, coi là spec chưa đủ rõ cho category đó, cần ghi nhận vào Feedback Loop (mục 10).

### 8.5 Evaluation trên repo thật — đo precision/recall (mục quan trọng nhất để trả lời "tool này tốt tới đâu")

Ba mục 8.1-8.4 ở trên đều có một điểm yếu chung: **chúng ta tự ra đề rồi tự chấm.** Fixture do chính mình viết nên tool đương nhiên khớp; "không lệch quá xa so với đếm tay" là tiêu chí không đo được. Mục này bổ sung phép đo khách quan trên code mà không ai trong đội viết ra.

#### 8.5.1 Chuẩn bị ground truth (con người làm, KHÔNG giao Agent)

1. Chọn **1 repo FastAPI open-source thật**, quy mô 30-80 file Python. Tiêu chí chọn: có nhiều router lồng nhau, có SQLAlchemy model, có gọi HTTP ra ngoài, và **không phải repo do đội tự viết** (tránh việc vô tình viết code "vừa khít" với extractor).
2. Hai người **đọc tay độc lập** toàn bộ repo, mỗi người tự liệt kê ra file CSV/JSON:
   - toàn bộ API route (method + path đầy đủ sau khi ghép prefix),
   - toàn bộ DB entity (class + tên bảng),
   - toàn bộ external call (host/URL + nơi gọi).
3. Đối chiếu 2 danh sách. Chỗ nào lệch nhau → thảo luận tới khi thống nhất. **Chính những chỗ 2 người đọc ra khác nhau là dữ liệu quý nhất** — nó cho biết đâu là phần mà ngay cả con người cũng thấy mơ hồ, và tool không thể bị kỳ vọng làm tốt hơn.
4. Chốt thành file `ground_truth.json`, commit vào repo tool.

**Lưu ý về công sức:** Bước này tốn khoảng 1-1.5 ngày cho 2 người. Đây là chi phí bắt buộc, không cắt được — không có ground truth thì mọi con số về sau đều vô nghĩa.

#### 8.5.2 Các chỉ số phải đo

Với mỗi loại thực thể (route / entity / external call), tính riêng:

| Chỉ số | Công thức | Nó trả lời câu hỏi gì |
|---|---|---|
| **Precision** | (số thực thể tool báo đúng) / (tổng số tool báo) | Trong những gì tool nói có, bao nhiêu phần trăm là thật? (đo mức độ "bịa") |
| **Recall** | (số thực thể tool báo đúng) / (tổng số có thật trong ground truth) | Trong những gì thật sự tồn tại, tool tìm được bao nhiêu phần trăm? (đo mức độ "bỏ sót") |
| **Precision theo mức confidence** | tính riêng cho `exact` và `inferred`; luôn ghi kèm số mẫu của từng nhóm | Nhãn bằng chứng có thực sự phản ánh độ tin cậy không? |
| **Phân bố completeness** | đếm riêng `full` và `partial` | Bao nhiêu kết quả còn thiếu một phần thuộc tính vì phụ thuộc runtime? |

**Kiểm định tính hợp lệ của hai nhãn:** nếu cả hai nhóm có đủ mẫu, precision của `exact` phải cao hơn nhóm `inferred`; nếu không, phải xem lại quy tắc gán confidence ở mục 5.1. Không xếp `partial` thấp hơn `full` về độ chính xác: `partial` nói rằng **thiếu thuộc tính**, không nói rằng thực thể được phát hiện là sai. Với nhóm `partial`, kiểm tra thủ công lý do có nêu đúng phần còn thiếu hay không. Nếu nhóm `inferred` quá ít hoặc rỗng, báo đúng thực tế đó thay vì đưa ra kết luận thống kê.

#### 8.5.3 Ngưỡng chấp nhận (đặt trước khi chạy, không sửa sau khi thấy kết quả)

| Nhóm | Ngưỡng tối thiểu | Ghi chú |
|---|---|---|
| Route — recall | ≥ 85% | Miss chủ yếu được phép rơi vào dynamic registration |
| Route — precision (nhóm `exact`) | ≥ 95% | Đã đánh dấu `exact` mà vẫn sai là lỗi nghiêm trọng |
| Entity — recall | ≥ 90% | SQLAlchemy declarative tương đối dễ nhận diện, kỳ vọng cao hơn route |
| External call — recall | ≥ 80% | Chấp nhận thấp hơn vì nhiều cách gọi gián tiếp |

**Quy tắc xử lý khi không đạt ngưỡng:** Không được hạ ngưỡng. Hai lựa chọn hợp lệ: (a) sửa extractor, hoặc (b) ghi nhận rõ vào Known Limitations kèm phân tích *vì sao* loại pattern đó không thể xử lý bằng static analysis, và giữ nguyên con số thật trong báo cáo.

#### 8.5.4 Phân tích lỗi (bắt buộc, giá trị hơn cả con số)

Với **mọi** trường hợp false negative (bỏ sót) và false positive (báo sai), phải phân loại nguyên nhân thành nhóm và đếm số lượng, ví dụ:

```
False negative (8 routes bị bỏ sót):
  - 5 do dynamic registration trong vòng lặp     → không thể xử lý bằng static AST
  - 2 do decorator custom bọc ngoài @router.get  → có thể xử lý, cần thêm rule
  - 1 do file bị lỗi cú pháp                      → đúng như thiết kế

False positive (2 routes báo thừa):
  - 2 do route nằm trong khối `if DEBUG:`         → cần rule xử lý conditional
```

Bảng phân tích này là **output quan trọng nhất của cả mục 8.5**: nó biến câu "tool chưa hoàn hảo" thành "tool bỏ sót đúng 3 loại pattern, 2 trong đó sửa được, 1 là giới hạn bản chất của static analysis". Đây cũng là đầu vào trực tiếp cho quyết định mở rộng scope ở giai đoạn sau.

#### 8.5.5 Báo cáo

Kết quả evaluation phải được commit thành file `EVALUATION.md` trong repo, gồm: repo đã dùng (kèm commit hash để tái lập), bảng chỉ số, bảng phân tích lỗi, và kết luận thẳng thắn về việc tool đã dùng được cho mục đích gì / chưa dùng được cho mục đích gì.

**Bắt buộc có thêm: phần tóm tắt cho người không đọc bảng số** (đặt ở **đầu** `EVALUATION.md`, trước mọi bảng). Cùng dữ liệu, khác cách kể — 3-5 câu, không thuật ngữ thống kê:

> **Ví dụ mẫu:**
> "Chúng tôi kiểm chứng trên repo mã nguồn mở `<tên>` gồm 47 file Python. Hai kỹ sư đọc tay toàn bộ repo để lập danh sách đối chiếu độc lập, trước khi chạy công cụ.
> Công cụ tìm đúng 43 trong 45 API route thực có (96%) và 11/11 DB entity (100%). Hai route bị bỏ sót đều thuộc cùng một kiểu khai báo động mà phân tích tĩnh không đọc được — kiểu này đã được ghi rõ trong phần Giới hạn đã biết của mọi tài liệu sinh ra.
> Không có trường hợp nào công cụ báo ra một route không tồn tại."

**Câu cuối trong ví dụ trên là câu quan trọng nhất** — với người mua, "không bịa ra thứ không có" đáng giá hơn "tìm được nhiều". Một tài liệu bỏ sót thì người đọc còn phát hiện được; một tài liệu bịa thì họ tin nhầm.

**Quy tắc:** phần tóm tắt này chỉ được dùng con số lấy thẳng từ bảng phía dưới. Nếu chỉ số nào chưa đạt ngưỡng ở mục 8.5.3, **vẫn phải nêu** — kèm lý do và cách khắc phục. Che số liệu xấu trong một tài liệu mà toàn bộ giá trị nằm ở chỗ "trung thực về giới hạn" là tự phá hỏng lập luận bán hàng của chính mình.

**Giải thích dễ hiểu:** Hãy tưởng tượng một máy dò kim loại. Nói "máy này tốt" không có nghĩa gì cả. Nói "trên bãi thử có 100 vật kim loại chôn sẵn, máy tìm được 87 vật, báo nhầm 4 lần vào vỏ lon, và toàn bộ 13 vật bị bỏ sót đều nằm sâu hơn 50cm" — đó mới là thông tin dùng được, vì người nghe biết chính xác khi nào tin được máy và khi nào phải tự đào. Mục 8.5 làm đúng việc đó cho tool này: biến "hình như chạy ổn" thành những con số mà bất kỳ ai cũng kiểm chứng lại được bằng cách chạy lại trên đúng repo đó.

---

## 9. Kế hoạch triển khai (Task breakdown, làm tuần tự)

> Khi bắt đầu một task extractor (task 3-7), đọc khối tương ứng ở **mục 6c** — nó gom sẵn nhiệm vụ, ví dụ code, fixture và bẫy hay gặp của extractor đó.

1. Định nghĩa Pydantic schema IAM + `Reference` + `Confidence` + `Completeness` (mục 5, 5.1) + viết 7 fixture và expected output (mục 8.1) — **làm trước khi giao Agent bất kỳ code nào khác**. Fixture phải bao phủ `exact / partial` (ví dụ prefix là biến) và ít nhất một trường hợp `inferred`.
2. Repo Scanner + AST Parser (bước 1-2) — test bằng `fixture_5_broken_syntax.py`.
2b. **Service Discovery + Stack Detection (bước 1b, mục 4.4)** — hai phần tách biệt: (a) tìm ranh giới service theo manifest, (b) nhận diện stack từng đơn vị. Test theo mục 8.1b, **đặc biệt nhóm B (repo nhiều đơn vị)** vì đây là chỗ dễ sai nhất. Làm sớm vì mọi extractor phía sau đều cần biết mình đang chạy trong phạm vi service nào.
3. RouteExtractor — test bằng fixture 1, 2, **kèm gán `confidence` + `completeness` + `reason` theo mục 5.1**.
4. EntityExtractor — test bằng fixture 3, **kèm gán `confidence` + `completeness` + `reason` theo mục 5.1**.
5. ExternalCallExtractor — test bằng fixture 4, **kèm gán `confidence` + `completeness` + `reason` theo mục 5.1**.
6. CallGraphExtractor (bao gồm đánh dấu function nào có try/except bao quanh lời gọi — dữ liệu này AI Reviewer sẽ cần ở task 13).
7. ImportExtractor (bước 3e) — test bằng fixture 6, 7 (chỉ phần lập bảng import, chưa resolve).
8. Model Builder (gộp + phát hiện unresolved reference).
9. Cross-file Resolver (bước 4b) — **đọc kỹ mục 15 trước khi code**, đây là task khó nhất của dự án. Làm theo thứ tự 8 bước ở mục 15.8, sau mỗi bước ghi lại tỷ lệ resolve được. Test bằng fixture 6, 7: xác nhận `Reference.resolved`/`resolved_module` đúng 100%, và trường hợp import thư viện ngoài trả về `resolved = False` đúng cách.
10. Graph Builder (bước 4c) — định nghĩa `GraphNode`/`GraphEdge` (mục 5.2) + test mỗi edge trace ngược được về đúng 1 phần tử IAM + test ID/thứ tự output ổn định khi chạy hai lần từ cùng IAM.
11. Chạy toàn bộ pipeline (bước 1-4c) trên codebase mẫu lớn hơn (mục 8.2) — review thủ công trước khi sang bước AI, đặc biệt kiểm tra tỷ lệ resolve xuyên file và graph.json.
12. AI Enrichment (bước 5) — kèm test khóa schema (mục 8.3).
13. AI Reviewer (bước 6b) — định nghĩa `ReviewFinding` (mục 6b.1) + kèm test khóa schema và evidence (mục 8.4).
14. Doc Generator (Markdown + Mermaid + `graph.json` + `IAM.json` theo template mục 7) — bảng output dùng một cột gọn `Bằng chứng / đầy đủ`, không tách thêm bảng hay tài liệu.
15. **Evaluation (mục 8.5)** — chuẩn bị ground truth thủ công, đo precision/recall, phân tích lỗi, viết `EVALUATION.md` (mở đầu bằng tóm tắt cho người không đọc bảng số, mục 8.5.5). Ground truth nên chuẩn bị **song song từ sớm** (không đợi tới bước 15) vì đây là việc của con người, không phụ thuộc tiến độ code.
16. **Đóng gói & tài liệu (mục 12)** — `pyproject.toml`, `README.md`, `examples/`. (~1,25 ngày)
17. **Web UI (mục 13)** — phần mở rộng, làm sau khi lõi đã chạy đúng. Thứ tự màn hình theo mục 13.7. (~5 ngày)

**Hai task làm xen kẽ, không đợi tới cuối:**

- **CLI + xử lý lỗi (mục 4.2, 4.3)** — khung CLI và `--no-ai` phải có **ngay từ task 2**, vì toàn bộ giai đoạn đầu đều chạy không có AI. Phần xử lý lỗi tử tế hoàn thiện dần, chốt lại trước khi đóng gói. (~0,5 ngày rải rác)
- **Value Metrics (mục 5.3)** — `RunMetrics` nằm trong IAM nên khai báo cùng task 1; phần đo và in ra hoàn thiện ở task 14 (Doc Generator). (~0,5 ngày)

**Tổng phát sinh so với bản trước:** khoảng 2,25 ngày (chi tiết ở mục 12.4).

**Giải thích dễ hiểu:** Thứ tự này đảm bảo phần "xương sống" (dữ liệu chính xác, không dùng AI) được xây và kiểm chứng chắc chắn trước — bao gồm cả cross-file resolution và graph, vì cả hai đều là static analysis thuần, không dùng AI. Hai bước AI (Enrichment và Reviewer) chỉ được thêm vào sau cùng khi phần xương sống đã đứng vững, và **AI Reviewer cố tình đặt sau AI Enrichment nhưng nhận input độc lập** (từ IAM, không từ output Enrichment) để tránh 2 bước AI "ăn theo" nhau — nếu Reviewer đọc luôn cả mô tả do Enrichment viết, một lỗi hallucination ở Enrichment có thể lan sang Reviewer mà không ai nhận ra.

---

## 10. Ghi chú cho Feedback Loop (Agentic SDLC)

Trong quá trình triển khai, cần ghi nhận riêng (theo yêu cầu chung của chương trình):
- Có fixture nào phát sinh thêm ngoài 7 cái ban đầu không (dấu hiệu spec ban đầu thiếu case).
- Agent có từng đề xuất "tiện thể" dùng AI để bù chỗ static analysis chưa làm được không (ví dụ dùng AI để đoán cross-file resolution thay vì tra bảng import) — nếu có, đây là tín hiệu cần ghi nhận và từ chối theo đúng nguyên tắc mục 3.1.
- Thời gian/số vòng lặp cần để mỗi Extractor/Resolver đạt 100% khớp fixture.
- Cross-file Resolver có gặp pattern import nào (ví dụ import tương đối phức tạp, `import as`, wildcard `from x import *`) mà spec ban đầu chưa lường tới không — nếu wildcard import xuất hiện thực tế, cần quyết định rõ: coi là unresolved hay mở rộng resolver, không để Agent tự quyết.
- AI Reviewer có từng sinh finding mà evidence không thực sự trỏ đúng chỗ, hoặc category bị "lạm dụng" cho tình huống không thuộc 4 loại đã định nghĩa không.
- Có trường hợp nào Agent gán `confidence = exact` cho kết luận thực tế chỉ được suy ra, hoặc gán `completeness = full` khi còn thiếu thuộc tính không — đây là dấu hiệu hai quy tắc ở mục 5.1 đang bị trộn lẫn.
- Khi đo evaluation (mục 8.5): có phải hạ ngưỡng chấp nhận không, và nếu có thì vì lý do gì. Ghi lại **con số thật ở lần đo đầu tiên**, trước mọi vòng sửa extractor — đây là dữ liệu cho thấy Agentic SDLC đi từ đâu tới đâu.
- Hai người viết ground truth độc lập lệch nhau ở bao nhiêu mục, và lệch ở loại pattern nào — cho biết chỗ nào bản thân bài toán vốn đã mơ hồ với cả con người.

---

## 11. Tham khảo thị trường (đã khảo sát, dùng để định vị khác biệt)

- **Swark** (github.com/swark-io/swark): để 100% LLM đọc code và tự suy luận kiến trúc, không có bước AST riêng — nhanh, hỗ trợ mọi ngôn ngữ, nhưng không đảm bảo chính xác, không tra ngược được bằng chứng. Đây là mô hình spec này **chủ động không đi theo**, vì vi phạm nguyên tắc 3.1.
- **CodeBoarding** (github.com/CodeBoarding/CodeBoarding): kết hợp static analysis + LLM reasoning, tách 2 tầng output (tổng quan + chi tiết theo subsystem), có GitHub Action tự cập nhật trong CI. Đây là mô hình **gần nhất với hướng đi đúng** của spec này; điểm khác biệt spec này giữ lại là gắn nhãn tường minh nguồn gốc từng phần dữ liệu (AST-verified vs AI-generated) ngay trong tài liệu xuất ra.

---

## 12. Đóng gói & tài liệu repo (yêu cầu mức prototype bàn giao được)

Tool được dùng để trình bày cho người ngoài đội và có thể được người khác tự cài thử. Yêu cầu tối thiểu:

### 12.1 Cài đặt

- `pyproject.toml` chuẩn, cài được bằng `pip install -e .`
- Entry point `l3gen` khả dụng ngay sau khi cài (không phải gọi `python -m ...`)
- Dependencies tối thiểu, phiên bản có chốt cận trên để không vỡ bất ngờ
- Python 3.10+ (khớp mục 2.1)

### 12.2 `README.md` — bắt buộc có, theo đúng thứ tự sau

1. **Một câu mô tả tool làm gì** (người đọc 10 giây đầu phải hiểu)
2. **Quickstart 3 lệnh**: cài → chạy → xem kết quả ở đâu
3. **Ví dụ output thật** — trích một đoạn `L3.md` đã sinh, không mô tả suông
4. **Tool này KHÔNG làm gì** — trích từ mục 2.2, đặt ngay phần đầu, không giấu xuống cuối
5. **Kết quả kiểm chứng** — 3-5 câu tóm tắt từ `EVALUATION.md` (mục 8.5.5), kèm link tới bản đầy đủ
6. Cấu hình (biến môi trường, các tùy chọn CLI — mục 4.2)
7. Hạn chế đã biết và hướng phát triển

**Mục 4 đặt ngay phần đầu là có chủ ý.** Nói trước giới hạn làm người đọc tin phần còn lại hơn; giấu xuống cuối thì lúc họ tự phát hiện sẽ mất lòng tin vào toàn bộ tài liệu.

### 12.3 Trong repo phải có

| File | Mục đích |
|---|---|
| `README.md` | mục 12.2 |
| `EVALUATION.md` | mục 8.5.5 — kết quả đo, mở đầu bằng tóm tắt cho người không đọc bảng số |
| `SPEC_Code_to_L3_Generator.md` | chính tài liệu này |
| `examples/` | ít nhất 1 bộ output đã sinh sẵn (`L3.md` + `diagram.mmd` + `graph.json` + `IAM.json`) để xem ngay không cần chạy |
| `tests/fixtures/` | 7 fixture + expected JSON (mục 8.1) — **luôn commit, không đưa vào `.gitignore`** |

**`examples/` quan trọng hơn vẻ ngoài của nó:** nó cho phép người quan tâm thấy kết quả thật trong 30 giây mà không cần cài gì, không cần API key, không cần mạng. Đồng thời là phương án dự phòng khi trình bày trực tiếp mà môi trường trục trặc.

### 12.4 Ước tính công sức cho mục 12

| Hạng mục | Ước tính |
|---|---|
| `pyproject.toml` + entry point + dọn dependencies | 0,5 ngày |
| `README.md` đầy đủ 7 phần | 0,5 ngày |
| `examples/` (chạy và commit output) | 0,25 ngày |
| Xử lý lỗi tử tế theo mục 4.3 | 0,5 ngày |
| Value Metrics theo mục 5.3 | 0,5 ngày |
| **Tổng** | **~2,25 ngày** |

Con số này để cân đối khi quyết định cắt hay giữ phạm vi.

---

## 13. Web UI (phần mở rộng — dùng để trình bày)

Toàn bộ mục 1-12 mô tả một CLI tool hoàn chỉnh, chạy độc lập và đủ giá trị. Mục này bổ sung **một lớp giao diện web đặt lên trên**, phục vụ hai mục đích: xem kết quả dễ hơn so với đọc Markdown thô, và có thứ trình bày trực quan khi demo.

### 13.1 Nguyên tắc: UI là lớp phủ, không phải lõi

```
┌──────────────────────────────────────┐
│   Web UI (mục 13)  ← phần mở rộng    │
│   đọc IAM / graph.json, không phân   │
│   tích lại source                    │
└───────────────┬──────────────────────┘
                │ đọc
┌───────────────▼──────────────────────┐
│   CLI + Pipeline (mục 1-12) ← lõi    │
│   chạy được hoàn toàn độc lập        │
└──────────────────────────────────────┘
```

**Ràng buộc cứng:**
1. **UI không bao giờ tự phân tích source code.** Nó chỉ đọc `IAM.json` và `graph.json` do pipeline sinh ra.
2. **Xoá toàn bộ thư mục UI thì CLI vẫn chạy đúng như cũ.** Không có phụ thuộc ngược từ lõi lên UI.
3. **UI không được hiển thị thông tin nào không có trong IAM.** Mọi con số, mọi dòng, mọi node trên màn hình đều truy được về dữ liệu gốc.
4. **UI phải trung thành với nhãn nguồn gốc** (mục 3.3): dữ liệu từ AST và mô tả do AI sinh phải phân biệt được bằng mắt, không được trộn lẫn cho "đẹp".

**Giải thích dễ hiểu:** UI ở đây giống như một khung tranh đẹp — làm bức tranh dễ ngắm hơn, nhưng không vẽ thêm nét nào lên tranh. Nếu tháo khung ra, bức tranh vẫn nguyên vẹn.

### 13.2 Hình thái

**Static site tự chứa**, không có backend:

- Pipeline sinh thêm `IAM.json` (toàn bộ IAM, không chỉ graph) vào thư mục output
- UI là các file HTML/CSS/JS tĩnh, đọc JSON đó bằng `fetch`
- Chạy bằng `l3gen ui ./l3-output/` → mở server tĩnh ở `localhost:8000` và tự mở trình duyệt
- Không database, không đăng nhập, không state phía server

Lý do chọn static thay vì dựng backend: giữ đúng tinh thần "hạn chế ảnh hưởng hệ thống đang vận hành", không phát sinh thứ phải deploy và vận hành, và demo được ngay cả khi không có mạng.

### 13.3 Các màn hình

| Mã | Màn hình | Nội dung chính |
|---|---|---|
| **U-01** | Tổng quan | Số liệu lần chạy (từ `RunMetrics`), phân bố confidence/completeness, danh sách cảnh báo nổi bật, nút điều hướng sang các màn còn lại |
| **U-02** | API Routes | Bảng route lọc/tìm được theo method, confidence và completeness; click một dòng → mở panel chi tiết bên phải |
| **U-03** | DB Entities | Danh sách entity, cột, khoá chính/ngoại; hiển thị quan hệ giữa các bảng |
| **U-04** | Dependency Graph | Đồ thị tương tác: kéo/thả, zoom, lọc theo loại node, click node để xem chi tiết |
| **U-05** | Review Findings | Danh sách cảnh báo AI, nhóm theo loại, mỗi cảnh báo mở được vị trí bằng chứng |
| **U-06** | Known Limitations | File bị bỏ qua, tham chiếu chưa resolve — **luôn hiển thị, kể cả khi rỗng** |

### 13.4 Quy tắc hiển thị bắt buộc

Đây là phần dễ bị làm sai nhất khi ưu tiên "cho đẹp", nên quy định rõ:

| Loại dữ liệu | Cách hiển thị |
|---|---|
| Dữ liệu từ AST | Chữ thường, màu văn bản chính |
| Mô tả do AI sinh | Nền khác biệt rõ + nhãn "AI" ở đầu khối. Không bao giờ trình bày giống hệt dữ liệu AST |
| `confidence = exact` | Không cần nhãn riêng (đây là mặc định) |
| `confidence = inferred` | Nhãn "suy ra" màu đậm + `reason` hiện luôn, không giấu trong tooltip |
| `completeness = full` | Không cần nhãn riêng (đây là mặc định) |
| `completeness = partial` | Nhãn "chưa đầy đủ" màu cảnh báo + tooltip hiện `reason` |
| `Reference.resolved = false` | Hiển thị mờ + ghi chú "không xác định được đích" |
| Vị trí source | Luôn hiện `file:line`, click để copy đường dẫn |

**Không được làm:**
- Ẩn mục Known Limitations khi rỗng (phải hiện dòng "không có giới hạn nào được ghi nhận")
- Làm tròn hoặc lược bớt số liệu trong `RunMetrics` cho gọn
- Dùng màu/biểu tượng khiến `inferred` trông như `exact`, hoặc `partial` trông như `full`
- Thêm biểu đồ hay con số không suy ra được từ IAM

### 13.5 Ràng buộc kỹ thuật

- Không framework nặng; ưu tiên HTML + CSS + JS thuần hoặc một thư viện nhỏ cho phần đồ thị
- Không gọi mạng ra ngoài (không CDN) — mọi thứ nằm trong thư mục output, mở được offline
- Chạy được trên trình duyệt hiện hành, không cần cài thêm gì
- Hỗ trợ cả nền sáng và nền tối
- Bảng dài phải cuộn được trong khung riêng, trang không tràn ngang

### 13.6 Tiêu chí nghiệm thu cho UI

1. Xoá thư mục UI → chạy `l3gen <path>` vẫn cho ra 4 file output đúng như trước (kiểm bằng cách so sánh file).
2. Mở UI ở chế độ máy bay (ngắt mạng) → mọi màn hình vẫn hiển thị đầy đủ.
3. Lấy ngẫu nhiên 10 dòng bất kỳ trên UI → cả 10 đều truy được về đúng một phần tử trong `IAM.json`.
4. Chạy tool với `--no-ai` rồi mở UI → màn U-05 hiện thông báo bước AI không chạy, không phải màn trống không giải thích.
5. Một người chưa biết dự án mở UI → trong 2 phút nói được service có bao nhiêu route, chỗ nào là suy ra và chỗ nào còn thiếu dữ liệu.

### 13.7 Ước tính công sức

| Hạng mục | Ước tính |
|---|---|
| Sinh thêm `IAM.json` + lệnh `l3gen ui` | 0,5 ngày |
| U-01 Tổng quan + U-06 Known Limitations | 0,5 ngày |
| U-02 Routes + U-03 Entities (bảng, lọc, panel chi tiết) | 1 ngày |
| U-04 Dependency Graph tương tác | 1,5 ngày |
| U-05 Review Findings | 0,5 ngày |
| Nền sáng/tối, tinh chỉnh, kiểm nghiệm thu | 1 ngày |
| **Tổng** | **~5 ngày** |

**Thứ tự ưu tiên nếu thiếu thời gian:** U-01 → U-02 → U-04 → U-05 → U-03 → U-06. Ba màn đầu đã đủ để trình bày; các màn sau tăng độ hoàn chỉnh.

---

## 14. Cấu trúc thư mục project

Cấu trúc này được thiết kế để **thêm ngôn ngữ/framework mới không phải sửa code đã có**. Giai đoạn đầu chỉ có Python/FastAPI, nhưng khung thư mục đã đúng chỗ ngay từ đầu để việc mở rộng chỉ là thêm file, không phải tái cấu trúc.

### 14.1 Cây thư mục

```
code-to-l3/
├── src/l3gen/
│   ├── __init__.py
│   ├── cli.py                      # điểm vào CLI (mục 4.2)
│   ├── pipeline.py                 # điều phối các bước 1 → 6b
│   │
│   ├── models/                     # ← IAM, dùng chung mọi ngôn ngữ
│   │   ├── iam.py                  # IntermediateArchitectureModel, APIRoute, DBEntity...
│   │   ├── graph.py                # GraphNode, GraphEdge (mục 5.2)
│   │   ├── findings.py             # ReviewFinding (mục 6b.1)
│   │   └── stack.py                # ServiceUnit, DetectedStack (mục 4.4.7)
│   │
│   ├── detection/                  # ← bước 1b
│   │   ├── discovery.py            # tìm ranh giới service theo manifest (mục 4.4.2)
│   │   ├── detector.py             # nhận diện ngôn ngữ + framework mỗi đơn vị (4.4.3-4.4.4)
│   │   └── signatures.py           # bảng dấu hiệu manifest + import
│   │
│   ├── languages/                  # ← TÁCH THEO NGÔN NGỮ TRƯỚC
│   │   ├── base.py                 # giao diện chung: parse(file) → cây cú pháp
│   │   │
│   │   ├── python/
│   │   │   ├── parser.py           # dùng module `ast` chuẩn
│   │   │   ├── resolution.py       # LUẬT RIÊNG của Python: module path,
│   │   │   │                       #   suy kiểu biến, MRO đơn giản hoá (15.2, 15.4c)
│   │   │   ├── common/             # extractor dùng chung cho MỌI framework Python
│   │   │   │   ├── imports.py      # ImportExtractor (bước 3e)
│   │   │   │   └── callgraph.py    # CallGraphExtractor (bước 3d)
│   │   │   └── frameworks/
│   │   │       ├── fastapi/        # ← PHẠM VI HIỆN TẠI
│   │   │       │   ├── routes.py   # @app.get, APIRouter, include_router
│   │   │       │   └── external.py # httpx, requests
│   │   │       ├── flask/          # (mở rộng sau)
│   │   │       └── django/         # (mở rộng sau)
│   │   │
│   │   └── java/                   # (mở rộng sau — cần parser riêng)
│   │       ├── parser.py           # tree-sitter hoặc javalang
│   │       ├── resolution.py       # luật riêng của Java: package/classpath
│   │       └── frameworks/spring/
│   │
│   ├── orm/                        # ← ORM tách riêng khỏi framework
│   │   ├── base.py
│   │   ├── sqlalchemy.py           # ← PHẠM VI HIỆN TẠI
│   │   ├── django_orm.py           # (mở rộng sau)
│   │   └── jpa.py                  # (mở rộng sau)
│   │
│   ├── core/                       # ← KHÔNG phụ thuộc ngôn ngữ nào
│   │   ├── builder.py              # Model Builder (bước 4)
│   │   ├── graph_builder.py        # Graph Builder (bước 4c)
│   │   ├── evidence.py             # quy tắc gán confidence/completeness (mục 5.1)
│   │   └── resolution/             # khung resolve, KHÔNG chứa luật của ngôn ngữ nào
│   │       ├── orchestrator.py     # điều phối 4 bước của mục 15.2
│   │       ├── symbol_table.py     # bảng import THEO FILE (mục 15.3)
│   │       └── inheritance.py      # leo kế thừa: chặn vòng, giới hạn tầng (15.4b/d)
│   │
│   ├── ai/
│   │   ├── enrichment.py           # bước 5
│   │   ├── reviewer.py             # bước 6b
│   │   └── schemas.py              # schema khoá cứng output LLM
│   │
│   ├── output/
│   │   ├── markdown.py             # sinh L3.md (mục 7)
│   │   ├── mermaid.py              # sinh diagram.mmd
│   │   └── json_export.py          # sinh graph.json, IAM.json
│   │
│   └── ui/                         # ← phần mở rộng (mục 13)
│       ├── server.py               # phục vụ static, lệnh `l3gen ui`
│       └── static/                 # HTML/CSS/JS
│
├── tests/
│   ├── fixtures/
│   │   ├── python/fastapi/         # fixture 1-7: route, entity, external, cross-file
│   │   ├── python/resolution/      # fixture 8-12: các ca khó của mục 15.4
│   │   ├── python/flask/           # (mở rộng sau)
│   │   └── detection/              # repo mẫu nhiều service để test bước 1b
│   ├── unit/
│   └── integration/
│
├── examples/                       # output đã sinh sẵn (mục 12.3)
├── docs/
│   ├── USE_CASES.md
│   ├── SCENARIOS.md
│   └── diagrams/
├── README.md
├── EVALUATION.md
├── SPEC_Code_to_L3_Generator.md
└── pyproject.toml
```

### 14.2 Bốn quy tắc phụ thuộc

Đây là phần quan trọng hơn cây thư mục — cây thư mục chỉ là hệ quả của bốn quy tắc này:

1. **`core/` không được import từ `languages/`.** Graph builder và quy tắc confidence/completeness làm việc trên IAM đã chuẩn hoá, không cần biết dữ liệu đến từ Python hay Java.

   **Ngoại lệ có kiểm soát — resolution (mục 15).** Resolve tham chiếu *bản chất* phụ thuộc ngôn ngữ: Python tra theo module path, Java theo package/classpath, mỗi ngôn ngữ một quy tắc suy kiểu biến riêng. Nhưng *khung* thì chung: bốn bước ở 15.2, bảng import theo file ở 15.3, chặn vòng và giới hạn tầng ở 15.4. Nên tách làm hai:

   ```
   core/resolution/        ← khung: điều phối 4 bước, cấu trúc bảng ký hiệu,
                             thuật toán leo kế thừa (chặn vòng, đếm tầng)
                             KHÔNG biết cú pháp của ngôn ngữ nào

   languages/<lang>/resolution.py  ← luật riêng: "module path của ngôn ngữ này
                             viết thế nào", "suy kiểu biến từ đâu",
                             "đa kế thừa giải quyết ra sao"
   ```

   `core/resolution/` gọi xuống qua một giao diện hẹp (cho tên + ngữ cảnh file, nhận về đường dẫn file hoặc `None`). Đây **không phải** vi phạm quy tắc — `core/` vẫn không import trực tiếp module Python hay Java nào, nó nhận đối tượng luật được truyền vào từ pipeline sau khi bước 1b đã xác định ngôn ngữ.

2. **`languages/<lang>/frameworks/<fw>/` chỉ biết framework của chính nó.** FastAPI extractor không được import gì từ thư mục Flask. Hai framework không bao giờ gọi nhau.

3. **`orm/` tách khỏi `frameworks/`.** Một project FastAPI có thể dùng SQLAlchemy; một project Flask cũng vậy. Gắn ORM vào framework sẽ phải viết lại cùng một logic hai lần.

4. **`ui/` chỉ đọc output, không import gì từ `core/` hay `languages/`** (mục 13.1). Xoá cả thư mục đi thì phần còn lại vẫn chạy.

### 14.3 Thêm một framework mới cần làm gì

**Trường hợp A — framework cùng ngôn ngữ đã hỗ trợ** (ví dụ thêm Flask):

1. Thêm dấu hiệu nhận diện vào `detection/signatures.py`
2. Tạo `languages/python/frameworks/flask/routes.py`
3. Thêm fixture vào `tests/fixtures/python/flask/`
4. Cập nhật ma trận hỗ trợ (mục 4.4.5)

Không đụng tới `core/`, không đụng tới parser, **không đụng tới `languages/python/resolution.py`** (luật resolve của Python không đổi khi thêm framework), không đụng tới framework khác. Đây là trường hợp mà việc mở rộng thực sự chủ yếu là viết rule.

**Trường hợp B — ngôn ngữ mới** (ví dụ thêm Java):

1. Bốn bước như trên, cộng thêm:
2. Viết `languages/java/parser.py` với thư viện parse riêng
3. Viết lớp ánh xạ từ cây cú pháp của thư viện đó về IAM
4. Viết `languages/java/resolution.py` — luật riêng của ngôn ngữ: Java dùng package/classpath thay vì module path, khai báo kiểu tường minh nên suy kiểu biến dễ hơn Python, nhưng `interface` và generic thì phức tạp hơn

`core/resolution/` **dùng lại được nguyên vẹn** — khung bốn bước, chặn vòng, giới hạn tầng không đổi theo ngôn ngữ. Bước 2 và 3 là phần tốn công nhất và không tái sử dụng được gì từ Python.

### 14.4 Vì sao dựng sẵn thư mục rỗng cho phần chưa làm

Thông thường không nên tạo abstraction cho code chưa tồn tại. Ở đây có ngoại lệ, vì đa ngôn ngữ là **mục tiêu đã xác định từ đầu**, không phải khả năng giả định.

Cái giá phải trả nếu bỏ qua: khi tất cả extractor FastAPI nằm phẳng trong `src/l3gen/extractors/`, việc thêm Flask buộc phải di chuyển file, sửa mọi câu lệnh import, và rất dễ để logic hai framework dính vào nhau trong lúc dọn dẹp. Chi phí đó lớn hơn nhiều so với việc tạo sẵn vài thư mục ngay từ đầu.

**Tuy nhiên:** chỉ tạo **thư mục**, không tạo file rỗng, không viết lớp cơ sở trừu tượng cho thứ chưa có người kế thừa. `languages/base.py` chỉ nên xuất hiện khi đã có ngôn ngữ thứ hai để biết phần chung thực sự là gì — viết trước khi đó là đoán mò.

---

## 15. Thách thức kỹ thuật — Reference Resolution

Mục này đặc tả phần khó nhất của dự án: từ một lời gọi trong code, xác định nó trỏ tới định nghĩa nào, ở file nào. Các mục trước nói *phải làm gì*; mục này nói *làm thế nào* và *gãy ở đâu*.

**Vì sao tách riêng:** những việc còn lại (nhận diện ngôn ngữ, chia service, tìm decorator, dựng graph) đều là tra bảng hoặc duyệt cây — làm đúng là xong. Riêng resolution đòi hỏi suy ra thông tin không có sẵn trong cú pháp, và đó là chỗ duy nhất mà lựa chọn thiết kế sai sẽ tạo ra kết quả *trông đúng mà sai*.

### 15.1 Bài toán

```python
# api/orders.py
from services.order import OrderService

@router.post("/orders")
def create_order(data: OrderIn):
    svc = OrderService()
    return svc.create(data)      # ← svc.create là gì? ở đâu?
```

AST cho biết *có một lời gọi tên `svc.create`*. Nó **không** cho biết `svc` là instance của class nào — đó là thông tin ngữ nghĩa, không phải cú pháp. Phải tự suy ra.

### 15.2 Thuật toán bốn bước

```
[1] Xác định kiểu của biến nhận (receiver)
    svc = OrderService()  → svc có kiểu OrderService
    Nguồn suy ra, theo thứ tự ưu tiên:
      a. gán trực tiếp trong cùng hàm:  svc = OrderService()
      b. type annotation của tham số:   def f(svc: OrderService)
      c. type annotation của biến:      svc: OrderService = ...
      d. không có nguồn nào → DỪNG, resolved = False

[2] Tra tên class về file
    OrderService → tra bảng import của CHÍNH file đang xét (api/orders.py)
      · from services.order import OrderService → "services/order.py"
      · không có trong bảng import → tìm định nghĩa ngay trong file hiện tại
      · vẫn không thấy → DỪNG, resolved = False (có thể là thư viện ngoài)

[3] Tìm method trong class đó
    Mở services/order.py, tìm class OrderService, tìm method create
      · thấy → resolved = True, resolved_module = "services/order.py"
      · không thấy → sang bước 4 (leo kế thừa)

[4] Leo chuỗi kế thừa
    class OrderService(BaseService)  → lặp lại bước 2-3 với BaseService
    Xem quy tắc chi tiết ở 15.4
```

**Nguyên tắc xuyên suốt:** mỗi bước chỉ được kết luận khi có bằng chứng cú pháp trực tiếp. Không có bằng chứng thì dừng và ghi `resolved = False` — không suy đoán tiếp bằng heuristic.

### 15.3 Bảng import phải gắn với file, không phải toàn cục

Đây là lỗi kinh điển khi làm loại tool này, và nó âm thầm cho ra kết quả sai:

```python
# api/orders.py
from services.order import OrderService      # → services/order.py

# legacy/handler.py
from legacy.order import OrderService        # → legacy/order.py  (KHÁC!)
```

Cùng tên `OrderService`, hai định nghĩa khác nhau. Nếu tra theo bảng toàn cục kiểu `{"OrderService": "services/order.py"}`, mọi lời gọi trong `legacy/handler.py` sẽ bị gán nhầm sang file sai — **và không có cách nào phát hiện qua test thông thường**, vì kết quả vẫn hợp lệ về mặt cấu trúc.

**Bắt buộc:** bảng import là `dict[file_path, dict[local_name, module_path]]`. Mọi tra cứu phải bắt đầu từ file chứa lời gọi.

### 15.4 Kế thừa xuyên file — quy tắc bắt buộc

Trường hợp cơ bản giải được đơn giản: đọc `class OrderService(BaseService)`, lấy tên `BaseService`, tra bảng import của chính file đó để biết `BaseService` nằm ở đâu, mở file đó tìm tiếp. Lặp lại cho tới khi tìm thấy method hoặc hết đường.

Bốn trường hợp cần quy định rõ vì chúng không tự nhiên:

**(a) Class cha nằm ngoài repo**

```python
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase): ...        # DeclarativeBase không có trong repo
```

Leo tới đây là hết đường. Ghi `resolved = False` với lý do "class cha thuộc thư viện ngoài phạm vi quét". **Không được coi là lỗi** — đây là kết quả đúng.

**(b) Nhiều tầng kế thừa**

```
OrderService(BaseService) → BaseService(AbstractService) → AbstractService(Base)
```

Leo tuần tự từng tầng. **Giới hạn cứng: tối đa 10 tầng.** Vượt quá thì dừng, ghi `unresolved_references` với lý do "chuỗi kế thừa quá sâu". Giới hạn này tồn tại để phòng trường hợp bệnh lý, không phải vì 10 tầng là hợp lý.

**(c) Đa kế thừa**

```python
class OrderService(BaseService, LoggingMixin):
    pass    # create() nằm ở cả hai class cha
```

Python dùng MRO (thứ tự trái sang phải, chiều sâu trước). Spec này **không tái hiện đầy đủ MRO** — quá phức tạp so với giá trị mang lại. Quy tắc đơn giản hoá:

- Duyệt các class cha theo thứ tự khai báo, lấy kết quả đầu tiên tìm thấy
- Nếu tìm thấy method **ở nhiều hơn một** class cha: vẫn lấy cái đầu tiên, gán `confidence = inferred`, `completeness = full`, với `reason = "đa kế thừa, chọn class cha đầu tiên theo quy tắc đơn giản hoá"`
- Ghi rõ trong Known Limitations rằng tool không tái hiện MRO đầy đủ

**(d) Kế thừa vòng**

```python
# a.py: class A(B)
# b.py: class B(A)      ← code sai, nhưng vẫn parse được
```

Không chặn thì lặp vô hạn. **Bắt buộc:** giữ một tập các class đã đi qua trong lần leo hiện tại; gặp lại class đã có trong tập thì dừng ngay, ghi `unresolved_references` với lý do "phát hiện kế thừa vòng". Tool phân tích code hỏng vẫn phải chạy được, không được treo.

### 15.5 Các trường hợp dừng — bảng tổng hợp

Mọi trường hợp dưới đây đều cho `resolved = False`. Điều quan trọng là **`reason` phải nêu đúng nguyên nhân**, vì đó là thứ giúp người đọc phân biệt "tool chưa làm được" với "code có vấn đề":

| Tình huống | Lý do ghi vào kết quả |
|---|---|
| Không suy được kiểu của biến nhận | "không xác định được kiểu của `svc`" |
| Biến đến từ `Depends(...)` | "tham số inject qua Depends, ngoài phạm vi phân tích" |
| Tên không có trong bảng import và không định nghĩa trong file | "không tìm thấy định nghĩa trong phạm vi repo" |
| Class cha thuộc thư viện ngoài | "class cha thuộc thư viện ngoài phạm vi quét" |
| Chuỗi kế thừa vượt 10 tầng | "chuỗi kế thừa quá sâu" |
| Phát hiện kế thừa vòng | "phát hiện kế thừa vòng" |
| Gọi qua biến động (`getattr`, dict lookup) | "lời gọi động, không phân tích tĩnh được" |

### 15.6 Ranh giới không được vượt qua

Đây là phần quan trọng nhất của cả mục 15. Khi code thật, mỗi lần gặp trường hợp không resolve được sẽ xuất hiện cám dỗ "thêm một heuristic nữa cho đẹp số liệu". Ba thứ bị cấm:

**Cấm 1 — đoán theo tên.** Thấy `svc.create` và trong repo có đúng một class tên `OrderService` có method `create` thì **không được** kết luận đó là nó. Trùng tên không phải bằng chứng.

**Cấm 2 — đoán theo vị trí thư mục.** Thấy lời gọi trong `api/` và có file `services/` cùng tên thì không được suy ra quan hệ. Quy ước đặt tên không phải bằng chứng.

**Cấm 3 — dùng AI để lấp chỗ trống.** Đây là vi phạm trực tiếp mục 3.1. Nếu static analysis không resolve được, kết quả đúng là "không resolve được", không phải "hỏi LLM xem nó nghĩ là gì".

**Phép thử khi phân vân:** nếu phải giải thích cho người khác vì sao lời gọi này trỏ tới file kia, mà lời giải thích không chỉ ra được **một dòng code cụ thể** làm bằng chứng, thì đó là suy đoán — ghi `resolved = False`.

### 15.7 Vì sao đây là phần khó nhất

Không phải vì thuật toán phức tạp — bốn bước ở 15.2 đều là tra bảng. Khó ở hai chỗ khác:

**Thứ nhất, sai mà không biết mình sai.** Bảng import toàn cục (15.3) vẫn cho ra graph đầy đủ, đẹp mắt, chạy qua mọi test cấu trúc — chỉ có điều một số cạnh trỏ sai file. Không có ground truth thủ công (mục 8.5) thì không cách nào phát hiện.

**Thứ hai, ranh giới "biết" và "đoán" rất mờ trong lúc code.** Mỗi heuristic thêm vào đều làm số liệu đẹp hơn và có vẻ hợp lý tại thời điểm viết. Chỉ khi cộng dồn mới thành một tool cho ra kết quả tự tin mà không đáng tin — đúng thứ mà toàn bộ spec này được viết ra để tránh.

**Giải thích dễ hiểu:** Giống như lần theo dấu chân trong rừng. Chỗ đất mềm in rõ dấu thì đi tiếp được. Tới chỗ đá không còn dấu, có hai lựa chọn: dừng lại ghi "mất dấu tại đây", hoặc đoán bừa một hướng rồi đi tiếp. Người đoán bừa sẽ vẽ ra tấm bản đồ dài hơn, đầy đủ hơn — và sai. Tệ nhất là người đọc bản đồ không phân biệt được đoạn nào dựa trên dấu thật, đoạn nào dựa trên phỏng đoán. `resolved`, `confidence` và `completeness` tồn tại để tách ba câu hỏi: đã tìm được đích chưa, kết luận dựa trên bằng chứng trực tiếp hay suy ra, và dữ liệu đã đủ hay chưa.

### 15.8 Thứ tự triển khai đề xuất

Làm theo thứ tự này để mỗi bước đều kiểm chứng được trước khi sang bước sau:

1. Bảng import theo từng file (15.3) — nền tảng, sai chỗ này thì mọi thứ sau đều sai
2. Resolve lời gọi hàm tự do: `create_order(...)` — không cần suy kiểu biến
3. Suy kiểu biến từ gán trực tiếp: `svc = OrderService()` (15.2 bước 1a)
4. Resolve method trong chính class đó (15.2 bước 3)
5. Leo kế thừa một tầng (15.4 cơ bản)
6. Leo nhiều tầng + chặn vòng + giới hạn độ sâu (15.4b, 15.4d)
7. Suy kiểu từ type annotation (15.2 bước 1b, 1c)
8. Đa kế thừa (15.4c) — làm cuối vì ít gặp nhất và quy tắc đã đơn giản hoá

Sau mỗi bước, chạy lại toàn bộ fixture và ghi lại tỷ lệ resolve được. Tỷ lệ này chỉ được tăng — nếu một thay đổi làm nó giảm, đó là hồi quy cần tìm nguyên nhân ngay.
