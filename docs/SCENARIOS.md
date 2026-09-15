# Scenarios — Code → L3 Generator

Dự án: **Code → Architecture / L3 Generator**
Phiên bản: v1.3 — bổ sung Scenario 10 (repo đa ngôn ngữ), cập nhật nhận diện theo đơn vị service

> Use case tương ứng: [USE_CASES.md](USE_CASES.md) · Sơ đồ: [usecase-overview.svg](diagrams/usecase-overview.svg)
> Các số liệu trong tài liệu này là **ví dụ minh hoạ** một lần chạy điển hình, không phải kết quả đo thực tế. Kết quả đo thật nằm ở `EVALUATION.md`.

---

## Scenario 1 — Sinh tài liệu L3 cho một service chưa quen

| | |
|---|---|
| **Scenario** | Sinh tài liệu L3 cho một service chưa quen |
| **Actors** | Developer |
| **Pre-condition** | Đã cài `l3gen` bằng `pip install -e .`<br>Có thư mục source `./services/order-service/` chứa code Python/FastAPI.<br>Đã cấu hình biến môi trường `L3GEN_API_KEY`. |
| **Post-condition** | Developer hiểu được service có những API nào, đụng vào bảng nào, gọi ra ngoài đâu — và kiểm chứng được từng dòng về source gốc. |

**Main events**

1. Developer được giao sửa một bug trong `order-service`, một service anh chưa từng đọc code.
2. Developer mở terminal và gõ lệnh `l3gen ./services/order-service/`.
3. Terminal in dòng nhận diện stack: "Phát hiện: Python (47/52 file) + FastAPI — tìm thấy trong requirements.txt và import ở 12 file".
4. Terminal in các dòng tiến trình: "Đang phân tích cú pháp...", "Đang trích xuất route, entity, external call...", "Đang đối chiếu tham chiếu xuyên file...", "Đang sinh mô tả (AI)...", "Đang rà soát cảnh báo (AI)...".
5. Terminal in bảng tóm tắt kết quả:

   | Hạng mục | Số lượng |
   |---|---|
   | File đã quét | 47 |
   | File bỏ qua | 2 |
   | API route | 23 |
   | DB entity | 11 |
   | External dependency | 6 |
   | Thời gian chạy | 18,3 giây |

6. Terminal in dòng cuối: "Đã ghi: L3.md, diagram.mmd, graph.json, IAM.json vào ./l3-output/" kèm gợi ý "Chạy `l3gen ui ./l3-output/` để xem trên giao diện web".
7. Developer mở file `./l3-output/L3.md`.
8. Đầu tài liệu hiện phần Tổng quan gồm: stack đã nhận diện (Python + FastAPI), số file đã phân tích, số thành phần tìm được, phân bố mức tin cậy "19 exact, 4 partial, 0 inferred", và dòng ghi chế độ chạy "có mô tả AI".
9. Developer cuộn xuống mục "API Routes" và thấy bảng gồm các cột Method, Path, Handler, Gọi tới, Tin cậy, Lý do, Vị trí, Mô tả:

   | Method | Path | Handler | Tin cậy | Vị trí |
   |---|---|---|---|---|
   | POST | /orders | create_order_endpoint | exact | api/orders.py:24-38 |
   | GET | /orders/{order_id} | get_order_endpoint | exact | api/orders.py:41-52 |
   | PUT | /orders/{order_id}/cancel | cancel_order_endpoint | exact | api/orders.py:55-70 |

10. Developer cuộn tiếp xuống mục "DB Entities" và thấy entity `Order` gắn với bảng `orders`, có khoá ngoại `customer_id` trỏ tới `customers.id`.
11. Developer cuộn xuống mục "Dependency Diagram" và thấy sơ đồ Mermaid vẽ quan hệ giữa các route, service và bảng dữ liệu.
12. Developer đã nắm được cấu trúc service trong khoảng 5 phút, thay vì đọc hết 47 file.

---

## Scenario 2 — Kiểm chứng một dòng tài liệu về đúng source gốc

