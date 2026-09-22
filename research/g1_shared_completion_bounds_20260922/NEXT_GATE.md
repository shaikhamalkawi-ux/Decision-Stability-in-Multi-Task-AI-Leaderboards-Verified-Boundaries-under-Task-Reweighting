# G2: evidence-tightening and novelty review, not benchmark expansion

## Preserve

Do not edit R3 or relabel its 122-task results. Keep the 11 published methods,
source gate, transformation, score direction, and tie semantics explicit. Do not
silently admit TabPFN-3 or newer living-registry results. The new endpoint
experiment is 142 tasks with equal full-scope task weights, not the R3 baseline.

## Recover the exact original partial evidence

Use `sources/INHERITED_THIRD_PARTY_RETRIEVAL_MANIFEST.json` for original raw-byte
identities. The old manifest itself reports missing exact download URLs. An
available new file with the same name is not an exact replacement. In particular,
recover the recorded core-task table and method artifacts for TabDPT and
TabPFN-2.6, then the other nine admitted methods and the source aggregation code.
Verify all raw bytes against their listed SHA-256 and byte counts. A new version
must be separately admitted and cannot be mixed into the frozen experiment.

Build a cell-status register: observed score, unsupported/failed evaluation,
not run, or unresolved. Preserve observed metric endpoints and admissible bounds.
Do not pretend a failed task has an unobserved ordinary score unless that
counterfactual completion is explicitly the research question.

Reconstruct the 122 complete rows exactly and the nine-model 142-task bridge.
For each of the other 20 tasks, retain *every* originally observed comparison,
including any available TabDPT or TabPFN-2.6 score. Generate only rank patterns
compatible with these additional constraints. Recompute sharp endpoints.

## Expected logical check

If the added evidence is consistent, its completion family F is a subset of the
G1 family C. The refined envelope must obey L(C) <= L(F) <= U(F) <= U(C).
G1 upper witnesses may cease to be admissible. Do not preserve their endpoint
values by omitting newly recovered constraints. Empty completion sets are an
admission error, not a zero-width certificate.

## Novelty scrutiny

Check the exact formulation against partial-ranking winner determination,
Borda/partial-chain results, incomplete-benchmark aggregation, and TV support
optimization. The candidate contribution is quantitative sharp TV stability
endpoints with shared rank completions, not the invention of possible winners,
missing-data analysis, mass transfer, or mixed-integer programming. Request a
mathematical reviewer to examine the proofs and exact DP certificate independently.

## Integration criterion

Integrate only if the contribution survives the closest-prior-work comparison.
The current mathematics can be reported for the precisely declared coarsened
ordinal model; calling it a sharp original-raw missingness result additionally
requires the raw admission work above. Replace repetitive exposition rather than
adding a new application section, new NASA data, or an arbitrary benchmark.
