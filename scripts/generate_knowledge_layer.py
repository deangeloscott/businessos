#!/usr/bin/env python3
"""Generate an Obsidian/Markdown-friendly human view from canonical BusinessOS state."""
from _common import *
import argparse,json,shutil

PAGES=[
    ('Business','Business, Brand, products, offers, markets, audiences and other durable context.'),
    ('Priorities','Objectives, opportunities, initiatives, work requests and active attention.'),
    ('Learning','Current BusinessOS Learning and its maturity/status.'),
    ('Experiments','Experiments, outcome evaluations and measured learning state.'),
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
    for key in ['name','title','statement','conclusion','task','display_name','id']:
        if obj.get(key): return _clean(obj[key],160)
    return obj.get('object_type','Object')


def _entry(obj,path):
    oid=obj.get('id','(no id)'); typ=obj.get('object_type','Object'); title=_title(obj)
    lines=[f"### {title}",f"- **Type:** `{typ}`",f"- **ID:** `{oid}`"]
    for label,key in [('Owner','owner_system'),('Status','status'),('Maturity','maturity'),('Scope','owner_scope')]:
        if obj.get(key) is not None: lines.append(f"- **{label}:** `{_clean(obj.get(key),120)}`")
    if obj.get('confidence') is not None: lines.append(f"- **Confidence:** `{obj.get('confidence')}`")
    lines.append(f"- **Canonical source:** `{storage_ref(path)}`")
    for key,label in [('statement','Statement'),('conclusion','Conclusion'),('recommended_decision','Recommended decision'),('purpose','Purpose')]:
        if obj.get(key): lines += ['',f"**{label}:** {_clean(obj.get(key))}"]
    return '\n'.join(lines)+'\n'


def _page_for(obj):
    typ=obj.get('object_type'); owner=obj.get('owner_system')
    if typ=='Learning': return 'Learning'
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
    return f"---\nbusinessos_generated: true\ncanonical: false\nbusiness_id: {business_id}\ntitle: {json.dumps(title)}\ngenerated_at: {generated_at}\nobject_count: {count}\n---\n\n"


def generate(business_id):
    base=instance_dir(business_id)
    if not base.exists(): raise ValueError(f'Unknown business: {business_id}')
    profile=workspace_profile()
    if profile.get('knowledge_enabled') is False: raise ValueError('Human knowledge layer is disabled for the active workspace')
    kbase=knowledge_root()/business_id; generated=kbase/'_generated'; notes=kbase/'notes'
    kbase.mkdir(parents=True,exist_ok=True);notes.mkdir(parents=True,exist_ok=True)
    if generated.exists(): shutil.rmtree(generated)
    generated.mkdir(parents=True)
    ts=now(); grouped={name:[] for name,_ in PAGES}
    objects=iter_instance_objects(business_id)
    for obj,path in objects: grouped[_page_for(obj)].append((obj,path))
    for name,description in PAGES:
        vals=sorted(grouped[name],key=lambda x:(x[0].get('object_type',''),_title(x[0]),x[0].get('id','')))
        body=_frontmatter(business_id,name,ts,len(vals))+f"# {name}\n\n{description}\n\n> Generated view only. Canonical BusinessOS truth remains under `instances/{business_id}/`. Human edits here may be overwritten.\n\n"
        body += '\n'.join(_entry(obj,path) for obj,path in vals) if vals else '_No current canonical objects in this view._\n'
        (generated/f'{name}.md').write_text(body)
    links='\n'.join(f"- [{name}](_generated/{name}.md) — {desc}" for name,desc in PAGES)
    home=_frontmatter(business_id,'Home',ts,len(objects))+f"# {business_id} — BusinessOS Knowledge\n\nThis is the human-facing view of the active BusinessOS workspace. It can be opened directly in Obsidian, VS Code, or any Markdown tool.\n\n**Canonical truth:** `instances/{business_id}/`  \n**Human notes:** `knowledge/{business_id}/notes/` (noncanonical until explicitly incorporated through BusinessOS governance)\n\n## Views\n{links}\n"
    (generated/'Home.md').write_text(home)
    readme=kbase/'README.md'
    if not readme.exists():
        readme.write_text(f"# {business_id} Knowledge\n\nStart with [`_generated/Home.md`](_generated/Home.md). Generated files are derived views and may be replaced on refresh. Put human-authored working notes in `notes/`; those notes are not canonical BusinessOS truth unless explicitly incorporated through normal evidence/truth workflows.\n")
    notes_readme=notes/'README.md'
    if not notes_readme.exists():
        notes_readme.write_text('# Human Notes\n\nWrite working notes here. These files are intentionally noncanonical. BusinessOS must not treat a note as verified business truth merely because it exists in this folder.\n')
    return {'business_id':business_id,'knowledge_root':str(kbase),'generated_root':str(generated),'canonical_object_count':len(objects),'pages':1+len(PAGES),'generated_at':ts}


def main():
    p=argparse.ArgumentParser();p.add_argument('business_id');p.add_argument('--json',action='store_true');a=p.parse_args()
    try:r=generate(a.business_id)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps(r,indent=2) if a.json else f"generated human knowledge: {r['pages']} pages from {r['canonical_object_count']} canonical objects -> {r['generated_root']}")

if __name__=='__main__':main()