| | |
|---|---|
| **Scenario** | Kiểm chứng một dòng tài liệu về đúng source gốc |
| **Actors** | Architect / Reviewer |
| **Pre-condition** | Đã có file `L3.md` sinh từ Scenario 1.<br>Có quyền đọc source code của repo tương ứng. |
| **Post-condition** | Reviewer xác nhận được dòng tài liệu khớp với code thật, không phải do AI bịa ra. |

**Main events**

1. Reviewer đọc tài liệu L3 và thấy dòng ghi route `PUT /orders/{order_id}/cancel` gọi tới `OrderService.cancel_order`.
2. Reviewer nghi ngờ vì trong thiết kế ban đầu không có endpoint huỷ đơn.
3. Reviewer nhìn cột "Vị trí" của dòng đó, thấy ghi `api/orders.py:55-70`.
4. Reviewer mở file `api/orders.py` và nhảy tới dòng 55.
5. Tại dòng 55-70, Reviewer thấy đúng đoạn code khai báo endpoint huỷ đơn với decorator `@router.put("/{order_id}/cancel")`.
6. Reviewer xác nhận endpoint này có thật trong code, tức là code đã đi trước tài liệu thiết kế.
7. Reviewer nhìn cột "Mô tả" ở cùng dòng, thấy ghi chú rõ đây là phần do AI sinh ra để dễ đọc.
8. Reviewer đọc dòng cảnh báo ở đầu tài liệu: "Cột Mô tả do AI sinh thêm — KHÔNG dùng làm căn cứ xác lập cấu trúc."
9. Reviewer kết luận: dữ liệu cấu trúc đáng tin vì tra ngược được, còn phần mô tả chỉ dùng để đọc cho nhanh.
10. Reviewer ghi nhận endpoint này vào danh sách cần cập nhật lại tài liệu thiết kế.

---

## Scenario 3 — Chạy khi không có API key

| | |
|---|---|
| **Scenario** | Chạy khi không có API key |
| **Actors** | Developer |
| **Pre-condition** | Đã cài `l3gen`.<br>Biến môi trường `L3GEN_API_KEY` và `ANTHROPIC_API_KEY` đều chưa được đặt. |
| **Post-condition** | Tài liệu vẫn được sinh đầy đủ phần dữ liệu chứng minh được; người chạy biết rõ phần nào đang thiếu và vì sao. |

**Main events**

1. Developer chạy tool trên máy mới cài, chưa kịp cấu hình API key.
2. Developer gõ lệnh `l3gen ./services/order-service/`.
3. Terminal in dòng cảnh báo ngay đầu: "Chưa cấu hình API key — đang chạy chế độ phân tích tĩnh. Tài liệu sẽ không có mô tả AI và không có mục Review Findings."
4. Tool **không dừng lại**, tiếp tục chạy các bước phân tích tĩnh.
5. Terminal in bảng tóm tắt với cùng số liệu route/entity/external call như khi có API key: 23 route, 11 entity, 6 external dependency.
6. Terminal in dòng cuối: "Đã ghi: L3.md, diagram.mmd, graph.json, IAM.json vào ./l3-output/".
7. Developer mở `L3.md` và thấy phần Tổng quan ghi chế độ chạy là "không có mô tả AI".
8. Bảng "API Routes" hiện đầy đủ các cột Method, Path, Handler, Tin cậy, Vị trí — chỉ riêng cột "Mô tả (AI)" bị bỏ trống toàn bộ.
9. Mục "Review Findings" hiện dòng "Bước rà soát AI không chạy trong lần này (chưa cấu hình API key)."
10. Mục "Known Limitations" ghi thêm một dòng tương ứng, để người đọc sau này biết tài liệu này thiếu phần nào.
11. Developer xác nhận toàn bộ dữ liệu cấu trúc vẫn dùng được bình thường, chỉ thiếu phần diễn giải.

---

## Scenario 4 — Gặp code không phân tích tĩnh được

| | |
|---|---|
| **Scenario** | Gặp code không phân tích tĩnh được |
| **Actors** | Developer, Architect / Reviewer |
| **Pre-condition** | Repo có ít nhất một route khai báo với prefix lấy từ biến cấu hình.<br>Repo có ít nhất một file lỗi cú pháp. |
| **Post-condition** | Tool không bỏ sót âm thầm: mọi chỗ không chắc chắn đều được ghi nhận kèm lý do đọc hiểu được. |

