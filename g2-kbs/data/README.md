# TabArena provenance and retrieval note

The empirical evaluation uses TabArena evidence with:

- 51 admitted tasks;
- 14 pre-specified methods;
- 816 paired fold vectors;
- four disclosure policies, ten seeds, and TV radii 2/51 and 4/51.

One disclosure is the complete method-loss vector for one recorded fold of one task.

The exact admitted task and method lists are recorded in `TABARENA_SCOPE.json`.

## Upstream retrieval boundary

The underlying benchmark evidence is third-party TabArena material cited in the manuscript. Raw upstream benchmark artifacts are not redistributed here where redistribution rights are unclear. To reconstruct the study, retrieve the corresponding TabArena source artifacts from the upstream TabArena release/repository identified by manuscript reference [12], then require exact identity with the retained research inputs before admission.

Accepted source identities:

- transcript SHA-256: `feddd565bc543dbc34dba2f19853c74f0ba030da55a3dab9a948f920563b3564`
- paired-fold CSV SHA-256: `8f06784d4a4b2f2449f28eec229b50b558832fd914384671df7e9a3a865d36dc`
- checkpoint record SHA-256: `a02a7077feb527498325a85fd09ffaba4dc13a6104a0a9f726cd3527fa83694f`

Do not silently substitute a newer hosted benchmark snapshot when its byte identity differs from these retained source identities.

## Public empirical verification material

- `TABARENA_SCOPE.json` records the admitted task/method scope and source identities.
- `../verification/PHASE8_EQUALIZED_CHECK.md` records the independently checked trial/comparison counts and claim boundaries.
- `../results/primary_summary.csv` records the publication-facing counts.

The public records support audit of the declared scope and reported counts without claiming redistribution rights over the upstream raw benchmark data.
