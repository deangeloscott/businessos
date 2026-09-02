#!/usr/bin/env python3
"""Build bounded organizational context for an explicitly selected AURA Workflow.

This retrieves useful durable organization state and the selected authored Workflow. It
does not inspect host tools, provider bindings, scheduler state, permissions, or runtime
inventories. The active model/harness decides how to accomplish the work using the best
available tools, Skills, resources, and execution approach.
"""
from _common import *
import argparse,json,os
from resolve_preferences import resolve_effective_preferences,_load_task_preferences


def _strings(value):
    if isinstance(value,str):yield value
    elif isinstance(value,list):
        for item in value:yield from _strings(item)
    elif isinstance(value,dict):
        for item in value.values():yield from _strings(item)

def _existing_material_path(raw,relative_to=None):
    if not isinstance(raw,str) or not raw.strip() or '://' in raw:return None
    value=raw.strip();candidates=[];p=Path(value).expanduser()
    if p.is_absolute():candidates.append(p)
    else:
        if relative_to is not None:candidates.append(Path(relative_to).parent/p)
        candidates.append(resolve_storage_ref(value))
    for candidate in candidates:
        try:resolved=candidate.resolve()
        except Exception:continue
        if resolved.exists() and resolved.is_file():return resolved
    return None

def _material_inputs(selected,idx,declared):
    related=dict(selected);frontier=list(selected);selected_ids=set(selected)
    for _ in range(2):
        following=[]
        for oid in frontier:
            obj,_=related[oid]
            for ref in refs_in_object(obj):
                if ref in related or ref not in idx:continue
                related[ref]=idx[ref];following.append(ref)
        frontier=following
    canonical=[];supplied_paths=[]
    for oid in sorted(related):
        obj,path=related[oid];canonical.append({'object_ref':oid,'object_type':obj.get('object_type'),'path':storage_ref(path),'relationship':'selected_context' if oid in selected_ids else 'provenance'})
        for raw in _strings({k:obj.get(k) for k in ('source_reference','location_reference') if obj.get(k)}):
            material=_existing_material_path(raw)
            if material and material not in supplied_paths:supplied_paths.append(material)
        ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
        for member in ext.get('source_members',[]) or []:
            if not isinstance(member,dict):continue
            material=_existing_material_path(member.get('reference'))
            if material and material not in supplied_paths:supplied_paths.append(material)
    for source in list(supplied_paths):
        if source.suffix.lower()!='.json':continue
        try:data=json.loads(source.read_text(encoding='utf-8'))
        except Exception:continue
        for raw in _strings(data):
            material=_existing_material_path(raw,source)
            if material and material not in supplied_paths:supplied_paths.append(material)
    return {'declared_evidence_inputs':list(declared or []),'canonical_inputs':canonical,'supplied_evidence_refs':[storage_ref(path) for path in supplied_paths]}

def _add(files,rel):
    if rel and rel not in files and (ROOT/rel).exists():files.append(rel)


