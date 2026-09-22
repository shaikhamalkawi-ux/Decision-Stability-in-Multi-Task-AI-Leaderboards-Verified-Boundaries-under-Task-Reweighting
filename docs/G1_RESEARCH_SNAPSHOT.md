# G1 research snapshot: shared-completion bounds

Date: 22 September 2026

Status: development research snapshot; not the final MLWA supporting archive

## Scientific result

G1 studies sharp lower and upper endpoints of the task-reweighting distance needed
to remove a candidate's unique-winner status when only incomplete ordinal evidence
is admitted. It distinguishes a joint endpoint, which must use one completion
shared across every competitor, from a pairwise relaxation that may optimize a
different completion for each competitor.

The constructed three-model, three-task example has 125 weak-order completions.
Its pairwise upper relaxation is `2/9`, while its sharp joint endpoint is `1/5`
when new ties are allowed. Excluding introduced ties changes the endpoint to `1/6`.

For the declared coarsened released BeyondArena ordinal evidence:

- TabPFN-2.6 has sharp envelope `[0, 96/1207]`.
- RealMLP has sharp envelope `[0, 55/2414]`.
- RealMLP's pairwise upper relaxation is `69/2698`, an overstatement of about
  12.2488% relative to the sharp joint endpoint.
- The other nine candidates have envelope `[0, 0]` under this completion model.

The brackets report sharp endpoints; they do not assert that every intervening
value is attainable and are not confidence intervals.

## Evidence boundary

The experiment preserves all 122 complete 11-model ranking rows and the relative
nine-model orders on 20 additional rows. The positions of TabDPT and TabPFN-2.6
on those 20 rows are unspecified in this selected evidence representation. These
40 unspecified positions are not asserted to be the original raw missing cells.
No missing score, failure meaning, metric constraint, or task result was invented.

Accordingly, the snapshot supports sharp endpoints for the declared coarsened
ordinal model only. Original full-raw missingness validation remains `HOLD`.
R3 is unchanged, manuscript integration was not executed, and a first-in-literature
claim is not established.

## Reproducibility and integrity

The package's internal manifest verifies `66/66` files. A fresh independent run
of `code/reproduce.py` completed successfully on 22 September 2026 and reported:

> PASS: exact endpoint certificates, compatible witnesses, and independent
> numerical checks.

The frozen downloadable package is:

`CERT_Bench_Missingness_G1_ContributionGate_20260922_Package.zip`

SHA-256:

`8bf1057a3793e99d12281ba722f3adecb456fffcb2dde4d1a958122c5df05c4c`

The expanded, manifest-covered files are stored under
`research/g1_shared_completion_bounds_20260922/`. The repository-level citation,
license scope, and release notes are intentionally outside the frozen 66-file
manifest and do not modify its scientific contents.

## Reproduce

From `research/g1_shared_completion_bounds_20260922/`:

```bash
python -m pip install -r requirements.txt
python code/verify_manifest.py
python code/reproduce.py
```

The recorded environment used Python 3.13.5, NumPy 2.3.5, pandas 2.2.3, and
SciPy 1.17.0. Generated files can differ byte-for-byte across environments even
when the exact mathematical results pass; the frozen package is the checksum
authority.

## Release meaning

The corresponding Git tag and Zenodo record, if published, identify this G1
research snapshot only. They must not be cited as the final manuscript-linked
reproducibility release until manuscript integration and an independent audit are
complete.
