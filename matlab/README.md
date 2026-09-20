# MATLAB Cross-Implementation

Use MATLAB primarily as an independent LP implementation for CERT-Bench.

Preferred tool:
- Optimization Toolbox / `linprog`

Do not use Simulink unless a scientifically necessary dynamic-system component is introduced and justified. The current study is a benchmark decision-stability analysis, not a control-system simulation study.

Outputs should be machine-readable CSV/JSON where possible and compared numerically against the released locked results.

`independent_lp_crosscheck.m` accepts one released normalized matrix, its
nominal-weight CSV, and an output CSV path. It does not depend on the Python
implementation. A MATLAB installation with an active Optimization Toolbox
license is required.
