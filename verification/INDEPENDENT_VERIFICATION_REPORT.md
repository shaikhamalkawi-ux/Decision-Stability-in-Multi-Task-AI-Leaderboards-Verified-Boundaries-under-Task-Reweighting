# Independent verification report

Status: **PASS** for the locked v0.8/R2B scientific record.

## Scope and independence

The audit implementation in `independent_verify.py` does not import the release analysis modules. It reconstructs the three primary admitted matrices from archived source artifacts, applies the declared score directions, source gates, complete-case rules, and no-imputation rule, and then recomputes the decision boundaries. Pairwise and Top-k boundaries use ordered mass transfer; TabArena global feasible-winner entry uses a separately written `scipy.optimize.linprog` formulation.

This is an independent code path, not a different solver family or a formal-arithmetic proof. The original and independent paths share the same archived evidence state and mathematical specification.

## Results

- Raw-to-derived reconstruction: PASS for TabArena (51 x 14), BenchPress (11 x 10), and BeyondArena (122 x 11).
- Largest normalized-matrix difference: `1.1102230246251565e-16` for TabArena, `5.551115123125783e-17` for BenchPress, and `0` for the BeyondArena rank matrix (`1.7763568394002505e-15` for its pre-rank loss matrix).
- Primary locked cases: 3/3 PASS.
- Winner-versus-competitor cases: 109/109 PASS, comprising 101 finite boundaries and 8 infeasible cases.
- TabArena global-entry cases: 14/14 PASS, comprising 13 finite entries and one dominance-certified infeasible case.
- Maximum pairwise-radius difference: `2.9976021664879227e-15`.
- Maximum finite global-entry difference: `3.3306690738754696e-16`.
- Locked results changed: no.

The machine-readable evidence is in `MATRIX_RECONSTRUCTION_AUDIT.csv`, `PRIMARY_RECOMPUTATION.csv`, `PAIRWISE_RECOMPUTATION.csv`, `GLOBAL_RECOMPUTATION.csv`, and `INDEPENDENT_VERIFICATION_RESULTS.json`.

## Environment

The recorded successful run used Python 3.12.14, NumPy 2.3.5, pandas 3.0.1, SciPy 1.18.1, and Windows 11. The audit tolerance was `5e-8`; the downstream equality/tie tolerance was `1e-12`.

## MATLAB cross-check

The MATLAB implementation was prepared, but MATLAB R2024a could not start because license checkout failed with License Manager Error -10 (expired license). The Python verification therefore stands as the executed independent check. `MATLAB_CROSSCHECK.csv` and `PYTHON_MATLAB_DIFFERENCE_AUDIT.csv` record this as `NOT_RUN_LICENSE_EXPIRED`, not as a pass.

## R3 temporal extension

The internal R3 temporal material is excluded from the manuscript and locked results. Its frozen-lock check failed because its reconstructed TabArena radii do not match the byte-pinned v0.8/R2B evidence state. See `TABARENA_HISTORICAL_ARTIFACT_SEARCH.md`.
