"""Display-only native activity. Never used as instructions or business memory."""
import argparse
import json
import re
import threading
import time
from pathlib import Path

from _common import workspace_root, workspace_scope, write_json_atomic
from workspace_startup import state_dir


def tool_title(name,value):
    """Readable label for a named tool call: what it ran, read or delegated."""
    value=value if isinstance(value,dict) else {}
    if value.get('command'):return command_title(value['command'])
    if name in {'Task','Agent'} and value.get('description'):return 'Sub-agent: '+str(value['description'])[:70]
    if value.get('url'):return f"{name}: {str(value['url'])[:80]}"
    if value.get('pattern'):return f"{name}: {str(value['pattern'])[:80]}"
    target=value.get('file_path') or value.get('path')
    return f'{name}: {Path(str(target)).name or target}' if target else name


def command_title(command):
    """A short readable label for a shell step: the command itself, without shell wrappers."""
    text=' '.join(command) if isinstance(command,list) else str(command or '')
    text=re.sub(r'^\S*(?:powershell|pwsh|bash|sh|cmd)(?:\.exe)?"?\s+(?:-NoProfile\s+)?(?:-Command|-lc|-c|/c)\s+','',text.strip(),flags=re.I).strip().strip('"\'')
    text=' '.join(text.split())
    return ('Command: '+text[:70]+('…' if len(text)>70 else '')) if text else 'Terminal command'


def path(request_id):
    if not isinstance(request_id,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}',request_id):
        raise ValueError('Choose a valid request.')
    import hashlib
    key=hashlib.sha256(str(workspace_root().resolve()).encode()).hexdigest()[:20]
    return state_dir()/'chat-activity'/key/(request_id+'.json')


def text(value):
    if isinstance(value,str):return value
    if isinstance(value,list):return '\n'.join(filter(None,(text(v) for v in value)))
    if isinstance(value,dict):
        # Allow only content intended for display, never raw protocol/configuration.
        if value.get('type') in {'image','audio','encrypted','redacted_thinking'}:return ''
        return str(value.get('text') or value.get('thinking') or value.get('content') and text(value['content']) or '')
    return ''


def plan_text(value):
    if isinstance(value,list):return '\n'.join(filter(None,(plan_text(v) for v in value)))
    if isinstance(value,dict):
        label=value.get('content') or value.get('step') or value.get('title') or value.get('text') or value.get('name') or ''
        status=str(value.get('status') or '').replace('_',' ')
        children=value.get('phases') or value.get('todos') or value.get('items') or value.get('tasks') or []
        return (status+': ' if status else '')+str(label)+('\n'+plan_text(children) if children else '')
    return str(value or '')


