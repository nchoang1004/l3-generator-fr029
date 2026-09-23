---
uid: "01M34AM2AHJFJNYT5MRZVKA38S"
key: "FR-L3GEN-022"
type: "functional-requirement"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"product-owner","affected_teams":[]}
relations: {"satisfies":["GOAL-L3GEN-004"],"constrained_by":["NFR-L3GEN-ACC-002","NFR-L3GEN-ABST-002","NFR-L3GEN-AI-002"],"measured_by":["OBS-L3GEN-001"]}
verified_at: null
verified_against: []
classification: "internal"
ai_assisted: true
---

# FR-L3GEN-022 — Dựng component và quan hệ kiến trúc

## Mô tả

Từ tập dữ kiện code của FR-L3GEN-021, công cụ dựng component, vai trò của chúng và các cạnh dependency ở mức application/component. Việc chia làm hai phần:

| Phần | Ai làm |
|---|---|
| Chia file vào component | Code, tất định: theo cây thư mục, tên và số lời gọi giữa các nhóm. Riêng repository phẳng thì mô hình ngôn ngữ đề xuất cách chia (AC-L3GEN-022-05) |
| Cạnh giữa component | Code, từ lời gọi và tham chiếu đã xác định đích |
| Tên, mô tả, vai trò component; nhãn cạnh | Mô hình ngôn ngữ |
| Cạnh mà phân tích tĩnh không thấy, ví dụ qua REST, queue, cấu hình | Mô hình ngôn ngữ đề xuất; code kiểm dữ kiện chứng minh (AC-L3GEN-022-02) |

Cách chia này học từ CodeBoarding: cho model tự chia component cho kết quả dao động giữa các lần chạy mà không tốt hơn cách chia tất định.

| Thuộc tính | Giá trị |
|---|---|
| Nhóm luồng | Dựng mô hình kiến trúc |
| Ưu tiên | Must Have |
| Mốc | M2 |
| Người sở hữu | Vai Product của TEAM-L3GEN |

## Acceptance Criteria

### AC-L3GEN-022-01

- **Given:** Đã có tập dữ kiện code kèm vị trí file của một đơn vị phân tích, và cây thư mục chia được file source thành ít nhất hai nhóm.
- **When:** công cụ dựng mô hình kiến trúc.
- **Then:** code chia mỗi file source vào đúng một component, và dựng cạnh từ lời gọi, tham chiếu đã xác định đích; mô hình ngôn ngữ đặt tên, mô tả, vai trò cho từng component và gắn nhãn cho từng cạnh, nhưng không thêm, bớt, gộp hay tách component. Mỗi component và mỗi cạnh trỏ được về các dữ kiện code đã sinh ra nó.
- `constrained_by:` [NFR-L3GEN-ACC-002, NFR-L3GEN-ABST-002, NFR-L3GEN-AI-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-022-02

- **Given:** Mô hình ngôn ngữ đề xuất thêm một cạnh A→B mà code chưa dựng được.
- **When:** công cụ kiểm đề xuất trước khi đưa vào mô hình kiến trúc.
- **Then:** đề xuất chỉ được giữ khi mọi dữ kiện nó trích dẫn có trong tập dữ kiện của lần chạy và nằm ở file có trong snapshot, và có dữ kiện ở cả hai đầu: một dữ kiện có vị trí thuộc A, một dữ kiện có vị trí thuộc B. Đề xuất không thỏa bị loại, ghi lý do loại, và không xuất hiện trong sơ đồ hoặc tài liệu.
- `constrained_by:` [NFR-L3GEN-AI-002, NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

### AC-L3GEN-022-03

- **Given:** Mô hình ngôn ngữ không khả dụng, hết quota, tập dữ kiện vượt trần token của một lần chạy, hoặc model trả về payload sai schema.
- **When:** công cụ chạy phân tích.
- **Then:** công cụ dừng bước dùng model và báo rõ nguyên nhân, trả kết quả partial gồm tập dữ kiện code và phần chia nhóm, cạnh do code dựng; component chưa có tên do model thì đặt tên theo đường dẫn và ghi rõ chưa được đặt tên. Không tự thêm quan hệ bằng cách đoán để lấp chỗ trống.
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

### AC-L3GEN-022-05

- **Given:** Repository phẳng: cây thư mục không chia được file source trong phạm vi thành ít nhất hai nhóm.
- **When:** công cụ dựng mô hình kiến trúc.
- **Then:** mô hình ngôn ngữ đề xuất cách chia file vào component; code kiểm mỗi file source thuộc đúng một component và mỗi file có trong snapshot, loại đề xuất không thỏa kèm lý do. Component chia theo cách này mang nhãn `inferred` với lý do "chia nhóm do model vì cây thư mục không đủ".
- `constrained_by:` [NFR-L3GEN-AI-002, NFR-L3GEN-ACC-002]
- `implementation_target:` []
- `validated_by:` []

## Trạng thái liên kết triển khai

`implementation_target` và `validated_by` để trống ở Scope Gate; component, contract và test ID được lập ở bước thiết kế và planning. Hai mapping phải hoàn tất trước Definition of Ready cho code. Không tạo ID giả để lấp chỗ trống.

## Tài liệu liên quan

- [PRD](../../product/prd/PRD-L3GEN-2609-001.md)
- [Thuật ngữ](../../domain/glossary-core.md)
