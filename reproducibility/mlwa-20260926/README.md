# CERT-Bench: reproducibility software and derived data for Decision Stability in Multi-Task AI Leaderboards

Version: `v0.8.1-mlwa-r2.20260926`  
Release date: 26 September 2026

Archive DOI: <https://doi.org/10.5281/zenodo.22975098>.

Development repository: <https://github.com/shaikhamalkawi-ux/Decision-Stability-in-Multi-Task-AI-Leaderboards-Verified-Boundaries-under-Task-Reweighting>.
Use the versioned archive for byte-pinned reproduction; the development repository may contain other branches and historical work.

This archive supports the manuscript *Decision Stability in Multi-Task AI Leaderboards: Verified Boundaries under Task Reweighting*. It contains the unchanged released derived matrices, nominal weights, expected boundary results, primal-dual witnesses and independent checking software for the manuscript's scientific baseline.

## What is independently checkable

- Three primary cases: TabArena (51 tasks, 14 methods), BenchPress (11 tasks, 10 methods) and BeyondArena (122 tasks, 11 methods).
- Eleven released analysis cases in total, each with a normalized matrix and nominal weights.
- 109 winner-versus-competitor pairwise boundaries, including 101 finite cases and eight infeasible cases; top-1 and top-3/top-5 possible-entry boundaries for the three primary cases.
- Fourteen TabArena global feasible-winner entries: 13 finite entries and one strict-dominance infeasibility certificate.
- Standalone primal-dual witness checks for all 101 finite pairwise cases and all 14 global cases. These standard-library checkers neither import the analysis implementation nor solve an optimization problem.
- Three unit tests, including 120 seeded randomized comparisons of ordered mass transfer with an independent SciPy linear-programming formulation.

Matrices are **tasks x methods**, with lower normalized values preferred. Each weight CSV preserves the corresponding matrix's task order. No missing values are imputed. Weights, scopes, score transformations, tie semantics, constants and reference results are preserved from the supplied scientific evidence. The independent boundary-recomputation code uses tie tolerance `1e-12` and comparison tolerance `5e-8`; witness records carry their own verification tolerance. The unchanged standalone checkers permit complementarity residuals up to ten times their record tolerance; the release checks additionally report whether the actual residuals are at most `1e-8`.

## Scope limitations

This is a **derived-matrix recomputation and archived-witness verification release**, not a complete raw-source acquisition/reconstruction pipeline. It does not include third-party raw Parquet bytes, the original result-determining analysis implementation, or every resampling and admission/scope-sensitivity experiment in the manuscript. It validates archived witnesses; it does not regenerate all witnesses from original raw artifacts. The supplied figure plotting script and manuscript source are intentionally outside this archive.

The recorded third-party manifest identifies upstream sources and retained artifact hashes. Exact per-file BeyondArena download URLs were not retained, and its artifact-level redistribution permissions are not inferred from a repository license. See `legal/THIRD_PARTY_RETRIEVAL_MANIFEST.json`. A matrix-only PASS does not establish full raw reconstruction or immutable temporal/upstream validation.

All decision-boundary results are conditional on the admitted matrices, transformations, method/task scope, weights and tie definitions. They are not confidence intervals, preference estimates, safety/compliance guarantees or claims of universal model superiority.

## Quick start

Tested with Python 3.12.14, NumPy 2.3.5, pandas 3.0.1 and SciPy 1.18.1. Create an isolated Python environment, then run from the extracted archive root:

```sh
python -m pip install -r requirements.txt
python -B verify_manifest.py
python -B run_public_checks.py
```

The last command recomputes the matrix-based quantities, runs the independent unit tests and both standalone witness checkers, and writes a concise `qa/PUBLIC_CHECK_SUMMARY.json`. The expected outcome is PASS for 3/3 primary cases, 109/109 pairwise cases, 14/14 global cases, 101/101 finite pairwise witness records, 14/14 global witness records and three unit tests.

Check the manifest **before** running the computations. Re-execution refreshes generated files under `qa/` and `verification/public_recheck/`; these files can differ across environments. It does not edit frozen matrices, weights, expected-result CSVs, witness records or verification implementations. Keep an untouched extraction if byte-identical archived QA is needed.

Individual commands are also available:

```sh
python -B verification/independent_outputs/independent_verify.py --archive-root . --output-dir verification/new_matrix_recheck --matrix-only
python -B -m unittest discover -s verification/independent_outputs -p test_independent_verify.py -v
python -B standalone_verify_witnesses.py --root .
python -B standalone_verify_global_winners.py
```

The two standalone witness commands require only Python's standard library. Do not omit `--matrix-only` from the independent recomputation command: its optional raw reconstruction path requires additional artifacts deliberately not distributed here.

## File map and rights

- `data/processed/`: 22 matrix/weight CSVs for 11 cases.
- `results/`: four preserved expected-result CSVs, used for comparison only.
- `witnesses/`: 11 finite pairwise witness JSONL files and one global witness JSONL file.
- `verification/independent_outputs/`: independent numerical implementation and unit tests.
- `standalone_verify_*.py`: dependency-free archived witness checkers.
- `verification/public_recheck/` and `qa/`: executed public-safe verification results.
- `legal/`: license text, scoped third-party notices and retrieval metadata.
- `SHA256SUMS.txt`: release-file integrity manifest; `verify_manifest.py` checks it.

See `LICENSE_SCOPE.md`. Author-created code is Apache-2.0; the repository's existing documentation policy is CC-BY-4.0. These terms do not relicense third-party benchmark data or remove upstream obligations. No manuscript, personal contact information, private administrative files or unrelated research-snapshot contents are bundled.
