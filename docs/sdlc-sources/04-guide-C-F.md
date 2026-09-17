# C. Context và code agent

## C.1 Compile context package

```
aide context compile --task TASK-PAY-103 --baseline BL-CHG-084-r3
```

Output `context/CTX-TASK-PAY-103.yaml`:

```yaml
key: CTX-TASK-PAY-103
compiled_at: 2026-09-09T09:00:00Z
graph_revision: 893214

objective: TASK-PAY-103
requirements: [FR-PAY-041, AC-PAY-041-01]
design:       [CMP-PAY-INSTALLMENT]
decisions:    [ADR-2026-019]
contracts:    [API-PAY-v3, TBL-installment-plan]
constraints:  [NFR-PERF-001, NFR-SEC-004]
applicable_rules: [VAL-SEC-003, VAL-GO-ERR-002]     # nạp theo trigger
rule_pack: RP-2026-09-a                              # pin theo Change Set
code_scope:   ["services/payment/installment/**", "tests/payment/installment/**"]
golden_examples: [REF-GO-SERVICE-003]
previous_findings: [FIND-PAY-813]

inputs:
  FR-PAY-041:   { revision: 7, hash: a1b2 }
  ADR-2026-019: { revision: 2, hash: c3d4 }

authority:
  baseline: BL-CHG-084-r3
  minimum_status: approved_in_baseline
  reject_if_stale: true
security: { effective_principal: <người khởi tạo>, max_classification: confidential }
```

**Revalidate trước merge.** Hash đổi → chạy lại impact → rebase hoặc escalate.

## C.2 Context theo loại thay đổi

Danh sách tối thiểu. Thiếu một dòng thì chưa đủ điều kiện code.

| Loại | Bắt buộc có |
|---|---|
| **Backend / API** | AC · **L2 của component — gồm transaction boundary, idempotency, concurrency** · API contract · NFR perf + sec · code service + test hiện có · rule API |
| **Database** | AC · **L2 — nhất là transaction boundary** · TBL schema · migration hiện có · NFR retention · rule DB · **chính sách rollback** |
| **Frontend / UI** | AC · UI spec + tokens · API contract phía consume · UX flow · component hiện có · rule accessibility |
| **Security** | AC · threat model · NFR bảo mật · classification của dữ liệu chạm tới · rule sec · finding bảo mật cũ |
| **Bug fix** | AC bị vi phạm · test tái hiện · code vùng lỗi · finding liên quan · **không nạp cả L2** |

## C.3 Prompt cho coding agent

Render từ context package, **không gõ tay**:

```text
Bạn đang thực hiện TASK-PAY-103.

MỤC TIÊU
Implement AC-PAY-041-01 (tạo lịch trả góp + hiển thị tổng phí).

NGUỒN CHUẨN TẮC — chỉ tin những thứ này
- FR-PAY-041 rev 7
- AC-PAY-041-01
- CMP-PAY-INSTALLMENT rev 3
- ADR-2026-019 rev 2
- API-PAY v3 (contract), TBL-installment-plan

RÀNG BUỘC
- NFR-PERF-001: P95 < 500ms
- NFR-SEC-004: không log số thẻ
- Rule: VAL-SEC-003, VAL-GO-ERR-002

CODE LIÊN QUAN
- services/payment/installment/**
- tests/payment/installment/**

PHẠM VI
- Chỉ TASK-PAY-103. Không đụng CMP-PAY-LEDGER. Không refactor xung quanh.

FINDING CŨ CÒN MỞ
- FIND-PAY-813: thiếu validation kỳ hạn ở nhánh retry

ĐẦU RA
- Code + test (RED trước, chứng minh fail đúng lý do)
- MR khai implements/satisfies
- Nhật ký quyết định 4 heading

TRƯỚC KHI BÁO XONG
- Chạy test bắt buộc, ghi evidence
- Đối chiếu từng AC
- Báo mọi chỗ lệch khỏi CMP-PAY-INSTALLMENT

DỪNG VÀ HỎI khi
- Spec mâu thuẫn hoặc thiếu → tạo OQ, KHÔNG đoán
- Phải sửa spec mới làm được → route bad_spec, KHÔNG patch xuống code
```

