# Codex ↔ Google Drive Working Bridge

Authoritative private working materials for the current pre-submission cycle are stored in the user's Google Drive folder:

`CERT_Bench_Codex_Workspace_20260920`

## Codex workflow

1. Read the private Drive files:
   - `00_START_HERE/00_START_HERE_CERT_BENCH_CODEX.md`
   - `00_START_HERE/CODEX_MASTER_TASK.md`
   - `CERT_Bench_Codex_Transfer_20260920.zip`
2. Treat **R2B — Finding-First Pre-Submission Closure** as the active scientific baseline.
3. Read this repository's `AGENTS.md` and `docs/CODEX_START_HERE.md`.
4. Work on a dedicated branch, preferably:
   `codex/pre-submission-audit-20260920`
5. Do not push author-private metadata, submission credentials, private correspondence, or identifying review material to GitHub while repository visibility is public.
6. Public-safe code, tests, documentation, and reproducibility improvements may be committed on the Codex branch.
7. Return the complete revised manuscript/package to the Drive subfolder:
   `03_RETURN_FROM_CODEX`
8. Open a PR summarizing:
   - scientific/editorial changes;
   - verification results;
   - whether any locked result changed;
   - any HOLD/FAIL blocker.

## Scientific fail-closed rule

Do not silently change the locked datasets, method/task scope, normalization, task weights, tie semantics, tolerances, or numerical results.

If a result-determining mismatch is found, stop and document it before propagating any manuscript change.
