# Báo cáo tổng thể code L3 — 01/10/2026 (bản 2)

Báo cáo này ghi phần đã code, đã test và đã đo của L3 Generator theo [kế hoạch code L3](L3-Generator-ke-hoach-code-L3.md) (Đợt 0–10, 11 mục), kèm giao diện web cục bộ. Bản 2 thay bản 1. Bản 1 nói quá ở một số chỗ, đã bị review chỉ ra (xem §5).

Repo: `D:\VSF\l3-generator-l3`, HEAD `5d06f14`. **Chưa commit.** HEAD không định danh được code mô tả ở đây.

## 1. Tóm tắt

- Có code và test cho phần lớn Đợt 0–10 cùng một giao diện web. Một số đợt mới làm một phần hoặc đang bị chặn (bảng §2). 152 test pass. Không test nào gọi mạng ngoài máy.
- Đã sửa 7 lỗi do review tìm ra và 11 lỗi do bộ đánh giá độc lập `evaluation_l3` tìm ra. Mỗi lỗi có test hồi quy. Gỡ bản sửa ra thì test fail.
- **Chưa** đạt điều kiện nghiệm thu ở §8 của kế hoạch:
  - D-03 chưa chọn;
  - gold chưa review, held-out chưa chạy;
  - chưa gọi LLM thật;
  - chưa tải GitHub thật;
  - chưa có người review mẫu output.

## 2. Trạng thái từng đợt

"Đã đo" chỉ ghi phép đo trên dữ liệu ngoài bộ test. Test pass không phải là số đo.

| Đợt | Nội dung | Trạng thái | Đã đo | Còn thiếu |
|---|---|---|---|---|
| 0 | Sửa lỗi đã biết | Xong | — | — |
| 1 | Bộ trích CMP-004 | Có code, test | Golden dev (bộ trích) | Chưa so số với `l3gen` 0.1 |
| 2 | Cạnh tĩnh CMP-005 | Có code, test | Golden dev (reference) | — |
| 3 | Verifier CMP-007 | Một phần | — | Rule `http-binding`, `config-binding` trả `RULE_UNSUPPORTED`: bộ trích chưa có dữ kiện định danh service |
| 4 | Bộ sinh tài liệu CMP-008 | Có code, test | `evaluation_l3` 80/82 | Không tách module |
| 5 | SVG, ghi file an toàn, retry | Có code, test | `evaluation_l3` | — |
| 6 | Cổng LLM CMP-006 | Có code, test với provider giả | — | Chưa gọi provider thật; ước lượng token chưa hiệu chỉnh |
| 7 | LLM trong CMP-005; thí nghiệm D-03 | Có code; D-03 **chờ chọn** | D-03 trên 7 case dev | Ứng viên C `not_run`; `group_flat` chưa nối pipeline |
| 8 | Tiếp nhận ZIP, GitHub, nhiều unit | ZIP xong; GitHub có code nhưng **tắt mặc định**; nhiều unit **bị chặn** | — | Security review GitHub (API-002 §1); review quy tắc tìm root (API-003 §1) |
| 9 | Vòng đời run, HTTP facade | Có code, test | — | Coordinator nhiều tiến trình cho CLI (exit 75) |
| 10 | Tích hợp và đo | Một phần | 3 case dev qua CLI, 1 case qua web | Held-out `blocked`; chưa có người review mẫu |
| UI | Web cục bộ (API-001 §8.1) | Có code, test tự động, ảnh chụp | — | Chưa có UXF/SCR được duyệt; chưa ai thao tác tay |

## 3. Số đo

### 3.1. Bộ trích trên golden v1, tập development

Lệnh: `slice/tools/run_golden.py`. 38 case. Gold `candidate`, `human_review_complete: false`, nên chỉ báo TP/FP/FN.

| Nhóm | TP | FP | FN |
|---|---:|---:|---:|
| route | 61 | 0 | 0 |
| reference | 84 | 0 | 1 |
| entity | 18 | 0 | 4 |
| entity_columns | 108 | 0 | 0 |
| limitation | 2 | 0 | 0 |

Phạm vi của số đo này:

