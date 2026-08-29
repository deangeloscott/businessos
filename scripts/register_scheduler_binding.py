#!/usr/bin/env python3
"""Record a verified host/OS/workflow scheduler binding in regenerable environment state.

This helper does not create an external schedule. Call it only after the active harness/tool
has actually created or verified the schedule/reminder and can provide a concrete executor ref.
"""
from _common import *
from jsonschema import Draft202012Validator
import argparse, json, os

EXECUTOR_KINDS={"harness_scheduler","os_scheduler","workflow_runner","viraltrac","reminder_only","other"}
TARGET_KINDS={"subject","source_profile","business_monitoring","reminder"}
STATUSES={"active","paused","disabled","error"}


def _schema():
    return json.loads((ROOT/'core/schemas/runtime/scheduler-bindings.schema.json').read_text())


def _validate(data):
    errors=sorted(Draft202012Validator(_schema()).iter_errors(data),key=lambda e:list(e.path))
    if errors: raise ValueError('scheduler bindings invalid: '+'; '.join(f'{list(e.path)} {e.message}' for e in errors))


def _path(environment):
    if not environment_exists(environment): raise ValueError(f'Unknown environment: {environment}')
    return environment_overlay_dir(environment,create=True)/'scheduler-bindings.json'


def register(args):
    if not instance_dir(args.business_id).exists(): raise ValueError(f'Unknown business: {args.business_id}')
    if args.target_kind=='subject' and not args.subject_key: raise ValueError('--target-kind subject requires --subject-key')
    if args.target_kind=='source_profile' and not args.source_profile_id: raise ValueError('--target-kind source_profile requires --source-profile-id')
    if args.status=='active' and not args.verified_at: raise ValueError('active scheduler binding requires --verified-at from the actual scheduler/host verification')
    if not args.executor_ref.strip(): raise ValueError('--executor-ref must identify the real created/verified schedule or reminder')
    path=_path(args.environment)
    data=json.loads(path.read_text()) if path.exists() else {'format_version':'1.0','bindings':[]}
    data.setdefault('format_version','1.0');data.setdefault('bindings',[])
    ts=now();existing=next((x for x in data['bindings'] if x.get('id')==args.binding_id),None)
    created_at=(existing or {}).get('created_at') or ts
    row={
        'id':args.binding_id,
        'environment':args.environment,
        'business_id':args.business_id,
        'target_kind':args.target_kind,
        'subject_key':args.subject_key,
        'source_profile_id':args.source_profile_id,
        'executor_kind':args.executor_kind,
        'executor_ref':args.executor_ref,
        'cadence_expression':args.cadence_expression,
        'timezone':args.timezone,
        'status':args.status,
        'next_run_at':args.next_run_at,
        'last_verified_at':args.verified_at or (existing or {}).get('last_verified_at') or ts,
        'created_at':created_at,
        'updated_at':ts,
        'notes':args.notes
    }
    if args.target_kind!='subject': row['subject_key']=None
    if args.target_kind!='source_profile': row['source_profile_id']=None
    if existing: data['bindings'][data['bindings'].index(existing)]=row
    else:data['bindings'].append(row)
    _validate(data)
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n');os.replace(tmp,path)
    return row,path


def main():
    p=argparse.ArgumentParser(description='Record an actual verified scheduler/reminder binding. This does not create the external schedule itself.')
    p.add_argument('environment',nargs='?',default='local')
    p.add_argument('binding_id',help='Stable ID beginning sched_')
    p.add_argument('--business-id',required=True)
    p.add_argument('--target-kind',required=True,choices=sorted(TARGET_KINDS))
    p.add_argument('--subject-key')
    p.add_argument('--source-profile-id')
    p.add_argument('--executor-kind',required=True,choices=sorted(EXECUTOR_KINDS))
    p.add_argument('--executor-ref',required=True,help='Concrete host/OS/workflow schedule/reminder reference or receipt')
    p.add_argument('--cadence-expression',required=True)
    p.add_argument('--timezone')
    p.add_argument('--status',choices=sorted(STATUSES),default='active')
    p.add_argument('--next-run-at')
    p.add_argument('--verified-at',help='ISO timestamp from/for the actual scheduler verification; required for active bindings')
    p.add_argument('--notes')
    a=p.parse_args()
    if not a.binding_id.startswith('sched_'): raise SystemExit('binding_id must begin sched_')
    try:row,path=register(a)
    except (ValueError,json.JSONDecodeError) as e:raise SystemExit(str(e))
    print(json.dumps({'binding':row,'state_ref':storage_ref(path),'rule':'This receipt proves schedule mechanics only; it does not prove the future AURA work ran or succeeded.'},indent=2))

if __name__=='__main__':main()
