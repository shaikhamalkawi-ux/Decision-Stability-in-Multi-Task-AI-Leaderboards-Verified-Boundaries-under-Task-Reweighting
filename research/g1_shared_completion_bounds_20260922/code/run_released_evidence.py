from pathlib import Path
import numpy as np,pandas as pd,json,hashlib,shutil,math
from fractions import Fraction
from scipy.stats import rankdata
from completion_bounds import *
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data';OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
p=pd.read_csv(DATA/'primary11__all__rank__equal__normalized_matrix.csv',index_col=0)
q=pd.read_csv(DATA/'coverage9__all__rank__equal__normalized_matrix.csv',index_col=0)
assert p.shape==(122,11) and q.shape==(142,9)
assert set(p.index).issubset(q.index) and set(q.columns).issubset(p.columns)
common=(rankdata(p[q.columns].values,axis=1,method='average')-1)/8
assert np.max(abs(common-q.loc[p.index].values)) < 1e-12
methods=p.columns.tolist();tasks=q.index.tolist();D=len(tasks);M=len(methods)
unknown=[c for c in methods if c not in q.columns];counts=[];patterns=[];masked=[]
for task in tasks:
 if task in p.index:
  a=p.loc[task].values
 else:
  a=q.loc[task].reindex(methods).values
  masked.append(task)
 patt=rank_patterns(a)
 patterns.append(patt)
 counts.append(dict(task=task,compatible_rank_vectors=len(patt),unspecified_candidates=';'.join(unknown) if task in masked else ''))
pd.DataFrame(counts).to_csv(OUT/'released_ordinal_row_patterns.csv',index=False)

def fmt(f):return 'inf' if f is None else str(f)
def num(f):return math.inf if f is None else float(f)
rows=[];byrival=[]
for i,candidate in enumerate(methods):
 b=extremal_gap_bounds(patterns,i,exact=True)
 jlo=min(range(M-1),key=lambda j:num(b['lower_by_rival'][j]))
 low_idx=b['argmin'][:,jlo]
 zlo=np.array([p[k] for p,k in zip(patterns,low_idx)])
 low_true=winner_radius(zlo,i,exact=True)
 assert low_true==b['lower']
 # Build a shared completion that maximizes gaps to each possible binding rival,
 # then retain the one with the largest actual all-competitor radius.
 zbest=None;best=None;argbest=None
 for j in range(M-1):
  idx=b['argmax'][:,j]
  z=np.array([p[k] for p,k in zip(patterns,idx)])
  true=winner_radius(z,i,exact=True)
  if zbest is None or num(true)>num(best):best=true;zbest=z;argbest=j
 sharp=best==b['upper_relaxation']
 for j,rival in enumerate(b['rivals']):
  byrival.append(dict(candidate=candidate,rival=methods[rival],lower_pairwise_exact=fmt(b['lower_by_rival'][j]),upper_pairwise_exact=fmt(b['upper_by_rival'][j])))
 rows.append(dict(candidate=candidate,complete_case_radius_exact=fmt(winner_radius(p.values,i,exact=True)),
  lower_radius_exact=fmt(low_true),lower_radius=float(low_true) if low_true is not None else math.inf,
  upper_feasible_exact=fmt(best),upper_feasible=num(best),upper_relaxation_exact=fmt(b['upper_relaxation']),upper_relaxation=num(b['upper_relaxation']),
  sharp_upper=sharp,lower_binding=methods[b['rivals'][jlo]],upper_construction_rival=methods[b['rivals'][argbest]],
  lower_nominal_winner=methods[int(zlo.mean(axis=0).argmin())],upper_nominal_winner=methods[int(zbest.mean(axis=0).argmin())]))
 tag=str(i).zfill(2)
 for suffix,z in [('lower',zlo),('upper_feasible',zbest)]:
  # Semantic constraints: full observed rankings preserved and restricted
  # rankings on all nine-model rows preserved, with exact ties.
  for d,task in enumerate(tasks):
   cols=range(M) if task in p.index else [methods.index(c) for c in q.columns]
   expected=p.loc[task].values if task in p.index else q.loc[task].values
   selected=z[d,list(cols)]
   assert np.array_equal(np.sign(selected[:,None]-selected[None,:]),np.sign(expected[:,None]-expected[None,:]))
  pd.DataFrame(z,index=tasks,columns=methods).to_csv(OUT/f'completion_{tag}_{suffix}_rank.csv',float_format='%.17g',index_label='task')
 print(rows[-1],flush=True)
pd.DataFrame(rows).to_csv(OUT/'initial_screening_envelopes.csv',index=False)
pd.DataFrame(byrival).to_csv(OUT/'released_ordinal_pairwise_envelopes.csv',index=False)
meta=dict(evidence_type='COARSENED_RELEASED_ORDINAL_EVIDENCE_NOT_FULL_RAW_SCORE_AUDIT',
 no_claim='The 40 unspecified positions are not asserted to be the original raw missing-cell pattern.',
 complete_tasks=122,full_tasks=142,methods=11,additional_tasks=20,unspecified_method_task_positions=40,unspecified_candidates=unknown,
 state_count_exact=str(math.prod(len(a) for a in patterns)),screening_sharp_upper_count=sum(r['sharp_upper'] for r in rows),
 primary_input_sha256=hashlib.sha256((DATA/'primary11__all__rank__equal__normalized_matrix.csv').read_bytes()).hexdigest(),
 bridge_input_sha256=hashlib.sha256((DATA/'coverage9__all__rank__equal__normalized_matrix.csv').read_bytes()).hexdigest())
# Count each observed unordered pair; numerical margins are not retained in this ordinal gate.
meta['observed_pairwise_relations']=122*55+20*36
(OUT/'released_ordinal_audit.json').write_text(json.dumps(meta,indent=2)+'\n')
