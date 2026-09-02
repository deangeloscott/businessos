#!/usr/bin/env python3
"""Ensure customer-facing production preserves substantive QA without execution orchestration."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from _common import read_frontmatter


def req(condition,message):
    if not condition:raise AssertionError(message)

def load(rel):
    path=ROOT/rel;meta,body=read_frontmatter(path);return path,meta,body


def main():
    _,pre_meta,pre_body=load('systems/content-synthesis/contracts/qa/pre-publish/CONTEXT.md')
    req(pre_meta.get('id')=='content.qa.pre-publish' and pre_meta.get('type')=='workflow','shared Content pre-publish QA Workflow is missing')
    req('actual final artifact' in pre_body.lower(),'pre-publish QA must inspect the real rendered/final artifact')
    req('claim_surface_ref' in pre_body,'opaque/rendered QA lost claim-surface verification')
    req('accessibility' in pre_body.lower(),'pre-publish QA lost accessibility checks')
    req('run/work receipt is optional' in pre_body.lower(),'pre-publish QA became Run-dependent again')

    # Article may reuse shared final QA knowledge without turning Workflow composition into
    # an execution ledger or forcing every medium through one universal implementation.
    _,article_meta,article_body=load('systems/content-synthesis/contracts/production/article/CONTEXT.md')
    required=[x.get('id') if isinstance(x,dict) else x for x in ((article_meta.get('workflows') or {}).get('required') or [])]
    req(required.count('content.qa.pre-publish')==1,f'article should reference shared pre-publish QA Workflow once: {required}')
    req('required execution ledger' in article_body.lower(),'article lost explicit non-orchestration boundary')
    req('subcontract' not in article_body.lower(),'article retained retired subcontract vocabulary')

    _,image_meta,image_body=load('systems/content-synthesis/contracts/production/image/CONTEXT.md')
    req(image_meta.get('artifact_role')=='customer_facing_production_root' and image_meta.get('type')=='workflow','image production lost customer-facing Workflow role')
    for phrase in ('inspect final image','visual errors','legibility','accessibility'):
        req(phrase in image_body.lower(),f'image production lost native final QA: {phrase}')

    _,info_meta,info_body=load('systems/content-synthesis/contracts/production/infographic/CONTEXT.md')
    req(info_meta.get('artifact_role')=='customer_facing_production_root' and info_meta.get('type')=='workflow','infographic production lost customer-facing Workflow role')
    for phrase in ('inspect the actual final visual','legibility','factual fidelity','accessibility'):
        req(phrase in info_body.lower(),f'infographic production lost native final QA: {phrase}')
    req('manual action package' not in info_body.lower(),'infographic recreated retired capability fallback')

    _,landing_meta,landing_body=load('systems/marketing-synthesis/contracts/landing-page/qa/CONTEXT.md')
    req(landing_meta.get('id')=='marketing.landing-page.qa' and landing_meta.get('type')=='workflow','landing-page QA Workflow missing')
    for phrase in ('actual available artifact','claim policy','accessibility','no run is required'):
        req(phrase in landing_body.lower(),f'landing-page QA lost substantive boundary: {phrase}')

    for retired in ('scripts/record_contract_completion.py','scripts/finalize_run.py','scripts/complete_sop_run.py'):
        req(not (ROOT/retired).exists(),f'QA invariant recreated Run orchestration helper: {retired}')

    print('customer-facing QA regressions passed: substantive artifact QA remains strong as reusable Workflow knowledge without execution orchestration')

if __name__=='__main__':main()
