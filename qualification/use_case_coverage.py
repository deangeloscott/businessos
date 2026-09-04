#!/usr/bin/env python3
"""Small maintainer view of real-world use-case coverage. Coverage describes observation, never candidate execution requirements."""
from pathlib import Path
import json,re
from common import ROOT,load_workflows

BASE=ROOT/'qualification/use-cases'
LIB=json.loads((BASE/'library.json').read_text())
PLAYBOOK_MAP=json.loads((BASE/'playbook-coverage.json').read_text()).get('coverage',{})


def authored_playbooks():
    text=(ROOT/'PLAYBOOKS.md').read_text(encoding='utf-8')
    return {m.group(1).strip() for m in re.finditer(r'^- \*\*(.+?)\*\* —',text,re.M)}


def main():
    cases=LIB.get('cases',[]);ids=[c.get('id') for c in cases]
    if len(ids)!=len(set(ids)):raise SystemExit('duplicate use-case id')
    case_ids=set(ids);known={w['workflow_id'] for w in load_workflows()};playbooks=authored_playbooks()
    industries=set();domains=set();explicit=set();kinds={};missing=[];bad=[]
    for c in cases:
        industries.add(c.get('industry','unknown'));kinds[c.get('kind','unknown')]=kinds.get(c.get('kind','unknown'),0)+1
        domains.update(c.get('domains') or [])
        for wid in c.get('workflows') or []:
            explicit.add(wid)
            if wid not in known:bad.append(f"{c.get('id')}: {wid}")
        pairs=c.get('stages') or [c]
        for p in pairs:
            for key in ('request','judge'):
                rel=p.get(key)
                if rel and not (BASE/rel).is_file():missing.append(f"{c.get('id')}: {rel}")
        fixture=c.get('fixture')
        if fixture and not (ROOT/'qualification/fixtures'/f'{fixture}.json').is_file():missing.append(f"{c.get('id')}: fixture {fixture}")
    unknown_playbooks=sorted(set(PLAYBOOK_MAP)-playbooks);unmapped=sorted(playbooks-set(PLAYBOOK_MAP));bad_case_refs=[]
    for pb,refs in PLAYBOOK_MAP.items():
        for cid in refs:
            if cid not in case_ids:bad_case_refs.append(f'{pb}: {cid}')
    if missing:raise SystemExit('missing use-case files:\n- '+'\n- '.join(missing))
    if bad:raise SystemExit('unknown Workflow coverage ids:\n- '+'\n- '.join(bad))
    if unknown_playbooks:raise SystemExit('unknown Playbook coverage names:\n- '+'\n- '.join(unknown_playbooks))
    if bad_case_refs:raise SystemExit('Playbook coverage references unknown cases:\n- '+'\n- '.join(bad_case_refs))
    print(json.dumps({
        'use_cases':len(cases),'industries':sorted(industries),'industry_count':len(industries),
        'kinds':kinds,'domains':sorted(domains),'domain_count':len(domains),
        'playbooks_covered':len(playbooks)-len(unmapped),'authored_playbooks':len(playbooks),'playbooks_remaining':len(unmapped),'unmapped_playbooks':unmapped,
        'explicit_workflows_covered':len(explicit),'authored_workflows':len(known),'explicit_workflows_remaining':len(known-explicit)
    },indent=2))

if __name__=='__main__':main()
