---
uid: "01M36K31QW5H0G8JKV8BZD5H8Y"
key: "CMP-L3GEN-005"
type: "component"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"implements":["CAP-L3GEN-010"],"governed_by":["ADR-2026-003","ADR-2026-001"],"depends_on":["CMP-L3GEN-004","CMP-L3GEN-006"]}
verified_at: 2026-09-23
verified_against: [{"key":"CAP-L3GEN-010","revision":1},{"key":"ADR-2026-003","revision":2},{"key":"ADR-2026-001","revision":5},{"key":"FR-L3GEN-027","revision":3},{"key":"GLOSS-L3GEN-001","revision":5}]
classification: "internal"
ai_assisted: true
---

# CMP-L3GEN-005 — Dựng mô hình kiến trúc

## 1. Trách nhiệm

Thực hiện [CAP-L3GEN-010](../l1/CAP-L3GEN-010.md). Biến tập dữ kiện thành mô hình kiến trúc: component, vai trò, cạnh dependency ở mức application/component.

Phân việc giữa code và model:

| Việc | Ai làm |
|---|---|
| Chia file vào component | Code, theo thư mục và liên kết. Repository phẳng thì model đề xuất, code kiểm (AC-L3GEN-022-05) |
| Dựng cạnh từ lời gọi đã nối được đích | Code |
| Đặt tên, mô tả, vai trò, nhãn cạnh | Model |
| Đề xuất cạnh phân tích tĩnh không thấy | Model; code kiểm dữ kiện ở hai đầu (AC-L3GEN-022-02) |

Component này **không gọi provider trực tiếp**; mọi yêu cầu tới model đi qua [CMP-L3GEN-006](CMP-L3GEN-006.md).

Không làm: không đọc source mới ngoài dữ kiện của CMP-004. Không công bố kết luận; kiểm lần cuối là việc của CMP-007.

### Phần phục vụ tài liệu L3

Mô hình giao đi giữ cả dữ kiện API/TBL/EVT của CMP-004, liên kết với component và nguồn chứng minh. CMP-005 chịu trách nhiệm xác định component sở hữu contract; CMP-008 dùng kết quả này để chia thư mục, không tự gán lại chủ sở hữu.

Việc chia nhóm không được bỏ trường của request/response, cột bảng hoặc payload. Trần node của sơ đồ chỉ áp cho góc nhìn sơ đồ; dữ liệu đầy đủ vẫn chuyển tới bước sinh tài liệu. Thiếu một cạnh dependency không tự làm mất route, bảng hoặc điểm phát/nhận đã trích được.

Áp dụng [quy tắc chia tài liệu của FR-027](../../requirements/fr/FR-L3GEN-027.md): API/TBL theo nơi khai báo; EVT theo từng component có điểm gửi/nhận. Nơi dùng API/bảng chỉ tham chiếu. Hai tài liệu EVT có thể nói về cùng topic nhưng giữ vai trò riêng, lấy từ cùng mô hình đã kiểm. Chưa đủ bằng chứng cùng broker/cấu hình thì không gộp topic hoặc nối hai bên.

Không xác định được nơi khai báo API/TBL thì giữ dữ kiện chưa gán cùng lý do trong kết quả `partial`; không tự đặt vào component gọi nó. CMP-008 liệt kê phần chưa gán trong README và JSON.

## 2. Cấu trúc bên trong

| Phần | Việc |
|---|---|
| Chia nhóm | Gom file thành component theo thư mục và liên kết; mỗi file thuộc đúng một component |
| Dựng cạnh tĩnh | Gộp nhiều lời gọi giữa hai component thành một cạnh, giữ danh sách lời gọi gốc |
| Liên kết contract | Giữ dữ kiện API/TBL/EVT và nguồn; xác định component sở hữu theo quy tắc được chốt |
| Nhờ model | Chuẩn bị đầu vào cho từng việc, gửi qua CMP-006, nhận kết quả đã đúng schema |
| Kiểm đề xuất | Loại đề xuất trỏ tới dữ kiện hoặc file không có, cạnh thiếu dữ kiện ở một đầu, cách chia nhóm để sót hoặc trùng file |

