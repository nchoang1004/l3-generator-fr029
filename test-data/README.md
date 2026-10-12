# Dữ liệu test: repo ngoài và đáp án (gold)

Thư mục này chứa các repo mã nguồn mở dùng để chạy và đo chương trình, cùng file đáp án. Mỗi repo giữ giấy phép riêng của nó; không phải code của dự án này.

Chỉ chép file nhỏ hơn 1 MB và bỏ `.git`, `node_modules`, ảnh, video, font, file nén. Công cụ chỉ đọc file mã và cấu hình nên không ảnh hưởng. `_copy-report.json` ghi số file từng thư mục và đường dẫn gốc.

| Thư mục | Dùng cho |
|---|---|
| `acceptance-repos/` | 4 repo đo nghiệm thu FR-029 (tdd-docker, AgentGPT...) |
| `acceptance-gold/` | Đáp án và membership của các repo trên |
| `heldout-repos/`, `heldout-repos2/`, `heldout-repos3/`, `heldout-repos4/` | Repo chưa dùng khi chỉnh bộ kiểm (nsidnev realworld, orderflow, caura...) |
| `heldout-gold2/` | Đáp án viết cho repo held-out đợt 2 |
| `sample-repos/` | Repo mẫu khác (Teamhide...) |

## Đường dẫn trong các file kết quả

Nhiều file trong `ket-qua-chay/` và `.aide/` ghi đường dẫn tuyệt đối của máy gốc, ví dụ `D:/VSF/l3-heldout-repos/...`. Khi chạy lại trên máy khác, đổi sang đường dẫn tới thư mục tương ứng ở đây. Bảng đổi:

| Đường dẫn gốc | Thư mục ở đây |
|---|---|
| `D:/VSF/l3-acceptance-repos` | `test-data/acceptance-repos` |
| `D:/VSF/l3-acceptance-gold` | `test-data/acceptance-gold` |
| `D:/VSF/l3-heldout-repos`, `...repos2`, `...repos3`, `...repos4` | `test-data/heldout-repos`, `...repos2`, `...repos3`, `...repos4` |
| `D:/VSF/l3-heldout-gold2` | `test-data/heldout-gold2` |
| `D:/VSF/l3-generator-quote-evidence/sample-repos` | `test-data/sample-repos` |

## Ví dụ chạy giao diện với model thật trên repo vừa

```powershell
cd slice
$env:OPENAI_API_KEY = "<khóa của bạn>"
python -m l3slice.docweb --workdir "$env:TEMP/l3-out" --port 8001 `
  --base-url https://api.openai.com/v1 --model gpt-5-2025-08-07 --key-env OPENAI_API_KEY `
  --max-output-tokens 20000 --reasoning-effort low --timeout 900 `
  --prices 1.25,0.125,10 --max-cost-usd 0.35 --max-tokens 400000 --max-seconds 1200 `
  --source ../test-data/heldout-repos/nsidnev_fastapi-realworld-example-app `
  --membership ../ket-qua-chay/8-repo-khiem/membership-realworld.json
```

Mở `http://127.0.0.1:8001/`, chọn **Đọc một lần**. Lần chạy thật 12/10 tốn khoảng 0,46 USD.

## File đã bỏ

Các file `.env` thật của repo ngoài (liệt kê ở `_omitted-env-files.txt`) không được chép, để tránh đưa khóa lên git. File `.env.example` vẫn còn.
