#!/usr/bin/env python3
"""Regression checks for the maintainer-only real-world use-case library."""
from pathlib import Path
import json,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'qualification/use-cases'
LIB=json.loads((BASE/'library.json').read_text())


def req(cond,msg):
    if not cond:raise AssertionError(msg)


def main():
    cases=LIB.get('cases',[]);req(len(cases)>=30,'real-world library is unexpectedly small')
    ids=[c.get('id') for c in cases];req(len(ids)==len(set(ids)),'duplicate use-case ids')
    required_industries={'b2b-saas','local-services','ecommerce','creator-media','professional-services'}
    industries={c.get('industry') for c in cases};req(required_industries<=industries,f'missing representative industries: {required_industries-industries}')
    required_domains={'core','customer-intelligence','competitor-intelligence','industry-intelligence','seo-aeo','content-synthesis','marketing-synthesis','customer-optimization'}
    domains={d for c in cases for d in c.get('domains',[])};req(required_domains<=domains,f'missing operating-area coverage: {required_domains-domains}')
    kinds={c.get('kind') for c in cases};req({'composed','cross-domain','longitudinal'}<=kinds,'use-case library lost composition/cross-domain/longitudinal coverage')
    forbidden=('qualification rubric','qualification score','qualification checkpoint','qualification receipt','target workflow','judge criteria')
    longitudinal=0
    for c in cases:
        fixture=ROOT/'qualification/fixtures'/f"{c['fixture']}.json";req(fixture.is_file(),f"missing fixture for {c['id']}: {fixture.name}")
        pairs=c.get('stages') or [c]
        if c.get('stages'):longitudinal+=1
        for p in pairs:
            for key in ('request','judge'):
                path=BASE/p[key];req(path.is_file(),f"missing {key} for {c['id']}: {p[key]}")
            request=(BASE/p['request']).read_text(encoding='utf-8').strip();req(request,f"empty request: {c['id']}")
            lower=request.lower();req(not any(x in lower for x in forbidden),f"candidate request leaks evaluator framing: {c['id']}")
            judge=(BASE/p['judge']).read_text(encoding='utf-8');req('Expected business outcome' in judge,f"judge guidance lacks outcome framing: {c['id']}")
    req(longitudinal>=2,'need at least two longitudinal/change-oriented cases')
    p=subprocess.run([sys.executable,str(ROOT/'qualification/use_case_coverage.py')],cwd=ROOT,capture_output=True,text=True)
    req(p.returncode==0,f'use-case coverage validation failed:\n{p.stdout}\n{p.stderr}')
    summary=json.loads(p.stdout);req(summary['use_cases']==len(cases),'coverage helper case count mismatch');req(summary['domain_count']>=8,'coverage helper lost domain coverage')
    print(f"real-world use-case library regressions passed: {len(cases)} cases, {len(industries)} industries, {len(domains)} operating areas, blind request/judge separation")

if __name__=='__main__':main()
