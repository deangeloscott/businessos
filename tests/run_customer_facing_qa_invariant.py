#!/usr/bin/env python3
"""Ensure customer-facing production preserves substantive QA without Run orchestration."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from _common import read_frontmatter


def req(condition,message):
    if not condition:raise AssertionError(message)


def load(rel):
    path=ROOT/rel;meta,body=read_frontmatter(path);return path,meta,body


def main():
    pre_path,pre_meta,pre_body=load('systems/content-synthesis/contracts/qa/pre-publish/CONTEXT.md')
    req(pre_meta.get('id')=='content.qa.pre-publish','shared Content pre-publish QA playbook is missing')
    req('actual final artifact' in pre_body.lower(),'pre-publish QA must inspect the real rendered/final artifact')
    req('claim_surface_ref' in pre_body,'opaque/rendered QA lost claim-surface verification')
    req('accessibility' in pre_body.lower(),'pre-publish QA lost accessibility checks')
    req('run/work receipt is optional' in pre_body.lower(),'pre-publish QA became Run-dependent again')

    # Article explicitly composes shared final QA as useful operating knowledge, but the
    # body makes clear the subprocess list is not an execution ledger.
    _,article_meta,article_body=load('systems/content-synthesis/contracts/production/article/CONTEXT.md')
    required=[x.get('id') if isinstance(x,dict) else x for x in ((article_meta.get('subcontracts') or {}).get('required') or [])]
    req(required.count('content.qa.pre-publish')==1,f'article should reference shared pre-publish QA once: {required}')
    req('subcontract-completion ledger are optional' in article_body.lower(),'article composition was turned back into mandatory Run conformance')

    # Native visual methods may perform their relevant final inspection directly rather
    # than being forced through one universal QA subprocess.
    _,image_meta,image_body=load('systems/content-synthesis/contracts/production/image/CONTEXT.md')
    req(image_meta.get('artifact_role')=='customer_facing_production_root','image production lost customer-facing root role')
    for phrase in ('inspect final image','visual errors','legibility','accessibility'):
        req(phrase in image_body.lower(),f'image production lost native final QA: {phrase}')

    _,info_meta,info_body=load('systems/content-synthesis/contracts/production/infographic/CONTEXT.md')
    req(info_meta.get('artifact_role')=='customer_facing_production_root','infographic production lost customer-facing root role')
    for phrase in ('inspect the actual final visual','legibility','factual fidelity','accessibility'):
        req(phrase in info_body.lower(),f'infographic production lost native final QA: {phrase}')
    req('manual action package' not in info_body.lower(),'infographic recreated retired capability fallback')

    # Marketing keeps the same substantive separation without inheriting Content's internal
    # composition list or a Run-level QA gate.
    _,landing_meta,landing_body=load('systems/marketing-synthesis/contracts/landing-page/qa/CONTEXT.md')
    req(landing_meta.get('id')=='marketing.landing-page.qa','landing-page QA playbook missing')
    for phrase in ('actual available artifact','claim policy','accessibility','no run is required'):
        req(phrase in landing_body.lower(),f'landing-page QA lost substantive boundary: {phrase}')

    for retired in ('scripts/record_contract_completion.py','scripts/finalize_run.py','scripts/complete_sop_run.py'):
        req(not (ROOT/retired).exists(),f'QA invariant recreated Run orchestration helper: {retired}')

    print('customer-facing QA regressions passed: substantive artifact QA remains strong without Run execution orchestration')


if __name__=='__main__':main()
