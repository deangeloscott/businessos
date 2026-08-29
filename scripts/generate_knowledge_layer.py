#!/usr/bin/env python3
"""Generate an Obsidian/Markdown-friendly human view from canonical AURA/BusinessOS state."""
from _common import *
import argparse,json,shutil

PAGES=[
    ('Business','Business, Brand, products, offers, markets, audiences and other durable context.'),
    ('Priorities','Objectives, opportunities, initiatives, work requests and active attention.'),
    ('Learning','Current AURA/BusinessOS Learning and its maturity/status.'),
    ('Experiments','Experiments, outcome evaluations and measured learning state.'),
    ('Tracked-Subjects','Public/authorized subjects and sources AURA is intentionally watching, why they matter, and current checkpoints.'),
    ('Customers','Customer Intelligence and customer-understanding state.'),
    ('Competitors','Competitor Intelligence state.'),
    ('Industry','Industry Intelligence state.'),
    ('SEO-AEO','SEO/AEO intelligence and operating state.'),
    ('Content-Marketing','Content Synthesis and Marketing Synthesis state.'),
    ('Customer-Optimization','Customer Optimization state.'),
    ('Operations','Actions, approvals, incidents, change/verification and operational attention.'),
    ('Evidence','Sources, observations, insights and proof lineage.')
]

BUSINESS_TYPES={'Business','Brand','ProductService','Offer','Market','AudienceSegment','EconomicContext','BusinessClaim','PreferenceProfile'}
PRIORITY_TYPES={'Objective','Opportunity','Initiative','WorkRequest','AttentionItem'}
EXPERIMENT_TYPES={'Experiment','OutcomeEvaluation','MetricDefinition','MetricObservation'}
OPERATIONS_TYPES={'ActionPacket','Approval','Incident','ChangeEvent','VerificationRecord','WorkRequest','AttentionItem','EventReactionDecision','PlatformChange'}
EVIDENCE_TYPES={'SourceRecord','SourceProfile','Observation','Insight','ProofRecord'}


def _clean(value,limit=700):
    if value is None:return ''
    if isinstance(value,(dict,list)): value=json.dumps(value,ensure_ascii=False,sort_keys=True)
    s=' '.join(str(value).split())
    return s if len(s)<=limit else s[:limit-1]+'…'


def _title(obj):
    for key in ['name','title','subject_name','statement','conclusion','task','display_name','id']:
        if obj.get(key): return _clean(obj[key],160)
    return obj.get('object_type','Object')


def _scheduler_bindings():
    environment=installation().get('default_environment') or 'local'
    try:path=environment_file(environment,'scheduler-bindings.json')
    except Exception:return environment,[]
    try:data=json.loads(path.read_text())
    except Exception:return environment,[]
    return environment,data.get('bindings',[]) or []


def _matching_scheduler_bindings(obj,bindings):
    out=[]
    for b in bindings:
        if b.get('business_id')!=obj.get('business_id'):continue
        kind=b.get('target_kind')
        if kind=='subject' and obj.get('subject_key') and b.get('subject_key')==obj.get('subject_key'):out.append(b)
        elif kind=='source_profile' and b.get('source_profile_id')==obj.get('id'):out.append(b)
        elif kind=='business_monitoring':out.append(b)
    return out


def _schedule_state(obj,bindings):
    matched=_matching_scheduler_bindings(obj,bindings)
    active=[b for b in matched if b.get('status')=='active' and b.get('last_verified_at')]
    if any(b.get('executor_kind')!='reminder_only' for b in active):return 'active automatic',active
    if any(b.get('executor_kind')=='reminder_only' for b in active):return 'reminder-only',active
    if any(b.get('status')=='paused' for b in matched):return 'paused',matched
    if obj.get('monitoring_cadence') or obj.get('next_check_at'):return 'planned / not automatically scheduled',matched
    return 'manual',matched


def _cadence_text(obj):
    c=obj.get('monitoring_cadence')
    if not c:return ''
    expr=c.get('expression') or c.get('mode') or ''
    src=c.get('source')
    tz=c.get('timezone')
    bits=[expr]
    if src:bits.append(f'{src}')
    if tz:bits.append(tz)
    return ' · '.join(x for x in bits if x)


