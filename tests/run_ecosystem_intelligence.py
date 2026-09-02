#!/usr/bin/env python3
"""Regression checks for external intelligence without an AURA routing/control plane."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from _common import read_frontmatter
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
def contracts():
    out={}
    for p in ROOT.rglob('CONTEXT.md'):
        if '/contracts/' not in p.as_posix():continue
        meta,body=read_frontmatter(p)
        if meta.get('id'):out[meta['id']]=(p,meta,body)
    return out
def workflow_ids(meta):
    refs=[]
    for kind in ('required','conditional'):
        for item in (meta.get('workflows') or {}).get(kind,[]) or []:
            refs.append(item.get('id') if isinstance(item,dict) else item)
    return refs


def main():
    cs=contracts();missing=(CORE_IDS|DOMAIN_IDS)-set(cs)
    req(not missing,'missing ecosystem Workflows: '+', '.join(sorted(missing)))
    for wid in CORE_IDS|DOMAIN_IDS:req(cs[wid][1].get('type')=='workflow',f'{wid} must be represented as a Workflow')
    for cid in RETIRED_IDS:req(cid not in cs,f'retired semantic/routing Workflow returned: {cid}')

    policy=(ROOT/'core/policies/external-learning.md').read_text()
    for concepts in [
        ('active model/user','semantic interpretation'),
        ('host/harness','scheduling','execution'),
        ('source attention','source truth'),
        ('repetition','independent replication'),
        ('freshness','mechanism-specific'),
        ('sourceRecord','Observation','Insight','not mandatory lifecycle'),
        ('external discovery','automatically establish','active-business fact'),
    ]:
        req(contains(policy,*concepts),f'external-learning policy missing concepts: {concepts}')
    req('ActionPacket' not in policy,'external-learning policy reintroduced ActionPacket')

    schema=json.loads((ROOT/'core/schemas/intelligence/source-profile.schema.json').read_text())
    req(schema.get('title')=='SourceProfile' and schema.get('additionalProperties') is False,'SourceProfile schema must remain strict')
    required=set(schema.get('required',[]))
    for field in ['source_reference','source_kind','owner_systems','watch_status','attention_priority','fact_type_assessments']:
        req(field in required,f'SourceProfile missing required field {field}')

    helper=(ROOT/'scripts/upsert_source_profile.py').read_text()
    for phrase in ['outcome_events','event_key','Source history changes discovery attention only']:
        req(phrase in helper,f'source profile helper missing {phrase}')

    a='HTTPS://Example.COM:443/Research/Article/';b='https://example.com/Research/Article'
    req(_normalized_reference(a)==b,'URL normalization must collapse scheme/host casing, default HTTPS port, and trailing slash')
    req(_profile_id('test-business',a)==_profile_id('test-business',b),'mechanically equivalent URLs must share a deterministic profile id')
    req(_profile_id('test-business',b)!=_profile_id('test-business','https://example.com/research/article'),'URL normalization must preserve potentially case-sensitive paths')
    try:_normalized_reference('https://user:secret@example.com/research')
    except ValueError:pass
    else:fail('SourceProfile references must reject embedded URL credentials')

    discovery=cs['core.intelligence.ecosystem.source-discovery'][2]
    for concepts in [
        ('active model/user','fresh'),('semantic source identity','model/user'),('normalization','hashes','exact identifiers'),
        ('discovery-only','support-grade'),('additional discovery','unlikely to change the decision'),
    ]:req(contains(discovery,*concepts),f'source discovery lost boundary: {concepts}')

    triangulation=cs['core.intelligence.ecosystem.evidence-triangulation'][2]
    for concepts in [
        ('originating evidence','independent support','independent contradiction'),('echo','independent corroboration'),
        ('freshness','novelty'),('semantic','current Insights/Learnings'),
    ]:req(contains(triangulation,*concepts),f'evidence triangulation lost invariant: {concepts}')

    source_profile=cs['core.intelligence.ecosystem.maintain-source-profile'][2]
    req(contains(source_profile,'discovery priors only','never use SourceProfile history as support'),'SourceProfile history became evidence authority')
    req(contains(source_profile,'never merge namesakes','name similarity'),'SourceProfile lost semantic identity boundary')

    core_meta=cs['core.intelligence.ecosystem-radar'][1];core_body=cs['core.intelligence.ecosystem-radar'][2]
    req('schedule' not in core_meta,'Core ecosystem radar reintroduced AURA-owned schedule metadata')
    req('capabilities' not in core_meta,'Core ecosystem radar reintroduced AURA capability ontology')
    req('SourceProfile' in (core_meta.get('reads') or []),'Core ecosystem radar must reuse durable source/watch state')
    req('WorkRequest' not in (core_meta.get('writes') or []) and 'Opportunity' not in (core_meta.get('writes') or []),'Core radar should not manufacture routed work objects')
    refs=workflow_ids(core_meta)
    req('core.intelligence.ecosystem.source-discovery' in refs and 'core.intelligence.ecosystem.evidence-triangulation' in refs,'Core radar lost shared evidence Workflows')
    req('core.intelligence.ecosystem.route-learning' not in refs,'Core radar reintroduced retired route-learning controller')
    for concepts in [('active harness/runtime','scheduling'),('does not automatically invoke or route','domain'),('model/user','disposition'),('do not manufacture WorkRequests','Opportunities')]:
        req(contains(core_body,*concepts),f'Core radar lost model/runtime boundary: {concepts}')

    for cid in DOMAIN_IDS:
        meta,body=cs[cid][1],cs[cid][2];refs=workflow_ids(meta)
        for needed in ['core.intelligence.ecosystem.source-discovery','core.intelligence.ecosystem.evidence-triangulation']:
            req(needed in refs,f'{cid} does not reuse shared Core evidence Workflow {needed}')
        req('WorkRequest' not in (meta.get('writes') or []),f'{cid} still writes WorkRequest as radar orchestration')
        req(contains(body,'model') or contains(body,'active model'),f'{cid} lost explicit model judgment')
        req(not contains(body,'exact next route'),f'{cid} still requires an exact routed next method')

    community=cs['core.intelligence.community-evidence-review'];crefs=workflow_ids(community[1])
    req('core.intelligence.ecosystem.evidence-triangulation' in crefs,'community evidence review lost triangulation Workflow')
    req('core.intelligence.ecosystem.route-learning' not in crefs,'community review reintroduced route-learning')
    req('WorkRequest' not in (community[1].get('writes') or []) and 'Opportunity' not in (community[1].get('writes') or []),'community review became a routing-object producer')

    map_expected={
        'core/process-map.json':'core.intelligence.ecosystem-radar','systems/competitor-intelligence/process-map.json':'competitor.intelligence.ecosystem-radar',
        'systems/customer-intelligence/process-map.json':'customer.intelligence.ecosystem-radar','systems/industry-intelligence/process-map.json':'industry.intelligence.ecosystem-radar',
        'systems/seo-aeo/process-map.json':'seo.intelligence.ecosystem.tactic-radar','systems/content-synthesis/process-map.json':'content.intelligence.ecosystem-radar',
        'systems/marketing-synthesis/process-map.json':'marketing.intelligence.ecosystem-radar','systems/customer-optimization/process-map.json':'customer-optimization.intelligence.ecosystem-radar',
    }
    for rel,cid in map_expected.items():
        data=json.loads((ROOT/rel).read_text());req(cid in [a.get('entry_contract') for a in data.get('activities',[])],f'{rel} missing radar Workflow {cid}')

    print(f'ecosystem intelligence regressions passed: {len(CORE_IDS)} shared Workflows + {len(DOMAIN_IDS)} domain radars without routing/control authority')

if __name__=='__main__':main()