**Main events**

1. Developer chạy tool trên một repo có cấu trúc phức tạp hơn bình thường.
2. Terminal in bảng tóm tắt, trong đó dòng "File bỏ qua" ghi số 2.
3. Developer mở `L3.md` và cuộn xuống mục "API Routes".
4. Ở bảng route, Developer thấy một dòng có cột Tin cậy ghi `partial` thay vì `exact`:

   | Method | Path | Tin cậy | Lý do |
   |---|---|---|---|
   | GET | {settings.API_PREFIX}/orders | partial | prefix từ biến settings.API_PREFIX, không resolve được giá trị |

5. Developer hiểu rằng route này có thật, nhưng đường dẫn đầy đủ chỉ biết được lúc chạy thật.
6. Developer cuộn xuống mục "Known Limitations".
7. Mục này liệt kê hai file bị bỏ qua kèm lý do: `legacy/old_api.py` — lỗi cú pháp dòng 142; `scripts/migrate.py` — lỗi cú pháp dòng 7.
8. Mục này liệt kê tiếp các tham chiếu chưa xác định được đích, trong đó có dòng ghi khoá ngoại `payment_id` trỏ tới bảng `payments` không tồn tại trong phạm vi đã quét.
9. Developer chuyển tài liệu cho Reviewer.
10. Reviewer đọc mục "Review Findings" và thấy cảnh báo loại `unresolved_reference` cho chính khoá ngoại `payment_id`, kèm vị trí `models/order.py:31`.
11. Reviewer mở `models/order.py` dòng 31, xác nhận bảng `payments` nằm ở service khác — đúng như tool đã cảnh báo, không phải lỗi của tool.
12. Reviewer kết luận: phạm vi quét cần mở rộng sang service thanh toán nếu muốn có bức tranh đầy đủ.

---

## Scenario 5 — Rà soát cảnh báo thiếu sót trong codebase

| | |
|---|---|
| **Scenario** | Rà soát cảnh báo thiếu sót trong codebase |
| **Actors** | Architect / Reviewer |
| **Pre-condition** | Đã có `L3.md` sinh với chế độ đầy đủ (có API key).<br>Repo có ít nhất một entity không được route nào sử dụng. |
| **Post-condition** | Reviewer có danh sách điểm cần kiểm tra, mỗi điểm kèm bằng chứng cụ thể để tự xác minh. |

**Main events**

1. Reviewer chuẩn bị cho buổi review kiến trúc định kỳ của `order-service`.
2. Reviewer mở `L3.md` và cuộn thẳng tới mục "Review Findings".
3. Hệ thống hiện bảng cảnh báo gồm ba cột: Loại, Mô tả, Vị trí bằng chứng:

   | Loại | Mô tả | Vị trí |
   |---|---|---|
   | orphan_entity | Entity `AuditLog` không được route hay function nào tham chiếu trong phạm vi đã quét | models/audit.py:12 |
   | external_call_no_error_handling | Lời gọi tới payment gateway không thấy xử lý lỗi bao quanh | services/payment.py:58 |
   | empty_handler_calls | Route `GET /health` có handler không gọi tới thành phần nào khác | api/health.py:8 |

4. Reviewer đọc dòng ghi chú phía trên bảng: "Đây là cảnh báo cần con người xác nhận, KHÔNG phải kết luận chắc chắn."
5. Reviewer bấm vào vị trí `services/payment.py:58` để mở file.
6. Tại dòng 58, Reviewer thấy lời gọi `httpx.post(...)` tới cổng thanh toán thật sự không có khối `try/except` bao quanh.
7. Reviewer xác nhận đây là vấn đề thật và ghi vào danh sách việc cần sửa.
8. Reviewer kiểm tra tiếp cảnh báo `orphan_entity` ở `models/audit.py:12`.
9. Reviewer biết entity `AuditLog` được ghi bởi một background worker nằm ngoài phạm vi quét, nên đây là cảnh báo đúng về mặt dữ liệu nhưng không phải vấn đề thật.
10. Reviewer đánh dấu cảnh báo này là "đã xem xét, không cần xử lý" trong biên bản review.
11. Reviewer kiểm tra cảnh báo `empty_handler_calls` ở `api/health.py:8` và xác nhận đây là endpoint kiểm tra sức khoẻ, không gọi gì là đúng thiết kế.
12. Reviewer kết luận: trong ba cảnh báo, một là vấn đề thật cần sửa, hai là đúng như thiết kế.

