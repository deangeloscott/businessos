#!/usr/bin/env python3
from pathlib import Path
import argparse, json, os, shlex, subprocess
from common import now, write_json
from task_controller import start, finish


def main():
    ap=argparse.ArgumentParser(description='Launch one external AI/harness command against the next blind AURA business task.')
    ap.add_argument('run_dir')
    ap.add_argument('--command',required=True,help='Shell command template. Candidate-safe placeholders: {request} {workspace} {product_root} {business_id}')
    ap.add_argument('--label',default='candidate')
    a=ap.parse_args(); rd=Path(a.run_dir).expanduser().resolve()
    task=start(rd)
    if task.get('status')=='complete': print(json.dumps(task,indent=2)); return
    forbidden=('{instructions}','{run_dir}','{event_id}','{qualification}')
    if any(x in a.command for x in forbidden):
        raise SystemExit('Blind qualification launch templates may not expose qualification/run metadata. Use only {request}, {workspace}, {product_root}, and {business_id}.')
    values={'request':task['candidate_message'],'workspace':task['workspace'],'product_root':task['product_root'],'business_id':task['business_id']}
    quote=(lambda v:subprocess.list2cmdline([str(v)])) if os.name=='nt' else (lambda v:shlex.quote(str(v)))
    command=a.command.format(**{k:quote(v) for k,v in values.items()})
    env=dict(os.environ); env['BUSINESSOS_WORKSPACE']=task['workspace']; env['PYTHONDONTWRITEBYTECODE']='1'; env['PYTHONUTF8']='1'
    # Do not expose AURA_QUALIFICATION_RUN or evaluator paths to the candidate process.
    env.pop('AURA_QUALIFICATION_RUN',None)
    logs=rd/'evaluator'/'logs'; logs.mkdir(parents=True,exist_ok=True); out=logs/f'{a.label}.stdout.log'; err=logs/f'{a.label}.stderr.log'
    launch={'label':a.label,'business_id':task['business_id'],'command':command,'started_at':now(),'stdout':str(out),'stderr':str(err),'candidate_blind':True}; write_json(logs/f'{a.label}.launch.json',launch)
    with out.open('a') as fo, err.open('a') as fe:
        proc=subprocess.run(command,cwd=task['product_root'],env=env,shell=True,stdout=fo,stderr=fe,text=True)
    launch.update({'completed_at':now(),'returncode':proc.returncode})
    if proc.returncode==0:
        launch['controller_finish']=finish(rd)
    else:
        launch['controller_finish']=None; launch['recovery']='Task remains in progress with its original before-checkpoint. Use task_controller.py status/resume_status.py before replacement execution.'
    write_json(logs/f'{a.label}.launch.json',launch)
    print(json.dumps(launch,indent=2)); raise SystemExit(proc.returncode)

if __name__=='__main__': main()
