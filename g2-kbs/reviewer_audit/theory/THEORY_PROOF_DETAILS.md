# Reviewer-auditable proof details

This note records the accepted exact-arithmetic proof structure for the four-task fixed-joint-mixture obstruction used in the paper.

## Feasible uncertain-task rank rows

With A fixed at normalized rank 1, the feasible triples `(r_B,r_C,r_D)` are:

- `(0,1/3,2/3)`
- `(1/3,0,2/3)`
- `(1/6,1/6,2/3)`
- `(0,1/2,1/2)`
- `(1/2,0,1/2)`
- `(1/3,1/3,1/3)`

All are realizable by the declared closed mean intervals. In every row, `r_B+r_C+r_D=1` and `r_D>=1/3`.

## Every compatible completion has no common weak winner

Let `g=(1-r_B,1-r_C,1-r_D)` and `t=(5/6,2/3,1/2)`. The A-minus-rival nominal gaps are

`v_j=(21/68)(g_j-t_j)-5/102`.

Both `g` and `t` sum to 2. Because the feasible coordinates are on the 1/6 lattice and `t` is not a feasible `g`, at least one coordinate has `g_j-t_j>=1/6`. Therefore

`max_j v_j >= 1/408 > 0`.

So A is excluded in every legal completion.

For B, C and D, feasible TV transfers of epsilon `13/400` yield largest possible A-minus-rival gaps

- B: `-211/4080`
- C: `-1/4080`
- D: `-211/4080`

and hence each non-A candidate is defeated by A somewhere in the admissible weight neighborhood.

## No completion-independent joint mixture uniformly excludes A

Use the two legal task-1 mean rows

- `z1=(3/4,0,1/8,1/4)`
- `z2=(3/4,1/4,1/4,1/4)`.

On the arithmetic average of their rank tables, the maximum A-minus-rival supports are

- B: `-11/40800`
- C: `-29/5100`
- D: `-11/40800`.

For any fixed probability mixture `mu` over admissible joint actions `(w,j)`, linearity gives

`(F_mu(z1)+F_mu(z2))/2 < 0`.

Thus at least one legal completion has negative payoff for every fixed `mu`, so no completion-independent joint mixture can certify A's exclusion uniformly over all compatible completions.

The averaged rank table is a convexified proof object, not a claimed realizable raw completion.

## Verification identities

- Exact evidence JSON SHA-256: `8d96a68de17e5bb02966458dd4a17d6063f679df3a5040b6dbe93cd501fc4d8f`
- Independent machine-audit JSON SHA-256: `c718d5bea6a8ddb36a4af78e57f6c1eddae05d2ef291e3bf67dff11b6dc71183`

The accompanying checker and tests are included in this reviewer-audit directory.
