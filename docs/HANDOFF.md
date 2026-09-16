# Bàn giao — Code → L3 Generator

Cập nhật: 16/09/2026. Đây là bản tiếp tục công việc, không phải chứng nhận V2 đã hoàn tất.
Đọc file này đầu phiên; đối chiếu code trước khi khẳng định năng lực hiện tại.

## 1. Việc đang làm và thứ tự đã chốt

Người dùng đã chốt hướng kéo sản phẩm về đúng Code → L3:

1. Phân tích chi tiết chỉ để chứng minh quan hệ kiến trúc.
2. L3 và diagram trình bày application/component, không liệt kê toàn bộ function/class.
3. Repository Knowledge Graph đầy đủ không phải sản phẩm chính của dự án này.
4. Resolver được giữ làm công cụ nội bộ nhưng không tiếp tục mở rộng nếu không phục vụ câu hỏi L3.
5. Unresolved raw call không được biến thành semantic edge nét đứt.
6. Giao diện web là đường dùng chính cho người dùng tương tác; CLI/script/CI là đường tự động hóa phụ, không phải hình thức duy nhất của sản phẩm.
7. Thiết kế đầu vào của giao diện gồm thư mục cục bộ, file ZIP và URL GitHub; mở lại kết quả phân tích đã có là một use case riêng. Đây là phạm vi yêu cầu/thiết kế, chưa phải tuyên bố code hiện tại đã hỗ trợ.
8. Kết quả được khám phá theo mục tiêu: tổng quan, application/component, API/luồng gọi, dữ liệu/tích hợp, phụ thuộc, bằng chứng nguồn, chất lượng/giới hạn và xuất artifact.

Đã đồng bộ [ARCHITECTURE_V2_IDEA.md](ARCHITECTURE_V2_IDEA.md),
[USE_CASES.md](USE_CASES.md), [SCENARIOS.md](SCENARIOS.md),
[SPEC](../SPEC_Code_to_L3_Generator.md) và [README](../README.md).

Đã tạo PRD gốc dạng draft tại
[`PRD-L3GEN.md`](../.aide/product/prd/PRD-L3GEN.md) theo đủ khung I–IX của mentor.
PRD ở revision 6. Đã tạo 5 FR với 52 AC tại `.aide/requirements/fr/` và 5 NFR tại
`.aide/requirements/nfr/`. PRD chưa qua Scope Gate; OBS chưa được tạo nên coverage
KPI→OBS còn thiếu.
Sơ đồ use case, `USE_CASES.md`, `SCENARIOS.md`, SPEC và README đã cùng mô tả sản phẩm
có giao diện với ba hình thức đầu vào và lịch sử phân tích. Đây là phạm vi mục tiêu:
code hiện chỉ nhận thư mục cục bộ qua dòng lệnh, giao diện chỉ đọc output đã sinh, và
phần ZIP/GitHub/lịch sử chưa được viết code.

Tạm bỏ qua EVALUATION và examples; không dùng số đo V1 để chứng minh V2. Chưa sửa code
sản phẩm và chưa thực hiện thao tác Git trong lượt đồng bộ tài liệu này.

## 2. Những nguyên tắc đã thống nhất

- Đọc source, không chạy hoặc import code của repo được phân tích.
- Kiểm kê theo file và ngôn ngữ. Không coi mỗi folder hay nhóm ngôn ngữ là một service triển khai.
- Python là ngôn ngữ phân tích chính hiện tại. Nhận diện file Java/TypeScript không đồng nghĩa đã phân tích được chúng.
- Dùng AST (cây biểu diễn cú pháp), dữ liệu trung gian, nối tên và truyền giá trị để tìm quan hệ.
- Framework adapter diễn giải API bằng luật đã duyệt. Không nhận diện chỉ bằng tên ngắn như `mount`.
- AI chỉ viết mô tả hoặc hỗ trợ diễn đạt review; không sửa dữ kiện, tự nối call hoặc tự tạo luật trong V2.
- Agent đề xuất framework rule thuộc ý tưởng V2.5, không triển khai trong V2 hiện tại.
- Thiếu bằng chứng phải ghi phần chưa biết và lý do. Không tự dựng cạnh để graph trông đầy đủ.
- Áp dụng nguyên tắc “Analyze deep enough; present at L3”: function/call là evidence nội bộ, không mặc nhiên là node L3.
- Architecture graph công khai tập trung application/component/API/data/external/event. Function graph, nếu giữ, là diagnostic artifact riêng.
- Chỉ phân tích sâu từ architectural anchor hoặc trên đường trả lời câu hỏi kiến trúc đã chốt.
- Giữ tên các bước pipeline bằng tiếng Anh; phần giải thích dùng tiếng Việt dễ hiểu, giải nghĩa thuật ngữ mới.
- CLAUDE.md là hướng dẫn cục bộ, đang có trong .gitignore. Không tự đưa vào commit hay sao chép nội dung riêng tư sang tài liệu công khai.

