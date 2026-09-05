#!/usr/bin/env python3
"""Run the independent qualification judge against exactly one prepared run.

This is maintainer-only evaluator tooling. It removes fragile shell ceremony by:
- constructing an explicit current-run-only judge prompt;
- running the judge from the selected evaluator run directory;
- preserving judge command output for diagnosis;
- verifying that judgments were written for exactly the events in this run's judge packet.

The wrapped command must contain `{judge_prompt}` as an argument placeholder. Example:

    python3 qualification/run_judge.py /path/to/run -- \
      your-agent-cli --add-dir '{candidate_surface}' -p '{judge_prompt}'
"""
from pathlib import Path
import argparse,json,os,subprocess,sys
from common import now,read_json,write_json

PROMPT_TOKEN='{judge_prompt}'


def judge_prompt(rd,run,instructions,judgments):
    surface=Path(run['candidate_surface_root']).resolve()
    return f'''You are the independent professional judge for exactly this qualification run:
{rd}

Read exactly this instruction file:
{instructions}

The candidate surface for this run is:
{surface}

Do not inspect, judge, reuse, continue, or write to any other qualification run, previous evaluator directory, previous session, or prior task.

Inspect only this run's candidate response, workspace state, evidence, artifacts, and persisted organizational meaning as directed by the instruction file. Verify important factual and product claims against this run's available evidence rather than trusting candidate assertions.

Write the required judgment only to:
{judgments}

Do not modify candidate work or AURA state.'''


def render_command(command,rd,run,instructions,judgments):
    replacements={
        PROMPT_TOKEN:judge_prompt(rd,run,instructions,judgments),
        '{run_dir}':str(rd),
        '{candidate_surface}':str(Path(run['candidate_surface_root']).resolve()),
        '{judge_instructions}':str(instructions),
        '{judgments}':str(judgments),
    }
    rendered=[]
    for arg in command:
        value=arg
        for token,replacement in replacements.items():value=value.replace(token,replacement)
        rendered.append(value)
    return rendered


def execute(command,cwd,log_path):
    env=dict(os.environ)
    env.pop('BUSINESSOS_WORKSPACE',None)
    env.pop('BUSINESSOS_WORKSPACE_CONFIG',None)
    env.pop('AURA_QUALIFICATION_RUN',None)
    env['PYTHONDONTWRITEBYTECODE']='1'
    env['PYTHONUTF8']='1'
    log_path=Path(log_path);log_path.parent.mkdir(parents=True,exist_ok=True)
    with log_path.open('w',encoding='utf-8') as log:
        proc=subprocess.Popen(command,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
        assert proc.stdout is not None
        for chunk in proc.stdout:
            sys.stdout.write(chunk);sys.stdout.flush();log.write(chunk);log.flush()
        return proc.wait()


def validate_judgments(judgments_path,packets):
    data=read_json(judgments_path)
    if not isinstance(data,list):return False,'judgments.json must contain a JSON array'
    expected=[p.get('event_id') for p in packets if isinstance(p,dict) and p.get('event_id')]
    actual=[]
    for row in data:
        if not isinstance(row,dict) or not row.get('event_id'):
            return False,'every judgment must be an object with event_id'
        actual.append(row['event_id'])
    if len(actual)!=len(set(actual)):return False,'judgments.json contains duplicate event_id values'
    if set(actual)!=set(expected):
        return False,f'judgment event IDs do not match this run: expected {expected}, got {actual}'
    return True,None


def main():
    ap=argparse.ArgumentParser(description='Run an independent professional judge against exactly one AURA qualification run.')
    ap.add_argument('run_dir')
    ap.add_argument('command',nargs=argparse.REMAINDER,help='Command after --. Include {judge_prompt} in one argument.')
    a=ap.parse_args()
    command=list(a.command)
    if command and command[0]=='--':command=command[1:]
    if not command:raise SystemExit('A judge command is required after --')
    if not any(PROMPT_TOKEN in arg for arg in command):raise SystemExit('Judge command must contain {judge_prompt}')

    rd=Path(a.run_dir).expanduser().resolve()
    run=read_json(rd/'run.json') or {}
    packets=read_json(rd/'evaluator/review-packets-to-judge.json')
    instructions=(rd/'evaluator/JUDGE-INSTRUCTIONS.md').resolve()
    judgments=(rd/'evaluator/judgments.json').resolve()
    if not run or not run.get('candidate_surface_root'):raise SystemExit(f'Not a prepared qualification run: {rd}')
    if not isinstance(packets,list):raise SystemExit('review-packets-to-judge.json missing; run evaluate_run.py and build_judge_prompt.py first')
    if not instructions.is_file():raise SystemExit('JUDGE-INSTRUCTIONS.md missing; run build_judge_prompt.py first')
    if judgments.exists():raise SystemExit(f'Judgment already exists at {judgments}; preserve it or prepare a fresh run rather than silently overwriting review evidence')

    expected=[p.get('event_id') for p in packets if isinstance(p,dict) and p.get('event_id')]
    if not expected:raise SystemExit('Judge packet contains no reviewable events')
    execution_path=rd/'evaluator/judge-execution.json'
    output_path=rd/'evaluator/judge-output.txt'
    if execution_path.exists() or output_path.exists():raise SystemExit('Judge execution evidence already exists for this run; preserve it before retrying')

    rendered=render_command(command,rd,run,instructions,judgments)
    record={'format_version':'1.0','started_at':now(),'status':'running','run_dir':str(rd),'expected_event_ids':expected,'candidate_surface_root':str(Path(run['candidate_surface_root']).resolve()),'judgments_path':str(judgments),'command_program':rendered[0]}
    write_json(execution_path,record)
    code=execute(rendered,rd,output_path)
    valid=False;error=None
    if code==0:
        if not judgments.exists():error='judge command exited successfully but did not write this run judgments.json'
        else:valid,error=validate_judgments(judgments,packets)
    else:error=f'judge command exited with status {code}'
    record.update({'finished_at':now(),'exit_code':code,'status':'completed' if code==0 and valid else 'judge_error','judgment_valid':valid,'error':error,'output_path':str(output_path)})
    write_json(execution_path,record)
    print(json.dumps(record,indent=2))
    if code!=0 or not valid:raise SystemExit(error or 'judge output did not validate')


if __name__=='__main__':main()
