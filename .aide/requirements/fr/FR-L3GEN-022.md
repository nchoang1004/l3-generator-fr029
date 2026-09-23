---
uid: "01M34AM2AHJFJNYT5MRZVKA38S"
key: "FR-L3GEN-022"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 1
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-004"],"constrained_by":["NFR-L3GEN-ACC-002","NFR-L3GEN-ABST-002","NFR-L3GEN-AI-002"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-022 — Dựng component và quan hệ kiến trúc

## Mô tả

Từ tập dữ kiện code của FR-L3GEN-021, công cụ dựng component, vai trò của chúng và các cạnh dependency ở mức application/component. Đây là bước mô hình ngôn ngữ tham gia. Model chỉ **đề xuất**. Code kiểm từng đề xuất với tập dữ kiện, và chỉ phần có dữ kiện chứng minh mới vào mô hình kiến trúc.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Dựng mô hình kiến trúc |
| Ưu tiên | Must Have |
| Mốc | M2 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-022-01

- **Given:** Đã có tập dữ kiện code kèm vị trí file của một đơn vị phân tích.
- **When:** công cụ dựng mô hình kiến trúc.
- **Then:** kết quả gồm component, vai trò của từng component và cạnh dependency giữa chúng; mỗi component và mỗi cạnh trỏ được về các dữ kiện code đã sinh ra nó.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-022-02

- **Given:** Mô hình ngôn ngữ đề xuất một component hoặc một cạnh A→B.
- **When:** công cụ kiểm đề xuất trước khi đưa vào mô hình kiến trúc.
- **Then:** đề xuất chỉ được giữ khi mọi dữ kiện nó trích dẫn có trong tập dữ kiện của lần chạy và nằm ở file có trong snapshot; với cạnh A→B, phải có ít nhất một dữ kiện đã xác định đích mà vị trí thuộc A và đích thuộc B. Đề xuất không thỏa bị loại, ghi lý do loại, và không xuất hiện trong sơ đồ hoặc tài liệu.
- `constrained_by:` [NFR-L3GEN-AI-002, NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-022-03

- **Given:** Mô hình ngôn ngữ không khả dụng, hết quota, tập dữ kiện vượt trần token của một lần chạy, hoặc model trả về payload sai schema.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ dừng bước dựng quan hệ kiến trúc và báo rõ nguyên nhân, giữ lại tập dữ kiện code đã trích được; không tự dựng quan hệ bằng cách đoán để lấp chỗ trống.
- `constrained_by:` [NFR-L3GEN-AI-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-022-04

- **Given:** Repository có số lượng thực thể vượt ngưỡng số node của sơ đồ mặc định.
- **When:** công cụ dựng sơ đồ.
- **Then:** sơ đồ mặc định vẫn ở mức application/component trong trần số node đã quy định; phần không lên sơ đồ mặc định được giữ ở lớp bằng chứng, không bị loại khỏi bộ kết quả.
- `constrained_by:` [NFR-L3GEN-ABST-002]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)
