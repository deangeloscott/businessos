#!/usr/bin/env python3
"""Finalize a selected AURA playbook Run through a deterministic, judgment-safe interface.

This helper composes playbook completion, provenance, evidence, validation, and optional
human-knowledge refresh. It never creates business evidence or decides what an artifact
means. Automatic evidence resolution is limited to exact Run/contract provenance and
structurally valid, mechanically unique roles; ambiguity leaves the Run incomplete.

General external-Skill, model-created, or ad-hoc work receipts do not use this contract
finalizer. They may be completed through the ordinary Run receipt path instead.
"""
from pathlib import Path
import argparse, json, os

from _common import *
from completion_evidence import contract_index, completion_spec, subcontract_manifest_errors, validate_evidence
from record_contract_completion import record_contract_completion
from complete_run import complete_run, snapshot_files, restore_files
from validate_business import validate_business
from generate_knowledge_layer import generate as generate_knowledge
from run_provenance import RUN_LINKABLE_TYPES
from artifact_readiness import summarize_readiness
from run_lifecycle import reconcile_run_lifecycle


ANCHOR_KINDS={'qa_record','detector_record','analysis_record','completion_record'}
IGNORED_RUN_ARTIFACTS={'effective-preferences.json'}


def _json(path):
    try:return json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception:return None


def _run_ref(business_id,run_id):return f'runtime/runs/{business_id}/{run_id}'


def _contract_ids(value):
    ids=set()
    if not isinstance(value,dict):return ids
    ext=value.get('extensions') if isinstance(value.get('extensions'),dict) else {}
    bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
    for raw in (value.get('contract_id'),ext.get('contract_id'),bos.get('contract_id'),bos.get('run_contract_id')):
        if isinstance(raw,str) and raw.strip():ids.add(raw.strip())
    for raw in bos.get('contract_chain') or []:
        if isinstance(raw,str) and raw.strip():ids.add(raw.strip())
    nested=value.get('analysis_record')
    if isinstance(nested,dict):ids.update(_contract_ids(nested))
    return ids


def _is_run_linked(obj,business_id,run_id):
    if not isinstance(obj,dict):return False
    ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
    bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
    lineage=obj.get('lineage') if isinstance(obj.get('lineage'),list) else []
    rr=_run_ref(business_id,run_id)
    return bos.get('run_id')==run_id or bos.get('run_ref')==rr or run_id in lineage or rr in lineage


def _record_kind(data):
    value=data.get('analysis_record') if isinstance(data,dict) and isinstance(data.get('analysis_record'),dict) else data
    if not isinstance(value,dict):return 'supporting_record'
    status=str(value.get('status','')).lower();result=str(value.get('result','')).lower()
    checks=value.get('checks_performed',value.get('checks'))
    if result in {'no_finding','no_material_finding','no_opportunity','no_material_opportunity'}:return 'detector_record'
    if status in {'pass','passed'} and checks:return 'qa_record'
    if all(k in value for k in ('method','evidence_sample','findings','limitations','recommended_actions')):return 'analysis_record'
    if status in {'completed','complete','no_finding'}:return 'completion_record'
    return 'supporting_record'


def _candidate(ref,path,kind,contract_ids=None,object_type=None):
    return {'ref':ref,'path':Path(path),'kind':kind,'contract_ids':set(contract_ids or []),'object_type':object_type}


def _run_candidates(business_id,run_id):
    """Return canonical Run-linked outputs and contract-labelled Run artifacts."""
    out=[]
    for obj,path in iter_instance_objects(business_id):
        if not _is_run_linked(obj,business_id,run_id):continue
        ids=_contract_ids(obj);ref=storage_ref(path);typ=obj.get('object_type')
        out.append(_candidate(ref,path,'canonical',ids,typ))
        if typ=='Asset' and isinstance(obj.get('location_reference'),str):
            loc=resolve_storage_ref(obj['location_reference'])
            if loc.exists() and loc.is_file():out.append(_candidate(storage_ref(loc),loc,'asset_location',ids,typ))
    artifacts=run_dir_path(business_id,run_id)/'artifacts'
    if artifacts.exists():
        for path in sorted(p for p in artifacts.rglob('*') if p.is_file() and p.name not in IGNORED_RUN_ARTIFACTS):
            data=_json(path);ids=_contract_ids(data)
            if not ids:continue
            out.append(_candidate(storage_ref(path),path,_record_kind(data),ids))
    dedup={}
    for row in out:
        key=(row['ref'],row['kind'])
        if key in dedup:dedup[key]['contract_ids'].update(row['contract_ids'])
        else:dedup[key]=row
    return list(dedup.values())


