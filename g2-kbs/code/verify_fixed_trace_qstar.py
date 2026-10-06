#!/usr/bin/env python3
"""Verify exact fixed-trace decision points from accepted Phase-2/6/8 summaries.

For a successful Phase-8 trace:
- Q-1 has an explicit opposite-answer completion pair, so the decision predicate is
  not constant on X(h_{Q-1}). The same pair is compatible with every earlier prefix.
- Q is a checked Phase-2/6 preference_dependence certificate, so the decision predicate
  is constant and equal to 1 on X(h_Q), subject to the original mean-enclosure and
  finite-canonical-target qualifications.
Therefore q* = Q along that fixed disclosure trace.
"""
from __future__ import annotations
import argparse, json, pathlib, hashlib
import pandas as pd

def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--phase2-fold-runs',required=True)
    ap.add_argument('--phase6-trace-summary',required=True)
    ap.add_argument('--phase8-trace-summary',required=True)
    ap.add_argument('--output-csv',required=True)
    args=ap.parse_args()
    p2=pathlib.Path(args.phase2_fold_runs)
    p6=pathlib.Path(args.phase6_trace_summary)
    p8=pathlib.Path(args.phase8_trace_summary)
    df2=pd.read_csv(p2)
    rows6=json.loads(p6.read_text())
    rows8=json.loads(p8.read_text())
    map6={(r['seed'],r['policy'],float(r['task_mass_units'])):r for r in rows6}
    records=[]
    for r in rows8:
        key=(r['seed'],r['policy'],float(r['units']))
        m=df2[(df2.seed==r['seed'])&(df2.policy==r['policy'])&
              (df2.task_mass_units==float(r['units']))]
        if len(m)!=1:
            raise RuntimeError(f'Phase-2 identity count !=1 for {key}: {len(m)}')
        m=m.iloc[0]
        s6=map6.get(key)
        if s6 is None:
            raise RuntimeError(f'Missing Phase-6 trace for {key}')
        identity_ok=(
            int(m.fold_vectors_used)==r['Q'] and
            m.status=='preference_dependence' and
            m.trace_sha256==r['trace_sha256'] and
            s6['Q']==r['Q'] and s6['terminal_reproduced'] and
            s6['trace_sha256']==r['trace_sha256']
        )
        if not identity_ok:
            raise RuntimeError(f'Q-certificate identity mismatch for {key}')
        qstar=(
            r['status']=='SUCCESS' and r['fixed_trace_ambiguity_witness'] and
            r['conditional_fixed_trace_Q_lower_upper_match']
        )
        records.append({
            'seed':r['seed'],'policy':r['policy'],'tv_radius':f"{r['units']}/51",
            'Q':r['Q'],'Q_minus_1':r['q'],'qstar_equals_Q':bool(qstar),
            'trace_sha256':r['trace_sha256'],
            'Q_minus_1_prefix_sha256':r['prefix_sha256']
        })
    out=pd.DataFrame(records)
    out.to_csv(args.output_csv,index=False)
    count=int(out.qstar_equals_Q.sum())
    if count!=47:
        raise RuntimeError(f'Expected 47 exact fixed-trace decision points, found {count}')
    print(json.dumps({
        'status':'PASS','records':len(out),'qstar_equals_Q':count,
        'phase2_sha256':sha(p2),'phase6_sha256':sha(p6),'phase8_sha256':sha(p8)
    },indent=2))

if __name__=='__main__':
    main()
