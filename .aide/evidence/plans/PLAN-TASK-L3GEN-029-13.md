# PLAN-TASK-L3GEN-029-13 — r1

Viết ngày 12/10/2026, **trước khi sửa code giao diện** (EXEC §B.14). Chưa phải approval.

## 0. Chặn

CLAUDE.md yêu cầu nạp skill `taste-skill` trước mọi việc giao diện. Ngày 12/10 skill chưa cài (`~/.claude/skills/taste-skill/` không có). Chưa sửa code cho tới khi người dùng cài skill hoặc quyết cách khác.

## 1. Việc đề xuất (chờ người dùng chọn)

| # | Việc | File | Kiểm |
|---|---|---|---|
| 1 | Đưa `TAI-LIEU.md` lên đầu danh sách, mở sẵn khi chạy xong | `docui/app.js` | Test DOM: tài liệu đầu tiên là `TAI-LIEU.md` |
| 2 | Hiển thị Markdown (tiêu đề, bảng, danh sách) thay cho văn bản thô; không tải thư viện ngoài (CSP) | `docui/app.js`, `app.css` | Test DOM: bảng Markdown thành `<table>`; nội dung HTML trong file không chạy |
| 3 | Chọn chế độ `agent` / `oneshot` trên biểu mẫu | `docweb.py` (`submit` nhận `mode`), `index.html` | `test_docweb`: `mode` sai → 422; `oneshot` gọi `run_documents(mode="oneshot")` |
| 4 | Nhóm tài liệu theo loại: đọc chính, API, bảng, sự kiện, máy đọc | `docui/app.js` | Test DOM |
| 5 | Trình bày lại theo `taste-skill` | `docui/*` | Kiểm bằng mắt trên desktop và mobile; ghi ảnh chụp |

## 2. Thứ tự

1 → 2 → 3 → 4 → 5. Mỗi bước: test đỏ trước, sửa, chạy `test_docweb` và `node --test slice/tests/ui/docui.test.cjs`, rồi chạy cả suite.

## 3. Không làm

- Không thêm upload ZIP, GitHub, cancel/resume (ngoài phạm vi).
- Không gọi model trả tiền khi test.
- Không commit hay push khi người dùng chưa yêu cầu.