def _required_run_linked_refs(candidates):
    """Return canonical refs that a linked playbook receipt must index before completion."""
    return list(dict.fromkeys(
        row['ref'] for row in candidates
        if row.get('kind')=='canonical' and row.get('object_type') in RUN_LINKABLE_TYPES
    ))


def _normalize_refs(refs):
    out=[]
    for raw in refs or []:
        path=resolve_storage_ref(raw)
        if not path.exists() or not path.is_file():raise ValueError(f'Evidence path does not resolve to an existing file: {raw}')
        ref=storage_ref(path)
        if ref not in out:out.append(ref)
    return out


def _evidence_resolution(contract,manifest,business_id,run_id,phase,candidates,explicit=None):
    cid=contract.get('id')
    if explicit:
        try:refs=_normalize_refs(explicit)
        except ValueError as e:return {'status':'invalid_or_incomplete_evidence','contract_id':cid,'reason':str(e),'candidate_refs':[]}
        errors=validate_evidence(contract,refs,business_id,run_id,phase=phase,manifest=manifest)
        if errors:return {'status':'invalid_or_incomplete_evidence','contract_id':cid,'reason':'Supplied evidence does not satisfy the playbook completion profile.','errors':errors[:8],'candidate_refs':refs}
        return {'status':'resolved','contract_id':cid,'refs':refs,'resolution':'explicit'}

    exact=[x for x in candidates if cid in x['contract_ids']]
    if exact:
        anchors=[x for x in exact if x['kind'] in ANCHOR_KINDS]
        by_kind={kind:[x for x in anchors if x['kind']==kind] for kind in ANCHOR_KINDS}
        ambiguous=[rows for rows in by_kind.values() if len(rows)>1]
        deliverables=[x for x in exact if x['kind']=='asset_location']
        if ambiguous or (phase=='root' and len(deliverables)>1):
            rows=[x for group in ambiguous for x in group]
            if phase=='root' and len(deliverables)>1:rows.extend(deliverables)
            refs=list(dict.fromkeys(x['ref'] for x in rows))
            return {
                'status':'needs_judgment','contract_id':cid,
                'reason':'Multiple plausible completion records or root deliverables satisfy the same semantic role; AURA will not choose between them.',
                'candidate_refs':refs,
                'needed':'Provide the intended evidence explicitly with --evidence for the root or --contract-evidence CONTRACT_ID=REF for the subcontract.'
            }
        refs=list(dict.fromkeys(x['ref'] for x in exact))
        errors=validate_evidence(contract,refs,business_id,run_id,phase=phase,manifest=manifest)
        if not errors:return {'status':'resolved','contract_id':cid,'refs':refs,'resolution':'exact_run_contract_provenance'}
        return {'status':'invalid_or_incomplete_evidence','contract_id':cid,'reason':'Exact Run/contract-linked evidence exists but does not satisfy the completion profile.','errors':errors[:8],'candidate_refs':refs}

    # A fallback is safe only when one individual Run-linked artifact uniquely satisfies
    # the declared role. Do not search scratch files or combine semantic guesses.
    valid=[]
    for row in candidates:
        if row['kind']=='supporting_record':continue
        if not validate_evidence(contract,[row['ref']],business_id,run_id,phase=phase,manifest=manifest):valid.append(row)
    if len(valid)==1:
        return {'status':'resolved','contract_id':cid,'refs':[valid[0]['ref']],'resolution':'unique_structural_run_link'}
    if len(valid)>1:
        return {
            'status':'needs_judgment','contract_id':cid,
            'reason':'Multiple Run-linked artifacts could satisfy this completion role; AURA will not select one arbitrarily.',
            'candidate_refs':[x['ref'] for x in valid],
            'needed':'Provide the intended evidence explicitly.'
        }
    return {
        'status':'invalid_or_incomplete_evidence','contract_id':cid,
        'reason':'No exact or mechanically unique Run-linked evidence satisfies the completion profile.',
        'candidate_refs':[],'needed':'Persist the real playbook result/evidence or provide its existing storage reference explicitly.'
    }


