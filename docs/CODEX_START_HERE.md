# Codex Start Here

## Immediate objective

Set up an independent, fail-closed verification workflow for the current CERT-Bench manuscript baseline.

Do not change the science. First reproduce it.

## Phase A — Repository intake
1. Inventory all available source matrices, scripts, manuscript source, supplement source, machine-readable outputs, and verification artifacts.
2. Record SHA-256 hashes for all result-determining inputs.
3. Identify missing artifacts before attempting reconstruction.
4. Do not infer or fabricate missing files.

## Phase B — Independent recomputation
Reimplement the result-determining optimization independently.

Verify:
- nominal winner;
- nearest challenger;
- Top-1 decision radius;
- Top-3 possible-entry radius;
- Top-5 possible-entry radius;
- finite pairwise winner boundaries;
- global feasible-winner entry;
- dominance/infeasibility cases;
- tie/equality semantics;
- normalization;
- score direction;
- no-imputation conditions.

Do not import the existing optimization implementation into the independent verifier.

## Phase C — MATLAB cross-check
If MATLAB Optimization Toolbox is available:
1. implement the LPs independently with `linprog`;
2. compare MATLAB results against the locked released results;
3. output a machine-readable difference table;
4. stop on any result-determining mismatch.

Simulink is not required unless a real scientific reason emerges.

## Phase D — manuscript number audit
Check every quantitative statement in the manuscript against machine-readable outputs.

Required table:
`location | manuscript value | source output | absolute difference | status`

## Phase E — TabArena historical artifact search
Search official TabArena history only for an immutable, byte-pinned artifact capable of reproducing the historical locked matrix exactly.

Rules:
- exact reproduction first;
- no approximate reconstruction;
- no causal claim;
- no living comparison if the historical lock fails;
- unresolved historical state => HOLD.

## Required outputs
- `verification/INDEPENDENT_VERIFICATION_REPORT.md`
- `verification/MATLAB_CROSSCHECK.csv`
- `verification/PYTHON_MATLAB_DIFFERENCE_AUDIT.csv`
- `verification/MANUSCRIPT_NUMBER_AUDIT.csv`
- `verification/TABARENA_HISTORICAL_ARTIFACT_SEARCH.md`
- `verification/SHA256SUMS.txt`

## Final status
Use exactly one:
- PASS — locked result independently reproduced
- FAIL — reproducibility/scientific defect found
- HOLD — required external evidence/artifact unavailable
