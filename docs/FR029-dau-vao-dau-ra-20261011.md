# FR-029: đầu vào, đầu ra và các vấn đề còn lại — 11/10/2026

File này trả lời ba câu: hệ thống nhận gì, xuất gì, và đã hợp lý chưa. Số liệu lấy từ lượt chạy gpt-5 trên Teamhide ngày 11/10. Đầu ra của lượt đó được dựng lại offline từ checkpoint, không gọi lại model.

**Kết luận ngắn:** đầu vào dùng được nhưng chưa được kiểm đủ. Đầu ra **chưa đạt** yêu cầu "một file, dễ đọc": hiện có 4 file, file dành cho người đọc chứa nhiều mã băm, và phần lớn dung lượng là dữ liệu máy.

## 1. Đầu vào

Mục này liệt kê những gì lệnh `document` nhận, và chỗ chưa ổn của từng thứ.

| Đầu vào | Bắt buộc | Vấn đề |
|---|---|---|
| Thư mục source | Có | Repo lớn (kibo, ~112k token) vượt giới hạn của chế độ "đọc một lần"; chưa có chế độ chia gói |
| `membership.json`: danh sách component do bước kiến trúc (FR-028) cấp | Có | Không kiểm loại component. File của Teamhide không ghi `kind`, nên `tests/` và `migrations/` bị coi là component thường và hiện trong README (vi phạm FR-029: phải bỏ Kiểm thử, Migration) |
| `archdia.json`: dữ liệu kiến trúc để đối chiếu route (AC-04) | Không | Chỉ đọc được khuôn `archdia-fixture-v1` tự đặt. Chưa có khuôn thật từ FR-028, nên AC-04 luôn "not_evaluated" |
| Sơ đồ Mermaid | Không | Không có thì README thiếu mục sơ đồ (AC-06 chưa đủ) |
| Model, khóa API, ngân sách | Có khi chạy thật | Ổn: có trần USD và chặn trước mỗi request |

Thêm một lỗi môi trường: `slice/` **không có file khai báo thư viện cần cài**. Bước kiểm OpenAPI thêm ngày 11/10 cần `openapi-spec-validator`. Lượt gpt-5 chạy bằng Python không có thư viện này, nên file API bị chặn (FORMAT_INVALID) dù 4 route đã qua bộ kiểm.

## 2. Đầu ra hiện tại

FR-029 quy định nhiều file, theo mẫu `tech-specs/` của mentor. Lượt Teamhide sinh ra:

| File | Cỡ | Dành cho | Nội dung |
|---|---|---|---|
| `README.md` | 255 dòng | Người đọc | Mục lục, cấu trúc component (vai trò từng file), lời gọi HTTP, giới hạn |
| `tech-specs/APP/api/API-TEAMHIDE-APP-v1.md` | 482 dòng | Người đọc + máy | Bảng route (4 dòng), bảng model, ~20 dòng truy vết, ~360 dòng OpenAPI JSON |
| `result.json` | 7.460 dòng | Máy | Toàn bộ dữ kiện, bằng chứng, độ phủ |
| `manifest.json` | 7.492 dòng | Máy | Gần như trùng `result.json`, thêm danh sách file |

Người đọc phải mở ít nhất hai file (README và từng file API). Thông tin chính chỉ chiếm phần nhỏ: 4 route và 7 model nằm trong khoảng 60 dòng.

## 3. Chỗ khó đọc (ví dụ thật)

| Chỗ | Ví dụ | Nên là |
|---|---|---|
| Đầu file API là mã băm | `fact_ids: ["fact:1a9144874101b8b5…", …]` (hai dòng rất dài) | Dời sang `result.json` |
| Ô Auth dài, lặp ở mọi dòng | `dependency: Provide[Container.jwt_service], Logging; auth: unknown — Không có Security/Depends auth trong mã route; middleware…` | `chưa rõ`, giải thích một lần dưới bảng |
| Từ kỹ thuật | `200 (suy theo fastapi.default_status_200)` | `200 (mặc định của FastAPI)` |
| Tiếng Anh lẫn | `True`, `False`, `Nullable` | `có`, `không`, `được null` |
| Nhãn khó hiểu | `inferred (pydantic.v2_required_no_default) / full` | `suy luận` / `đủ`, lý do ghi một lần |
| File không cần vai trò vẫn hiện "unknown" | `app/__init__.py — vai trò unknown: agent chưa xác định` (file rỗng) | Bỏ dòng, hoặc ghi "file rỗng" |
| Mục không nên có | `### tests`, `### migrations` trong "Cấu trúc component" | Bỏ (do lỗi đầu vào ở mục 1) |
| Bảng truy vết | Mã băm 64 ký tự trong mỗi ô | Chỉ giữ `file:dòng`; mã đầy đủ ở `result.json` |

## 4. Yêu cầu "đầu ra chỉ một file, dễ đọc"

Yêu cầu này **khác FR-029 hiện tại**, vì FR-029 theo mẫu mentor có một file API cho mỗi component. Có hai cách:

