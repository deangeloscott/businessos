#!/usr/bin/env python3
"""Generate a simple human-readable Markdown view of canonical AURA organization state."""
from _common import *
import argparse,json,shutil

PAGES=[
    ('Business','Durable organization, brand, product, offer, market and audience context.'),
    ('Priorities','Objectives, opportunities, initiatives, work requests and active attention.'),
    ('Learning','Evidence-supported organizational Learning.'),
    ('Experiments','Experiments, measurements and outcome evaluations.'),
    ('Tracked-Subjects','Subjects and sources AURA intends to keep current, including cadence and material-change intent.'),
    ('Customers','Customer Intelligence state.'),('Competitors','Competitor Intelligence state.'),('Industry','Industry Intelligence state.'),
    ('SEO-AEO','SEO/AEO intelligence and work.'),('Content-Marketing','Content/Marketing synthesis state.'),('Customer-Optimization','Customer Optimization state.'),
    ('Operations','Decisions, incidents, material changes, work requests and attention.'),('Evidence','Sources, observations, insights and proof lineage.')
]
BUSINESS_TYPES={'Business','Brand','ProductService','Offer','Market','AudienceSegment','EconomicContext','BusinessClaim','PreferenceProfile'}
PRIORITY_TYPES={'Objective','Opportunity','Initiative','WorkRequest','AttentionItem'}
EXPERIMENT_TYPES={'Experiment','OutcomeEvaluation','MetricDefinition','MetricObservation'}
OPERATIONS_TYPES={'DecisionRecord','Incident','ChangeEvent','VerificationRecord','WorkRequest','AttentionItem','PlatformChange'}
EVIDENCE_TYPES={'SourceRecord','SourceProfile','Observation','Insight','ProofRecord'}
DEFAULT_NOTIFICATION='material_changes_only'


def _clean(value,limit=700):
    if value is None:return ''
    if isinstance(value,(dict,list)):value=json.dumps(value,ensure_ascii=False,sort_keys=True)
    text=' '.join(str(value).split())
    return text if len(text)<=limit else text[:limit-1]+'…'


def _title(obj):
    for key in ('name','title','subject_name','statement','conclusion','task','display_name','id'):
        if obj.get(key):return _clean(obj[key],160)
    return obj.get('object_type','Object')


def _cadence(obj):
    c=obj.get('monitoring_cadence') or {}
    bits=[c.get('expression') or c.get('mode'),c.get('source'),c.get('timezone')]
    return ' · '.join(str(x) for x in bits if x)


def _notification(obj):
    n=obj.get('monitoring_notification') or {}
    return n.get('mode') or DEFAULT_NOTIFICATION


def _signal(row):
    bits=[row.get('signal'),row.get('expression') or row.get('mode')]
    if row.get('notification_mode'):bits.append(f"notify={row['notification_mode']}")
    if row.get('next_check_at'):bits.append(f"next={row['next_check_at']}")
    return ' · '.join(str(x) for x in bits if x)


def _entry(obj,path):
    lines=[f"### {_title(obj)}",f"- **Type:** `{obj.get('object_type','Object')}`",f"- **ID:** `{obj.get('id','(no id)')}`",f"- **Canonical source:** `{storage_ref(path)}`"]
    for label,key in [('Owner','owner_system'),('Status','status'),('Maturity','maturity'),('Scope','owner_scope')]:
        if obj.get(key) is not None:lines.append(f"- **{label}:** `{_clean(obj.get(key),120)}`")
    if obj.get('confidence') is not None:lines.append(f"- **Confidence:** `{obj.get('confidence')}`")
    if obj.get('object_type')=='SourceProfile':
        for label,key in [('Subject kind','subject_kind'),('Relationship to organization','subject_relationships'),('Watch status','watch_status'),('Attention priority','attention_priority'),('Source/surface','source_reference'),('Last checked','last_checked_at'),('Next useful check','next_check_at')]:
            if obj.get(key):lines.append(f"- **{label}:** `{_clean(obj.get(key),500)}`")
        if _cadence(obj):lines.append(f"- **Cadence intent:** `{_clean(_cadence(obj),200)}`")
        lines.append(f"- **Notification intent:** `{_notification(obj)}`")
        if obj.get('monitoring_signal_cadences'):lines+=['','**Signal-specific cadence:**']+[f"- {_clean(_signal(x),500)}" for x in obj.get('monitoring_signal_cadences') or []]
        if obj.get('monitoring_questions'):lines+=['',f"**Monitoring questions:** {_clean(obj.get('monitoring_questions'))}"]
        if obj.get('material_change_signals'):lines+=['',f"**Material-change signals:** {_clean(obj.get('material_change_signals'))}"]
        lines+=['','> Scheduling/execution is runtime state outside AURA; cadence and next-check fields do not prove a background task exists.']
    for key,label in [('statement','Statement'),('conclusion','Conclusion'),('recommended_decision','Recommended decision'),('purpose','Purpose')]:
        if obj.get(key):lines+=['',f"**{label}:** {_clean(obj.get(key))}"]
    return '\n'.join(lines)+'\n'


