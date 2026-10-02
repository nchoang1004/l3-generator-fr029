---
uid: "01M36K31QXS846KCCX0TH72EWT"
key: "CMP-L3GEN-006"
type: "component"
group: "normative"
scope: "system"
system: "SYS-L3GEN"
status: "draft"
revision: 4
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"architect","affected_teams":[]}
relations: {"implements":["CAP-L3GEN-010"],"governed_by":["ADR-2026-003","ADR-2026-004","ADR-2026-005"],"constrained_by":["TM-SYS-L3GEN"],"depends_on":["CMP-L3GEN-004"]}
verified_at: 2026-10-02
verified_against: [{"key":"CAP-L3GEN-010","revision":2},{"key":"ADR-2026-003","revision":4},{"key":"ADR-2026-004","revision":2},{"key":"ADR-2026-005","revision":1},{"key":"NFR-L3GEN-AI-002","revision":6},{"key":"NFR-L3GEN-SEC-002","revision":6},{"key":"GLOSS-L3GEN-001","revision":10}]
classification: "internal"
ai_assisted: true
---

# CMP-L3GEN-006 — Cổng gọi model

**Revision 3 (02/10/2026):** viết lại theo [NFR-L3GEN-AI-002](../../requirements/nfr/NFR-L3GEN-AI-002.md) revision 6 và code thật. Một provider (OpenRouter), một model, trả phí, có trần mỗi lần chạy. Bỏ Groq, Google, chính sách miễn phí và công cụ đọc code của revision 2. Code ở `experiments/quote-evidence/`.

**Revision 4 (02/10/2026):** sửa theo review REVIEW-ARCH-L3GEN-2026-001 (A2, A16): bỏ cache và sổ chi phí dùng chung khỏi đường chạy sản phẩm, chi phí ghi vào provenance trong output (Khiêm quyết A2 ngày 02/10/2026); provenance ghi phiên bản Pyright.

## 1. Trách nhiệm

Hỗ trợ [CAP-L3GEN-010](../l1/CAP-L3GEN-010.md). Đây là **chỗ duy nhất gửi dữ liệu ra ngoài**. Mọi request tới model đi qua đây.

- Gửi tới OpenRouter, model `openai/gpt-6-luna`, mức suy luận trung bình, không gửi `temperature`. Provider và model đọc từ cấu hình. Lỗi thì không đổi sang model khác.
- Trước request đầu tiên của lần chạy, in tên provider, tên model và loại dữ liệu sẽ gửi ([NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md)).
- Chỉ gửi đúng mục "Đầu vào gửi cho model" của NFR-L3GEN-AI-002. Dòng code trong payload đã che bí mật bằng luật của [CMP-L3GEN-004](CMP-L3GEN-004.md).
- Ước tính token trước request đầu; giữ trần mỗi lần chạy: ≤ 0,20 USD, ≤ 300.000 token, ≤ 4 request, ≤ 12.000 token trả lời mỗi request, timeout 300 giây.
- Thử lại một lần khi lỗi mạng hoặc timeout. Kiểm câu trả lời là JSON đúng schema; sai thì báo lỗi cho [CMP-L3GEN-005](CMP-L3GEN-005.md), để CMP-005 quyết gửi lại.
- Ghi provenance vào bộ output của lần chạy: provider, model, phiên bản prompt, phiên bản công cụ, phiên bản scip-python, Pyright, Node ([ADR-2026-005](../adr/ADR-2026-005.md)), mã snapshot, số request, token, chi phí do provider trả về.
- Không giữ gì ngoài thư mục output: không cache câu trả lời, không sổ chi phí dùng chung ([NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md) "Vòng đời"). Cache chỉ có trong công cụ đo khi phát triển, bật bằng cờ riêng, ngoài sản phẩm.
- Khóa API nhận lúc chạy, chỉ nằm trong header `Authorization`; không ghi vào output, log hay provenance.

Không làm: không quyết đề xuất nào đúng về nội dung (việc của CMP-005 và CMP-007). Model không có công cụ nào để đọc thêm code.

## 2. Cấu trúc bên trong

| Phần | Việc | Code hiện tại |
|---|---|---|
| Client OpenRouter | Gửi request, đọc usage và chi phí, thử lại | `llm.py` (lớp `Groq` với `url=OPENROUTER_URL`) |
| Bộ đếm trần | Cộng token, request, chi phí của lần chạy; chặn trước khi gửi | `llm.py`, đang đếm theo sổ chung `usage-openrouter.jsonl` (lệch 006-1) |
| Cache câu trả lời | Không có trên đường chạy sản phẩm; chỉ trong công cụ đo khi phát triển | `llm.py` bật cache mặc định (lệch 006-6) |
| Kiểm schema | JSON schema của từng việc | `llm.py` (`json`), schema ở `contract_llm.py` |
| Provider giả | Thay provider trong test | `FakeLLM` trong `test_ai7.py`; chưa dùng cho `contract_llm.py` (lệch 005-7) |
| Cổng của nhánh Hoàng | Groq, Google, chính sách miễn phí | `l3slice/gateway.py`; không nằm trên đường chạy của `l3gen` |