---

## Scenario 6 — Xuất graph cho hệ thống khác dùng lại

| | |
|---|---|
| **Scenario** | Xuất graph cho hệ thống khác dùng lại |
| **Actors** | Developer, Hệ thống khác |
| **Pre-condition** | Đã chạy tool và có file `./l3-output/graph.json`. |
| **Post-condition** | Một công cụ khác đọc được cấu trúc codebase mà không cần tự phân tích lại source. |

**Main events**

1. Đội platform muốn xây một công cụ trả lời câu hỏi "API nào đụng vào bảng `orders`".
2. Developer chạy `l3gen ./services/order-service/` để sinh dữ liệu đầu vào.
3. Developer mở file `./l3-output/graph.json` để xem cấu trúc.
4. File chứa hai mảng chính là `nodes` và `edges`. Mỗi node gồm định danh, loại, nhãn và vị trí trong source:

   ```json
   {
     "id": "route:POST /orders",
     "type": "Route",
     "label": "POST /orders",
     "location": { "file": "api/orders.py", "line_start": 24, "line_end": 38 }
   }
   ```

5. Mỗi edge gồm node nguồn, node đích, loại quan hệ và cờ cho biết đã resolve được hay chưa:

   ```json
   {
     "source_id": "route:POST /orders",
     "target_id": "function:OrderService.create_order",
     "type": "calls",
     "resolved": true
   }
   ```

6. Developer viết một đoạn script duyệt graph: từ node bảng `orders` đi ngược theo các cạnh `reads_writes` và `calls` để tìm ra các route liên quan.
7. Script trả về ba route: `POST /orders`, `GET /orders/{order_id}`, `PUT /orders/{order_id}/cancel`.
8. Developer đối chiếu kết quả với mục "API Routes" trong `L3.md` và thấy khớp.
9. Developer kiểm tra một cạnh bất kỳ trong graph, xác nhận nó tương ứng đúng với một dòng dữ liệu trong tài liệu — graph không chứa thông tin nào mà tài liệu không có.
10. Đội platform dùng `graph.json` làm nguồn dữ liệu, không cần tự viết lại phần phân tích cú pháp.

---

## Scenario 7 — Đo độ chính xác của công cụ

| | |
|---|---|
| **Scenario** | Đo độ chính xác của công cụ |
| **Actors** | Developer (2 người) |
| **Pre-condition** | Đã chọn được một repo FastAPI mã nguồn mở quy mô vài chục file.<br>Pipeline phân tích tĩnh đã hoàn thiện. |
| **Post-condition** | Có `EVALUATION.md` với số đo precision/recall thật, kèm phân tích nguyên nhân từng trường hợp sai. |

**Main events**

1. Hai thành viên cần trả lời câu hỏi "công cụ này chính xác tới đâu" bằng số liệu thay vì cảm tính.
2. Cả hai chọn một repo FastAPI mã nguồn mở, ghi lại commit hash để về sau tái lập được.
3. **Trước khi chạy tool**, mỗi người đọc tay toàn bộ repo và tự liệt kê độc lập: danh sách API route, danh sách DB entity, danh sách external call.
4. Hai người đối chiếu hai danh sách và phát hiện lệch nhau ở 3 mục.
5. Cả hai thảo luận từng mục lệch, thống nhất kết quả, và ghi nhận rằng 3 mục này là chỗ ngay cả người đọc cũng thấy mơ hồ.
6. Kết quả thống nhất được ghi thành file `ground_truth.json` và commit vào repo.
7. Một người chạy `l3gen` trên đúng repo đó.
8. Người này viết script so sánh output của tool với `ground_truth.json`, tính ra bảng chỉ số:

   | Loại | Ground truth | Tool tìm được | Đúng | Recall | Precision |
   |---|---|---|---|---|---|
   | API route | 45 | 43 | 43 | 95,6% | 100% |
   | DB entity | 11 | 11 | 11 | 100% | 100% |
   | External call | 9 | 7 | 7 | 77,8% | 100% |

