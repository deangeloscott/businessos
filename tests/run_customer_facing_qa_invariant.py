#!/usr/bin/env python3
"""Protect strong customer-facing QA as reusable expertise, not execution orchestration."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from _common import read_frontmatter


def req(condition,message):
    if not condition:raise AssertionError(message)
def load(rel):
    path=ROOT/rel;meta,body=read_frontmatter(path);return path,meta,body


def main():
    _,pre_meta,pre_body=load('systems/content-synthesis/workflows/qa/pre-publish/CONTEXT.md')
    req(pre_meta.get('id')=='content.qa.pre-publish' and pre_meta.get('type')=='workflow','shared Content pre-publish QA Workflow is missing')
    for phrase in ('actual final artifact','claim_surface_ref','accessibility','run/work receipt is optional'):
        req(phrase in pre_body.lower(),f'pre-publish QA lost substantive boundary: {phrase}')
    req('approval object' in pre_body.lower() and 'publication decision' in pre_body.lower(),'pre-publish QA must preserve real-review needs without becoming launch authority')

    # Article can draw on briefs, narrative/proof methods, and final QA when useful, but no
    # metadata may turn those expert methods into an execution graph.
    _,article_meta,article_body=load('systems/content-synthesis/workflows/production/article/CONTEXT.md')
    req(article_meta.get('id')=='content.production.article' and article_meta.get('type')=='workflow','Article production Workflow is missing')
    req('artifact_role' not in article_meta,'Article production regained retired artifact_role metadata')
    req(not (article_meta.get('workflows') or {}).get('required'),'Article production regained mandatory supporting-Workflow composition')
    req('optional expert methods, not a required execution graph' in article_body,'Article lost advisory-composition boundary')
    req('evidence-bounded' in article_body and 'high-quality article' in article_body,'Article quality/evidence standard was weakened')
    req('mandatory completion artifact' in article_body,'Article claim provenance became mandatory semantic paperwork')

    _,image_meta,image_body=load('systems/content-synthesis/workflows/production/image/CONTEXT.md')
    req(image_meta.get('id')=='content.production.image' and image_meta.get('type')=='workflow','Image production Workflow is missing')
    req('artifact_role' not in image_meta,'Image production regained retired artifact_role metadata')
    for phrase in ('inspect the final image','visual errors','legibility','accessibility'):
        req(phrase in image_body.lower(),f'image production lost native final QA: {phrase}')
    req('not required' in image_body.lower(),'Image production lost direct-request/no-durable-handoff boundary')

    _,info_meta,info_body=load('systems/content-synthesis/workflows/production/infographic/CONTEXT.md')
    req(info_meta.get('id')=='content.production.infographic' and info_meta.get('type')=='workflow','Infographic production Workflow is missing')
    req('artifact_role' not in info_meta,'Infographic production regained retired artifact_role metadata')
    for phrase in ('inspect the actual final visual','legibility','factual fidelity','accessibility'):
        req(phrase in info_body.lower(),f'infographic production lost native final QA: {phrase}')
    req('manual-action workflow' not in info_body.lower(),'Infographic recreated retired capability fallback')
    req('no run or completion ledger is required' in info_body.lower(),'Infographic QA became receipt/ledger dependent')

    _,landing_meta,landing_body=load('systems/marketing-synthesis/workflows/landing-page/qa/CONTEXT.md')
    req(landing_meta.get('id')=='marketing.landing-page.qa' and landing_meta.get('type')=='workflow','Landing-page QA Workflow missing')
    for phrase in ('actual available artifact','customer-facing claim policy','accessibility','no run is required'):
        req(phrase in landing_body.lower(),f'landing-page QA lost substantive boundary: {phrase}')
    req('aura does not own launch authorization' in landing_body.lower(),'Landing QA regained release authority')
    req('routing issues to another aura service' in landing_body.lower(),'Landing QA lost direct cross-domain continuation boundary')

    for retired in ('scripts/record_contract_completion.py','scripts/finalize_run.py','scripts/complete_sop_run.py'):
        req(not (ROOT/retired).exists(),f'QA invariant recreated execution-orchestration helper: {retired}')

    print('customer-facing QA regressions passed: strong final-artifact QA remains reusable expert knowledge without required composition, semantic approval, or execution orchestration')


if __name__=='__main__':main()
