#!/usr/bin/env python3
from _common import *
import hashlib, os, shutil, subprocess, sys, zipfile

env=dict(os.environ)
env['PYTHONDONTWRITEBYTECODE']='1'

def run(path):
    subprocess.run([sys.executable, str(ROOT/path)], check=True, env=env)

run('scripts/generate_registry.py')
run('scripts/validate_workspace.py')
run('scripts/validate_public_distribution.py')
run('tests/run_all.py')

# Remove transient test/runtime artifacts and bytecode before packaging.
for rel in ['instances/init-test-business','instances/_context-resolution','instances/context-resolution-test']:
    p=ROOT/rel
    if p.exists(): shutil.rmtree(p)
for p in ROOT.rglob('__pycache__'):
    shutil.rmtree(p, ignore_errors=True)
for p in ROOT.rglob('*.pyc'):
    p.unlink(missing_ok=True)

# Refresh generated files after cleanup so the packaged manifest describes the package.
run('scripts/generate_registry.py')
run('scripts/validate_workspace.py')
run('scripts/validate_public_distribution.py')

out=ROOT.parent/(ROOT.name+'.zip')
if out.exists(): out.unlink()
shutil.make_archive(str(out.with_suffix('')), 'zip', ROOT.parent, ROOT.name)

with zipfile.ZipFile(out) as zf:
    bad=zf.testzip()
    if bad:
        raise SystemExit(f'ZIP integrity failed at {bad}')

digest=hashlib.sha256(out.read_bytes()).hexdigest()
sha=out.with_suffix(out.suffix+'.sha256')
sha.write_text(f'{digest}  {out.name}\n')
print(out)
print(sha)
print('sha256', digest)
print('zip integrity passed')
