# Sound diagnostic procedure

Given a partial transcript h, a nominal task-weight vector p, a total-variation radius epsilon, and a declared certificate family:

1. Search for two compatible completions with opposite decision labels. If verified, return **information-limited**.
2. Otherwise, attempt to prove that the decision label is constant over all compatible completions. If this is not established, return **inconclusive**.
3. If semantic determination is established, evaluate the declared certificate. If the certificate succeeds, return **certified/resolved**; otherwise return **certificate-limited**.

The procedure is sound but need not be complete when the witness search or semantic-determination subroutine is incomplete.
