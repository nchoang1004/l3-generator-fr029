# CMP-008 — independent renderer evaluation

Cases: 82. Pass: 66; fail: 13; evaluator/runtime error: 3.

**This is a synthetic contract regression result, not a percentage of product quality or acceptance.**
No real-repository precision/recall, LLM quality, component quality or Scope Gate approval is inferred.

| Case | Result | Requirement | Findings |
|---|---|---|---|
| [bundle-complete](bundle-complete/checks.json) | pass | AC-L3GEN-025-01/02/04; API-008 §3/4 | — |
| [bundle-repeat](bundle-repeat/checks.json) | pass | AC-L3GEN-025-01/02/04; API-008 §3/4 | — |
| [bundle-no-upstream](bundle-no-upstream/checks.json) | pass | AC-L3GEN-025-01/02/04; API-008 §3/4 | — |
| [api-method-get](api-method-get/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-method-post](api-method-post/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-method-put](api-method-put/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-method-delete](api-method-delete/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-method-patch](api-method-patch/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-method-head](api-method-head/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-method-options](api-method-options/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-method-trace](api-method-trace/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-unknown-path](api-unknown-path/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-unknown-status_codes](api-unknown-status_codes/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-unknown-method](api-unknown-method/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-unknown-application_id](api-unknown-application_id/checks.json) | fail | AC-L3GEN-027-01; API-008 §5 | expected-operation-count, operation-identity-known |
| [api-unknown-registration_context](api-unknown-registration_context/checks.json) | fail | AC-L3GEN-027-01; API-008 §5 | expected-operation-count, operation-identity-known |
| [api-prefix-unknown](api-prefix-unknown/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-app-collision](api-app-collision/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-two-mounts](api-two-mounts/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-missing-path-parameter](api-missing-path-parameter/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-parameters](api-parameters/checks.json) | error | AC-L3GEN-027-01; API-008 §5 | 'schema' |
| [api-body](api-body/checks.json) | fail | AC-L3GEN-027-01; API-008 §5 | body-required-not-invented |
| [api-response-model](api-response-model/checks.json) | pass | AC-L3GEN-027-01; API-008 §5 | — |
| [api-nested-union](api-nested-union/checks.json) | fail | AC-L3GEN-027-01; API-008 §5 | nested-model-resolved |
| [table-unknown-dialect](table-unknown-dialect/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-unknown-name](table-unknown-name/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-unknown-columns](table-unknown-columns/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-column-unknown-type](table-column-unknown-type/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-column-unknown-nullable](table-column-unknown-nullable/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-column-unknown-primary_key](table-column-unknown-primary_key/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-column-unknown-foreign_key](table-column-unknown-foreign_key/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-column-unknown-name](table-column-unknown-name/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-type-32](table-type-32/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-type-33](table-type-33/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-type-34](table-type-34/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-type-35](table-type-35/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-invalid-type-36](table-invalid-type-36/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-invalid-type-37](table-invalid-type-37/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-invalid-type-38](table-invalid-type-38/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-foreign-key](table-foreign-key/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-fk-control](table-fk-control/checks.json) | fail | AC-L3GEN-027-02; API-008 §6.1 | ddl-foreign-key, expected-ddl-count |
| [table-quoted-identifiers](table-quoted-identifiers/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-compound-pk](table-compound-pk/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [table-nullable-pk](table-nullable-pk/checks.json) | pass | AC-L3GEN-027-02; API-008 §6.1 | — |
| [event-publish](event-publish/checks.json) | pass | AC-L3GEN-027-03; API-008 §6.2 | — |
| [event-consume](event-consume/checks.json) | pass | AC-L3GEN-027-03; API-008 §6.2 | — |
| [event-payload-unknown](event-payload-unknown/checks.json) | pass | AC-L3GEN-027-03; API-008 §6.2 | — |
| [event-unknown-broker](event-unknown-broker/checks.json) | pass | AC-L3GEN-027-03; API-008 §6.2 | — |
| [event-unknown-namespace](event-unknown-namespace/checks.json) | pass | AC-L3GEN-027-03; API-008 §6.2 | — |
| [event-unknown-serialization_context](event-unknown-serialization_context/checks.json) | pass | AC-L3GEN-027-03; API-008 §6.2 | — |
| [event-unknown-topic](event-unknown-topic/checks.json) | pass | AC-L3GEN-027-03; API-008 §6.2 | — |
| [event-different-brokers](event-different-brokers/checks.json) | pass | AC-L3GEN-027-03; API-008 §6.2 | — |
| [event-same-binding](event-same-binding/checks.json) | pass | AC-L3GEN-027-03; API-008 §6.2 | — |
| [event-two-owners](event-two-owners/checks.json) | pass | AC-L3GEN-027-03; API-008 §6.2 | — |
| [graph-nodes-0](graph-nodes-0/checks.json) | pass | AC-L3GEN-025-02/04; API-008 §3 | — |
| [graph-nodes-1](graph-nodes-1/checks.json) | pass | AC-L3GEN-025-02/04; API-008 §3 | — |
| [graph-nodes-50](graph-nodes-50/checks.json) | pass | AC-L3GEN-025-02/04; API-008 §3 | — |
| [graph-nodes-51](graph-nodes-51/checks.json) | pass | AC-L3GEN-025-02; API-008 §3/7 | — |
| [graph-parallel-types](graph-parallel-types/checks.json) | error | AC-L3GEN-025-02/04; API-008 §3 | Fixture violates input schema |
| [graph-directed](graph-directed/checks.json) | pass | AC-L3GEN-025-02/04; API-008 §3 | — |
| [bundle-owner-unknown](bundle-owner-unknown/checks.json) | pass | AC-L3GEN-025-01/02/04; API-008 §3/4 | — |
| [names-61](names-61/checks.json) | pass | SEC-002; API-008 §4/7 | — |
| [names-62](names-62/checks.json) | pass | SEC-002; API-008 §4/7 | — |
| [names-63](names-63/checks.json) | pass | SEC-002; API-008 §4/7 | — |
| [names-64](names-64/checks.json) | error | SEC-002; API-008 §4/7 | [Errno 2] No such file or directory: 'D:\\VSF\\l3-generator-l3\\ket-qua-chay\\l3-evaluation-development-01\\names-64\\.output.l3slice-rpypskb9\\tech-specs\\AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\\api\\API-REVIEW-SHOP-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA-v1.md' |
| [input-missing-schema](input-missing-schema/checks.json) | fail | AC-L3GEN-025-02; API-008 §3/7 | no-publish-invalid-input, typed-rejection |
| [input-wrong-schema](input-wrong-schema/checks.json) | fail | AC-L3GEN-025-02; API-008 §3/7 | no-publish-invalid-input, typed-rejection |
| [input-cross-snapshot](input-cross-snapshot/checks.json) | fail | AC-L3GEN-025-02; API-008 §3/7 | no-publish-invalid-input, typed-rejection |
| [input-dangling-edge](input-dangling-edge/checks.json) | fail | AC-L3GEN-025-02; API-008 §3/7 | typed-rejection |
| [input-rejected-component](input-rejected-component/checks.json) | fail | AC-L3GEN-025-02; API-008 §3/7 | no-publish-invalid-input, typed-rejection |
| [input-duplicate-fact](input-duplicate-fact/checks.json) | fail | AC-L3GEN-025-02; API-008 §3/7 | no-publish-invalid-input, typed-rejection |
| [input-missing-evidence](input-missing-evidence/checks.json) | fail | AC-L3GEN-025-02; API-008 §3/7 | no-publish-invalid-input, typed-rejection |
| [input-dangling-owner](input-dangling-owner/checks.json) | pass | AC-L3GEN-025-02; API-008 §3/7 | — |
| [publish-nonempty](publish-nonempty/checks.json) | pass | AC-L3GEN-025-03; API-008 §7 | — |
| [publish-svg-failure](publish-svg-failure/checks.json) | pass | AC-L3GEN-025-03; API-008 §7 | — |
| [publish-retry](publish-retry/checks.json) | pass | AC-L3GEN-025-03; API-008 §7 | — |
| [publish-retry-ready](publish-retry-ready/checks.json) | pass | AC-L3GEN-025-03; API-008 §7 | — |
| [publish-retry-version](publish-retry-version/checks.json) | pass | AC-L3GEN-025-03; API-008 §7 | — |
| [publish-retry-tamper](publish-retry-tamper/checks.json) | pass | AC-L3GEN-025-03; API-008 §7 | — |
| [publish-retry-crash](publish-retry-crash/checks.json) | pass | AC-L3GEN-025-03; API-008 §7 | — |
| [publish-retry-nonretryable](publish-retry-nonretryable/checks.json) | pass | AC-L3GEN-025-03; API-008 §7 | — |
| [publish-publish-failure](publish-publish-failure/checks.json) | fail | AC-L3GEN-025-03; API-008 §7 | typed-rejection |

## Not measured / outside this boundary

- **manual-diagram-readability** (not_run): Human review at 1/10/50 nodes, long labels, arrow visibility and overlapping edges is still required; XML parity is not visual quality.
- **real-verified-result-integration** (not_run): Synthetic CMP-008 boundary only; no independent real-repository accepted input corpus in this suite.
- **web-download-expiry-concurrency** (out_of_scope): CMP-001 facade: expiry, download authorization and concurrent writers require separate integration tests.
- **source-truth-LLM-component-quality** (out_of_scope): Extractor accuracy, LLM reasoning and D-03 partition quality are not renderer metrics.
- **external-user-and-NFR-benchmark** (not_run): No pilot, OS matrix, large-file performance or acceptance sampling claim; elapsed seconds are diagnostic only.
- **full-crash-matrix** (not_run): Tests staging write failure and crash after artifact install; not every OS rename/disk-full/process-kill boundary.

## Reproduce

See `provenance.json` for actual source/contract hashes and installed versions. Each case has `input.json`, `case.json`, `checks.json`, and output bytes if published.
Inputs are hand-authored synthetic accepted facts. Their evidence metadata does not claim a real source-ground-truth judgment.
Exit 0 = selected automated cases passed; exit 1 = product assertions failed; exit 2 = at least one evaluator/runtime error. Manual and acceptance gaps remain even with exit 0.
