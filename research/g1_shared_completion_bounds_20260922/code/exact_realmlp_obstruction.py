"""Integer-DP upper obstruction, independent of the MILP solver.

Proves no compatible coarsened-release completion has RealMLP radius >55/2414.
Both rivals are treated jointly using exact clipped-sum constraints.
Second rival (TabPFN-2.6) is checked over every completion under that constraint
using an exact top-tail identity and a finite row-separable dynamic program.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import numpy as np,pandas as pd
from completion_bounds import rank_patterns,radius_exact
ROOT=Path(__file__).resolve().parents[1]
p=pd.read_csv(ROOT/'data/primary11__all__rank__equal__normalized_matrix.csv',index_col=0)
q=pd.read_csv(ROOT/'data/coverage9__all__rank__equal__normalized_matrix.csv',index_col=0)
names=p.columns.tolist();i=names.index('TA-REALMLP (tuned + ensemble)');a=names.index('TA-TABICLv2 (default)');b=names.index('TA-TABPFN-2.6 (default)')
D=142;scale=20;eps=F(55,2414);t=D*eps
known=np.rint(p.values*scale).astype(int)
ka=known[:,a]-known[:,i];kb=known[:,b]-known[:,i]
partials=[]
for task in q.index.difference(p.index):
 z=np.rint(rank_patterns(q.loc[task].reindex(names).values)*scale).astype(int)
 pairs=sorted(set(zip(z[:,a]-z[:,i],z[:,b]-z[:,i])))
 partials.append((task,pairs))
# min b is fixed for all completions: one known task attains it and no
# compatible partial row goes lower.
bmin=int(kb.min());assert all(bb>=bmin for _,pairs in partials for aa,bb in pairs)
# Both rivals have fixed minimum gaps across every compatible completion.
amin=int(ka.min());assert all(aa>=amin for _,pairs in partials for aa,bb in pairs)
k=t.numerator//t.denominator
# Uniform-TV support uses the (floor(D*epsilon)+1)-st largest donor gap
# as a maximizing clipping cutoff. Known rows bound that cutoff below.
avmin=sorted(map(int,ka),reverse=True)[k]
bvmin=sorted(map(int,kb),reverse=True)[k]
rows=[]
for va in range(avmin,scale+1):
 threshold=t*(va-amin)-sum(min(int(x),va) for x in ka)
 required=threshold.numerator//threshold.denominator+1
 for vb in range(bvmin,scale+1):
  dp={0:0}
  for task,pairs in partials:
   choices={}
   for aa,bb in pairs:
    ca=min(int(aa),va);cb=min(int(bb),vb)
    choices[ca]=max(choices.get(ca,-10**9),cb)
   nd={}
   for ca0,val0 in dp.items():
    for ca,cb in choices.items():
     key=ca0+ca;nd[key]=max(nd.get(key,-10**9),val0+cb)
   dp=nd
  feas=[score for asum,score in dp.items() if asum>=required]
  if not feas:best=None;residual=None
  else:
   best=max(feas)
   residual=F(sum(min(int(x),vb) for x in kb)+best)-t*(vb-bmin)
  rows.append(dict(first_cutoff_gap_units=va,second_cutoff_gap_units=vb,
   first_unknown_clipped_sum_strict_threshold=str(threshold),first_unknown_clipped_sum_integer_minimum=int(required),
   max_second_partial_clipped_sum=best,second_known_clipped_sum=sum(min(int(x),vb) for x in kb),
   max_scaled_margin_exact='infeasible' if residual is None else str(residual),
   all_nonpositive=residual is None or residual<=0,dp_final_states=len(dp)))
assert all(row['all_nonpositive'] for row in rows), [r for r in rows if not r['all_nonpositive']]
best_res=max(F(r['max_scaled_margin_exact']) for r in rows if r['max_scaled_margin_exact']!='infeasible')
info=dict(status='PASS_EXACT_INTEGER_ARITHMETIC',candidate=names[i],radius_upper_exact=str(eps),
 first_rival=names[a],second_rival=names[b],D=D,rank_integer_scale=scale,
 transferred_uniform_row_units_exact=str(t),known_first_gap_sum=int(ka.sum()),known_second_gap_sum=int(kb.sum()),
 fixed_first_minimum=amin,fixed_second_minimum=bmin,first_cutoff_range=[avmin,scale],second_cutoff_range=[bvmin,scale],
 maximum_second_margin_scaled_exact=str(best_res),maximum_second_margin_exact=str(best_res/(D*scale)),
 threshold_pairs_checked=len(rows),unresolved_tasks=len(partials),
 explanation='Any completion with radius greater than the stated bound must admit clipping cutoffs making both rival margins strictly positive. Exact integer DP over all admissible cutoff pairs proves this impossible.')
(ROOT/'results/realmlp_exact_obstruction.json').write_text(json.dumps(info,indent=2)+'\n')
pd.DataFrame(rows).to_csv(ROOT/'results/realmlp_exact_obstruction_thresholds.csv',index=False)
print(json.dumps(info,indent=2))
