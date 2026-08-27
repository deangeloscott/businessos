#!/usr/bin/env python3
"""Maintainer-side controller for blind AURA business-work qualification.

The candidate/model should receive only the staged AURA product, the organization
workspace, and the plain-language business request printed by `start`. Checkpoints,
fixture releases, receipts, evaluator mappings, and qualification state remain outside
the candidate environment.
"""
from pathlib import Path
import argparse, json

from common import now, read_json, snapshot_diff, write_json
from checkpoint import capture_checkpoint
from release_fixture import release_event

VALID_BLOCKERS={
    'external_capability','authorization','missing_required_data','external_service',
    'qualification_fixture','aura_process'
}


def _load(run_dir):
    rd=Path(run_dir).expanduser().resolve()
    run=read_json(rd/'run.json')
    queue=read_json(rd/'evaluator/queue.json')
    if not isinstance(run,dict) or not isinstance(queue,dict) or not isinstance(queue.get('events'),list):
        raise SystemExit(f'Not a prepared AURA qualification run: {rd}')
    return rd,run,queue


def _receipt_path(rd,event):
    return rd/event.get('receipt_path',f"evaluator/receipts/{event['event_id']}.json")


def classify(rd,event):
    eid=event['event_id']
    before=rd/'checkpoints'/eid/'before.json'
    after=rd/'checkpoints'/eid/'after.json'
    receipt=_receipt_path(rd,event)
    if after.exists() and receipt.exists(): state='terminal'
    elif before.exists() or after.exists() or receipt.exists(): state='in_progress'
    else: state='pending'
    return {
        'event_id':eid,'business_id':event.get('business_id'),'lane':event.get('lane'),
        'state':state,'before_checkpoint':before.exists(),'after_checkpoint':after.exists(),
        'controller_receipt':receipt.exists(),'receipt_path':str(receipt)
    }


def rows(rd,queue):
    return [classify(rd,e) for e in queue['events']]


def _event(rd,queue,event_id=None,prefer_in_progress=False):
    states=rows(rd,queue)
    if event_id:
        for event,state in zip(queue['events'],states):
            if event.get('event_id')==event_id:
                return event,state
        raise SystemExit(f'Unknown evaluator event: {event_id}')
    if prefer_in_progress:
        for event,state in zip(queue['events'],states):
            if state['state']=='in_progress': return event,state
    for event,state in zip(queue['events'],states):
        if state['state']!='terminal': return event,state
    return None,None


def _changed_objects(before,after):
    b={x.get('id'):x.get('sha256') for x in (before or {}).get('objects',[]) if x.get('id')}
    return [x for x in (after or {}).get('objects',[]) if x.get('id') and b.get(x.get('id'))!=x.get('sha256')]


def _changed_runs(before,after,event):
    b={x.get('run_id'):(x.get('status'),x.get('contract_id')) for x in (before or {}).get('runs',[]) if x.get('run_id')}
    out=[]
    for row in (after or {}).get('runs',[]):
        rid=row.get('run_id')
        if not rid: continue
        prior=b.get(rid)
        changed=prior is None or prior!=(row.get('status'),row.get('contract_id'))
        if not changed: continue
        if event.get('contract_id') and row.get('contract_id')!=event.get('contract_id'): continue
        out.append(row)
    return out


def _root_evidence(workspace,business_id,run_ids):
    refs=[]
    for rid in run_ids:
        manifest=read_json(workspace/'runtime'/'runs'/business_id/rid/'contract-execution.json',{}) or {}
        for ref in manifest.get('root_evidence_refs') or []:
            if isinstance(ref,str) and ref not in refs: refs.append(ref)
    return refs


def _changed_workspace_paths(before,after):
    diff=snapshot_diff((before or {}).get('workspace',{}),(after or {}).get('workspace',{}))
    return diff.get('created',[])+diff.get('modified',[])


def derive_receipt(rd,run,event,blocker_classification=None,blocker_detail=None):
    eid=event['event_id']; workspace=Path(run['workspace'])
    before=read_json(rd/'checkpoints'/eid/'before.json',{}) or {}
    after=read_json(rd/'checkpoints'/eid/'after.json',{}) or {}
    changed_runs=_changed_runs(before,after,event)
    run_ids=[x['run_id'] for x in changed_runs if x.get('run_id')]
    artifact_refs=_root_evidence(workspace,event['business_id'],run_ids)
    changed_objects=_changed_objects(before,after)
    canonical_refs=[]; source_refs=[]
    for obj in changed_objects:
        path=obj.get('path')
        if not isinstance(path,str): continue
        if path not in canonical_refs: canonical_refs.append(path)
        if obj.get('object_type')=='SourceRecord' and path not in source_refs: source_refs.append(path)
    changed_paths=_changed_workspace_paths(before,after)
    field_refs=[]
    for path in changed_paths:
        normalized=str(path).replace('\\','/')
        if normalized.startswith('attachments/supplied/'): continue
        if normalized.startswith('attachments/') or '/intelligence/sources/' in normalized or '/evidence/' in normalized:
            if normalized not in field_refs: field_refs.append(normalized)
    release_audit=read_json(rd/'evaluator'/'releases'/f'{eid}.json',{}) or {}
    released_refs=[]
    released=release_audit.get('released_path')
    if isinstance(released,str):
        try: released_refs.append(Path(released).resolve().relative_to(workspace.resolve()).as_posix())
        except ValueError: released_refs.append(released)
    completed=bool(changed_runs) and all(x.get('status')=='completed' for x in changed_runs)
    blocker=None
    if blocker_classification:
        if blocker_classification not in VALID_BLOCKERS:
            raise SystemExit('Invalid blocker classification: '+blocker_classification)
        blocker={'classification':blocker_classification,'detail':blocker_detail or 'Required condition was unavailable during the business task.'}
        status='blocked'
    elif completed:
        status='completed'
    else:
        status='blocked'
        blocker={'classification':'aura_process','detail':'The controller did not observe a completed matching root AURA Run for this business task.'}
    receipt={
        'format_version':'2.0','generated_by':'qualification_controller','generated_at':now(),
        'event_id':eid,'business_id':event['business_id'],'status':status,'root_run_ids':run_ids,
        'artifact_refs':artifact_refs,'canonical_refs':canonical_refs,'source_refs':source_refs,
        'field_snapshot_refs':field_refs,'released_fixture_refs':released_refs,
        'summary':f'Controller observed {len(run_ids)} changed matching root Run(s), {len(changed_objects)} changed canonical object(s), and {len(artifact_refs)} root evidence reference(s).',
        'blocker':blocker,'quality_notes':'Controller-generated bookkeeping only; professional quality is evaluated separately.'
    }
    write_json(_receipt_path(rd,event),receipt)
    return receipt


