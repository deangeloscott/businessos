#!/usr/bin/env python3
from pathlib import Path
import json, os, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'qualification'))
from common import product_snapshot, read_json
from evaluate_run import qualification_status, staged_product_integrity_flags


def req(cond,msg):
    if not cond: raise AssertionError(msg)


def main():
    with tempfile.TemporaryDirectory(prefix='aura-product-integrity-') as td:
        root=Path(td)
        prep=subprocess.run([
            sys.executable,str(ROOT/'qualification/prepare_run.py'),
            '--profile','atomic','--domain','core','--run-root',str(root),'--run-id','product-integrity-smoke'
        ],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        req(prep.returncode==0,f'qualification preparation failed:\n{prep.stdout}\n{prep.stderr}')
        rd=root/'product-integrity-smoke'; run=read_json(rd/'run.json'); product=Path(run['product_root'])
        baseline=read_json(rd/'evaluator/product-snapshot.json')
        req(isinstance(baseline,dict) and baseline.get('digest'),'prepared qualification must persist staged product snapshot')
        req(run.get('product_snapshot_digest')==baseline.get('digest'),'run metadata must bind the staged product snapshot digest')
        req(run.get('qualification_status')=='NOT_EVALUATED','prepared queue must not imply qualification success')
        instructions=(rd/'candidate/RUN-INSTRUCTIONS.md').read_text(encoding='utf-8')
        req('staged AURA product' in instructions and 'immutable' in instructions,'candidate instructions must make staged product immutability explicit')
        req('not a qualification pass' in instructions.lower() and 'only the independent evaluator' in instructions.lower(),'candidate instructions must distinguish queue completion from qualification success')
        req(not staged_product_integrity_flags(rd,product,run),'untouched staged product must pass product-integrity check')

        transient=product/'__pycache__'/'scratch.cpython-313.pyc'; transient.parent.mkdir(); transient.write_bytes(b'transient')
        ds=product/'.DS_Store'; ds.write_bytes(b'transient')
        req(not staged_product_integrity_flags(rd,product,run),'ignored interpreter/editor transients must not invalidate qualification')

        helper=product/'run_all_events.py'; helper.write_text("print('private qualification solver')\n",encoding='utf-8')
        flags=staged_product_integrity_flags(rd,product,run)
        mutation=next((x for x in flags if x.get('type')=='staged_product_mutation'),None)
        req(mutation and 'run_all_events.py' in mutation.get('created',[]),f'candidate-created product helper must be a critical product mutation: {flags}')
        helper.unlink()
        req(not staged_product_integrity_flags(rd,product,run),'restoring exact staged product should clear current-state mutation flag')

        target=product/'README.md'; original=target.read_text(encoding='utf-8'); target.write_text(original+'\nqualification mutation\n',encoding='utf-8')
        flags=staged_product_integrity_flags(rd,product,run)
        mutation=next((x for x in flags if x.get('type')=='staged_product_mutation'),None)
        req(mutation and 'README.md' in mutation.get('modified',[]),'modified staged source must fail product integrity')
        target.write_text(original,encoding='utf-8')

        target.unlink(); flags=staged_product_integrity_flags(rd,product,run)
        mutation=next((x for x in flags if x.get('type')=='staged_product_mutation'),None)
        req(mutation and 'README.md' in mutation.get('deleted',[]),'deleted staged source must fail product integrity')

        run_bad={**run,'product_snapshot_digest':'tampered'}
        mismatch=staged_product_integrity_flags(rd,product,run_bad)
        req(mismatch and mismatch[0].get('type')=='product_integrity_baseline_mismatch','run metadata snapshot tampering must fail integrity')

        snapshot_path=rd/'evaluator/product-snapshot.json'; saved=snapshot_path.read_text(encoding='utf-8'); snapshot_path.unlink()
        missing=staged_product_integrity_flags(rd,product,run)
        req(missing and missing[0].get('type')=='product_integrity_baseline_missing','missing product integrity baseline must fail closed')
        snapshot_path.write_text(saved,encoding='utf-8')

    req(qualification_status({'FAIL':1})=='FAILED','any evaluator FAIL must set qualification status FAILED')
    req(qualification_status({'HARD-PASS / REVIEW-PENDING':2})=='REVIEW_REQUIRED','hard-pass without professional review must not be called qualified')
    req(qualification_status({'BLOCKED-EXTERNAL':1})=='INCOMPLETE','blocked qualification must be incomplete')
    req(qualification_status({'ACCEPTABLE':2,'COMPETITIVE':1,'EXCEPTIONAL':1})=='QUALIFIED','only fully reviewed acceptable-or-better events may be qualified')
    print('qualification staged-product integrity regressions passed')

if __name__=='__main__': main()
