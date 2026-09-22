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

This repository is being prepared for a reproducible, independently verifiable research workflow.

The separate **G1 research snapshot (22 September 2026)** is available under
[`research/g1_shared_completion_bounds_20260922/`](research/g1_shared_completion_bounds_20260922/).
It contains proofs, code, declared inputs, endpoint witnesses, exact certificates,
and validation outputs for shared-completion bounds under incomplete rank evidence.
The snapshot is a contribution investigation: it does not replace the active R3
manuscript, is not the final MLWA supporting archive, and does not claim to
reconstruct the original raw missing-score pattern.

See [`docs/G1_RESEARCH_SNAPSHOT.md`](docs/G1_RESEARCH_SNAPSHOT.md) for the exact
claim boundary, reproducibility result, integrity hash, and release status.

**Important:** scientific results are fail-closed. Do not silently alter data, task/method scope, normalization, tie rules, tolerances, weights, or claims.

See `AGENTS.md` and `docs/CODEX_START_HERE.md` before making changes.

## Licensing

Author-created source code is licensed under Apache-2.0. Author-created narrative
and documentation are licensed under CC-BY-4.0. Derived inputs and third-party
references retain their upstream rights and are not relicensed. See
[`LICENSE_SCOPE.md`](LICENSE_SCOPE.md) for the controlling scope statement.
