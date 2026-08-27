#!/usr/bin/env python3
from pathlib import Path
import argparse, json
from common import read_json, write_json, now


def release_event(run_dir,event_id):
    rd=Path(run_dir).expanduser().resolve(); run=read_json(rd/'run.json'); queue=read_json(rd/'evaluator/queue.json')
    if not isinstance(run,dict) or not isinstance(queue,dict): raise SystemExit(f'Not an AURA qualification run: {rd}')
    events=queue.get('events',[]); index=next((i for i,x in enumerate(events) if x.get('event_id')==event_id),None)
    if index is None: raise SystemExit(f'Unknown evaluator event: {event_id}')
    event=events[index]; release=event.get('release_fixture'); fixture=event.get('fixture')
    if not release: raise SystemExit(f'Event {event_id} has no release_fixture')
    before=rd/'checkpoints'/event_id/'before.json'
    if not before.exists(): raise SystemExit(f'Cannot release {event_id} evidence before its before-checkpoint exists')
    incomplete=[x.get('event_id') for x in events[:index] if not (rd/'checkpoints'/x.get('event_id','')/'after.json').exists()]
    if incomplete: raise SystemExit('Cannot release future evidence while earlier tasks are incomplete: '+', '.join(incomplete[:20]))
    hidden=rd/'evaluator'/'hidden-fixtures'/f'{fixture}-releases.json'; data=read_json(hidden)
    if not isinstance(data,dict) or release not in data: raise SystemExit(f'Hidden release {release!r} missing for fixture {fixture!r}')
    workspace=Path(run['workspace']); target=workspace/'attachments'/'supplied'/f'{fixture}-{release}.json'
    payload={'format_version':'1.0','supplied_at':now(),'source_type':'business_supplied_update','evidence':data[release]}
    if target.exists():
        existing=read_json(target)
        if existing!=payload and existing.get('evidence')!=payload.get('evidence'):
            raise SystemExit(f'Supplied-update target already exists with incompatible content: {target}')
    else:
        write_json(target,payload)
    audit=rd/'evaluator'/'releases'/f'{event_id}.json'
    write_json(audit,{'event_id':event_id,'fixture':fixture,'release_fixture':release,'released_path':str(target),'released_at':payload['supplied_at'],'prior_events_complete':True})
    return target,payload


def main():
    ap=argparse.ArgumentParser(description='Maintainer-side release of intentionally withheld business evidence at a qualification task boundary.')
    ap.add_argument('event_id'); ap.add_argument('--run-dir',required=True); a=ap.parse_args()
    target,payload=release_event(a.run_dir,a.event_id)
    print(json.dumps({'released_path':str(target),'source_type':payload['source_type']},indent=2))

if __name__=='__main__': main()
