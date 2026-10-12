# L3 Generator — bản đọc để báo cáo mentor ngày 02/10/2026

Ngày kiểm tra và chạy: **01/10/2026**. Đây là tài liệu giải thích và kịch bản trình bày, không thay PRD, không ký duyệt thay nhóm.

## 1. Nếu chỉ nhớ một đoạn

> Nhóm em làm công cụ đọc mã nguồn để tạo bản mô tả kiến trúc ban đầu. Phần của Khiêm nhận repository, dùng phân tích tĩnh kết hợp LLM để chia khối, đặt tên và dựng sơ đồ có trích dẫn code. Phần của em sinh tài liệu contract theo từng component: API, bảng dữ liệu và sự kiện. Mỗi tài liệu có bảng cho người đọc, khối dữ liệu cho máy và thông tin truy về nguồn. Hai phần đã có các lần chạy riêng; nhóm chưa chứng minh một luồng tích hợp hoàn chỉnh từ graph v8 tới toàn bộ tài liệu L3.

**Không nói “đã hoàn thành toàn bộ sản phẩm” hoặc “đạt 90–100% chất lượng”.** Có kết quả demo thật, có giới hạn và có lỗi cần sửa.

## 2. Đọc đúng tài liệu và đúng phiên bản

| Nguồn | Vai trò | Trạng thái được đọc |
|---|---|---|
| [PRD](../.aide/product/prd/PRD-L3GEN-2609-001.md) | Sản phẩm cần làm gì, cho ai, phạm vi và đo thế nào | Revision 28, draft |
| [FR-019…027](../.aide/requirements/fr/) | Yêu cầu chức năng và AC cụ thể | 9 FR; chỉ mục PRD ghi 36 AC |
| [NFR](../.aide/requirements/nfr/) | Chất lượng, bảo mật, tài nguyên, giới hạn AI | 5 NFR hiện hành |
| [OBS-001](../.aide/observability/OBS-L3GEN-001.md) | Cách tổ chức phép đo và đáp án | Kết quả nghiệm thu chưa được xác nhận |
| [Bộ thiết kế L3](../.aide/tech-specs/README.md) | Giao diện và schema trao đổi giữa các module của chính L3 Generator | 8 contract draft revision 4 |
| [Code của em](../slice/README.md) | Lát triển khai từ source local tới output L3 | CLI cần membership soạn sẵn |
| [Bản Khiêm](../../l3-generator-quote-evidence/docs/BAO-CAO-SO-DO-COMPONENT.md) | Thử nghiệm sơ đồ component v8 | Demo chạy commit `a14d32c`; checkout sau đó lên `42d0468` (Pyright/v10) |

Bản PRD r23 trong lịch sử có 18 FR và AI chủ yếu diễn giải. **Không dùng bản đó để mô tả hướng hiện tại.** Bộ mới đổi vai trò AI và dùng FR-019…027. Approval cũ BL-r14 đã superseded theo PRD r28.

Một số đoạn hành chính trong PRD r28 vẫn nhắc revision 25, BL-r1, hoặc “chưa có L1/L2”; README nhắc BL-r5 và thư mục thiết kế đã có. Vì vậy khi mentor hỏi đã ký chưa, trả lời: **bộ đang review, chưa có căn cứ trong các file đã đọc để tuyên bố baseline mới đã được duyệt**. Đừng đọc trạng thái cũ thành sự thật hiện tại.

## 3. PRD là gì, đọc để trả lời những câu nào?

PRD là tài liệu yêu cầu sản phẩm. Nó trả lời: giải quyết vấn đề gì, ai dùng, đầu vào/đầu ra là gì, làm đến đâu và thế nào là đạt. Nó không phải danh sách code đã hoàn thành.

| Mục PRD | Hiểu đơn giản | Cách nói khi báo cáo |
|---|---|---|
| I. Thông tin | Ai chịu trách nhiệm, nguồn yêu cầu, lịch sử | Khiêm đầu mối Product; Hoàng review/UAT; mentor cố vấn/reviewer |
| II. Tổng quan | Vấn đề, mục tiêu, chỉ số | Tạo kiến trúc ban đầu có thể kiểm chứng bằng code |
| III. Bối cảnh | Người dùng, giả định, ràng buộc, phụ thuộc | Ưu tiên developer tiếp quản repo Python/FastAPI |
| IV. Yêu cầu | Trong/ngoài phạm vi, FR và NFR | Phân biệt cam kết sản phẩm với code thử nghiệm |
| V. Luồng | Người dùng làm gì, công cụ trả gì, lỗi xử lý sao | Local qua CLI; ZIP/GitHub public qua web là yêu cầu |
| VI. DoD | Điều kiện đủ để bàn giao | AC đạt, NFR có phép đo, code/test review, có evidence |
| VII. Thiết kế | Màn hình/góc nhìn cần có | Không dùng bảng màn hình để nói UI đã hoạt động |
| VIII. Phasing | Thứ tự mốc nội bộ | M0 yêu cầu; M1 lõi; M2 mô hình/web; M3 hoàn thiện và đánh giá |
| IX. Phê duyệt | Ai duyệt bộ revision nào | Review/approval phải gắn đúng tài liệu; không tự nhận đã ký |

