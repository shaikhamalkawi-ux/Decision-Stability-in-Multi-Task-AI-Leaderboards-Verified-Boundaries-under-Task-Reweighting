# Beyond Rank: Decision-Stability Radii for Multi-Task AI Leaderboards under Task Reweighting

Public project repository for the CERT-Bench study.

**Author:** Ghassan Malkawi  
**Affiliation:** Faculty of Computer Information Science, Higher Colleges of Technology, Al Ain, Abu Dhabi, United Arab Emirates  
**Current journal target:** Journal of Applied Research and Technology (JART)

## Scientific question

How much task-weight mass must be redistributed before a stated multi-task leaderboard decision changes, while the observed score matrix is held fixed?

The study distinguishes:

- unique-winner loss;
- possible top-k entry;
- pairwise contact with the nominal winner;
- all-competitor feasible-winner entry;
- deterministic task-weight sensitivity from statistical uncertainty.

## Verified primary evidence states

| Benchmark | Matrix | Nominal winner | Nearest top-1 challenger | Top-1 DSR |
|---|---:|---|---|---:|
| TabArena | 51 × 14 | RealMLP | LightGBM | 0.0366013072 |
| BenchPress | 11 × 10 | Claude Opus 4.6 | GPT-5.2 | 0.0909090909 |
| BeyondArena | 122 × 11 | TabPFN-2.6 | TabICLv2 | 0.0186703097 |

A central TabArena example is RandomForest: pairwise access to RealMLP occurs at DSR 0.29758, while global feasible-winner entry requires DSR 0.50561.

## Repository contents

- `manuscript/main.tex` — current single-author manuscript source.
- `manuscript/figure1_dsr_concept.tex`, `figure2_pairwise_vs_global.tex`, `figure3_beyondarena_regimes.tex` — publication figure sources.
- `supplement/supplement.tex` — current supplementary source.
- `data/evidence_states.csv` — declared benchmark scopes used in the paper.
- `results/primary_results.csv` — primary reported DSR values.
- `verification/verification_summary.csv` — numerical-verification counts reported in the paper.
- `CITATION.cff` — citation metadata.

Third-party raw benchmark artifacts are not redistributed when their redistribution status is unclear. The repository records derived evidence states and reported results only; it should not be interpreted as redistributing the upstream benchmark datasets.

## Numerical verification reported in the manuscript

- 109 winner-versus-competitor cases across the reported scopes;
- 101 finite pairwise witnesses passing independent checks;
- 14 TabArena global feasible-winner cases passing all-competitor checks;
- 6,402 finite random validation problems for the independent mass-transfer comparison;
- maximum absolute LP–transfer discrepancy: 1.14 × 10^-13.

## Status

This repository is public and synchronized with the current JART submission candidate. Scientific results are fixed to the evidence states declared in the manuscript; updates to documentation or packaging must not silently change the reported numerical results.

## Contact

Ghassan Malkawi — gmalkawi@hct.ac.ae
