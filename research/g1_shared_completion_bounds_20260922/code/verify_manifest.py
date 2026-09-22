"""Verify file integrity relative to the package root."""
from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parents[1];fail=[];n=0
for line in (root/'SHA256SUMS.txt').read_text().splitlines():
    sha,name=line.split('  ',1);p=root/name;n+=1
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:fail.append(name)
if fail:raise SystemExit('FAIL: '+', '.join(fail))
print(f'PASS: {n}/{n} files match SHA-256 manifest.')