Lịch cũ 11/09–09/10 **không còn là lịch cam kết mới trong mục VIII của r28**. Mục này yêu cầu đặt lại lịch sau Scope Gate.

### Vấn đề và người dùng

Developer mới vào một repo phải lần theo route, service, model dữ liệu và tích hợp. Tài liệu viết tay có thể cũ. Một sơ đồ chỉ có function thì quá chi tiết; một sơ đồ do AI đoán mà không có bằng chứng thì khó tin.

Sản phẩm giúp đọc tổng quan trước, mở chi tiết sau và kiểm lại kết luận tại source. Architect dùng để review dependency; platform engineer có thể dùng lại JSON. Public job API/lịch sử thuộc phase sau, không phải đã có ở demo.

### Bốn goal hiện hành

| Goal | Yêu cầu | Ví dụ chứng minh |
|---|---|---|
| GOAL-004 | Dựng sơ đồ application/component | Thấy API → nghiệp vụ → dữ liệu; đối chiếu membership và cạnh |
| GOAL-005 | Kết luận truy được về source | Chọn cạnh, chỉ ra file và dòng tạo ra quan hệ |
| GOAL-006 | Sinh tài liệu L3 từ cùng mô hình | API có endpoint, TBL có cột, EVT có điểm gửi/nhận |
| GOAL-007 | Công bố mức chắc chắn và giới hạn | Không biết auth/broker thì ghi unknown; không tự điền cho đẹp |

**Phần của em đóng góp trực tiếp vào GOAL-006, đồng thời phải giữ GOAL-005 và GOAL-007.** Golden test là công cụ kiểm các goal, không phải một chức năng sản phẩm độc lập để người dùng cuối sử dụng.

## 4. FR, AC, NFR, OBS khác nhau thế nào?

- **FR — Functional Requirement:** sản phẩm làm được việc gì. Ví dụ: sinh contract API.
- **AC — Acceptance Criteria:** tình huống và kết quả cụ thể để biết FR đã đạt. Ví dụ: có route thì file API phải giữ method, full path, status, evidence và khối OpenAPI cùng nội dung.
- **NFR — Non-functional Requirement:** làm với chất lượng/ràng buộc nào. Ví dụ: không thực thi source, không bịa dữ kiện, giới hạn tài nguyên.
- **OBS:** lấy dữ liệu nào, lập đáp án thế nào, dùng công thức nào để đo KPI/NFR.

Ví dụ xuyên suốt: source khai báo `GET /items`, status `200` → FR-027 yêu cầu sinh API → AC-027-01 kiểm bảng và OpenAPI cùng ghi đúng → NFR-ACC-002 yêu cầu dữ kiện/bằng chứng đúng → OBS quy định chấm trên đáp án độc lập. “File sinh được” mới trả lời một phần, chưa đủ để nói “đúng”.

### Chín FR cần thuộc

| FR | Nội dung dễ hiểu | Liên quan phần em |
|---|---|---|
| 019 | Nhận source, kiểm đầu vào, bắt đầu chạy | Đầu vào phải đúng snapshot; export không ghi vào source |
| 020 | Nói rõ phần nào được phân tích/bỏ qua | Giới hạn phải đi theo tài liệu |
| 021 | Trích route/model/table/HTTP/config/event/library/reference | Cung cấp nguyên liệu; renderer không tự đoán phần còn thiếu |
| 022 | Dựng component và quan hệ, sử dụng LLM | Cung cấp membership và mô hình; D-03 chưa chốt trong bộ L3 |
| 023 | Evidence và nhãn chất lượng | Tài liệu giữ fact ID, evidence ID, file:dòng, confidence/completeness |
| 024 | Công bố giới hạn/lỗi một phần | README và notices phải nói rõ phần thiếu |
| 025 | Xuất JSON, sơ đồ, tài liệu và mã sơ đồ | Phần export, manifest, định dạng, parity, retry |
| 026 | Xem/tìm/lọc/kiểm bằng chứng trên web | UI tiêu thụ cùng kết quả; hiện chưa demo web full của slice |
| 027 | Sinh API/TBL/EVT theo component | Trọng tâm công việc L3 của em |

