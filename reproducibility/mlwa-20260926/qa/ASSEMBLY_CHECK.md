# Public assembly check

Date: 26 September 2026. Version: `v0.8.1-mlwa-r2.20260926`.

Result: PASS for scientific-file preservation and execution in the assembled public directory. This report does not claim that an archive was published or that a final external DOI was assigned.

- All 31 selected supplemental files (28 runnable scientific core files plus three license/provenance records) remain byte-identical to their supplied versions after the fresh checks.
- All 14 selected witness-extension files (12 JSONL records files plus two checkers) match their recorded SHA256 values after the fresh checks.
- Fresh matrix recomputation passed 3/3 primary, 109/109 pairwise and 14/14 global cases. Raw reconstruction was not requested.
- Fresh standalone checks passed 101/101 finite pairwise witness records and 14/14 global records (13 finite and one infeasibility certificate).
- Three independent unit tests passed, including 120 seeded randomized pairwise LP comparisons.
- Maximum actual complementarity residual across the checked witness records was `4.649058915617843e-16`, below `1e-8`.
- The output JSON records the actual interpreter and scientific-library versions. No local filesystem paths or personal contact details are needed in the public QA.
- The assembled release excludes manuscript source/PDFs, private administrative notes/logs, full raw third-party artifacts and unrelated research snapshots. A targeted scan found no project-author identities, private email addresses, personal filesystem roots, private workspace links or credential-pattern matches in the assembled files.

Before publishing, update any intended public release identifiers, generate the final manifest, verify all manifest hashes, then validate the exact extracted ZIP and its file list. Changes to release metadata after this assembly check require regenerating the final manifest. Preserve the scope limitations in README.md.
