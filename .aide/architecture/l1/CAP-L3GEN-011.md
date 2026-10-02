---
uid: "01M369VEYVVCNYQRQB91P3VQHV"
key: "CAP-L3GEN-011"
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

# CAP-L3GEN-011 — Kiểm chứng bằng chứng và công bố giới hạn

## Năng lực này là gì

Cửa kiểm cuối cho mọi kết luận, dù do code dựng hay do model đề xuất và đã qua CAP-L3GEN-010, trước khi công bố: bằng chứng là dữ kiện có thật trong snapshot, cạnh nối đúng hai đầu, nhãn `exact` / `inferred` và `full` / `partial` đúng nghĩa. Ghi rõ phần không đọc được, phần ngoài phạm vi và phần bị loại kèm lý do.

## Ranh giới

- Là bước tất định, không dùng mô hình ngôn ngữ.
- Kết luận không có bằng chứng hợp lệ bị loại, không hạ thành cảnh báo.
- Phạm vi chưa xét đủ ghi là giới hạn, không ghi là không phát hiện thấy.
- Source trên đĩa đổi sau lần chạy thì báo snapshot không còn khớp.

## FR được phủ

| FR key | Tên | Phần dựa vào năng lực này |
|---|---|---|
| [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md) | Sơ đồ kiến trúc có bằng chứng | Kiểm bằng chứng và nhãn của khối, mũi tên; phần giới hạn |
| [FR-L3GEN-029](../../requirements/fr/FR-L3GEN-029.md) | Tài liệu L3 API và cấu trúc component | Kiểm bằng chứng từng dòng contract; nhãn `exact`/`inferred`/`unknown` |
| [FR-L3GEN-030](../../requirements/fr/FR-L3GEN-030.md) | Tài liệu L3 bảng dữ liệu | Như FR-029, cho bảng và cột |
| [FR-L3GEN-031](../../requirements/fr/FR-L3GEN-031.md) | Tài liệu L3 sự kiện và tác vụ nền | Như FR-029, cho sự kiện |

## Ràng buộc chính

[NFR-L3GEN-ACC-002](../../requirements/nfr/NFR-L3GEN-ACC-002.md), [NFR-L3GEN-OPS-001](../../requirements/nfr/NFR-L3GEN-OPS-001.md).

## Ghi chú

Đây là năng lực, không phải component triển khai. Cách chia component nằm ở L2, lập sau L1. Thuật ngữ theo [glossary](../../domain/glossary-core.md).