## 3. Code hiện có

Luồng chính đã dùng các thành phần V2 dưới đây. “Có code” không có nghĩa mọi tình huống đã được kiểm chứng.

| Phần | Bằng chứng trong source | Hiện trạng |
|---|---|---|
| Điều phối | [pipeline.py](../src/l3gen/pipeline.py), [builder.py](../src/l3gen/core/builder.py) | Builder gọi frontend, resolver và adapter V2 |
| File Inventory | [discovery.py](../src/l3gen/detection/discovery.py) | Kiểm kê, nhóm ngôn ngữ và ghi phần bỏ qua |
| Python Frontend + Common Semantic IR | [frontend.py](../src/l3gen/languages/python/frontend.py), [semantic.py](../src/l3gen/models/semantic.py) | Thu import, khai báo, phạm vi tên, phép gán, call, tham số, return… |
| Tên module | [modules.py](../src/l3gen/languages/python/modules.py) | Suy từ package; tên trùng được tách bằng namespace theo file và ghi chú |
| Resolver + Dataflow | [dataflow.py](../src/l3gen/core/resolution/dataflow.py) | Truyền tập giá trị bằng hàng đợi, nối call, giữ bằng chứng và giới hạn xử lý |
| Kiến thức thư viện | [registry.py](../src/l3gen/core/semantics/registry.py) | Bảng kiểu và thao tác tất định; phiên bản bảng là builtin-semantics-v1 |
| FastAPI | [adapter_v2.py](../src/l3gen/languages/python/frameworks/fastapi/adapter_v2.py) | Nhận thao tác đăng ký, ghép route từ quan hệ app/router |
| ORM và gọi ra ngoài | [sqlalchemy_v2.py](../src/l3gen/orm/sqlalchemy_v2.py), [external_v2.py](../src/l3gen/languages/python/frameworks/fastapi/external_v2.py) | Đọc entity và lời gọi HTTP qua dữ liệu V2 |
| IAM và graph | [graph_builder.py](../src/l3gen/core/graph_builder.py) | Tạo node/cạnh; ranh giới application ở mức candidate/unknown |
| Đầu ra và UI | [output](../src/l3gen/output), [ui](../src/l3gen/ui) | Đã có code sinh tài liệu, JSON, sơ đồ và giao diện; không còn trạng thái “chưa làm UI” |

Các file V1 còn tồn tại không có nghĩa chúng còn là luồng chạy chính.
Trường `service="python"` trong builder hiện là tương thích dữ liệu cũ, không chứng minh có một service tên Python.
Comment đầu builder còn nói application boundary là việc tương lai, trong khi graph_builder đã có phần tạo boundary. Đây là lệch comment/code cần xử lý khi được phép sửa code.

## 4. Mức kiểm chứng và giới hạn

### Kiểm chứng

- Phiên cập nhật này: đọc source, đối chiếu tài liệu và kiểm tra hai file bàn giao; không chạy test hoặc benchmark.
- Bản HANDOFF cũ ghi 55 test và số đo V1. Những số đó không đại diện cho source V2 hiện tại.
- Không công bố số test đạt mới khi chưa có lần chạy tương ứng với đúng trạng thái code.
- Các số đo lịch sử trong PROGRESS/EVALUATION cần kiểm tra lại phiên bản và phạm vi trước khi sử dụng.
- Phiên bản sản phẩm, phiên bản frontend và phiên bản bảng luật là ba thông tin khác nhau.

### Giới hạn thấy trong source hoặc cần kiểm chứng thêm

- Source root (thư mục gốc để tính tên import) chưa có mô hình cấu hình đầy đủ. Trùng tên module được tránh gộp nhầm, nhưng chưa vì thế resolve được import.
- Dataflow có giới hạn 32 đích mỗi call, 128 giá trị mỗi ô lưu và 250.000 lượt truyền. Giới hạn này không phải cam kết thời gian/RAM tối đa.
- Tham số và kết quả trả về dùng chung theo định nghĩa hàm có thể trộn thông tin giữa nhiều lần gọi. Cần test riêng factory tạo nhiều app/router.
- Cần kiểm chứng điều kiện, thứ tự và ngữ cảnh thực thi khi kết luận route đã được gắn vào app; không đồng nhất “có câu lệnh trong source” với “chắc chắn được thực thi”.
- Chưa có cơ chế lưu kết quả file không đổi để phân tích tăng dần.
- Phiên bản registry chưa chứng minh tương thích với mọi phiên bản framework.
- Parse được file không đồng nghĩa hiểu hết ngữ nghĩa trong file. Phải giữ ghi chú phần chưa hỗ trợ.
- Chưa xác nhận chất lượng V2 bằng đánh giá đầy đủ. Không ghi “hoàn tất V2” chỉ vì các tầng đã có code.

