"""Independent, deterministic checks for the contribution gate.

Uses direct integer-label weak-order enumeration (not the insertion generator),
fresh primal linear programs, and full small-state completion enumeration.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import math,json,sys,platform
import numpy as np
import pandas as pd
from scipy.optimize import linprog
import scipy
from completion_bounds import (rank_patterns,radius_exact,radius_lp,enumerate_envelope,
                               extremal_gap_bounds,winner_radius)
from joint_completion_milp import solve_joint_margin
ROOT=Path(__file__).resolve().parents[1]


def independent_patterns(obs,allow_ties=True):
    obs=np.asarray(obs,float);m=len(obs);known=np.flatnonzero(np.isfinite(obs));out=set()
    for labels in product(range(m),repeat=m):
        x=np.array(labels)
        if not np.array_equal(np.sign(x[known,None]-x[None,known]),
                              np.sign(obs[known,None]-obs[None,known])): continue
        if not allow_ties:
            bad=False
            for a in range(m):
                for b in range(a):
                    if x[a]==x[b] and (a not in known or b not in known):bad=True
            if bad:continue
        # Twice the zero-based average rank is an integer.
        ranks=tuple(int(2*sum(x<x[j])+sum(x==x[j])-1) for j in range(m))
        out.add(ranks)
    return out


def support_lp(g,eps,w0):
    g=np.asarray(g,float);w0=np.asarray(w0,float);d=len(g)
    A=np.block([[np.eye(d),-np.eye(d)],[-np.eye(d),-np.eye(d)]])
    A=np.vstack([A,np.r_[np.zeros(d),np.ones(d)]])
    b=np.r_[w0,-w0,2*eps]
    eq=np.r_[np.ones(d),np.zeros(d)][None,:]
    r=linprog(np.r_[g,np.zeros(d)],A_ub=A,b_ub=b,A_eq=eq,b_eq=[1],bounds=(0,None),method='highs')
    assert r.success,r.message
    return float(r.fun)


def direct_joint_margin(pats,i,eps,w0):
    best=-np.inf
    for inds in product(*(range(len(p)) for p in pats)):
        z=np.array([p[k] for p,k in zip(pats,inds)])
        val=min(support_lp(z[:,j]-z[:,i],eps,w0) for j in range(z.shape[1]) if j!=i)
        best=max(best,val)
    return best


def clipped_uniform_support_integer(a,eps):
    a=list(map(int,a));d=len(a);m=min(a);t=d*eps
    # This expression is valid also at epsilon=0 or 1; cutoffs cover all gaps.
    return max(F(sum(min(x,v) for x in a))-t*(v-m) for v in range(m,max(a)+1))/d


def main():
    rng=np.random.default_rng(220926)
    result={'status':'RUNNING','seed':220926,'python':sys.version.split()[0],
            'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__,
            'platform':platform.platform(),'tests':{}}
    # Independent rank completions, including observed ties, no observations,
    # and insertions on both sides of the observed order.
    profiles=[np.full(m,np.nan) for m in [2,3,4,5]]
    for m in [3,4]:
        for _ in range(15):
            obs=rng.integers(0,3,m).astype(float)
            obs[rng.random(m)<.5]=np.nan;profiles.append(obs)
    checks=0
    for obs in profiles:
        for ties in [True,False]:
            got={tuple(v) for v in np.rint(rank_patterns(obs,ties)*2*(len(obs)-1)).astype(int)}
            wanted=independent_patterns(obs,ties)
            assert got==wanted,(obs,ties,len(got),len(wanted))
            checks+=1
    result['tests']['rank_pattern_generator']={'cases':checks,'pass':checks,
         'method':'independent integer-label weak-order enumeration'}
    # Pairwise transfer tested against fresh primal LPs, including nonuniform
    # weights, zero weights, ties, already-lost candidates and infeasibility.
    errors=[];ninf=0
    for _ in range(400):
        d=int(rng.integers(2,15));g=rng.integers(-5,6,d)
        if rng.random()<.1:g=abs(g)+1
        u=rng.integers(0,9,d);u[0]+=1;w=[F(int(x),int(sum(u))) for x in u]
        exact=radius_exact(list(g),w);value,_=radius_lp(g,[float(x) for x in w])
        assert (exact is None)==math.isinf(value)
        if exact is None:ninf+=1
        else:errors.append(abs(float(exact)-value));assert errors[-1]<1e-9
    result['tests']['rational_pairwise_vs_primal_lp']={'cases':400,'infeasible':ninf,'max_abs_error':max(errors)}
    obs=np.array([[2.,0.,np.nan],[1.,np.nan,0.],[1.,np.nan,2.]])
    pats=[rank_patterns(r) for r in obs]
    b=extremal_gap_bounds(pats,0,exact=True);e=enumerate_envelope(pats,0,exact=True)
    assert e['states']==125 and e['lower']==0 and e['upper']==F(1,5)
    assert b['upper_relaxation']==F(2,9)
    assert e['attained']=={F(0),F(1,15),F(1,6),F(1,5)}
    enum_lp_err=[]
    for idx in product(*(range(len(p)) for p in pats)):
        z=np.array([p[k] for p,k in zip(pats,idx)])
        val=min(radius_lp(z[:,j]-z[:,0])[0] for j in [1,2])
        r=winner_radius(z,0,exact=True)
        enum_lp_err.append(abs(val-float(r)))
    no_tie=enumerate_envelope([rank_patterns(r,False) for r in obs],0,exact=True)
    assert no_tie['upper']==F(1,6)
    cex={'observed_loss_rows':[[2,0,None],[1,None,0],[1,None,2]],
         'candidate':'A','weak_order_completions':125,'lower_exact':'0','upper_exact':'1/5',
         'upper_pairwise_relaxation_exact':'2/9','attainable_radii_exact':['0','1/15','1/6','1/5'],
         'no_new_ties_upper_exact':'1/6','max_lp_enumeration_error':max(enum_lp_err)}
    (ROOT/'results/counterexample_exact.json').write_text(json.dumps(cex,indent=2)+'\n')
    result['tests']['counterexample_complete_enumeration']=cex
    # Lower bound theorem and upper relaxation checked on fresh random complete
    # profiles. All completions are enumerated, not independently paired rivals.
    nprofiles=0
    for rep in range(24):
        d=int(rng.integers(2,5));m=3
        obs=rng.integers(0,4,(d,m)).astype(float)
        for row in obs: row[int(rng.integers(m))]=np.nan
        pp=[rank_patterns(row) for row in obs]
        u=rng.integers(1,6,d);w=[F(int(x),int(sum(u))) for x in u]
        for i in range(m):
            got=extremal_gap_bounds(pp,i,exact=True,w0=w)
            truth=enumerate_envelope(pp,i,exact=True,w0=w)
            key=lambda x:math.inf if x is None else float(x)
            assert got['lower']==truth['lower']
            assert key(got['upper_relaxation'])>=key(truth['upper'])-1e-12
            nprofiles+=1
    result['tests']['sharp_lower_and_relaxed_upper_vs_enumeration']={'candidate_profiles':nprofiles,'pass':nprofiles}
    # Finite-epsilon shared-completion formulation, including positive, zero and
    # negative joint margins. LP relaxation may overstate a realizable completion.
    merr=[];mipchecks=[]
    samples=[pats]
    for _ in range(5):
        rr=rng.integers(0,3,(2,3)).astype(float)
        for row in rr:row[int(rng.integers(3))]=np.nan
        samples.append([rank_patterns(r) for r in rr])
    for k,pp in enumerate(samples):
        d=len(pp);ww=np.arange(1,d+1,dtype=float);ww/=sum(ww)
        for eps in [0.,.12,.3,.8,1.]:
            expected=direct_joint_margin(pp,0,eps,ww)
            info,z,_,_=solve_joint_margin(pp,0,eps,ww,time_limit=30)
            assert info['status']==0,info
            err=abs(info['eta']-expected);assert err<1e-8,(k,eps,info,expected)
            merr.append(err);mipchecks.append({'profile':k,'epsilon':eps,'eta_exact_enumeration_lp':expected,'eta_milp':info['eta']})
    result['tests']['joint_milp_vs_full_completion_enumeration']={'cases':len(merr),'max_abs_error':max(merr)}
    pd.DataFrame(mipchecks).to_csv(ROOT/'qa/joint_formulation_validation.csv',index=False)
    # Clipping identity independently compared with fresh support LPs.
    cerr=[]
    for _ in range(200):
        d=int(rng.integers(2,20));a=rng.integers(-20,21,d)
        ep=F(int(rng.integers(0,101)),100)
        ex=clipped_uniform_support_integer(a,ep)
        lp=support_lp(a,float(ep),np.full(d,1/d))
        cerr.append(abs(float(ex)-lp));assert cerr[-1]<1e-8
    result['tests']['integer_clipping_identity_vs_primal_lp']={'cases':200,'max_abs_error':max(cerr)}
    # Verify real endpoint witnesses preserve every observed ordinal relation,
    # belong to one full ranking on each row, and attain exact claimed radii.
    p=pd.read_csv(ROOT/'data/primary11__all__rank__equal__normalized_matrix.csv',index_col=0)
    q=pd.read_csv(ROOT/'data/coverage9__all__rank__equal__normalized_matrix.csv',index_col=0)
    names=p.columns.tolist();tasks=q.index.tolist();pp=[]
    for task in tasks:
        row=p.loc[task].values if task in p.index else q.loc[task].reindex(names).values
        pp.append(rank_patterns(row))
    werr=[];wsummary=[]
    witnessspec=[('TabPFN-2.6','TA-TABPFN-2.6 (default)','completion_09_upper_feasible_rank.csv',F(96,1207)),
                 ('RealMLP','TA-REALMLP (tuned + ensemble)','realmlp_joint_best_rank.csv',F(55,2414))]
    for label,full,file,claimed in witnessspec:
        zf=pd.read_csv(ROOT/'results'/file,index_col=0);assert list(zf.index)==tasks and list(zf.columns)==names
        z0=zf.values;z=np.rint(z0*20).astype(int)
        assert abs(z0-z/20).max()<1e-10
        for row,patt in zip(z,pp):assert tuple(row) in {tuple(r) for r in np.rint(patt*20).astype(int)}
        i=names.index(full);rad=[]
        for j in range(len(names)):
            if j==i:continue
            rg=radius_exact([F(int(v),20) for v in z[:,j]-z[:,i]])
            lp,ww=radius_lp((z[:,j]-z[:,i])/20.)
            assert rg is not None and abs(float(rg)-lp)<1e-9
            werr.append(abs(float(rg)-lp));rad.append(rg)
            wsummary.append({'candidate':label,'rival':names[j],'exact_radius':str(rg),'lp_radius':lp})
        assert min(rad)==claimed
    pd.DataFrame(wsummary).to_csv(ROOT/'qa/endpoint_witness_independent_lp.csv',index=False)
    result['tests']['real_endpoint_witnesses']={'completions':2,'pairwise_programs':20,'row_membership_checks':284,
                                              'max_abs_error':max(werr),'observed_relations_per_completion':122*55+20*36}
    result['status']='PASS'
    (ROOT/'qa/VALIDATION_REPORT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
