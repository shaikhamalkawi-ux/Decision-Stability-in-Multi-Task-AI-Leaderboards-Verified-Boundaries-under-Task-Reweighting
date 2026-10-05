# Reviewer-auditable exact proof record

This note states the two synthetic certificate-obstruction constructions used in the manuscript in a form intended for independent audit. It contains no TabArena data and requires only exact rational arithmetic.

## Decision convention

There are four methods A, B, C, D. Within each task, lower loss is better and normalized midranks are `(rank-1)/3`. For an ordered candidate-rival pair `(i,j)`, the weighted gap is candidate rank minus rival rank. A positive gap means the candidate loses to the rival. A method is a common weak winner if all of its ordered-pair support values are nonpositive throughout the declared total-variation (TV) weight neighborhood.

The certificate family studied in the paper fixes, for each candidate, one completion-independent distribution over joint actions `(w,j)`, where `w` is an admissible task-weight vector and `j` is a rival. A positive expected candidate-minus-rival gap for every compatible completion excludes that candidate. The theorem asks whether semantic determination of “no common weak winner” implies existence of such a fixed joint mixture.

---

## A. Four-task nonuniform construction

### A.1 Data and completion set

Nominal task weights and TV radius are

- `p = (21,21,21,5)/68`
- `epsilon = 13/400`.

Task 1 has three disclosed fold vectors

- `(1,0,0,1)`
- `(1,0,0,0)`
- `(1,0,0,0)`

and one unknown vector in `[0,1]^4`. Therefore the exact task-1 mean intervals are

- A: `[3/4,1]`
- B: `[0,1/4]`
- C: `[0,1/4]`
- D: `[1/4,1/2]`.

The other tasks are fully disclosed and have normalized-rank rows

- Task 2: `(0,1/3,2/3,1)`
- Task 3: `(1/2,1,1/2,0)`
- Task 4: `(0,2/3,2/3,2/3)`.

Every legal task-1 completion has A last and yields exactly one of the six normalized-rank rows

1. `(1,0,1/3,2/3)`
2. `(1,1/3,0,2/3)`
3. `(1,1/6,1/6,2/3)`
4. `(1,0,1/2,1/2)`
5. `(1,1/2,0,1/2)`
6. `(1,1/3,1/3,1/3)`.

These six weak-order patterns are exhaustive and realizable.

### A.2 Every completion has no common weak winner

For task 1 write `(r_B,r_C,r_D)` for the three rival ranks, define

- `g = (1-r_B, 1-r_C, 1-r_D)`
- `t = (5/6, 2/3, 1/2)`.

The nominal A-minus-rival gaps are

`v_j = (21/68)(g_j-t_j) - 5/102`.

Both `g` and `t` sum to 2. Every coordinate of every feasible `g` lies on the `1/6` grid, while `t` is not a feasible `g`. Hence at least one coordinate satisfies `g_j-t_j >= 1/6`, so

`max_j v_j >= 21/(68*6) - 5/102 = 1/408 > 0`.

Thus A is strictly defeated at the nominal weights in every legal completion.

For B, transfer `epsilon` from Task 1 to Task 4. The A-minus-B gap becomes

`1/408 - (21/68)r_B - epsilon(5/3-r_B)`.

Because `21/68 > epsilon`, this is maximized at `r_B=0`, where it equals

`1/408 - 13/240 = -211/4080 < 0`.

Therefore B is strictly defeated by A at an admissible weight.

For C, transfer `epsilon` from Task 1 to Task 2. The A-minus-C gap is

`11/204 - (21/68)r_C - epsilon(5/3-r_C)`

and is maximized at `r_C=0`, giving

`11/204 - 13/240 = -1/4080 < 0`.

For D, transfer `epsilon` from Task 1 to Task 2. The A-minus-D gap is

`43/408 - (21/68)r_D - epsilon(2-r_D)`.

Since every feasible row has `r_D >= 1/3`, its maximum occurs at `r_D=1/3` and equals

`1/408 - 13/240 = -211/4080 < 0`.

Hence A, B, C and D are all excluded from common-weak-winner status for every compatible completion. The defeating rival and admissible weight are allowed to depend on the candidate and completion.

### A.3 No completion-independent joint mixture can uniformly exclude A

Consider two legal task-1 mean rows

- `z1 = (3/4,0,1/8,1/4)` with unknown fold `(0,0,1/2,0)` and rank row 1 above;
- `z6 = (3/4,1/4,1/4,1/4)` with unknown fold `(0,1,1,0)` and rank row 6 above.

On the arithmetic average of the two rank tables, the A-minus-rival task-gap rows are

| Rival | Task 1 | Task 2 | Task 3 | Task 4 |
|---|---:|---:|---:|---:|
| B | 5/6 | -1/3 | -1/2 | -2/3 |
| C | 2/3 | -2/3 | 0 | -2/3 |
| D | 1/2 | -1 | 1/2 | -2/3 |

The exact TV supports are

- B: `-11/40800 < 0`
- C: `-29/5100 < 0`
- D: `-11/40800 < 0`.

Let `mu` be any completion-independent probability distribution over admissible `(w,j)` actions. Linearity in the rank table gives

`[F_mu(z1)+F_mu(z6)]/2 < 0`.

Therefore at least one of `z1,z6` has negative mixed payoff. No fixed joint mixture can have positive exclusion payoff for A on every legal completion, although the semantic “no common weak winner” decision is fixed. This proves certificate limitation for the declared family.

