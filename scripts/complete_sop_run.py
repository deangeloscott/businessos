#!/usr/bin/env python3
from _common import *
from run_provenance import bind_evidence_paths
from validate_business_claims import claim_errors
from completion_evidence import contract_index, completion_spec, subcontract_manifest_errors, validate_evidence
import argparse,json

CUSTOMER_FACING_ROLE='customer_facing_production_root'

def _customer_facing_assets_for_run(business_id, run_rel):
    out=[]
    for obj,path in iter_instance_objects(business_id):
        if obj.get('object_type')!='Asset' or obj.get('owner_system') not in {'content-synthesis','marketing-synthesis'}:
            continue
        bos=(obj.get('extensions') or {}).get('businessos',{}) if isinstance(obj.get('extensions'),dict) else {}
        if bos.get('run_ref')==run_rel and bos.get('customer_facing',True) is not False:
            out.append((obj,path))
    return out

def _require_customer_facing_asset(business_id, run_id, m, rels):
    contracts=contract_index();root_id=m.get('root_contract_id');root=contracts.get(root_id,{})
    if root.get('artifact_role')!=CUSTOMER_FACING_ROLE:return []
    run_rel=f'runtime/runs/{business_id}/{run_id}';assets=_customer_facing_assets_for_run(business_id,run_rel)
    if not assets:raise ValueError('Cannot complete customer-facing production Run; persist at least one canonical customer-facing Asset referencing this Run before completion')
    required=set(m.get('required_subcontracts') or []);root_evidence={str(Path(x)) for x in rels};errors=[];eligible=[]
    for asset,path in assets:
        bos=(asset.get('extensions') or {}).get('businessos',{}) if isinstance(asset.get('extensions'),dict) else {}
        chain=bos.get('contract_chain')
        if not isinstance(chain,list) or root_id not in chain or not required.issubset(set(chain)):
            errors.append(f'{path}: Asset contract_chain must contain customer-facing root {root_id!r} and every required subcontract before Run completion');continue
        loc=asset.get('location_reference')
        if not loc:errors.append(f'{path}: customer-facing Asset requires location_reference');continue
        lp=resolve_storage_ref(loc)
        try: rel=storage_ref(lp)
        except Exception: rel=str(Path(loc))
        if str(Path(rel)) not in root_evidence:
            errors.append(f'{path}: customer-facing Asset file must be supplied as root --evidence before Run completion: {rel}');continue
        cerr=claim_errors(business_id,[(asset,path)])
        if cerr:errors.extend(cerr);continue
        eligible.append((asset,path))
    if not eligible:
        msg='Cannot complete customer-facing production Run; no governed canonical Asset satisfies provenance/claim requirements'
        if errors:msg+=':\n- '+'\n- '.join(errors)
        raise ValueError(msg)
    return eligible

def _run_linked_result_refs(business_id,run_id):
    """Return a compact index of canonical organizational results linked to this Run."""
    rr=f'runtime/runs/{business_id}/{run_id}';out=[]
    for obj,path in iter_instance_objects(business_id):
        ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
        bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
        lineage=obj.get('lineage') if isinstance(obj.get('lineage'),list) else []
        if not (bos.get('run_id')==run_id or bos.get('run_ref')==rr or run_id in lineage or rr in lineage):continue
        try:ref=storage_ref(path)
        except Exception:continue
        if ref not in out:out.append(ref)
    return sorted(out)

def snapshot_files(paths):
    snapshots={}
    for raw in paths:
        p=Path(raw);p=p if p.is_absolute() else ROOT/p
        if p.exists() and p.is_file():snapshots[p]=p.read_bytes()
    return snapshots

def restore_files(snapshots):
    for path,data in snapshots.items():path.write_bytes(data)