## 5. Pipeline và contract đã chốt ở mức tài liệu

```text
File Inventory + Analysis Context
→ Language Frontends
→ Common Semantic IR
→ Architectural Anchor Discovery
→ Targeted Resolver + Dataflow ↔ Library Models
→ Framework Adapters
→ Registration & Composition
→ Component Synthesis + Architecture IAM
→ L3 Projection + Validation + Outputs
```

Khoảng cách chính giữa code và contract mới:

- chưa có Component Synthesis hoàn chỉnh;
- IAM còn trộn dữ liệu kỹ thuật và kiến trúc;
- graph còn lấy function/class/call làm node chính;
- Mermaid hiện chủ yếu route/entity/external, chưa phải component diagram hoàn chỉnh;
- registration chưa phân biệt đầy đủ declared/potentially reachable;
- event/config relationship chưa hoàn chỉnh;
- registry chưa thể hiện dải phiên bản framework.

Thứ tự code tiếp theo: acceptance test → Architecture IAM/projection → component
synthesis → output/UI → đo resolver → sau đó mới EVALUATION/examples. Không xóa resolver
ồ ạt và không mở rộng resolver tổng quát trước khi có acceptance criterion L3.

## 6. Quy tắc tự cập nhật bàn giao

Quy tắc này là yêu cầu thường xuyên của người dùng, không cần đợi nhắc ở mỗi phiên.

- Đầu phiên: đọc HANDOFF, xác định việc đã chốt, việc còn chờ duyệt và trạng thái kiểm chứng.
- Sau mỗi nhóm thay đổi có ý nghĩa về code, test, cấu hình, tài liệu hoặc quyết định: cập nhật mục hiện trạng liên quan và thêm nhật ký ngắn ở mục 7. Không cần ghi từng lần gõ.
- Hoàn tất cập nhật trước khi kết thúc phiên hoặc chuyển giao; ghi cả việc đang dở và bước tiếp theo.
- Nếu chỉ điều tra mà không sửa, ghi kết luận hữu ích khi phạm vi cho phép. Nếu người dùng yêu cầu chỉ đọc/không sửa file, tôn trọng yêu cầu đó và báo nội dung cần cập nhật trong chat.
- Mỗi nhật ký ghi: yêu cầu, file thay đổi, làm gì/vì sao, kiểm chứng thực tế, việc còn lại và kinh nghiệm nếu có.
- Ghi rõ kiểm chứng “đạt”, “thất bại” hoặc “chưa chạy”, kèm lệnh/phạm vi khi có. Không chuyển kết quả cũ thành kết quả mới.
- Tách rõ đề xuất, quyết định đã duyệt, code đã viết và kết quả đã đo. Không tự coi im lặng là phê duyệt.
- Sửa trạng thái hiện hành khi thông tin cũ sai; giữ nhật ký đã có để hiểu quá trình thay đổi. Không chỉ nối nhật ký rồi để phần đầu tiếp tục sai.
- Bàn giao không mở rộng quyền: không tự sửa tính năng, tài liệu khác, commit hoặc push ngoài yêu cầu.
- Không đưa khóa, dữ liệu riêng tư hoặc đường dẫn phiên chat cá nhân vào HANDOFF.

## 7. Nhật ký thay đổi

### 16/09/2026 — Thu hẹp sản phẩm về Code → L3

