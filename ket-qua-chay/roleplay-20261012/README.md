# Test cả luồng bằng agent Claude đóng vai model — 12/10/2026

Thư mục này lưu lần test luồng FR-029 trên repo thật mà không gọi API trả phí. Hai agent Claude đóng vai model: mỗi agent chỉ đọc đúng prompt và request mà model thật sẽ nhận (chế độ đọc một lần, prompt v6), không đọc code bộ kiểm hay gold. Câu trả lời được phát lại qua pipeline thật.

**Cách này kiểm được bộ kiểm, prompt và đầu ra. Nó không đo được model sẽ dùng thật (gpt-5…).**

| Repo | Request | Kết quả | So với gold |
|---|---|---|---|
| tdd-docker (`project/`) | 1 | completed, 0 mục bị từ chối; 2 file API, 1 file EVT | route 6/6 (handler, tham số, body, response, status đều đúng); model 4/4; vai trò 9/9; giới hạn 2/2 (`tdd/score.txt`) |
| Teamhide | 2 (1 vòng sửa) | completed; 5 route, 8 model, 54 vai trò, 1 bảng, 2 điểm sự kiện; file API, TBL, EVT | route 5/5; khóa cấu hình 13/13; thư viện 20/20; bảng `user` 9/9 cột (so với golden v1) |

Lần chạy đầu tìm ra 3 lỗi **bộ kiểm** từ chối nhầm câu trả lời đúng. Cả 3 đã sửa, có test (`test_review_20261011.RolePlayFindings`):
1. Literal `prefix=` nằm ở dòng sau của `include_router(` viết nhiều dòng.
2. Model tạo lúc chạy (`X = pydantic_model_creator(...)`) là dấu hiệu Schema API.
3. Đường gọi qua lớp gọi được (`Depends(PermissionDependency(...))` → `__call__`).

Hai mục bị từ chối **đúng** ở Teamhide, agent sửa ở vòng 2: lỗi 401 qua `raise cls.exception` (không chứng minh được lớp lỗi), và dẫn sai một dòng.

Chạy lại (từ gốc repo):

```powershell
python ket-qua-chay/roleplay-20261012/replay.py D:/VSF/l3-acceptance-repos/testdrivenio_fastapi-tdd-docker-16433b6/project D:/VSF/l3-acceptance-gold/tdd-docker/membership.json ket-qua-chay/roleplay-20261012/tdd tdd-docker answer.json
python ket-qua-chay/roleplay-20261012/replay.py D:/VSF/l3-generator-quote-evidence/sample-repos/teamhide_fastapi-boilerplate-df4e6d4 ket-qua-chay/fr029-20261002/teamhide-existing.membership.json ket-qua-chay/roleplay-20261012/teamhide teamhide answer.json repair1.json
```

Đầu ra: `tdd/out1/`, `teamhide/out2/` (file đọc chính: `TAI-LIEU.md`). `dump_oneshot.py` xuất request cho một repo khác.
