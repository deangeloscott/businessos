#!/usr/bin/env python3
"""Small maintainer view of real-world use-case coverage. Coverage describes observation, never candidate execution requirements."""
from pathlib import Path
import json
from common import ROOT,load_workflows

BASE=ROOT/'qualification/use-cases'
LIB=json.loads((BASE/'library.json').read_text())


def main():
    cases=LIB.get('cases',[]); ids=[c.get('id') for c in cases]
    if len(ids)!=len(set(ids)):raise SystemExit('duplicate use-case id')
    known={w['workflow_id'] for w in load_workflows()}
    industries=set();domains=set();explicit=set();kinds={};missing=[];bad=[]
    for c in cases:
        industries.add(c.get('industry','unknown'));kinds[c.get('kind','unknown')]=kinds.get(c.get('kind','unknown'),0)+1
        domains.update(c.get('domains') or [])
        for wid in c.get('workflows') or []:
            explicit.add(wid)
            if wid not in known:bad.append(f"{c.get('id')}: {wid}")
        stages=c.get('stages') or []
        pairs=stages or [c]
        for p in pairs:
            for key in ('request','judge'):
                rel=p.get(key)
                if rel and not (BASE/rel).is_file():missing.append(f"{c.get('id')}: {rel}")
        fixture=c.get('fixture')
        if fixture and not (ROOT/'qualification/fixtures'/f'{fixture}.json').is_file():missing.append(f"{c.get('id')}: fixture {fixture}")
    if missing:raise SystemExit('missing use-case files:\n- '+'\n- '.join(missing))
    if bad:raise SystemExit('unknown Workflow coverage ids:\n- '+'\n- '.join(bad))
    print(json.dumps({
        'use_cases':len(cases),'industries':sorted(industries),'industry_count':len(industries),
        'kinds':kinds,'domains':sorted(domains),'domain_count':len(domains),
        'explicit_workflows_covered':len(explicit),'authored_workflows':len(known),
        'explicit_workflows_remaining':len(known-explicit)
    },indent=2))

if __name__=='__main__':main()
