---
uid: "01M36K31QVGZA2CYGJYAQNH3AR"
key: "CMP-L3GEN-001"
type: "component"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"implements":["CAP-L3GEN-007"],"governed_by":["ADR-2026-003"],"constrained_by":["TM-SYS-L3GEN"],"depends_on":["CMP-L3GEN-002","CMP-L3GEN-003","CMP-L3GEN-004","CMP-L3GEN-005","CMP-L3GEN-007","CMP-L3GEN-008"]}
verified_at: 2026-10-02
verified_against: [{"key":"CAP-L3GEN-007","revision":2},{"key":"ADR-2026-003","revision":4},{"key":"FR-L3GEN-028","revision":3},{"key":"FR-L3GEN-029","revision":3},{"key":"NFR-L3GEN-OPS-001","revision":3},{"key":"NFR-L3GEN-SEC-002","revision":6},{"key":"GLOSS-L3GEN-001","revision":10}]
classification: "internal"
ai_assisted: true
---

# CMP-L3GEN-001 — Điều phối lần chạy

**Revision 3 (02/10/2026):** viết lại theo code thật và FR-L3GEN-028 đến 031. Dòng lệnh là đường chính của đợt này. Phần web giữ thiết kế của revision 2 (Khiêm quyết 02/10/2026); web chưa có FR ở CHG-L3GEN-2026-002. Code ở `experiments/quote-evidence/`.

**Revision 4 (02/10/2026):** sửa theo review REVIEW-ARCH-L3GEN-2026-001 (A1, A4, A20): snapshot trước, kiểm kê sau; một luật cho phần output lỗi (luôn xuất phần có được, `partial`); trạng thái ghi trong bộ output; web không thành Task khi chưa có FR (Khiêm quyết A4 ngày 02/10/2026).

## 1. Trách nhiệm

Thực hiện phần điều phối của [CAP-L3GEN-007](../l1/CAP-L3GEN-007.md). Đây là điểm vào của dòng lệnh và web. Nó giữ trạng thái, ngân sách và hàng đợi của lần chạy.

- Kiểm đầu vào và thư mục output **trước khi phân tích**: source tồn tại và đọc được; output chưa có hoặc rỗng; hai thư mục không lồng nhau (AC-L3GEN-028-02).
- Gọi các component theo thứ tự ở mục 3. Một lần chạy sinh cả sơ đồ (FR-L3GEN-028) và tài liệu L3 (FR-L3GEN-029 đến 031).
- Giữ trạng thái `completed` / `partial` / `failed` kèm lý do; in đường dẫn các file output.
- Giữ ngân sách: 30 phút, 2 GiB ([NFR-L3GEN-OPS-001](../../requirements/nfr/NFR-L3GEN-OPS-001.md)). Trần của model do [CMP-L3GEN-006](CMP-L3GEN-006.md) đếm rồi báo về đây.
- Trên web: mỗi lúc 1 lần chạy, lần sau xếp hàng; xóa source và output 24 giờ sau khi lần chạy kết thúc ([NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md), áp khi có FR web).

Không làm: không đọc source, không gọi model, không tự quyết trạng thái của từng phần kết quả.

## 2. Cấu trúc bên trong

| Phần | Việc | Code hiện tại |
|---|---|---|
| Dòng lệnh | Nhận thư mục source, thư mục output; gọi một lần chạy | `l3gen.py` (`main`, `analyze`) |
| Chuỗi bước | Gọi tiếp nhận, kiểm kê, trích, dựng mô hình, kiểm, xuất | `l3gen.analyze`; phần L3 qua `l3slice/__init__.py` (`run`) |
| Theo dõi lần chạy | Thời gian từng giai đoạn, bộ nhớ đỉnh, kích thước output | `l3slice/__init__.py` (`metrics`), `l3slice/engine.py` |
| Web | API `/api/v1`, hàng đợi, giữ 24 giờ, dọn lúc khởi động | `l3slice/engine.py`, `l3slice/web.py`; khởi chạy bằng `l3gen.py --web` |

## 3. Sequence

Dòng lệnh:

```mermaid
sequenceDiagram
    participant U as Người dùng
    participant R as CMP-001 Điều phối
    participant V as CMP-003 Kiểm kê
    participant I as CMP-002 Tiếp nhận
    participant X as CMP-004 Trích dữ kiện
    participant A as CMP-005 Dựng mô hình
    participant E as CMP-007 Kiểm bằng chứng
    participant P as CMP-008 Xuất
    U->>R: chạy (thư mục source, thư mục output)
    R->>R: kiểm đầu vào và output; sai thì dừng, không tạo gì
    R->>I: snapshot thư mục source
    R->>V: kiểm kê phạm vi trên snapshot
    R->>I: bản sao chỉ gồm file trong phạm vi
    R->>X: trích dữ kiện
    R->>A: chia component, dựng mô hình (gọi model qua CMP-006)
    R->>E: kiểm bằng chứng
    E-->>R: mô hình đã kiểm + phần giới hạn
    R->>P: xuất sơ đồ, tech-specs, README, JSON
    P-->>R: danh sách file hoặc artifact lỗi
    R-->>U: trạng thái cuối + đường dẫn output
```

