---
uid: "01M2J06Z4FXRF64RR15V4TZY6T"
key: "FR-L3GEN-008"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 7
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001","GOAL-L3GEN-003"],"constrained_by":["NFR-L3GEN-ABST-001","NFR-L3GEN-COMP-001","NFR-L3GEN-DET-001","NFR-L3GEN-PERF-001","NFR-L3GEN-REL-001","NFR-L3GEN-TRACE-001","NFR-L3GEN-USA-001"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-008 — Xuất và sử dụng bộ kết quả

## Mô tả

Người dùng nhận tài liệu đọc được và JSON có cấu trúc cho công cụ khác, cùng thông tin phiên bản và phạm vi lần chạy.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Tài liệu và tích hợp |
| Ưu tiên đề xuất | Must Have |
| Mốc bắt đầu đề xuất | M1: xuất dữ kiện ban đầu; M2: tích hợp component/L3 |
| Mốc nghiệm thu đầy đủ đề xuất | M3: sau khi tích hợp config/event từ FR-L3GEN-014/015; tất cả AC của FR này phải đạt |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-008-01

- **Given:** Phân tích hoàn tất ở chế độ không AI.
- **When:** người dùng mở output.
- **Then:** có tài liệu L3 Markdown, mô hình kiến trúc dạng JSON và mã nguồn sơ đồ Mermaid; biểu diễn được component cùng quan hệ API/DB/event theo FR-L3GEN-011. Bộ kết quả có bằng chứng, giới hạn phân tích và thông tin lần chạy phân biệt với dữ kiện chuẩn; danh sách cảnh báo có thể rỗng.
- `constrained_by:` [NFR-L3GEN-REL-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu nội dung theo FR-L3GEN-011 và cảnh báo theo FR-L3GEN-009. Tên, số lượng file và schema chi tiết chốt ở contract; không bắt buộc tách mô hình thành nhiều file JSON.

### AC-L3GEN-008-02

- **Given:** Người dùng nhập mô hình kiến trúc vào bộ đọc JSON và mã nguồn sơ đồ vào renderer Mermaid mục tiêu.
- **When:** người dùng đọc/xem kết quả.
- **Then:** JSON hợp lệ, ID không trùng, cạnh không treo đích, khai phiên bản schema; Mermaid render được với tên có dấu/ký tự đặc biệt.
- `constrained_by:` [NFR-L3GEN-COMP-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Renderer/version và schema cụ thể chốt ở contract sau Scope Gate.

### AC-L3GEN-008-03

- **Given:** Graph có nhiều thành phần.
- **When:** người dùng xem sơ đồ rút gọn.
- **Then:** báo rõ quy tắc rút gọn và phần bị ẩn; JSON giữ dữ liệu đầy đủ trong phạm vi đã phân tích.
- `constrained_by:` [NFR-L3GEN-TRACE-001, NFR-L3GEN-USA-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Không dùng sơ đồ rút gọn để tính coverage.

### AC-L3GEN-008-04

- **Given:** Người dùng chạy lại cùng source snapshot và cấu hình ở thư mục output khác.
- **When:** người dùng so sánh dữ liệu chuẩn.
- **Then:** nội dung cấu trúc và ID ổn định theo NFR determinism; timestamp/duration của từng lần chạy không bị làm giả để đạt byte equality.
- `constrained_by:` [NFR-L3GEN-DET-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Kiểm hash chuẩn hóa, giữ metrics thật trong metadata.

## Trạng thái liên kết triển khai

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-ABST-001](../nfr/NFR-L3GEN-ABST-001.md)
- [NFR-L3GEN-DET-001](../nfr/NFR-L3GEN-DET-001.md)
- [NFR-L3GEN-TRACE-001](../nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-REL-001](../nfr/NFR-L3GEN-REL-001.md)
- [NFR-L3GEN-USA-001](../nfr/NFR-L3GEN-USA-001.md)
- [NFR-L3GEN-COMP-001](../nfr/NFR-L3GEN-COMP-001.md)
- [NFR-L3GEN-PERF-001](../nfr/NFR-L3GEN-PERF-001.md)
- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../../domain/glossary-core.md)

