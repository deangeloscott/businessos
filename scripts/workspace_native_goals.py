"""Native goal requests and observations. The harness owns every continuation turn."""
import json
import os
import subprocess
import time
from pathlib import Path


def objective(goal,limit=None):
    target=goal.get('target')
    text=goal['name']+('\nDone when: '+(target if isinstance(target,str) else json.dumps(target,ensure_ascii=False)) if target else '')
    if limit and len(text)>limit:raise ValueError('This AI app limits its native goal to 4,000 characters. Shorten the goal or completion criteria before starting.')
    return text


def support(kind,agent,permission='native'):
    custom=agent.get('native_goal') or {}
    if custom:
        argv=custom.get('argv')
        if custom.get('protocol')!='aura-goal-v1' or not isinstance(argv,list) or not argv or not all(isinstance(v,str) and v for v in argv):
            raise ValueError('The custom native goal connection needs protocol aura-goal-v1 and an argv list.')
        return {'supported':True,'protocol':'aura-goal-v1','token_budget':bool(custom.get('token_budget')),'status_sync':True}
    if kind=='antigravity' and '--disable-slash-commands' in agent.get('argv',[]):return {'supported':False,'protocol':None,'token_budget':False,'status_sync':False,'reason':'This connection disables native commands. Enable them in its connection command or use a native goal adapter.'}
    protocol={'codex':'codex','omp':'omp','claude':'slash','antigravity':'slash'}.get(kind)
    if kind=='hermes':
        from workspace_hermes import enabled
        if enabled(agent.get('argv',[]),agent.get('native_options'),permission):protocol='hermes-gateway'
    return {'supported':bool(protocol),'protocol':protocol,'token_budget':kind in {'codex','omp'},'status_sync':kind in {'codex','omp'} or protocol=='hermes-gateway',
            'reason':{'pi':'Native goal mode is not available in this Pi connection. You can still use the goal in chat.',
                      'hermes':'Native goal mode is not available in this Hermes connection. Use Hermes directly for persistent goals, or use this goal as chat context.'}.get(kind,'Native goal mode is not available in this connection. You can still use the goal as chat context.') if not protocol else ''}


def spec(goal,options,kind,agent,permission='native'):
    from workspace_goals import scope,available,fingerprint
    if scope(goal)!='chat':raise ValueError('Native goal mode belongs to a chat goal. Create a chat goal for this workspace outcome.')
    if not available(goal):raise ValueError('Resume this chat goal before starting native work.')
    capability=support(kind,agent,permission)
    if not capability['supported']:raise ValueError(capability['reason'])
    budget=options.get('token_budget')
    if budget is not None:
        if not capability['token_budget']:raise ValueError('This connection does not expose a native token budget.')
        if isinstance(budget,bool) or not isinstance(budget,int) or budget<=0:raise ValueError('Enter a positive token budget or leave it empty.')
    return {'id':goal['id'],'objective':objective(goal,4000 if kind in {'codex','claude'} and capability['protocol']!='aura-goal-v1' else None),'token_budget':budget,'protocol':capability['protocol'],'basis':fingerprint(goal)}


