#!/usr/bin/env python3
"""Generate a human-readable Markdown view of canonical AURA organization state.

The view lives under knowledge/<business-id>/_generated/ and is a replaceable
derivative of the canonical records under instances/<business-id>/. Each refresh
is staged completely, validated, and only then swapped into place with a
Windows-safe rename, backup and rollback. Concurrent readers may briefly see no
generated directory during the rename. Human notes are never replaced. The
staged layer records a content fingerprint of the canonical inputs so
enter.py/remember.py can report whether the view is current without
regenerating it.
"""
from _common import *
import argparse
import hashlib
import json
import os
import shutil
import tempfile

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
PRIORITY_TYPES={'Objective','Opportunity','Initiative','WorkRequest','AttentionItem'};EXPERIMENT_TYPES={'Experiment','OutcomeEvaluation','MetricDefinition','MetricObservation'}
OPERATIONS_TYPES={'DecisionRecord','Incident','ChangeEvent','VerificationRecord','WorkRequest','AttentionItem','PlatformChange'};EVIDENCE_TYPES={'SourceRecord','SourceProfile','Observation','Insight','ProofRecord'};DEFAULT_NOTIFICATION='material_changes_only'
STATE_FILE='.generated-state.json'
STATE_FORMAT_VERSION='1.0'
SYSTEM_PAGES={
    'competitor-intelligence':'Competitors','customer-intelligence':'Customers','industry-intelligence':'Industry',
    'seo-aeo':'SEO-AEO','content-synthesis':'Content-Marketing','marketing-synthesis':'Content-Marketing','customer-optimization':'Customer-Optimization'}

def _render_fingerprint():
    paths=(Path(__file__),PRODUCT_ROOT/'scripts/_common.py',PRODUCT_ROOT/'generated/schema-registry.json')
    return hashlib.sha256(''.join(hashlib.sha256(path.read_bytes()).hexdigest() for path in paths).encode('ascii')).hexdigest()


_TYPE_SYSTEMS=None
def _type_systems():
    """object_type -> owning system, from schema-registry path ownership (systems/<system>/... or core)."""
    global _TYPE_SYSTEMS
    if _TYPE_SYSTEMS is None:
        rows=json.loads((PRODUCT_ROOT/'generated/schema-registry.json').read_text(encoding='utf-8'))
        out={}
        for row in rows:
            if not isinstance(row,dict):continue
            title=row.get('title')
            if not title:continue
            parts=str(row.get('path') or '').split('/')
            out[title]=parts[1] if len(parts)>=2 and parts[0]=='systems' else 'core'
        _TYPE_SYSTEMS=out
    return _TYPE_SYSTEMS


def _clean(value,limit=700):
    if value is None:return ''
    if isinstance(value,(dict,list)):value=json.dumps(value,ensure_ascii=False,sort_keys=True)
    text=' '.join(str(value).split());return text if len(text)<=limit else text[:limit-1]+'…'
def _title(obj):return _clean(object_title(obj),160)
def _cadence(obj):
    c=obj.get('monitoring_cadence') or {};bits=[c.get('expression') or c.get('mode'),c.get('source'),c.get('timezone')];return ' · '.join(str(x) for x in bits if x)
def _notification(obj):return (obj.get('monitoring_notification') or {}).get('mode') or DEFAULT_NOTIFICATION
def _signal(row):
    bits=[row.get('signal'),row.get('expression') or row.get('mode')]
    if row.get('notification_mode'):bits.append(f"notify={row['notification_mode']}")
    if row.get('next_check_at'):bits.append(f"next={row['next_check_at']}")
    return ' · '.join(str(x) for x in bits if x)

