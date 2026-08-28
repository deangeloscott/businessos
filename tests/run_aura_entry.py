#!/usr/bin/env python3
"""Focused regression for the harness-neutral AURA business-work front door."""
from pathlib import Path
import json, os, shutil, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'


def require(cond,msg):
    if not cond:raise AssertionError(msg)


def run(args,env,check=True):
    p=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,env=env,capture_output=True,text=True)
    if check and p.returncode!=0:raise AssertionError(f"command failed: {args}\nstdout={p.stdout}\nstderr={p.stderr}")
    return p


def init_business(bid,env):
    run([SCRIPTS/'init_business.py',bid,'--name',bid.replace('-',' ').title()],env)


def enter(request,bid,workspace,env,*extra):
    p=run([SCRIPTS/'enter.py',request,'--business-id',bid,'--workspace',workspace,*extra],env)
    return json.loads(p.stdout)


def main():
    with tempfile.TemporaryDirectory(prefix='aura-entry-regression-') as td:
        ws=Path(td).resolve();env=os.environ.copy();env['BUSINESSOS_WORKSPACE']=str(ws)
        bid='entry-regression'
        init_business(bid,env)
        request='Create a presentation for this business.'
        first=enter(request,bid,ws,env)
        require(first.get('status')=='ready',f'entry should be ready: {first}')
        require(first.get('business_id')==bid,'explicit business should resolve')
        require(first.get('original_request')==request,'original request must be preserved')
        require(first.get('route',{}).get('contract_id')=='content.production.presentation',f'expected presentation route, got {first.get("route")}')
        rid=first.get('run',{}).get('run_id');require(rid and rid.startswith('run_'),'entry should create a bounded Run')
        work=ws/'runtime/runs'/bid/rid/'work';require(work.is_dir(),'entry Run must expose workspace-owned work/')
        require(Path(first['run']['work_dir']).resolve()==work.resolve(),'returned work_dir should be the actual Run work directory')
        require(first['run'].get('resumed') is False,'first entry should create, not resume')
        require(first.get('execution_env',{}).get('BUSINESSOS_RUN_ID')==rid,'execution envelope should identify the Run')
        require(first.get('context_plan',{}).get('run_id')==rid,'context plan must be bound to the Run')
        require(first.get('process_plan',{}).get('entry_contract')=='content.production.presentation','process plan should use routed root contract')

        second=enter(request,bid,ws,env)
        require(second.get('status')=='ready','repeat entry should remain ready')
        require(second.get('run',{}).get('run_id')==rid,'exact active request should resume the existing Run')
        require(second.get('run',{}).get('resumed') is True,'repeat entry should report resumed')

        third=enter(request,bid,ws,env,'--new-run')
        require(third.get('run',{}).get('run_id')!=rid,'--new-run should force a distinct Run')
        require(third.get('run',{}).get('resumed') is False,'forced new Run should not report resumed')

        second_bid='entry-regression-two';init_business(second_bid,env)
        ambiguous=run([SCRIPTS/'enter.py','Analyze our business.','--workspace',ws],env,check=False)
        require(ambiguous.returncode==2,'ambiguous business entry should be non-ready')
        payload=json.loads(ambiguous.stdout)
        require(payload.get('status')=='needs_input' and 'active_business' in payload.get('missing',[]),f'multiple businesses must not be silently selected: {payload}')
        require(sorted(payload.get('available_business_ids',[]))==sorted([bid,second_bid]),'ambiguous response should expose available business IDs')

        # External-workspace entry must not create corresponding business state under product root.
        require(not (ROOT/'instances'/bid).exists(),'entry regression leaked business state into product instances/')
        require(not (ROOT/'runtime/runs'/bid).exists(),'entry regression leaked Run state into product runtime/')

    print('aura entry regressions passed')


if __name__=='__main__':main()
