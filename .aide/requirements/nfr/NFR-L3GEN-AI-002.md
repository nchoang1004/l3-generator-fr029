---
uid: "01M34AM2AKW0142NJS913FEHT7"
key: "NFR-L3GEN-AI-002"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-021","FR-L3GEN-022","FR-L3GEN-024"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-AI-002 — Ranh giới, chi phí và truy vết của mô hình ngôn ngữ

- **Nhóm:** AI reliability.
- **Trạng thái:** hướng đã chốt ngày 22/09/2026; provider, model và trần mỗi lần chạy chốt tại OQ-L3GEN-008 ngày 23/09/2026. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-021](../fr/FR-L3GEN-021.md), [FR-L3GEN-022](../fr/FR-L3GEN-022.md), [FR-L3GEN-024](../fr/FR-L3GEN-024.md).

## Yêu cầu có thể kiểm chứng

Thay cho NFR-L3GEN-AI-001 và NFR-L3GEN-DET-001 của BL-r14; tái lập hạ xuống mức ghi nhận.

**Ranh giới.** Mô hình ngôn ngữ chỉ nhận tập dữ kiện code đã trích kèm vị trí file, không nhận toàn bộ source repository. Model chỉ đề xuất component, vai trò và cạnh; nó không sửa dữ kiện code và không tự công bố kết luận. Kết quả model trả về phải đúng schema đã định; phần sai schema, trỏ tới file không có trong snapshot, tham chiếu định danh không tồn tại, hoặc không qua bước kiểm bằng chứng của NFR-L3GEN-ACC-002 thì bị loại và ghi lý do loại.

**Provider và model phase đầu.** Groq, model `openai/gpt-oss-120b`, gói miễn phí. Giới hạn gói do Khiêm cung cấp ngày 23/09/2026: 30 request/phút, 1.000 request/ngày, 8.000 token/phút, 200.000 token/ngày. Giới hạn này do Groq đặt và có thể đổi; công cụ đọc lỗi rate limit thực tế thay vì tin con số ghi ở đây.

**Trần mỗi lần chạy.**

| Trần | Giá trị | Lý do |
|---|---|---|
| Token mỗi lần chạy, vào và ra cộng lại | ≤ 100.000 | Một nửa quota ngày, chừa chỗ cho một lần chạy lại |
| Token mỗi request | ≤ 6.000 | Dưới trần 8.000 token/phút của gói |
| Request mỗi lần chạy | ≤ 40 | Chặn vòng gọi không dừng |
| Timeout và thử lại | 30 giây mỗi request, thử lại tối đa 2 lần | Giữ từ BL-r14 |

Công cụ ước tính số token của tập dữ kiện trước request đầu tiên; vượt trần thì không gọi model và xử lý theo AC-L3GEN-022-03. Trần token thay cho "trần kích thước repository": model nhận tập dữ kiện chứ không nhận source, nên đơn vị đo là token. Quy đổi sang số file hoặc số dòng code chưa đo; M1 đo và công bố.

**Chi phí.** Chỉ dùng model qua API. Phase đầu giới hạn ở quota miễn phí với trần chi phí trả phí bằng 0 đồng. Hết quota, bị rate limit, thiếu key hoặc chạm trần thì dừng bước dựng quan hệ kiến trúc và báo rõ, không tự chuyển sang phương án tính tiền, không tự đổi sang model khác, và không đoán để lấp chỗ trống.

**Bí mật.** Khóa API do người dùng cung cấp lúc chạy, không được ghi vào output, log, bằng chứng hay bộ kết quả lưu lại. Công cụ không phát biểu thay người dùng về mức an toàn dữ liệu của provider họ chọn.

**Tái lập.** Kết quả không bắt buộc giống hệt giữa các lần chạy. Bù lại, mỗi lần chạy phải ghi lại provider, tên model, phiên bản prompt, phiên bản tool và định danh snapshot, đủ để dựng lại bối cảnh của một kết quả cũ. Đây là yêu cầu ghi nhận, không phải ngưỡng chặn phát hành.

## Điều kiện và cách kiểm

Dùng provider giả trả về JSON hỏng, định danh lạ, đường dẫn không tồn tại, timeout và lỗi rate limit; kiểm rằng phần không hợp lệ bị loại và lý do được ghi. Đặt khóa API dạng đánh dấu rồi kiểm toàn bộ output, log và bằng chứng không chứa giá trị đó. Kiểm đổi provider bằng cấu hình mà không sửa code. Kiểm mỗi bộ kết quả có đủ trường truy vết đã nêu. Không dùng giá hoặc model giả định để kết luận về chi phí.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