def _entry(obj,path):
    lines=[f"### {_title(obj)}",f"- **Type:** `{obj.get('object_type','Object')}`",f"- **ID:** `{obj.get('id','(no id)')}`",f"- **Canonical source:** `{storage_ref(path)}`"]
    for label,key in [('Domain','domain'),('Status','status'),('Maturity','maturity'),('Scope','scope')]:
        if obj.get(key) is not None:lines.append(f"- **{label}:** `{_clean(obj.get(key),120)}`")
    if obj.get('confidence') is not None:lines.append(f"- **Confidence:** `{obj.get('confidence')}`")
    if obj.get('object_type')=='SourceProfile':
        if obj.get('domains'):lines.append(f"- **Relevant domains:** `{_clean(obj.get('domains'),300)}`")
        for label,key in [('Subject kind','subject_kind'),('Relationship to organization','subject_relationships'),('Watch status','watch_status'),('Attention priority','attention_priority'),('Source/surface','source_reference'),('Last checked','last_checked_at'),('Next useful check','next_check_at')]:
            if obj.get(key):lines.append(f"- **{label}:** `{_clean(obj.get(key),500)}`")
        if _cadence(obj):lines.append(f"- **Cadence intent:** `{_clean(_cadence(obj),200)}`")
        lines.append(f"- **Notification intent:** `{_notification(obj)}`")
        if obj.get('monitoring_signal_cadences'):lines+=['','**Signal-specific cadence:**']+[f"- {_clean(_signal(x),500)}" for x in obj.get('monitoring_signal_cadences') or []]
        if obj.get('monitoring_questions'):lines+=['',f"**Monitoring questions:** {_clean(obj.get('monitoring_questions'))}"]
        if obj.get('material_change_signals'):lines+=['',f"**Material-change signals:** {_clean(obj.get('material_change_signals'))}"]
        lines+=['','> Scheduling/execution is runtime state outside AURA; cadence and next-check fields do not prove a background task exists.']
    if obj.get('object_type')=='Asset':
        desc=describe_object(obj,path)
        if desc.get('artifact_reference'):lines.append(f"- **Location/artifact:** `{_clean(desc['artifact_reference'],300)}`")
        if desc.get('version'):lines.append(f"- **Version:** `{_clean(desc['version'],120)}`")
        if desc.get('purpose'):lines.append(f"- **Business role:** `{_clean(desc['purpose'],300)}`")
    if obj.get('object_type')=='ChangeEvent':
        if obj.get('change_kind'):lines.append(f"- **Change kind:** `{obj.get('change_kind')}`")
        if obj.get('target_refs'):lines.append(f"- **Target refs:** `{_clean(obj.get('target_refs'),500)}`")
        before=obj.get('before_state') if isinstance(obj.get('before_state'),dict) else {}
        after=obj.get('after_state') if isinstance(obj.get('after_state'),dict) else {}
        for key in sorted(set(before)|set(after)):
            lines.append(f"- **Changed field `{key}`:** {_clean(before.get(key),300) or '(none)'} → {_clean(after.get(key),300) or '(none)'}")
        details=obj.get('change_details')
        if isinstance(details,list) and details:
            lines+=['','**Canonical records possibly impacted by this change:**']
            for row in details:
                if not isinstance(row,dict):lines.append(f'- {_clean(row,400)}');continue
                lines.append(f"- `{row.get('object_ref')}` ({row.get('object_type')}) — `{_clean(row.get('path'),220)}` — relationship `{row.get('relationship')}` — review status `{row.get('review_status')}`")
            lines+=['','> Review status is what the record says; regenerating this view does not review or clear recorded impacts.']
    for key,label in [('statement','Statement'),('summary','Summary'),('conclusion','Conclusion'),('recommended_decision','Recommended decision'),('purpose','Purpose')]:
        if obj.get(key):lines+=['',f"**{label}:** {_clean(obj.get(key))}"]
    return '\n'.join(lines)+'\n'

