---
uid: "01M2J06Z3SMZD88VJ6YYGF4Y68"
key: "OQ-L3GEN-005"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "answered"
revision: 6
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Khiêm"
due: "2026-09-19"
change_set: "CHG-L3GEN-2026-001"
---

# OQ-L3GEN-005 — Chốt môi trường web, dữ liệu và AI

## Câu hỏi cần người quyết định

Product đã chốt, đã vào PRD mục IV và các NFR liên quan:

- Chỉ hỗ trợ GitHub public. Repository private và mọi cơ chế nhận hoặc lưu credential nằm ngoài phạm vi.
- Không có đăng nhập, SSO hoặc multi-tenant public hosting.
- AI mặc định tắt, phải chủ động bật. Phần lõi chạy đầy đủ khi không có AI.
- Dòng lệnh chạy cục bộ, không cần web server và không cần mạng.
- Hạn giữ dữ liệu và giới hạn lịch sử theo NFR-L3GEN-PRIV-001; Product đã chốt con số.

Phần chưa chốt cần Tech Lead và Security quyết:

1. Web triển khai ở đâu: máy cá nhân, máy nội bộ của nhóm, hay môi trường được cấp. Việc này ảnh hưởng NFR-L3GEN-SEC-001 và cách đo NFR-L3GEN-PERF-001.
2. Allowlist domain khi lấy source từ GitHub, và threat model cho luồng tiếp nhận ZIP.
3. Provider AI nào được phép, ai trả chi phí và trần chi phí là bao nhiêu.
4. Môi trường được chọn có đáp ứng được hạn giữ dữ liệu đã chốt không. Nếu không, phải đổi môi trường chứ không hạ yêu cầu riêng tư.

## Trả lời bốn mục còn lại, ngày 17/09/2026

**Người trả lời và owner:** Khiêm, ngày 17/09/2026. Khiêm nhận trách nhiệm cho câu hỏi này
thay cho owner theo vai trước đó. Mentor xác nhận lại việc phân vai tại Scope Gate
(OQ-L3GEN-001); xác nhận đó không làm thay đổi bốn quyết định dưới đây.

**1. Web triển khai ở đâu → máy cá nhân.**
Không có URL công khai, không multi-tenant, không ai ngoài mạng gọi tới được. Hệ quả phải giữ:
NFR-L3GEN-PERF-001 phải đo trên chính cấu hình máy cá nhân dùng để chạy, không mượn số của máy
chủ mạnh hơn. Đổi môi trường triển khai thì phải đo lại, không giữ số cũ.

**2. Allowlist domain và threat model ZIP.**

- Chỉ nhận URL dạng `https://github.com/...`. Giữ nguyên phạm vi GitHub public mà Product đã chốt;
  GitLab và forge khác **không** thuộc phạm vi phiên bản đầu.
- Chặn địa chỉ IP thô, tên máy nội bộ và địa chỉ metadata của môi trường đám mây, kể cả khi chúng
  đến qua chuyển hướng. Chặn bằng máy, không chỉ ghi trong tài liệu.
- ZIP: từ chối mục có `..` trong đường dẫn; bỏ qua liên kết tượng trưng thay vì đi theo; đặt trần
  dung lượng sau giải nén và trần số file. Vượt trần thì dừng và báo, không giải nén tiếp.
- Con số trần lấy từ NFR-L3GEN-PERF-001 và NFR-L3GEN-SEC-001, **không ghi số vào đây**.

**3. Provider AI.**

- Provider là tham số cấu hình, không khoá cứng vào một hãng. Người dùng tự cung cấp API key;
  công cụ không nhận, không lưu và không ghi log key.
- Đồ án dùng bậc miễn phí; điều đó **không** trở thành cam kết rằng gửi source đi là an toàn cho
  mọi người dùng. Người dùng chịu trách nhiệm với điều khoản của provider họ chọn, gồm cả việc
  dữ liệu có bị dùng để huấn luyện hay không.
- Giữ nguyên ràng buộc đã có ở NFR-L3GEN-AI-001: AI mặc định tắt, phần lõi chạy đủ khi không có AI,
  chưa cấu hình trần chi phí thì không gọi AI.
- Chi phí do nhóm tự chịu trong phạm vi bậc miễn phí; chưa có ngân sách được cấp.

