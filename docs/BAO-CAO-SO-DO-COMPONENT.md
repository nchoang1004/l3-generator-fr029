# Sơ đồ component có bằng chứng: đã làm gì, đo được gì, còn vướng gì

Cập nhật 30/09/2026. Tài liệu này tóm tắt phần việc "đọc repo → vẽ sơ đồ component" (không phải L3 contract): bài toán, cách làm hiện tại, số đo, nút thắt, độ khó so với nghiên cứu, và những gì thế giới đã làm. Chi tiết từng phiên nằm ở `docs/HANDOFF.md`.

## 1. Bài toán

Mục này nói ta cần làm ra cái gì và đo bằng gì.

- **Đầu vào:** một repo Python dùng FastAPI.
- **Đầu ra:** sơ đồ C4 mức 2 (khối và mũi tên giữa các khối, xếp theo tầng: Điểm vào, API, Nghiệp vụ, Dữ liệu, Hạ tầng). Mỗi khối và mỗi mũi tên kèm một dòng code làm bằng chứng, dạng `file:dòng`. Code kiểm dòng đó có thật, khớp nguyên văn.
- **Đáp án:** 8 repo, sơ đồ vẽ tay (`experiments/quote-evidence/oracle/`). 4 repo "lộ" được xem chi tiết khi phát triển (rhoboro, fullstack, realworld, teamhide); 4 repo "kín" chỉ xem số tổng (boilerplate, kibo, lnbits, fba).
- **Tiêu chí đạt:** P ≥ 0,8; R ≥ 0,6; trích dẫn hợp lệ ≥ 90%. P là tỉ lệ mũi tên vẽ ra mà đúng; R là tỉ lệ mũi tên đáp án mà ta vẽ được; Pk là P khắt khe (mũi tên "chấp nhận được nhưng không cần" cũng tính sai).

| Nhóm | Repo | Số file |
|---|---|---:|
| Nhỏ (mục tiêu chính, 30/09) | rhoboro, fullstack, realworld, teamhide | 15–54 |
| Vừa | boilerplate, kibo | 103–126 |
| Lớn (chỉ đo để lấy số) | lnbits, fba | 170–226 |

## 2. Cách làm hiện tại (v8)

Mục này mô tả pipeline đang chạy. Code làm phần chắc chắn; AI làm phần cần phán đoán; code kiểm mọi thứ AI trả.

| Bước | Ai làm | Việc |
|---|---|---|
| 1. Đọc code | Code | Cây cú pháp: ai gọi ai, gọi kiểu gì (luồng, kiểm tra, truyền session, lắp ráp), mở kết nối gì (CSDL, Redis, HTTP...), dấu hiệu tầng gần như không sai (`FastAPI(`, `@router.get`, `__tablename__`, `create_engine`) |
| 2. Bản tóm tắt repo | Code | Cây router, mỗi thư mục một dòng, mỗi file một dòng. Mỗi dòng code đưa cho AI có một mã `[L12]` |
| 3. Bản nháp khối | Code | Chia khối từ dữ kiện ở bước 1 (`draft.py`) |
| 4. Chia khối | AI | Đọc bản tóm tắt (và bản nháp), trả danh sách khối: tên, tầng, thư mục/file, **mã dòng** làm bằng chứng |
| 5. Kiểm | Code | Kiểm luật gộp bằng dữ kiện chắc; vi phạm thì gửi lại AI một lần. Mã dòng sai hoặc nằm ngoài khối thì code tự chọn dòng bằng chứng trong khối |
| 6. File mơ hồ | AI | Chỉ file chưa được thư mục nào phủ, hoặc có dấu hiệu tầng mâu thuẫn |
| 7. Mũi tên | Code | Gộp lời gọi "luồng" giữa các file thành mũi tên giữa khối; bỏ lắp ráp, kiểm tra, đi ngược tầng |
| 8. Đặt tên | AI | Tên tiếng Việt, vai trò một câu (kèm mã dòng), nhãn mũi tên, tên API ngoài |

