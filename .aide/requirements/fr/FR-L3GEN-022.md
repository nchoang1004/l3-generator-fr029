---
uid: "01M34AM2AHJFJNYT5MRZVKA38S"
key: "FR-L3GEN-004"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-001"],"constrained_by":["NFR-L3GEN-ACC-001","NFR-L3GEN-ABST-001","NFR-L3GEN-AI-001"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-004 — Dựng component và quan hệ kiến trúc

## Mô tả

Từ tập dữ kiện code của FR-L3GEN-003, công cụ dựng component, vai trò của chúng và các cạnh dependency ở mức application/component. Đây là bước mô hình ngôn ngữ tham gia.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Dựng mô hình kiến trúc |
| Ưu tiên | Must Have |
| Mốc | M2 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-004-01

- **Given:** Đã có tập dữ kiện code kèm vị trí file của một đơn vị phân tích.
- **When:** công cụ dựng mô hình kiến trúc.
- **Then:** kết quả gồm component, vai trò của từng component và cạnh dependency giữa chúng; mỗi component và mỗi cạnh trỏ được về các dữ kiện code đã sinh ra nó.
- `constrained_by:` [NFR-L3GEN-ACC-001, NFR-L3GEN-ABST-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-004-02

- **Given:** Mô hình ngôn ngữ trả về một component hoặc cạnh trỏ tới file không có trong snapshot.
- **When:** công cụ kiểm kết quả trả về.
- **Then:** phần đó bị loại khỏi mô hình và được ghi lại lý do loại; không xuất hiện trong sơ đồ hoặc tài liệu.
- `constrained_by:` [NFR-L3GEN-AI-001, NFR-L3GEN-ACC-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-004-03

- **Given:** Mô hình ngôn ngữ không khả dụng, hết quota, hoặc trả về payload sai schema.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ dừng bước dựng quan hệ kiến trúc và báo rõ nguyên nhân, giữ lại tập dữ kiện code đã trích được; không tự dựng quan hệ bằng cách đoán để lấp chỗ trống.
- `constrained_by:` [NFR-L3GEN-AI-001]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-004-04

- **Given:** Repository có số lượng thực thể vượt ngưỡng số node của sơ đồ mặc định.
- **When:** công cụ dựng sơ đồ.
- **Then:** sơ đồ mặc định vẫn ở mức application/component trong trần số node đã quy định; phần không lên sơ đồ mặc định được giữ ở lớp bằng chứng, không bị loại khỏi bộ kết quả.
- `constrained_by:` [NFR-L3GEN-ABST-001]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)
