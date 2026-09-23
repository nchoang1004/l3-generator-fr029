---
uid: "01M2J06Z46Y30FK51W5B9CZZ2V"
key: "FR-L3GEN-003"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "deprecated"
revision: 8
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001","GOAL-L3GEN-002"],"constrained_by":["NFR-L3GEN-ACC-001","NFR-L3GEN-COMP-001","NFR-L3GEN-TRACE-001"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-003 — Liệt kê API routes và handler

## Mô tả

Người dùng xem method, path, handler, điều kiện đăng ký và nguồn khai báo của route trong phạm vi stack đã công bố. Phase đầu phủ FastAPI; Java/Spring Boot thuộc phase sau.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Trích xuất dữ kiện |
| Ưu tiên đề xuất | Must Have |
| Mốc đề xuất | M1: route FastAPI; phase sau: route Spring Boot |
| Người sở hữu | Vai Product của TEAM-L3GEN; tên người chốt ở OQ-L3GEN-001 |

## Acceptance Criteria

### AC-L3GEN-003-01

- **Given:** FastAPI/APIRouter được khai báo trực tiếp cùng decorator GET, POST, PUT, DELETE hoặc PATCH.
- **When:** người dùng phân tích.
- **Then:** mỗi route xuất hiện đúng method, path, handler và nguồn; HTTP method ngoài phạm vi được báo là chưa hỗ trợ khi phát hiện.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Có fixture dùng alias import và hai router cùng tên ở hai module.

### AC-L3GEN-003-02

- **Given:** Router được include nhiều tầng hoặc app con được mount với prefix chuỗi hằng.
- **When:** người dùng phân tích.
- **Then:** path gồm đủ prefix của chuỗi đăng ký; router được đăng ký tại nhiều path có các route tương ứng.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Đối chiếu cả include_router và app.mount.

### AC-L3GEN-003-03

- **Given:** Prefix là giá trị động, đăng ký nằm trong if hoặc router chưa nối được tới app gốc.
- **When:** người dùng phân tích.
- **Then:** công cụ giữ phần chưa biết/điều kiện, hạ completeness thành partial và ghi lý do; không tuyên bố URL chạy thật đã đầy đủ.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Fixture kiểm route không được mount và prefix thiếu.

### AC-L3GEN-003-04

- **Given:** create_app() tạo FastAPI và truyền app qua tham số được khai kiểu tới hàm đăng ký route chứa decorator lồng.
- **When:** người dùng phân tích.
- **Then:** công cụ tìm được các route của mẫu này; phần binding không xác định được phải hiện cảnh báo thay vì kết luận không có route.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Fixture độc lập có hàm tạo app và hàm đăng ký route nhận tham số kiểu FastAPI; không cam kết mọi factory động.

### AC-L3GEN-003-05

- **Given:** Repo đăng ký route bằng vòng lặp hoặc add_api_route chưa được hỗ trợ.
- **When:** người dùng phân tích.
- **Then:** công cụ ghi nguồn pattern chưa hỗ trợ trong giới hạn; không tự tạo danh sách route suy đoán.
- `constrained_by:` [NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Phân biệt không tìm thấy route với không hỗ trợ cách đăng ký.

### AC-L3GEN-003-06

- **Given:** Repository Java dùng Spring Boot với controller khai báo route bằng annotation trong phạm vi đã công bố.
- **When:** người dùng phân tích.
- **Then:** route Java hiện ra với cùng cấu trúc dữ liệu và cùng nhãn chất lượng như route Python; không có trường riêng chỉ dành cho một ngôn ngữ.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-COMP-001, NFR-L3GEN-TRACE-001]
- `implementation_target:` []
- `validated_by:` []
- **Cách kiểm dự kiến:** Dùng ma trận Java roadmap đã chốt tại NFR-L3GEN-COMP-001; annotation ngoài ma trận phải hiện ở phần giới hạn, không im lặng bỏ qua. AC này thuộc phase sau.

## Trạng thái liên kết triển khai

Ở Scope Gate, `implementation_target` và `validated_by` có thể để trống vì component/contract/test IDs được lập ở bước thiết kế và planning tiếp theo. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [NFR-L3GEN-ACC-001](../nfr/NFR-L3GEN-ACC-001.md)
- [NFR-L3GEN-TRACE-001](../nfr/NFR-L3GEN-TRACE-001.md)
- [NFR-L3GEN-COMP-001](../nfr/NFR-L3GEN-COMP-001.md)
- [PRD](../../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../../domain/glossary-core.md)

