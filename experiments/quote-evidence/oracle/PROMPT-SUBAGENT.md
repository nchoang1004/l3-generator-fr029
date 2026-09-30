# Viết đáp án cho repo mới bằng subagent

File này hướng dẫn giao việc viết đáp án (ground truth) cho một subagent chưa thấy kết quả chạy pipeline. Mục đích: repo kiểm kín thật sự kín.

## 1. Cách dùng

Trong Claude Code, ở thư mục gốc repo, gõ một câu như sau (thay phần trong ngoặc nhọn):

> Dùng subagent general-purpose. Prompt là nguyên văn mục 2 của `experiments/quote-evidence/oracle/PROMPT-SUBAGENT.md`, thay `<REPO_DIR>` = `sample-repos/<thư mục repo>`, `<OUT>` = `experiments/quote-evidence/oracle/<tên>.json`, `<SET>` = `held-out`. Chỉ báo lại cho tôi đường dẫn file và mục "điểm không chắc", không tóm tắt nội dung đáp án.

Sau khi subagent xong:

- Phiên chính **không mở** file đáp án của repo kín. Chỉ chạy pipeline và đọc điểm tổng (P, P khắt khe, R, trích dẫn hợp lệ, số khối).
- Khiêm (hoặc một subagent khác) xem đáp án trên trang sơ đồ (`scripts-2026-09-28/make_oracle_page.py`) nếu cần duyệt.
- Repo lộ (dùng để phát triển): repo dễ và 1 repo trung bình. Repo kín: repo khó, gồm cả repo mới.

Tiêu chí chọn repo mới: FastAPI, trên 150 file có nội dung, cấu trúc khác các repo đã có (ví dụ nhiều app con, plugin, DI container, nhiều hệ thống ngoài). Tải về `sample-repos/<owner>_<name>-<sha7>` trước khi giao việc.

## 2. Prompt (dán nguyên văn)

```text
Bạn viết đáp án (ground truth) cho sơ đồ component (C4 mức 2) của một repo Python/FastAPI.

Repo: <REPO_DIR>
File ra: <OUT>
Nhóm: <SET>

Đọc trước, đọc kỹ: experiments/quote-evidence/oracle/CHUAN-DAP-AN.md. Làm đúng 7 quy tắc, bảng cạnh bắt buộc, bảng xếp tầng và quy trình trong đó.

Giới hạn (bắt buộc):
- Chỉ đọc: mã nguồn trong <REPO_DIR>, file CHUAN-DAP-AN.md, và chạy experiments/quote-evidence/oracle/oracle_tool.py.
- Không đọc, không liệt kê: evaluation/, experiments/quote-evidence/runs, các file khác trong experiments/quote-evidence/oracle/ (kể cả rev1/), docs/, CLAUDE.md, thư mục memory.
- Không chạy pipeline (run.py), không gọi API AI nào.
- Không sửa file nào ngoài <OUT>.

Cách làm:
1. Tìm điểm vào (main.py, __main__.py, run/server, cli), file dựng app (FastAPI(), app factory, registrar), file gộp router (include_router).
2. Đi theo luồng: route -> service -> dữ liệu -> DB/hệ thống ngoài. Ghi các luồng phụ: CLI, admin, worker/tác vụ nền, plugin/extension, tool.
3. Viết components và shared theo chuẩn. Gộp khối cùng tầng, cùng cơ chế. Mục tiêu khoảng 10-20 khối không dùng chung.
4. Chạy: python experiments/quote-evidence/oracle/oracle_tool.py <REPO_DIR> <OUT>
   Đọc danh sách file ngoài khối và danh sách cạnh import kèm dòng code.
5. Chọn cạnh bắt buộc. Với mỗi cạnh, mở đúng file và dòng để xác nhận, ghi "file:dòng đoạn code".
6. Thêm cạnh tới hệ thống ngoài từ dòng tạo kết nối (engine/client/URL/host/SMTP/broker).
7. Xếp mỗi khối không dùng chung vào một tầng (layers), mỗi khối một dòng bằng chứng. Cạnh bắt buộc đi lên tầng trên chuyển sang "up".
8. Chạy lại với --finalize. Dòng "required without import", "no layer" và "upward" phải trống, hoặc có lý do trong note.
9. Dùng python có sẵn: .audit-output/python-3.14.7/python.exe -B, đặt PYTHONIOENCODING=utf-8.

Trả lời ngắn khi xong:
- Đường dẫn file đã viết.
- Số khối, số khối dùng chung, số cạnh bắt buộc, số cạnh không qua import.
- Điểm không chắc: tối đa 5 dòng, mỗi dòng một chỗ bạn phải chọn giữa hai cách chia hoặc hai cách hiểu, kèm file:dòng.
Không kể lại toàn bộ đáp án.
```

## 3. Vì sao làm như vậy

- Subagent bắt đầu với ngữ cảnh trống, nên không biết pipeline đã sai ở đâu.
- Giới hạn chỉ là lời dặn, không phải khóa thật. Vì vậy phiên chính cũng không mở đáp án kín, để hai phía không lộ cho nhau.
- `oracle_tool.py` lấy cạnh từ import thật, nên người viết chỉ chọn cạnh chứ không bịa cạnh.

