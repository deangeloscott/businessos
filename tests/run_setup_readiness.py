#!/usr/bin/env python3
"""Protect minimal setup/readiness and smoother persistence mechanics."""
from pathlib import Path
import json,os,shutil,subprocess,sys,tempfile

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
        root=Path(td).resolve();initial=root/'initial';ws=root/'workspace';initial.mkdir()
        old_workspace=os.environ.get('BUSINESSOS_WORKSPACE');old_config=os.environ.get('BUSINESSOS_WORKSPACE_CONFIG')
        os.environ['BUSINESSOS_WORKSPACE']=str(initial);os.environ.pop('BUSINESSOS_WORKSPACE_CONFIG',None)
        try:
            first=setup(workspace=ws,organization='Setup Readiness Org',write_link=False)
            req(first['status']=='ready',f'first setup did not prove readiness: {first}')
            bid=first['business_id'];req(bid=='setup-readiness-org','setup did not derive stable readable organization ID')
            req(business_ids()==[bid],'setup did not select the configured workspace or initialized duplicate state')
            req(not any(obj.get('asset_type')=='aura_doctor_probe' for obj,_ in object_index(bid).values()),'doctor left its temporary canonical probe behind')
            req(not any((ws/'runtime/runs').rglob('*')),'setup/readiness manufactured Run state')

            second=setup(workspace=ws,organization='Setup Readiness Org',write_link=False)
            req(second['status']=='ready','repeat setup was not idempotently ready')
            req(second['business_id']==bid and business_ids()==[bid],'repeat setup duplicated or switched organization state')
            req(not any(row.get('action')=='organization_initialized' for row in second['changes']),'repeat setup reinitialized existing organization')

            created=remember(bid,{'objects':[{'object_type':'Asset','content':{'asset_type':'brief','business_role':'durable setup test artifact','version':'1','status':'active'}}]})
            row=created['objects'][0];asset_ref=row['id']
            req(row['key']=='object_1','generic persistence should supply a mechanical local key when none is needed')
            req(row['object_type']=='Asset','generic persistence changed the caller-authored canonical type')
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
            # Exercise CLI behavior in a source copy, without touching live state/indexes.
            product=root/'product'
            shutil.copytree(ROOT,product,ignore=lambda directory,names: [name for name in names if name=='__pycache__' or (Path(directory)==ROOT and name in {'.git','.businessos','generated','instances','runtime','knowledge','attachments','qualification','.venv'})])
            shutil.copytree(ROOT/'instances/_template',product/'instances/_template')
            env=dict(os.environ);env['BUSINESSOS_WORKSPACE_CONFIG']=str(root/'test-link.json')
            def cli(script,*args):
                completed=subprocess.run([sys.executable,str(product/'scripts'/script),*args,'--json'],cwd=product,env=env,capture_output=True,text=True)
                try:payload=json.loads(completed.stdout)
                except json.JSONDecodeError:raise AssertionError(f'{script} did not return JSON: {completed.stdout}\n{completed.stderr}')
                return completed,payload
            completed,payload=cli('setup.py','--business-id',bid)
            req(completed.returncode==0 and payload['status']=='ready',f'fresh source setup failed: {payload}; {completed.stderr}')
            candidate=product/'generated/workflow-candidate-index.json';candidate.unlink()
            completed,payload=cli('setup.py','--business-id',bid)
            req(completed.returncode==0 and candidate.exists(),'setup failed to regenerate missing candidate index')
            registry=product/'generated/workflow-registry.json';registry.unlink()
            completed,payload=cli('doctor.py','--business-id',bid)
            req(completed.returncode==1 and payload['status']=='not_ready','missing registry did not produce structured failure')
            req(any(c['name']=='retrieval' and not c['ok'] for c in payload['checks']),'missing registry failure was not identified')
            env.pop('BUSINESSOS_WORKSPACE',None)
            Path(env['BUSINESSOS_WORKSPACE_CONFIG']).write_text('{broken')
            completed,payload=cli('doctor.py')
            req(completed.returncode==1 and payload['status']=='not_ready','invalid workspace config did not produce structured failure')
            req(payload['checks'][0]['name']=='workspace_resolution','invalid workspace config failure was not identified')
            print('AURA setup/readiness regressions passed: idempotent setup, real readiness proof, smoother persistence, compact receipts')
        finally:
            if old_workspace is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
            else:os.environ['BUSINESSOS_WORKSPACE']=old_workspace
            if old_config is None:os.environ.pop('BUSINESSOS_WORKSPACE_CONFIG',None)
            else:os.environ['BUSINESSOS_WORKSPACE_CONFIG']=old_config

if __name__=='__main__':main()