def start(run_dir,event_id=None):
    rd,run,queue=_load(run_dir); event,state=_event(rd,queue,event_id)
    if not event:
        return {'status':'complete','message':'All prepared business tasks are terminal. Run the evaluator.'}
    # Preserve the original baseline across provider/session interruption.
    if not state['before_checkpoint']:
        capture_checkpoint(Path(run['product_root']),Path(run['workspace']),rd,event['event_id'],'before',event['business_id'])
    if event.get('release_fixture') and not (rd/'evaluator'/'releases'/f"{event['event_id']}.json").exists():
        release_event(rd,event['event_id'])
    run['execution_status']='in_progress'; run['active_event_id']=event['event_id']; write_json(rd/'run.json',run)
    return {
        'status':'ready','product_root':run['product_root'],'workspace':run['workspace'],
        'business_id':event['business_id'],'business_request':event['task'],
        'candidate_message':event['task'],
        'maintainer_note':'Give the model only the staged product/workspace and candidate_message. Do not give it the qualification run directory, evaluator files, event ID, checkpoints, receipts, or scoring metadata.',
        'finish_command':f'python3 qualification/task_controller.py finish "{rd}"'
    }


def finish(run_dir,event_id=None,blocker_classification=None,blocker_detail=None):
    rd,run,queue=_load(run_dir)
    active=event_id or run.get('active_event_id')
    event,state=_event(rd,queue,active,prefer_in_progress=True)
    if not event: raise SystemExit('No unfinished business task is available to finish')
    if not state['before_checkpoint']:
        raise SystemExit(f"Task {event['event_id']} has no before checkpoint; run controller start first")
    if not state['after_checkpoint']:
        capture_checkpoint(Path(run['product_root']),Path(run['workspace']),rd,event['event_id'],'after',event['business_id'])
    receipt=derive_receipt(rd,run,event,blocker_classification,blocker_detail)
    run.pop('active_event_id',None)
    remaining=[r for r in rows(rd,queue) if r['state']!='terminal']
    run['execution_status']='completed' if not remaining else 'prepared'; write_json(rd/'run.json',run)
    out={'status':'finished','event_id':event['event_id'],'controller_receipt':receipt,'remaining':len(remaining)}
    if remaining: out['next_command']=f'python3 qualification/task_controller.py start "{rd}"'
    else: out['evaluate_command']=f'python3 qualification/evaluate_run.py "{rd}"'
    return out


def status(run_dir):
    rd,run,queue=_load(run_dir); state_rows=rows(rd,queue)
    counts={k:sum(x['state']==k for x in state_rows) for k in ('terminal','in_progress','pending')}
    event,state=_event(rd,queue,prefer_in_progress=True)
    out={'run_dir':str(rd),'event_count':len(state_rows),**counts,'events':state_rows}
    if event:
        out['next_business_request']=event['task']; out['business_id']=event['business_id']
        out['start_command']=f'python3 qualification/task_controller.py start "{rd}"'
    else:
        out['evaluate_command']=f'python3 qualification/evaluate_run.py "{rd}"'
    return out


def main():
    ap=argparse.ArgumentParser(description='External controller for blind AURA qualification business tasks.')
    sub=ap.add_subparsers(dest='command',required=True)
    for name in ('start','status'):
        p=sub.add_parser(name); p.add_argument('run_dir'); p.add_argument('--event-id')
    p=sub.add_parser('finish'); p.add_argument('run_dir'); p.add_argument('--event-id'); p.add_argument('--blocker-classification',choices=sorted(VALID_BLOCKERS)); p.add_argument('--blocker-detail')
    a=ap.parse_args()
    if a.command=='start': result=start(a.run_dir,a.event_id)
    elif a.command=='finish': result=finish(a.run_dir,a.event_id,a.blocker_classification,a.blocker_detail)
    else: result=status(a.run_dir)
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
