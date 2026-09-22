"""Reproduce the mathematical evidence without downloading data or modifying R3.

Default: regenerate row patterns, endpoint bounds, exact upper obstruction,
independent tests, and final sharp-envelope summary. The stored RealMLP endpoint
is a mathematical witness and is independently checked; no solver is required to
rediscover the witness. --rediscover runs its mixed-integer search as well.
"""
from pathlib import Path
import subprocess,sys,argparse,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--rediscover',action='store_true');args=p.parse_args()
expected={'primary11__all__rank__equal__normalized_matrix.csv':'dae0f073833ee9200767a83c42221b023a2753300aed63df02c5e71a427d5167',
          'coverage9__all__rank__equal__normalized_matrix.csv':'134b7004ca17a69bb1bf35fd5d19b45ca8794de8a337fc7b40ebbdcd3d857393'}
for fn,sha in expected.items():
    got=hashlib.sha256((ROOT/'data'/fn).read_bytes()).hexdigest()
    if got!=sha:raise RuntimeError('Input hash mismatch: '+fn)
scripts=['run_released_evidence.py']
if args.rediscover:scripts.append('refine_realmlp.py')
scripts+=['exact_realmlp_obstruction.py','validation.py','finalize_results.py']
for script in scripts:
    print('RUN',script,flush=True)
    with (ROOT/'qa'/('replay_'+script+'.log')).open('w') as log:
        subprocess.run([sys.executable,str(ROOT/'code'/script)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
print('PASS: exact endpoint certificates, compatible witnesses, and independent numerical checks.')
