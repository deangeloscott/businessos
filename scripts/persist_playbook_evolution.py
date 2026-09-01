#!/usr/bin/env python3
"""Persist evidence-backed proposals for reusable organization process knowledge."""
from _common import *
from jsonschema import Draft202012Validator
from persist_process_extension import _validate_method_metadata
import argparse,json,hashlib,os,re


def _schema(title):
    for path in schemas():
        try:data=json.loads(path.read_text())
        except Exception:continue
        if data.get('title')==title:return data
    raise ValueError(f'Unknown schema title: {title}')

def _validate(title,obj):
    errors=sorted(Draft202012Validator(_schema(title)).iter_errors(obj),key=lambda error:list(error.path))
    if errors:raise ValueError('; '.join(f"{list(error.path)}: {error.message}" for error in errors))

def _canonical_contract_exists(contract_id):
    for path in contract_files():
        try:meta,_=read_frontmatter(path)
        except Exception:continue
        if meta.get('id')==contract_id:return True
    return False


def persist_proposal(business_id,payload):
    base=ROOT/'instances'/business_id
    if not base.exists():raise ValueError(f'Unknown business: {business_id}')
    if not isinstance(payload,dict):raise ValueError('Proposal input must be a JSON object')
    learning_refs=list(dict.fromkeys(payload.get('learning_refs') or []))
    if not learning_refs:raise ValueError('At least one learning_ref is required')
    index=object_index(business_id)
    for ref in learning_refs:
        if ref not in index or index[ref][0].get('object_type')!='Learning':raise ValueError(f'Unknown Learning reference for {business_id}: {ref}')

    kind=payload.get('change_kind');target=payload.get('target_contract_id');local_id=payload.get('proposed_local_contract_id')
    if kind=='augment_existing' and (not target or not _canonical_contract_exists(target)):raise ValueError(f'augment_existing requires an installed canonical target contract: {target!r}')
    if kind=='new_local_playbook':
        if not local_id or not re.match(r'^custom\.[a-z0-9][a-z0-9.-]*$',local_id):raise ValueError('new_local_playbook requires proposed_local_contract_id beginning custom.')
        for obj,_ in iter_instance_objects(business_id):
            if obj.get('object_type')=='ProcessExtension' and obj.get('local_contract_id')==local_id and obj.get('status')!='retired':raise ValueError(f'Local playbook id already exists: {local_id}')
    _validate_method_metadata(payload.get('reads') or [],payload.get('writes') or [],payload.get('required_capabilities') or [],payload.get('optional_capabilities') or [])

    seed='|'.join([business_id,str(payload.get('owner_system')),str(kind),str(target),str(local_id),str(payload.get('summary'))]);oid='pev_'+hashlib.sha256(seed.encode()).hexdigest()[:20]
    outdir=base/'learning'/'evolution'/'proposals';outdir.mkdir(parents=True,exist_ok=True);path=outdir/f'{oid}.json';existing=json.loads(path.read_text()) if path.exists() else {};timestamp=now()
    obj={
        'id':oid,'object_type':'PlaybookEvolutionProposal','schema_version':'1.0.0','business_id':business_id,
        'created_at':existing.get('created_at') or timestamp,'updated_at':timestamp,'owner_system':payload.get('owner_system'),'change_kind':kind,'proposed_scope':payload.get('proposed_scope','business'),
        'target_contract_id':target,'proposed_local_contract_id':local_id,'title':payload.get('title') or 'Playbook evolution proposal','summary':payload.get('summary'),
        'learning_refs':learning_refs,'evidence_refs':list(dict.fromkeys(payload.get('evidence_refs') or [])),'applies_when':list(dict.fromkeys(payload.get('applies_when') or [])),
        'does_not_apply_when':list(dict.fromkeys(payload.get('does_not_apply_when') or [])),'route_terms':list(dict.fromkeys(payload.get('route_terms') or [])),'reads':list(dict.fromkeys(payload.get('reads') or [])),
        'writes':list(dict.fromkeys(payload.get('writes') or [])),'required_capabilities':list(dict.fromkeys(payload.get('required_capabilities') or [])),'optional_capabilities':list(dict.fromkeys(payload.get('optional_capabilities') or [])),
        'instructions':payload.get('instructions') or [],'verification':payload.get('verification') or [],'status':existing.get('status') if existing.get('status')=='adopted' else 'candidate','extensions':payload.get('extensions') or {}
    }
    _validate('PlaybookEvolutionProposal',obj);temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(obj,indent=2)+'\n');os.replace(temporary,path);return obj,path


def main():
    parser=argparse.ArgumentParser(description='Persist a bounded evidence-backed ProcessExtension proposal from Learning.');parser.add_argument('business_id');parser.add_argument('--proposal-file',required=True);args=parser.parse_args()
    try:payload=json.loads(Path(args.proposal_file).read_text());obj,path=persist_proposal(args.business_id,payload)
    except (ValueError,json.JSONDecodeError) as exc:raise SystemExit(str(exc))
    print(json.dumps({'proposal_id':obj['id'],'path':str(path.relative_to(ROOT)),'status':obj['status']},indent=2))

if __name__=='__main__':main()