- Yêu cầu: chỉnh tài liệu sau khi xác nhận dự án có nguy cơ lấn sang Repository Knowledge Graph.
- File sửa: `docs/ARCHITECTURE_V2_IDEA.md`, `docs/USE_CASES.md`, `docs/SCENARIOS.md`, `SPEC_Code_to_L3_Generator.md`, `README.md`, `docs/COMPETITOR_RESEARCH.md`, `docs/AGENTIC_SDLC_LOG.md`, `PROGRESS.md` (cục bộ, ignored), `docs/HANDOFF.md`.
- Thay đổi: tách phân tích kỹ thuật khỏi L3 projection; định nghĩa architectural anchor, targeted resolver, Component Synthesis, Architecture IAM và component-level graph; bỏ full function graph khỏi public L3 contract; đánh dấu các đề xuất/roadmap khảo sát cũ là lịch sử.
- Kết quả: architecture, requirement, scenarios, spec và README cùng một hướng; README nói rõ code hiện mới phù hợp một phần.
- Kiểm chứng: rà heading, liên kết tài liệu và các cụm từ dễ mâu thuẫn; chưa chạy test/benchmark vì không sửa code.
- Kinh nghiệm: mức chi tiết cần cho evidence không phải mức chi tiết phải đưa vào diagram. Spec mở rộng sai có thể kéo toàn bộ implementation lệch khỏi đề bài gốc.
- Việc tiếp theo: review diff tài liệu; sau khi người dùng đồng ý mới lập test/code migration theo SPEC mục 10 và 13.

### 16/09/2026 — Đồng bộ bàn giao với V2 và thiết lập tự cập nhật

- Yêu cầu: ưu tiên chốt pipeline rồi mới UC/scenario, SPEC/README; tạm bỏ qua EVALUATION/examples.
- File sửa: docs/HANDOFF.md và CLAUDE.md cục bộ.
- Thay đổi: thay ảnh chụp hiện trạng V1 bằng bảng đối chiếu code V2; ghi giới hạn, đề xuất chờ duyệt và quy tắc cập nhật sau thay đổi.
- Kiểm chứng: đọc lại hai tài liệu và kiểm tra các đường dẫn source; không chạy test/benchmark vì không sửa code.
- Kết quả: có điểm tiếp tục cho phiên sau; chưa phê duyệt hoặc triển khai thay đổi pipeline.
- Kinh nghiệm: HANDOFF phải cập nhật theo thay đổi thực tế, không phụ thuộc lời nhắc. Viết xong code, test đạt và đo chất lượng là ba trạng thái khác nhau.
- Bước tiếp theo: người dùng xem đề xuất pipeline trong chat. Sau khi chốt mới sửa ARCHITECTURE_V2_IDEA theo phạm vi đã duyệt.

### 16/09/2026 — Thiết kế lại use case tổng quan theo hướng UI-first

- Yêu cầu: bổ sung đầu vào thư mục cục bộ, file ZIP và URL GitHub; tham khảo cách tổ chức UI của RepoDNA; vẽ lại `docs/diagrams/usecase-overview.svg`.
- File sửa: `docs/diagrams/usecase-overview.svg`, `docs/HANDOFF.md`.
- Thay đổi: bỏ mô hình cũ coi hệ thống là CLI tool; dùng actor trừu tượng `Engineering User` cho Developer và Architect/Reviewer; tách ba nhóm use case phân tích kho mã, khám phá kiến trúc, xem xét/sử dụng kết quả; thể hiện ba cách cung cấp source và GitHub. Sơ đồ tổng quan không tách riêng automation, theo dõi/cấu hình phân tích, AI hay nền tảng tiếp nhận. Phần kết quả được rút gọn thành xem chi tiết và xuất tài liệu.
- Kết quả: sơ đồ mô tả mục tiêu/người dùng và quan hệ UML ở mức tổng quan, không đưa pipeline phân tích nội bộ vào use case.
- Kiểm chứng: parse XML thành công và render SVG bằng Chrome headless để kiểm tra bố cục; không chạy test sản phẩm vì chỉ sửa tài liệu/sơ đồ.
- Kinh nghiệm: input format là biến thể của use case cung cấp source, không phải actor; GitHub là external system vì hệ thống thực sự trao đổi với nó. Các view nên bám câu hỏi người dùng muốn trả lời, không bám trực tiếp từng bước engine.
- Việc tiếp theo: đồng bộ `USE_CASES.md`, scenario, PRD/FR/NFR với mô hình này sau khi người dùng duyệt; cần chốt riêng phạm vi repository GitHub private, xác thực và giới hạn an toàn khi giải nén ZIP.

### 16/09/2026 — Đồng bộ use case và tạo PRD gốc

