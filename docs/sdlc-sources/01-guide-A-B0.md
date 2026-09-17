# Agentic SDLC — Execution Guide

**Tài liệu này nói *làm gì*. Không nói *vì sao*.** Mọi lý do, lập luận và đánh đổi nằm ở `process-working.md` (PROC-SDLC-001); ở đây chỉ trích mục để tra khi cần.

Quan hệ hai tài liệu:

| | `process-working.md` | `execution-guide-working.md` *(tài liệu này)* |
|---|---|---|
| Trả lời | Mô hình là gì, vì sao chọn thế | Tôi phải làm gì, ở đâu, ra cái gì |
| Ai đọc | Người phải đồng ý với mô hình | Người đang làm việc |
| Đọc khi | Một lần, lúc onboard hoặc lúc muốn đổi mô hình | Mỗi lần làm một bước |

Tra nhanh: **§A** thư mục · **§B** 23 bước · **§C** context và prompt cho agent · **§D** gate và governance · **§E** UI/UX · **§F** ví dụ đầy đủ · **§G** theo vai · **§H** rollout.

---

# A. Cấu trúc thư mục

## A.1 Cây chuẩn

> **Giả định: một repo = một System.** Cây dưới không có trục system vì không cần — mọi artifact trong repo này thuộc về cùng một System, và `<SYS>` trong `key` chỉ để ID unique toàn tổ chức.
>
> Nhiều System thì **nhiều repo**, mỗi repo một cây như dưới. Tham chiếu chéo (ví dụ `depends_on: API-IAM-v2` ở repo khác) đi qua **metadata graph tập trung** (PROC §4.4.2) chứ không qua đường dẫn file — nên nó chỉ chạy được từ mức C1 trở lên. Ở pilot C0+ với một System thì không gặp ca này.
>
> Nếu sau này thật sự cần monorepo nhiều System, thêm một tầng `systems/<SYS>/` bọc từ `product/` tới `observability/`; `lifecycle/`, `evidence/`, `policies/`, `registry/`, `generated/` vẫn ở gốc vì chúng cắt ngang mọi System.