def _tracked_subjects(vals):
    groups={}
    for obj,path in vals:groups.setdefault(obj.get('subject_key') or obj.get('id'),[]).append((obj,path))
    blocks=[]
    for key,items in sorted(groups.items(),key=lambda kv:_title(kv[1][0][0]).lower()):
        first=items[0][0];name=first.get('subject_name') or first.get('display_name') or key
        subject_kinds=list(dict.fromkeys(x.get('subject_kind') for x,_ in items if x.get('subject_kind')))
        relationships=list(dict.fromkeys(r for x,_ in items for r in (x.get('subject_relationships') or [])))
        questions=list(dict.fromkeys(q for x,_ in items for q in (x.get('monitoring_questions') or [])))
        signals=list(dict.fromkeys(q for x,_ in items for q in (x.get('material_change_signals') or [])))
        cadences=list(dict.fromkeys(_cadence(x) for x,_ in items if _cadence(x)))
        notifications=list(dict.fromkeys(_notification(x) for x,_ in items))
        nexts=sorted([x.get('next_check_at') for x,_ in items if x.get('next_check_at')]+[s.get('next_check_at') for x,_ in items for s in (x.get('monitoring_signal_cadences') or []) if s.get('next_check_at')])
        lines=[f"## {name}",f"- **Tracked sources/surfaces:** `{len(items)}`"]
        if first.get('subject_key'):lines.append(f"- **Subject key:** `{first.get('subject_key')}`")
        if subject_kinds:lines.append(f"- **Subject kind:** {_clean(subject_kinds,300)}")
        if relationships:lines.append(f"- **Relationship to organization:** {_clean(relationships,500)}")
        if cadences:lines.append(f"- **Cadence intent:** {_clean(cadences,300)}")
        if notifications:lines.append(f"- **Notification intent:** {_clean(notifications,300)}")
        if nexts:lines.append(f"- **Next useful check:** `{nexts[0]}`")
        lines.append('- **Runtime scheduling:** external / not inferred by AURA')
        if questions:lines+=['',f"**Monitoring questions:** {_clean(questions,900)}"]
        if signals:lines+=['',f"**Material-change signals:** {_clean(signals,900)}"]
        lines+=['','**Sources / surfaces:**']
        for obj,path in sorted(items,key=lambda x:_title(x[0]).lower()):lines.append(f"- {_clean(obj.get('display_name') or obj.get('source_reference') or obj.get('id'),220)} (`{obj.get('id')}`; `{storage_ref(path)}`)")
        blocks.append('\n'.join(lines)+'\n')
    return '\n'.join(blocks) if blocks else '_No current tracked subjects._\n'


def _page_for(obj):
    typ=obj.get('object_type');owner=obj.get('owner_system')
    if typ=='Learning':return 'Learning'
    if typ=='SourceProfile':return 'Tracked-Subjects'
    if typ in BUSINESS_TYPES:return 'Business'
    if typ in PRIORITY_TYPES:return 'Priorities'
    if typ in EXPERIMENT_TYPES:return 'Experiments'
    if owner=='customer-intelligence':return 'Customers'
    if owner=='competitor-intelligence':return 'Competitors'
    if owner=='industry-intelligence':return 'Industry'
    if owner=='seo-aeo':return 'SEO-AEO'
    if owner in {'content-synthesis','marketing-synthesis'}:return 'Content-Marketing'
    if owner=='customer-optimization':return 'Customer-Optimization'
    if typ in EVIDENCE_TYPES:return 'Evidence'
    if typ in OPERATIONS_TYPES:return 'Operations'
    return 'Operations'


def _frontmatter(business_id,title,generated_at,count):
    return f"---\naura_generated: true\ncanonical: false\nproduct: ViralTrac AURA\nbusiness_id: {business_id}\ntitle: {json.dumps(title)}\ngenerated_at: {generated_at}\nobject_count: {count}\n---\n\n"


def generate(business_id):
    base=instance_dir(business_id)
    if not base.exists():raise ValueError(f'Unknown business: {business_id}')
    if workspace_profile().get('knowledge_enabled') is False:raise ValueError('Human knowledge layer is disabled for the active workspace')
    kbase=knowledge_root()/business_id;generated=kbase/'_generated';notes=kbase/'notes';kbase.mkdir(parents=True,exist_ok=True);notes.mkdir(parents=True,exist_ok=True)
    if generated.exists():shutil.rmtree(generated)
    generated.mkdir(parents=True)
    ts=now();grouped={name:[] for name,_ in PAGES};objects=iter_instance_objects(business_id)
    for obj,path in objects:grouped[_page_for(obj)].append((obj,path))
    for name,description in PAGES:
        vals=sorted(grouped[name],key=lambda x:(x[0].get('object_type',''),_title(x[0]),x[0].get('id','')))
        body=_frontmatter(business_id,name,ts,len(vals))+f"# {name}\n\n{description}\n\n> Generated view only. Canonical AURA truth remains under `instances/{business_id}/`. Human edits here may be overwritten.\n\n"
        if name=='Tracked-Subjects':body+=_tracked_subjects(vals)
        else:body+='\n'.join(_entry(obj,path) for obj,path in vals) if vals else '_No current records._\n'
        (generated/f'{name}.md').write_text(body)
    links='\n'.join(f'- [[{name}]] — {description}' for name,description in PAGES)
    (generated/'Home.md').write_text(_frontmatter(business_id,'Home',ts,len(objects))+f"# AURA Knowledge — {business_id}\n\nOrganization-owned human view generated from canonical AURA state.\n\n{links}\n\n## Human notes\n\nHuman-authored notes live in `../notes/` and are not canonical until deliberately incorporated with provenance.\n")
    return {'business_id':business_id,'generated_root':str(generated),'page_count':len(PAGES)+1,'object_count':len(objects)}


def main():
    p=argparse.ArgumentParser(description='Generate a human-readable Markdown view of canonical AURA organization state.');p.add_argument('business_id');a=p.parse_args()
    try:r=generate(a.business_id)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps(r,indent=2))

if __name__=='__main__':main()