def _entry(obj,path,bindings=None):
    bindings=bindings or []
    oid=obj.get('id','(no id)'); typ=obj.get('object_type','Object'); title=_title(obj)
    lines=[f"### {title}",f"- **Type:** `{typ}`",f"- **ID:** `{oid}`"]
    for label,key in [('Owner','owner_system'),('Status','status'),('Maturity','maturity'),('Scope','owner_scope')]:
        if obj.get(key) is not None: lines.append(f"- **{label}:** `{_clean(obj.get(key),120)}`")
    if obj.get('confidence') is not None: lines.append(f"- **Confidence:** `{obj.get('confidence')}`")
    lines.append(f"- **Canonical source:** `{storage_ref(path)}`")
    if typ=='SourceProfile':
        if obj.get('subject_kind'): lines.append(f"- **Subject kind:** `{_clean(obj.get('subject_kind'),120)}`")
        if obj.get('subject_relationships'): lines.append(f"- **Relationship(s):** {_clean(obj.get('subject_relationships'),240)}")
        if obj.get('owner_systems'): lines.append(f"- **Used by:** {_clean(obj.get('owner_systems'),240)}")
        if obj.get('source_reference'): lines.append(f"- **Source/surface:** {_clean(obj.get('source_reference'),500)}")
        if obj.get('source_modalities'): lines.append(f"- **Modality:** {_clean(obj.get('source_modalities'),160)}")
        if obj.get('watch_status'): lines.append(f"- **Watch status:** `{_clean(obj.get('watch_status'),80)}`")
        if obj.get('attention_priority'): lines.append(f"- **Attention priority:** `{_clean(obj.get('attention_priority'),80)}`")
        if _cadence_text(obj):lines.append(f"- **Cadence:** `{_clean(_cadence_text(obj),200)}`")
        execution,matched=_schedule_state(obj,bindings);lines.append(f"- **Automatic execution:** `{execution}`")
        if matched:lines.append(f"- **Scheduler binding(s):** {_clean([x.get('id') for x in matched],220)}")
        if obj.get('last_checked_at'): lines.append(f"- **Last checked:** `{_clean(obj.get('last_checked_at'),120)}`")
        if obj.get('next_check_at'): lines.append(f"- **Next check:** `{_clean(obj.get('next_check_at'),120)}`")
        if obj.get('last_material_change_at'): lines.append(f"- **Last material change:** `{_clean(obj.get('last_material_change_at'),120)}`")
        if obj.get('discovery_reason'): lines += ['',f"**Why AURA watches this:** {_clean(obj.get('discovery_reason'))}"]
        if obj.get('monitoring_questions'): lines += ['',f"**Monitoring questions:** {_clean(obj.get('monitoring_questions'))}"]
        if obj.get('material_change_signals'): lines += ['',f"**Material-change signals:** {_clean(obj.get('material_change_signals'))}"]
    for key,label in [('statement','Statement'),('conclusion','Conclusion'),('recommended_decision','Recommended decision'),('purpose','Purpose')]:
        if obj.get(key): lines += ['',f"**{label}:** {_clean(obj.get(key))}"]
    return '\n'.join(lines)+'\n'


