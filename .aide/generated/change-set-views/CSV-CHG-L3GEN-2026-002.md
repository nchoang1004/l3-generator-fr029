---
key: CSV-CHG-L3GEN-2026-002
group: derived
non_normative: true
derived_from: [BL-CHG-L3GEN-2026-002-r4]
hand_written: false
status: candidate
generated_by: scripts/prd_package.py render --baseline BL-r4.yaml
---

# Làm lại phạm vi — mô hình ngôn ngữ đề xuất, code kiểm bằng chứng

Bản ứng viên chưa duyệt, sinh từ `BL-CHG-L3GEN-2026-002-r4`. Khi view và nguồn bất đồng, **FR/NFR/PRD nguồn thắng**; sửa nguồn rồi chạy lại script render. Không dùng view này như approval.

Gồm 9 FR, 5 NFR và 1 OBS trong baseline.

## 1. Mục tiêu

Bốn mục tiêu, xếp theo thứ tự: sinh ra được gì, rồi mới tới tin được tới đâu.

| Goal key | Mục tiêu | Liên kết KPI |
|---|---|---|
| GOAL-L3GEN-004 | Dựng được sơ đồ cấu trúc hệ thống ở mức application/component, phản ánh code đang chạy chứ không phải tài liệu cũ | KPI-L3GEN-006 |
| GOAL-L3GEN-005 | Mọi kết luận trên sơ đồ và tài liệu đều lần ngược được về đúng đoạn source sinh ra nó, để người đọc tự kiểm chứng thay vì phải tin | KPI-L3GEN-007 |
| GOAL-L3GEN-006 | Từ cùng mô hình đó sinh ra tài liệu L3 đủ để người mới đọc hiểu hệ thống mà không cần mở source | KPI-L3GEN-008 |
| GOAL-L3GEN-007 | Nói thật về giới hạn của chính mình: tách rõ phần đọc trực tiếp từ bằng chứng, phần suy ra, và phần không kết luận được, để người đọc biết chỗ nào tin ngay và chỗ nào phải tự kiểm | KPI-L3GEN-009, KPI-L3GEN-010 |

## 2. Mục tiêu nghiệp vụ đổi

Change Set này thay cho `CHG-L3GEN-2026-001`. Mọi GOAL/KPI mang key mới; GOAL/KPI của Change Set cũ không còn hiệu lực. Ánh xạ cũ sang mới ở PRD.

## 3. Tính năng mới

Toàn bộ FR trong candidate baseline; Must/Should và mốc nằm tại từng nguồn.

---

Nguồn: [FR-L3GEN-019](../../requirements/fr/FR-L3GEN-019.md) · revision 1 · status draft · SHA-256 `c561b13248d85aa3a1240a2b30ee2405ad1feeceedc6a5a76cef65a4a304470c`

### FR-L3GEN-019 — Nhận source và chạy phân tích

#### Mô tả

Người dùng chỉ định source rồi bắt đầu một lần phân tích. Dòng lệnh nhận thư mục cục bộ và thư mục output; web nhận file ZIP hoặc URL GitHub public. Công cụ kiểm đầu vào trước khi phân tích và giải thích lỗi thay vì trả kết quả rỗng.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tiếp nhận đầu vào |
| Ưu tiên | Must Have |
| Mốc | M1 cho CLI; M2 cho web |
| Người sở hữu | Vai Product của TEAM-L3GEN |

#### Acceptance Criteria

##### AC-L3GEN-019-01

- **Given:** Người dùng chỉ định một thư mục source đọc được và một thư mục output ghi được.
- **When:** người dùng chạy phân tích qua dòng lệnh.
- **Then:** công cụ phân tích rồi ghi tài liệu L3, diagram và JSON vào thư mục output, và in ra đường dẫn các file đã tạo.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-019-02

- **Given:** Đường dẫn source không tồn tại, là file, không có quyền đọc, hoặc thư mục output không ghi được.
- **When:** người dùng chạy phân tích.
- **Then:** công cụ dừng trước khi phân tích, nêu rõ nguyên nhân và cách sửa, và không tạo thư mục output dở dang.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-019-03

