# Code L3 của L3 Generator

Luồng FR-029 (`document`, `docweb`) dùng agent đọc source để sinh API và README, nhận component/sơ đồ từ bước kiến trúc. Giao diện mới chạy tại cổng 8001; hướng dẫn bên dưới.

Thư mục còn giữ lát cắt cũ (`analyze`, `web`): trích dữ kiện tĩnh để sinh API, TBL, EVT và sơ đồ; nhận thư mục Python, ZIP hoặc GitHub khi bật. Các contract của lát cắt này nằm ở [.aide/tech-specs](../.aide/tech-specs/README.md). Hai giao diện dùng hai luồng xử lý khác nhau.

## Module

| File | Contract | Làm gì |
|---|---|---|
| `l3slice/snapshot.py` | API-002, 003 | Snapshot thư mục local hoặc ZIP (kiểm từng entry, không giải ra đĩa; local và ZIP cùng quy tắc chọn file); một unit `.` |
| `l3slice/github.py` | API-002 §1 | Tải zipball của commit SHA mặc định; chỉ 2 host GitHub, kiểm IP public, 120 giây; chỉ chạy khi web bật `--enable-github` |
| `l3slice/pyindex.py`, `extract.py` | API-004 | Duyệt cây cú pháp: route, model request/response, bảng, event, HTTP client, config, thư viện, reference; che giá trị có dấu hiệu credential. Không import, không chạy source |
| `l3slice/model.py` | API-005 | Membership từ file JSON soạn sẵn (`fixture-membership-v1`); owner contract; cạnh tĩnh |
| `l3slice/gateway.py` | API-006 | Cổng gọi model: ngân sách, giới hạn theo phút, retry, che bí mật, công cụ đọc code; client Groq/Gemini viết bằng `urllib` |
| `l3slice/annotate.py` | API-005 §3–5 | Nhãn component, đề xuất cạnh, chia nhóm repo phẳng qua cổng model; đề xuất phải được rule tĩnh chứng minh |
| `l3slice/verify.py` | API-007 | Kiểm hash, range, giá trị literal (nguyên token), miền status, owner, cạnh |
| `l3slice/render.py` | API-008 | Kiểm đầu vào; `result.json`, `manifest.json`, README, Mermaid, SVG, API/TBL/EVT; đọc lại giá trị đã xuất; ghi file an toàn; retry một artifact |
| `l3slice/engine.py`, `web.py` | API-001 | Vòng đời run, hàng đợi FIFO, hạn 24 giờ, trần 30 phút/2 GiB giữa các giai đoạn; HTTP `/api/v1` chỉ nghe loopback |
| `l3slice/ui/` | API-001 §8.1 | Trang web tĩnh: gửi repo, trạng thái, artifact, sơ đồ, component, bằng chứng, phạm vi, giới hạn |
| `tools/run_golden.py`, `golden_adapter.py` | — | Chấm bộ trích trên golden v1 tập development |
| `tools/d03_experiment.py` | — | So sánh ứng viên chia nhóm D-03 trên 7 case dev có nhãn kiến trúc |
| `l3slice/source_tools.py`, `docfacts.py`, `docagent.py`, `docpipeline.py`, `tailieu.py` | FR-029 | Luồng tài liệu bằng agent: model đọc source qua công cụ, code kiểm bằng chứng rồi sinh API, README và `TAI-LIEU.md` (một file đọc chính cho người). Component, `archdia.json` và sơ đồ là đầu vào, không tự tạo |
| `tools/fr029_score.py`, `tools/fr029_oracle.py` | FR-029 | Chấm `result.json` với gold; oracle dựng gold từ `app.openapi()` trong venv riêng (xem `tests/fixtures/fr029/README.md`) |

`evaluation_l3/` và `tools/evaluate_l3.py` là bộ đánh giá CMP-008 độc lập do người khác viết.

## Giới hạn của lát cắt cũ

- Chưa chọn thuật toán chia component (D-03). CLI cần `--membership`. Web không có membership thì mọi run kết thúc `failed/partition_policy_unavailable`; `--demo-partition` chia tạm theo thư mục để chạy thử.
- GitHub có code nhưng chưa qua Security review (API-002 §1) và chưa tải thật lần nào.
- Chưa tìm nhiều unit: API-003 §1 yêu cầu review quy tắc tìm root trước khi code.
- Chưa gọi provider thật. Bản ghi capability và free-only để trống, nên với `--llm` mọi tác vụ model dừng trước khi gửi (`PAID_ROUTE_DISABLED`).
- Rule `http-binding`, `config-binding` vẫn trả `RULE_UNSUPPORTED`.

## Chạy

Cài thư viện cần khi chạy: `python -m pip install -r slice/requirements.txt`. Thiếu `openapi-spec-validator` thì file API không được xuất.

### Giao diện sinh tài liệu FR-029

Giao diện mới nối trực tiếp agent của lệnh `document`. Nhận component và sơ đồ từ bước kiến trúc, không tự chia hoặc dựng lại.

Chạy thử offline, từ thư mục `slice`:

```powershell
python -m l3slice.docweb --workdir "$env:TEMP/l3-fr029-ui" --script demo/fr029.script.json --source tests/fixtures/fr029_e2e --membership tests/fixtures/fr029_e2e.membership.json
```

Mở `http://127.0.0.1:8001/`. Kịch bản chỉ dùng với fixture được điền sẵn; không gọi model, chỉ phát lại chế độ agent. Giao diện cho chạy, chọn cách đọc (agent hoặc đọc một lần, khi dùng model thật), xem trạng thái/độ phủ/giới hạn, xem `TAI-LIEU.md` dạng tài liệu (có nút xem văn bản gốc) và tải từng file.

