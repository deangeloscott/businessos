#!/usr/bin/env python3
"""Finalize a non-AURA-playbook Run as an organization-owned work receipt.

This is continuity, not contract certification. It preserves material evidence, results,
decisions, unresolved work, and a concise summary without inventing an AURA SOP execution.
AURA playbook Runs continue to use finalize_run.py so their selected SOP conformance is
verified separately.
"""
from pathlib import Path
import argparse, json, os
from jsonschema import Draft202012Validator

from _common import *
from run_provenance import bind_evidence_paths
from validate_business import validate_business
from generate_knowledge_layer import generate as generate_knowledge


def _json(path):
    try:return json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception:return None


def _resolve_run(business_id,run_id=None):
    root=runtime_root()/'runs'/business_id
    explicit=run_id or os.environ.get('BUSINESSOS_RUN_ID')
    if explicit:
        rp=root/explicit/'run.json'
        if not rp.exists():return None,None,f'Run does not exist for business {business_id}: {explicit}'
        data=_json(rp)
        if not isinstance(data,dict) or data.get('business_id')!=business_id or data.get('run_id')!=explicit:
            return None,None,'Run identity does not match the requested business/Run.'
        return explicit,data,None
    active=[]
    if root.exists():
        for rp in root.glob('*/run.json'):
            data=_json(rp)
            if isinstance(data,dict) and data.get('business_id')==business_id and data.get('status')=='active':active.append(data)
    if len(active)==1:return active[0]['run_id'],active[0],None
    if not active:return None,None,'No active Run is uniquely available.'
    return None,None,'Multiple active Runs exist; provide the Run ID explicitly.'


def _normalize_ref(business_id,raw):
    if not isinstance(raw,str) or not raw.strip():raise ValueError('References must be non-empty strings')
    raw=raw.strip();idx=object_index(business_id)
    if raw in idx:return storage_ref(idx[raw][1])
    path=resolve_storage_ref(raw)
    if not path.exists() or not path.is_file():raise ValueError(f'Reference does not resolve to an existing file or canonical object: {raw}')
    return storage_ref(path)


def _normalize_refs(business_id,values):
    out=[]
    for raw in values or []:
        ref=_normalize_ref(business_id,raw)
        if ref not in out:out.append(ref)
    return out


def _linked_refs(business_id,run_id):
    rr=f'runtime/runs/{business_id}/{run_id}';results=[];decisions=[]
    for obj,path in iter_instance_objects(business_id):
        ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
        bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
        lineage=obj.get('lineage') if isinstance(obj.get('lineage'),list) else []
        if not (bos.get('run_id')==run_id or bos.get('run_ref')==rr or run_id in lineage or rr in lineage):continue
        ref=storage_ref(path)
        target=decisions if obj.get('object_type')=='DecisionRecord' else results
        if ref not in target:target.append(ref)
    return sorted(results),sorted(decisions)


def _knowledge_result(business_id,refresh):
    if not refresh:return {'status':'skipped'}
    if workspace_profile().get('knowledge_enabled') is False:return {'status':'disabled'}
    try:
        result=generate_knowledge(business_id)
        return {'status':'refreshed','human_start_ref':storage_ref(result['human_start']),'generated_root_ref':storage_ref(result['generated_root']),'canonical_object_count':result['canonical_object_count'],'pages':result['pages']}
    except Exception as e:return {'status':'warning','reason':str(e),'rule':'The derived human view is optional and can be regenerated safely.'}


def _validate_run_schema(run):
    schema=json.loads((PRODUCT_ROOT/'core/schemas/runtime/run.schema.json').read_text())
    return [f'{list(e.path)}: {e.message}' for e in Draft202012Validator(schema).iter_errors(run)]


