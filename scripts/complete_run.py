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
    if not assets:raise SystemExit('Cannot complete customer-facing production Run; persist at least one canonical customer-facing Asset referencing this Run before completion')
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
        raise SystemExit(msg)
    return eligible

def main():
    ap=argparse.ArgumentParser(description='Complete a Run only after every declared required subcontract has auditable, contract-appropriate completion evidence.')
    ap.add_argument('business_id');ap.add_argument('run_id');ap.add_argument('--evidence',action='append',default=[]);a=ap.parse_args()
    d=ROOT/'runtime/runs'/a.business_id/a.run_id;mp=d/'contract-execution.json';rp=d/'run.json'
    if not mp.exists() or not rp.exists():raise SystemExit('Run files missing')
    m=json.loads(mp.read_text());pending=[k for k,v in m.get('contracts',{}).items() if v.get('status')!='completed']
    if pending:raise SystemExit('Cannot complete Run; required subcontract(s) incomplete: '+', '.join(pending))
    subcontract_errors=subcontract_manifest_errors(m,a.business_id,a.run_id)
    if subcontract_errors:raise SystemExit('Cannot complete Run; required subcontract evidence is invalid:\n- '+'\n- '.join(subcontract_errors))
    if not a.evidence:raise SystemExit('Run completion requires at least one --evidence path for the root deliverable/result')
    rels=[]
    for e in a.evidence:
        p=resolve_storage_ref(e)
        if not p.exists():raise SystemExit(f'Root completion evidence missing: {e}')
        rels.append(storage_ref(p))
    # Preserve the established customer-facing provenance/claim gate first so callers get the
    # most specific product-governance error before deeper evidence-profile validation.
    eligible_assets=_require_customer_facing_asset(a.business_id,a.run_id,m,rels)
    contracts=contract_index();root_id=m.get('root_contract_id');root=contracts.get(root_id)
    if not root:raise SystemExit(f'Installed contract metadata missing for Run root {root_id!r}')
    errors=validate_evidence(root,rels,a.business_id,a.run_id,phase='root',manifest=m)
    if errors:raise SystemExit('Cannot complete Run; evidence does not satisfy root contract completion profile:\n- '+'\n- '.join(errors))
    bind_evidence_paths(a.business_id,a.run_id,rels,'root_completion_evidence')
    # The external deliverable file is root evidence, while the canonical Asset record is the
    # durable state object. Finalize its run_id/run_contract_id/history deterministically too.
    if eligible_assets:
        bind_evidence_paths(a.business_id,a.run_id,[path for _,path in eligible_assets],'root_asset_record')
    m['root_status']='completed';m['root_evidence_refs']=rels;m['root_completion_evidence_spec']=m.get('root_completion_evidence_spec') or completion_spec(root);m['updated_at']=now();mp.write_text(json.dumps(m,indent=2)+'\n')
    r=json.loads(rp.read_text());r['status']='completed';r['updated_at']=now();rp.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'run_id':a.run_id,'status':'completed','required_subcontracts':list(m.get('contracts',{})),'root_evidence_refs':rels,'root_completion_evidence_spec':m['root_completion_evidence_spec']},indent=2))
if __name__=='__main__':main()