Để dùng model thật, đặt khóa trong biến môi trường rồi khởi động server:

```powershell
python -m l3slice.docweb --workdir <thư-mục-kết-quả> --base-url <API-base-URL> --model <tên-model> --key-env <tên-biến-chứa-khóa>
```

`--base-url` là URL gốc API; provider nối thêm `/chat/completions`. Giao diện hiển thị nơi nhận source trước khi chạy. Có thể đặt `--max-turns`, `--max-tokens`, `--max-seconds` và `--max-output-tokens`.

Nhập đường dẫn tuyệt đối tới source và membership trên máy chạy server. `--workdir` phải nằm ngoài cây source. Mỗi lần chạy tạo thư mục riêng, không ghi đè kết quả cũ. Lịch sử UI chỉ tồn tại trong phiên server; file đã xuất vẫn nằm trên đĩa sau khi tắt. Không tắt server khi đang chạy; bản cơ bản chưa có tiếp tục/cancel hoặc tải ZIP/GitHub. Chỉ lắng nghe loopback.

Trạng thái “Đã xuất kết quả” không phải nghiệm thu. Agent, coverage và đối chiếu kiến trúc có trạng thái riêng; không có archdia/sơ đồ thì hiển thị giới hạn. [Kế hoạch hoàn thiện FR-029](../docs/FR029-ke-hoach-hoan-thien-yeu-cau.md) liệt kê phần còn phải làm.

Kiểm thử DOM tùy chọn (không thay kiểm bố cục trên trình duyệt), từ gốc repo, cần Node 22.13+ hoặc 24+:

```powershell
$uiTestRoot = Join-Path $env:TEMP 'l3-fr029-dom-test'
npm install --prefix $uiTestRoot --no-audit --no-fund jsdom@29.1.1
$env:L3_UI_JSDOM = Join-Path $uiTestRoot 'node_modules/jsdom'
$env:L3_UI_PYTHON = (Resolve-Path scripts/.venv/Scripts/python.exe).Path
node --test slice/tests/ui/docui.test.cjs
```

### CLI và giao diện lát cắt cũ

Cần Python 3.11 trở lên. Code chỉ dùng thư viện chuẩn. Test cần thêm thư viện ở `scripts/requirements-l3-check.txt`.

```powershell
cd slice
python -m l3slice analyze --source tests/fixtures/shop_full --output <thư mục mới> --membership tests/fixtures/shop_full.membership.json [--llm] [--json]
python -m l3slice retry --output <thư mục output> --artifact <artifact_id> [--json]
python -m l3slice document --source <repo> --output <thư mục mới> --membership <component.json> [--archdia <archdia.json>] [--diagram <sơ đồ.mmd>] --base-url <endpoint OpenAI-compatible> --model <tên> --key-env <BIẾN_MÔI_TRƯỜNG> [--mode agent|oneshot] [--checkpoint <file.json>] [--max-output-tokens <n>] [--json]
python -m l3slice.web --workdir <thư mục làm việc> --port 8000 [--demo-partition] [--enable-github] [--llm]
```

Mở UI tại `http://127.0.0.1:8000/`.

Lệnh `document` ghi `TAI-LIEU.md`: một file đọc chính cho người, gồm endpoint, model, bảng CSDL, sự kiện, cấu trúc code, gọi HTTP, thư viện, cấu hình, middleware và giới hạn. `--mode oneshot` gửi toàn bộ source trong một request, rồi tối đa 2 vòng sửa; cần `--max-output-tokens` đủ lớn (ví dụ 12000). Repo lớn hơn `--max-context-chars` thì dùng `--mode agent`.

Exit code của CLI:

| Code | Nghĩa |
|---|---|
| `0` | completed |
| `2` | lỗi đầu vào hoặc chỗ output |
| `3` | partial |
| `4` | engine không publish được hoặc lỗi nội bộ |
| `130` | người dùng ngắt |

CLI `analyze` của lát cắt cũ luôn trả `3`, vì inventory ghi giới hạn `SLICE_SCOPE`. `--json` in đúng một object `CliResult` ra stdout. Với `document`, exit `0` vẫn có thể chưa đối chiếu kiến trúc nếu thiếu đầu vào; cần đọc giới hạn trong kết quả.

Test, chạy từ gốc repo:

```powershell
python -m venv scripts/.venv
scripts/.venv/Scripts/python.exe -m pip install -r scripts/requirements-l3-check.txt
$env:PYTHONIOENCODING='utf-8'
scripts/.venv/Scripts/python.exe -m unittest discover -s slice/tests
```

Test validate output theo JSON Schema và OpenAPI nhúng trong contract, và chạy lại các kiểm tra bất biến của `scripts/check_l3_contracts.py`. Không test nào gọi mạng ngoài máy: GitHub dùng transport giả, provider dùng `FakeProvider`.

Golden (cần checkout `VSF-L3 Generator` có `evaluation/`):

```powershell
scripts/.venv/Scripts/python.exe slice/tools/run_golden.py --golden-root "D:/VSF/VSF-L3 Generator" --out <thư mục mới>
scripts/.venv/Scripts/python.exe slice/tools/d03_experiment.py --golden-root "D:/VSF/VSF-L3 Generator" --out <thư mục mới>
```

Hai công cụ từ chối tập held-out.

## Fixture

| Fixture | Nội dung |
|---|---|
| `shop_full` | App FastAPI, `GET /items` có `status_code=200`; SQLite; hai bảng đủ khóa và FK; `create_all` nối engine với `Base` |
| `shop_partial` | `APIRouter(prefix="/v1")`, prefix của app đọc từ `os.environ`; route không có status; không có `create_engine` |
| `events` | Hai nơi gửi và hai nơi nhận topic `order-created`, một số chỗ broker chưa rõ |