### Năm NFR và cách giải thích

| NFR | Điều quan trọng | Chưa nên tuyên bố |
|---|---|---|
| ACC-002 | Precision và recall ≥80% riêng từng nhóm khi đủ mẫu; evidence hợp lệ 100%; nhãn đúng ≥80%; false-exact ≤5% | Một repo demo đạt 100% không chứng minh toàn hệ thống đạt |
| ABST-002 | Sơ đồ ở mức application/component; trần 50 node theo contract hiện tại | Không gọi hình vẽ toàn bộ hàm là sơ đồ component đạt yêu cầu |
| AI-002 | Giới hạn dữ liệu gửi, ngân sách, provider và provenance | GPT-5.6 Sol tính phí của demo không tự trở thành cấu hình PRD đã duyệt |
| SEC-002 | Read-only source, intake an toàn, che bí mật, quản lý vòng đời dữ liệu | Không nói đã qua security review chỉ vì demo không lỗi |
| OPS-001 | 60s/5k dòng và 300s/50k dòng cho phần tĩnh+ghi; 2 GiB; toàn run 30 phút; 1 run cùng lúc | Demo 15 file không chứng minh các trần NFR này |

Máy đo chuẩn OPS ghi 4 CPU logical, RAM 8 GiB, SSD, Python 3.12. Cấu hình khác phải công bố. Thời gian API demo chỉ là thời gian của lần chạy này.

## 5. Phạm vi và những điều phải nói đúng

**Phase đầu:** Python/FastAPI; source local/ZIP/GitHub public theo hai kênh; phân tích tĩnh; component và dependency; evidence; API/TBL/EVT; JSON và diagram. Phạm vi event trong PRD là Kafka.

**Ngoài phase đầu:** mọi framework/ngôn ngữ, Java/Spring Boot, Git private/SSO/multi-tenant, chạy source để khám phá runtime, sửa code tự động, drift/impact/incremental, lịch sử nhiều lần chạy, SLA production.

LLM được đưa vào phần phân tích chính theo hướng mới. Nhưng **công đoạn render L3 từ dữ liệu đã có không nhất thiết cần LLM**. Hai câu này không mâu thuẫn: một câu nói cả sản phẩm, một câu nói module xuất tài liệu.

Source không cho biết đầy đủ mọi thứ. Route prefix động, kiểu được tạo lúc chạy, auth nằm ngoài phạm vi có thể chưa xác định. “Unknown” có lý do là kết quả trung thực, không được thay bằng `200`, `nullable=false`, PostgreSQL hoặc tên component đoán.

## 6. Phân biệt hai nghĩa của “L3”

1. **Thiết kế L3 của chính công cụ:** `.aide/tech-specs/` định nghĩa giao diện, input/output, schema, lỗi, invariant của module 001…008. Đây là tài liệu để nhóm viết code tương thích.
2. **Tài liệu L3 công cụ sinh cho repo người dùng:** `output/tech-specs/<component>/api|schema|events`. Đây là tính năng FR-027.

Em vừa có bộ thiết kế contract cho công cụ, vừa triển khai chức năng sinh contract. Đừng chỉ mở `.aide/tech-specs` rồi gọi đó là output phân tích repo mẫu.

Trong tài liệu nhóm, sơ đồ component được gọi “L2”, còn “L3” là API/TBL/EVT theo quy trình mentor. **Đây là cách dùng cấp độ trong quy trình nhóm; không tự đồng nhất với tên Level 2/3 của mô hình C4 chuẩn.** Khi trình bày, dùng “sơ đồ component” và “tài liệu contract” để tránh nhầm.

## 7. Luồng toàn sản phẩm mong muốn

```text
Local/ZIP/GitHub
  → snapshot: nhận diện đúng phiên bản source
  → inventory: phạm vi file/đơn vị phân tích
  → FactSet: dữ kiện và vị trí source
  → ArchitectureModel: component, thành viên, cạnh, chủ sở hữu contract
       ↔ LLM: đề xuất/đặt tên/diễn giải, có kiểm chứng
  → VerifiedResult: bộ dữ liệu đã qua kiểm tra
  → renderer: README + JSON + Mermaid/SVG + API/TBL/EVT
  → manifest: file nào ready/failed, hash, số byte, lỗi
  → CLI hoặc web dùng cùng kết quả
```

