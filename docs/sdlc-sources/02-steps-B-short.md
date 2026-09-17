chi tiết các bước như sau:
 
## B.1 Bước 0 — Proposal *(tuỳ chọn)*
**Không chạy cho từng thay đổi.** Chỉ chạy khi mở một hướng đi mới: sản phẩm mới, thị trường mới, một nỗ lực nhiều quý.
| | |
|---|---|
| **Ai** | Product |
| **Trả lời** | Có nên làm không — vấn đề, thị trường, wedge, business case, ranh giới roadmap |
| **Output** | `product/proposals/PROP-2026Q4-003.md` |
| **Scope** | `org` hoặc `domain` — **không** `system`, vì lúc này có thể chưa biết chạm hệ thống nào |
| **Vòng đời** | **Không chết.** Các Change Set của nó đóng hết thì Proposal vẫn là bản ghi *vì sao đã quyết* |
| **Gate** | Duyệt danh mục theo chu kỳ (quý), không phải gate của quy trình này |
### Gom nhiều Change Set là một truy vấn, không phải một object
Một nỗ lực lớn gồm nhiều thay đổi thì mỗi thay đổi là **một Change Set riêng**, và cả cụm gom lại bằng `derived_from`:
```yaml
# lifecycle/change-sets/CHG-PAY-2026-084/change-set.yaml
derived_from: [PROP-2026Q4-003]
```
```yaml
# lifecycle/change-sets/CHG-CHK-2026-091/change-set.yaml
derived_from: [PROP-2026Q4-003]
```
Muốn xem toàn cụm: truy vấn "mọi Change Set `derived_from` PROP-2026Q4-003". **Không có object "Initiative" phải tạo và bảo trì.**
Lý do mỗi thay đổi là một Change Set riêng chứ không gộp làm một: **baseline phải là tập revision duyệt cùng nhau và release cùng nhau.** Một nỗ lực 6 tháng có 5 lần release thì không thể có một baseline.
### Khi nào bỏ qua
Đa số công việc. Một thay đổi đơn lẻ đi thẳng vào bước 2, `derived_from` để rỗng.
**GOAL và KPI không sống ở Proposal.** Chúng vào `PRD-<SYS>.md` của hệ thống bị chạm, ở bước 4, vì đó là thứ sống cùng hệ thống chứ không chết cùng nỗ lực.
## B.2 Bước 1 — PRD gốc *(chỉ flow New System)*
**Chạy đúng một lần cho mỗi System, trước bước 4.** Bước 4 (FR & AC) giả định `PRD-<SYS>.md` đã tồn tại (Input: "Impact, PRD hiện có") — đúng cho flow Change, nhưng **sai cho New System**: lúc này chưa hề có PRD nào. Bước này lấp khoảng trống đó. Không chạy lại cho các thay đổi sau — từ Change Set thứ hai trở đi, hệ thống đã có PRD, quay lại flow Change bình thường (bước 4 chỉ *bump*).
| | |
|---|---|
| **Ai** | Product |
| **Input** | Proposal nếu có (§B.1), hoặc yêu cầu trực tiếp |
| **Trả lời** | Mục tiêu nghiệp vụ và ranh giới ban đầu của System này |
| **Output** | `product/prd/PRD-<SYS>.md` — GOAL · KPI · Scope · Persona · Assumption · Constraint (PROC §1.2.3) |
| **Scope** | `system` — khác Proposal (org/domain); từ đây `<SYS>` chính thức tồn tại trong `key` |
| **Gate** | Không riêng — bản GOAL/KPI đầu tiên này được duyệt cùng lúc với FR/AC đầu tiên ở **Scope Gate** (bước 4), không tách gate thứ hai |
**Sau bước này, `KHÔNG tạo PRD mới` (§B.5) mới có hiệu lực.** Quy tắc "PRD chỉ bump" ở bước 4 giả định trước đúng một PRD gốc — bước này là cái tạo ra tiền đề đó.
---
## B.3 Bước 2 — Intake & Triage
**Chạy:** `aide impact <mô tả yêu cầu>`
**Trước khi tính impact, ghi lại nguyên văn yêu cầu** — `evidence/requests/CR-PAY-2026-084.yaml` (§PROC 2.5.1). Không diễn giải, không tóm tắt — agent chạy `aide impact` nhận mô tả yêu cầu và tự tạo CR trước, rồi mới phân tích impact dựa trên CR đó.
**Agent làm:** đối chiếu graph, tính flow · tier · blast radius, liệt kê artifact bị chạm và bị stale.
**Người quyết:** tier ở ca ranh giới. Hạ tier phải ghi lý do + người duyệt.
**Output** — `lifecycle/change-sets/<CHG>/impact.yaml`:
```yaml
change_request: CR-PAY-2026-084   # bắt buộc — CI reject nếu CR không tồn tại
touches: [FR-PAY-012]
stale_artifacts: [CMP-PAY-AUTH, API-PAY]
affected_teams: [TEAM-PAYMENT]
external_consumers: []
risk_signals: { pii: true, financial: true }
path_signals: ["services/payment/**"]
tier: T1
flow: change
skipped_with_reason:                        # BẮT BUỘC
  - { area: SVC-reporting, reason: "chỉ đọc EVT cũ, schema không đổi" }
confidence: { graph_coverage: 0.62 }
```
**Xong khi:** có `tier`, `flow`, `confidence`, và `skipped_with_reason` không rỗng.
## B.4 Bước 3 — Change Set Shell
**Chưa có Epic ở bước này** — Epic thật, mang `implements: [FR-...]`, chỉ sinh ở **bước 11** (§B.12), sau khi FR đã tồn tại (bước 4) và sau L2 (bước 7). Bước 3 chỉ tạo khung điều phối của Change Set.
**Một team:** Change Set tự sinh, vô hình. Về sau ở bước 11 bạn sẽ chỉ thấy **một Epic**, và bốn field cam kết liên team của nó để rỗng.
**Nhiều team:** Change Set hiện ra, mỗi team sẽ có một Epic ở bước 11, `blocked_by` bắc qua giữa các Epic.
**Output** — `lifecycle/change-sets/<CHG>/change-set.yaml`:
```yaml
key: CHG-PAY-2026-084
label: "Phase 2 — Trả góp"          # tên người gọi nó; để rỗng nếu là bugfix lẻ
status: draft
objective: { satisfies: [] }        # điền dần ở bước 4
affected_systems: [SYS-PAYMENT]
affected_teams: [TEAM-PAYMENT]
coordination: { mode: compatible-rollout, integration_gate_required: false }
tier: T1
flow: change
```
## B.5 Bước 4 — FR & AC  ⟶ **Scope Gate**
**KHÔNG tạo PRD mới.** Hệ thống đã có `PRD-<SYS>.md` — trừ **New System**, nơi bước này chạy ngay sau §B.2 (PRD gốc mới viết xong).
**Bạn tạo:** `requirements/fr/FR-PAY-041.md`, mỗi FR một file, AC nằm trong.
**Bạn bump `PRD-<SYS>.md`** chỉ khi GOAL / KPI / Scope đổi.
**Mẫu FR** *(dùng luôn, thay `[...]`)*:
```yaml
---
uid:
key: FR-PAY-041
type: functional-requirement
group: normative
scope: system
system: SYS-PAYMENT
status: draft
revision: 1
ownership: { accountable_team: TEAM-PAYMENT, accountable_role: product-owner }
relations:
  satisfies: [GOAL-PAY-004]
  measured_by: [OBS-PAY-011]
---
# FR-PAY-041 — [Tiêu đề]
## Mô tả
[Hành vi nghiệp vụ người dùng thấy. Không mô tả cách làm.]
## Acceptance Criteria
### AC-PAY-041-01
- **given** [tiền đề]
- **when** [hành động]
- **then** [kết quả quan sát được]
- `constrained_by:` [NFR-PERF-001]
- `implementation_target:` [CMP-…, API-…]
- `validated_by:` [TEST-…]
```
**Bốn luật khi viết AC:**
- Số liệu ngưỡng → `constrained_by` tới NFR, **không gõ lại con số**
- Telemetry → `measured_by` tới OBS, **không khai trong FR**
- Entity → tra `domain/glossary`, không định nghĩa lại
- Mơ hồ → tạo OQ ở `lifecycle/change-sets/<CHG>/open-questions/`, **không đoán**
**Scope Gate — Product duyệt.** Sau gate, **chỉ Product** đổi được AC, qua change request.
## B.6 Bước 5 — Domain design *(bỏ được ở T2/T3)*
Chạy khi FR đưa vào khái niệm nghiệp vụ mới hoặc invariant mới.
**Output:** bổ sung `domain/<domain>/glossary.md` + danh sách invariant. **Không** vẽ lại class diagram nếu code đã có.
## B.7 Bước 6 — L1 capability
**Bạn làm:** map mỗi FR mới sang ít nhất một CAP bằng cạnh `covers`.
```yaml
# architecture/l1/CAP-PAY-009.md
relations:
  covers: [FR-PAY-041, FR-PAY-042]
```
Tạo `CAP` mới **chỉ khi** là năng lực nghiệp vụ mới. FR nằm gọn trong CAP sẵn có → chỉ thêm cạnh.
**Bounded context mới** → chuyển sang flow Architecture change, Architecture Gate cần Enterprise Architecture. *(PROC §3.3)*
**Xong khi:** luật coverage #2 xanh — mọi FR có ≥1 CAP `covers`.
## B.8 Bước 7 — L2 + ADR  ⟶ **Architecture Gate**
**Agent đề xuất 2–3 phương án kèm tradeoff.** Ghi cả phương án bị loại và lý do loại.
**Thứ tự bắt buộc:**
1. Viết vấn đề và ràng buộc **trước khi** ai nêu phương án
2. Viết tiêu chí quyết định **trước khi** xem phương án
3. Rồi mới xem phương án
**Bạn tạo hoặc bump:**
- `architecture/l2/CMP-PAY-INSTALLMENT.md` — component mới
- `architecture/l2/CMP-PAY-AUTH.md` — bump `revision: 17 → 18`
- `architecture/adr/ADR-2026-019.md` — nếu có quyết định kiến trúc
- `architecture/threat-model/TM-SYS-PAYMENT.md` — bump nếu chạm bảo mật
### Bảy mục bắt buộc trong một file CMP
Thiếu ba mục cuối là agent phải tự quyết, và quyết đúng hay sai là may rủi:
| Mục | Trả lời |
|---|---|
| Trách nhiệm | Component này gánh phần nào của CAP |
| Cấu trúc bên trong | Chia thế nào, vì sao chia thế |
| Sequence | Luồng chính, dạng diagram-as-code |
| Failure mode | Hỏng ở đâu, hỏng thì sao |
| **Transaction boundary** | Đơn vị nguyên tử tới đâu — commit ở chỗ nào, cái gì nằm ngoài |
| **Idempotency** | Gọi lại hai lần thì sao — khoá idempotency là gì, giữ bao lâu |
| **Concurrency** | Hai request cùng lúc thì sao — optimistic hay pessimistic, khoá ở mức nào |
Ví dụ ba mục cuối cho `CMP-PAY-INSTALLMENT`:
```markdown
## Transaction boundary
Tạo lịch + ghi ledger trong một transaction. Gửi EVT-INSTALLMENT-CREATED
nằm NGOÀI transaction, qua outbox — không để publish fail làm rollback lịch.
## Idempotency
Khoá: `(order_id, term_months)`. Giữ 24h. Gọi lại trong window trả về lịch cũ
kèm 200, không tạo mới, không lỗi.
## Concurrency
Optimistic lock trên `order.version`. Hai request cùng order thì request thứ hai
nhận 409 và client retry — KHÔNG merge, vì hai lịch trả góp cho một đơn là sai nghiệp vụ.
```
**Review:** panel 3 reviewer blind theo vai (security / operability / completeness), class `advisory` — finding tới người, không có vòng sửa tự động. *(PROC §2.3.3)*
**Architecture Gate — Architect chọn phương án.** Authority theo phạm vi rủi ro: T2 trong một component → Tech Lead · cross-component cùng domain → Domain Architect · bounded context mới → + Enterprise Architecture.
**Hệ thống nhiều component — đem gì ra gate.** Không viết một tài liệu SAD gộp toàn hệ thống rồi coi đó là "L2" (vi phạm §1.3.8 — một CMP một component, mọi Change Set sau sẽ chạm cùng file đó). Đem ra gate là **`AVW`** (architecture-view, PROC §1.2.2) — sinh từ các CMP/ADR/threat-model liên quan, `non_normative: true`, ở `generated/architecture-views/`. Nội dung nào trong bản gộp cũ không suy ra được từ CMP/ADR nào cả (rationale gốc, chưa có nơi ở) thì đó là tín hiệu thiếu một CMP hoặc ADR, không phải lý do giữ nó trong view.
## B.9 Bước 8 — UX / UI cấp 1–3 + mock  ⟶ **UI/UX Gate**
Xem **§E**. Bỏ được khi thay đổi không chạm giao diện.
**Chạy song song với bước 5–7, không chờ L1/L2.** UX Flow, Screen Inventory, UI Design (§E.1 cấp 1–3) chỉ cần FR/AC — bắt đầu ngay sau Scope Gate (bước 4), cùng lúc Domain Owner làm bước 5 và Architect làm bước 6–7.
### Dựng mock để duyệt
Spec không trả lời được câu hỏi quan trọng nhất: **người dùng có dùng được không.** Nên trước khi sang L3, dựng một bản trực quan cho người duyệt bấm thử.
**Ba hình thức, chọn theo hoàn cảnh — không hình thức nào bị cấm:**
| Hình thức | Khi nào hợp | Đánh đổi |
|---|---|---|
| **Ảnh tĩnh · Figma** | Thăm dò sớm, luồng chưa chốt | Không dùng token thật → **duyệt cái này, ra cái khác** |
| **HTML/CSS/JS** | Chưa chốt framework, hoặc mock cần sống độc lập với repo | Phải viết lại khi implement |
| **Prototype trên chính stack** | Đã có design token và component | Tốn hơn ảnh, nhưng **không vứt đi** |
Cách chọn: **mock càng gần thứ sẽ chạy thật, giá trị của lần duyệt càng cao.** Ảnh tĩnh duyệt xong vẫn có thể ra một giao diện khác hẳn; prototype trên token thật thì cái được duyệt chính là cái sẽ ship.
Điều **bắt buộc với mọi hình thức**: mock phải dùng **design token thật**, không phải màu và khoảng cách gõ tay. Không có ràng buộc này thì gate duyệt một thứ không tồn tại.
### Mock bao nhiêu màn hình
**Không mock hết.** Mock **hệ thiết kế + các màn hình quyết định cảm nhận sản phẩm** — thường là màn hình người dùng chạm nhiều nhất, màn hình hậu quả cao nhất, và màn hình của người dùng ít khoan dung nhất.
Màn hình còn lại **kế thừa** hệ đã duyệt. Nếu một màn hình sau này cần mẫu chưa có trong hệ, đó là tín hiệu **mở rộng UI Design** — qua change request, không phải tự chế tại chỗ.
### Cái được duyệt không phải cái mock
Mock là `group: derived`, `non_normative: true`, khai `derived_from` tới UXF/SCR/UID và mang luật phân xử:
```yaml
> Khi mock và UXF/SCR/UID bất đồng, **UXF/SCR/UID thắng**.
```
**Thứ được ký ở gate là revision của UXF · SCR · UID.** Mock chỉ là phương tiện trình bày — đúng vai trò của Change Set view ở Scope Gate (§D.1b). Không có luật phân xử này thì mock thành nguồn sự thật thứ hai, và PROC §4.4.4 cấm đúng điều đó.
## B.10 Bước 9 — L3 contracts  ⟶ **Contract Gate** *(nếu breaking)*
**Sinh từ L2 + AC**, đặt ở `tech-specs/<CMP-slug>/` — đúng component đang expose contract đó (§A.1). Bắt buộc Git.
**Breaking hay không** do máy quyết (OpenAPI diff), không do người tự nhận.
**Nếu breaking:**
```yaml
# tech-specs/PAY-INSTALLMENT/api/API-PAY.changelog.yaml
from: v2
to: v3
compatibility: breaking
consumers:                     # DERIVED từ graph — không khai tay
  - { team: TEAM-MOBILE, ack: required, state: not-started }
coexistence: { v2: true, v3: true }
migration_window: { start: 2026-09-15, end: 2026-12-15 }
```
**Contract Gate:** Tech Lead + consumer teams ack. Consumer chính và partner ngoài luôn `ack: required`.
## B.11 Bước 10 — UI Specification — cấp 4
**Cấp 4** tham chiếu field/endpoint của contract nên phải chờ L3 đủ hình dạng, và phải xong **trước khi Contract Gate đóng** (§E.4).
Tách khỏi bước 8 vì phụ thuộc khác nhau: cấp 1–3 cần FR/AC, cấp 4 cần L3. Gộp hai thứ là lý do bản trước không có gate UI — nửa cần L3, nửa không, nên không đặt gate ở đâu được.
### Cấp 1–3 dùng để làm gì, nếu cấp 4 chỉ cần L3 + AC?
Câu hỏi này đúng, và nó lộ ra một lỗi nếu cấp 4 chỉ ghi Input là `L3, AC`: vậy thì cấp 1–3 là ba tài liệu không ai tiêu thụ — và một artifact không ai tiêu thụ là artifact nên xoá (`NT-10`).
Thực tế cấp 1–3 có **hai** người tiêu thụ, và cả hai đều bắt buộc:
| Ai tiêu thụ | Dùng làm gì |
|---|---|
| **UI/UX Gate** | Đây là thứ được **ký**. Gate không ký mock (`derived`), không ký UI Spec (chưa tồn tại) — nó ký revision của `UXF` · `SCR` · `UID` |
| **Cấp 4** | `UIS` **dẫn xuất từ** `SCR` + `UXF` và **bị chi phối bởi** `UID`. Không có chúng thì UI Spec không biết mình đang đặc tả màn hình nào, trong luồng nào, dùng component nào |
Quan hệ thứ hai là quan hệ thật, không phải lý thuyết — nó xuất hiện ngay trong metadata của `UIS`:
```yaml
relations:
  derived_from: [SCR-…-001, UXF-…-002]   # màn hình nào, trong luồng nào
  refines:      [UID-…-003]              # component nào, hành vi nào
  satisfies:    [AC-…-01, …]             # AC nào
```
`refines`, **không phải** `governed_by`. Vocabulary đóng (`PROC §1.3.3`) dành
`governed_by` cho *rule/policy*; `UID` là spec thiết kế, và cấp 4 **làm mịn** nó
ở tầng dưới — đúng định nghĩa của `refines`.
Nên Input đúng của bước 10 là **`L3` · `AC` · cấp 1–3 đã duyệt**, và bảng §B.0 đã ghi theo đó.
**Cách nhớ ranh giới:** cấp 1–3 trả lời *"người dùng thấy gì và đi đường nào"* — quyết được bằng FR/AC. Cấp 4 trả lời *"component nào bind vào field nào của endpoint nào"* — không quyết được trước khi endpoint tồn tại. Hai câu hỏi khác nhau, hai người duyệt khác nhau (`Product + Design` ở UI/UX Gate; `Tech Lead + consumer` ở Contract Gate), nên hai bước.
## B.12 Bước 11 — Epic / Story / Task decomposition
**Task sinh sau L2, không trước.** Trước khi có thiết kế thì task chỉ là phỏng đoán.
```
Change Set  ─→  Epic (một team)  ─→  Story  ─→  Task
                                       │           └─ satisfies ─→  AC
                                       └────────────────────→  Task   (không qua Story — không có AC)
```
**`Task` có hai cha loại trừ nhau: `story:` hoặc `epic:`.** Có AC để tách nhỏ (feature, đổi hành vi quan sát được) → qua `Story`, dùng `story:` — tương đương Jira **Sub-task**. Không có AC nào cả (tech debt, refactor, tích hợp hạ tầng, đổi công cụ nội bộ — không đổi hành vi người dùng thấy) → đi thẳng `epic:`, không tạo Story rỗng chỉ để có nơi treo — tương đương Jira **Task** ngang hàng Story dưới cùng Epic. Cùng `type: task`, không phải hai loại khác nhau.
**Git là nguồn; Jira là bản ghi để PM quản lý, có thể có hoặc không.** Nếu có, nối bằng frontmatter — không đồng bộ hai chiều, không sửa nội dung ở Jira.
### Epic
```yaml
---
key: EPIC-084-PAYMENT
type: epic
group: normative
scope: lifecycle
change_set: CHG-PAY-2026-084
accountable_team: TEAM-PAYMENT
status: not-started
jira_epic: PAY-1204                    # tuỳ chọn
implements: [FR-PAY-041]
affected_components: [CMP-PAY-INSTALLMENT]
# Bốn field dưới: ca MỘT team thì để rỗng, đừng bịa cho đủ
contracts: { produces: [API-PAY-v3], consumes: [] }
blocked_by: []                         # [EPIC-084-IAM] khi chờ team khác
ready_criteria: [contract_frozen, context_valid, tests_green]
---
# EPIC-084-PAYMENT — Thanh toán trả góp (phần backend)
## Phạm vi
[Team này gánh phần nào của Change Set. 2–4 dòng.]
## Story
- STORY-PAY-211 — tạo lịch trả góp
- STORY-PAY-212 — hiển thị tổng phí
## Task (không qua Story — không có AC)
- TASK-PAY-560 — trả nợ kỹ thuật: tách connection pool riêng cho installment worker
```
### Story
```yaml
---
key: STORY-PAY-211
type: story
group: normative
scope: lifecycle
epic: EPIC-084-PAYMENT
status: not-started
jira_story: PAY-1211                   # tuỳ chọn
satisfies: [AC-PAY-041-01]             # BẮT BUỘC khác rỗng
---
# STORY-PAY-211 — Tạo lịch trả góp
## Giao cái gì
[Lát cắt này giao được gì. KHÔNG viết given/when/then — hành vi ở AC-PAY-041-01.]
## Ngoài phạm vi
[Thứ dễ bị hiểu là thuộc story này nhưng không phải.]
## Task
- TASK-PAY-551 — migration TBL-installment-plan
- TASK-PAY-552 — endpoint POST /installment-plans
- TASK-PAY-553 — validation kỳ hạn
```
> **Không viết `given`/`when`/`then` trong Story.** CI reject. Hành vi thuộc AC; Story chỉ trỏ tới. Đây là chỗ NT-01 bị vi phạm thường xuyên nhất.
### Task
**Cha là `story:` hoặc `epic:` — không phải cả hai, không thể để trống cả hai.**
```yaml
---
key: TASK-PAY-551
type: task
group: normative
scope: lifecycle
story: STORY-PAY-211                   # có AC để tách nhỏ → story: (≈ Jira Sub-task)
status: not-started
jira_task: PAY-1551                    # tuỳ chọn
implements: [CMP-PAY-INSTALLMENT]
---
# TASK-PAY-551 — Migration TBL-installment-plan
## Làm gì
[Một đơn vị thực thi. Đủ nhỏ để một context package phủ hết.]
## Xong khi
[Kiểm được bằng máy.]
```
Việc không có AC (tech debt, refactor, tích hợp, đổi công cụ nội bộ) thì bỏ `story:`, khai `epic:` thay vào — không tạo một Story rỗng chỉ để có nơi treo, và không bỏ luôn field cha (mất containment, Task trôi tự do):
```yaml
---
key: TASK-PAY-560
type: task
group: normative
scope: lifecycle
epic: EPIC-084-PAYMENT                 # không có AC → epic: trực tiếp (≈ Jira Task, ngang Story)
status: not-started
jira_task: PAY-1560                    # tuỳ chọn — phía Jira tạo Task, không phải Sub-task
implements: [CMP-PAY-INSTALLMENT]
---
# TASK-PAY-560 — Trả nợ kỹ thuật: tách connection pool riêng cho installment worker
## Làm gì
[Một đơn vị thực thi. Đủ nhỏ để một context package phủ hết.]
## Xong khi
[Kiểm được bằng máy.]
```
### Bug
```yaml
---
key: BUG-PAY-078
type: bug
group: normative
scope: lifecycle
status: triage
jira_bug: PAY-1678                     # tuỳ chọn
violates: [AC-PAY-041-02]              # AC bị vi phạm — rỗng nếu AC chưa tồn tại
severity: high
---
# BUG-PAY-078 — Thẻ không hỗ trợ trả góp vẫn tạo được lịch
## Quan sát được
[Hành vi thật, có bước tái hiện.]
## Kỳ vọng
[Theo AC nào. Nếu không có AC nào nói tới → xem phân nhánh dưới.]
## Phân nhánh (PROC §2.1.4)
- [ ] Code lệch AC → bug thật, sửa code + test tái hiện
- [ ] AC sai hoặc thiếu → **change request trá hình**, chuyển sang flow Change
```
**Ai chốt gì:** agent đề xuất decomposition; **người chốt** `accountable_team`, thứ tự, và `blocked_by`. Regenerate không được xoá thoả thuận đã chốt.
## B.13 Bước 12 — Context package
Xem **§C**.
## B.14 Bước 13 — Implementation plan
Agent viết plan trước khi sửa dòng đầu tiên, ghi vào `evidence/plans/` — **append-only**. Plan phải có, cho từng bước: **file nào đổi · đổi gì · kiểm bằng cách nào**.
Giá trị của plan nằm ở chỗ nó được viết **trước**, nên nó là một **cam kết kiểm chứng được**, không phải mô tả viết lại sau khi xong. Đổi hướng giữa chừng thì ghi revision mới, không sửa file cũ.
```markdown
# PLAN-TASK-PAY-103
## Thứ tự (TDD)
1. RED: test cho AC-PAY-041-01 → fail vì thiếu module `installment-calculator`
2. GREEN: implement calculator
3. RED: test kỳ hạn không hợp lệ → fail
4. GREEN: validation
5. Migration TBL-installment-plan
6. Wire API-PAY-v3 endpoint
## Không làm
- Không đụng CMP-PAY-LEDGER
- Không refactor code xung quanh
```
## B.15 Bước 14 — Implementation
**Bốn luật cứng:** *(PROC §2.2.3)*
1. Agent **không sửa spec**. Mâu thuẫn → tạo OQ và dừng.
2. Agent **không review output của chính mình**.
3. MR **bắt buộc khai quan hệ**:
   ```yaml
   implements: [FR-PAY-041]
   satisfies:  [AC-PAY-041-01, AC-PAY-041-02]
   ```