- Chỉ đo **bộ trích** qua bộ chuyển (snapshot → extract → adapter → scorer). Không chạy verifier, renderer hay model. Route 61/0/0 không chứng minh `requestBody`, nullable, OpenAPI hay SVG đúng. Hai lỗi 6 và 7 ở §5 nằm đúng vào phần không được đo.
- `false_exact = 0` chỉ đúng **sau adapter**. Adapter gán route thành `exact`, còn completeness chỉ theo path. Một route sản phẩm ghi `inferred/partial` có thể thành `exact/full` trong bản dự đoán. Số này không chứng minh nhãn của sản phẩm đúng.
- 4 FN entity: 2 ở `dispatch-case-read` (tên bảng tính lúc import), 2 ở `orders-derived-tablename` (tên bảng suy từ code). Bộ trích không chạy code nên để `unknown`.
- 1 FN reference: `pycg-classes-nested_class_calls` (`B(self.c)`), giới hạn đã biết.

### 3.2. Thí nghiệm D-03, 7 case dev có nhãn kiến trúc

Lệnh: `slice/tools/d03_experiment.py`. Gold có 20 component, 28 membership, 13 cạnh. Chỉ báo TP/FP/FN.

| Ứng viên | Membership TP/FP/FN | Cạnh TP/FP/FN |
|---|---|---|
| A `directory-v1` | 14/14/14 | 0/0/13 |
| B `signals-v0` | 27/1/1 | 13/11/0 |
| C pipeline v8 | `not_run` | `not_run` |

Bảng từ khóa của B do tôi viết **sau khi đọc** 7 case dev. 6/7 case là cùng một fixture `orders`. Số tốt của B chưa nói được gì về repo khác. Tôi không chọn D-03.

### 3.3. Bộ đánh giá độc lập CMP-008 (`slice/evaluation_l3`)

Bộ này **không do tôi viết**: thư mục được tạo lúc 17:15–17:22 ngày 01/10/2026. Nó dùng 82 ca tổng hợp và kiểm renderer theo contract. Đây không phải số đo chất lượng trên repo thật.

| Lần chạy | Pass | Fail | Lỗi |
|---|---:|---:|---:|
| Trước khi sửa | 68 | 11 | 3 |
| Sau khi sửa | 80 | 1 | 1 |

Hai ca còn lại do fixture:
- `api-parameters` ghi tham số bằng khóa `type`, trong khi API-004 định nghĩa Parameter là `{name,in,required,schema}`;
- `graph-parallel-types` dùng relation `depends`, không có trong schema (bộ đánh giá tự báo "Fixture violates input schema").

Ca `names-64` chỉ pass khi thư mục output đủ ngắn. Ở thư mục tạm dài, path vượt 260 ký tự và renderer trả `OUTPUT_UNSAFE` đúng theo API-008 §4.

### 3.4. Chạy thật

| Cách chạy | Case | Kết quả |
|---|---|---|
| CLI, membership theo thư mục | `dispatch-case-read`, `sqlmodel-docs-teams-tutorial001`, `orders-base` | exit 3, 6/6 artifact ready; hai lần chạy cho cùng sha256 (đo ở bản 1, trước các sửa của bản 2) |
| Web, `--demo-partition` | `dispatch-case-read` (ZIP) | `partial`; 6/6 ready; intake 15 ms, phân tích 281 ms, xuất 172 ms, bộ nhớ đỉnh của tiến trình 49,7 MB |

Ảnh chụp UI của lần chạy web: `ket-qua-chay/6-ui/`. Chưa ai review thủ công từng file API/TBL của mẫu.

### 3.5. Test và bộ kiểm contract

- 152 test, Python 3.11.9, Windows 11: pass.
- Gỡ từng bản sửa đều làm test fail: 7 lỗi review, kiểm đầu vào renderer, `PUBLISH_FAILED`, Host/Origin, FIFO, hạn 24 giờ, che bí mật…
- Một bản gỡ không làm test fail: bỏ kiểm "artifact đã ready" trong `engine.retry`. Hành vi không đổi vì `render.retry_artifact` tự bỏ qua artifact ready.
- `scripts/check_l3_contracts.py --report`: 8 contract, 136 `$ref`, 20 ca dương, 31 ca âm; pass.

## 4. Việc chưa chạy hoặc bị chặn

| Việc | Trạng thái | Lý do |
|---|---|---|
| Golden held-out | `blocked` | Gold chưa review (D23) |
| Gọi Groq/Gemini thật | `not_run` | Không có khóa. Với `--llm`, tác vụ dừng trước khi gửi (`PAID_ROUTE_DISABLED`) vì chưa có bản ghi free-only và capability |
| Tải GitHub thật | `not_run` | Code có, test bằng transport giả. Chỉ bật bằng `--enable-github`; cần Security review danh sách host (`api.github.com`, `codeload.github.com`) theo API-002 §1. Chưa pin kết nối TCP vào địa chỉ đã kiểm |
| Nhiều unit | `blocked` | API-003 §1: quy tắc tìm root cần review trước code |
| Chọn D-03 | `blocked` | Người phụ trách chọn. Web mặc định trả `failed/partition_policy_unavailable`; `--demo-partition` chỉ để chạy thử và ghi lý do `demo_partition` trên mọi run |
| `http-binding`, `config-binding` | Chưa code | Cần dữ kiện định danh service mà bộ trích chưa có |
| Exit 75 của CLI | Không áp dụng | CLI chạy engine trong cùng tiến trình, mỗi lần gọi một run |
| Trần 30 phút/2 GiB | Một phần | Kiểm giữa các giai đoạn, không ngắt giữa một giai đoạn; bộ nhớ đo của cả tiến trình |

