"""Self-contained exact replay for the two synthetic certificate-obstruction results.

Uses only Python's standard library and exact fractions. It does not read TabArena
or any third-party benchmark data.
"""
from fractions import Fraction as F
from itertools import combinations
import json

EPS = F(13, 400)
P4 = (F(21,68), F(21,68), F(21,68), F(5,68))
U = ((6,0,2,4),(6,2,0,4),(6,1,1,4),(6,0,3,3),(6,3,0,3),(6,2,2,2))
K2=(0,2,4,6); K3=(3,6,3,0); K4=(0,4,4,4)
KNOWN=(K2,K3,K4)

def dot(a,b):
    return sum((x*y for x,y in zip(a,b)), F(0))

def support_untruncated(coeffs, p=P4, eps=EPS):
    coeffs=tuple(F(x) for x in coeffs)
    return dot(coeffs,p)+eps*(max(coeffs)-min(coeffs))

def weak_compositions(total, parts):
    for bars in combinations(range(total+parts-1), parts-1):
        bounds=(-1,)+bars+(total+parts-1,)
        yield tuple(bounds[i+1]-bounds[i]-1 for i in range(parts))

def tv_support_levels(level_mass, eps=EPS):
    levels={F(c):F(m) for c,m in level_mass.items() if m}
    base=sum((c*m for c,m in levels.items()),F(0))
    high=max(levels); rem=F(eps); val=base
    for c in sorted(levels):
        if c==high or rem==0: break
        moved=min(rem,levels[c])
        val += moved*(high-c); rem -= moved
    return val

def support_uniform68(rows, counts, candidate, rival):
    levels={}
    for row,n in zip(rows,counts):
        if not n: continue
        c=F(row[candidate]-row[rival],6)
        levels[c]=levels.get(c,F(0))+F(n,68)
    return tv_support_levels(levels)

def four_task_check():
    rows_known=tuple(tuple(F(x,6) for x in r) for r in KNOWN)
    for ur in U:
        rows=(tuple(F(x,6) for x in ur),)+rows_known
        supports={}
        for i in range(4):
            for j in range(4):
                if i!=j:
                    supports[(i,j)]=support_untruncated([row[i]-row[j] for row in rows])
        possible=[i for i in range(4) if all(supports[(i,j)]<=0 for j in range(4) if j!=i)]
        assert not possible, (ur,possible)
    avg=tuple(F(a+b,12) for a,b in zip(U[0],U[5]))
    rows=(avg,)+rows_known
    obs=[support_untruncated([row[0]-row[j] for row in rows]) for j in (1,2,3)]
    expected=(F(-11,40800),F(-29,5100),F(-11,40800))
    assert tuple(obs)==expected,(obs,expected)
    return {"legal_rank_patterns":6,"average_A_supports":[str(x) for x in obs]}

def uniform68_check():
    rows=U+(K2,K3,K4)
    state_count=pair_checks=semantic=0
    for counts6 in weak_compositions(21,6):
        counts=counts6+(21,21,5); supports={}
        for i in range(4):
            for j in range(4):
                if i!=j:
                    supports[(i,j)]=support_uniform68(rows,counts,i,j); pair_checks+=1
        possible=[i for i in range(4) if all(supports[(i,j)]<=0 for j in range(4) if j!=i)]
        assert not possible,(counts6,possible)
        semantic+=1; state_count+=1
    assert (state_count,pair_checks,semantic)==(65780,789360,65780)

    avg=tuple(F(a+b,12) for a,b in zip(U[0],U[5]))
    block_rows=(avg,tuple(F(x,6) for x in K2),tuple(F(x,6) for x in K3),tuple(F(x,6) for x in K4))
    block_counts=(21,21,21,5); supports=[]
    for j in (1,2,3):
        levels={}
        for row,n in zip(block_rows,block_counts):
            c=row[0]-row[j]
            levels[c]=levels.get(c,F(0))+F(n,68)
        supports.append(tv_support_levels(levels))
    expected=(F(-11,40800),F(-29,5100),F(-11,40800))
    assert tuple(supports)==expected,(supports,expected)

    h=[(6,4,2),(4,6,2),(5,5,2),(6,3,3),(3,6,3),(4,4,4)]
    exceptional=0
    for mask in range(1,64):
        ids=[i for i in range(6) if mask>>i & 1]
        maxs=[max(h[i][k] for i in ids) for k in range(3)]
        msum=maxs[0]+maxs[1]+max(maxs[2],3)
        if msum<14:
            S=set(ids)
            assert (S <= {0,3}) or (S <= {1,4}) or S=={2} or S=={5}
            exceptional+=1
    assert exceptional==8
    return {"states":state_count,"ordered_pair_supports":pair_checks,
            "semantic_no_common_weak":semantic,"type_subsets":63,
            "exceptional_type_subsets":exceptional,
            "average_A_supports":[str(x) for x in supports]}

if __name__=="__main__":
    print(json.dumps({"four_task":four_task_check(),"uniform68":uniform68_check()},indent=2,sort_keys=True))
