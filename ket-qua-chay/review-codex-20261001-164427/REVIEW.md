# Review code L3 — 01/10/2026

## Kết luận

Đã có một bản thử nghiệm hoạt động qua CLI khi cung cấp membership. Chưa đủ điều kiện nghiệm thu chức năng sinh tài liệu hoặc toàn hệ thống. 116 test hiện có pass, nhưng các ca bổ sung tái hiện lỗi về bảo mật, kiểm dữ liệu, xử lý lỗi và nội dung OpenAPI. Không quy đổi số test thành phần trăm hoàn thành.

Review trên working tree `D:/VSF/l3-generator-l3`, HEAD `5d06f14`. Code mới chưa commit: HEAD không định danh được code đã kiểm. `source-hashes.json` ghi hash các file code/test/contract hiện tại. Không sửa code sản phẩm, không chạy held-out, không gọi provider LLM, không chọn D-03.

## Đã chạy và đối chiếu

| Kiểm tra | Kết quả |
|---|---|
| `scripts/.venv/Scripts/python.exe -m unittest discover -s slice/tests -v` | 116 test, 10,186 giây, OK |
| `scripts/check_l3_contracts.py` | 8 contract, 7 JSON Schema, 136 refs, 70 links, 20 ca dương, 31 ca âm; pass |
| `slice/tools/run_golden.py` trên development | 38 case; số đếm khớp báo cáo |
| `slice/tools/d03_experiment.py` | 7 case; A/B khớp báo cáo; C not_run |
| CLI `shop_full` với membership fixture | Exit 3, sáu artifact ready, gồm SVG và API/TBL |
| Hash artifact đã lưu của demo và ba case CLI | Khớp manifest ở cả bốn bundle |
| `probes.py` | Tái hiện các lỗi bên dưới; dùng dữ liệu tự tạo, không thực thi source đầu vào |

Golden development: route 61/0/0; reference 84/0/1; entity 18/0/4; entity_columns 108/0/0; limitation 2/0/0 (TP/FP/FN). Đây là số đo bộ trích qua adapter, không phải số đo toàn pipeline hoặc độ đúng mọi thuộc tính tài liệu. Gold vẫn candidate, chưa hoàn tất human review.

Kết quả lưu tại `golden-dev/`, `d03/`, `cli-demo/`, `probes.json`, `saved-artifact-hash-check.json`. Chỉ chạy lại một demo CLI trong review này; ba case CLI cũ được kiểm hash, không tuyên bố đã chạy lại cả ba.

## Lỗi đã tái hiện, cần sửa

### 1. P1 — Giá trị bí mật trong URL cấu hình lọt vào output và qua bộ che dữ liệu

- Code: `slice/l3slice/extract.py:961`, `slice/l3slice/gateway.py:50`.
- Input tự tạo: `BaseSettings.DATABASE_URL` chứa URL PostgreSQL có user/password giả.
- Kết quả: password giả còn nguyên trong `result.json`; `gateway.mask_obj` cũng không che.
- Nguyên nhân: extractor chủ yếu kiểm tên khóa bằng regex; `DATABASE_URL` không khớp. Bộ che không xử lý credential trong URL.
- Hệ quả: artifact có thể lộ credential. Khi bật provider, cùng dữ liệu có nguy cơ đi ra ngoài. Review không gửi request mạng và không dùng khóa thật.
- Sửa: che userinfo/query nhạy cảm trong URL ngay khi lập fact và trước egress; giữ lý do redacted. Thêm ca URL, DSN, nested JSON và assertion marker không xuất hiện trong artifact/payload/log.

### 2. P1 — Verifier và bước xuất chưa chặn dữ liệu sai kiểu/ngữ nghĩa

- Code: `slice/l3slice/verify.py:47`, `slice/l3slice/render.py:221`.
- Source có `status_code=200`. Probe đổi fact thành `[20]` nhưng giữ evidence gốc.
- Kết quả: verifier vẫn giữ `known [20]`; file API và JSON vẫn được publish `ready`.
- Nguyên nhân: phép kiểm chuỗi `20 in 200` pass; không có kiểm runtime bắt buộc status trong 100–599 trước publish.
- Sửa: so giá trị đã parse và vai trò AST thay vì substring; kiểm kiểu, miền giá trị và liên kết ID của typed attributes. Validate khối OpenAPI/DDL/JSON Schema thực sự trước ghi trạng thái ready.
- Đây là ca tiêm dữ liệu sai để kiểm hàng rào xác minh, không phải khẳng định extractor bình thường tự biến 200 thành 20.

### 3. P1 — Bộ kiểm tài liệu bỏ sót sai giá trị khi ID vẫn đúng

- Code: `slice/l3slice/render.py:529`.
- Probe đổi status trong bảng Markdown từ 200 sang 404, giữ OpenAPI và ID nguyên vẹn.
- Kết quả: `check_doc` trả `None` (không lỗi).
- Nguyên nhân: kiểm rows/machine/omitted đang đối chiếu ID, chưa đối chiếu giá trị từng trường.
- Sửa: đọc lại thuộc tính ở bảng và khối máy rồi so với bản dữ kiện chuẩn. Bổ sung mutation test đổi method/path/status/nullable/FK/payload mà không đổi ID.
- Điều kiện “đổi sai một trường trong output thì checker báo lỗi” của kế hoạch hiện chưa đạt.

### 4. P1 — Manifest sai kiểu làm run mắc ở running và có thể dừng worker