## 5. Lỗi đã sửa trong bản 2

**Từ review** (`ket-qua-chay/review-codex-20261001-164427/REVIEW.md`). Test ở `slice/tests/test_review_fixes.py`.

| # | Lỗi | Sửa |
|---|---|---|
| 1 | Mật khẩu trong `DATABASE_URL` lọt vào `result.json` và payload gửi model | Một bộ che chung ở `common.py`: thêm mẫu `user:pass@` và tham số query nhạy cảm. Bộ trích đổi mọi giá trị có dấu hiệu credential sang `redacted` và ghi giới hạn `VALUE_REDACTED` |
| 2 | Verifier nhận `20` khi source ghi `200` | So nguyên literal hoặc nguyên token, không so chuỗi con; status ngoài 100–599 về `unknown`; path ghép từ nhiều đoạn được so theo segment |
| 3 | Sửa status trong bảng mà `check_doc` không báo | `check_doc` đọc lại giá trị bảng, OpenAPI, cột, DDL, topic và payload, so với fact |
| 4 | Manifest sai kiểu làm run kẹt ở `running` | Manifest sai cấu trúc thành `MANIFEST_INVALID`; mọi lỗi lạ chuyển run sang `failed/internal_error`; worker chạy tiếp |
| 5 | Local và ZIP cho snapshot khác nhau | Dùng chung quy tắc bỏ `.git`, `.venv`, `node_modules`…; cùng `excluded` |
| 6 | Body tùy chọn bị ghi `required: true` | Body có thêm trường `required`; đã sửa API-004 cho khớp |
| 7 | `list[int \| None]` mất `null` | Giữ nullable của phần tử; `tuple` nhiều kiểu để unknown; tham số nullable được giữ |

**Từ `evaluation_l3`.** Test ở lớp `RendererInputAndPublish`.

- Renderer kiểm VerifiedResult trước khi sinh. Sai thì trả `INVALID_INPUT`, `SNAPSHOT_MISMATCH` hoặc `REFERENCE_INVALID` và không publish gì. Các trường hợp: thiếu hoặc sai `schema_version`, lệch snapshot, cạnh treo, fact trùng, thiếu evidence, component bị `rejected`.
- Route chưa biết application hoặc registration context thì bị bỏ khỏi OpenAPI (API-008 §5).
- Tên bảng đích của FK có ký tự điều khiển thì bảng bị bỏ khỏi DDL.
- Lỗi ghi file trả `PUBLISH_FAILED`, kể cả khi retry; manifest cũ giữ nguyên. Path quá giới hạn Windows trả `OUTPUT_UNSAFE`.
- Slug có suffix vẫn giữ tối đa 64 ký tự.

## 6. Phần mới trong bản 2

| Phần | File | Ghi chú |
|---|---|---|
| Tải GitHub | `slice/l3slice/github.py` | Default branch → SHA → zipball của SHA đó; chỉ HTTPS tới 2 host; kiểm IP public sau mỗi redirect; 120 giây cho cả thao tác; không gửi credential |
| Trần tài nguyên | `slice/l3slice/engine.py` | Vượt trần sau khi có snapshot: bỏ bước model, vẫn kiểm và xuất (`partial`). Vượt trần trước khi có snapshot: `failed` |
| CLI | `slice/l3slice/__main__.py` | `analyze`/`retry` có `--json` trả `CliResult`; exit 0/2/3/4/130 |
| UI | `slice/l3slice/ui/` | Xem §7 |

## 7. Giao diện web

Chạy:

```powershell
cd slice
python -m l3slice.web --workdir <thư mục làm việc> --port 8000 --demo-partition
```

Mở `http://127.0.0.1:8000/`. Các màn hình theo bảng API-001 §8.1:

