"""Small observed work references. Not business truth, transcripts, or an agent bus."""
from pathlib import Path
import argparse
import hashlib
import json
import time

from _common import workspace_root,workspace_scope,resolve_business,write_json_atomic
from workspace_history import store
from workspace_startup import state_dir


def record(bid,job,chat):
    if job.get('keep_warm') or job.get('welcome'):return
    from workspace_sharing import destination_lock
    target=store(bid).parent/'activity'/f'{bid}.json';target.parent.mkdir(parents=True,exist_ok=True)
    row={k:job[k] for k in ('id','chat_id','agent','status','progress','created','updated','native_id') if k in job}
    row.update(title=chat.get('title','Work'),app=chat.get('agent',''),assistant=chat.get('assistant_name',''),
               source='AURA native connection',observed_at=time.time())
    if chat.get('summary'):row['summary']=str(chat['summary'])[:600]
    if job.get('requests'):row['needs_input']=any(r['status']=='pending' for r in job['requests'])
    with destination_lock(target):
        try:rows=json.loads(target.read_text(encoding='utf-8'))
        except FileNotFoundError:rows=[]
        rows=[r for r in rows if r.get('chat_id')!=row.get('chat_id')]+[row]
        # Active work is not pushed out by completed work.
        active=[r for r in rows if r['status']=='working'];done=[r for r in rows if r['status']!='working'][-100:]
        write_json_atomic(target,active[-100:]+done)


def _rows(bid):
    target=store(bid).parent/'activity'/f'{bid}.json'
    try:return json.loads(target.read_text(encoding='utf-8'))
    except FileNotFoundError:return []


def inventory(bid,query='',exclude_chat='',limit=20,live_jobs=()):
    live={job['id']:job for job in live_jobs if job.get('business_id')==bid and job.get('workspace')==str(workspace_root().resolve()) and job.get('status')=='working'}
    rows=[]
    for row in _rows(bid):
        active=live.get(row['id'],{})
        pending=any(r.get('status')=='pending' for r in active.get('requests',[]))
        values={**row,'last_needs_input':bool(row.get('needs_input')),'needs_input':pending}
        if row.get('needs_input') and not pending:
            values['progress']=active.get('progress') or 'Previously needed input. Check the native chat for its outcome.'
        rows.append(values)
    query=str(query).casefold();limit=max(1,min(100,int(limit)))
    rows=[r for r in rows if r.get('chat_id')!=exclude_chat and (not query or query in ' '.join(str(r.get(k,'')) for k in ('title','summary','assistant','agent','status','progress')).casefold())]
    rows.sort(key=lambda r:r.get('observed_at',0),reverse=True)
    return {'items':rows[:limit],'total':len(rows),'workspace':str(workspace_root().resolve()),'business_id':bid,
            'source':'Observed AURA-launched work; native-only activity may not appear. Status is last observed, not a live lock.',
            'checked_at':time.time()}


def result(bid,chat_id,limit=6000):
    """Explicit retrieval of one saved public reply, not an automatic context feed."""
    if not isinstance(chat_id,str) or not chat_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in chat_id):
        raise ValueError('Choose a valid chat reference.')
    row=next((r for r in _rows(bid) if r.get('chat_id')==chat_id),None)
    if not row:raise ValueError('No observed work matches this chat in this workspace and business.')
    folder=hashlib.sha256(str(workspace_root().resolve()).encode()).hexdigest()[:20]
    path=state_dir()/'chat-views'/folder/(chat_id+'.json')
    try:messages=json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError:raise ValueError('This result is not available in the saved display. Open the chat in AURA or its native app.') from None
    message=next((m for m in reversed(messages) if m.get('role')=='assistant' and m.get('request_id')==row['id']),None)
    if not message:raise ValueError('This request has not saved a public result yet. Check its last-observed status.')
    limit=max(100,min(12000,int(limit)));text=str(message.get('text',''))
    return {'chat_id':chat_id,'status':row['status'],'source':'Saved public reply from '+row['agent'],'observed_at':row['observed_at'],
            'text':text[:limit],'truncated':len(text)>limit,'canonical_business_truth':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace',type=Path,default=workspace_root());parser.add_argument('--business-id');parser.add_argument('--search',default='');parser.add_argument('--exclude-chat',default='');parser.add_argument('--limit',type=int,default=20);parser.add_argument('--result',metavar='CHAT_ID');parser.add_argument('--max-chars',type=int,default=6000);parser.add_argument('--json',action='store_true')
    args=parser.parse_args()
    with workspace_scope(args.workspace):
        resolved=resolve_business(args.business_id)
        if resolved['status']!='resolved':raise ValueError('Choose a business for activity.')
        output=result(resolved['business_id'],args.result,args.max_chars) if args.result else inventory(resolved['business_id'],args.search,args.exclude_chat,args.limit)
    print(json.dumps(output,ensure_ascii=False))


if __name__=='__main__':main()
