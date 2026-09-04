#!/usr/bin/env python3
"""Regression checks for external intelligence as evidence-guided knowledge, not a routing/control plane."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from _common import workflow_files,read_frontmatter
from upsert_source_profile import _normalized_reference,_profile_id

CORE_IDS={
    'core.intelligence.ecosystem-radar',
    'core.intelligence.ecosystem.source-discovery',
    'core.intelligence.ecosystem.evidence-triangulation',
    'core.intelligence.ecosystem.maintain-source-profile',
}
DOMAIN_IDS={
    'competitor.intelligence.ecosystem-radar',
    'customer.intelligence.ecosystem-radar',
    'industry.intelligence.ecosystem-radar',
    'seo.intelligence.ecosystem.tactic-radar',
    'content.intelligence.ecosystem-radar',
    'marketing.intelligence.ecosystem-radar',
    'customer-optimization.intelligence.ecosystem-radar',
}
RETIRED_IDS={
    'core.intelligence.ecosystem.route-learning',
    'core.routing.resolve-intent',
    'core.coordination.multi-domain-request',
}


def fail(msg):raise AssertionError(msg)
def req(cond,msg):
    if not cond:fail(msg)
def contains(text,*parts):
    low=text.lower();return all(str(p).lower() in low for p in parts)
def workflows():
    out={}
    for p in workflow_files():
        meta,body=read_frontmatter(p)
        if meta.get('id'):out[meta['id']]=(p,meta,body)
    return out


def main():
    ws=workflows();missing=(CORE_IDS|DOMAIN_IDS)-set(ws)
    req(not missing,'missing ecosystem Workflows: '+', '.join(sorted(missing)))
    for wid in CORE_IDS|DOMAIN_IDS:req(ws[wid][1].get('type')=='workflow',f'{wid} must be represented as a Workflow')
    for wid in RETIRED_IDS:req(wid not in ws,f'retired semantic/routing Workflow returned: {wid}')

    policy=(ROOT/'core/policies/external-learning.md').read_text()
    for concepts in [
        ('active model/user','semantic interpretation'),
        ('host/harness','scheduling','execution'),
        ('source attention','source truth'),
        ('repetition','independent replication'),
        ('freshness','mechanism-specific'),
        ('SourceRecord','Observation','Insight','not mandatory lifecycle'),
        ('external discovery','automatically establish','active-business fact'),
    ]:
        req(contains(policy,*concepts),f'external-learning policy missing concepts: {concepts}')
    req('ActionPacket' not in policy,'external-learning policy reintroduced ActionPacket')

    schema=json.loads((ROOT/'core/schemas/intelligence/source-profile.schema.json').read_text())
    req(schema.get('title')=='SourceProfile' and schema.get('additionalProperties') is False,'SourceProfile schema must remain strict')
    props=schema.get('properties',{});required=set(schema.get('required',[]))
    for field in ['source_reference','source_kind','watch_status','attention_priority','fact_type_assessments']:
        req(field in required,f'SourceProfile missing required field {field}')
    req('domains' in props and 'domains' not in required,'SourceProfile semantic domains should be available but optional')
    req('owner_systems' not in props,'SourceProfile regained internal AURA ownership')

    helper=(ROOT/'scripts/upsert_source_profile.py').read_text()
    for phrase in ['outcome_events','event_key','--domain']:
        req(phrase in helper,f'source profile helper missing {phrase}')
    req('--owner-system' not in helper,'source profile helper regained internal AURA ownership')

    a='HTTPS://Example.COM:443/Research/Article/';b='https://example.com/Research/Article'
    req(_normalized_reference(a)==b,'URL normalization must collapse scheme/host casing, default HTTPS port, and trailing slash')
    req(_profile_id('test-business',a)==_profile_id('test-business',b),'mechanically equivalent URLs must share a deterministic profile id')
    req(_profile_id('test-business',b)!=_profile_id('test-business','https://example.com/research/article'),'URL normalization must preserve potentially case-sensitive paths')
    try:_normalized_reference('https://user:secret@example.com/research')
    except ValueError:pass
    else:fail('SourceProfile references must reject embedded URL credentials')

    discovery=ws['core.intelligence.ecosystem.source-discovery'][2]
    for concepts in [
        ('active model/user','fresh'),('semantic source identity','model/user'),('normalization','hashes','exact identifiers'),
        ('discovery-only','support-grade'),('additional discovery','unlikely to change the decision'),
    ]:req(contains(discovery,*concepts),f'source discovery lost boundary: {concepts}')

    triangulation=ws['core.intelligence.ecosystem.evidence-triangulation'][2]
    for concepts in [
        ('originating evidence','independent support','independent contradiction'),('echo','independent corroboration'),
        ('freshness','novelty'),('semantic','current Insights/Learnings'),
    ]:req(contains(triangulation,*concepts),f'evidence triangulation lost invariant: {concepts}')

    source_profile=ws['core.intelligence.ecosystem.maintain-source-profile'][2]
    req(contains(source_profile,'discovery priors only','never use SourceProfile history as support'),'SourceProfile history became evidence authority')
    req(contains(source_profile,'never merge namesakes','name similarity'),'SourceProfile lost semantic identity boundary')

    for wid in ['core.intelligence.ecosystem-radar',*sorted(DOMAIN_IDS),'core.intelligence.community-evidence-review']:
        meta,body=ws[wid][1],ws[wid][2]
        req('schedule' not in meta,f'{wid} reintroduced AURA-owned schedule metadata')
        req('capabilities' not in meta,f'{wid} reintroduced AURA capability ontology')
        req('workflows' not in meta,f'{wid} reintroduced supporting-Workflow composition metadata')
        req('WorkRequest' not in (meta.get('writes') or []),f'{wid} writes WorkRequest as orchestration state')
        req('route-learning' not in body,f'{wid} reintroduced retired route-learning controller')
        req(contains(body,'model') or contains(body,'active model'),f'{wid} lost explicit capable-model judgment')

    core_meta,core_body=ws['core.intelligence.ecosystem-radar'][1],ws['core.intelligence.ecosystem-radar'][2]
    req('SourceProfile' in (core_meta.get('reads') or []),'Core ecosystem radar must reuse durable source/watch state')
    req('Opportunity' not in (core_meta.get('writes') or []),'Core radar should not manufacture Opportunity routing state')
    for concepts in [('active harness/runtime','scheduling'),('does not automatically invoke or route','domain'),('model/user','disposition'),('do not manufacture WorkRequests','Opportunities')]:
        req(contains(core_body,*concepts),f'Core radar lost model/runtime boundary: {concepts}')

    community=ws['core.intelligence.community-evidence-review']
    req(contains(community[2],'popularity','independent evidence'),'community review must keep popularity distinct from evidence')
    req('Opportunity' not in (community[1].get('writes') or []),'community review became an Opportunity producer')

    map_expected={
        'core/process-map.json':'core.intelligence.ecosystem-radar','systems/competitor-intelligence/process-map.json':'competitor.intelligence.ecosystem-radar',
        'systems/customer-intelligence/process-map.json':'customer.intelligence.ecosystem-radar','systems/industry-intelligence/process-map.json':'industry.intelligence.ecosystem-radar',
        'systems/seo-aeo/process-map.json':'seo.intelligence.ecosystem.tactic-radar','systems/content-synthesis/process-map.json':'content.intelligence.ecosystem-radar',
        'systems/marketing-synthesis/process-map.json':'marketing.intelligence.ecosystem-radar','systems/customer-optimization/process-map.json':'customer-optimization.intelligence.ecosystem-radar',
    }
    for rel,wid in map_expected.items():
        data=json.loads((ROOT/rel).read_text());req(wid in [a.get('entry_workflow') for a in data.get('activities',[])],f'{rel} missing radar Workflow {wid}')

    print(f'ecosystem intelligence regressions passed: shared evidence methods + {len(DOMAIN_IDS)} domain radars without composition, routing, or runtime authority')

if __name__=='__main__':main()