## 3. Sequence

```mermaid
sequenceDiagram
    participant A as CMP-005 Dựng mô hình
    participant M as CMP-006 Cổng gọi model
    participant U as Người dùng (dòng lệnh)
    participant O as OpenRouter
    A->>M: việc + đầu vào đã có mã dòng, đã che bí mật
    M->>M: có khóa? ước tính token; còn trong trần?
    M-->>U: lần đầu: in provider, model, loại dữ liệu sẽ gửi
    M->>O: request
    O-->>M: câu trả lời + usage + chi phí
    M->>M: kiểm JSON schema; cộng bộ đếm trần; ghi provenance
    M-->>A: câu trả lời hợp lệ, hoặc lỗi kèm lý do
```

## 4. Failure mode

| Hỏng ở đâu | Hành vi |
|---|---|
| Thiếu khóa API | Không gửi; báo CMP-005; lần chạy `partial` (AC-L3GEN-028-08) |
| Ước tính vượt trần token hoặc chi phí | Không gửi; báo CMP-005; `partial` |
| Lỗi mạng, timeout 300 giây, provider trả 5xx | Thử lại một lần; vẫn lỗi thì báo lỗi |
| Hết tiền, rate limit | Dừng việc, báo rõ; không đổi model |
| Câu trả lời rỗng, bị cắt, hoặc sai schema | Báo lỗi schema; CMP-005 quyết gửi lại một lần |
| Chạm trần giữa chừng | Dừng mọi request còn lại của lần chạy |

## 5. Transaction boundary

Đơn vị là **một request**. Chỉ trả câu trả lời khi đã qua kiểm schema. Lỗi thì trả lỗi; không trả nửa câu trả lời. Provenance ghi cả request lỗi.

## 6. Idempotency

Không tất định: gửi lại cùng đầu vào có thể nhận câu trả lời khác. Không tự gửi lại request đã thành công. Thử lại chỉ áp cho lỗi mạng và timeout.

## 7. Concurrency

Gửi tuần tự, mỗi lần chạy một việc. Bộ đếm trần tính riêng cho từng lần chạy; không có trạng thái dùng chung giữa các lần chạy.

## 8. Lệch với code hiện tại

Đếm ngày 02/10/2026. Mỗi dòng là ứng viên Task ở bước 11.

| # | Lệch | Căn cứ |
|---|---|---|
| 006-1 | Trần chưa đúng: `llm.py` chặn theo tổng sổ của mọi lần chạy (`--budget`) và thử tới 4 lần mỗi request; chưa chặn 0,20 USD, 300.000 token, 4 request mỗi lần chạy | NFR-L3GEN-AI-002 |
| 006-2 | Chưa in provider, model, loại dữ liệu trước request đầu | NFR-L3GEN-SEC-002, AC-L3GEN-028-01 |
| 006-3 | Provider và model viết cứng trong `l3gen._client` | NFR-L3GEN-AI-002 (đổi bằng cấu hình) |
| 006-4 | Provenance thiếu phiên bản prompt, phiên bản công cụ, phiên bản Pyright và Node, mã snapshot; `archdia.llm.json` có prompt và câu trả lời, sổ có model, token, USD | NFR-L3GEN-AI-002 "Tái lập", ADR-2026-005 |
| 006-5 | Hai cổng: `llm.py` (dùng) và `l3slice/gateway.py` (không dùng) | ADR-2026-003 (một chỗ gửi ra ngoài) |
| 006-6 | Cache câu trả lời (kèm văn bản suy luận) và sổ chi phí bật mặc định, nằm ở `evaluation/quote-evidence/` của công cụ, ngoài thư mục output, không bị xóa. Cần tách cache sang công cụ đo và ghi chi phí vào provenance | NFR-L3GEN-SEC-002 "Vòng đời" |

## Liên quan

| Nguồn | Nội dung |
|---|---|
| [NFR-L3GEN-AI-002](../../requirements/nfr/NFR-L3GEN-AI-002.md) | Việc của model, đầu vào, trần, provenance |
| [NFR-L3GEN-SEC-002](../../requirements/nfr/NFR-L3GEN-SEC-002.md) | Dữ liệu gửi ra ngoài, bí mật |
| [ADR-2026-003](../adr/ADR-2026-003.md) | Vì sao tách component này |
| [ADR-2026-004](../adr/ADR-2026-004.md) | Model chỉ gộp nhóm và đặt tên |
