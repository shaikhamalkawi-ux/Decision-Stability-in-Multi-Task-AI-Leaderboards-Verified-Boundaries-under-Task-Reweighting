# Fixed-trace decision-point audit

For a fixed disclosure trace, let h_q denote the first q disclosures and define

q* = min { q : D(X) is constant over all X in X(h_q) }.

The frozen Phase-8 ledger contains verified opposite-answer completion witnesses at Q-1 on 47 of the 80 predeclared traces. Those same 47 identities match the accepted stopping records at Q, whose mean-enclosure certificate proves the no-common-weak-winner decision for every compatible completion.

Therefore, on each of those 47 fixed disclosure traces:

- the Q-1 witness proves q* >= Q;
- the checked Q certificate proves q* <= Q;
- hence q* = Q.

Identity audit: 80/80 Phase-2 / Phase-6 / Phase-8 trace identities matched, with 0 mismatches. The 47 recorded successes correspond to 35 unique trace/prefix hashes because some predeclared policies coincide.

Decision-point counts:
- epsilon=2/51: 39/40 exact q*=Q; Q range 786–816; median 816.
- epsilon=4/51: 8/40 exact q*=Q; Q range 726–812; median 726.
- combined: 47/80 exact q*=Q; Q range 726–816; median 816.

This result is specific to the declared completion model and each fixed disclosure order. It does not claim that the disclosure order itself is optimal. The remaining 33 traces are not assigned an exact q* by the current witness search.
