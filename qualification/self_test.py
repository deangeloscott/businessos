#!/usr/bin/env python3
"""Maintainer-only self-test for the qualification/evaluator harness.

This does not test whether AURA is a good product and is not part of the AURA
product-integrity gate. It only checks that the blind evaluator, recovery,
integrity, and staged-product observation machinery are trustworthy enough to
use when running real-work qualification.
"""
from pathlib import Path
import os,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONUTF8']='1'
SELF_TESTS=[
    'tests/run_qualification_framework.py',
    'tests/run_qualification_resume.py',
    'tests/run_qualification_integrity.py',
    'tests/run_qualification_product_integrity.py',
]

failures=[]
for rel in SELF_TESTS:
    print(f'== {rel} ==',flush=True)
    completed=subprocess.run([sys.executable,str(ROOT/rel)],cwd=ROOT,env=env)
    if completed.returncode!=0:failures.append((rel,completed.returncode))

if failures:
    print(f'\nqualification harness self-test failed: {len(failures)}/{len(SELF_TESTS)} suites failed')
    for rel,code in failures:print(f'- {rel} (exit {code})')
    raise SystemExit(1)

print(f'qualification harness self-test passed: {len(SELF_TESTS)} suites')