- **Given:** Thư mục source nằm trong thư mục output, hoặc ngược lại.
- **When:** người dùng chạy phân tích.
- **Then:** công cụ từ chối; không đọc lại artifact của chính nó và không ghi vào cây source.
- `constrained_by:` [NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-019-04

- **Given:** Người dùng gửi file ZIP hỏng, sai định dạng, chứa đường dẫn thoát khỏi vùng giải nén, hoặc vượt ngưỡng kích thước.
- **When:** web tiếp nhận file.
- **Then:** công cụ từ chối và nêu lý do; không ghi file ra ngoài vùng xử lý.
- `constrained_by:` [NFR-L3GEN-SEC-002, NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-019-05

- **Given:** Người dùng nhập URL GitHub sai, repository không tồn tại, hoặc repository yêu cầu quyền truy cập.
- **When:** web lấy source.
- **Then:** công cụ báo đúng nguyên nhân truy cập, không hiển thị như repository rỗng và không yêu cầu credential.
- `constrained_by:` [NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-020](../../requirements/fr/FR-L3GEN-020.md) · revision 1 · status draft · SHA-256 `242fa0670871662126dbf0e9b9d39a2948be464b272033c88a459706b94d5602`

### FR-L3GEN-020 — Xác định phạm vi phân tích

#### Mô tả

Người dùng biết phần nào của repository được phân tích, phần nào bị bỏ qua và phần nào nằm ngoài ngôn ngữ hoặc framework được hỗ trợ, trước khi đọc kết quả kiến trúc.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Phân tích repository |
| Ưu tiên | Must Have |
| Mốc | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

#### Acceptance Criteria

##### AC-L3GEN-020-01

- **Given:** Repository chứa nhiều thư mục, trong đó có phần thuộc stack được hỗ trợ và phần không.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ liệt kê các đơn vị phân tích đã xét kèm đường dẫn, và liệt kê riêng phần bỏ qua kèm lý do.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-020-02

- **Given:** Repository rỗng, hoặc toàn bộ nội dung thuộc ngôn ngữ chưa được hỗ trợ.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ báo trạng thái rỗng hoặc ngoài phạm vi hỗ trợ, không trả về kết quả thành công rỗng.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-020-03

- **Given:** Một đơn vị phân tích thuộc ngôn ngữ được hỗ trợ nhưng ở mức độ sâu thấp hơn Python.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ công bố mức hỗ trợ áp dụng cho đơn vị đó, để người đọc biết nhãn chất lượng của kết luận trong đơn vị này được đặt theo mức nào.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-021](../../requirements/fr/FR-L3GEN-021.md) · revision 2 · status draft · SHA-256 `598cb3e9cb8851236f344b56f75c68dc28003df817d289d34f5a09a970f31a04`

### FR-L3GEN-021 — Trích dữ kiện code

#### Mô tả

Công cụ trích từ source các dữ kiện làm nguyên liệu cho mô hình kiến trúc và tài liệu L3 contract: API route cùng request/response model, mô hình dữ liệu, lời gọi ra ngoài, tham chiếu xuyên file, cấu hình, quan hệ sự kiện và thư viện phụ thuộc. Mỗi dữ kiện kèm vị trí file trong snapshot.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Phân tích repository |
| Ưu tiên | Must Have |
| Mốc | M1 cho route, entity, HTTP và tham chiếu; M3 cho config, event và thư viện |
| Người sở hữu | Vai Product của TEAM-L3GEN |

#### Acceptance Criteria

##### AC-L3GEN-021-01

- **Given:** Đơn vị phân tích khai báo API route theo pattern thuộc phạm vi đã công bố.
- **When:** công cụ trích dữ kiện.
- **Then:** mỗi route có method, path, handler và nguồn khai báo; path ghép từ prefix và mount được ghi đầy đủ, phần chưa xác định được mang nhãn partial kèm lý do.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-021-02

- **Given:** Đơn vị phân tích khai báo lớp dữ liệu ánh xạ tới bảng.
- **When:** công cụ trích dữ kiện.
- **Then:** mỗi lớp có tên bảng nếu xác định được, danh sách cột và khóa ngoại; tên bảng sinh lúc chạy để unknown kèm nguồn, không suy từ tên lớp.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-021-03

- **Given:** Đơn vị phân tích gọi HTTP ra ngoài, phát hoặc nhận sự kiện, đọc khóa cấu hình, hoặc khai báo thư viện trong manifest.
- **When:** công cụ trích dữ kiện.
- **Then:** mỗi dữ kiện ghi được nơi sử dụng và mức độ xác định của đích; giá trị bí mật bị che; broker hoặc manifest ngoài phạm vi hỗ trợ hiện ở phần giới hạn thay vì bị bỏ qua.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-021-04

- **Given:** Một lời gọi hoặc tham chiếu có đích không xác định được bằng bảng import và symbol.
- **When:** công cụ trích dữ kiện.
- **Then:** dữ kiện được giữ lại với nhãn unresolved kèm lý do, và không được nâng thành quan hệ kiến trúc ở FR-L3GEN-022.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-AI-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-021-05

- **Given:** Handler của một route khai báo kiểu cho request body, tham số, hoặc response model, ví dụ bằng Pydantic model.
- **When:** công cụ trích dữ kiện.
- **Then:** mỗi route ghi được tên model của request và response cùng danh sách trường, kiểu và trường bắt buộc, kèm vị trí khai báo; status code nếu khai báo trong code. Phần không khai kiểu hoặc sinh lúc chạy để `unknown` kèm lý do, không suy từ tên biến.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-022](../../requirements/fr/FR-L3GEN-022.md) · revision 2 · status draft · SHA-256 `b4b5e77d235b1cde3ca493b726accc11865f013e460617a2496552749b7cf264`

### FR-L3GEN-022 — Dựng component và quan hệ kiến trúc

#### Mô tả

Từ tập dữ kiện code của FR-L3GEN-021, công cụ dựng component, vai trò của chúng và các cạnh dependency ở mức application/component. Việc chia làm hai phần:

| Phần | Ai làm |
|---|---|
| Chia file vào component | Code, tất định: theo cây thư mục, tên và số lời gọi giữa các nhóm. Riêng repository phẳng thì mô hình ngôn ngữ đề xuất cách chia (AC-L3GEN-022-05) |
| Cạnh giữa component | Code, từ lời gọi và tham chiếu đã xác định đích |
| Tên, mô tả, vai trò component; nhãn cạnh | Mô hình ngôn ngữ |
| Cạnh mà phân tích tĩnh không thấy, ví dụ qua REST, queue, cấu hình | Mô hình ngôn ngữ đề xuất; code kiểm dữ kiện chứng minh (AC-L3GEN-022-02) |

Cách chia này học từ CodeBoarding: cho model tự chia component cho kết quả dao động giữa các lần chạy mà không tốt hơn cách chia tất định.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Dựng mô hình kiến trúc |
| Ưu tiên | Must Have |
| Mốc | M2 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

#### Acceptance Criteria

##### AC-L3GEN-022-01

- **Given:** Đã có tập dữ kiện code kèm vị trí file của một đơn vị phân tích, và cây thư mục chia được file source thành ít nhất hai nhóm.
- **When:** công cụ dựng mô hình kiến trúc.
- **Then:** code chia mỗi file source vào đúng một component, và dựng cạnh từ lời gọi, tham chiếu đã xác định đích; mô hình ngôn ngữ đặt tên, mô tả, vai trò cho từng component và gắn nhãn cho từng cạnh, nhưng không thêm, bớt, gộp hay tách component. Mỗi component và mỗi cạnh trỏ được về các dữ kiện code đã sinh ra nó.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002, NFR-L3GEN-AI-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-022-02