def build_plan(business_id,workflow_id,focus=None,operator_ref=None,team_ref=None,role_ref=None,task_preferences=None,output_type=None,channel=None):
    focus=focus or [];match=next((x for x in load_registry().get('workflows',[]) if x.get('id')==workflow_id),None)
    if not match or match.get('type')!='workflow':raise ValueError('Unknown AURA Workflow')
    base=ROOT/'instances'/business_id
    if not base.exists():raise ValueError('Unknown business')
    owner=match.get('owner_system') or 'core';installed=installed_modules()
    if isinstance(task_preferences,(str,Path)):task_preferences=_load_task_preferences(str(task_preferences))
    operator_ref=operator_ref or os.environ.get('BUSINESSOS_OPERATOR_REF');team_ref=team_ref or os.environ.get('BUSINESSOS_TEAM_REF');role_ref=role_ref or os.environ.get('BUSINESSOS_ROLE_REF')
    prefs=resolve_effective_preferences(business_id,operator_ref,team_ref,role_ref,owner,workflow_id,output_type,channel,task_preferences)

    files=['CONTEXT.md','docs/operating-knowledge.md']
    if owner!='core':_add(files,f'systems/{owner}/DEFAULTS.md')
    cp=ROOT/match['path'];stop=(ROOT/f'systems/{owner}/contracts') if owner!='core' else (ROOT/'core/workflows');chain=[]
    for parent in cp.parents:
        if parent==stop:break
        defaults=parent/'DEFAULTS.md'
        if defaults.exists():chain.append(defaults.relative_to(ROOT).as_posix())
    for rel in reversed(chain):_add(files,rel)
    _add(files,match['path'])

    read_types={selector_type(x) for x in match.get('read_selectors',[])};write_types=set(match.get('write_types',[]));context_types=set(match.get('context_types',[]));combined=read_types|write_types
    if owner in {'content-synthesis','marketing-synthesis'} or {'BusinessClaim','Brand'} & combined:_add(files,'core/policies/active-business-truth.md');_add(files,'core/policies/context-provenance-and-claims.md')
    if {'SourceRecord','Observation','Insight','Learning','ProofRecord'} & combined:_add(files,'core/policies/evidence.md');_add(files,'core/policies/provenance.md')
    if {'SourceRecord','Observation','Insight'} & write_types:_add(files,'core/policies/research-evidence.md')
    if 'Opportunity' in write_types:_add(files,'core/policies/decision-grounding.md')
    if 'AttentionItem' in combined:_add(files,'core/policies/attention-lifecycle.md')
    if 'PlatformChange' in combined:_add(files,'core/policies/platform-intelligence.md')
    if owner=='seo-aeo' and 'Observation' in combined:_add(files,'core/policies/local-evidence.md')
    if workflow_id.startswith(('core.opportunity.','core.diagnosis.','core.coordination.')):_add(files,'core/policies/resource-aware-execution.md')

    idx=object_index(business_id);selectors=match.get('read_selectors',[]);selected={};queue=[]
    for oid in focus:
        if oid in idx:selected[oid]=idx[oid];queue.append(oid)
    seen=set(queue)
    for _ in range(2):
        nxt=[]
        for oid in queue:
            obj,_=idx[oid]
            for ref in refs_in_object(obj):
                if ref in seen or ref not in idx:continue
                robj,rpath=idx[ref]
                if robj.get('object_type') in context_types or any(object_matches(robj,s) for s in selectors):selected[ref]=(robj,rpath);nxt.append(ref);seen.add(ref)
        queue=nxt

    unresolved=[];optional_unavailable=[]
    if owner in {'content-synthesis','marketing-synthesis'}:context_types.add('BusinessClaim')
    for typ in sorted(context_types):
        candidates=[(o,p) for o,p in idx.values() if o.get('object_type')==typ and o.get('status') not in {'archived','superseded'}];already=any(o.get('object_type')==typ for o,_ in selected.values())
        if typ=='BusinessClaim' and not already:
            for obj,path in candidates:selected[obj['id']]=(obj,path)
        elif not already and len(candidates)==1:selected[candidates[0][0]['id']]=candidates[0]
        elif not already and len(candidates)>1:unresolved.append({'type':typ,'reason':'multiple candidates; resolve from request/focus rather than bulk-loading'})
        elif not already:unresolved.append({'type':typ,'reason':'not present in durable AURA context'})
    for sel in selectors:
        ns=normalize_selector(sel);source_owner=ns.get('owner_system')
        if source_owner and source_owner not in installed:optional_unavailable.append({**ns,'reason':f'optional module {source_owner} is not installed'});continue
        if any(object_matches(o,sel) for o,_ in selected.values()):continue
        candidates=[(o,p) for o,p in idx.values() if object_matches(o,sel) and o.get('status') not in {'archived','superseded'}]
        if len(candidates)==1:selected[candidates[0][0]['id']]=candidates[0]
        elif len(candidates)>1:unresolved.append({**ns,'reason':'multiple candidates; resolve from request/focus rather than bulk-loading'})
        else:unresolved.append({**ns,'reason':'not present in durable AURA context'})

    for applied in prefs.get('applied_profiles',[]):_add(files,applied.get('path'))
    if 'ProofRecord' in write_types or any(obj.get('object_type')=='ProofRecord' for obj,_ in selected.values()):_add(files,'core/policies/proof.md')
    for rel in match.get('references',[]):_add(files,rel)
    object_files=[]
    for oid,(obj,path) in selected.items():
        rel=path.relative_to(ROOT).as_posix()
        if rel not in object_files:object_files.append(rel)
    schema_registry=json.loads((ROOT/'generated/schema-registry.json').read_text());schema_paths={row.get('title'):row['path'] for row in schema_registry if row.get('title')};schema_files=[schema_paths[typ] for typ in sorted(write_types) if typ in schema_paths]
    for rel in schema_files+object_files:_add(files,rel)
    return {'version':os_version(),'business_id':business_id,'workflow_id':workflow_id,'focus_refs':focus,'operator_ref':operator_ref,'team_ref':team_ref,'role_ref':role_ref,'effective_preferences':prefs.get('effective_preferences',{}),'preference_profiles':[x.get('id') for x in prefs.get('applied_profiles',[])],'preference_conflicts':prefs.get('conflicts',[]),'files':files,'object_refs':sorted(selected),'object_files':object_files,'schema_files':schema_files,'unresolved_selectors':unresolved,'optional_unavailable_selectors':optional_unavailable,'evidence_inputs':match.get('evidence_inputs',[]),'material_inputs':_material_inputs(selected,idx,match.get('evidence_inputs',[])),'execution_rule':'The Workflow describes the outcome, procedure, evidence, and quality requirements. The active model/harness chooses the best available tools, external Skills, providers, orchestration, and implementation details.'}


def main():
    p=argparse.ArgumentParser(description='Build bounded organizational context for an explicitly selected AURA Workflow.');p.add_argument('business_id');p.add_argument('workflow_id');p.add_argument('--focus',action='append',default=[]);p.add_argument('--operator-ref');p.add_argument('--team-ref');p.add_argument('--role-ref');p.add_argument('--task-preferences');p.add_argument('--output-type');p.add_argument('--channel');a=p.parse_args();print(json.dumps(build_plan(a.business_id,a.workflow_id,a.focus,a.operator_ref,a.team_ref,a.role_ref,a.task_preferences,a.output_type,a.channel),indent=2,ensure_ascii=False))

if __name__=='__main__':main()
