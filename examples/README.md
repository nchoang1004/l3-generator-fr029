# Kết quả đã chạy sẵn

Xem kết quả thật trong 30 giây — không cần cài gì, không cần API key, không cần mạng.

Cả hai bộ chạy bằng `l3gen 0.1.0` với `--no-ai`, ngày 15/09/2026.

---

## Hai bộ ví dụ

| Thư mục | Repo | Quy mô | Thời gian chạy |
|---|---|---|---|
| [`full-stack-fastapi-template/`](full-stack-fastapi-template/) | `fastapi/full-stack-fastapi-template` @ `cb740b6` | 25 file, 1.487 dòng | 0,04 giây |
| [`netflix-dispatch/`](netflix-dispatch/) | `Netflix/dispatch` @ `dd2837e` | 657 file, 73.301 dòng | 1,85 giây |

Bắt đầu bằng [`full-stack-fastapi-template/L3.md`](full-stack-fastapi-template/L3.md) —
nhỏ, đọc hết được.

---

## Mỗi bộ có gì

| File | `template` | `dispatch` |
|---|---|---|
| `L3.md` — tài liệu chính | có | có |
| `diagram.mmd` — sơ đồ Mermaid | có | có |
| `findings.json` — cảnh báo | có | có |
| `graph.json` — node và cạnh | có | **không** |
| `IAM.json` — toàn bộ dữ liệu đọc từ code | có | **không** |

Hai file JSON của `dispatch` nặng 11 MB nên không commit. Sinh lại:

```bash
git clone https://github.com/Netflix/dispatch && cd dispatch && git checkout dd2837e
l3gen . --no-ai -o out
```

---

## Ba chỗ đáng xem

**1. Công cụ không đoán giá trị lúc chạy.** Mở
[`full-stack-fastapi-template/L3.md`](full-stack-fastapi-template/L3.md) mục 2. Đường
dẫn ghi `/{settings.API_V1_STR}/items/` chứ không phải `/api/v1/items/`. Giá trị thật
chỉ biết khi chạy chương trình, nên công cụ giữ nguyên biểu thức và hạ nhãn xuống
`partial` kèm lý do.

**2. File hỏng không kéo sập cả lượt chạy.** Cùng file đó, mục 9. Repo template có một
lỗi cú pháp thật ở `app/api/deps.py:36` — dùng cú pháp `except A, B:` của Python 2.
Công cụ báo đúng vị trí, bỏ qua riêng file đó, vẫn đọc 24 file còn lại và tìm đủ 23/23
route.

**3. Công cụ tự nói chỗ nào của nó chưa đầy đủ.** Mục 9 của cả hai file.

Với `dispatch`: liệt kê thẳng 75 lớp mà tên bảng **chưa đọc được** — các lớp này không
khai `__tablename__`, lớp cơ sở của repo tự sinh tên lúc chạy. Cột *Bảng* ở mục 3 ghi
*chưa đọc được* thay vì đoán một cái tên nghe hợp lý nhưng sai.

Với `template`: nêu rõ `POST /private/users/` chỉ tồn tại khi
`settings.FASTAPI_ENV == 'development'`. Route này có thật trong code nhưng không có
trên môi trường production.

---

## Tự kiểm chứng

Mọi dòng trong `L3.md` đều có cột *Vị trí* dạng `file:dòng`. Clone repo gốc, mở đúng
dòng đó, đối chiếu.

Chạy hai lần cho ra kết quả giống hệt từng byte — `IAM.json`, `graph.json`,
`diagram.mmd`, `findings.json`. Riêng `L3.md` khác hai chỗ cố ý: dòng thời điểm chạy
ở đầu file, và con số thời lượng chạy ở mục 1.
