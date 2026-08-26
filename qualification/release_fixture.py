#!/usr/bin/env python3
from pathlib import Path
import argparse, json, os
from common import read_json, write_json, now

def main():
    ap=argparse.ArgumentParser(description='Release one intentionally withheld qualification evidence fixture at its scheduled event boundary.')
    ap.add_argument('event_id'); ap.add_argument('--run-dir'); a=ap.parse_args()
    raw=a.run_dir or os.environ.get('AURA_QUALIFICATION_RUN')
    if not raw: raise SystemExit('AURA_QUALIFICATION_RUN or --run-dir is required')
    rd=Path(raw).expanduser().resolve(); run=read_json(rd/'run.json'); queue=read_json(rd/'candidate/queue.json')
    if not run or not queue: raise SystemExit(f'Not an AURA qualification run: {rd}')
    events=queue.get('events',[]); index=next((i for i,x in enumerate(events) if x.get('event_id')==a.event_id),None)
    if index is None: raise SystemExit(f'Unknown qualification event: {a.event_id}')
    event=events[index]; release=event.get('release_fixture'); fixture=event.get('fixture')
    if not release: raise SystemExit(f'Event {a.event_id} has no release_fixture')
    before=rd/'checkpoints'/a.event_id/'before.json'
    if not before.exists(): raise SystemExit(f'Cannot release {a.event_id} evidence before its before-checkpoint exists')
    incomplete=[x.get('event_id') for x in events[:index] if not (rd/'checkpoints'/x.get('event_id','')/'after.json').exists()]
    if incomplete: raise SystemExit('Cannot release future evidence while earlier queue events are incomplete: '+', '.join(incomplete[:20]))
    hidden=rd/'evaluator'/'hidden-fixtures'/f'{fixture}-releases.json'; data=read_json(hidden)
    if release not in data: raise SystemExit(f'Hidden release {release!r} missing for fixture {fixture!r}')
    workspace=Path(run['workspace']); target=workspace/'attachments'/'qualification-inputs'/f'{fixture}-{release}.json'
    payload={'format_version':'1.0','qualification_event_id':a.event_id,'fixture':fixture,'release_fixture':release,'released_at':now(),'evidence':data[release]}
    if target.exists():
        existing=read_json(target)
        if existing.get('fixture')!=fixture or existing.get('release_fixture')!=release:
            raise SystemExit(f'Release target already exists with incompatible content: {target}')
    else:
        write_json(target,payload)
    audit=rd/'candidate'/'releases'/f'{a.event_id}.json'; audit.parent.mkdir(parents=True,exist_ok=True)
    write_json(audit,{'event_id':a.event_id,'fixture':fixture,'release_fixture':release,'released_path':str(target),'released_at':payload['released_at'],'prior_events_complete':True})
    print(json.dumps({'event_id':a.event_id,'released_fixture':release,'path':str(target)},indent=2))

if __name__=='__main__': main()