Hai điều mới của v8 so với trước:
- **AI chỉ trỏ, không chép.** Trước đây AI phải chép lại dòng code làm bằng chứng; chép sai một ký tự là mất cả khối. Nay AI trả mã `L12`, code tra ra nguyên văn. Cách này học từ Citations API của Anthropic (đoạn trích lấy từ tài liệu, không do model viết lại).
- **Chạy qua OpenRouter** thay Groq miễn phí. Hết giới hạn 8 nghìn token/phút, nên bản tóm tắt không phải nén thư mục nữa. Mức suy luận của model đặt theo bước (bước 4: vừa; các bước khác: thấp), và văn bản suy luận được lưu lại (`reasoning.json`) để xem vì sao AI chia như vậy.

## 3. Đã làm gì (24/09 → 30/09)

Mục này liệt kê các hướng đã thử, theo thứ tự, và vì sao đổi.

| Phiên bản | Ý chính | Kết quả, vì sao đổi |
|---|---|---|
| v3–v6 (24–28/09) | AI chia khối từ danh sách thư mục; mọi cạnh import đều vẽ | Đạt ở repo nhỏ theo đáp án cũ; repo lớn: AI bịa đường dẫn, bỏ sót file (danh sách bị rút gọn cho vừa giới hạn token) |
| Đáp án bản 1 → 4 (26–30/09) | Chuẩn vẽ đổi: chỉ vẽ luồng xử lý, xếp theo tầng, bỏ cạnh kiểm tra/truyền session, vẽ tay cả 8 repo | Số đo cũ không so được với số mới; cho thấy đáp án có tính chủ quan |
| v7 (30/09) | Code tính dữ kiện; AI xếp từng file theo lô | AI chỉ thấy vài thư mục mỗi lô nên chia sai; trả lời dài bị cắt |
| v7 "từ trên xuống" (30/09) | AI thấy bản tóm tắt toàn repo, chốt khối trước, code xếp file theo đường dẫn | Ba lần chạy liền hỏng vì đường ống (định dạng lý do, bị cắt, JSON hỏng), chưa đo được thiết kế |
| v8 (30/09 tối) | AI trỏ mã dòng; bản nháp của code; OpenRouter | Mục 4 |

## 4. Số đo v8

Mục này cho số của lần chạy mới nhất (gpt-oss-120b qua OpenRouter, 30/09 20:34–21:27, 16 lần chạy), so với cách không dùng AI. "Không nháp" và "có nháp" là hai cách chạy bước 4. Số của repo kín là số tổng.

| Repo | Cách tốt nhất của v8 | P / Pk / R | File đúng khối | Không AI (luật): P / Pk / R | Chi phí |
|---|---|---|---:|---|---|
| rhoboro | có nháp | 1,00 / 0,80 / 1,00 | 92% | 1,00 / 0,80 / 1,00 | 0,0007 USD, 35 s |
| fullstack | có nháp | 1,00 / 1,00 / 1,00 | 93% | 0,83 / 0,83 / 0,83 | 0,0023 USD, 294 s |
| realworld | không nháp | 1,00 / 0,75 / 1,00 | 89% | 1,00 / 0,75 / 1,00 | 0,0019 USD, 46 s |
| teamhide | không nháp | 0,88 / 0,88 / 0,88 | 85% | 1,00 / 1,00 / 0,75 | 0,0016 USD, 54 s |
| kibo (kín) | không nháp | 0,93 / 0,72 / 1,00 | 81% | 0,79 / 0,65 / 0,85 | 0,0119 USD, 1.219 s |
| boilerplate (kín) | có nháp | 0,62 / 0,48 / 0,91 | 82% | 0,62 / 0,46 / 0,91 | 0,006 USD, 1.128 s |
| lnbits (kín) | không nháp | 0,75 / 0,35 / 0,50 | 88% | 0,62 / 0,42 / 0,28 | 0,0012 USD, 73 s |
| fba (kín) | không nháp | 0,47 / 0,28 / 0,29 | 59% | 0,30 / 0,26 / 0,29 | 0,0013 USD, 31 s |