def _tracked_subjects(vals):
    groups={}
    for obj,path in vals:groups.setdefault(obj.get('subject_key') or obj.get('id'),[]).append((obj,path))
    blocks=[]
    for key,items in sorted(groups.items(),key=lambda kv:_title(kv[1][0][0]).lower()):
        first=items[0][0];name=first.get('subject_name') or first.get('display_name') or key;subject_kinds=list(dict.fromkeys(x.get('subject_kind') for x,_ in items if x.get('subject_kind')));relationships=list(dict.fromkeys(r for x,_ in items for r in (x.get('subject_relationships') or [])));questions=list(dict.fromkeys(q for x,_ in items for q in (x.get('monitoring_questions') or [])));signals=list(dict.fromkeys(q for x,_ in items for q in (x.get('material_change_signals') or [])));cadences=list(dict.fromkeys(_cadence(x) for x,_ in items if _cadence(x)));notifications=list(dict.fromkeys(_notification(x) for x,_ in items));nexts=sorted([x.get('next_check_at') for x,_ in items if x.get('next_check_at')]+[s.get('next_check_at') for x,_ in items for s in (x.get('monitoring_signal_cadences') or []) if s.get('next_check_at')])
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
    typ=obj.get('object_type')
    system=_type_systems().get(typ)
    if system in SYSTEM_PAGES:return SYSTEM_PAGES[system]
    if typ=='Learning':return 'Learning'
    if typ=='SourceProfile':return 'Tracked-Subjects'
    if typ in BUSINESS_TYPES:return 'Business'
    if typ in PRIORITY_TYPES:return 'Priorities'
    if typ in EXPERIMENT_TYPES:return 'Experiments'
    if obj.get('domain') in SYSTEM_PAGES:return SYSTEM_PAGES[obj['domain']]
    if typ in EVIDENCE_TYPES:return 'Evidence'
    if typ in OPERATIONS_TYPES:return 'Operations'
    return 'Operations'
def _frontmatter(business_id,title,generated_at,count):return f"---\naura_generated: true\ncanonical: false\nproduct: ViralTrac AURA\nbusiness_id: {business_id}\ntitle: {json.dumps(title)}\ngenerated_at: {generated_at}\nobject_count: {count}\n---\n\n"

def _canonical_fingerprint(objects,diagnostics,base):
    """Fingerprint the parsed snapshot actually rendered, not a later file read."""
    unreadable=[{'path':d.get('path'),'reason':str(d.get('reason'))} for d in diagnostics]
    rows=sorted((path.relative_to(base).as_posix(),json.dumps(obj,sort_keys=True,ensure_ascii=False)) for obj,path in objects)
    digest=hashlib.sha256(json.dumps(rows,ensure_ascii=False).encode('utf-8')).hexdigest()
    return (None if unreadable else digest),unreadable

def _new_stage_dir(kbase):
    return Path(tempfile.mkdtemp(prefix='_generated.staging-',dir=kbase))

def _verify_stage(stage,pages):
    """Read back every staged artifact before publishing; the swap only follows this."""
    for name in pages:
        p=stage/f'{name}.md'
        try:text=p.read_text(encoding='utf-8')
        except Exception as exc:raise RuntimeError(f'Staged knowledge page unreadable after write: {name} ({exc})') from exc
        if not text.startswith('---\n') or 'aura_generated: true' not in text.split('---')[1]:raise RuntimeError(f'Staged knowledge page missing generated frontmatter: {name}')
        if hashlib.sha256(text.encode('utf-8')).hexdigest()!=pages[name]:raise RuntimeError(f'Staged knowledge page content mismatch: {name}')
    state=json.loads((stage/STATE_FILE).read_text(encoding='utf-8'))
    if state.get('pages')!=pages:raise RuntimeError('Staged knowledge state does not match staged pages')
    if len(state.get('business_id',''))==0:raise RuntimeError('Staged knowledge state is incomplete')

