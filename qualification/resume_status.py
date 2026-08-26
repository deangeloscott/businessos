#!/usr/bin/env python3
from pathlib import Path
import argparse, json

TERMINAL_RECEIPT_STATUSES={'completed','blocked'}


def _read_json(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return None


def _current_event_runs(run_dir,event,before):
    meta=_read_json(run_dir/'run.json') or {}
    workspace=Path(meta.get('workspace',''))
    if not workspace.exists(): return []
    base=workspace/'runtime'/'runs'/event.get('business_id','')
    if not base.exists(): return []
    before_ids={r.get('run_id') for r in (before or {}).get('runs',[]) if r.get('run_id')}
    rows=[]
    for p in sorted(base.glob('*/run.json')):
        d=_read_json(p)
        if not isinstance(d,dict): continue
        rid=d.get('run_id')
        if rid in before_ids: continue
        if event.get('contract_id') and d.get('contract_id')!=event.get('contract_id'): continue
        rows.append({'run_id':rid,'contract_id':d.get('contract_id'),'status':d.get('status'),'path':str(p)})
    return rows


def classify(run_dir,event):
    eid=event['event_id']
    before_path=run_dir/'checkpoints'/eid/'before.json'
    after_path=run_dir/'checkpoints'/eid/'after.json'
    receipt_path=run_dir/event.get('receipt_path',f'candidate-results/{eid}.json')
    before=_read_json(before_path) if before_path.exists() else None
    after=_read_json(after_path) if after_path.exists() else None
    receipt=_read_json(receipt_path) if receipt_path.exists() else None
    receipt_status=receipt.get('status') if isinstance(receipt,dict) else None
    if after is not None and receipt is not None and receipt_status in TERMINAL_RECEIPT_STATUSES:
        state='terminal'
    elif before is not None or after is not None or receipt is not None:
        state='in_progress'
    else:
        state='pending'
    return {
        'event_id':eid,'kind':event.get('kind'),'business_id':event.get('business_id'),'contract_id':event.get('contract_id'),
        'state':state,'before_checkpoint':before is not None,'receipt':receipt is not None,'receipt_status':receipt_status,
        'after_checkpoint':after is not None,'receipt_path':str(receipt_path),
        'candidate_event_runs':_current_event_runs(run_dir,event,before)
    }


def _resume_text(run_dir,queue,rows):
    remaining=[(i,r) for i,r in enumerate(rows) if r['state']!='terminal']
    if not remaining:
        return f'''# AURA Qualification Resume Instructions\n\nThe queue for `{run_dir}` is already exhausted. Do not rerun completed events. Run the evaluator instead.\n'''
    idx,row=remaining[0]; event=queue['events'][idx]
    lines=[
        '# AURA Qualification Resume Instructions','',
        f'Qualification run: `{run_dir}`',
        f'Original candidate instructions: `{run_dir/"candidate/RUN-INSTRUCTIONS.md"}`','',
        f'Completed/terminal events before resume point: **{idx} of {len(rows)}**.',
        f'Resume at queue event **{idx+1}/{len(rows)}**: `{row["event_id"]}`.',
        f'Business: `{row["business_id"]}`.',
    ]
    if row.get('contract_id'): lines.append(f'Contract: `{row["contract_id"]}`.')
    lines += ['', 'Read and continue to follow the original `RUN-INSTRUCTIONS.md`. Do not restart the qualification and do not redo terminal events. Preserve the existing workspace, evidence, receipts, checkpoints, and AURA Runs.']
    if row['state']=='pending':
        lines += ['', 'This event has not started. Begin it normally with its required `before` checkpoint, then execute it, write the receipt, take the `after` checkpoint, and continue through the remaining queue.']
    else:
        lines += ['', 'This event was interrupted after it started. Recover from the smallest incomplete point rather than starting it over.']
        if row['before_checkpoint']:
            lines.append('- Its `before` checkpoint already exists; preserve it as the event baseline and do not replace it merely because the agent session changed.')
        if row['candidate_event_runs']:
            runs=', '.join(f"{r['run_id']} ({r.get('status')})" for r in row['candidate_event_runs'])
            lines.append(f'- Candidate Run(s) created since the event baseline: {runs}. Inspect and resume compatible active/incomplete Run state instead of creating a duplicate root Run.')
        if row['receipt'] and not row['after_checkpoint']:
            lines.append('- A receipt exists but the `after` checkpoint does not. Verify the receipt is truthful and the AURA work is genuinely complete; if so, take the required `after` checkpoint and continue. If not, repair/resume the incomplete work first.')
        elif not row['receipt']:
            lines.append('- No terminal receipt exists yet; finish or truthfully block the event, then write its receipt and take the `after` checkpoint.')
    lines += ['', 'After this event becomes terminal, immediately continue with the next queue event. A provider/session interruption is an execution-environment interruption, not by itself an AURA pass or failure.','']
    return '\n'.join(lines)


def main():
    ap=argparse.ArgumentParser(description='Inspect an interrupted AURA qualification run and generate safe resume instructions.')
    ap.add_argument('run_dir'); ap.add_argument('--write-instructions',action='store_true'); ap.add_argument('--json',action='store_true')
    a=ap.parse_args(); run_dir=Path(a.run_dir).expanduser().resolve()
    queue_path=run_dir/'candidate/queue.json'
    if not queue_path.exists(): raise SystemExit(f'Qualification queue not found: {queue_path}')
    queue=_read_json(queue_path)
    if not isinstance(queue,dict) or not isinstance(queue.get('events'),list): raise SystemExit(f'Invalid qualification queue: {queue_path}')
    rows=[classify(run_dir,e) for e in queue['events']]
    terminal=sum(r['state']=='terminal' for r in rows); in_progress=sum(r['state']=='in_progress' for r in rows); pending=sum(r['state']=='pending' for r in rows)
    first=next((r for r in rows if r['state']!='terminal'),None)
    summary={'run_dir':str(run_dir),'event_count':len(rows),'terminal':terminal,'in_progress':in_progress,'pending':pending,'first_unfinished':first}
    text=_resume_text(run_dir,queue,rows)
    if a.write_instructions:
        out=run_dir/'candidate/RESUME-INSTRUCTIONS.md'; out.write_text(text,encoding='utf-8'); summary['resume_instructions']=str(out)
    if a.json: print(json.dumps({'summary':summary,'events':rows},indent=2))
    else:
        print(json.dumps(summary,indent=2))
        if a.write_instructions: print(f"Wrote {summary['resume_instructions']}")
        elif first: print('\n'+text)

if __name__=='__main__': main()
