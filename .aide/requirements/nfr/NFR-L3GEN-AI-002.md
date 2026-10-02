---
uid: "01M34AM2AKW0142NJS913FEHT7"
key: "NFR-L3GEN-AI-002"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 6
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-028"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-AI-002 — Ranh giới, chi phí và truy vết của mô hình ngôn ngữ

- **Nhóm:** AI reliability.
- **Trạng thái:** revision 4 theo quyết định của Khiêm ngày 02/10/2026 (CR-L3GEN-2026-004, OQ-L3GEN-009): model bắt buộc, trả phí ít, qua OpenRouter. Revision 5 (02/10/2026) sửa theo review REVIEW-SCOPE-L3GEN-2026-002: trần chi phí và token do Khiêm chốt khi đóng OQ-L3GEN-009; bỏ việc chọn chủ bảng (bảng theo file khai báo model, FR-L3GEN-028); mỗi loại lỗi câu trả lời một đường xử lý. Revision 6 (02/10/2026): Khiêm chốt số request, độ dài câu trả lời và timeout (finding F13 của REVIEW-SCOPE-L3GEN-2026-003). Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-028](../fr/FR-L3GEN-028.md).

## Yêu cầu có thể kiểm chứng

Thay revision 3 (Groq và Google, gói miễn phí, trần chi phí 0 đồng).

**Việc của model.** Model nhận kết quả code đã lần theo và trả về: các nhóm route cùng trách nhiệm nghiệp vụ cần gộp; tên và một câu trách nhiệm cho mỗi component; tên dùng chung nào thuộc riêng một component. Mỗi quyết định trỏ một mã dòng code đã hiện cho model. Model không tách nhóm route, không thêm mũi tên, không sửa dữ kiện code và không tự công bố kết luận.

**Đầu vào gửi cho model.** Danh sách nhóm route (method, path, bảng và hệ thống ngoài mỗi route chạm, dòng khai báo route), tên dùng chung kèm dòng khai báo, số lời gọi giữa các nhóm. Mỗi dòng code gửi đi mang một mã `[L12]`; model trả mã, code tra ra `file:dòng` và nguyên văn. Không gửi nguyên file source hoặc cả repository.

**Kiểm câu trả lời.** Code kiểm: câu trả lời đúng schema; mỗi nhóm route thuộc đúng một component và không bị tách; tên dùng chung dùng tối đa một lần; mã dòng có trong danh sách đã gửi. Mỗi loại lỗi một đường xử lý:

| Lỗi | Xử lý |
|---|---|
| JSON hỏng hoặc sai schema | Gửi lại một lần kèm lỗi. Vẫn sai thì bỏ cả câu trả lời, giữ cách chia của code, trạng thái partial (AC-L3GEN-028-08) |
| Đúng schema nhưng vi phạm luật kiểm | Gửi lại một lần kèm danh sách lỗi. Vẫn sai thì loại phần vi phạm, giữ phần hợp lệ, ghi lý do (AC-L3GEN-028-05) |

**Provider và model.**

| Thuộc tính | Giá trị |
|---|---|
| Provider | OpenRouter |
| Model | `openai/gpt-6-luna` |
| Mức suy luận | trung bình |
| Tham số `temperature` | không gửi (model không nhận) |

Đổi model hoặc provider bằng cấu hình, không sửa code; mỗi lần đổi ghi vào provenance và chạy lại phép đo của OBS-L3GEN-001.

**Trần mỗi lần chạy.**

| Trần | Giá trị |
|---|---|
| Chi phí | ≤ 0,20 USD |
| Token vào và ra cộng lại | ≤ 300.000 |
| Request | ≤ 4 (một lần hỏi, một lần gửi lại, mỗi lần thử lại tối đa một lần khi lỗi mạng) |
| Độ dài câu trả lời | ≤ 12.000 token mỗi request |
| Timeout | 300 giây mỗi request |

Chi phí và token do Khiêm chốt tại OQ-L3GEN-009 ngày 02/10/2026. Số request, độ dài câu trả lời và timeout: Khiêm chốt ngày 02/10/2026, giữ như revision 4. Công cụ ước tính token trước request đầu tiên; vượt trần thì không gọi model và xử lý theo AC-L3GEN-028-08. Số tham khảo khi phát triển: 7 request trên 5 repo nhỏ, khoảng 25.000 token, 0,008 USD (02/10/2026).

**Thiếu model.** Thiếu khóa, hết ngân sách, chạm trần, provider lỗi, hoặc vẫn sai schema sau lần gửi lại thì dừng bước dùng model, giữ kết quả do code chia, trạng thái partial kèm nguyên nhân (AC-L3GEN-028-08). Không tự đổi sang model khác, không đoán để lấp chỗ trống.

**Bí mật.** Khóa API do người dùng cung cấp lúc chạy, không được ghi vào output, log, bằng chứng hay bộ kết quả lưu lại. Dòng code chứa giá trị bí mật được che trước khi vào payload gửi model, theo NFR-L3GEN-SEC-002.

**Tái lập.** Kết quả không bắt buộc giống hệt giữa các lần chạy. Mỗi lần chạy ghi provider, tên model, phiên bản prompt, phiên bản tool, định danh snapshot, số request, token và chi phí. Đây là yêu cầu ghi nhận, không phải ngưỡng chặn phát hành.

## Điều kiện và cách kiểm

Dùng provider giả trả về JSON hỏng, mã dòng lạ, nhóm route dùng hai lần, timeout và lỗi mạng; kiểm phần không hợp lệ bị loại, lý do được ghi, và lần gửi lại có kèm lỗi. Đặt khóa API dạng đánh dấu rồi kiểm toàn bộ output, log và bằng chứng không chứa giá trị đó. Kiểm mỗi bộ kết quả có đủ trường truy vết. Chi phí lấy từ số provider trả về, không ước bằng giá giả định.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [OQ-L3GEN-009](../../lifecycle/change-sets/CHG-L3GEN-2026-002/open-questions/OQ-L3GEN-009.md)
