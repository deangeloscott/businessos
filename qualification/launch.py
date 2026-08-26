#!/usr/bin/env python3
from pathlib import Path
import argparse, json, os, shlex, subprocess
from common import now, read_json, write_json

def main():
    ap=argparse.ArgumentParser(description='Launch one external AI/harness command against a prepared uninterrupted AURA qualification run.')
    ap.add_argument('run_dir'); ap.add_argument('--command',required=True,help='Shell command template. Placeholders: {instructions} {workspace} {run_dir} {product_root}')
    ap.add_argument('--label',default='candidate'); a=ap.parse_args()
    rd=Path(a.run_dir).expanduser().resolve(); meta=read_json(rd/'run.json')
    if not meta: raise SystemExit('run.json missing; prepare the run first')
    values={'instructions':str(rd/'candidate/RUN-INSTRUCTIONS.md'),'workspace':meta['workspace'],'run_dir':str(rd),'product_root':meta['product_root']}
    quote=(lambda v:subprocess.list2cmdline([v])) if os.name=='nt' else shlex.quote
    command=a.command.format(**{k:quote(v) for k,v in values.items()})
    env=dict(os.environ); env['BUSINESSOS_WORKSPACE']=meta['workspace']; env['AURA_QUALIFICATION_RUN']=str(rd); env['PYTHONDONTWRITEBYTECODE']='1'; env['PYTHONUTF8']='1'
    logs=rd/'candidate-logs'; logs.mkdir(exist_ok=True); out=logs/f'{a.label}.stdout.log'; err=logs/f'{a.label}.stderr.log'
    launch={'label':a.label,'command':command,'started_at':now(),'stdout':str(out),'stderr':str(err)}; write_json(logs/f'{a.label}.launch.json',launch)
    with out.open('a') as fo, err.open('a') as fe:
        proc=subprocess.run(command,cwd=meta['product_root'],env=env,shell=True,stdout=fo,stderr=fe,text=True)
    launch.update({'completed_at':now(),'returncode':proc.returncode}); write_json(logs/f'{a.label}.launch.json',launch)
    print(json.dumps(launch,indent=2)); raise SystemExit(proc.returncode)
if __name__=='__main__': main()