- Code: `slice/l3slice/extract.py:983`, `slice/l3slice/engine.py:135`, `slice/l3slice/engine.py:173`.
- ZIP thử nghiệm chứa TOML hợp cú pháp nhưng sai cấu trúc: `[project] dependencies = 1`.
- Kết quả: `TypeError: 'int' object is not iterable`; run còn `running/extraction`.
- `serve_forever` không bắt exception này quanh `step`, nên lỗi có thể kết thúc worker, ảnh hưởng run xếp hàng tiếp theo.
- Sửa: kiểm cấu trúc manifest, ghi limitation phù hợp; thêm ranh giới xử lý lỗi cuối của mỗi run để luôn chuyển trạng thái terminal, dọn dữ liệu và tiếp tục phục vụ hàng đợi.

### 5. P2 — Cùng repo qua local và ZIP có phạm vi khác nhau

- Code: `slice/l3slice/snapshot.py:37`, `slice/l3slice/snapshot.py:71`.
- Input có `main.py` và `.venv/dependency.py`.
- Local bỏ `.venv`; ZIP đưa `.venv/dependency.py` vào snapshot. Snapshot ID khác nhau.
- Sửa: dùng chung chính sách chọn/bỏ file, công bố excluded nhất quán. Test parity cho `.venv`, `node_modules`, `.git`, Unicode và manifest; không chỉ test repo sạch.

### 6. P2 — OpenAPI làm body tùy chọn thành bắt buộc

- Code: `slice/l3slice/extract.py:575`, `slice/l3slice/render.py:241`.
- Input: handler có `item: Item = None`.
- Output: `requestBody.required = true`.
- Nguyên nhân: dữ kiện body không giữ required; renderer gán cứng true.
- Sửa: giữ trạng thái required và bằng chứng trong contract/body fact; renderer chỉ xuất true/false khi đã biết, phần chưa biết phải có notice. Đồng bộ contract trước nếu cần thêm trường.

### 7. P2 — Mất nullable của phần tử collection

- Code: `slice/l3slice/extract.py:357`.
- Input: `values: list[int | None]`.
- Output: items chỉ có `type: integer`, không có nhánh null; trường được coi là known.
- Sửa: bảo toàn schema của kiểu lồng nhau; phân biệt nullable của mảng và nullable của phần tử. Kiểm cả list/tuple/dict/union và nested model; không hỗ trợ thì unknown có lý do.

## Số đo và báo cáo cần diễn giải lại

1. `golden_adapter.py:64` chủ động chuẩn hóa route thành `confidence=exact`, completeness theo riêng path. Probe có route sản phẩm `inferred/partial` nhưng prediction thành `exact/full`. Đây có thể là projection để so các trường route đã gán nhãn; phải công bố phạm vi. `false_exact=0` sau adapter không chứng minh nhãn của toàn bộ sản phẩm đúng. Cần phép đo riêng giữ nguyên nhãn sản phẩm, hoặc đặt tên chỉ số thể hiện rõ projection.
2. `run_golden.py` gọi snapshot → extract → adapter → scorer; không chạy model, verifier, renderer. Route 61/0/0 không chứng minh requestBody, nullable, OpenAPI, SVG, LLM hay edge binding đúng.
3. Câu “đã code đủ 10 đợt” mâu thuẫn với phần còn thiếu. Nên ghi “đã có code và test cho nhiều phần của Đợt 0–10; một số đợt mới một phần hoặc bị chặn”. Đợt 0–10 thực tế có 11 mục.
4. Báo cáo §7 nói kết quả chỉ trong thư mục tạm đã lỗi thời: hiện có `ket-qua-chay/` với các artifact kiểm được hash.
5. Report ghi 4 FN entity đều là tên tính lúc import cần tách theo từng case. Summary chạy lại có 2 FN ở `netflix-dispatch` và 2 ở `orders-fixture`; không nên diễn đạt như cả bốn đều từ Dispatch.

## Phần chưa thể nghiệm thu

- D-03 chưa chọn; membership còn fixture; `group_flat` chưa nối pipeline.
- Web mặc định không có partition policy nên run thất bại; GitHub chưa tải được.
- Chưa có multi-unit, HTTP/config binding, trần 30 phút/2 GiB, CLI đầy đủ.
- Provider thật chưa chạy. Hiện preflight khóa egress; không lấy provider giả làm bằng chứng tích hợp thật.
- Gold chưa review, held-out chưa chạy; không công bố tỷ lệ nghiệm thu từ tập development.
- Bộ test hiện có có giá trị hồi quy, nhưng chưa đủ kiểm chất lượng trên repo tổng quát.

## Thứ tự xử lý đề nghị

1. Sửa lộ credential, worker mắc trạng thái, semantic validation và checker tài liệu.
2. Sửa body/nullable và chính sách local/ZIP; biến các probe thành regression test có assertion.
3. Làm một luồng API/TBL/EVT thật từ source → facts → verify → output, review thủ công các thuộc tính đã chọn trước.
4. Giữ D-03 mở cho tới khi có quyết định; các sửa lỗi trên không cần chọn thuật toán.
5. Hoàn thiện tích hợp/provider/budget theo phạm vi đã duyệt, rồi nghiệm thu bằng gold đã review và tập đo phù hợp OBS.

## Chạy lại probe

Từ gốc checkout:

```powershell
$env:PYTHONIOENCODING='utf-8'
scripts/.venv/Scripts/python.exe ket-qua-chay/review-codex-20261001-164427/probes.py
```

Probe tạo input giả trong thư mục tạm, ghi `probes.json` tại đây; không sửa source sản phẩm. Các giá trị có chữ password trong probe là marker giả. Probe ghi quan sát, không phải bộ test pass/fail nghiệm thu và không đóng các finding.
