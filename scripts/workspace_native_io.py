"""Thin bidirectional transports for the native apps' documented request protocols."""
import json
import queue
import subprocess
import threading
import time

from workspace_interactions import answers_for,question


def channel(process,execution,errors):
    events=queue.Queue(maxsize=256);lock=threading.Lock();started=time.monotonic();closed=threading.Event()
    session=execution.native_session
    if session:session.events=events
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
            (session.execution if session else execution).check()
            errors.send(process,json.dumps(value,ensure_ascii=False)+'\n')
    def read_events():
        while True:
            owner=session.execution if session else execution
            owner.check();owner.requests.expire()
            if owner.retry_check_at is not None and time.time()>=owner.retry_check_at:
                owner.retry_check_at=None
                if owner.retry_check:owner.retry_check()
            if not getattr(owner,'protocol_ready',False) and time.monotonic()-started>45:
                raise ValueError('The native app did not initialize. No AI request was resubmitted.')
            wait=(1 if session and session.active is None else .25) if owner.retry_check_at is None else min(.25,max(.001,owner.retry_check_at-time.time()))
            try:event=events.get(timeout=wait)
            except queue.Empty:continue
            if event is None:return
            yield event
    return send,read_events(),closed.set


def add_request(execution,ident,title,questions,send,convert,detail='',timeout=None):
    def validate(answers):return convert(answers_for(questions,answers))
    execution.requests.add(ident,title,questions,send,validate,detail,timeout)


from workspace_native_requests import codex_request, notice, provider