| Module thiết kế | Nhiệm vụ |
|---|---|
| CMP-001 | Điều phối CLI/web, trạng thái lần chạy |
| CMP-002 | Snapshot, đọc đúng file và phiên bản |
| CMP-003 | Kiểm kê/phạm vi |
| CMP-004 | Trích dữ kiện |
| CMP-005 | Mô hình component, cạnh, ownership |
| CMP-006 | Cổng LLM, quota và dữ liệu trao đổi |
| CMP-007 | Kiểm bằng chứng và kết luận |
| CMP-008 | Sinh artifact, kiểm định dạng/parity, publish/retry |

API-002…008 trong bộ thiết kế là giao diện nội bộ, **không có nghĩa phải dựng bảy HTTP microservice**.

## 8. Phần Khiêm đang làm cụ thể

Checkout: `D:\VSF\l3-generator-quote-evidence`. Code chính ở `experiments/quote-evidence/`.

| Bước thực tế v8 | Code chính | Hiểu đơn giản |
|---|---|---|
| Quét source | `inventory.py` | Chọn file, băm nội dung, ghi phần loại trừ |
| Đọc cú pháp | `pyindex.py`, `calls.py` | Tìm symbol, import, lời gọi và dấu hiệu framework |
| Phân loại luồng | `flow.py` | Phân biệt xử lý chính, lắp ráp, kiểm tra, truyền session |
| Bản nháp | `draft.py` | Dùng dữ kiện tạo phương án nhóm ban đầu |
| Đề xuất khối | `ai7.py`: `top_blocks/group` | AI đọc tóm tắt toàn repo, nhận bản nháp, trả nhóm và mã dòng |
| Kiểm và xếp file | `ai7.py` | Kiểm đề xuất; hỏi lại một lần khi vi phạm; file mơ hồ xử lý riêng |
| Dựng/chọn cạnh | `flow.py`, `ai7.py`: `check_edges` | Code dựng từ lời gọi; AI có thể phân loại cặp mơ hồ để quyết định có trình bày như luồng không |
| Đặt tên | `ai7.py`: `describe` | AI đặt tên tiếng Việt, mô tả, nhãn cạnh; trỏ mã dòng |
| Xuất/chấm | `run7.py`, `render.py`, `evaluate.py` | `graph.json`, `diagram.mmd`, `score.json` nếu cung cấp oracle |

**v8 vẫn chạy bằng file `run7.py`.** Tên file và một số metadata/docstring còn “v7”. Bản demo lưu rõ commit/code và ghi chú phiên bản, không đoán phiên bản chỉ từ tên file.

AI trả `L12`; code ánh xạ mã đó về file, dòng và nguyên văn. Điều này giảm lỗi AI chép sai. Nhưng **dòng code tồn tại chưa chứng minh toàn bộ cách chia khối đúng về ngữ nghĩa**. Vẫn cần đáp án/review riêng.

Sơ đồ v8 chủ đích giản lược để đọc luồng xử lý. Không phải mọi import đều được vẽ. Bỏ cạnh kiểm tra/lắp ráp/đi ngược tầng có thể hợp mục tiêu trình bày, nhưng cần phân biệt với mô hình đầy đủ và tiêu chí dependency trong PRD.

## 9. Phần L3 của em đang làm cụ thể

Checkout: `D:\VSF\l3-generator-l3`; code `slice/l3slice/`.

**Ranh giới cốt lõi:** nhận `VerifiedResult` rồi xuất đúng nội dung, không chia lại component, không tự thêm API/bảng/event.

### API

Với mỗi component sở hữu route, tạo một Markdown: bảng method/path/handler/request/response/status/auth và evidence; bên dưới có OpenAPI 3.1. Thiếu full path hoặc status thì giữ thông tin biết được và nói rõ vì sao operation bị bỏ khỏi khối máy. Hai app trùng method/path không được âm thầm chọn một handler.

### TBL

Mỗi component sở hữu bảng có Markdown mô tả cột, kiểu, PK, FK, nullable. DDL chỉ dựng từ trường đã biết và dialect đã chứng minh. Bảng thiếu trường bắt buộc hoặc kiểu ngoài catalogue thì bỏ cả bảng khỏi DDL, có notice; không bỏ một cột rồi khiến người xem tưởng bảng đầy đủ. DDL là mô tả tĩnh, **không chạy SQL**.

### EVT

Mỗi component có điểm gửi/nhận có tài liệu riêng. Hai nơi dùng cùng tên topic chưa đủ để nối cạnh: phải chứng minh broker/config tương ứng. Chưa biết payload thì schema mở có nhãn partial, không bịa cấu trúc. Không biết bên gửi vẫn có thể mô tả bên nhận.

### Manifest, consistency, retry

