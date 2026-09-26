# TabArena historical-artifact search

Status: **HOLD for the temporal extension only**. This does not block the v0.8/R2B primary result.

## Frozen target

The active scientific baseline is the byte-pinned v0.8 release archive with SHA-256:

`0a85ae39025ad7d8e4bbca031752964a18c1a5c012f246929ee8c92cc0205511`

Its TabArena primary state is 51 tasks x 14 methods, RealMLP as winner, and Top-1/Top-3/Top-5 radii `0.0366013072`, `0.0283224401`, and `0.0054466231`.

## Historical search result

The R3 collection referenced the official TabArena repository at commit `f64c3742f2cb1b734ecbfa6b429cba76afec2c73`. The recovered collection matches the locked task count, method count, and winner, but it does not reproduce the locked normalized matrix or radii. Its observed Top-1/Top-3/Top-5 radii are `0.02521008403361362`, `0.029411764705882897`, and `0.014447884416924938`.

No immutable historical artifact was recovered that reproduces the byte-pinned locked matrix exactly while also providing the intended temporal provenance. The mismatch is therefore treated as a provenance boundary, not silently reconciled.

## Decision

- R3 temporal claims and figures: not integrated.
- R2B/v0.8 locked primary science: unchanged and independently reproduced from the byte-pinned archive.
- Reopening condition: an immutable historical artifact whose hashes and admitted matrix reproduce the locked baseline, or an explicitly authorized new estimand/version with a fresh lock and manuscript-level interpretation.
