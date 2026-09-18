---
uid: "01M2J06Z3VNH1Y1S9Y9PAWFCDW"
key: "OQ-L3GEN-006"
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

# OQ-L3GEN-006 — Xác nhận quy trình và schema khi thiếu tooling

## Quyết định cuối cùng ngày 18/09/2026

**Người quyết định:** Khiêm và Hoàng trong phạm vi quyền mentor đã trao cho nhóm. Nhóm chọn phương án dùng chuẩn nội bộ có giới hạn cho Gate 1:

1. Dùng schema, key và UID hiện tại làm chuẩn nội bộ của dự án. Giữ UID ổn định; chỉ migration bằng change riêng nếu sau này có policy/registry chính thức yêu cầu.
2. Chấp nhận `scripts/prd_package.py` và `scripts/impact.py` làm tooling cục bộ cho Gate 1. Không gọi kết quả của chúng là kiểm tra `aide`/`check-sdlc` chính thức hoặc bằng chứng tuân thủ cấp tổ chức.
3. Chấp nhận impact dựng từ frontmatter để review phạm vi yêu cầu, giữ nguyên công bố `confidence: low`, `skipped_with_reason` và giới hạn về consumer ngoài repository/source code chưa quét.
4. Tại Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component, contract và test ID được tạo ở thiết kế/planning sau đó. Hai mapping phải hoàn tất trước Definition of Ready cho code; không tạo ID giả.
5. Giữ `flow: new-system`, `tier: T1`, `coordination.mode: independent` và `integration_gate_required: false`. T1 là lựa chọn kiểm soát chặt cho hệ thống nhận source từ xa, không phải waiver.
6. Áp dụng nguyên tắc Agent chịu trách nhiệm chính cho production code; human đặc tả, cung cấp constraint, review và kiểm chứng. Không bắt buộc lưu mọi prompt. Mỗi task implementation phải truy được tới spec/AC, plan/context, diff hoặc MR, test evidence và nhật ký quyết định của Agent. Nếu human sửa production code để unblock thì ghi rõ lý do, phạm vi file, cách kiểm và bài học cần đưa ngược vào spec/instruction/test.

Quyết định này đủ để đóng OQ-006 và chuẩn bị candidate Gate 1, nhưng không biến tooling cục bộ thành chuẩn chính thức của tổ chức. Mentor tiếp tục là reviewer/cố vấn.

## Câu hỏi cần người quyết định

Tại thời điểm mở câu hỏi, chưa có bản PROC-SDLC-001, registry hay mẫu NFR/OBS đầy đủ trong attachment. Tài liệu quy trình nhận được nằm ở [docs/sdlc-sources/](../../../../../docs/sdlc-sources/), trong đó phần mẫu PRD và execution guide có, còn PROC và registry thì không. Câu hỏi nhằm xác nhận bộ schema tạm, trình tự Scope Gate trước design/test mapping, quy tắc hash/UID và cách lưu evidence khi không có công cụ `aide`.

1. Ai cung cấp registry/policy và xác nhận type/edge, mã, `coordination.mode`, checklist và quyền ký trước Scope Gate?
2. New System chưa có graph đầy đủ thì khởi tạo và sinh impact thế nào? Nếu dùng cách thay thế, ai chấp nhận và lưu bằng chứng ra sao? Hiện intake/impact chưa chạy; không tự viết `impact.yaml` rồi đánh dấu hoàn tất.
3. Mẫu PRD DoD yêu cầu AC→implementation_target, trong khi trình tự B/C đặt thiết kế/planning sau Scope Gate. Cần xác định mapping bắt buộc ở gate nào; helper local không thay `check-sdlc` chính thức.
4. Chốt cách làm vertical slice hoặc golden example phù hợp giới hạn human production code của đề bài.
5. Không có công cụ cấp ULID. UID của các artifact mới được sinh bằng script tạm theo định dạng Crockford base32, không phải bằng lệnh `aide`. Nếu tổ chức có công cụ chính thức, các UID này cần được cấp lại.
6. Script đóng gói hồ sơ không có trong repository. [docs/PRD-REVIEW-README.md](../../../../../docs/PRD-REVIEW-README.md) nhắc tới `scripts/prd_package.py` để render Change Set View và chạy kiểm gói, nhưng file đó không tồn tại trên nhánh này. Vì vậy hai file trong `generated/` đang là bản render theo baseline cũ và đã được đánh dấu lỗi thời. Cần biết script nằm ở đâu, hoặc chấp nhận rằng phần `generated/` được duy trì bằng tay.

**Lịch sử cập nhật:** ở revision 2 từng hỏi về NFR một theme. Bản dự thảo NFR-USA revision 2 đã bỏ đề xuất này và theo checklist sáng/tối của mentor. Đây là sửa hồ sơ theo nguồn, không phải câu trả lời hoặc waiver do mentor cấp; OQ-006 vẫn mở cho các vấn đề trên.

- **Owner:** Khiêm và Hoàng; mentor là reviewer/cố vấn.
- **Hạn trả lời đề xuất:** 19/09/2026, trước Scope Gate. Hạn cũ 17/09 đã qua mà chưa có câu trả lời; đây là hạn do nhóm tự đặt, không phải ngày mentor đã cam kết.
- **Blocking:** Không còn. Candidate vẫn phải khớp hash và vượt kiểm tra cục bộ trước khi Khiêm ký Scope Gate.
- **Cách xử lý:** Dùng chuẩn nội bộ đã chốt ở trên và công khai giới hạn. Không tuyên bố đã pass `check-sdlc` chính thức hoặc đã có approval khi Scope Gate chưa được ký.
- **Trả lời:** Đã chốt phương án B ngày 18/09/2026.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.


## Cập nhật thực tế và đề nghị ngày 17/09/2026 — lịch sử

Đã có scripts/prd_package.py (render/check), scripts/impact.py và impact graph cục bộ; không còn thiếu script đóng gói. Các đoạn trên mô tả tình trạng trước khi bổ sung công cụ, không phải trạng thái hiện tại. Intake đã ghi ở mức nhóm, role_confirmed=false; chưa có Scope Gate. Bản kiểm cục bộ không thay registry/check-sdlc chính thức.

Đề xuất xin chấp nhận cho giai đoạn draft: ULID sinh bằng công cụ Python; SHA-256 bytes làm snapshot; CSV sinh từ baseline; impact từ frontmatter công khai giới hạn. Giữ UID ổn định đã cấp, chỉ migration nếu chính sách tổ chức yêu cầu rõ, không cấp lại tùy tiện.

Các câu hỏi từng gửi mentor:
1. Bộ schema/mã và công cụ cục bộ trên có được dùng cho review draft không? Nếu không, xin nguồn PROC/registry/tooling và tiêu chí cần bổ sung.
2. Scope Gate có cho phép implementation_target/validated_by chưa điền trước thiết kế không, và thời điểm bắt buộc hoàn thành mapping là bước nào?
3. Ai xác nhận tier/flow và giới hạn impact khi chưa có graph tập trung?
4. Quy tắc human production code áp dụng thế nào cho vertical slice/golden example của nhóm?

Phương án này đã được Khiêm và Hoàng chấp nhận ngày 18/09/2026 theo quyền mentor trao cho nhóm. Mentor không còn là người ký bắt buộc; vẫn có thể review và khuyến nghị thay đổi qua một revision/change riêng.