- **Given:** Mô hình ngôn ngữ đề xuất thêm một cạnh A→B mà code chưa dựng được.
- **When:** công cụ kiểm đề xuất trước khi đưa vào mô hình kiến trúc.
- **Then:** đề xuất chỉ được giữ khi mọi dữ kiện nó trích dẫn có trong tập dữ kiện của lần chạy và nằm ở file có trong snapshot, và có dữ kiện ở cả hai đầu: một dữ kiện có vị trí thuộc A, một dữ kiện có vị trí thuộc B. Đề xuất không thỏa bị loại, ghi lý do loại, và không xuất hiện trong sơ đồ hoặc tài liệu.
- `constrained_by:` [NFR-L3GEN-AI-002, NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-022-03

- **Given:** Mô hình ngôn ngữ không khả dụng, hết quota, tập dữ kiện vượt trần token của một lần chạy, hoặc model trả về payload sai schema.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ dừng bước dùng model và báo rõ nguyên nhân, trả kết quả partial gồm tập dữ kiện code và phần chia nhóm, cạnh do code dựng; component chưa có tên do model thì đặt tên theo đường dẫn và ghi rõ chưa được đặt tên. Không tự thêm quan hệ bằng cách đoán để lấp chỗ trống.
- `constrained_by:` [NFR-L3GEN-AI-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-022-04

- **Given:** Repository có số lượng thực thể vượt ngưỡng số node của sơ đồ mặc định.
- **When:** công cụ dựng sơ đồ.
- **Then:** sơ đồ mặc định vẫn ở mức application/component trong trần số node đã quy định; phần không lên sơ đồ mặc định được giữ ở lớp bằng chứng, không bị loại khỏi bộ kết quả.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-022-05

- **Given:** Repository phẳng: cây thư mục không chia được file source trong phạm vi thành ít nhất hai nhóm.
- **When:** công cụ dựng mô hình kiến trúc.
- **Then:** mô hình ngôn ngữ đề xuất cách chia file vào component; code kiểm mỗi file source thuộc đúng một component và mỗi file có trong snapshot, loại đề xuất không thỏa kèm lý do. Component chia theo cách này mang nhãn `inferred` với lý do "chia nhóm do model vì cây thư mục không đủ".
- `constrained_by:` [NFR-L3GEN-AI-002, NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-023](../../requirements/fr/FR-L3GEN-023.md) · revision 1 · status draft · SHA-256 `38c1fee95c6ce178adcb690bcc90cc03fb4515e3f6298d569e56bb2cbdacf759`

### FR-L3GEN-023 — Bằng chứng và nhãn mức chắc chắn

#### Mô tả

Người đọc lần ngược được mỗi kết luận về đúng dữ kiện code và file trong snapshot đã phân tích, và phân biệt được phần đọc trực tiếp từ bằng chứng, phần suy ra, và phần chưa kết luận được.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Kiểm chứng kết quả |
| Ưu tiên | Must Have |
| Mốc | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

#### Acceptance Criteria

##### AC-L3GEN-023-01

- **Given:** Người đọc chọn một component, một cạnh dependency hoặc một dữ kiện trong kết quả.
- **When:** người đọc mở phần bằng chứng.
- **Then:** công cụ chỉ ra các dữ kiện code và vị trí của chúng trong snapshot làm cơ sở cho kết luận đó.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-023-02

- **Given:** Một kết luận được công bố trong tài liệu hoặc sơ đồ.
- **When:** công cụ sinh kết quả.
- **Then:** kết luận mang nhãn confidence là exact hoặc inferred và nhãn completeness là full hoặc partial ở hai trường riêng; inferred và partial kèm lý do.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-023-03

- **Given:** Source trên đĩa đã thay đổi so với snapshot đã phân tích.
- **When:** người đọc mở bằng chứng của một kết luận.
- **Then:** công cụ báo snapshot không còn khớp, không dùng nội dung source mới làm bằng chứng cho kết luận cũ.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-023-04

- **Given:** Một kết luận không có bằng chứng là dữ kiện code có thật trong snapshot, hoặc bằng chứng đó không qua bước kiểm ở AC-L3GEN-022-02.
- **When:** công cụ sinh kết quả.
- **Then:** kết luận đó không được công bố trong sơ đồ hoặc tài liệu L3.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-024](../../requirements/fr/FR-L3GEN-024.md) · revision 1 · status draft · SHA-256 `7aa296a2bdbfbfcba0d31ed5a9550405eb48d4d8a3dcb26c9021f6296f483d35`

### FR-L3GEN-024 — Công bố giới hạn của lần chạy

#### Mô tả

Mỗi lần chạy kèm phần nêu rõ những gì công cụ không đọc được. Bỏ sót có báo là chấp nhận được; bỏ sót im lặng thì không.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Kiểm chứng kết quả |
| Ưu tiên | Must Have |
| Mốc | M1 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

#### Acceptance Criteria

##### AC-L3GEN-024-01

- **Given:** Một số file trong phạm vi phân tích bị lỗi cú pháp hoặc lỗi encoding.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ vẫn xử lý phần hợp lệ, và nêu từng file lỗi kèm lý do ở phần giới hạn của kết quả.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-024-02

- **Given:** Phân tích chạm giới hạn tài nguyên, hết quota model, hoặc bị ngắt giữa chừng.
- **When:** công cụ kết thúc lần chạy.
- **Then:** công cụ trả kết quả partial kèm lý do và phạm vi đã xử lý được; không để lại bộ output trông như đã hoàn chỉnh.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-AI-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-024-03

- **Given:** Repository dùng framework, broker hoặc manifest nằm ngoài phạm vi hỗ trợ.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ nêu phần ngoài phạm vi ở mục giới hạn, không mô tả repository như thể phần đó không tồn tại.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-024-04

- **Given:** Một phạm vi chưa được xét đầy đủ vì thiếu bộ đọc, thiếu ngữ cảnh hoặc chạm giới hạn.
- **When:** công cụ sinh kết quả.
- **Then:** công cụ ghi trạng thái là giới hạn hoặc partial cho phạm vi đó, không ghi là không phát hiện thấy.
- `constrained_by:` [NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-025](../../requirements/fr/FR-L3GEN-025.md) · revision 2 · status draft · SHA-256 `2da45b8291d1f7bb02cbde4491d4a83f8198b55959f6648562d4f6902abf906a`

### FR-L3GEN-025 — Xuất kết quả

#### Mô tả

Người dùng lấy được sơ đồ component (mức L2), tài liệu L3 contract theo FR-L3GEN-027, và bộ dữ liệu có cấu trúc để công cụ khác dùng lại, cùng thông tin phiên bản và phạm vi của lần chạy.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Sử dụng kết quả |
| Ưu tiên | Must Have |
| Mốc | M1 cho bản đầu; M2 khi có component |
| Người sở hữu | Vai Product của TEAM-L3GEN |

#### Acceptance Criteria

##### AC-L3GEN-025-01

- **Given:** Một lần phân tích kết thúc với trạng thái hoàn tất hoặc partial.
- **When:** người dùng xuất kết quả.
- **Then:** công cụ tạo tài liệu L3 contract theo FR-L3GEN-027, sơ đồ component và dependency, mã nguồn sơ đồ, và bộ dữ liệu JSON.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-025-02

- **Given:** Một hệ thống khác đọc bộ dữ liệu JSON.
- **When:** hệ thống đó nạp file.
- **Then:** file có schema version, định danh của snapshot đã phân tích, và không chứa cạnh trỏ tới thực thể không tồn tại trong cùng file.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-025-03

- **Given:** Một artifact trong bộ kết quả sinh lỗi.
- **When:** công cụ xuất kết quả.
- **Then:** công cụ nêu rõ artifact nào lỗi và cho phép thử lại, giữ nguyên các artifact hợp lệ.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-025-04

- **Given:** Cùng một mô hình kiến trúc được xuất ra nhiều dạng artifact.
- **When:** người dùng đối chiếu giữa các artifact.
- **Then:** không artifact nào chứa component hoặc quan hệ mà artifact khác không có; mọi artifact giữ mức application/component.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-026](../../requirements/fr/FR-L3GEN-026.md) · revision 1 · status draft · SHA-256 `c10cedb6e6f0b2a6a1a8885a9f761b5b9d44f9d3b2cf8f5b44d298c6f1a75adb`