**4. Hạn giữ dữ liệu.**
Máy cá nhân đáp ứng được hạn giữ và giới hạn lịch sử đã chốt ở NFR-L3GEN-PRIV-001, vì dữ liệu nằm
trên máy người chạy và xoá được trực tiếp. Không hạ yêu cầu riêng tư nào để hợp với môi trường.

## Kết quả rà AC/NFR, ngày 17/09/2026

Đã rà từng artifact bị ảnh hưởng. Bốn quyết định phần lớn **đã được phủ sẵn**; chỉ một chỗ hở.

| Quyết định | Đã phủ ở đâu | Cần sửa |
|---|---|---|
| 1. Máy cá nhân | NFR-L3GEN-SEC-001 "web local/workspace tin cậy, không công khai Internet"; NFR-L3GEN-PERF-001 "đo trên máy công bố, không ngoại suy từ máy khác" | Không |
| 2. Allowlist domain | NFR-L3GEN-SEC-001 "chỉ HTTPS GitHub public; từ chối host khác, địa chỉ private/loopback/link-local và redirect trái allowlist; kiểm lại đích sau DNS/redirect" | Không |
| 2. Threat model ZIP | NFR-L3GEN-SEC-001 "đọc/giải nén chỉ trong vùng được cấp; không đi theo symlink ra ngoài"; AC-L3GEN-016-03 phủ traversal, symlink và bomb; NFR-L3GEN-PERF-001 giữ các trần | Không |
| 3. Provider AI | NFR-L3GEN-AI-001 đã có provider cấu hình được và trần chi phí; NFR-L3GEN-PRIV-001 cấm gửi credential **của repository được phân tích** | **Có** — xem dưới |
| 4. Hạn giữ dữ liệu | NFR-L3GEN-PRIV-001 xóa source tạm sau 24 giờ, giữ output tối đa 14 ngày, 10 lần mỗi repository | Không |

**Chỗ hở đã sửa:** không NFR nào ràng buộc **khóa API của chính công cụ**. NFR-L3GEN-PRIV-001 nói
về credential nằm trong repository được phân tích, khác hẳn khóa mà người dùng nhập để gọi AI.
Đã bổ sung vào NFR-L3GEN-AI-001 (revision 1 → 2): provider là tham số cấu hình, khóa API do người
dùng cung cấp lúc chạy và không được ghi vào output, log, evidence hay bộ kết quả lưu lại; công cụ
không phát biểu thay người dùng về mức an toàn dữ liệu của provider. Cách kiểm thêm khóa canary và
kiểm đổi provider bằng cấu hình.

**Không sửa:** FR-L3GEN-012, FR-L3GEN-016, FR-L3GEN-017, NFR-L3GEN-SEC-001, NFR-L3GEN-PRIV-001,
NFR-L3GEN-PERF-001. Nội dung hiện có đã đúng với bốn quyết định; sửa thêm chỉ làm trùng lặp.

**Lưu ý cho Scope Gate:** NFR-L3GEN-SEC-001 ghi "chưa có kết quả kiểm" cho threat model và kiểm thử
an toàn. Quyết định ở đây là quyết định phạm vi, **không phải bằng chứng đã kiểm**.

**Đã trả lời.** `status: answered` — bốn mục đều có quyết định và có người chịu trách nhiệm.
Chuyển sang `closed` sau khi AC/NFR bị ảnh hưởng đã rà xong và mentor xác nhận phân vai.

- **Owner:** Khiêm (nhận ngày 17/09/2026; trước đó ghi theo vai Tech Lead/Security).
- **Hạn trả lời đề xuất:** 19/09/2026, trước Scope Gate. Hạn cũ 17/09 đã qua mà chưa có câu trả lời; đây là hạn do nhóm tự đặt, không phải ngày mentor đã cam kết.
- **Blocking:** FR-L3GEN-012, FR-L3GEN-016, FR-L3GEN-017; NFR SEC/PRIV/AI.
- **Cách xử lý trong bản nháp:** Giả định workspace tin cậy hoặc local. Không viết thông số môi trường cụ thể vào NFR khi chưa biết web chạy ở đâu.
- **Trả lời một phần, ngày 17/09/2026.** Product đã chốt năm điểm về phạm vi truy cập và AI nêu trên. Bốn mục còn lại chưa có quyết định.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.

