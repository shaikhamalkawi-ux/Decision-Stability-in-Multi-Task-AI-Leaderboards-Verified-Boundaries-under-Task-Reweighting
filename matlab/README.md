# MATLAB Cross-Implementation

Use MATLAB primarily as an independent LP implementation for CERT-Bench.

Preferred tool:
- Optimization Toolbox / `linprog`

Do not use Simulink unless a scientifically necessary dynamic-system component is introduced and justified. The current study is a benchmark decision-stability analysis, not a control-system simulation study.

Outputs should be machine-readable CSV/JSON where possible and compared numerically against the released locked results.