def observe(app,bid,chat,request,value):
    """Record native evidence; only a native completion can finish the linked chat goal."""
    from workspace_goals import find,save,scope,deleted,changed,fingerprint
    if not isinstance(value,dict):return
    allowed={'status','objective','tokenBudget','tokensUsed','timeUsedSeconds','reason','native_id','native_basis'}
    state={k:v for k,v in (value or {}).items() if k in allowed}
    if isinstance(state.get('objective'),str) and len(state['objective'])>4000:state['objective']=request['objective']
    state.update(goal_id=request['id'],checked_at=time.time(),protocol=request['protocol'],requested_objective=request['objective'])
    native_objective=value.get('objective')
    if value.get('bound_to')==request['objective'] and isinstance(native_objective,str) and 'native_objective' not in request:
        request['native_objective']=native_objective
        if value.get('native_basis'):request['native_basis']=value['native_basis']
    expected=request.get('native_objective',request['objective'])
    if isinstance(native_objective,str) and native_objective!=expected and not native_objective.startswith(expected+'\n\n'):
        request['native_changed']=True
    if value.get('native_basis') and request.get('native_basis') and value['native_basis']!=request['native_basis']:request['native_changed']=True
    if request.get('native_changed'):
        state.update(status='needs_review',native_changed=True,reason='The native goal changed in this chat. Review it before continuing with this saved goal.')
        chat['native_goal']=state;app.save_preferences();return
    chat['native_goal']=state
    try:goal=find(bid,request['id'],include_deleted=True)
    except ValueError:return
    if deleted(goal) or scope(goal)!='chat' or chat.get('goal_id')!=goal['id'] or request.get('basis') and fingerprint(goal)!=request['basis']:return
    status=state.get('status') if isinstance(state.get('status'),str) else 'unknown'
    desired='active' if status=='active' else 'completed' if status in {'complete','completed'} else 'paused' if status in {'paused','blocked','budgetLimited','usageLimited','budget_limited','usage_limited','budget-limited','usage-limited','cleared','cancelled','canceled'} else None
    # A late active update must never undo a user pause, deletion or completion.
    if request.get('completed') and desired!='completed':return
    if desired=='completed':request['completed']=True
    if desired and goal.get('status','active')!=desired:
        goal=save(bid,{'id':goal['id'],'status':desired});request['basis']=fingerprint(goal);changed(app,bid,goal['id']);app.read_cache.clear()
    app.save_preferences()


def control(app,bid,goal,action):
    """Change only the selected goal in its live process or saved native session."""
    from workspace_goals import metadata,scope,goals
    if scope(goal)=='workspace':
        for child in goals(bid):
            if metadata(child).get('workspace_goal_ref')==goal['id']:control(app,bid,child,'pause')
        return
    owner=metadata(goal).get('chat_id')
    chat=next((c for c in app.preferences['chats'] if c['id']==owner and c['business_id']==bid and Path(c.get('workspace') or app.workspace_path).resolve()==Path(app.workspace_path).resolve()),None)
    if not chat:return
    if (chat.get('native_goal') or {}).get('native_changed'):return
    for job in app.running_jobs():
        if job.get('chat_id')==owner and job.get('workspace')==app.workspace_path:
            execution=app.executions.get(job['id'])
            if execution and (getattr(execution,'native_goal',None) or {}).get('id')==goal['id']:
                execution.goal_cancelled=True
                if getattr(execution,'goal_control',None):execution.goal_control(action)
                else:execution.stop()
                return
    state=chat.get('native_goal') or {}
    if state.get('goal_id')!=goal['id'] or not chat.get('native_id'):return
    session=getattr(app,'native_sessions',None)
    session=session.items.get((str(Path(app.workspace_path).resolve()),bid,owner)) if session else None
    if session and not session.closed and session.active is None and (session.execution.native_goal or {}).get('id')==goal['id'] and session.execution.goal_control:
        try:session.execution.goal_control(action)
        except (ValueError,OSError) as error:
            chat['native_goal']={**state,'status':'needs_review','reason':'The native app could not confirm this goal change. Check its goal before continuing.'}
            chat['native_goal_error']=str(error)
        return
    agent=app.native_choice(chat['agent']) or {}
    try:
        actual=saved_control(agent,agent.get('native_protocol') or chat['agent'],app.workspace_path,app.agent_environment(agent),chat['native_id'],state.get('objective') or objective(goal),action,expected_basis=state.get('native_basis'))
        chat['native_goal']={**state,**actual,'checked_at':time.time()}
    except (ValueError,OSError,subprocess.SubprocessError) as error:
        chat['native_goal']={**state,'status':'needs_review','reason':'The local goal changed, but the native app could not confirm the same change. Check its goal before continuing.'}
        chat['native_goal_error']=str(error)


