# Đối chiếu nguồn trước khi viết tiếp L3

Ngày 01/10/2026. Người lập: Hoàng (người soạn L3). Trạng thái: **các điểm chờ đã được người soạn tự review và chốt ngày 01/10/2026**; chưa có review của Khiêm. File này không sửa PRD, FR, L2 hay BL.

**Cập nhật cùng ngày:** đã tạo nhánh `docs/l3-align-gate2` từ `origin/docs/gate-2` (`5d06f14`, trùng phần `.aide/` với nhánh của Khiêm) và sửa 8 contract lên revision 4 cho khớp nguồn đó. Kết quả ở [mục 7](#7-đã-sửa-trong-contract-revision-4).

File này là đầu ra của chặng 0 và 0b trong [kế hoạch L3](L3-Generator-ke-hoach-trien-khai-L3.md#4-chặng-0-và-0b--đồng-bộ-nguồn-và-dữ-liệu-đầu-vào).

## 1. Hai mốc đang có

Mục này ghi hai nhánh làm cơ sở và mốc chung của chúng.

| | Nhánh L3 draft | Nhánh của Khiêm |
|---|---|---|
| Tên nhánh | `docs/l3-contracts-review` | `feature/quote-evidence` |
| Commit | `714f26e` (Hoàng, 25/09) | `a14d32c` |
| Commit đổi nguồn | `714f26e` | Chỉ `5d06f14` (Khiêm, 30/09). Năm commit sau không sửa `.aide/`; chỉ sửa `experiments/`, `evaluation/`, `docs/`, `CLAUDE.md` |
| Nội dung chính | PRD r29, FR/NFR, L2 đồng bộ, 8 contract, BL-r5 | ADR-003 r2, CAP-012 r3, FR-027 r3, CMP-004/005/007/008, threat model r4, BL-r5, CR-L3GEN-2026-003 |

Mốc chung: `2e909a8` (Khiêm, 23/09). Cột "sửa" ở các bảng dưới nghĩa là khác mốc chung.

## 2. Các file nguồn khác nhau

Có 22 file trong `.aide/product`, `requirements`, `architecture` khác nhau giữa hai nhánh.

| Nhóm | File | L3 draft | Khiêm | Đè nhau? |
|---|---|---|---|---|
| Chỉ L3 draft sửa | PRD (r28→r29); FR-022, 024, 025, 026; NFR-ABST-002, ACC-002, AI-002, OPS-001, SEC-002 | sửa | giữ nguyên | Không |
| Chỉ Khiêm sửa | ADR-003 (r1→r2), CAP-012 (r2→r3) | giữ nguyên | sửa | Không |
| Khiêm chỉ đổi metadata | CMP-002, CMP-003 (r1→r2) | giữ nguyên | chỉ `revision`, `verified_against` | Không |
| L3 draft sửa nội dung, Khiêm chỉ đổi metadata | CMP-001, CMP-006 | sửa | chỉ metadata | Không về nội dung, nhưng cả hai cùng ghi r2 |
| Cả hai sửa nội dung | CMP-004, 005, 007, 008; FR-027; threat model | sửa | sửa | Có. Cùng số revision (r2, r3, r4) mà nội dung khác |

Kết luận: phần lớn thay đổi **bổ sung cho nhau**. Nhánh L3 draft sửa vòng đời lần chạy, quota, binding cạnh, projection. Nhánh của Khiêm sửa đường đi của dữ kiện API/TBL/EVT. Vì vậy không chọn nguyên một nhánh. Phải gộp theo từng file.

## 3. Sáu file cả hai cùng sửa

| File | L3 draft thêm | Khiêm thêm | Nhận xét |
|---|---|---|---|
| FR-027 | Ngữ cảnh application/registration; mỗi application một khối OpenAPI; cột `default`; DDL theo catalogue đã pin; `CONTRACT_OWNER_UNRESOLVED`; `DDL_TABLE_OMITTED` (bỏ cả bảng khỏi DDL) | Mục "Chia tài liệu theo component"; EVT ở từng bên gửi/nhận; chỉ gom cùng topic khi cùng broker; tên file trùng thêm `-2`, `-3`; README làm mục lục; mục "Khi chưa đủ dữ kiện"; dialect lấy từ source | Bổ sung nhau. Cả hai đều đặt API/TBL theo nơi khai báo, EVT theo nơi gửi/nhận. Còn một điểm cần chốt: bảng [mục 6](#6-l2-thiếu-hoặc-mâu-thuẫn), dòng 2 |
| CMP-004 | ID dữ kiện gồm dòng, cột và khoá ngữ nghĩa | Bảng dữ kiện API/TBL/EVT; mỗi giá trị có nguồn riêng | Bổ sung nhau |
| CMP-005 | Quy tắc binding cạnh; projection khi quá 50 node | **CMP-005 xác định component sở hữu contract; CMP-008 không tự gán** | Mâu thuẫn với API-008 draft: [mục 6](#6-l2-thiếu-hoặc-mâu-thuẫn), dòng 1 |
| CMP-007 | Kiểm cạnh có dữ kiện ở hai đầu và rule version; mở evidence qua CMP-001 | Kiểm từng trường contract và liên kết với component sở hữu | Bổ sung nhau |
| CMP-008 | Mỗi application một khối OpenAPI; TBL theo catalogue; JSON chứa VerifiedResult | Ba bộ sinh API/TBL/EVT; bước kiểm bản xuất; giao cho L3 việc "đặc tả cách biểu diễn phần thiếu cho từng định dạng và bộ ví dụ kiểm tương ứng" | Bổ sung nhau, trừ chỗ ai gán owner |
| Threat model | ZIP và đường dẫn, quota, khoá API, T-13 (trang ngoài gọi web local) | T-08: nội dung contract lệch giữa các bản biểu diễn | Bổ sung nhau |

## 4. Hai candidate BL-r5

Mục này mô tả hai file cùng tên `BL-r5.yaml` mà nội dung khác nhau.

| | L3 draft | Khiêm |
|---|---|---|
| Key | `BL-CHG-L3GEN-2026-002-r5` | `BL-CHG-L3GEN-2026-002-r5` |
| `supersedes` | r4 | r4 |
| Ngày ghi trong `note` | 25/09 | 23/09 (commit ngày 30/09) |
| PRD | r29 | r28 |
| Nội dung | 8 contract, L2 đồng bộ | FR-027 r3 theo quyết định của Khiêm |

Cách xử lý đề xuất (**chưa làm**, chờ thống nhất nguồn):

1. Giữ cả hai bản làm lịch sử, không sửa byte. Hai file nằm cùng đường dẫn nên khi gộp nhánh không thể để cả hai ở đúng chỗ đó. Cần chốt bản nào nằm ở đường dẫn, còn bản kia được giữ ở đâu (ví dụ chỉ giữ qua commit Git).
2. Sau khi gộp nguồn, tạo candidate mới với mã chưa dùng. Hiện cả hai nhánh mới tới r5.
3. Cập nhật các liên kết tới candidate cũ.
4. Tính lại sha256 từng file trong candidate mới và so với file thật.

## 5. Đầu vào L3 so với `graph.json` của v8 (chặng 0b)

Mục này so đầu vào CMP-008 trong L3 draft với file mà pipeline v8 đang xuất.

- **L3 draft:** CMP-008 nhận `VerifiedResult` (API-L3GEN-007-v1). Bên trong có `FactSet` (API-004) và `ArchitectureModel` (API-005).
- **v8:** `experiments/quote-evidence/run7.py` ghi `graph.json`. Đã xem ba lần chạy: `v8-nodraft-realworld`, `-fullstack`, `-lnbits`.

| Trường L3 cần | Trong `graph.json` | Trạng thái |
|---|---|---|
| `snapshot_id` | `snapshot`: map đường dẫn → sha256, không có mã snapshot | Chuyển đổi được |
| `inventory`: unit, mức hỗ trợ, phần bỏ qua | `file_lines`; `excluded` dạng `"dir:tests": 12` | Thiếu unit và mức hỗ trợ |
| Fact route: method, path, handler, request/response | Không có. `calls.py` chỉ giữ dòng đầu tiên có dấu hiệu (`@router.<verb>`, `__tablename__`) trong bộ nhớ, không ghi ra file | **Thiếu** |
| Fact bảng: tên, cột, kiểu, khoá | Không có | **Thiếu** |
| Fact event: topic, broker, payload | Không có | **Thiếu** |
| Component: `id`, `name`, `member_file_ids` | `components[].id`, `name`, `files` | Chuyển đổi được (đường dẫn → file_id) |
| Component: `grouping_source` | `meta.grouping`, `meta.by_rule` | Chuyển đổi được một phần |
| Component: `confidence`, `completeness`, `label_status` | Không có | Thiếu |
| Cạnh: nguồn, đích | `edges[].source`, `target` | Có sẵn |
| Cạnh: `relation_type` | `label` là chữ tự do do code đặt ("gọi X", "đăng ký qua X") | Chuyển đổi được nếu chốt bảng ánh xạ |
| Cạnh: `fact_ids`, `rule_id`, `rule_version` | Không có. `prompt_sha` là phiên bản prompt, không phải rule | Thiếu |
| `external_systems` | `externals` | Có sẵn |
| `evidence_index`: đường dẫn, sha256, dòng, cột | `quote{file, line, text}`; sha256 lấy từ `snapshot` | Chuyển đổi được; cột để `null` |
| `decisions`: accepted/rejected kèm rule | `rejected`, `meta.edge_check` | Chuyển đổi được một phần |
| `limitations`: mã, `affected_ids` | `meta.issues` là chuỗi tự do | Chuyển đổi được một phần |
| Component sở hữu từng API/TBL/EVT | Không có | **Thiếu** |
| Mức kiểm bằng chứng | `verify.py` kiểm câu trích có đúng nguyên văn ở dòng đó, và file thuộc component. File ghi: nghĩa của câu vẫn là suy luận. L3 (`FieldValue`) cần bằng chứng chứng minh giá trị của từng trường | **Khác mức** |

Ghi chú: `meta.pipeline` trong các lần chạy v8 ghi `"v7"`. Không dùng trường này để biết phiên bản pipeline.

**Kết luận:** `graph.json` đủ để dựng sơ đồ component. Nó không đủ để sinh API/TBL/EVT. Không ép L3 dùng nguyên `graph.json`. Cần hỏi Khiêm:

1. v8 sẽ thành pipeline thật, hay chỉ là thí nghiệm cho sơ đồ?
2. Bộ nào sẽ trích fact route/bảng/event? `l3gen` 0.1 đang trích route và bảng vào `IAM.json`, nhưng chưa ai đối chiếu với `FactSet`.
3. Dữ liệu bàn giao cho CMP-008 giữ tên và cấu trúc `VerifiedResult`, hay đổi?

## 6. L2 thiếu hoặc mâu thuẫn

Mục này liệt kê các vấn đề ở nguồn mà L3 phụ thuộc. Cột "Ảnh hưởng" ghi vấn đề có chặn việc viết L3 không.

| # | Chỗ phát hiện | Vấn đề | Đề xuất | Ảnh hưởng tới L3 | Trạng thái |
|---|---|---|---|---|---|
| 1 | CMP-005 bản Khiêm và API-008 draft §5 | Ai gán component sở hữu contract | Theo ADR-003 r2: CMP-005 gán, CMP-007 kiểm, CMP-008 chỉ đọc | Đã hết chặn | **Đã xử lý:** contract r4 làm theo nguồn git; không cần sửa L2 |
| 2 | FR-027 hai bản | Bảng thiếu dữ kiện: bỏ cả bảng khỏi DDL, hay giữ phần biểu diễn được? | Bỏ cả bảng, có notice. Lý do: một bảng thiếu cột trong DDL dễ bị đọc như bảng đầy đủ | Không chặn | **Đã chốt (tự review):** bỏ cả bảng khỏi DDL; contract và code làm theo |
| 3 | Mục 2, 4 | Sáu file và BL-r5 cùng số revision mà nội dung khác | Nhánh mới chỉ dùng nguồn git; trên nhánh này chỉ còn một BL-r5 (của Khiêm) | Không chặn | **Đã chốt:** không tạo BL-r6. BL-r5 là baseline của Scope Gate, chỉ chứa PRD/FR/NFR. Đưa contract vào baseline là việc ở Contract/Architecture Gate và phải sửa `change-set.yaml` do Khiêm lập |
| 4 | CMP-001, CMP-006 | Bản L3 draft sửa nội dung; bản Khiêm chỉ đổi metadata | Nhánh mới không mang các sửa đó; contract ghi phần chi tiết thêm là "chi tiết L3" | Để mở được | Đã xử lý trong L3 |
| 5 | Mục 5 | Đầu vào CMP-008 chưa có fact API/TBL/EVT và owner trong `graph.json` | L3 giữ `VerifiedResult` làm đầu vào CMP-008. Pipeline nào cấp dữ liệu phải chuyển về cấu trúc này; trường thiếu ghi `unknown`/limitation (API-008 §1). Lát cắt đầu dùng bộ trích riêng theo API-004 | Không chặn L3. Việc viết bộ chuyển từ `graph.json` thuộc phần pipeline | **Đã chốt (tự review)** |
| 6 | CMP-001, 004, 005, 006, 007, 008 và threat model bản L3 draft | L2 và threat model bị sửa ngày 25/09 khi làm L3 (ghi chú "Cập nhật draft 25/09/2026…" hoặc "Draft đồng bộ 25/09/2026…" ở đầu file), chưa có Khiêm duyệt | Không mang sang nhánh mới. Phần nào cần thì đưa vào nguồn qua bước thống nhất | Không chặn | Đã xử lý trong L3 |
| 7 | NFR-OPS-001 r1, CMP-001 r2 | Nguồn không giới hạn số run chờ, không có hạn chờ. Web cục bộ nhận ZIP tới 100 MB nên hàng đợi dài có thể đầy đĩa | Thêm vào nguồn: tối đa 1 run chờ, hạn chờ 30 phút | Không chặn | **Đã chốt (tự review):** giữ đúng nguồn, không giới hạn. Đề xuất giới hạn chỉ áp dụng khi nguồn được sửa |
| 8 | Các contract r4 | Một số quy tắc là "chi tiết L3", chưa có trong nguồn: cách tính ID, binding cạnh chặt hơn AC-022-02, cách đếm request, hợp các đoạn source không phủ nguyên file, prompt nhập khóa, slug, catalogue DDL | Giữ làm quy tắc L3. Các quy tắc này chỉ chi tiết hóa hoặc loại thêm, không nhận thứ mà nguồn loại | Không chặn | **Đã chốt (tự review)** |

## 7. Đã sửa trong contract revision 4

Mục này ghi chỗ contract r3 trái nguồn trên git và cách r4 sửa.

| Contract r3 | Nguồn trên git | Contract r4 |
|---|---|---|
| JSON giữ model đầy đủ; sơ đồ là projection ≤50 node, có hidden IDs | PRD r28, FR-025 r2 AC-04: không artifact nào chứa thứ artifact khác không có. CMP-005 r2 §4: giữ trần 50, phần dư ở lớp bằng chứng | Bỏ `ViewProjection`. Mọi artifact cùng tập node/cạnh; model >50 node là lỗi invariant |
| Hàng đợi 1 chạy + 1 chờ, từ chối `429 queue_full`, hạn chờ 30 phút | NFR-OPS-001 r1: "1; lần sau xếp hàng" | FIFO không giới hạn; bỏ `queue_full`, `queue_expired`, `queue_deadline_at` |
| Không còn fact dùng được thì `failed` | CMP-007 r2 §4: loại hết thì mô hình rỗng, `partial`; CMP-001 r2 §4: hết 30 phút thì `partial` | `partial` khi publish được; `failed` chỉ khi intake từ chối, tiến trình chết, không publish được |
| CMP-008 tự tra owner từ membership | ADR-003 r2, CMP-005 r2: CMP-005 gán owner | Thêm `contract_owners` vào API-005; rule `CONTRACT-OWNER` ở API-007; API-008 chỉ đọc |
| Mỗi application một khối OpenAPI | FR-027 r3 AC-01: "một khối OpenAPI 3.1" | Một khối mỗi file; trùng method/path giữa application thì omitted có notice |
| Cột có `default`; default unknown làm bỏ cả bảng khỏi DDL | AC-027-02: tên, kiểu, PK, FK, nullable | Bỏ `default` |
| Chưa có kiểm từng trường contract | CMP-007 r2 §1 "Kiểm nội dung contract" | Rule `CONTRACT-FIELD`: giá trị literal phải có trong evidence |
| Chưa có bước kiểm bản xuất và bảng phần thiếu theo định dạng | CMP-008 r2 §2: phải đặc tả cách biểu diễn phần thiếu cho từng định dạng và bộ ví dụ kiểm | API-008 §3.1, §3.2; ví dụ kiểm trong `slice/tests/` cho API và TBL |
| EVT theo owner/channel | FR-027 r3: EVT ở từng bên gửi/nhận; trùng tên theo thứ tự nguồn; topic chưa biết dùng nhãn từ mã dữ kiện | API-008 §4, §6.2 theo đúng các quy tắc đó |
| Viện dẫn PRD r29, FR r3, NFR r3/r4 | Không có trên git | Viện dẫn đúng revision trên git; phần thêm ghi "chi tiết L3" |

Đã kiểm lại một điểm từng nghi là lệch: CMP-006 r2 có dòng "Provider trả 503 quá tải | Tính như timeout", nên retry khi 503 là đúng nguồn.

## 8. Việc tiếp theo

- Phần L3 không gồm UI/UX: đã xong ở mức draft tự review (xem checklist trong kế hoạch L3).
- Khi cần review chéo: gửi mục 6–7 cho Khiêm.
- UI cấp 4 làm sau, khi có UXF/SCR/UID đã duyệt.