## C.4 Definition of Ready — đủ điều kiện code

Agent phải trả lời được **tất cả**, nếu không thì task chưa ready:

```
Đang xây cái gì? Vì sao?
AC nào?
Invariant nghiệp vụ nào?
Ràng buộc hệ thống nào (NFR)?
L2 nào mô tả cách làm — gồm transaction boundary, idempotency, concurrency?
Contract API/DB nào?
Hành vi UI nào (nếu có)?
Code nào liên quan?
Rule nào áp dụng?
Finding cũ nào còn mở?
Kiểm đúng bằng cách nào?
```

## C.5 Definition of Done

Xong **chỉ khi tất cả** đúng:

```
AC thoả          AND  design bị chạm đã approved trong baseline
AND  MR merged   AND  test bắt buộc xanh (có RED-first proof)
AND  finding blocking đã resolve hoặc waive có lý do
AND  release approval ghi nhận  AND  deploy thành công
AND  production verification pass
AND  evidence link đầy đủ, có captured_against
```

---

# D. Gate và governance thực thi

## D.1 Ai duyệt cái gì

| Gate | Ai quyết | Bật khi | Chặn cái gì nếu fail |
|---|---|---|---|
| **Scope Gate** | Product | Có FR/AC mới | Không được sang bước 6 |
| **Architecture Gate** | Architect *(federated §3.3)* | T1/T2, hoặc Architecture change | Không được sang bước 9 |
| **UI/UX Gate** | Product + Design | Chạm giao diện ở mức luồng hoặc màn hình mới | **Không được sang bước 9** |
| **Contract Gate** | Tech Lead + consumer ack | Contract breaking | Không được release |
| **Component Merge Gate** | Tech Lead | Mọi MR | Không merge |
| **UAT Gate** | **Business Owner** | T1/T2, Change Set đổi FR/AC | **Không được sang bước 19** |
| **Change Integration Gate** | Tech Lead các team | Nhiều team, `mode != independent` | Không release |
| **Production Gate** | SRE | Mọi release | Không deploy |

## D.1b Bản đem ra gate — Change Set view

Người duyệt không đọc file FR rời rạc. Trước mỗi commitment gate, sinh **Change Set view**:

```
aide csv render --change-set CHG-EKP-2026-002 --baseline BL-r1
→ generated/change-set-views/CSV-CHG-EKP-2026-002.md
```

Bảy mục, tất cả suy ra từ baseline:

```markdown
# Phase 2 — Engineering Knowledge Platform     ← change_set.label

## Mục tiêu                    ← change_set.objective
## Mục tiêu nghiệp vụ đổi      ← diff GOAL/KPI; rỗng nếu không đổi
## Tính năng mới               ← FR mới trong baseline, kèm AC đầy đủ
## Thay đổi hành vi hiện có    ← FR bump revision, hiện diff
## NGOÀI phạm vi lần này       ← FR đã tồn tại nhưng chưa vào baseline nào
## Ràng buộc mới               ← NFR mới hoặc siết chặt
## Câu hỏi mở còn lại          ← OQ chưa đóng
```

Mục **"NGOÀI phạm vi lần này"** là thứ người duyệt luôn hỏi, và nó suy ra được — viết tay thì không ai nhớ liệt kê.

**Chưa có generator (pilot C0+)?** Viết tay, nhưng gắn nhãn cho đúng bản chất và kèm luật phân xử:

```yaml
---
key: CSV-CHG-EKP-2026-002
group: derived
non_normative: true
derived_from: [BL-CHG-002-r1]
hand_written: true          # tạm — bỏ khi có generator
---
> Khi bản này và file FR bất đồng, **FR thắng**.
```

Không có dòng phân xử đó thì bạn vừa tạo nguồn sự thật thứ hai.

**Đừng đặt tên file là `PRD-…-phase2.md`** — người sau sẽ tưởng nó là nguồn. Tên file là `CSV-<CHG-key>.md`; tiêu đề hiển thị để "Phase 2 — PRD" cho quen mắt.

