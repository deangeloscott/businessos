#!/usr/bin/env python3
from pathlib import Path
import argparse, json


def _read_json(path):
    try: return json.loads(Path(path).read_text())
    except Exception: return None


def _event_runs(run_dir,event,before):
    meta=_read_json(run_dir/'run.json') or {}; workspace=Path(meta.get('workspace',''))
    if not workspace.exists(): return []
    base=workspace/'runtime'/'runs'/event.get('business_id','')
    if not base.exists(): return []
    before_map={r.get('run_id'):(r.get('status'),r.get('workflow_id')) for r in (before or {}).get('runs',[]) if r.get('run_id')}
    rows=[]
    for p in sorted(base.glob('*/run.json')):
        d=_read_json(p)
        if not isinstance(d,dict): continue
        rid=d.get('run_id'); prior=before_map.get(rid)
        changed=prior is None or prior!=(d.get('status'),d.get('workflow_id'))
        if not changed: continue
        if event.get('workflow_id') and d.get('workflow_id')!=event.get('workflow_id'): continue
        rows.append({'run_id':rid,'workflow_id':d.get('workflow_id'),'status':d.get('status'),'path':str(p)})
    return rows


def classify(run_dir,event):
    eid=event['event_id']; before_path=run_dir/'checkpoints'/eid/'before.json'; after_path=run_dir/'checkpoints'/eid/'after.json'; receipt_path=run_dir/event.get('receipt_path',f'evaluator/receipts/{eid}.json')
    before=_read_json(before_path) if before_path.exists() else None; after=_read_json(after_path) if after_path.exists() else None; receipt=_read_json(receipt_path) if receipt_path.exists() else None
    if after is not None and receipt is not None: state='terminal'
    elif before is not None or after is not None or receipt is not None: state='in_progress'
    else: state='pending'
    return {'event_id':eid,'kind':event.get('kind'),'business_id':event.get('business_id'),'workflow_id':event.get('workflow_id'),'state':state,'before_checkpoint':before is not None,'controller_receipt':receipt is not None,'receipt_status':receipt.get('status') if isinstance(receipt,dict) else None,'after_checkpoint':after is not None,'receipt_path':str(receipt_path),'event_runs':_event_runs(run_dir,event,before)}


def _resume_text(run_dir,queue,rows):
    remaining=[(i,r) for i,r in enumerate(rows) if r['state']!='terminal']
    if not remaining: return f'# AURA Qualification Recovery\n\nThe prepared work in `{run_dir}` is complete. Run the evaluator.\n'
    idx,row=remaining[0]; event=queue['events'][idx]
    lines=['# AURA Qualification Recovery','',f'Run: `{run_dir}`',f'Completed tasks before resume point: **{idx} of {len(rows)}**.','',
           'The candidate/model should still receive only the normal AURA product/workspace and an ordinary business request. Do not expose evaluator metadata, workflow targets, checkpoints, receipts, or qualification rules.','',
           '**Request to give the candidate:**','',event.get('task','')]
    if row['state']=='in_progress':
        lines += ['', 'This task already has its original before-checkpoint. Keep that baseline and resume the existing AURA workspace rather than restarting the benchmark.']
        if row['event_runs']:
            lines.append('Observed task Run(s): '+', '.join(f"{r['run_id']} ({r.get('status')})" for r in row['event_runs']))
    lines += ['',f'Controller command: `python3 qualification/task_controller.py start "{run_dir}"`','']
    return '\n'.join(lines)


def main():
    ap=argparse.ArgumentParser(description='Inspect an interrupted blind AURA qualification run without creating candidate-visible test instructions.')
    ap.add_argument('run_dir'); ap.add_argument('--write-instructions',action='store_true'); ap.add_argument('--json',action='store_true'); a=ap.parse_args(); run_dir=Path(a.run_dir).expanduser().resolve()
    queue_path=run_dir/'evaluator/queue.json'
    if not queue_path.exists(): raise SystemExit(f'Evaluator queue not found: {queue_path}')
    queue=_read_json(queue_path)
    if not isinstance(queue,dict) or not isinstance(queue.get('events'),list): raise SystemExit(f'Invalid evaluator queue: {queue_path}')
    rows=[classify(run_dir,e) for e in queue['events']]; terminal=sum(r['state']=='terminal' for r in rows); in_progress=sum(r['state']=='in_progress' for r in rows); pending=sum(r['state']=='pending' for r in rows); first=next((r for r in rows if r['state']!='terminal'),None)
    summary={'run_dir':str(run_dir),'event_count':len(rows),'terminal':terminal,'in_progress':in_progress,'pending':pending,'first_unfinished':first}; text=_resume_text(run_dir,queue,rows)
    if a.write_instructions:
        out=run_dir/'evaluator/RECOVERY.md'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(text,encoding='utf-8'); summary['recovery_instructions']=str(out)
    if a.json: print(json.dumps({'summary':summary,'events':rows},indent=2))
    else:
        print(json.dumps(summary,indent=2))
        if a.write_instructions: print(f"Wrote {summary['recovery_instructions']}")
        elif first: print('\n'+text)

if __name__=='__main__': main()
