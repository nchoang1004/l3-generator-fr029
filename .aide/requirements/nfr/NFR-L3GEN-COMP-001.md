---
uid: 01M2MV1DYC0N3QADT4E9DAQ4VA
key: NFR-L3GEN-COMP-001
type: non-functional-requirement
group: normative
scope: system
system: SYS-L3GEN
status: draft
revision: 1
category: compatibility
ownership:
  accountable_team: TEAM-L3GEN
  accountable_role: tech-lead
relations:
  constrains: [FR-L3GEN-005]
verified_at: 2026-09-16
verified_against: []
classification: internal
ai_assisted: true
---

# NFR-L3GEN-COMP-001 — Artifact dùng được ở nơi khác

## Mục đích

Tài liệu và mô hình xuất ra sẽ được đọc bằng công cụ khác, đưa vào kho tài liệu, hoặc
so sánh giữa hai lần chạy. Yêu cầu này giữ cho artifact có định dạng ổn định và không
phụ thuộc máy đã tạo ra nó.

## Yêu cầu

### 1. Định dạng và mã hóa

| Hạng mục | Quy định |
|---|---|
| Mã hóa ký tự | UTF-8 cho mọi artifact văn bản |
| Ký tự xuống dòng | Thống nhất một kiểu, không lẫn trong cùng file |
| Tài liệu L3 | Markdown đọc được bằng trình xem Markdown thông thường |
| Sơ đồ | Diagram-as-Code dạng văn bản, không phải ảnh nhị phân |
| Mô hình kiến trúc | JSON có schema và có phiên bản |

### 2. Đường dẫn độc lập với máy chạy

Mọi đường dẫn trong artifact là đường dẫn tương đối tính từ gốc source đã phân tích.
Không ghi đường dẫn tuyệt đối, tên người dùng hệ điều hành hoặc tên máy.

### 3. Kết quả ổn định

Cùng một kết quả phân tích xuất ra hai lần phải cho nội dung giống nhau, trừ các trường
ghi thời điểm chạy. Thứ tự các mục trong artifact phải ổn định, không phụ thuộc thứ tự
duyệt thư mục của hệ điều hành.

### 4. Phiên bản schema

Mô hình kiến trúc xuất ra mang số phiên bản schema. Đổi cấu trúc theo hướng không tương
thích thì phải tăng phiên bản, để công cụ đọc biết mình đang xử lý bản nào.

### 5. Môi trường hỗ trợ

Artifact tạo trên Windows, macOS hoặc Linux phải có cùng nội dung cho cùng đầu vào.

## Điều kiện chấp nhận

- Có test so sánh hai lần xuất từ cùng một kết quả phân tích.
- Có test xác nhận artifact không chứa đường dẫn tuyệt đối.
- Mô hình kiến trúc xuất ra có trường phiên bản schema.

## Việc còn lại

Schema của mô hình kiến trúc chưa được chốt. Phải hoàn thành cùng với Architecture IAM
trước khi đánh số phiên bản đầu tiên.
