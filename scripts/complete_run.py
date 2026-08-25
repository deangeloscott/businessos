#!/usr/bin/env python3
from _common import *
from run_provenance import bind_evidence_paths
from validate_business_claims import claim_errors
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
    try: contracts={c['id']:c for c in load_registry().get('contracts',[]) if c.get('id')}
    except Exception: contracts={}
    root_id=m.get('root_contract_id'); root=contracts.get(root_id,{})
    if root.get('artifact_role')!=CUSTOMER_FACING_ROLE:
        return
    run_rel=f'runtime/runs/{business_id}/{run_id}'
    assets=_customer_facing_assets_for_run(business_id,run_rel)
    if not assets:
        raise SystemExit('Cannot complete customer-facing production Run; persist at least one canonical customer-facing Asset referencing this Run before completion')
    required=set(m.get('required_subcontracts') or [])
    root_evidence={str(Path(x)) for x in rels}
    errors=[]; eligible=[]
    for asset,path in assets:
        bos=(asset.get('extensions') or {}).get('businessos',{}) if isinstance(asset.get('extensions'),dict) else {}
        chain=bos.get('contract_chain')
        if not isinstance(chain,list) or root_id not in chain or not required.issubset(set(chain)):
            errors.append(f'{path}: Asset contract_chain must contain customer-facing root {root_id!r} and every required subcontract before Run completion')
            continue
        loc=asset.get('location_reference')
        if not loc:
            errors.append(f'{path}: customer-facing Asset requires location_reference')
            continue
        lp=Path(loc); lp=lp if lp.is_absolute() else ROOT/lp
        try: rel=str(lp.resolve().relative_to(ROOT.resolve()))
        except Exception: rel=str(Path(loc))
        if str(Path(rel)) not in root_evidence:
            errors.append(f'{path}: customer-facing Asset file must be supplied as root --evidence before Run completion: {rel}')
            continue
        cerr=claim_errors(business_id,[(asset,path)])
        if cerr:
            errors.extend(cerr); continue
        eligible.append((asset,path))
    if not eligible:
        msg='Cannot complete customer-facing production Run; no governed canonical Asset satisfies provenance/claim requirements'
        if errors: msg+=':\n- '+'\n- '.join(errors)
        raise SystemExit(msg)

def main():
    ap=argparse.ArgumentParser(description='Complete a Run only after every declared required subcontract has auditable completion evidence.')
    ap.add_argument('business_id');ap.add_argument('run_id');ap.add_argument('--evidence',action='append',default=[]);a=ap.parse_args()
    d=ROOT/'runtime/runs'/a.business_id/a.run_id;mp=d/'contract-execution.json';rp=d/'run.json'
    if not mp.exists() or not rp.exists():raise SystemExit('Run files missing')
    m=json.loads(mp.read_text());pending=[k for k,v in m.get('contracts',{}).items() if v.get('status')!='completed']
    if pending:raise SystemExit('Cannot complete Run; required subcontract(s) incomplete: '+', '.join(pending))
    if not a.evidence: raise SystemExit('Run completion requires at least one --evidence path for the root deliverable/result')
    rels=[]
    for e in a.evidence:
        p=Path(e);p=p if p.is_absolute() else ROOT/p
        if not p.exists():raise SystemExit(f'Root completion evidence missing: {e}')
        rels.append(str(p.relative_to(ROOT)))
    # Customer-facing production roots cannot complete on a loose file alone. Require a
    # canonical outward Asset whose Run, contract chain, actual file, and claim manifest are
    # already coherent. The Run may still be in-progress at this check; completion happens below.
    _require_customer_facing_asset(a.business_id,a.run_id,m,rels)
    # Canonical root evidence is bound to this Run before the completion state is committed.
    # This makes the manifest, not a free-form object assertion, the provenance authority.
    bind_evidence_paths(a.business_id,a.run_id,rels,'root_completion_evidence')
    m['root_status']='completed';m['root_evidence_refs']=rels;m['updated_at']=now();mp.write_text(json.dumps(m,indent=2)+'\n')
    r=json.loads(rp.read_text());r['status']='completed';r['updated_at']=now();rp.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'run_id':a.run_id,'status':'completed','required_subcontracts':list(m.get('contracts',{})),'root_evidence_refs':rels},indent=2))
if __name__=='__main__':main()