def _tracked_subjects(vals,bindings):
    groups={}
    for obj,path in vals:
        key=obj.get('subject_key') or obj.get('id')
        groups.setdefault(key,[]).append((obj,path))
    blocks=[]
    for key,items in sorted(groups.items(),key=lambda kv:(_title(kv[1][0][0]).lower(),kv[0])):
        first=items[0][0];name=first.get('subject_name') or first.get('display_name') or key
        kinds=sorted({x.get('subject_kind') for x,_ in items if x.get('subject_kind')})
        rels=sorted({r for x,_ in items for r in (x.get('subject_relationships') or [])})
        used=sorted({r for x,_ in items for r in (x.get('owner_systems') or [])})
        questions=list(dict.fromkeys(q for x,_ in items for q in (x.get('monitoring_questions') or [])))
        signals=list(dict.fromkeys(q for x,_ in items for q in (x.get('material_change_signals') or [])))
        cadences=list(dict.fromkeys(_cadence_text(x) for x,_ in items if _cadence_text(x)))
        last=max([x.get('last_checked_at') for x,_ in items if x.get('last_checked_at')],default=None)
        nexts=sorted([x.get('next_check_at') for x,_ in items if x.get('next_check_at')]);next_check=nexts[0] if nexts else None
        states=[];binding_ids=[]
        for x,_ in items:
            state,matched=_schedule_state(x,bindings);states.append(state);binding_ids += [b.get('id') for b in matched if b.get('id')]
        if 'active automatic' in states:execution='active automatic'
        elif 'reminder-only' in states:execution='reminder-only'
        elif 'paused' in states:execution='paused'
        elif any(s=='planned / not automatically scheduled' for s in states):execution='planned / not automatically scheduled'
        else:execution='manual'
        lines=[f"## {name}"]
        if first.get('subject_key'):lines.append(f"- **Subject key:** `{first.get('subject_key')}`")
        if kinds:lines.append(f"- **Kind:** {_clean(kinds,180)}")
        if rels:lines.append(f"- **Relationship(s):** {_clean(rels,240)}")
        if used:lines.append(f"- **Used by:** {_clean(used,240)}")
        lines.append(f"- **Tracked sources/surfaces:** `{len(items)}`")
        if cadences:lines.append(f"- **Cadence:** {_clean(cadences,300)}")
        lines.append(f"- **Automatic execution:** `{execution}`")
        if binding_ids:lines.append(f"- **Scheduler binding(s):** {_clean(sorted(set(binding_ids)),240)}")
        if last:lines.append(f"- **Last checked:** `{last}`")
        if next_check:lines.append(f"- **Next check:** `{next_check}`")
        if questions:lines += ['',f"**Monitoring questions:** {_clean(questions,900)}"]
        if signals:lines += ['',f"**Material-change signals:** {_clean(signals,900)}"]
        lines += ['','**Sources / surfaces:**']
        for obj,path in sorted(items,key=lambda x:(_title(x[0]).lower(),x[0].get('id',''))):
            label=obj.get('display_name') or obj.get('source_reference') or obj.get('id')
            modality=f" — {_clean(obj.get('source_modalities'),120)}" if obj.get('source_modalities') else ''
            lines.append(f"- {_clean(label,220)}{modality} (`{obj.get('id')}`; `{storage_ref(path)}`)")
        blocks.append('\n'.join(lines)+'\n')
    return '\n'.join(blocks) if blocks else '_No current tracked subjects._\n'


def _page_for(obj):
    typ=obj.get('object_type'); owner=obj.get('owner_system')
    if typ=='Learning': return 'Learning'
    if typ=='SourceProfile': return 'Tracked-Subjects'
    if typ in BUSINESS_TYPES:return 'Business'
    if typ in PRIORITY_TYPES:return 'Priorities'
    if typ in EXPERIMENT_TYPES:return 'Experiments'
    if typ in EVIDENCE_TYPES:
        if owner=='customer-intelligence':return 'Customers'
        if owner=='competitor-intelligence':return 'Competitors'
        if owner=='industry-intelligence':return 'Industry'
        if owner=='seo-aeo':return 'SEO-AEO'
        if owner in {'content-synthesis','marketing-synthesis'}:return 'Content-Marketing'
        if owner=='customer-optimization':return 'Customer-Optimization'
        return 'Evidence'
    if owner=='customer-intelligence':return 'Customers'
    if owner=='competitor-intelligence':return 'Competitors'
    if owner=='industry-intelligence':return 'Industry'
    if owner=='seo-aeo':return 'SEO-AEO'
    if owner in {'content-synthesis','marketing-synthesis'}:return 'Content-Marketing'
    if owner=='customer-optimization':return 'Customer-Optimization'
    if typ in OPERATIONS_TYPES:return 'Operations'
    return 'Operations'


