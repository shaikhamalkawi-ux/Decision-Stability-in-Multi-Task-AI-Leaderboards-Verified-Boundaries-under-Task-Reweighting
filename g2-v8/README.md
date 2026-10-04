# Diagnosing Unresolved ML Leaderboards — G2 V8 Reproducibility Materials

Publication-facing reproducibility materials for:

**Diagnosing Unresolved ML Leaderboards: Evidence Ambiguity versus Certificate Failure under Task Reweighting**

**Repository author/maintainer:** Ghassan Malkawi

## Scientific scope

This material supports the paper's distinction between:

- **certificate-limited states**: all compatible completions give the same decision, while the restricted completion-independent certificate can still fail; and
- **information-limited states**: the same disclosed benchmark evidence admits compatible completions with opposite decisions.

## Locked reported results

- exact 4-task nonuniform obstruction;
- exact 68-task uniform-center obstruction;
- 65,780 canonical states;
- 789,360 exact ordered support comparisons;
- TabArena audit: 51 tasks, 14 methods, 816 paired fold vectors;
- 80 fixed disclosure traces;
- 480 sampled checkpoints;
- zero sampled disclosure savings for the tested strengthening;
- 47/80 opposite-answer completion witnesses;
- 39/40 witnesses at epsilon = 2/51;
- 8/40 witnesses at epsilon = 4/51;
- 33 traces remain inconclusive;
- 1,120 candidate-completion trials;
- 14,560 candidate support comparisons;
- 364 comparisons against the archived completion.

## Contents

- `CITATION.cff` — repository citation metadata.
- `results/primary_summary.csv` — locked publication-facing result summary.
- `verification/verification_summary.csv` — locked verification counts.
- `verification/README.md` — scope and claim boundaries.
- `data/README.md` — upstream-data and redistribution note.

## Important boundaries

The 80 traces overlap within one benchmark archive and are not independent datasets. Percentages are descriptive, not population estimates.

The 33 traces without a found opposite-answer witness are **inconclusive**; they are not evidence that all compatible completions agree.

The zero-savings result is limited to the tested certificate strengthening and sampled checkpoints. It is not a universal claim that stronger certificates cannot reduce evaluation cost.

The historical unverified BeyondArena candidate result of approximately 12.25% is excluded from this G2 study.

Third-party TabArena raw benchmark artifacts are not redistributed here where redistribution status is unclear. Use the upstream TabArena source and the paper's declared task/method/disclosure specification.

## Public link

https://github.com/shaikhamalkawi-ux/Decision-Stability-in-Multi-Task-AI-Leaderboards-Verified-Boundaries-under-Task-Reweighting/tree/main/g2-v8
