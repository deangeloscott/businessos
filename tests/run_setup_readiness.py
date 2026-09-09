#!/usr/bin/env python3
"""Protect minimal setup/readiness and smoother persistence mechanics."""
from pathlib import Path
import os,sys,tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from _common import business_ids,object_index
from setup import setup
from remember import remember
from persist_research_bundle import persist as persist_research
from validate_business import validate_business


def req(condition,message):
    if not condition:raise AssertionError(message)


def main():
    with tempfile.TemporaryDirectory(prefix='aura-setup-readiness-') as td:
        ws=Path(td).resolve();old=os.environ.get('BUSINESSOS_WORKSPACE')
        os.environ.pop('BUSINESSOS_WORKSPACE',None)
        try:
            first=setup(workspace=ws,organization='Setup Readiness Org',write_link=False)
            req(first['status']=='ready',f'first setup did not prove readiness: {first}')
            bid=first['business_id'];req(bid=='setup-readiness-org','setup did not derive stable readable organization ID')
            req(business_ids()==[bid],'setup did not select the configured workspace or initialized duplicate state')
            req(not any(obj.get('asset_type')=='aura_doctor_probe' for obj,_ in object_index(bid).values()),'doctor left its temporary canonical probe behind')
            req(not (ws/'runtime/runs').exists(),'setup/readiness manufactured Run state')

            second=setup(workspace=ws,organization='Setup Readiness Org',write_link=False)
            req(second['status']=='ready','repeat setup was not idempotently ready')
            req(second['business_id']==bid and business_ids()==[bid],'repeat setup duplicated or switched organization state')
            req(not any(row.get('action')=='organization_initialized' for row in second['changes']),'repeat setup reinitialized existing organization')

            created=remember(bid,{'objects':[{'kind':'asset','content':{'asset_type':'brief','business_role':'durable setup test artifact','version':'1','status':'active'}}]})
            row=created['objects'][0];asset_ref=row['id']
            req(row['key']=='object_1','generic persistence should supply a mechanical local key when none is needed')
            req(row['object_type']=='Asset','kind alias did not resolve to canonical object type')
            req(created['receipt']=={'status':'saved','objects':1,'created':1,'updated':0,'object_types':{'Asset':1},'validation':'passed'},f'compact persistence receipt is wrong: {created.get("receipt")}')

            updated=remember(bid,{'objects':[{'object_ref':asset_ref,'content':{'business_role':'updated durable setup test artifact'}}]})
            req(updated['objects'][0]['object_type']=='Asset' and updated['objects'][0]['operation']=='updated','update did not infer object_type from object_ref')
            req(updated['receipt']['updated']==1 and updated['receipt']['validation']=='passed','update receipt did not reflect successful persistence')

            bundle={
                'method_type':'ad_hoc','method_ref':'setup-readiness-test',
                'sources':[{
                    'source_type':'first_party_note','origin':'organization supplied','access_scope':'business_internal',
                    'source_reference':'attachments/setup-readiness-note.txt','acquisition_method':'user_provided',
                    'captured_text':'The organization supplied a durable readiness test note.'
                }],
                'observations':[{
                    'statement':'The organization supplied a durable readiness test note.',
                    'source_indexes':[0],'observation_type':'setup_test','extraction_confidence':'high'
                }]
            }
            written,_=persist_research(bid,bundle)
            observation=next(obj for obj,_ in written if obj.get('object_type')=='Observation')
            req(observation.get('extraction_confidence') is None,'qualitative confidence should not invent numeric precision')
            req((observation.get('extensions') or {}).get('businessos',{}).get('extraction_confidence_label')=='high','qualitative confidence label was not preserved')

            errors,_,_=validate_business(bid,True);req(not errors,f'setup/persistence state must remain valid: {errors}')
            print('AURA setup/readiness regressions passed: idempotent setup, real readiness proof, smoother persistence, compact receipts')
        finally:
            if old is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
            else:os.environ['BUSINESSOS_WORKSPACE']=old

if __name__=='__main__':main()
