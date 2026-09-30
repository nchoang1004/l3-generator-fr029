---
uid: "01M36K31QXF9SNPSHE6JDDV4AW"
key: "CMP-L3GEN-008"
type: "component"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"implements":["CAP-L3GEN-012"],"governed_by":["ADR-2026-003","ADR-2026-001"],"depends_on":["CMP-L3GEN-007"]}
verified_at: 2026-09-23
verified_against: [{"key":"CAP-L3GEN-012","revision":3},{"key":"ADR-2026-003","revision":2},{"key":"ADR-2026-001","revision":5},{"key":"FR-L3GEN-027","revision":3},{"key":"FR-L3GEN-025","revision":2},{"key":"GLOSS-L3GEN-001","revision":5}]
classification: "internal"
ai_assisted: true
---

# CMP-L3GEN-008 — Trình bày và xuất

## 1. Trách nhiệm

Thực hiện [CAP-L3GEN-012](../l1/CAP-L3GEN-012.md). Từ **một** mô hình đã kiểm của CMP-007, sinh mọi output:

- Sơ đồ component và dependency, kèm mã nguồn sơ đồ.
- Tài liệu L3 contract trong `tech-specs/`, tên file theo [FR-L3GEN-027](../../requirements/fr/FR-L3GEN-027.md).
- JSON có schema version và mã snapshot.
- `README.md` mục lục kèm phần giới hạn.
- Trang web: theo dõi lần chạy, tổng quan, đi sâu từng component, mở bằng chứng.

Không làm: không đọc source, không gọi model, không thêm kết luận.

## 2. Cấu trúc bên trong

| Phần | Việc |
|---|---|
| Sơ đồ | Sinh mã sơ đồ; giữ mức application/component, ≤ 50 node |
| Tài liệu L3 | Ba bộ sinh riêng API/TBL/EVT; mỗi bộ dùng nội dung contract đã kiểm, gắn nguồn cho từng dòng |
| Kiểm bản xuất | Bảng và khối máy cùng nguồn dữ liệu; kiểm định dạng, tham chiếu, phần thiếu và danh sách file |
| JSON | Bộ dữ liệu máy đọc, có schema version |
| Trang web | Các màn hình đọc từ cùng bộ JSON. Mở bằng chứng thì gọi CMP-007 kiểm snapshot còn khớp, không tự đọc source |
| Ghi file | Ghi vào thư mục tạm rồi đổi tên một lần |

### Sinh tài liệu L3

Đầu vào phải có snapshot, component, dữ kiện contract, nguồn từng trường và phần giới hạn đã qua CMP-007. Lỗi thiếu trường trong đầu vào và giá trị `unknown` là hai trường hợp khác nhau: lỗi cấu trúc thì báo lỗi; `unknown` có lý do thì sinh bản `partial`.

| Bộ sinh | Cách dựng từ dữ kiện đã kiểm |
|---|---|
| API | Gom endpoint theo component sở hữu; giữ method, path đầy đủ, handler, tham số, request/response, status, dependency/auth nếu biết. Bảng và OpenAPI 3.1 dùng chung danh sách endpoint và trường model |
| TBL | Gom bảng theo component sở hữu; giữ tên, từng cột, kiểu, khóa, nullable. Bảng và DDL dùng chung danh sách cột và ràng buộc |
| EVT | Sinh theo từng component có điểm gửi/nhận, ghi rõ vai trò và payload nếu biết. Liên kết các file chỉ theo quan hệ đã kiểm; không tự ghép theo tên topic. Quy tắc gom và tránh trùng tên theo FR-027 |

Tên thư mục/file theo FR-027. Mỗi file có metadata bản sinh tự động, snapshot và component sở hữu. Nội dung lấy từ mô hình, không cắt theo số node đang hiện trên sơ đồ. Các bộ sinh xử lý dữ liệu thành văn bản; không chạy code, OpenAPI hay DDL để khám phá thêm dữ kiện.

**Dữ liệu thiếu — Khiêm đã chọn:** xuất phần biết được, đánh dấu `partial` và chỉ rõ trường thiếu cùng lý do. Markdown giữ dòng `unknown`; phần máy chỉ biểu diễn giá trị đã biết theo đúng định dạng, kèm thông tin phần chưa biểu diễn được. Không tạo tên bảng, kiểu cột, path hoặc status giả để lấp chỗ trống. DDL ghi biến thể SQL nếu source chứng minh được; chưa xác định thì ghi chưa biết, không mặc định một hệ quản trị.