- Yêu cầu: cập nhật `USE_CASES.md` theo sơ đồ mới nhất và làm PRD theo từng mục trong mẫu mentor.
- File sửa/tạo: `docs/USE_CASES.md`, `.aide/product/prd/PRD-L3GEN.md`, `docs/HANDOFF.md`.
- Thay đổi use case: chỉ giữ UC1 Phân tích kho mã, UC2 Khám phá kiến trúc, UC3 Xem xét và sử dụng kết quả; đầu vào gồm thư mục, ZIP, GitHub URL; UC3 gồm xem chi tiết và xuất tài liệu; AI không là use case riêng.
- Thay đổi PRD: tạo đúng một PRD cho `SYS-L3GEN`, đủ frontmatter và các phần I–IX; thêm GOAL/KPI draft, persona, giả định/ràng buộc/phụ thuộc, in/out scope, chỉ mục FR/NFR dự kiến, hai user flow sequence diagram, edge cases, DoD, screen inventory, phasing, Scope Gate và Open Questions.
- Kiểm chứng: rà đủ heading theo mẫu mentor và kiểm tra không còn UC cũ trong `USE_CASES.md`; không chạy test code vì chỉ thay tài liệu.
- Trạng thái: PRD là `draft`, chưa baseline. KPI target và ngày OQ là đề xuất; FR/NFR/OBS chưa được tạo nên chưa thể qua Scope Gate.
- Việc tiếp theo: người dùng review lần lượt PRD I→IX; chốt Open Questions quan trọng, sau đó tạo mỗi FR và NFR thành một file riêng. Đồng bộ scenario/SPEC/README sau khi phạm vi PRD được duyệt.

### 16/09/2026 — Không tái sử dụng tab preview trong workspace

- Yêu cầu: giữ đồng thời nhiều file Markdown thay vì file sau thay thế tab preview trước.
- File tạo: `.vscode/settings.json`.
- Thay đổi: tắt `workbench.editor.enablePreview` và `workbench.editor.enablePreviewFromQuickOpen` ở mức workspace.
- Kiểm chứng: JSON parse thành công. Markdown Preview dạng render vẫn cần khóa từng tab bằng lệnh `Markdown: Toggle Preview Locking`, vì VS Code không có workspace setting tương đương cho trạng thái khóa của từng preview.

### 16/09/2026 — Chốt một phần Open Questions của PRD

- Quyết định người dùng: MVP không hỗ trợ GitHub private; thêm Java bên cạnh Python; phải lưu/mở lịch sử phân tích. Giới hạn tài nguyên và KPI chưa chốt.
- File sửa: `.aide/product/prd/PRD-L3GEN.md`, `docs/USE_CASES.md`, `docs/HANDOFF.md`.
- Thay đổi: bump PRD draft lên revision 2; chuyển OQ-001, OQ-002, OQ-005 sang đã trả lời; đưa Java và history vào scope/flow/DoD/phasing; GitHub private thành out of scope dứt khoát.
- Đề xuất chờ duyệt: Java dùng Spring Boot; MVP đọc cấu hình ứng dụng/environment và chỉ hỗ trợ Kafka cho event producer/consumer/topic; giới hạn pilot tạm thời 100 MB ZIP nén, 500 MB sau giải nén, 50.000 file và 10 phút phân tích.
- Open Questions mới: framework Java cụ thể và retention/dung lượng/xóa lịch sử. KPI vẫn mở vì người dùng chưa trả lời mục 6.
- Kiểm chứng: rà các đoạn scope, phase và OQ liên quan; không chạy test code vì chỉ sửa requirement.

### 16/09/2026 — Ghi nhận nhóm, mentor và chia lại phasing

- Thông tin người dùng: nhóm thực hiện gồm Khiêm và Hoàng trong 4 tuần; mentor là Nguyễn Chí Thức và Đinh Thái Hà.
- File sửa: `.aide/product/prd/PRD-L3GEN.md`, `docs/HANDOFF.md`.
- Thay đổi: bump PRD draft lên revision 3; Khiêm là document PIC, Hoàng là internal technical reviewer chờ xác nhận vai trò; hai mentor là reviewer chờ Scope Gate; MVP chia Phase 1 FastAPI (tuần 1–2), Phase 2 Java (tuần 3–4), Phase 3 sau pilot.
- Làm rõ mã: KPI sống trong PRD; OBS là artifact đo lường riêng sẽ tạo sau khi KPI được duyệt; đồ án không dùng OKR cấp khối.
- Chưa chốt: người kiêm QA/Test owner, Spring Boot hay Java framework khác, resource limits, Kafka/config scope, history retention, KPI/OBS và quy tắc cần một hay cả hai mentor phê duyệt.
- Kiểm chứng: rà lại các trường `chưa/planned/pending` trong PRD để lập danh sách thiếu; không chạy test code.

### 16/09/2026 — Chốt mốc MVP, Test owner và quy tắc mentor duyệt

