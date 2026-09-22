from completion_bounds import *
from joint_completion_milp import *
from fractions import Fraction
from pathlib import Path
import pandas as pd,numpy as np,json
root=Path(__file__).resolve().parents[1]
p=pd.read_csv(root/'data/primary11__all__rank__equal__normalized_matrix.csv',index_col=0);q=pd.read_csv(root/'data/coverage9__all__rank__equal__normalized_matrix.csv',index_col=0)
pat=[rank_patterns(p.loc[t].values if t in p.index else q.loc[t].reindex(p.columns).values) for t in q.index]
i=p.columns.get_loc('TA-REALMLP (tuned + ensemble)');rho=Fraction(55,2414);history=[]
for iteration in range(8):
 info,z,yy,kept=solve_joint_margin(pat,i,float(rho),time_limit=60)
 if z is None or info['status']!=0:
  raise RuntimeError('Joint solve did not certify optimality: '+str(info))
 rounded=np.rint(z*20)/20
 assert np.max(abs(z-rounded))<1e-7
 true=winner_radius(rounded,i,exact=True)
 info.update(iteration=iteration,input_radius_exact=str(rho),achieved_radius_exact=str(true))
 print(info,flush=True);history.append(info)
 if true>rho:rho=true
 else:break
pd.DataFrame(rounded,index=q.index,columns=p.columns).to_csv(root/'results/realmlp_joint_best_rank.csv',float_format='%.17g')
(root/'results/realmlp_joint_refinement.json').write_text(json.dumps(history,indent=2))
for j,name in enumerate(p.columns):
 if j!=i:print(name,radius_exact(rounded[:,j]-rounded[:,i]),flush=True)