- `result.json`: dữ liệu chuẩn của lần chạy và context xuất.
- `manifest.json`: thêm danh sách artifact, trạng thái, SHA-256, bytes và lỗi.
- Markdown, sơ đồ và khối máy phải thống nhất **nội dung theo phạm vi biểu diễn**. Có thể có omission hợp lệ nhưng phải thông báo.
- Một artifact lỗi không có nghĩa mọi file đều hỏng. Retry artifact lỗi giữ byte của file đã ready, dùng lại dữ liệu và phiên bản renderer cũ.
- `generated: true`, `non_normative: true` nghĩa là bản sinh để review, không phải tài liệu đã được chủ repo ký duyệt.

Slice có bộ trích/verify và CLI để tự test đầu-cuối. Nhưng membership hiện lấy từ JSON soạn sẵn; nó không chứng minh đã giải xong thuật toán chia component tự động.

## 10. Hai phần đã nối chưa?

**Chưa có phép chạy xác nhận nối tự động hoàn chỉnh.** Bản v8 tạo graph gồm component/files/quote và cạnh. Renderer của em nhận VerifiedResult có FactSet, EvidenceRef, quyết định kiểm, owner contract và schema version.

| Đầu ra Khiêm | Đầu vào L3 cần | Việc cần làm |
|---|---|---|
| `components[].files` | `member_file_ids`, unit và partition version | Ánh xạ path tới file ID của cùng snapshot |
| `quote {file,line,text}` | EvidenceRef có hash, range và ID | Kiểm nguồn rồi tạo định danh; không giả hash |
| `edges {source,target,label}` | Edge có relation_type, fact_ids, evidence_ids, rule/provenance | Không lấy nhãn tiếng Việt làm loại quan hệ được chứng minh |
| Graph và mô tả | Route/model/table/event facts | Graph không tự có đủ request/response/column/payload; cần tầng trích dữ kiện |
| Không có đủ `contract_owners` | Chủ sở hữu từng API/TBL/EVT | Chốt quy tắc declaration-file, không gán theo nơi gọi |
| Kiểm quote | VerifiedResult/verdict | Đối chiếu kiểm cú pháp trích dẫn và kiểm ngữ nghĩa/binding |

**Thứ tự nối:** pin source chung → chốt ánh xạ/schema → một repo nhỏ qua hai phần → kiểm API/TBL/EVT và evidence → mở rộng. Không sửa adapter bằng cách tự điền những trường nguồn chưa cung cấp.

## 11. Những điểm PRD và code thử nghiệm chưa khớp

| Điểm | PRD/thiết kế | Code hiện tại | Cách nói |
|---|---|---|---|
| Chia component | Code chia; AI chia repo phẳng | V8 cho AI đề xuất nhóm từ trên xuống trên repo thông thường | Thử nghiệm mới, cần đồng bộ quyết định thiết kế |
| Provider/chi phí | Groq/Google, quota miễn phí, trần trả phí 0 | Khiêm đo OpenRouter; demo này dùng OpenAI theo yêu cầu Hoàng | Được phép cho lần demo này, không tự thay baseline sản phẩm |
| Chất lượng cạnh | ACC: P/R ≥80% khi đủ mẫu | Báo cáo thử nghiệm dùng P≥80%, R≥60%, có P chặt/lỏng | Không dùng ngưỡng thử nghiệm để tuyên bố đạt NFR |
| Scope giao diện | CLI + web ZIP/GitHub | Slice web thiếu partition policy; GitHub trả 503 | Demo CLI/artifact; web full chưa sẵn sàng |
| Kết quả đầy đủ | Cùng engine/mô hình | Hai checkout và schema khác nhau | Trình bày hai luồng riêng, ghi rõ phần nối chưa xong |

## 12. Kết quả đã chạy lại hôm nay

### 12.1 Bản Khiêm + OpenAI thật

**Mốc phiên bản:** demo kết thúc 20:53:26 trên a14d32c; checkout được fast-forward lên 42d0468 lúc 20:53:49. Bản mới thêm phân giải tên bằng Pyright/scip-python và có thử nghiệm v10, chưa được chạy trong demo này. Không lấy số đo a14d32c để đánh giá 42d0468. Code tái hiện đã lưu riêng cùng bằng chứng. Theo HANDOFF của Khiêm, v10 mới có 5/16 lần hoàn tất, kết quả chưa chứng minh cải thiện so với v8. Đây là số báo cáo của Khiêm, không phải phép đo mới của tôi.

