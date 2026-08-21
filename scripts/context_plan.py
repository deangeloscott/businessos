#!/usr/bin/env python3
from _common import *
import argparse,json

def build_plan(business_id,contract_id,focus=None):
    focus=focus or []
    reg=load_registry();match=next((x for x in reg['contracts'] if x['id']==contract_id),None)
    if not match: raise ValueError('Unknown contract')
    base=ROOT/'instances'/business_id
    if not base.exists(): raise ValueError('Unknown business')
    files=['CONTEXT.md','core/DEFAULTS.md']
    optional_unavailable=[]
    installed=installed_modules()
    owner=match['owner_system']
    if owner!='core': files.append(f'systems/{owner}/DEFAULTS.md')
    cp=ROOT/match['path']; parents=list(cp.parents)
    stop=(ROOT/f'systems/{owner}/contracts') if owner!='core' else (ROOT/'core/contracts')
    chain=[]
    for parent in parents:
        if parent==stop: break
        d=parent/'DEFAULTS.md'
        if d.exists(): chain.append(str(d.relative_to(ROOT)))
    for x in reversed(chain):
        if x not in files: files.append(x)
    files.append(match['path'])

    read_types={selector_type(x) for x in match.get('read_selectors',[])}
    write_types=set(match.get('write_types',[]))
    policy=[]
    if {'SourceRecord','Observation','Insight','Learning','ProofRecord'} & (read_types|write_types): policy += ['core/policies/evidence.md','core/policies/provenance.md']
    policy += ['core/policies/business-isolation.md']
    required_caps=[c for c in match.get('capabilities',{}).get('required',[]) if c!='none']
    optional_caps=[c for c in match.get('capabilities',{}).get('optional',[]) if c!='none']
    all_caps=required_caps+optional_caps
    # Provider policy/config is resolved lazily only when a capability is missing; do not load it into every job.
    mutating_caps=[]
    for c in all_caps:
        if c.endswith(('.update','.publish','.send','.schedule')) or c in {'checkout.update','workflow.update','search.index.request','business.action.governed.execute'}: mutating_caps.append(c)
    # Load first-party companion policy only when an active ViralTrac binding is relevant to this job.
    # Event-plane setup/diagnosis also needs the policy when ViralTrac is connected through any existing capability,
    # because event capabilities may not have been synchronized/activated yet.
    companion_caps={c for c in all_caps if c.startswith('business.')}
    env_name=installation().get('default_environment') or 'local'
    bp=ROOT/'deployment/environments'/env_name/'capability-bindings.json'
    try:
        active=json.loads(bp.read_text()).get('bindings',[]) if bp.exists() else []
    except Exception:
        active=[]
    any_vt=any(b.get('enabled',True) and b.get('provider_id')=='viraltrac' for b in active)
    relevant_vt=any(b.get('enabled',True) and b.get('provider_id')=='viraltrac' and b.get('capability') in companion_caps for b in active)
    event_job=match.get('id','').startswith('core.monitoring.') and any(c.startswith('business.event.') for c in all_caps)
    if companion_caps and (relevant_vt or (event_job and any_vt)):
        policy += ['core/policies/viraltrac-native-companion.md']
    if {'browser.interact','email.read'} & set(all_caps):
        policy += ['core/policies/external-research-interaction.md','core/policies/context-reuse-and-question-minimization.md']
    if mutating_caps or {'ChangeEvent','Approval'} & write_types:
        policy += ['core/policies/change-control.md','core/policies/verification.md','core/policies/autonomy.md','core/policies/risk.md','core/policies/approval.md']
    elif match.get('risk') in {'medium','high','critical'}:
        policy += ['core/policies/autonomy.md','core/policies/risk.md','core/policies/approval.md']
    for x in policy:
        if x not in files and (ROOT/x).exists(): files.append(x)

    idx=object_index(business_id); selectors=match.get('read_selectors',[]); context_types=set(match.get('context_types',[]))
    selected={};queue=[]
    for rid in focus:
        if rid in idx:selected[rid]=idx[rid];queue.append(rid)
    seen=set(queue)
    for _ in range(2):
        nq=[]
        for rid in queue:
            obj,_=idx[rid]
            for ref in refs_in_object(obj):
                if ref in seen or ref not in idx:continue
                robj,rp=idx[ref]
                if robj.get('object_type') in context_types or any(object_matches(robj,s) for s in selectors):
                    selected[ref]=(robj,rp);nq.append(ref);seen.add(ref)
        queue=nq
    unresolved=[]
    for typ in sorted(context_types):
        candidates=[(o,p) for o,p in idx.values() if o.get('object_type')==typ and o.get('status') not in {'archived','superseded'}]
        already=any(o.get('object_type')==typ for o,_ in selected.values())
        if not already and len(candidates)==1:selected[candidates[0][0]['id']]=candidates[0]
        elif not already and len(candidates)>1:unresolved.append({'type':typ,'reason':'multiple candidates; provide focus/relationship'})
        elif not already and not candidates:unresolved.append({'type':typ,'reason':'not present in active business'})
    for sel in selectors:
        ns=normalize_selector(sel)
        source_owner=ns.get('owner_system')
        if source_owner and source_owner not in installed:
            optional_unavailable.append({**ns,'reason':f'optional module {source_owner} is not installed; use module-independence fallback'})
            continue
        already=any(object_matches(o,sel) for o,_ in selected.values())
        if already:continue
        candidates=[(o,p) for o,p in idx.values() if object_matches(o,sel) and o.get('status') not in {'archived','superseded'}]
        if len(candidates)==1:selected[candidates[0][0]['id']]=candidates[0]
        elif len(candidates)>1:unresolved.append({**normalize_selector(sel),'reason':'multiple candidates; resolve from focus/query, do not bulk-load'})
        else:unresolved.append({**normalize_selector(sel),'reason':'not present in active business'})
    if optional_unavailable or installation().get('standalone_distribution'):
        modpol='core/policies/module-independence.md'
        if modpol not in files and (ROOT/modpol).exists(): files.append(modpol)
    if 'ProofRecord' in write_types or any(obj.get('object_type')=='ProofRecord' for obj,_ in selected.values()):
        proof_policy='core/policies/proof.md'
        if proof_policy not in files and (ROOT/proof_policy).exists():files.append(proof_policy)
    if {'browser.interact','email.read'} & set(all_caps):
        rp=base/'config/external-research-profile.json'
        if rp.exists():
            rel=str(rp.relative_to(ROOT))
            if rel not in files: files.append(rel)
        op=ROOT/'deployment/operator-profile.json'
        if op.exists():
            rel=str(op.relative_to(ROOT))
            if rel not in files: files.append(rel)

    if event_job:
        for ep in [ROOT/'core/monitoring/event-consumer-profile.json', base/'config/reactive-monitoring.json']:
            if ep.exists():
                rel=str(ep.relative_to(ROOT))
                if rel not in files: files.append(rel)
        if any_vt:
            vp=ROOT/'core/providers/viraltrac/event-interoperability.json'
            if vp.exists():
                rel=str(vp.relative_to(ROOT))
                if rel not in files: files.append(rel)

    object_files=[]
    for oid,(obj,op) in selected.items():
        rel=str(op.relative_to(ROOT))
        if rel not in object_files:object_files.append(rel)
    sreg=json.loads((ROOT/'generated/schema-registry.json').read_text());spath={s.get('title'):s['path'] for s in sreg if s.get('title')}
    schema_files=[]
    for typ in sorted(write_types):
        if typ in spath:schema_files.append(spath[typ])
    for x in schema_files:
        if x not in files:files.append(x)
    for x in match.get('references',[]):
        if x not in files and (ROOT/x).exists():files.append(x)
    for x in object_files:
        if x not in files:files.append(x)
    return {'version':os_version(),'business_id':business_id,'contract_id':contract_id,'focus_refs':focus,'files':files,'object_refs':sorted(selected),'object_files':object_files,'schema_files':schema_files,'unresolved_selectors':unresolved,'optional_unavailable_selectors':optional_unavailable,'evidence_inputs':match.get('evidence_inputs',[]),'required_capabilities':required_caps,'optional_capabilities':optional_caps,'mutating_capabilities':mutating_caps}

def main():
    p=argparse.ArgumentParser();p.add_argument('business_id');p.add_argument('contract_id');p.add_argument('--focus',action='append',default=[]);p.add_argument('--output');a=p.parse_args()
    try:plan=build_plan(a.business_id,a.contract_id,a.focus)
    except ValueError as e:raise SystemExit(str(e))
    out=json.dumps(plan,indent=2)+'\n'
    if a.output:Path(a.output).write_text(out)
    else:print(out,end='')
if __name__=='__main__':main()