Đọc bảng:
- **Repo nhỏ: đạt tiêu chí cả 4** (P ≥ 0,8, R ≥ 0,6). Mọi bằng chứng do AI trỏ đều hợp lệ; không khối nào phải để code chọn bằng chứng thay. Mỗi repo tốn dưới 0,003 USD.
- **Repo vừa: kibo đạt tiêu chí; boilerplate chưa** (P 0,62 < 0,8). Boilerplate: mũi tên ngang luật, nhưng sơ đồ gọn hơn (15 khối so với 28) và xếp file đúng hơn (82% so với 73%).
- **Repo lớn: chưa đạt.** lnbits R 0,50, fba R 0,29. AI chia khối đúng file hơn hẳn luật (lnbits 88% so với 54%), nhưng cạnh vẫn thiếu.
- **Trước v8, ba lần chạy liền (v7, v7b, v7c) có phần lớn quyết định của AI bị loại** vì lỗi định dạng; v7c ở rhoboro R 0,50. v8 cùng repo, cùng model: R 1,00.

**Bản nháp của code (bước 3) chưa giúp rõ.** Có nháp tốt hơn ở fullstack (R 0,33 → 1,00), boilerplate (R 0,73 → 0,91) và xếp file ở kibo (81% → 97%); kém hơn ở teamhide (R 0,88 → 0,75), realworld (Pk 0,75 → 0,50) và lnbits (R 0,50 → 0,00; lỗi ở mục 5). Chấm riêng bản nháp không AI: tương đương luật cũ (R trung bình 8 repo khoảng 0,67). Chưa kết luận; cần sửa lỗi lượt gửi lại (mục 5) rồi đo lại.

**Vì sao cách tốt nhất đổi theo repo** (`scripts-2026-09-30/error_kinds.py`, phân loại từng cạnh sai/thiếu, repo kín chỉ đếm):
- Repo nhỏ chỉ có 3–8 mũi tên bắt buộc. Một quyết định gộp/tách một khối phụ (script khởi tạo, middleware, cấu hình, hạ tầng) làm lệch 1–4 mũi tên, tức 0,12–0,67 điểm R. Cách "thắng" ở mỗi repo do 1–2 quyết định như vậy quyết định, không phải do cách làm tốt hơn hẳn.
- Bản nháp giúp khi nó mang đúng một luật mà AI hay bỏ qua (fullstack: tách CSDL, email, script theo dữ kiện). Nó hại khi AI giữ theo chỗ sai của nháp (teamhide: dependency của route bị xếp vào khối web app) hoặc khi lượt sửa hỏng (lnbits).
- Không AI thắng khi cấu trúc thư mục đã khớp đáp án (rhoboro, realworld, boilerplate). AI gộp khối lớn hơn nên kéo theo nhiều mũi tên "chấp nhận được" (tổng 8 repo: không AI 19, không nháp 33, có nháp 30), làm giảm Pk.
- Cách chấm chặt khuếch đại chênh lệch: khi một khối gộp hai khối đáp án, khối chiếm thiểu số mất hết mũi tên (7–11 cạnh "mất khối do ánh xạ" trên tổng 87).
- Chưa đo độ dao động giữa hai lần chạy cùng cách; một phần chênh lệch có thể chỉ là dao động.

**Cách chấm bổ sung (30/09)**, cho trường hợp "đúng nhưng vẽ khác đáp án":
- **R luồng:** mũi tên đáp án X→Y có hiện trên sơ đồ không, kể cả đi qua tối đa 2 khối trung gian.
- **P luồng:** mũi tên vẽ ra có ứng với một luồng thật không.
- **ARI:** độ giống cách chia file thành khối (1 là giống hệt, 0 là như chia ngẫu nhiên). Đây là thước đo các paper khôi phục kiến trúc hay dùng.

Ví dụ: `fba` có nháp có P / R chặt 0,29 / 0,29 nhưng P / R luồng 0,79 / 0,71. Giới hạn đã thấy: khi AI gộp hai hệ thống ngoài (CSDL và email) vào một khối, R luồng vẫn cho điểm đủ (fullstack không nháp: R chặt 0,33, R luồng 1,00). Vì vậy **cách chấm luồng chỉ đi kèm, không thay cách chấm chặt**.

## 5. Nút thắt ở đâu

Mục này chỉ ra lỗi đến từ đâu, có số đo. Cách tách: cho code vẽ cạnh với đúng khối của đáp án; lỗi nào vẫn còn là lỗi của code, lỗi nào biến mất là lỗi do chia khối.