## 4. Failure mode

| Hỏng ở đâu | Hành vi |
|---|---|
| Source không có, không đọc được; output không ghi được, đã có file, hoặc lồng với source | Dừng trước khi phân tích, nêu nguyên nhân và cách sửa, không tạo output (AC-L3GEN-028-02) |
| Hết 30 phút hoặc vượt bộ nhớ | Dừng giai đoạn đang chạy, trả `partial` với phần đã xong |
| Model lỗi, thiếu khóa, chạm trần | Không dừng lần chạy. Giữ cách chia của code, `partial` kèm nguyên nhân (AC-L3GEN-028-08) |
| Không có file nào trong phạm vi, hoặc repository ngoài ma trận hỗ trợ | `failed`; lý do ở phần giới hạn (AC-L3GEN-028-09) |
| Một phần output không sinh được (ví dụ L3 lỗi vì trùng định danh dữ kiện) | Vẫn xuất mọi phần sinh được; ghi phần thiếu và lý do ở phần giới hạn; `partial` |
| Sơ đồ và `tech-specs/` lệch tập component hoặc tập route | Vẫn xuất; liệt kê chỗ lệch ở phần giới hạn; `partial` (AC-L3GEN-029-04) |
| Tiến trình chết giữa chừng | Không để thư mục output trông như hoàn chỉnh (mục 5). Web: lần khởi động sau đánh dấu `failed`, xóa output dở |

## 5. Transaction boundary

Đơn vị trọn vẹn là **một lần chạy**. Chỉ đánh `completed` khi mọi artifact bắt buộc đã sinh xong, không phần nào thiếu. Trạng thái ghi vào `result.json` và `archdia.json` trong thư mục tạm, trước khi [CMP-L3GEN-008](CMP-L3GEN-008.md) đổi tên thư mục một lần; không có file trạng thái riêng.

## 6. Idempotency

Gửi cùng đầu vào hai lần là hai lần chạy riêng; phần do model làm có thể khác. Chạy lại vào cùng thư mục output thì bị từ chối vì output phải rỗng; công cụ không ghi đè. Xem trạng thái hay dọn dữ liệu nhiều lần không gây tác dụng phụ.

## 7. Concurrency

Dòng lệnh: một tiến trình, một lần chạy. Web: mỗi lúc 1 lần chạy, lần sau xếp hàng theo thứ tự đến, vì các lần chạy dùng chung khóa và tiền của model. Mỗi lần chạy có vùng làm việc riêng.

## 8. Lệch với code hiện tại

Đếm ngày 02/10/2026 trên `l3gen.py` và `runs/l3gen-v1/`. Mỗi dòng là ứng viên Task ở bước 11.

| # | Lệch | Căn cứ |
|---|---|---|
| 001-1 | Model chỉ chạy khi có cờ `--llm`; không có cờ thì không gọi model và không báo `partial` | NFR-L3GEN-AI-002 (model bắt buộc) |
| 001-2 | Không kiểm output trước khi phân tích. `analyze` tự tạo thư mục; `l3slice` từ chối output không rỗng ở bước xuất, sau đó `l3gen` vẫn ghi `archdia.*` | AC-L3GEN-028-02 |
| 001-3 | Đường `l3gen` không có trạng thái `completed` / `partial` / `failed` cho cả lần chạy; chỉ in số artifact | AC-L3GEN-028-08, NFR-L3GEN-OPS-001 |
| 001-4 | Đường `l3gen` không ghi thời gian từng giai đoạn và bộ nhớ đỉnh | NFR-L3GEN-OPS-001 |
| 001-5 | Web của `l3gen` thay hàm trích của `engine` bằng cách gán lại `eng.extract`; web chưa hiện sơ đồ `archdia`, chưa lọc file test. **Không lập Task tới khi có FR web** | Thiết kế web (chưa có FR) |

## Liên quan

| Nguồn | Nội dung |
|---|---|
| [CAP-L3GEN-007](../l1/CAP-L3GEN-007.md) | Tiếp nhận source và điều phối lần chạy |
| [ADR-2026-003](../adr/ADR-2026-003.md) | Chia component của công cụ |
| [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md) | Đầu vào, output, trạng thái |
| [NFR-L3GEN-OPS-001](../../requirements/nfr/NFR-L3GEN-OPS-001.md) | Thời gian, bộ nhớ |
