---
uid: "01M34AM2AKW0142NJS913FEHT7"
key: "NFR-L3GEN-AI-001"
type: "non-functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"constrains":["FR-L3GEN-003","FR-L3GEN-004","FR-L3GEN-006"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# NFR-L3GEN-AI-001 — Ranh giới, chi phí và truy vết của mô hình ngôn ngữ

- **Nhóm:** AI reliability.
- **Trạng thái:** hướng đã chốt ngày 22/09/2026; provider, model và trần kích thước repository chờ OQ-L3GEN-008. Chưa đo nghiệm thu.
- **Áp dụng:** [FR-L3GEN-003](../fr/FR-L3GEN-003.md), [FR-L3GEN-004](../fr/FR-L3GEN-004.md), [FR-L3GEN-006](../fr/FR-L3GEN-006.md).

## Yêu cầu có thể kiểm chứng

Gộp phần ranh giới AI trước đây ở NFR-AI-001 với phần tái lập ở NFR-DET-001, sau khi tái lập bị hạ xuống mức ghi nhận.

**Ranh giới.** Mô hình ngôn ngữ chỉ nhận tập dữ kiện code đã trích kèm vị trí file, không nhận toàn bộ source repository. Kết quả model trả về phải đúng schema đã định; phần sai schema, trỏ tới file không có trong snapshot, hoặc tham chiếu định danh không tồn tại thì bị loại và ghi lý do loại.

**Chi phí.** Chỉ dùng model qua API. Phase đầu giới hạn ở quota miễn phí với trần chi phí trả phí bằng 0 đồng. Hết quota, bị rate limit, thiếu key hoặc chạm trần thì dừng bước dựng quan hệ kiến trúc và báo rõ, không tự chuyển sang phương án tính tiền và không đoán để lấp chỗ trống. Mỗi lần chạy có trần số request và timeout cho mỗi request.

**Bí mật.** Khóa API do người dùng cung cấp lúc chạy, không được ghi vào output, log, bằng chứng hay bộ kết quả lưu lại. Công cụ không phát biểu thay người dùng về mức an toàn dữ liệu của provider họ chọn.

**Tái lập.** Kết quả không bắt buộc giống hệt giữa các lần chạy. Bù lại, mỗi lần chạy phải ghi lại provider, tên model, phiên bản prompt, phiên bản tool và định danh snapshot, đủ để dựng lại bối cảnh của một kết quả cũ. Đây là yêu cầu ghi nhận, không phải ngưỡng chặn phát hành.

## Điều kiện và cách kiểm

Dùng provider giả trả về JSON hỏng, định danh lạ, đường dẫn không tồn tại, timeout và lỗi rate limit; kiểm rằng phần không hợp lệ bị loại và lý do được ghi. Đặt khóa API dạng đánh dấu rồi kiểm toàn bộ output, log và bằng chứng không chứa giá trị đó. Kiểm đổi provider bằng cấu hình mà không sửa code. Kiểm mỗi bộ kết quả có đủ trường truy vết đã nêu. Không dùng giá hoặc model giả định để kết luận về chi phí.

## Người chốt và ngoại lệ

Product cùng Tech Lead/QA chốt ở Scope Gate. Không có waiver nào được cấp sẵn. Chưa đạt thì ghi kết quả failed hoặc not_run, thu hẹp phạm vi qua review, hoặc sửa sản phẩm; không tự hạ ngưỡng sau khi đã đo.

## Liên kết

- [Phương pháp đo](../../observability/OBS-L3GEN-001.md)
- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
