#!/usr/bin/env python3
"""Dependency-free verifier for CERT-Bench global feasible-winner witnesses.

Reads only released CSV matrices/weights and JSONL witness records. It does not
import the analysis implementation and does not solve an optimization problem.
"""
from __future__ import annotations
import csv, hashlib, json, math, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
WIT=ROOT/'witnesses'/'TABARENA_GLOBAL_FEASIBLE_WINNER_WITNESSES.jsonl'
OUT=ROOT/'qa'/'STANDALONE_GLOBAL_WINNER_VERIFIER_RESULTS.csv'
SUMMARY=ROOT/'qa'/'STANDALONE_GLOBAL_WINNER_VERIFIER_SUMMARY.json'

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for ch in iter(lambda:f.read(1024*1024),b''): h.update(ch)
    return h.hexdigest()

def read_matrix(path):
    with open(path,newline='',encoding='utf-8-sig') as f:
        r=csv.reader(f); header=next(r); methods=header[1:]; tasks=[]; z=[]
        for row in r:
            tasks.append(row[0]); z.append([float(x) for x in row[1:]])
    return tasks,methods,z

def read_weights(path):
    with open(path,newline='',encoding='utf-8-sig') as f:
        r=csv.DictReader(f); rows=list(r)
    return [x['task'] for x in rows],[float(x['nominal_weight']) for x in rows]

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def max0(xs): return max([0.0]+list(xs))

def verify(rec):
    matrix_path=ROOT/rec['normalized_matrix_file']; weights_path=ROOT/rec['nominal_weights_file']
    if not rec.get('feasible'):
        hash_ok=(sha256(matrix_path)==rec['normalized_matrix_sha256'] and sha256(weights_path)==rec['nominal_weights_sha256'])
        tasks,methods,z=read_matrix(matrix_path); wt,w0=read_weights(weights_path)
        cert=rec.get('infeasibility_certificate') or {}
        c=int(rec['candidate_index']); j=int(cert.get('dominating_method_index',-1)); tol=float(cert.get('strict_tolerance',1e-12))
        shape_ok=(tasks==rec['task_ids'] and methods==rec['method_ids'] and wt==tasks and 0<=c<len(methods) and 0<=j<len(methods) and c!=j)
        gaps=[row[c]-row[j] for row in z] if shape_ok else []
        min_gap=min(gaps) if gaps else float('-inf')
        passed=(hash_ok and shape_ok and cert.get('type')=='strict_taskwise_dominance' and min_gap>tol)
        return {'candidate_method':rec['candidate_method'],'status':'PASS' if passed else 'FAIL','certificate_type':cert.get('type'),
                'dominating_method':methods[j] if shape_ok else None,'minimum_taskwise_gap':min_gap,'hash_ok':hash_ok,'shape_ok':shape_ok,
                'verification_tolerance':tol}
    hash_ok=(sha256(matrix_path)==rec['normalized_matrix_sha256'] and sha256(weights_path)==rec['nominal_weights_sha256'])
    tasks,methods,z=read_matrix(matrix_path); wt,w0=read_weights(weights_path)
    c=int(rec['candidate_index']); d=len(z); m=len(methods); others=[j for j in range(m) if j!=c]
    w=[float(x) for x in rec['critical_weights']]; u=[float(x) for x in rec['absolute_deviations']]
    alpha=[float(x) for x in rec['dual_alpha']]; beta=[float(x) for x in rec['dual_beta']]
    lam=[float(x) for x in rec['dual_lambdas']]; nu=float(rec['dual_nu']); tol=1e-8
    shape_ok=(tasks==rec['task_ids'] and methods==rec['method_ids'] and wt==tasks and all(len(x)==m for x in z)
              and len(w)==len(u)==len(alpha)==len(beta)==d and len(lam)==len(others))
    h=[[z[i][c]-z[i][j] for j in others] for i in range(d)]
    global_ineq=[sum(h[i][k]*w[i] for i in range(d)) for k in range(len(others))]
    pviol=[]
    for i in range(d): pviol += [-w[i],-u[i],w[i]-u[i]-w0[i],-w[i]-u[i]+w0[i]]
    pviol += global_ineq+[abs(sum(w)-1.0)]
    maxp=max0(pviol)
    dw=[alpha[i]-beta[i]+sum(h[i][k]*lam[k] for k in range(len(others)))-nu for i in range(d)]
    du=[0.5-alpha[i]-beta[i] for i in range(d)]
    dviol=[-x for x in alpha]+[-x for x in beta]+[-x for x in lam]+[-x for x in dw]+[-x for x in du]
    maxd=max0(dviol)
    pobj=0.5*sum(u); dobj=nu+dot(w0,[beta[i]-alpha[i] for i in range(d)])
    stored_p=float(rec['primal_objective']); stored_d=float(rec['dual_objective'])
    objgap=abs(stored_p-stored_d); recalc=max(abs(stored_p-pobj),abs(stored_d-dobj))
    s1=[w0[i]-w[i]+u[i] for i in range(d)]; s2=[w[i]+u[i]-w0[i] for i in range(d)]
    sg=[-x for x in global_ineq]
    comp=[alpha[i]*s1[i] for i in range(d)]+[beta[i]*s2[i] for i in range(d)]\
         +[lam[k]*sg[k] for k in range(len(others))]+[w[i]*dw[i] for i in range(d)]+[u[i]*du[i] for i in range(d)]
    maxcomp=max(abs(x) for x in comp)
    scores=[sum(w[i]*z[i][j] for i in range(d)) for j in range(m)]
    maxwin=max(scores[c]-x for x in scores)
    tv=0.5*sum(abs(w[i]-w0[i]) for i in range(d)); tvgap=abs(tv-float(rec['radius_tv']))
    passed=hash_ok and shape_ok and maxp<=tol and maxd<=tol and objgap<=tol and recalc<=tol and maxcomp<=10*tol and maxwin<=tol and tvgap<=tol
    return {'candidate_method':rec['candidate_method'],'status':'PASS' if passed else 'FAIL','hash_ok':hash_ok,'shape_ok':shape_ok,
            'maximum_primal_violation':maxp,'maximum_dual_violation':maxd,'objective_gap':objgap,
            'objective_recalculation_gap':recalc,'maximum_complementarity_residual':maxcomp,
            'maximum_global_winner_inequality':maxwin,'tv_recalculation_gap':tvgap,'verification_tolerance':tol}

def main():
    records=[json.loads(x) for x in WIT.read_text(encoding='utf-8').splitlines() if x.strip()]
    rows=[verify(r) for r in records]
    keys=[]
    for r in rows:
        for k in r:
            if k not in keys: keys.append(k)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=keys); w.writeheader(); w.writerows(rows)
    finite=[r for r,rec in zip(rows,records) if rec.get('feasible')]
    infeasible=[r for r,rec in zip(rows,records) if not rec.get('feasible')]
    summary={'records':len(rows),'finite_records':len(finite),'infeasible_certificates':len(infeasible),
             'pass':sum(r['status']=='PASS' for r in rows),'fail':sum(r['status']=='FAIL' for r in rows),
             'all_records_verified':all(r['status']=='PASS' for r in rows)}
    SUMMARY.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))
    if summary['fail'] or summary['pass']!=summary['records']: return 1
    return 0
if __name__=='__main__': raise SystemExit(main())