### FR-L3GEN-026 — Khám phá kết quả trên web

#### Mô tả

Trên web, người dùng theo dõi lần chạy hiện tại rồi xem tổng quan kiến trúc, đi sâu theo component, và mở bằng chứng của từng quan hệ.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Sử dụng kết quả |
| Ưu tiên | Must Have |
| Mốc | M2 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

#### Acceptance Criteria

##### AC-L3GEN-026-01

- **Given:** Một lần phân tích đang chạy trên web.
- **When:** người dùng mở màn hình trạng thái.
- **Then:** công cụ hiển thị giai đoạn đang chạy và trạng thái running, completed, partial hoặc failed kèm lý do lỗi.
- `constrained_by:` [NFR-L3GEN-OPS-001]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-026-02

- **Given:** Một lần phân tích đã có kết quả.
- **When:** người dùng mở kết quả.
- **Then:** công cụ hiển thị tổng quan kiến trúc, các góc nhìn component, API, dữ liệu, tích hợp và dependency, cùng phần giới hạn của lần chạy.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-026-03

- **Given:** Người dùng cần tìm một component hoặc quan hệ cụ thể trong kết quả.
- **When:** người dùng tìm và lọc.
- **Then:** công cụ trả về kết quả khớp và cho mở phần bằng chứng theo FR-L3GEN-023 từ đó.
- `constrained_by:` [NFR-L3GEN-OPS-001, NFR-L3GEN-SEC-002]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

---

Nguồn: [FR-L3GEN-027](../../requirements/fr/FR-L3GEN-027.md) · revision 2 · status draft · SHA-256 `9742b69841cded17b030d716fbe916a656cec4406a294dd1c99e16cf77cf955d`

### FR-L3GEN-027 — Sinh tài liệu L3 contract

#### Mô tả

Theo quy trình của mentor, L3 là contract: API, bảng dữ liệu (TBL) và sự kiện (EVT), chia theo component sở hữu. Sơ đồ component là mức L2. FR này sinh tài liệu L3 cho repository được phân tích.

Định dạng theo đúng cấu trúc `tech-specs/` của mentor (execution guide mục A.1 và B.10): thư mục gốc, cách chia theo component và cách đặt tên file. Mỗi contract là một file `.md`: bảng cho người đọc, cộng một khối máy đọc được bên trong.

```text
<thư mục output>/
  README.md                                  mục lục, sơ đồ component, phần giới hạn
  tech-specs/
    <CMP-slug>/                              chỉ component sở hữu ít nhất một API, TBL hoặc EVT
      api/API-<SYS>-<CMP>-v1.md              bảng endpoint + khối OpenAPI 3.1
      schema/TBL-<SYS>-<CMP>.md              bảng cột + khối DDL
      events/EVT-<SYS>-<CMP>-<topic>.md      producer, consumer + schema payload
```

Quy tắc đặt tên:

| Phần | Lấy từ | Ví dụ |
|---|---|---|
| `<SYS>` | Tên repository: viết hoa, bỏ dấu, ký tự không phải chữ hoặc số đổi thành `-` | `fastapi-shop` → `FASTAPI-SHOP` |
| `<CMP-slug>`, `<CMP>` | Tên component, cùng quy tắc; trùng thì thêm `-2`, `-3` | `Order Service` → `ORDER-SERVICE` |
| `-v1` | Luôn là `v1`: mỗi lần chạy sinh mới toàn bộ, không so với lần chạy trước | `API-FASTAPI-SHOP-ORDER-SERVICE-v1.md` |

`README.md` nằm ngoài `tech-specs/` vì mẫu của mentor không có file mục lục. Component không sở hữu contract nào thì không có thư mục.

Mỗi file có frontmatter ghi là bản sinh tự động, định danh snapshot và component sở hữu. Mỗi dòng trỏ về dữ kiện code làm bằng chứng. OpenAPI dựng từ phân tích tĩnh, không chạy code của repository. Nội dung sinh từ cùng mô hình với sơ đồ và JSON.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Sử dụng kết quả |
| Ưu tiên | Must Have |
| Mốc | M1 cho API và TBL; M3 cho EVT |
| Người sở hữu | Vai Product của TEAM-L3GEN |

#### Acceptance Criteria

##### AC-L3GEN-027-01

- **Given:** Lần chạy đã trích được route và request/response model theo FR-L3GEN-021.
- **When:** công cụ sinh tài liệu L3.
- **Then:** mỗi component có route sinh một file API gồm bảng endpoint (method, path đầy đủ, handler, request model, response model, status code, dependency hoặc auth nếu xác định được) và một khối OpenAPI 3.1 cùng nội dung. Trường không xác định được ghi `unknown` kèm lý do; mỗi dòng trỏ về dữ kiện code làm bằng chứng.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-027-02

- **Given:** Lần chạy đã trích được lớp dữ liệu ánh xạ tới bảng theo FR-L3GEN-021.
- **When:** công cụ sinh tài liệu L3.
- **Then:** mỗi component sở hữu bảng sinh một file TBL gồm bảng cột (tên, kiểu, khóa chính, khóa ngoại, nullable) và một khối DDL cùng nội dung. Tên bảng hoặc kiểu không xác định được ghi `unknown` kèm lý do, không suy từ tên lớp; mỗi dòng trỏ về dữ kiện code làm bằng chứng.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