| Cách | Làm gì | Ưu | Nhược |
|---|---|---|---|
| **A. Giữ FR-029, thêm một file đọc chính** | Sinh thêm `TAI-LIEU.md`: mọi route, model, cấu trúc, giới hạn của cả repo, viết gọn theo mục 3. Các file cũ giữ nguyên cho máy và cho mẫu mentor | Không phải sửa spec | Thông tin lặp ở hai nơi (cùng sinh từ một nguồn nên không lệch) |
| **B. Đổi FR-029 thành một file** | Gộp README và các file API vào một file; `result.json` giữ cho máy | Đúng "một file" | Phải mở yêu cầu thay đổi (CR) theo quy trình, lệch mẫu `tech-specs/` của mentor, sửa AC-01, 04, 06 |

Khung đề xuất cho file đọc chính (cả hai cách dùng chung):

```text
# <repo> — tài liệu API
Tình trạng: <đủ / còn thiếu: …>   Đọc source: <x/y file>   Sinh lúc: …
1. Danh sách endpoint      bảng: method | path | vào | ra | status | auth
2. Chi tiết từng endpoint  tham số, body, response; nguồn: file:dòng
3. Model dữ liệu           mỗi model một bảng: trường | kiểu | bắt buộc | được null
4. Cấu trúc code           mỗi component: file → vai trò (chỉ file có vai trò)
5. Gọi ra ngoài            thư viện | method | đích | file:dòng
6. Chưa biết / giới hạn    mỗi mục một dòng, nói rõ vì sao
Phụ lục: OpenAPI (cho máy, đặt cuối)
```

## 5. Vấn đề còn lại khác

| # | Vấn đề | Mức | Trạng thái |
|---|---|---|---|
| 1 | Chưa đo lại nghiệm thu sau các sửa ngày 11/10; mới chạy thật 1 repo, 1 lần (Teamhide, 4/5 route) | Cao | Chưa làm |
| 2 | "Được bộ kiểm nhận" chưa chắc đúng; chưa chấm nội dung với gold | Cao | Chưa làm |
| 3 | Repo lớn: chưa có chế độ chia gói; ước 0,8–1,5 USD/lần cho kibo bằng gpt-5 | Trung bình | Chưa làm |
| 4 | Đối chiếu kiến trúc chỉ đọc khuôn fixture (AC-04) | Trung bình | Chờ quyết định |
| 5 | Thư viện cần cài chưa khai báo (mục 1) | Trung bình | Đã sửa, xem mục 6 |
| 6 | `membership.json` không được kiểm loại component (mục 1) | Trung bình | Đã sửa, xem mục 6 |
| 7 | Đường gọi Service: hàm truyền làm tham số bị từ chối nhầm (1/16 trên gold) | Thấp | Giới hạn đã biết |
| 8 | Luật auth mới chỉ có test, chưa có gold để đo | Thấp | Chưa đo |
| 9 | Thư mục tên `venv` không có `pyvenv.cfg` vẫn bị bỏ qua | Thấp | Chờ quyết định (quy định FR-028) |
| 10 | 8 luật kiểm mới chưa qua giám khảo độc lập | Trung bình | Dự kiến cho Codex/agent Claude đóng vai, không tốn API |

## 6. Quyết định và việc đã làm (11/10/2026)

Người dùng quyết:
1. Chọn cách A.
2. Để nguyên `archdia.json`.
3. Làm các mục còn lại.

| Việc | Đã làm (code chưa commit) | Kiểm chứng |
|---|---|---|
| Cách A | `slice/l3slice/tailieu.py` sinh `TAI-LIEU.md` theo khung ở mục 4. Không có mã fact/evidence, không có khối JSON. Dòng còn trông giống route mà chưa xác nhận được nêu ở mục 6 của file. Loại file ghi là `readme`, không phải sửa contract | `slice/tests/test_tai_lieu.py` 8/8; mẫu thật: `ket-qua-chay/tai-lieu-mau-teamhide-20261011/output/TAI-LIEU.md` (240 dòng, dựng lại offline từ câu trả lời gpt-5) |
| Mục 5.5 | `slice/requirements.txt`; một dòng hướng dẫn ở `slice/README.md` | Đọc lại |
| Mục 5.6 | Membership không ghi loại: component chỉ gồm file kiểm thử hoặc migration được xếp theo phạm vi đọc, kèm giới hạn `MEMBERSHIP_KIND_DERIVED`. Ghi `normal` cho file kiểm thử: giới hạn `MEMBERSHIP_KIND_SUSPECT`. README ghi "file rỗng" hoặc "ngoài phạm vi đọc" thay cho "vai trò unknown" | Như trên; suite 467/468 (lỗi `test_gateway` cũ) |

Còn treo:
- FR-029 mục "Đầu ra" chưa ghi `TAI-LIEU.md`. Sửa spec phải theo quy trình yêu cầu thay đổi (CR); chưa làm.
- Các file cũ (README, file API) chưa được làm gọn theo mục 3, vì cách A giữ nguyên chúng.