## D.2 Checklist mỗi gate

**Scope Gate** — CSV đã sinh từ baseline hiện tại · FR có ≥1 AC · AC dạng given/when/then · số liệu là reference không phải literal · OQ có owner + due · không FR nào approved mà đang blocked_by OQ mở

**Architecture Gate** — có ≥2 phương án + tradeoff · phương án bị loại có ghi lý do · tiêu chí quyết định ghi trước · threat model cập nhật nếu chạm bảo mật · mọi FR có CAP `covers` · nếu đem `AVW` ra gate thì nó `derived_from` CMP/ADR thật, không phải nguồn

**UI/UX Gate** — mock dựng từ token thật, không phải màu cứng · tương phản đạt ngưỡng ở **cả hai** chế độ sáng/tối · a11y tự động xanh · mock khai `non_normative: true` kèm luật phân xử · mọi màn hình trong screen inventory có layout xác định · **đi hết luồng chính mà không cần ai hướng dẫn** · mỗi màn hình đúng **một** hành động chính · trạng thái rỗng · tải · lỗi đều có · xem trên **thiết bị chính thật**, không phải trình giả lập · chuỗi dài nhất trong mọi ngôn ngữ không làm vỡ bố cục

**Contract Gate** — breaking detection chạy bằng máy · consumer list derived từ graph · consumer chính + partner đã ack · có migration window · coexistence khai rõ

**Component Merge Gate** — deterministic pass · review pass · test xanh có RED-first · context còn valid · MR khai đủ quan hệ · MR là lát mỏng tự đứng được

**UAT Gate** — build trên staging khớp `build`/commit SHA đang test · CSV đã sinh từ baseline hiện tại làm script đi test · mọi AC trong "Tính năng mới" + "Thay đổi hành vi hiện có" của CSV có `result: pass/fail` · `approved_by` khác `accountable_role` của FR đang test · fail được route đúng `patch` (bug) hoặc `intent_gap` (thiếu AC → OQ), không lẫn vào nhau · có bằng chứng người thật (§2.2.1)

**Production Gate** — release plan có ordering + rollback boundary · unit không rollback được đã khai · evidence đủ · approval có bằng chứng người thật + commit SHA

## D.3 Thao tác với finding

```
Tạo:      agent review sinh, có finding_key (rule_id + location_anchor + fingerprint)
Route:    intent_gap | bad_spec | patch | defer
          → bad_spec = sửa spec tầng trên rồi regenerate, KHÔNG patch xuống code
Xử lý:    ACCEPTED | REJECTED | WAIVED | NOT_APPLICABLE | DUPLICATE | NEEDS_MORE_EVIDENCE
Bác bỏ:   phải khai lý do khác rỗng. CẤM suy từ feedback chung chung
Vòng sau: giữ nguyên ID, chỉ cập nhật status. CẤM đánh số lại
```

## D.4 Waiver và override

```
1. Lựa chọn phải được offer tường minh (không cờ trần)
2. Một thao tác của người
3. Lý do khác rỗng
4. Ghi evidence, dùng một lần
5. CẤM ở chế độ chạy tự động
```

Waiver chỉ cấp được ở **tầng sở hữu rule**. Waiver lặp lại trên cùng một rule = tín hiệu rule sai, đưa vào vòng học.

**Nhưng trước khi sửa rule, kiểm nguyên nhân.** Ba waiver cho cùng một rule vì ba lý do khác nhau là **ba vấn đề**, không phải một — một bản vá sẽ chỉ phủ được một trong ba. Đếm triệu chứng giống nhau không phải chẩn đoán; đó là tín hiệu để **điều tra**, không phải kết luận đã có. *(Ca thật: hai trong ba waiver hoá ra là vòng tròn bootstrap thật — sửa ở PROC §1.3.6, không phải ở rule bị waiver. Waiver thứ ba không có vòng tròn nào; lỗ hổng nằm ở thiếu trigger của gate khác, sửa gate đó mới đúng chỗ.)*