---

## B. Uniform 68-task construction with independent unknown folds

### B.1 Construction

Use 68 distinct tasks with nominal weight `1/68` each and the same radius `epsilon=13/400`.

- Block 1: 21 independently incomplete tasks. Each has the same three disclosed vectors as Task 1 above and its own independent unknown vector in `[0,1]^4`.
- Block 2: 21 fully known tasks with rank row `(0,1/3,2/3,1)`.
- Block 3: 21 fully known tasks with rank row `(1/2,1,1/2,0)`.
- Block 4: 5 fully known tasks with rank row `(0,2/3,2/3,2/3)`.

Each uncertain task independently takes one of the same six feasible rank-row types. Heterogeneous assignments are allowed.

### B.2 Symmetry reduction

The 21 uncertain tasks are exchangeable under the uniform nominal center. A rank table is therefore characterized, for support calculations, by the counts of the six row types. The number of weak compositions of 21 into six counts is

`C(26,5) = 65,780`.

For four methods there are `4*3 = 12` ordered candidate-rival comparisons per state, giving

`65,780 * 12 = 789,360`

ordered support comparisons.

### B.3 Exclusion of A for every heterogeneous completion

For an uncertain row let `h = 6*(A-minus-(B,C,D))`. The six possible integer vectors are

| Type | h_B | h_C | h_D |
|---|---:|---:|---:|
| 1 | 6 | 4 | 2 |
| 2 | 4 | 6 | 2 |
| 3 | 5 | 5 | 2 |
| 4 | 6 | 3 | 3 |
| 5 | 3 | 6 | 3 |
| 6 | 4 | 4 | 4 |

Every row sums to 12. Let `S_j` be the sum of coordinate `j` across the 21 uncertain tasks and let `m_j` be the coordinatewise maximum among the row types that appear. The nominal A-minus-rival gaps are

- `v_B = (S_B-125)/408`
- `v_C = (S_C-104)/408`
- `v_D = (S_D-83)/408`.

They satisfy `v_B+v_C+v_D = -5/34` for every heterogeneous assignment.

The exact upper supports are

- `H_B = v_B + epsilon*(m_B+4)/6`
- `H_C = v_C + epsilon*(m_C+4)/6`
- `H_D = v_D + epsilon*(max(m_D,3)+6)/6`.

The mass transfers attaining these supports are feasible despite `epsilon > 1/68`: the donor coefficient is repeated across a fixed known block with total nominal mass at least `5/68 > epsilon`, so the radius can be withdrawn across several equal-minimum atoms and placed on one maximum atom.

For any observed type set containing a distinct-type pair other than `{1,4}` or `{2,5}`, the maxima obey

`m_B + m_C + max(m_D,3) >= 14`.

Hence

`H_B+H_C+H_D >= -5/34 + (13/400)*(28/6) = 47/10200 > 0`,

so at least one rival strictly defeats A at an admissible weight.

The remaining exceptional type sets are handled at nominal weights:

- subset of `{1,4}`: `v_B = 1/408 > 0`;
- subset of `{2,5}`: `v_C = 11/204 > 0`;
- singleton `{3}`: `v_C = 1/408 > 0`;
- singleton `{6}`: `v_D = 1/408 > 0`.

This exhausts all 63 nonempty type subsets and therefore every heterogeneous completion.

### B.4 Exclusion of B, C and D

Let `bar r_j` be the average uncertain-task rank of rival `j`. Always `bar r_B,bar r_C >= 0` and `bar r_D >= 1/3`.

Withdraw total mass `epsilon` proportionally from all 21 uncertain-task atoms, and redistribute it proportionally within a known receiving block. The resulting A-minus-rival gaps obey

- B: `1/408 - (21/68)bar r_B - epsilon(5/3-bar r_B) <= -211/4080 < 0`;
- C: `11/204 - (21/68)bar r_C - epsilon(5/3-bar r_C) <= -1/4080 < 0`;
- D: `43/408 - (21/68)bar r_D - epsilon(2-bar r_D) <= -211/4080 < 0`.

Thus B, C and D are strictly defeated by A at admissible weights for every completion. Combined with B.3, every one of the 65,780 canonical count states has no common weak winner.

### B.5 Completion-independent mixture obstruction

Select two legal global completions:

- `Z1`: all 21 uncertain tasks use type 1;
- `Z6`: all 21 uncertain tasks use type 6.

These are two particular members of the independent product completion set; they do not impose synchronization on other completions.

Their average uncertain-block rank row yields the same A-minus-rival gaps `(5/6,2/3,1/2)` as in the four-task average. Exact pushforward/lifting of the uniform micro-task TV ball to the four block masses gives supports

- B: `-11/40800`
- C: `-29/5100`
- D: `-11/40800`.

Therefore, for any completion-independent joint mixture `mu`,

`[F_mu(Z1)+F_mu(Z6)]/2 < 0`,

so no such mixture can exclude A on every completion. The semantic decision is fixed, but the declared certificate family is incomplete.

---

## C. Exact replay

Run:

```bash
python code/replay_exact_obstructions.py
```

The replay uses only `fractions.Fraction` and enumerates all 65,780 canonical uniform-center states and all 789,360 ordered support comparisons. Its expected summary is stored in `verification/REPLAY_SUMMARY.json`.

The repository also preserves the accepted exact-evidence and independent-check JSON/Markdown records used during the research audit. These files support traceability; the analytical derivations above carry the theorem claims.