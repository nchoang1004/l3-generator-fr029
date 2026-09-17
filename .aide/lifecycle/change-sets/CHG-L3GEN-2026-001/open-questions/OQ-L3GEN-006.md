---
uid: "01M2J06Z3VNH1Y1S9Y9PAWFCDW"
key: "OQ-L3GEN-006"
type: "open-question"
group: "normative"
scope: "lifecycle"
system: "SYS-L3GEN"
status: "open"
revision: 5
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
owner: "Người phụ trách PRD phối hợp mentor"
due: "2026-09-19"
change_set: "CHG-L3GEN-2026-001"
---

# OQ-L3GEN-006 — Xác nhận quy trình và schema khi thiếu tooling

## Câu hỏi cần người quyết định

Chưa có bản PROC-SDLC-001, registry hay mẫu NFR/OBS đầy đủ trong attachment. Tài liệu quy trình nhận được nằm ở [docs/sdlc-sources/](../../../../../docs/sdlc-sources/), trong đó phần mẫu PRD và execution guide có, còn PROC và registry thì không. Xác nhận bộ schema tạm, trình tự Scope Gate trước design/test mapping, quy tắc hash/UID và cách lưu evidence khi không có công cụ `aide`.

1. Ai cung cấp registry/policy và xác nhận type/edge, mã, `coordination.mode`, checklist và quyền ký trước Scope Gate?
2. New System chưa có graph đầy đủ thì khởi tạo và sinh impact thế nào? Nếu dùng cách thay thế, ai chấp nhận và lưu bằng chứng ra sao? Hiện intake/impact chưa chạy; không tự viết `impact.yaml` rồi đánh dấu hoàn tất.
3. Mẫu PRD DoD yêu cầu AC→implementation_target, trong khi trình tự B/C đặt thiết kế/planning sau Scope Gate. Mentor xác nhận coverage nào cần tại từng gate; mapping hiện rỗng là chưa đạt, không phải ngoại lệ đã được chấp nhận. Helper local không thay check-sdlc chính thức.
4. Chốt cách làm vertical slice hoặc golden example phù hợp giới hạn human production code của đề bài.
5. Không có công cụ cấp ULID. UID của các artifact mới được sinh bằng script tạm theo định dạng Crockford base32, không phải bằng lệnh `aide`. Nếu tổ chức có công cụ chính thức, các UID này cần được cấp lại.
6. Script đóng gói hồ sơ không có trong repository. [docs/PRD-REVIEW-README.md](../../../../../docs/PRD-REVIEW-README.md) nhắc tới `scripts/prd_package.py` để render Change Set View và chạy kiểm gói, nhưng file đó không tồn tại trên nhánh này. Vì vậy hai file trong `generated/` đang là bản render theo baseline cũ và đã được đánh dấu lỗi thời. Cần biết script nằm ở đâu, hoặc chấp nhận rằng phần `generated/` được duy trì bằng tay.

**Lịch sử cập nhật:** ở revision 2 từng hỏi về NFR một theme. Bản dự thảo NFR-USA revision 2 đã bỏ đề xuất này và theo checklist sáng/tối của mentor. Đây là sửa hồ sơ theo nguồn, không phải câu trả lời hoặc waiver do mentor cấp; OQ-006 vẫn mở cho các vấn đề trên.

- **Owner theo vai:** Người phụ trách PRD phối hợp mentor.
- **Hạn trả lời đề xuất:** 19/09/2026, trước Scope Gate. Hạn cũ 17/09 đã qua mà chưa có câu trả lời; đây là hạn do nhóm tự đặt, không phải ngày mentor đã cam kết.
- **Blocking:** Hoàn tất intake và kết luận tuân thủ/qua Scope Gate; không ngăn lấy ý kiến bản nháp PRD.
- **Cách xử lý trong bản nháp:** Giữ intake/impact/tier chưa xác nhận; xem [ghi chú intake và checklist gate](../../../../../docs/PRD-REVIEW-README.md). Mapping design/test còn trống được ghi chưa đủ điều kiện code. Không tuyên bố đã pass check-sdlc hoặc có approval.
- **Trả lời:** Chưa có.

Khi có câu trả lời, giữ câu hỏi và lịch sử, ghi người trả lời/ngày/ảnh hưởng FR-NFR. Không tự coi im lặng là đồng ý.

