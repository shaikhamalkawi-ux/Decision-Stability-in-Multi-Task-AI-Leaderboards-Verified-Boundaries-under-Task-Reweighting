# Release notes: v0.8.1-mlwa-r2.20260926

26 September 2026

Title: CERT-Bench: reproducibility software and derived data for Decision Stability in Multi-Task AI Leaderboards.

This release packages the current manuscript-linked derived inputs and reference results with independent numerical verification and archived primal-dual witness verification. No locked numerical result, dataset/method scope, weight, score transformation, tie rule or scientific claim is changed by this packaging step.

The 22 processed matrix/weight CSVs, four result CSVs and two independent verification modules are copied byte-for-byte from the reviewed supplement. The 12 witness JSONL files and two standalone checkers are copied byte-for-byte from the existing archived witness-closure evidence. Their matrices and weights were checked against the current inputs before inclusion. New files provide public-facing instructions, environment requirements, manifest verification and an orchestration wrapper; the wrapper does not replace any numerical algorithm.

Executed check results are recorded in `qa/PUBLIC_CHECK_SUMMARY.json` and the underlying CSV/JSON reports. Expected counts are 3 primary cases, 109 pairwise recomputations, 14 global recomputations, 101 finite pairwise witness checks, 14 global witness checks and three unit tests (including 120 randomized LP comparisons). Consult the actual status rather than treating this description as a substitute for executing the tests.

The public archive intentionally excludes manuscript source/PDFs, personal contact information, private submission administration, raw third-party artifacts, unrelated development research and old private QA logs. Scope is derived-matrix recomputation and archived-witness checking; full raw reconstruction, every resampling/admission-sensitivity experiment and witness regeneration are not claimed. See README.md and the third-party retrieval manifest for remaining limits.

Public release does not constitute submission of the manuscript to a journal.
