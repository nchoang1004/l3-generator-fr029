# FR-029 - provenance, independence and acceptance readiness

Date: 2026-10-07. Reviewer session: quality_independence. Encoding of the initial unsent draft corrected before release.

**Verdict:** useful regression assets within their declared scopes; insufficient evidence to treat the combined assets as FR-029/NFR-ACC-002 acceptance gold. Approval of an artifact is not proof of semantic completeness.

## Scope

Read source/spec/gold/metadata/approval and scoring scripts only. Did not read prior audits, HANDOFF, mentor reports, product model output, reviewer/judge/adjudication content or product prompts. No model/network calls or third-party application imports. Source/spec/gold unchanged. Checks used Python stdlib hashes and read-only Git commands.

Normative references: local FR-L3GEN-029 revision 3, NFR-L3GEN-ACC-002 revision 4, OBS-L3GEN-001 revision 9. OBS requires blind gold before product output, Khiem approval, one run per locked configuration and totals-only access to held-out cases. Thresholds apply separately per kind and per small/medium held-out repository. Zero denominator is not evaluated.

## Dataset verdicts

| Dataset | Direct evidence | Appropriate use |
|---|---|---|
| Six fixtures plus e2e | Fixture README lines 65-68 documents oracle + source construction and explicitly says no second reviewer yet. Six gold files record oracle versions; README gives venv/runtime commands. E2e has 2 routes, 3 models, 1 HTTP call; no author/review/approval/source-digest metadata in its gold. | Targeted regression candidate. README independence claim is not an independently verified receipt. Not real-repository acceptance. |
| Nineteen development route cases | Mapping selects 19 development cases in three families. Manifest says candidate, human_review_complete=false, product_benchmark=not_run; all 19 gold review fields say candidate/adjudication pending. | Selected-route regression, not approved acceptance. |
| Four full-repository gold files | All four final SHA-256 values match APPROVAL-golden-v1-2026-10-04. Approval identifies Khiem, exact approval wording, request source and judge filenames. All four source HEADs match gold/OBS pins; tracked files clean. | Approved exact artifact bytes, but FR-029 scorer uses only a subset: routes, model names on matched routes, HTTP source locations. Not full FR-029 coverage. |
| Three new acceptance gold files | tdd-docker, AgentGPT and Kibo record repository/commit/root/oracle versions. All three source HEADs match OBS and gold; tracked files clean. | Candidate reference. Blind-author, frozen-revision and human approval receipts were not established within the searched locations below. |

## Findings

### I-01: runner's independence claim conflicts with current gold metadata

slice/tools/fr029_golden_routes.py:1 describes independent gold with two reviewers plus adjudication. Seven older cases (six orders cases plus dispatch) explicitly record that the revision-3 author had seen l3gen output on 2026-09-28; revision 3 is not blind. Example: D:/VSF/VSF-L3 Generator/evaluation/golden/v1/cases/orders-base/gold.json:335-341.

Six FastAPI-docs cases say they used the upstream project's OpenAPI snapshots and label themselves not blind. Upstream runtime oracle exposure is not automatically product-output exposure; those two claims must be distinguished. Six newer orders cases record that one author wrote the fixture and gold and checked routes/tables with a runtime oracle. All 19 retain candidate/pending review metadata. Existence of old reviewer files does not prove review of the current revision.

Positive result: all 130 files listed in the 19 source manifests match their SHA-256 pins. Third-party snippets identify full commits. This supports reproducibility, not independence or semantic completeness. The route runner does not enforce hashes or annotation status before running.

### I-02: igorbenav held-out role is unresolved

OBS-001 lists igorbenav as mandatory medium held-out. The golden-v1 approval lines 34-36 and fr029_golden4.py:28 instead designate it for prompt tuning. fr029_accept.py:33-35 still defaults to the same source and approved old gold as held-out.

This is a documented role conflict, not proof that a particular person actually opened output. An authoritative decision and exposure provenance are needed before treating it as held-out. Blind rewriting of answers does not by itself undo prior tuning use of the case/source.

### I-03: acceptance cases receive unequal scoring coverage

fr029_accept.py:123-139 scores routes/models/HTTP/file roles/limitations plus exact-route/model/HTTP error for the three new golds. The igorbenav golden-v1 branch scores only route and HTTP existence plus model names on matched routes. It does not produce model TP/FP/FN or exact error for that repository. Other repositories cannot compensate for missing per-repository measurements.

fr029_golden4.py:45-83 compares only the first request/response model, shortening names by dropping their module, and HTTP calls by file:line. It does not measure model fields, parameters, status, HTTP method/target or file roles. fr029_golden_routes.py:24-26 selects only method/path/source_id. Results from these scopes must not be pooled as full FR-029 accuracy.

### I-04: protocol instructions exceed enforcement

Acceptance runner separates per-item score files into private and totals into summary, which is useful. However, run_documents receives a.out / name (line 111), outside private. The script shows no access control over detailed raw artifacts. A private folder is a convention, not evidence of isolation from the prompt tuner.

A single invocation runs each selected repository once and rejects a nonempty output directory. A fresh directory still permits the same configuration again; no cross-run locked-configuration registry is checked. Approval, gold hash and source commit are not validated by these runners. The acceptance script emits counts but never decides threshold pass/fail and returns 0 even when a repository lacks gold or fails. Exit 0 therefore does not mean acceptance passed. This review did not inspect output/run history and does not assert actual protocol violations occurred.

## Verification limits

Approval search covered local .aide/evidence/approvals and D:/VSF/l3-generator-golden-v2/.aide/evidence/approvals, plus direct listing of the three D:/VSF/l3-acceptance-gold directories. Confirmed only the four-repository receipt within that search. This does not establish that no other review or approval exists elsewhere. Any additional receipt must bind the exact current revision/hash. Judge contents were deliberately not opened, so individual reviewer histories were not independently validated.

Seven real-repository HEADs match all prescribed pins and tracked files are clean. Untracked/ignored source inclusion was not certified. Local fixture gold lacks a separate source digest. Three new acceptance golds lack top-level digest/author/revision/approval fields. Kibo records oracle versions but has no adjacent oracle.json, whereas the other two do. Reproduction may be possible using material elsewhere; the inspected package is not self-contained proof of that workflow.

## Conditions for acceptance readiness

1. Keep regression suites and label their scope accurately. Correct provenance descriptions with new evidence rather than replacing prior records.
2. Freeze source/gold/membership/scorer hashes. Bind blind-author/reviewer and Khiem approval receipts to the three new gold revisions. Resolve igorbenav's held-out/tuning conflict through an authoritative protocol decision.
3. Measure the same FR-029 scope on all four required small/medium held-out repositories, including the missing igorbenav model/exact checks. Keep zero denominators not_evaluated.
4. Lock configuration before the first run; record first runs, justified infrastructure retries and failures. Restrict both detailed scores and raw artifacts from prompt tuners. Decide thresholds using raw counts, not rounded rates.
5. Perform independent semantic source review. Matching hashes, runtime oracles and approval alone do not prove complete and statically appropriate route/model/HTTP answers.

No new product performance score was calculated by this review.