9. Script tính thêm precision tách theo mức tin cậy: nhóm `exact` đạt 100%, nhóm `partial` đạt 88%.
10. Hai người xác nhận điều quan trọng: precision của nhóm `exact` cao hơn nhóm `partial`, tức là nhãn tin cậy phản ánh đúng thực tế chứ không phải nhãn trang trí.
11. Hai người phân loại toàn bộ trường hợp bỏ sót thành nhóm nguyên nhân:

   | Nguyên nhân | Số lượng | Xử lý được không |
   |---|---|---|
   | Route đăng ký động trong vòng lặp | 2 | Không — giới hạn bản chất của phân tích tĩnh |
   | External call qua lớp bọc tự viết | 2 | Có — cần thêm rule |

12. Hai người đối chiếu với ngưỡng đã đặt ra từ trước: recall route ≥ 85% (đạt), recall external call ≥ 80% (không đạt, thiếu 2,2%).
13. Hai người **không hạ ngưỡng**; thay vào đó ghi rõ vào `EVALUATION.md` phần chưa đạt cùng nguyên nhân và hướng khắc phục.
14. Người viết báo cáo đặt phần tóm tắt 4 câu lên đầu `EVALUATION.md`, trong đó có câu "Không có trường hợp nào công cụ báo ra một route không tồn tại."

---

## Scenario 8 — Xem kết quả trên giao diện web

| | |
|---|---|
| **Scenario** | Xem kết quả trên giao diện web |
| **Actors** | Developer, Architect / Reviewer |
| **Pre-condition** | Đã chạy `l3gen` và có đủ 4 file trong `./l3-output/`.<br>Máy có trình duyệt. Không cần mạng. |
| **Post-condition** | Người xem nắm được cấu trúc service và biết chỗ nào tool không chắc chắn, mà không phải đọc Markdown thô. |

**Main events**

1. Developer muốn trình bày cấu trúc `order-service` cho cả nhóm trong buổi họp thiết kế.
2. Developer gõ lệnh `l3gen ui ./l3-output/`.
3. Terminal in "Đang phục vụ tại http://localhost:8000 — nhấn Ctrl+C để dừng" và trình duyệt tự mở.
4. Màn hình **Tổng quan** hiện ra gồm: bốn thẻ số (47 file, 23 route, 11 entity, 6 external dependency), biểu đồ tròn phân bố mức tin cậy, danh sách ba cảnh báo nổi bật, và thanh điều hướng sang các màn còn lại.
5. Thẻ phân bố tin cậy hiển thị "19 exact · 4 partial · 0 inferred", trong đó phần `partial` có màu cảnh báo riêng.
6. Developer bấm vào mục **API Routes** trên thanh điều hướng.
7. Màn hình hiện bảng route kèm ô tìm kiếm, bộ lọc theo method (GET/POST/PUT/DELETE) và bộ lọc theo mức tin cậy.
8. Developer bấm bộ lọc "partial" để xem riêng các route không chắc chắn.
9. Bảng thu lại còn 4 dòng, mỗi dòng có nhãn màu cảnh báo và dòng lý do hiện ngay bên dưới đường dẫn.
10. Developer bấm vào dòng `GET {settings.API_PREFIX}/orders`.
11. Panel chi tiết trượt ra từ bên phải gồm: đường dẫn đầy đủ, tên hàm xử lý, danh sách hàm được gọi kèm module đã resolve, vị trí `api/orders.py:41-52` có nút copy, và khối mô tả AI đặt trên nền khác biệt với nhãn "AI" ở đầu.
12. Developer bấm mục **Dependency Graph**.
13. Màn hình hiện đồ thị tương tác: mỗi loại node một màu (route, class, function, entity, external host), có thể kéo thả, phóng to thu nhỏ và lọc theo loại.
14. Developer bấm vào node `orders` (bảng dữ liệu).
15. Đồ thị làm nổi bật node đó cùng các cạnh liên quan, các node còn lại mờ đi; panel bên phải liệt kê ba route có đường đi tới bảng này.
16. Một thành viên trong nhóm hỏi về độ tin cậy của tài liệu; Developer bấm mục **Known Limitations**.
17. Màn hình liệt kê hai file bị bỏ qua kèm lý do lỗi cú pháp, và các tham chiếu chưa xác định được đích.
18. Developer đóng trình duyệt và nhấn Ctrl+C ở terminal để dừng server.

