# quote-evidence: từ repo ra sơ đồ component có trích dẫn

Cập nhật 28/09/2026 (v6). Mục này mô tả pipeline dựng sơ đồ component (mức C4-2) cho một repo Python bất kỳ.

- AI đọc các dòng code do code chọn.
- Mọi phát biểu của AI kèm trích dẫn `file:dòng`, và code kiểm trích dẫn đó khớp nguyên văn với source.
- Cạnh giữa các khối do code vẽ, không do AI.
- Không có luật riêng cho framework hay cho repo nào.

## Ai làm gì (v6)

| Bước | Ai làm | Evidence |
|---|---|---|
| Snapshot, chỉ mục ký hiệu và import | Code (`inventory.py`, `pyindex.py`) | sha256 từng file |
| Chia file thành khối, đánh dấu "dùng chung" | AI (bước 1, một request) | Không có trích dẫn |
| File AI bỏ sót | Code: `__init__.py` vào khối cùng thư mục; file khác thành khối theo thư mục; ghi vào danh sách vấn đề | — |
| Kiểm khối trộn lớp (khối trải trên ≥2 thư mục con import lẫn nhau) | Code báo, AI sửa một lượt: tách, hoặc giữ kèm lý do | Lý do ghi ở `graph.json` → `meta.review` |
| Cạnh giữa các khối | Code, theo quy tắc: mọi quan hệ import giữa hai khối, trừ khối dùng chung | Dòng dùng import ở phía nguồn và dòng định nghĩa ở phía đích, cả hai do code lấy |
| Nhãn cạnh | Code, từ cách dùng: "gọi X", "đăng ký qua X", "dùng kiểu X"... | Như trên |
| Tên, vai trò khối | AI (bước 2, lô ≤ 3 khối) | Trích dẫn một dòng; code kiểm khớp nguyên văn |
| Hệ thống ngoài (DB, SMTP, API...) | AI (bước 2) | Phải trích đúng một "dòng kết nối" do code chọn |

**Vì sao cạnh do code vẽ:** trên nhóm repo kiểm, AI phân loại cạnh không thắng quy tắc đơn giản. Ví dụ ở rhoboro, recall là 0,71 khi AI phân loại, so với 1,00 khi dùng quy tắc. Bỏ phần cạnh khỏi AI còn làm prompt ngắn một nửa và giảm 37% token của bước mô tả.

## Chạy

```bash
export PYTHONIOENCODING=utf-8
PY=.audit-output/python-3.14.7/python.exe
$PY -B experiments/quote-evidence/run.py <repo> --dry-run                     # ước lượng token, không gọi AI
$PY -B experiments/quote-evidence/run.py <repo> --out <thư mục mới> --budget <trần token> [--oracle experiments/quote-evidence/oracle/<repo>.json]
$PY -B experiments/quote-evidence/test_quote_evidence.py                     # test offline
```

Output gồm 3 file: `diagram.mmd`, `README.md` (bảng trích dẫn đặt cạnh từng phát biểu, kèm thời gian và token) và `graph.json`. Nếu có đáp án thì thêm `score.json`. Sổ token và cache ở `evaluation/quote-evidence/`. Model đang dùng là Groq `openai/gpt-oss-120b`.

## Số đo (28/09/2026)

Đáp án ở `oracle/`, bản 2, **chỉ luồng xử lý** (chuẩn: `oracle/CHUAN-DAP-AN.md`; bản 1 ở `oracle/rev1/`). Cách chấm ghi ở đầu `evaluate.py`:
- Cạnh `required` (luồng xử lý) bị thiếu thì mất recall.
- Cạnh `acceptable` (gồm cạnh lắp ráp `wiring`) không tính ở P, nhưng tính sai ở P khắt khe.
- Cạnh vẽ khác đều tính là sai.

Cạnh nội bộ, các lần chạy đã có, chấm lại theo đáp án bản 2:

| Repo | File | Lần chạy | P / P khắt khe / R |
|---|---:|---|---|
| rhoboro | 15 | `v4-rhoboro` | 1,00 / 1,00 / 1,00 |
| teamhide | 54 | `v3-teamhide` | 0,69 / 0,69 / 0,69 |
| igorbenav boilerplate | 99 | `v3-boilerplate` | 1,00 / 0,74 / 1,00 |
| lnbits | 170 | `v5-lnbits` | 0,42 / 0,26 / 0,50 |
| fba | 226 | `v6-fba` | 0,36 / 0,30 / 0,43 |

Trích dẫn hợp lệ 96–100%. Thời gian 1–25 phút mỗi repo, phần lớn là chờ giới hạn 8k token/phút của Groq miễn phí. Chi tiết và các repo khác: `docs/HANDOFF.md`, mục 4.

## Giới hạn

- **Chia khối ở repo lớn chưa ổn.** Danh sách thư mục gửi AI bị rút gọn khi repo lớn, nên AI bịa đường dẫn, bỏ sót file (fba: 114/226 file không được xếp khối), và đặt cờ "dùng chung" sai.
- **Pipeline vẽ mọi cạnh import**, gồm cả cạnh lắp ráp (container DI, khởi động) và cạnh chỉ dùng kiểu. Đáp án chỉ tính luồng xử lý, nên P khắt khe thấp. Thiết kế sửa ở `docs/HANDOFF.md`, mục 6; chưa làm.
- Cạnh chỉ lấy từ import đã phân giải, nên không thấy plugin nạp theo tên hay pool lấy qua `request.app.state`.
- Chỉ có bộ lập chỉ mục Python.
- Trích dẫn khớp chỉ chứng minh dòng code tồn tại, không chứng minh câu mô tả đúng nghĩa.
- 8 đáp án hiện tại do chính phiên phát triển viết. Repo kín mới cần subagent viết (`oracle/PROMPT-SUBAGENT.md`).