##### AC-L3GEN-027-03

- **Given:** Lần chạy đã trích được quan hệ phát hoặc nhận sự kiện theo FR-L3GEN-021.
- **When:** công cụ sinh tài liệu L3.
- **Then:** mỗi topic sinh một file EVT gồm topic, component phát, component nhận và schema payload nếu biết. Không nối producer với consumer chỉ vì cùng tên topic khi broker hoặc cấu hình chưa xác định; phần đó ghi `unknown` kèm lý do.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

#### Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## 4. Thay đổi hành vi hiện có

Không có FR nào bump revision: mọi FR trong baseline này mang key mới. FR của `CHG-L3GEN-2026-001` đã deprecated; ánh xạ cũ sang mới ở PRD mục IV.3. PRD không lấy hành vi code hiện tại làm chuẩn.

## 5. NGOÀI phạm vi lần này

**Phạm vi phân tích.** Ngôn ngữ và framework ngoài Python/FastAPI, kể cả Java/Spring Boot — thuộc roadmap phase sau, không báo pass ở nghiệm thu phase đầu. Message broker ngoài Kafka. Thực thi source để khám phá runtime, dynamic import và metaprogramming tổng quát. Suy luận deployment topology khi source và config không đủ bằng chứng.

**Mức trình bày.** Sơ đồ vẽ toàn bộ function hoặc class của repository, và call graph đầy đủ ở mức function như một đầu ra cho người đọc. Repository Knowledge Graph nói chung gồm graph query API, graph traversal và incremental graph — đây là phạm vi của đề bài mục 3.8, muốn đưa vào cần đề xuất và AC riêng.

**Lịch sử và tích hợp.** Danh sách nhiều lần chạy, mở lại kết quả cũ, retention theo repository, xóa từng phiên, và public API để hệ thống khác theo dõi trạng thái. Toàn bộ nhóm này thuộc phase sau.

**Ghi ngược và phân tích thay đổi.** Sửa code hoặc tài liệu nguồn tự động, tạo pull request, ghi ngược vào repository đầu vào. Rà code không dùng, kết luận lỗ hổng bảo mật hoặc lỗi nghiệp vụ. Change impact, test impact, architecture drift và incremental analysis. Chỉnh mô hình thủ công trên giao diện.

**Truy cập và vận hành.** GitHub private repository và mọi cơ chế nhận hoặc lưu credential. Git submodules, đăng nhập và multi-tenant public hosting. Quản trị tài khoản và phân quyền tổ chức. Khám phá kiến trúc tương tác trên dòng lệnh — đây là phạm vi của kênh web. SLA production cấp doanh nghiệp.

**Mô hình ngôn ngữ.** Model chạy cục bộ, và mọi phương án dùng model có tính phí. Phase đầu chỉ dùng API với quota miễn phí.

Các mục trên muốn đưa vào phạm vi đều cần đề xuất phạm vi và AC riêng.

Không có FR chuẩn tắc nào bị giấu khỏi candidate.

## 6. Ràng buộc mới

---

Nguồn: [NFR-L3GEN-ABST-002](../../requirements/nfr/NFR-L3GEN-ABST-002.md) · revision 2 · status draft · SHA-256 `3688067a84de64602791c1e581f1d7c19612538685093a622531675ea8bc1292`

### NFR-L3GEN-ABST-002 — Mức trừu tượng của kết quả trình bày

- **Nhóm:** Abstraction level.
- **Trạng thái:** thay cho NFR-L3GEN-ABST-001 của BL-r14, giữ nguyên phạm vi và ngưỡng. Ngưỡng 500/50 đã chốt tại OQ-L3GEN-004 (CHG-L3GEN-2026-001); chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-022](../../requirements/fr/FR-L3GEN-022.md), [FR-L3GEN-023](../../requirements/fr/FR-L3GEN-023.md), [FR-L3GEN-025](../../requirements/fr/FR-L3GEN-025.md), [FR-L3GEN-026](../../requirements/fr/FR-L3GEN-026.md), [FR-L3GEN-027](../../requirements/fr/FR-L3GEN-027.md).
- **Quyết định nền:** [ADR-2026-001](../../architecture/adr/ADR-2026-001.md).

#### Yêu cầu có thể kiểm chứng

Phân tích và trình bày là hai mức khác nhau. Công cụ được đọc sâu tới function, tham số và phép gán để chứng minh một quan hệ, nhưng kết quả mặc định cho người đọc dừng ở application/component.

- Sơ đồ mặc định (mức L2) chỉ có node mức application, component và hệ thống ngoài. Node mức function, class hoặc file không xuất hiện ở lớp mặc định.
- Tài liệu L3 liệt kê contract: endpoint, bảng, sự kiện, chia theo component. Function và class chỉ xuất hiện khi là handler hoặc model được nêu trong contract, hoặc ở lớp bằng chứng.
- Số node của sơ đồ mặc định không tỷ lệ với số function của repository. Repository có từ 500 function trở lên vẫn cho sơ đồ mặc định không quá 50 node. Phần vượt trần không bị loại khỏi bộ kết quả mà nằm ở lớp bằng chứng; không xuất sơ đồ đầy đủ rồi để người đọc tự lọc.
- Dữ kiện mức function và class vẫn nằm trong bộ kết quả, nhưng ở lớp bằng chứng có nhãn riêng, không trộn vào lớp kiến trúc mặc định.
- Một quan hệ kiến trúc chỉ tồn tại khi đích đã xác định. Lời gọi chưa xác định được đích giữ ở lớp dữ kiện với nhãn unresolved, không nâng thành cạnh giữa hai component.

#### Điều kiện và cách kiểm

Chạy trên bộ dữ liệu đã pin, đếm node theo lớp trong bộ kết quả máy đọc được của FR-L3GEN-025, không đếm bằng mắt trên hình. Kiểm cả repository nhỏ và repository từ 500 function trở lên. Kiểm rằng bỏ lớp bằng chứng đi thì lớp kiến trúc vẫn đọc được, và mọi cạnh kiến trúc đều có đích đã xác định. Sơ đồ vẽ được không phải bằng chứng mức trừu tượng đúng.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)

