#!/usr/bin/env python3
"""Protect explicit organization-authored operating knowledge as first-class AURA state."""
from pathlib import Path
import json,os,sys,tempfile

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from init_business import init_business
from remember import remember
from persist_process_extension import persist_extension
from process_extensions import local_playbooks,local_playbook_candidates,resolve_effective
from validate_business import validate_business


def req(condition,message):
    if not condition:raise AssertionError(message)


def main():
    with tempfile.TemporaryDirectory(prefix='aura-explicit-sop-') as td:
        ws=Path(td).resolve();old=os.environ.get('BUSINESSOS_WORKSPACE');os.environ['BUSINESSOS_WORKSPACE']=str(ws)
        try:
            bid='explicit-sop';init_business(bid,'Explicit SOP Co')
            sop_path=ws/'attachments/client-kickoff.md';sop_path.parent.mkdir(parents=True,exist_ok=True)
            sop_path.write_text('# Client kickoff\nConfirm goals and access, then produce a written kickoff summary.\n')
            saved=remember(bid,{'objects':[{'key':'sop_source','object_type':'Asset','content':{'asset_type':'organization_sop','owner_system':'core','business_role':'source operating procedure','location_reference':'attachments/client-kickoff.md','version':'1','status':'active'}}]})
            source_ref=saved['objects'][0]['id']

            spec={
                'mode':'local_playbook','owner_system':'core','local_contract_id':'custom.client-kickoff',
                'title':'Client Kickoff','purpose':'Run the organization\'s established client kickoff procedure.',
                'discovery_terms':['client kickoff','kickoff new client'],'source_refs':[source_ref],
                'instructions':['Confirm the client goal and required access.','Produce a written kickoff summary that records material decisions and unresolved items.'],
                'verification':['The kickoff summary reflects the supplied goal, access state, material decisions, and unresolved items.']
            }
            extension,path=persist_extension(bid,spec)
            req(extension['source_kind']=='organization_authored','explicit SOP was not marked organization-authored')
            req(extension['source_learning_refs']==[],'explicit SOP fabricated Learning provenance')
            req(extension['source_refs']==[source_ref],'explicit SOP lost its real source provenance')
            req(extension.get('discovery_terms')==['client kickoff','kickoff new client'],'explicit SOP lost its retrieval cues')
            req('route_terms' not in extension,'explicit SOP reintroduced retired routing vocabulary')
            req(path.exists(),'explicit SOP was not persisted')

            local=local_playbooks(bid);req(any(row.get('local_contract_id')=='custom.client-kickoff' for row in local),'explicit local playbook is not available to AURA retrieval')
            candidates=local_playbook_candidates('Kick off this new client',bid)
            req(any(row.get('contract_id')=='custom.client-kickoff' for row in candidates),'local SOP was not discoverable from bounded lexical cues')
            req(all(row.get('selection_authority') is False for row in candidates),'local SOP candidate search claimed semantic authority')

            _,meta,content,_=resolve_effective('custom.client-kickoff',bid)
            req(meta.get('local_playbook') is True and 'Confirm the client goal' in content,'explicit model-selected local SOP did not resolve as operating knowledge')

            errors,_,_=validate_business(bid,True);req(not errors,f'explicit operating knowledge must validate: {errors}')
            print('explicit operating knowledge regression passed: organization SOPs use discovery, not routing or fake Learning')
        finally:
            if old is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
            else:os.environ['BUSINESSOS_WORKSPACE']=old

if __name__=='__main__':main()
