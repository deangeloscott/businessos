"""Use Hermes's own desktop/TUI gateway; Hermes owns commands and goal turns."""
import os
import hashlib
import json
import re
import shlex
from pathlib import Path
import subprocess
from functools import lru_cache
from contextlib import contextmanager


@lru_cache(maxsize=16)
def gateway_command(command):
    """Recognize installed native runtimes without bypassing custom launchers."""
    if len(command)!=1:return None
    executable=Path(command[0]).resolve()
    candidates=[executable.parent.parent/'hermes-agent',executable.parent.parent,executable.parent.parent.parent,
                executable.parent.parent.parent/'hermes-agent']
    for root in candidates:
        if not (root/'tui_gateway'/'entry.py').is_file():continue
        for python in (root/'venv'/'Scripts'/'python.exe',root/'.venv'/'Scripts'/'python.exe',
                       root/'venv'/'bin'/'python',root/'.venv'/'bin'/'python'):
            if python.is_file():return (str(python),'-P','-m','tui_gateway.entry'),str(root)
    return None


def connection(command,options=None):
    from workspace_agents import base_command
    configured=(options or {}).get('gateway_argv')
    if configured==[]:return None
    if configured is not None:
        if not isinstance(configured,list) or not all(isinstance(v,str) and v for v in configured):raise ValueError('Hermes gateway needs a non-empty command list.')
        return list(configured),None
    found=gateway_command(tuple(base_command(command)))
    return (list(found[0]),found[1]) if found else None


def enabled(command,options=None,permission='native'):
    return permission in {'native','yolo'} and not (options or {}).get('config') and bool(connection(command,options))


def session_options(options):
    values=(options or {}).get('session',{})
    if not isinstance(values,dict):raise ValueError('Hermes session options must be an object.')
    if {'session_id','cwd','cwd_explicit','model','provider','reasoning_effort','omit_messages','lazy'}&values.keys():
        raise ValueError('Set the chat, folder, model and effort through their AURA controls. Keep other Hermes session options here.')
    return dict(values)


@contextmanager
def profile_client(command,options,cwd,env):
    """Use the installed gateway's profile APIs without starting a model turn."""
    from workspace_agents import Metadata
    launch=connection(command,options)
    if not launch:raise ValueError('This Hermes connection does not expose native profile management. Update Hermes or use its own profile settings.')
    argv,root=launch
    if root:env={**env,'PYTHONPATH':os.pathsep.join([root,env.get('PYTHONPATH','')])}
    host=Metadata(argv,'acp',cwd,env)
    try:yield host.call
    finally:host.close()


def metadata(command,options,cwd,env,method,**params):
    with profile_client(command,options,cwd,env) as call:return call(method,**params)


def profiles(command,options,cwd,env):
    return metadata(command,options,cwd,env,'profiles.list',include_sessions=False).get('profiles',[])


def profile(command,options,cwd,env,name):
    """Return the native editor snapshot, with no sign-ins or private histories."""
    return profile_snapshot(metadata(command,options,cwd,env,'profiles.describe',name=name),name)


def profile_snapshot(row,name):
    model=row.get('model') or {};provider=model.get('provider','');model=model.get('default','')
    return {'app':'hermes','scope':'profile','file':name,'name':name,'description':row.get('description',''),
        'instructions':row.get('soul',''),'model':provider+':'+model if provider and model else model,'effort':'',
        'settings':row,'primary':True,'revision':hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()}


def save_profile(command,options,cwd,env,data):
    with profile_client(command,options,cwd,env) as call:return _save_profile(call,data)