| Màn hình | Làm gì |
|---|---|
| Gửi repository | Hiện thông báo `l3gen-egress-v1` trước khi gửi; gửi ZIP hoặc URL GitHub; không có ô credential; lỗi mạng khi POST không tự gửi lại |
| Trạng thái run | Poll ≥2 giây; tôn trọng `Retry-After`; giai đoạn hiện theo tên, không bịa phần trăm; lý do, số đo ("chưa đo" khi null) |
| Artifact | Chỉ tải file ready; nút thử lại chỉ có khi `failed` và còn retry được |
| Tổng quan | Sơ đồ SVG (hiện bằng `<img>`); tìm và lọc component, file, route, bảng, quan hệ trên cùng một bundle |
| Chi tiết component | File thành viên, contract sở hữu, nhãn confidence/completeness |
| Bằng chứng | Đoạn source đã che bí mật; snapshot không khớp thì báo lỗi, không hiện source mới |
| Phạm vi, giới hạn | Unit, mức hỗ trợ, đường dẫn bị loại; giới hạn phân tích; phần chưa biểu diễn, gom theo mã |

Bảo vệ:
- Content-Security-Policy chỉ cho script và style cùng origin;
- không dùng `innerHTML`, không dùng `localStorage`;
- run hết hạn hoặc 404 thì xóa nội dung đang hiện;
- đổi run thì bỏ phản hồi của run cũ.

UI chưa gắn ID màn hình UXF/SCR vì nhóm chưa duyệt.

## 8. Quyết định và lưu ý

| Việc | Đã làm |
|---|---|
| Tách `render.py` thành module (kế hoạch Đợt 4) | Không tách: CLAUDE.md không cho refactor khi không cần |
| D-07 "không gửi nguyên file" | Chỉ tính các đoạn mà công cụ đọc code gửi. Chữ ký trong FactSet là `ast.unparse`, không phải đoạn nguyên văn |
| Mô tả và vai trò do model đặt | Hiện trong UI, chưa có trong README vì API-008 không quy định chỗ hiện |
| BL-r6 | Không tạo; chưa ghi lý do riêng, cần anh xác nhận |
| `sqlglot` cài nhầm vào venv gate2 | Vẫn còn trong `D:\VSF\l3-generator-gate2\scripts\.venv`, chưa gỡ |
| File không do tôi tạo | `slice/evaluation_l3/`, `slice/tools/evaluate_l3.py`, `ket-qua-chay/l3-evaluation-development-01/`. Tôi chỉ chạy, không sửa |

## 9. Cần anh quyết định

1. Chọn ứng viên D-03.
2. Review danh sách host GitHub và quy tắc tìm root nhiều unit.
3. Duyệt UXF/SCR, hoặc cho dùng UI hiện tại làm bản nháp.
4. Có báo người viết `evaluation_l3` về 2 fixture lệch contract không.
5. Có gỡ `sqlglot` khỏi venv gate2, xóa `docs/L3-Generator-ke-hoach-hoan-thien-bo-sinh-tai-lieu.md`, và commit không.

## 10. Địa chỉ file và chạy lại

| Nhóm | File (gốc `D:\VSF\l3-generator-l3\`) |
|---|---|
| Code | `slice/l3slice/`: `common`, `snapshot`, `github`, `pyindex`, `extract`, `model`, `gateway`, `annotate`, `verify`, `render`, `engine`, `web`, `__main__`; UI ở `slice/l3slice/ui/` |
| Công cụ đo | `slice/tools/run_golden.py`, `golden_adapter.py`, `d03_experiment.py` |
| Test | `slice/tests/` (12 file, 152 test) |
| Contract | `.aide/tech-specs/`; bảng AC → code → test ở `.aide/tech-specs/README.md` §4.1 |
| Kết quả chạy | `ket-qua-chay/`: `2-golden-dev-v2`, `3-d03-v2`, `5-evaluation-l3`, `6-ui`; kết quả bản 1 ở `1-…`, `2-golden-dev`, `3-d03`, `4-…` |

```powershell
$env:PYTHONIOENCODING='utf-8'
scripts/.venv/Scripts/python.exe -m unittest discover -s slice/tests
scripts/.venv/Scripts/python.exe scripts/check_l3_contracts.py
scripts/.venv/Scripts/python.exe slice/tools/run_golden.py --golden-root "D:/VSF/VSF-L3 Generator" --out <thư mục mới>
scripts/.venv/Scripts/python.exe slice/tools/d03_experiment.py --golden-root "D:/VSF/VSF-L3 Generator" --out <thư mục mới>
scripts/.venv/Scripts/python.exe slice/tools/evaluate_l3.py --output <thư mục mới, path ngắn>
```

Mới chạy lại trên một máy, chưa thử trên máy khác.