Ở bước L3 phải đặc tả cách biểu diễn phần thiếu cho từng định dạng và bộ ví dụ kiểm tương ứng. Định dạng máy hợp lệ không có nghĩa nội dung đã đầy đủ. Không dựng được khối máy hợp lệ thì ghi rõ khối đó chưa có cùng lý do; vẫn giữ phần Markdown đã biết. README và JSON liệt kê cả contract chưa gán được component, không âm thầm bỏ dữ kiện.

## 3. Sequence

```mermaid
sequenceDiagram
    participant R as CMP-001 Điều phối
    participant P as CMP-008 Xuất
    R->>P: mô hình đã kiểm + giới hạn
    P->>P: sinh JSON
    P->>P: gom contract theo component sở hữu
    P->>P: sinh bảng và khối máy từ cùng dữ liệu; gắn nguồn từng dòng
    P->>P: ghi phần thiếu, kiểm định dạng và tham chiếu
    P->>P: sinh sơ đồ và README từ cùng mô hình
    P->>P: kiểm chéo: mọi artifact cùng tập component và cạnh
    P->>P: ghi vào thư mục tạm, đổi tên thành thư mục output
    P-->>R: danh sách file hoặc artifact lỗi
```

## 4. Failure mode

| Hỏng ở đâu | Hành vi |
|---|---|
| Một artifact sinh lỗi | Báo artifact nào lỗi, giữ artifact hợp lệ, cho thử lại (AC-L3GEN-025-03) |
| Artifact lệch nhau về component hoặc cạnh | Không xuất; đây là lỗi của công cụ |
| JSON có cạnh trỏ tới thực thể không có | Không xuất (AC-L3GEN-025-02) |
| Trường contract chưa biết, đã có lý do | Xuất phần đã biết và đánh dấu `partial`; giữ phần thiếu trong tài liệu và bộ kết quả |
| Không biểu diễn được một phần bằng OpenAPI hoặc DDL hợp lệ | Giữ thông tin đã biết trong Markdown, liệt kê phần thiếu; chỉ xuất khối máy hợp lệ nếu dựng được, không chèn giá trị giả |
| Bảng Markdown và khối máy mâu thuẫn, mất nguồn hoặc tham chiếu hỏng | Báo lỗi artifact đó, không công bố bản mâu thuẫn; giữ artifact khác hợp lệ theo AC-L3GEN-025-03 |
| Hai component trùng tên thư mục | Thêm `-2`, `-3` theo FR-L3GEN-027 |
| Output quá hạn 24 giờ trên web | Không phục vụ; báo đã hết hạn |
| Mở bằng chứng mà file đã đổi hoặc mất so với snapshot | Hiện "snapshot không còn khớp", không hiện nội dung mới (AC-L3GEN-023-03) |

## 5. Transaction boundary

Đơn vị trọn vẹn là **cả bộ output** của một lần chạy. Kết quả `partial` vẫn xuất đủ phần đã có. Thư mục tạm chỉ để tránh file bị cắt nửa chừng khi tiến trình chết: ghi vào thư mục tạm, ghi xong mới đổi tên thành thư mục output.

## 6. Idempotency

Tất định: cùng mô hình đã kiểm cho cùng bộ file, cùng nội dung. Sinh lại một artifact lỗi không đổi các artifact khác.

Thử lại chỉ dùng mô hình của cùng lần chạy và cùng phiên bản bộ sinh. Không phân tích lại source hoặc gọi model trong lần thử xuất lại. Trạng thái artifact và trạng thái toàn bộ kết quả phải phản ánh phần còn thiếu.

## 7. Concurrency

Mỗi lần chạy ghi vào thư mục riêng. Trang web chỉ đọc. Không cần khóa.

## Liên quan

| Nguồn | Nội dung |
|---|---|
| [CAP-L3GEN-012](../l1/CAP-L3GEN-012.md) | Trình bày và xuất |
| [CMP-L3GEN-007](CMP-L3GEN-007.md) | Kiểm snapshot khi mở bằng chứng |
| [FR-L3GEN-025](../../requirements/fr/FR-L3GEN-025.md), [FR-L3GEN-026](../../requirements/fr/FR-L3GEN-026.md), [FR-L3GEN-027](../../requirements/fr/FR-L3GEN-027.md) | Xuất, web, tài liệu L3 |
| [NFR-L3GEN-ABST-002](../../requirements/nfr/NFR-L3GEN-ABST-002.md) | Mức trừu tượng |
