# CMP-008 — independent renderer evaluation

Cases: 1. Pass: 1; fail: 0; evaluator/runtime error: 0.

**This is a synthetic contract regression result, not a percentage of product quality or acceptance.**
No real-repository precision/recall, LLM quality, component quality or Scope Gate approval is inferred.

| Case | Result | Requirement | Findings |
|---|---|---|---|
| [names-64](names-64/checks.json) | pass | SEC-002; API-008 §4/7 | — |

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
