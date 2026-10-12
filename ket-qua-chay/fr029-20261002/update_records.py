"""Repair UTF-8 text in this task's new records and append final evidence; never alter approvals."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
titles = ['Cảnh báo route không qua decorator', 'Loại route và đăng ký router trong test',
          'Đọc HTTP client theo phạm vi biến', 'Xuất lời gọi HTTP vào README', 'Đọc response danh sách model']
checks = ['test_non_decorator_routes_are_reported_individually', 'test_test_routes_and_test_registration_are_excluded',
          'test_client_scopes_do_not_turn_database_get_into_http', 'test_http_readme_escaping_and_secret_redaction',
          'test_array_response_decorator_and_annotation']
note = 'Nháp, chờ Architecture Gate BL-r10. Chưa phải approval hoặc nghiệm thu độc lập.'
def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
def body(path, text):
    p = ROOT / path
    original = p.read_text(encoding='utf-8')
    front = original.split('---', 2)
    write(path, '---' + front[1] + '---\n\n' + text)

body('.aide/lifecycle/epics/EPIC-L3GEN-029.md', '# EPIC-L3GEN-029\n\n'+note+
     '\n\n## Phạm vi\nT1–T5 trong HANDOFF-CODEX-FR029. Giữ nguyên các phần hoãn: archdia.json, vai trò file/component, Python 3.14, trần node và UI.\n'
     '\n## Story\n- STORY-L3GEN-029-02\n- STORY-L3GEN-029-05\n- STORY-L3GEN-029-08\n')
for s in ('02', '05', '08'):
    body(f'.aide/lifecycle/stories/STORY-L3GEN-029-{s}.md',f'# STORY-L3GEN-029-{s}\n\n{note}\n\n## Giao cái gì\nPhần AC tương ứng qua các task T1–T5; hành vi chuẩn giữ tại FR-029.\n')
for n, (title, test) in enumerate(zip(titles, checks), 1):
    key = f'TASK-L3GEN-029-{n}'
    body(f'.aide/lifecycle/tasks/{key}.md', f'# {key}\n\n{note}\n\n## Việc làm\n{title}.\n\n## Xong khi\n'
         f'`slice/tests/test_fr029.py::{test}` qua. Xem báo cáo và log tại `ket-qua-chay/fr029-20261002/`. '
         'Test code không thay review độc lập hoặc quyết định Gate.\n')
    write(f'.aide/evidence/plans/PLAN-{key}-r2.md',f'# PLAN-{key} — r2\n\n{note}\n\n'
          'Bản r1 được ghi trước khi sửa production nhưng mất dấu tiếng Việt khi truyền qua PowerShell. Giữ r1; r2 đính chính chữ và ghi bước kiểm cuối, không giả thời điểm lập kế hoạch.\n\n'
          f'## Mục tiêu\n{title}.\n\n## Bước kiểm cuối\nChạy test mới, toàn bộ test, contract, baseline, golden development và bốn repo thật. '
          'Xuất Teamhide theo membership cũ và snapshot khớp. Lưu lệnh, log, số trước/sau.\n\n## Không làm\nKhông sửa spec nguồn, test gateway cũ, UI, component; không commit/push.\n')
    ctxpath = ROOT / f'.aide/evidence/context/CTX-{key}.yaml'
    ctx = json.loads(ctxpath.read_text(encoding='utf-8'))
    ctx['authority']['status'] = 'nháp, chưa ký'
    ctx['authority']['note'] = 'Context cục bộ; không tuyên bố aide context compile đã chạy.'
    ctx['key'] += '-r2'
    for name, record in ctx['inputs'].items():
        p = ROOT / name
        m = re.search(r'^revision: (\d+)', p.read_text(encoding='utf-8'), re.M)
        record.update(revision=int(m[1]) if m else None, sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    write(f'.aide/evidence/context/CTX-{key}-r2.yaml', json.dumps(ctx, ensure_ascii=False, indent=2)+'\n')
    write(f'.aide/evidence/diaries/DIARY-{key}.md',f'# DIARY-{key}\n\n## Diễn giải\n02/10/2026 — {title}, theo phạm vi Hoàng đã giao.\n\n'
          '## Đi chệch\nThêm add_api_websocket_route theo bàn giao. Chỉ lọc file test cho route/HTTP. Bản plan r1 bị lỗi encoding, có r2 đính chính.\n\n'
          '## Đánh đổi\nKhông gọi mạng hoặc chạy source đầu vào. Header/credential trong call_text được redacted. '
          'Để nguyên test gateway lỗi sẵn theo quyết định người dùng.\n\n'
          f'## Kiểm chứng\nTest `{test}` và các log ở ket-qua-chay/fr029-20261002. Đây là kiểm tự động của người triển khai, chưa là review độc lập.\n\n'
          '## Câu hỏi mở\nAC-029-04 và AC-029-07 còn chờ tích hợp; chưa chốt component hoặc Gate.\n')
print('Updated task records (UTF-8).')
