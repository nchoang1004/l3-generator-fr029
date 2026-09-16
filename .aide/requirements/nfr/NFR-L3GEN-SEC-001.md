---
uid: 01M2MV1DYD6RD3Q694DMEDV6ZH
key: NFR-L3GEN-SEC-001
type: non-functional-requirement
group: normative
scope: system
system: SYS-L3GEN
status: draft
revision: 1
category: security
ownership:
  accountable_team: TEAM-L3GEN
  accountable_role: security
relations:
  constrains: [FR-L3GEN-001, FR-L3GEN-002, FR-L3GEN-003, FR-L3GEN-005]
verified_at: 2026-09-16
verified_against: []
classification: internal
ai_assisted: true
---

# NFR-L3GEN-SEC-001 — An toàn khi xử lý mã nguồn của người khác

## Mục đích

Hệ thống nhận mã nguồn từ bên ngoài, gồm cả mã nguồn mà người vận hành không kiểm soát.
Yêu cầu này đặt ranh giới để việc phân tích không trở thành đường thực thi mã lạ, không
ghi ra ngoài vùng xử lý, và không giữ dữ liệu lâu hơn cần thiết.

## Yêu cầu

### 1. Không thực thi mã nguồn đầu vào

Hệ thống chỉ đọc source dưới dạng văn bản và phân tích cú pháp. Cấm:

- import module của repository đầu vào;
- chạy source đầu vào dưới bất kỳ hình thức nào;
- gọi `exec` hoặc `eval` trên nội dung source;
- cài dependency của repository đầu vào;
- ghi, sửa hoặc xóa file trong repository đầu vào.

### 2. Giải nén archive an toàn

- Từ chối entry có đường dẫn tuyệt đối hoặc chứa thành phần đi ngược ra thư mục cha.
- Từ chối symbolic link trỏ ra ngoài vùng giải nén.
- Kiểm tra tổng kích thước sau giải nén trước khi ghi hết ra đĩa, để tránh archive nén
  nhỏ nhưng giãn rất lớn.
- Không file nào được ghi ra ngoài vùng xử lý dành riêng cho lần phân tích đó.

Giới hạn kích thước cụ thể nằm ở [NFR-L3GEN-PERF-001](NFR-L3GEN-PERF-001.md).

### 3. Không nhận và không lưu credential

- MVP chỉ truy cập repository GitHub public.
- Hệ thống không yêu cầu, không nhận và không lưu token hoặc mật khẩu truy cập
  repository.
- Repository cần quyền thì báo không truy cập được, không mở đường nhập credential.

### 4. Không lộ thông tin trong kết quả

- Không ghi giá trị bí mật đọc được từ file cấu hình vào kết quả hoặc artifact; chỉ ghi
  tên khóa khi cần cho quan hệ kiến trúc.
- Không ghi đường dẫn tuyệt đối của máy chạy vào artifact công khai.
- Khi có gọi AI, chỉ gửi dữ kiện kiến trúc tối thiểu cần cho mô tả, không gửi toàn bộ
  source.

### 5. Vòng đời dữ liệu lịch sử

| Quy tắc | Giá trị |
|---|---|
| Số lần phân tích giữ mỗi repository | 10 lần gần nhất |
| Thời hạn lưu mỗi kết quả | 14 ngày kể từ lúc chạy |
| Vượt số lần | Xóa kết quả cũ nhất |
| Quá hạn | Hệ thống tự xóa |
| Người dùng chủ động xóa | Cho phép trước khi hết hạn, có bước xác nhận |

Xóa phải xóa cả dữ liệu kết quả và source tạm đã lưu cho lần phân tích đó, không chỉ ẩn
khỏi danh sách.

## Điều kiện chấp nhận

- Có test chứng minh hệ thống không import và không chạy source đầu vào.
- Có test cho archive chứa đường dẫn thoát khỏi vùng giải nén, và không file nào được
  ghi ra ngoài.
- Có test cho repository cần quyền, kết quả là báo lỗi truy cập chứ không hỏi credential.
- Có test cho xóa thủ công, hết hạn và vượt số lần lưu.
- Security review xác nhận trước khi MVP được dùng ngoài nhóm phát triển.

## Việc còn lại

Security review chưa được thực hiện. Trạng thái hiện tại là yêu cầu đã viết, chưa có
xác nhận của người chịu trách nhiệm bảo mật.