def _resolve_run(business_id,run_id=None):
    root=runtime_root()/'runs'/business_id
    explicit=run_id or os.environ.get('BUSINESSOS_RUN_ID')
    if explicit:
        rp=root/explicit/'run.json'
        if not rp.exists():return {'status':'needs_judgment','reason':f'Run does not exist for business {business_id}: {explicit}','candidate_run_ids':[]}
        data=_json(rp)
        if not isinstance(data,dict) or data.get('business_id')!=business_id or data.get('run_id')!=explicit:
            return {'status':'needs_judgment','reason':'Run identity does not match the requested business/Run.','candidate_run_ids':[explicit]}
        return {'status':'resolved','run_id':explicit,'run':data}
    active=[]
    if root.exists():
        for rp in root.glob('*/run.json'):
            data=_json(rp)
            if isinstance(data,dict) and data.get('business_id')==business_id and data.get('status')=='active':active.append(data)
    if len(active)==1:return {'status':'resolved','run_id':active[0]['run_id'],'run':active[0]}
    if not active:return {'status':'needs_judgment','reason':'No active Run is uniquely available; provide the Run ID explicitly.','candidate_run_ids':[]}
    return {'status':'needs_judgment','reason':'Multiple active Runs exist; AURA will not guess which work receipt to finalize.','candidate_run_ids':sorted(x['run_id'] for x in active)}


def _knowledge_result(business_id,refresh):
    if not refresh:return {'status':'skipped'}
    if workspace_profile().get('knowledge_enabled') is False:return {'status':'disabled'}
    try:
        result=generate_knowledge(business_id)
        return {'status':'refreshed','human_start_ref':storage_ref(result['human_start']),'generated_root_ref':storage_ref(result['generated_root']),'canonical_object_count':result['canonical_object_count'],'pages':result['pages']}
    except Exception as e:return {'status':'warning','reason':str(e),'rule':'Canonical Run completion remains valid; the derived human view can be regenerated safely.'}


def _concise_validation(result):
    validation=result.get('validation') or {};warnings=validation.get('warnings') or []
    return {'status':'clean','error_count':0,'warning_count':len(warnings),'warnings':warnings[:5],'canonical_object_counts':validation.get('canonical_object_counts',{})}


def _completion_scope(business_id,run_id,manifest,candidates,run_completed):
    contracts=contract_index();root=contracts.get(manifest.get('root_contract_id'),{});assets=[]
    for row in candidates:
        if root.get('artifact_role')!='customer_facing_production_root':continue
        if row.get('kind')!='canonical' or row.get('object_type')!='Asset':continue
        asset=_json(row['path'])
        if not isinstance(asset,dict):continue
        ext=asset.get('extensions') if isinstance(asset.get('extensions'),dict) else {}
        bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
        if bos.get('customer_facing',True) is False:continue
        assets.append((asset,row['ref']))
    qa=[]
    for cid in manifest.get('required_subcontracts') or []:
        if completion_spec(contracts.get(cid,{'id':cid})).get('profile')!='qa':continue
        step=(manifest.get('contracts') or {}).get(cid) or {}
        for ref in step.get('evidence_refs') or []:
            data=_json(resolve_storage_ref(ref))
            if not isinstance(data,dict) or data.get('contract_id')!=cid:continue
            raw=next((data.get(k) for k in ('tested_asset','target_asset','asset_ref','target_ref') if data.get(k)),None)
            version=next((data.get(k) for k in ('tested_version','asset_version','version') if data.get(k) is not None),None)
            qa.append({'contract_id':cid,'status':str(data.get('status','')).lower(),'tested_asset':raw,'tested_version':str(version) if version is not None else None,'scope':'artifact_version_qa','artifact_qa_blockers':data.get('blockers',[])})
    return summarize_readiness(assets,qa,run_completed)