---

Nguồn: [NFR-L3GEN-ACC-002](../../requirements/nfr/NFR-L3GEN-ACC-002.md) · revision 2 · status draft · SHA-256 `006f6eea321fc7cf8b9a6fcddfdbd7cbe43ed19de941f32f3bd3966ec770a8ef`

### NFR-L3GEN-ACC-002 — Độ đúng của kết quả và bằng chứng

- **Nhóm:** Accuracy.
- **Trạng thái:** ngưỡng đã chốt tại OQ-L3GEN-007 ngày 22/09/2026. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-020](../../requirements/fr/FR-L3GEN-020.md), [FR-L3GEN-021](../../requirements/fr/FR-L3GEN-021.md), [FR-L3GEN-022](../../requirements/fr/FR-L3GEN-022.md), [FR-L3GEN-023](../../requirements/fr/FR-L3GEN-023.md), [FR-L3GEN-024](../../requirements/fr/FR-L3GEN-024.md), [FR-L3GEN-027](../../requirements/fr/FR-L3GEN-027.md).

#### Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-ACC-001 và NFR-L3GEN-TRACE-001 của BL-r14.

**Độ đúng của dữ kiện và component.** Precision và recall đều phải đạt từ 80% trở lên, đo riêng cho từng loại: route, request/response model, entity/table, lời gọi HTTP, config, event, thư viện, thành viên component và cạnh dependency. Ngưỡng 80% chốt tại OQ-L3GEN-007, thay cho ngưỡng 90% của revision 23 vốn đặt cho bộ luật tất định; bộ trích xuất dùng mô hình ngôn ngữ không có cùng đặc tính sai số nên không dùng lại con số đó.

Chấm thuộc tính riêng với chấm sự tồn tại: một route thiếu prefix không tính là route đúng, một tên bảng suy sai không tính là tên bảng đúng. Nhóm nào chưa đủ mẫu thì báo TP/FP/FN, không báo đạt.

**Bằng chứng.** Bằng chứng của một kết luận là các dữ kiện code trong tập dữ kiện của lần chạy, mỗi dữ kiện nằm ở file có thật trong snapshot đã phân tích. Với cạnh dependency A→B do code dựng, phải có ít nhất một dữ kiện đã xác định đích, vị trí thuộc A và đích thuộc B. Với cạnh do model đề xuất thêm, phải có dữ kiện ở cả hai đầu theo AC-L3GEN-022-02. Code kiểm điều này; lời khẳng định của model không được tính là bằng chứng. Tỷ lệ kết luận công bố có bằng chứng hợp lệ phải đạt 100%, không có ngoại lệ: kết luận không thỏa thì bị loại trước khi xuất, không được hạ thành cảnh báo. Bằng chứng không được trỏ sang snapshot khác hoặc sang source hiện tại trên đĩa.

**Nhãn chất lượng.** Confidence, completeness và coverage là ba trục độc lập, không dùng trục này thay trục kia. Nhãn `exact` chỉ dùng cho kết luận đọc trực tiếp từ bằng chứng; kết luận suy ra mang nhãn `inferred` kèm lý do. Không được nâng `inferred` thành `exact` để kết quả trông chắc chắn hơn. Tỷ lệ nhãn khớp đánh giá người duyệt phải đạt từ 80% trở lên. Riêng tỷ lệ gán `exact` cho kết luận thật ra sai phải ở mức 5% trở xuống, và là chỉ số chặn: gán nhãn chắc chắn cho kết luận sai gây hại hơn bỏ sót, vì người đọc tin mà không kiểm lại.

#### Điều kiện và cách kiểm

OBS-L3GEN-001 quy định dataset, người lập đáp án độc lập, cách matching và cỡ mẫu tối thiểu. Nhóm nào chưa đủ mẫu thì báo counts và `not_evaluated`, không báo phần trăm.

Phần bằng chứng kiểm tự động trên mọi lần chạy: đối chiếu từng dữ kiện được trích dẫn với tập dữ kiện, từng đường dẫn với danh sách file của snapshot, và hai đầu của mỗi cạnh với vị trí và đích của dữ kiện. Máy kiểm được bằng chứng có tồn tại và nối đúng; việc dữ kiện có thật sự đủ ý nghĩa cho kết luận thì chấm bằng đáp án của người. Phần nhãn và độ đúng kiểm bằng đáp án do người lập trước khi xem output. Không loại ca khó ra khỏi mẫu sau khi đã xem kết quả.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)

---

Nguồn: [NFR-L3GEN-AI-002](../../requirements/nfr/NFR-L3GEN-AI-002.md) · revision 3 · status draft · SHA-256 `a142ee726a8d39bcff28f3a4925c00c0df826294c24eae8b218b2664649782fa`

### NFR-L3GEN-AI-002 — Ranh giới, chi phí và truy vết của mô hình ngôn ngữ

- **Nhóm:** AI reliability.
- **Trạng thái:** hướng đã chốt ngày 22/09/2026; provider, model và trần mỗi lần chạy chốt tại OQ-L3GEN-008 ngày 23/09/2026. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-021](../../requirements/fr/FR-L3GEN-021.md), [FR-L3GEN-022](../../requirements/fr/FR-L3GEN-022.md), [FR-L3GEN-024](../../requirements/fr/FR-L3GEN-024.md).

#### Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-AI-001 và NFR-L3GEN-DET-001 của BL-r14; tái lập hạ xuống mức ghi nhận.

**Ranh giới.** Mô hình ngôn ngữ chỉ nhận tập dữ kiện code đã trích kèm vị trí file, không nhận toàn bộ source repository. Model đặt tên, mô tả, vai trò cho component đã được code chia, gắn nhãn cạnh, và đề xuất cạnh mà phân tích tĩnh không thấy. Chỉ với repository phẳng, model mới đề xuất cách chia component (AC-L3GEN-022-05). Model không sửa dữ kiện code và không tự công bố kết luận.