- Quyết định: FastAPI hoàn thiện 26/09/2026; Java hoàn thiện 30/09/2026; Hoàng phụ trách Test/QA; Scope Gate chỉ cần ít nhất một trong hai mentor duyệt.
- File sửa: `.aide/product/prd/PRD-L3GEN.md`, `docs/HANDOFF.md`.
- Thay đổi: bump PRD draft lên revision 4, điền reviewer/phase/approval và sinh ULID `01M2MQ12YPDN94K6MSP63DS8DT` cho PRD.
- UID: quy trình tham chiếu `aide generate prd` và script cấp UID trước commit, nhưng repo hiện không cài lệnh `aide` và không có script ULID. UID lần này được sinh bằng Python standard library với timestamp + 80-bit randomness, không gõ tay.
- Kiểm chứng: ULID đủ 26 ký tự và giải mã timestamp đúng 16/09/2026; rà lại các dòng phase, Test/QA và OQ-009.
- Bước tiếp theo: có thể soạn FR/AC rồi NFR ở trạng thái draft; chỉ chờ mentor trước khi đổi trạng thái sang approved/baseline.

### 16/09/2026 — Kiểm chứng và chia commit theo phạm vi

- Yêu cầu: commit nhưng không push, chia nhỏ để dễ quản lý và không thêm author/co-author vào commit message.
- Test: `python -m pytest -q -p no:cacheprovider --basetemp .pytest-runtime-codex-commit` đạt `112 passed in 2.41s`. Lần chạy mặc định trước đó có 96 pass và 16 setup error do không có quyền với thư mục temp của user khác; không phải lỗi assertion của code.
- Commit implementation + tests: `f1c6505` — `feat: implement language-first semantic analysis v2`.
- Commit kiến trúc/spec: `b666e81` — `docs: align architecture and specification with L3 scope`.
- Commit use case/PRD: `977c749` — `docs: define UI-first use cases and product requirements`.
- Commit cuối chỉ chứa `.gitignore` và HANDOFF để tách repository hygiene khỏi nội dung sản phẩm.
- Không push. Commit dùng danh tính Git đã cấu hình sẵn; không thêm `Author`, `Co-authored-by` hoặc trailer AI vào message.

### 16/09/2026 — Chốt retention lịch sử và chuẩn bị publish branch

- Quyết định: mỗi repository lưu tối đa 10 lần phân tích; mỗi kết quả hết hạn sau 14 ngày.
- Làm rõ: Kafka chỉ là công nghệ trong repository đầu vào mà analyzer có thể nhận diện để vẽ event relationship; Kafka không phải hạ tầng vận hành L3 Generator. Đề xuất chuyển Kafka sang Phase 3 vẫn chờ người dùng duyệt.
- File sửa: `.aide/product/prd/PRD-L3GEN.md`, `docs/HANDOFF.md`.
- Thay đổi: bump PRD draft lên revision 5, bổ sung retention và edge cases; OQ-008 còn mở phần xóa thủ công.
- Git: người dùng yêu cầu publish branch `feat/language-first-semantic-v2`; sẽ push lên `origin` sau commit tài liệu này.

### 16/09/2026 — Đồng bộ use case theo sơ đồ và viết lại scenario

- Yêu cầu: lấy `usecase-overview.svg` làm chuẩn để sửa `USE_CASES.md`, sau đó sửa `SCENARIOS.md` theo use case.
- File sửa: `docs/USE_CASES.md`, `docs/SCENARIOS.md`, `docs/HANDOFF.md`.
- Đối chiếu trước khi sửa: tính lại tọa độ từng cạnh trong SVG và khớp với ellipse gần nhất. Cả 6 association/include/extend đều nối đúng đích; hình học sơ đồ không có lỗi. Lệch nằm ở phần chữ giữa hai tài liệu.
- Sửa use case theo sơ đồ: `Kiểm tra bằng chứng nguồn` chuyển từ cách xem thứ sáu thành hành vi `extend` của `Truy vết phụ thuộc`; `GitHub` gắn vào biến thể `Nhập URL GitHub` thay vì làm actor hỗ trợ của UC1; thêm bảng quan hệ UML đầy đủ cho cả use case và actor; đưa bốn nguyên tắc tổ chức giao diện từ note trong SVG vào tài liệu.
- Ngoại lệ có chủ ý: giữ hành vi mở lại lịch sử phân tích trong `USE_CASES.md` dù sơ đồ chưa vẽ, vì PRD đã chốt nó thuộc MVP (OQ-L3GEN-005, 10 lần/14 ngày), có trong FR-L3GEN-003, DoD, edge cases và Phase 1. Đây là chỗ sơ đồ thiếu, không phải tài liệu thừa. Đã ghi chú trong `USE_CASES.md` và cần bổ sung vào SVG ở lượt sau.
- Sửa scenario: tách Scenario 1 thành 1a (giao diện, luồng chính) và 1b (dòng lệnh, biến thể tự động hóa); thêm 1c cho ba hình thức đầu vào và các lỗi kèm theo; Scenario 3 viết lại theo quan hệ `extend`; thêm Scenario 12 (mở lại lịch sử) và 13 (xuất tài liệu).
- Sửa lỗi liên kết: bảng cuối `SCENARIOS.md` đang trỏ tới UC1–UC7 của mô hình 9 use case đã bị thay ở commit `977c749`. Đã thay bằng bảng theo UC1/UC2/UC3 hiện hành và thêm bảng độ phủ ngược để thấy use case nào chưa có scenario.
- Kiểm chứng: `grep` xác nhận không còn tham chiếu UC4–UC9 trong cả hai file; rà lại thứ tự heading sau khi thêm mục mới. Không chạy test vì chỉ sửa tài liệu.
- Việc còn lại: bổ sung lịch sử phân tích vào SVG; đồng bộ SPEC và README theo mô hình UI-first; sau đó mới viết FR/AC và NFR.
- Kinh nghiệm: khi viết lại hai tài liệu liên kết nhau trong cùng một commit, bảng tham chiếu chéo là chỗ dễ sót nhất vì nội dung chính đã đúng. Nên kiểm bằng `grep` các mã định danh cũ thay vì đọc lướt.