4. **MR là lát mỏng nhất tự đứng được** — compile được, test xanh, review được một mình.
**Nhật ký quyết định** — agent ghi trong lúc làm, người không sửa tay:
```markdown
# DIARY-TASK-PAY-103
## Diễn giải
- 2026-09-09T10:14Z — AC nói "kỳ hạn hợp lệ" không định nghĩa; hiểu là 3/6/9/12 tháng theo bảng phí hiện có.
## Đi chệch
## Đánh đổi
- 2026-09-09T11:02Z — Tính phí lúc tạo lịch thay vì lúc thanh toán, vì AC-041-01 đòi hiển thị tổng phí ngay.
## Câu hỏi mở
- Kỳ hạn 24 tháng có trong roadmap không? Ảnh hưởng schema.
```
**Isolation:** mỗi MR một worktree riêng, không sửa checkout chính.
## B.16 Bước 15 — Automated validation
CI chạy, theo thứ tự:
```
1. structural + referential + scope     (schema, relation, group/scope hợp lệ)
2. coverage → sinh generated/traceability/TRC-<key>.json
3. ownership + freshness
4. contract lint + breaking detection
5. test suite (kèm RED-first proof + baseline attribution)
```
**Ba trạng thái, không phải hai:** `passed` · `failed` · **`not_run`**. Gộp `not_run` vào `passed` là nói dối.
## B.17 Bước 16 — Review  ⟶ **Component Merge Gate**
**Class do loại artifact quyết, không do người chọn:**
| Đối tượng | Class | Cấu hình |
|---|---|---|
| Code, contract, schema, test | `adversarial` | 1 reviewer, trần 2 vòng, có vòng sửa |
| FR/AC, L1, L2, ADR | `advisory` | 1 pass, finding tới người, không vòng sửa |
**Reviewer KHÔNG được nhận:** nhật ký quyết định, plan, lý lẽ của tác giả. Chúng nằm trong `evidence/` để lưu vết, **không** vì thế mà vào review package — evidence là thứ được ghi lại, không phải thứ mặc định đem cho reviewer đọc.
**Review freeze:** từ lúc ghi receipt tới lúc approve, **cấm ghi vào artifact đã review**. Lỡ ghi → đúng một recovery review.
**Component Merge Gate:** deterministic pass · review pass · test xanh · context còn valid · MR khai đủ quan hệ.
## B.18 Bước 17 — Fix / re-review
- Sửa **chỉ** finding của gate đang fail. Không "tiện tay dọn".
- Fix đổi hành vi → chạy lại evidence.
- Reviewer vòng sau **giữ nguyên ID finding**, chỉ cập nhật status.
- Chạm trần 2 vòng → mở lựa chọn **"chấp nhận như hiện trạng"**, ghi evidence, đi tiếp.
## B.19 Bước 18 — UAT  ⟶ **UAT Gate**
**Chỉ chạy khi Change Set đổi FR hoặc AC, ở T1/T2.** T3 bỏ; T2 bỏ nếu Change Set không đổi hành vi quan sát được (refactor, migration nội bộ, perf fix). *(PROC §2.1.3, §2.2.1)*
**Giả định hạ tầng: staging luôn chạy build mới nhất đã merge.** Deploy lên staging **không phải một bước trong quy trình này** — coi CI/CD tới staging là hạ tầng có sẵn, giống cách bước 15 (Automated validation) không mô tả cách CI được cài. Nếu tổ chức bạn chưa có CD tự động tới staging, đó là việc cần làm trước, không phải việc UAT Gate tự làm.
**Ai làm:** Business Owner — vai trò **độc lập với Product**, người viết AC (PROC §1.4.2, §2.2.5 "Biz Process — nhãn tổ chức trong PRD"). Không cưỡng chế bằng máy được việc một người không tự ký nghiệm thu spec của chính mình (`enforced_by: unenforced`) — nhưng identity ở `human_presence` phải khác identity ở `accountable_role` của FR đang test, và review-log cho thấy sai lệch này thì đó là finding severity cao, không phải chuyện nhỏ.
**Dùng lại Change Set view (CSV, §D.1b) làm script đi test** — không viết "UAT script" riêng. Mục "Tính năng mới" và "Thay đổi hành vi hiện có" của CSV chính là danh sách AC cần đi qua trên staging; CSV đã suy ra từ baseline nên không lệch với AC thật.
**Approval record** (`evidence/approvals/`, `type: approval`) mở rộng đúng khuôn Production Gate (§B.20), thêm `verified_against`:
```yaml
baseline: BL-CHG-084-r3
environment: staging
build: 7f3c9d1                      # commit SHA đang chạy trên staging
verified_against:
  - { key: AC-PAY-041-01, result: pass }
  - { key: AC-PAY-041-02, result: pass }
  - { key: AC-PAY-042-01, result: fail, finding: FIND-PAY-902 }
human_presence: { evidence_id: HT-…, mode: interactive }
approved_by: <danh tính thật — KHÁC accountable_role của FR đang test>
```
**Fail thì route đúng vocabulary đã có ở §2.3.3, không phải một nhánh riêng:**
| Fail vì | Route | Đi đâu |
|---|---|---|
| Build sai so với AC đã duyệt | `patch` | Bug — quay lại bước 14 (Implementation), chạy lại 15–18 |
| AC đúng nhưng thiếu một ca thực tế Business Owner mới thấy | `intent_gap` | Open Question → Product — **không patch code để che gap trong spec** |
Không phân biệt hai đường này thì UAT Gate biến "requirement thiếu" thành "code có bug" — đúng lỗi §2.3.3 đã cảnh báo cho review, giờ lặp lại ở nghiệm thu.
## B.20 Bước 19–21 — Release
**19. Release prep** — `lifecycle/releases/REL-PLAN-NNN.yaml`, nhiều unit có thứ tự:
```yaml
units:
  - { key: REL-DB-114,  type: migration, order: 0, rollback: forward-only }
  - { key: REL-PAY-982, type: backend,   order: 1, rollback: reversible }
  - { key: REL-MOB-403, type: mobile,    order: 2, rollback: none }
partial_failure_policy: halt-and-hold
```
**20. Release approval ⟶ Production Gate** — SRE. Approval record phải có:
```yaml
baseline: BL-CHG-084-r3
covers: [{ key: CMP-PAY-INSTALLMENT, revision: 3, hash: a1b2 }]
human_presence: { evidence_id: HT-…, mode: interactive }
approved_by: <danh tính thật>
commit_sha: 7f3c9d1
accepted_risk:                    # TỰ ĐỘNG — mọi finding còn mở
  - { finding: FIND-PAY-813, severity: medium }
rejected_findings:                # phải khai tường minh
  - { finding: FIND-PAY-815, reason: "consumer đã deprecated từ Q1" }
```
**21. Deploy & verify** — mỗi unit một Deployment Record. Release là lúc revision thành **as-deployed**. Đo hành vi quan sát được ngoài đời có đúng FR/KPI không (không phải "code có đúng AC" — đó là bước 15) xem PROC §2.3.7 (Cấp 3 — Production).
## B.21 Bước 22 — Close / Learn
Trước khi đóng, chạy nghi thức tại gate:
1. Surface nhật ký **verbatim** — không tóm tắt, không lọc
2. Hỏi *"còn gì cho lần sau không?"*
3. Người tick cái muốn giữ, chọn heading — **heading quyết định đích đến**
4. **Câu hỏi mở không promote thành rule**
5. Nhật ký rỗng → ghi lặng lẽ, đi tiếp
Bài học đi vào: `policies/rules/` (rule mới) · `AGENTS.md` (module) · ADR · hoặc **một check deterministic mới**.
**Phạm vi mặc định hẹp nhất** (system). Lên domain/org là hành động tường minh riêng.
## B.22 Ba flow còn lại
§B.3–B.21 viết cho flow **Change** — 80% công việc. Ba flow kia khác ở đâu:
### New system
Giống Change, khác năm chỗ:
| Khác | Chi tiết |
|---|---|
| **Có thêm §B.2 trước bước 2** | Viết `PRD-<SYS>.md` lần đầu — GOAL/KPI/Scope gốc. Flow Change không có bước này vì PRD đã tồn tại |
| **Cổng người dày ở đầu, mỏng ở sau** | Bounded context và domain model là cửa đắt nhất; implement từng FR khi chưa có user thì rủi ro thấp |
| **Vertical slice mẫu do người viết** | Trước khi thả agent, trừ khi đã có golden example phù hợp. Agent học pattern từ slice này |
| **Kế thừa, không dựng lại** | ADR nền tảng, Glossary lõi, reference repo đã có — bước 5 và 6 gần như bằng 0 |
| **Có user thật → chuyển sang Change** | New system là trạng thái tạm thời |
Vẫn đi chiều dọc: một FR đi hết bước 4→16 rồi mới tới FR tiếp.
### Architecture change *(luôn T1)*
Kích hoạt khi: bounded context mới · lật ADR nền tảng · thay đổi cross-domain.
Chèn ba bước **trước** B.8 (L2), theo đúng thứ tự:
```
a. Viết vấn đề và ràng buộc      ← TRƯỚC khi ai nêu phương án
b. Viết tiêu chí quyết định       ← TRƯỚC khi xem phương án
c. Rồi mới xem 2–3 phương án
```
Khác Change:
- Tier **luôn T1**, không tính
- Architecture Gate authority: bounded context mới cần **Domain Architect + Enterprise Architecture**
- ADR mới `supersedes` ADR cũ nếu lật
- Mọi CMP `implements` / `governed_by` ADR cũ thành **stale** → xử lý theo strangler, chỉ nâng artifact bị chạm
### Hotfix
**Câu hỏi đầu tiên, trước khi sửa gì:**
| Hành vi hiện tại sai so với AC, hay AC vốn đã sai? | Làm gì |
|---|---|
| **Code lệch AC** | Bug thật. Sửa code, thêm test tái hiện, gắn `satisfies: [AC-xxx]`. **Không sửa tài liệu** |
| **AC sai hoặc thiếu** | Change request trá hình → **chuyển sang flow Change**, đừng hotfix |
| **Production đang cháy** | Sửa code trước → **backfill trong 48h** |
**Backfill gồm:** bump revision node bị chạm · AC bổ sung nếu hành vi mới là intended · evidence của lần hotfix.
CI gắn `undocumented_change` lên service **cho tới khi xong**. Đây là cơ chế cưỡng chế, không phải nhắc nhở.
 
 