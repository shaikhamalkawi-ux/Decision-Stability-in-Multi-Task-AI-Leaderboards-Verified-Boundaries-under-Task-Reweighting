# Fixed-trace Q-match audit

This audit is derived from the accepted Phase-8 TRACE_SUMMARY record and does not rerun the scientific producer.

- Trace records: 80
- Verified opposite-answer successes: 47
- Stored conditional fixed-trace lower/upper matches: 47
- Successful traces without the match flag: 0
- Match flags on inconclusive traces: 0
- Every matched record retains the numerical mean-enclosure qualification.
- Every matched record retains the finite-defined-target qualification.

## Interpretation

For each matched trace, the accepted Phase-8 witness proves ambiguity at Q-1 and the previously checked Q certificate supplies the qualified upper bound. The same opposite-answer pair also agrees on every earlier prefix of the same fixed trace, so the lower obstruction propagates to all q<Q.

Conditional on the original finite-defined-target and numerical mean-enclosure scope of the Q certificate, the first resolvable disclosure count along the recorded order is therefore q*=Q for those 47 traces.

This is a fixed-trace information result. It does not compare alternative disclosure orders and is not a global policy-optimality result.

## Machine-readable ledger

See `g2-kbs/results/fixed_trace_Q_match.csv`.
