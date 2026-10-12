# Hướng dẫn demo L3 Generator (FR-029/030/031) — 12/10/2026

File này nói cách demo chương trình trong khoảng 10 phút, không tốn tiền API. Mô tả đầy đủ chương trình ở [L3-Generator-chuong-trinh-hien-tai.md](L3-Generator-chuong-trinh-hien-tai.md).

## 1. Chuẩn bị (một lần)

Chạy từ thư mục gốc repo, PowerShell:

```powershell
scripts/.venv/Scripts/python.exe -m pip install -r slice/requirements.txt
scripts/.venv/Scripts/python.exe -m unittest discover -s slice/tests
```

Kết quả mong đợi: 521 test, 1 lỗi `test_gateway` có từ trước. Lần chạy 12/10: 520/521.

## 2. Ba cách demo

| Cách | Cho thấy | Tốn tiền | Thời gian |
|---|---|---|---|
| A. Giao diện web, kịch bản offline | Luồng chạy: nhập đầu vào → agent đọc → kết quả, độ phủ, giới hạn | Không | 3 phút |
| B. Mở `TAI-LIEU.md` có sẵn của repo thật | Chất lượng tài liệu sinh ra | Không | 5 phút |
| C. CLI với model thật | Model thật đọc repo | Có, ~0,2 USD/repo nhỏ với gpt-5 | 5–10 phút |

Nên demo A rồi B. Chỉ làm C khi đã duyệt tiền.

## 3. Cách A — giao diện web, không gọi model

Từ thư mục `slice`:

```powershell
../scripts/.venv/Scripts/python.exe -m l3slice.docweb --workdir "$env:TEMP/l3-demo" --script demo/fr029.script.json --source tests/fixtures/fr029_e2e --membership tests/fixtures/fr029_e2e.membership.json
```

Mở `http://127.0.0.1:8001/`.

1. Hai ô source và membership đã điền sẵn. Đánh dấu ô đồng ý, bấm **Sinh tài liệu**.
2. Trạng thái chạy, rồi "Đã xuất kết quả". Agent: completed, 4 lượt.
3. `TAI-LIEU.md` tự mở khi chạy xong. Danh sách tài liệu chia nhóm: Đọc chính, API, Cho máy đọc.
4. Mở "Giới hạn" và "Chi tiết độ phủ đọc": mọi file đã đọc hết.

Nói rõ khi demo: "Kịch bản offline phát lại câu trả lời đã ghi sẵn của agent trên một repo nhỏ. Bộ kiểm và phần xuất tài liệu chạy thật."

Giới hạn của giao diện hiện tại:
- Kịch bản offline chỉ phát lại chế độ `agent`; ô "Đọc một lần" bị khóa. Với model thật (`--base-url`, `--model`, `--key-env`) ô này dùng được; phần này mới test bằng mock.
- Xem tài liệu dạng Markdown (bảng, tiêu đề). Nút "Xem văn bản gốc" cho bản chưa dựng.

## 4. Cách B — tài liệu thật đã sinh

| Repo | File | Ghi chú |
|---|---|---|
| Teamhide (5 route) | `ket-qua-chay/tai-lieu-mau-teamhide-20261011/output/TAI-LIEU.md` | Dựng lại offline từ câu trả lời gpt-5 ngày 11/10 |
| orderflow-services (4 service, 23 route) | `ket-qua-chay/heldout-orderflow-20261012/after-fix/out2/TAI-LIEU.md` | Repo chưa dùng khi phát triển; agent Claude đóng vai model |
| 4 repo có bảng CSDL | `ket-qua-chay/db-check-20261012/final/<repo>/TAI-LIEU.md` | Mục 4 (bảng CSDL) đã qua 2 vòng giám khảo |

Mở bằng VS Code, nhấn `Ctrl+Shift+V` để xem bảng.

Nên chỉ vào:
- Mục 1–2: mỗi endpoint có method, path đủ prefix, tham số, body, response, mã lỗi, `file:dòng`.
- Nhãn **chắc chắn / suy luận / chưa rõ / AI viết**: chỗ nào không chắc thì nói không chắc.
- Mục 4: bảng CSDL có khóa chính, khóa ngoại, ràng buộc; dấu `*` là giá trị mặc định của ORM.
- Mục 11: giới hạn. Ví dụ orderflow ghi rõ có Redis pub/sub nhưng chưa đọc được.

## 5. Cách C — model thật (tốn tiền)

```powershell
cd slice
../scripts/.venv/Scripts/python.exe -m l3slice document --source <repo> --output <thư-mục-mới> --membership <component.json> --base-url https://api.openai.com/v1 --model gpt-5 --key-env <BIẾN_CHỨA_KHÓA> --mode oneshot --max-output-tokens 12000 --checkpoint <file.json>
```

- Khóa đặt trong biến môi trường; không dán khóa vào lệnh.
- `--checkpoint`: dừng giữa chừng thì chạy lại cùng lệnh để làm tiếp, không trả tiền lại phần đã xong.
- Prompt hiện tại (oneshot v6, agent v17) **chưa chạy với model thật**. Lần đo thật gần nhất dùng prompt v3–v4.

## 6. Số đo nói khi demo

Chỉ nói các số đã đo. Ghi rõ cách đo.

| Phần | Số đo | Cách đo |
|---|---|---|
| API (route, model) | orderflow: route 23/23, model 9/9 | Gold có sẵn; agent Claude đóng vai model |
| API với model thật | Teamhide: gpt-5 4/5 route, 0,168 USD | 11/10, prompt v4 |
| Bảng CSDL | 32/32 bảng, 341/341 cột, khóa chính, khóa ngoại | Gold 4 repo |
| Giám khảo độc lập | orderflow 202/213 mục đúng; CSDL 285/287 cột | Agent Claude Sonnet, đầu ra đóng băng trước khi chấm |
| Dễ đọc | 3/5 (repo lớn), ~4/5 (repo nhỏ) | Giám khảo chấm |
| Test | 520/521 | Lỗi `test_gateway` có từ trước |

## 7. Điều phải nói thật

- Chưa nghiệm thu bằng model thật với prompt hiện tại.
- Giám khảo và agent đóng vai model đều là Claude; có thể thiên vị cùng họ model.
- Phần bảng, sự kiện, thư viện, cấu hình đọc tĩnh bằng code, không qua model. Quyết định này chưa duyệt (OQ-L3GEN-019).
- `TAI-LIEU.md` và các mục lỗi trả về, tags, ví dụ chưa có trong FR (OQ-L3GEN-020).
- Chưa đối chiếu với `archdia.json` (AC-030-05, AC-031-04 hoãn).
- Chế độ oneshot chưa chia gói cho repo lớn: source vượt `--max-context-chars` thì báo `SOURCE_TOO_LARGE`; khi đó dùng `--mode agent`.
