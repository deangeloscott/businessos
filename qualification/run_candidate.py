#!/usr/bin/env python3
"""Run one blind qualification event through any command-line model/harness.

This is maintainer tooling, not AURA runtime architecture. It does only three things
that should not be left to ad-hoc shell scripts:
- pin the staged organization workspace for AURA helpers;
- preserve the candidate-visible command output for professional review;
- record a harness execution failure as an external qualification blocker while
  returning success to the surrounding batch so later independent cases can continue.

The wrapped command must contain either `{candidate_prompt}` or
`{candidate_message}` as an argument placeholder. Example:

    python3 qualification/run_candidate.py /path/to/run -- \
      your-agent-cli -p '{candidate_prompt}'
"""
from pathlib import Path
import argparse,json,os,subprocess,sys
from common import now,read_json,write_json
from task_controller import start,finish

PROMPT_TOKEN='{candidate_prompt}'
MESSAGE_TOKEN='{candidate_message}'


def candidate_prompt(started):
    return 'Use the AURA product in ./product and the organization workspace in ./workspace.\n\n'+started['candidate_message']


def candidate_environment(run):
    env=dict(os.environ)
    env['BUSINESSOS_WORKSPACE']=str(run['workspace'])
    env.pop('BUSINESSOS_WORKSPACE_CONFIG',None)
    env.pop('AURA_QUALIFICATION_RUN',None)
    env['PYTHONDONTWRITEBYTECODE']='1'
    env['PYTHONUTF8']='1'
    return env


def render_command(command,started,run):
    prompt=candidate_prompt(started)
    replacements={
        PROMPT_TOKEN:prompt,
        MESSAGE_TOKEN:started['candidate_message'],
        '{product_root}':str(run['product_root']),
        '{workspace}':str(run['workspace']),
        '{candidate_surface}':str(run['candidate_surface_root']),
    }
    rendered=[]
    for arg in command:
        value=arg
        for token,replacement in replacements.items():value=value.replace(token,replacement)
        rendered.append(value)
    return rendered


def execute(command,cwd,env,log_path):
    log_path=Path(log_path);log_path.parent.mkdir(parents=True,exist_ok=True)
    with log_path.open('w',encoding='utf-8') as log:
        proc=subprocess.Popen(command,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
        assert proc.stdout is not None
        for chunk in proc.stdout:
            sys.stdout.write(chunk);sys.stdout.flush();log.write(chunk);log.flush()
        return proc.wait()


def main():
    ap=argparse.ArgumentParser(description='Run one blind AURA qualification event through a command-line model/harness.')
    ap.add_argument('run_dir')
    ap.add_argument('--event-id')
    ap.add_argument('command',nargs=argparse.REMAINDER,help='Command after --. Include {candidate_prompt} or {candidate_message} in one argument.')
    a=ap.parse_args()
    command=list(a.command)
    if command and command[0]=='--':command=command[1:]
    if not command:raise SystemExit('A candidate command is required after --')
    if not any(PROMPT_TOKEN in arg or MESSAGE_TOKEN in arg for arg in command):
        raise SystemExit('Candidate command must contain {candidate_prompt} or {candidate_message} so the ordinary business request is actually delivered')

    rd=Path(a.run_dir).expanduser().resolve()
    started=start(rd,a.event_id)
    if started.get('status')!='ready':
        print(json.dumps(started,indent=2));return
    run=read_json(rd/'run.json') or {}
    event_id=run.get('active_event_id')
    if not event_id:raise SystemExit('Controller did not expose an active qualification event')
    surface=Path(run['candidate_surface_root'])
    response_ref=f'evaluator/candidate-responses/{event_id}.txt'
    response_path=rd/response_ref
    execution_ref=f'evaluator/candidate-executions/{event_id}.json'
    execution_path=rd/execution_ref
    if response_path.exists() or execution_path.exists():
        raise SystemExit(f'Candidate execution evidence already exists for {event_id}; preserve it and prepare a fresh run for a clean retry')

    rendered=render_command(command,started,run)
    record={
        'format_version':'1.0','event_id':event_id,'started_at':now(),'status':'running',
        'candidate_surface_root':str(surface),'workspace_pin':str(run['workspace']),
        'response_ref':response_ref,'command_program':rendered[0]
    }
    write_json(execution_path,record)
    code=execute(rendered,surface,candidate_environment(run),response_path)
    record.update({'finished_at':now(),'exit_code':code,'status':'completed' if code==0 else 'harness_error'})
    write_json(execution_path,record)

    if code==0:
        controller=finish(rd,event_id=event_id)
        blocker=None
    else:
        detail=f'Candidate model/harness command exited with status {code}; see {execution_ref}. This is an external execution failure, not evidence of an AURA product defect.'
        controller=finish(rd,event_id=event_id,blocker_classification='external_capability',blocker_detail=detail)
        blocker='external_capability'

    print(json.dumps({
        'run_dir':str(rd),'event_id':event_id,'candidate_exit_code':code,
        'candidate_response':str(response_path),'candidate_execution':str(execution_path),
        'workspace_pin':str(run['workspace']),'qualification_blocker':blocker,
        'controller_status':controller.get('status'),'remaining':controller.get('remaining')
    },indent=2))
    # Candidate-process failures are recorded above instead of terminating a surrounding
    # multi-case shell campaign. Runner/controller failures still exit nonzero normally.


if __name__=='__main__':main()
