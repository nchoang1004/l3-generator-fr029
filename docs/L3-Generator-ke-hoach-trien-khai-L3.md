# Kế hoạch thiết kế L3 — L3 Generator

Ngày lập: 25/09/2026. Cập nhật: 01/10/2026. Trạng thái: **tài liệu L3 (không gồm UI cấp 4) đã xong ở mức draft do người soạn tự review ngày 01/10/2026**; chưa có review chéo, chưa qua gate.

**Triển khai code còn lại:** xem [kế hoạch code phần còn lại của L3](L3-Generator-ke-hoach-code-L3.md). Các ước lượng trong file này chỉ dành cho công việc thiết kế.

**Cơ sở hiện tại:** nhánh `docs/l3-align-gate2`, tạo từ `origin/docs/gate-2` commit `5d06f14` (nguồn trên git: PRD r28, FR-027 r3, ADR-003 r2, CMP r2). Bản 25/09 nằm ở nhánh `docs/l3-contracts-review` commit `714f26e`; bản đó tự sửa nguồn (PRD r29…) chưa được duyệt, nên nhánh này **không** mang các sửa nguồn đó, chỉ mang 8 contract rồi sửa cho khớp git. Hai BL-r5 vẫn chờ xử lý ở [chặng 0](#4-chặng-0-và-0b--đồng-bộ-nguồn-và-dữ-liệu-đầu-vào). Kế hoạch không thay thế tài liệu nguồn hay phê duyệt; thuật toán component D-03 vẫn để mở theo yêu cầu.

**Cập nhật thực hiện 25/09/2026:** đã hoàn thiện nội dung [bộ tám contract L3 draft và hướng dẫn review](../.aide/tech-specs/README.md), với schema, OpenAPI, kiểu lỗi, quy tắc retry, consumer UI và [ví dụ xuyên luồng](../.aide/tech-specs/examples/contract-walkthrough.md). **D-03 — thuật toán chia component vẫn OPEN theo yêu cầu người phụ trách; chưa chọn phương án.** Binding, projection, identity, budget, lifecycle và xuất contract đã đồng bộ vào bản nguồn draft. Các quy ước interface còn cần reviewer xác nhận; chưa có phê duyệt mới. Việc viết xong tài liệu không phải approval hoặc bằng chứng sản phẩm đã triển khai.

**Cập nhật 01/10/2026:** thêm chặng 0 và 0b, phân công lại, ghi quyết định EVT đã chốt. Kết quả đối chiếu ở [L3-Generator-doi-chieu-nguon-L3.md](L3-Generator-doi-chieu-nguon-L3.md).

**Cập nhật 01/10/2026, lần 2:** 8 contract lên revision 4, khớp nguồn trên git (bỏ projection ẩn node, bỏ giới hạn hàng đợi, CMP-005 gán owner, một khối OpenAPI mỗi file, bỏ `default` ở TBL, thêm bảng biểu diễn phần thiếu và bước kiểm bản xuất). Code lát cắt đầu ở [slice/](../slice/README.md): route, bảng và event (dữ kiện event soạn tay) đi tới API/TBL/EVT, 27 test pass. Các điểm chờ đã chốt khi tự review; chưa có review chéo.

## 1. Nhiệm vụ và sản phẩm bàn giao

Nhiệm vụ của người viết L3 là chuyển yêu cầu và thiết kế L2 thành các contract đủ cụ thể để người triển khai không phải tự đoán: đầu vào, đầu ra, quy tắc, lỗi, phiên bản và ví dụ. Kế hoạch này chỉ tổ chức công việc; hoàn thành kế hoạch chưa có nghĩa đã hoàn thành L3.

Phân biệt hai phần:

| Phần | Nhóm phải làm gì? |
|---|---|
| L3 của chính L3 Generator | Thiết kế API web, giao diện nội bộ, cấu trúc dữ kiện/model/evidence và quy tắc xuất kết quả |
| Tài liệu L3 do sản phẩm sinh ra | Thiết kế cách CMP-008 chuyển dữ kiện của repo đầu vào thành API/TBL/EVT theo FR-027 |

Đích bàn giao: bộ spec có thể review trong Git, ví dụ kiểm được, mapping tới FR/AC và danh sách task triển khai. Không mặc định phải tạo database, Kafka hoặc tám HTTP service. L3 ở đây là cấp contract trong quy trình mentor, không suy từ cách đánh số C4.

## 2. Tài liệu đầu vào cần đọc

1. [PRD](../.aide/product/prd/PRD-L3GEN-2609-001.md): phạm vi, luồng và giới hạn phase đầu.
2. [L2](../.aide/architecture/l2/): trách nhiệm, sequence, transaction boundary, idempotency và concurrency của CMP-001 đến CMP-008.
3. [FR và AC](../.aide/requirements/fr/), [NFR](../.aide/requirements/nfr/): hành vi và điều kiện phải đạt.
4. [FR-027 (đã thay thế)](../.aide/requirements/_superseded-r28/fr/FR-L3GEN-027.md): yêu cầu lịch sử về định dạng API/TBL/EVT; yêu cầu hiện tại tách thành FR-029/030/031.
5. [Execution Guide](agentic-sdlc-execution-guide.md): A.1, B.10, B.11 và phần UI cấp 4.
6. [OBS-001](../.aide/observability/OBS-L3GEN-001.md): cách đo; ví dụ contract không thay gold độc lập.
7. Nhánh `feature/quote-evidence`: ADR-003 r2, FR-027 r3 bản Khiêm, `.aide/evidence/requests/CR-L3GEN-2026-003-decisions-01.yaml`. Chưa có trên nhánh này nên không đặt link.

[Architecture View](../.aide/generated/architecture-views/AVW-CHG-L3GEN-2026-002.md) ghi nhận phần sinh contract chưa thiết kế chi tiết. Tại mốc nguồn trên chưa có `.aide/tech-specs/`. Không coi tài liệu tham khảo hoặc kế hoạch cũ là contract hiện hành.

## 3. Phân công

Hoàng phụ trách toàn bộ tài liệu L3. Khiêm phụ trách pipeline và review kiến trúc.

| Loại việc | Ai quyết |
|---|---|
| Soạn draft L3, bảng đối chiếu, schema đề xuất, ví dụ, danh sách lỗi, quy tắc xuất | Hoàng tự làm |
| Sửa PRD/FR/NFR/L2 hoặc đổi kiến trúc | Hoàng đề xuất; hai người thống nhất trước khi chốt |
| Dữ liệu bàn giao mà pipeline phải cung cấp cho L3 | Hoàng đề xuất; hai người thống nhất trước khi chốt |

Trong lúc chờ thống nhất, vẫn viết và kiểm bằng dữ liệu mẫu; ghi rõ phần nào là đề xuất. Không đổi kiến trúc chỉ trong L3. Người viết không tự đánh dấu người kia đã review. Nếu một người đổi contract mà bên sử dụng chưa biết, task phụ thuộc chưa được coi là sẵn sàng.

## 4. Chặng 0 và 0b — Đồng bộ nguồn và dữ liệu đầu vào

Chặng này làm trước chặng A. Lý do: hai nhánh đang có hai bộ nguồn khác nhau, nên chưa kiểm được L3 khớp với bản nào.

| | Nhánh L3 draft | Nhánh của Khiêm |
|---|---|---|
| Nhánh, commit | `docs/l3-contracts-review`, `714f26e` | `feature/quote-evidence`, `a14d32c` (nguồn đổi ở `5d06f14`) |
| PRD | r29 | r28 |
| Quyết định riêng | Đồng bộ draft ngày 25/09 | ADR-003 r2; CR-L3GEN-2026-003-decisions-01 (23/09) |

Kết quả đối chiếu: [L3-Generator-doi-chieu-nguon-L3.md](L3-Generator-doi-chieu-nguon-L3.md).

**Chặng 0 — đồng bộ nguồn.**

- Không chọn nguyên một nhánh. Gộp theo từng file: đối chiếu yêu cầu mới của Khiêm với L3 draft cũ.
- Ghi rõ commit và revision làm cơ sở cho từng contract.
- Hai BL-r5 khác nội dung: giữ cả hai làm lịch sử. Sau khi thống nhất nguồn, tạo candidate mới với mã chưa dùng, cập nhật liên kết, kiểm sha256. Không chỉ đổi tên file.

**Chặng 0b — dữ liệu đầu vào.** Đây là việc quan trọng nhất của chặng 0.

- So đầu vào CMP-008 đã thiết kế (`VerifiedResult`) với `graph.json` của pipeline v8. Chia ba loại: trường có sẵn, chuyển đổi được, còn thiếu.
- Không ép L3 dùng nguyên `graph.json`. File này chưa có dữ kiện API/TBL/EVT.
- Ghi rõ mức kiểm: `verify.py` chỉ kiểm câu trích đúng nguyên văn; L3 cần bằng chứng cho giá trị từng trường.

**Bảng "L2 thiếu/mâu thuẫn"** nằm ở mục 6 của file đối chiếu. Mỗi dòng có cột ảnh hưởng tới L3: chặn hay để mở được. Chỉ dòng "chặn" mới phải chờ.

Điều kiện hoàn thành: Khiêm đồng ý các dòng "chặn" và dữ liệu bàn giao; đã có candidate mới thay hai BL-r5.

## 5. Chặng A — Chốt điểm mâu thuẫn trước khi đóng contract

Không phải chờ tất cả mới bắt đầu soạn. Có thể viết phần độc lập, nhưng phần phụ thuộc quyết định dưới đây chưa được đóng băng hoặc giao code như đã chốt.

Vấn đề ở nguồn tìm thấy ở chặng 0 ghi vào bảng L2 của file đối chiếu, không lặp lại ở đây.

| Quyết định | Nguồn hiện tại | Cần làm rõ | Chặn phần nào? |
|---|---|---|---|
| Bằng chứng của cạnh model đề xuất | FR-022 AC-02; NFR-ACC-002; CMP-005/007 | Có dữ kiện hai đầu chưa đủ; quy tắc nào chứng minh loại, chiều và đích liên kết? Không kiểm được thì giữ ở đâu? | Model proposal, evidence gate |
| Nhất quán giữa các output | FR-025 AC-04; CMP-008; NFR-ABST-002 | Đã chốt theo git (01/10): mọi artifact cùng tập component/cạnh (FR-025 r2 AC-04, CMP-008 r2); trần 50 node do CMP-005 giữ | Renderer, JSON, bộ kiểm export |
| Chia component và tái lập — D-03 OPEN | PRD phần tóm tắt; FR-022; CMP-005 | Giữ schema membership/ID/version; thử các thuật toán trước khi chọn. Không mặc định directory-v1 hoặc mở thêm quyền LLM | Thuật toán production và policy root/flat; không chặn kiểm consumer bằng membership fixture |
| ID dữ kiện | CMP-004 | Phân biệt hai dữ kiện cùng loại trên cùng dòng; không chỉ file + dòng + loại | Fact schema, evidence |
| Ngân sách LLM | NFR-AI-002; CMP-006 | Trần theo provider hay toàn run; retry/tool/pha JSON tính thế nào; token vào/ra; rate limit qua nhiều run | Gateway contract |
| Hàng đợi và trạng thái | CMP-001; NFR-OPS-001 | Đã chốt theo git (01/10): FIFO, không giới hạn số run chờ (NFR-OPS-001 r1); `queued` và hạn 30 phút tính từ lúc bắt đầu là chi tiết L3. Muốn giới hạn số run chờ thì phải sửa nguồn trước | Run API, UI |
| Partial và output lỗi | CMP-001/007/008 | Khi không còn kết quả dùng được thì failed hay partial; trạng thái phân tích và trạng thái từng artifact | RunResult, export |
| Gửi đoạn source | NFR-SEC-002; NFR-AI-002 | File ngắn hoặc nhiều lần đọc bao phủ cả file có vi phạm “không gửi nguyên file” không? “Phạm vi” của quota đọc là gì? | Tool đọc code |

Sản phẩm bàn giao của chặng A: bảng quyết định ghi phương án, lý do, phần bị ảnh hưởng, người review và trạng thái. Ghi ngay trong spec liên quan hoặc nhật ký quyết định hiện có; không tạo thêm tài liệu trùng vai. Thay đổi yêu cầu phải cập nhật nguồn và candidate theo quy trình, không chỉ sửa L3 để bỏ qua mâu thuẫn.

## 6. Chặng B — Contract dữ liệu cốt lõi

Phần này đã được soạn trong API-002/003/004/005/007. Tên cấu trúc bên dưới là schema của draft, chưa phải phiên bản đã duyệt.

| Contract | Owner → consumer | Nội dung tối thiểu |
|---|---|---|
| Snapshot / SourceLocation | CMP-002 → CMP-003/004/006/007 | Snapshot identity, danh sách file, digest, đường dẫn tương đối, encoding, quy ước dòng/cột, lỗi đọc, phạm vi đọc được phép |
| Inventory | CMP-003 → CMP-001/004/005 | Đơn vị phân tích, phạm vi file, mức hỗ trợ, phần bỏ qua/lý do, căn cứ xác định repo phẳng |
| FactSet | CMP-004 → CMP-005/007/008 | ID, loại dữ kiện, chủ thể/đích, thuộc tính, vị trí, resolved/unresolved và giới hạn; route, request/response, table, HTTP, config, event, library |
| ArchitectureModel | CMP-005 → CMP-007 | Component, membership, nguồn chia nhóm, cạnh có hướng/loại, fact references, nhãn, đề xuất bị loại |
| VerifiedResult | CMP-007 → CMP-008 | Mô hình đã kiểm, evidence, kết luận bị loại và lý do, coverage/limitations, snapshot và phiên bản |

Việc cần thực hiện:

1. Chốt định danh và phạm vi duy nhất: trong snapshot, run hay qua các lần chạy. Không hứa ID bền qua sửa source nếu chưa có thiết kế.
2. Phân biệt tên hiển thị có thể do model đặt với ID máy dùng tham chiếu.
3. Phân biệt giá trị chưa biết, không hỗ trợ, không áp dụng, đã kiểm nhưng không có. Không dùng chung `null` hoặc mảng rỗng cho tất cả.
4. Chốt trường bắt buộc, kiểu, enum, giới hạn độ dài/kích thước, quy tắc tham chiếu và thứ tự canonical khi cần.
5. Chốt membership theo file như FR-022 hiện hành; nếu muốn theo symbol phải đưa thành thay đổi có review.
6. Chốt đầu vào/đầu ra từng giao diện nội bộ; không ép giao diện hàm Python thành HTTP API.

Đầu ra: schema nhúng trong spec owner, từ điển trường, quy tắc liên kết và ví dụ. Điều kiện hoàn thành: trace được một route từ snapshot → fact → component → evidence → kết quả; ID không trùng, không cạnh mồ côi, không tham chiếu sai snapshot.

## 7. Chặng C — Contract LLM và cửa kiểm bằng chứng

Owner: CMP-006 cho giao tiếp model; CMP-005 cho đề xuất kiến trúc; CMP-007 cho kết quả kiểm cuối. Liên quan FR-022/023/024.

| Tác vụ | Nhận gì? | Trả gì? | Không được làm gì? |
|---|---|---|---|
| Đặt tên/mô tả | Nhóm đã có, dữ kiện và ID được phép tham chiếu | Tên, vai trò, mô tả, nhãn gắn vào ID có sẵn | Đổi membership hoặc sửa fact |
| Đề xuất cạnh | Component và dữ kiện liên quan trong phạm vi | Đầu/cuối, loại/chiều, evidence references, lý do | Tự công bố cạnh hoặc tạo fact giả |
| Chia repo phẳng — nhánh theo FR hiện hành | Tập file và dữ kiện đã nhận, sau khi có policy nhận diện flat | Nhóm và membership | Sót/trùng file, thêm file ngoài snapshot hoặc suy rằng D-03 đã chốt |
| Đọc code | Snapshot, phạm vi được cấp, file và range | Đoạn đã che bí mật hoặc lỗi từ chối | Đọc đường dẫn tùy ý ngoài snapshot |

Phải ghi: schema request/response riêng từng tác vụ, ngân sách, cách tính request vật lý, timeout/retry, lỗi provider/schema, provenance, cách bỏ phần lỗi và giữ phần hợp lệ. Kiểm khả năng thực tế của provider/model trước khi pin contract; các con số trong NFR không thay phép kiểm trên tài khoản dùng thật.

Cửa kiểm bằng chứng cần bảng quy tắc theo loại cạnh, phiên bản rule, dữ kiện cần có, điều kiện accepted/rejected và lý do. Kiểm schema không thay kiểm ý nghĩa liên kết; vượt kiểm tự động không thay đánh giá bằng gold.

Điều kiện hoàn thành: provider giả mô phỏng payload sai, ID lạ, sai snapshot, cạnh có evidence thật nhưng không liên kết, timeout, hết quota, nhóm trùng/sót file; mỗi ca có kết quả mong đợi. Fixture lỗi dùng để kiểm contract, không báo như benchmark chất lượng LLM thật.

## 8. Chặng D — Giao diện chạy CLI và web

Owner chính: CMP-001; tiếp nhận thuộc CMP-002; đọc kết quả/export thuộc CMP-008, evidence qua CMP-007. Liên quan FR-019/024/025/026.

| Thao tác | Cần đặc tả |
|---|---|
| CLI phân tích thư mục | Tham số, source/output hợp lệ, cách báo tiến trình, exit code cho completed/partial/failed, xử lý output đã tồn tại |
| Web gửi ZIP/GitHub public | HTTP method/path, content type, field, giới hạn, lỗi, consent dữ liệu gửi provider và cách xử lý key |
| Xem trạng thái | Mã run, trạng thái chờ/chạy/kết thúc theo quyết định A, stage, timestamps, lý do lỗi và expiry |
| Đọc kết quả | Snapshot, model version, dữ kiện và giới hạn của đúng run; lỗi chưa sẵn sàng/hết hạn |
| Mở evidence | Nhận evidence ID thay vì đường dẫn tùy ý; kiểm snapshot; trả đoạn hoặc lý do không phục vụ |
| Xuất/tải/thử lại artifact | Artifact ID, trạng thái riêng, định dạng, checksum, lỗi; thử lại không gọi lại model hoặc đổi model đã kiểm nếu chỉ lỗi renderer |

Chốt state machine và bảng lỗi trước tên endpoint. API web phục vụ UI phase đầu, không tự mở scope sang public job API, lịch sử, đăng nhập, private Git hoặc multi-tenant. CLI và web gọi cùng engine; CLI không cần web server.

Điều kiện hoàn thành: một người chỉ đọc contract có thể dựng mock consumer; mẫu request/response cho đường thành công, chờ, partial, failed và expired không mâu thuẫn. Tính đúng cấu trúc dữ kiện chung không có nghĩa hai lần gọi LLM độc lập phải ra cùng kết quả.

## 9. Chặng E — Xuất JSON, sơ đồ và sinh L3 cho repo đầu vào

Owner: CMP-008. Liên quan FR-025/027, NFR-ABST/ACC/SEC-002.

### E1. Model đầy đủ và góc nhìn

- JSON giữ mô hình đã kiểm và schema version; không cắt mất component vì trần sơ đồ.
- Mọi artifact dùng cùng tập component/cạnh; không ẩn node, không tạo cạnh tắt (API-008 §3).
- Các phần chung giữa artifact phải cùng ID/nội dung; từng góc nhìn có thể là tập con theo quyết định A.
- Chốt manifest output: file nào thành công/lỗi, checksum, snapshot, renderer version và giới hạn.
- Chốt publish bộ output/partial, retry, cleanup và việc đọc khi output hết hạn; không để file ghi dở được tải như hoàn chỉnh.

### E2. API của repository được phân tích

- Route thuộc component chứa nơi khai báo (FR-027). Bước nào gán owner đang chờ chốt: [đối chiếu, mục 6, dòng 1](L3-Generator-doi-chieu-nguon-L3.md#6-l2-thiếu-hoặc-mâu-thuẫn). Lưu app/registration context để không gộp nhầm hai app cùng method/path.
- Chốt chuyển fact thành bảng endpoint và OpenAPI 3.1: prefix, handler, parameters, request/response, status và auth khi có bằng chứng.
- Chốt biểu diễn phần chưa biết. Không chép chuỗi `unknown` vào trường yêu cầu kiểu chuẩn hoặc bịa endpoint/status để validator pass.
- Phân biệt contract partial đọc được với OpenAPI đủ điều kiện dùng cho client/code generation; công bố phần bị thiếu.

### E3. Bảng dữ liệu của repository được phân tích

- Chốt owner của bảng dùng chung, quan hệ giữa ORM model và bảng thật, trùng tên bảng khác schema/database.
- Chốt SQL dialect được hỗ trợ, kiểu, PK/FK, nullable/default nếu biết; chưa biết dialect thì không hứa DDL chạy được.
- Bảng thiếu dữ kiện: bỏ cả bảng khỏi DDL hay giữ phần biểu diễn được. Đang chờ chốt: [đối chiếu, mục 6, dòng 2](L3-Generator-doi-chieu-nguon-L3.md#6-l2-thiếu-hoặc-mâu-thuẫn).
- Chốt trường hợp chỉ xuất bảng mô tả/DDL một phần và cảnh báo. Không chạy DDL hoặc import ORM của repo để kiểm.

### E4. Event của repository được phân tích

- Chốt topic identity theo broker/context, producer, consumer và payload.
- Cùng tên topic nhưng chưa biết cùng broker không đủ để nối chắc hai bên.
- Đã chốt (CR-L3GEN-2026-003-decisions-01): EVT nằm ở từng component có điểm gửi hoặc nhận; chỉ liên kết hai bên khi có bằng chứng broker/cấu hình; chỉ thấy bên nhận vẫn xuất.
- Còn phải đặc tả: gom trong một component, topic chưa biết, payload partial, tên file trùng.
- Không triển khai Kafka bên trong L3 Generator chỉ vì công cụ cần mô tả Kafka của repository đầu vào.

### E5. Định dạng file và provenance

Tuân thủ cây output tại FR-027. Chốt cách xử lý tên/slug trùng, tên không có ký tự dùng được, ký tự đường dẫn không an toàn và thứ tự cấp hậu tố ổn định. Mỗi kết luận/thuộc tính được sinh phải truy được tới fact/evidence; heading hoặc lời nối mẫu không cần bịa evidence như một kết luận source.

File sinh tự động phải ghi rõ là tài liệu suy ra từ snapshot, chưa được người sở hữu repo phê duyệt. Không tạo UID/chữ ký/approval giả để giống hồ sơ chuẩn tắc của nhóm.

Điều kiện hoàn thành: bảng và khối máy đọc cùng thông tin; kiểm cú pháp đúng phiên bản; test route trùng giữa app, tên bảng động, broker chưa biết, mô hình hơn 50 node và lỗi một artifact. Mỗi định dạng (bảng Markdown, OpenAPI, DDL, EVT) có ít nhất một ví dụ partial cùng kết quả kiểm mong đợi, theo yêu cầu của CMP-008 bản Khiêm. Không coi render thành công là đã suy luận đúng kiến trúc.

## 10. Chặng F — UI cấp 4, mapping và bàn giao code

UI specification cấp 4 dùng **L3 + AC + UI cấp 1–3 đã được review theo gate áp dụng**. Nếu thiếu đầu vào UI thì ghi còn thiếu, không tự coi đã duyệt.

- Mỗi màn hình bind vào endpoint và field nào.
- Trạng thái loading/chờ/running/partial/failed/expired hiển thị gì, thao tác nào được phép.
- Khi nào không được hiển thị “không có dữ liệu” vì thực tế chưa phân tích được.
- Tìm/lọc/sơ đồ/evidence dùng ID và phạm vi dữ liệu nào.
- Thông báo lỗi và điều kiện retry; đường dẫn tải artifact có thể hết hạn.

Sau khi contract đủ rõ: cập nhật mapping AC → implementation target → test dự kiến; tách task theo luồng chạy được. Spec/test ID chỉ được tham chiếu khi đã có hoặc được ghi rõ là kế hoạch; không tạo evidence chạy test giả.

Phần golden hiện có ở checkout khác (`D:/VSF/VSF-L3 Generator/evaluation/`) là pilot trên mốc yêu cầu cũ, chưa là output contract của sản phẩm. Phải đối chiếu membership theo file/symbol, confidence, unknown và matching trước khi dùng. Viết adapter output sản phẩm → input evaluator; không ép sản phẩm đổi schema chỉ để khớp gold cũ. Không đưa đáp án gold vào prompt sản phẩm.

## 11. Thứ tự làm và thời gian dự kiến

Ước lượng dưới đây là ngày công tập trung của người soạn, không gồm chờ review, sửa lớn do đổi kiến trúc hoặc triển khai production. Cần cập nhật sau chặng B; không phải cam kết deadline.

| Chặng | Thời gian tham khảo | Phụ thuộc | Kết quả để review |
|---|---|---|---|
| 0/0b — Đồng bộ nguồn, dữ liệu đầu vào | 0,5–1 ngày soạn; chưa tính thời gian chờ thống nhất | Hai nhánh, pipeline v8 | File đối chiếu + bảng L2 |
| A — Danh mục và quyết định | 0,5–1 ngày | PRD/L2/AC | Bảng mâu thuẫn, owner và quyết định |
| B — Dữ liệu cốt lõi | 1–2 ngày | Quyết định ID, membership, unknown | Schema + một ví dụ xuyên suốt |
| C — Model/evidence | 1–1,5 ngày | B, quyết định evidence/budget | Contract tác vụ + bộ ca lỗi |
| D — CLI/web | 0,5–1 ngày | B, trạng thái/lifecycle | CLI contract + OpenAPI web và bảng lỗi |
| E — Export và API/TBL/EVT | 1–2 ngày | B/C, owner do CMP-005 gán | Quy tắc chuyển đổi + output mẫu |
| F — UI binding và bàn giao | 0,5–1 ngày | D/E và UI cấp 1–3 | UI spec, mapping và task list |

Tổng tham khảo: khoảng 5–9,5 ngày công; lịch thực tế còn vòng review. Nếu thiếu thời gian, ưu tiên một lát cắt dọc nhỏ thay vì viết sơ sài toàn bộ rồi tuyên bố xong.

**Lát cắt đầu tiên khi triển khai:** source nhỏ có một route và một bảng → snapshot → facts → membership fixture → model đặt tên/đề xuất trong phạm vi → kiểm evidence → JSON + tài liệu API/TBL. Khi D-03 còn mở, membership được cung cấp bởi test double có tên `fixture-membership-v1`, không đưa vào registry production. Ví dụ tài liệu hiện tại chỉ dựng dữ liệu và artifact JSON để kiểm contract; chưa thực hiện extraction/LLM/verification/rendering của sản phẩm. Provider giả cho phép kiểm giao diện trước; lượt provider thật được ghi riêng khi có cấu hình/ngân sách. Không bỏ LLM khỏi thiết kế chỉ vì mock chưa gọi provider thật.

Sau lát cắt này: thêm web và evidence viewer, rồi repo phẳng, nhiều app/đơn vị, event và partial. Trường hợp lỗi được viết cùng contract từng chặng, không đợi cuối dự án mới nghĩ tới.

## 12. Cách tổ chức file, review và đóng phiên bản

Contract chuẩn tắc đặt theo component trong `.aide/tech-specs/<CMP-slug>/`, theo Execution Guide:

```text
.aide/tech-specs/
  <component-so-huu>/
    api/API-<SYS>-<CMP>-vN.md
    schema/TBL-<SYS>-<CMP>.md       # chỉ khi có bảng dữ liệu thực sự
    events/EVT-<SYS>-<CMP>-<topic>.md # ở từng component có điểm gửi hoặc nhận
```

API/TBL/EVT là `.md` có metadata; OpenAPI/DDL/schema nhúng trong khối mã. File máy đọc trích từ spec phục vụ kiểm/code là artifact dẫn xuất, không thành một nguồn chuẩn tắc thứ hai có thể sửa độc lập.

Giao diện nội bộ và schema trao đổi cần owner rõ; chốt quy ước artifact với nhóm trước khi tạo. Có thể nhúng schema được giao diện sử dụng vào spec owner. Không biến mọi JSON thành TBL, không thêm HTTP chỉ để có file API, không tạo thư mục rỗng cho đủ tám CMP. UID và metadata dùng công cụ/quy ước của nhóm; không tự gõ ID giả.

Mỗi contract cần:

- Mục đích, owner, consumer, FR/AC/NFR và CMP liên quan.
- Đầu vào/đầu ra với kiểu, bắt buộc/tùy chọn, enum, giới hạn và unknown.
- Quy tắc tham chiếu, nghiệp vụ, lỗi, retry/idempotency/concurrency khi áp dụng.
- Phiên bản, cách thay đổi và tác động tới bên dùng.
- Ví dụ thành công, partial và lỗi cùng kết quả mong đợi.
- Cách kiểm cấu trúc và ý nghĩa; phần chưa chốt và ai xử lý.

Nhịp review: người soạn mở diff nhỏ theo một nhóm contract → người tiêu thụ kiểm bằng cách dựng request/output mẫu → ghi vấn đề và sửa → khóa revision cho task phụ thuộc. Trước khi chốt contract liên quan UI, hoàn tất binding cấp 4 theo quy trình. Breaking detection/Contract Gate áp dụng theo Execution Guide; chưa có baseline so sánh không được ghi “đã pass breaking check”.

Thay đổi PRD/FR/NFR từ quyết định A cần cập nhật revision, candidate và view/check theo quy trình của repo, giữ nguyên hồ sơ lịch sử. Đợt sửa ngày 25/09 đồng bộ các nguồn trên nhánh này và tạo BL-r5; nhánh của Khiêm có một BL-r5 khác (xem chặng 0). Không ký gate. Có thể soạn draft để thảo luận; trạng thái sẵn sàng code chỉ ghi sau khi hoàn tất điều kiện và review áp dụng.

## 13. Checklist bàn giao bản viết và triển khai tiếp

### Tài liệu L3 — đã xong (draft, tự review)

- [x] Tám owner/consumer, giao diện, schema và lỗi; không giữ bản sao schema có thể sửa độc lập.
- [x] Ví dụ snapshot → inventory → facts → membership định trước → verified fixture → JSON, có hash/range và ID để đối chiếu.
- [x] Script kiểm schema, OpenAPI, liên kết, ví dụ dương/âm và invariant tham chiếu; báo cáo dẫn xuất ghi đúng hash nguồn đã kiểm.
- [x] Quy tắc unknown/partial, evidence binding và không sửa fact bằng LLM được mô tả.
- [x] Ngân sách LLM, vòng đời run, status artifact và retry được đặc tả với ca lỗi cần triển khai.
- [x] Mọi artifact cùng tập component/cạnh, model tối đa 50 node; API/TBL/EVT có quy tắc owner (CMP-005 gán) và bảng biểu diễn phần thiếu theo định dạng.
- [x] Binding consumer web theo endpoint/field/trạng thái và mapping FR/AC ở từng spec.
- [x] D-03 để mở rõ ràng; phần còn thiếu và giới hạn phép kiểm đã công bố.
- [x] Chặng 0: nhánh `docs/l3-align-gate2` dùng nguồn trên git (`docs/gate-2` `5d06f14`). Không tạo BL-r6: lý do ở [bản đối chiếu](L3-Generator-doi-chieu-nguon-L3.md#6-l2-thiếu-hoặc-mâu-thuẫn), dòng 3. Bản 25/09 (nhánh `docs/l3-contracts-review`) giữ làm lịch sử.
- [x] Chặng 0b: đầu vào CMP-008 giữ là `VerifiedResult`; pipeline phải chuyển về cấu trúc này (API-008 §1).
- [x] 8 contract revision 4 khớp nguồn trên git; các điểm chờ đã chốt khi tự review (bản đối chiếu, mục 6). Bộ kiểm contract pass (20 ca dương, 31 ca âm).
- [x] Ví dụ kiểm cho từng định dạng của API-008 §3.2: API, TBL (fixture `shop_full`, `shop_partial`), EVT (`EventsFixture`, dữ kiện event soạn tay).
- [x] Mapping AC → contract → code → test của lát cắt đầu ([README bộ L3](../.aide/tech-specs/README.md), mục 4.1).
- [x] Code lát cắt đầu ở `slice/`: snapshot, route FastAPI, bảng SQLAlchemy, membership fixture, owner, kiểm trường, kiểm cạnh event, API/TBL/EVT, kiểm bản xuất; 27 test pass. Chưa chạy trên repo thật.

### Để sau hoặc ngoài phần tài liệu L3

- [ ] UI cấp 4: gắn contract với UXF/SCR/UID đã duyệt. Để sau theo yêu cầu người phụ trách.
- [ ] Review chéo với Khiêm (không bắt buộc theo người phụ trách). Nếu đổi tiếp thì tăng revision.
- [ ] Code sản phẩm: request/response model, tham số, `include_router`, cạnh dependency, trích event, SVG, gateway LLM, web, retry, hàng đợi, kiểm budget/quota/path/cleanup.
- [ ] Chọn và đánh giá thuật toán component (D-03) theo dữ liệu/gold độc lập; ghi partition version được chọn rồi thay test double.
- [ ] Benchmark/NFR/UAT và gate theo quy trình. Không lấy báo cáo kiểm draft làm bằng chứng pass AC của sản phẩm.

Thứ tự đề xuất cho phần code: review dữ liệu và verifier (004/005/007) → gateway (006) → output (008) → facade/intake/inventory (001/002/003) → task triển khai có phạm vi nhỏ. Khi còn D-03, có thể làm schema/consumer/verifier/renderer bằng fixture sau review áp dụng; chưa tuyên bố pipeline production hoàn chỉnh.

## 14. Tài liệu chuẩn tham khảo

- [OpenAPI 3.1.1](https://spec.openapis.org/oas/v3.1.1.html): tham khảo cách mô tả HTTP API, schema và extension. Chọn patch version cụ thể trong dòng 3.1 theo FR-027 rồi pin validator; không gọi 3.1.1 là bản mới nhất.
- [JSON Schema — object](https://json-schema.org/understanding-json-schema/reference/object): phân biệt field bắt buộc, field bị thiếu và `null`. Schema không tự chứng minh ID tham chiếu tồn tại hoặc bằng chứng đúng ý nghĩa.
- [AsyncAPI 3.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0): tham khảo channel/message/send/receive khi thiết kế EVT. Chưa phải yêu cầu bổ sung toàn bộ AsyncAPI vào phase đầu.

Nguồn chuẩn chỉ giúp chọn biểu diễn hợp lệ. Phạm vi sản phẩm và quyết định nhóm vẫn dựa trên PRD/FR/NFR được review; tài liệu này là kế hoạch nghiên cứu và thiết kế, không phải bằng chứng sản phẩm đã chạy.
