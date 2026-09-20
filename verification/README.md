# Independent Verification

This directory is for independent cross-implementation checks.

The verifier must not import the result-determining optimization implementation it is auditing.

Preferred checks:
- independent Python implementation;
- MATLAB `linprog` cross-check where available;
- primal feasibility;
- objective agreement;
- dual/complementarity checks where applicable;
- manuscript-number audit;
- SHA-256 input/output inventory.

Every audit ends in PASS, FAIL, or HOLD.

## Independent verifier

`independent_verify.py` consumes the byte-pinned v0.8 release archive without
importing its result-determining optimization modules. It:

- reconstructs the TabArena, BenchPress, and BeyondArena primary matrices from
  archived raw artifacts;
- checks task x method orientation, score direction, complete-case rules, and
  no-imputation conditions;
- recomputes all 109 pairwise cases with ordered mass transfer (101 finite,
  eight infeasible);
- recomputes the three primary Top-1/Top-3/Top-5 boundaries; and
- recomputes all 14 TabArena global feasible-winner entries with a fresh LP.

Run from the repository root:

```powershell
python verification/independent_verify.py `
  --archive-root C:\path\to\CERT_Bench_v0_8_ReleaseIntegrityWitnessClosure `
  --output-dir verification
python -m unittest verification/test_independent_verify.py
```

For the anonymous supplement, which intentionally omits third-party raw files,
run the same verification against the supplied derived matrices/results with:

```powershell
python verification/independent_verify.py `
  --archive-root C:\path\to\supplement_verification_bundle `
  --output-dir verification `
  --matrix-only
```

Build the manuscript-number and reference/identifier audit tables with
`build_audit_artifacts.py`. The script fails closed if a displayed value is
outside its stated precision tolerance or an identifier does not resolve.

The archive path is intentionally external: third-party raw artifacts are not
committed to this public repository.
