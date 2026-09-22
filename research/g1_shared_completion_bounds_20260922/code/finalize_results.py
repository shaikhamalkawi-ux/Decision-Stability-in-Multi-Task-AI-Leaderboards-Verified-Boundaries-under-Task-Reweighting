"""Build the final sharp envelopes from validated endpoint certificates.

This never substitutes a candidate-specific pairwise relaxation for an attainable
shared-completion upper bound.
"""
from pathlib import Path
from fractions import Fraction as F
import pandas as pd,numpy as np,json,hashlib,shutil
from completion_bounds import winner_radius
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
screen=pd.read_csv(R/'initial_screening_envelopes.csv',keep_default_na=False)
obstruction=json.loads((R/'realmlp_exact_obstruction.json').read_text())
assert obstruction['status']=='PASS_EXACT_INTEGER_ARITHMETIC'
assert obstruction['radius_upper_exact']=='55/2414'
assert json.loads((ROOT/'qa/VALIDATION_REPORT.json').read_text())['status']=='PASS'
rows=[]
for i,r in screen.iterrows():
    real=r['candidate']=='TA-REALMLP (tuned + ensemble)'
    file='realmlp_joint_best_rank.csv' if real else f'completion_{i:02d}_upper_feasible_rank.csv'
    z=pd.read_csv(R/file,index_col=0)
    actual=winner_radius(np.rint(z.values*20)/20,i,exact=True)
    upper=F(55,2414) if real else F(r['upper_relaxation_exact'])
    assert actual==upper
    assert r['lower_radius_exact'] in ['0','0.0',0]
    rows.append(dict(candidate=r['candidate'],lower_exact='0',upper_exact=str(upper),
                     lower=0.,upper=float(upper),pairwise_upper_relaxation_exact=r['upper_relaxation_exact'],
                     upper_certificate='exact integer DP plus endpoint witness' if real else 'pairwise upper bound attained by shared completion',
                     upper_witness=file,lower_witness=f'completion_{i:02d}_lower_rank.csv',
                     can_be_unique_nominal_winner=bool(upper>0)))
pd.DataFrame(rows).to_csv(R/'FINAL_SHARP_ENVELOPES.csv',index=False)
summary={'status':'PASS_SHARP_ENDPOINTS_FOR_DECLARED_COARSENED_ORDINAL_EVIDENCE',
 'R3_changed':False,'original_full_raw_missingness_validation':'HOLD_NOT_EXECUTED',
 'complete_tasks':122,'partial_tasks':20,'full_task_scope':142,'candidate_scope':11,
 'unspecified_positions_in_this_evidence_representation':40,
 'original_raw_missing_cell_count':'NOT_ASSERTED',
 'completion_count_exact':str(381**20),'retained_ordinal_relations':7430,
 'scope_note':'Preserves full 11-model ranks on 122 tasks and relative nine-model ranks on 20 additional tasks. The two unspecified model positions on those 20 tasks are a declared evidence coarsening, not an assertion about which original raw scores were missing.',
 'sharp_candidate_envelopes':rows,
 'shared_completion_incompatibility':{'candidate':'RealMLP','relaxed_upper_exact':'69/2698',
    'sharp_upper_exact':'55/2414','absolute_overstatement_exact':str(F(69,2698)-F(55,2414)),
    'relative_overstatement_exact':str(F(69,2698)/F(55,2414)-1),
    'relative_overstatement_percent':float(100*(F(69,2698)/F(55,2414)-1))},
 'novelty_status':'CANDIDATE_CONTRIBUTION; no first-in-literature claim; foundational components acknowledged',
 'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'data').glob('*.csv')}}
(R/'FINAL_RESULT_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['sharp_candidate_envelopes']},indent=2))
