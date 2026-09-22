"""Exact fixed-budget formulation; numerical solutions use HiGHS tolerances.

For epsilon >= 0, eta* = max over ONE compatible completion of
min_{j != i} min_{w in simplex: TV(w,w0)<=epsilon} w.(z_j-z_i).
eta* > 0 iff a completion has winner radius strictly greater than epsilon.
The strict comparison is essential at ties/flat zero margins.
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_array


def nondominated_pattern_indices(p, candidate):
    rivals=[j for j in range(p.shape[1]) if j!=candidate]
    g=p[:,rivals]-p[:,candidate,None]
    # Remove a pattern only under coordinatewise gap dominance; not merely a
    # nominal score comparison. This is valid for every nonnegative task weight.
    keep=[]
    for k in range(len(p)):
        dom=np.all(g>=g[k]-1e-13,axis=1)&np.any(g>g[k]+1e-13,axis=1)
        if not dom.any():keep.append(k)
    return np.array(keep,dtype=int)


def solve_joint_margin(patterns, candidate, epsilon, w0=None, relax=False, prune=True, time_limit=30):
    D=len(patterns);M=patterns[0].shape[1];rivals=[j for j in range(M) if j!=candidate];J=len(rivals)
    w0=np.full(D,1/D) if w0 is None else np.asarray(w0,float)
    if epsilon<0 or len(w0)!=D or (w0<0).any() or abs(w0.sum()-1)>1e-10:raise ValueError('Invalid epsilon/weights')
    kept=[nondominated_pattern_indices(p,candidate) if prune and len(p)>1 else np.arange(len(p)) for p in patterns]
    pp=[p[k] for p,k in zip(patterns,kept)]
    ys={}; n=1 # eta = x[0]
    for d,p in enumerate(pp):
        if len(p)>1:ys[d]=np.arange(n,n+len(p));n+=len(p)
    nu=np.arange(n,n+J);n+=J;t=np.arange(n,n+J);n+=J
    v=np.arange(n,n+J*D).reshape(J,D);n+=J*D
    lower=np.full(n,-1.);upper=np.ones(n);integrality=np.zeros(n)
    for idx in ys.values():lower[idx]=0;integrality[idx]=0 if relax else 1
    lower[t]=0
    rr=[];cc=[];aa=[];lb=[];ub=[]
    def row(items,l=-np.inf,u=0.):
        k=len(lb)
        for col,val in items:
            if val:rr.append(k);cc.append(int(col));aa.append(float(val))
        lb.append(l);ub.append(u)
    for d,idx in ys.items():row([(a,1) for a in idx],1,1)
    for j,rival in enumerate(rivals):
        row([(0,1),(nu[j],-1),(t[j],2*epsilon)]+[(v[j,d],-w0[d]) for d in range(D)])
        for d,p in enumerate(pp):
            gap=p[:,rival]-p[:,candidate]
            terms=[(nu[j],1),(v[j,d],1)]
            if d in ys:terms.extend((col,-value) for col,value in zip(ys[d],gap));rhs=0
            else:rhs=float(gap[0])
            row(terms,u=rhs)
            row([(v[j,d],1),(t[j],-1)])
            row([(v[j,d],-1),(t[j],-1)])
    A=coo_array((aa,(np.asarray(rr,dtype=np.int32),np.asarray(cc,dtype=np.int32))),shape=(len(lb),n)).tocsc()
    c=np.zeros(n);c[0]=-1
    res=milp(c,integrality=integrality,bounds=Bounds(lower,upper),constraints=LinearConstraint(A,lb,ub),options={'time_limit':time_limit,'mip_rel_gap':1e-10,'presolve':True})
    info=dict(epsilon=epsilon,relax=relax,status=int(res.status),message=res.message,
              variables=n,binary_count=int(integrality.sum()),retained_row_patterns=[len(p) for p in pp],
              eta=None if res.fun is None else -float(res.fun),
              eta_upper_bound=None if getattr(res,'mip_dual_bound',None) is None else -float(res.mip_dual_bound),
              mip_gap=None if getattr(res,'mip_gap',None) is None else float(res.mip_gap))
    z=None;weights=None
    if res.x is not None:
        z=np.empty((D,M));weights=[]
        for d,p in enumerate(pp):
            yy=res.x[ys[d]] if d in ys else np.array([1.])
            z[d]=yy@p;weights.append(yy)
        info['max_integrality_violation']=max((float(np.max(np.minimum(abs(w),abs(w-1)))) for d,w in enumerate(weights) if d in ys),default=0.)
        info['max_constraint_violation']=float(max(np.max(np.asarray(A@res.x)-np.asarray(ub)),np.max(np.asarray(lb)-np.asarray(A@res.x)),0.))
    return info,z,weights,kept