```text
repo/
│
├── .aide/
│   │
│   ├── product/                          ← SCOPE TIER, sống lâu                              [Normative]
│   │   ├── vision/                      VISION-<SCOPE>.md     org hoặc system
│   │   ├── proposals/                   PROP-YYYYQN-NNN.md    org/domain — KHÔNG chết
│   │   └── prd/                         PRD-<SYS>.md          ← MỘT PRD cho mỗi System
│   │
│   ├── requirements/                                                                          [Normative]
│   │   ├── fr/                          FR-<SYS>-NNN.md       ← AC nằm trong file FR
│   │   └── nfr/                         NFR-<SCOPE>-<CAT>-NNN.md
│   │
│   ├── domain/                                                                                [Normative]
│   │   ├── glossary-core.md
│   │   └── <domain>/glossary.md
│   │
│   ├── architecture/                                                                          [Normative]
│   │   ├── l1/                          CAP-<SYS>-NNN.md · SVC-<SYS>-NNN.md
│   │   ├── l2/                          CMP-<SYS>-NNN.md
│   │   ├── adr/                         ADR-YYYY-NNN.md
│   │   └── threat-model/                TM-<SYS>.md
│   │
│   ├── tech-specs/                      ← L3, BẮT BUỘC ở Git — chia theo COMPONENT             [Normative]
│   │   └── <CMP-slug>/                  chỉ component sở hữu ≥1 API/TBL/EVT mới có thư mục
│   │       ├── api/                     API-<SYS>-<CMP>-vN.md
│   │       ├── events/                  EVT-<SYS>-<CMP>-<topic>.md
│   │       └── schema/                  TBL-<SYS>-<CMP>.md
│   │
│   ├── design/                                                                                [Normative]
│   │   ├── ux/                          UXF-<SYS>-NNN.md · SCR-<SYS>-NNN.md
│   │   └── ui/                          UID-<SYS>-NNN.md · UIS-<SYS>-NNN.md · tokens/
│   │
│   ├── observability/                   OBS-<SYS>-NNN.md                                     [Normative]
│   │
│   ├── lifecycle/                       ← normative-lifecycle: điều phối + work item; Git là nguồn, Jira là bản ghi   [Normative]
│   │   ├── change-sets/
│   │   │   └── CHG-<SYS>-YYYY-NNN/
│   │   │       ├── change-set.yaml                                                            [Normative]
│   │   │       ├── impact.yaml                                                                [Derived — sinh từ graph, cấm sửa tay]
│   │   │       ├── baseline/BL-r<n>.yaml                                                      [Normative — tập revision đã duyệt]
│   │   │       └── open-questions/      OQ-<SYS>-NNN.md                                       [Normative]
│   │   ├── epics/                       EPIC-NNN-<TEAM>.md                                    [Normative]
│   │   ├── stories/                     STORY-<SYS>-NNN.md                                    [Normative]
│   │   ├── tasks/                       TASK-<SYS>-NNN.md                                     [Normative]
│   │   ├── bugs/                        BUG-<SYS>-NNN.md                                      [Normative]
│   │   └── releases/                    REL-PLAN-NNN.yaml                                     [Normative]
│   │
│   ├── evidence/                        ← TOÀN BỘ nhóm Evidence · append-only · shard theo clone   [Evidence]
│   │   ├── requests/                    CR-<SYS>-NNN.yaml     yêu cầu gốc, nguyên văn
│   │   ├── context/                     CTX-<task-key>.yaml   snapshot agent đã thấy
│   │   ├── plans/                       PLAN-<task-key>.md    agent định làm gì
│   │   ├── diaries/                     DIARY-<task-key>.md   agent đã làm gì
│   │   ├── reviews/                     REVIEW-NNN.yaml · RCPT-NNN.yaml
│   │   ├── findings/                    FIND-<SYS>-NNN.yaml
│   │   ├── approvals/                   approval-NNN.yaml
│   │   ├── tests/
│   │   ├── deployments/
│   │   └── production/
│   │
│   ├── policies/                                                                              [Normative]
│   │   ├── rules/                       VAL-<GRP>-NNN.yaml + fixtures/
│   │   ├── gates/                       GATE-<NAME>.yaml
│   │   └── eval/                        EVAL-<AGENT>-NNN.yaml
│   │
│   ├── registry/                                                                              [Normative]
│   │   ├── REG-TYPE-001.md              Type Registry
│   │   ├── REG-OWNER-001.md             Ownership Registry
│   │   └── REG-REPO-001.md              Reference repo registry
│   │
│   └── generated/                       ← KHÔNG BAO GIỜ SỬA TAY                               [Derived]
│       ├── traceability/                TRC-<stage>-<key>.json
│       ├── change-set-views/            CSV-<CHG-key>.md
│       ├── architecture-views/          AVW-<key>.md — bản gộp CMP/API/TBL/EVT gửi review
│       └── diagrams/
│
├── AGENTS.md                            root                                              [Operational]
├── src/          (mỗi module có AGENTS.md riêng nếu khác root)
└── tests/
```

> **`TBL`/`API`/`EVT` đều là `.md`, không phải `.sql`/`.yaml`.** Spec chuẩn tắc phải mang frontmatter (§A.4) và bị `hash-artifact`/`check-sdlc` quét — chỉ file `.md` làm được cả hai; DDL (cho `TBL`) hoặc OpenAPI/schema sự kiện (cho `API`/`EVT`) nằm trong một khối mã bên trong file spec đó, không phải file rời. Migration **chạy được**, sinh ra từ khối DDL đó bằng script trích xuất, **không phải artifact chuẩn tắc** — nó là sản phẩm của task implement, sống ở `**/migrations/` (đã liệt `irreversible` — PROC §2.5.1), không mang frontmatter và không bị check-sdlc quét. Một `.yaml` changelog riêng (ví dụ breaking-change diff ở §B.10) không phải spec chuẩn tắc, không cần frontmatter, nên giữ `.yaml` được.

> **`tech-specs/` chia theo component, không theo loại contract.** Một component thường sinh ra cả API + schema + event cùng lúc — gộp theo component để agent load context một task bằng một `glob`. "Liệt mọi API của hệ thống" là việc của graph/`traceability.json` (NT-11 — *"identity thì graph là canonical"*), không phải đi bộ thư mục. Component không sở hữu API/TBL/EVT nào (ví dụ frontend thuần tiêu thụ qua gateway) **không có** thư mục con — đừng tạo `api/` rỗng cho đủ.

## A.2 Bảy luật thư mục

**1. Thiết kế và yêu cầu KHÔNG bao giờ nằm dưới `lifecycle/`.**
Change Set chứa: `change-set.yaml`, `impact.yaml`, `baseline/`, `open-questions/`. Hết. Thiết kế nằm ở `architecture/`, `tech-specs/`, `requirements/` — bump revision, không tạo file mới trong thư mục epic. *(PROC §1.2.2)*

CI reject file trong `lifecycle/` mang `type` thuộc nhóm design hoặc requirement.

