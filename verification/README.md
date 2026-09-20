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
