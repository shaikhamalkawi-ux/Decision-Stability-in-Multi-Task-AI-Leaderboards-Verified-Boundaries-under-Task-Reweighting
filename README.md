# Decision Stability in Multi-Task AI Leaderboards

Development repository for the study:

**Decision Stability in Multi-Task AI Leaderboards: Verified Boundaries under Task Reweighting**

## Scientific question

How far must declared task priorities move, with benchmark scores held fixed, before a leaderboard decision changes?

The project distinguishes:
- winner-change boundaries,
- Top-k membership boundaries,
- pairwise challenger access,
- global feasible-winner entry,
- deterministic weight sensitivity from statistical uncertainty.

## Repository status

The manuscript-linked reproducibility release is in [`reproducibility/mlwa-20260926/`](reproducibility/mlwa-20260926/README.md), version `v0.8.1-mlwa-r2.20260926`.

It supports independent recomputation from released derived matrices and archived primal-dual witness checks. Its clean-extraction checks reproduce all nine primary Top-1/Top-3/Top-5 radii, 109 pairwise cases and 14 global cases; witness checks cover 101 finite pairwise records and 14 global records. Scientific inputs and numerical results are unchanged.

Full raw-source reconstruction, every resampling/scope experiment, and witness regeneration are not claimed for this public archive. Third-party raw artifacts, manuscript/author-private files and unrelated development research are excluded. See the release README for exact scope, reproducibility commands and file-specific licensing.

The archive DOI is [10.5281/zenodo.22975098](https://doi.org/10.5281/zenodo.22975098). The older root `verification/` material remains a dated audit record; use the versioned release directory for the current portable execution instructions.

**Important:** scientific results are fail-closed. Do not silently alter data, task/method scope, normalization, tie rules, tolerances, weights, or claims.

See `AGENTS.md` and `docs/CODEX_START_HERE.md` before making changes.