## D.5 Hai chỉ số phải công khai

| Chỉ số | Ý nghĩa nếu cao |
|---|---|
| Tỷ lệ rule `enforced_by: unenforced` | Quy trình phần lớn là lời khuyên |
| Tỷ lệ `accepted_risk` mỗi gate | Gate đang thành nghi thức |

---

# E. UI / UX

## E.1 Bốn cấp

```
UX Flow          →  Screen Inventory  →  UI Design      →│→  UI Specification
luồng người dùng    danh mục màn hình    bố cục, visual  │    hành vi máy đọc được
UXF-<SYS>-NNN       SCR-<SYS>-NNN        UID-<SYS>-NNN   │    UIS-<SYS>-NNN
design/ux/          design/ux/           design/ui/      │    design/ui/
                                                          │
          ├──────── cấp 1–3: chỉ cần FR/AC ─────────────┤
                              +                          │
                      UI mock (UIM, derived)             │
                              ↓                          │
                       ⟶ UI/UX GATE ⟶                    │  ⟵ cần L3, chốt sau bước 9
                                                          │
                                                    Contract Gate
```

**Ranh giới gate nằm giữa cấp 3 và cấp 4, và nó không tuỳ tiện.** Cấp 1–3 chỉ cần FR/AC nên duyệt được sớm; cấp 4 tham chiếu field và endpoint nên không tồn tại trước L3. Đó cũng là ranh giới đúng về mặt người duyệt: Product và Design review *luồng và hình thức*, không review binding máy đọc.

## E.2 UI Specification — cấp duy nhất agent đọc

Figma đẹp không giúp agent implement. UI Spec phải máy đọc được:

*(Cấp 1–3 không vô dụng — chỉ không phải cho agent. UI/UX Gate ký chính revision của chúng, và UIS `derived_from`/`refines` chúng để biết đang đặc tả màn hình nào. Xem §B.11 "Cấp 1–3 dùng để làm gì".)*

```yaml
component: RegistrationForm
states: [idle, submitting, success, error]
fields:
  - { name: term, type: select, options_from: API-PAY-v3#terms, required: true }
validation:
  - { field: term, rule: "∈ {3,6,9,12}", message_key: err.term.invalid }
behavior:
  - on: submit
    when: valid
    then: POST API-PAY-v3/installment-plans
  - on: error.409
    then: show message_key=err.duplicate, giữ nguyên form
tokens: [color.primary, spacing.md]
a11y: { focus_order: [term, submit], label_required: true }
```

## E.3 Khi nào cần Figma

| Cần Figma | Không cần |
|---|---|
| Màn hình mới, luồng mới | Thêm field vào form đã có |
| Đổi visual language, token | Sửa validation message |
| Component chưa có trong design system | Dùng lại component có sẵn |

**Có Figma vẫn phải có UI Spec ở Git.** Figma là nguồn cho *visual*; Git là nguồn cho *hành vi*.

## E.4 Gate

**Hai điểm kiểm, hai mục đích khác nhau.**

### UI/UX Gate — cấp 1–3, TRƯỚC L3

| | |
|---|---|
| **Trả lời** | Người dùng có dùng được không? |
| **Ai quyết** | Product + Design |
| **Bật khi** | Chạm giao diện ở mức **luồng hoặc màn hình mới**. Bỏ khi chỉ thêm field vào form đã có |
| **Đem ra** | UI mock (`UIM`) — `derived`, `non_normative` |
| **Được ký** | Revision của UXF · SCR · UID — **không phải mock** |
| **Chặn** | Không được sang bước 9 |

Checklist ở §D.2. Điều chỉ gate này kiểm được: **đi hết luồng chính mà không cần ai hướng dẫn.** Không spec nào chứng minh được điều đó, và đo sau khi production thì đã muộn.

### Contract Gate — cấp 4, SAU L3

UI Spec là input bắt buộc của Contract Gate khi thay đổi chạm giao diện, và là input của context package cho task frontend. Không đổi so với trước.

### Timing

