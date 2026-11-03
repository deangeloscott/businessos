"""Thin bidirectional transports for the native apps' documented request protocols."""
import json
import queue
import subprocess
import threading
import time

from workspace_interactions import answers_for,question


def channel(process,execution,errors):
    events=queue.Queue(maxsize=256);lock=threading.Lock();started=time.monotonic();closed=threading.Event()
    def enqueue(event):
        while not closed.is_set():
            try:events.put(event,timeout=.25);return
            except queue.Full:pass
    def read():
        try:
            for line in process.stdout:
                try:event=json.loads(line)
                except ValueError:continue
                if isinstance(event,dict):enqueue(event)
                if closed.is_set():return
        finally:enqueue(None)
    threading.Thread(target=read,daemon=True).start()
    def send(value):
        with lock:
            execution.check()
            errors.send(process,json.dumps(value,ensure_ascii=False)+'\n')
    def read_events():
        while True:
            execution.check();execution.requests.expire()
            if not getattr(execution,'protocol_ready',False) and time.monotonic()-started>45:
                raise ValueError('The native app did not initialize. No AI request was resubmitted.')
            try:event=events.get(timeout=.25)
            except queue.Empty:continue
            if event is None:return
            yield event
    return send,read_events(),closed.set


def add_request(execution,ident,title,questions,send,convert,detail='',timeout=None):
    def validate(answers):return convert(answers_for(questions,answers))
    execution.requests.add(ident,title,questions,send,validate,detail,timeout)


def codex_request(event,execution,send):
    ident=event['id'];method=event.get('method','');params=event.get('params') or {}
    reply=lambda payload:send({'id':ident,'result':payload})
    if method in {'item/commandExecution/requestApproval','item/fileChange/requestApproval'}:
        available=params.get('availableDecisions')
        allowed=[v for v in (available if available is not None else ['accept','decline','cancel']) if isinstance(v,str) and v in {'accept','decline','cancel'}]
        if not allowed:
            send({'id':ident,'error':{'code':-32601,'message':'Use the native app for this approval decision.'}});return
        labels={'accept':'Approve once','decline':'Decline','cancel':'Cancel request'}
        q=question('decision',params.get('reason') or 'Allow this native operation?', [labels[v] for v in allowed])
        detail=json.dumps({k:params[k] for k in ('command','cwd','grantRoot','networkApprovalContext','additionalPermissions') if k in params},ensure_ascii=False,indent=2)
        add_request(execution,ident,'Approval needed',[q],reply,lambda a:{'decision':next(v for v in allowed if labels[v]==a['decision'][0])},detail)
    elif method=='item/tool/requestUserInput':
        questions=[]
        for value in params.get('questions',[]):
            q=question(value['id'],value.get('question',''),[o['label'] for o in value.get('options') or []],free=value.get('isOther',False))
            q['secret']=value.get('isSecret',False)
            for option,original in zip(q['options'],value.get('options') or []):option['description']=original.get('description','')
            questions.append(q)
        add_request(execution,ident,'Your AI has a question',questions,reply,lambda a:{'answers':{k:{'answers':v} for k,v in a.items()}},timeout=params.get('autoResolutionMs'))
    elif method=='item/permissions/requestApproval':
        q=question('decision',params.get('reason') or 'Grant the requested access for this turn?', ['Approve this turn','Decline'])
        permissions=params.get('permissions') or {}
        add_request(execution,ident,'Permission request',[q],reply,
            lambda a:{'permissions':permissions if a['decision']==['Approve this turn'] else {},'scope':'turn'},json.dumps(permissions,indent=2))
    else:
        # Auth, arbitrary MCP schemas, dynamic tools and future methods are not guessed.
        send({'id':ident,'error':{'code':-32601,'message':'This native interaction is not supported in Aura. Use the native app.'}})