def _failure_for_evidence(failure,business_id,run_id):
    return {
        'format_version':'1.0','status':failure.get('status'),
        'category':'semantic_or_evidence_judgment' if failure.get('status')=='needs_judgment' else 'invalid_or_incomplete_evidence',
        'business_id':business_id,'run_id':run_id,'run_status':'active','issue':failure
    }


def finalize_run(business_id=None,run_id=None,root_evidence=None,contract_evidence=None,workspace=None,refresh_human_knowledge=True):
    if workspace:os.environ['BUSINESSOS_WORKSPACE']=str(Path(workspace).expanduser().resolve())
    resolved_business=resolve_business(business_id)
    if resolved_business.get('status')!='resolved':
        return {'format_version':'1.0','status':'needs_judgment','category':'business_resolution','workspace':str(workspace_root()),**{k:v for k,v in resolved_business.items() if k!='status'}}
    bid=resolved_business['business_id'];run_resolution=_resolve_run(bid,run_id)
    if run_resolution.get('status')!='resolved':return {'format_version':'1.0','status':'needs_judgment','category':'run_resolution','business_id':bid,**{k:v for k,v in run_resolution.items() if k!='status'}}
    rid=run_resolution['run_id'];run=run_resolution['run'];rd=run_dir_path(bid,rid);mp=rd/'contract-execution.json';rp=rd/'run.json'
    method=run.get('method_type') or ('aura_playbook' if run.get('contract_id') else 'ad_hoc')
    if method!='aura_playbook':
        return {
            'format_version':'1.0','status':'needs_judgment','category':'method_not_applicable',
            'business_id':bid,'run_id':rid,
            'reason':'finalize_run.py applies only to a selected AURA playbook Run. Complete general external-Skill, model-created, or ad-hoc work through the ordinary work-receipt completion path.'
        }
    if not mp.exists():return {'format_version':'1.0','status':'invalid_or_incomplete_evidence','category':'invalid_run_state','business_id':bid,'run_id':rid,'reason':'AURA playbook Run contract-execution manifest is missing.'}
    manifest=_json(mp)
    if not isinstance(manifest,dict) or manifest.get('business_id')!=bid or manifest.get('run_id')!=rid:
        return {'format_version':'1.0','status':'invalid_or_incomplete_evidence','category':'invalid_run_state','business_id':bid,'run_id':rid,'reason':'Run contract-execution manifest identity is invalid.'}
    contracts=contract_index();root_id=manifest.get('root_contract_id');root=contracts.get(root_id)
    if not root:return {'format_version':'1.0','status':'invalid_or_incomplete_evidence','category':'invalid_run_state','business_id':bid,'run_id':rid,'reason':f'Installed root contract metadata is missing: {root_id!r}'}
    supplied={k:list(v) for k,v in (contract_evidence or {}).items()}
    allowed=set(manifest.get('required_subcontracts') or [])|{root_id};unknown=sorted(set(supplied)-allowed)
    if unknown:return {'format_version':'1.0','status':'needs_judgment','category':'evidence_mapping','business_id':bid,'run_id':rid,'reason':'Evidence was mapped to contracts that are not the Run root or declared required subcontracts.','contract_ids':unknown}
    if root_id in supplied:root_evidence=list(root_evidence or [])+supplied.pop(root_id)

    if run.get('status')=='completed' or manifest.get('root_status')=='completed':
        sub_errors=subcontract_manifest_errors(manifest,bid,rid,contracts)
        root_errors=validate_evidence(root,manifest.get('root_evidence_refs') or [],bid,rid,phase='root',manifest=manifest)
        business_errors,warnings,counts=validate_business(bid)
        errors=sub_errors+root_errors+business_errors
        if errors:return {'format_version':'1.0','status':'invalid_or_incomplete_evidence','category':'invalid_completed_state','business_id':bid,'run_id':rid,'run_status':run.get('status'),'errors':errors[:12]}
        candidates=_run_candidates(bid,rid);knowledge=_knowledge_result(bid,refresh_human_knowledge)
        reconciliation=reconcile_run_lifecycle(bid,rid,apply_safe_supersession=True)
        repairs=[{'operation':'supersede_mechanically_redundant_run','run_id':x.get('run_id'),'resolution':'explicit_exact_replacement_without_material_work'} for x in reconciliation.get('mechanically_superseded_runs',[])]
        return {'format_version':'1.0','status':'completed','category':'mechanically_repaired' if repairs else 'mechanically_clean','business_id':bid,'run_id':rid,'run_ref':storage_ref(rd),'root_contract_id':root_id,'completion_scope':_completion_scope(bid,rid,manifest,candidates,True),'run_reconciliation':reconciliation,'validation':{'status':'clean','error_count':0,'warning_count':len(warnings),'warnings':warnings[:5],'canonical_object_counts':counts},'human_knowledge':knowledge,'automatic_repairs':repairs}

    candidates=_run_candidates(bid,rid);plans=[]
    for cid in manifest.get('required_subcontracts') or []:
        step=(manifest.get('contracts') or {}).get(cid) or {};contract=contracts.get(cid)
        if not contract:return {'format_version':'1.0','status':'invalid_or_incomplete_evidence','category':'invalid_run_state','business_id':bid,'run_id':rid,'reason':f'Installed subcontract metadata is missing: {cid!r}'}
        if step.get('status')=='completed':
            resolution=_evidence_resolution(contract,manifest,bid,rid,'subcontract',candidates,step.get('evidence_refs') or [])
            resolution['already_recorded']=True
        else:resolution=_evidence_resolution(contract,manifest,bid,rid,'subcontract',candidates,supplied.get(cid))
        if resolution.get('status')!='resolved':return _failure_for_evidence(resolution,bid,rid)
        plans.append(resolution)
    required_run_refs=_required_run_linked_refs(candidates)
    explicit_root=list(root_evidence or [])
    effective_root=[*explicit_root,*required_run_refs] if explicit_root or required_run_refs else None
    root_resolution=_evidence_resolution(root,manifest,bid,rid,'root',candidates,effective_root)
    if root_resolution.get('status')!='resolved':return _failure_for_evidence(root_resolution,bid,rid)

    explicitly_normalized=[]
    if explicit_root:
        try:explicitly_normalized=_normalize_refs(explicit_root)
        except ValueError:pass
    mechanically_included=[ref for ref in required_run_refs if ref not in explicitly_normalized]
    if mechanically_included:
        root_resolution['resolution']='required_run_linked_completion_evidence'+('_plus_explicit' if explicit_root else '')
        root_resolution['mechanically_included_refs']=mechanically_included

    # Validate current organization/reference/evidence conditions before any completion
    # mutation. active_run_id defers only the facts that cannot be true until this
    # finalizer records evidence and completes the selected playbook receipt.
    business_errors,_,_=validate_business(bid,active_run_id=rid)
    if business_errors:
        return {
            'format_version':'1.0','status':'invalid_or_incomplete_evidence','category':'pre_finalization_validation_failed',
            'business_id':bid,'run_id':rid,'run_status':'active','mutation':'none',
            'errors':business_errors[:12],
            'deferred_integrity_conditions':['active Run completion status','final completion-evidence recording'],
            'needed':'Correct the reported organization/reference/evidence issue, then call finalize_run.py again.'
        }

    touched=[mp,rp]
    for row in candidates:touched.append(row['path'])
    for plan in plans+[root_resolution]:touched.extend(resolve_storage_ref(x) for x in plan.get('refs',[]))
    snapshots=snapshot_files(touched);repairs=[]
    if mechanically_included:
        repairs.append({'operation':'include_required_run_linked_evidence','evidence_refs':mechanically_included,'resolution':'comprehensive_exact_run_link'})
    try:
        for plan in plans:
            if plan.get('already_recorded'):continue
            record_contract_completion(bid,rid,plan['contract_id'],plan['refs'])
            repairs.append({'operation':'record_subcontract_completion','contract_id':plan['contract_id'],'evidence_refs':plan['refs'],'resolution':plan.get('resolution')})
        completed=complete_run(bid,rid,root_resolution['refs'])
        repairs.append({'operation':'complete_root_run','contract_id':root_id,'evidence_refs':completed.get('root_evidence_refs',[]),'resolution':root_resolution.get('resolution')})
        reconciliation=reconcile_run_lifecycle(bid,rid,apply_safe_supersession=True)
        repairs.extend({'operation':'supersede_mechanically_redundant_run','run_id':x.get('run_id'),'resolution':'explicit_exact_replacement_without_material_work'} for x in reconciliation.get('mechanically_superseded_runs',[]))
    except Exception as exc:
        restore_files(snapshots)
        return {
            'format_version':'1.0','status':'invalid_or_incomplete_evidence','category':'finalization_validation_failed',
            'business_id':bid,'run_id':rid,'run_status':'active','reason':str(exc),'rollback':'restored_pre_finalization_state',
            'automatic_repairs':[]
        }
    knowledge=_knowledge_result(bid,refresh_human_knowledge)
    return {
        'format_version':'1.0','status':'completed','category':'mechanically_repaired' if repairs else 'mechanically_clean',
        'business_id':bid,'workspace':str(workspace_root()),'run_id':rid,'run_ref':storage_ref(rd),'root_contract_id':root_id,
        'root_evidence_refs':completed.get('root_evidence_refs',[]),'required_subcontracts':completed.get('required_subcontracts',[]),
        'completion_scope':_completion_scope(bid,rid,_json(mp) or manifest,_run_candidates(bid,rid),True),'run_reconciliation':reconciliation,
        'automatic_repairs':repairs,'validation':_concise_validation(completed),'human_knowledge':knowledge,
        'rule':'AURA playbook Run completion proves the selected SOP/evidence completion state. Artifact QA, production readiness, deployment, real external constraints, and measured outcomes remain distinct facts.'
    }


