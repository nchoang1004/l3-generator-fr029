# Đặc tả sơ đồ kiến trúc cho smoke test

Ngày 24/09/2026. Mục này nói sơ đồ phải có gì và pipeline làm gì. Đây là quy ước của smoke test, không thay PRD/FR/NFR.

## 1. Quyết định của Khiêm

| Điểm | Quyết định |
|---|---|
| Mức sơ đồ | Mức 2: mỗi khối là một component. Thêm góc nhìn tổng quan mức 1 (nhóm thư mục cấp 1) |
| Cách chia khối | Theo tầng: bám thư mục, code chia tất định. AI không chia, không gộp |
| Evidence | Mức 2 là chính: cặp component, số file, tên ký hiệu. Mức 3 (`file:dòng`) chỉ khi cần, nằm trong JSON |
| Vai trò AI | Đặt tên, vai trò, mô tả, nhãn nghĩa cạnh; nhận diện hệ thống ngoài. Không quyết khối hay cạnh |
| Cạnh | Chỉ cạnh nghiệp vụ và cạnh kết nối hệ thống ngoài. Cạnh chỉ dùng kiểu dữ liệu và cạnh tới/từ phần dùng chung không vẽ, vẫn giữ trong JSON |
| Phạm vi | Loại thư mục `migrations`, `alembic`, `tests`, `test`, `scripts`; ghi ở mục giới hạn |
| Khung "Dùng chung" | Vai trò AI thuộc config/logging/error_handling/constants/utility **và** có căn cứ tĩnh |
| Model | Tạm thời chỉ Groq `gpt-oss-120b` (Gemini sắp hết quota). Ngân sách buổi thử 140k token |
| Chấm | Xem bằng mắt so với `mockup/target-detail.svg`; cộng các kiểm tự động ở mục 4 |
| `read_code` | Giữ (Khiêm chốt 24/09): chạy với `--read-code`, lượt đọc dùng `tool_choice=auto`. Quota còn lại chỉ đủ boilerplate |

**Lệch có chủ ý so với PRD/đề bài:** Nhãn nghĩa cạnh và tên hệ thống ngoài là mô tả do AI viết, mức `inferred`; quan hệ chính vẫn do phân tích tĩnh chứng minh (đề bài 3.6).

## 2. Sơ đồ có gì

**Chi tiết:** khối component (tên, vai trò, số endpoint, số bảng) trong subgraph theo nhóm thư mục cấp 1; khung "Dùng chung" không có cạnh; khung "Hệ thống ngoài"; cạnh nghiệp vụ có nhãn nghĩa; cạnh kết nối có nhãn là hàm tạo kết nối.

**Tổng quan:** mỗi nhóm thư mục cấp 1 là một node, cộng "dùng chung" và hệ thống ngoài; số trên cạnh là số cạnh chi tiết gộp lại.

**Không có:** file, class, function, thư viện; cạnh chưa xác định được đích.

## 3. Pipeline: ai làm gì, kiểm thế nào

| Bước | Ai làm | Luật / cửa kiểm |
|---|---|---|
| Chia khối | Code | Thư mục; thư mục có < 2 file có nội dung gộp vào cha; thư mục con chỉ cha dùng, không dùng gì cha không dùng, không thêm thư viện mới thì gộp vào cha. Mỗi file thuộc đúng một khối |
| Cạnh | Code | Import đã xác định đích; `file:dòng` ở hai đầu |
| Cạnh chỉ dùng kiểu | Code (mức 3) | Mọi ký hiệu lấy từ đích là lớp model/schema/enum/mixin (kể cả gián tiếp) hoặc type alias |
| Tên, vai trò, mô tả, nhãn nghĩa cạnh | Groq, 1 request/lô | Đủ ID; tên không phải đường dẫn; vai trò có tín hiệu tĩnh (`role_check`); nhãn chỉ nhận cho cạnh ra thật. Không qua thì dùng nhãn code |
| Khung dùng chung | Code, dựa vai trò AI | Vai trò dùng chung + căn cứ tĩnh (biến môi trường, thư viện log, lớp lỗi, chỉ hằng) + không route/bảng/kết nối + có nơi dùng |
| Hệ thống ngoài | Groq, 1 request | Thư viện có trong dữ kiện; lời gọi tạo kết nối là `external_call` của thư viện đó. Code đặt cạnh ở mọi khối có lời gọi |
| Render | Code | Mermaid chi tiết + tổng quan, `graph.json`, `README.md` |

## 4. Tiêu chí đạt

1. Chi tiết ≤ 20 khối (trần 50), tổng quan ≤ 8 node; mermaid-cli render được.
2. Mọi cạnh vẽ có evidence mức 2 trong README và ít nhất một cặp `file:dòng` hai đầu trong JSON.
3. Không cạnh tới hệ thống ngoài nào xuất phát từ khối không có lời gọi tạo kết nối.
4. ≥ 90% khối có tên qua kiểm; báo số tên tiếng Việt.
5. Khiêm so bằng mắt với hình mẫu.
6. Chi phí boilerplate ≤ 30k token (có `read_code`; ước tính trước khi chạy khoảng 28k).