## 4. Nâng đáp án có sẵn từ bản 2 lên bản 3 (dán nguyên văn)

Dùng cho 8 đáp án đã có. Khối giữ nguyên; thêm tầng và chuyển một số cạnh bắt buộc sang `pass`, `check`, `up`. Thay `<REPO_DIR>` và `<OUT>` như mục 1. Bản 2 đã chép ở `oracle/rev2/`. fba làm ngày 28/09 bằng bản đầu của prompt này (chưa có `check`, `up`), rồi sửa bổ sung.

```text
Bạn nâng đáp án (ground truth) sơ đồ component của một repo Python/FastAPI từ chuẩn bản 2 lên bản 3. Chỉ sửa: thêm tầng cho từng khối, và chuyển một số cạnh bắt buộc sang "chấp nhận được" với nhãn pass, check, up. Không chia lại khối.

Repo: <REPO_DIR>
File đáp án (sửa tại chỗ): <OUT>

Đọc trước, đọc kỹ: experiments/quote-evidence/oracle/CHUAN-DAP-AN.md (bản 3). Chú ý quy tắc 6 và 7, bảng mục 2 (nhãn "pass", "check", "up"), mục 3 (xếp tầng; worker nhận việc từ service ở tầng service, vòng nền tự chạy ở entry), mục 4 (định dạng JSON).

Giới hạn (bắt buộc):
- Chỉ đọc: mã nguồn trong thư mục repo trên, file CHUAN-DAP-AN.md, file đáp án trên, và chạy experiments/quote-evidence/oracle/oracle_tool.py.
- Không đọc, không liệt kê: evaluation/, experiments/quote-evidence/runs, các file khác trong experiments/quote-evidence/oracle/ (kể cả rev1/, rev2/), docs/, CLAUDE.md, thư mục memory.
- Không chạy pipeline (run.py), không gọi API AI nào.
- Không sửa file nào ngoài file đáp án trên.

Việc cần làm:
1. Giữ nguyên "components", "shared", "externals", và mọi cạnh bắt buộc không thuộc bước 3–5.
2. Thêm "layers": mỗi khối không dùng chung thuộc đúng một tầng (entry, api, service, data, infra) theo bảng mục 3. Mỗi khối kèm một dòng bằng chứng "file:dòng đoạn code"; mở đúng file và dòng để xác nhận đoạn code khớp nguyên văn. Khối có dấu hiệu của nhiều tầng thì lấy tầng đứng trên trong bảng. Tầng service lấy bằng chứng là dòng một khối tầng trên gọi nó. Worker tác vụ nền xếp service.
3. Xét từng cạnh bắt buộc có lý do là lấy session DB hoặc client Redis/cache. Mở code của khối nguồn: nếu khối nguồn gọi method trên session/client (execute, commit, get, set...), giữ là bắt buộc. Nếu khối nguồn chỉ nhận (qua Depends, tham số) hoặc tự mở (async with async_db_session() as db) rồi truyền cho khối khác, không gọi method nào trên nó, chuyển cạnh sang "acceptable" dạng ["<nguồn>", "<đích>", "pass", "<file>:<dòng> <đoạn code>"] và bỏ khỏi "required".
4. Xét từng cạnh bắt buộc có lý do là kiểm tra rồi quay về: kiểm token, quyền, session, captcha và dạng tương tự (dependency xác thực, decorator khóa API, jwt_authentication). Chuyển sang "acceptable" nhãn "check" kèm file:dòng.
5. Sau khi xếp tầng: cạnh bắt buộc nào đi từ tầng dưới lên tầng trên (thứ tự entry, api, service, data, infra) thì chuyển sang "acceptable" nhãn "up", giữ file:dòng.
6. Đặt "rev": 3. Thêm vào đầu "written" dòng "<ngày> bản 3: thêm layers, cạnh pass, check, up". Thêm vào "note" các chỗ phải chọn giữa hai tầng, kèm lý do.
7. Chạy từ thư mục gốc repo, trong Git Bash:
   PYTHONIOENCODING=utf-8 .audit-output/python-3.14.7/python.exe -B experiments/quote-evidence/oracle/oracle_tool.py <REPO_DIR> <OUT> --finalize
   Dòng "no layer" và "upward" phải không xuất hiện. Dòng "required without import" chỉ được còn những cạnh đã có từ trước.

Nếu thấy chỗ nào trong đáp án có vẻ sai ngoài hai việc trên (khối, cạnh khác), không sửa; chỉ ghi vào câu trả lời.

Trả lời ngắn khi xong:
- Số khối theo từng tầng (ví dụ entry 3, api 4...).
- Số cạnh chuyển sang "pass", "check", "up"; số cạnh bắt buộc còn lại.
- Điểm không chắc: tối đa 5 dòng, mỗi dòng một chỗ phải chọn giữa hai tầng hoặc giữa bắt buộc/pass/check, kèm file:dòng.
- Chỗ nghi sai khác (nếu có): tối đa 3 dòng.
Không kể lại toàn bộ đáp án.
```
