# Reviewer audit index

This directory supports the KBS submission candidate.

## Public reviewer-facing materials
- `theory/THEORY_PROOF_DETAILS.md` — analytical proof details for the fixed-joint-mixture obstruction.
- Public result and verification summaries in the parent `g2-kbs` directory.
- Diagnostic procedure and provenance notes in the parent directory.

## Reviewer package supplied with the submission
The submission package also contains two audit archives:

1. `REVIEWER_AUDIT_THEORY_FIXED_MIXTURE.zip`
   - analytical proof,
   - independent analytical review,
   - exact verification protocol,
   - exact checker and tests,
   - exact-case evidence JSON,
   - independent machine-check outputs.

2. `REVIEWER_AUDIT_PHASE8_EQUALIZED_WITNESSES.zip`
   - witness-construction and verification code,
   - tests,
   - aggregate and trace-level summaries,
   - trial ledger,
   - verification outputs,
   - external-dependency record.

The reviewer archives do not redistribute third-party raw TabArena data. They rely on the upstream benchmark materials identified by the provenance record.

## Claim boundary
The theory package supports the certificate-limited construction. The Phase-8 package supports the information-limited witness analysis. The 33 traces without a verified opposite-answer pair remain inconclusive and are not relabeled as certificate-limited.
