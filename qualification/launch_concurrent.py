#!/usr/bin/env python3
from pathlib import Path
import argparse, json, os, shlex, subprocess
from common import now, read_json, write_json
from task_controller import start, finish, classify


def make_command(template,values):
    forbidden=('{instructions}','{run_dir}','{event_id}','{qualification}')
    if any(x in template for x in forbidden):
        raise SystemExit('Blind concurrent launch templates may not expose qualification/run metadata. Use only {request}, {workspace}, {product_root}, {business_id}, and {operator_ref}.')
    return template.format(**{k:shlex.quote(str(v)) for k,v in values.items()})


def lane_event(rd,queue,lane):
    for event in queue.get('events',[]):
        if event.get('lane')!=lane: continue
        if classify(rd,event)['state']!='terminal': return event
    return None


def main():
    ap=argparse.ArgumentParser(description='Launch two blind AURA business tasks concurrently against one shared organization workspace.')
    ap.add_argument('run_dir'); ap.add_argument('--command-a',required=True); ap.add_argument('--command-b',required=True); a=ap.parse_args()
    rd=Path(a.run_dir).expanduser().resolve(); meta=read_json(rd/'run.json'); queue=read_json(rd/'evaluator/queue.json')
    if not isinstance(meta,dict) or not isinstance(queue,dict): raise SystemExit('Prepared concurrency run metadata missing')
    logs=rd/'evaluator'/'logs'; logs.mkdir(parents=True,exist_ok=True)
    procs=[]; handles=[]
    for lane,template in [('A',a.command_a),('B',a.command_b)]:
        event=lane_event(rd,queue,lane)
        if event is None: continue
        task=start(rd,event['event_id']); operator_ref=f'operator-{lane.lower()}'
        vals={'request':task['candidate_message'],'workspace':task['workspace'],'product_root':task['product_root'],'business_id':task['business_id'],'operator_ref':operator_ref}
        cmd=make_command(template,vals)
        env=dict(os.environ); env['BUSINESSOS_WORKSPACE']=task['workspace']; env['BUSINESSOS_OPERATOR_REF']=operator_ref; env['PYTHONDONTWRITEBYTECODE']='1'; env['PYTHONUTF8']='1'; env.pop('AURA_QUALIFICATION_RUN',None)
        fo=(logs/f'lane-{lane.lower()}.stdout.log').open('a'); fe=(logs/f'lane-{lane.lower()}.stderr.log').open('a'); handles += [fo,fe]
        p=subprocess.Popen(cmd,cwd=task['product_root'],env=env,shell=True,stdout=fo,stderr=fe,text=True)
        procs.append((lane,event['event_id'],cmd,p))
    if not procs: print(json.dumps({'status':'complete','message':'No unfinished concurrency lane tasks remain.'},indent=2)); return
    started=now(); result=[]
    for lane,event_id,cmd,p in procs:
        rc=p.wait(); row={'lane':lane,'command':cmd,'returncode':rc,'candidate_blind':True}
        if rc==0: row['controller_finish']=finish(rd,event_id=event_id)
        else: row['controller_finish']=None; row['recovery']='Lane task remains in progress with its original before-checkpoint.'
        result.append(row)
    for h in handles: h.close()
    payload={'started_at':started,'completed_at':now(),'results':result}; write_json(logs/'concurrent-launch.json',payload); print(json.dumps(payload,indent=2))
    raise SystemExit(0 if all(x['returncode']==0 for x in result) else 1)

if __name__=='__main__': main()