**2. `product/` là scope tier, `lifecycle/` là lifecycle object.** Đây là §1.2.2 hiện lên trong filesystem. Proposal và PRD sống lâu; Change Set và work item chết khi xong việc.

Nhưng **cây chia theo nhóm artifact, không chia theo tuổi thọ** — `lifecycle/` chứa toàn bộ nhóm **normative-lifecycle**: đơn vị điều phối (Change Set), work item (Epic/Story/Task/Bug), và **Release Plan** — cả năm đều `group: normative` + `scope: lifecycle` trong registry (§1.3.1), nên `releases/` là sibling **trong** `lifecycle/`, không phải top-level riêng (PROC §1.2.2 dòng "Ranh giới: cái gì thuộc đâu" đã xếp Release Plan chung rổ với baseline/impact report/OQ — cùng bên Change Set). Loại khác mang tầng Lifecycle nhưng **khác nhóm** thì nằm chỗ khác: `CSV` → `generated/` (derived), `MR` → chính repo (derived), `PLAN` → `evidence/plans/` (evidence). Vòng đời ngắn không phải tiêu chí xếp thư mục — **nhóm** mới là tiêu chí.

**3. Story KHÔNG chứa hành vi.** Không có `given`/`when`/`then` trong file Story — hành vi thuộc AC, Story chỉ `satisfies` tới nó. *(PROC §1.2.4)* `enforced_by: deterministic-check` — VAL-WORK-001.

**4. `generated/` không bao giờ sửa tay.** Sửa nguồn rồi sinh lại. *(PROC §1.2.1)*

**5. Một artifact một file.** AC nằm trong file FR của nó. GOAL/KPI nằm trong PRD.

**6. `evidence/` chứa TOÀN BỘ nhóm Evidence, và append-only.** Review, receipt, finding, approval, context snapshot, **implementation plan**, nhật ký, test, deployment — tất cả. Sai thì thêm bản đính chính, không sửa file cũ. Ghi theo shard `<host>-<clone>` để nhiều worktree không conflict. *(PROC §4.4.3)*

Ba thư mục con là **bộ ba của một lượt agent chạy**, cùng `<task-key>`: `context/` — agent **thấy gì** · `plans/` — agent **định làm gì** · `diaries/` — agent **đã làm gì**. Append-only là cái làm cho plan có nghĩa: kế hoạch sửa được sau khi làm xong thì không chứng minh được điều gì. Replan là revision mới, và số lần replan tự nó là tín hiệu.

Đừng nhầm với `lifecycle/releases/`: đó là **Release Plan** (normative — sửa được qua review, đem ra Production Gate), khác hẳn Implementation Plan dù tên gần giống. Approval của release thì nằm ở `evidence/approvals/`, không nằm cạnh Release Plan.

**7. `generated/` không gitignore cả cục.** Tách theo hai loại: nội dung **được ký hoặc được trích dẫn ở nơi khác** (CSV đem ra gate, `AVW` gửi review, diagram được link từ tài liệu khác) — **không bao giờ** gitignore, vì đó là bằng chứng: "gắn commit SHA của thứ được duyệt" (PROC §2.2.1) vô nghĩa nếu bản đó không tồn tại ở đúng commit. Nội dung **sinh lại mỗi lần CI chạy, không ai ký lên nó** (`traceability/`, coverage report) — được gitignore theo dự án. `hand_written: true` (§D.1b) là dấu hiệu chắc chắn nhất cho loại phải commit: nếu người phải viết tay thì gitignore nghĩa là xoá công sức viết tay ngay khi có ai `clone` sạch.

## A.3 Đặt tên và ID

```
key    = <PREFIX>-<SYSTEM>-<NNN>        FR-PAY-041, CMP-PAY-INSTALLMENT
uid    = ULID, tooling sinh, không gõ tay
file   = <key>.md  (hoặc .yaml/.json theo loại)
```

Prefix hợp lệ: xem `registry/REG-TYPE-001.md`. Thêm prefix mới = thêm một dòng vào registry qua PR. *(PROC §1.3.1)*

## A.4 Frontmatter tối thiểu

Dán vào mọi artifact chuẩn tắc:

```yaml
---
uid:      # ULID — để trống, chạy script cấp trước khi commit
key: FR-PAY-041
type: functional-requirement
group: normative
scope: system                    # normative BẮT BUỘC ∈ {org, domain, system}
system: SYS-PAYMENT
status: draft                    # draft → in-review → approved → deprecated
revision: 1

ownership:
  accountable_team: TEAM-PAYMENT
  accountable_role: product-owner

relations:
  satisfies: [GOAL-PAY-004]
  constrained_by: [NFR-PERF-001]

verified_at: 2026-09-09
verified_against:
  - { key: GOAL-PAY-004, revision: 3, hash: abc123 }

classification: internal
ai_assisted: true
---
```

