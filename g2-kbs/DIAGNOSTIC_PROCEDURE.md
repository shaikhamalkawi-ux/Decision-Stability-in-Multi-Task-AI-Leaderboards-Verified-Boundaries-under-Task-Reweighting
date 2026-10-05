# Sound diagnostic procedure

Given a partial transcript h, a nominal task-weight vector p, a total-variation radius epsilon, and a declared certificate family:

1. Search for two compatible completions with opposite decision labels. If verified, return **information-limited**.
2. Otherwise, attempt to prove that the decision label is constant over all compatible completions. If this is not established, return **inconclusive**.
3. If semantic determination is established, use a **complete certificate-existence test** for the declared family when one is available:
   - if a valid certificate is found, return **certified/resolved**;
   - if nonexistence of any valid certificate in the declared family is proved, return **certificate-limited**;
   - if certificate existence remains undecided because the search is incomplete, return **inconclusive**.

A failed or incomplete certificate search is therefore never, by itself, sufficient for a certificate-limited label.

The procedure is sound but need not be complete when the opposite-answer search, semantic-determination step, or certificate-existence step is incomplete.