def complete_run(business_id,run_id,evidence):
    d=ROOT/'runtime/runs'/business_id/run_id;mp=d/'contract-execution.json';rp=d/'run.json'
    if not mp.exists() or not rp.exists():raise ValueError('Run files missing')
    m=json.loads(mp.read_text());pending=[k for k,v in m.get('contracts',{}).items() if v.get('status')!='completed']
    if pending:raise ValueError('Cannot complete Run; required subcontract(s) incomplete: '+', '.join(pending))
    subcontract_errors=subcontract_manifest_errors(m,business_id,run_id)
    if subcontract_errors:raise ValueError('Cannot complete Run; required subcontract evidence is invalid:\n- '+'\n- '.join(subcontract_errors))
    if not evidence:raise ValueError('Run completion requires at least one evidence path for the root deliverable/result')
    rels=[]
    for e in evidence:
        p=resolve_storage_ref(e)
        if not p.exists():raise ValueError(f'Root completion evidence missing: {e}')
        rels.append(storage_ref(p))
    # Preserve the established customer-facing provenance/claim gate first so callers get the
    # most specific product-governance error before deeper evidence-profile validation.
    eligible_assets=_require_customer_facing_asset(business_id,run_id,m,rels)
    contracts=contract_index();root_id=m.get('root_contract_id');root=contracts.get(root_id)
    if not root:raise ValueError(f'Installed contract metadata missing for Run root {root_id!r}')
    errors=validate_evidence(root,rels,business_id,run_id,phase='root',manifest=m)
    if errors:raise ValueError('Cannot complete Run; evidence does not satisfy root contract completion profile:\n- '+'\n- '.join(errors))
    # Completion is a small local transaction: finalize provenance/state, run the same full
    # active-business validator operators use, and restore the prior incomplete state if any
    # schema, reference, provenance, claim, or Run semantic remains invalid.
    touched=[mp,rp,*[resolve_storage_ref(x) for x in rels],*[path for _,path in eligible_assets]]
    snapshots=snapshot_files(touched)
    try:
        bind_evidence_paths(business_id,run_id,rels,'root_completion_evidence')
        # The external deliverable file is root evidence, while the canonical Asset record is the
        # durable state object. Finalize its run_id/run_contract_id/history deterministically too.
        if eligible_assets:
            bind_evidence_paths(business_id,run_id,[path for _,path in eligible_assets],'root_asset_record')
        ts=now();result_refs=_run_linked_result_refs(business_id,run_id)
        m['root_status']='completed';m['root_evidence_refs']=rels;m['root_completion_evidence_spec']=m.get('root_completion_evidence_spec') or completion_spec(root);m['updated_at']=ts;mp.write_text(json.dumps(m,indent=2)+'\n')
        r=json.loads(rp.read_text());r['status']='completed';r['updated_at']=ts
        continuity=dict(r.get('continuity') or {})
        continuity.update({
            'format_version':'1.0','purpose':'organizational_work_receipt','state':'completed','method_ref':root_id,
            'evidence_refs':list(dict.fromkeys(rels)),'result_refs':result_refs,'completed_at':ts,'superseded_by_run_id':None
        })
        r['continuity']=continuity;rp.write_text(json.dumps(r,indent=2)+'\n')
        from validate_business import validate_business
        business_errors,business_warnings,counts=validate_business(business_id)
        if business_errors:
            raise ValueError('active business validation is not clean:\n- '+'\n- '.join(business_errors))
    except Exception as exc:
        restore_files(snapshots)
        raise ValueError(f'Cannot complete Run; {exc}')
    return {'run_id':run_id,'status':'completed','required_subcontracts':list(m.get('contracts',{})),'root_evidence_refs':rels,'root_completion_evidence_spec':m['root_completion_evidence_spec'],'continuity':continuity,'validation':{'errors':0,'warnings':business_warnings,'canonical_object_counts':counts}}

def main():
    ap=argparse.ArgumentParser(description='Complete a Run only after every declared required subcontract has auditable, contract-appropriate completion evidence.')
    ap.add_argument('business_id');ap.add_argument('run_id');ap.add_argument('--evidence',action='append',default=[]);a=ap.parse_args()
    try:result=complete_run(a.business_id,a.run_id,a.evidence)
    except (ValueError,json.JSONDecodeError) as e:raise SystemExit(str(e))
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