---

## Scenario 9 — Chạy trên repo dùng framework chưa hỗ trợ

| | |
|---|---|
| **Scenario** | Chạy trên repo dùng framework chưa hỗ trợ |
| **Actors** | Developer |
| **Pre-condition** | Đã cài `l3gen`.<br>Có một repo Python viết bằng Flask (chưa nằm trong phạm vi hỗ trợ). |
| **Post-condition** | Developer biết chính xác vì sao tool không chạy được và cần làm gì tiếp — không hiểu nhầm là repo trống hoặc tool hỏng. |

**Main events**

1. Developer nghe đồng nghiệp giới thiệu tool, muốn thử trên service của mình.
2. Developer gõ lệnh `l3gen ./services/notification-service/`.
3. Tool duyệt thư mục tìm file manifest và thấy đúng một file `requirements.txt` ở thư mục gốc — kết luận đây là repo một đơn vị phân tích.
4. Tool đọc `requirements.txt` và thấy dòng `Flask==3.0.0`.
5. Tool kiểm tra thêm trong source và thấy `from flask import Flask` ở `app/main.py`.
6. Tool đối chiếu với ma trận hỗ trợ, xác định Flask chưa được hỗ trợ và đánh dấu đơn vị này `analyzed = False`.
7. Vì đây là đơn vị duy nhất và nó không phân tích được, tool **dừng lại**, không chạy các bước trích xuất.
8. Terminal in thông báo:

   ```
   Không có đơn vị nào phân tích được.

   Phát hiện 1 đơn vị:
     [x] notification-service/   Python + Flask   -> chưa hỗ trợ

   Căn cứ: "Flask==3.0.0" trong requirements.txt
           và "from flask import Flask" trong app/main.py

   Công cụ hiện hỗ trợ: Python + FastAPI
   Đang trong kế hoạch: Flask, Django, Java/Spring

   Không có file nào được ghi ra.
   ```

9. Tool thoát với mã lỗi 1, thư mục `l3-output` không được tạo.
10. Developer hiểu rằng vấn đề không nằm ở repo của mình, mà ở phạm vi hỗ trợ hiện tại của tool.
11. Developer ghi nhận Flask vào danh sách đề xuất mở rộng cho đội phát triển tool.

**Điểm mấu chốt của scenario này:** nếu tool cứ chạy tiếp rồi sinh ra tài liệu với 0 route, Developer sẽ tưởng service của mình không có API nào, hoặc tưởng tool bị lỗi. Cả hai hiểu nhầm đều tệ hơn việc dừng lại và nói thật.

**Lưu ý — khác với Scenario 10:** ở đây đơn vị duy nhất không phân tích được nên tool dừng hẳn. Khi repo có nhiều đơn vị mà chỉ một số chưa hỗ trợ, tool vẫn chạy cho phần còn lại (xem Scenario 10).

---

## Scenario 10 — Repo đa ngôn ngữ, chỉ một phần được hỗ trợ

| | |
|---|---|
| **Scenario** | Repo đa ngôn ngữ, chỉ một phần được hỗ trợ |
| **Actors** | Developer |
| **Pre-condition** | Repo chứa hai service: `mobile-app/` viết bằng Java/Spring Boot (có `pom.xml`) và `ai-service/` viết bằng Python/FastAPI (có `requirements.txt`). Hai service giao tiếp qua REST. |
| **Post-condition** | Tài liệu được sinh cho phần hỗ trợ được, và Developer biết chính xác phần nào của hệ thống chưa được bao phủ. |

**Main events**