def _contract_evidence(values):
    out={}
    for raw in values or []:
        if '=' not in raw:raise ValueError('--contract-evidence requires CONTRACT_ID=STORAGE_REF')
        cid,ref=raw.split('=',1);cid=cid.strip();ref=ref.strip()
        if not cid or not ref:raise ValueError('--contract-evidence requires non-empty CONTRACT_ID=STORAGE_REF')
        out.setdefault(cid,[]).append(ref)
    return out


def main():
    ap=argparse.ArgumentParser(description='Finalize a selected AURA playbook Run. Ambiguous or semantic evidence is never silently selected.')
    ap.add_argument('business_id',nargs='?',help='Defaults to BUSINESSOS_BUSINESS_ID or the only initialized workspace business')
    ap.add_argument('run_id',nargs='?',help='Defaults to BUSINESSOS_RUN_ID or the only active Run for the business')
    ap.add_argument('--workspace',help='Optional organization workspace root')
    ap.add_argument('--evidence',action='append',default=[],help='Explicit root evidence storage reference; repeat as needed')
    ap.add_argument('--contract-evidence',action='append',default=[],metavar='CONTRACT_ID=REF',help='Explicit evidence for an ambiguous required subcontract; repeat as needed')
    ap.add_argument('--skip-human-knowledge',action='store_true',help='Do not refresh the optional derived human knowledge view')
    a=ap.parse_args()
    try:result=finalize_run(a.business_id,a.run_id,a.evidence,_contract_evidence(a.contract_evidence),a.workspace,not a.skip_human_knowledge)
    except (ValueError,json.JSONDecodeError) as e:result={'format_version':'1.0','status':'invalid_or_incomplete_evidence','category':'invalid_request','reason':str(e)}
    print(json.dumps(result,indent=2,ensure_ascii=False))
    raise SystemExit(0 if result.get('status')=='completed' else 2)


if __name__=='__main__':main()