Evidence thì thêm `captured_against` thay cho `verified_against`:

```yaml
captured_against:
  artifacts: [{ key: CMP-PAY-AUTH, revision: 18, hash: a1b2 }]
  code_tree: 7f3c9d1
  graph_revision: 893214
```

---

# B. 23 bước triển khai

## B.0 Bảng tổng

| # | Bước | Ai làm | Input | Output | Thư mục | Gate | CLI/Skill `aide` |
|---|---|---|---|---|---|---|---|
| 0 | Proposal *(tuỳ chọn)* | Product | Yêu cầu mở hướng đi mới | Proposal | `product/proposals/` | — | CLI — `aide generate proposal` |
| 1 | PRD gốc *(chỉ New System)* | Product | Proposal nếu có, hoặc yêu cầu trực tiếp | `PRD-<SYS>.md` gốc — GOAL/KPI/Scope | `product/prd/` | *(duyệt cùng Scope Gate ở bước 4)* | CLI — `aide generate prd` |
| 2 | Intake & Triage | Product + Tech Lead | Yêu cầu | CR *(evidence)* · Impact report, tier, flow | `evidence/requests/`, `lifecycle/change-sets/<CHG>/impact.yaml` | — | Cả hai — `aide tier suggest` (CLI) + `/aide-intake` (skill, viết impact report) |
| 3 | Change Set Shell | Tự sinh | Impact | Change Set khung | `lifecycle/change-sets/<CHG>/change-set.yaml` | — | CLI — `aide changeset init` |
| 4 | FR & AC | **Product** | Impact, PRD hiện có | FR mới + AC · PRD *bump nếu GOAL/KPI/Scope đổi* | `requirements/fr/` (+ `product/prd/` nếu bump) | **Scope Gate** | Cả hai — `aide generate fr` (CLI) + `/aide-spec-draft`, `/aide-spec-review` (skill) |
| 5 | Domain design | Domain Owner | FR, AC | Glossary bổ sung, invariant | `domain/` | — | CLI — `aide generate domain` |
| 6 | L1 — capability | Architect | FR, AC | Cạnh `covers`, CAP mới nếu có | `architecture/l1/` | *(bounded context mới → Arch Gate)* | CLI — `aide generate l1` |
| 7 | L2 + ADR | **Architect** | L1, FR, AC, NFR | CMP mới hoặc revision, ADR, threat model | `architecture/l2/`, `adr/` | **Architecture Gate** | Cả hai — `aide generate l2/adr` (CLI) + `/aide-design-propose`, `/aide-design-review` (skill — panel 3 vai là GĐ6, Phase 1 chỉ 1 reviewer) |
| 8 | UX / UI — cấp 1–3 + mock | Design + Tech Lead | FR, AC | UX flow, screen inventory, UI design, **UI mock** | `design/ux/`, `design/ui/`, `generated/ui-mocks/` | **UI/UX Gate** | Cả hai — `aide generate ux/ui` (CLI) + mock dựng bằng Artifact/code thật (không phải skill riêng của `aide`) |
| 9 | L3 — contracts | **Tech Lead** | L2, AC | API / TBL / EVT | `tech-specs/` | **Contract Gate** *nếu breaking* | Cả hai — `aide generate api/tbl/evt`, `aide verify --contract` (CLI) + `/aide-contract-draft`, `/aide-code-review` (skill) |
| 10 | UI Specification — cấp 4 | Design + Tech Lead | **L3** · AC · **cấp 1–3 đã duyệt** | UI spec máy đọc được | `design/ui/` | *(input của Contract Gate)* | CLI — `aide generate ui-spec` |
| 11 | Epic / Story / Task decomposition | Tech Lead | AC, L2, L3 | Epic, Story, Task | `lifecycle/` | — | Cả hai — `aide generate epic/story/task` (CLI) + `/aide-task-decompose` (skill) |
| 12 | Context package | Platform *(tự động)* | Task, graph, baseline | Context package | `evidence/context/` | — | CLI — `aide context compile` |
| 13 | Implementation plan | Agent → Dev | Context package | Plan có bước + cách kiểm từng bước | `evidence/plans/` | — | Cả hai — `aide generate plan` (CLI) + `/aide-plan-draft` (skill) |
| 14 | Implementation | **Developer** + agent | Context package, plan | MR, nhật ký quyết định | repo; `evidence/diaries/` | — | Skill — Implementer là Claude Code (không phải skill riêng của `aide`, chỉ giới hạn quyền); `/aide-diary-log` ghi nền + `aide diary log` (CLI, phần khung) |
| 15 | Automated validation | CI | MR | Test result, coverage, `traceability.json` | `evidence/tests/`, `generated/traceability/` | — | CLI — `aide verify` trong CI |
| 16 | Review | Agent + **Tech Lead** | MR, evidence | Review pass, receipt, finding | `evidence/reviews/`, `evidence/findings/` | **Component Merge Gate** | Cả hai — `/aide-code-review` (skill) + `aide finding reconcile`, `aide gate approve GATE-MERGE` (CLI) |
| 17 | Fix / re-review | Developer | Finding | MR mới, review pass mới | như trên | — | Cả hai — lặp lại bước 16 |
| 18 | UAT | **Business Owner** | MR đã merge (build trên staging) · AC baseline | UAT approval record | `evidence/approvals/` | **UAT Gate** *T1/T2 nếu Change Set đổi FR/AC* | CLI — `aide csv render`, `aide gate approve GATE-UAT --approver` (chặn nếu approver = accountable_role của FR) |
| 19 | Release prep | SRE | Change Set đã ready | Release plan | `lifecycle/releases/` | **Change Integration Gate** *nếu nhiều team* | — *(ngoài phạm vi `aide` hiện tại)* |
| 20 | Release approval | **SRE** | Release plan, evidence | Approval record | `evidence/approvals/` | **Production Gate** | CLI — `aide gate approve GATE-PRODUCTION` |
| 21 | Deploy & verify | SRE | Approval | Deployment record, production verification | `evidence/deployments/`, `production/` | — | — *(ngoài phạm vi `aide` hiện tại — hạ tầng CI/CD)* |
| 22 | Close / learn | Product + Governance | Nhật ký, finding, KPI | Rule/ADR/AGENTS.md cập nhật | `policies/`, `AGENTS.md` | *(knowledge promotion)* | CLI — `aide diary surface` (nghi thức verbatim §2.5.5); quyết định vẫn là người |

