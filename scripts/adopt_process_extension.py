#!/usr/bin/env python3
"""Adopt an intentionally selected business-scoped AURA process extension."""
from _common import *
from jsonschema import Draft202012Validator
from persist_playbook_evolution import _schema
import argparse,json,hashlib,os

def _find_proposal(business_id,proposal_id):
    for obj,p in iter_instance_objects(business_id):
        if obj.get('object_type')=='PlaybookEvolutionProposal' and obj.get('id')==proposal_id:return obj,p
    raise ValueError(f'Unknown PlaybookEvolutionProposal for {business_id}: {proposal_id}')
def _validate(obj):
    errs=sorted(Draft202012Validator(_schema('ProcessExtension')).iter_errors(obj),key=lambda e:list(e.path))
    if errs:raise ValueError('; '.join(f"{list(e.path)}: {e.message}" for e in errs))

def adopt_extension(business_id,proposal_id):
    proposal,ppath=_find_proposal(business_id,proposal_id)
    if proposal.get('status') in {'rejected','superseded'}:raise ValueError(f"Proposal is {proposal.get('status')}")
    if proposal.get('change_kind')=='canonical_revision' or proposal.get('proposed_scope')!='business':raise ValueError('Broader/canonical proposals are AURA product-development candidates and are not adopted as business-scoped ProcessExtensions.')
    mode='augment_contract' if proposal['change_kind']=='augment_existing' else 'local_playbook'
    if mode=='augment_contract':
        target=proposal.get('target_contract_id');base_meta=None
        for cp in contract_files():
            try:meta,_=read_frontmatter(cp)
            except Exception:continue
            if meta.get('id')==target:base_meta=meta;break
        if not base_meta:raise ValueError(f'Unknown canonical target contract: {target}')
        base_writes={selector_type(x) for x in base_meta.get('writes',[])};extra_writes=sorted(set(proposal.get('writes') or [])-base_writes)
        if extra_writes:raise ValueError('augment_existing may not introduce new canonical write types; use a new local playbook or explicit canonical revision instead: '+', '.join(extra_writes))
    seed=f"{business_id}|{proposal_id}|{mode}";oid='pex_'+hashlib.sha256(seed.encode()).hexdigest()[:20];outdir=ROOT/'instances'/business_id/'learning'/'process-extensions';outdir.mkdir(parents=True,exist_ok=True);path=outdir/f'{oid}.json';existing=json.loads(path.read_text()) if path.exists() else {};ts=now()
    obj={'id':oid,'object_type':'ProcessExtension','schema_version':'1.0.0','business_id':business_id,'created_at':existing.get('created_at') or ts,'updated_at':ts,'extension_version':existing.get('extension_version') or '1.0.0','mode':mode,'owner_system':proposal['owner_system'],'target_contract_id':proposal.get('target_contract_id'),'local_contract_id':proposal.get('proposed_local_contract_id'),'title':proposal['title'],'purpose':proposal['summary'],'route_terms':proposal.get('route_terms') or [],'status':'active','scope':'business','scope_ref':None,'priority':100,'applies_when':proposal.get('applies_when') or [],'does_not_apply_when':proposal.get('does_not_apply_when') or [],'reads':proposal.get('reads') or [],'writes':proposal.get('writes') or [],'required_capabilities':proposal.get('required_capabilities') or [],'optional_capabilities':proposal.get('optional_capabilities') or [],'instructions':proposal.get('instructions') or [],'verification':proposal.get('verification') or [],'source_learning_refs':proposal.get('learning_refs') or [],'evidence_refs':proposal.get('evidence_refs') or [],'compatibility':{'aura_min':os_version(),'aura_max':None},'extensions':{'playbook_evolution_proposal_ref':proposal_id}}
    _validate(obj);tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,path);proposal['status']='adopted';proposal['updated_at']=ts;ppath.write_text(json.dumps(proposal,indent=2)+'\n');return obj,path

def main():
    ap=argparse.ArgumentParser(description='Adopt an intentionally selected business-scoped evolution proposal as a reversible ProcessExtension. Calling this command is the adoption action; AURA has no separate Approval object/gate.');ap.add_argument('business_id');ap.add_argument('proposal_id');a=ap.parse_args()
    try:obj,path=adopt_extension(a.business_id,a.proposal_id)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps({'process_extension_id':obj['id'],'path':str(path.relative_to(ROOT)),'mode':obj['mode'],'status':obj['status']},indent=2))
if __name__=='__main__':main()
