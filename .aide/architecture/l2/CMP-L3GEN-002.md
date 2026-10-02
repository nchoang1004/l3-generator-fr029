---
uid: "01M36K31QV1EJECM7KJ65E1VS7"
key: "CMP-L3GEN-002"
type: "component"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"implements":["CAP-L3GEN-007","CAP-L3GEN-008"],"governed_by":["ADR-2026-003"],"constrained_by":["TM-SYS-L3GEN"],"depends_on":[]}
verified_at: 2026-10-02
verified_against: [{"key":"CAP-L3GEN-007","revision":2},{"key":"CAP-L3GEN-008","revision":2},{"key":"ADR-2026-003","revision":4},{"key":"NFR-L3GEN-SEC-002","revision":6},{"key":"FR-L3GEN-028","revision":3},{"key":"GLOSS-L3GEN-001","revision":10}]
classification: "internal"
ai_assisted: true
---

# CMP-L3GEN-002 — Tiếp nhận source

**Revision 3 (02/10/2026):** viết lại theo code thật và FR-L3GEN-028 đến 031. Đợt này chỉ nhận thư mục cục bộ qua dòng lệnh ([NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md)). ZIP và GitHub giữ thiết kế của revision 2 cho web (Khiêm quyết 02/10/2026). Code ở `experiments/quote-evidence/`.

**Revision 4 (02/10/2026):** sửa theo review REVIEW-ARCH-L3GEN-2026-001 (A1, A9, A18): snapshot chụp trước, kiểm kê chạy trên snapshot; component này không quyết phạm vi; sửa số lần chụp snapshot trong code.

## 1. Trách nhiệm

Thực hiện phần tiếp nhận của [CAP-L3GEN-007](../l1/CAP-L3GEN-007.md) và phần khoanh vùng file của [CAP-L3GEN-008](../l1/CAP-L3GEN-008.md). Đây là **chỗ duy nhất nhận dữ liệu từ ngoài vào**: thư mục trên máy; trên web thêm file ZIP và URL GitHub. Mọi component khác đọc source qua snapshot, không đọc thư mục gốc.

- Tạo `source snapshot` **trước mọi bước khác**: danh sách file kèm mã băm nội dung và mã snapshot. Lấy mọi file `.py` và manifest Python; bỏ `.git`; không đi theo symlink. Phần bị bỏ ghi kèm lý do.
- Không quyết file nào được phân tích; việc đó thuộc [CMP-L3GEN-003](CMP-L3GEN-003.md).
- Dựng **bản sao trong phạm vi**: thư mục tạm chỉ gồm file CMP-003 chọn, chép từ snapshot. Công cụ cần file trên đĩa (Pyright, [ADR-2026-005](../adr/ADR-2026-005.md)) chạy trên bản sao này.
- Cho đọc một dòng hoặc một đoạn file trong snapshot, để bằng chứng được kiểm và hiện từ đúng bản đã phân tích.

Không làm: không chạy, không import, không cài gì từ source. Không ghi vào cây source gốc.

## 2. Cấu trúc bên trong

| Phần | Việc | Code hiện tại |
|---|---|---|
| Snapshot thư mục | Đọc file, tính mã băm, ghi phần bị bỏ | `l3slice/snapshot.py` (`take`) |
| Bản sao trong phạm vi | Chép file CMP-003 chọn vào thư mục tạm | `l3gen.py` (`_in_scope`) |
| Kiểm ZIP (web) | Trần kích thước, số file, đường dẫn thoát vùng, symlink; không ghi ZIP ra đĩa | `l3slice/snapshot.py` (`take_zip`) |
| Lấy từ GitHub (web) | Chỉ HTTPS, chỉ host GitHub, kiểm lại sau chuyển hướng; tắt mặc định | `l3slice/github.py` |

## 3. Sequence

```mermaid
sequenceDiagram
    participant R as CMP-001 Điều phối
    participant S as CMP-002 Tiếp nhận
    participant V as CMP-003 Kiểm kê
    R->>S: thư mục source
    S->>S: đọc mọi file .py và manifest; bỏ .git, symlink; tính mã băm
    S-->>R: snapshot (mã snapshot, danh sách file, mã băm, phần bị bỏ)
    R->>V: snapshot
    V-->>R: file trong phạm vi + loại; file bị bỏ + lý do
    R->>S: dựng bản sao trong phạm vi
    S-->>R: thư mục tạm chỉ gồm file trong phạm vi
```

## 4. Failure mode

| Hỏng ở đâu | Hành vi |
|---|---|
| Symlink | Không đi theo; ghi thành phần bị bỏ kèm lý do |
| File không đọc được | Ghi thành phần bị bỏ kèm lý do; đọc tiếp file khác |
| Web: ZIP > 100 MB, giải nén > 500 MB, > 50.000 file | Từ chối, nêu trần bị vượt |
| Web: đường dẫn trong ZIP thoát vùng làm việc, hoặc ZIP chứa liên kết | Từ chối cả file ZIP |
| Web: URL không phải GitHub public HTTPS, hoặc quá 120 giây | Từ chối kèm nguyên nhân; không hỏi credential |

Kiểm source và output lồng nhau thuộc [CMP-L3GEN-001](CMP-L3GEN-001.md), vì cần cả hai đường dẫn. Repository không có file nào trong phạm vi do CMP-003 báo.

## 5. Transaction boundary

Snapshot chỉ được giao đi khi đã đọc xong mọi file và tính xong mã băm. Đọc dở thì không giao snapshot thiếu. Thư mục tạm xóa khi lần chạy kết thúc.

## 6. Idempotency

Cùng nội dung đầu vào cho cùng danh sách file, cùng mã băm, cùng mã snapshot. Đọc một đoạn file bao nhiêu lần cũng cho cùng nội dung.

## 7. Concurrency

Snapshot chỉ đọc sau khi tạo, nên nhiều component đọc cùng lúc được. Mỗi lần chạy có thư mục tạm riêng.

## 8. Lệch với code hiện tại

Đếm ngày 02/10/2026. Mỗi dòng là ứng viên Task ở bước 11.

| # | Lệch | Căn cứ |
|---|---|---|
| 002-1 | Code không theo thứ tự "snapshot trước". `snapshot.take` chạy 3 lần (`l3gen._in_scope`, `l3gen.analyze`, `l3slice.run`); `inventory.scan` chạy 2 lần trên thư mục gốc (`_in_scope`, `contract_trace.analyse`); `contract_trace` và Pyright đọc thẳng thư mục gốc. Bằng chứng của sơ đồ và của L3 vì vậy không được kiểm trên cùng một snapshot | AC-L3GEN-028-11, glossary bất biến #1 |
| 002-2 | `l3slice/snapshot.py` tự bỏ `venv`, `.venv`, `node_modules`, `__pycache__` không điều kiện; luật phạm vi lẽ ra chỉ ở CMP-003 (FR-028 xét `venv/` khi file import code của repository) | FR-L3GEN-028 "Phạm vi đọc" |

## Liên quan

| Nguồn | Nội dung |
|---|---|
| [CAP-L3GEN-007](../l1/CAP-L3GEN-007.md), [CAP-L3GEN-008](../l1/CAP-L3GEN-008.md) | Tiếp nhận, phạm vi |
| [NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md) | Read-only, tiếp nhận an toàn, trần ZIP |
| [ADR-2026-003](../adr/ADR-2026-003.md) | Chia component của công cụ |
| [ADR-2026-005](../adr/ADR-2026-005.md) | Pyright chạy trên bản sao trong phạm vi |
