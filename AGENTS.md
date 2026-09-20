# AGENTS.md — CERT-Bench Research Rules

These instructions apply to Codex and any automated coding agent working in this repository.

## 1. Scientific lock
- Do not change scientific definitions, datasets, method/task scope, normalization, nominal weights, tie semantics, tolerances, numerical results, or manuscript claims unless a documented reproducibility defect is found.
- Never silently repair a mismatch.
- Any result-determining mismatch is a STOP condition and must be reported.

## 2. Current manuscript baseline
- Treat the current finding-first manuscript baseline as the active scientific baseline.
- The scientific narrative is:
  1. point rank is not decision proximity;
  2. pairwise access to the nominal winner is not equivalent to global feasible-winner status;
  3. winner, shortlist, and regime-specific stability are distinct decision events.
- CERT-Bench is the implementation/reproducibility layer, not the main narrative protagonist.

## 3. Reproducibility
- Recompute from released source matrices/data, not from cached result files.
- Keep matrix orientation explicit: tasks × methods.
- Enforce no-imputation where specified.
- Preserve score direction registries.
- Preserve exact stored-score tie construction rules and downstream numerical tolerances.
- Record software versions, solver versions, seeds, hashes, and input/output paths.

## 4. Independent verification
- Independent reimplementations must not import the result-determining optimization code they are checking.
- Prefer a second solver/language implementation where possible.
- MATLAB Optimization Toolbox / linprog may be used as an independent LP cross-check.
- Do not use Simulink unless a genuine scientific need is identified; this is not a control-system simulation paper.
- Verify primal feasibility, objective agreement, and dual/complementarity conditions when applicable.

## 5. Temporal/upstream checks
- Do not claim temporal validation, certificate drift, or benchmark drift unless an immutable historical artifact exactly reproduces the locked historical score matrix/result state.
- If exact historical reconstruction is unavailable, report HOLD.
- Never approximate or silently reconstruct a historical benchmark state.

## 6. Manuscript discipline
- Finding first, method second, reproducibility third.
- Do not introduce fuzzy logic, arbitrary stakeholder weights, new frameworks, new benchmarks, or additional claims without explicit scientific justification and approval.
- Avoid internal workflow language in the manuscript (e.g. lock, gate, checklist, package status) unless scientifically necessary.
- Keep all claims conditional on the actual evidence state.
- Do not describe deterministic radii as probabilities, confidence intervals, safety guarantees, regulatory certification, or stakeholder preference recovery.

## 7. Branch and review workflow
- Do not push result-changing edits directly to main.
- Use a dedicated branch and pull request for substantive changes.
- Report exactly what changed, why, which files changed, and whether any locked result changed.
- Keep generated artifacts separate from source.

## 8. Fail-closed outcome
Every independent audit must end with one of:
- PASS — locked result independently reproduced;
- FAIL — reproducibility/scientific defect found;
- HOLD — required external evidence/artifact unavailable.

No other wording may conceal an unresolved result.
