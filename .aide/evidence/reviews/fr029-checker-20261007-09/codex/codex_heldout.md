Bạn là giám khảo độc lập. Chỉ đọc, không sửa file. Mỗi kết luận phải có `file:dòng` trong source. Không chạy code của repo.

## Bối cảnh

Một công cụ sinh tài liệu API cho repo FastAPI có bộ kiểm tự động. Trên 4 repo (chưa từng dùng để chỉnh công cụ), bộ kiểm đã xuất "gói" ở:
D:/VSF/l3-generator-l3/ket-qua-chay/fr029-heldout-20261008/*.packet.json

Repo tương ứng:
- dispatch: D:/VSF/VSF-L3 Generator/sample-repos/dispatch
- nsidnev_fastapi-realworld-example-app, rhoboro_async-fastapi-sqlalchemy, rafsaf_minimal-fastapi-postgres-template: D:/VSF/l3-heldout-repos/<tên>

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
