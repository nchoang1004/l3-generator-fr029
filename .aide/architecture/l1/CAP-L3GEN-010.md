---
uid: "01M369VEYTPZT8AK24PR5BEZGJ"
key: "CAP-L3GEN-010"
type: "capability"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"covers":["FR-L3GEN-028","FR-L3GEN-029","FR-L3GEN-030","FR-L3GEN-031"]}
verified_at: 2026-10-02
verified_against: [{"key":"FR-L3GEN-028","revision":3},{"key":"FR-L3GEN-029","revision":3},{"key":"FR-L3GEN-030","revision":2},{"key":"FR-L3GEN-031","revision":2},{"key":"GLOSS-L3GEN-001","revision":9}]
classification: "internal"
ai_assisted: true
---

# CAP-L3GEN-010 — Dựng mô hình kiến trúc mức component

## Năng lực này là gì

Từ tập dữ kiện, dựng component, mũi tên và vai trò file ở mức component, theo định nghĩa component của FR-L3GEN-028. Code lần theo từng route xuống tới bảng và hệ thống ngoài, lập nhóm route, xếp file vào component, xác định component sở hữu từng contract và dựng mũi tên từ lời gọi thuộc luồng. Mô hình ngôn ngữ gộp các nhóm route cùng trách nhiệm, đặt tên, viết một câu trách nhiệm và chọn tên dùng chung chỉ một component dùng, kèm mã dòng (NFR-L3GEN-AI-002).

## Ranh giới

- Không trích dữ kiện mới từ source — chỉ dùng dữ kiện của CAP-L3GEN-009 và các dòng code mang mã đã gửi model.
- Kiểm đề xuất của model trước khi đưa vào mô hình thuộc năng lực này (AC-L3GEN-028-05): đề xuất trỏ mã dòng không có, hoặc sai luật gộp, bị loại kèm lý do. Kiểm lần cuối mọi kết luận trước khi công bố là CAP-L3GEN-011.
- Model không tách nhóm route và không thêm mũi tên.
- Model lỗi hoặc hết trần thì dừng bước dùng model, giữ cách chia của code với tên theo đường dẫn, trạng thái `partial` (AC-L3GEN-028-08).

## FR được phủ

| FR key | Tên | Phần dựa vào năng lực này |
|---|---|---|
| [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md) | Sơ đồ kiến trúc có bằng chứng | Chia component, mũi tên, phần model gộp nhóm và đặt tên |
| [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md) | Tài liệu L3 API và cấu trúc component | Component sở hữu từng route; vai trò file trong component (AC-07) |
| [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md) | Tài liệu L3 bảng dữ liệu | Component sở hữu từng bảng |
| [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md) | Tài liệu L3 sự kiện và tác vụ nền | Component có điểm gửi hoặc nhận |

## Ràng buộc chính

[NFR-L3GEN-AI-002](../../requirements/nfr/NFR-L3GEN-AI-002.md), [NFR-L3GEN-ABST-002](../../requirements/nfr/NFR-L3GEN-ABST-002.md), [NFR-L3GEN-ACC-002](../../requirements/nfr/NFR-L3GEN-ACC-002.md).

## Ghi chú

Đây là năng lực, không phải component triển khai. Cách chia component nằm ở L2, lập sau L1. Thuật ngữ theo [glossary](../../domain/glossary-core.md).