### 16/09/2026 — Thêm lịch sử vào sơ đồ và chuyển SPEC/README sang mô hình có giao diện

- Yêu cầu: bổ sung lịch sử phân tích vào SVG và tài liệu; sửa SPEC/README để sản phẩm không còn được mô tả như CLI đơn thuần.
- File sửa: `docs/diagrams/usecase-overview.svg`, `docs/USE_CASES.md`, `docs/SCENARIOS.md`, `SPEC_Code_to_L3_Generator.md`, `README.md`, `docs/HANDOFF.md`.
- Sơ đồ: thêm use case `Mở lần phân tích đã lưu` ở nhóm 3, nối `UC3.1 «include» Mở lần phân tích đã lưu`. Chọn `include` vì muốn xem kết quả chi tiết thì trước hết phải chọn được một lần phân tích. Cập nhật `<desc>` cho khớp nội dung mới.
- Tài liệu: bỏ ghi chú ngoại lệ trong `USE_CASES.md` vì sơ đồ đã có lịch sử; thêm mục con mô tả use case được include kèm giới hạn 10 lần/14 ngày; thêm quan hệ vào bảng và vào bảng độ phủ của `SCENARIOS.md`.
- SPEC: đổi mục 0.1 từ "một CLI tool" sang phần mềm có giao diện; viết lại mục 4 thành `Input và interface contract` gồm hai đường dùng chung một engine, ba nguồn mã nguồn, nhóm màn hình, lưu trữ lần phân tích, dòng lệnh và bảng lỗi dùng chung; thêm mục 10.0 acceptance criteria cho input/interface; bổ sung năm tiêu chí giao diện vào Definition of Done mục 14.
- README: mở đầu mô tả phần mềm có giao diện, dòng lệnh là đường tự động hóa; đổi tiêu đề mục 5 thành "Dòng lệnh"; ghi rõ đầu vào hiện chỉ là thư mục cục bộ.
- Ranh giới mục tiêu và hiện trạng: cả SPEC lẫn README đều có cảnh báo rằng đầu vào ZIP/GitHub và lịch sử là phạm vi mục tiêu, chưa có code. Không được đọc SPEC mục 4 như mô tả năng lực hiện tại.
- Kiểm chứng: SVG parse XML thành công và render bằng Chrome headless ba lần để sửa đường nối; lần cuối arrow rời UC3.1 và tới đúng ellipse mới, không chồng UC3.2, nằm trong khung nhóm 3. Tính toán va chạm bằng Bezier trước khi render. Bảng markdown của bốn file đều cân đối. Không còn tham chiếu UC4–UC9.
- Test: `python -m pytest -q -p no:cacheprovider` — lần chạy đầu `1 failed, 111 passed`, lần chạy lại `112 passed`. Test hỏng là `tests/unit/test_ui_boundary.py::test_xoa_thu_muc_ui_thi_lenh_phan_tich_van_chay`; nó di chuyển `src/l3gen/ui/` trong lúc chạy nên thỉnh thoảng hỏng. Chạy riêng thì đạt. Không liên quan thay đổi lượt này vì lượt này không sửa code Python, nhưng đây là test không ổn định cần xử lý riêng.
- Việc tiếp theo: viết FR/AC rồi NFR. `NFR-L3GEN-PERF-001` và `NFR-L3GEN-SEC-001` vẫn chờ OQ-L3GEN-004 để có ngưỡng.
- Kinh nghiệm: với sơ đồ, tính toán tọa độ chưa đủ để kết luận đường nối dễ hiểu. Đường nối không chạm ellipse nào vẫn có thể bị đọc nhầm điểm xuất phát; phải render ra ảnh để kiểm tra.