def finalize_work_receipt(business_id=None,run_id=None,evidence=None,results=None,decisions=None,unresolved=None,summary=None,workspace=None,refresh_human_knowledge=True):
    if workspace:os.environ['BUSINESSOS_WORKSPACE']=str(Path(workspace).expanduser().resolve())
    resolved=resolve_business(business_id)
    if resolved.get('status')!='resolved':return {'format_version':'1.0','status':'needs_judgment','category':'business_resolution',**resolved}
    bid=resolved['business_id'];rid,run,problem=_resolve_run(bid,run_id)
    if problem:return {'format_version':'1.0','status':'needs_judgment','category':'run_resolution','business_id':bid,'reason':problem}
    rd=run_dir_path(bid,rid);rp=rd/'run.json'
    method=run.get('method_type') or ('aura_playbook' if run.get('contract_id') else 'ad_hoc')
    if method=='aura_playbook':
        return {'format_version':'1.0','status':'needs_judgment','category':'wrong_finalizer','business_id':bid,'run_id':rid,'reason':'This Run selected an AURA playbook. Use scripts/finalize_run.py so the selected SOP conformance is verified.'}
    if (rd/'contract-execution.json').exists():
        return {'format_version':'1.0','status':'invalid_run_state','category':'fabricated_contract_execution','business_id':bid,'run_id':rid,'reason':'A non-AURA method Run must not carry contract-execution.json.'}

    if run.get('status')=='completed':
        errors,warnings,counts=validate_business(bid)
        if errors:return {'format_version':'1.0','status':'invalid_run_state','category':'invalid_completed_state','business_id':bid,'run_id':rid,'errors':errors[:12]}
        return {'format_version':'1.0','status':'completed','category':'already_completed','business_id':bid,'run_id':rid,'run_ref':storage_ref(rd),'method_type':method,'continuity':run.get('continuity',{}),'validation':{'errors':0,'warnings':warnings[:5],'canonical_object_counts':counts},'human_knowledge':_knowledge_result(bid,refresh_human_knowledge)}

    pre_errors,_,_=validate_business(bid,active_run_id=rid)
    if pre_errors:
        return {'format_version':'1.0','status':'invalid_or_incomplete_evidence','category':'pre_finalization_validation_failed','business_id':bid,'run_id':rid,'run_status':'active','mutation':'none','errors':pre_errors[:12]}

    try:
        evidence_refs=_normalize_refs(bid,evidence)
        result_refs=_normalize_refs(bid,results)
        decision_refs=_normalize_refs(bid,decisions)
    except ValueError as e:
        return {'format_version':'1.0','status':'invalid_request','category':'reference_resolution','business_id':bid,'run_id':rid,'reason':str(e)}

    # Explicit canonical refs may be the first durable binding for work produced outside an
    # AURA SOP. Bind them to the actual method Run, then collect every canonical result that
    # is already linked to the Run so the receipt is comprehensive without fabricating data.
    touched=[rp]
    for ref in [*evidence_refs,*result_refs,*decision_refs]:
        p=resolve_storage_ref(ref)
        if p.suffix.lower()=='.json' and p.exists():touched.append(p)
    snapshots={p:p.read_bytes() for p in dict.fromkeys(touched) if p.exists() and p.is_file()}
    try:
        bind_evidence_paths(bid,rid,[resolve_storage_ref(x) for x in [*evidence_refs,*result_refs,*decision_refs]],'work_receipt')
        linked_results,linked_decisions=_linked_refs(bid,rid)
        current=dict(run.get('continuity') or {})
        def merged(key,new):
            return list(dict.fromkeys([*(current.get(key) or []),*new]))
        ts=now();run['status']='completed';run['updated_at']=ts
        run['continuity']={
            'format_version':'2.0','purpose':'organizational_work_receipt','state':'completed',
            'method_type':method,'method_ref':run.get('method_ref'),'summary':summary if summary is not None else current.get('summary'),
            'evidence_refs':merged('evidence_refs',evidence_refs),
            'result_refs':merged('result_refs',[*result_refs,*linked_results]),
            'decision_refs':merged('decision_refs',[*decision_refs,*linked_decisions]),
            'unresolved':list(dict.fromkeys([*(current.get('unresolved') or []),*[x.strip() for x in (unresolved or []) if isinstance(x,str) and x.strip()]])),
            'completed_at':ts,'superseded_by_run_id':None
        }
        schema_errors=_validate_run_schema(run)
        if schema_errors:raise ValueError('Run schema invalid: '+'; '.join(schema_errors[:8]))
        rp.write_text(json.dumps(run,indent=2)+'\n')
        post_errors,warnings,counts=validate_business(bid)
        if post_errors:raise ValueError('active business validation is not clean: '+'; '.join(post_errors[:12]))
    except Exception as exc:
        for path,data in snapshots.items():path.write_bytes(data)
        return {'format_version':'1.0','status':'invalid_or_incomplete_evidence','category':'finalization_validation_failed','business_id':bid,'run_id':rid,'run_status':'active','reason':str(exc),'rollback':'restored_pre_finalization_state'}

    return {
        'format_version':'1.0','status':'completed','category':'work_receipt_completed','business_id':bid,'workspace':str(workspace_root()),
        'run_id':rid,'run_ref':storage_ref(rd),'method_type':method,'method_ref':run.get('method_ref'),'continuity':run['continuity'],
        'validation':{'errors':0,'warnings':warnings[:5],'canonical_object_counts':counts},
        'human_knowledge':_knowledge_result(bid,refresh_human_knowledge),
        'rule':'This receipt proves only what AURA durably recorded about the work. It does not fabricate AURA SOP conformance, external execution, production readiness, or business outcomes.'
    }


def main():
    ap=argparse.ArgumentParser(description='Finalize an external-Skill, model-created, or ad-hoc AURA work receipt without fabricating contract execution.')
    ap.add_argument('business_id',nargs='?')
    ap.add_argument('run_id',nargs='?')
    ap.add_argument('--workspace')
    ap.add_argument('--evidence',action='append',default=[])
    ap.add_argument('--result',action='append',default=[])
    ap.add_argument('--decision',action='append',default=[])
    ap.add_argument('--unresolved',action='append',default=[])
    ap.add_argument('--summary')
    ap.add_argument('--skip-human-knowledge',action='store_true')
    a=ap.parse_args()
    result=finalize_work_receipt(a.business_id,a.run_id,a.evidence,a.result,a.decision,a.unresolved,a.summary,a.workspace,not a.skip_human_knowledge)
    print(json.dumps(result,indent=2,ensure_ascii=False))
    raise SystemExit(0 if result.get('status')=='completed' else 2)


if __name__=='__main__':main()