def _frontmatter(business_id,title,generated_at,count):
    # businessos_generated is a stable compatibility marker; public branding is AURA.
    return f"---\nbusinessos_generated: true\ncanonical: false\nproduct: ViralTrac AURA\nbusiness_id: {business_id}\ntitle: {json.dumps(title)}\ngenerated_at: {generated_at}\nobject_count: {count}\n---\n\n"


def generate(business_id):
    base=instance_dir(business_id)
    if not base.exists(): raise ValueError(f'Unknown business: {business_id}')
    profile=workspace_profile()
    if profile.get('knowledge_enabled') is False: raise ValueError('Human knowledge layer is disabled for the active workspace')
    kbase=knowledge_root()/business_id; generated=kbase/'_generated'; notes=kbase/'notes'
    kbase.mkdir(parents=True,exist_ok=True);notes.mkdir(parents=True,exist_ok=True)
    if generated.exists(): shutil.rmtree(generated)
    generated.mkdir(parents=True)
    ts=now(); grouped={name:[] for name,_ in PAGES};environment,bindings=_scheduler_bindings()
    objects=iter_instance_objects(business_id)
    for obj,path in objects: grouped[_page_for(obj)].append((obj,path))
    for name,description in PAGES:
        vals=sorted(grouped[name],key=lambda x:(x[0].get('object_type',''),_title(x[0]),x[0].get('id','')))
        body=_frontmatter(business_id,name,ts,len(vals))+f"# {name}\n\n{description}\n\n> Generated view only. Canonical AURA/BusinessOS truth remains under `instances/{business_id}/`. Human edits here may be overwritten.\n\n"
        if name=='Tracked-Subjects':body += f"**Scheduler environment:** `{environment}`. Cadence/next-check is organizational intent; automatic execution is shown only when a verified environment binding exists.\n\n"+_tracked_subjects(vals,bindings)
        else:body += '\n'.join(_entry(obj,path,bindings) for obj,path in vals) if vals else '_No current canonical objects in this view._\n'
        (generated/f'{name}.md').write_text(body)
    links='\n'.join(f"- [{name}](_generated/{name}.md) — {desc}" for name,desc in PAGES)
    home=_frontmatter(business_id,'Home',ts,len(objects))+f"# {business_id} — ViralTrac AURA Knowledge\n\nThis is the human-facing view of the active AURA workspace. It can be opened directly in Obsidian, VS Code, or any Markdown tool.\n\n**Canonical truth:** `instances/{business_id}/`  \n**Human notes:** `knowledge/{business_id}/notes/` (noncanonical until explicitly incorporated through AURA evidence/context governance)\n\n## Views\n{links}\n"
    (generated/'Home.md').write_text(home)
    readme=kbase/'README.md'
    if not readme.exists():
        readme.write_text(f"# {business_id} — ViralTrac AURA Knowledge\n\nStart with [`_generated/Home.md`](_generated/Home.md). Generated files are derived views and may be replaced on refresh. Put human-authored working notes in `notes/`; those notes are not canonical BusinessOS truth unless explicitly incorporated through normal AURA evidence/truth workflows.\n")
    notes_readme=notes/'README.md'
    if not notes_readme.exists():
        notes_readme.write_text('# Human Notes\n\nWrite working notes here. These files are intentionally noncanonical. AURA must not treat a note as verified business truth merely because it exists in this folder.\n')
    return {'business_id':business_id,'knowledge_root':str(kbase),'generated_root':str(generated),'human_start':str(generated/'Home.md'),'tracked_subjects_view':str(generated/'Tracked-Subjects.md'),'canonical_object_count':len(objects),'pages':1+len(PAGES),'generated_at':ts}


def main():
    p=argparse.ArgumentParser();p.add_argument('business_id');p.add_argument('--json',action='store_true');a=p.parse_args()
    try:r=generate(a.business_id)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps(r,indent=2) if a.json else f"generated AURA human knowledge: {r['pages']} pages from {r['canonical_object_count']} canonical objects -> {r['generated_root']}")

if __name__=='__main__':main()