- Repo public: `rhoboro/async-fastapi-sqlalchemy`; commit `6c08827241e9737487905c62d8834edc2a0da8e7`.
- Source ở `D:\VSF\l3-generator-quote-evidence\sample-repos\rhoboro-demo`.
- Model `gpt-5.6-sol`; **2 request mới, không cache**; 3.412 token; 18,5 giây tổng, 18,4 giây model.
- Trạng thái pipeline `complete`; 15 file; 6 khối gồm 5 khối chức năng và 1 khối dùng chung; 5 cạnh nội bộ; 1 hệ thống ngoài.
- 5/5 quote được bộ đếm của pipeline ghi hợp lệ; không hiểu thành chứng nhận ngữ nghĩa mọi phát biểu.
- Chấm theo oracle sẵn của thử nghiệm: internal P=1,00; P chặt=0,80; R=1,00; agreement file=0,923; ARI=0,687.
- Đây là repo development đã được dùng trước, không phải held-out mới; số trên là chẩn đoán một demo, **không phải KPI nghiệm thu theo OBS**.
- Chi phí ước lượng bảo thủ theo token: khoảng **0,02852 USD**; endpoint không trả hóa đơn nên `billed_usd=null`.
- Unit test của bộ code demo a14d32c: **59 test pass** trên Python 3.12 trong lượt kiểm này; không suy thành test pass cho checkout Pyright mới.

Kết quả: [summary.json](../../l3-generator-quote-evidence/evaluation/quote-evidence/runs/demo-openai-20261001-b/summary.json), [graph.json](../../l3-generator-quote-evidence/evaluation/quote-evidence/runs/demo-openai-20261001-b/graph.json), [diagram.mmd](../../l3-generator-quote-evidence/evaluation/quote-evidence/runs/demo-openai-20261001-b/diagram.mmd), [score.json](../../l3-generator-quote-evidence/evaluation/quote-evidence/runs/demo-openai-20261001-b/score.json).

Lượt `demo-openai-20261001` đầu tiên dừng ở kiểm ngân sách **trước khi gửi request**. Lượt `-b` giới hạn mỗi response tối đa 8.192 token và chạy thành công. Giữ cả log, không chọn lại lần chạy vì điểm thấp.

### 12.2 L3 của em

| Mẫu | Chạy thật | Đầu ra | Cách hiểu |
|---|---|---|---|
| shop_full | CLI exit 3 | 6 artifact ready, API + TBL, 2 component và 1 cạnh | Sinh được tài liệu; toàn run vẫn partial |
| shop_partial | CLI exit 3 | 6 artifact ready | Minh họa trường chưa biết, không giả full path/dialect |
| events cũ | CLI exit 3 | 4 artifact chung, không EVT | Chỉ có tham số producer/consumer không rõ loại; không chứng minh Kafka |
| kafka demo có import/khởi tạo rõ | CLI exit 3 | 6 artifact, gồm EVT Orders và EVT Stock | Có bằng chứng nhận dạng Kafka; nguồn mẫu không được thực thi |

Log/command/exit thật ở [cli-runs.json](../ket-qua-chay/demo-mentor-20261001/cli-runs.json) và [kafka-run.json](../ket-qua-chay/demo-mentor-20261001/kafka-run.json). Exit 3 có nghĩa **partial**, do `SLICE_SCOPE`, `MODEL_NOT_RUN`; không gọi nó là crash cũng không nói completed toàn sản phẩm.

Bộ test cũ 116 pass đã được kiểm trong review trước cùng ngày. Bộ chấm CMP-008 độc lập đang được xây thêm: lượt phát triển đầu có **66 pass, 13 fail, 3 error** trên 82 ca. Có cả lỗi fixture của bộ chấm cần sửa, nên **không lấy 66/82 làm tỷ lệ chất lượng sản phẩm**. Xem `ket-qua-chay/l3-evaluation-development-01/`; đây chưa phải báo cáo chốt bộ chấm.

## 13. Kịch bản trình bày 10–12 phút

### Phút 0–2: vấn đề và phạm vi

“Nhóm em giúp developer hiểu repo lạ bằng sơ đồ và contract có bằng chứng. Phase đầu tập trung Python/FastAPI. Đầu ra không chỉ là ảnh: có JSON, tài liệu API, bảng dữ liệu, event. Công cụ không chạy source và không tự sửa source.”

Mở PRD mục II, IV. Chỉ 4 goal và 9 FR. Không đọc toàn bộ lịch sử revision.

### Phút 2–4: luồng Khiêm

Mở kết quả OpenAI vừa chạy. Giải thích theo đường:

```text
Ứng dụng web → API notebook/note → Service notebook/note → Mô hình ORM → Hạ tầng database → Database
                                      └──────── quản lý session ──────────┘
```