def codex_run(command,cwd,prompt,native_id,model,effort,update,env,execution,child_model=''):
    from workspace_codex import base_command
    from workspace_delegation import Tracker
    from _process_errors import ErrorTail
    import workspace_usage
    mode=execution.permission
    params={**execution.native_options.get('thread',{k:v for k,v in execution.native_options.items() if k!='initialize'}),'cwd':str(cwd),**({'model':model} if model else {})}
    if mode!='native':params.update(sandbox='danger-full-access' if mode=='full' else mode,approvalPolicy='never' if mode=='full' else 'on-request')
    if child_model:params['config']={**params.get('config',{}),'agents.default_subagent_model':child_model}
    if native_id:params.update(threadId=native_id)
    final='';usage={};thread=native_id;complete=False;items={};delegation=Tracker(update)
    previous_total=None;turn_tokens={};turn_started=False;turn_id=None;owned=set();child_started=set();background=[];background_checked=False;background_pages=[]
    goal=getattr(execution,'native_goal',None);goal_state=None;turn_finished=False
    session=execution.native_session
    def settled():
        return turn_finished and background_checked and not background and not execution.helpers and not any(c.get('status') in {'working','pending'} for c in delegation.items.values()) and not any(r['status']=='pending' for r in execution.requests.snapshot()) and (not goal or (goal_state or {}).get('status')!='active')
    with execution.popen([*base_command(command),'app-server'],cwd=cwd,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                         text=True,encoding='utf-8',errors='replace') as process:
        errors=ErrorTail(process,env);send,events,close=channel(process,execution,errors)
        def controls():
            owner=execution
            def current():
                if session and (not session.active or session.active.execution is not owner):raise ValueError('This request has ended. Send a new message instead.')
            def interrupt():
                current()
                if not turn_id:raise ValueError('The native turn has not started yet.')
                send({'id':'aura-interrupt','method':'turn/interrupt','params':{'threadId':thread,'turnId':turn_id}})
            def steer(text,attachments=None):
                current()
                if turn_finished:execution.control(send,{'method':'turn/start','params':{'threadId':thread,'input':[{'type':'text','text':text},*(attachments or [])]}})
                else:execution.control(send,{'method':'turn/steer','params':{'threadId':thread,'expectedTurnId':turn_id,'input':[{'type':'text','text':text},*(attachments or [])]}})
            execution.interrupt=interrupt;execution.steer=steer
            update(native_controls={'steer':True,'interrupt':True})
        def idle(event):
            p=event.get('params') or {};method=event.get('method')
            if execution.resolve_control(event.get('id'),(event.get('error') or {}).get('message')):
                if (event.get('result') or {}).get('goal'):update(native_goal=event['result']['goal'])
                return
            if method and event.get('id') is not None:
                if p.get('threadId') and p['threadId'] not in {thread,*owned}:
                    send({'id':event['id'],'error':{'code':-32602,'message':'This request belongs to another conversation.'}})
                else:codex_request(event,execution,send,update)
            elif method=='serverRequest/resolved':execution.requests.resolve(p.get('requestId'))
            elif method in {'thread/goal/updated','thread/goal/cleared'} and p.get('threadId')==thread:update(native_goal=p.get('goal') or {'status':'cleared'})
        def finish():
            nonlocal execution,update,prompt,model,effort,goal,goal_state,turn_finished,turn_started,turn_id,turn_tokens,usage,final,items,delegation,background_checked
            if not session:return True
            if not final.strip():raise ValueError('Codex ended without a final reply. Open its native chat before retrying.')
            call=session.next({'reply':final,'native_id':thread,'usage':usage},events,idle)
            execution=call.execution;update=call.update;prompt=call.prompt
            execution.protocol_ready=True
            connection=getattr(execution,'connection',{})
            model=connection.get('model') or model;effort=connection.get('effort','')
            goal=execution.native_goal;goal_state=None;turn_finished=False;turn_started=False;turn_id=None
            turn_tokens={};usage={};final='';items={};background_checked=False;delegation=Tracker(update)
            update(native_id=thread,permission_effective=effective)
            controls()
            if goal:send({'id':'aura-goal-read','method':'thread/goal/get','params':{'threadId':thread}})
            else:start_turn(prompt,images=execution.attachments)
            return False
        def start_turn(text,ident='aura-turn',images=None):
            if text.strip()=='/compact':
                send({'id':ident,'method':'thread/compact/start','params':{'threadId':thread}});return
            if text.strip()=='/review' or text.lstrip().startswith('/review '):
                instructions=text.strip()[len('/review'):].strip()
                target={'type':'custom','instructions':instructions} if instructions else {'type':'uncommittedChanges'}
                send({'id':ident,'method':'review/start','params':{'threadId':thread,'delivery':'inline','target':target}});return
            turn={'threadId':thread,'input':[{'type':'text','text':text},*(images or [])],**({'model':model} if model else {})}
            if effort:turn['effort']=effort
            send({'id':ident,'method':'turn/start','params':turn})
        send({'id':'aura-init','method':'initialize','params':{'clientInfo':{'name':'aura_workspace','version':'1.0'},'capabilities':{'experimentalApi':True},**execution.native_options.get('initialize',{})}})
        try:
            for event in events:
                ident=event.get('id');method=event.get('method');p=event.get('params') or {}
                if method=='thread/started':
                    child=p.get('thread') or {}
                    if child.get('parentThreadId') in {thread,*owned} and child.get('id'):
                        owned.add(child['id']);delegation.put(child['id'],status='pending')
                if getattr(execution,'trace',None) and (not p.get('threadId') or p['threadId'] in {thread,*owned}):execution.trace.observe('codex',event,thread)
                if method and ident is not None:
                    if thread and p.get('threadId') and p['threadId']!=thread and p['threadId'] not in owned:
                        send({'id':ident,'error':{'code':-32602,'message':'Different thread.'}});continue
                    codex_request(event,execution,send,update);continue
                if execution.resolve_control(ident,(event.get('error') or {}).get('message')):
                    returned=(event.get('result') or {}).get('turn') or {}
                    if returned.get('id'):turn_id=returned['id'];turn_started=True;turn_finished=False;background_checked=False
                    continue
                if method=='thread/status/changed' and p.get('threadId') in owned:
                    status=p.get('status') or {};status=status.get('type') if isinstance(status,dict) else status
                    if status=='active':child_started.add(p['threadId']);delegation.put(p['threadId'],status='working')
                    elif status in {'notLoaded','systemError'} or status=='idle' and p['threadId'] in child_started:delegation.put(p['threadId'],status='error' if status=='systemError' else 'complete')
                if method=='turn/started' and p.get('threadId') in owned:
                    child_started.add(p['threadId']);delegation.put(p['threadId'],status='working')
                if method=='turn/completed' and p.get('threadId') in owned:
                    delegation.put(p['threadId'],status='complete' if p.get('turn',{}).get('status')=='completed' else 'error')
                if ident=='aura-background':
                    result=event.get('result') or {}
                    background_pages.extend(result.get('data') or [])
                    if result.get('nextCursor'):
                        send({'id':'aura-background','method':'thread/backgroundTerminals/list','params':{'threadId':thread,'cursor':result['nextCursor']}});continue
                    background_checked=True;background=background_pages;background_pages=[]
                    update(background_processes=background,reply_ready=turn_finished,progress='Background processes are running' if background else 'Finishing your request')
                if ident=='aura-interrupt' and 'error' not in event:
                    # The acknowledgement precedes turn/completed. Keep reading
                    # so the native app can unwind its tools before stdin closes.
                    continue
                if ident in {'aura-init','aura-thread','aura-turn','aura-goal-read','aura-goal-set','aura-goal-check','aura-goal-control'} and 'error' in event:
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
                    controls()
                    if goal:send({'id':'aura-goal-read','method':'thread/goal/get','params':{'threadId':thread}})
                    else:start_turn(prompt,images=execution.attachments)
                    execution.protocol_ready=True
                elif ident=='aura-goal-read':
                    existing=(event.get('result') or {}).get('goal')
                    if existing and existing.get('status') not in {'complete','completed'} and existing.get('objective')!=goal['objective']:
                        raise ValueError('This native chat has a different goal. Review or clear it in Codex before starting this goal.')
                    values={'threadId':thread,'objective':goal['objective'],'status':'active','origin':'user'}
                    if goal.get('token_budget') is not None:values['tokenBudget']=goal['token_budget']
                    send({'id':'aura-goal-set','method':'thread/goal/set','params':values})
                elif ident=='aura-goal-set':
                    if execution.goal_cancelled:raise ValueError('The goal changed before work started. Reopen it before continuing.')
                    goal_state=(event.get('result') or {}).get('goal')
                    if not goal_state or goal_state.get('status')!='active':raise ValueError('Codex did not activate native goal mode. No goal request was submitted.')
                    update(native_goal=goal_state)
                    def control(action):
                        value={'method':'thread/goal/clear' if action=='clear' else 'thread/goal/set',
                              'params':{'threadId':thread,'origin':'user',**({} if action=='clear' else {'status':'complete' if action=='complete' else 'paused'})}}
                        if session and session.active is None:execution.control(send,value)
                        else:send({'id':'aura-goal-control',**value})
                    execution.goal_control=control
                    start_turn(prompt,images=execution.attachments)
                elif ident in {'aura-goal-check','aura-goal-control'} or method in {'thread/goal/updated','thread/goal/cleared'} and p.get('threadId')==thread:
                    observed=(event.get('result') or p).get('goal')
                    if observed:
                        goal_state=observed;update(native_goal=observed)
                    elif ident in {'aura-goal-check','aura-goal-control'} or method=='thread/goal/cleared':
                        if (goal_state or {}).get('status')!='complete':goal_state={'status':'cleared'};update(native_goal=goal_state)
                elif ident in {'aura-turn','aura-followup'} or method=='turn/started' and p.get('threadId',thread)==thread:
                    turn_started=True;turn_finished=False;background_checked=False
                    turn_id=((event.get('result') or {}).get('turn') or p.get('turn') or {}).get('id') or turn_id
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
                    delegation.observe('codex',{'type':method,**p})
                    if settled() and finish():complete=True;break
                    continue
                elif method in {'item/started','item/completed'}:
                    if method=='item/completed' and (p.get('item') or {}).get('type')=='contextCompaction':
                        update(native_maintenance={'type':'auto_compaction_end'})
                    item=p.get('item') or {};typ=item.get('type')
                    if typ=='subAgentActivity':
                        if item.get('agentThreadId'):owned.add(item['agentThreadId'])
                        delegation.observe('codex',{'item':item})
                    elif typ=='agentMessage':
                        items[item['id']]=item
                        if method=='item/completed' and item.get('phase')!='commentary':final=item.get('text','');update(reply=final)
                    elif typ=='exitedReviewMode' and method=='item/completed':
                        final=item.get('review') or final;update(reply=final)
                    elif typ=='contextCompaction' and method=='item/completed':
                        final='Conversation compacted.';update(reply=final)
                    else:
                        label={'commandExecution':'Running a command','fileChange':'Updating files','webSearch':'Searching the web','mcpToolCall':'Using a connected tool'}.get(typ)
                        if label:update(progress=label)
                        if typ=='collabAgentToolCall':
                            new_children=set(item.get('receiverThreadIds',[]))-owned
                            owned.update(new_children)
                            adapted={**item,'type':'collab_tool_call','sender_thread_id':item.get('senderThreadId'),
                                'receiver_thread_ids':item.get('receiverThreadIds',[]),
                                'agents_states':{key:{'status':{'pendingInit':'pending_init','notFound':'not_found'}.get(value.get('status'),value.get('status')),'message':value.get('message')}
                                                for key,value in item.get('agentsStates',{}).items()}}
                            delegation.observe('codex',{'type':method.replace('/','.'),'item':adapted})
                            for child in new_children:
                                send({'id':'aura-child-'+child,'method':'thread/resume','params':{'threadId':child}})
                elif method=='item/agentMessage/delta':
                    item=items.setdefault(p.get('itemId'),{'text':''});item['text']=item.get('text','')+p.get('delta','')
                    if item.get('phase')!='commentary':update(reply=item['text'])
                elif method=='turn/completed':
                    turn=p.get('turn') or {}
                    if execution.interrupt_requested:
                        from workspace_execution import Stopped
                        raise Stopped()
                    if turn.get('status')!='completed':raise ValueError(str((turn.get('error') or {}).get('message') or 'The native turn did not complete.'))
                    turn_finished=True
                    update(reply_ready=True,progress='Waiting for native background work' if any(c.get('status') in {'working','pending'} for c in delegation.items.values()) else 'Finishing your request')
                    send({'id':'aura-background','method':'thread/backgroundTerminals/list','params':{'threadId':thread}})
                    if goal and (goal_state or {}).get('status')=='active':send({'id':'aura-goal-check','method':'thread/goal/get','params':{'threadId':thread}})
                elif method=='error' and not p.get('willRetry'):raise ValueError(str((p.get('error') or {}).get('message') or 'The native app reported an error.'))
                if background and method in {'item/completed','thread/status/changed','item/commandExecution/terminalInteraction','process/exited'}:
                    send({'id':'aura-background','method':'thread/backgroundTerminals/list','params':{'threadId':thread}})
                if settled():
                    if finish():complete=True;break
            if not complete:
                if execution.interrupt_requested:
                    from workspace_execution import Stopped
                    raise Stopped()
                raise ValueError(errors.message('Codex disconnected before completing. Open the native chat; this request was not resubmitted.'))
        finally:
            execution.goal_control=None;execution.interrupt=None;execution.steer=None;execution.close_controls();close();execution.requests.close();ErrorTail.close_input(process)
            try:process.wait(timeout=3)
            except subprocess.TimeoutExpired:process.terminate();process.wait(timeout=5)
    execution.check()
    if not final.strip():raise ValueError('Codex ended without a final reply. Open its native chat before retrying.')
    return {'reply':final,'native_id':thread,'usage':usage}


