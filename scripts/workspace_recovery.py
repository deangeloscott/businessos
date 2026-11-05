"""Small local work receipts and recovery decisions. Never replay or schedule work."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import os
import subprocess
import time

from _common import workspace_root,workspace_scope

CONTINUE=('Continue the previous assignment. Check the latest conversation and saved work, then resume only '
          'what remains. Confirm uncertain action outcomes before repeating them. If the assignment is already '
          'finished, report that.')


def process_mark(pid):
    """Identify one process incarnation without an extra runtime dependency."""
    if not isinstance(pid,int) or isinstance(pid,bool) or pid<=0:return None
    try:
        if os.name=='nt':
            import ctypes
            from ctypes import wintypes
            kernel=ctypes.WinDLL('kernel32',use_last_error=True)
            kernel.OpenProcess.restype=wintypes.HANDLE
            kernel.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD]
            kernel.CloseHandle.argtypes=[wintypes.HANDLE]
            kernel.GetProcessTimes.argtypes=[wintypes.HANDLE,*([ctypes.POINTER(wintypes.FILETIME)]*4)]
            kernel.GetExitCodeProcess.argtypes=[wintypes.HANDLE,ctypes.POINTER(wintypes.DWORD)]
            handle=kernel.OpenProcess(0x1000,False,pid)
            if not handle:return False if ctypes.get_last_error()==87 else None
            try:
                code=wintypes.DWORD()
                if not kernel.GetExitCodeProcess(handle,ctypes.byref(code)):return None
                if code.value!=259:return False
                times=[wintypes.FILETIME() for _ in range(4)]
                if not kernel.GetProcessTimes(handle,*[ctypes.byref(v) for v in times]):return None
                if times[1].dwHighDateTime or times[1].dwLowDateTime:return False
                return str((times[0].dwHighDateTime<<32)|times[0].dwLowDateTime)
            finally:kernel.CloseHandle(handle)
        stat=Path('/proc')/str(pid)/'stat'
        if Path('/proc').is_dir():
            raw=stat.read_text(encoding='utf-8');fields=raw[raw.rfind(')')+2:].split()
            if fields[0]=='Z':return False
            return Path('/proc/sys/kernel/random/boot_id').read_text(encoding='utf-8').strip()+':'+fields[19]
        result=subprocess.run(['ps','-p',str(pid),'-o','lstart='],capture_output=True,text=True,timeout=2)
        return result.stdout.strip() or (False if result.returncode==1 else None)
    except (FileNotFoundError,ProcessLookupError):return False
    except (OSError,ValueError,IndexError,subprocess.SubprocessError):return None


def process_state(record):
    mark=record.get('process') or {}
    if not mark.get('pid') or not mark.get('born'):return 'unknown'
    current=process_mark(mark['pid'])
    if current is None:return 'unknown'
    return 'running' if current and current==mark['born'] else 'ended'


def begin(chat,job):
    chat['recovery']={'request_id':job['id'],'started':job['created'],'status':'working'}


def attach(chat,job,process):
    if chat.get('recovery',{}).get('request_id')!=job['id']:return
    born=process_mark(process.pid)
    if isinstance(born,str):chat['recovery']['process']={'pid':process.pid,'born':born}


def finish(chat,job):
    if chat.get('recovery',{}).get('request_id')==job['id']:
        chat['recovery'].update(status=job['status'],ended=job['updated'])


def revision(chat):
    fields={k:chat.get(k) for k in ('id','workspace','business_id','native_id','status','updated','source_marker','recovery','goal_id','permission_mode')}
    return hashlib.sha256(json.dumps(fields,sort_keys=True).encode()).hexdigest()


def needed(chat):return bool(chat and (chat.get('status') in {'working','error'} or chat.get('recovery',{}).get('status')=='working'))


def saved_observation(messages):
    for row in reversed(messages):
        if row.get('role')=='assistant' and row.get('status')=='complete':return {'request_id':row.get('request_id'),'state':'complete'}
        if row.get('role')=='user':break
    return None


def native_observation(messages,kind):
    """Only an explicit native final reply for an identified Aura request is proof."""
    from workspace_context import message_ref
    from workspace_agents import message_text
    current='';state='unknown'
    for row in messages:
        role=row.get('role');content=row.get('content','')
        if role=='user':
            # Claude carries tool results in user envelopes, not new assignments.
            tool_result=isinstance(content,list) and content and all(isinstance(p,dict) and p.get('type')=='tool_result' for p in content)
            if not tool_result:current=message_ref(message_text(content));state='unfinished'
        elif role=='assistant' and current:
            reason=row.get('stopReason') or row.get('stop_reason') or row.get('finish_reason')
            tools=row.get('tool_calls') or isinstance(content,list) and any(isinstance(p,dict) and p.get('type') in {'tool_use','toolCall'} for p in content)
            state='complete' if reason in {'stop','end_turn','endTurn'} and not tools else 'unfinished'
        elif role in {'tool','toolResult'} and current:state='unfinished'
    return {'request_id':current,'state':state}


def describe(chat,job=None,observation=None):
    record=chat.get('recovery') or {};state='saved';message='';allow=False
    live=job and job.get('status')=='working'
    process=process_state(record) if not live and needed(chat) else 'unknown'
    if live:state='running'
    elif chat.get('status')=='stopped':state='stopped'
    elif needed(chat):
        if process=='running':
            state='running_elsewhere';message='This request is still running. Check for its latest reply before continuing.'
        elif observation and observation.get('request_id')==record.get('request_id') and record.get('request_id') and observation.get('state')=='complete':
            state='complete';message='The saved reply is ready.'
        elif record.get('status')=='complete':state='complete'
        elif chat.get('agent')!='configured' and not chat.get('native_id'):
            state='uncertain';message='The connection ended before its chat could be saved. Review recent work before trying again.';allow=True
        elif process=='ended' and chat.get('agent')!='hermes' and not record.get('background_work') and not any(c.get('status') in {'pending','working','unconfirmed'} for c in chat.get('subagents',[])):
            state='interrupted';message='This chat was interrupted. Review the latest messages, then continue when you’re ready.';allow=True
        else:
            state='uncertain';message='The last request’s outcome is unconfirmed. Check recent work before continuing.';allow=True
    return {'state':state,'message':message,'can_continue':allow,'revision':revision(chat),
            'native_resume':False,'checked_at':time.time()}


def check(app,bid,ident,refresh=True):
    from workspace_native_chats import marker
    with app.recovery_lock:
        with app.lock:
            chat=next((c for c in app.preferences['chats'] if c['id']==ident and c['business_id']==bid and c.get('workspace',app.workspace_path)==app.workspace_path),None)
            if not chat:raise ValueError('Choose a chat in this business and workspace.')
            key=('chat-recovery',bid,ident,revision(chat),process_state(chat.get('recovery') or {}),json.dumps(marker(chat.get('source_file'))))
            old=[k for k,v in app.read_cache.items() if isinstance(k,tuple) and k[0]=='chat-recovery']
            for k in old:
                if time.monotonic()-app.read_cache[k][0]>10:app.read_cache.pop(k,None)
            retained=[k for k in old if k in app.read_cache]
            for k in retained[:-63]:app.read_cache.pop(k,None)
        return copy.deepcopy(app.cached_read(key,lambda:_check(app,bid,ident,refresh),seconds=3))


def _check(app,bid,ident,refresh):
    with app.lock:
        root=app.workspace_path
        chat=next((c for c in app.preferences['chats'] if c['id']==ident and c['business_id']==bid and c.get('workspace',root)==root),None)
        if not chat:raise ValueError('Choose a chat in this business and workspace.')
        initial=describe(chat,app.chat_job(bid,ident))
    # Native reads remain outside the shared UI lock. Live local work already has
    # its own stream; don't open a second connection to it.
    result=app.conversation(bid,ident)
    saved=saved_observation(result['messages'])
    if refresh and chat.get('native_id') and needed(chat) and initial['state'] not in {'running','running_elsewhere'} and not (saved and saved.get('request_id')==chat.get('recovery',{}).get('request_id')):
        result=app.conversation(bid,ident,refresh=True)
    with app.lock:
        if app.workspace_path!=root:raise ValueError('The workspace changed. Open this chat again.')
        current=next((c for c in app.preferences['chats'] if c['id']==ident and c['business_id']==bid),None)
        if not current:raise ValueError('This chat is no longer available.')
        job=app.chat_job(bid,ident)
        state=describe(current,job,result.get('native_observation') or saved_observation(result['messages']))
        if state['state']=='complete' and needed(current) and not (job and job['status']=='working'):
            current.update(status='complete',work_state='complete');current.pop('continuation',None)
            current['recovery']['status']='complete';app.save_preferences()
            result['chat']=dict(current);state=describe(current,job);state.update(state='complete',message='The saved reply is ready.')
        result['recovery']=state;result['workspace']=root
        return result


def prepare(app,bid,ident,expected=None,reviewed=False):
    result=check(app,bid,ident)
    with app.lock:
        state=result['recovery'];chat=next(c for c in app.preferences['chats'] if c['id']==ident and c['business_id']==bid)
        if any(j.get('chat_id')==ident for j in app.running_jobs(workspace_root())):
            raise ValueError('This chat is still working. Open it to see its progress.')
        if revision(chat)!=state['revision']:raise ValueError('This chat changed. Check its latest state before continuing.')
        if expected is not None and expected!=state['revision']:raise ValueError('This chat changed. Check its latest state before continuing.')
        if not state['can_continue']:raise ValueError('Check this chat’s latest reply before continuing.')
        if state['state']=='uncertain' and reviewed is not True:raise ValueError('Review the recent work before continuing this chat.')
        if process_state(chat.get('recovery') or {})=='running':raise ValueError('This request is still running. Check its progress before continuing.')
        result['draft']=CONTINUE
        if chat.get('agent')!='configured' and not chat.get('native_id'):
            # An interrupted first connection has no native history to continue.
            # Prepare a reviewable assignment with its original source references.
            import workspace_context
            index=next((i for i in range(len(result['messages'])-1,-1,-1) if result['messages'][i].get('role')=='user'),None)
            if index is not None:
                source=workspace_context.reusable(app,bid,ident,index,workspace_context.message_key(result['messages'][index]))
                result['draft']='Check existing work first and avoid repeating completed actions.\n\nOriginal assignment:\n'+source['text']
                result['context']={'files':source['files'],'references':source['references']}
        previous=copy.deepcopy(chat)
        chat.update(status='stopped',work_state='stopped');chat.pop('continuation',None)
        if chat.get('recovery'):chat['recovery']['status']='reviewed'
        try:app.save_preferences()
        except OSError:
            chat.clear();chat.update(previous);raise
        result['chat']=dict(chat)
        result['recovery']=describe(chat)
        return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['check','prepare'])
    parser.add_argument('--workspace',type=Path,default=workspace_root());parser.add_argument('--business-id',required=True);parser.add_argument('--chat',required=True)
    parser.add_argument('--url',default='http://127.0.0.1:4187');parser.add_argument('--revision');parser.add_argument('--reviewed',action='store_true');parser.add_argument('--json',action='store_true')
    args=parser.parse_args()
    from workspace_goals import live_change
    with workspace_scope(args.workspace):
        result=live_change(args.url,args.business_id,{'action':args.action,'id':args.chat,'revision':args.revision,'reviewed':args.reviewed},route='/api/chats/recovery')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
