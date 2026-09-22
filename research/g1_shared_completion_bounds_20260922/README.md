# Shared-completion bounds for incomplete-benchmark stability

**G1 contribution investigation — 22 September 2026. Not a replacement manuscript.**

The CERT-Bench R3 manuscript and its frozen results are unchanged. This package
contains a separate mathematical contribution test, exact endpoint witnesses,
an independently checked upper-bound obstruction, source/evidence contracts,
and reproducible computation.

## Result

A sharp pairwise upper bound cannot generally be combined across rivals into a
sharp winner-stability upper bound: the best completions can be incompatible.

- Exact constructed example, allowing ties: true upper radius `1/5`, independently
  optimized pairwise relaxation `2/9`. All 125 weak-order completions are enumerated.
- On the declared **coarsened released BeyondArena ordinal evidence**, RealMLP's
  sharp upper radius is `55/2414`, versus the pairwise relaxation `69/2698`.
  The relaxation overstates the attainable upper endpoint by `128/1045`, or
  about **12.2488% relative to the sharp endpoint**.
- TabPFN-2.6's sharp envelope on the same evidence is `[0,96/1207]`.
- RealMLP's sharp envelope is `[0,55/2414]`. The other nine models have `[0,0]`.
  This identifies possible **unique** nominal winners, not all possible co-winners.

The brackets summarize sharp endpoints. They do not assert that every value
between the endpoints is attainable. They are not statistical confidence intervals.

## Critical evidence boundary

The inputs preserve all 122 complete 11-model ranking rows and the relative
nine-model orders on 20 additional rows. Positions of TabDPT and TabPFN-2.6 on
those 20 rows are unspecified **in this selected evidence representation**.
The resulting 40 unspecified positions are **not claimed to be the original raw
missing-cell pattern**. Exact raw artifact identities are recorded in the inherited
manifest, but those raw files were not recovered in this investigation. Failures,
unsupported tasks, metric bounds, and additional available raw scores were not
admitted or silently invented. The endpoint completions are mathematical witnesses,
not measurements or imputed estimates.

## Reproduce

Python 3.13.5, NumPy 2.3.5, pandas 2.2.3, SciPy 1.17.0 were used.

```bash
python -m pip install -r requirements.txt
python code/reproduce.py
```

This regenerates row-pattern sets, lower and relaxed upper bounds, an exact
integer-dynamic-programming upper obstruction, independent tests, and final sharp
endpoint summaries. It checks the stored RealMLP endpoint witness rather than
requiring the optimizer to rediscover the same witness. To also rerun its
mixed-integer optimization, use:

```bash
python code/reproduce.py --rediscover
```

Alternative optimal witnesses can exist. Scientific values and exact obstruction
certificates, not the identity of a solver-selected completion, determine success.

## Read first

`proofs/Contribution_Note.pdf`: complete mathematical argument and results.
`results/FINAL_RESULT_SUMMARY.json`: machine-readable final claims and limits.
`qa/VALIDATION_REPORT.json`: independent numerical/enumeration checks.
`sources/NOVELTY_AND_EVIDENCE_REGISTER.md`: prior work and admission boundaries.
`NEXT_GATE.md`: bounded next step; no new data collection merely for breadth.

## Claim status

Mathematical/computational G1: **PASS for the declared completion model**.
Original full-raw missingness experiment: **HOLD / not executed**.
First-in-literature novelty: **not established**. Closest foundations are credited.
Manuscript integration: **not executed**. R3 remains the active manuscript.

The packaged derived inputs originate from the author-supplied R3 supplement.
Third-party raw artifacts, login information, author biographies, and unrelated
project files are excluded. No publication license or repository deposit is implied.
