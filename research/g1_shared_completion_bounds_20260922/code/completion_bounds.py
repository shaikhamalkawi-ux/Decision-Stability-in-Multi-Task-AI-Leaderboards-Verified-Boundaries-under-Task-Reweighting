"""Finite rank-consistent completion envelopes for conditional winner stability.

Exploratory contribution gate, not a change to CERT-Bench R3.
Ranks use average positions for ties; all losses are lower-is-better.
No probabilistic distribution or imputed point estimate is assigned to missing cells.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import product
from typing import Sequence
import math
import numpy as np
from scipy.optimize import linprog


def rank_patterns(observed: Sequence[float], allow_ties: bool=True) -> np.ndarray:
    """All weak-order rank vectors extending finite observed scores.

    NaN means unspecified. The completion model imposes only observed order/tie
    constraints. Bounds or cross-task restrictions require a restricted pattern
    generator; they are not silently imposed here. All scores are loss-like.
    """
    a=np.asarray(observed,dtype=float)
    if a.ndim != 1 or len(a)<2 or np.isinf(a).any():
        raise ValueError('Require a one-dimensional loss row with M>=2; NaN permitted, inf forbidden')
    m=len(a); known=np.where(np.isfinite(a))[0]
    blocks=tuple(tuple(int(k) for k in known if a[k]==v) for v in sorted(set(a[known])))
    patterns=[blocks]
    for k in np.where(np.isnan(a))[0]:
        nxt=[]
        for b in patterns:
            for pos in range(len(b)+1):
                nxt.append(b[:pos]+((int(k),),)+b[pos:])
            if allow_ties:
                for pos in range(len(b)):
                    nxt.append(b[:pos]+(b[pos]+(int(k),),)+b[pos+1:])
        patterns=nxt
    out=[]
    for b in patterns:
        r=np.empty(m); pos=0
        for block in b:
            r[list(block)]=(pos+(len(block)-1)/2)/(m-1)
            pos+=len(block)
        out.append(r)
    ans=np.array(out)
    if len(ans)!=len(np.unique(ans,axis=0)):
        raise AssertionError('Duplicate weak-order patterns')
    return ans


def radius_exact(g: Sequence[Fraction|int|float], w0: Sequence[Fraction|int|float]|None=None):
    """Exact rational TV distance to g.w <= 0; None denotes +infinity.

    Uses donor transfer to any minimum-gap row. The rational conversion of floats
    is intended only for exactly discrete ranks and rational declared weights.
    """
    def frac(x):
        if isinstance(x,Fraction): return x
        return Fraction(float(x)).limit_denominator(10**9)
    g=[frac(x) for x in g]; d=len(g)
    w=[Fraction(1,d) for _ in g] if w0 is None else [frac(x) for x in w0]
    if d<1 or len(w)!=d or min(w)<0 or sum(w)!=1:
        raise ValueError('Invalid probability weights')
    gap=sum(a*b for a,b in zip(g,w))
    if gap<=0:return Fraction(0)
    low=min(g)
    if low>0:return None
    moved=Fraction(0)
    for k in sorted(range(d),key=lambda k:-g[k]):
        improvement=g[k]-low
        if improvement<=0:break
        amount=min(w[k],gap/improvement)
        moved+=amount;gap-=amount*improvement
        if gap==0:return moved
    raise AssertionError('Feasible rational boundary not reached')


def radius_float(g, w0=None):
    g=np.asarray(g,float);d=len(g)
    w=np.full(d,1/d) if w0 is None else np.asarray(w0,float)
    gap=float(w@g)
    if gap <= 1e-12:return 0.0
    low=float(g.min())
    if low>1e-12:return math.inf
    moved=0.0
    for k in np.argsort(-g,kind='stable'):
        diff=g[k]-low
        if diff<=1e-14:break
        amount=min(w[k],gap/diff); moved+=amount;gap-=amount*diff
        if gap<=1e-12:return moved
    raise AssertionError('Feasible boundary not reached')


def radius_lp(g, w0=None):
    g=np.asarray(g,float);d=len(g)
    w0=np.full(d,1/d) if w0 is None else np.asarray(w0,float)
    A=np.block([[np.eye(d),-np.eye(d)],[-np.eye(d),-np.eye(d)]])
    A=np.vstack([A,np.r_[g,np.zeros(d)]])
    b=np.r_[w0,-w0,0.]
    eq=np.r_[np.ones(d),np.zeros(d)][None,:]
    out=linprog(np.r_[np.zeros(d),np.full(d,.5)],A_ub=A,b_ub=b,A_eq=eq,b_eq=[1.],bounds=(0,None),method='highs')
    if out.status==2:return math.inf,None
    if not out.success:raise RuntimeError(out.message)
    return float(out.fun),out.x[:d]


def winner_radius(z, candidate, exact=False, w0=None):
    m=np.asarray(z).shape[1]
    vals=[(radius_exact if exact else radius_float)(np.asarray(z)[:,j]-np.asarray(z)[:,candidate],w0) for j in range(m) if j!=candidate]
    if exact:
        finite=[r for r in vals if r is not None]
        return min(finite) if finite else None
    return min(vals)


def extremal_gap_bounds(patterns, candidate, exact=False, w0=None):
    """Exact lower radius and pairwise-relaxed upper bound.

    The upper result is NOT automatically attainable by one shared completion.
    """
    m=patterns[0].shape[1]; rivals=[j for j in range(m) if j!=candidate]
    lower=np.zeros((len(patterns),len(rivals)));upper=lower.copy()
    argmin=[];argmax=[]
    for d,p in enumerate(patterns):
        gaps=p[:,rivals]-p[:,candidate,None]
        lower[d]=gaps.min(axis=0);upper[d]=gaps.max(axis=0)
        argmin.append(gaps.argmin(axis=0));argmax.append(gaps.argmax(axis=0))
    fun=radius_exact if exact else radius_float
    lo=[fun(lower[:,j],w0) for j in range(len(rivals))]
    up=[fun(upper[:,j],w0) for j in range(len(rivals))]
    key=lambda r: math.inf if r is None else float(r)
    return dict(lower=min(lo,key=key),upper_relaxation=min(up,key=key),rivals=rivals,
                lower_by_rival=lo,upper_by_rival=up,lower_gaps=lower,upper_gaps=upper,
                argmin=np.asarray(argmin),argmax=np.asarray(argmax))


def enumerate_envelope(patterns, candidate, exact=False, w0=None, max_states=1000000):
    count=math.prod(len(p) for p in patterns)
    if count>max_states:raise ValueError(f'Enumeration guard: {count} states exceeds {max_states}')
    key=lambda r: math.inf if r is None else float(r)
    lo,hi=None,None;lo_idx=hi_idx=None;attained=set()
    for idx in product(*(range(len(p)) for p in patterns)):
        z=np.array([p[k] for p,k in zip(patterns,idx)])
        r=winner_radius(z,candidate,exact,w0)
        attained.add(r)
        if lo_idx is None or key(r)<key(lo):lo,lo_idx=r,idx
        if hi_idx is None or key(r)>key(hi):hi,hi_idx=r,idx
    return dict(lower=lo,upper=hi,lower_indices=lo_idx,upper_indices=hi_idx,states=count,attained=attained)
