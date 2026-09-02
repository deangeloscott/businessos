#!/usr/bin/env python3
"""Adopt intentionally selected, evidence-backed organization Workflow knowledge."""
from _common import *
from jsonschema import Draft202012Validator
from persist_workflow_evolution import _schema
from persist_process_extension import _validate_method_metadata
import argparse,json,hashlib,os


def _find_proposal(business_id,proposal_id):
    for obj,path in iter_instance_objects(business_id):
        if obj.get('object_type')=='WorkflowEvolutionProposal' and obj.get('id')==proposal_id:return obj,path
    raise ValueError(f'Unknown WorkflowEvolutionProposal for {business_id}: {proposal_id}')
def _validate(obj):
    errors=sorted(Draft202012Validator(_schema('ProcessExtension')).iter_errors(obj),key=lambda error:list(error.path))
    if errors:raise ValueError('; '.join(f"{list(error.path)}: {error.message}" for error in errors))
def _workflow_exists(workflow_id):
    for path in workflow_files():
        try:meta,_=read_frontmatter(path)
        except Exception:continue
        if meta.get('id')==workflow_id and meta.get('type')=='workflow':return True
    return False


def adopt_extension(business_id,proposal_id):
    proposal,proposal_path=_find_proposal(business_id,proposal_id)
    if proposal.get('status') in {'rejected','superseded'}:raise ValueError(f"Proposal is {proposal.get('status')}")
    if proposal.get('change_kind')=='canonical_revision' or proposal.get('proposed_scope')!='business':raise ValueError('Broader/canonical proposals are AURA product-development candidates and are not adopted as organization ProcessExtensions.')
    mode='augment_workflow' if proposal['change_kind']=='augment_existing' else 'local_workflow'
    target=proposal.get('target_workflow_id');local_id=proposal.get('proposed_local_workflow_id')
    if mode=='augment_workflow' and not _workflow_exists(target):raise ValueError(f"Unknown canonical target Workflow: {target}")
    _validate_method_metadata(proposal.get('reads') or [],proposal.get('writes') or [])

    seed=f"{business_id}|{proposal_id}|{mode}";oid='pex_'+hashlib.sha256(seed.encode()).hexdigest()[:20];outdir=ROOT/'instances'/business_id/'learning'/'process-extensions';outdir.mkdir(parents=True,exist_ok=True);path=outdir/f'{oid}.json';existing=json.loads(path.read_text()) if path.exists() else {};timestamp=now()
    obj={
        'id':oid,'object_type':'ProcessExtension','schema_version':'1.0.0','business_id':business_id,
        'created_at':existing.get('created_at') or timestamp,'updated_at':timestamp,
        'mode':mode,'owner_system':proposal['owner_system'],'target_workflow_id':target,'local_workflow_id':local_id,
        'title':proposal['title'],'purpose':proposal['summary'],'discovery_terms':proposal.get('discovery_terms') or [],'status':'active','scope':'business','scope_ref':None,
        'applies_when':proposal.get('applies_when') or [],'does_not_apply_when':proposal.get('does_not_apply_when') or [],'reads':proposal.get('reads') or [],'writes':proposal.get('writes') or [],
        'instructions':proposal.get('instructions') or [],'verification':proposal.get('verification') or [],
        'source_kind':'learning_evolved','source_learning_refs':proposal.get('learning_refs') or [],'source_refs':proposal.get('evidence_refs') or [],'evidence_refs':proposal.get('evidence_refs') or [],
        'compatibility':{'aura_min':os_version(),'aura_max':None},'extensions':{'workflow_evolution_proposal_ref':proposal_id}
    }
    _validate(obj);temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(obj,indent=2)+'\n');os.replace(temporary,path)
    proposal['status']='adopted';proposal['updated_at']=timestamp;proposal_path.write_text(json.dumps(proposal,indent=2)+'\n');return obj,path


def main():
    parser=argparse.ArgumentParser(description='Adopt evidence-backed Learning as reversible organization-scoped Workflow knowledge. Explicit organization-authored procedures use persist_process_extension.py instead of fabricating Learning.')
    parser.add_argument('business_id');parser.add_argument('proposal_id');args=parser.parse_args()
    try:obj,path=adopt_extension(args.business_id,args.proposal_id)
    except ValueError as exc:raise SystemExit(str(exc))
    print(json.dumps({'process_extension_id':obj['id'],'path':str(path.relative_to(ROOT)),'mode':obj['mode'],'status':obj['status'],'source_kind':obj.get('source_kind')},indent=2))

if __name__=='__main__':main()