| Nút thắt | Mức | Bằng chứng |
|---|---|---|
| **Chia khối** | Chính | Cạnh thiếu do chia khối: fba 16/17 (Groq), 17/18 (OpenRouter, v7); lnbits 11/13 |
| **Đường ống đưa vào / lấy ra khỏi AI** (trước v8) | Chính, đã sửa phần lớn | v7c: 26 lý do bị loại, 18 chỉ do định dạng chép code. Groq: trả lời bị cắt, JSON hỏng. v8 (trỏ mã dòng): 0 lý do bị loại ở repo nhỏ |
| **Lượt gửi lại tệ hơn lượt đầu** (v8, repo lớn) | Mới thấy | lnbits có nháp: lượt đầu có 23 đường dẫn trùng giữa các khối; lượt sửa chỉ còn phủ 10/170 file, mất khối Dữ liệu. Code đang lấy lượt sau mà không so với lượt đầu |
| **Code vẽ cạnh** | Phụ | Với khối đúng: repo nhỏ 0 sai, 0 thiếu. Repo lớn thiếu 1–2 cạnh; vẽ thừa 47 cạnh, trong đó 34 là lời gọi có thật nhưng người vẽ tay bỏ vì ít quan trọng (chọn mức quan trọng, không phải phân loại sai), 13 phân loại sai (truyền session 6, kiểm tra 4, lắp ráp 3) |
| **Code hiểu sai kiểu dữ liệu** | Phụ | Tham số `session: SessionDep` (alias khai báo trong `deps.py`) làm `session.exec(...)` bị hiểu là gọi vào `deps.py` (fullstack) |
| **Hạ tầng** | Đã hết với OpenRouter | Groq miễn phí 8 nghìn token/phút, 6 nghìn/request; model suy luận tới 27–31 nghìn token/request. OpenRouter: 16 lần chạy, 93 request, 640 nghìn token, 0,079 USD. Còn lỗi: OpenRouter đôi khi trả thân rỗng (chỉ dòng trống); đã sửa để coi như rớt mạng và thử lại (3 lần xảy ra sau khi sửa, cả 3 thử lại thành công) |

Kết luận: nút thắt lớn nhất trước đây là **cách đưa dữ liệu vào và lấy kết quả ra khỏi AI**, không phải AI kém. Khi sửa đường ống (v8), AI chia khối đúng ở repo nhỏ và vừa. Ở repo lớn, AI tốt hơn luật về xếp file nhưng mũi tên vẫn thiếu; chưa rõ do model hay do cách hỏi.

## 6. Bài toán khó đến đâu

Mục này đặt bài toán vào bối cảnh nghiên cứu. Tên chuyên môn: **khôi phục kiến trúc** (architecture recovery), tức dựng lại kiến trúc từ code.

