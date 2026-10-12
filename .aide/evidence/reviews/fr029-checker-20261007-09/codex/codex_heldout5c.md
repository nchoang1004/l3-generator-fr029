Bạn là giám khảo độc lập. Chỉ đọc, không sửa file. Mỗi kết luận phải có `file:dòng` trong source. Không chạy code của repo.

## Bối cảnh

Một công cụ sinh tài liệu API cho repo FastAPI có bộ kiểm tự động. Trên một repo (chưa từng dùng để chỉnh công cụ), bộ kiểm đã xuất "gói" ở:
D:/VSF/l3-generator-l3/ket-qua-chay/fr029-heldout-20261008-r18/xiao-villamor_PrintStash.packet.json

Repo tương ứng:
- xiao-villamor_PrintStash: D:/VSF/l3-heldout-repos3/xiao-villamor_PrintStash (CHỈ chấm repo này)


Mỗi gói có:
- `dependencies`: với mỗi hàm Depends mà một route dùng, danh sách tham số request (`in`: header|query|cookie|path, `name` là tên HTTP) mà bộ kiểm cho rằng FastAPI thêm vào endpoint vì dependency này (đi theo cả Depends lồng nhau). Tên header là tên HTTP (FastAPI đổi `_` thành `-`, trừ khi có alias).
- `suspects`: các dòng bộ kiểm bắt agent phải giải thích vì trông giống lời gọi HTTP (`http`), lời gọi thư viện HTTP khác (`other_http`), đăng ký route không qua decorator (`registration`). Dòng decorator route không nằm trong danh sách này.
- `decorators_refused`: decorator route thật bị bộ kiểm từ chối (mong đợi rỗng).

KHÔNG đọc code của bộ kiểm (thư mục d:/VSF/l3-generator-l3/slice/), HANDOFF, docs/, .aide/. Chỉ dùng gói + source repo + hiểu biết về FastAPI.

## Việc cần làm cho từng repo

1. **Dependencies:** với mỗi mục, đọc định nghĩa hàm (và Depends lồng nhau, alias `Annotated[..., Depends(x)]`, factory trả về hàm lồng, class có `__call__`). Liệt kê tham số request đúng theo FastAPI. So với gói: đánh dấu từng tham số `đúng`/`sai`, liệt kê tham số `thiếu`. Chú ý: tham số kiểu `Request`, `Session`, model Pydantic (body), `Depends` không phải tham số header/query.
2. **Dependency bị bỏ sót khỏi gói:** lấy mẫu ít nhất 15 route (dispatch: ít nhất 30, trải đều các module) và kiểm route đó có dùng dependency nào (ở handler, `dependencies=[...]` của decorator, router, app) mà gói không có không. Ghi rõ dependency ở cấp router/app riêng.
3. **Suspects:** với từng dòng, phân loại: `http_that` (lời gọi qua httpx/requests/aiohttp), `http_khac` (thư viện HTTP khác), `registration`, `can_giai_thich` (không phải HTTP nhưng hợp lý để agent xem lại, ví dụ session CSDL), `nhieu` (rõ ràng không liên quan).
4. **Bỏ sót HTTP:** tìm trong toàn repo mọi lời gọi HTTP qua httpx/requests/aiohttp (kể cả `client.get` trên client tạo ở chỗ khác, `requests.Session().get`, gọi nhiều dòng). Liệt kê lời gọi KHÔNG có trong `suspects` (so theo file và dòng có lời gọi; lệch 1–2 dòng do gọi nhiều dòng thì coi là có).

## Đầu ra

Tin nhắn cuối cùng: một khối ```json duy nhất:
{"repos": [{"repo": "...",
  "dependencies": {"params_dung": n, "params_sai": [{"dep","in","name","ly_do","source"}], "params_thieu": [{"dep","in","name","source"}]},
  "deps_bo_sot": {"routes_kiem": n, "items": [{"route","dependency","cap": "handler|decorator|router|app","source"}]},
  "suspects": {"http_that": n, "http_khac": n, "registration": n, "can_giai_thich": n, "nhieu": [{"at","ly_do"}]},
  "http_bo_sot": [{"at","code"}]}],
 "ghi_chu": ["..."]}
Sau khối json, tối đa 10 dòng tiếng Việt tóm tắt. Không bịa số: chỉ đếm thứ đã đọc.

## Quy ước bổ sung cho vòng này (giữ nguyên các yêu cầu trên)

- Phạm vi đọc của công cụ loại thư mục test (tests/, test_*.py, conftest.py) theo FR-028. Lời gọi HTTP trong test KHÔNG tính là bỏ sót; liệt kê riêng trong "ghi_chu" nếu muốn, không đưa vào http_bo_sot.
- Tham số do security dependency (`Security(...)`, `OAuth2PasswordBearer`, `APIKeyHeader`, `HTTPBearer`) đi vào cột auth/securitySchemes, không tính là params_thieu. Header khai bằng `Header(...)` thì vẫn là tham số.
- `decorators_refused`: với từng mục, phán xét bộ kiểm từ chối ĐÚNG (receiver không phải FastAPI/APIRouter) hay SAI (đây là route FastAPI thật). Thêm vào mỗi repo trường "decorators_refused_judgement": [{"at","dung_hay_sai","ly_do","source"}].
- Dependency do lớp có `__call__` hoặc `Depends()` không đối số với annotation là class: liệt kê ở deps_bo_sot nếu tham số request của nó (header/query/cookie/path) bị bỏ sót; nếu chỉ là body/form thì ghi chú, không tính lỗi.

- Gói có thể ghi cùng một dependency hai lần với `called` true/false: `Depends(X())` (instance, FastAPI đọc `__call__`) khác `Depends(X)` (class, FastAPI đọc `__init__`). Chấm từng mục theo đúng cách dùng đó.
- Repo lớn: với "Bỏ sót HTTP", quét toàn repo bằng tìm kiếm văn bản (rg) cho httpx/requests/aiohttp rồi đọc từng chỗ.
- Phạm vi đọc theo FR-028 còn loại: file `*_test.py`, và file trong `scripts/` không import code của repo. Lời gọi trong các file đó không tính là bỏ sót.
- Chỉ tính lời gọi TRỰC TIẾP qua httpx/requests/aiohttp (kể cả `super().request` trong lớp con client). Lời gọi qua hàm bọc của dự án ghi riêng trong ghi_chu, không đưa vào http_bo_sot.
- Nếu suspects quá nhiều để đọc hết, chấm mẫu ít nhất 60 dòng trải đều các file và ghi rõ số đã chấm.
