#!/usr/bin/env python3
"""Protect the simple harness-neutral AURA front door."""
from pathlib import Path
import json,os,subprocess,sys,tempfile

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'scripts'


def req(condition,message):
    if not condition:raise AssertionError(message)


def run(args,env,check=True):
    result=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,env=env,capture_output=True,text=True)
    if check and result.returncode!=0:raise AssertionError(f'command failed: {args}\nstdout={result.stdout}\nstderr={result.stderr}')
    return result


def enter(request,bid,workspace,env,*extra,check=True):
    result=run([S/'enter.py',request,'--business-id',bid,'--workspace',workspace,*extra],env,check=check)
    return result,json.loads(result.stdout)


def main():
    with tempfile.TemporaryDirectory(prefix='aura-entry-regression-') as td:
        ws=Path(td).resolve();env=os.environ.copy();env['BUSINESSOS_WORKSPACE']=str(ws);env['PYTHONDONTWRITEBYTECODE']='1'
        bid='entry-regression'
        run([S/'init_business.py',bid,'--name','Entry Regression'],env)
        supplied=ws/'attachments';supplied.mkdir(parents=True)
        source=supplied/'business-source.txt';source.write_text('The organization wants to create a presentation for a proposal.\n')
        run([S/'bootstrap_explicit_context.py',bid,'--facts-json',json.dumps({'objectives':['Create a presentation for a proposal']}),'--source-file',source,'--initialization-only'],env)

        request='Create a presentation for this business proposal.'
        result,payload=enter(request,bid,ws,env)
        req(result.returncode==0 and payload.get('status')=='ready',f'entry should prepare useful work context: {payload}')
        req(payload.get('business_id')==bid and payload.get('original_request')==request,'entry lost business identity or original request')
        req(payload.get('run',{}).get('created') is False,'entry must not create a Run merely to begin reasoning')
        req({'aura_playbook','external_skill','model_created','ad_hoc'}<=set(payload.get('method_options',[])),'entry lost method freedom')
        rec=payload.get('recommended_playbook',{})
        req(rec.get('status') in {'model_judgment','none'},f'unselected entry must leave semantic method choice to the model: {rec}')
        req(rec.get('contract_id') is None,'candidate discovery silently became playbook selection')
        req('active model/user' in rec.get('rule','') or 'model/user' in rec.get('rule',''),'playbook candidates became semantic authority')
        req(payload.get('retrieval',{}).get('context_files')==['CONTEXT.md'],'unselected entry should not front-load redundant AURA policy files')
        req('semantic intent and execution remain with the active intelligence/runtime' in payload.get('rule',''),'front door lost model/runtime ownership boundary')
        req(not (ws/'runtime/runs'/bid).exists(),'entry created runtime Run state despite optional-Run architecture')

        selected_result,selected=enter(request,bid,ws,env,'--selected-contract','content.production.presentation')
        req(selected_result.returncode==0 and selected.get('status')=='ready','explicit AURA playbook selection should remain available')
        req(selected.get('recommended_playbook',{}).get('contract_id')=='content.production.presentation','explicit playbook selection was not preserved')
        req(selected.get('recommended_playbook',{}).get('selection_mode')=='explicit_model_selection','explicit model selection mode was lost')
        req(selected.get('recommended_playbook',{}).get('status')=='selected','explicitly selected playbook was not marked selected')
        req(selected.get('playbook_process') is not None,'selected AURA playbook should expose its reusable process knowledge')
        req(selected.get('run',{}).get('created') is False,'explicit playbook selection still must not auto-create a Run')
        loaded=selected.get('retrieval',{}).get('context_files',[])
        req('CONTEXT.md' in loaded and 'core/DEFAULTS.md' not in loaded and 'core/policies/agent-execution.md' not in loaded,'selected playbook context reintroduced redundant universal instruction stack')

        # Multiple organizations require real resolution rather than guessing.
        second='entry-regression-two';run([S/'init_business.py',second,'--name','Entry Regression Two'],env)
        unresolved=run([S/'enter.py','Analyze the business.','--workspace',ws],env,check=False)
        data=json.loads(unresolved.stdout)
        req(unresolved.returncode==2 and data.get('status')=='needs_input','ambiguous organization should request only the missing organization choice')
        req(sorted(data.get('available_business_ids',[]))==sorted([bid,second]),'business-resolution handoff should expose the stable IDs')
        names={row['id']:row['name'] for row in data.get('available_businesses',[])}
        req(names=={bid:'Entry Regression',second:'Entry Regression Two'},f'business-resolution handoff should expose human-readable organization names: {names}')

        # External workspace operation must not leak organization state into product source.
        req(not (ROOT/'instances'/bid).exists(),'front-door regression leaked organization state into product instances/')
        req(not (ROOT/'runtime/runs'/bid).exists(),'front-door regression leaked Run state into product runtime/')

    print('AURA entry regression passed: organization retrieval + model-owned method selection without execution-control machinery')


if __name__=='__main__':main()
