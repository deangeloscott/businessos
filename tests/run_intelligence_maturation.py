#!/usr/bin/env python3
"""Regression checks for AURA's shared intelligence maturation invariants."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from _common import read_frontmatter
from generate_knowledge_layer import _page_for,_entry
from validate_research_evidence import DIRECT_ACQUISITION_METHODS,DISCOVERY_ONLY_METHODS,_capture_quality


def fail(msg): raise AssertionError(msg)


def contract(cid):
    for p in ROOT.rglob('CONTEXT.md'):
        if '/contracts/' not in p.as_posix(): continue
        meta,body=read_frontmatter(p)
        if meta.get('id')==cid:return p,meta,body
    fail(f'missing contract {cid}')


def main():
    policy=ROOT/'core/policies/intelligence-foundation.md'
    if not policy.exists():fail('missing shared intelligence foundation policy')
    ptext=policy.read_text()
    for phrase in ['The organization is the durable unit of intelligence','Shared mechanics, domain-specific meaning','Capability-neutral','Minimum sufficient research','Contextual comparison','Human and machine legibility']:
        if phrase not in ptext:fail(f'intelligence foundation missing invariant: {phrase}')

    research=(ROOT/'core/policies/research-evidence.md').read_text()
    for phrase in ['Modality-specific support boundary','image_inspection','audio_inspection','video_inspection','transcript_read','does not establish tone','Transcript-only evidence can support spoken-language claims']:
        if phrase not in research:fail(f'research evidence policy missing multimodal boundary: {phrase}')
    for method in ['image_inspection','audio_inspection','video_inspection','transcript_read','document_visual_inspection']:
        if method not in DIRECT_ACQUISITION_METHODS:fail(f'multimodal acquisition method not support-grade: {method}')
    if not {'search_result','ai_summary'} <= DISCOVERY_ONLY_METHODS:fail('discovery-only evidence boundary regressed')
    media_source={'extensions':{'businessos_evidence':{'capture_status':'captured','acquisition_method':'video_inspection','asset_refs':['ast_frame']}}}
    if not _capture_quality(media_source)[0]:fail('direct inspected media with preserved evidence should pass capture-quality floor')
    unseen_summary={'extensions':{'businessos_evidence':{'capture_status':'captured','acquisition_method':'ai_summary','captured_text':'model summary'}}}
    if _capture_quality(unseen_summary)[0]:fail('AI summary of unseen media must remain discovery-only')

    schema=json.loads((ROOT/'core/schemas/intelligence/source-profile.schema.json').read_text())
    props=schema.get('properties',{})
    for field in ['subject_key','subject_name','subject_kind','subject_relationships','source_modalities','monitoring_questions','material_change_signals','monitoring_cadence','monitoring_signal_cadences','monitoring_notification','last_material_change_at']:
        if field not in props:fail(f'SourceProfile missing intelligence-maturation field {field}')
    required=set(schema.get('required',[]))
    if any(field in required for field in ['subject_key','subject_name','subject_kind','source_modalities','monitoring_questions','monitoring_cadence','monitoring_signal_cadences','monitoring_notification']):
        fail('new subject/watch enrichment must remain optional for backward compatibility')
    rels=set(props['subject_relationships']['items']['enum'])
    if {'customer','prospect'} & rels:
        fail('shared public subject monitoring must not become a customer/prospect surveillance relationship model')

    helper=(ROOT/'scripts/upsert_source_profile.py').read_text()
    for flag in ['--subject-key','--subject-name','--subject-kind','--subject-relationship','--source-modality','--monitoring-question','--material-change-signal','--cadence-mode','--cadence-expression','--cadence-source','--signal-cadence-json','--notification-mode']:
        if flag not in helper:fail(f'SourceProfile helper missing {flag}')
    if 'Source history changes discovery attention only' not in helper:
        fail('existing SourceProfile discovery-only invariant was lost')

    _,subject_meta,subject_body=contract('core.intelligence.subject-monitoring')
    for phrase in ['one SourceProfile per source/surface','shared `subject_key`','text, documents, images, audio, video, transcripts','cadence/`next_check_at` is monitoring intent','monitoring_signal_cadences','material_changes_only']:
        if phrase not in subject_body:fail(f'subject monitoring missing behavior: {phrase}')
    if 'core.intelligence.ecosystem.maintain-source-profile' not in (subject_meta.get('subcontracts') or {}).get('required',[]):
        fail('subject monitoring must reuse shared SourceProfile mechanics')

    _,_,routing_body=contract('core.routing.resolve-intent')
    for phrase in ['durable subject watch/refresh','`core.intelligence.subject-monitoring`','not merely because it contains words such as “track” or “monitor.”']:
        if phrase not in routing_body:fail(f'semantic intent resolution missing durable monitoring rule: {phrase}')

    core_map=json.loads((ROOT/'core/process-map.json').read_text())
    entry_ids=[a.get('entry_contract') for a in core_map.get('activities',[])]
    if 'core.intelligence.subject-monitoring' not in entry_ids:fail('Core process map missing durable subject monitoring')
    if 'core.monitoring.status' not in entry_ids:fail('Core process map missing human monitoring status view')

    for rel,phrases in {
        'systems/competitor-intelligence/DEFAULTS.md':['Contextual Competitive Set','geography/service area','aspirational/category-benchmark'],
        'systems/customer-intelligence/DEFAULTS.md':['Decision Context and Motivations','loss avoidance','status/identity'],
        'systems/content-synthesis/DEFAULTS.md':['TOF/MOF/BOF','up to three genuinely distinct options','Content Stretching'],
        'systems/marketing-synthesis/DEFAULTS.md':['Persuasion Context','Marketing Doctrine and Baseline Excellence','up to three genuinely distinct strategic options','Offer and Value Reasoning'],
        'systems/seo-aeo/DEFAULTS.md':['Contextual Organic Competition','local/map packs','national category giant'],
        'systems/customer-optimization/DEFAULTS.md':['mutually valuable','cost-to-serve','High-value customer','value-at-risk'],
    }.items():
        text=(ROOT/rel).read_text()
        for phrase in phrases:
            if phrase not in text:fail(f'{rel} missing intelligence behavior: {phrase}')

    _,value_meta,value_body=contract('customer-optimization.measurement.customer-value')
    for phrase in ['customer ROI/value realization','LTV','cost-to-serve','high spend alone','risk likelihood','value-at-risk']:
        if phrase not in value_body:fail(f'customer-value contract missing {phrase}')
    if value_meta.get('owner_system')!='customer-optimization':fail('customer-value semantic owner changed')
    co_map=json.loads((ROOT/'systems/customer-optimization/process-map.json').read_text())
    if 'customer-optimization.measurement.customer-value' not in [a.get('entry_contract') for a in co_map.get('activities',[])]:
        fail('Customer Optimization process map missing customer-value analysis')

    source_profile={
        'id':'sprof_demo','object_type':'SourceProfile','subject_name':'Example Creator','subject_kind':'creator',
        'subject_relationships':['thought_leader'],'source_reference':'https://example.com/channel','source_modalities':['video'],
        'watch_status':'active','attention_priority':'medium','discovery_reason':'Learn durable content mechanisms.',
        'monitoring_questions':['What topics are changing?'],'material_change_signals':['Major positioning shift'],
        'monitoring_cadence':{'mode':'recurring','expression':'weekly','source':'inferred','timezone':None,'notes':None},
        'monitoring_notification':{'mode':'material_changes_only','source':'policy','notes':None},
        'last_checked_at':'2026-08-29T00:00:00Z','next_check_at':'2026-09-05T00:00:00Z'
    }
    if _page_for(source_profile)!='Tracked-Subjects':fail('SourceProfile human view is not routed to Tracked-Subjects')
    rendered=_entry(source_profile,ROOT/'instances/example/intelligence/source-profiles/sprof_demo.json')
    for phrase in ['Example Creator','thought_leader','What topics are changing?','Major positioning shift','Default cadence','Notification mode','material_changes_only','planned / not automatically scheduled','Last checked','Next check']:
        if phrase not in rendered:fail(f'tracked-subject human view missing {phrase}')

    print('AURA intelligence maturation regressions passed: shared monitoring, semantic routing, multimodal evidence, contextual intelligence, marketing/customer value, and human/machine legibility')

if __name__=='__main__':main()