def agent_lines(process,kind,prompt,native_id,execution,errors):
    """Yield ordinary native events to the existing reply/usage/delegation parser."""
    send,events,close=channel(process,execution,errors);finished=False
    goal=getattr(execution,'native_goal',None);last_goal_status=None;result_received=False;session_state=None;tasks=set();activity=False
    session=execution.native_session
    def idle(event):
        from workspace_native_requests import claude_request,extension_request,display
        if event.get('type') in {'cache_warming_start','cache_warming_end','auto_compaction_end','manual_compaction_end'}:
            session.update(native_maintenance=event)
            return
        if event.get('type')=='response' and execution.resolve_control(event.get('id'),event.get('error') if event.get('success') is False else None):
            value=(event.get('data') or {}).get('goal')
            if value:session.update(native_goal=value)
            return
        if event.get('type')=='goal_updated' and goal:
            session.update(native_goal=event.get('goal') or (event.get('data') or {}).get('goal') or {'status':'cleared'})
            return
        if event.get('type')=='control_request' and kind=='claude':claude_request(event,execution,send)
        elif event.get('type')=='control_cancel_request':execution.requests.resolve(event.get('request_id'))
        elif event.get('type')=='extension_ui_request':
            shown=extension_request(event,execution,send)
            if shown:display(shown,execution,session.update)
    def next_request():
        nonlocal execution,prompt,native_id,goal,last_goal_status,result_received,session_state,activity
        if execution.interrupt_requested:
            from workspace_execution import Stopped
            raise Stopped()
        yield json.dumps({'type':'aura_turn_end'})
        call=session.next(session.turn_result,events,idle)
        execution=call.execution;prompt=call.prompt;native_id=call.native_id or session.native_id
        execution.protocol_ready=True;goal=execution.native_goal;last_goal_status=None;result_received=False;session_state=None;activity=False
        execution.retry_check=retry_check
        yield call
        controls()
        if kind=='claude':send({'type':'user','session_id':native_id or '', 'message':{'role':'user','content':[{'type':'text','text':prompt},*execution.attachments] if execution.attachments else prompt},'parent_tool_use_id':None})
        else:send({'id':'aura-state','type':'get_state'})
    def controls():
        owner=execution
        def current():
            if session and (not session.active or session.active.execution is not owner):raise ValueError('This request has ended. Send a new message instead.')
        def interrupt():
            current()
            send({'type':'control_request','request_id':'aura-interrupt','request':{'subtype':'interrupt'}} if kind=='claude' else {'id':'aura-interrupt','type':'abort'})
        def steer(text,attachments=None):
            current()
            if kind=='claude':send({'type':'user','session_id':native_id or '','message':{'role':'user','content':[{'type':'text','text':text},*(attachments or [])]},'parent_tool_use_id':None})
            else:execution.control(send,{'type':'steer','message':text,**({'images':attachments} if attachments else {})})
        execution.interrupt=interrupt;execution.steer=steer
    def retry_check():
        reason=execution.continuation_guard()
        if reason:
            send({'id':'aura-abort-retry','type':'abort_retry'})
            execution.continuation_changed({'continuation_note':reason,'progress':'Continuation needs review'})
    execution.retry_check=retry_check
    if kind=='claude':
        send({'type':'control_request','request_id':'aura-init','request':{'subtype':'initialize',**execution.native_options.get('initialize',{})}})
        controls()
    else:
        send({'id':'aura-commands','type':'get_commands'})
        send({'id':'aura-state','type':'get_state'})
    try:
        for event in events:
            typ=event.get('type')
            if kind=='claude' and typ=='system' and event.get('subtype')=='compact_boundary' and session:
                session.update(native_maintenance={'type':'auto_compaction_end'})
            if typ in {'cache_warming_start','cache_warming_end','auto_compaction_end','manual_compaction_end'}:
                session.update(native_maintenance=event) if session else None
            if kind in {'pi','omp'} and (typ in {'agent_start','tool_execution_start','prompt_result'} or typ in {'message_start','message_end','message_update'} and (event.get('message') or {}).get('role','assistant')=='assistant'):activity=True
            if typ=='response' and execution.resolve_control(event.get('id'),event.get('error') if event.get('success') is False else None):continue
            if kind in {'pi','omp'} and getattr(execution,'continuation',None) is not None:
                if typ=='auto_retry_start':
                    delay=event.get('delayMs');until=execution.continuation.get('until')
                    reason=execution.continuation_guard()
                    if not reason and (not isinstance(delay,(float,int)) or delay<0):reason='The native app did not report a retry time. Continue manually.'
                    if not reason and until and time.time()+delay/1000>=until:reason='The native retry would occur after this assignment’s continuation expiry.'
                    if not reason:reason=execution.claim_continuation()
                    if reason:
                        send({'id':'aura-abort-retry','type':'abort_retry'})
                        execution.continuation_changed({'continuation_note':reason,'progress':'Waiting for manual continuation'})
                    else:
                        retry_at=time.time()+delay/1000
                        execution.retry_check_at=max(time.time(),retry_at-.05)
                        execution.continuation_changed({'retry_at':retry_at,'progress':'Waiting for the native app to retry','continuation_note':'Native retry scheduled. Availability is not guaranteed.'})
                elif typ=='auto_retry_end':
                    execution.retry_check_at=None;execution.release_continuation()
                    execution.continuation_changed({'retry_at':None,'progress':'Continuing the assignment' if event.get('success') else 'Native retries ended'})
            if kind=='claude':
                if typ=='control_response' and event.get('response',{}).get('request_id')=='aura-interrupt':
                    continue
                if typ=='control_response' and event.get('response',{}).get('request_id')=='aura-init':
                    if event['response'].get('subtype')=='error':raise ValueError(event['response'].get('error','Claude initialization failed.'))
                    available=event['response'].get('response') or {}
                    yield json.dumps({'type':'aura_native_commands','commands':available.get('commands') or available.get('slash_commands') or []})
                    send({'type':'user','session_id':native_id or '', 'message':{'role':'user','content':[{'type':'text','text':prompt},*execution.attachments] if execution.attachments else prompt},'parent_tool_use_id':None})
                    execution.protocol_ready=True
                    yield json.dumps({'type':'aura_controls','steer':True,'interrupt':True})
                elif typ=='control_cancel_request':execution.requests.resolve(event.get('request_id'))
                elif typ=='control_request':
                    from workspace_native_requests import claude_request
                    claude_request(event,execution,send)
                    continue
                if typ=='system':
                    subtype=event.get('subtype');task=event.get('task_id')
                    if subtype=='task_started' and task:tasks.add(task)
                    elif subtype=='task_notification' and task:tasks.discard(task)
                    elif subtype=='task_updated' and (event.get('patch') or {}).get('status') in {'completed','failed','stopped'}:tasks.discard(task)
                    elif subtype=='session_state_changed':session_state=event.get('state')
                yield json.dumps(event)
                if typ=='result':result_received=True;yield json.dumps({'type':'aura_reply_ready','background':bool(tasks) or session_state not in {None,'idle'}})
                if result_received and not tasks and session_state in {None,'idle'} and not execution.helpers and not any(r['status']=='pending' for r in execution.requests.snapshot()):
                    if session:yield from next_request();continue
                    finished=True;break
            else:
                if typ=='response' and event.get('id')=='aura-commands':
                    if event.get('success'):yield json.dumps({'type':'aura_native_commands','commands':(event.get('data') or {}).get('commands') or []})
                    continue
                if typ=='response' and event.get('id')=='aura-state':
                    if not event.get('success'):raise ValueError(event.get('error','Could not read the native session.'))
                    state=event.get('data') or {};ident=state.get('sessionId')
                    if not ident:raise ValueError('The native app did not provide a saved session ID. No request was sent.')
                    if native_id and ident!=native_id:raise ValueError('The native app opened a different session. No request was sent.')
                    yield json.dumps({'type':'session','id':ident})
                    controls()
                    if kind=='omp':
                        send({'id':'aura-ask','type':'set_ask_dialog','enabled':True})
                        send({'id':'aura-children','type':'set_subagent_subscription','level':'events' if execution.trace else 'progress'})
                    if goal and kind=='omp':
                        existing=state.get('goal')
                        if existing and existing.get('status') not in {'complete','completed'} and not existing.get('objective','').startswith(goal['objective']+'\n\n'):
                            raise ValueError('OMP already has a different native goal in this chat. Review or drop it in OMP before starting another goal.')
                        if existing and existing.get('status') not in {'complete','completed'} and goal.get('token_budget') is not None and existing.get('tokenBudget')!=goal['token_budget']:
                            raise ValueError('OMP keeps the existing native goal budget when resuming. Keep that budget or drop the native goal in OMP before choosing a different one.')
                        values={'id':'aura-goal-create','type':'goal','op':'resume' if existing and existing.get('status') not in {'complete','completed'} else 'create','objective':goal['objective']+'\n\n'+prompt}
                        if goal.get('token_budget') is not None:values['token_budget']=goal['token_budget']
                        send(values)
                        def control(action):
                            value={'type':'goal','op':'pause' if action=='pause' else 'drop'}
                            if session and session.active is None:execution.control(send,value)
                            else:send({'id':'aura-goal-control',**value})
                        execution.goal_control=control
                    elif prompt.strip()=='/compact' or prompt.strip().startswith('/compact '):
                        send({'id':'aura-compact','type':'compact',**({'customInstructions':prompt.strip()[8:].strip()} if prompt.strip()[8:].strip() else {})})
                    else:send({'id':'aura-prompt','type':'prompt','message':prompt,**({'images':execution.attachments} if execution.attachments else {})})
                    execution.protocol_ready=True
                    yield json.dumps({'type':'aura_controls','steer':True,'interrupt':True})
                elif typ=='response' and event.get('id')=='aura-compact':
                    if not event.get('success'):raise ValueError(event.get('error') or 'The AI app could not compact this conversation.')
                    if session:session.update(native_maintenance={'type':'manual_compaction_end'})
                    yield json.dumps({'type':'aura_compact_done'})
                    if session:yield from next_request();continue
                    finished=True;break
                elif typ=='response' and event.get('id')=='aura-children' and not event.get('success'):
                    yield json.dumps({'type':'aura_notice','text':'This installed connection could not provide subagent progress. Work can continue without the progress display.'})
                elif typ=='response' and event.get('id') in {'aura-goal-create','aura-goal-control'}:
                    if not event.get('success'):raise ValueError(event.get('error') or 'The native app could not change this goal.')
                    value=(event.get('data') or {}).get('goal')
                    if event['id']=='aura-goal-create' and not value:raise ValueError('OMP did not confirm native goal activation.')
                    if value:
                        last_goal_status=value.get('status');yield json.dumps({'type':'aura_native_goal','goal':value})
                    elif event['id']=='aura-goal-control' and last_goal_status not in {'complete','completed'}:
                        last_goal_status='cleared';yield json.dumps({'type':'aura_native_goal','goal':{'status':'cleared'}})
                elif typ=='goal_updated' and goal:
                    value=event.get('goal') or (event.get('data') or {}).get('goal')
                    if value:
                        last_goal_status=value.get('status');yield json.dumps({'type':'aura_native_goal','goal':value})
                    elif last_goal_status not in {'complete','completed'}:
                        last_goal_status='cleared';yield json.dumps({'type':'aura_native_goal','goal':{'status':'cleared'}})
                elif typ=='response' and event.get('id')=='aura-prompt' and not event.get('success'):raise ValueError(event.get('error','The native app rejected this request.'))
                elif typ=='extension_ui_request':
                    from workspace_native_requests import extension_request
                    shown=extension_request(event,execution,send)
                    if shown:yield json.dumps(shown)
                    continue
                else:yield json.dumps(event)
                if typ in {'agent_settled','session_settled'} and activity:
                    if session:yield from next_request();continue
                    finished=True;break
                if typ=='prompt_result' and event.get('status') in {'error','aborted'}:raise ValueError(str(event.get('error') or 'The native request did not complete.'))
                if typ=='prompt_result' and event.get('sessionSettled') is True:
                    if session:yield from next_request();continue
                    finished=True;break
                if typ=='agent_end' and activity:send({'id':'aura-idle','type':'get_state'})
                if typ=='response' and event.get('id')=='aura-idle' and event.get('success'):
                    state=event.get('data') or {}
                    settled=state.get('isSettled') if 'isSettled' in state else state.get('isStreaming') is False and not any(state.get(k) for k in ('isCompacting','isRetrying','pendingMessageCount','queuedMessageCount','hasPendingAsyncWork'))
                    if settled:
                        if session:yield from next_request();continue
                        finished=True;break
        if execution.interrupt_requested:
            from workspace_execution import Stopped
            raise Stopped()
        if not finished:raise ValueError(errors.message('The native connection closed before completing. Open its saved chat before retrying.'))
    finally:
        execution.goal_control=None
        execution.interrupt=None;execution.steer=None
        execution.retry_check_at=None
        execution.close_controls();close();execution.requests.close();errors.close_input(process)
        try:process.wait(timeout=3)
        except subprocess.TimeoutExpired:process.terminate();process.wait(timeout=5)