def codex_run(command,cwd,prompt,native_id,model,effort,update,env,execution,child_model=''):
    from workspace_codex import base_command
    from workspace_delegation import Tracker
    from _process_errors import ErrorTail
    import workspace_usage
    mode=execution.permission
    params={'cwd':str(cwd),'model':model}
    if mode!='native':params.update(sandbox='danger-full-access' if mode=='full' else mode,approvalPolicy='never' if mode=='full' else 'on-request')
    if child_model:params['config']={'agents.default_subagent_model':child_model}
    if native_id:params.update(threadId=native_id)
    final='';usage={};thread=native_id;complete=False;items={};delegation=Tracker(update)
    previous_total=None;turn_tokens={};turn_started=False
    with execution.popen([*base_command(command),'app-server'],cwd=cwd,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                         text=True,encoding='utf-8',errors='replace') as process:
        errors=ErrorTail(process,env);send,events,close=channel(process,execution,errors)
        send({'id':'aura-init','method':'initialize','params':{'clientInfo':{'name':'aura_workspace','version':'1.0'},'capabilities':{'experimentalApi':True}}})
        try:
            for event in events:
                ident=event.get('id');method=event.get('method');p=event.get('params') or {}
                if method and ident is not None:
                    if thread and p.get('threadId') and p['threadId']!=thread:
                        send({'id':ident,'error':{'code':-32602,'message':'Different thread.'}});continue
                    codex_request(event,execution,send);continue
                if ident in {'aura-init','aura-thread','aura-turn'} and 'error' in event:
                    raise ValueError(str(event['error'].get('message','Native request failed.')))
                if ident=='aura-init':
                    send({'method':'initialized','params':{}})
                    send({'id':'aura-thread','method':'thread/resume' if native_id else 'thread/start','params':params})
                elif ident=='aura-thread':
                    thread=((event.get('result') or {}).get('thread') or {}).get('id')
                    if not thread:raise ValueError('Codex did not return a native thread ID. No AI request was sent.')
                    if native_id and thread!=native_id:raise ValueError('Codex returned a different native chat. No request was sent.')
                    effective={k:event['result'][k] for k in ('approvalPolicy','sandbox') if k in event['result']}
                    update(native_id=thread,permission_effective=effective)
                    turn={'threadId':thread,'input':[{'type':'text','text':prompt}],'model':model}
                    if effort:turn['effort']=effort
                    send({'id':'aura-turn','method':'turn/start','params':turn})
                    execution.protocol_ready=True
                elif ident=='aura-turn' or method=='turn/started':turn_started=True
                elif method=='serverRequest/resolved':execution.requests.resolve(p.get('requestId'))
                elif method=='thread/tokenUsage/updated' and p.get('threadId')==thread:
                    token=p.get('tokenUsage') or {};last=token.get('last') or {}
                    fields=[('inputTokens','input_tokens'),('outputTokens','output_tokens'),('cachedInputTokens','cached_input_tokens')]
                    total=token.get('total') or {}
                    raw={dest:last[src] for src,dest in fields if src in last}
                    if turn_started:
                        for src,dest in fields:
                            if total and isinstance(total.get(src),(float,int)):
                                delta=total[src]-previous_total[src] if previous_total and src in previous_total and total[src]>=previous_total[src] else last.get(src)
                                if isinstance(delta,(float,int)):turn_tokens[dest]=turn_tokens.get(dest,0)+delta
                            elif dest in raw:turn_tokens[dest]=raw[dest]
                        usage=workspace_usage.measure(turn_tokens,'codex',time.time())
                        usage['last']=workspace_usage.measure(raw,'codex',time.time());update(usage=usage)
                    if total:previous_total=total
                elif p.get('threadId') and p['threadId']!=thread:
                    delegation.observe('codex',{'type':method,**p});continue
                elif method in {'item/started','item/completed'}:
                    item=p.get('item') or {};typ=item.get('type')
                    if typ=='agentMessage':
                        items[item['id']]=item
                        if method=='item/completed' and item.get('phase')!='commentary':final=item.get('text','');update(reply=final)
                    else:
                        label={'commandExecution':'Running a command','fileChange':'Updating files','webSearch':'Searching the web','mcpToolCall':'Using a connected tool'}.get(typ)
                        if label:update(progress=label)
                        if typ=='collabAgentToolCall':
                            adapted={**item,'type':'collab_tool_call','sender_thread_id':item.get('senderThreadId'),
                                'receiver_thread_ids':item.get('receiverThreadIds',[]),
                                'agents_states':{key:{'status':{'pendingInit':'pending_init','notFound':'not_found'}.get(value.get('status'),value.get('status')),'message':value.get('message')}
                                                for key,value in item.get('agentsStates',{}).items()}}
                            delegation.observe('codex',{'type':method.replace('/','.'),'item':adapted})
                elif method=='item/agentMessage/delta':
                    item=items.setdefault(p.get('itemId'),{'text':''});item['text']=item.get('text','')+p.get('delta','')
                    if item.get('phase')!='commentary':update(reply=item['text'])
                elif method=='turn/completed':
                    turn=p.get('turn') or {}
                    if turn.get('status')!='completed':raise ValueError(str((turn.get('error') or {}).get('message') or 'The native turn did not complete.'))
                    complete=True;break
                elif method=='error' and not p.get('willRetry'):raise ValueError(str((p.get('error') or {}).get('message') or 'The native app reported an error.'))
            if not complete:raise ValueError(errors.message('Codex disconnected before completing. Open the native chat; this request was not resubmitted.'))
        finally:
            close();execution.requests.close();ErrorTail.close_input(process)
            try:process.wait(timeout=3)
            except subprocess.TimeoutExpired:process.terminate();process.wait(timeout=5)
    execution.check()
    if not final.strip():raise ValueError('Codex ended without a final reply. Open its native chat before retrying.')
    return {'reply':final,'native_id':thread,'usage':usage}


