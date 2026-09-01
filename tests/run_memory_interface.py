#!/usr/bin/env python3
"""Protect AURA memory as a first-class primitive independent of Runs/contracts."""
from pathlib import Path
import json,os,sys,tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from _common import object_index
from init_business import init_business
from remember import remember
from forget import forget
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

            corrected=remember(bid,{'objects':[{
                'key':'asset_correction','object_type':'Asset','object_ref':asset_id,'content':{},
                'remove_fields':['location_reference']
            }]})
            req(corrected['objects'][0]['removed_fields']==['location_reference'],'field removal was not reported truthfully')
            asset=json.loads(asset_path.read_text());req('location_reference' not in asset,'obsolete optional field survived direct current-truth correction')
            proposal_dir=ws/'instances'/bid/'context/proposals'
            req(not proposal_dir.exists() or not list(proposal_dir.glob('*.json')),'direct current-truth correction manufactured ContextUpdateProposal ceremony')

            required_rejected=False
            try:
                remember(bid,{'objects':[{
                    'key':'invalid_required_removal','object_type':'Asset','object_ref':asset_id,'content':{},
                    'remove_fields':['asset_type']
                }]})
            except ValueError:required_rejected=True
            req(required_rejected,'schema-required field removal should fail mechanical validation')
            asset=json.loads(asset_path.read_text());req(asset.get('asset_type')=='draft','failed required-field removal mutated canonical memory')

            mechanical_rejected=False
            try:
                remember(bid,{'objects':[{
                    'key':'invalid_mechanical_removal','object_type':'Asset','object_ref':asset_id,'content':{},
                    'remove_fields':['id']
                }]})
            except ValueError:mechanical_rejected=True
            req(mechanical_rejected,'AURA-owned mechanical fields must not be removable through semantic memory updates')

            linked=remember(bid,{'objects':[
                {
                    'key':'obsolete_source','object_type':'Asset','content':{
                        'asset_type':'note','owner_system':'core','business_role':'temporary context',
                        'version':'1','status':'active'
                    }
                },
                {
                    'key':'dependent_asset','object_type':'Asset','lineage_refs':['@obsolete_source'],'content':{
                        'asset_type':'brief','owner_system':'core','business_role':'depends on temporary context',
                        'version':'1','status':'active'
                    }
                }
            ]})
            source_id=next(row['id'] for row in linked['objects'] if row['key']=='obsolete_source')
            dependent_id=next(row['id'] for row in linked['objects'] if row['key']=='dependent_asset')
            blocked=False
            try:forget(bid,source_id)
            except ValueError:blocked=True
            req(blocked,'forget must refuse to delete memory that current canonical state still references')
            req(source_id in object_index(bid),'blocked forget removed referenced memory')
            req(forget(bid,dependent_id)['status']=='forgotten','unreferenced dependent object could not be forgotten')
            req(forget(bid,source_id)['status']=='forgotten','formerly referenced object could not be forgotten after dependency was resolved')

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
            print('AURA memory interface regressions passed: direct create/update/correction/forget and research do not require Run, contract, or proposal ceremony')
        finally:
            if old is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
            else:os.environ['BUSINESSOS_WORKSPACE']=old


if __name__=='__main__':main()
