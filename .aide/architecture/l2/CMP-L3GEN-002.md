---
uid: "01M36K31QV1EJECM7KJ65E1VS7"
key: "CMP-L3GEN-002"
type: "component"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 2
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"implements":["CAP-L3GEN-007","CAP-L3GEN-008"],"governed_by":["ADR-2026-003"],"depends_on":[]}
verified_at: 2026-09-23
verified_against: [{"key":"CAP-L3GEN-007","revision":1},{"key":"CAP-L3GEN-008","revision":1},{"key":"ADR-2026-003","revision":2},{"key":"GLOSS-L3GEN-001","revision":5}]
classification: "internal"
ai_assisted: true
---

# CMP-L3GEN-002 — Tiếp nhận source

## 1. Trách nhiệm

Thực hiện phần tiếp nhận của [CAP-L3GEN-007](../l1/CAP-L3GEN-007.md) và phần khoanh vùng file của [CAP-L3GEN-008](../l1/CAP-L3GEN-008.md). Đây là **chỗ duy nhất nhận dữ liệu từ ngoài vào**: file ZIP, URL GitHub, thư mục trên máy.

- Kiểm đầu vào, lấy source về vùng làm việc riêng của lần chạy.
- Tạo `source snapshot`: danh sách file kèm mã băm nội dung (content digest). Mọi component khác chỉ đọc source qua snapshot này.
- Cho đọc một đoạn file trong snapshot (dùng cho công cụ đọc code của [CMP-L3GEN-006](CMP-L3GEN-006.md)).

Không làm: không chạy, không import, không cài gì từ source. Không ghi vào cây source gốc.

## 2. Cấu trúc bên trong

| Phần | Việc | Vì sao tách |
|---|---|---|
| Kiểm đầu vào | Kích thước ZIP, số file, URL chỉ GitHub public HTTPS | Từ chối sớm, trước khi tốn tài nguyên |
| Lấy source | Giải nén hoặc tải từ GitHub vào vùng làm việc | Chỗ có rủi ro: đường dẫn thoát vùng, symlink ra ngoài |
| Snapshot | Danh sách file, mã băm, cho đọc theo đoạn | Là nguồn duy nhất để chứng minh bằng chứng tồn tại |

## 3. Sequence

```mermaid
sequenceDiagram
    participant R as CMP-001 Điều phối
    participant K as Kiểm đầu vào
    participant L as Lấy source
    participant S as Snapshot
    R->>K: đầu vào
    K-->>R: từ chối kèm lý do (nếu vượt trần)
    K->>L: đầu vào hợp lệ
    L->>L: giải nén / tải; chặn đường dẫn thoát vùng, symlink ra ngoài
    L->>S: cây file trong vùng làm việc
    S-->>R: snapshot (danh sách file + mã băm)
```

## 4. Failure mode

| Hỏng ở đâu | Hành vi |
|---|---|
| ZIP > 100 MB, giải nén > 500 MB, > 50.000 file | Từ chối, nêu trần bị vượt |
| Đường dẫn trong ZIP thoát khỏi vùng làm việc | Từ chối cả file ZIP |
| Symlink trỏ ra ngoài | Không đi theo; ghi thành giới hạn |
| URL không phải GitHub public, hoặc repo private | Báo đúng nguyên nhân truy cập; không hỏi credential (AC-L3GEN-019-05) |
| Tải GitHub quá 120 giây | Từ chối, báo quá thời gian |
| Thư mục đầu vào là thư mục output của chính công cụ | Từ chối (AC-L3GEN-019-03) |

## 5. Transaction boundary

Snapshot chỉ được giao đi khi đã lấy xong toàn bộ và tính xong mã băm. Lấy dở thì xóa vùng làm việc, không giao snapshot thiếu.

## 6. Idempotency

Cùng nội dung đầu vào cho cùng danh sách file và cùng mã băm. Đọc một đoạn file bao nhiêu lần cũng cho cùng nội dung, vì snapshot không đổi sau khi tạo.

## 7. Concurrency

Snapshot chỉ đọc sau khi tạo, nên nhiều component đọc cùng lúc được. Mỗi lần chạy có vùng làm việc riêng.

## Liên quan

| Nguồn | Nội dung |
|---|---|
| [CAP-L3GEN-007](../l1/CAP-L3GEN-007.md), [CAP-L3GEN-008](../l1/CAP-L3GEN-008.md) | Tiếp nhận, phạm vi |
| [NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md) | Trần tiếp nhận, read-only |
| [ADR-2026-003](../adr/ADR-2026-003.md) | Chia component |