def _save_profile(call,data):
    name=data.get('file') or data.get('name','')
    if not isinstance(name,str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',name):raise ValueError('Use a Hermes profile name with lowercase letters, numbers, hyphens, or underscores.')
    fields={k:data[k] for k in ('name','description','instructions','model') if k in data}
    if any(not isinstance(v,str) or len(v)>20000 for v in fields.values()):raise ValueError('Enter valid profile instructions and preferences.')
    if not data.get('file'):
        call('profiles.create',name=name,no_alias=True,mirror_credentials=False,
                 no_skills=data.get('include_skills') is False,soul=data.get('instructions',''),description=data.get('description',''),timeout=120)
    current=profile_snapshot(call('profiles.describe',name=name),name)
    if data.get('file') and data.get('revision')!=current['revision']:raise ValueError('This Hermes profile changed. Reopen it before saving.')
    changes={native:data[key] for key,native in (('description','description'),('instructions','soul')) if key in data and data[key]!=current[key]}
    if 'model' in data and data['model']!=current['model']:
        if data['model']:
            catalog=call('model.options',profile=name,explicit_only=True)
            changes.update(model_route(catalog,data['model']))
        elif data.get('file'):raise ValueError('Choose a model for this Hermes profile, or keep its current model.')
    for key in ('disabled_skills','enabled_toolsets','enabled_mcp_servers'):
        if key in data:
            if not isinstance(data[key],list) or any(not isinstance(v,str) for v in data[key]):raise ValueError('Choose valid native profile capabilities.')
            available=current['settings'].get({'disabled_skills':'skills','enabled_toolsets':'toolsets','enabled_mcp_servers':'mcp_servers'}[key],[])
            if set(data[key])-{r['name'] for r in available}:raise ValueError('The native capabilities changed. Reopen this profile.')
            changes[key]=data[key]
    if changes:
        result=call('profiles.configure',name=name,**changes)
        if not result.get('ok') or result.get('confirm_required'):raise ValueError(result.get('confirm_message') or 'Hermes did not apply every profile change. Reopen its settings to check.')
    saved=profile_snapshot(call('profiles.describe',name=name),name)
    if any(saved[key]!=data[key] for key in ('description','instructions') if key in data):raise ValueError('Hermes did not confirm these instructions. Reopen the profile to check.')
    if any(saved['settings'].get('model',{}).get('default' if key=='model' else key)!=changes[key] for key in ('model','provider') if key in changes):raise ValueError('Hermes did not confirm the selected model. Reopen the profile to check.')
    for key,collection in (('disabled_skills','skills'),('enabled_toolsets','toolsets'),('enabled_mcp_servers','mcp_servers')):
        if key in changes:
            if key=='enabled_toolsets' and not changes[key]:
                if saved['settings'].get('toolsets_pinned'):raise ValueError('Hermes did not restore its default tools. Reopen the profile to check.')
                continue
            actual={r['name'] for r in saved['settings'].get(collection,[]) if bool(r.get('enabled'))!=(key=='disabled_skills')}
            if actual!=set(changes[key]):raise ValueError('Hermes did not confirm every capability change. Reopen the profile to check.')
    return saved


def tokens(value):
    from workspace_usage import number
    return {key:value[native] for key,native in (('input_tokens','input'),('output_tokens','output')) if number(value.get(native)) is not None}


def model_route(catalog,choice):
    """Match ACP's opaque choice to the gateway's own provider/model catalog."""
    if not choice:return {}
    matches=[]
    for row in catalog.get('providers',[]):
        names={row['slug'],*(row.get('aliases') or [])}
        # ACP's unnamed custom endpoint represents the current native route.
        if row.get('is_current') and row.get('is_user_defined'):names.add('custom')
        for model in row.get('models',[]):
            if choice in {name+':'+model for name in names} or choice==model==catalog.get('model') and row['slug']==catalog.get('provider'):
                matches.append({'model':model,'provider':row['slug']})
    if len(matches)!=1:raise ValueError('Hermes could not match this model to one native provider. Refresh the model choices and select it again.')
    return matches[0]


def goal_state(control):
    value=(control or {}).get('goal')
    if not value:return {'status':'cleared'}
    status={'achieved':'complete','done':'complete','failed':'paused'}.get(value.get('status'),value.get('status','unknown'))
    basis=hashlib.sha256(json.dumps([value.get('title',''),value.get('contract') or {}],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    return {'status':status,'objective':value.get('title',''),'reason':value.get('last_reason') or value.get('paused_reason',''),'native_basis':basis}


def saved_control(command,options,cwd,env,native_id,expected,action,expected_basis=None):
    from workspace_agents import Metadata
    launch=connection(command,options)
    if not launch:raise ValueError('This Hermes installation does not expose native goal controls.')
    argv,root=launch
    if root:env={**env,'PYTHONPATH':os.pathsep.join([root,env.get('PYTHONPATH','')])}
    host=Metadata(argv,'acp',cwd,env)
    try:
        state=host.call('session.resume',session_id=native_id,lazy=True,omit_messages=True,**session_options(options))
        actual=state.get('stored_session_id') or state.get('session_key') or (state.get('info') or {}).get('stored_session_id')
        if actual!=native_id:raise ValueError('Hermes did not confirm the requested saved conversation.')
        ident=state['session_id'];current=goal_state(host.call('session.control.read',session_id=ident).get('control'))
        if current['status']=='cleared':return current
        if current.get('objective')!=expected and not current.get('objective','').startswith(expected+'\n\n'):raise ValueError('The native goal changed. No native goal was modified.')
        if expected_basis and current.get('native_basis')!=expected_basis:raise ValueError('The native goal criteria changed. No native goal was modified.')
        return goal_state(host.call('session.control',session_id=ident,action='goal.pause' if action=='pause' else 'goal.clear').get('control'))
    finally:host.close()


def run(command,cwd,env,prompt,native_id,model,effort,update,execution):
    from workspace_native_io import channel
    from workspace_native_requests import provider,notice
    from workspace_interactions import question,answers_for
    from workspace_execution import Stopped
    from _process_errors import ErrorTail
    from workspace_delegation import Tracker
    delegation=Tracker(lambda **values:update(**values))
    launch=connection(command,execution.native_options)
    if not launch:raise ValueError('This Hermes installation does not expose its native gateway. Update Hermes or configure its gateway command.')
    argv,root=launch
    if root:env={**env,'PYTHONPATH':os.pathsep.join([root,env.get('PYTHONPATH','')])}
    if execution.permission=='yolo':env={**env,'HERMES_YOLO_MODE':'1'}
    session=execution.native_session;runtime=None;stored=native_id;final='';usage={};goal=execution.native_goal;verdict=None;ended=False;setup=[];aliases=0;goal_prompt=None;children=set();active_children=0
    # Native counters cover the whole session, including autonomous goal turns.
    # Unknown resumed counters stay unknown until a baseline is available.
    baseline={} if native_id else {'input_tokens':0,'output_tokens':0};totals=dict(baseline);route={}
    with execution.popen(argv,cwd=cwd,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace') as process:
        errors=ErrorTail(process,env);send,events,close=channel(process,execution,errors)
        def request(ident,method,**params):send({'jsonrpc':'2.0','id':ident,'method':method,'params':params})
        def observe_control(control,bound=False):
            nonlocal verdict
            verdict=goal_state(control)
            if session:
                session.goal_active=verdict['status']=='active'
                session.native_work=any((control.get(key) or {}).get('status')=='active' for key in ('loop','heartbeat'))
            if goal and (bound or 'native_objective' in goal):update(native_goal={**verdict,**({'bound_to':goal['objective']} if bound else {})})
        def controls():
            owner=execution
            def current():
                if session and (not session.active or session.active.execution is not owner):raise ValueError('This request has ended. Send a new message instead.')
            def interrupt():
                current();request('aura-interrupt','session.interrupt',session_id=runtime)
            def steer(text,attachments=None):
                current()
                if attachments:raise ValueError('Attach images to the next message in this connection.')
                execution.control(send,{'jsonrpc':'2.0','method':'prompt.submit','params':{'session_id':runtime,'text':text}})
            def goal_control(action):
                execution.control(send,{'jsonrpc':'2.0','method':'session.control','params':{'session_id':runtime,'action':'goal.clear' if action in {'clear','complete'} else 'goal.pause'}})
            execution.interrupt=interrupt;execution.steer=steer;execution.goal_control=goal_control
            update(native_controls={'steer':True,'interrupt':True})
        def submit():
            nonlocal goal
            goal=execution.native_goal
            text='/goal '+goal['objective'] if goal else prompt
            if text.lstrip().startswith('/'):
                request('aura-command','slash.exec',session_id=runtime,command=text.strip())
            else:request('aura-prompt','prompt.submit',session_id=runtime,text=text)
        def prepare():
            if setup:
                method,params=setup.pop(0);request('aura-setup',method,session_id=runtime,**params)
            else:submit()
        def incoming(event):
            nonlocal final,usage,verdict,ended,stored,active_children,totals
            method=event.get('method');params=event.get('params') or {};ident=event.get('id')
            if execution.resolve_control(ident,(event.get('error') or {}).get('message')):
                value=(event.get('result') or {}).get('control')
                if value:observe_control(value)
                return
            if method and ident is not None:
                if params.get('session_id') not in {None,runtime}:
                    send({'id':ident,'error':{'code':-32602,'message':'This request belongs to another conversation.'}});return
                def reply(value):send({'jsonrpc':'2.0','id':ident,'result':value})
                if method=='approval':
                    choices=params.get('choices') or ['once','deny'];q=question('choice',params.get('description') or 'Allow this native operation?',choices)
                    execution.requests.add(ident,'Approval needed',[q],reply,lambda a:{'choice':answers_for([q],a)['choice'][0]},params.get('command',''))
                elif method=='clarify':
                    qs=[question(q['qid'],q['question'],q.get('choices') or [],multiple=q.get('multi_select',False),free=not q.get('choices')) for q in params.get('questions',[])]
                    execution.requests.add(ident,'Hermes needs your input',qs,reply,lambda a:{'answers':{k:(', '.join(v) if v else None) for k,v in answers_for(qs,a).items()}})
                elif method in {'sudo','secret'}:
                    q=question('value',params.get('prompt') or params.get('command') or 'Enter the requested value.',[],free=True);q['secret']=True
                    execution.requests.add(ident,'Hermes needs your input',[q],reply,lambda a:{'value':answers_for([q],a)['value'][0] if answers_for([q],a)['value'] else ''})
                elif not provider(execution,event,send,update):
                    send({'jsonrpc':'2.0','id':ident,'error':{'code':-32601,'message':'This interaction needs its native provider.'}})
                    notice(execution,update,'This native step needs a connected service. Check this connection’s setup.')
                    update(native_diagnostic={'method':method,'reason':'Native provider required'})
                return
            if method!='event':return
            if params.get('session_id') not in {None,runtime}:return
            if getattr(execution,'trace',None):execution.trace.observe('hermes',event,runtime)
            typ=params.get('type');p=params.get('payload') or {}
            if typ.startswith('subagent.'):
                delegation.observe('hermes',{'type':typ,'payload':p})
            if typ=='message.start':final='';update(reply='')
            elif typ=='message.delta':final+=p.get('text','');update(reply=final)
            elif typ=='message.complete':
                if p.get('status') in {'error','interrupted'}:raise Stopped() if execution.interrupt_requested else ValueError(p.get('error') or 'Hermes could not finish this request.')
                final=p.get('text') or final
                from workspace_usage import number
                native_usage=p.get('usage') or {}
                active_children=native_usage.get('active_subagents',0)
                if session:session.background=bool(children or active_children)
                totals=tokens(native_usage)
                for key,value in totals.items():
                    if key in baseline and value<baseline[key]:baseline[key]=0
                usage={key:value-baseline[key] for key,value in totals.items() if key in baseline}
                if number(native_usage.get('context_used')) is not None:
                    usage['context']={'tokens':native_usage['context_used'],**({'window':native_usage['context_max']} if number(native_usage.get('context_max')) else {})}
                if native_usage.get('cost_usd') is not None:usage.update(session_cost_usd=native_usage['cost_usd'],cost_kind='reported')
                ended=True
                update(reply=final,reply_ready=True)
                request('aura-goal-status','session.control.read',session_id=runtime)
            elif typ=='session.control.update':
                observe_control(p.get('control') or p)
            elif typ=='session.info':
                if p.get('stored_session_id') and stored and p['stored_session_id']!=stored:raise ValueError('Hermes changed the saved conversation identity. Check its native chat before continuing.')
                if p.get('title'):update(native_title=p['title'])
                if isinstance(p.get('usage'),dict) and 'active_subagents' in p['usage']:
                    active_children=p['usage']['active_subagents']
                    if session:session.background=bool(children or active_children)
            elif typ=='request.cancel':execution.requests.resolve(p.get('request_id') or p.get('id'))
            elif typ=='status.update':
                text=p.get('text') or 'Hermes is working'
                if 'Auxiliary title generation failed' in text:
                    update(native_diagnostic={'method':'hermes/title','reason':text})
                elif re.search(r'Traceback|\b(?:ValueError|TypeError|TemplateError)\b|HTTP [45]\d\d.*[{}<]',text):
                    update(native_diagnostic={'method':'hermes/status','reason':text})
                    notice(execution,update,'Hermes reported a connection problem. Check its settings if your work cannot continue.')
                else:update(progress=text)
            elif typ=='error':raise ValueError(p.get('message') or 'Hermes needs attention.')
            elif typ=='notice':notice(execution,update,p.get('message',''))
            elif typ=='tool.start':update(progress='Using '+str(p.get('name') or 'a native tool'),native_tool=p.get('name'))
            elif typ=='tool.complete':update(progress='Native tool finished')
            elif typ in {'subagent.spawn_requested','subagent.start','subagent.complete'}:
                ident=p.get('subagent_id') or p.get('child_session_id') or p.get('delegation_id')
                if ident:
                    if typ=='subagent.complete':children.discard(ident)
                    else:children.add(ident)
                    if session:session.background=bool(children or active_children)
        try:
            for event in events:
                ident=event.get('id');p=event.get('params') or {};result=event.get('result') or {}
                if execution.resolve_control(ident,(event.get('error') or {}).get('message')):
                    if result.get('control'):
                        observe_control(result['control'])
                    continue
                if ident in {'aura-models','aura-session','aura-command','aura-prompt','aura-goal-status','aura-bound-goal','aura-setup','aura-initial-goal','aura-client'} and event.get('error'):raise ValueError(event['error'].get('message') or 'Hermes could not complete this operation.')
                if event.get('method')=='event' and p.get('type')=='gateway.ready':
                    handler=execution.native_handler or {}
                    if not isinstance(handler,dict):raise ValueError('Native provider configuration must be an object.')
                    extra=handler.get('methods',[])
                    if not isinstance(extra,list) or not all(isinstance(v,str) and v for v in extra):raise ValueError('Native provider methods must be a list of names.')
                    request('aura-client','client.capabilities',server_requests=list(dict.fromkeys(['approval','clarify','sudo','secret',*extra])))
                    request('aura-models','model.options',explicit_only=True,**{k:v for k,v in session_options(execution.native_options).items() if k=='profile'})
                elif ident=='aura-models':
                    route=model_route(result,model)
                    request('aura-session','session.resume' if native_id else 'session.create',**({'session_id':native_id,'omit_messages':True} if native_id else {'cwd':str(cwd),'cwd_explicit':True,**route}),**session_options(execution.native_options))
                elif ident=='aura-session':
                    runtime=result.get('session_id');stored=result.get('stored_session_id') or result.get('session_key') or (result.get('info') or {}).get('stored_session_id')
                    if not runtime or not stored or native_id and stored!=native_id:raise ValueError('Hermes did not confirm the requested saved conversation. No message was sent.')
                    if native_id:
                        info=result.get('info') or {};baseline=tokens(info.get('usage') or {})
                        # A cold, lazy resume has not built its agent yet. Its new
                        # runtime counters start at zero, not at saved lifetime use.
                        if not baseline and info.get('lazy') is True:baseline={'input_tokens':0,'output_tokens':0}
                        totals=dict(baseline)
                    update(native_id=stored);execution.protocol_ready=True;controls()
                    info=result.get('info') or {};current=info.get('model','')
                    same_model=model==current or route.get('model')==current and route.get('provider')==info.get('provider')
                    # Create takes structured fields; /model uses native command
                    # syntax. Explicit provider flags also bypass a broken default.
                    if native_id and model and (not same_model or getattr(execution,'native_model_changed',False)):
                        setup.append(('config.set',{'key':'model','value':shlex.join([route['model'],'--provider',route['provider']]),'scope':'session','confirm_expensive_model':True}))
                    if effort:setup.append(('config.set',{'key':'reasoning','value':effort,'scope':'session'}))
                    setup.extend(('image.attach_bytes',{'data':img['data']}) for img in execution.attachments)
                    request('aura-commands','commands.catalog',session_id=runtime)
                    request('aura-initial-goal','session.control.read',session_id=runtime)
                elif ident=='aura-initial-goal':
                    current=goal_state(result.get('control'))
                    expected=(goal or {}).get('native_objective',(goal or {}).get('objective',''))
                    if goal and current.get('objective') and current['objective']!=expected and not current['objective'].startswith(expected+'\n\n'):raise ValueError('Hermes has a different goal in this chat. Review that goal before replacing it.')
                    if goal and current['status']!='cleared' and goal.get('native_basis') and current.get('native_basis')!=goal['native_basis']:raise ValueError('The native goal criteria changed. Review that goal before continuing.')
                    prepare()
                elif ident=='aura-setup':prepare()
                elif ident=='aura-commands':update(native_commands=[{'name':r[0].lstrip('/'),'description':r[1]} for r in result.get('pairs',[]) if len(r)>1])
                elif ident=='aura-command':
                    if result.get('type') in {'send','skill'}:
                        if goal:
                            goal_prompt=result.get('message') or ''
                            request('aura-bound-goal','session.control.read',session_id=runtime)
                        else:request('aura-prompt','prompt.submit',session_id=runtime,text=result.get('message') or '')
                    elif result.get('type')=='prefill':
                        final=result.get('display') or result.get('notice') or 'Draft prepared.';ended=True;update(native_editor={'id':'hermes-command','text':result.get('message') or ''},reply=final)
                        request('aura-goal-status','session.control.read',session_id=runtime)
                    elif result.get('type')=='alias':
                        aliases+=1
                        if aliases>8:raise ValueError('Hermes returned a circular command alias. Check the command in its settings.')
                        target=str(result.get('target') or '').lstrip('/').split(None,1)
                        if not target:raise ValueError('Hermes returned an empty command alias.')
                        request('aura-command','slash.exec',session_id=runtime,command='/'+ ' '.join(target))
                    else:
                        final=result.get('output') or result.get('notice') or result.get('message') or 'Command completed.';ended=True;update(reply=final)
                        request('aura-goal-status','session.control.read',session_id=runtime)
                elif ident=='aura-goal-status':
                    observe_control(result.get('control') or {})
                elif ident=='aura-bound-goal':
                    verdict=goal_state(result.get('control'))
                    if verdict['status']!='active':raise ValueError('Hermes did not activate the native goal. No work prompt was sent.')
                    goal['native_objective']=verdict.get('objective','');goal['native_basis']=verdict.get('native_basis')
                    observe_control(result.get('control') or {},bound=True)
                    request('aura-prompt','prompt.submit',session_id=runtime,text=prompt+'\n\n'+goal_prompt)
                else:incoming(event)
                if ended and verdict and verdict['status']!='active' and not children and not active_children and not execution.helpers and not any(r['status']=='pending' for r in execution.requests.snapshot()):
                    output={'reply':final or 'Native request completed.','native_id':stored,'usage':usage}
                    if not session:return output
                    call=session.next(output,events,incoming)
                    baseline=dict(totals)
                    execution=call.execution;update=call.update;prompt=call.prompt;goal=execution.native_goal;final='';usage={};verdict=None;ended=False;aliases=0
                    setup.extend(('image.attach_bytes',{'data':img['data']}) for img in execution.attachments)
                    execution.protocol_ready=True;update(native_id=stored);controls();prepare()
            raise ValueError(errors.message('The Hermes connection ended. Your request was not resent.'))
        finally:
            execution.interrupt=None;execution.steer=None;execution.goal_control=None;execution.close_controls();execution.requests.close();close();errors.close_input(process)
            try:process.wait(timeout=3)
            except subprocess.TimeoutExpired:execution._force_stop();process.wait(timeout=5)