**Đọc thêm code.** Đầu vào mặc định là tập dữ kiện, danh sách file của từng component, lời gọi giữa component, và chữ ký hàm (tên, tham số, kiểu, decorator, docstring). Khi cần xem thân hàm, model gọi công cụ đọc code của engine; công cụ chỉ trả đoạn code thuộc snapshot và phạm vi đang xét, đã che bí mật. Model phải hỗ trợ gọi công cụ; với `gpt-oss-120b` trên Groq điều này **chưa kiểm**, kiểm ở M1. Kết quả model trả về phải đúng schema đã định; phần sai schema, trỏ tới file không có trong snapshot, tham chiếu định danh không tồn tại, hoặc không qua bước kiểm bằng chứng của NFR-L3GEN-ACC-002 thì bị loại và ghi lý do loại.

**Provider và model phase đầu.** Hai model, chia theo việc, đều dùng gói miễn phí:

| Việc | Model | Số request mỗi lần chạy |
|---|---|---|
| Đọc code qua công cụ, đặt tên, mô tả, vai trò component, gắn nhãn cạnh | Groq `openai/gpt-oss-120b`, `reasoning_effort` trung bình | Nhiều, trong trần token bên dưới |
| Đề xuất cạnh bổ sung cho cả repository, gộp trong một request, không đọc thêm code | Google `gemini-3.5-flash` | 1 |
| Chia component khi repository phẳng (AC-L3GEN-022-05) | Google `gemini-3.5-flash` | 1, chỉ khi repository phẳng |

Giới hạn gói do Khiêm cung cấp ngày 23/09/2026. Groq `gpt-oss-120b`: 30 request/phút, 1.000 request/ngày, 8.000 token/phút, 200.000 token/ngày. Google `gemini-3.5-flash`: 5 request/phút, 250.000 token/phút, 20 request/ngày. Giới hạn do provider đặt và có thể đổi; công cụ đọc lỗi rate limit thực tế thay vì tin con số ghi ở đây.

Mỗi việc luôn do đúng model đã ghi ở bảng. Model của một việc lỗi hoặc hết quota thì việc đó dừng và báo, không chuyển sang model kia. Provenance ghi model của từng phần kết quả.

**Trần mỗi lần chạy.**

| Trần | Giá trị | Lý do |
|---|---|---|
| Token mỗi lần chạy với `gpt-oss-120b`, vào và ra cộng lại | ≤ 100.000 | Một nửa quota ngày, chừa chỗ cho một lần chạy lại |
| Request mỗi lần chạy với `gemini-3.5-flash` | ≤ 2 | Quota 20 request/ngày; cho khoảng 10 lần chạy mỗi ngày |
| Token mỗi request với `gemini-3.5-flash` | ≤ 50.000 | Dưới trần 250.000 token/phút; chưa đo trên repo thật |
| Token mỗi request | ≤ 6.000 | Dưới trần 8.000 token/phút của gói |
| Request mỗi lần chạy | ≤ 40 | Chặn vòng gọi không dừng |
| Timeout và thử lại | 30 giây mỗi request, thử lại tối đa 2 lần | Giữ từ BL-r14 |
| Lần đọc code theo yêu cầu model | ≤ 6 lần mỗi phạm vi, mỗi lần ≤ 60 dòng | 6 lần theo CodeBoarding; 60 dòng để vừa trần token mỗi request |

Công cụ ước tính số token của tập dữ kiện trước request đầu tiên; vượt trần thì không gọi model và xử lý theo AC-L3GEN-022-03. Trần token thay cho "trần kích thước repository": model nhận tập dữ kiện chứ không nhận source, nên đơn vị đo là token. Quy đổi sang số file hoặc số dòng code chưa đo; M1 đo và công bố.

**Chi phí.** Chỉ dùng model qua API. Phase đầu giới hạn ở quota miễn phí với trần chi phí trả phí bằng 0 đồng. Hết quota, bị rate limit, thiếu key hoặc chạm trần thì dừng bước dựng quan hệ kiến trúc và báo rõ, không tự chuyển sang phương án tính tiền, không tự đổi sang model khác, và không đoán để lấp chỗ trống.

**Bí mật.** Khóa API do người dùng cung cấp lúc chạy, không được ghi vào output, log, bằng chứng hay bộ kết quả lưu lại. Công cụ không phát biểu thay người dùng về mức an toàn dữ liệu của provider họ chọn.

**Tái lập.** Kết quả không bắt buộc giống hệt giữa các lần chạy. Bù lại, mỗi lần chạy phải ghi lại provider, tên model, phiên bản prompt, phiên bản tool và định danh snapshot, đủ để dựng lại bối cảnh của một kết quả cũ. Đây là yêu cầu ghi nhận, không phải ngưỡng chặn phát hành.

#### Điều kiện và cách kiểm

Dùng provider giả trả về JSON hỏng, định danh lạ, đường dẫn không tồn tại, timeout và lỗi rate limit; kiểm rằng phần không hợp lệ bị loại và lý do được ghi. Đặt khóa API dạng đánh dấu rồi kiểm toàn bộ output, log và bằng chứng không chứa giá trị đó. Kiểm đổi provider bằng cấu hình mà không sửa code. Kiểm mỗi bộ kết quả có đủ trường truy vết đã nêu. Không dùng giá hoặc model giả định để kết luận về chi phí.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)

---

Nguồn: [NFR-L3GEN-OPS-001](../../requirements/nfr/NFR-L3GEN-OPS-001.md) · revision 1 · status draft · SHA-256 `eac4c3dfbed44efad794b67ba0ed21b14ba74b00955260cf1610671cd424e187`

### NFR-L3GEN-OPS-001 — Hiệu năng, độ tin cậy và phạm vi hỗ trợ

- **Nhóm:** Operability.
- **Trạng thái:** ngưỡng đã chốt; trần token của model ở NFR-L3GEN-AI-002 theo OQ-L3GEN-008. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-019](../../requirements/fr/FR-L3GEN-019.md), [FR-L3GEN-020](../../requirements/fr/FR-L3GEN-020.md), [FR-L3GEN-024](../../requirements/fr/FR-L3GEN-024.md), [FR-L3GEN-025](../../requirements/fr/FR-L3GEN-025.md), [FR-L3GEN-026](../../requirements/fr/FR-L3GEN-026.md).

#### Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-PERF-001, REL-001, COMP-001 và phần còn dùng được của USA-001 của BL-r14. Key OPS-001 chưa từng dùng trước đây.

**Thời gian và tài nguyên.** Mỗi lần chạy ghi lại riêng thời gian lấy source, phân tích tĩnh, gọi model và sinh artifact, cùng bộ nhớ đỉnh và kích thước output.