1. Developer làm việc trên hệ thống có ứng dụng mobile Java gọi sang một AI service viết bằng FastAPI.
2. Developer gõ lệnh `l3gen ./` ở thư mục gốc của repo.
3. Tool duyệt cây thư mục tìm file manifest và tìm thấy hai file: `mobile-app/pom.xml` và `ai-service/requirements.txt`.
4. Tool kết luận repo có **hai đơn vị phân tích**, mỗi thư mục một đơn vị.
5. Tool nhận diện độc lập từng đơn vị: `mobile-app` là Java + Spring Boot; `ai-service` là Python + FastAPI.
6. Tool đối chiếu ma trận hỗ trợ và đánh dấu `mobile-app` là chưa hỗ trợ.
7. Terminal in kết quả nhận diện:

   ```
   Phát hiện 2 đơn vị phân tích:

     [v] ai-service/      Python + FastAPI      -> sẽ phân tích
     [x] mobile-app/      Java + Spring Boot    -> BỎ QUA (chưa hỗ trợ)

   Đang phân tích 1/2 đơn vị...
   ```

8. Tool **không dừng lại**, tiếp tục phân tích `ai-service/` bình thường.
9. Terminal in bảng tóm tắt cho phần đã phân tích: 31 file, 8 route, 3 entity, 2 external dependency.
10. Terminal in cảnh báo cuối cùng: "1 đơn vị bị bỏ qua. Tài liệu này KHÔNG bao gồm mobile-app/."
11. Developer mở `L3.md` và thấy ngay ở phần Tổng quan một bảng liệt kê **cả hai** đơn vị, trong đó `mobile-app` ghi rõ trạng thái "Bỏ qua — chưa hỗ trợ".
12. Developer cuộn xuống mục "API Routes" và thấy mọi dòng đều có cột Service ghi `ai-service`.
13. Developer cuộn xuống mục "Known Limitations" và đọc dòng: "Đơn vị `mobile-app/` (Java + Spring Boot, 84 file) không được phân tích. Các API mà mobile-app cung cấp, cũng như lời gọi từ mobile-app sang ai-service, không có trong tài liệu này."
14. Developer hiểu rằng tài liệu mô tả đúng nửa hệ thống, và biết chính xác nửa nào còn thiếu.
15. Developer dùng tài liệu cho công việc trên `ai-service`, không nhầm tưởng đây là bức tranh toàn hệ thống.

**Điểm mấu chốt:** nếu tool chọn ngôn ngữ theo số file chiếm đa số, nó sẽ thấy Java 84 file so với Python 31 file, kết luận "đây là project Java", rồi báo chưa hỗ trợ và dừng hẳn — **bỏ lỡ hoàn toàn service FastAPI vốn phân tích được**. Đó là lý do phải chia đơn vị theo manifest trước khi nhận diện stack.

---

## Bảng tổng hợp

| STT | Scenario | Actors | Use case liên quan | Artifact liên quan |
|---|---|---|---|---|
| 1 | Sinh tài liệu L3 cho một service chưa quen | Developer | UC1, UC3, UC9 | L3.md, diagram.mmd, graph.json, IAM.json |
| 2 | Kiểm chứng một dòng tài liệu về đúng source gốc | Architect/Reviewer | UC5 | L3.md, source code |
| 3 | Chạy khi không có API key | Developer | UC2 | L3.md (không có mô tả AI) |
| 4 | Gặp code không phân tích tĩnh được | Developer, Architect/Reviewer | UC1, UC4, UC6 | L3.md (Known Limitations, Review Findings) |
| 5 | Rà soát cảnh báo thiếu sót trong codebase | Architect/Reviewer | UC4, UC5 | L3.md (Review Findings), source code |
| 6 | Xuất graph cho hệ thống khác dùng lại | Developer, Hệ thống khác | UC7 | graph.json |
| 7 | Đo độ chính xác của công cụ | Developer | — (quy trình kiểm chứng) | ground_truth.json, EVALUATION.md |
| 8 | Xem kết quả trên giao diện web | Developer, Architect/Reviewer | UC8 | IAM.json, graph.json (qua Web UI) |
| 9 | Chạy trên repo dùng framework chưa hỗ trợ | Developer | UC1 (luồng thay thế 2b) | — (không sinh file) |
| 10 | Repo đa ngôn ngữ, chỉ một phần được hỗ trợ | Developer | UC1 (luồng thay thế 2c) | L3.md (một phần), Known Limitations |
