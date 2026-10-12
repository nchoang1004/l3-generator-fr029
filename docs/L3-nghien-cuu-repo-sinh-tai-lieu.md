# Nghiên cứu repo để triển khai tài liệu FR-029

Cập nhật: 07/10/2026. Đã đọc README và các phần mã liên quan đến đọc source, điều phối, ghi tài liệu và kiểm kết quả. Chưa cài, chạy hay benchmark các repo này. Các nhận xét dưới đây chỉ áp cho phần đã kiểm ở commit được ghi.

Mục tiêu là agent phân tích source cho đủ 8 AC của [FR-029](../.aide/requirements/fr/FR-L3GEN-029.md). Kế hoạch áp dụng nằm ở [kế hoạch triển khai](L3-ke-hoach-agent-sinh-tai-lieu.md); tài liệu này giữ bằng chứng nghiên cứu để không lặp trong từng nhiệm vụ.

## 1. Phiên bản đã kiểm

Ghi commit cố định để người triển khai mở đúng mã đã tham khảo.

| Repo | Commit | Giá trị chính cho FR-029 |
|---|---|---|
| [OpenDeepWiki](https://github.com/AIDotNet/OpenDeepWiki/tree/d33113c88c56458c202fa6904ec114387319f1f5) | `d33113c88c56458c202fa6904ec114387319f1f5` | Công cụ đọc source và ngân sách vòng agent |
| [CodeWiki của FSoft](https://github.com/FSoft-AI4Code/CodeWiki/tree/46ce743d7a15cc14aa1215ba0759023eaafd6671) | `46ce743d7a15cc14aa1215ba0759023eaafd6671` | Điều phối tài liệu và tách backend gọi model |
| [RepoAgent](https://github.com/OpenBMB/RepoAgent/tree/825d988127d7bfd757237d9c4e8678d9104030f0) | `825d988127d7bfd757237d9c4e8678d9104030f0` | Ngữ cảnh hàm gọi và hàm được gọi |
| [pnp/copilot-prompts](https://github.com/pnp/copilot-prompts/tree/ce4596399aa07af052ae4c032043e9e238ede230) | `ce4596399aa07af052ae4c032043e9e238ede230` | Checklist nội dung API; chỉ là mẫu prompt |

## 2. OpenDeepWiki: học vòng đọc, bổ sung kiểm độ phủ

`GitTool.ReadAsync` nhận đường dẫn và khoảng dòng, trả code có số dòng. Nó ghi nhận tên file đã đọc, nhưng có thể chỉ trả một phần file và cắt dòng dài. Vì vậy, danh sách file này chưa phải bằng chứng đã đọc hết nội dung. [GitTool.cs](https://github.com/AIDotNet/OpenDeepWiki/blob/d33113c88c56458c202fa6904ec114387319f1f5/src/OpenDeepWiki/Agents/Tools/GitTool.cs)

`DocumentSourceToolBudget` bọc ListFiles/Grep/ReadFile bằng bộ đếm. Mỗi lượt đọc bị giới hạn 240 dòng, liệt kê tối đa 20 file, tìm kiếm tối đa 12 kết quả. Có test tín hiệu hết ngân sách; test đó không đo tính đúng của tài liệu. [Bộ giới hạn](https://github.com/AIDotNet/OpenDeepWiki/blob/d33113c88c56458c202fa6904ec114387319f1f5/src/OpenDeepWiki/Agents/Tools/DocumentSourceToolBudget.cs), [test](https://github.com/AIDotNet/OpenDeepWiki/blob/d33113c88c56458c202fa6904ec114387319f1f5/tests/OpenDeepWiki.Tests/Agents/Tools/DocumentSourceToolBudgetTests.cs).

Prompt sinh một trang yêu cầu chỉ đọc 2–4 file quan trọng và viết khi hết ngân sách. `DocTool.WriteAsync` lưu Markdown cùng danh sách file đã đọc. Trong hàm này, chưa thấy kiểm từng khẳng định với đoạn source. [WikiGenerator.cs](https://github.com/AIDotNet/OpenDeepWiki/blob/d33113c88c56458c202fa6904ec114387319f1f5/src/OpenDeepWiki/Services/Wiki/WikiGenerator.cs), [DocTool.cs](https://github.com/AIDotNet/OpenDeepWiki/blob/d33113c88c56458c202fa6904ec114387319f1f5/src/OpenDeepWiki/Agents/Tools/DocTool.cs).

**Áp dụng:** N2 lưu khoảng nội dung thực gửi; N3 giữ giới hạn request/token/timeout; hết ngân sách trả phần hợp lệ và danh sách còn thiếu. N4 gắn evidence tới từng trường. Agent trả dữ kiện, renderer viết Markdown. Không lấy chính sách đọc vài file làm chính sách bao phủ FR-029.

## 3. CodeWiki: học điều phối, tách khỏi phân nhóm component

`DocumentationGenerator` dựng dependency graph, có bước clustering, rồi sinh trang chi tiết trước phần tổng quan. Nó lưu commit/model/version. `validate_generated_docs` kiểm trang còn thiếu trên đĩa; hàm này không chấm ngữ nghĩa của endpoint hay model. [documentation_generator.py](https://github.com/FSoft-AI4Code/CodeWiki/blob/46ce743d7a15cc14aa1215ba0759023eaafd6671/codewiki/src/be/documentation_generator.py)

Trong backend PydanticAI, agent được cấp công cụ đọc code và sửa tài liệu, có giới hạn request. `read_code_components` lấy source từ các node đã được phân tích. Node hàm/lớp ở đây không đồng nghĩa component sở hữu contract của FR-029. [Backend](https://github.com/FSoft-AI4Code/CodeWiki/blob/46ce743d7a15cc14aa1215ba0759023eaafd6671/codewiki/src/be/pydantic_ai_backend.py), [reader](https://github.com/FSoft-AI4Code/CodeWiki/blob/46ce743d7a15cc14aa1215ba0759023eaafd6671/codewiki/src/be/agent_tools/read_code_components.py).

Công cụ editor còn có đường đọc file và kiểm Mermaid sau thao tác ghi. Đây là kiểm đầu ra trình bày, không thay phép đo độ đúng FR-029. [str_replace_editor.py](https://github.com/FSoft-AI4Code/CodeWiki/blob/46ce743d7a15cc14aa1215ba0759023eaafd6671/codewiki/src/be/agent_tools/str_replace_editor.py)

**Áp dụng:** N3 tách adapter model và điều phối; giữ tham chiếu khi chia lượt đọc. V2 lưu phiên bản và kiểm đủ artifact. Nhận membership sẵn có; không lấy clustering, sinh module con hay công cụ sửa source vào luồng mới. A06 tổng hợp README từ dữ kiện đã kiểm thay vì cho model viết lại mọi kết luận.

## 4. RepoAgent: học ngữ cảnh quan hệ gọi

`ChatEngine.build_prompt` đưa code của hàm/lớp cùng code và mô tả của bên gọi/bên được gọi vào prompt. `generate_doc` gọi model trên ngữ cảnh đó. Prompt cũng yêu cầu tạo ví dụ giá trị trả về có thể có; không được dùng ví dụ kiểu này làm response contract thật. [chat_engine.py](https://github.com/OpenBMB/RepoAgent/blob/825d988127d7bfd757237d9c4e8678d9104030f0/repo_agent/chat_engine.py)

`FileHandler` dùng `ast.parse` và duyệt cây để tìm hàm/lớp. `Runner` điều phối sinh tài liệu và lưu trạng thái. Đây chưa phải cách agent tự đọc mọi source để xác định hợp đồng HTTP. [file_handler.py](https://github.com/OpenBMB/RepoAgent/blob/825d988127d7bfd757237d9c4e8678d9104030f0/repo_agent/file_handler.py), [runner.py](https://github.com/OpenBMB/RepoAgent/blob/825d988127d7bfd757237d9c4e8678d9104030f0/repo_agent/runner.py).

**Áp dụng:** A07 yêu cầu agent lần theo route → hàm trung gian → data access/hạ tầng trước khi gán Service. A02/A08 đọc thêm định nghĩa model/client ở file khác. Mỗi mắt xích lưu evidence; tóm tắt tài liệu cũ chỉ gợi ý nơi đọc, không làm nguồn chứng minh.

## 5. Mẫu pnp: lấy checklist, bỏ giá trị đoán

Mẫu yêu cầu method/path, tham số, body, response, status và auth; có hướng dẫn xử lý model ở file khác. Tuy nhiên, phần đầu đặt Base URL và Bearer auth mặc định khi thiếu thông tin. Đây là mẫu hướng dẫn, không có runtime kiểm source, độ phủ hoặc độ đúng. [API Docs Generator](https://github.com/pnp/copilot-prompts/blob/ce4596399aa07af052ae4c032043e9e238ede230/samples/skills/api-docs-generator/SKILL.md)

**Áp dụng:** dùng checklist làm đầu vào soát thiếu cho A01/A02. A03 bắt buộc unknown kèm lý do hoặc inferred có quy tắc đủ điều kiện. Không chép mẫu URL, auth, response hay lỗi minh họa thành dữ kiện của repository.

## 6. Quyết định thiết kế đề xuất

Chỉ học cơ chế phù hợp; tiếp tục triển khai trên Python của dự án hiện tại. Chưa có căn cứ phải chuyển framework agent hoặc fork toàn bộ một repo.

| Vấn đề | Thiết kế cho FR-029 | Nhiệm vụ |
|---|---|---|
| Agent đọc sót file/đoạn | Danh mục snapshot đầy đủ; đọc theo phần; lưu khoảng đã gửi và phản hồi đã xử lý | N2, N3 |
| Có source link nhưng kết luận sai | Evidence theo field + kiểm cấu trúc + gold độc lập về ngữ nghĩa | N1, N4, V1 |
| Context quá lớn | Chia lượt đọc cơ học; sổ dữ kiện/tham chiếu; đọc lại source khi cần | N3 |
| Ngân sách hết trước khi đọc xong | Trạng thái partial; phần còn thiếu hiện rõ; không tự fallback extractor | N3, V2 |
| Markdown và OpenAPI khác nhau | Một tập dữ kiện đã kiểm; hai cách trình bày; kiểm chéo độc lập | A01–A03, V1 |
| Tài liệu lệch kiến trúc | So route/owner/snapshot sau phân tích; không lấy route upstream làm đáp án | A04 |
| Gán vai trò theo tên file | Thứ tự vai trò theo FR; Service cần bằng chứng đường gọi | A07 |
| HTTP động bị đoán URL | Tách URL, khóa cấu hình và phần chỉ biết lúc chạy | A08 |

Đây là thiết kế đề xuất từ nghiên cứu. Chưa có số đo chứng minh đạt 8 AC; phiên này không sửa code sản phẩm.

## 7. Nguồn checklist luật framework (bổ sung 07/10/2026)

Mục này ghi nguồn để lập ca kiểm và gold cho A01, A02 và A08. Đây là nguồn checklist, không phải code đưa vào luồng agent.

| Nguồn | Nội dung dùng được | Đã kiểm |
|---|---|---|
| [CodeQL `FastApi.qll`](https://github.com/github/codeql/blob/main/python/ql/lib/semmle/python/frameworks/FastApi.qll) | Nhận `FastAPI`, `APIRouter` và lớp con; route qua decorator động từ HTTP, `api_route`, `websocket`. Không tính prefix của `include_router` | Đọc file ở nhánh `main`, chưa ghim commit |
| [CodeQL `Httpx.qll`](https://github.com/github/codeql/blob/main/python/ql/lib/semmle/python/frameworks/Httpx.qll) | Dạng gọi: hàm module, Client/AsyncClient và lớp con, `request`/`stream`. URL ở `url=`, đối số thứ hai với `request`/`stream`, còn lại đối số đầu. Method lấy theo tên hàm | Như trên |
| CodeQL `Requests.qll`, `Aiohttp.qll` (cùng thư mục) | Dạng gọi của `requests` và `aiohttp` | Mới xác nhận file tồn tại, chưa đọc |
| [route-detect](https://github.com/mschwager/route-detect) (BSD-3) | Luật Semgrep tìm route FastAPI; dùng làm nguồn ca âm/dương | Đọc README |
| Source FastAPI: `routing.py`, `dependencies/utils.py`, `openapi/utils.py` | Ghép prefix, vị trí tham số, gộp tham số `Depends`, status mặc định | Chưa đọc; phải ghim version ở N1 rồi đọc |
| Tài liệu Pydantic v1, v2 | Khác nhau của `Optional` không có default về required/nullable | Chưa đọc |
