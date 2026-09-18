---
uid: "01M2J06Z3SMZD88VJ6YYGF4Y68"
key: "OQ-L3GEN-005"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "closed"
revision: 8
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Khiêm và Hoàng"
due: "2026-09-19"
change_set: "CHG-L3GEN-2026-001"
---

# OQ-L3GEN-005 — Chốt môi trường web, dữ liệu và AI

## Quyết định cuối cùng ngày 18/09/2026

**Người quyết định:** Khiêm và Hoàng trong phạm vi quyền mentor đã trao cho nhóm.

- Web phase đầu chạy trên máy cá nhân/local workspace tin cậy, không công khai Internet và không multi-tenant.
- Chỉ nhận GitHub public qua HTTPS và ZIP; giữ allowlist, chống SSRF/redirect, traversal, symlink và decompression bomb theo NFR SEC/PERF.
- AI mặc định tắt, người dùng chủ động bật. Provider cấu hình qua adapter được công bố, key chỉ tồn tại lúc chạy và không được ghi vào output/log/evidence.
- Phase đầu chỉ dùng quota miễn phí, với trần chi phí trả phí bằng **0 đồng**. Hết quota, thiếu key/SDK hoặc không áp được cap thì chạy lõi tĩnh và cảnh báo, không coi là lỗi toàn phiên.
- Dữ liệu hết hạn không được phục vụ. Khi dịch vụ đang chạy, dữ liệu phải được dọn đúng hạn; nếu máy tắt qua hạn, lần khởi động tiếp theo phải cleanup trước khi phục vụ dữ liệu. UI/help phải công khai giới hạn xóa vật lý này.
- Quy tắc nhận diện repository, terminal run, eviction, source digest và xóa dữ liệu tại NFR-L3GEN-PRIV-001 được chấp nhận. Phase đầu không cam kết SLA xóa vật lý tuyệt đối khi máy tắt.

AC/NFR liên quan đã được rà và đồng bộ. Quyết định phạm vi không thay thế threat model, canary test, cleanup test hoặc bằng chứng nghiệm thu khi triển khai. OQ này không còn chặn FR/NFR; mentor tiếp tục là reviewer/cố vấn.

## Câu hỏi cần người quyết định

Product đã chốt, đã vào PRD mục IV và các NFR liên quan:

- Chỉ hỗ trợ GitHub public. Repository private và mọi cơ chế nhận hoặc lưu credential nằm ngoài phạm vi.
- Không có đăng nhập, SSO hoặc multi-tenant public hosting.
- AI mặc định tắt, phải chủ động bật. Phần lõi chạy đầy đủ khi không có AI.
- Dòng lệnh chạy cục bộ, không cần web server và không cần mạng.
- Hạn giữ dữ liệu và giới hạn lịch sử theo NFR-L3GEN-PRIV-001; Product đã chốt con số.

Trong lần rà ban đầu, bốn câu hỏi sau được đặt ra cho Tech Lead và Security:

1. Web triển khai ở đâu: máy cá nhân, máy nội bộ của nhóm, hay môi trường được cấp. Việc này ảnh hưởng NFR-L3GEN-SEC-001 và cách đo NFR-L3GEN-PERF-001.
2. Allowlist domain khi lấy source từ GitHub, và threat model cho luồng tiếp nhận ZIP.
3. Provider AI nào được phép, ai trả chi phí và trần chi phí là bao nhiêu.
4. Môi trường được chọn có đáp ứng được hạn giữ dữ liệu đã chốt không. Nếu không, phải đổi môi trường chứ không hạ yêu cầu riêng tư.

## Trả lời bốn mục còn lại, ngày 17/09/2026

**Người trả lời và owner tại thời điểm đó:** Khiêm, ngày 17/09/2026. Quyền quyết định sau đó được xác nhận tại OQ-L3GEN-001; Hoàng cùng tham gia quyết định đóng ngày 18/09/2026.

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
  công cụ nhận key lúc chạy để xác thực với provider, không ghi log hoặc lưu bền key.
- Đồ án dùng bậc miễn phí; điều đó **không** trở thành cam kết rằng gửi source đi là an toàn cho
  mọi người dùng. Người dùng chịu trách nhiệm với điều khoản của provider họ chọn, gồm cả việc
  dữ liệu có bị dùng để huấn luyện hay không.
- Giữ nguyên ràng buộc đã có ở NFR-L3GEN-AI-001: AI mặc định tắt, phần lõi chạy đủ khi không có AI;
  chỉ gọi qua adapter được công bố và khi áp được giới hạn chi phí.
- Phase đầu chỉ dùng quota miễn phí; trần chi phí trả phí là 0 đồng.

**4. Hạn giữ dữ liệu.**
Máy cá nhân được chấp nhận với điều kiện dữ liệu hết hạn không được phục vụ và startup phải cleanup trước khi phục vụ dữ liệu nếu máy từng tắt qua hạn. Đây là yêu cầu cần kiểm khi triển khai, chưa phải bằng chứng đã đạt. Không hạ yêu cầu riêng tư để hợp với môi trường.

## Kết quả rà AC/NFR, ngày 17/09/2026

Đã rà từng artifact bị ảnh hưởng. Bốn quyết định phần lớn **đã được phủ sẵn**; chỉ một chỗ hở.

