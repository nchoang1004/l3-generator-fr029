---
uid: "01M36K31QWNEHCQX5YJZN50CCA"
key: "CMP-L3GEN-003"
type: "component"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"implements":["CAP-L3GEN-008"],"governed_by":["ADR-2026-003"],"depends_on":["CMP-L3GEN-002"]}
verified_at: 2026-10-02
verified_against: [{"key":"CAP-L3GEN-008","revision":2},{"key":"ADR-2026-003","revision":4},{"key":"FR-L3GEN-028","revision":3},{"key":"FR-L3GEN-029","revision":3},{"key":"NFR-L3GEN-OPS-001","revision":3},{"key":"GLOSS-L3GEN-001","revision":10}]
classification: "internal"
ai_assisted: true
---

# CMP-L3GEN-003 — Kiểm kê phạm vi

**Revision 3 (02/10/2026):** viết lại theo code thật và bảng "Phạm vi đọc" của FR-L3GEN-028. Bỏ khái niệm "repository phẳng" (glossary revision 6). Code ở `experiments/quote-evidence/`.

**Revision 4 (02/10/2026):** sửa theo review REVIEW-ARCH-L3GEN-2026-001 (A1, A18): kiểm kê chạy trên snapshot; là chỗ duy nhất giữ luật phạm vi; repository không có file trong phạm vi xử lý một cách.

## 1. Trách nhiệm

Thực hiện [CAP-L3GEN-008](../l1/CAP-L3GEN-008.md). Đọc snapshot của [CMP-L3GEN-002](CMP-L3GEN-002.md) và trả lời: phân tích file nào, bỏ file nào, vì sao. Đây là **chỗ duy nhất giữ luật phạm vi**, lấy từ bảng "Phạm vi đọc" của [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md):

- Xét file `.py` của repository.
- Bỏ và gắn loại: file test (Kiểm thử), `migrations/`, `alembic/` (Migration), thư mục ẩn, `node_modules`, `__pycache__`, `site-packages`, thư mục có `pyvenv.cfg`.
- File trong `scripts/`, `seeds/`, `docs/`, `examples/`, `build/`, `dist/`, `env/`, `venv/`, `testing/` chỉ được xét khi import code của repository. Dòng import đọc từ snapshot.
- Đếm phần bị bỏ ở phần giới hạn (cột "Ngoài danh sách thì" của bảng "Phạm vi đọc").
- Giữ ma trận hỗ trợ: ngôn ngữ, framework, độ sâu phân tích, và có Pyright hay không ([NFR-L3GEN-OPS-001](../../requirements/nfr/NFR-L3GEN-OPS-001.md)). Phase đầu chỉ Python/FastAPI có mức đầy đủ.

Route khai trong file bị bỏ không vào tài liệu và không vào sơ đồ (AC-L3GEN-029-05).

Không làm: không đọc thư mục gốc; không trích dữ kiện. Đọc import chỉ để quyết file trong `scripts/`, `seeds/`... có được xét không.

## 2. Cấu trúc bên trong

| Phần | Việc | Code hiện tại |
|---|---|---|
| Luật phạm vi | Quyết file được xét, file bị bỏ kèm loại | `inventory.py` (`scan`) |
| Đơn vị phân tích | Một đơn vị cho cả repository ở phase đầu | `l3slice/snapshot.py` (`inventory`) |
| Ma trận hỗ trợ | Bảng khai báo ngôn ngữ, framework, mức hỗ trợ, công cụ phân giải tên | Chưa có (mục 8) |

## 3. Sequence

```mermaid
sequenceDiagram
    participant R as CMP-001 Điều phối
    participant V as CMP-003 Kiểm kê
    participant S as CMP-002 Snapshot
    R->>V: snapshot
    V->>S: danh sách file; đọc import của file trong scripts/, seeds/...
    V->>V: áp luật phạm vi; tra ma trận hỗ trợ
    V-->>R: file được xét + loại; file bị bỏ + lý do; mức hỗ trợ
```

## 4. Failure mode

| Hỏng ở đâu | Hành vi |
|---|---|
| Không có file nào trong phạm vi | Báo CMP-001 kèm lý do. CMP-001 kết thúc lần chạy `failed`, lý do ở phần giới hạn; không có bộ kết quả trông như thành công (AC-L3GEN-028-09) |
| Repository ngoài ma trận hỗ trợ | Như trên, nêu ngôn ngữ đã thấy |
| Không có Pyright | Ghi ở ma trận và phần giới hạn; phân tích chạy tiếp bằng phần tự đọc |
| File trong `scripts/` không đọc được import | Bỏ file đó, ghi lý do |

## 5. Transaction boundary

Kết quả kiểm kê giao đi một lần, đủ cả danh sách xét và danh sách bỏ.

## 6. Idempotency

Tất định: cùng snapshot và cùng luật cho cùng kết quả, cùng thứ tự.

## 7. Concurrency

Không có trạng thái riêng. Luật và ma trận chỉ đọc. Không cần khóa.

## 8. Lệch với code hiện tại

Đếm ngày 02/10/2026. Mỗi dòng là ứng viên Task ở bước 11.

| # | Lệch | Căn cứ |
|---|---|---|
| 003-1 | Hai bộ luật phạm vi: `inventory.py` (theo FR-028) và `l3slice/snapshot.py` (lệch 002-2). `inventory.scan` duyệt thư mục gốc, không duyệt snapshot (lệch 002-1) | FR-L3GEN-028 "Phạm vi đọc" |
| 003-2 | File bị bỏ chưa được đếm ở phần giới hạn. README của `l3slice` ghi "0 file bị loại" vì chỉ nhận bản sao đã lọc | FR-L3GEN-028 "Phạm vi đọc" |
| 003-3 | Chưa có ma trận hỗ trợ khai báo. Việc thiếu Pyright chỉ ghi ở phần giới hạn của sơ đồ (`names.UNAVAILABLE`) | NFR-L3GEN-OPS-001 |
| 003-4 | Thư mục không có file `.py`: `l3slice.run` dừng bằng lỗi `INVALID_INPUT`, không ghi lý do ở phần giới hạn | AC-L3GEN-028-09 |

## Liên quan

| Nguồn | Nội dung |
|---|---|
| [CAP-L3GEN-008](../l1/CAP-L3GEN-008.md) | Kiểm kê phạm vi |
| [FR-L3GEN-028](../../requirements/fr/FR-L3GEN-028.md) | Bảng "Phạm vi đọc" |
| [NFR-L3GEN-OPS-001](../../requirements/nfr/NFR-L3GEN-OPS-001.md) | Ma trận hỗ trợ |