def _swap_staged(stage,target):
    """Windows-safe directory replacement: the old directory is renamed aside first
    (rename requires an absent target), the staged directory takes its place, and any
    failure restores the previous view before reporting."""
    if target.exists():
        if not target.is_dir():raise ValueError(f'Existing knowledge layer path is not a directory: {storage_ref(target)}')
        backup=stage.with_name(stage.name+'.previous')
        os.rename(str(target),str(backup))
        try:os.rename(str(stage),str(target))
        except OSError as exc:
            try:os.rename(str(backup),str(target))
            except OSError as restore_exc:
                raise OSError(f'Knowledge layer swap failed ({exc}) and the previous view could not be restored from {storage_ref(backup)}: {restore_exc}') from exc
            raise ValueError(f'Knowledge layer swap failed; the previous view was restored: {exc}') from exc
        try:shutil.rmtree(backup)
        except OSError as exc:return {'retained_backup':storage_ref(backup),'reason':str(exc)}
    else:os.rename(str(stage),str(target))

def _state_payload(business_id,generated_at,object_count,pages,fingerprint,render_fingerprint):
    return {'format_version':STATE_FORMAT_VERSION,'business_id':business_id,'generated_at':generated_at,'object_count':object_count,'pages':pages,'fingerprint':fingerprint,'render_fingerprint':render_fingerprint,'generator':'scripts/generate_knowledge_layer.py'}

def generate(business_id):
    global _TYPE_SYSTEMS
    _TYPE_SYSTEMS=None
    render_fingerprint=_render_fingerprint()
    base=instance_dir(business_id)
    if not base.exists():raise ValueError(f'Unknown business: {business_id}')
    if workspace_profile().get('knowledge_enabled') is False:raise ValueError('Human knowledge layer is disabled for the active workspace')
    kbase=knowledge_root()/business_id;generated=kbase/'_generated';notes=kbase/'notes'
    kbase.mkdir(parents=True,exist_ok=True);notes.mkdir(parents=True,exist_ok=True)
    diagnostics=[]
    objects=list(iter_instance_objects(business_id,diagnostics=diagnostics))
    fingerprint,unreadable=_canonical_fingerprint(objects,diagnostics,base)
    if unreadable:
        rows='; '.join(f"{d['path']}: {d['reason']}" for d in unreadable)
        raise ValueError(f'Refusing to publish knowledge layer: {len(unreadable)} unreadable canonical record(s) ({rows}); the previous generated view was left unchanged')
    ts=now();grouped={name:[] for name,_ in PAGES}
    for obj,path in objects:grouped[_page_for(obj)].append((obj,path))
    stage=_new_stage_dir(kbase)
    try:
        pages={}
        for name,description in PAGES:
            vals=sorted(grouped[name],key=lambda x:(x[0].get('object_type',''),_title(x[0]),x[0].get('id','')))
            body=_frontmatter(business_id,name,ts,len(vals))+f"# {name}\n\n{description}\n\n> Generated view only. Canonical AURA truth remains under `instances/{business_id}/`. Human edits here may be overwritten.\n\n"
            body+=_tracked_subjects(vals) if name=='Tracked-Subjects' else ('\n'.join(_entry(obj,path) for obj,path in vals) if vals else '_No current records._\n')
            (stage/f'{name}.md').write_text(body,encoding='utf-8')
            pages[name]=hashlib.sha256(body.encode('utf-8')).hexdigest()
        links='\n'.join(f'- [[{name}]] — {description}' for name,description in PAGES)
        home=_frontmatter(business_id,'Home',ts,len(objects))+f"# AURA Knowledge — {business_id}\n\nOrganization-owned human view generated from canonical AURA state.\n\n{links}\n\n## Human notes\n\nHuman-authored notes live in `../notes/` and are not canonical until deliberately incorporated with provenance.\n"
        (stage/'Home.md').write_text(home,encoding='utf-8');pages['Home']=hashlib.sha256(home.encode('utf-8')).hexdigest()
        state=_state_payload(business_id,ts,len(objects),pages,fingerprint,render_fingerprint)
        (stage/STATE_FILE).write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        _verify_stage(stage,pages)
        latest_diagnostics=[]
        latest=iter_instance_objects(business_id,latest_diagnostics)
        latest_fingerprint,_=_canonical_fingerprint(latest,latest_diagnostics,base)
        if latest_fingerprint!=fingerprint:raise ValueError('Canonical inputs changed during refresh; previous view retained. Retry against the current state.')
        if _render_fingerprint()!=render_fingerprint:raise ValueError('Rendering inputs changed during refresh; previous view retained.')
        status='updated' if generated.exists() else 'created'
        cleanup_warning=_swap_staged(stage,generated)
        return {'business_id':business_id,'status':status,'generated_root':str(generated),'state_file':storage_ref(generated/STATE_FILE),'page_count':len(PAGES)+1,'object_count':len(objects),'fingerprint':fingerprint,'cleanup_warning':cleanup_warning}
    except Exception:
        shutil.rmtree(stage,ignore_errors=True)
        raise