| Quyết định | Đã phủ ở đâu | Cần sửa |
|---|---|---|
| 1. Máy cá nhân | NFR-L3GEN-SEC-001 "web local/workspace tin cậy, không công khai Internet"; NFR-L3GEN-PERF-001 "đo trên máy công bố, không ngoại suy từ máy khác" | Không |
| 2. Allowlist domain | NFR-L3GEN-SEC-001 "chỉ HTTPS GitHub public; từ chối host khác, địa chỉ private/loopback/link-local và redirect trái allowlist; kiểm lại đích sau DNS/redirect" | Không |
| 2. Threat model ZIP | NFR-L3GEN-SEC-001 "đọc/giải nén chỉ trong vùng được cấp; không đi theo symlink ra ngoài"; AC-L3GEN-016-03 phủ traversal, symlink và bomb; NFR-L3GEN-PERF-001 giữ các trần | Không |
| 3. Provider AI | NFR-L3GEN-AI-001 có provider cấu hình được, adapter công bố, key runtime và trần trả phí 0 đồng; NFR-L3GEN-PRIV-001 cấm gửi credential **của repository được phân tích** | Đã đồng bộ |
| 4. Hạn giữ dữ liệu | NFR-L3GEN-PRIV-001 quy định expiry, cleanup khi đang chạy và startup cleanup nếu máy tắt qua hạn | Đã đồng bộ |

**Chỗ hở đã sửa:** không NFR nào ràng buộc **khóa API của chính công cụ**. NFR-L3GEN-PRIV-001 nói
về credential nằm trong repository được phân tích, khác hẳn khóa mà người dùng nhập để gọi AI.
Đã bổ sung vào NFR-L3GEN-AI-001 (revision 1 → 2): provider là tham số cấu hình, khóa API do người
dùng cung cấp lúc chạy và không được ghi vào output, log, evidence hay bộ kết quả lưu lại; công cụ
không phát biểu thay người dùng về mức an toàn dữ liệu của provider. Cách kiểm thêm khóa canary và
kiểm đổi provider bằng cấu hình.

Ngày 18/09/2026, NFR-L3GEN-AI-001, NFR-L3GEN-PRIV-001 và cách kiểm AC-L3GEN-017-06 được cập nhật để khóa trần trả phí 0 đồng và hành vi cleanup khi máy tắt. FR-L3GEN-012/016 cùng NFR-L3GEN-SEC/PERF đã phủ đúng quyết định nên chỉ gỡ blocker.

**Lưu ý cho Scope Gate:** NFR-L3GEN-SEC-001 ghi "chưa có kết quả kiểm" cho threat model và kiểm thử
an toàn. Quyết định ở đây là quyết định phạm vi, **không phải bằng chứng đã kiểm**.

**Đã đóng.** `status: closed` — bốn mục đều có quyết định, phần bổ sung đã được nhóm xác nhận và AC/NFR bị ảnh hưởng đã rà xong.

- **Owner:** Khiêm và Hoàng; mentor là reviewer/cố vấn.
- **Hạn trả lời đề xuất:** 19/09/2026, trước Scope Gate. Hạn cũ 17/09 đã qua mà chưa có câu trả lời; đây là hạn do nhóm tự đặt, không phải ngày mentor đã cam kết.
- **Blocking:** Không còn; blocker OQ-L3GEN-005 đã được gỡ khỏi PRD, FR-L3GEN-012/016/017 và NFR SEC/PRIV/AI.
- **Cách xử lý đã chốt:** Web phase đầu chạy local/workspace tin cậy; đổi môi trường thì phải review lại security, privacy và performance.
- **Lịch sử trước câu trả lời đầy đủ, ngày 17/09/2026.** Product đã chốt năm điểm về phạm vi truy cập và AI nêu trên. Bốn mục còn lại chưa có quyết định.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.


## Bổ sung vòng đời và xác thực ngày 17/09/2026 — lịch sử

Quy tắc chi tiết mới tại NFR-PRIV (identity repository, terminal runs, ngày hết hạn, nguồn bị xóa) ban đầu là đề xuất chờ xác nhận.

Máy cá nhân không chứng minh SLA xóa khi máy tắt. Phương án là không phục vụ dữ liệu hết hạn, cleanup trước phục vụ khi khởi động lại và công khai giới hạn xóa vật lý. Nếu về sau cần xóa vật lý đúng giờ tuyệt đối thì phải đổi sang môi trường luôn chạy. Không đánh dấu đã kiểm cleanup.

Key AI được nhận trong thời gian chạy để xác thực request tới provider; không nhận credential của repo private, không ghi key vào output/log/evidence hay lưu bền. Provider/endpoint và trần chi phí phải cấu hình trước gọi; không hứa mọi provider dùng được nếu chưa có adapter được công bố. Dùng mock để kiểm core/AI fallback trước, không cần chi phí thật cho review PRD.

Phương án này đã được Khiêm và Hoàng xác nhận ngày 18/09/2026 và được đồng bộ vào NFR-PRIV/AI cùng FR-017. Canary/cleanup vẫn phải kiểm khi có triển khai; đóng câu hỏi không có nghĩa sản phẩm đã qua kiểm thử an toàn.