def agent_lines(process,kind,prompt,native_id,execution,errors):
    """Yield ordinary native events to the existing reply/usage/delegation parser."""
    send,events,close=channel(process,execution,errors);finished=False
    if kind=='claude':
        send({'type':'control_request','request_id':'aura-init','request':{'subtype':'initialize','hooks':None}})
    else:send({'id':'aura-state','type':'get_state'})
    try:
        for event in events:
            typ=event.get('type')
            if kind=='claude':
                if typ=='control_response' and event.get('response',{}).get('request_id')=='aura-init':
                    if event['response'].get('subtype')=='error':raise ValueError(event['response'].get('error','Claude initialization failed.'))
                    send({'type':'user','session_id':native_id or '', 'message':{'role':'user','content':prompt},'parent_tool_use_id':None})
                    execution.protocol_ready=True
                elif typ=='control_cancel_request':execution.requests.resolve(event.get('request_id'))
                elif typ=='control_request':
                    ident=event.get('request_id');request=event.get('request') or {}
                    def reply(payload,ident=ident):send({'type':'control_response','response':{'subtype':'success','request_id':ident,'response':payload}})
                    if request.get('subtype')!='can_use_tool':
                        send({'type':'control_response','response':{'subtype':'error','request_id':ident,'error':'Use the native app for this interaction.'}});continue
                    original=request.get('input') or {}
                    if request.get('tool_name')=='AskUserQuestion':
                        qs=[question(str(i),q.get('question',''),[o['label'] for o in q.get('options',[])],q.get('multiSelect'),True) for i,q in enumerate(original.get('questions',[]))]
                        def convert(a,original=original):return {'behavior':'allow','updatedInput':{**original,'answers':{q.get('question',''):', '.join(a[str(i)]) for i,q in enumerate(original.get('questions',[]))}}}
                        add_request(execution,ident,'Your AI has a question',qs,reply,convert)
                    else:
                        q=question('decision',request.get('description') or 'Allow this tool call?', ['Approve once','Decline'])
                        add_request(execution,ident,'Approval needed: '+str(request.get('tool_name','Tool')),[q],reply,
                            lambda a,original=original:{'behavior':'allow','updatedInput':original} if a['decision']==['Approve once'] else {'behavior':'deny','message':'Declined by the user in Aura.'},json.dumps(original,ensure_ascii=False,indent=2))
                    continue
                yield json.dumps(event)
                if typ=='result':finished=True;break
            else:
                if typ=='response' and event.get('id')=='aura-state':
                    if not event.get('success'):raise ValueError(event.get('error','Could not read the native session.'))
                    state=event.get('data') or {};ident=state.get('sessionId')
                    if not ident:raise ValueError('The native app did not provide a saved session ID. No request was sent.')
                    if native_id and ident!=native_id:raise ValueError('The native app opened a different session. No request was sent.')
                    yield json.dumps({'type':'session','id':ident})
                    if kind=='omp':
                        send({'id':'aura-ask','type':'set_ask_dialog','enabled':True})
                        send({'id':'aura-children','type':'set_subagent_subscription','mode':'progress'})
                    send({'id':'aura-prompt','type':'prompt','message':prompt})
                    execution.protocol_ready=True
                elif typ=='response' and event.get('id')=='aura-prompt' and not event.get('success'):raise ValueError(event.get('error','The native app rejected this request.'))
                elif typ=='extension_ui_request':
                    ident=event.get('id');method=event.get('method')
                    if method=='cancel':execution.requests.resolve(event.get('targetId'))
                    elif method=='ask':
                        qs=[question(q['id'],q.get('question',''),[o['label'] for o in q.get('options',[])],q.get('multi'),True) for q in event.get('questions',[])]
                        for q,original in zip(qs,event.get('questions',[])):
                            for option,source in zip(q['options'],original.get('options',[])):option['description']=source.get('description','')
                        def reply(payload,ident=ident):send({'type':'extension_ui_response','id':ident,**payload})
                        def convert(a,qs=qs):
                            return {'answers':[{'id':q['id'],'selectedOptions':[v for v in a[q['id']] if v in {o['value'] for o in q['options']}],
                                **({'customInput':'\n'.join(v for v in a[q['id']] if v not in {o['value'] for o in q['options']})} if any(v not in {o['value'] for o in q['options']} for v in a[q['id']]) else {})} for q in qs]}
                        add_request(execution,ident,event.get('title') or 'Your AI has a question',qs,reply,convert,timeout=event.get('timeout'))
                    elif method in {'select','confirm','input','editor'}:
                        if event.get('secret'):
                            send({'type':'extension_ui_response','id':ident,'cancelled':True});continue
                        options=event.get('options',[]) if method=='select' else ['Yes','No'] if method=='confirm' else []
                        q=question('answer',event.get('message') or event.get('title',''),options)
                        def reply(payload,ident=ident):send({'type':'extension_ui_response','id':ident,**payload})
                        def convert(a,method=method):return {'confirmed':a['answer']==['Yes']} if method=='confirm' else {'value':a['answer'][0]}
                        add_request(execution,ident,event.get('title') or 'Your AI has a question',[q],reply,convert,timeout=event.get('timeout'))
                    continue
                else:yield json.dumps(event)
                if typ in {'agent_settled','session_settled'}:finished=True;break
                if typ=='prompt_result' and event.get('status') in {'error','aborted'}:raise ValueError(str(event.get('error') or 'The native request did not complete.'))
                if typ=='prompt_result' and event.get('sessionSettled') is True:finished=True;break
                if typ=='agent_end':send({'id':'aura-idle','type':'get_state'})
                if typ=='response' and event.get('id')=='aura-idle' and event.get('success'):
                    state=event.get('data') or {}
                    settled=state.get('isSettled') if 'isSettled' in state else state.get('isStreaming') is False and not any(state.get(k) for k in ('isCompacting','isRetrying','pendingMessageCount','queuedMessageCount','hasPendingAsyncWork'))
                    if settled:
                        finished=True;break
        if not finished:raise ValueError(errors.message('The native connection closed before completing. Open its saved chat before retrying.'))
    finally:
        close();execution.requests.close();errors.close_input(process)
        try:process.wait(timeout=3)
        except subprocess.TimeoutExpired:process.terminate();process.wait(timeout=5)