```text
Scope Gate → cấp 1–3 + mock → UI/UX GATE → L3 → cấp 4 → Contract Gate
             (song song bước 5–7)          (bước 9)
```

**Mock không thay UI Spec cho agent.** Agent đọc `UIS` và design token; mock là đường cho *người* duyệt. Hai đường phục vụ hai đối tượng, và trộn chúng là cách nhanh nhất tạo nguồn sự thật thứ hai (PROC §4.4.4).

**Timing:** UX Flow, Screen Inventory, UI Design (cấp 1–3) chỉ cần FR/AC — làm sớm, song song bước 5–7 (EXEC B.9). UI Specification (cấp 4) tham chiếu field/endpoint hợp đồng nên chốt cùng nhịp với L3 (bước 9), không sớm hơn được.

---

# F. Ví dụ đầy đủ — thêm "thanh toán trả góp" vào PaymentHub

Flow **Change**, tier **T1**, một team.

## F.1 Bảng delta

| Bước | Tạo mới | Bump revision | Không đụng |
|---|---|---|---|
| 2–3 | `CHG-PAY-2026-084` | — | — |
| 4 | `FR-PAY-041..045` + AC · `GOAL-PAY-004` · `KPI-PAY-007` | `PRD-PAYMENTHUB` *chỉ khi GOAL/KPI/Scope đổi* | PRD nếu chỉ thêm FR |
| 6 | `CAP-PAY-009` *nếu năng lực mới* · cạnh `covers` | `L1` mapping | L1 nếu nằm gọn trong CAP cũ |
| 7 | `CMP-PAY-INSTALLMENT` · `ADR-2026-019` | `CMP-PAY-AUTH` r17→r18 · threat model | CMP không liên quan |
| 8 | `UXF-PAY-004` · `SCR-PAY-011` · `UIS-PAY-011` | — | design system tokens |
| 9 | `TBL-installment-plan` · `EVT-INSTALLMENT-CREATED` | `API-PAY` r14→r15, v2→**v3** | — |
| 11 | — *(1 team: không tạo WP)* | — | — |
| 12–16 | `CTX-…` · `PLAN-…` · MR · `DIARY-…` · `TRC-…` · review · finding | — | — |
| 19–21 | `REL-PLAN-084` · deployment record · production verification | — | — |

## F.2 Ba điểm dễ sai

**`CMP-PAY-INSTALLMENT` sinh trong epic nhưng là node của System.** Nằm ở `architecture/l2/`, mang `system: SYS-PAYMENT`, sống tiếp sau khi CHG-084 đóng. Cái thuộc epic chỉ là baseline.

**Không có file nào tên `L2-EPIC-084.md`.** Muốn xem epic đổi gì → sinh `generated/change-set-views/CSV-CHG-PAY-2026-084.md`.

**`API-PAY` v2→v3 breaking** → Contract Gate. Consumer list derived. Mobile `ack: required`. Coexistence + migration window 3 tháng.

## F.3 Ai đọc gì

| Vai | Đọc | Không đọc |
|---|---|---|
| Product ở Scope Gate | 5 FR + AC mới, GOAL bị chạm | Toàn bộ PRD |
| Architect ở Arch Gate | 2–3 phương án, CMP bị chạm, ADR liên quan | Toàn bộ L2 |
| **Agent implement** | **Context package** — 1–2 CMP + contract + NFR + rule + golden example | Cả L2, cả PRD, cả epic |
| Team khác | Revision **as-deployed** | Baseline đang dở |

## F.4 Nếu là bounded context mới

Flow → **Architecture change**. Tier luôn T1. Architecture Gate cần **Domain Architect + Enterprise Architecture**. L1 thêm `SVC` mới + ranh giới context. Glossary domain có thể phải tách. ADR ghi rõ vì sao tách chứ không mở rộng context cũ.

## F.5 Nếu nhiều team

Change Set hiện ra · mỗi team một Epic · `EPIC-084-MOBILE` `blocked_by: [EPIC-084-PAYMENT]` vì mobile cần API v3 trước · Change Integration Gate bật · mode `compatible-rollout` nên mobile migrate theo nhịp của họ.

---