def saved_control(agent,kind,cwd,env,native_id,expected,action,expected_basis=None):
    """No prompt or native goal resume is sent by a pause, completion or clear operation."""
    if kind=='hermes':
        import workspace_hermes
        return workspace_hermes.saved_control(agent['argv'],agent.get('native_options'),cwd,env,native_id,expected,action,expected_basis)
    if kind=='codex':
        from workspace_codex import rpc
        def call(client):
            client('thread/resume',{'threadId':native_id})
            current=client('thread/goal/get',{'threadId':native_id}).get('goal')
            if not current:return {'status':'cleared'}
            if action=='complete' and current.get('status')=='complete':return current
            if current.get('objective')!=expected:raise ValueError('The native goal changed. No native goal was modified.')
            result=client('thread/goal/clear',{'threadId':native_id,'origin':'user'}) if action=='clear' else client('thread/goal/set',{'threadId':native_id,'origin':'user','status':'complete' if action=='complete' else 'paused'})
            return result.get('goal') or {'status':'cleared'}
        return rpc(agent['argv'],call,cwd,env,experimental=True)
    if kind=='omp':
        from workspace_agents import Metadata
        host=Metadata(agent['argv'],kind,cwd,env,native_id=native_id)
        try:
            current=host.call('goal',op='get').get('goal')
            if not current:return {'status':'cleared'}
            if not current.get('objective','').startswith(expected):raise ValueError('The native goal changed. No native goal was modified.')
            result=host.call('goal',op='pause' if action=='pause' else 'drop')
            return result.get('goal') or {'status':'cleared'}
        finally:host.close()
    custom=agent.get('native_goal') or {}
    if custom.get('protocol')=='aura-goal-v1':
        result=subprocess.run(custom['argv'],input=json.dumps({'action':action,'native_id':native_id,'objective':expected})+'\n',capture_output=True,text=True,encoding='utf-8',cwd=cwd,env=env,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        rows=[json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        state=next((r for r in reversed(rows) if r.get('type')=='goal'),None)
        if result.returncode or not state:raise ValueError('The custom adapter did not confirm the goal change.')
        return {k:v for k,v in state.items() if k in {'status','reason'}}
    raise ValueError('This connection does not expose a saved native goal control API.')


def custom_run(command,cwd,env,prompt,native_id,execution,update):
    """Optional machine-owned JSONL adapter; it drives its own harness, never an Aura loop."""
    from _process_errors import ErrorTail
    from workspace_native_io import channel
    request=execution.native_goal;reply='';ident=native_id;finished=False
    with execution.popen(command,cwd=cwd,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace') as process:
        errors=ErrorTail(process,env);send,events,close=channel(process,execution,errors)
        execution.goal_control=lambda action:send({'action':action,'goal_id':request['id']})
        send({'action':'run','goal':request,'prompt':prompt,'native_id':native_id,'workspace':str(cwd),'connection':getattr(execution,'connection',{}),'permission_mode':execution.permission})
        execution.protocol_ready=True
        try:
            for event in events:
                typ=event.get('type')
                if typ=='session':
                    if native_id and event.get('id')!=native_id:raise ValueError('The goal adapter opened a different native chat.')
                    ident=event.get('id');update(native_id=ident)
                elif typ=='goal':update(native_goal=event)
                elif typ=='reply':reply=str(event.get('text',''));update(reply=reply)
                elif typ=='result':
                    if event.get('status')!='complete':raise ValueError(event.get('message') or 'The native goal adapter stopped before completing the request.')
                    finished=True;break
                elif typ=='error':raise ValueError(event.get('message') or 'The native goal adapter could not run this goal.')
            if not finished:raise ValueError('The native goal adapter disconnected. Check its saved goal before continuing.')
        finally:
            execution.goal_control=None;close();errors.close_input(process)
            try:process.wait(timeout=3)
            except subprocess.TimeoutExpired:process.terminate();process.wait(timeout=5)
    if not reply.strip():raise ValueError('The native goal adapter finished without a reply. Check the saved native chat.')
    return {'reply':reply,'native_id':ident,'usage':{}}