### 16/09/2026 — Đóng Open Questions và viết FR/NFR

- Quyết định người dùng: chốt ngưỡng tài nguyên pilot; **Kafka thuộc MVP** (phương án B, không chuyển Phase 3); Java giới hạn Spring Boot; lịch sử có cả xóa thủ công và tự động xóa.
- File sửa: `.aide/product/prd/PRD-L3GEN.md` lên revision 6.
- File tạo: 5 FR tại `.aide/requirements/fr/` và 5 NFR tại `.aide/requirements/nfr/`.
- PRD revision 6: đóng OQ-004, 006, 007, 008; thêm Kafka và xóa thủ công vào In Scope; thêm broker khác Kafka và framework Java ngoài Spring Boot vào Out of Scope; thêm 3 edge case; Kafka vào Phase 1 và Phase 2 vì Python và Java cần adapter riêng.
- FR: 001 đầu vào (11 AC), 002 phân tích (15 AC), 003 xem/lưu/xóa (11 AC), 004 evidence/giới hạn (8 AC), 005 xuất tài liệu (7 AC). Tổng 52 AC dạng given/when/then.
- NFR: PERF-001 giữ ngưỡng tài nguyên, SEC-001 giữ an toàn archive và vòng đời dữ liệu lịch sử, REL-001 suy giảm dần, USA-001 dùng được không cần hướng dẫn, COMP-001 artifact ổn định.
- Nguồn nội dung AC: SPEC mục 10, SCENARIOS 1a–13 và edge cases trong PRD. Không tự nghĩ ra hành vi mới; đây là bước chuyển hành vi đã chốt sang dạng có key để truy vết.
- Kiểm chứng: 52/52 AC đủ given/when/then; mọi `constrained_by` trỏ tới NFR có thật; cả 3 GOAL đều được FR tham chiếu và không có GOAL bịa; frontmatter parse được; link tương đối không hỏng. Đã sửa một vi phạm luật §B.5 khi FR-003 chép lại ngưỡng 10 lần/14 ngày, nay trỏ sang NFR-SEC-001.
- Test: `python -m pytest -q -p no:cacheprovider` đạt `112 passed in 2.27s`. Lượt này không sửa code Python; chạy test để xác nhận không có tác dụng phụ.
- Còn lại trước Scope Gate: OQ-L3GEN-003 (ngưỡng KPI) vẫn mở nhưng chỉ chặn GOAL-001/002, không chặn FR nào; chưa tạo OBS nên coverage KPI→OBS còn thiếu; `validated_by` trỏ tới TEST-* chưa tồn tại.
- Kinh nghiệm: luật "số liệu ngưỡng thì trỏ NFR, không gõ lại" rất dễ vi phạm ở phần mô tả FR chứ không phải ở AC. Nên kiểm bằng script tìm số có đơn vị thay vì đọc lại bằng mắt.

### 16/09/2026 — Sinh ULID và commit theo phạm vi

- Yêu cầu: tự sinh UID cho các artifact mới rồi commit, chia nhỏ để dễ xem, không ghi author/co-author.
- Làm rõ: `01M2MQ12YPDN94K6MSP63DS8DT` là UID của riêng file PRD, không phải của cả hệ thống. Theo execution guide §A.3 và §A.4, mỗi artifact chuẩn tắc mang UID riêng.
- Sinh 10 ULID cho 5 FR và 5 NFR bằng Python standard library: 48 bit timestamp mili giây cộng 80 bit ngẫu nhiên, mã Crockford base32. Repo vẫn chưa có lệnh `aide` hay script cấp ULID.
- Kiểm chứng: cả 11 UID dài đúng 26 ký tự, chỉ dùng bảng chữ Crockford, không trùng nhau, giải mã timestamp ra đúng 16/09/2026.
- Commit: 5 commit tách theo phạm vi — use case và scenario; SPEC và README; PRD revision 6; FR/NFR; bàn giao. Không push. Không thêm `Author`, `Co-authored-by` hoặc trailer AI vào message.
- Trạng thái ba phần mentor yêu cầu hôm nay: PRD, FR và NFR đã đủ. Chưa qua Scope Gate vì còn thiếu OBS và OQ-L3GEN-003.