**Cột `CLI/Skill aide` mô tả một tool tham chiếu cụ thể (`aide`), không phải một phần bắt buộc của PROC/EXEC** — tổ chức dùng tool khác thì bỏ qua cột này, các cột còn lại không đổi. CLI = deterministic (`aide <verb>`, chạy shell/CI); Skill = agent LLM (`/aide-<tên>`, chạy trong Claude Code). Nhiều mục còn ở mức thiết kế, chưa implement — xem roadmap ở PRD-AIDE §VIII.

**In đậm = người chịu trách nhiệm cuối cho bước đó.** Bước không in đậm thì agent làm chính, người advisory.

**Bước 0 và 1 không chạy cho từng thay đổi** — chỉ khi mở một hướng đi mới (bước 0, §B.1) hoặc dựng System mới (bước 1, §B.2). Đa số thay đổi bắt đầu thẳng từ bước 2, `derived_from`/PRD đã có để rỗng hoặc giữ nguyên.

**Bước bỏ được theo tier:** T3 bỏ 5, 6, 7, 8, 18, 19 · T2 bỏ 5, có thể gộp 6 vào 7, bỏ 18 nếu Change Set không đổi FR/AC · T1 chạy hết. *(PROC §2.1.3)*

**Bước 8 và 10 tách nhau vì phụ thuộc khác nhau.** Cấp 1–3 chỉ cần FR/AC nên chạy sớm và **qua UI/UX Gate trước bước 9**. Cấp 4 tham chiếu field/endpoint của contract nên chỉ chốt được **sau** bước 9. Gộp hai thứ lại là lý do bản trước không có gate UI: nửa cần L3, nửa không.

**Số thứ tự không phải trình tự bắt buộc — cột Input mới là dependency thật.** Bước 5 (Domain), 6 (L1), và 8 cấp 1–3 (UX Flow, Screen Inventory, UI Design — §E.1) đều chỉ cần `FR, AC`: ba PIC khác nhau (Domain Owner · Architect · Design + Tech Lead) chạy **song song** ngay sau Scope Gate, không ai chờ ai. Bước 7 (L2) mới thật sự chờ bước 6 vì Input có `L1`; bước 9 (L3) chờ bước 7 vì Input có `L2`. Riêng **UI Specification** (bước **10** — field/endpoint máy đọc được, ví dụ §E.2 tham chiếu `API-PAY-v3#terms`) cần thêm L3 nên chỉ chốt được **sau** bước 9, trước khi Contract Gate đóng (§E.4) — ba cấp đầu không chờ L3, cấp cuối thì có.
 