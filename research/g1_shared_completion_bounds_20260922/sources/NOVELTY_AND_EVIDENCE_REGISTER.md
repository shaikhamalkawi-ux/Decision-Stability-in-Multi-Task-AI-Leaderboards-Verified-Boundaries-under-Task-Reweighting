# Novelty and evidence register — 22 September 2026

## Research question retained

For a specified model, full task scope, nominal weight vector and admissible
rank-completion family, determine sharp lower and upper endpoints of the minimum
TV task-weight movement that removes unique-winner status. Separate the exact
lower endpoint from a potentially unattainable pairwise upper relaxation.

## Closest primary sources checked

1. **Himmi, A., Irurozki, E., Noiry, N., Clémençon, S., and Colombo, P. (2024).**
   *Towards More Robust NLP System Evaluation: Handling Missing Scores in Benchmarks.*
   Findings of EMNLP, 11759–11785. DOI: 10.18653/v1/2024.findings-emnlp.688.
   Primary: https://aclanthology.org/2024.findings-emnlp.688/ and its paper PDF.
   Existing contribution: compatible partial rankings, missing-score treatment,
   and Borda aggregation. Therefore missing-score benchmark analysis and compatible
   rankings are not new. The proposed target is an extremal TV decision radius,
   not a completed point ranking. Scope checked: abstract, problem framing and
   method sections. No claim of exhaustive comparison of every variant.

2. **Xia, L., and Conitzer, V. (2011).** *Determining Possible and Necessary Winners
   Given Partial Orders.* JAIR 41, 25–67. DOI: 10.1613/jair.3186.
   Primary author deposit: https://arxiv.org/abs/1401.3876.
   Existing contribution: necessary/possible winner semantics and computational
   characterization. The all/some-completion quantifiers are inherited foundations,
   not a proposed invention. A positive radius refines unique nominal feasibility
   by asking how much task-weight displacement can be survived.

3. **Chakraborty, V., Delemazure, T., Kimelfeld, B., Kolaitis, P. G., Relia, K., and
   Stoyanovich, J. (2021).** *Algorithmic Techniques for Necessary and Possible Winners.*
   ACM/IMS Transactions on Data Science 2(3), Article 22. DOI: 10.1145/3458472.
   Primary author deposit: https://arxiv.org/abs/2005.06779; full paper examined.
   Existing contribution: practical ILP formulations for possible winners and
   accelerated necessary-winner calculations. Generic ILP or shared complete
   rankings cannot be claimed as new. G1 couples one shared rank completion to
   dual certificates for a continuum of TV-bounded task weights.

4. **Chakraborty, V., and Kolaitis, P. G. (2021).** *Classifying the Complexity of the
   Possible Winner Problem on Partial Chains.* AAMAS, 297–305.
   Primary: https://research.ibm.com/publications/classifying-the-complexity-of-the-possible-winner-problem-on-partial-chains
   Author deposit: https://arxiv.org/abs/2002.12510.
   Existing contribution: complexity on partial chains, i.e. ordering only a subset
   of candidates. This is especially close to ordinal missing-model evidence.
   G1 does not claim a generic polynomial-time upper-envelope algorithm or a new
   hardness theorem. It also allows new ties, unlike a strict-completion restriction.

5. **Charalambous, C. D., Tzortzis, I., Loyka, S., and Charalambous, T. (2013).**
   *Extremum Problems with Total Variation Distance and their Applications.*
   Primary author deposit: https://arxiv.org/abs/1301.4763.
   Existing contribution: TV-constrained linear-functional extrema and closed-form
   extremal distributions. Ordered mass transfer and the clipping-support identity
   are computational foundations here, not novelty claims.

6. **Ghosh, A., Dziadzio, S., Prabhu, A., Udandarao, V., Albanie, S., and Bethge, M.
   (2025 revision).** *ONEBench to Test Them All: Sample-Level Benchmarking Over
   Open-Ended Capabilities.* arXiv:2412.06745v2.
   Primary: https://arxiv.org/html/2412.06745v2.
   Existing contribution: aggregation of heterogeneous incomplete sample-level
   evaluations and model-score identification under its assumptions. G1 instead
   computes deterministic extrema over an explicit admissible completion family;
   it does not assert asymptotic recovery or assign completion probabilities.

## Novelty verdict

The search supports a **narrow candidate contribution**, not a first-in-literature
certificate. Required positioning: sharp, rank-consistent TV stability envelopes;
separation of the cheap sharp lower endpoint from the coupled upper problem;
constructive incompatibility example; exact endpoint certificates on declared
released benchmark evidence. General minimax inequalities, necessary/possible
winner notions, partial-order modeling, TV extrema and MILP are acknowledged
foundations. Absence of a matching search result is not proof of originality.

## Evidence used versus evidence unavailable

Source inputs are two byte-identical author-derived matrices recovered from the
R3 supplement. The 122-by-11 matrix and 142-by-9 matrix agree exactly in their
nine-model relative rankings on shared tasks. G1 retains those relations and no
additional raw-score information. The 20 remaining rows admit 381 weak orders
each after inserting two unspecified model positions, including ties.

The original raw artifact manifest preserves hashes and byte counts but states
that exact per-file download URLs were not retained. Neither the recovered R3
working package nor the recovered R2C archive supplied the raw parquet files.
Therefore this is a **coarsened released-ordinal experiment**, not a reconstruction
of the original missing-score/failure mask. Additional exact raw evidence could
remove current endpoint witnesses and narrow the envelope. No source was silently
updated from a live registry to replace the frozen snapshot.

## Search coverage

Queries covered incomplete benchmark score/ranking evaluation, partial-order
necessary/possible winners, partial chains, margin of victory, uncertain weights,
and total-variation ranking sensitivity. Relevant primary papers were opened as
listed above. Some unrelated search results were discarded. This register is a
focused novelty screen, not a systematic review or comprehensive database search.