Settings ở khối dùng chung, không vẽ cạnh trong góc nhìn này. 6 component không phải 6 dịch vụ deploy độc lập.

Chọn cạnh API → Service: quote ở `app/api/notebooks/views.py:22`, `Depends(CreateNotebook)`. Chọn Service → ORM: `app/api/notebooks/use_cases.py:18`, gọi `Notebook.create(...)`. Đây là ví dụ người xem tự mở file kiểm được.

Nói: “AI giúp chia/đặt tên; code dựng và kiểm phần bằng chứng. Không phải vẽ từ lời đoán tự do, nhưng cách gom nhóm vẫn cần đánh giá.”

### Phút 4–7: phần L3 của em

Mở [shop_full README](../ket-qua-chay/demo-mentor-20261001/shop_full-recorded/README.md), rồi:

1. [API](../ket-qua-chay/demo-mentor-20261001/shop_full-recorded/tech-specs/CUA-HANG-API/api/API-SHOP-FULL-CUA-HANG-API-v1.md): chỉ `GET /items`, status `200`, handler, evidence `app/main.py:8`; kéo xuống OpenAPI có cùng method/path/status.
2. [TBL](../ket-qua-chay/demo-mentor-20261001/shop_full-recorded/tech-specs/LUU-TRU/schema/TBL-SHOP-FULL-LUU-TRU.md): bảng `items`, `categories`, `category_id` tham chiếu `categories.id`; chỉ nullable và DDL SQLite.
3. [EVT Orders](../ket-qua-chay/demo-mentor-20261001/kafka/tech-specs/ORDERS/events/EVT-KAFKA-ORDERS-ORDER-CREATED.md) và [EVT Stock](../ket-qua-chay/demo-mentor-20261001/kafka/tech-specs/STOCK/events/EVT-KAFKA-STOCK-ORDER-CREATED.md): gửi/nhận topic, phần chưa biết được ghi rõ. Không hứa đã resolve mọi binding chỉ vì tên topic giống nhau.

Nói: “Bảng cho người đọc; OpenAPI/DDL/JSON Schema cho máy dùng. Các bản xuất cần được kiểm nội dung khớp nhau.”

### Phút 7–8: chứng minh công cụ không bịa

Mở [shop_partial](../ket-qua-chay/demo-mentor-20261001/shop_partial-recorded/README.md), vào API/TBL theo mục lục. Prefix lấy từ biến môi trường không xác định bằng tĩnh; không biến hậu tố route thành full path. Không biết dialect thì không tự chọn PostgreSQL.

### Phút 8–10: đo và điểm chưa xong

Phân biệt: unit test kiểm hành vi; contract checker kiểm cấu trúc; bộ chấm renderer kiểm preservation/parity; gold độc lập kiểm đúng với source. Nói kết quả demo cụ thể ở mục 12, không đọc một số phần trăm “tiến độ chất lượng”.

Kết thúc: “Việc tiếp theo là chốt bridge graph v8 → VerifiedResult, sửa lỗi phát hiện ở validation/parity, rồi đo trên repo mới với gold độc lập. Web và các ngưỡng NFR còn phải kiểm.”

## 14. Chạy demo lại

### A. Bản Khiêm, OpenAI thật

PowerShell, dùng thư mục output mới cho mỗi lần chạy:

```powershell
cd D:\VSF\l3-generator-quote-evidence
$env:PYTHONIOENCODING='utf-8'
$demoRun = 'evaluation/quote-evidence/runs/demo-' + (Get-Date -Format 'yyyyMMdd-HHmmss')
py -3.12 evaluation/quote-evidence/runs/demo-openai-20261001-b-api-evidence/pipeline-code/run_openai_demo.py sample-repos/rhoboro-demo --env .env --out $demoRun --oracle experiments/quote-evidence/oracle/rhoboro-async-fastapi-sqlalchemy.json
```

`.env` nằm tại gốc checkout; adapter đọc `OPENAI_API_KEY` hoặc tên `Open_API` hiện bạn đã điền. Model mặc định `gpt-5.6-sol`, không tự đổi model. Mỗi lần chạy lại sẽ gọi API mới và có chi phí; khi báo cáo nên dùng kết quả đã lưu nếu mạng/quota không ổn.

Chỉ source của repo mẫu public đã chọn được gửi qua prompt. Không gửi `.env`, không mở `.env` lên màn hình lúc trình bày. File request/response của demo ở thư mục `demo-openai-20261001-b-api-evidence`, không có Authorization header.

### B. L3 local không cần key