## 3. Sequence

```mermaid
sequenceDiagram
    participant R as CMP-001 Điều phối
    participant A as CMP-005 Dựng mô hình
    participant M as CMP-006 Cổng gọi model
    R->>A: tập dữ kiện + cờ repo phẳng
    alt repo phẳng
        A->>M: chia nhóm (gemini-3.5-flash)
        M-->>A: cách chia đề xuất
        A->>A: kiểm mỗi file đúng một nhóm; sai thì loại
    else repo có thư mục
        A->>A: code chia nhóm
    end
    A->>A: dựng cạnh tĩnh
    A->>M: đặt tên, mô tả, nhãn cạnh (gpt-oss-120b)
    A->>M: đề xuất cạnh bổ sung (gemini-3.5-flash)
    M-->>A: kết quả hoặc lỗi
    A->>A: kiểm đề xuất, loại kèm lý do
    A->>A: liên kết dữ kiện contract với component theo quy tắc đã chốt
    A-->>R: mô hình kiến trúc + đề xuất bị loại
```

## 4. Failure mode

| Hỏng ở đâu | Hành vi |
|---|---|
| Model lỗi, hết quota, vượt trần | Giữ phần code dựng; component chưa có tên do model thì dùng tên thư mục, đánh dấu chưa đặt tên; trạng thái `partial` (AC-L3GEN-022-03) |
| Tập dữ kiện gửi Gemini vượt 50.000 token | Bỏ bước đó, không cắt bớt dữ kiện. Đề xuất cạnh: chỉ giữ cạnh do code dựng. Chia nhóm repo phẳng: mỗi đơn vị là một component. Ghi giới hạn, trạng thái `partial` (AC-L3GEN-022-03) |
| Model đề xuất cạnh không có dữ kiện ở hai đầu | Loại, ghi lý do |
| Cách chia nhóm của model sót hoặc trùng file | Loại cả đề xuất; repo phẳng thì giữ mỗi đơn vị là một component, ghi giới hạn |
| Quá 50 node ở mức mặc định | Giữ trần NFR-L3GEN-ABST-002; phần dư nằm ở lớp bằng chứng |
| Chưa đủ căn cứ nối producer với consumer | Giữ hai quan sát riêng kèm nguồn và lý do thiếu; không tạo quan hệ chỉ từ tên topic (AC-L3GEN-027-03) |

## 5. Transaction boundary

Mô hình chỉ giao đi khi nhất quán: mã node duy nhất, cạnh có đủ hai đầu, mỗi file thuộc đúng một component. Phần model hỏng thì mô hình vẫn nhất quán, chỉ thiếu tên và cạnh bổ sung.

## 6. Idempotency

Phần do code làm (chia nhóm, cạnh tĩnh, mã node) tất định với cùng tập dữ kiện. Phần do model làm có thể khác giữa hai lần chạy; mỗi phần ghi model và phiên bản prompt đã sinh ra nó.

## 7. Concurrency

Chia nhóm và dựng cạnh chạy một luồng vì là phép toàn cục. Các yêu cầu đặt tên theo từng component có thể gửi song song, nhưng tốc độ gửi do CMP-006 quyết theo rate limit.

## Liên quan

| Nguồn | Nội dung |
|---|---|
| [CAP-L3GEN-010](../l1/CAP-L3GEN-010.md) | Dựng mô hình kiến trúc |
| [FR-L3GEN-022](../../requirements/fr/FR-L3GEN-022.md) | Component và quan hệ |
| [ADR-2026-001](../adr/ADR-2026-001.md) | Phân tích sâu, trình bày mức component |
| [NFR-L3GEN-ABST-002](../../requirements/nfr/NFR-L3GEN-ABST-002.md) | Trần 50 node |
