# Bộ tài liệu sinh còn thiếu gì — 11/10/2026

File này liệt kê những gì bộ tài liệu L3 đang sinh còn thiếu, xếp theo mức cần. Mỗi mục ghi nguồn yêu cầu, hiện trạng và cách bổ sung.

**Nguồn đối chiếu:**
- Đề bài mục 3.6.
- FR-L3GEN-028 đến 031.
- Mẫu `tech-specs/` của mentor (`docs/agentic-sdlc-execution-guide.md` mục A.1, B.10).
- Hướng dẫn ký hiệu C4.
- arc42 mục 5.
- Các bài hướng dẫn viết OpenAPI.
- Hai công cụ cùng loại (archdocs, gavlix-docs). Trang của hai công cụ này không mở được; phần so sánh chỉ dựa trên đoạn mô tả trong kết quả tìm kiếm.

**Mẫu đối chiếu:** đầu ra Teamhide ngày 11/10 (`ket-qua-chay/tai-lieu-mau-teamhide-20261011/output/`).

## 1. Spec đã yêu cầu nhưng luồng mới chưa sinh

Luồng agent hiện chỉ sinh tài liệu API (FR-029). Các mục dưới đây là bắt buộc theo spec hoặc đề bài.

| # | Thiếu | Nguồn | Hiện trạng | Ví dụ Teamhide |
|---|---|---|---|---|
| 1 | Tài liệu bảng CSDL (`schema/TBL-…md`) | FR-030; đề bài "DB relationships"; mẫu mentor | Chỉ luồng tĩnh cũ (`analyze`) sinh được. Luồng agent chỉ xếp vai trò "Model bảng" cho file | `app/user/domain/entity/user.py` khai bảng nhưng không có tài liệu bảng |
| 2 | Tài liệu sự kiện, tác vụ nền (`events/EVT-…md`) | FR-031; đề bài "Event relationships", "queue/event" | Như trên | Có thư mục `celery_task/`, chỉ được xếp vai trò "Hạ tầng" |
| 3 | Thư viện quan trọng | Đề bài "important dependency"; FR-028 mục "Thư viện" | Không có. Agent có đọc `pyproject.toml`/`requirements*.txt` nhưng không xuất | FastAPI, SQLAlchemy, Redis, Celery, dependency-injector… không được nêu |
| 4 | Cấu hình: các khóa cấu hình, biến môi trường | Đề bài "configuration"; FR-028 "khóa cấu hình" | Chỉ xếp vai trò "Cấu hình" cho file, không liệt kê khóa | `core/config.py` có các khóa DB, Redis, JWT nhưng không được liệt kê |
| 5 | Sơ đồ component / sơ đồ phụ thuộc | Đề bài "Dependency diagram"; AC-029-06 | Phụ thuộc đầu vào từ FR-028; chưa có thì README ghi "chưa có sơ đồ" | Mọi lượt chạy đều thiếu |

Mục 5 và việc đối chiếu `archdia.json` (AC-04) phụ thuộc bước FR-028. Người dùng đã quyết để nguyên.

## 2. Thiếu với người dùng tài liệu API

Đây là những gì người gọi API cần mà tài liệu chưa có. Mục 6 và 7 làm tài liệu Teamhide hiện **sai về thực tế dùng**, không chỉ thiếu.

| # | Thiếu | Vì sao cần | Ví dụ Teamhide |
|---|---|---|---|
| 6 | Lỗi có thể trả về (status và dạng body) | Hướng dẫn OpenAPI: khai mọi mã trả về, kèm dạng body lỗi | `server.py:31` đổi `CustomException` thành JSON `{error_code, message}`. Service ném lỗi 400, 401, 404 (`app/user/application/exception`). Tài liệu chỉ ghi 200 |
| 7 | Xác thực và middleware toàn cục | Người gọi phải biết cần token hay không; OpenAPI có `securitySchemes` | `AuthenticationMiddleware` và `CORSMiddleware` ở `server.py:52-62`. Tài liệu ghi "auth: chưa rõ" cho cả 4 route |
| 8 | Mô tả ngắn cho endpoint và component | C4: mỗi phần tử có mô tả và công nghệ. Đề bài cho dùng AI để bổ sung mô tả. FastAPI có `summary`, `description`, `tags`, docstring | Không có mô tả nào |
| 9 | Ví dụ request/response | Hướng dẫn OpenAPI: ví dụ cho schema phức tạp | `Body(example=…)` có trong agentgpt, chưa được đọc |
| 10 | `tags`, `deprecated`, `responses=` khai ở decorator | Một phần của OpenAPI mà FastAPI tự sinh | Prompt và bộ kiểm đều chưa đọc |

