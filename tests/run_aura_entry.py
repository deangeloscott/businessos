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
        ws=Path(td).resolve();env=os.environ.copy();env['BUSINESSOS_WORKSPACE']=str(ws);env['PYTHONDONTWRITEBYTECODE']='1';bid='entry-regression'
        run([S/'init_business.py',bid,'--name','Entry Regression'],env)
        supplied=ws/'attachments';supplied.mkdir(parents=True);source=supplied/'business-source.txt';source.write_text('The organization wants to create a presentation for a proposal.\n')
        run([S/'bootstrap_explicit_context.py',bid,'--facts-json',json.dumps({'objectives':['Create a presentation for a proposal']}),'--source-file',source],env)

        request='Create a presentation for this business proposal.';result,payload=enter(request,bid,ws,env)
        req(result.returncode==0 and payload.get('status')=='ready',f'entry should prepare useful work context: {payload}')
        req(payload.get('business_id')==bid and payload.get('original_request')==request,'entry lost business identity or original request')
        req(payload.get('run',{}).get('created') is False,'entry must not create a Run merely to begin reasoning')
        req({'aura_playbook','aura_workflow','external_skill','model_created','ad_hoc'}<=set(payload.get('method_options',[])),'entry lost method freedom')
        knowledge=payload.get('operating_knowledge') or {}
        req(knowledge.get('selected_playbook') is None and knowledge.get('selected_workflow') is None,'candidate discovery silently became method selection')
        req(knowledge.get('playbook_candidates'),f'presentation request should surface at least one high-level Playbook candidate: {knowledge}')
        req(knowledge.get('workflow_candidates'),f'presentation request should surface detailed Workflow candidates: {knowledge}')
        req(all(row.get('selection_authority') is False for row in knowledge.get('playbook_candidates',[])),'Playbook candidates claimed semantic authority')
        req(all(row.get('selection_authority') is False for row in knowledge.get('workflow_candidates',[])),'Workflow candidates claimed semantic authority')
        context_files=payload.get('retrieval',{}).get('context_files',[])
        req('CONTEXT.md' in context_files and 'docs/operating-knowledge.md' in context_files,'unselected entry lost small universal operating context')
        req('semantic intent and execution remain with the active intelligence/runtime' in payload.get('rule',''),'front door lost model/runtime ownership boundary')
        req('tool/provider allowlist' in payload.get('execution_rule',''),'front door lost tool/provider freedom boundary')
        req(not (ws/'runtime/runs'/bid).exists(),'entry created runtime Run state despite optional-Run architecture')

        # Explicit high-level Playbook selection frames the job but does not force an execution graph.
        pb_result,pb=enter(request,bid,ws,env,'--selected-playbook','content-synthesis-presentation')
        req(pb_result.returncode==0 and pb.get('status')=='ready','explicit Presentation Playbook selection should remain available')
        selected_pb=(pb.get('operating_knowledge') or {}).get('selected_playbook') or {}
        req(selected_pb.get('id')=='content-synthesis-presentation','explicit high-level Playbook selection was not preserved')
        req(pb.get('run',{}).get('created') is False,'Playbook selection must not auto-create a Run')

        # Explicit Workflow selection loads bounded procedure/context and still creates no Run.
        selected_result,selected=enter(request,bid,ws,env,'--selected-workflow','content.production.presentation')
        req(selected_result.returncode==0 and selected.get('status')=='ready','explicit AURA Workflow selection should remain available')
        op=selected.get('operating_knowledge') or {};sw=op.get('selected_workflow') or {}
        req(sw.get('workflow_id')=='content.production.presentation','explicit Workflow selection was not preserved')
        req(sw.get('selection_mode')=='explicit_model_selection','explicit model selection mode was lost')
        req(op.get('workflow_view') is not None,'selected AURA Workflow should expose its reusable browse view')
        req('workflow_process' not in op,'front door reintroduced process-plan framing for a Workflow browse view')
        req(selected.get('run',{}).get('created') is False,'explicit Workflow selection still must not auto-create a Run')
        loaded=selected.get('retrieval',{}).get('context_files',[])
        req('CONTEXT.md' in loaded and 'core/DEFAULTS.md' not in loaded and 'core/policies/agent-execution.md' not in loaded,'selected Workflow context reintroduced redundant universal instruction stack')

        second='entry-regression-two';run([S/'init_business.py',second,'--name','Entry Regression Two'],env)
        unresolved=run([S/'enter.py','Analyze the business.','--workspace',ws],env,check=False);data=json.loads(unresolved.stdout)
        req(unresolved.returncode==2 and data.get('status')=='needs_input','ambiguous organization should request only the missing organization choice')
        req(sorted(data.get('available_business_ids',[]))==sorted([bid,second]),'business-resolution handoff should expose stable IDs')
        names={row['id']:row['name'] for row in data.get('available_businesses',[])};req(names=={bid:'Entry Regression',second:'Entry Regression Two'},f'business-resolution handoff should expose human-readable organization names: {names}')

        req(not (ROOT/'instances'/bid).exists(),'front-door regression leaked organization state into product instances/')
        req(not (ROOT/'runtime/runs'/bid).exists(),'front-door regression leaked Run state into product runtime/')

    print('AURA entry regression passed: bounded organization retrieval + Playbook/Workflow discovery with model-owned execution')

if __name__=='__main__':main()