class Recorder:
    """Coalesce streaming deltas; bound local display without limiting native work."""
    def __init__(self,request_id,business_id,redact=lambda s:s):
        self.request_id=request_id;self.business_id=business_id;self.redact=redact
        self.rows=[];self.revision=0;self.truncated=False;self.lock=threading.RLock()
        self.target=path(request_id);self.bytes=0
        self.phases={}

    def put(self,kind,title,body='',*,owner='',ident='',status='',delta=False,inputs=''):
        with self.lock:
            body=self.redact(str(body));title=None if title is None else self.redact(str(title))[:240]
            key=(kind,str(owner),str(ident))
            row=next((r for r in reversed(self.rows) if (r['kind'],r['owner'],r['native_id'])==key),None) if ident else None
            if row is None:
                row={'id':str(self.revision+1),'kind':kind,'owner':str(owner),'native_id':str(ident),'title':title or 'Tool result','text':'','at':time.time()}
                self.rows.append(row)
            old=len(row['text'])+len(row.get('input',''));raw=self.redact((row['text']+body) if delta else (body or row['text']))
            if len(raw)>24000:row['truncated']=True
            row.update(title=title or row['title'],text=raw[:24000],status=str(status or row.get('status','')),updated=time.time())
            if inputs:row['input']=self.redact(str(inputs))[:24000]
            self.bytes+=len(row['text'])+len(row.get('input',''))-old
            while len(self.rows)>500 or self.bytes>1000000:
                removed=self.rows.pop(0);self.bytes-=len(removed['text'])+len(removed.get('input',''));self.truncated=True
            self.revision+=1

    def snapshot(self):
        with self.lock:
            return {'request_id':self.request_id,'business_id':self.business_id,'revision':self.revision,
                    'items':[dict(r) for r in self.rows],'truncated':self.truncated,
                    'source':'Native app activity. Only details exposed by this connection are available.'}

    def save(self):
        data=self.snapshot();self.target.parent.mkdir(parents=True,exist_ok=True);write_json_atomic(self.target,data)
        # Native originals retain the full history. This is a bounded display cache.
        total=0
        def modified(p):
            try:return p.stat().st_mtime
            except FileNotFoundError:return 0
        files=sorted(self.target.parent.glob('*.json'),key=modified,reverse=True)
        for i,p in enumerate(files):
            try:
                total+=p.stat().st_size
                if i>=200 or total>64*1024*1024:p.unlink(missing_ok=True)
            except FileNotFoundError:continue

    def observe(self,kind,event,parent=''):
        try:self._observe(kind,event,parent)
        except (ValueError,TypeError,KeyError,AttributeError):
            # Optional display must never interrupt the native app.
            return

    def _observe(self,kind,e,parent):
        p=e.get('params') or {};typ=e.get('type','');owner=''
        if kind=='codex':
            method=e.get('method','');thread=p.get('threadId','')
            owner=thread if thread and thread!=parent else ''
            item=p.get('item') or {};it=item.get('type','');ident=item.get('id') or p.get('itemId','')
            if it=='agentMessage' and ident:
                self.phases[ident]=item.get('phase')
                if len(self.phases)>500:self.phases.pop(next(iter(self.phases)))
            if method=='turn/plan/updated':
                plan=p.get('plan') or [];self.put('plan','Plan','\n'.join(f"{r.get('status','pending')}: {r.get('step','')}" for r in plan),owner=owner,ident='plan');return
            if method in {'item/reasoning/summaryTextDelta','item/reasoning/textDelta'}:
                # Only public summaries; raw reasoning/textDelta is deliberately omitted.
                if method.endswith('summaryTextDelta'):self.put('thinking','Thinking summary',p.get('delta',''),owner=owner,ident=str(ident)+':'+str(p.get('summaryIndex',0)),delta=True)
                return
            if method=='item/agentMessage/delta' and (p.get('phase',self.phases.get(ident))=='commentary' or owner):
                self.put('commentary','Agent progress' if owner else 'Progress',p.get('delta',''),owner=owner,ident=ident,delta=True);return
            if method not in {'item/started','item/completed'}:return
            if it=='agentMessage' and item.get('phase')=='commentary':self.put('commentary','Progress',item.get('text',''),owner=owner,ident=ident)
            elif it in {'commandExecution','fileChange','webSearch','mcpToolCall','dynamicToolCall'}:
                title=item.get('tool') or (command_title(item.get('command')) if it=='commandExecution' else None) or {'fileChange':'File changes','webSearch':'Web search'}.get(it,'Tool')
                if it=='commandExecution' and item.get('exitCode') not in (None,0):title+=f" · exit {item['exitCode']}"
                body=item.get('aggregatedOutput') or text(item.get('result')) or json.dumps(item.get('changes') or item.get('action') or item.get('arguments') or {},ensure_ascii=False)
                self.put('file' if it=='fileChange' else 'tool',title,body,owner=owner,ident=ident,status=item.get('status') or ('completed' if method.endswith('completed') else 'in_progress'),inputs=str(item['command']) if item.get('command') else json.dumps(item.get('arguments'),ensure_ascii=False) if item.get('arguments') else '')
            elif it=='subAgentActivity':self.put('delegation','Agent '+str(item.get('kind','activity')),item.get('message') or item.get('summary',''),owner=item.get('agentThreadId',''),ident=ident,status=item.get('kind',''))
            return
        if kind=='antigravity':
            u=p.get('update') or {};typ=u.get('sessionUpdate','');ident=u.get('toolCallId','')
            if typ=='plan':self.put('plan','Plan','\n'.join(f"{r.get('status','pending')}: {r.get('content','')}" for r in u.get('entries',[])),ident='plan')
            elif typ=='agent_thought_chunk':self.put('thinking','Thinking',text(u.get('content')),ident='thinking',delta=True)
            elif typ in {'tool_call','tool_call_update'}:
                self.put('tool',u.get('title') or 'Tool',text(u.get('content')) or json.dumps(u.get('rawOutput') or u.get('rawInput') or {},ensure_ascii=False),ident=ident,status=u.get('status',''))
            return
        if kind=='hermes':
            typ=p.get('type',typ);v=p.get('payload') or e.get('payload') or {}
            owner=str(v.get('subagent_id') or v.get('agent_id') or '') if typ.startswith('subagent.') else ''
            ident=str(v.get('tool_call_id') or v.get('call_id') or v.get('id') or '')
            ident=ident or str(v.get('tool_id') or '')
            if typ in {'reasoning.delta','thinking.delta','reasoning.available','subagent.thinking'}:self.put('thinking','Thinking',v.get('text') or v.get('delta',''),owner=owner,ident='thinking',delta=typ!='reasoning.available')
            elif typ in {'tool.start','tool.complete','subagent.tool'}:
                self.put('tool',v.get('name') or v.get('tool_name') or 'Tool',v.get('result_text') or text(v.get('result')) or v.get('summary') or v.get('tool_preview') or '',owner=owner,ident=ident,status=typ.rsplit('.',1)[-1],inputs=json.dumps(v['args'],ensure_ascii=False) if v.get('args') else '')
                if isinstance(v.get('todos'),list):self.put('plan','Plan',plan_text(v['todos']),owner=owner,ident='plan')
            elif typ=='subagent.text':self.put('commentary','Agent progress',v.get('text',''),owner=owner,ident='message',delta=True)
            elif typ=='status.update':self.put('commentary','Progress',v.get('message') or v.get('text') or v.get('status',''))
            return
        if kind in {'pi','omp'}:
            if typ=='subagent_event':
                v=e.get('payload') or {};nested=v.get('event') or e.get('event')
                if isinstance(nested,dict):self._observe(kind,dict(nested,subagentId=v.get('id') or e.get('subagentId','')),parent)
                return
            child=e.get('subagentId') or e.get('subagent_id') or e.get('agentId') or ''
            owner=str(child);v=e.get('assistantMessageEvent') or {}
            if typ=='message_update' and v.get('type') in {'thinking_delta','thinking_end'}:
                self.put('thinking','Thinking',v.get('delta') or v.get('content',''),owner=owner,ident=str(e.get('message',{}).get('timestamp',''))+':'+str(v.get('contentIndex',0)),delta=v.get('type')=='thinking_delta')
            elif typ in {'tool_execution_start','tool_execution_update','tool_execution_end'}:
                result=e.get('result') or e.get('partialResult') or {}
                self.put('tool',e.get('toolName') or 'Tool',text(result),owner=owner,ident=e.get('toolCallId',''),status='error' if e.get('isError') else ('completed' if typ.endswith('end') else 'in_progress'),inputs=json.dumps(e['args'],ensure_ascii=False) if e.get('args') else '')
                if 'todo' in str(e.get('toolName','')).lower():
                    plan=result.get('details') if isinstance(result,dict) else None
                    if plan:self.put('plan','Plan',plan_text(plan),owner=owner,ident='plan')
                # Pi extensions often expose child transcripts in a task result rather
                # than a separate stream. Show only the messages the extension supplied.
                details=result.get('details') or {} if isinstance(result,dict) else {}
                children=details.get('results') or [] if isinstance(details,dict) else []
                for i,child in enumerate(children):
                    if not isinstance(child,dict):continue
                    child_id=str(e.get('toolCallId',''))+':'+str(i)
                    for j,m in enumerate(child.get('messages') or []):
                        if not isinstance(m,dict):continue
                        if m.get('role')=='toolResult':self.put('tool',m.get('toolName') or 'Tool result',text(m.get('content')),owner=child_id,ident=m.get('toolCallId') or str(j),status='error' if m.get('isError') else 'completed')
                        elif m.get('role')=='assistant':
                            for k,block in enumerate(m.get('content') or []):
                                if not isinstance(block,dict):continue
                                ident=f'{j}:{k}'
                                if block.get('type')=='thinking':self.put('thinking','Thinking',block.get('thinking',''),owner=child_id,ident=ident)
                                elif block.get('type')=='text':self.put('commentary','Agent reply',block.get('text',''),owner=child_id,ident=ident)
                                elif block.get('type')=='toolCall':self.put('tool',block.get('name') or 'Tool',owner=child_id,ident=block.get('id') or ident,inputs=json.dumps(block.get('arguments') or {},ensure_ascii=False))
            elif typ=='message_end' and owner:
                self.put('commentary','Agent reply',text((e.get('message') or {}).get('content')),owner=owner,ident=str(e.get('messageId') or (e.get('message') or {}).get('timestamp','reply')))
            elif typ=='todo_reminder':self.put('plan','Plan',plan_text(e.get('todos') or []),owner=owner,ident='plan')
            elif typ in {'subagent_event','subagent_progress'} and isinstance(e.get('event'),dict):
                nested=dict(e['event'],subagentId=child or e.get('id',''));self._observe(kind,nested,parent)
            return
        if kind=='claude':
            owner=e.get('parent_tool_use_id') or ''
            if typ=='assistant':
                for i,c in enumerate((e.get('message') or {}).get('content',[])):
                    ident=(e.get('message') or {}).get('id','')+':'+str(i)
                    if c.get('type')=='thinking':self.put('thinking','Thinking',c.get('thinking',''),owner=owner,ident=ident)
                    elif c.get('type')=='tool_use':self.put('tool',tool_title(c.get('name','Tool'),c.get('input')),'',owner=owner,ident=c.get('id',''),status='in_progress',inputs=json.dumps(c.get('input') or {},ensure_ascii=False))
            elif typ=='user':
                for c in (e.get('message') or {}).get('content',[]) if isinstance(e.get('message',{}).get('content'),list) else []:
                    if c.get('type')=='tool_result':self.put('tool',None,text(c.get('content')),owner=owner,ident=c.get('tool_use_id',''),status='error' if c.get('is_error') else 'completed')


def read(request_id):
    try:return json.loads(path(request_id).read_text(encoding='utf-8'))
    except FileNotFoundError:return {'request_id':request_id,'items':[],'revision':0,'expired':True}


def public(data,item='',after=''):
    """Small polling response; tool arguments and output load only when expanded."""
    if item:
        row=next((r for r in data['items'] if r['id']==item),None)
        if not row:raise ValueError('This detail is no longer in recent activity. Check the native app.')
        return row
    if str(data['revision'])==str(after):return {'revision':data['revision'],'unchanged':True}
    return {**data,'items':[{**{k:v for k,v in r.items() if k not in {'text','input'}},
                           'text':r['text'][:2000] if r['kind'] in {'plan','commentary'} else '',
                           'has_detail':bool(r['text'] or r.get('input'))} for r in data['items']]}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workspace',type=Path,default=workspace_root());p.add_argument('--request',required=True)
    a=p.parse_args()
    with workspace_scope(a.workspace):print(json.dumps(read(a.request),ensure_ascii=False))


if __name__=='__main__':main()
