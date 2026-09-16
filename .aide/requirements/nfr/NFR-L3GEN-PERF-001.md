---
uid: 01M2MV1DYDCSSF782T0E3SWF27
key: NFR-L3GEN-PERF-001
type: non-functional-requirement
group: normative
scope: system
system: SYS-L3GEN
status: draft
revision: 1
category: performance
ownership:
  accountable_team: TEAM-L3GEN
  accountable_role: tech-lead
relations:
  constrains: [FR-L3GEN-001, FR-L3GEN-002, FR-L3GEN-003]
verified_at: 2026-09-16
verified_against: []
classification: internal
ai_assisted: true
---

# NFR-L3GEN-PERF-001 — Hiệu năng và giới hạn xử lý

## Mục đích

Đặt giới hạn quy mô đầu vào và thời gian xử lý, để người dùng biết trước hệ thống phục
vụ được repository cỡ nào, và để hệ thống có mốc dừng rõ ràng thay vì chạy vô hạn.

## Trạng thái các ngưỡng

**Đây là ngưỡng pilot, chưa phải kết quả benchmark.** Nhóm chưa đo hiệu năng trên
contract hiện tại. Các số dưới đây được chốt để có mốc triển khai và đo; sau pilot phải
xem lại bằng số đo thật.

Không trích các số này như năng lực đã được chứng minh.

## Ngưỡng

### Giới hạn đầu vào

| Hạng mục | Ngưỡng | Áp dụng khi |
|---|---|---|
| Kích thước file ZIP nén | 100 MB | Người dùng tải lên ZIP |
| Kích thước sau giải nén | 500 MB | Người dùng tải lên ZIP |
| Số file trong một lần phân tích | 50.000 | Mọi hình thức đầu vào |
| Thời gian một lần phân tích | 10 phút | Mọi hình thức đầu vào |

Vượt ngưỡng đầu vào thì từ chối trước khi phân tích, theo AC-L3GEN-001-08. Chạm ngưỡng
trong lúc phân tích thì trả kết quả partial kèm giới hạn đã chạm, theo AC-L3GEN-002-12.

### Giới hạn xử lý nội bộ

Hệ thống phải có giới hạn cấu hình được hoặc hằng số rõ cho số ứng viên mỗi lời gọi, số
giá trị mỗi ô lưu, số lượt truyền giá trị và độ dài đường bằng chứng. Chạm giới hạn nào
cũng phải được ghi vào kết quả, không được cắt trong im lặng.

## Cách đo

- Đo theo từng giai đoạn: kiểm kê, phân tích cú pháp, resolver, adapter, tổng hợp
  component và sinh output.
- Ghi số file, số byte, thời gian và bộ nhớ đỉnh cho mỗi lần chạy.
- Không cam kết độ phức tạp tuyến tính cho toàn pipeline; chi phí resolver phụ thuộc số
  quan hệ truyền giá trị chứ không chỉ số file.

## Điều kiện chấp nhận

- Repository trong giới hạn công bố phân tích xong trong 10 phút.
- Vượt giới hạn thì được từ chối hoặc trả partial có lý do, không treo và không sập.
- Mỗi lần chạy ghi lại số đo theo giai đoạn để so sánh giữa các phiên bản.

## Việc còn lại

Chạy benchmark trên tập repository pilot rồi thay ngưỡng đề xuất bằng ngưỡng có số đo.
Trước khi có kết quả đó, không ghi ngưỡng nào vào README như năng lực đã đo.
