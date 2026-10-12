# FR-029 — kết quả bổ sung ngày 02/10/2026

Đã triển khai năm task trong `HANDOFF-CODEX-FR029.md`. Chưa tuyên bố toàn bộ FR-029 đạt nghiệm thu; Architecture Gate BL-r10 vẫn chưa ký. Không commit/push, không khởi động lại server demo và không ghi đè file tại D:/FPT3.

## Những phần đã sửa

| Task | Thay đổi | Kiểm chứng |
|---|---|---|
| T1 | Báo từng lời gọi đăng ký route không qua decorator, có file/dòng | Test cảnh báo riêng từng lời gọi |
| T2 | Loại route và đường đăng ký router từ file test | Test app thật và app trong conftest cùng gắn router |
| T3 | Nhận HTTP client httpx/requests/aiohttp theo phạm vi biến; không nhận session DB chỉ theo tên; báo thư viện ngoài hỗ trợ | Test client, biến bị che/gán lại, tham số có kiểu, self.client, URL từ cấu hình |
| T4 | README liệt kê HTTP theo component, thư viện, method, đích và bằng chứng | Test xuất, escape dấu phân cách bảng, không lộ credential/header |
| T5 | Đọc response list/List/Sequence/set của Pydantic model; xuất array/items trong OpenAPI | Test decorator và return annotation, OpenAPI validator |

HTTP call_text giữ source expression khi an toàn; đối số credential/header được che. Không thực thi repository đầu vào, không gọi LLM hoặc mạng ngoài.

## Kết quả kiểm

- 11 test mới qua, gồm nhiều subcase. Toàn bộ suite: **187/188 test qua**. Một lỗi có sẵn `test_gateway.Gateway.test_unknown_ids_are_dropped` giữ nguyên theo quyết định đã ghi trong bàn giao; trước sửa là 176/177.
- Kiểm contract: 8 draft contract, 7 JSON Schema, 136 reference, 71 link, 20 ví dụ dương và 31 ca âm qua. Đây là kiểm cấu trúc, không phải nghiệm thu accuracy.
- Baseline BL-r10: 34 artifact khớp hash/revision/key/UID. Không tạo hoặc thay chữ ký duyệt.
- Golden development 38 case: trước/sau cùng route TP/FP/FN = 61/0/0; reference 84/0/1; entity 18/0/4; cột 108/0/0. Gold còn candidate, chưa review độc lập. Không báo tỷ lệ nghiệm thu.
- Bốn repo development: rhoboro 11, template 23, realworld 19, teamhide 5 route; tổng 58 trước/sau. Chỉ kiểm số và đầu ra, không tự coi đây là 58 route được nghiệm thu độc lập.
- Cả bốn repo có 0 http_call/ROUTE_NOT_DECORATOR/HTTP_LIBRARY_UNSUPPORTED trong phép chạy này; khả năng mới của các nhánh này được kiểm bằng fixture dương/âm, chưa được chứng minh trên bốn repo đó.
- Teamhide: `GET /api/v1/user` đã có `list[GetUserListResponseDTO]`, cả bảng và OpenAPI; xuất được sáu artifact ready. Auth vẫn unknown, dialect vẫn unknown; không lấp dữ liệu thiếu bằng suy đoán.

## File để xem

- Code: `slice/l3slice/extract.py`, `slice/l3slice/render.py`.
- Test: `slice/tests/test_fr029.py`.
- Log mới nhất: `ket-qua-chay/fr029-20261002/tests-final.log` (188 test); `tests.log` là lượt kiểm trung gian 187 test.
- Số đo bốn repo: `ket-qua-chay/fr029-20261002/real-before/summary.json`, `real-after/summary.json`.
- Golden: `ket-qua-chay/fr029-before-20261002/summary.json`, `fr029-after2-20261002/summary.json`. Thư mục after đầu là lần chạy bị lỗi trước khi sửa; không dùng như kết quả hoàn tất.
- Bộ Teamhide mới: `ket-qua-chay/fr029-20261002/teamhide-export/`.
- Script tái hiện: `run_checks.py`, `measure_repos.py`, `export_teamhide.py` cùng thư mục kết quả. Các phép đo yêu cầu thư mục output mới; không ghi đè lần cũ. Script export dùng membership đã có ở D:/FPT3/result.json và xác nhận snapshot khớp, chỉ là fixture membership, không phải thuật toán component đã duyệt.

## Chưa hoàn tất của FR-029

- AC-029-04: đối chiếu route/component với archdia.json của pipeline chung.
- AC-029-07 và phần Cấu trúc component của AC-029-06: nhận vai trò file từ CMP-005 của Khiêm.
- Chưa kết luận toàn bộ các biến thể tham số và model của AC-029-01/02 đã được bao phủ; thay đổi này chỉ hoàn tất phạm vi T1–T5.
- Test gateway cũ, parser Python 3.14, UI và chính sách component không thuộc phạm vi sửa.

## Hồ sơ và giới hạn quy trình

Epic/Story/Task, context, plan và diary ở `.aide/lifecycle/` và `.aide/evidence/`. Các plan r1 được tạo trước sửa production nhưng lỗi dấu tiếng Việt do PowerShell; giữ nguyên r1 và có r2 đính chính. Context r2 cập nhật hash contract API-004 r6. Không giả rằng đã chạy aide CLI hoặc có review độc lập. PRD/FR/NFR/CMP/ADR nguồn không sửa.