| Ngưỡng | Giá trị | Nguồn |
|---|---|---|
| Phân tích tĩnh và ghi output, không gồm lấy source và gọi model | ≤ 60 giây cho 5.000 dòng Python; ≤ 300 giây cho 50.000 dòng | Giữ từ BL-r14 |
| Máy đo chuẩn | 4 CPU logical, RAM 8 GiB, SSD, Python 3.12; máy khác thì công bố, không ngoại suy | Giữ từ BL-r14 |
| Bộ nhớ | ≤ 2 GiB mỗi lần chạy | Giữ từ BL-r14 |
| Toàn bộ một lần chạy | ≤ 30 phút; quá hạn thì dừng, trả partial kèm lý do | Mới. 100.000 token ở 8.000 token/phút cần ít nhất 12,5 phút; trần 10 phút của BL-r14 không còn đủ |
| Số lần chạy cùng lúc | 1; lần sau xếp hàng | Mới, vì các lần chạy dùng chung một quota model |

Trần tiếp nhận ở NFR-L3GEN-SEC-002; trần token ở NFR-L3GEN-AI-002. Vượt trần thì từ chối trước bước tương ứng, kèm lý do, không chạy dở rồi hỏng.

**Lỗi một phần.** Một đơn vị phân tích hỏng không làm hỏng cả lần chạy. Kết quả partial phải nêu rõ phạm vi đã xử lý được. Trạng thái của lần chạy là completed, partial hoặc failed, và phải phản ánh đúng thực tế: không có bộ output trông như hoàn chỉnh khi thực ra thiếu artifact.

**Phạm vi hỗ trợ.** Có một ma trận khai báo, cho mỗi ngôn ngữ và framework, độ sâu phân tích áp dụng và mức chất lượng đi kèm. Ma trận này là nguồn duy nhất để trả lời câu hỏi công cụ hỗ trợ gì; phase đầu chỉ Python/FastAPI có mức hỗ trợ đầy đủ.

**Thông báo cho người dùng.** Mọi lỗi từ chối đầu vào nêu được nguyên nhân và cách sửa, không chỉ báo thất bại chung chung.

#### Điều kiện và cách kiểm

Đo trên bộ dữ liệu đã pin, ghi đủ các trường ở trên cho mỗi lần chạy. Dựng ca lỗi một phần bằng cách cố ý làm hỏng một đơn vị phân tích và kiểm trạng thái trả về. Kiểm ma trận hỗ trợ khớp với hành vi thật: mỗi ô trong ma trận có ít nhất một ca kiểm. Đọc lại toàn bộ thông báo lỗi của ba hình thức đầu vào trước nghiệm thu.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)

---

Nguồn: [NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md) · revision 3 · status draft · SHA-256 `39cad9c4bd1ba58d339560c865cb3296a615d442f94d2176855515665dfcba8f`

### NFR-L3GEN-SEC-002 — An toàn khi tiếp nhận source và vòng đời dữ liệu

- **Nhóm:** Security và Privacy.
- **Trạng thái:** phạm vi đã chốt; chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-019](../../requirements/fr/FR-L3GEN-019.md), [FR-L3GEN-021](../../requirements/fr/FR-L3GEN-021.md), [FR-L3GEN-025](../../requirements/fr/FR-L3GEN-025.md), [FR-L3GEN-026](../../requirements/fr/FR-L3GEN-026.md).
- **Threat model:** [TM-SYS-L3GEN](../../architecture/threat-model/TM-SYS-L3GEN.md).

#### Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-SEC-001 và NFR-L3GEN-PRIV-001 của BL-r14.

**Read-only với source.** Không chạy, không import, không `exec` hay `eval`, không cài dependency, không chạy hook hoặc submodule, và không ghi ngược vào cây source đầu vào.

**Tiếp nhận an toàn.** File nén giải ra phải nằm trong vùng xử lý; đường dẫn thoát khỏi vùng đó bị từ chối. Trần một lần tiếp nhận, giữ từ BL-r14: ZIP nén 100 MB, giải nén 500 MB, 50.000 file. Lấy source từ GitHub timeout 120 giây. Vượt trần thì từ chối kèm lý do. Chỉ nhận repository GitHub public qua HTTPS; công cụ không nhận và không lưu credential truy cập repository.

**Dữ liệu gửi ra ngoài.** Trước khi chạy, người dùng được cho biết dữ liệu nào sẽ được gửi tới provider model. Dữ liệu gửi đi gồm: tập dữ kiện đã trích (tên symbol, đường dẫn file, vị trí, giá trị literal như path của route), chữ ký hàm kèm docstring, và các đoạn code model yêu cầu qua công cụ đọc code trong giới hạn của NFR-L3GEN-AI-002. Không gửi nguyên file source hoặc cả repository. Dữ liệu đi tới hai provider: Groq và Google, theo phân việc ở NFR-L3GEN-AI-002; màn hình và dòng lệnh báo rõ cả hai. Điều khoản dùng dữ liệu của gói miễn phí là của provider; công cụ nêu tên provider, không phát biểu thay họ. Giá trị cấu hình mang dấu hiệu bí mật bị che trước khi vào bất kỳ đầu ra nào, kể cả payload gửi model.

**Vòng đời.** Phase đầu chỉ giữ dữ liệu cần cho lần chạy hiện tại. Trên web, source đã tiếp nhận và output hết hạn 24 giờ sau trạng thái cuối của lần chạy, và không được phục vụ sau hạn. Mốc 24 giờ cho source giữ từ BL-r14; áp cho output là mới, vì lịch sử 14 ngày của BL-r14 thuộc phase sau. Nếu máy tắt qua hạn, lần khởi động kế tiếp phải dọn trước khi phục vụ dữ liệu. Output của dòng lệnh do người dùng quản lý.

#### Điều kiện và cách kiểm

Chạy trên bộ dữ liệu chứa file nén độc hại, đường dẫn thoát vùng giải nén, symlink trỏ ra ngoài, repository vượt trần kích thước, và file cấu hình chứa giá trị bí mật. Kiểm cây source trước và sau khi chạy phải giống nhau về nội dung. Kiểm payload gửi model không chứa giá trị bí mật. Kiểm dữ liệu tạm đã được dọn sau vòng đời đã công bố.

#### Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

#### Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)

## 7. Câu hỏi mở còn lại

Không còn câu hỏi mở.
