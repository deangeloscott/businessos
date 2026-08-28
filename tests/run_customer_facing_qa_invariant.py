#!/usr/bin/env python3
"""Ensure customer-facing Content production cannot silently skip pre-publish QA."""
from pathlib import Path
import json, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'scripts'
BID='customer-facing-qa-invariant'
BASE=ROOT/'instances'/BID
RUNS=ROOT/'runtime'/'runs'/BID


def req(condition,message):
    if not condition: raise AssertionError(message)


def create_manifest(contract_id):
    p=subprocess.run(
        [sys.executable,str(S/'create_run.py'),BID,contract_id,'customer-facing QA invariant regression'],
        cwd=ROOT,capture_output=True,text=True
    )
    req(p.returncode==0,f'create_run failed for {contract_id}: {p.stderr+ p.stdout}')
    rid=p.stdout.strip().splitlines()[-1]
    path=RUNS/rid/'contract-execution.json'
    req(path.exists(),f'{contract_id} did not create contract-execution manifest')
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    for path in (BASE,RUNS):
        if path.exists(): shutil.rmtree(path)
    try:
        p=subprocess.run([sys.executable,str(S/'init_business.py'),BID,'--name','Customer-facing QA Invariant'],cwd=ROOT,capture_output=True,text=True)
        req(p.returncode==0,f'init failed: {p.stderr+p.stdout}')

        # Media roots that historically described QA only in prose must now receive
        # the shared Content pre-publish QA requirement in their Run manifest.
        for cid in ('content.production.infographic','content.production.image'):
            manifest=create_manifest(cid)
            required=manifest.get('required_subcontracts') or []
            req('content.qa.pre-publish' in required,f'{cid} did not inherit content.qa.pre-publish: {required}')
            req('content.qa.pre-publish' in (manifest.get('contracts') or {}),f'{cid} QA subcontract was not initialized')

        # Contracts that already declared pre-publish QA must not receive duplicates.
        article=create_manifest('content.production.article')
        required=article.get('required_subcontracts') or []
        req(required.count('content.qa.pre-publish')==1,f'article duplicated pre-publish QA: {required}')

        # Keep the invariant scoped to Content Synthesis. Marketing owns its own QA.
        landing=create_manifest('marketing.assets.landing-page')
        required=landing.get('required_subcontracts') or []
        req('marketing.landing-page.qa' in required,'marketing landing page lost its domain QA subcontract')
        req('content.qa.pre-publish' not in required,f'Content QA leaked into Marketing run: {required}')

        print('customer-facing Content pre-publish QA invariant regressions passed')
    finally:
        for path in (BASE,RUNS):
            if path.exists(): shutil.rmtree(path)


if __name__=='__main__': main()