- 6 kỹ thuật tự động so với 8 kiến trúc chuẩn: độ giống chỉ **38–59%** (thước đo MoJoFM: 100% là giống hệt) [Garcia và cộng sự, ASE 2013].
- 10 công cụ trên 9 hệ thống: MoJoFM **0,14–0,76**. Khôi phục tay một hệ thống lớn "có thể tốn hàng trăm giờ chuyên gia"; 9 hệ thống vẫn bị tác giả gọi là bộ dữ liệu "rất nhỏ" [SemRef, 2026].
- Dựng kiến trúc chuẩn cho 4 hệ thống (70–280 nghìn dòng) cần kỹ sư của chính hệ thống tham gia [Garcia và cộng sự, ICSE 2013]. Không có chuẩn chung về độ chi tiết.
- Nhận ra component chỉ từ code: F1 0,58; khi có tài liệu kiến trúc: 0,76 [Who's Who, 2025].
- Ở dự án này: đáp án đổi 4 lần trong 5 ngày; cùng một repo có nhiều cách vẽ hợp lý (mục 4, ví dụ fullstack).

Kết luận: tự động vẽ đúng mọi repo là **bài toán mở** trong nghiên cứu. Nhưng phạm vi hẹp (FastAPI, repo nhỏ và vừa, C4 mức 2, có bằng chứng) **làm được**: v8 đạt tiêu chí ở 4/4 repo nhỏ và kibo.

## 7. Thế giới đã làm gì

Mục này so với công cụ và paper tìm được (tìm ngày 30/09/2026).

**Công cụ**

| Công cụ | Làm gì | Bằng chứng về code | Công bố độ đúng? |
|---|---|---|---|
| DeepWiki (Cognition, 4/2025) | Wiki + sơ đồ Mermaid cho repo GitHub | Trả lời chat có trích dẫn tới dòng | Không |
| Google Code Wiki (11/2025) | Wiki, sơ đồ kiến trúc, lớp, trình tự | Mỗi mục có link tới file và định nghĩa | Không |
| CodeBoarding (MIT, 2,5 nghìn sao) | Phân tích tĩnh (đồ thị lời gọi) + LLM nhóm khối | "Kiểm kết quả LLM với phân tích tĩnh"; có tham chiếu nguồn | Không |
| GitDiagram (17,6 nghìn sao) | Repo → sơ đồ | Bấm khối → file hoặc thư mục | Không |
| Swark (1,7 nghìn sao), flowchitect | Code → sơ đồ qua LLM | flowchitect buộc mỗi khối/quan hệ ghi file nguồn (mức file) | Không |

**Paper**

| Paper | Cách làm | Kết quả |
|---|---|---|
| ArchAgent (ICASSP 2026) | Tóm tắt từng file bằng LLM (được gọi công cụ xem cây thư mục, đọc file, ai tham chiếu ai) → README từ các điểm vào → sơ đồ từng phần → ghép | F1 0,966 so với DeepWiki 0,860, do 30 kỹ sư chấm; không gắn bằng chứng; **không công bố code**, chỉ công bố prompt và bộ dữ liệu (8 repo rất lớn, đáp án dạng ảnh và PDF) |
| SemRef (2026) | LLM **sửa** kết quả của công cụ có sẵn | Tăng 17–43%; Llama 70B hỏng ở 2 repo lớn nhất |
| Rukmono và cộng sự (ICSE-NIER 2024) | Khôi phục từ trên xuống bằng GPT-4 | Đúng 70% trên 54 class |
| Santilli và cộng sự (ECSA 2025) | LLM dùng như công cụ có sẵn | Tốt ở phong cách kiến trúc; yếu ở quan hệ phức tạp |
| Who's Who (2025) | Chỉ dùng LLM cho việc con nó làm tốt | F1 0,87; model mở kém hơn (0,71 so với 0,86) |
| RIG (2026) | Bản đồ kiến trúc tất định từ build, cho agent dùng | Agent đúng hơn 12,2% |

**Nhận xét:** chưa tìm thấy công cụ hay paper nào vẽ C4 mức 2 mà mọi khối và mũi tên có bằng chứng `file:dòng` do máy kiểm **và** công bố độ đúng. Công cụ thương mại có link về code nhưng không công bố số đo; paper có số đo nhưng không gắn bằng chứng. Đây có thể là điểm khác biệt của dự án. Nói "chưa tìm thấy", không nói "chưa ai làm".

**Có dựng lại ArchAgent để so được không:** được một phần. Có prompt và mô tả 4 bước, nhưng thiếu code và thuật toán ghép sơ đồ. Họ chấm bằng người, nên số 0,966 không so thẳng được với số của ta. Có thể dựng một bản "kiểu ArchAgent" chạy trên 8 repo của ta, chấm cùng thước đo; tên node của họ là tên file/hàm gốc nên ánh xạ về file được. Chưa làm.

## 8. Kinh nghiệm rút ra

Mục này ghi những điều nên nhớ cho các bước sau.

1. **Đừng bắt AI chép lại dữ liệu.** Cho AI trỏ vào mã, code tra ngược. Lỗi chép chiếm phần lớn thất bại trước v8.
2. **Test giả (FakeLLM) không bắt được lỗi của model thật.** Ba lỗi đường ống đều qua test 100%. Nên lấy câu trả lời thật trong cache làm test.
3. **Đo từng phần trước khi chạy cả pipeline.** Các phép đo 0 token (khối đúng như đáp án → code vẽ cạnh ra sao; phát lại câu trả lời cũ qua code mới) chỉ ra nút thắt nhanh và rẻ hơn chạy lại.
4. **Đừng vá luật theo repo.** Chỉnh bản nháp nhiều lần: sửa làm repo này tốt lên thì repo kia kém đi. Luật phải chung, và dừng khi không còn cải thiện chung.
5. **Đáp án là một cách vẽ, không phải cách duy nhất.** Cần cả cách chấm chặt lẫn cách chấm chấp nhận vẽ khác, và đọc hai cách cùng nhau.
6. **Model suy luận ăn chỗ trả lời.** Đặt mức suy luận theo bước; bị cắt thì hỏi lại với mức thấp; lưu văn bản suy luận để đọc lại.
7. **Chạy song song cần xử lý lỗi mạng kỹ.** Một phản hồi rỗng từ nhà cung cấp làm chết 8/16 lần chạy trước khi sửa.

## 9. Việc tiếp theo (đề xuất, chưa làm)

- Lượt gửi lại: giữ câu trả lời nào ít vấn đề hơn và phủ nhiều file hơn, thay vì luôn lấy lượt sau (sửa lỗi lnbits).
- Thêm một kiểm bằng dữ kiện chắc: khối Hạ tầng chứa hai loại kết nối ngoài khác nhau thì vi phạm luật "mỗi loại hệ thống ngoài một khối".
- Thử Claude Sonnet trên repo nhỏ và vừa, cùng thước đo (Khiêm: khi gpt-oss khả quan).
- Repo lớn: học ArchAgent (tóm tắt từng file bằng LLM, lần theo điểm vào, chia nhóm có chồng lấn).
- Sửa `calls.py`: kiểu `Annotated[..., Depends(...)]` khai báo ở file khác.
- Có thêm 2–3 repo kín cỡ nhỏ: cả 4 repo nhỏ hiện đều đã lộ.

## Nguồn

- Garcia, Ivkovic, Medvidovic. A comparative analysis of software architecture recovery techniques. ASE 2013. https://dl.acm.org/doi/10.1109/ASE.2013.6693106
- Garcia, Krka, Mattmann, Medvidovic. Obtaining ground-truth software architectures. ICSE 2013. https://dl.acm.org/doi/10.5555/2486788.2486911
- SemRef: Semantic-Enhanced Automatic Refinement of Architecture Recovery Results Using LLMs. 2026. https://arxiv.org/html/2607.23774
- ArchAgent: Scalable Legacy Software Architecture Recovery with LLMs. 2026. https://arxiv.org/abs/2601.13007 — prompt: https://github.com/panrusheng/ArchAgent-supplement — dữ liệu: https://github.com/panrusheng/arch-eval-benchmark
- Who's Who? LLM-assisted Software Traceability with Architecture Entity Recognition. 2025. https://arxiv.org/html/2511.02434
- Repository Intelligence Graph. 2026. https://arxiv.org/abs/2601.10112
- Rukmono, Ochoa, Chaudron. Deductive Software Architecture Recovery via Chain-of-thought Prompting. ICSE-NIER 2024. https://dl.acm.org/doi/10.1145/3639476.3639776
- Santilli và cộng sự. Automated Software Architecture Design Recovery from Source Code Using LLMs. ECSA 2025. https://conf.researchr.org/details/ecsa-2025/ecsa-2025-call-for-research-papers/7/Automated-Software-Architecture-Design-Recovery-from-Source-Code-Using-LLMs
- Schmid và cộng sự. Software Architecture Meets LLMs: A Systematic Literature Review. 2025. https://arxiv.org/abs/2505.16697
- Anthropic Citations API. https://claude.com/blog/introducing-citations-api
- DeepWiki: https://cognitionai.mintlify.app/work-with-devin/deepwiki — Google Code Wiki: https://developers.googleblog.com/introducing-code-wiki-accelerating-your-code-understanding/ — CodeBoarding: https://github.com/CodeBoarding/CodeBoarding — GitDiagram: https://github.com/ahmedkhaleel2004/gitdiagram — Swark: https://github.com/swark-io/swark — flowchitect: https://github.com/kryptokommunist/flowchitect
