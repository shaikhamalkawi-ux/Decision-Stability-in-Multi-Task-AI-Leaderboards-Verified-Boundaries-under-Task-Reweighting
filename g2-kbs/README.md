# Decision diagnosis for incomplete machine-learning leaderboards

Publication-facing reproducibility materials for the Knowledge-Based Systems submission candidate:

**A Decision-Diagnostic Framework for Incomplete Machine Learning Leaderboards: Evidence Ambiguity versus Certificate Failure under Task Reweighting**

**Repository author/maintainer:** Ghassan Malkawi

## Diagnostic framework

The paper distinguishes four logically different outcomes for partial benchmark evidence:

1. **Information-limited** — verified compatible completions yield opposite decisions.
2. **Certificate-limited** — the decision is proved fixed, but the declared certificate fails.
3. **Certified/resolved** — the declared certificate establishes the fixed decision.
4. **Inconclusive** — neither information limitation nor semantic determination is proved.

This separation is sound by construction: a failed witness search is never treated as evidence that compatible completions agree.

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
- 39/40 at epsilon = 2/51;
- 8/40 at epsilon = 4/51;
- 33 traces remain inconclusive;
- 1,120 candidate-completion trials;
- 14,560 candidate support comparisons;
- 364 archived-completion comparisons.

## Boundaries

The trace counts are descriptive and are not population estimates. Logical completions are defined by the declared numerical domains and are not claimed to be realizable by retraining the named methods. The zero-savings result applies only to the tested certificate strengthening and sampled checkpoints.


## Final figure-generation entry points

For the KBS pre-submission package, use these scripts:

- `code/reproduce_graphical_abstract_v11r2.py` — final graphical abstract.
- `code/reproduce_supplementary_figure_s1_v11r2.py` — Supplementary Figure S1.
- `code/reproduce_all_figures_v11.py` and earlier figure scripts are retained as development lineage and are not the final submission entry points.

The final graphical abstract is generated programmatically with matplotlib; it is not produced by a general-purpose generative-image model.