## 3. Thiếu quan hệ

Đề bài yêu cầu quan hệ "phải được chứng minh từ source". Tài liệu hiện có từng phần riêng lẻ nhưng chưa nối chúng.

| # | Thiếu | Hiện trạng |
|---|---|---|
| 11 | Mỗi endpoint đi qua service nào, đọc/ghi bảng nào | Chỉ có đường gọi của file Service, không gắn với từng endpoint |
| 12 | Component nào gọi component nào | Có danh sách file theo component, không có cạnh giữa các component (đầu vào từ FR-028) |

## 4. Trình bày

| # | Thiếu | Ghi chú |
|---|---|---|
| 13 | Thời điểm sinh, commit, model, phiên bản prompt trong `TAI-LIEU.md` | Có trong `result.json`, chưa đưa lên đầu file đọc |
| 14 | Chú giải nhãn "chắc chắn / suy luận / chưa rõ" | C4: mỗi sơ đồ có chú giải |
| 15 | Gom lý do "suy luận" lặp lại | Ở Teamhide, 4 endpoint lặp cùng một câu lý do dài |

## 5. Đề xuất thứ tự làm

Mọi mục đều theo cách đang dùng: model đề xuất, bộ kiểm đòi bằng chứng `file:dòng`, test viết trước. Test bằng Codex hoặc agent Claude đóng vai model, không tốn tiền API.

| Đợt | Mục | Lý do | Cỡ (ước) |
|---|---|---|---|
| 1 | 6, 7 | Tài liệu hiện sai so với hành vi thật của API | Vừa: thêm loại dữ kiện "lỗi trả về" và "middleware", có bộ kiểm |
| 2 | 3, 4, 13, 14, 15 | Đọc tĩnh được, chắc chắn, không cần model | Nhỏ |
| 3 | 1, 2 | Spec bắt buộc (FR-030, 031). Có thể lấy luồng tĩnh cũ làm điểm tựa | Lớn |
| 4 | 11, 8 | Giá trị cao với người đọc. Mô tả (8) do model viết nên phải gắn nhãn "do AI viết" | Vừa |
| 5 | 9, 10, 12 | Bổ sung | Nhỏ đến vừa |

Mục 3, 4, 6–15 vượt phạm vi FR-029 hiện tại. Làm thì cần ghi vào FR (yêu cầu thay đổi theo quy trình) hoặc mở FR mới.

## 6. Trạng thái 12/10/2026

Người dùng bảo "làm đi", nên đã làm cả 5 đợt. Code chưa commit; chi tiết ở HANDOFF.

| Mục | Trạng thái |
|---|---|
| 1, 2 bảng CSDL, sự kiện | Đã làm. Đọc tĩnh; thêm Celery và BackgroundTasks; có file TBL/EVT |
| 3, 4 thư viện, cấu hình | Đã làm (đọc tĩnh) |
| 5 sơ đồ | Chưa: phụ thuộc FR-028, người dùng quyết để nguyên |
| 6, 7 lỗi trả về, middleware | Đã làm. Lỗi do agent đề xuất và bộ kiểm chứng minh; middleware đọc tĩnh |
| 8 mô tả | Đã làm, nhãn "AI viết" |
| 9, 10 ví dụ, tags, deprecated | Đã làm (`responses=` của decorator chưa đọc) |
| 11 đường gọi endpoint | Đã làm (suy từ vai trò Service) |
| 12 quan hệ component | Đã làm, đọc tĩnh từ các lời gọi đã nối được |
| 13–15 trình bày | Đã làm |

Đã kiểm bằng agent Claude đóng vai model trên tdd-docker và Teamhide: `ket-qua-chay/roleplay-20261012/`. Chưa đo bằng model thật.

## 7. Nguồn

- Đề bài mục 3.6: `Đề bài.md`, dòng 558–612.
- FR: `.aide/requirements/fr/FR-L3GEN-028.md` … `031.md`.
- Mẫu mentor: `docs/agentic-sdlc-execution-guide.md` mục A.1, B.10.
- C4, ký hiệu: https://c4model.com/diagrams/notation
- arc42 mục 5: https://docs.arc42.org/section-5/
- OpenAPI: https://dev.to/hsmall/10-openapi-best-practices-that-elevate-your-api-game-2hpj, https://www.speakeasy.com/openapi/security/custom-auth.md
- Công cụ cùng loại: https://pypi.org/project/archdocs/, https://pypi.org/project/gavlix-docs/
