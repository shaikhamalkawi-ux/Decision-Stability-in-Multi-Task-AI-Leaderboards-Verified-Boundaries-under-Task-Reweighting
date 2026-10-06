# Decision diagnosis for incomplete machine-learning leaderboards

Publication-facing reproducibility materials for the Knowledge-Based Systems submission candidate:

**A Decision-Diagnostic Framework for Incomplete Machine Learning Leaderboards: Evidence Ambiguity versus Certificate Failure under Task Reweighting**

**Repository author/maintainer:** Ghassan Malkawi

## Diagnostic framework

The paper distinguishes four logically different outcomes for partial benchmark evidence:

1. **Information-limited** — verified compatible completions yield opposite decisions.
2. **Certificate-limited** — the decision is proved fixed **and nonexistence of a valid certificate in the declared family is proved**.
3. **Certified/resolved** — the declared certificate establishes the fixed decision.
4. **Inconclusive** — ambiguity, semantic determination, or certificate existence remains undecided.

A failed witness search is never treated as evidence that compatible completions agree, and a failed/incomplete certificate search is never treated as proof that no certificate exists.

## Locked reported results

- exact 4-task nonuniform obstruction;
- exact 68-task uniform-center obstruction;
- 65,780 canonical states;
- 789,360 exact ordered support comparisons;
- TabArena: 51 tasks, 14 methods, 816 paired fold vectors;
- 80 fixed overlapping disclosure traces;
- 480 sampled checkpoints;
- zero sampled disclosure savings for the tested strengthening;
- 47/80 information-limited immediate pre-stopping prefixes;
- exact fixed-trace decision point q*=Q on those same 47 traces, from the Q-1 ambiguity witness plus the checked Q certificate;
- Q range among the 47 exact decision points: 726–816 disclosures;
- 39/40 at epsilon = 2/51;
- 8/40 at epsilon = 4/51;
- 33 traces remain inconclusive;
- 1,120 candidate-completion trials;
- 14,560 candidate support comparisons;
- 364 archived-completion comparisons.

## Reviewer-auditable theory materials

- `proofs/PUBLIC_EXACT_PROOF.md` — explicit four-task and uniform-68 derivations.
- `code/replay_exact_obstructions.py` — self-contained exact-rational replay.
- `verification/REPLAY_SUMMARY.json` — expected replay output.

These theory files use only synthetic data and Python standard-library exact arithmetic.

## Fixed-trace decision-point audit

For each of the 47 traces with a verified opposite-answer pair at Q-1, the accepted Phase-2/Phase-6 stopping certificate at Q establishes the same fixed decision over every compatible completion. The two evidence items are identity-matched across the frozen ledgers with 0 mismatches, so the first logically resolvable prefix along each of those fixed disclosure orders is exactly q*=Q. This is a fixed-order result, not an optimization over alternative disclosure orders.

## Empirical-data boundary

The trace counts are descriptive and are not population estimates. Logical completions are defined by the declared numerical domains and are not claimed to be realizable by retraining the named methods. The zero-savings result applies only to the tested certificate strengthening and sampled checkpoints.

Third-party TabArena raw benchmark artifacts are not redistributed where rights are unclear. The repository records the admitted task/method scope and source-identification information needed for source-faithful reconstruction.

## Final figure-generation entry points

- `code/reproduce_graphical_abstract_v11r4.py` — current graphical abstract.
- `code/reproduce_supplementary_figure_s1_v11r2.py` — Supplementary Figure S1.
- `code/verify_fixed_trace_qstar.py` — fixed-trace decision-point verifier.
- Earlier figure scripts are retained only as development lineage.

The final graphical abstract is generated programmatically with matplotlib; it is not produced by a general-purpose generative-image model.
