---
uid: "01M369VEYVTNDWABXMQGG5H4W1"
key: "CAP-L3GEN-012"
type: "capability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"covers":["FR-L3GEN-028","FR-L3GEN-029","FR-L3GEN-030","FR-L3GEN-031"]}
verified_at: 2026-10-02
verified_against: [{"key":"FR-L3GEN-028","revision":3},{"key":"FR-L3GEN-029","revision":3},{"key":"FR-L3GEN-030","revision":2},{"key":"FR-L3GEN-031","revision":2},{"key":"GLOSS-L3GEN-001","revision":9}]
classification: "internal"
ai_assisted: true
---

# CAP-L3GEN-012 — Trình bày và xuất kết quả

## Năng lực này là gì

Từ cùng một mô hình kiến trúc đã kiểm, sinh sơ đồ component (mức L2) kèm mã nguồn sơ đồ, tài liệu L3 contract (API, TBL, EVT đặt trong `tech-specs/` theo đúng mẫu của mentor, quy tắc tên ở FR-L3GEN-029), README và JSON có schema version. Trên web, cho theo dõi lần chạy, xem tổng quan, đi sâu theo component và mở bằng chứng; phần web chưa có FR ở CHG-L3GEN-2026-002.

## Phần sinh tài liệu L3

| Đầu ra | Nội dung | FR |
|---|---|---|
| API | Endpoint, request/response, status, dependency/auth nếu biết; bảng đọc được và OpenAPI cùng nội dung | [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md) |
| README | Mục lục contract, sơ đồ, cấu trúc component, lời gọi HTTP ra ngoài, phần giới hạn | [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md) |
| TBL | Bảng, cột, kiểu, khóa, nullable; bảng đọc được và DDL cùng nội dung | [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md) |
| EVT | Topic hoặc tên tác vụ, bên gửi/nhận, payload nếu biết; phần chưa biết có lý do | [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md) |

Đường dữ liệu: [CAP-009](CAP-L3GEN-009.md) trích dữ kiện → [CAP-010](CAP-L3GEN-010.md) dựng mô hình component → [CAP-011](CAP-L3GEN-011.md) kiểm bằng chứng → CAP-012 sinh tài liệu. Mỗi dòng contract giữ được nguồn chứng minh. Giới hạn số node của sơ đồ không được dùng để bỏ dữ kiện khỏi tài liệu L3.

Lát triển khai ưu tiên là FR-L3GEN-029 cùng phần phụ thuộc cần để đi từ source đến tài liệu. Các năng lực dùng chung được triển khai đến mức phục vụ lát này; việc nghiệm thu đầy đủ từng FR vẫn theo AC của FR đó.

## Ranh giới

- Không phân tích lại source; mọi nội dung lấy từ mô hình đã kiểm.
- Không artifact nào chứa component hoặc quan hệ mà artifact khác không có.
- Sơ đồ mặc định giữ mức application/component theo NFR-L3GEN-ABST-002.
- Khám phá tương tác chỉ có trên web; dòng lệnh chỉ ghi file.

## FR được phủ

| FR key | Tên | Phần dựa vào năng lực này |
|---|---|---|
| [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md) | Sơ đồ kiến trúc có bằng chứng | `archdia.md`, `archdia.mmd`, `archdia.json` |
| [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md) | Tài liệu L3 API và cấu trúc component | File API trong `tech-specs/`, `README.md`, `result.json` |
| [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md) | Tài liệu L3 bảng dữ liệu | File TBL trong `tech-specs/` |
| [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md) | Tài liệu L3 sự kiện và tác vụ nền | File EVT trong `tech-specs/` |

## Ràng buộc chính

[NFR-L3GEN-ABST-002](../../requirements/nfr/NFR-L3GEN-ABST-002.md), [NFR-L3GEN-OPS-001](../../requirements/nfr/NFR-L3GEN-OPS-001.md), [NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md).

## Ghi chú

Đây là năng lực, không phải component triển khai. Cách chia component nằm ở L2, lập sau L1. Thuật ngữ theo [glossary](../../domain/glossary-core.md).