def knowledge_layer_freshness(business_id):
    """Read-only freshness report for enter/remember; never mutates the workspace.
    Returns {'business_id','generated','current','generated_at','object_count','fingerprint',
    'current_fingerprint','unreadable':[{'path','reason'}],'reason'} where reason is one of
    'unknown-business','missing','state-unreadable','page-incomplete','unreadable-canonical',
    'stale','stale-renderer','renderer-unreadable', or None when current."""
    report={'business_id':business_id,'generated':False,'current':False,'generated_at':None,'object_count':None,'fingerprint':None,'current_fingerprint':None,'unreadable':[],'reason':'missing'}
    base=instance_dir(business_id)
    if not base.exists():report['reason']='unknown-business';return report
    diagnostics=[]
    objects=list(iter_instance_objects(business_id,diagnostics=diagnostics))
    digest,unreadable=_canonical_fingerprint(objects,diagnostics,base)
    report['unreadable']=[{'path':d.get('path'),'reason':d.get('reason')} for d in unreadable]
    report['current_fingerprint']=digest
    state_path=(knowledge_root()/business_id/'_generated'/STATE_FILE)
    if not state_path.is_file():report['reason']='missing';return report
    try:
        state=json.loads(state_path.read_text(encoding='utf-8'))
        if not isinstance(state,dict) or not state.get('fingerprint') or state.get('business_id')!=business_id or state.get('format_version')!=STATE_FORMAT_VERSION:raise ValueError('state file identity or fingerprint is invalid')
    except (OSError,ValueError) as exc:
        report['generated']=True;report['reason']='state-unreadable';return report
    report['generated']=True
    report['generated_at']=state.get('generated_at')
    report['object_count']=state.get('object_count')
    report['fingerprint']=state.get('fingerprint')
    try:render_fingerprint=_render_fingerprint()
    except OSError:
        report['reason']='renderer-unreadable';return report
    if state.get('render_fingerprint')!=render_fingerprint:
        report['reason']='stale-renderer';return report
    pages=state.get('pages')
    if not isinstance(pages,dict) or set(pages)!={name for name,_ in PAGES}|{'Home'}:
        report['reason']='page-incomplete';return report
    for name in pages:
        try:
            text=(state_path.parent/f'{name}.md').read_text(encoding='utf-8')
            if hashlib.sha256(text.encode('utf-8')).hexdigest()!=pages[name]:report['reason']='page-incomplete';return report
        except (OSError,UnicodeError):report['reason']='page-incomplete';return report
    if unreadable:report['reason']='unreadable-canonical';return report
    if report['fingerprint']!=digest:report['reason']='stale';return report
    report['current']=True;report['reason']=None
    return report

def main():
    p=argparse.ArgumentParser(description='Generate a human-readable Markdown view of canonical AURA organization state.')
    p.add_argument('business_id')
    p.add_argument('--freshness',action='store_true',help='Report whether the existing generated view is current without regenerating it')
    a=p.parse_args()
    try:
        r=knowledge_layer_freshness(a.business_id) if a.freshness else generate(a.business_id)
    except (ValueError,RuntimeError) as e:raise SystemExit(str(e))
    print(json.dumps(r,indent=2,ensure_ascii=False))
if __name__=='__main__':main()