```powershell
cd D:\VSF\l3-generator-l3\slice
$env:PYTHONIOENCODING='utf-8'
$demoOut = '../ket-qua-chay/l3-live-' + (Get-Date -Format 'yyyyMMdd-HHmmss')
../scripts/.venv/Scripts/python.exe -m l3slice --source tests/fixtures/shop_full --membership tests/fixtures/shop_full.membership.json --output $demoOut
# Exit 3 là partial có chủ đích; đọc thông báo và README.
```

Đổi `--source demo/kafka --membership demo/kafka.membership.json` để demo EVT. Chạy bộ phân tích, **không chạy** `orders.py`, không cần mở database/Kafka server.

Đọc Markdown trong VS Code bằng **Ctrl+Shift+V**, hoặc **Ctrl+K rồi V** để xem bên cạnh. Mở `.svg` bằng browser. Mở `diagram.mmd` bằng trình xem Mermaid đã cài; nếu không có, dùng sơ đồ trong phần trình bày và JSON có evidence. Không coi việc mở được file Mermaid là đã kiểm mọi cạnh đúng.

## 15. Câu mentor dễ hỏi và câu trả lời ngắn

**“AI chính ở đâu?”** Trong bước suy luận/gom nhóm/đặt tên ở pipeline Khiêm; renderer L3 dùng code từ dữ kiện đã có để giữ định dạng và tránh tự thêm sự thật.

**“Sao không đưa cả repo cho LLM?”** Tốn context và khó kiểm. Tầng tĩnh rút ra dữ kiện; AI nhận tóm tắt và đoạn source có ID; code đối chiếu output. Cách này vẫn có thể bỏ sót, nên phải đo.

**“Bằng chứng đúng nghĩa là kết luận đúng?”** Không hoàn toàn. Máy kiểm file/dòng/hash/đích tham chiếu; đáp án/reviewer kiểm xem dữ kiện có đủ hỗ trợ cách diễn giải và chia khối không.

**“Sao auth unknown?”** Không nhìn thấy dependency không chứng minh endpoint công khai; auth có thể nằm ở middleware hoặc ngoài phạm vi phân tích.

**“Phần em phụ thuộc bạn kia thế nào?”** Cần component membership, fact/evidence và owner. Em có thể test renderer độc lập bằng dữ liệu đúng contract; tích hợp phải thống nhất schema và cùng snapshot.

**“Đã hỗ trợ mọi framework chưa?”** Chưa. Mục tiêu thích ứng nhiều framework là định hướng; phase đầu và dữ liệu demo vẫn Python/FastAPI.

**“Sao test pass mà vẫn có lỗi?”** Test chỉ kiểm những trường hợp đã viết. Bộ chấm mới tìm thêm lỗi; pass schema không đảm bảo OpenAPI/Markdown cùng giá trị và không đảm bảo gold độc lập.

**“Gold là gì?”** Repo cố định phiên bản + phạm vi + đáp án có evidence do người lập/review độc lập + quy tắc matching. Model mạnh chỉ hỗ trợ soạn candidate; AI đồng ý không tự trở thành ground truth.

**“Precision khác recall?”** Precision hỏi những thứ công cụ xuất có bao nhiêu đúng; recall hỏi những thứ đúng cần có công cụ tìm được bao nhiêu. Xuất một cạnh đúng rồi bỏ chín cạnh còn lại có precision tốt nhưng recall thấp.

**“P=1,00 mà P chặt=0,80?”** Bộ chấm thử nghiệm cho một số cạnh hợp lý nhưng không bắt buộc vào nhóm chấp nhận. Chấm chặt tính chúng là dư. Đó là hai policy khác nhau, không che bằng một số đẹp.

**“Bao giờ hoàn thành?”** Cần thống nhất lại phạm vi/lịch và các bước còn thiếu. Đưa danh sách cụ thể: bridge, validation/parity, gold/review độc lập, tích hợp/UI, NFR. Không hứa theo timeline cũ đã superseded.

## 16. Thứ tự đọc tối nay

1. Mục 1–5: hiểu sản phẩm và yêu cầu.
2. Mục 6–10: phân biệt trách nhiệm và cách nối.
3. Mục 12–14: mở đúng output, diễn tập theo script.
4. Mục 11, 15: chuẩn bị câu hỏi khó.

Nếu chỉ có 5 phút trình bày: **vấn đề → 4 goal → sơ đồ Khiêm → API/TBL của em → evidence/unknown → phần nối chưa xong**.

Nguồn model dùng khi thiết lập demo: [OpenAI GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol). Tên model được kiểm thêm bằng API models trên chính tài khoản, không suy từ tên trong ứng dụng. Chi phí ở trên là ước lượng token, không phải hóa đơn.
