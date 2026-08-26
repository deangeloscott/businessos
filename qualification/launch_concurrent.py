#!/usr/bin/env python3
from pathlib import Path
import argparse, json, os, shlex, subprocess
from common import now, read_json, write_json

def make_command(template,values): return template.format(**{k:shlex.quote(str(v)) for k,v in values.items()})
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('run_dir'); ap.add_argument('--command-a',required=True); ap.add_argument('--command-b',required=True); a=ap.parse_args()
    rd=Path(a.run_dir).expanduser().resolve(); meta=read_json(rd/'run.json'); logs=rd/'candidate-logs'; logs.mkdir(exist_ok=True)
    procs=[]; handles=[]
    for lane,template in [('A',a.command_a),('B',a.command_b)]:
        instructions=rd/f'candidate-{lane.lower()}/RUN-INSTRUCTIONS.md'; vals={'instructions':instructions,'workspace':meta['workspace'],'run_dir':rd,'product_root':meta['product_root']}; cmd=make_command(template,vals)
        env=dict(os.environ); env['BUSINESSOS_WORKSPACE']=meta['workspace']; env['AURA_QUALIFICATION_RUN']=str(rd); env['BUSINESSOS_OPERATOR_REF']=f'qualification-{lane.lower()}'; env['PYTHONDONTWRITEBYTECODE']='1'
        fo=(logs/f'lane-{lane.lower()}.stdout.log').open('a'); fe=(logs/f'lane-{lane.lower()}.stderr.log').open('a'); handles += [fo,fe]
        p=subprocess.Popen(cmd,cwd=meta['product_root'],env=env,shell=True,stdout=fo,stderr=fe,text=True); procs.append((lane,cmd,p))
    started=now(); result=[]
    for lane,cmd,p in procs: result.append({'lane':lane,'command':cmd,'returncode':p.wait()})
    for h in handles: h.close()
    payload={'started_at':started,'completed_at':now(),'results':result}; write_json(logs/'concurrent-launch.json',payload); print(json.dumps(payload,indent=2))
    raise SystemExit(0 if all(x['returncode']==0 for x in result) else 1)
if __name__=='__main__': main()
