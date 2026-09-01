#!/usr/bin/env python3
"""Protect AURA memory as a first-class primitive independent of Runs/contracts."""
from pathlib import Path
import json,os,sys,tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from init_business import init_business
from remember import remember
from persist_research_bundle import persist as persist_research
from validate_business import validate_business


def req(condition,message):
    if not condition:raise AssertionError(message)


def main():
    with tempfile.TemporaryDirectory(prefix='aura-memory-interface-') as td:
        ws=Path(td).resolve();old=os.environ.get('BUSINESSOS_WORKSPACE');os.environ['BUSINESSOS_WORKSPACE']=str(ws)
        try:
            bid='memory-interface';init_business(bid,'Memory Interface')
            payload={
                'provenance':{'method_type':'ad_hoc','method_ref':'active model'},
                'objects':[{
                    'key':'draft_asset','object_type':'Asset','content':{
                        'asset_type':'draft','owner_system':'core','business_role':'useful durable draft',
                        'location_reference':'attachments/draft.md','version':'1','status':'active'
                    }
                }]
            }
            result=remember(bid,payload);row=result['objects'][0];asset_id=row['id']
            req(row['operation']=='created','Run-independent memory did not create canonical object')
            req(not (ws/'runtime/runs').exists(),'remember created a Run even though none was requested')
            asset_path=ws/row['path'];asset=json.loads(asset_path.read_text())
            req((asset.get('extensions') or {}).get('businessos',{}).get('memory_provenance',{}).get('method_type')=='ad_hoc','optional method provenance was not preserved')

            updated=remember(bid,{'objects':[{'key':'asset_update','object_type':'Asset','object_ref':asset_id,'content':{'business_role':'approved reusable draft'}}]})
            req(updated['objects'][0]['operation']=='updated','canonical current memory update failed without Run')
            asset=json.loads(asset_path.read_text());req(asset['business_role']=='approved reusable draft','canonical memory update did not persist')

            bundle={
                'method_type':'external_skill','method_ref':'first-party-review',
                'owner_system':'core',
                'sources':[{
                    'source_type':'first_party_note','origin':'organization supplied','access_scope':'business_internal',
                    'source_reference':'attachments/customer-note.txt','acquisition_method':'user_provided',
                    'captured_text':'A customer asked whether wholesale ordering is available.'
                }],
                'observations':[{
                    'statement':'A customer asked whether wholesale ordering is available.',
                    'source_indexes':[0],'observation_type':'customer_request'
                }]
            }
            written,_=persist_research(bid,bundle)
            req(any(obj.get('object_type')=='SourceRecord' for obj,_ in written),'research without AURA contract did not persist SourceRecord')
            req(any(obj.get('object_type')=='Observation' for obj,_ in written),'research without AURA contract did not persist Observation')
            source=next(obj for obj,_ in written if obj.get('object_type')=='SourceRecord')
            method=(source.get('extensions') or {}).get('businessos_method',{})
            req(method.get('method_type')=='external_skill' and method.get('method_ref')=='first-party-review','non-AURA research method provenance was lost')
            req('contract_id' not in (source.get('extensions') or {}),'non-AURA research fabricated contract provenance')

            errors,_,_=validate_business(bid,True);req(not errors,f'Run-independent memory must remain valid: {errors}')
            print('AURA memory interface regressions passed: remember/research do not require Run or contract')
        finally:
            if old is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
            else:os.environ['BUSINESSOS_WORKSPACE']=old


if __name__=='__main__':main()
